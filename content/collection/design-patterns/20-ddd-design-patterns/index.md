---
collection_order: 200
title: "[Design Patterns] 도메인 주도 설계와 디자인 패턴"
description: "도메인 주도 설계(DDD) 철학과 GoF 디자인 패턴의 융합을 탐구합니다. Entity, Value Object, Aggregate, Repository 등 DDD의 핵심 빌딩 블록과 패턴의 결합을 통해 비즈니스 도메인을 효과적으로 표현하는 방법을 학습하고, CQRS, Event Sourcing 등 현대적 아키텍처 패턴까지 다룹니다."
image: "wordcloud.png"
date: 2024-12-20T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Domain Driven Design
- Architectural Patterns
- Enterprise Patterns
tags:
- Domain Driven Design
- DDD Building Blocks
- Entity Pattern
- Value Object
- Aggregate Root
- Repository Pattern
- Domain Service
- Application Service
- Ubiquitous Language
- Bounded Context
- Context Mapping
- Anti Corruption Layer
- CQRS Pattern
- Event Sourcing
- Domain Events
- Specification Pattern
- Factory Pattern
- Strategy Pattern
- Template Method
- Observer Pattern
- Command Pattern
- Enterprise Patterns
- Architectural Design
- Business Logic
- Domain Modeling
- Hexagonal Architecture
- Clean Architecture
- Microservices
- Event Driven Architecture
- Saga Pattern
- 도메인 주도 설계
- DDD 빌딩 블록
- 엔티티 패턴
- 값 객체
- 애그리거트 루트
- 리포지토리 패턴
- 도메인 서비스
- 애플리케이션 서비스
- 보편 언어
- 경계 컨텍스트
- 컨텍스트 매핑
- 부패 방지 계층
- CQRS 패턴
- 이벤트 소싱
- 도메인 이벤트
- 명세 패턴
- 팩토리 패턴
- 전략 패턴
- 템플릿 메서드
- 옵저버 패턴
- 커맨드 패턴
- 엔터프라이즈 패턴
- 아키텍처 설계
- 비즈니스 로직
- 도메인 모델링
- 헥사고날 아키텍처
- 클린 아키텍처
- 마이크로서비스
- 이벤트 주도 아키텍처
- 사가 패턴
---

Domain-Driven Design과 디자인 패턴의 융합을 탐구합니다. Aggregate, Repository, Domain Event 등 DDD 전술 패턴을 통한 비즈니스 도메인 모델링을 학습합니다.

## 서론: 도메인이 주도하는 설계

> *"좋은 소프트웨어의 핵심은 도메인을 잘 이해하고 표현하는 것이다. DDD는 이를 위한 철학이고, 디자인 패턴은 이를 구현하는 도구다."*

**Domain-Driven Design(DDD)**는 복잡한 비즈니스 도메인을 소프트웨어로 효과적으로 모델링하기 위한 접근법입니다. 전통적인 GoF 패턴들이 DDD 환경에서 어떻게 진화하고 활용되는지 살펴보겠습니다.

### DDD의 핵심 철학과 패턴의 융합
- **Ubiquitous Language**: 도메인 전문가와 개발자 간의 공통 언어
- **Bounded Context**: 모델의 경계와 Context Map
- **Domain Model**: 비즈니스 규칙과 로직의 중심화
- **Anti-Corruption Layer**: 레거시 시스템과의 통합

## DDD Building Blocks와 디자인 패턴

### Entity 패턴과 Identity 관리

```java
// Entity의 핵심 - Identity와 생명주기 관리
public abstract class Entity<ID> {
    protected ID id;
    
    protected Entity(ID id) {
        this.id = Objects.requireNonNull(id, "Entity ID cannot be null");
    }
    
    public ID getId() {
        return id;
    }
    
    // Identity-based equality
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Entity<?> entity = (Entity<?>) obj;
        return Objects.equals(id, entity.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
    
    // Template Method 패턴으로 비즈니스 규칙 검사
    protected final void checkBusinessRules(BusinessRule... rules) {
        for (BusinessRule rule : rules) {
            if (!rule.isSatisfied()) {
                throw new BusinessRuleViolationException(rule.getMessage());
            }
        }
    }
}

// Value Object 패턴 구현
public class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public Money(BigDecimal amount, Currency currency) {
        this.amount = Objects.requireNonNull(amount);
        this.currency = Objects.requireNonNull(currency);
    }
    
    public Money add(Money other) {
        ensureSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }
    
    private void ensureSameCurrency(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot operate on different currencies");
        }
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Money money = (Money) obj;
        return Objects.equals(amount, money.amount) && 
               Objects.equals(currency, money.currency);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }
}
```

### Aggregate Root 패턴

```java
// Aggregate Root - 복합체 패턴과 도메인 이벤트 결합
public abstract class AggregateRoot<ID> extends Entity<ID> {
    private final List<DomainEvent> domainEvents = new ArrayList<>();
    
    protected AggregateRoot(ID id) {
        super(id);
    }
    
    protected void addDomainEvent(DomainEvent event) {
        domainEvents.add(event);
    }
    
    public List<DomainEvent> getDomainEvents() {
        return Collections.unmodifiableList(domainEvents);
    }
    
    public void clearDomainEvents() {
        domainEvents.clear();
    }
}

// Order Aggregate 예시
public class Order extends AggregateRoot<OrderId> {
    private CustomerId customerId;
    private List<OrderLine> orderLines;
    private OrderStatus status;
    private Money totalAmount;
    
    // Factory Method 패턴
    public static Order create(CustomerId customerId, ShippingAddress address) {
        OrderId orderId = OrderId.generate();
        Order order = new Order(orderId, customerId);
        
        order.addDomainEvent(new OrderCreatedEvent(orderId, customerId));
        return order;
    }
    
    private Order(OrderId id, CustomerId customerId) {
        super(id);
        this.customerId = Objects.requireNonNull(customerId);
        this.orderLines = new ArrayList<>();
        this.status = OrderStatus.DRAFT;
    }
    
    public void addOrderLine(ProductId productId, int quantity, Money unitPrice) {
        checkBusinessRules(
            new OrderCanBeModifiedRule(this.status),
            new QuantityMustBePositiveRule(quantity)
        );
        
        OrderLine orderLine = new OrderLine(productId, quantity, unitPrice);
        orderLines.add(orderLine);
        
        addDomainEvent(new OrderLineAddedEvent(this.getId(), productId, quantity));
    }
    
    public void confirm() {
        checkBusinessRules(
            new OrderMustHaveItemsRule(this.orderLines),
            new OrderCanBeConfirmedRule(this.status)
        );
        
        this.status = OrderStatus.CONFIRMED;
        addDomainEvent(new OrderConfirmedEvent(this.getId(), this.totalAmount));
    }
}
```

## Repository 패턴과 데이터 접근

```java
// Repository의 도메인 중심 설계
public interface Repository<T extends AggregateRoot<ID>, ID> {
    void save(T aggregate);
    void delete(T aggregate);
    Optional<T> findById(ID id);
    boolean exists(ID id);
}

// 구체적인 Repository 인터페이스
public interface OrderRepository extends Repository<Order, OrderId> {
    List<Order> findByCustomerId(CustomerId customerId);
    List<Order> findByStatus(OrderStatus status);
    List<Order> findBySpecification(OrderSpecification specification);
}

// Repository 구현체 - Adapter 패턴
@Repository
public class JpaOrderRepository implements OrderRepository {
    private final JpaOrderDataRepository jpaRepository;
    private final OrderMapper orderMapper;
    
    @Override
    public void save(Order order) {
        OrderEntity entity = orderMapper.toEntity(order);
        jpaRepository.save(entity);
        
        // 도메인 이벤트 발행
        publishDomainEvents(order);
    }
    
    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepository.findById(id.getValue())
                           .map(orderMapper::toDomain);
    }
    
    private void publishDomainEvents(Order order) {
        order.getDomainEvents().forEach(event -> {
            DomainEventPublisher.instance().publish(event);
        });
        order.clearDomainEvents();
    }
}
```

## CQRS와 Event Sourcing 패턴

### Command Query Responsibility Segregation

```java
// Command 측면
public interface OrderCommandService {
    OrderId placeOrder(PlaceOrderCommand command);
    void cancelOrder(CancelOrderCommand command);
}

// Query 측면  
public interface OrderQueryService {
    OrderSummary getOrderSummary(OrderId orderId);
    List<OrderListItem> getOrdersByCustomer(CustomerId customerId);
}

// Domain Service - 여러 Aggregate를 조정
@Service
public class OrderProcessingService {
    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    
    @Transactional
    public OrderId processOrder(PlaceOrderCommand command) {
        // 1. 고객 조회 및 검증
        Customer customer = customerRepository.findById(command.getCustomerId())
            .orElseThrow(() -> new CustomerNotFoundException(command.getCustomerId()));
        
        // 2. 주문 생성
        Order order = Order.create(command.getCustomerId(), command.getShippingAddress());
        
        // 3. 주문 항목 추가
        for (OrderItemRequest item : command.getItems()) {
            order.addOrderLine(item.getProductId(), item.getQuantity(), item.getUnitPrice());
        }
        
        // 4. 주문 확정
        order.confirm();
        
        // 5. 저장
        orderRepository.save(order);
        
        return order.getId();
    }
}
```

### Event Sourcing 패턴

```java
// Event Store 패턴
public interface EventStore {
    void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion);
    List<DomainEvent> getEvents(String aggregateId);
}

// Event Sourcing을 지원하는 Aggregate Root
public abstract class EventSourcedAggregateRoot<ID> {
    private ID id;
    private int version = 0;
    private final List<DomainEvent> uncommittedEvents = new ArrayList<>();
    
    // Event를 적용하여 상태 복원
    public void loadFromHistory(List<DomainEvent> events) {
        for (DomainEvent event : events) {
            applyEvent(event, false);
            version++;
        }
    }
    
    // 새로운 Event 적용
    protected void applyEvent(DomainEvent event) {
        applyEvent(event, true);
    }
    
    private void applyEvent(DomainEvent event, boolean isNew) {
        // Event Handler 메서드 호출 로직
        handleEvent(event);
        
        if (isNew) {
            uncommittedEvents.add(event);
        }
    }
    
    protected abstract void handleEvent(DomainEvent event);
    
    public List<DomainEvent> getUncommittedEvents() {
        return Collections.unmodifiableList(uncommittedEvents);
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
}
```

## 실습 과제

### 과제 1: 도서관 도메인 모델링
다음 요구사항을 만족하는 도서관 시스템을 DDD로 설계하세요:

1. 회원은 도서를 대출하고 반납할 수 있다
2. 도서마다 대출 가능한 복본 수가 있다
3. 회원은 연체료가 있으면 새로운 대출을 할 수 없다
4. 인기 도서는 예약이 가능하다

### 과제 2: 전자상거래 주문 처리
Event Sourcing을 적용한 주문 처리 시스템을 구현하세요:

1. 주문 생성, 결제, 배송, 완료의 생명주기
2. 주문 취소 및 환불 처리
3. 재고 관리와의 연계
4. 주문 이력 추적 및 감사

## 토론 주제

1. **DDD vs Traditional Layered Architecture**: 언제 DDD를 선택해야 하는가?

2. **Aggregate 크기의 딜레마**: 큰 Aggregate vs 작은 Aggregate의 트레이드오프는?

3. **Event Sourcing의 복잡성**: Event Sourcing이 정말 필요한 상황은 언제인가?

4. **도메인 서비스 vs 애플리케이션 서비스**: 비즈니스 로직을 어디에 배치해야 하는가?

## 한눈에 보는 DDD 전술 패턴

### DDD 전술 패턴 요약표

| 패턴 | 핵심 역할 | 특징 | 적용 기준 |
|------|----------|------|----------|
| Entity | 식별자로 구분되는 객체 | 가변 상태, 생명주기 | ID로 동등성 판단 |
| Value Object | 값으로 구분되는 객체 | 불변, 교체 가능 | 속성으로 동등성 판단 |
| Aggregate | 일관성 경계 | 루트를 통한 접근, 트랜잭션 단위 | 불변식 보장 범위 |
| Repository | 영속성 추상화 | 컬렉션처럼 동작 | Aggregate당 하나 |
| Domain Service | 도메인 로직 수행 | 상태 없음, 도메인 동작 | Entity에 속하지 않는 로직 |
| Domain Event | 도메인 내 발생 사건 | 불변, 과거형 명명 | 상태 변경 알림 |
| Factory | 복잡한 객체 생성 | 생성 로직 캡슐화 | 복잡한 Aggregate 생성 |

### Entity vs Value Object 비교

| 비교 항목 | Entity | Value Object |
|----------|--------|-------------|
| 동등성 기준 | 식별자(ID) | 속성 값 |
| 가변성 | 가변 (상태 변경) | 불변 (새 객체 생성) |
| 생명주기 | 있음 (생성-소멸) | 없음 (교체) |
| 저장 방식 | 독립 테이블 | 임베디드/별도 테이블 |
| 예시 | User, Order, Product | Money, Address, DateRange |

### Aggregate 설계 원칙

| 원칙 | 설명 | 효과 |
|------|------|------|
| 작게 유지 | 필요한 것만 포함 | 동시성, 성능 향상 |
| 루트 통한 접근 | 외부는 루트만 참조 | 일관성 보장 |
| 참조는 ID로 | 다른 Aggregate는 ID 참조 | 결합도 감소 |
| 트랜잭션 경계 | 하나의 트랜잭션에서 하나만 | 확장성 확보 |
| 최종 일관성 | Aggregate 간은 이벤트로 | 분산 환경 적합 |

### Event Sourcing vs 전통적 저장

| 비교 항목 | Event Sourcing | 전통적 저장 |
|----------|---------------|-----------|
| 저장 대상 | 이벤트 (변경 이력) | 현재 상태 |
| 이력 추적 | 완전 (모든 변경) | 별도 구현 필요 |
| 복잡도 | 높음 | 낮음 |
| 성능 | 쓰기 빠름, 읽기 재구성 | 읽기 빠름 |
| 적합 상황 | 감사, 시간 여행 필요 | 일반적인 CRUD |

### CQRS 적용 가이드

| 상황 | CQRS 적합도 | 이유 |
|------|-----------|------|
| 읽기/쓰기 비율 불균형 | ★★★★★ | 독립적 최적화 가능 |
| 복잡한 조회 요구 | ★★★★☆ | 읽기 모델 최적화 |
| 단순 CRUD | ★☆☆☆☆ | 과도한 복잡성 |
| 이벤트 소싱과 함께 | ★★★★★ | 자연스러운 조합 |

### DDD 패턴과 GoF 패턴 연결

| DDD 패턴 | 관련 GoF 패턴 | 연결 방식 |
|---------|-------------|----------|
| Factory | Factory Method, Abstract Factory | 생성 캡슐화 |
| Repository | - (DDD 고유) | 컬렉션 추상화 |
| Domain Service | Strategy | 알고리즘 캡슐화 |
| Domain Event | Observer | 이벤트 발행/구독 |
| Aggregate | Composite | 객체 그룹화 |
| Specification | Strategy | 비즈니스 규칙 캡슐화 |

### 적용 체크리스트

| 체크 항목 | 설명 |
|----------|------|
| 복잡한 비즈니스 도메인인가? | DDD 적합성 판단 |
| 유비쿼터스 언어 정의했는가? | 도메인 전문가와 소통 |
| Bounded Context 식별했는가? | 도메인 경계 설정 |
| Aggregate 경계 적절한가? | 일관성 범위 검토 |
| Event Sourcing 필요한가? | 이력/감사 요구사항 확인 |

---

## 참고 자료

### 핵심 도서
- Eric Evans, "Domain-Driven Design" (2003)
- Vaughn Vernon, "Implementing Domain-Driven Design" (2013)
- Scott Millett, "Patterns, Principles, and Practices of Domain-Driven Design" (2015)

### 현대적 접근법
- Greg Young, "Event Sourcing" 
- Udi Dahan, "Advanced Distributed Systems Design"
- Martin Fowler, "Event Sourcing", "CQRS"

---

**"도메인의 복잡성을 코드로 표현하는 것이 DDD의 본질이다. 패턴은 그 표현을 위한 언어다."** 