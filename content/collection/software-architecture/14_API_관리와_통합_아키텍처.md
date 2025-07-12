---
draft: true
---
# 14장. API 관리와 통합 아키텍처

## 📋 학습 목표
- API 게이트웨이 패턴과 설계 방법을 이해한다
- 메시징 패턴과 이벤트 기반 통합을 습득한다
- 엔터프라이즈 서비스 버스(ESB) 개념을 파악한다
- 시스템 간 통합 전략을 학습한다

---

## 14.1 API 게이트웨이 패턴

### 14.1.1 API 게이트웨이란?

API 게이트웨이는 **모든 클라이언트 요청에 대한 단일 진입점 역할을 하는 서버**로, 라우팅, 인증, 모니터링, 트래픽 제어 등을 담당합니다.

### 14.1.2 API 게이트웨이 구현 예제

```java
// Spring Cloud Gateway 구현
@Configuration
public class GatewayConfig {
    
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .filters(f -> f
                    .stripPrefix(2)
                    .circuitBreaker(config -> config
                        .setName("userServiceCB")
                        .setFallbackUri("forward:/fallback/users"))
                )
                .uri("lb://user-service"))
            
            .route("order-service", r -> r.path("/api/orders/**")
                .filters(f -> f
                    .stripPrefix(2)
                    .retry(config -> config.setRetries(3))
                )
                .uri("lb://order-service"))
            .build();
    }
}

// 인증 필터
@Component
public class AuthenticationFilter implements GatewayFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return handleUnauthorized(exchange);
        }
        
        try {
            String token = authHeader.substring(7);
            Claims claims = jwtUtil.validateToken(token);
            
            ServerHttpRequest modifiedRequest = request.mutate()
                .header("X-User-Id", claims.getSubject())
                .build();
            
            return chain.filter(exchange.mutate().request(modifiedRequest).build());
        } catch (Exception e) {
            return handleUnauthorized(exchange);
        }
    }
    
    private Mono<Void> handleUnauthorized(ServerWebExchange exchange) {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        return exchange.getResponse().setComplete();
    }
}

// 요율 제한 필터
@Component
public class RateLimitingFilter implements GatewayFilter {
    
    private final RedisTemplate<String, String> redisTemplate;
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String clientId = getClientId(exchange.getRequest());
        String key = "rate_limit:" + clientId;
        
        return Mono.fromCallable(() -> {
            String currentCount = redisTemplate.opsForValue().get(key);
            int count = currentCount != null ? Integer.parseInt(currentCount) : 0;
            
            if (count >= 100) { // 분당 100회 제한
                return false;
            }
            
            redisTemplate.opsForValue().increment(key);
            redisTemplate.expire(key, Duration.ofMinutes(1));
            return true;
        })
        .flatMap(allowed -> {
            if (allowed) {
                return chain.filter(exchange);
            } else {
                exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
                return exchange.getResponse().setComplete();
            }
        });
    }
}
```

### 14.1.3 API 게이트웨이 모니터링

```java
// 메트릭 수집 필터
@Component
public class MetricsFilter implements GatewayFilter {
    
    private final MeterRegistry meterRegistry;
    
    public MetricsFilter(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        long startTime = System.currentTimeMillis();
        String serviceName = getServiceName(exchange.getRequest());
        
        return chain.filter(exchange)
            .doOnSuccess(result -> recordMetrics(serviceName, startTime, true))
            .doOnError(error -> recordMetrics(serviceName, startTime, false));
    }
    
    private void recordMetrics(String serviceName, long startTime, boolean success) {
        long duration = System.currentTimeMillis() - startTime;
        
        Timer.Sample sample = Timer.start(meterRegistry);
        sample.stop(Timer.builder("gateway.request.duration")
            .tag("service", serviceName)
            .tag("success", String.valueOf(success))
            .register(meterRegistry));
        
        Counter.builder("gateway.request.count")
            .tag("service", serviceName)
            .tag("success", String.valueOf(success))
            .register(meterRegistry)
            .increment();
    }
}
```

---

## 14.2 메시징 패턴과 이벤트 기반 통합

### 14.2.1 메시징 패턴

```java
// 발행-구독 패턴
@Component
public class OrderEventPublisher {
    
    private final RabbitTemplate rabbitTemplate;
    
    public void publishOrderCreated(OrderCreatedEvent event) {
        rabbitTemplate.convertAndSend(
            "order.exchange", 
            "order.created", 
            event
        );
    }
}

// 메시지 소비자
@RabbitListener(queues = "inventory.order.created")
@Component
public class InventoryEventHandler {
    
    private final InventoryService inventoryService;
    
    @RabbitHandler
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            inventoryService.reserveItems(event.getOrderId(), event.getItems());
        } catch (Exception e) {
            throw new AmqpRejectAndDontRequeueException("재고 예약 실패", e);
        }
    }
}

// Dead Letter Queue 처리
@RabbitListener(queues = "inventory.order.created.dlq")
@Component
public class DeadLetterHandler {
    
    private final NotificationService notificationService;
    
    @RabbitHandler
    public void handleDeadLetter(OrderCreatedEvent event, 
                                @Header Map<String, Object> headers) {
        log.error("Dead letter 처리: {}, 헤더: {}", event, headers);
        
        // 관리자에게 알림
        notificationService.notifyAdmins(
            "메시지 처리 실패", 
            "주문 이벤트 처리 실패: " + event.getOrderId()
        );
    }
}

// 메시지 중복 처리 방지
@Component
public class IdempotentMessageHandler {
    
    private final RedisTemplate<String, String> redisTemplate;
    
    public boolean isProcessed(String messageId) {
        String key = "processed_message:" + messageId;
        return redisTemplate.hasKey(key);
    }
    
    public void markAsProcessed(String messageId) {
        String key = "processed_message:" + messageId;
        redisTemplate.opsForValue().set(key, "true", Duration.ofHours(24));
    }
}
```

### 14.2.2 이벤트 소싱과 CQRS 통합

```java
// 이벤트 스트림 처리
@Component
public class EventStreamProcessor {
    
    private final EventStore eventStore;
    private final ReadModelUpdater readModelUpdater;
    
    @EventListener
    @Async
    public void handleDomainEvent(DomainEvent event) {
        // 이벤트 스토어에 저장
        eventStore.append(event);
        
        // Read Model 업데이트
        readModelUpdater.handle(event);
        
        // 외부 시스템에 알림
        publishToExternalSystems(event);
    }
    
    private void publishToExternalSystems(DomainEvent event) {
        // 메시지 브로커로 발행
        rabbitTemplate.convertAndSend("domain.events", event);
    }
}

// 이벤트 재생 (Event Replay)
@Service
public class EventReplayService {
    
    private final EventStore eventStore;
    private final List<EventHandler> eventHandlers;
    
    public void replayEvents(String aggregateId, LocalDateTime fromTimestamp) {
        List<DomainEvent> events = eventStore.getEventsAfter(aggregateId, fromTimestamp);
        
        for (DomainEvent event : events) {
            for (EventHandler handler : eventHandlers) {
                if (handler.canHandle(event)) {
                    handler.handle(event);
                }
            }
        }
    }
}
```

---

## 14.3 엔터프라이즈 서비스 버스 (ESB)

### 14.3.1 ESB 개념과 구현

```java
// 메시지 라우터
@Component
public class MessageRouter {
    
    private final Map<String, MessageHandler> handlers;
    private final MessageTransformer transformer;
    
    public MessageRouter(List<MessageHandler> handlerList, 
                        MessageTransformer transformer) {
        this.handlers = handlerList.stream()
            .collect(Collectors.toMap(
                MessageHandler::getMessageType,
                Function.identity()
            ));
        this.transformer = transformer;
    }
    
    public void routeMessage(Message message) {
        try {
            // 메시지 변환
            Message transformedMessage = transformer.transform(message);
            
            // 적절한 핸들러 선택
            MessageHandler handler = handlers.get(transformedMessage.getType());
            if (handler != null) {
                handler.handle(transformedMessage);
            } else {
                log.warn("핸들러를 찾을 수 없음: {}", transformedMessage.getType());
            }
            
        } catch (Exception e) {
            handleRoutingError(message, e);
        }
    }
    
    private void handleRoutingError(Message message, Exception e) {
        log.error("메시지 라우팅 실패: {}", message, e);
        // 에러 큐로 전송
        errorQueueSender.send(message, e.getMessage());
    }
}

// 메시지 변환기
@Component
public class MessageTransformer {
    
    private final ObjectMapper objectMapper;
    
    public Message transform(Message sourceMessage) {
        String sourceType = sourceMessage.getType();
        Object sourcePayload = sourceMessage.getPayload();
        
        switch (sourceType) {
            case "ORDER_CREATED_V1":
                return transformOrderV1ToV2(sourcePayload);
            case "CUSTOMER_UPDATED_LEGACY":
                return transformLegacyCustomer(sourcePayload);
            default:
                return sourceMessage; // 변환 불필요
        }
    }
    
    private Message transformOrderV1ToV2(Object payload) {
        // V1 주문 형식을 V2로 변환
        OrderV1 orderV1 = (OrderV1) payload;
        OrderV2 orderV2 = OrderV2.builder()
            .orderId(orderV1.getId())
            .customerId(orderV1.getCustomerId())
            .items(convertItems(orderV1.getItems()))
            .totalAmount(orderV1.getTotal())
            .currency("KRW") // V2에서 추가된 필드
            .build();
        
        return new Message("ORDER_CREATED_V2", orderV2);
    }
}

// 메시지 브로커 추상화
public interface MessageBroker {
    void send(String destination, Message message);
    void subscribe(String source, MessageConsumer consumer);
}

@Component
public class RabbitMQBroker implements MessageBroker {
    
    private final RabbitTemplate rabbitTemplate;
    
    @Override
    public void send(String destination, Message message) {
        rabbitTemplate.convertAndSend(destination, message);
    }
    
    @Override
    public void subscribe(String source, MessageConsumer consumer) {
        // RabbitMQ 리스너 등록 로직
    }
}
```

---

## 14.4 시스템 간 통합 전략

### 14.4.1 동기 vs 비동기 통합

```java
// 동기 통합 - REST API 호출
@Service
public class SynchronousIntegrationService {
    
    private final PaymentGatewayClient paymentClient;
    private final CircuitBreaker circuitBreaker;
    
    public PaymentResult processPayment(PaymentRequest request) {
        return circuitBreaker.executeSupplier(() -> {
            return paymentClient.processPayment(request);
        });
    }
}

// 비동기 통합 - 메시지 기반
@Service
public class AsynchronousIntegrationService {
    
    private final MessageBroker messageBroker;
    
    public void processOrderAsync(Order order) {
        OrderProcessingMessage message = OrderProcessingMessage.builder()
            .orderId(order.getId())
            .customerId(order.getCustomerId())
            .items(order.getItems())
            .build();
        
        messageBroker.send("order.processing.queue", message);
    }
    
    @EventListener
    public void handleOrderProcessed(OrderProcessedEvent event) {
        Order order = orderRepository.findById(event.getOrderId())
            .orElseThrow();
        
        order.markAsProcessed();
        orderRepository.save(order);
        
        notificationService.notifyOrderProcessed(order);
    }
}
```

### 14.4.2 데이터 동기화 패턴

```java
// Change Data Capture (CDC) 패턴
@Component
public class DatabaseChangeListener {
    
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleEntityChange(EntityChangeEvent event) {
        switch (event.getChangeType()) {
            case INSERT:
                eventPublisher.publish(new EntityCreatedEvent(event.getEntity()));
                break;
            case UPDATE:
                eventPublisher.publish(new EntityUpdatedEvent(event.getEntity()));
                break;
            case DELETE:
                eventPublisher.publish(new EntityDeletedEvent(event.getEntityId()));
                break;
        }
    }
}

// 배치 동기화
@Component
public class BatchSynchronizer {
    
    @Scheduled(fixedDelay = 300000) // 5분마다 실행
    public void synchronizeCustomerData() {
        LocalDateTime lastSync = getLastSyncTimestamp();
        List<Customer> changedCustomers = customerRepository
            .findByLastModifiedAfter(lastSync);
        
        for (Customer customer : changedCustomers) {
            try {
                externalSystemClient.updateCustomer(customer);
            } catch (Exception e) {
                retryQueue.add(new SyncRetryItem(customer.getId(), e.getMessage()));
            }
        }
        
        updateLastSyncTimestamp(LocalDateTime.now());
    }
}
```

---

## 🎯 핵심 요약

### API 관리와 통합 패턴 비교

| **패턴** | **장점** | **단점** | **적용 시나리오** |
|---------|---------|---------|-----------------|
| **API 게이트웨이** | 중앙 집중 관리 | 단일 장애점 | 마이크로서비스 |
| **동기 통합** | 즉시 결과 확인 | 높은 결합도 | 실시간 처리 |
| **비동기 통합** | 낮은 결합도 | 복잡한 에러 처리 | 대용량 처리 |
| **배치 동기화** | 안정적 처리 | 지연된 일관성 | 대량 데이터 |

### 통합 아키텍처 설계 원칙
1. **느슨한 결합 (Loose Coupling)**
2. **높은 응집도 (High Cohesion)**
3. **비동기 처리 우선**
4. **장애 격리 (Fault Isolation)**

---

## 💭 생각해보기

1. API 게이트웨이의 단일 장애점 문제를 어떻게 해결할 것인가?
2. 동기와 비동기 통합의 선택 기준은 무엇인가?
3. 레거시 시스템과의 통합 시 고려해야 할 사항들은?

---

## 📚 추가 학습 자료

### 도서
- "Enterprise Integration Patterns" - Gregor Hohpe
- "Building Microservices" - Sam Newman

### 온라인 자료
- Spring Cloud Gateway 문서
- RabbitMQ 공식 가이드 