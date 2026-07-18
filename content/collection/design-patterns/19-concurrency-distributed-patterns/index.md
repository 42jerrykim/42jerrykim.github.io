---
draft: true
collection_order: 190
title: "[Design Patterns] 19. 동시성과 분산 시스템에서의 패턴"
slug: "concurrency-distributed-patterns"
description: "동시성과 분산 시스템 환경에서 적용되는 고급 디자인 패턴을 탐구합니다. Thread-Safe Singleton과 Producer-Consumer 등 동시성 패턴, Circuit Breaker와 CQRS 등 분산 시스템 패턴으로 확장성과 안정성을 갖춘 아키텍처 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-19T10:00:00+09:00
lastmod: 2026-07-18T07:18:00+09:00
categories:
- Design Patterns
- Concurrency Patterns
- Distributed Systems
- Scalability Patterns
tags:
- Microservices(마이크로서비스)
- Scalability(확장성)
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Singleton
- Concurrency(동시성)
- Async(비동기)
- System-Design
- Message-Queue
- Event-Driven
- CQRS(Command Query Responsibility Segregation)
- Software-Architecture(소프트웨어아키텍처)
- Reliability
- Throughput
- Latency
- Production
- Implementation(구현)
- Best-Practices
- Clean-Architecture(클린아키텍처)
- Java
- Thread
- Mutex
- Synchronization
- Tutorial(튜토리얼)
- Deep-Dive
- Advanced
- Case-Study
- Guide(가이드)
---

동시성과 분산 시스템 환경에서 전통적 패턴의 진화와 새로운 패턴을 탐구합니다. 확장 가능한 시스템 설계를 위한 동시성 제어와 분산 패턴을 학습합니다.

## 서론: 분산 세계의 패턴 진화

> *"단일 시스템에서 동작하던 패턴들이 분산 환경에서 어떻게 진화하고 있는가? 동시성과 분산성은 기존 패턴에 새로운 도전과 기회를 가져다준다."*

현대 소프트웨어는 **분산 시스템**과 **고동시성** 환경에서 동작해야 합니다. 전통적 디자인 패턴들이 이러한 환경에서 어떻게 적응하고 진화했는지, 그리고 분산 시스템만의 새로운 패턴들을 탐구해보겠습니다.

이 글의 모든 예제는 아래 임포트를 전제로 합니다.

```java
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.function.*;
import java.util.stream.*;
import java.time.Duration;
import java.time.LocalDateTime;
import java.math.BigDecimal;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
```

## 동시성 패턴들

### Thread-Safe Singleton - 동시성의 첫 번째 시험

```java
// 현대적 Thread-Safe Singleton 구현들
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

### Producer-Consumer 패턴 - 동시성의 핵심

```java
// 현대적 Producer-Consumer 구현
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

`ModernProducerConsumer`의 핵심은 `BlockingQueue`가 생산자와 소비자 사이의 속도 차이를 흡수하는 버퍼 역할을 한다는 데 있다. 생산자 여러 개와 소비자 여러 개가 동시에 같은 큐에 접근하므로, 상태(큐 내부 데이터)를 지키는 주체는 특정 스레드가 아니라 큐 구현체 자체의 락/CAS 메커니즘이다. 그래서 Producer-Consumer는 "여러 생산자·여러 소비자가 공유 버퍼를 통해 결합도를 낮추는" 패턴이지, 다음에 볼 Actor 패턴처럼 "하나의 주체가 자신의 상태를 독점 관리하는" 패턴과는 설계 의도가 다르다.

### Actor 패턴 - 동시성의 새로운 접근

```java
// Java에서의 Actor 패턴 구현
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

`OrderProcessorActor`가 `orderCounts`를 `ConcurrentHashMap`으로 선언했음에도 불구하고, 실제로는 동시성 문제를 피하기 위한 최소한의 방어일 뿐 Actor 패턴의 핵심은 아니다. Actor 패턴의 핵심은 각 액터가 `mailbox`라는 자신만의 큐를 갖고 `messageLoop()` 스레드 하나만 그 상태(`orderCounts`)를 변경한다는 데 있다 — 외부 스레드는 `send()`로 메시지를 큐에 넣을 뿐 상태에 직접 접근하지 않는다. 이 덕분에 액터 내부 로직은 락 없이 순차적으로 작성할 수 있고, 동시성 제어는 "메시지를 어떻게 큐잉하느냐"라는 단일 지점으로 좁혀진다. 반면 다음에 볼 Producer-Consumer는 여러 소비자가 하나의 공유 큐(`BlockingQueue`)를 동시에 놓고 경쟁하므로, 상태를 갖는 주체가 액터처럼 하나로 고정되지 않는다.

## 분산 시스템 패턴들

### Circuit Breaker - 장애 전파 방지

```java
// Circuit Breaker 패턴 구현
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

`CircuitBreaker.execute()`는 호출할 때마다 현재 `state`를 확인하고 그 결과에 따라 `onSuccess()` 또는 `onFailure()`를 실행해 상태를 전이시킨다. `OPEN` 상태에서 `retryTimeout`이 지나면 `HALF_OPEN`으로 바뀌어 시험 호출을 한 번 허용하는데, 이 시험 호출이 성공하면 `failureCount`가 0으로 초기화되며 `CLOSED`로 돌아가고, 실패하면 `failureCount`가 이미 임계값을 넘은 상태이므로 즉시 다시 `OPEN`으로 돌아간다.

```mermaid
stateDiagram-v2
    [*] --> CLOSED
    CLOSED --> CLOSED: execute() 성공</br>onSuccess()
    CLOSED --> OPEN: execute() 실패</br>failureCount >= failureThreshold
    OPEN --> HALF_OPEN: execute() 호출 시</br>retryTimeout 경과
    OPEN --> OPEN: execute() 호출 시</br>retryTimeout 미경과</br>CircuitBreakerOpenException
    HALF_OPEN --> CLOSED: 시험 호출 성공</br>onSuccess(), failureCount=0
    HALF_OPEN --> OPEN: 시험 호출 실패</br>onFailure()
```

### Event Sourcing - 분산 상태 관리

```java
// Event Sourcing 패턴
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

### CQRS - 읽기/쓰기 분리

```java
// CQRS 패턴 구현
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

CQRS는 쓰기 경로와 읽기 경로가 서로 다른 모델을 갖는다는 점이 핵심이다. `CreateOrderCommandHandler`는 `Order` Aggregate를 통해 이벤트를 생성하고 `EventStore`에 추가만 할 뿐, 조회에 필요한 형태로 데이터를 가공하지 않는다. 반대로 `OrderQueryService`는 `EventStore`가 아니라 이벤트를 구독해 자신만의 비정규화된 `OrderSummaryView` 맵을 갱신하며, 조회 요청은 이 맵만 읽는다. 두 경로가 공유하는 것은 오직 이벤트뿐이다.

```mermaid
flowchart LR
    subgraph Write["쓰기 경로 (Command)"]
        Cmd["CreateOrderCommand"] --> Handler["CreateOrderCommandHandler"]
        Handler --> Agg["Order.create()</br>(Aggregate)"]
        Agg --> Store["EventStore.append()"]
    end

    subgraph Read["읽기 경로 (Query)"]
        Store -.이벤트 구독.-> Projector["OrderQueryService.on(event)"]
        Projector --> View["OrderSummaryView</br>(비정규화 맵)"]
        Query["getOrdersByCustomer()"] --> View
    end
```

## 성능과 확장성 분석

### 패턴별 성능 특성

아래 표의 등급(높음/중간/낮음)은 벤치마크 수치가 아니라 각 패턴의 구조적 특징에서 비롯되는 정성적 평가다. 실제 수치는 워크로드와 하드웨어에 따라 달라지므로, 프로덕션 적용 전에는 반드시 JMH 등으로 직접 측정해야 한다.

| 패턴 | 처리량 | 지연시간 | 메모리 사용 | 확장성 | 복잡성 | 근거 |
|------|--------|----------|-------------|--------|---------|------|
| Thread-Safe Singleton | 높음 | 낮음 | 낮음 | 제한적 | 낮음 | 접근 자체는 필드 참조 수준이지만 인스턴스가 하나뿐이라 수평 확장의 병목이 되기 쉽다 |
| Producer-Consumer | 매우 높음 | 중간 | 중간 | 높음 | 중간 | 큐가 생산자·소비자 속도 차이를 흡수하지만, 큐 자체의 락/CAS 경합이 지연시간에 반영된다 |
| Actor Model | 높음 | 낮음 | 높음 | 매우 높음 | 높음 | 액터마다 독립된 메일박스를 유지하므로 액터 수에 비례해 메모리가 증가하지만 락 경합이 없어 지연시간은 낮다 |
| Circuit Breaker | 중간 | 낮음 | 낮음 | 높음 | 중간 | OPEN 상태에서는 즉시 예외를 던져 지연시간을 낮추지만, 그만큼 처리량은 일시적으로 제한된다 |
| Event Sourcing | 중간 | 높음 | 높음 | 높음 | 높음 | 조회 시 이벤트를 재생(replay)해야 하므로 지연시간이 늘고, 이벤트 전체를 보관하므로 메모리·스토리지 사용이 크다 |
| CQRS | 높음 | 중간 | 중간 | 매우 높음 | 높음 | 읽기 모델을 쓰기 모델과 분리해 각각 독립적으로 확장할 수 있지만, 두 모델을 동기화하는 프로젝션 로직이 복잡성을 더한다 |

## 한눈에 보는 동시성/분산 패턴

### 동시성/분산 패턴 비교표

동시성 패턴(단일 프로세스 내 스레드 조정)과 분산 패턴(서비스 간 조정)은 다루는 대상이 다르지만, "핵심 목적"과 "복잡도"라는 동일한 기준으로 비교할 수 있어 하나의 표로 정리한다.

| 유형 | 패턴 | 핵심 목적 | 적용 상황 / 해결 문제 | 복잡도 |
|------|------|----------|----------------------|--------|
| 동시성 | Thread Pool | 스레드 재사용, 자원 관리 | 다수 작업 병렬 처리 | 낮음 |
| 동시성 | Producer-Consumer | 생산/소비 분리, 버퍼링 | 비동기 작업 큐 | 중간 |
| 동시성 | Read-Write Lock | 읽기 동시성, 쓰기 독점 | 읽기 빈번, 쓰기 드묾 | 중간 |
| 동시성 | Double-Checked Locking | 지연 초기화 + 스레드 안전 | 싱글톤, 캐시 | 중간 |
| 동시성 | Future/Promise | 비동기 결과 표현 | 비동기 작업 결과 처리 | 낮음 |
| 동시성 | Actor Model | 메시지 기반 동시성 | 분산 시스템, 고동시성 | 높음 |
| 분산 | Saga | 분산 트랜잭션 | 서비스 간 일관성 (보상 로직 필요) | 높음 |
| 분산 | Circuit Breaker | 장애 격리 | 연쇄 장애 방지 (일시적 서비스 불가 감수) | 중간 |
| 분산 | Retry + Backoff | 일시적 장애 극복 | 네트워크 불안정 (지연 증가 감수) | 낮음 |
| 분산 | Bulkhead | 자원 격리 | 장애 전파 방지 (자원 효율성 감소 감수) | 중간 |
| 분산 | CQRS | 읽기/쓰기 분리 | 성능 최적화 (일관성 복잡성 감수) | 높음 |
| 분산 | Event Sourcing | 이벤트 기반 상태 | 감사, 이력 추적 (구현 복잡성 감수) | 높음 |

### CAP 정리와 패턴 선택

| 선택 | 패턴 적합성 | 사용 예 |
|------|-----------|--------|
| CP (일관성+분할내성) | SAGA, 2PC | 금융 시스템 |
| AP (가용성+분할내성) | Event Sourcing, CQRS | SNS, 쇼핑몰 |
| CA (일관성+가용성) | 전통적 ACID | 단일 DB 시스템 |

### 마이크로서비스 패턴 매트릭스

| 패턴 | 서비스 디커플링 | 장애 내성 | 성능 | 복잡도 |
|------|---------------|---------|------|--------|
| API Gateway | 높음 | 중간 | 중간 | 중간 |
| Service Mesh | 매우 높음 | 높음 | 약간 저하 | 높음 |
| Event-Driven | 매우 높음 | 높음 | 높음 | 높음 |
| Choreography | 높음 | 높음 | 높음 | 중간 |
| Orchestration | 중간 | 중간 | 중간 | 중간 |

### 비동기 통신 패턴

| 패턴 | 특징 | 장점 | 단점 |
|------|------|------|------|
| Request-Reply | 동기식 대기 | 단순함 | 블로킹 |
| Fire-and-Forget | 응답 없음 | 빠름 | 결과 확인 불가 |
| Publish-Subscribe | 다대다 브로드캐스트 | 느슨한 결합 | 순서 보장 어려움 |
| Message Queue | 버퍼링 + 전달 보장 | 신뢰성 | 복잡성 증가 |

### 적용 체크리스트

| 동시성 패턴 체크 | 분산 패턴 체크 |
|----------------|---------------|
| 공유 자원 경합이 있는가? | 서비스 간 트랜잭션 필요? |
| 스레드 안전성이 필요한가? | 장애 격리가 중요한가? |
| 비동기 처리가 필요한가? | 확장성이 중요한가? |
| 성능 병목이 동시성 때문인가? | 일관성 vs 가용성 선택? |

## 흔한 오해 바로잡기

동시성·분산 패턴을 다룰 때 자주 나오는 오해 세 가지를 짚어본다.

첫째, "Circuit Breaker는 장애를 막는다"는 오해다. `CircuitBreaker.execute()`를 다시 보면, OPEN 상태에서 하는 일은 실제 호출을 시도조차 하지 않고 즉시 `CircuitBreakerOpenException`을 던지는 것뿐이다. 즉 Circuit Breaker는 외부 서비스의 장애 자체를 막지 못한다 — 그 장애가 호출자 쪽 스레드 고갈이나 연쇄적인 타임아웃 누적으로 "전파"되는 것을 막을 뿐이다. 장애를 실제로 해결하는 것은 여전히 재시도, 대체 로직(`handleFailure`), 혹은 장애 서비스 자체의 복구다.

둘째, "Actor 패턴과 Producer-Consumer 패턴은 사실상 같다"는 오해다. 둘 다 큐에 아이템을 넣고 별도 스레드가 꺼내 처리한다는 점은 같지만, Producer-Consumer는 여러 생산자·소비자가 하나의 공유 큐를 동시에 두고 경쟁하는 구조이고, Actor는 각 액터가 자신만의 mailbox와 상태를 독점해 락 없이 순차 처리하는 구조다. Producer-Consumer에서 "소비자"는 상태를 소유하지 않지만, Actor에서 액터 자신은 상태(`orderCounts` 등)를 소유한다는 점이 근본적인 차이다.

셋째, "동시성 패턴을 쓰면 스레드 안전성이 자동으로 보장된다"는 오해다. `ModernSingleton`의 `DCLSingleton`처럼 패턴을 올바르게 구현해도, 그 인스턴스가 노출하는 가변 상태(`Map<String, String> config`를 외부에서 변경 가능하게 반환하는 등)를 잘못 다루면 여전히 경쟁 조건이 생긴다. 패턴은 "생성 시점"의 스레드 안전성을 보장할 뿐, 그 이후의 상태 접근까지 자동으로 지켜주지 않는다.

## 평가 기준

이 글을 읽고 다음을 스스로 설명할 수 있다면 핵심을 이해한 것이다.

- Circuit Breaker가 "장애를 방지"하는 것이 아니라 "장애 전파를 격리"하는 것이라는 차이를 `CircuitBreakerOpenException`이 던져지는 시점을 근거로 설명할 수 있다.
- Actor 패턴과 Producer-Consumer 패턴이 상태를 소유하는 주체(액터 자신 vs 공유 큐)에서 어떻게 다른지 설명할 수 있다.
- CQRS·Event Sourcing이 "최종 일관성"을 전제로 한다는 것과, 이 지연이 사용자 경험에 문제가 되는 상황을 예로 들 수 있다.
- 동시성 패턴을 적용해도 노출된 가변 상태를 잘못 다루면 여전히 경쟁 조건이 생길 수 있다는 것을 예시로 설명할 수 있다.

---

## 결론: 분산 시대의 패턴 진화

분산 시스템과 동시성 환경은 디자인 패턴에 **새로운 차원**을 열어주었습니다:

### 핵심 인사이트

1. **상태 관리의 복잡성**: 분산 환경에서 상태 일관성 유지의 도전
2. **장애 내성**: Circuit Breaker, Bulkhead 패턴을 통한 회복력 구축
3. **비동기 통신**: Event-driven 아키텍처의 중요성 증대
4. **확장성 vs 일관성**: CAP 정리에 따른 트레이드오프 관리

> *"분산 시스템에서는 완벽한 해결책은 없다. 있는 것은 적절한 트레이드오프뿐이다."*

현대 개발자는 **단일 시스템의 패턴**과 **분산 시스템의 패턴**을 모두 이해해야 합니다. 각각의 장단점을 파악하고 상황에 맞는 최적의 선택을 하는 것이 핵심입니다!

## 토론 주제

1. **Circuit Breaker의 HALF_OPEN 단일 시험**: 이 글의 `CircuitBreaker` 구현은 `HALF_OPEN` 상태에서 시험 호출 하나의 성공/실패로 바로 `CLOSED`/`OPEN`을 결정한다. 트래픽이 많은 서비스에서 이 방식은 어떤 문제를 일으킬 수 있으며, Netflix Hystrix나 resilience4j 같은 라이브러리는 이를 어떻게 다르게 설계했는가?
2. **Event Sourcing의 재생 비용**: "패턴별 성능 특성"에서 Event Sourcing의 지연시간을 "높음"으로 평가한 근거는 조회 시 이벤트 재생이다. 이 비용을 줄이기 위해 흔히 쓰는 스냅샷(snapshot) 기법은 어떤 트레이드오프를 추가로 만드는가?
3. **CQRS 프로젝션의 최종 일관성**: `OrderQueryService`의 `orderSummaries` 맵은 이벤트를 구독해 갱신되므로 쓰기 직후 조회하면 최신 상태가 반영되지 않을 수 있다(최종 일관성). 이 지연이 사용자 경험에 문제가 되는 화면이 있다면, 어떤 보완 전략을 적용할 수 있는가?
4. **Actor Model과 Producer-Consumer의 경계**: 두 패턴 모두 메시지/아이템을 큐에 넣고 별도 스레드가 소비한다는 점에서 유사하다. 어떤 기준으로 둘 중 하나를 선택해야 하는가?
5. **CAP 정리를 적용한 패턴 선택의 함정**: "CAP 정리와 패턴 선택" 표는 CP/AP/CA를 패턴과 일대일로 매칭한다. 실제 시스템이 부분적으로만 CP거나 AP인 경우(예: 특정 API는 강한 일관성, 나머지는 최종 일관성)에도 이 단순 매칭이 유효한가?

## 참고 자료

- Michael T. Nygard, *Release It!: Design and Deploy Production-Ready Software* (2nd Edition, Pragmatic Bookshelf, 2018) — Circuit Breaker, Bulkhead 등 장애 격리 패턴의 원전.
- Chris Richardson, *Microservices Patterns* (Manning, 2018) — Saga, CQRS, Event Sourcing 등 분산 시스템 패턴의 체계적 정리.