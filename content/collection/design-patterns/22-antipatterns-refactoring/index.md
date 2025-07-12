---
collection_order: 220
draft: true
title: "[Design Patterns] 안티패턴 식별과 리팩토링"
description: "소프트웨어 개발에서 자주 발생하는 안티패턴을 식별하고 체계적으로 리팩토링하는 전문가 기법을 학습합니다. God Object, Spaghetti Code 등 주요 안티패턴 분석, Strangler Fig Pattern을 활용한 점진적 개선, 코드 품질 측정과 기술 부채 관리를 통해 지속 가능한 소프트웨어를 만드는 방법을 탐구합니다."
date: 2024-12-22T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Anti Patterns
- Code Refactoring
- Software Quality
tags:
- Anti Patterns
- Code Refactoring
- Code Smells
- Technical Debt
- Software Quality
- Design Debt
- God Object
- Spaghetti Code
- Legacy Code
- Strangler Fig Pattern
- Code Quality Metrics
- Refactoring Techniques
- Clean Code
- Software Maintenance
- Code Review
- Static Analysis
- Code Analysis
- Quality Assurance
- Software Engineering
- Best Practices
- Code Optimization
- Design Principles
- SOLID Principles
- Code Structure
- Architecture Improvement
- Code Modernization
- Legacy System Migration
- Continuous Improvement
- Software Evolution
- Code Health
- 안티패턴
- 코드 리팩토링
- 코드 스멜
- 기술 부채
- 소프트웨어 품질
- 설계 부채
- 신 객체
- 스파게티 코드
- 레거시 코드
- 교살자 무화과 패턴
- 코드 품질 메트릭
- 리팩토링 기법
- 클린 코드
- 소프트웨어 유지보수
- 코드 리뷰
- 정적 분석
- 코드 분석
- 품질 보증
- 소프트웨어 공학
- 모범 사례
- 코드 최적화
- 설계 원칙
- SOLID 원칙
- 코드 구조
- 아키텍처 개선
- 코드 현대화
- 레거시 시스템 마이그레이션
- 지속적 개선
- 소프트웨어 진화
- 코드 건강성
---

# 안티패턴 식별과 리팩토링

## 🚨 **서론: 나쁜 설계 패턴의 역설**

> *"모든 좋은 패턴에는 그림자가 있다. 잘못 사용된 패턴은 코드를 더 복잡하게 만들고, 오히려 유지보수를 어렵게 한다."*

안티패턴(Anti-pattern)은 **겉보기에는 문제를 해결하는 것처럼 보이지만, 실제로는 더 큰 문제를 만드는 설계 방식**입니다. 이 글에서는 실무에서 자주 발생하는 안티패턴들을 식별하고, 체계적인 리팩토링 방법을 제시합니다.

### **안티패턴 식별의 핵심 관점**
- **코드 스멜(Code Smell)**: 즉각적인 문제 징후
- **설계 부채(Design Debt)**: 장기적 유지보수 비용
- **패턴 오남용**: 적절한 맥락이 아닌 곳에서의 패턴 사용
- **과도한 추상화**: 불필요한 복잡성 증가

## 🔍 **1. 주요 안티패턴 분석**

### **1.1 God Object (신 객체)**

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

### **1.2 Spaghetti Code (스파게티 코드)**

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

## 🔧 **2. 리팩토링 전략**

### **2.1 Strangler Fig Pattern (점진적 교체)**

```java
// 기존 레거시 시스템
@Component
public class LegacyOrderService {
    
    public void processOrder(OrderData orderData) {
        // 복잡한 레거시 로직 (500줄)
        // 여러 데이터베이스 직접 접근
        // 하드코딩된 비즈니스 규칙
        // 예외 처리 부족
    }
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
}

// 2단계: 새 서비스 구현
@Service
public class NewOrderService {
    private final OrderValidator validator;
    private final PaymentProcessor paymentProcessor;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    
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

## 📊 **3. 성과 측정**

### **3.1 리팩토링 효과 측정**

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

## 🚀 **실습 과제**

### **과제 1: God Object 리팩토링**
주어진 `OrderManager` 클래스를 분석하고, 단일 책임 원칙에 따라 여러 서비스로 분리하세요.

### **과제 2: Spaghetti Code 정리**
복잡한 중첩 조건문으로 이루어진 `PaymentProcessor.processPayment()` 메서드를 Command Pattern을 사용해 리팩토링하세요.

### **과제 3: 안티패턴 탐지기 구현**
정적 분석을 통해 다음 안티패턴을 탐지하는 도구를 구현하세요:
- Long Parameter List
- Data Class
- Feature Envy

## 💭 **토론 주제**

1. **기술 부채와 비즈니스 가치**: 언제 리팩토링에 투자해야 하는가?
2. **레거시 시스템 현대화**: 대규모 레거시 시스템을 안전하게 리팩토링하는 전략
3. **팀 차원의 코드 품질**: 코드 리뷰와 페어 프로그래밍의 역할

## 📚 **참고 자료**

- **도서**: "Refactoring: Improving the Design of Existing Code" by Martin Fowler
- **도서**: "Working Effectively with Legacy Code" by Michael Feathers
- **도서**: "Clean Code" by Robert C. Martin
- **온라인**: [Refactoring Guru - Code Smells](https://refactoring.guru/refactoring/smells)
- **도구**: SonarQube, PMD, SpotBugs, Checkstyle

---

## 🎓 **다음 단계**

안티패턴을 식별하고 체계적으로 리팩토링할 수 있게 되었다면, 다음 글에서는 **패턴을 활용한 코드 리뷰와 설계 리뷰**에 대해 알아보겠습니다. 팀 차원에서 좋은 설계를 유지하고 발전시키는 방법을 탐구해보겠습니다.

> *"좋은 코드는 한 번에 만들어지지 않는다. 지속적인 개선을 통해 진화한다."*
