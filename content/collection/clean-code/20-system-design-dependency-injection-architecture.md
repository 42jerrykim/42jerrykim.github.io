---
draft: true
---
# 11장: 시스템

## 강의 목표
- 시스템 레벨에서의 Clean Code 원칙 이해
- 관심사의 분리와 의존성 주입 개념 습득
- 시스템 아키텍처 설계 및 확장 전략 학습

## 내용 구성 전략

### 11.1 도시를 세운다면?
**접근 방법**:
- 도시 건설 비유를 통한 시스템 설계 이해
- 추상화와 모듈화의 중요성

**주요 내용**:
- 도시가 돌아가는 이유는 적절한 추상화와 모듈화 때문이다
- 깨끗한 코드를 구현하면 낮은 추상화 수준에서 관심사를 분리하기 쉬워진다
- 이 장에서는 높은 추상화 수준, 즉 시스템 수준에서도 깨끗함을 유지하는 방법을 살펴본다

### 11.2 시스템 제작과 시스템 사용을 분리하라
**접근 방법**:
- 제작(construction)과 사용(use)의 분리 필요성
- 소프트웨어 시스템에서의 '시작' 단계 분리

**주요 내용**:
- 소프트웨어 시스템은 (애플리케이션 객체를 제작하고 의존성을 서로 '연결'하는) 준비 과정과 (준비 과정 이후에 이어지는) 런타임 로직을 분리해야 한다
- 시작 단계는 모든 애플리케이션이 풀어야 할 '관심사'다
- Main 분리, 팩토리, 의존성 주입 등의 기법을 활용한다

#### 11.2.1 Main 분리
**접근 방법**:
- main 함수를 통한 시스템 생성과 비즈니스 로직 분리
- 제어 흐름의 명확한 구분

**주요 내용**:
- 시스템 생성과 시스템 사용을 분리하는 한 가지 방법으로, 생성과 관련한 코드는 모두 main이나 main이 호출하는 모듈로 옮기고, 나머지 시스템은 모든 객체가 생성되었고 모든 의존성이 연결되었다고 가정한다

**Main 분리 예시**:
```java
// Bad: 생성과 사용이 뒤섞임
public class MyApplication {
    private OrderService orderService;
    private PaymentService paymentService;
    
    public void processOrder(Order order) {
        // 생성 로직이 비즈니스 로직과 섞임
        if (orderService == null) {
            orderService = new OrderServiceImpl(new DatabaseRepository());
        }
        if (paymentService == null) {
            paymentService = new PaymentServiceImpl(new CreditCardProcessor());
        }
        
        // 비즈니스 로직
        orderService.validateOrder(order);
        paymentService.processPayment(order.getPayment());
    }
}

// Good: Main에서 생성, 애플리케이션에서는 사용만
public class Main {
    public static void main(String[] args) {
        // 시스템 생성
        DatabaseRepository repository = new DatabaseRepository();
        OrderService orderService = new OrderServiceImpl(repository);
        
        CreditCardProcessor processor = new CreditCardProcessor();
        PaymentService paymentService = new PaymentServiceImpl(processor);
        
        // 애플리케이션 실행
        MyApplication app = new MyApplication(orderService, paymentService);
        app.run();
    }
}

public class MyApplication {
    private final OrderService orderService;
    private final PaymentService paymentService;
    
    public MyApplication(OrderService orderService, PaymentService paymentService) {
        this.orderService = orderService;
        this.paymentService = paymentService;
    }
    
    public void processOrder(Order order) {
        // 오직 비즈니스 로직만
        orderService.validateOrder(order);
        paymentService.processPayment(order.getPayment());
    }
}
```

#### 11.2.2 팩토리
**접근 방법**:
- Abstract Factory 패턴을 통한 객체 생성 캡슐화
- 애플리케이션이 객체 생성 시점을 결정하지만 생성 방법은 모르게 하기

**주요 내용**:
- 때로는 객체가 생성되는 시점을 애플리케이션이 결정할 필요도 있다
- 이때는 ABSTRACT FACTORY 패턴을 사용한다
- 그러면 LineItem을 생성하는 시점은 애플리케이션이 결정하지만 LineItem을 생성하는 코드는 애플리케이션이 모른다

**팩토리 패턴 예시**:
```java
// 팩토리 인터페이스
public interface LineItemFactory {
    LineItem makeLineItem(String itemName, int quantity, Money price);
}

// 구체적인 팩토리 구현
public class LineItemFactoryImpl implements LineItemFactory {
    private OrderLineDatabase database;
    
    public LineItemFactoryImpl(OrderLineDatabase database) {
        this.database = database;
    }
    
    public LineItem makeLineItem(String itemName, int quantity, Money price) {
        LineItem lineItem = new LineItemImpl(itemName, quantity, price);
        database.save(lineItem);
        return lineItem;
    }
}

// 애플리케이션 코드
public class OrderProcessor {
    private LineItemFactory lineItemFactory;
    
    public OrderProcessor(LineItemFactory lineItemFactory) {
        this.lineItemFactory = lineItemFactory;
    }
    
    public void processOrder(String[] items) {
        for (String item : items) {
            // 생성 시점은 여기서 결정하지만 생성 방법은 팩토리가 담당
            LineItem lineItem = lineItemFactory.makeLineItem(
                item.getName(), item.getQuantity(), item.getPrice());
            // 비즈니스 로직 계속...
        }
    }
}
```

#### 11.2.3 의존성 주입
**접근 방법**:
- Inversion of Control 컨테이너와 Dependency Injection
- 제어의 역전을 통한 의존성 관리

**주요 내용**:
- 사용과 제작을 분리하는 강력한 메커니즘 하나가 의존성 주입(Dependency Injection, DI)이다
- 제어 역전(Inversion of Control, IoC) 기법을 의존성 관리에 적용한 메커니즘이다
- 한 객체가 맡은 보조 책임을 새로운 객체에게 전적으로 떠넘긴다

**의존성 주입 예시**:
```java
// Before: 의존성을 직접 생성
public class OrderService {
    private EmailService emailService;
    private DatabaseRepository repository;
    
    public OrderService() {
        // 의존성을 직접 생성 (하드 의존성)
        this.emailService = new SmtpEmailService("smtp.gmail.com");
        this.repository = new MySqlRepository("jdbc:mysql://localhost/orders");
    }
    
    public void processOrder(Order order) {
        repository.save(order);
        emailService.sendConfirmation(order.getCustomerEmail());
    }
}

// After: 의존성 주입 사용
public class OrderService {
    private final EmailService emailService;
    private final DatabaseRepository repository;
    
    // 생성자 주입
    public OrderService(EmailService emailService, DatabaseRepository repository) {
        this.emailService = emailService;
        this.repository = repository;
    }
    
    public void processOrder(Order order) {
        repository.save(order);
        emailService.sendConfirmation(order.getCustomerEmail());
    }
}

// DI 컨테이너 설정 (Spring 예시)
@Configuration
public class ApplicationConfig {
    
    @Bean
    public EmailService emailService() {
        return new SmtpEmailService("smtp.gmail.com");
    }
    
    @Bean
    public DatabaseRepository repository() {
        return new MySqlRepository("jdbc:mysql://localhost/orders");
    }
    
    @Bean
    public OrderService orderService(EmailService emailService, DatabaseRepository repository) {
        return new OrderService(emailService, repository);
    }
}
```

### 11.3 확장
**접근 방법**:
- 소프트웨어 시스템의 점진적 확장 전략
- "처음부터 올바르게" vs "점진적 개선"

**주요 내용**:
- 소프트웨어 시스템은 물리적인 시스템과 다르다. 관심사를 적절히 분리해 관리한다면 소프트웨어 아키텍처는 점진적으로 발전할 수 있다
- "처음부터 올바르게" 시스템을 만들 수 있다는 믿음은 미신이다
- 대신에 우리는 오늘 주어진 사용자 스토리에 맞춰 시스템을 구현해야 한다
- 내일은 새로운 스토리에 맞춰 시스템을 조정하고 확장하면 된다

**확장 가능한 시스템 예시**:
```java
// 초기 버전: 간단한 구현
public interface PaymentProcessor {
    boolean processPayment(PaymentInfo payment);
}

public class SimplePaymentProcessor implements PaymentProcessor {
    public boolean processPayment(PaymentInfo payment) {
        // 단순한 결제 처리
        return payment.getAmount() > 0;
    }
}

// 확장된 버전: 다양한 결제 방법 지원
public class AdvancedPaymentProcessor implements PaymentProcessor {
    private Map<PaymentType, PaymentHandler> handlers;
    
    public AdvancedPaymentProcessor() {
        handlers = new HashMap<>();
        handlers.put(PaymentType.CREDIT_CARD, new CreditCardHandler());
        handlers.put(PaymentType.PAYPAL, new PayPalHandler());
        handlers.put(PaymentType.BANK_TRANSFER, new BankTransferHandler());
    }
    
    public boolean processPayment(PaymentInfo payment) {
        PaymentHandler handler = handlers.get(payment.getType());
        return handler != null && handler.process(payment);
    }
}
```

#### 11.3.1 횡단(cross-cutting) 관심사
**접근 방법**:
- AOP(Aspect-Oriented Programming) 개념 소개
- 관심사의 분리를 통한 모듈화

**주요 내용**:
- 이론적으로는 독립적인 형태로 구분될 수 있지만 실제로는 코드에 산재하는 관심사들이 있다
- 영속성과 같은 관심사는 애플리케이션의 자연스러운 객체 경계를 넘나드는 경향이 있다
- 모든 객체가 전반적으로 동일한 방식을 이용하게 만들어야 한다

**횡단 관심사 예시**:
```java
// Bad: 비즈니스 로직과 횡단 관심사가 뒤섞임
public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);
    
    @Transactional
    public void processOrder(Order order) {
        logger.info("Processing order: " + order.getId());
        
        // 보안 검사
        if (!SecurityContext.getCurrentUser().hasPermission("PROCESS_ORDER")) {
            logger.warn("Unauthorized access attempt");
            throw new SecurityException("Not authorized");
        }
        
        try {
            // 실제 비즈니스 로직
            validateOrder(order);
            saveOrder(order);
            sendConfirmation(order);
            
            logger.info("Order processed successfully: " + order.getId());
        } catch (Exception e) {
            logger.error("Error processing order: " + order.getId(), e);
            throw e;
        }
    }
}

// Good: AOP를 사용한 관심사 분리
@Component
public class OrderService {
    
    @Loggable
    @SecuredOperation("PROCESS_ORDER")
    @Transactional
    public void processOrder(Order order) {
        // 오직 비즈니스 로직만
        validateOrder(order);
        saveOrder(order);
        sendConfirmation(order);
    }
}

// 횡단 관심사를 처리하는 Aspect
@Aspect
@Component
public class LoggingAspect {
    
    @Before("@annotation(Loggable)")
    public void logBefore(JoinPoint joinPoint) {
        logger.info("Executing: " + joinPoint.getSignature().getName());
    }
    
    @AfterReturning("@annotation(Loggable)")
    public void logAfterSuccess(JoinPoint joinPoint) {
        logger.info("Successfully executed: " + joinPoint.getSignature().getName());
    }
    
    @AfterThrowing(pointcut = "@annotation(Loggable)", throwing = "exception")
    public void logAfterException(JoinPoint joinPoint, Exception exception) {
        logger.error("Exception in: " + joinPoint.getSignature().getName(), exception);
    }
}
```

### 11.4 자바 프록시
**접근 방법**:
- 동적 프록시를 통한 횡단 관심사 처리
- JDK 동적 프록시와 CGLIB의 차이점

**주요 내용**:
- 자바 프록시는 단순한 상황에 적합하다
- 개별 객체나 클래스에서 메서드 호출을 감싸는 경우가 좋은 예다
- 하지만 JDK에서 제공하는 동적 프록시는 인터페이스만 지원한다

**프록시 패턴 예시**:
```java
// 프록시를 사용한 횡단 관심사 처리
public interface BankAccount {
    void deposit(double amount);
    void withdraw(double amount);
    double getBalance();
}

public class BankAccountImpl implements BankAccount {
    private double balance;
    
    public void deposit(double amount) {
        balance += amount;
    }
    
    public void withdraw(double amount) {
        if (balance >= amount) {
            balance -= amount;
        }
    }
    
    public double getBalance() {
        return balance;
    }
}

// 로깅 프록시
public class LoggingBankAccountProxy implements BankAccount {
    private final BankAccount target;
    private final Logger logger;
    
    public LoggingBankAccountProxy(BankAccount target) {
        this.target = target;
        this.logger = LoggerFactory.getLogger(this.getClass());
    }
    
    public void deposit(double amount) {
        logger.info("Depositing: " + amount);
        target.deposit(amount);
        logger.info("New balance: " + target.getBalance());
    }
    
    public void withdraw(double amount) {
        logger.info("Withdrawing: " + amount);
        target.withdraw(amount);
        logger.info("New balance: " + target.getBalance());
    }
    
    public double getBalance() {
        double balance = target.getBalance();
        logger.info("Current balance: " + balance);
        return balance;
    }
}

// 동적 프록시 생성
public class BankAccountProxyFactory {
    public static BankAccount createLoggingProxy(BankAccount target) {
        return (BankAccount) Proxy.newProxyInstance(
            BankAccount.class.getClassLoader(),
            new Class[]{BankAccount.class},
            new LoggingInvocationHandler(target)
        );
    }
}

class LoggingInvocationHandler implements InvocationHandler {
    private final Object target;
    private final Logger logger;
    
    public LoggingInvocationHandler(Object target) {
        this.target = target;
        this.logger = LoggerFactory.getLogger(target.getClass());
    }
    
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        logger.info("Calling method: " + method.getName());
        Object result = method.invoke(target, args);
        logger.info("Method completed: " + method.getName());
        return result;
    }
}
```

### 11.5 순수 자바 AOP 프레임워크
**접근 방법**:
- Spring AOP와 같은 프레임워크의 활용
- 선언적 프로그래밍의 장점

**주요 내용**:
- 프록시 코드는 상당히 많으며 복잡하다
- 깨끗한 코드를 작성하기 어렵다
- 스프링은 비즈니스 논리를 POJO로 구현한다
- POJO는 순수하게 도메인에 초점을 맞춘다

**Spring AOP 예시**:
```java
// POJO 비즈니스 로직
@Service
public class BankAccountService {
    
    @Autowired
    private AccountRepository repository;
    
    public void transfer(String fromAccount, String toAccount, double amount) {
        Account from = repository.findById(fromAccount);
        Account to = repository.findById(toAccount);
        
        from.withdraw(amount);
        to.deposit(amount);
        
        repository.save(from);
        repository.save(to);
    }
}

// XML 기반 AOP 설정
<aop:config>
    <aop:aspect ref="loggingAspect">
        <aop:pointcut id="businessMethods" 
                      expression="execution(* com.example.service.*.*(..))"/>
        <aop:before pointcut-ref="businessMethods" method="logBefore"/>
        <aop:after-returning pointcut-ref="businessMethods" method="logAfterSuccess"/>
    </aop:aspect>
</aop:config>

// 어노테이션 기반 AOP
@Aspect
@Component
public class TransactionAspect {
    
    @Around("@annotation(Transactional)")
    public Object manageTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        TransactionManager.beginTransaction();
        try {
            Object result = joinPoint.proceed();
            TransactionManager.commit();
            return result;
        } catch (Exception e) {
            TransactionManager.rollback();
            throw e;
        }
    }
}
```

### 11.6 AspectJ 관점
**접근 방법**:
- AspectJ를 통한 강력한 AOP 구현
- 컴파일 타임 위빙과 런타임 위빙

**주요 내용**:
- AspectJ는 언어 차원에서 관점을 모듈화 구성으로 지원하는 자바 언어 확장이다
- Spring AOP보다 강력하며 설정 또한 간편하다

### 11.7 테스트 주도 시스템 아키텍처 구축
**접근 방법**:
- 아키텍처의 진화적 발전
- BDUF(Big Design Up Front)의 문제점

**주요 내용**:
- 관점으로 관심사를 분리하는 방식은 그 위력이 막강하다
- 애플리케이션 도메인 논리를 POJO로 작성할 수 있다면, 즉 코드 수준에서 아키텍처 관심사를 분리할 수 있다면, 진정한 테스트 주도 아키텍처 구축이 가능해진다
- 그때그때 새로운 기술을 채택해 단순한 아키텍처를 복잡한 아키텍처로 키워갈 수도 있다

### 11.8 의사 결정을 최적화하라
**접근 방법**:
- 결정 시점의 최적화
- 정보가 충분할 때까지 결정 연기

**주요 내용**:
- 모듈을 나누고 관심사를 분리하면 지엽적인 관리와 결정이 가능해진다
- 가장 적합한 사람에게 책임을 맡기면 가장 좋다
- 우리는 때때로 가능한 마지막 순간까지 결정을 미루는 방법이 최선이라는 사실을 까먹곤 한다

### 11.9 명백한 가치가 있을 때 표준을 현명하게 사용하라
**접근 방법**:
- 표준의 적절한 활용
- 과도한 표준화의 위험성

**주요 내용**:
- 표준을 사용하면 아이디어와 컴포넌트를 재사용하기 쉽고, 적절한 경험을 가진 사람을 구하기 쉬우며, 좋은 아이디어를 캡슐화하기 쉽고, 컴포넌트를 엮기 쉽다
- 하지만 때로는 표준을 만드는 시간이 너무 오래 걸려 업계가 기다리지 못한다
- 어떤 표준은 원래 표준을 제정한 목적을 잊어버리기도 한다

### 11.10 시스템은 도메인 특화 언어가 필요하다
**접근 방법**:
- DSL(Domain Specific Language)의 중요성
- 도메인과 코드 사이의 의사소통 간극 줄이기

**주요 내용**:
- 대다수 도메인과 마찬가지로 건축 분야 역시 필수적인 정보를 명료하고 정확하게 전달하는 어휘, 관용구, 패턴이 풍부하다
- 소프트웨어 분야에서도 최근 들어 DSL(Domain-Specific Language)이 새롭게 조명받고 있다

**DSL 예시**:
```java
// 내부 DSL 예시 (Fluent Interface)
public class OrderBuilder {
    private Order order = new Order();
    
    public static OrderBuilder createOrder() {
        return new OrderBuilder();
    }
    
    public OrderBuilder forCustomer(String customerId) {
        order.setCustomerId(customerId);
        return this;
    }
    
    public OrderBuilder addItem(String productId, int quantity) {
        order.addLineItem(new LineItem(productId, quantity));
        return this;
    }
    
    public OrderBuilder withDiscount(double percentage) {
        order.setDiscount(percentage);
        return this;
    }
    
    public Order build() {
        return order;
    }
}

// 사용 예시
Order order = OrderBuilder.createOrder()
    .forCustomer("CUST001")
    .addItem("PROD001", 2)
    .addItem("PROD002", 1)
    .withDiscount(0.1)
    .build();
```

## 강의 진행 방식
1. **도입 (10분)**: 시스템 설계 경험 공유
2. **이론 (30분)**: 의존성 주입, AOP, 아키텍처 패턴 설명
3. **실습 (35분)**: 간단한 시스템에 DI와 AOP 적용
4. **설계 리뷰 (15분)**: 시스템 아키텍처 개선 방안 토론

## 실습 과제
1. **의존성 주입 적용**: 기존 시스템에 DI 컨테이너 도입
2. **횡단 관심사 분리**: AOP를 사용해 로깅, 보안, 트랜잭션 분리
3. **시스템 아키텍처 설계**: 확장 가능한 시스템 구조 설계

## 평가 기준
- 관심사 분리 이해 및 적용 (35%)
- 의존성 주입 활용 능력 (30%)
- 시스템 확장성 고려 (35%)

## 시스템 설계 체크리스트
- [ ] 시스템 생성과 사용이 분리되었는가?
- [ ] 의존성 주입이 적절히 활용되었는가?
- [ ] 횡단 관심사가 모듈화되었는가?
- [ ] 시스템이 점진적으로 확장 가능한가?
- [ ] 도메인 로직이 POJO로 구현되었는가?
- [ ] 결정이 적절한 시점에 이루어지는가?
- [ ] 표준이 현명하게 활용되었는가?
- [ ] DSL이 적절히 사용되었는가?

## 추가 자료
- Martin Fowler의 "Patterns of Enterprise Application Architecture"
- "Spring in Action" - 의존성 주입과 AOP
- "Aspect-Oriented Programming with AspectJ"
- Clean Architecture 패턴 (Hexagonal, Onion, Clean Architecture)
- 마이크로서비스 아키텍처 패턴 