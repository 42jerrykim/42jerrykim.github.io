---
collection_order: 201
draft: true
title: "[Design Patterns] 도메인 주도 설계와 디자인 패턴 실습 - 비즈니스 로직 설계"
description: "Domain-Driven Design과 디자인 패턴을 결합한 실습입니다. Aggregate, Repository, Factory, Service 등의 DDD 패턴과 기존 GoF 패턴을 조합하여 복잡한 비즈니스 도메인을 모델링하고, 실무에서 효과적인 도메인 계층 설계 기법을 학습합니다."
date: 2024-12-20T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Domain Driven Design
- Pattern Combinations
- Practice
- Business Logic
tags:
- DDD Practice
- Domain Driven Design
- Aggregate Pattern
- Repository Pattern
- Domain Service
- Factory Pattern
- Bounded Context
- Ubiquitous Language
- Business Logic
- Domain Modeling
- Entity Design
- Value Object
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Enterprise Patterns
- 도메인 주도 설계 실습
- DDD 실습
- 애그리게이트 패턴
- 리포지토리 패턴
- 도메인 서비스
- 팩토리 패턴
- 경계 컨텍스트
- 유비쿼터스 언어
- 비즈니스 로직
- 도메인 모델링
- 엔티티 설계
- 값 객체
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 엔터프라이즈 패턴
---

# DDD와 디자인 패턴 실습 - 비즈니스 로직 설계

## 🎯 **실습 목표**

1. 도서관 도메인 모델링으로 DDD 기본 개념 학습
2. 전자상거래 주문 처리를 통한 Event Sourcing 구현
3. Repository, Aggregate, Domain Service 패턴 실습

## 📋 **과제 1: 도서관 도메인 모델링**

### 요구사항
- 회원은 도서를 대출하고 반납할 수 있다
- 도서마다 대출 가능한 복본 수가 있다
- 회원은 연체료가 있으면 새로운 대출을 할 수 없다
- 인기 도서는 예약이 가능하다

### 기본 구조
```java
// Entity Base Class
public abstract class Entity<ID> {
    protected ID id;
    
    protected Entity(ID id) {
        this.id = Objects.requireNonNull(id);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Entity<?> entity = (Entity<?>) obj;
        return Objects.equals(id, entity.id);
    }
}

// Value Object 예시
public class ISBN {
    private final String value;
    
    public ISBN(String value) {
        if (!isValidISBN(value)) {
            throw new IllegalArgumentException("Invalid ISBN: " + value);
        }
        this.value = value;
    }
    
    private boolean isValidISBN(String isbn) {
        // TODO: ISBN 유효성 검사 구현
        return isbn != null && isbn.length() >= 10;
    }
}
```

### 구현 과제
```java
// TODO: 다음 클래스들을 구현하세요

// 1. Book Entity
public class Book extends Entity<BookId> {
    private ISBN isbn;
    private String title;
    private String author;
    private int availableCopies;
    private int totalCopies;
    
    // 비즈니스 메서드
    public boolean canBorrow() {
        // TODO: 대출 가능 여부 확인
    }
    
    public void borrow() {
        // TODO: 대출 처리
    }
    
    public void returnBook() {
        // TODO: 반납 처리
    }
}

// 2. Member Aggregate Root
public class Member extends AggregateRoot<MemberId> {
    private String name;
    private Email email;
    private Money overdueAmount;
    private List<Loan> currentLoans;
    
    // 비즈니스 규칙
    public boolean canBorrow() {
        // TODO: 연체료 확인, 대출 한도 확인
    }
    
    public void borrowBook(Book book) {
        // TODO: 도서 대출 로직
        // 1. 대출 가능 여부 확인
        // 2. 대출 기록 생성
        // 3. 도메인 이벤트 발행
    }
}

// 3. Loan Entity
public class Loan extends Entity<LoanId> {
    private BookId bookId;
    private MemberId memberId;
    private LocalDate borrowDate;
    private LocalDate dueDate;
    private LocalDate returnDate;
    private LoanStatus status;
    
    public boolean isOverdue() {
        // TODO: 연체 여부 확인
    }
    
    public Money calculateOverdueFee() {
        // TODO: 연체료 계산
    }
}
```

### Repository 인터페이스
```java
public interface BookRepository extends Repository<Book, BookId> {
    List<Book> findByTitle(String title);
    List<Book> findByAuthor(String author);
    List<Book> findAvailableBooks();
}

public interface MemberRepository extends Repository<Member, MemberId> {
    Optional<Member> findByEmail(Email email);
    List<Member> findMembersWithOverdueLoans();
}
```

## 📋 **과제 2: 전자상거래 주문 처리**

### Event Sourcing 구현
```java
// Domain Event Base
public abstract class DomainEvent {
    private final String eventId;
    private final Instant occurredOn;
    
    protected DomainEvent() {
        this.eventId = UUID.randomUUID().toString();
        this.occurredOn = Instant.now();
    }
}

// Order Events
public class OrderCreatedEvent extends DomainEvent {
    private final OrderId orderId;
    private final CustomerId customerId;
    private final Money totalAmount;
    
    // TODO: 생성자 및 getter 구현
}

public class OrderConfirmedEvent extends DomainEvent {
    // TODO: 구현
}

public class OrderCancelledEvent extends DomainEvent {
    // TODO: 구현
}
```

### Event Sourced Aggregate
```java
public class Order extends EventSourcedAggregateRoot<OrderId> {
    private CustomerId customerId;
    private List<OrderLine> orderLines;
    private OrderStatus status;
    private Money totalAmount;
    
    // Factory Method
    public static Order create(CustomerId customerId, ShippingAddress address) {
        Order order = new Order();
        order.applyEvent(new OrderCreatedEvent(OrderId.generate(), customerId));
        return order;
    }
    
    public void addOrderLine(ProductId productId, int quantity, Money unitPrice) {
        // TODO: 비즈니스 규칙 검증
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify confirmed order");
        }
        
        applyEvent(new OrderLineAddedEvent(this.id, productId, quantity, unitPrice));
    }
    
    public void confirm() {
        // TODO: 주문 확정 로직
        applyEvent(new OrderConfirmedEvent(this.id, this.totalAmount));
    }
    
    // Event Handler
    @Override
    protected void handleEvent(DomainEvent event) {
        if (event instanceof OrderCreatedEvent) {
            handle((OrderCreatedEvent) event);
        } else if (event instanceof OrderLineAddedEvent) {
            handle((OrderLineAddedEvent) event);
        } else if (event instanceof OrderConfirmedEvent) {
            handle((OrderConfirmedEvent) event);
        }
    }
    
    private void handle(OrderCreatedEvent event) {
        this.id = event.getOrderId();
        this.customerId = event.getCustomerId();
        this.status = OrderStatus.DRAFT;
        this.orderLines = new ArrayList<>();
    }
    
    // TODO: 다른 이벤트 핸들러들 구현
}
```

### Event Store
```java
public interface EventStore {
    void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion);
    List<DomainEvent> getEvents(String aggregateId);
    List<DomainEvent> getEvents(String aggregateId, int fromVersion);
}

public class InMemoryEventStore implements EventStore {
    private final Map<String, List<DomainEvent>> eventStreams = new ConcurrentHashMap<>();
    
    @Override
    public void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion) {
        // TODO: 이벤트 저장 로직 구현
        // 1. 버전 충돌 검사
        // 2. 이벤트 순서대로 저장
        // 3. 동시성 제어
    }
    
    @Override
    public List<DomainEvent> getEvents(String aggregateId) {
        // TODO: 이벤트 조회 로직 구현
        return eventStreams.getOrDefault(aggregateId, new ArrayList<>());
    }
}
```

## 📋 **과제 3: CQRS 패턴 구현**

### Command Side
```java
// Commands
public class PlaceOrderCommand {
    private final CustomerId customerId;
    private final ShippingAddress shippingAddress;
    private final List<OrderItemRequest> items;
    
    // TODO: 생성자, getter 구현
}

// Command Handler
@Service
public class OrderCommandHandler {
    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    
    @Transactional
    public OrderId handle(PlaceOrderCommand command) {
        // TODO: 주문 생성 로직 구현
        // 1. 고객 조회 및 검증
        // 2. 주문 생성
        // 3. 주문 항목 추가
        // 4. 주문 저장
        return null;
    }
}
```

### Query Side
```java
// Read Models
public class OrderSummary {
    private final String orderId;
    private final String customerName;
    private final BigDecimal totalAmount;
    private final String status;
    private final LocalDateTime orderDate;
    
    // TODO: 생성자, getter 구현
}

// Query Service
public interface OrderQueryService {
    OrderSummary getOrderSummary(OrderId orderId);
    List<OrderListItem> getOrdersByCustomer(CustomerId customerId);
    List<OrderListItem> getOrdersByDateRange(LocalDate from, LocalDate to);
}
```

## ✅ **완성도 체크리스트**

### DDD 기본 개념
- [ ] Entity와 Value Object 구분
- [ ] Aggregate Root 구현
- [ ] Repository 패턴 적용
- [ ] Domain Service 구현
- [ ] 비즈니스 규칙 캡슐화

### Event Sourcing
- [ ] Domain Event 정의
- [ ] Event Store 구현
- [ ] Event Handler 구현
- [ ] Aggregate 상태 복원
- [ ] 스냅샷 최적화

### CQRS
- [ ] Command/Query 분리
- [ ] Read Model 구현
- [ ] Command Handler 구현
- [ ] Query Service 구현
- [ ] 프로젝션 업데이트

## 🔍 **추가 도전 과제**

1. **Domain Event Publisher 구현**
   - 이벤트 발행/구독 메커니즘
   - 트랜잭션 경계 내 이벤트 처리

2. **Saga Pattern 구현**
   - 분산 트랜잭션 관리
   - 보상 트랜잭션 구현

3. **Specification Pattern**
   - 복잡한 비즈니스 규칙 조합
   - 동적 쿼리 생성

4. **Anti-Corruption Layer**
   - 레거시 시스템과의 통합
   - 도메인 모델 보호

## 🚀 **실무 적용 팁**

### Bounded Context 설계
```java
// 주문 컨텍스트
@BoundedContext("Order")
public class OrderContext {
    // 주문 관련 도메인 모델들
}

// 재고 컨텍스트
@BoundedContext("Inventory") 
public class InventoryContext {
    // 재고 관련 도메인 모델들
}
```

### Context Mapping
```java
// 컨텍스트 간 통합
public class OrderInventoryIntegration {
    // Anti-Corruption Layer
    public void reserveInventory(OrderCreatedEvent event) {
        // 주문 도메인 모델을 재고 도메인 모델로 변환
        InventoryReservationRequest request = mapToInventoryRequest(event);
        inventoryService.reserveItems(request);
    }
}
```

---

**💡 실습 팁**
- 도메인 전문가와 대화하며 Ubiquitous Language 구축
- 작은 Bounded Context부터 시작하여 점진적 확장
- Event Storming 기법으로 도메인 이벤트 발견
- 테스트 주도 개발로 비즈니스 규칙 검증 