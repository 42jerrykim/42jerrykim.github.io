---
collection_order: 221
draft: true
title: "[Design Patterns] 안티패턴과 리팩토링 실습 - 나쁜 설계 개선"
description: "안티패턴을 식별하고 디자인 패턴을 활용해 리팩토링하는 실습입니다. God Object, Spaghetti Code, Singleton 남용 등의 문제를 체계적으로 분석하고 적절한 패턴 적용을 통해 깔끔하고 유지보수 가능한 코드로 개선하는 실무 기법을 학습합니다."
date: 2024-12-22T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Anti Patterns
- Refactoring
- Practice
- Code Quality
tags:
- Anti Patterns Practice
- Refactoring Practice
- God Object
- Spaghetti Code
- Singleton Abuse
- Code Smell
- Pattern Misuse
- Legacy Code
- Technical Debt
- Code Quality
- Clean Code
- SOLID Principles
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Design Improvement
- 안티패턴 실습
- 리팩토링 실습
- 갓 오브젝트
- 스파게티 코드
- 싱글톤 남용
- 코드 스멜
- 패턴 오남용
- 레거시 코드
- 기술 부채
- 코드 품질
- 클린 코드
- SOLID 원칙
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 설계 개선
---

# 안티패턴과 리팩토링 실습 - 나쁜 설계 개선

## **실습 목표**

1. God Object 리팩토링으로 단일 책임 원칙 적용
2. Spaghetti Code를 Command Pattern으로 정리
3. 안티패턴 탐지기 구현

## **과제 1: God Object 리팩토링**

### 문제 코드
```java
// 안티패턴: 모든 책임을 가진 거대한 OrderManager
public class OrderManager {
    // 데이터베이스, 외부 서비스, 비즈니스 로직이 모두 혼재
    private Connection connection;
    private EmailServiceClient emailClient;
    private PaymentServiceClient paymentClient;
    
    public void processOrder(OrderRequest request) throws Exception {
        // 500+ 줄의 복잡한 로직
        // 고객 검증, 재고 확인, 가격 계산, 결제, 저장, 이메일, 배송...
    }
}
```

### 리팩토링 과제
```java
// TODO: 책임별로 서비스 분리
@Service
public class OrderDomainService {
    // 순수 비즈니스 로직만
}

@Service 
public class PricingService {
    // 가격 계산 전담
}

@Service
public class OrderProcessingService {
    // 워크플로우 오케스트레이션
}

@EventListener
public class OrderEventHandler {
    // 이메일, 배송 등 후속 처리
}
```

## **과제 2: Command Pattern으로 Spaghetti Code 정리**

### 문제 코드
```java
public class PaymentProcessor {
    public PaymentResult processPayment(PaymentRequest request) {
        // 깊은 중첩 조건문과 복잡한 분기 로직
        if (request != null) {
            if (request.getAmount() != null) {
                if ("CREDIT_CARD".equals(request.getPaymentMethod())) {
                    // 중첩된 조건들...
                } else if ("DEBIT_CARD".equals(request.getPaymentMethod())) {
                    // 또 다른 중첩...
                }
            }
        }
    }
}
```

### Command Pattern 적용
```java
// TODO: Command 인터페이스 정의
public interface PaymentCommand {
    PaymentResult execute(PaymentContext context);
    boolean canHandle(PaymentRequest request);
}

// TODO: 구체적인 Command들 구현
public class CreditCardPaymentCommand implements PaymentCommand {
    // 신용카드 결제 로직
}

public class DebitCardPaymentCommand implements PaymentCommand {
    // 직불카드 결제 로직  
}

// TODO: Command 실행 엔진
@Service
public class PaymentProcessor {
    private final List<PaymentCommand> commands;
    
    public PaymentResult processPayment(PaymentRequest request) {
        PaymentCommand command = findCommand(request);
        return command.execute(createContext(request));
    }
}
```

## **과제 3: 안티패턴 탐지기 구현**

### 기본 구조
```java
// TODO: 안티패턴 탐지 인터페이스
public interface AntiPatternDetector {
    List<CodeSmell> detect(Class<?> clazz);
}

// TODO: Long Parameter List 탐지
public class LongParameterListDetector implements AntiPatternDetector {
    private static final int MAX_PARAMETERS = 5;
    
    public List<CodeSmell> detect(Class<?> clazz) {
        // 파라미터 수가 많은 메서드 찾기
        return null;
    }
}

// TODO: Data Class 탐지
public class DataClassDetector implements AntiPatternDetector {
    public List<CodeSmell> detect(Class<?> clazz) {
        // getter/setter만 있고 비즈니스 로직 없는 클래스 찾기
        return null;
    }
}

// TODO: Feature Envy 탐지  
public class FeatureEnvyDetector implements AntiPatternDetector {
    public List<CodeSmell> detect(Class<?> clazz) {
        // 다른 클래스 데이터를 과도하게 사용하는 메서드 찾기
        return null;
    }
}
```

### 분석 엔진
```java
public class AntiPatternAnalyzer {
    private final List<AntiPatternDetector> detectors;
    
    public AnalysisReport analyzeCodebase(String packageName) {
        // TODO: 패키지 스캔하여 모든 안티패턴 탐지
        // 1. 클래스 목록 수집
        // 2. 각 탐지기 실행
        // 3. 결과 취합 및 리포트 생성
        return null;
    }
}
```

## **완성도 체크리스트**

### God Object 리팩토링
- [ ] 단일 책임 원칙 적용
- [ ] 의존성 주입으로 결합도 감소
- [ ] 이벤트 기반 후속 처리
- [ ] 단위 테스트 작성

### Command Pattern
- [ ] 복잡한 조건문 제거
- [ ] 확장 가능한 구조
- [ ] 에러 처리 중앙화
- [ ] 우선순위 기반 처리

### 안티패턴 탐지기
- [ ] 여러 안티패턴 탐지
- [ ] 심각도 분류
- [ ] 리팩토링 제안
- [ ] 통계 리포트

## **추가 도전 과제**

1. **정적 분석 도구 통합** - SonarQube, PMD 연계
2. **IDE 플러그인 개발** - 실시간 코드 분석
3. **CI/CD 통합** - 품질 게이트 적용
4. **머신러닝 탐지** - 패턴 학습 기반 분석

## **실무 적용**

### Strangler Fig Pattern
```java
@Service
public class ServiceFacade {
    // 점진적 레거시 교체
    private final LegacyService legacyService;
    private final NewService newService;
    
    public Result process(Request request) {
        if (shouldUseNewService(request)) {
            return newService.process(request);
        }
        return legacyService.process(request);
    }
}
```

---

**💡 실습 팁**
- 작은 단위로 점진적 리팩토링
- 테스트 코드 먼저 작성
- 정적 분석 도구 적극 활용
- 팀 코딩 표준 준수 