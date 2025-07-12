---
draft: true
---
# 9장. 도메인 주도 설계 (DDD) 기초 및 전략적 설계

## 📋 학습 목표
- DDD의 핵심 철학과 개념을 이해한다
- Bounded Context와 Context Map의 실무 적용 방법을 습득한다
- 유비쿼터스 언어의 중요성과 구축 방법을 파악한다
- 이벤트 스토밍 기법을 통한 도메인 탐색 방법을 학습한다

---

## 9.1 DDD의 핵심 철학

### 9.1.1 DDD란 무엇인가?

도메인 주도 설계(Domain-Driven Design)는 **복잡한 비즈니스 도메인을 중심으로 소프트웨어를 설계하는 방법론**입니다.

#### DDD의 핵심 가치
- **도메인 중심성**: 비즈니스 도메인이 설계의 중심
- **모델 기반**: 도메인 모델을 통한 복잡성 관리
- **유비쿼터스 언어**: 팀 전체가 공유하는 공통 언어
- **지속적 학습**: 도메인에 대한 이해를 지속적으로 심화

### 9.1.2 DDD 적용 예제

```java
// DDD 적용 전: 비즈니스 로직이 서비스 계층에 산재
@Service
public class OrderService {
    public void processOrder(OrderDto orderDto) {
        if (orderDto.getTotalAmount().compareTo(BigDecimal.valueOf(1000)) > 0) {
            orderDto.setDiscountAmount(orderDto.getTotalAmount().multiply(BigDecimal.valueOf(0.1)));
        }
        orderRepository.save(convertToEntity(orderDto));
    }
}

// DDD 적용 후: 비즈니스 로직이 도메인 모델에 집중
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    
    public Order(CustomerId customerId, List<OrderItem> items) {
        this.id = OrderId.generate();
        this.customerId = customerId;
        this.items = new ArrayList<>(items);
        this.status = OrderStatus.DRAFT;
        this.totalAmount = calculateTotalAmount();
        validateOrder();
    }
    
    public void applyDiscount(DiscountPolicy discountPolicy) {
        Money discountAmount = discountPolicy.calculateDiscount(this);
        this.totalAmount = this.totalAmount.subtract(discountAmount);
    }
    
    public void confirm() {
        this.status = OrderStatus.CONFIRMED;
        DomainEvents.publish(new OrderConfirmedEvent(this.id));
    }
    
    private void validateOrder() {
        if (items.isEmpty()) {
            throw new EmptyOrderException("주문 항목이 없습니다");
        }
    }
}
```

---

## 9.2 Bounded Context

### 9.2.1 Bounded Context란?

Bounded Context는 **특정 도메인 모델이 유효한 경계**를 의미합니다. 같은 용어라도 컨텍스트에 따라 다른 의미를 가질 수 있습니다.

### 9.2.2 Bounded Context 식별 예제

```java
// 1. 주문 컨텍스트에서의 고객
public class Customer {
    private CustomerId id;
    private String name;
    private ShippingAddress defaultShippingAddress;
    // 주문에 필요한 정보만 포함
}

// 2. 고객 관리 컨텍스트에서의 고객
public class Customer {
    private CustomerId id;
    private PersonalInfo personalInfo;
    private ContactInfo contactInfo;
    private List<Address> addresses;
    private CustomerSegment segment;
    // 고객의 모든 정보를 관리
}

// 3. 마케팅 컨텍스트에서의 고객
public class Customer {
    private CustomerId id;
    private CustomerSegment segment;
    private List<PurchaseHistory> purchaseHistory;
    private List<MarketingPreference> preferences;
    // 마케팅에 필요한 정보에 집중
}
```

---

## 9.3 Context Map

### 9.3.1 통합 패턴

```java
// 1. Customer-Supplier 관계
@Upstream
public class ProductCatalogService {
    public ProductInfo getProductInfo(ProductId productId) {
        return productRepository.findById(productId);
    }
}

@Downstream  
public class OrderService {
    @Autowired
    private ProductCatalogService productCatalogService;
    
    public void createOrder(CreateOrderCommand command) {
        ProductInfo productInfo = productCatalogService.getProductInfo(command.getProductId());
        // 주문 생성 로직...
    }
}

// 2. Anti-Corruption Layer
@Component
public class ExternalPaymentAdapter {
    
    public PaymentResult processPayment(PaymentRequest request) {
        ExternalPaymentRequest externalRequest = convertToExternalFormat(request);
        ExternalPaymentResponse externalResponse = externalGateway.processPayment(externalRequest);
        return convertToInternalFormat(externalResponse);
    }
}
```

---

## 9.4 유비쿼터스 언어

### 9.4.1 유비쿼터스 언어의 중요성

```java
// 문제: 기술적 용어 중심
public class OrderRecord {
    private String state; // "CREATED", "PAID", "SHIPPED"
    
    public void updateState(String newState) {
        this.state = newState;
    }
}

// 개선: 도메인 언어 중심
public class Order {
    private OrderStatus status; // PLACED, CONFIRMED, SHIPPED
    
    public void confirm() {
        if (this.status != OrderStatus.PLACED) {
            throw new IllegalStateException("주문이 아직 접수되지 않았습니다");
        }
        this.status = OrderStatus.CONFIRMED;
    }
    
    public void ship() {
        if (this.status != OrderStatus.CONFIRMED) {
            throw new IllegalStateException("확정되지 않은 주문은 배송할 수 없습니다");
        }
        this.status = OrderStatus.SHIPPED;
    }
}
```

---

## 9.5 이벤트 스토밍

### 9.5.1 이벤트 스토밍이란?

이벤트 스토밍은 **도메인 이벤트를 중심으로 비즈니스 프로세스를 탐색하고 모델링하는 워크샵 기법**입니다.

### 9.5.2 이벤트 스토밍 예제

```java
// 1. 도메인 이벤트 발견
public class OrderPlaced extends DomainEvent {
    private OrderId orderId;
    private CustomerId customerId;
    private List<OrderItem> items;
}

public class PaymentProcessed extends DomainEvent {
    private PaymentId paymentId;
    private OrderId orderId;
    private Money amount;
}

// 2. 커맨드 식별
public class PlaceOrder implements Command {
    private CustomerId customerId;
    private List<OrderItem> items;
    private ShippingAddress shippingAddress;
}

// 3. 애그리게이트 식별
@Aggregate
public class Order {
    public static Order place(PlaceOrderCommand command) {
        Order order = new Order(command.getCustomerId(), command.getItems());
        DomainEvents.publish(new OrderPlaced(order.getId()));
        return order;
    }
}
```

---

## 🎯 핵심 요약

### DDD 전략적 설계 요소

| **개념** | **목적** | **적용 방법** |
|---------|---------|-------------|
| **Bounded Context** | 모델 경계 명확화 | 언어/조직 기준 식별 |
| **유비쿼터스 언어** | 의사소통 명확화 | 도메인 전문가 협업 |
| **이벤트 스토밍** | 도메인 탐색 | 워크샵 기법 활용 |
| **Context Map** | 통합 전략 정의 | 관계 패턴 적용 |

### 성공 요인
1. **도메인 전문가와의 긴밀한 협업**
2. **점진적 도메인 모델 발전**
3. **명확한 컨텍스트 경계 설정**
4. **팀 간 협업 방식 정의**

---

## 💭 생각해보기

1. 현재 시스템에서 Bounded Context를 어떻게 나눌 수 있을까?
2. 팀에서 사용하는 용어들이 유비쿼터스 언어로 적절히 정의되어 있는가?
3. 이벤트 스토밍을 통해 놓치고 있는 비즈니스 프로세스는 없을까?

---

## 📚 추가 학습 자료

### 도서
- "Domain-Driven Design" - Eric Evans
- "Implementing Domain-Driven Design" - Vaughn Vernon
- "Learning Domain-Driven Design" - Vlad Khononov

### 온라인 자료
- DDD Community 웹사이트
- EventStorming 공식 가이드 