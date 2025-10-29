---
draft: true
---
# 2장. 아키텍처 설계 원칙

## 학습 목표
- SOLID 원칙의 이해와 아키텍처 레벨에서의 적용
- DRY, KISS, YAGNI 등 실용적 원칙의 활용
- 관심사의 분리를 통한 모듈화 설계
- 의존성 역전을 통한 유연한 아키텍처 구성

---

## SOLID 원칙

SOLID 원칙은 Robert C. Martin이 제시한 객체지향 설계의 5가지 기본 원칙입니다. 이는 코드 레벨뿐만 아니라 아키텍처 레벨에서도 적용되어 유지보수가 용이하고 확장 가능한 시스템을 구축하는 데 도움이 됩니다.

### S - 단일 책임 원칙 (Single Responsibility Principle)

> "한 클래스는 하나의 책임만 가져야 한다."

아키텍처 레벨에서는 **"한 모듈/컴포넌트는 하나의 변경 이유만 가져야 한다"**로 확장됩니다.

#### 위반 사례
```java
// ❌ 나쁜 예: 여러 책임을 가진 클래스
public class UserManager {
    public void createUser(User user) { /* 사용자 생성 */ }
    public void sendEmail(String email, String message) { /* 이메일 전송 */ }
    public void generateReport() { /* 보고서 생성 */ }
    public void logActivity(String activity) { /* 로깅 */ }
}
```

#### 개선된 설계
```java
// ✅ 좋은 예: 책임별로 분리된 클래스들
public class UserService {
    public void createUser(User user) { /* 사용자 관리만 담당 */ }
}

public class EmailService {
    public void sendEmail(String email, String message) { /* 이메일 전송만 담당 */ }
}

public class ReportService {
    public void generateReport() { /* 보고서 생성만 담당 */ }
}

public class LoggingService {
    public void logActivity(String activity) { /* 로깅만 담당 */ }
}
```

#### 아키텍처 적용
```
마이크로서비스 아키텍처 예시:
├── 사용자 서비스 (User Service)
├── 주문 서비스 (Order Service)  
├── 결제 서비스 (Payment Service)
├── 알림 서비스 (Notification Service)
└── 로깅 서비스 (Logging Service)
```

### O - 개방-폐쇄 원칙 (Open-Closed Principle)

> "소프트웨어 개체는 확장에는 열려 있고, 수정에는 닫혀 있어야 한다."

#### 전략 패턴을 이용한 구현
```java
// 추상화
public interface PaymentProcessor {
    PaymentResult process(Payment payment);
}

// 구체적 구현들
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) {
        // 신용카드 결제 로직
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) {
        // PayPal 결제 로직
    }
}

// 새로운 결제 방식 추가 시 기존 코드 수정 없이 확장 가능
public class CryptoProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) {
        // 암호화폐 결제 로직
    }
}

public class PaymentService {
    private PaymentProcessor processor;
    
    public PaymentService(PaymentProcessor processor) {
        this.processor = processor;
    }
    
    public PaymentResult processPayment(Payment payment) {
        return processor.process(payment);
    }
}
```

#### 플러그인 아키텍처
```
Core System
    ↓
Plugin Interface
    ↓
├── Authentication Plugin
├── Logging Plugin
├── Caching Plugin
└── Monitoring Plugin
```

### L - 리스코프 치환 원칙 (Liskov Substitution Principle)

> "프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 한다."

#### 위반 사례
```java
// ❌ LSP 위반: 하위 클래스가 상위 클래스의 계약을 위반
public class Rectangle {
    protected int width, height;
    
    public void setWidth(int width) { this.width = width; }
    public void setHeight(int height) { this.height = height; }
    public int getArea() { return width * height; }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(int width) {
        this.width = width;
        this.height = width; // 정사각형이므로 높이도 같이 변경
    }
    
    @Override
    public void setHeight(int height) {
        this.width = height;
        this.height = height; // 정사각형이므로 너비도 같이 변경
    }
}

// 클라이언트 코드
public void testRectangle(Rectangle rect) {
    rect.setWidth(5);
    rect.setHeight(4);
    assert rect.getArea() == 20; // Square를 넘기면 실패!
}
```

#### 개선된 설계
```java
// ✅ LSP 준수: 공통 인터페이스 사용
public interface Shape {
    int getArea();
    void resize(double factor);
}

public class Rectangle implements Shape {
    private int width, height;
    
    @Override
    public int getArea() { return width * height; }
    
    @Override
    public void resize(double factor) {
        width = (int)(width * factor);
        height = (int)(height * factor);
    }
}

public class Square implements Shape {
    private int side;
    
    @Override
    public int getArea() { return side * side; }
    
    @Override
    public void resize(double factor) {
        side = (int)(side * factor);
    }
}
```

### I - 인터페이스 분리 원칙 (Interface Segregation Principle)

> "특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다."

#### 위반 사례
```java
// ❌ 너무 많은 책임을 가진 인터페이스
public interface Worker {
    void work();
    void eat();
    void sleep();
    void managePeople();
    void writeCode();
    void designArchitecture();
}

// 모든 구현체가 모든 메서드를 구현해야 함
public class Developer implements Worker {
    public void work() { /* 작업 */ }
    public void eat() { /* 식사 */ }
    public void sleep() { /* 수면 */ }
    public void managePeople() { /* 불필요한 구현 */ }
    public void writeCode() { /* 코딩 */ }
    public void designArchitecture() { /* 불필요한 구현 */ }
}
```

#### 개선된 설계
```java
// ✅ 역할별로 분리된 인터페이스
public interface Workable {
    void work();
}

public interface Eatable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public interface Manageable {
    void managePeople();
}

public interface Codeable {
    void writeCode();
}

public interface Architecturable {
    void designArchitecture();
}

// 필요한 인터페이스만 구현
public class Developer implements Workable, Eatable, Sleepable, Codeable {
    public void work() { /* 작업 */ }
    public void eat() { /* 식사 */ }
    public void sleep() { /* 수면 */ }
    public void writeCode() { /* 코딩 */ }
}

public class Architect implements Workable, Eatable, Sleepable, Architecturable {
    public void work() { /* 작업 */ }
    public void eat() { /* 식사 */ }
    public void sleep() { /* 수면 */ }
    public void designArchitecture() { /* 아키텍처 설계 */ }
}
```

### D - 의존성 역전 원칙 (Dependency Inversion Principle)

> "고수준 모듈은 저수준 모듈에 의존해서는 안 된다. 둘 다 추상화에 의존해야 한다."

#### 위반 사례
```java
// ❌ 고수준 모듈이 저수준 모듈에 직접 의존
public class OrderService {
    private MySQLDatabase database; // 구체적인 구현에 의존
    
    public OrderService() {
        this.database = new MySQLDatabase(); // 강한 결합
    }
    
    public void createOrder(Order order) {
        database.save(order);
    }
}
```

#### 개선된 설계
```java
// ✅ 추상화에 의존하는 설계
public interface OrderRepository {
    void save(Order order);
    Order findById(Long id);
}

public class OrderService {
    private OrderRepository repository; // 추상화에 의존
    
    public OrderService(OrderRepository repository) {
        this.repository = repository; // 의존성 주입
    }
    
    public void createOrder(Order order) {
        repository.save(order);
    }
}

// 구체적 구현들
public class MySQLOrderRepository implements OrderRepository {
    public void save(Order order) { /* MySQL 저장 로직 */ }
    public Order findById(Long id) { /* MySQL 조회 로직 */ }
}

public class MongoOrderRepository implements OrderRepository {
    public void save(Order order) { /* MongoDB 저장 로직 */ }
    public Order findById(Long id) { /* MongoDB 조회 로직 */ }
}
```

---

## DRY, KISS, YAGNI 원칙

### DRY (Don't Repeat Yourself)

> "모든 지식은 시스템 내에서 단일하고, 애매하지 않고, 권위있는 표현을 가져야 한다."

#### 코드 중복 제거
```java
// ❌ 코드 중복
public class UserController {
    public ResponseEntity<User> getUser(Long id) {
        if (id == null || id <= 0) {
            return ResponseEntity.badRequest().build();
        }
        // 사용자 조회 로직
    }
    
    public ResponseEntity<User> updateUser(Long id, User user) {
        if (id == null || id <= 0) {
            return ResponseEntity.badRequest().build();
        }
        // 사용자 업데이트 로직
    }
}

// ✅ 공통 로직 추출
public class UserController {
    public ResponseEntity<User> getUser(Long id) {
        if (!isValidId(id)) {
            return ResponseEntity.badRequest().build();
        }
        // 사용자 조회 로직
    }
    
    public ResponseEntity<User> updateUser(Long id, User user) {
        if (!isValidId(id)) {
            return ResponseEntity.badRequest().build();
        }
        // 사용자 업데이트 로직
    }
    
    private boolean isValidId(Long id) {
        return id != null && id > 0;
    }
}
```

#### 아키텍처 레벨에서의 DRY
```
공통 라이브러리 활용:
├── 공통 인증 모듈
├── 공통 로깅 모듈
├── 공통 예외 처리 모듈
├── 공통 유틸리티 모듈
└── 공통 설정 모듈
```

### KISS (Keep It Simple, Stupid)

> "단순함을 유지하라."

#### 복잡한 설계 vs 단순한 설계
```java
// ❌ 과도하게 복잡한 설계
public interface UserServiceFactory {
    UserService createUserService();
}

public class DatabaseUserServiceFactory implements UserServiceFactory {
    public UserService createUserService() {
        return new DatabaseUserService(
            new UserRepositoryFactory().createRepository(),
            new ValidationServiceFactory().createValidator(),
            new NotificationServiceFactory().createNotifier()
        );
    }
}

// ✅ 단순한 설계
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private ValidationService validationService;
    
    @Autowired
    private NotificationService notificationService;
    
    public User createUser(User user) {
        validationService.validate(user);
        User savedUser = userRepository.save(user);
        notificationService.notifyUserCreated(savedUser);
        return savedUser;
    }
}
```

### YAGNI (You Aren't Gonna Need It)

> "필요하지 않은 기능을 미리 구현하지 마라."

#### 과도한 미래 대비 vs 현재 요구사항 중심
```java
// ❌ 과도한 미래 대비
public class PaymentService {
    // 현재는 신용카드만 지원하지만 미래를 위해 복잡한 구조 구축
    private PaymentProcessorFactory factory;
    private PaymentStrategy strategy;
    private PaymentValidator validator;
    private PaymentAuditor auditor;
    private PaymentLogger logger;
    // ... 많은 미사용 컴포넌트들
    
    public PaymentResult processPayment(Payment payment) {
        // 실제로는 간단한 신용카드 처리만 함
        return creditCardProcessor.process(payment);
    }
}

// ✅ 현재 요구사항에 집중
public class PaymentService {
    private CreditCardProcessor creditCardProcessor;
    
    public PaymentResult processPayment(Payment payment) {
        return creditCardProcessor.process(payment);
    }
    
    // 새로운 결제 방식이 필요할 때 리팩토링으로 확장
}
```

---

## 관심사의 분리 (Separation of Concerns)

### 관심사 분리의 개념

관심사의 분리는 복잡한 시스템을 **서로 다른 관심사(책임)별로 분리**하여 각각 독립적으로 다룰 수 있게 하는 설계 원칙입니다.

### 분리의 차원

#### **수직적 분리 (계층 분리)**
```
┌─────────────────────┐
│   Presentation      │ ← 사용자 인터페이스
├─────────────────────┤
│   Business Logic    │ ← 비즈니스 규칙
├─────────────────────┤
│   Data Access       │ ← 데이터 접근
└─────────────────────┘
```

#### **수평적 분리 (기능별 분리)**
```
User Management | Order Processing | Payment Handling | Notification
```

#### **횡단 관심사 (Cross-cutting Concerns) 분리**
```java
@Service
@Transactional  // 트랜잭션 관리
@Cacheable     // 캐싱
@Secured       // 보안
@Monitored     // 모니터링
public class OrderService {
    public Order createOrder(Order order) {
        // 핵심 비즈니스 로직만 집중
        return orderRepository.save(order);
    }
}
```

###️ 실제 적용 예시: 전자상거래 시스템

#### MVC 패턴을 통한 관심사 분리
```java
// Controller: 요청 처리와 응답 관심사
@RestController
@RequestMapping("/api/products")
public class ProductController {
    @Autowired
    private ProductService productService;
    
    @GetMapping("/{id}")
    public ResponseEntity<ProductDto> getProduct(@PathVariable Long id) {
        Product product = productService.findById(id);
        ProductDto dto = ProductMapper.toDto(product);
        return ResponseEntity.ok(dto);
    }
}

// Service: 비즈니스 로직 관심사
@Service
public class ProductService {
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private InventoryService inventoryService;
    
    public Product findById(Long id) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
        
        // 재고 정보 추가
        int stock = inventoryService.getStock(id);
        product.setStockQuantity(stock);
        
        return product;
    }
}

// Repository: 데이터 접근 관심사
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByCategory(String category);
    List<Product> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
}
```

### 마이크로서비스에서의 관심사 분리

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway                              │
└─────────────────────────────────────────────────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  User Service   │  │ Product Service │  │  Order Service  │
│                 │  │                 │  │                 │
│ - 사용자 관리   │  │ - 상품 관리     │  │ - 주문 처리     │
│ - 인증/인가     │  │ - 카탈로그      │  │ - 주문 이력     │
│ - 프로필 관리   │  │ - 재고 관리     │  │ - 배송 추적     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   User DB       │  │  Product DB     │  │   Order DB      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 의존성 역전 원칙 심화

### 의존성 방향과 제어 역전

#### 전통적인 의존성 방향
```
High-level Module → Low-level Module
      ↑                    ↑
 OrderService ────────→ MySQLRepository
```

#### 의존성 역전 후
```
High-level Module → Abstraction ← Low-level Module
      ↑                 ↑              ↑
 OrderService ────→ Repository ←── MySQLRepository
```

###️ 헥사고날 아키텍처 (포트와 어댑터)

```
                    ┌─────────────────────┐
                    │   Web Controller    │ (Primary Adapter)
                    └─────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                  Application Core                       │
    │  ┌─────────────────┐         ┌─────────────────────┐   │
    │  │   Use Cases     │ ────→   │     Domain          │   │
    │  │   (Ports)       │         │     Model           │   │
    │  └─────────────────┘         └─────────────────────┘   │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Database Adapter    │ (Secondary Adapter)
                    └─────────────────────┘
```

#### 구현 예시
```java
// 포트 (인터페이스)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
}

public interface PaymentGateway {
    PaymentResult processPayment(Payment payment);
}

// 도메인 서비스 (애플리케이션 코어)
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    
    public OrderService(OrderRepository orderRepository, 
                       PaymentGateway paymentGateway) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
    }
    
    public void processOrder(Order order) {
        // 도메인 로직
        PaymentResult result = paymentGateway.processPayment(order.getPayment());
        if (result.isSuccessful()) {
            orderRepository.save(order);
        }
    }
}

// 어댑터 (구현)
@Repository
public class JpaOrderRepository implements OrderRepository {
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public void save(Order order) {
        entityManager.persist(order);
    }
    
    @Override
    public Optional<Order> findById(OrderId id) {
        return Optional.ofNullable(entityManager.find(Order.class, id));
    }
}

@Component
public class StripePaymentGateway implements PaymentGateway {
    @Override
    public PaymentResult processPayment(Payment payment) {
        // Stripe API 호출
        return new PaymentResult(true, "Payment successful");
    }
}
```

### 의존성 주입 (Dependency Injection)

#### 생성자 주입 (권장)
```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    
    // 생성자 주입 - 불변성 보장, 필수 의존성 명시
    public OrderService(OrderRepository orderRepository, 
                       PaymentService paymentService) {
        this.orderRepository = orderRepository;
        this.paymentService = paymentService;
    }
}
```

#### 설정자 주입
```java
@Service
public class OrderService {
    private OrderRepository orderRepository;
    private PaymentService paymentService;
    
    @Autowired
    public void setOrderRepository(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }
    
    @Autowired
    public void setPaymentService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

#### 필드 주입 (권장하지 않음)
```java
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository; // 테스트하기 어려움
    
    @Autowired
    private PaymentService paymentService; // 의존성이 숨겨짐
}
```

---

## 핵심 요약

### 설계 원칙 정리

| 원칙 | 핵심 개념 | 아키텍처 적용 |
|------|-----------|---------------|
| **SRP** | 한 가지 책임만 | 마이크로서비스, 모듈 분리 |
| **OCP** | 확장 열림, 수정 닫힘 | 플러그인 아키텍처, 전략 패턴 |
| **LSP** | 하위 타입 치환 가능 | 인터페이스 설계, API 호환성 |
| **ISP** | 인터페이스 분리 | API 설계, 클라이언트 맞춤형 인터페이스 |
| **DIP** | 추상화에 의존 | 계층형 아키텍처, 의존성 주입 |
| **DRY** | 중복 제거 | 공통 라이브러리, 재사용 컴포넌트 |
| **KISS** | 단순성 유지 | 복잡성 최소화, 명확한 설계 |
| **YAGNI** | 필요한 것만 구현 | 점진적 개발, 오버 엔지니어링 방지 |

### 실무 적용 가이드

1. **프로젝트 초기**: YAGNI와 KISS 원칙 중심
2. **기능 확장 시**: OCP와 DIP 원칙 활용
3. **코드 리뷰**: SRP와 ISP 원칙 점검
4. **리팩토링**: DRY 원칙과 관심사 분리 적용

### 다음 장 연결고리
다음 장에서는 이러한 설계 원칙들이 어떻게 구체적인 **아키텍처 패턴과 스타일**로 구현되는지 학습하겠습니다. 계층화 아키텍처부터 이벤트 기반 아키텍처까지 다양한 패턴들을 살펴볼 예정입니다.

---

## 생각해보기

1. **현재 작업하고 있는 프로젝트**에서 SOLID 원칙을 위반하는 부분이 있다면 어떻게 개선할 수 있을까요?

2. **DRY 원칙과 KISS 원칙이 충돌**하는 상황을 경험한 적이 있나요? 어떻게 해결했나요?

3. **의존성 역전 원칙**을 적용하면 코드가 복잡해질 수 있습니다. 언제 적용하고 언제 적용하지 말아야 할까요?

---

## 추가 학습 자료

### 필수 도서
- "Clean Code" - Robert C. Martin
- "Effective Java" - Joshua Bloch  
- "Design Patterns" - Gang of Four
- "Refactoring" - Martin Fowler

### 온라인 자료
- [SOLID Principles](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Clean Architecture Blog](https://blog.cleancoder.com/)
- [Refactoring Guru - Design Principles](https://refactoring.guru/design-patterns) 