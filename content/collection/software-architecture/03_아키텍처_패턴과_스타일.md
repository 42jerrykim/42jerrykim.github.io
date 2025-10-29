---
draft: true
---
# 3장. 아키텍처 패턴과 스타일

## 학습 목표
- 주요 아키텍처 패턴의 구조와 동작 원리 이해
- 각 패턴의 장단점과 적용 시나리오 파악
- 패턴 선택을 위한 의사결정 기준 습득
- 실제 시스템에서의 패턴 조합과 변형 방법 학습

---

## 계층화 아키텍처 (Layered Architecture)

계층화 아키텍처는 가장 기본적이고 널리 사용되는 아키텍처 패턴입니다. 시스템을 수직적으로 분리된 계층들로 구성하여 각 계층이 특정 역할과 책임을 가지도록 합니다.

###️ 기본 구조

```
┌─────────────────────────────────────┐
│        Presentation Layer           │ ← UI, 사용자 인터페이스
├─────────────────────────────────────┤
│         Business Layer              │ ← 비즈니스 로직, 도메인 규칙
├─────────────────────────────────────┤
│        Persistence Layer            │ ← 데이터 접근, 저장소 관리
├─────────────────────────────────────┤
│         Database Layer              │ ← 데이터베이스, 파일 시스템
└─────────────────────────────────────┘
```

### 각 계층의 역할

#### **프레젠테이션 계층 (Presentation Layer)**
- 사용자 인터페이스 처리
- 사용자 입력 검증
- 요청/응답 변환
- 세션 관리

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @Autowired
    private OrderService orderService;
    
    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody OrderRequest request) {
        // 입력 데이터 변환
        CreateOrderCommand command = OrderMapper.toCommand(request);
        
        // 비즈니스 계층 호출
        Order order = orderService.createOrder(command);
        
        // 응답 데이터 변환
        OrderResponse response = OrderMapper.toResponse(order);
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        Order order = orderService.findById(id);
        OrderResponse response = OrderMapper.toResponse(order);
        return ResponseEntity.ok(response);
    }
}
```

#### **비즈니스 계층 (Business Layer)**
- 비즈니스 로직 처리
- 트랜잭션 관리
- 유효성 검사
- 도메인 규칙 구현

```java
@Service
@Transactional
public class OrderService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private InventoryService inventoryService;
    
    @Autowired
    private PaymentService paymentService;
    
    public Order createOrder(CreateOrderCommand command) {
        // 1. 비즈니스 규칙 검증
        validateOrderCreation(command);
        
        // 2. 재고 확인
        if (!inventoryService.isAvailable(command.getProductId(), command.getQuantity())) {
            throw new InsufficientStockException();
        }
        
        // 3. 주문 생성
        Order order = new Order(command.getCustomerId(), command.getProductId(), command.getQuantity());
        
        // 4. 결제 처리
        PaymentResult paymentResult = paymentService.processPayment(order.getTotalAmount());
        if (!paymentResult.isSuccessful()) {
            throw new PaymentFailedException();
        }
        
        // 5. 주문 저장
        order.confirm();
        Order savedOrder = orderRepository.save(order);
        
        // 6. 재고 차감
        inventoryService.reserveStock(command.getProductId(), command.getQuantity());
        
        return savedOrder;
    }
    
    private void validateOrderCreation(CreateOrderCommand command) {
        if (command.getQuantity() <= 0) {
            throw new InvalidOrderQuantityException();
        }
        if (command.getCustomerId() == null) {
            throw new InvalidCustomerException();
        }
    }
}
```

#### **데이터 접근 계층 (Data Access Layer)**
- 데이터베이스 연산
- 쿼리 실행
- 데이터 매핑
- 트랜잭션 처리

```java
@Repository
public class OrderRepositoryImpl implements OrderRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public Order save(Order order) {
        if (order.getId() == null) {
            entityManager.persist(order);
            return order;
        } else {
            return entityManager.merge(order);
        }
    }
    
    @Override
    public Optional<Order> findById(Long id) {
        Order order = entityManager.find(Order.class, id);
        return Optional.ofNullable(order);
    }
    
    @Override
    public List<Order> findByCustomerId(Long customerId) {
        TypedQuery<Order> query = entityManager.createQuery(
            "SELECT o FROM Order o WHERE o.customerId = :customerId", Order.class);
        query.setParameter("customerId", customerId);
        return query.getResultList();
    }
}
```

### 장점

1. **관심사 분리**: 각 계층이 명확한 책임을 가짐
2. **이해 용이성**: 직관적이고 이해하기 쉬운 구조  
3. **개발 분담**: 계층별로 팀을 나누어 개발 가능
4. **재사용성**: 하위 계층을 여러 상위 계층에서 재사용 가능
5. **테스트 용이성**: 각 계층을 독립적으로 테스트 가능

### 단점

1. **성능 오버헤드**: 계층 간 호출로 인한 성능 저하
2. **변경 전파**: 하위 계층 변경이 상위 계층에 영향
3. **복잡한 비즈니스 로직**: 여러 계층에 걸친 복잡한 로직 처리 어려움
4. **단일 장애점**: 하위 계층 장애가 전체 시스템에 영향

---

## 클라이언트-서버 아키텍처

클라이언트-서버 아키텍처는 분산 시스템의 기본 패턴으로, 서비스를 요청하는 클라이언트와 서비스를 제공하는 서버로 구성됩니다.

###️ 기본 구조

```
┌─────────────┐    Request     ┌─────────────┐
│   Client    │ ──────────→    │   Server    │
│             │                │             │
│ - UI Logic  │ ←──────────    │ - Business  │
│ - Validation│    Response    │   Logic     │
│             │                │ - Data      │
└─────────────┘                │   Access    │
                               └─────────────┘
```

### 2-Tier vs 3-Tier vs N-Tier

#### 2-Tier (Client-Database)
```java
// 클라이언트에서 직접 데이터베이스 접근
public class CustomerClient {
    private Connection dbConnection;
    
    public void displayCustomers() {
        String sql = "SELECT * FROM customers";
        PreparedStatement stmt = dbConnection.prepareStatement(sql);
        ResultSet rs = stmt.executeQuery();
        
        // UI에 데이터 표시
        while (rs.next()) {
            System.out.println(rs.getString("name"));
        }
    }
}
```

**장점**: 단순함, 빠른 개발
**단점**: 확장성 부족, 보안 취약, 유지보수 어려움

#### 3-Tier (Client-Application Server-Database)
```java
// 클라이언트
@RestController
public class CustomerController {
    @Autowired
    private CustomerService customerService;
    
    @GetMapping("/customers")
    public List<CustomerDto> getCustomers() {
        return customerService.getAllCustomers();
    }
}

// 애플리케이션 서버
@Service
public class CustomerService {
    @Autowired
    private CustomerRepository customerRepository;
    
    public List<CustomerDto> getAllCustomers() {
        List<Customer> customers = customerRepository.findAll();
        return customers.stream()
            .map(CustomerMapper::toDto)
            .collect(Collectors.toList());
    }
}

// 데이터베이스 계층
@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    List<Customer> findAll();
}
```

**장점**: 비즈니스 로직 분리, 확장성, 보안성
**단점**: 복잡성 증가, 네트워크 지연

### 장점

1. **분산 처리**: 클라이언트와 서버가 독립적으로 실행
2. **확장성**: 서버를 수평적으로 확장 가능
3. **중앙 집중화**: 데이터와 비즈니스 로직의 중앙 관리
4. **보안**: 서버에서 접근 제어와 인증 관리
5. **유지보수**: 서버 로직만 업데이트하면 모든 클라이언트에 적용

### 단점

1. **네트워크 의존성**: 네트워크 장애 시 서비스 불가
2. **단일 장애점**: 서버 장애 시 전체 서비스 중단
3. **트래픽 집중**: 서버에 모든 요청이 집중
4. **지연 시간**: 네트워크 통신으로 인한 지연

---

## 파이프-필터 아키텍처

파이프-필터 아키텍처는 데이터가 일련의 필터를 통해 순차적으로 처리되는 패턴입니다. 각 필터는 데이터를 변환하고, 파이프는 필터 간 데이터 전달을 담당합니다.

###️ 기본 구조

```
Input → Filter1 → Pipe → Filter2 → Pipe → Filter3 → Output
         ↓               ↓                ↓
      Transform      Transform        Transform
```

### 구현 예시

#### Java Stream API를 이용한 구현
```java
public class DataProcessingPipeline {
    
    public List<ProcessedData> processData(List<RawData> rawDataList) {
        return rawDataList.stream()
            .filter(this::validateData)           // Filter 1: 유효성 검사
            .map(this::normalizeData)             // Filter 2: 데이터 정규화
            .map(this::enrichData)                // Filter 3: 데이터 보강
            .filter(this::applyBusinessRules)     // Filter 4: 비즈니스 규칙 적용
            .map(this::transformToOutput)         // Filter 5: 출력 형식 변환
            .collect(Collectors.toList());
    }
    
    private boolean validateData(RawData data) {
        return data != null && 
               data.getId() != null && 
               data.getValue() != null;
    }
    
    private RawData normalizeData(RawData data) {
        // 데이터 정규화 로직
        data.setValue(data.getValue().trim().toLowerCase());
        return data;
    }
    
    private RawData enrichData(RawData data) {
        // 외부 데이터로 보강
        AdditionalInfo info = externalService.getInfo(data.getId());
        data.setAdditionalInfo(info);
        return data;
    }
    
    private boolean applyBusinessRules(RawData data) {
        // 비즈니스 규칙 적용
        return data.getValue().length() > 3 && 
               data.getAdditionalInfo() != null;
    }
    
    private ProcessedData transformToOutput(RawData data) {
        return new ProcessedData(
            data.getId(),
            data.getValue().toUpperCase(),
            data.getAdditionalInfo().getCategory()
        );
    }
}
```

### 장점

1. **재사용성**: 필터를 다른 파이프라인에서 재사용 가능
2. **유지보수**: 각 필터를 독립적으로 수정 가능
3. **병렬 처리**: 여러 필터를 병렬로 실행 가능
4. **확장성**: 새로운 필터를 쉽게 추가 가능
5. **테스트 용이성**: 각 필터를 개별적으로 테스트 가능

### 단점

1. **성능 오버헤드**: 데이터 전달과 변환으로 인한 비용
2. **복잡한 제어 흐름**: 조건부 처리나 반복이 어려움
3. **상태 관리**: 필터 간 상태 공유가 어려움
4. **에러 처리**: 중간 단계 실패 시 복구가 복잡

---

## 이벤트 기반 아키텍처

이벤트 기반 아키텍처는 컴포넌트들이 이벤트를 통해 느슨하게 결합되어 비동기적으로 소통하는 패턴입니다. 시스템의 상태 변화를 이벤트로 표현하고, 이를 구독하는 컴포넌트들이 반응합니다.

###️ 기본 구조

```
┌─────────────┐    Event    ┌─────────────────┐    Event    ┌─────────────┐
│  Producer   │ ─────────→  │  Event Channel  │ ─────────→  │  Consumer   │
│             │             │                 │             │             │
│ - Generate  │             │ - Store         │             │ - Subscribe │
│   Events    │             │ - Route         │             │ - Process   │
│             │             │ - Filter        │             │   Events    │
└─────────────┘             └─────────────────┘             └─────────────┘
```

### 발행-구독 패턴 구현

```java
// 이벤트 정의
public class OrderCreatedEvent {
    private final Long orderId;
    private final Long customerId;
    private final BigDecimal amount;
    private final LocalDateTime timestamp;
    
    public OrderCreatedEvent(Long orderId, Long customerId, BigDecimal amount) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.amount = amount;
        this.timestamp = LocalDateTime.now();
    }
    
    // getters...
}

// 이벤트 발행자
@Service
public class OrderService {
    
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    @Autowired
    private OrderRepository orderRepository;
    
    public Order createOrder(CreateOrderCommand command) {
        // 주문 생성
        Order order = new Order(command.getCustomerId(), command.getAmount());
        Order savedOrder = orderRepository.save(order);
        
        // 이벤트 발행
        OrderCreatedEvent event = new OrderCreatedEvent(
            savedOrder.getId(),
            savedOrder.getCustomerId(),
            savedOrder.getAmount()
        );
        eventPublisher.publishEvent(event);
        
        return savedOrder;
    }
}

// 이벤트 구독자들
@Component
public class EmailNotificationService {
    
    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 주문 확인 이메일 발송
        String customerEmail = customerService.getEmail(event.getCustomerId());
        emailService.sendOrderConfirmation(customerEmail, event.getOrderId());
        
        logger.info("Order confirmation email sent for order: {}", event.getOrderId());
    }
}

@Component
public class InventoryService {
    
    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 재고 업데이트
        reserveInventory(event.getOrderId());
        
        logger.info("Inventory reserved for order: {}", event.getOrderId());
    }
}
```

### 장점

1. **느슨한 결합**: 컴포넌트 간 직접적인 의존성 제거
2. **확장성**: 새로운 이벤트 처리기를 쉽게 추가
3. **비동기 처리**: 시스템 응답성 향상
4. **이력 추적**: 모든 변경 사항을 이벤트로 기록
5. **장애 격리**: 한 컴포넌트 장애가 다른 컴포넌트에 직접 영향 없음

### 단점

1. **복잡성**: 시스템 전체 흐름 파악이 어려움
2. **일관성**: 최종 일관성(Eventually Consistent) 모델
3. **디버깅 어려움**: 비동기 처리로 인한 추적의 어려움
4. **중복 처리**: 동일 이벤트의 중복 처리 가능성
5. **이벤트 순서**: 이벤트 처리 순서 보장의 어려움

---

## 핵심 요약

### 아키텍처 패턴 비교

| 패턴 | 주요 특징 | 장점 | 단점 | 적용 사례 |
|------|-----------|------|------|-----------|
| **계층화** | 수직적 분리 | 이해 용이, 개발 분담 | 성능 오버헤드 | 웹 애플리케이션, 엔터프라이즈 시스템 |
| **클라이언트-서버** | 분산 처리 | 중앙 집중화, 확장성 | 네트워크 의존성 | 웹 서비스, 모바일 앱 |
| **파이프-필터** | 순차적 변환 | 재사용성, 병렬 처리 | 복잡한 제어 흐름 | 컴파일러, 이미지 처리, ETL |
| **이벤트 기반** | 비동기 소통 | 느슨한 결합, 확장성 | 복잡성, 일관성 문제 | 마이크로서비스, 실시간 시스템 |

### 패턴 선택 가이드

1. **단순한 비즈니스 로직**: 계층화 아키텍처
2. **분산 시스템**: 클라이언트-서버 아키텍처
3. **데이터 변환 파이프라인**: 파이프-필터 아키텍처
4. **실시간 반응형 시스템**: 이벤트 기반 아키텍처

### 다음 장 연결고리
다음 장에서는 현대적인 **모던 아키텍처 패러다임**들을 학습하겠습니다. 마이크로서비스, 서버리스, 헥사고날 아키텍처, CQRS와 이벤트 소싱 등 최신 트렌드를 다룰 예정입니다.

---

## 생각해보기

1. **현재 프로젝트**에서 사용 중인 아키텍처 패턴은 무엇인가요? 왜 그 패턴을 선택했을까요?

2. **계층화 아키텍처의 성능 문제**를 해결하기 위한 방법들은 무엇이 있을까요?

3. **이벤트 기반 아키텍처**에서 발생할 수 있는 **데이터 일관성 문제**를 어떻게 해결할 수 있을까요?

---

## 추가 학습 자료

### 필수 도서
- "Pattern-Oriented Software Architecture" (POSA) 시리즈
- "Software Architecture Patterns" - Mark Richards
- "Enterprise Integration Patterns" - Gregor Hohpe
- "Reactive Design Patterns" - Roland Kuhn

### 온라인 자료
- [Microsoft Architecture Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)
- [AWS Architecture Patterns](https://aws.amazon.com/architecture/)
- [Martin Fowler's Architecture Articles](https://martinfowler.com/architecture/) 