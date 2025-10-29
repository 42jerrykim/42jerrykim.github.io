---
draft: true
---
# 4장. 모던 아키텍처 패러다임

## 학습 목표
- 마이크로서비스 아키텍처의 핵심 개념과 구현 방법을 이해한다
- 서버리스 아키텍처의 특징과 적용 시나리오를 파악한다
- 헥사고날 아키텍처의 설계 원칙과 구현 기법을 습득한다
- CQRS와 이벤트 소싱의 개념과 실무 적용 방법을 학습한다

---

## 마이크로서비스 아키텍처

### 마이크로서비스란?

마이크로서비스 아키텍처는 하나의 큰 애플리케이션을 여러 개의 작고 독립적인 서비스로 분해하는 접근 방식입니다.

#### 핵심 특징
- **서비스 자율성**: 각 서비스는 독립적으로 개발, 배포, 확장 가능
- **비즈니스 중심 분해**: 도메인 기반으로 서비스 경계 설정
- **분산 데이터 관리**: 서비스별 독립적인 데이터베이스
- **API 기반 통신**: REST API, GraphQL, gRPC 등을 통한 통신

### 모놀리스 vs 마이크로서비스

| **측면** | **모놀리스** | **마이크로서비스** |
|---------|-------------|------------------|
| **배포** | 전체 애플리케이션 단위 | 서비스별 독립 배포 |
| **확장성** | 수직 확장 중심 | 서비스별 수평 확장 |
| **기술 스택** | 단일 기술 스택 | 서비스별 최적 기술 선택 |
| **장애 영향도** | 전체 시스템 중단 | 특정 서비스만 영향 |
| **팀 구조** | 기능별 팀 | 서비스별 전담 팀 |

### 마이크로서비스 구현 예제

#### 주문 서비스 예제

```java
// OrderController.java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @Autowired
    private OrderService orderService;
    
    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        try {
            Order order = orderService.createOrder(request);
            return ResponseEntity.ok(new OrderResponse(order));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new OrderResponse("주문 생성 실패: " + e.getMessage()));
        }
    }
    
    @GetMapping("/{orderId}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable String orderId) {
        Optional<Order> order = orderService.findById(orderId);
        return order.map(o -> ResponseEntity.ok(new OrderResponse(o)))
                   .orElse(ResponseEntity.notFound().build());
    }
}

// OrderService.java
@Service
@Transactional
public class OrderService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    
    @Autowired
    private InventoryServiceClient inventoryServiceClient;
    
    public Order createOrder(CreateOrderRequest request) {
        // 1. 재고 확인
        if (!inventoryServiceClient.checkAvailability(request.getProductId(), request.getQuantity())) {
            throw new RuntimeException("재고 부족");
        }
        
        // 2. 주문 생성
        Order order = new Order(
            UUID.randomUUID().toString(),
            request.getCustomerId(),
            request.getProductId(),
            request.getQuantity(),
            request.getPrice(),
            OrderStatus.PENDING
        );
        
        orderRepository.save(order);
        
        // 3. 결제 처리 (비동기)
        CompletableFuture.runAsync(() -> {
            try {
                PaymentResult result = paymentServiceClient.processPayment(
                    order.getId(), order.getTotalAmount()
                );
                
                if (result.isSuccess()) {
                    updateOrderStatus(order.getId(), OrderStatus.CONFIRMED);
                } else {
                    updateOrderStatus(order.getId(), OrderStatus.FAILED);
                }
            } catch (Exception e) {
                updateOrderStatus(order.getId(), OrderStatus.FAILED);
            }
        });
        
        return order;
    }
    
    private void updateOrderStatus(String orderId, OrderStatus status) {
        orderRepository.findById(orderId).ifPresent(order -> {
            order.setStatus(status);
            orderRepository.save(order);
            
            // 주문 상태 변경 이벤트 발행
            eventPublisher.publishEvent(new OrderStatusChangedEvent(orderId, status));
        });
    }
}
```

#### 서비스 간 통신 - Feign Client

```java
// PaymentServiceClient.java
@FeignClient(name = "payment-service", url = "${payment.service.url}")
public interface PaymentServiceClient {
    
    @PostMapping("/api/payments")
    PaymentResult processPayment(@RequestBody PaymentRequest request);
    
    @GetMapping("/api/payments/{paymentId}")
    PaymentStatus getPaymentStatus(@PathVariable String paymentId);
}

// Circuit Breaker 적용
@Component
public class PaymentServiceClientImpl {
    
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    
    @CircuitBreaker(name = "payment-service", fallbackMethod = "fallbackPayment")
    public PaymentResult processPayment(String orderId, BigDecimal amount) {
        return paymentServiceClient.processPayment(
            new PaymentRequest(orderId, amount)
        );
    }
    
    public PaymentResult fallbackPayment(String orderId, BigDecimal amount, Exception ex) {
        // 장애 상황에서의 대안 처리
        return PaymentResult.failed("결제 서비스 일시 중단");
    }
}
```

### 마이크로서비스의 장점과 단점

#### 장점
- **독립적 배포**: 서비스별 독립적인 릴리즈 사이클
- **기술 다양성**: 서비스별 최적 기술 스택 선택 가능
- **확장성**: 트래픽에 따른 서비스별 확장
- **장애 격리**: 부분 장애가 전체 시스템에 미치는 영향 최소화

#### 단점
- **복잡성 증가**: 분산 시스템의 복잡성
- **네트워크 통신**: 서비스 간 네트워크 지연과 실패 가능성
- **데이터 일관성**: 분산 트랜잭션 관리의 어려움
- **운영 복잡성**: 여러 서비스의 모니터링과 디버깅

---

## 서버리스 아키텍처

### 서버리스란?

서버리스(Serverless)는 개발자가 서버 관리에 신경 쓰지 않고 코드 실행에만 집중할 수 있는 클라우드 컴퓨팅 모델입니다.

#### 핵심 특징
- **Function as a Service (FaaS)**: 함수 단위의 실행 환경
- **이벤트 기반**: 이벤트 발생 시에만 실행
- **자동 스케일링**: 요청량에 따른 자동 확장/축소
- **종량제 과금**: 실행 시간과 리소스 사용량에 따른 과금

### 서버리스 vs 전통적 서버

| **측면** | **전통적 서버** | **서버리스** |
|---------|---------------|-------------|
| **서버 관리** | 직접 관리 필요 | 클라우드 제공자가 관리 |
| **확장성** | 수동 스케일링 | 자동 스케일링 |
| **비용** | 고정 비용 | 사용량 기반 비용 |
| **개발 집중도** | 인프라 + 코드 | 코드에만 집중 |
| **콜드 스타트** | 없음 | 초기 지연 발생 가능 |

### 서버리스 구현 예제

#### AWS Lambda 함수 예제

```java
// OrderProcessor.java
public class OrderProcessor implements RequestHandler<OrderEvent, OrderResult> {
    
    private final DynamoDB dynamoDB = DynamoDBBuilder.standard().build();
    private final SQS sqs = SQSBuilder.standard().build();
    
    @Override
    public OrderResult handleRequest(OrderEvent event, Context context) {
        LambdaLogger logger = context.getLogger();
        logger.log("주문 처리 시작: " + event.getOrderId());
        
        try {
            // 1. 주문 정보 조회
            Order order = getOrderFromDynamoDB(event.getOrderId());
            
            // 2. 재고 확인
            if (!checkInventory(order)) {
                return OrderResult.failure("재고 부족");
            }
            
            // 3. 결제 처리
            PaymentResult paymentResult = processPayment(order);
            if (!paymentResult.isSuccess()) {
                return OrderResult.failure("결제 실패");
            }
            
            // 4. 주문 상태 업데이트
            updateOrderStatus(order.getId(), "CONFIRMED");
            
            // 5. 배송 큐에 메시지 전송
            sendToShippingQueue(order);
            
            logger.log("주문 처리 완료: " + event.getOrderId());
            return OrderResult.success();
            
        } catch (Exception e) {
            logger.log("주문 처리 실패: " + e.getMessage());
            return OrderResult.failure(e.getMessage());
        }
    }
    
    private Order getOrderFromDynamoDB(String orderId) {
        // DynamoDB에서 주문 정보 조회
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("orderId", new AttributeValue(orderId));
        
        GetItemRequest request = GetItemRequest.builder()
            .tableName("Orders")
            .key(key)
            .build();
            
        GetItemResponse response = dynamoDB.getItem(request);
        return mapToOrder(response.item());
    }
    
    private void sendToShippingQueue(Order order) {
        // SQS에 배송 메시지 전송
        String messageBody = objectMapper.writeValueAsString(
            new ShippingMessage(order.getId(), order.getCustomerId(), order.getAddress())
        );
        
        SendMessageRequest request = SendMessageRequest.builder()
            .queueUrl("https://sqs.region.amazonaws.com/account/shipping-queue")
            .messageBody(messageBody)
            .build();
            
        sqs.sendMessage(request);
    }
}
```

#### 이벤트 기반 서버리스 아키텍처

```yaml
# serverless.yml (Serverless Framework)
service: order-processing

provider:
  name: aws
  runtime: java11
  stage: ${opt:stage, 'dev'}
  region: ap-northeast-2

functions:
  processOrder:
    handler: com.example.OrderProcessor
    events:
      - sqs:
          arn: arn:aws:sqs:ap-northeast-2:123456789:order-queue
          batchSize: 10
    environment:
      ORDERS_TABLE: ${self:service}-orders-${self:provider.stage}
      SHIPPING_QUEUE_URL: ${cf:shipping-service-${self:provider.stage}.ShippingQueueUrl}

  processPayment:
    handler: com.example.PaymentProcessor
    events:
      - http:
          path: /payments
          method: post
          cors: true

resources:
  Resources:
    OrdersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-orders-${self:provider.stage}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: orderId
            AttributeType: S
        KeySchema:
          - AttributeName: orderId
            KeyType: HASH
```

### 서버리스 패턴

#### Event-Driven 패턴
```java
// 이벤트 기반 주문 처리 플로우
@Component
public class OrderEventHandler {
    
    // 주문 생성 이벤트 처리
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 재고 확인 함수 호출
        inventoryService.reserveItems(event.getOrderId(), event.getItems());
    }
    
    // 재고 예약 완료 이벤트 처리
    @EventListener
    public void handleInventoryReserved(InventoryReservedEvent event) {
        // 결제 처리 함수 호출
        paymentService.processPayment(event.getOrderId(), event.getAmount());
    }
    
    // 결제 완료 이벤트 처리
    @EventListener
    public void handlePaymentCompleted(PaymentCompletedEvent event) {
        // 배송 처리 함수 호출
        shippingService.createShipment(event.getOrderId());
    }
}
```

---

## 헥사고날 아키텍처 (포트와 어댑터)

### 헥사고날 아키텍처란?

헥사고날 아키텍처는 애플리케이션의 핵심 비즈니스 로직을 외부 세계로부터 격리하여 테스트 가능하고 유지보수하기 쉬운 구조를 만드는 아키텍처 패턴입니다.

#### 핵심 개념
- **포트(Port)**: 애플리케이션이 외부와 상호작용하는 인터페이스
- **어댑터(Adapter)**: 포트를 구현하여 실제 외부 시스템과 연결
- **도메인 중심**: 비즈니스 로직이 중심에 위치
- **의존성 역전**: 외부 의존성이 내부로 향하지 않음

### 계층 구조

```
┌─────────────────────────────────────┐
│           Adapters                  │  ← 외부 인터페이스
├─────────────────────────────────────┤
│           Ports                     │  ← 인터페이스 정의
├─────────────────────────────────────┤
│        Application Services         │  ← 애플리케이션 로직
├─────────────────────────────────────┤
│         Domain Model                │  ← 핵심 비즈니스 로직
└─────────────────────────────────────┘
```

### 헥사고날 아키텍처 구현 예제

#### 도메인 모델
```java
// Order.java (도메인 엔티티)
public class Order {
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderItem> items;
    private OrderStatus status;
    private final LocalDateTime createdAt;
    
    public Order(CustomerId customerId, List<OrderItem> items) {
        this.id = OrderId.generate();
        this.customerId = customerId;
        this.items = new ArrayList<>(items);
        this.status = OrderStatus.PENDING;
        this.createdAt = LocalDateTime.now();
        
        validateOrder();
    }
    
    private void validateOrder() {
        if (items.isEmpty()) {
            throw new IllegalArgumentException("주문 항목이 없습니다");
        }
        
        if (getTotalAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("주문 금액이 올바르지 않습니다");
        }
    }
    
    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("대기 중인 주문만 확인할 수 있습니다");
        }
        this.status = OrderStatus.CONFIRMED;
    }
    
    public BigDecimal getTotalAmount() {
        return items.stream()
                   .map(OrderItem::getAmount)
                   .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    // getters...
}

// OrderItem.java (값 객체)
public class OrderItem {
    private final ProductId productId;
    private final int quantity;
    private final BigDecimal unitPrice;
    
    public OrderItem(ProductId productId, int quantity, BigDecimal unitPrice) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("수량은 0보다 커야 합니다");
        }
        if (unitPrice.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("가격은 0보다 커야 합니다");
        }
        
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }
    
    public BigDecimal getAmount() {
        return unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
    
    // getters...
}
```

#### 포트 정의
```java
// OrderRepository.java (출력 포트)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
    List<Order> findByCustomerId(CustomerId customerId);
}

// PaymentService.java (출력 포트)
public interface PaymentService {
    PaymentResult processPayment(OrderId orderId, BigDecimal amount);
}

// OrderService.java (입력 포트)
public interface OrderService {
    OrderId createOrder(CreateOrderCommand command);
    void confirmOrder(OrderId orderId);
    Order getOrder(OrderId orderId);
}
```

#### 애플리케이션 서비스
```java
// OrderServiceImpl.java (입력 포트 구현)
@Service
@Transactional
public class OrderServiceImpl implements OrderService {
    
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final EventPublisher eventPublisher;
    
    public OrderServiceImpl(OrderRepository orderRepository,
                           PaymentService paymentService,
                           InventoryService inventoryService,
                           EventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
        this.eventPublisher = eventPublisher;
    }
    
    @Override
    public OrderId createOrder(CreateOrderCommand command) {
        // 1. 재고 확인
        for (OrderItemCommand item : command.getItems()) {
            if (!inventoryService.isAvailable(item.getProductId(), item.getQuantity())) {
                throw new InsufficientInventoryException("재고가 부족합니다: " + item.getProductId());
            }
        }
        
        // 2. 주문 생성
        List<OrderItem> orderItems = command.getItems().stream()
                .map(item -> new OrderItem(item.getProductId(), item.getQuantity(), item.getUnitPrice()))
                .collect(Collectors.toList());
                
        Order order = new Order(command.getCustomerId(), orderItems);
        
        // 3. 주문 저장
        orderRepository.save(order);
        
        // 4. 이벤트 발행
        eventPublisher.publish(new OrderCreatedEvent(order.getId(), order.getCustomerId()));
        
        return order.getId();
    }
    
    @Override
    public void confirmOrder(OrderId orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("주문을 찾을 수 없습니다: " + orderId));
        
        // 결제 처리
        PaymentResult paymentResult = paymentService.processPayment(orderId, order.getTotalAmount());
        
        if (paymentResult.isSuccess()) {
            order.confirm();
            orderRepository.save(order);
            
            eventPublisher.publish(new OrderConfirmedEvent(orderId));
        } else {
            throw new PaymentFailedException("결제 처리 실패: " + paymentResult.getErrorMessage());
        }
    }
    
    @Override
    public Order getOrder(OrderId orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("주문을 찾을 수 없습니다: " + orderId));
    }
}
```

#### 어댑터 구현
```java
// JpaOrderRepository.java (출력 어댑터)
@Repository
public class JpaOrderRepository implements OrderRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public void save(Order order) {
        OrderEntity entity = OrderMapper.toEntity(order);
        entityManager.merge(entity);
    }
    
    @Override
    public Optional<Order> findById(OrderId id) {
        OrderEntity entity = entityManager.find(OrderEntity.class, id.getValue());
        return Optional.ofNullable(entity)
                      .map(OrderMapper::toDomain);
    }
    
    @Override
    public List<Order> findByCustomerId(CustomerId customerId) {
        TypedQuery<OrderEntity> query = entityManager.createQuery(
            "SELECT o FROM OrderEntity o WHERE o.customerId = :customerId", 
            OrderEntity.class
        );
        query.setParameter("customerId", customerId.getValue());
        
        return query.getResultList().stream()
                   .map(OrderMapper::toDomain)
                   .collect(Collectors.toList());
    }
}

// RestOrderController.java (입력 어댑터)
@RestController
@RequestMapping("/api/orders")
public class RestOrderController {
    
    private final OrderService orderService;
    
    public RestOrderController(OrderService orderService) {
        this.orderService = orderService;
    }
    
    @PostMapping
    public ResponseEntity<CreateOrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        try {
            CreateOrderCommand command = new CreateOrderCommand(
                CustomerId.of(request.getCustomerId()),
                request.getItems().stream()
                    .map(item -> new OrderItemCommand(
                        ProductId.of(item.getProductId()),
                        item.getQuantity(),
                        item.getUnitPrice()
                    ))
                    .collect(Collectors.toList())
            );
            
            OrderId orderId = orderService.createOrder(command);
            
            return ResponseEntity.ok(new CreateOrderResponse(orderId.getValue()));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(new CreateOrderResponse(null, e.getMessage()));
        }
    }
    
    @PostMapping("/{orderId}/confirm")
    public ResponseEntity<Void> confirmOrder(@PathVariable String orderId) {
        try {
            orderService.confirmOrder(OrderId.of(orderId));
            return ResponseEntity.ok().build();
        } catch (OrderNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}
```

---

## CQRS와 이벤트 소싱

### CQRS (Command Query Responsibility Segregation)

CQRS는 명령(Command)과 조회(Query)의 책임을 분리하는 패턴으로, 읽기와 쓰기 모델을 각각 최적화할 수 있습니다.

#### 핵심 개념
- **명령 모델**: 데이터 변경 작업 담당
- **조회 모델**: 데이터 읽기 작업 담당
- **모델 분리**: 각각 다른 데이터 구조와 최적화
- **eventual Consistency**: 읽기 모델의 비동기 업데이트

### 이벤트 소싱 (Event Sourcing)

이벤트 소싱은 애플리케이션의 상태 변경을 이벤트 스트림으로 저장하는 패턴입니다.

#### 핵심 개념
- **이벤트 스트림**: 모든 변경사항을 순차적 이벤트로 저장
- **이벤트 재생**: 이벤트를 순서대로 재생하여 현재 상태 복원
- **시간 여행**: 과거 임의 시점의 상태 조회 가능
- **감사 추적**: 완전한 변경 이력 보존

### CQRS + 이벤트 소싱 구현 예제

#### 이벤트 정의
```java
// OrderEvent.java (기본 이벤트)
public abstract class OrderEvent {
    private final String orderId;
    private final LocalDateTime occurredAt;
    private final String eventId;
    
    protected OrderEvent(String orderId) {
        this.orderId = orderId;
        this.occurredAt = LocalDateTime.now();
        this.eventId = UUID.randomUUID().toString();
    }
    
    // getters...
}

// OrderCreatedEvent.java
public class OrderCreatedEvent extends OrderEvent {
    private final String customerId;
    private final List<OrderItem> items;
    private final BigDecimal totalAmount;
    
    public OrderCreatedEvent(String orderId, String customerId, 
                           List<OrderItem> items, BigDecimal totalAmount) {
        super(orderId);
        this.customerId = customerId;
        this.items = items;
        this.totalAmount = totalAmount;
    }
    
    // getters...
}

// OrderConfirmedEvent.java
public class OrderConfirmedEvent extends OrderEvent {
    private final String paymentId;
    private final LocalDateTime confirmedAt;
    
    public OrderConfirmedEvent(String orderId, String paymentId) {
        super(orderId);
        this.paymentId = paymentId;
        this.confirmedAt = LocalDateTime.now();
    }
    
    // getters...
}
```

#### 명령 처리 (Command Side)
```java
// OrderAggregate.java
public class OrderAggregate {
    private String id;
    private String customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private BigDecimal totalAmount;
    private List<OrderEvent> uncommittedEvents = new ArrayList<>();
    
    // 생성자 - 이벤트 재생을 통한 상태 복원
    public OrderAggregate(List<OrderEvent> events) {
        for (OrderEvent event : events) {
            apply(event);
        }
    }
    
    // 새 주문 생성
    public static OrderAggregate createOrder(String customerId, List<OrderItem> items) {
        OrderAggregate aggregate = new OrderAggregate(Collections.emptyList());
        
        String orderId = UUID.randomUUID().toString();
        BigDecimal totalAmount = items.stream()
                .map(OrderItem::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        OrderCreatedEvent event = new OrderCreatedEvent(orderId, customerId, items, totalAmount);
        aggregate.applyAndRecord(event);
        
        return aggregate;
    }
    
    // 주문 확인
    public void confirmOrder(String paymentId) {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("대기 중인 주문만 확인할 수 있습니다");
        }
        
        OrderConfirmedEvent event = new OrderConfirmedEvent(id, paymentId);
        applyAndRecord(event);
    }
    
    // 이벤트 적용 및 기록
    private void applyAndRecord(OrderEvent event) {
        apply(event);
        uncommittedEvents.add(event);
    }
    
    // 이벤트 적용 (상태 변경)
    private void apply(OrderEvent event) {
        if (event instanceof OrderCreatedEvent) {
            apply((OrderCreatedEvent) event);
        } else if (event instanceof OrderConfirmedEvent) {
            apply((OrderConfirmedEvent) event);
        }
        // 다른 이벤트 타입들...
    }
    
    private void apply(OrderCreatedEvent event) {
        this.id = event.getOrderId();
        this.customerId = event.getCustomerId();
        this.items = new ArrayList<>(event.getItems());
        this.status = OrderStatus.PENDING;
        this.totalAmount = event.getTotalAmount();
    }
    
    private void apply(OrderConfirmedEvent event) {
        this.status = OrderStatus.CONFIRMED;
    }
    
    public List<OrderEvent> getUncommittedEvents() {
        return new ArrayList<>(uncommittedEvents);
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
    
    // getters...
}

// OrderCommandHandler.java
@Service
public class OrderCommandHandler {
    
    private final EventStore eventStore;
    private final EventBus eventBus;
    
    public OrderCommandHandler(EventStore eventStore, EventBus eventBus) {
        this.eventStore = eventStore;
        this.eventBus = eventBus;
    }
    
    @CommandHandler
    public void handle(CreateOrderCommand command) {
        // 새 주문 생성
        OrderAggregate aggregate = OrderAggregate.createOrder(
            command.getCustomerId(),
            command.getItems()
        );
        
        // 이벤트 저장
        eventStore.saveEvents(aggregate.getId(), aggregate.getUncommittedEvents());
        
        // 이벤트 발행
        for (OrderEvent event : aggregate.getUncommittedEvents()) {
            eventBus.publish(event);
        }
        
        aggregate.markEventsAsCommitted();
    }
    
    @CommandHandler
    public void handle(ConfirmOrderCommand command) {
        // 기존 주문 로드
        List<OrderEvent> events = eventStore.getEvents(command.getOrderId());
        OrderAggregate aggregate = new OrderAggregate(events);
        
        // 주문 확인
        aggregate.confirmOrder(command.getPaymentId());
        
        // 이벤트 저장 및 발행
        eventStore.saveEvents(aggregate.getId(), aggregate.getUncommittedEvents());
        
        for (OrderEvent event : aggregate.getUncommittedEvents()) {
            eventBus.publish(event);
        }
        
        aggregate.markEventsAsCommitted();
    }
}
```

#### 조회 처리 (Query Side)
```java
// OrderReadModel.java
@Entity
@Table(name = "order_read_model")
public class OrderReadModel {
    @Id
    private String id;
    private String customerId;
    private String customerName;
    private BigDecimal totalAmount;
    private String status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // constructors, getters, setters...
}

// OrderProjection.java
@Component
public class OrderProjection {
    
    private final OrderReadModelRepository repository;
    
    public OrderProjection(OrderReadModelRepository repository) {
        this.repository = repository;
    }
    
    @EventHandler
    public void on(OrderCreatedEvent event) {
        OrderReadModel readModel = new OrderReadModel();
        readModel.setId(event.getOrderId());
        readModel.setCustomerId(event.getCustomerId());
        readModel.setTotalAmount(event.getTotalAmount());
        readModel.setStatus("PENDING");
        readModel.setCreatedAt(event.getOccurredAt());
        readModel.setUpdatedAt(event.getOccurredAt());
        
        repository.save(readModel);
    }
    
    @EventHandler
    public void on(OrderConfirmedEvent event) {
        repository.findById(event.getOrderId())
                  .ifPresent(readModel -> {
                      readModel.setStatus("CONFIRMED");
                      readModel.setUpdatedAt(event.getOccurredAt());
                      repository.save(readModel);
                  });
    }
}

// OrderQueryService.java
@Service
public class OrderQueryService {
    
    private final OrderReadModelRepository repository;
    
    public OrderQueryService(OrderReadModelRepository repository) {
        this.repository = repository;
    }
    
    public OrderReadModel getOrder(String orderId) {
        return repository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("주문을 찾을 수 없습니다: " + orderId));
    }
    
    public List<OrderReadModel> getOrdersByCustomer(String customerId) {
        return repository.findByCustomerId(customerId);
    }
    
    public Page<OrderReadModel> getOrdersByStatus(String status, Pageable pageable) {
        return repository.findByStatus(status, pageable);
    }
}
```

---

## 핵심 요약

### 모던 아키텍처 패러다임 비교

| **패러다임** | **주요 특징** | **적용 시나리오** | **장점** | **고려사항** |
|-------------|-------------|-----------------|---------|------------|
| **마이크로서비스** | 서비스 분해, 독립 배포 | 대규모 시스템, 다수 팀 | 확장성, 기술 다양성 | 복잡성, 데이터 일관성 |
| **서버리스** | 함수 기반, 이벤트 드리븐 | 이벤트 처리, 간헐적 작업 | 자동 스케일링, 비용 효율 | 벤더 종속, 콜드 스타트 |
| **헥사고날** | 포트-어댑터, 도메인 중심 | 복잡한 비즈니스 로직 | 테스트 용이성, 유연성 | 초기 복잡성, 학습 곡선 |
| **CQRS/ES** | 명령-조회 분리, 이벤트 저장 | 복잡한 도메인, 감사 필요 | 확장성, 감사 추적 | 복잡성, 일관성 관리 |

### 패러다임별 선택 가이드

1. **마이크로서비스**: 조직이 크고, 독립적인 팀 구조, 다양한 기술 스택 필요
2. **서버리스**: 이벤트 기반 처리, 간헐적 워크로드, 빠른 프로토타이핑
3. **헥사고날**: 복잡한 비즈니스 규칙, 높은 테스트 커버리지 필요
4. **CQRS/ES**: 복잡한 도메인, 완전한 감사 추적, 높은 읽기 성능 필요

---

## 생각해보기

1. 현재 진행 중인 프로젝트에 가장 적합한 아키텧처 패러다임은 무엇이며, 그 이유는?
2. 마이크로서비스를 도입할 때 가장 큰 도전과제는 무엇이고, 어떻게 해결할 수 있을까?
3. 이벤트 소싱을 적용하기 적합한 도메인의 특징은 무엇인가?

---

## 추가 학습 자료

### 도서
- "Building Microservices" - Sam Newman
- "Serverless Architectures on AWS" - Peter Sbarski  
- "Clean Architecture" - Robert C. Martin
- "Implementing Domain-Driven Design" - Vaughn Vernon

### 온라인 자료
- Netflix Technology Blog
- AWS Architecture Center
- Microsoft Azure Architecture Center
- Martin Fowler's Architecture Articles 