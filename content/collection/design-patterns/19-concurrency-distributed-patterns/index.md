---
collection_order: 190
draft: true
title: "[Design Patterns] 동시성과 분산 시스템에서의 패턴"
description: "동시성과 분산 시스템 환경에서 적용되는 고급 디자인 패턴을 탐구합니다. Thread-Safe Singleton, Producer-Consumer, Actor 패턴 등 동시성 패턴과 Circuit Breaker, Event Sourcing, CQRS 등 분산 시스템 패턴을 다루며, 확장성과 안정성을 보장하는 현대적 아키텍처 설계 기법을 학습합니다."
date: 2024-12-19T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Concurrency Patterns
- Distributed Systems
- Scalability Patterns
tags:
- Concurrency Patterns
- Distributed Patterns
- Thread Safety
- Actor Pattern
- Circuit Breaker
- Event Sourcing
- CQRS Pattern
- Microservices
- Scalability
- Fault Tolerance
- Asynchronous Programming
- Message Passing
- Load Balancing
- Data Consistency
- Distributed Computing
- Parallel Processing
- Reactive Programming
- Producer Consumer
- Observer Pattern
- Command Pattern
- Event Driven Architecture
- Saga Pattern
- Bulkhead Pattern
- Retry Pattern
- Timeout Pattern
- Cache Patterns
- Sharding Patterns
- Replication Patterns
- Consensus Algorithms
- CAP Theorem
- Eventual Consistency
- 동시성 패턴
- 분산 패턴
- 스레드 안전성
- 액터 패턴
- 서킷 브레이커
- 이벤트 소싱
- CQRS 패턴
- 마이크로서비스
- 확장성
- 장애 허용성
- 비동기 프로그래밍
- 메시지 전달
- 로드 밸런싱
- 데이터 일관성
- 분산 컴퓨팅
- 병렬 처리
- 리액티브 프로그래밍
- 생산자 소비자
- 옵저버 패턴
- 커맨드 패턴
- 이벤트 주도 아키텍처
- 사가 패턴
- 벌크헤드 패턴
- 재시도 패턴
- 타임아웃 패턴
- 캐시 패턴
- 샤딩 패턴
- 복제 패턴
- 합의 알고리즘
- CAP 이론
- 최종 일관성
---

# 동시성과 분산 시스템에서의 패턴 - 확장성의 도전

## 🌐 **서론: 분산 세계의 패턴 진화**

> *"단일 시스템에서 동작하던 패턴들이 분산 환경에서 어떻게 진화하고 있는가? 동시성과 분산성은 기존 패턴에 새로운 도전과 기회를 가져다준다."*

현대 소프트웨어는 **분산 시스템**과 **고동시성** 환경에서 동작해야 합니다. 전통적 디자인 패턴들이 이러한 환경에서 어떻게 적응하고 진화했는지, 그리고 분산 시스템만의 새로운 패턴들을 탐구해보겠습니다.

## ⚡ **1. 동시성 패턴들**

### **1.1 Thread-Safe Singleton - 동시성의 첫 번째 시험**

```java
// ✅ 현대적 Thread-Safe Singleton 구현들
public class ModernSingleton {
    
    // 1. Enum 기반 (가장 안전)
    public enum EnumSingleton {
        INSTANCE;
        
        private final ConfigService configService;
        
        EnumSingleton() {
            this.configService = new ConfigService();
        }
        
        public ConfigService getConfigService() {
            return configService;
        }
    }
    
    // 2. Double-Checked Locking (최적화된)
    public static class DCLSingleton {
        private static volatile DCLSingleton instance;
        private final Map<String, String> config;
        
        private DCLSingleton() {
            // 초기화 비용이 큰 작업
            this.config = loadConfiguration();
        }
        
        public static DCLSingleton getInstance() {
            if (instance == null) {
                synchronized (DCLSingleton.class) {
                    if (instance == null) {
                        instance = new DCLSingleton();
                    }
                }
            }
            return instance;
        }
        
        private Map<String, String> loadConfiguration() {
            // 실제로는 외부 설정 로드
            return Map.of("env", "production", "db.url", "jdbc:mysql://localhost");
        }
    }
    
    // 3. Initialization-on-demand holder (지연 로딩 + Thread-Safe)
    public static class LazyHolder {
        private static final class Holder {
            private static final LazyHolder INSTANCE = new LazyHolder();
        }
        
        public static LazyHolder getInstance() {
            return Holder.INSTANCE;
        }
    }
}
```

### **1.2 Producer-Consumer 패턴 - 동시성의 핵심**

```java
// ✅ 현대적 Producer-Consumer 구현
public class ModernProducerConsumer<T> {
    private final BlockingQueue<T> queue;
    private final AtomicBoolean running = new AtomicBoolean(true);
    private final ExecutorService producerPool;
    private final ExecutorService consumerPool;
    
    public ModernProducerConsumer(int capacity, int producerCount, int consumerCount) {
        this.queue = new ArrayBlockingQueue<>(capacity);
        this.producerPool = Executors.newFixedThreadPool(producerCount);
        this.consumerPool = Executors.newFixedThreadPool(consumerCount);
    }
    
    public void startProducers(Supplier<T> producer) {
        for (int i = 0; i < ((ThreadPoolExecutor) producerPool).getCorePoolSize(); i++) {
            producerPool.submit(() -> {
                while (running.get()) {
                    try {
                        T item = producer.get();
                        queue.put(item);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
    }
    
    public void startConsumers(Consumer<T> consumer) {
        for (int i = 0; i < ((ThreadPoolExecutor) consumerPool).getCorePoolSize(); i++) {
            consumerPool.submit(() -> {
                while (running.get() || !queue.isEmpty()) {
                    try {
                        T item = queue.poll(1, TimeUnit.SECONDS);
                        if (item != null) {
                            consumer.accept(item);
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
    }
    
    public void shutdown() {
        running.set(false);
        producerPool.shutdown();
        consumerPool.shutdown();
    }
}
```

### **1.3 Actor 패턴 - 동시성의 새로운 접근**

```java
// ✅ Java에서의 Actor 패턴 구현
public abstract class Actor<T> {
    private final BlockingQueue<T> mailbox = new LinkedBlockingQueue<>();
    private final AtomicBoolean running = new AtomicBoolean(false);
    private final ExecutorService executor;
    private Future<?> actorTask;
    
    public Actor(ExecutorService executor) {
        this.executor = executor;
    }
    
    public void start() {
        if (running.compareAndSet(false, true)) {
            actorTask = executor.submit(this::messageLoop);
        }
    }
    
    public void send(T message) {
        if (running.get()) {
            mailbox.offer(message);
        }
    }
    
    public void stop() {
        running.set(false);
        if (actorTask != null) {
            actorTask.cancel(true);
        }
    }
    
    protected abstract void handle(T message);
    
    private void messageLoop() {
        while (running.get()) {
            try {
                T message = mailbox.poll(1, TimeUnit.SECONDS);
                if (message != null) {
                    handle(message);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}

// 구체적인 Actor 구현
public class OrderProcessorActor extends Actor<OrderMessage> {
    private final Map<String, Integer> orderCounts = new ConcurrentHashMap<>();
    
    public OrderProcessorActor(ExecutorService executor) {
        super(executor);
    }
    
    @Override
    protected void handle(OrderMessage message) {
        switch (message.getType()) {
            case PROCESS_ORDER:
                processOrder(message.getOrder());
                break;
            case GET_STATS:
                sendStats(message.getSender());
                break;
        }
    }
    
    private void processOrder(Order order) {
        // 주문 처리 로직
        orderCounts.merge(order.getProductId(), 1, Integer::sum);
        System.out.println("Processed order for: " + order.getProductId());
    }
    
    private void sendStats(Actor<StatsMessage> sender) {
        StatsMessage stats = new StatsMessage(new HashMap<>(orderCounts));
        sender.send(stats);
    }
}
```

## 🌍 **2. 분산 시스템 패턴들**

### **2.1 Circuit Breaker - 장애 전파 방지**

```java
// ✅ Circuit Breaker 패턴 구현
public class CircuitBreaker {
    public enum State { CLOSED, OPEN, HALF_OPEN }
    
    private final String name;
    private final int failureThreshold;
    private final Duration timeout;
    private final Duration retryTimeout;
    
    private State state = State.CLOSED;
    private int failureCount = 0;
    private long lastFailureTime = 0;
    private long lastRetryTime = 0;
    
    public CircuitBreaker(String name, int failureThreshold, Duration timeout, Duration retryTimeout) {
        this.name = name;
        this.failureThreshold = failureThreshold;
        this.timeout = timeout;
        this.retryTimeout = retryTimeout;
    }
    
    public <T> T execute(Callable<T> operation) throws Exception {
        if (state == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime >= retryTimeout.toMillis()) {
                state = State.HALF_OPEN;
                lastRetryTime = System.currentTimeMillis();
            } else {
                throw new CircuitBreakerOpenException("Circuit breaker is OPEN for " + name);
            }
        }
        
        try {
            T result = operation.call();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            throw e;
        }
    }
    
    private void onSuccess() {
        failureCount = 0;
        state = State.CLOSED;
    }
    
    private void onFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        
        if (failureCount >= failureThreshold) {
            state = State.OPEN;
        }
    }
}

// 사용 예시
public class ExternalServiceClient {
    private final CircuitBreaker circuitBreaker;
    private final HttpClient httpClient;
    
    public ExternalServiceClient() {
        this.circuitBreaker = new CircuitBreaker("external-service", 5, 
            Duration.ofSeconds(30), Duration.ofMinutes(1));
        this.httpClient = HttpClient.newHttpClient();
    }
    
    public String callExternalService(String data) {
        try {
            return circuitBreaker.execute(() -> {
                HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.external-service.com/process"))
                    .POST(HttpRequest.BodyPublishers.ofString(data))
                    .build();
                
                HttpResponse<String> response = httpClient.send(request, 
                    HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() != 200) {
                    throw new RuntimeException("Service returned: " + response.statusCode());
                }
                
                return response.body();
            });
        } catch (Exception e) {
            return handleFailure(e);
        }
    }
    
    private String handleFailure(Exception e) {
        // 대체 로직 또는 캐시된 데이터 반환
        return "Service temporarily unavailable";
    }
}
```

### **2.2 Event Sourcing - 분산 상태 관리**

```java
// ✅ Event Sourcing 패턴
public abstract class Event {
    private final UUID id = UUID.randomUUID();
    private final LocalDateTime timestamp = LocalDateTime.now();
    private final String eventType = this.getClass().getSimpleName();
    
    public UUID getId() { return id; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return eventType; }
}

// 도메인 이벤트들
public class OrderCreatedEvent extends Event {
    private final String orderId;
    private final String customerId;
    private final List<OrderItem> items;
    
    public OrderCreatedEvent(String orderId, String customerId, List<OrderItem> items) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.items = items;
    }
    
    // getters...
}

public class OrderShippedEvent extends Event {
    private final String orderId;
    private final String trackingNumber;
    
    public OrderShippedEvent(String orderId, String trackingNumber) {
        this.orderId = orderId;
        this.trackingNumber = trackingNumber;
    }
    
    // getters...
}

// Event Store
public class EventStore {
    private final Map<String, List<Event>> eventStreams = new ConcurrentHashMap<>();
    
    public void append(String streamId, Event event) {
        eventStreams.computeIfAbsent(streamId, k -> new CopyOnWriteArrayList<>()).add(event);
    }
    
    public List<Event> getEvents(String streamId) {
        return eventStreams.getOrDefault(streamId, Collections.emptyList());
    }
    
    public List<Event> getEvents(String streamId, int fromVersion) {
        List<Event> events = getEvents(streamId);
        return events.size() > fromVersion ? 
            events.subList(fromVersion, events.size()) : Collections.emptyList();
    }
}

// Aggregate Root (Event Sourcing)
public class Order {
    private String id;
    private String customerId;
    private List<OrderItem> items = new ArrayList<>();
    private OrderStatus status = OrderStatus.CREATED;
    private List<Event> uncommittedEvents = new ArrayList<>();
    private int version = 0;
    
    public static Order create(String orderId, String customerId, List<OrderItem> items) {
        Order order = new Order();
        order.apply(new OrderCreatedEvent(orderId, customerId, items));
        return order;
    }
    
    public void ship(String trackingNumber) {
        if (status != OrderStatus.CONFIRMED) {
            throw new IllegalStateException("Order must be confirmed before shipping");
        }
        apply(new OrderShippedEvent(id, trackingNumber));
    }
    
    public static Order fromHistory(List<Event> events) {
        Order order = new Order();
        for (Event event : events) {
            order.apply(event);
            order.version++;
        }
        order.uncommittedEvents.clear();
        return order;
    }
    
    private void apply(Event event) {
        if (event instanceof OrderCreatedEvent) {
            handle((OrderCreatedEvent) event);
        } else if (event instanceof OrderShippedEvent) {
            handle((OrderShippedEvent) event);
        }
        
        uncommittedEvents.add(event);
    }
    
    private void handle(OrderCreatedEvent event) {
        this.id = event.getOrderId();
        this.customerId = event.getCustomerId();
        this.items = new ArrayList<>(event.getItems());
        this.status = OrderStatus.CREATED;
    }
    
    private void handle(OrderShippedEvent event) {
        this.status = OrderStatus.SHIPPED;
    }
    
    public List<Event> getUncommittedEvents() {
        return new ArrayList<>(uncommittedEvents);
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
}
```

### **2.3 CQRS - 읽기/쓰기 분리**

```java
// ✅ CQRS 패턴 구현
// Command 측면
public abstract class Command {
    private final UUID id = UUID.randomUUID();
    private final LocalDateTime timestamp = LocalDateTime.now();
    
    public UUID getId() { return id; }
    public LocalDateTime getTimestamp() { return timestamp; }
}

public class CreateOrderCommand extends Command {
    private final String customerId;
    private final List<OrderItem> items;
    
    public CreateOrderCommand(String customerId, List<OrderItem> items) {
        this.customerId = customerId;
        this.items = items;
    }
    
    // getters...
}

public interface CommandHandler<T extends Command> {
    void handle(T command);
}

public class CreateOrderCommandHandler implements CommandHandler<CreateOrderCommand> {
    private final EventStore eventStore;
    
    public CreateOrderCommandHandler(EventStore eventStore) {
        this.eventStore = eventStore;
    }
    
    @Override
    public void handle(CreateOrderCommand command) {
        String orderId = UUID.randomUUID().toString();
        Order order = Order.create(orderId, command.getCustomerId(), command.getItems());
        
        // 이벤트 저장
        for (Event event : order.getUncommittedEvents()) {
            eventStore.append(orderId, event);
        }
        
        order.markEventsAsCommitted();
    }
}

// Query 측면
public class OrderSummaryView {
    private final String orderId;
    private final String customerId;
    private final BigDecimal totalAmount;
    private final OrderStatus status;
    private final LocalDateTime createdAt;
    
    public OrderSummaryView(String orderId, String customerId, BigDecimal totalAmount, 
                           OrderStatus status, LocalDateTime createdAt) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.totalAmount = totalAmount;
        this.status = status;
        this.createdAt = createdAt;
    }
    
    // getters...
}

public class OrderQueryService {
    private final Map<String, OrderSummaryView> orderSummaries = new ConcurrentHashMap<>();
    
    // 이벤트 핸들러 (프로젝션 업데이트)
    public void on(OrderCreatedEvent event) {
        BigDecimal total = event.getItems().stream()
            .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        OrderSummaryView summary = new OrderSummaryView(
            event.getOrderId(),
            event.getCustomerId(),
            total,
            OrderStatus.CREATED,
            LocalDateTime.now()
        );
        
        orderSummaries.put(event.getOrderId(), summary);
    }
    
    public void on(OrderShippedEvent event) {
        OrderSummaryView existing = orderSummaries.get(event.getOrderId());
        if (existing != null) {
            OrderSummaryView updated = new OrderSummaryView(
                existing.getOrderId(),
                existing.getCustomerId(),
                existing.getTotalAmount(),
                OrderStatus.SHIPPED,
                existing.getCreatedAt()
            );
            orderSummaries.put(event.getOrderId(), updated);
        }
    }
    
    public List<OrderSummaryView> getOrdersByCustomer(String customerId) {
        return orderSummaries.values().stream()
            .filter(order -> order.getCustomerId().equals(customerId))
            .collect(Collectors.toList());
    }
}
```

## 📊 **3. 성능과 확장성 분석**

### **패턴별 성능 특성**

| 패턴 | 처리량 | 지연시간 | 메모리 사용 | 확장성 | 복잡성 |
|------|--------|----------|-------------|--------|---------|
| Thread-Safe Singleton | 높음 | 낮음 | 낮음 | 제한적 | 낮음 |
| Producer-Consumer | 매우 높음 | 중간 | 중간 | 높음 | 중간 |
| Actor Model | 높음 | 낮음 | 높음 | 매우 높음 | 높음 |
| Circuit Breaker | 중간 | 낮음 | 낮음 | 높음 | 중간 |
| Event Sourcing | 중간 | 높음 | 높음 | 높음 | 높음 |
| CQRS | 높음 | 중간 | 중간 | 매우 높음 | 높음 |

## 🎯 **결론: 분산 시대의 패턴 진화**

분산 시스템과 동시성 환경은 디자인 패턴에 **새로운 차원**을 열어주었습니다:

### **🌟 핵심 인사이트**

1. **상태 관리의 복잡성**: 분산 환경에서 상태 일관성 유지의 도전
2. **장애 내성**: Circuit Breaker, Bulkhead 패턴을 통한 회복력 구축
3. **비동기 통신**: Event-driven 아키텍처의 중요성 증대
4. **확장성 vs 일관성**: CAP 정리에 따른 트레이드오프 관리

> *"분산 시스템에서는 완벽한 해결책은 없다. 있는 것은 적절한 트레이드오프뿐이다."*

현대 개발자는 **단일 시스템의 패턴**과 **분산 시스템의 패턴**을 모두 이해해야 합니다. 각각의 장단점을 파악하고 상황에 맞는 최적의 선택을 하는 것이 핵심입니다! 🚀