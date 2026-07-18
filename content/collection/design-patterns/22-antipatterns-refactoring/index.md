---
draft: true
collection_order: 220
title: "[Design Patterns] 22. 안티패턴 식별과 리팩토링"
slug: "antipatterns-refactoring"
description: "소프트웨어 개발에서 자주 발생하는 안티패턴을 식별하고 체계적으로 리팩토링하는 전문가 기법을 학습합니다. God Object, Spaghetti Code 분석과 Strangler Fig Pattern 기반 점진적 개선, 코드 품질 측정을 통해 지속 가능한 소프트웨어를 만드는 방법을 탐구합니다."
image: "wordcloud.png"
date: 2024-12-22T10:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Anti Patterns
- Code Refactoring
- Software Quality
tags:
- Design-Pattern(디자인패턴)
- Refactoring(리팩토링)
- Clean-Code(클린코드)
- Code-Quality(코드품질)
- Code-Review(코드리뷰)
- Best-Practices
- SOLID
- Coupling(결합도)
- Cohesion(응집도)
- Maintainability
- Readability
- Modularity
- Pitfalls(함정)
- Software-Architecture(소프트웨어아키텍처)
- OOP(객체지향)
- Singleton
- Factory
- Observer
- Strategy
- Decorator
- Command
- Behavioral-Pattern
- Creational-Pattern
- Structural-Pattern
- Java
- Deep-Dive
- Advanced
- Case-Study
---

실무에서 자주 발생하는 안티패턴을 식별하고 체계적인 리팩토링 방법을 탐구합니다. 코드 스멜, 설계 부채, 패턴 남용의 문제를 해결하는 방법을 학습합니다.

## 서론: 나쁜 설계 패턴의 역설

> *"모든 좋은 패턴에는 그림자가 있다. 잘못 사용된 패턴은 코드를 더 복잡하게 만들고, 오히려 유지보수를 어렵게 한다."*

안티패턴(Anti-pattern)은 **겉보기에는 문제를 해결하는 것처럼 보이지만, 실제로는 더 큰 문제를 만드는 설계 방식**입니다. 이 글에서는 실무에서 자주 발생하는 안티패턴들을 식별하고, 체계적인 리팩토링 방법을 제시합니다.

### 안티패턴 식별의 핵심 관점
- **코드 스멜(Code Smell)**: 즉각적인 문제 징후
- **설계 부채(Design Debt)**: 장기적 유지보수 비용
- **패턴 오남용**: 적절한 맥락이 아닌 곳에서의 패턴 사용
- **과도한 추상화**: 불필요한 복잡성 증가

### 흔한 오해: 안티패턴은 처음부터 나쁜 코드다

안티패턴을 "처음부터 잘못 설계된 코드"로 오해하기 쉽지만, 실제로는 그 반대인 경우가 더 많습니다. 아래 God Object 예시의 `UserManager`도 처음에는 사용자 생성 메서드 하나짜리 작고 멀쩡한 클래스였을 가능성이 높습니다. 매 스프린트마다 "일단 여기 추가하자"는 합리적으로 보이는 선택이 누적되면서, 각 시점의 결정은 국소적으로 타당했지만 전체 결과는 God Object가 되는 것입니다. 이는 God Object가 한 번의 실수가 아니라 여러 번의 작은 타협이 쌓인 결과임을 뜻하며, 따라서 리팩토링도 "처음부터 다시 설계"가 아니라 그 타협들을 하나씩 되짚어 되돌리는 점진적 작업이어야 합니다.

## 주요 안티패턴 분석

### God Object (신 객체)

God Object는 "일단 여기에 추가하면 편하니까"라는 판단이 반복되면서 만들어집니다. 새 기능이 필요할 때마다 기존 클래스에 필드와 메서드를 얹는 쪽이, 새 클래스를 만들고 의존성을 연결하는 것보다 눈앞에서는 더 빨라 보이기 때문입니다. 그 결과 한 클래스가 데이터베이스 접근, 비즈니스 규칙, 외부 서비스 연동까지 모두 떠안게 되며, 이는 단일 책임 원칙(SRP) 위반의 가장 전형적인 형태입니다. Martin Fowler는 이런 축적형 코드 스멜을 *Refactoring: Improving the Design of Existing Code*(2nd ed., 2018)에서 "Large Class"로 분류하고, 책임이 늘어날 때마다 즉시 Extract Class로 분리할 것을 권고합니다. 아래 `UserManager`는 사용자 생성·인증·프로필·권한 관리를 800줄 넘는 하나의 클래스에 모아둔 예시입니다.

```java
// 안티패턴: 모든 책임을 가진 거대한 클래스
public class UserManager {
    // 데이터베이스 접근
    private Connection connection;
    private PreparedStatement userInsertStmt;
    private PreparedStatement userSelectStmt;
    
    // 비즈니스 로직
    private EmailValidator emailValidator;
    private PasswordEncoder passwordEncoder;
    private UserPolicyEngine policyEngine;
    
    // 외부 서비스 연동
    private EmailServiceClient emailClient;
    private PaymentServiceClient paymentClient;
    private AuditServiceClient auditClient;
    
    // 1. 사용자 관리
    public void createUser(String email, String password) throws Exception {
        // 입력 검증 (50줄)
        if (email == null || email.trim().isEmpty()) {
            throw new ValidationException("Email is required");
        }
        if (!emailValidator.isValid(email)) {
            throw new ValidationException("Invalid email format");
        }
        // ... 더 많은 검증 로직
        
        // 비즈니스 규칙 적용 (100줄)
        UserPolicy policy = policyEngine.getPolicy(email);
        if (!policy.allowsRegistration()) {
            throw new BusinessException("Registration not allowed");
        }
        // ... 복잡한 정책 로직
        
        // 패스워드 처리 (30줄)
        String hashedPassword = passwordEncoder.encode(password);
        
        // 데이터베이스 저장 (40줄)
        try {
            userInsertStmt.setString(1, email);
            userInsertStmt.setString(2, hashedPassword);
            userInsertStmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to save user", e);
        }
        
        // 환영 이메일 발송 (20줄)
        emailClient.sendWelcomeEmail(email);
        
        // 결제 시스템 연동 (30줄)
        paymentClient.createCustomerAccount(email);
        
        // 감사 로그 (15줄)
        auditClient.logUserCreation(email);
    }
    
    // 2. 인증 관련 (200줄)
    public boolean authenticateUser(String email, String password) { /* ... */ }
    public void resetPassword(String email) { /* ... */ }
    public void changePassword(String email, String oldPassword, String newPassword) { /* ... */ }
    
    // 3. 프로필 관리 (150줄)
    public void updateProfile(String email, UserProfile profile) { /* ... */ }
    public UserProfile getProfile(String email) { /* ... */ }
    
    // 4. 권한 관리 (100줄)
    public void grantRole(String email, String role) { /* ... */ }
    public void revokeRole(String email, String role) { /* ... */ }
    
    // ... 총 800줄이 넘는 거대한 클래스
}

// 문제점:
// 1. 단일 책임 원칙 위반 - 너무 많은 책임
// 2. 높은 결합도 - 여러 외부 시스템에 직접 의존
// 3. 테스트 어려움 - 모든 의존성을 모킹해야 함
// 4. 변경 영향도 큼 - 한 부분 변경이 전체에 영향
```

**리팩토링: 책임 분산과 의존성 주입**

```java
// 1. 사용자 도메인 서비스
@Service
public class UserDomainService {
    private final UserRepository userRepository;
    private final UserValidator userValidator;
    private final PasswordService passwordService;
    
    public UserDomainService(UserRepository userRepository,
                           UserValidator userValidator,
                           PasswordService passwordService) {
        this.userRepository = userRepository;
        this.userValidator = userValidator;
        this.passwordService = passwordService;
    }
    
    public User createUser(CreateUserCommand command) {
        // 검증
        ValidationResult validation = userValidator.validate(command);
        if (!validation.isValid()) {
            throw new ValidationException(validation.getErrors());
        }
        
        // 도메인 객체 생성
        User user = User.builder()
            .email(command.getEmail())
            .password(passwordService.encode(command.getPassword()))
            .createdAt(Instant.now())
            .build();
            
        return userRepository.save(user);
    }
}

// 2. 사용자 애플리케이션 서비스 (오케스트레이션)
@Service
@Transactional
public class UserApplicationService {
    private final UserDomainService userDomainService;
    private final UserEventPublisher eventPublisher;
    
    public void registerUser(RegisterUserCommand command) {
        // 도메인 로직 실행
        User user = userDomainService.createUser(
            new CreateUserCommand(command.getEmail(), command.getPassword())
        );
        
        // 이벤트 발행 (다른 서비스들이 구독)
        eventPublisher.publish(new UserRegisteredEvent(user.getId(), user.getEmail()));
    }
}

// 3. 이벤트 핸들러들 (각자의 책임)
@EventListener
@Component
public class UserRegistrationEventHandler {
    private final EmailService emailService;
    private final PaymentService paymentService;
    private final AuditService auditService;
    
    @Async
    public void handleUserRegistered(UserRegisteredEvent event) {
        // 병렬로 처리 가능한 후속 작업들
        CompletableFuture.allOf(
            emailService.sendWelcomeEmailAsync(event.getEmail()),
            paymentService.createCustomerAccountAsync(event.getEmail()),
            auditService.logUserCreationAsync(event.getUserId())
        ).join();
    }
}

// 개선 효과:
// 1. 단일 책임: 각 클래스가 하나의 명확한 책임
// 2. 느슨한 결합: 인터페이스를 통한 의존성 주입
// 3. 테스트 용이성: 각 컴포넌트를 독립적으로 테스트
// 4. 확장성: 새로운 기능 추가 시 기존 코드 변경 최소화
```

### Spaghetti Code (스파게티 코드)

Spaghetti Code는 조건문 하나하나는 정당한 검증 로직인데도, 그 검증들을 순서대로 중첩시키다 보니 전체 흐름을 한눈에 파악할 수 없게 된 상태를 가리킵니다. "null 체크 → 빈 값 체크 → 각 항목 검증 → 고객 상태 확인 → 한도 확인"처럼 서로 다른 층위의 검증이 들여쓰기 depth로만 구분되면, 예외 조건 하나를 추가하거나 순서를 바꿀 때마다 전체 중첩 구조를 다시 읽어야 합니다. Fowler(2018)는 이런 깊은 중첩을 "Nested Conditional" 계열의 코드 스멜로 다루며, Guard Clause 도입과 [Decompose Conditional](https://refactoring.guru/refactoring/smells) 리팩토링으로 조건들을 같은 층위로 평탄화할 것을 제안합니다. 아래 `OrderProcessor.processOrder()`는 5단계 검증이 중첩 if-else로 얽혀 있는 예시입니다.

```java
// 안티패턴: 복잡하게 얽힌 제어 흐름
public class OrderProcessor {
    
    public void processOrder(Order order) {
        if (order != null) {
            if (order.getItems() != null && !order.getItems().isEmpty()) {
                boolean hasValidItems = true;
                for (OrderItem item : order.getItems()) {
                    if (item.getQuantity() <= 0) {
                        hasValidItems = false;
                        break;
                    }
                    if (item.getPrice() == null || item.getPrice().compareTo(BigDecimal.ZERO) <= 0) {
                        hasValidItems = false;
                        break;
                    }
                }
                
                if (hasValidItems) {
                    Customer customer = getCustomer(order.getCustomerId());
                    if (customer != null) {
                        if (customer.getStatus().equals("ACTIVE")) {
                            BigDecimal total = BigDecimal.ZERO;
                            for (OrderItem item : order.getItems()) {
                                total = total.add(item.getPrice().multiply(
                                    BigDecimal.valueOf(item.getQuantity())));
                            }
                            
                            if (customer.getCreditLimit().compareTo(total) >= 0) {
                                // ... 복잡한 중첩 로직 계속
                            } else {
                                throw new BusinessException("Credit limit exceeded");
                            }
                        } else {
                            throw new BusinessException("Customer is not active");
                        }
                    } else {
                        throw new BusinessException("Customer not found");
                    }
                } else {
                    throw new ValidationException("Invalid order items");
                }
            } else {
                throw new ValidationException("Order has no items");
            }
        } else {
            throw new IllegalArgumentException("Order cannot be null");
        }
    }
}

// 문제점:
// 1. 깊은 중첩 - 가독성 극도로 떨어짐
// 2. 복잡한 제어 흐름 - 디버깅 어려움
// 3. 단일 메서드에 모든 로직 - SRP 위반
// 4. 예외 상황 처리가 흩어져 있음
```

**리팩토링: Command Pattern + Validation Chain**

```java
// 0. 지원 타입 최소 스텁 (컴파일 가능하도록 핵심 필드만 포함)
public enum ProcessingStatus { IN_PROGRESS, COMPLETED, FAILED, ERROR }

public class ProcessingResult {
    private final boolean failed;
    private final boolean warning;
    private final String message;

    private ProcessingResult(boolean failed, boolean warning, String message) {
        this.failed = failed;
        this.warning = warning;
        this.message = message;
    }

    public static ProcessingResult success(String message) {
        return new ProcessingResult(false, false, message);
    }

    public static ProcessingResult failed(List<String> errors) {
        return new ProcessingResult(true, false, String.join(", ", errors));
    }

    public boolean isFailed() { return failed; }
    public boolean isWarning() { return warning; }
    public String getMessage() { return message; }
}

// 1. 주문 처리 단계를 명확한 커맨드로 분리
public interface OrderProcessingStep {
    ProcessingResult execute(OrderProcessingContext context);
    boolean canHandle(OrderProcessingContext context);
    int getOrder(); // 실행 순서
}

// 2. 처리 컨텍스트
public class OrderProcessingContext {
    private final Order order;
    private Customer customer;
    private BigDecimal totalAmount;
    private List<ProcessingMessage> messages = new ArrayList<>();
    private ProcessingStatus status = ProcessingStatus.IN_PROGRESS;
    
    // getters, setters, builder pattern
}

// 3. 각 단계별 구체적인 구현
@Component
@Order(1)
public class OrderValidationStep implements OrderProcessingStep {
    private final OrderValidator orderValidator;
    
    @Override
    public ProcessingResult execute(OrderProcessingContext context) {
        ValidationResult result = orderValidator.validate(context.getOrder());
        
        if (!result.isValid()) {
            return ProcessingResult.failed(result.getErrors());
        }
        
        return ProcessingResult.success("Order validation completed");
    }
    
    @Override
    public boolean canHandle(OrderProcessingContext context) {
        return context.getOrder() != null;
    }
}

// 4. 주문 처리 오케스트레이터
@Service
public class OrderProcessingOrchestrator {
    private final List<OrderProcessingStep> steps;
    
    public OrderProcessingOrchestrator(List<OrderProcessingStep> steps) {
        this.steps = steps.stream()
            .sorted(Comparator.comparing(OrderProcessingStep::getOrder))
            .collect(Collectors.toList());
    }
    
    public OrderProcessingResult processOrder(Order order) {
        OrderProcessingContext context = new OrderProcessingContext(order);
        
        for (OrderProcessingStep step : steps) {
            if (!step.canHandle(context)) {
                continue;
            }
            
            try {
                ProcessingResult result = step.execute(context);
                
                if (result.isFailed()) {
                    context.setStatus(ProcessingStatus.FAILED);
                    return OrderProcessingResult.failed(context, result.getMessage());
                }
                
                if (result.isWarning()) {
                    context.addMessage(result.getMessage());
                }
                
            } catch (Exception e) {
                log.error("Error in step: " + step.getClass().getSimpleName(), e);
                context.setStatus(ProcessingStatus.ERROR);
                return OrderProcessingResult.error(context, e.getMessage());
            }
        }
        
        context.setStatus(ProcessingStatus.COMPLETED);
        return OrderProcessingResult.success(context);
    }
}

// 개선 효과:
// 1. 명확한 단계별 처리 - 각 단계의 책임이 명확
// 2. 테스트 용이성 - 각 단계를 독립적으로 테스트
// 3. 확장성 - 새로운 단계 추가가 쉬움
// 4. 오류 처리 집중화 - 일관된 예외 처리
```

## 리팩토링 전략

### Strangler Fig Pattern (점진적 교체)

```java
// 기존 레거시 시스템
// 아래 processOrder()는 실존하는 레거시 코드를 그대로 옮긴 것이 아니라,
// "이미 있고 당장 손댈 수 없는 500줄짜리 코드"라는 상황을 나타내는 자리표시자입니다.
// Strangler Fig 전략의 핵심은 이 내부를 뜯어고치지 않고도 트래픽을 점진적으로 새 서비스로 옮기는 데 있으므로,
// 본문 구현은 의도적으로 생략합니다.
@Component
public class LegacyOrderService {
    
    public void processOrder(OrderData orderData) {
        // 복잡한 레거시 로직 (500줄)
        // 여러 데이터베이스 직접 접근
        // 하드코딩된 비즈니스 규칙
        // 예외 처리 부족
    }
}

// 아래는 OrderServiceProxy / NewOrderService가 최소한이나마 컴파일되도록 하는 지원 타입 스텁입니다.
// 실제 필드·검증 로직은 프로젝트 도메인에 맞게 채워야 합니다.
class OrderData { /* 레거시 포맷 DTO */ }

interface FeatureToggle {
    boolean isEnabled(String key);
}

class OrderItem {}
class PaymentInfo {}

class Order {
    private long customerId;
    private List<OrderItem> items;
    private PaymentInfo paymentInfo;

    public long getCustomerId() { return customerId; }
    public List<OrderItem> getItems() { return items; }
    public PaymentInfo getPaymentInfo() { return paymentInfo; }
    public Order confirm(String transactionId) { return this; }
}

interface OrderValidator {
    ValidationResult validate(Order order);
}

class ValidationResult {
    private final boolean valid;
    private final List<String> errors;
    ValidationResult(boolean valid, List<String> errors) { this.valid = valid; this.errors = errors; }
    boolean isValid() { return valid; }
    List<String> getErrors() { return errors; }
}

interface InventoryService {
    ReservationResult reserveItems(List<OrderItem> items);
    void cancelReservation(String reservationId);
}

class ReservationResult {
    private final boolean successful;
    private final String reservationId;
    private final List<OrderItem> unavailableItems;
    ReservationResult(boolean successful, String reservationId, List<OrderItem> unavailableItems) {
        this.successful = successful;
        this.reservationId = reservationId;
        this.unavailableItems = unavailableItems;
    }
    boolean isSuccessful() { return successful; }
    String getReservationId() { return reservationId; }
    List<OrderItem> getUnavailableItems() { return unavailableItems; }
}

class PaymentException extends Exception {}

interface PaymentProcessor {
    PaymentResult processPayment(PaymentInfo paymentInfo) throws PaymentException;
}

class PaymentResult {
    private final String transactionId;
    PaymentResult(String transactionId) { this.transactionId = transactionId; }
    String getTransactionId() { return transactionId; }
}

interface NotificationService {
    void sendOrderConfirmation(Order order);
}

interface OrderRepository {
    Order save(Order order);
}

class OrderResult {
    static OrderResult success(Order order) { return new OrderResult(); }
}

class OrderValidationException extends RuntimeException {
    OrderValidationException(List<String> errors) { super(String.join(", ", errors)); }
}

class InsufficientStockException extends RuntimeException {
    InsufficientStockException(List<OrderItem> items) { super("insufficient stock"); }
}

// 1단계: 프록시 도입
@Service
public class OrderServiceProxy {
    private final LegacyOrderService legacyService;
    private final NewOrderService newService;
    private final FeatureToggle featureToggle;
    
    public void processOrder(Order order) {
        if (featureToggle.isEnabled("new-order-service")) {
            // 점진적으로 새 서비스로 이전
            if (shouldUseNewService(order)) {
                newService.processOrder(order);
            } else {
                legacyService.processOrder(convertToLegacyFormat(order));
            }
        } else {
            legacyService.processOrder(convertToLegacyFormat(order));
        }
    }
    
    private boolean shouldUseNewService(Order order) {
        // 카나리 배포: 특정 조건의 주문만 새 서비스 사용
        return order.getCustomerId() % 10 == 0; // 10% 트래픽
    }

    private OrderData convertToLegacyFormat(Order order) {
        // TODO: 신규 도메인 모델(Order) -> 레거시 스키마(OrderData) 변환
        return new OrderData();
    }
}

// 2단계: 새 서비스 구현
@Service
public class NewOrderService {
    private final OrderValidator validator;
    private final PaymentProcessor paymentProcessor;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    private final OrderRepository orderRepository;
    
    @Transactional
    public OrderResult processOrder(Order order) {
        // 1. 유효성 검사
        ValidationResult validation = validator.validate(order);
        if (!validation.isValid()) {
            throw new OrderValidationException(validation.getErrors());
        }
        
        // 2. 재고 확인 및 예약
        ReservationResult reservation = inventoryService.reserveItems(order.getItems());
        if (!reservation.isSuccessful()) {
            throw new InsufficientStockException(reservation.getUnavailableItems());
        }
        
        try {
            // 3. 결제 처리
            PaymentResult payment = paymentProcessor.processPayment(order.getPaymentInfo());
            
            // 4. 주문 확정
            Order confirmedOrder = orderRepository.save(order.confirm(payment.getTransactionId()));
            
            // 5. 후속 처리 (비동기)
            notificationService.sendOrderConfirmation(confirmedOrder);
            
            return OrderResult.success(confirmedOrder);
            
        } catch (PaymentException e) {
            // 결제 실패 시 예약 취소
            inventoryService.cancelReservation(reservation.getReservationId());
            throw e;
        }
    }
}
```

## 성과 측정

### 리팩토링 효과 측정

```java
@Component
public class RefactoringMetrics {
    
    // 코드 품질 지표
    public CodeQualityMetrics measureCodeQuality(String packageName) {
        return CodeQualityMetrics.builder()
            .cyclomaticComplexity(calculateAverageComplexity(packageName))
            .linesOfCode(countLinesOfCode(packageName))
            .testCoverage(getTestCoverage(packageName))
            .codeSmells(countCodeSmells(packageName))
            .technicalDebt(calculateTechnicalDebt(packageName))
            .maintainabilityIndex(calculateMaintainabilityIndex(packageName))
            .build();
    }
    
    // 개발 생산성 지표
    public ProductivityMetrics measureProductivity(String teamName, Period period) {
        return ProductivityMetrics.builder()
            .averageFeatureDeliveryTime(getAverageDeliveryTime(teamName, period))
            .bugRate(getBugRate(teamName, period))
            .codeReviewTime(getAverageReviewTime(teamName, period))
            .deploymentFrequency(getDeploymentFrequency(teamName, period))
            .meanTimeToRecovery(getMTTR(teamName, period))
            .build();
    }
}
```

## 실습 과제

### 과제 1: God Object 리팩토링
주어진 `OrderManager` 클래스를 분석하고, 단일 책임 원칙에 따라 여러 서비스로 분리하세요.

### 과제 2: Spaghetti Code 정리
복잡한 중첩 조건문으로 이루어진 `PaymentProcessor.processPayment()` 메서드를 Command Pattern을 사용해 리팩토링하세요.

### 과제 3: 안티패턴 탐지기 구현
정적 분석을 통해 다음 안티패턴을 탐지하는 도구를 구현하세요:
- Long Parameter List
- Data Class
- Feature Envy

## 토론 주제

1. **기술 부채와 비즈니스 가치**: 언제 리팩토링에 투자해야 하는가?
2. **레거시 시스템 현대화**: 대규모 레거시 시스템을 안전하게 리팩토링하는 전략
3. **팀 차원의 코드 품질**: 코드 리뷰와 페어 프로그래밍의 역할

## 한눈에 보는 안티패턴과 리팩토링

원래 이 절에는 6개의 표가 있었지만 상당수가 같은 안티패턴을 다른 각도로 반복하고 있었습니다(예: God Class와 Blob은 사실상 같은 문제입니다). 아래 3개 표로 통합합니다.

### 안티패턴 심각도와 해결 방향

| 안티패턴 | 문제점 | 심각도 | 수정 우선순위 | 해결 패턴 → 리팩토링 방향 |
|---------|-------|-------|-------------|------------------------|
| God Class / Blob | 과도한 책임, 낮은 응집도 (하나의 클래스에 모든 것) | 높음 | 높음 (시스템 전체 영향) | SRP 적용 → Extract Class |
| Spaghetti Code | 얽힌 의존성, 중첩된 흐름으로 이해 불가 | 높음 | 높음 (해당 모듈 영향) | 계층화 → Extract Method, Move |
| Copy-Paste | 코드 중복 | 중간 | 높음 (변경 시 버그 위험) | Template Method, Strategy → Extract Method/Class |
| Golden Hammer | 하나의 해법만 고집 | 중간 | 중간 (설계 품질 저하) | 상황별 적절한 패턴 → 요구사항 재분석 |
| Lava Flow | 죽은 코드 방치 | 낮음 | 낮음 (유지보수성 저하) | 정기적 정리 → Remove Dead Code |
| Poltergeist | 불필요한 중간 클래스 | 낮음 | 낮음 (가독성 저하) | 직접 호출 → Inline Class |
| Boat Anchor | 미사용 코드 보존 | 낮음 | 낮음 (가독성 저하) | 제거 → Remove |

### 코드 스멜·패턴 오용과 권장 대응

코드 스멜(구현 층위의 징후)과 패턴 오용(설계 층위의 징후)은 발견 지점은 다르지만 "리팩토링으로 대응한다"는 결론은 같으므로 하나의 표로 봅니다.

| 구분 | 항목 | 징후 / 오용 상황 | 권장 대응 |
|------|------|-----------------|----------|
| 코드 스멜 | Long Method | 50+ 줄 | Extract Method (Template Method) |
| 코드 스멜 | Large Class | 500+ 줄 | Extract Class (Facade) |
| 코드 스멜 | Long Parameter List | 5+ 파라미터 | Introduce Parameter Object (Builder) |
| 코드 스멜 | Duplicate Code | 동일 코드 반복 | Extract Method (Strategy, Template) |
| 코드 스멜 | Feature Envy | 다른 클래스 데이터 과다 사용 | Move Method |
| 코드 스멜 | Data Clumps | 함께 다니는 데이터 | Extract Class (Value Object) |
| 코드 스멜 | Primitive Obsession | 원시 타입 남용 | Replace Primitive with Object (Value Object) |
| 코드 스멜 | Switch Statements | switch/if 연쇄 | Replace with Polymorphism (Strategy, State) |
| 코드 스멜 | Parallel Inheritance | 계층 구조 동기화 필요 | Move/Merge (Bridge) |
| 코드 스멜 | Speculative Generality | 미래 대비 과설계 | Collapse Hierarchy (YAGNI) |
| 패턴 오용 | Singleton | 전역 상태 남용 | 진짜 유일해야 하는 자원에만 사용 |
| 패턴 오용 | Factory | 단순 생성에 과사용 | 생성 로직이 복잡할 때만 사용 |
| 패턴 오용 | Observer | 이벤트 지옥 (과도한 통지 체인) | 명확한 1:N 관계에만 사용 |
| 패턴 오용 | Strategy | 단일 알고리즘에 적용 | 교체 가능한 알고리즘이 여럿일 때 사용 |
| 패턴 오용 | Decorator | 과도한 래핑 | 동적 기능 조합이 실제로 필요할 때 사용 |

### 리팩토링 안전성 가이드

| 리팩토링 | 위험도 | 필요 조건 | 자동화 가능 |
|---------|-------|----------|-----------|
| Rename | 낮음 | IDE 지원 | O |
| Extract Method | 낮음 | 테스트 | O |
| Move Method/Class | 중간 | 의존성 분석 | 부분 |
| Change Signature | 중간 | 호출부 확인 | O |
| Replace Inheritance | 높음 | 설계 검토 | X |
| Introduce Pattern | 높음 | 팀 합의 | X |

### 안전한 리팩토링을 위한 체크리스트

체크박스에 "완료" 여부만 표시하는 대신, 각 항목이 왜 필요한지 근거를 함께 적었습니다.

- **기존 테스트가 통과하는가** — 리팩토링 시작 전 테스트가 초록불이어야, 이후 실패가 리팩토링 때문인지 기존 버그인지 구분할 수 있습니다.
- **변경 범위를 식별했는가** — 영향받는 클래스·모듈을 미리 나열해야 리팩토링 도중 범위가 예상보다 커지는 것을 막을 수 있습니다.
- **작은 단위로 분할했는가** — 위 "리팩토링 안전성 가이드"에서 위험도가 높은 항목(Replace Inheritance, Introduce Pattern)일수록 단계를 잘게 쪼개야 각 단계를 쉽게 되돌릴 수 있습니다.
- **각 단계 후 테스트를 실행했는가** — 자동화 가능(O)한 리팩토링이라도 매 단계 실행해야 누적된 실수를 조기에 발견합니다.
- **커밋을 단계별로 분리했는가** — 하나의 커밋에 여러 변경을 섞으면 문제 발생 시 원인을 좁히기 어렵습니다.
- **코드 리뷰를 요청했는가** — 위험도가 "높음"인 리팩토링은 설계 변경을 수반하므로, 팀 합의 없이 병합하면 되돌리기 비용이 큽니다.

## 평가 기준

이 글을 읽고 다음을 스스로 설명할 수 있다면 핵심을 이해한 것입니다.

- God Object 예제에서 왜 단일 책임 원칙 위반이 "테스트 어려움"과 "변경 영향도"라는 두 가지 실무 문제로 이어지는지 설명할 수 있다.
- Spaghetti Code를 Command Pattern으로 리팩토링했을 때, `OrderProcessingStep`의 `canHandle`/`execute` 분리가 왜 새 검증 단계 추가를 쉽게 만드는지 설명할 수 있다.
- Strangler Fig Pattern에서 `FeatureToggle`과 카나리 배포 비율(`% 10 == 0`)이 왜 "한 번에 전환"보다 안전한지 설명할 수 있다.
- 위 표에서 God Class와 Blob을 하나로 묶은 이유처럼, 서로 다른 이름의 안티패턴이 실제로는 같은 근본 원인(과도한 책임)을 공유하는 경우를 스스로 식별할 수 있다.

---

## 참고 자료

- **도서**: "Refactoring: Improving the Design of Existing Code" by Martin Fowler (1999, 2nd ed. 2018)
- **도서**: "Working Effectively with Legacy Code" by Michael Feathers (2004)
- **도서**: "Clean Code" by Robert C. Martin (2008)
- **온라인**: [Refactoring Guru - Code Smells](https://refactoring.guru/refactoring/smells)
- **도구**: SonarQube, PMD, SpotBugs, Checkstyle

---

## 다음 단계

안티패턴을 식별하고 체계적으로 리팩토링할 수 있게 되었다면, 다음 글([패턴을 활용한 코드 리뷰와 설계 리뷰](/post/design-patterns/pattern-code-review-design-review/))에서는 팀 차원에서 좋은 설계를 유지하고 발전시키는 방법을 탐구해보겠습니다.

> *"좋은 코드는 한 번에 만들어지지 않는다. 지속적인 개선을 통해 진화한다."*
