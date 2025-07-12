---
draft: true
---
# 10장. DDD 전술적 설계

## 📋 학습 목표
- Entity와 Value Object의 차이점과 설계 방법을 이해한다
- Aggregate의 개념과 설계 원칙을 습득한다
- Repository와 Domain Service의 역할을 파악한다
- 도메인 이벤트의 설계와 활용 방법을 학습한다

---

## 10.1 Entity (엔티티)

### 10.1.1 Entity란?

Entity는 **고유한 식별자를 가지며 생명주기 동안 연속성을 유지하는 도메인 객체**입니다.

### 10.1.2 Entity 구현 예제

```java
// 고객 Entity
public class Customer {
    private CustomerId id;
    private String name;
    private Email email;
    private CustomerStatus status;
    
    public Customer(CustomerId id, String name, Email email) {
        this.id = Objects.requireNonNull(id);
        this.name = Objects.requireNonNull(name);
        this.email = Objects.requireNonNull(email);
        this.status = CustomerStatus.ACTIVE;
        
        validateName(name);
    }
    
    public void changeEmail(Email newEmail) {
        if (this.status == CustomerStatus.SUSPENDED) {
            throw new IllegalStateException("정지된 고객은 이메일을 변경할 수 없습니다");
        }
        
        this.email = Objects.requireNonNull(newEmail);
        DomainEvents.publish(new CustomerEmailChangedEvent(this.id, newEmail));
    }
    
    public void suspend(String reason) {
        if (this.status == CustomerStatus.SUSPENDED) {
            throw new IllegalStateException("이미 정지된 고객입니다");
        }
        
        this.status = CustomerStatus.SUSPENDED;
        DomainEvents.publish(new CustomerSuspendedEvent(this.id, reason));
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Customer customer = (Customer) obj;
        return Objects.equals(id, customer.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
    
    private void validateName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("이름은 필수입니다");
        }
    }
}
```

---

## 10.2 Value Object (값 객체)

### 10.2.1 Value Object란?

Value Object는 **식별자가 없고 값 자체로 동등성을 판단하는 불변 객체**입니다.

### 10.2.2 Value Object 구현 예제

```java
// 이메일 Value Object
public class Email {
    private final String value;
    
    public Email(String value) {
        validateEmail(value);
        this.value = value.toLowerCase();
    }
    
    private void validateEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            throw new IllegalArgumentException("이메일은 필수입니다");
        }
        
        String emailRegex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
        if (!email.matches(emailRegex)) {
            throw new IllegalArgumentException("올바른 이메일 형식이 아닙니다");
        }
    }
    
    public String getDomain() {
        return value.substring(value.indexOf("@") + 1);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Email email = (Email) obj;
        return Objects.equals(value, email.value);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(value);
    }
    
    public String getValue() {
        return value;
    }
}

// 금액 Value Object
public class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public static final Money ZERO = new Money(BigDecimal.ZERO, Currency.getInstance("KRW"));
    
    public Money(BigDecimal amount, Currency currency) {
        this.amount = Objects.requireNonNull(amount);
        this.currency = Objects.requireNonNull(currency);
    }
    
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("다른 통화는 더할 수 없습니다");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
    
    public Money multiply(BigDecimal multiplier) {
        return new Money(this.amount.multiply(multiplier), this.currency);
    }
    
    public boolean isGreaterThan(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("다른 통화와 비교할 수 없습니다");
        }
        return this.amount.compareTo(other.amount) > 0;
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

---

## 10.3 Aggregate (애그리게이트)

### 10.3.1 Aggregate란?

Aggregate는 **데이터 변경의 단위로 취급되는 연관된 객체들의 클러스터**입니다.

### 10.3.2 Aggregate 구현 예제

```java
// 주문 Aggregate
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    
    protected Order() {
        this.items = new ArrayList<>();
    }
    
    public static Order create(CustomerId customerId, List<OrderItem> items) {
        Order order = new Order();
        order.id = OrderId.generate();
        order.customerId = Objects.requireNonNull(customerId);
        order.items = new ArrayList<>(Objects.requireNonNull(items));
        order.status = OrderStatus.PENDING;
        
        order.validateItems();
        order.calculateTotalAmount();
        
        DomainEvents.publish(new OrderCreatedEvent(order.id, order.customerId));
        return order;
    }
    
    public void addItem(ProductId productId, int quantity, Money unitPrice) {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("대기 중인 주문만 항목을 추가할 수 있습니다");
        }
        
        items.add(new OrderItem(productId, quantity, unitPrice));
        calculateTotalAmount();
    }
    
    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("대기 중인 주문만 확정할 수 있습니다");
        }
        
        this.status = OrderStatus.CONFIRMED;
        DomainEvents.publish(new OrderConfirmedEvent(this.id, this.totalAmount));
    }
    
    private void validateItems() {
        if (items.isEmpty()) {
            throw new IllegalArgumentException("주문 항목이 없습니다");
        }
    }
    
    private void calculateTotalAmount() {
        this.totalAmount = items.stream()
            .map(OrderItem::getAmount)
            .reduce(Money.ZERO, Money::add);
    }
    
    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(items);
    }
}

// 주문 항목 Entity (Aggregate 내부)
public class OrderItem {
    private OrderItemId id;
    private ProductId productId;
    private int quantity;
    private Money unitPrice;
    
    OrderItem(ProductId productId, int quantity, Money unitPrice) {
        this.id = OrderItemId.generate();
        this.productId = Objects.requireNonNull(productId);
        this.unitPrice = Objects.requireNonNull(unitPrice);
        this.quantity = quantity;
        
        if (quantity <= 0) {
            throw new IllegalArgumentException("수량은 0보다 커야 합니다");
        }
    }
    
    public Money getAmount() {
        return unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
}
```

---

## 10.4 Repository 패턴

### 10.4.1 Repository 구현 예제

```java
// Repository 인터페이스 (도메인 계층)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
    List<Order> findByCustomerId(CustomerId customerId);
    List<Order> findByStatus(OrderStatus status);
}

// Repository 구현체 (인프라 계층)
@Repository
public class JpaOrderRepository implements OrderRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public void save(Order order) {
        OrderJpaEntity entity = OrderMapper.toJpaEntity(order);
        entityManager.merge(entity);
    }
    
    @Override
    public Optional<Order> findById(OrderId id) {
        OrderJpaEntity entity = entityManager.find(OrderJpaEntity.class, id.getValue());
        return Optional.ofNullable(entity)
                      .map(OrderMapper::toDomainModel);
    }
    
    @Override
    public List<Order> findByCustomerId(CustomerId customerId) {
        TypedQuery<OrderJpaEntity> query = entityManager.createQuery(
            "SELECT o FROM OrderJpaEntity o WHERE o.customerId = :customerId", 
            OrderJpaEntity.class
        );
        query.setParameter("customerId", customerId.getValue());
        
        return query.getResultList().stream()
                   .map(OrderMapper::toDomainModel)
                   .collect(Collectors.toList());
    }
}
```

---

## 10.5 Domain Service

### 10.5.1 Domain Service 구현 예제

```java
// 할인 정책 Domain Service
@Service
public class DiscountPolicyService {
    
    public Money calculateDiscount(Order order, Customer customer) {
        Money discountAmount = Money.ZERO;
        
        // VIP 고객 할인
        if (customer.isVip()) {
            discountAmount = discountAmount.add(
                order.getTotalAmount().multiply(BigDecimal.valueOf(0.1))
            );
        }
        
        // 대량 주문 할인
        if (order.getTotalAmount().isGreaterThan(new Money(BigDecimal.valueOf(100000), Currency.getInstance("KRW")))) {
            discountAmount = discountAmount.add(
                order.getTotalAmount().multiply(BigDecimal.valueOf(0.05))
            );
        }
        
        return discountAmount;
    }
}

// 재고 확인 Domain Service
@Service
public class InventoryService {
    
    private final InventoryRepository inventoryRepository;
    
    public InventoryService(InventoryRepository inventoryRepository) {
        this.inventoryRepository = inventoryRepository;
    }
    
    public boolean isAvailable(ProductId productId, int requestedQuantity) {
        Optional<Inventory> inventory = inventoryRepository.findByProductId(productId);
        return inventory.map(inv -> inv.getAvailableQuantity() >= requestedQuantity)
                       .orElse(false);
    }
    
    public void reserveItems(List<OrderItem> items) {
        for (OrderItem item : items) {
            Inventory inventory = inventoryRepository.findByProductId(item.getProductId())
                .orElseThrow(() -> new ProductNotFoundException("상품을 찾을 수 없습니다"));
                
            inventory.reserve(item.getQuantity());
            inventoryRepository.save(inventory);
        }
    }
}
```

---

## 🎯 핵심 요약

### DDD 전술적 설계 요소

| **요소** | **특징** | **사용 시기** |
|---------|---------|-------------|
| **Entity** | 고유 식별자, 변경 가능 | 생명주기가 중요한 객체 |
| **Value Object** | 불변, 값 기반 동등성 | 개념적 전체를 나타내는 값 |
| **Aggregate** | 일관성 경계 | 트랜잭션 단위 |
| **Repository** | 영속성 추상화 | Aggregate 저장/조회 |
| **Domain Service** | 도메인 로직 캡슐화 | 여러 객체 간 협력 |

### 설계 원칙
1. **Aggregate 경계를 명확히 설정**
2. **Value Object 활용으로 표현력 향상**
3. **Domain Service로 복잡한 로직 분리**
4. **Repository를 통한 영속성 추상화**

---

## 💭 생각해보기

1. 현재 시스템에서 Entity와 Value Object를 어떻게 구분할 수 있을까?
2. Aggregate 경계를 잘못 설정했을 때 발생할 수 있는 문제는?
3. Domain Service와 Application Service의 차이점은 무엇인가?

---

## 📚 추가 학습 자료

### 도서
- "Implementing Domain-Driven Design" - Vaughn Vernon
- "Domain-Driven Design Distilled" - Vaughn Vernon

### 온라인 자료
- DDD Reference by Eric Evans 