---
draft: true
collection_order: 41
title: "[Design Patterns] Factory 패턴 실습 - 다양한 생성 전략 마스터하기"
description: "Simple Factory부터 Abstract Factory까지 다양한 Factory 패턴을 실제로 구현해보는 종합 실습입니다. 결제 시스템, 게임 캐릭터 생성, 로깅 시스템을 통해 각 패턴의 특징과 적용 시나리오를 체험하고, 현대적 Factory 구현 기법까지 마스터합니다. 실무에서 바로 적용 가능한 Factory 패턴 설계 노하우를 학습합니다."
image: "wordcloud.png"
date: 2024-12-04T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Creational Patterns
- Factory Patterns
- Practice
- Object Creation
tags:
- Factory Method
- Abstract Factory
- Simple Factory
- Static Factory
- Factory Pattern Practice
- Object Creation
- Creational Patterns
- Design Patterns
- GoF Patterns
- Payment System
- Game Character Creation
- Logging System
- Dependency Injection
- IoC Container
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Engineering
- Design Methodology
- Architectural Patterns
- Object Composition
- 팩토리 메서드
- 추상 팩토리
- 심플 팩토리
- 정적 팩토리
- 팩토리 패턴 실습
- 객체 생성
- 생성 패턴
- 디자인 패턴
- GoF 패턴
- 결제 시스템
- 게임 캐릭터 생성
- 로깅 시스템
- 의존성 주입
- IoC 컨테이너
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 공학
- 설계 방법론
- 아키텍처 패턴
- 객체 컴포지션
---

이 실습에서는 Simple Factory, Factory Method, Abstract Factory 패턴을 직접 구현하며 다양한 생성 전략을 익힙니다.

## 실습 목표
- Simple Factory, Factory Method, Abstract Factory 패턴의 차이점 이해
- 실무에서 Factory 패턴이 적용되는 다양한 상황 경험
- 현대적 Factory 패턴(DI Container, Functional Factory) 구현
- Factory 패턴의 성능 특성과 최적화 방법 학습

## 실습 1: 결제 시스템 Factory 패턴 적용

### 과제 설명
온라인 쇼핑몰의 결제 시스템을 구현합니다. 다양한 결제 방식(신용카드, PayPal, 암호화폐)을 지원하며, 각 결제 방식마다 다른 설정과 처리 로직이 필요합니다.

### 요구사항
1. **Simple Factory**: 기본적인 결제 프로세서 생성
2. **Factory Method**: 결제 서비스별 특화된 프로세서 생성
3. **Abstract Factory**: 지역별(미국, 유럽, 아시아) 결제 시스템 제공
4. **현대적 Factory**: 어노테이션 기반 자동 등록

### 코드 템플릿

```java
// TODO 1: PaymentProcessor 인터페이스 정의
public interface PaymentProcessor {
    // TODO: 결제 처리 메서드 정의
    // - processPayment(PaymentRequest request)
    // - validatePayment(PaymentInfo info)
    // - getProcessorName()
    // - getSupportedCurrencies()
}

// TODO 2: 구체적인 결제 프로세서들 구현
public class CreditCardProcessor implements PaymentProcessor {
    private final String apiKey;
    private final String endpoint;
    
    // TODO: 생성자 및 메서드 구현
}

public class PayPalProcessor implements PaymentProcessor {
    private final String clientId;
    private final String clientSecret;
    
    // TODO: 생성자 및 메서드 구현
}

public class CryptoProcessor implements PaymentProcessor {
    private final String walletAddress;
    private final String network;
    
    // TODO: 생성자 및 메서드 구현
}

// TODO 3: Simple Factory 구현
public class SimplePaymentFactory {
    public static PaymentProcessor createProcessor(PaymentType type, PaymentConfig config) {
        // TODO: switch 문을 사용한 기본 Factory 구현
        // 힌트: PaymentType enum을 사용하여 분기 처리
        return null;
    }
}

// TODO 4: Factory Method 패턴 구현
public abstract class PaymentServiceFactory {
    // TODO: abstract 메서드 정의
    // - createPaymentProcessor()
    // - createPaymentValidator()
    // - createPaymentLogger()
    
    // TODO: Template Method로 서비스 생성 과정 정의
    public final PaymentService createPaymentService() {
        PaymentProcessor processor = createPaymentProcessor();
        PaymentValidator validator = createPaymentValidator();
        PaymentLogger logger = createPaymentLogger();
        
        return new PaymentService(processor, validator, logger);
    }
}

// TODO 5: 구체적인 Factory Method 구현
public class CreditCardServiceFactory extends PaymentServiceFactory {
    // TODO: 신용카드 전용 컴포넌트들 생성 구현
}

public class PayPalServiceFactory extends PaymentServiceFactory {
    // TODO: PayPal 전용 컴포넌트들 생성 구현
}

// TODO 6: Abstract Factory 패턴 구현
public interface RegionalPaymentFactory {
    PaymentProcessor createCreditCardProcessor();
    PaymentProcessor createDigitalWalletProcessor();
    PaymentValidator createPaymentValidator();
    CurrencyConverter createCurrencyConverter();
    TaxCalculator createTaxCalculator();
}

// TODO 7: 지역별 구체적인 Factory 구현
public class USPaymentFactory implements RegionalPaymentFactory {
    // TODO: 미국 결제 시스템에 특화된 구현
}

public class EuropePaymentFactory implements RegionalPaymentFactory {
    // TODO: 유럽 결제 시스템에 특화된 구현
}

public class AsiaPaymentFactory implements RegionalPaymentFactory {
    // TODO: 아시아 결제 시스템에 특화된 구현
}

// TODO 8: 어노테이션 기반 현대적 Factory
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface PaymentProcessorProduct {
    String value(); // payment type identifier
    String region() default "global";
    int priority() default 0;
}

// TODO 9: 자동 등록 Factory 구현
public class AutoPaymentProcessorFactory {
    private static final Map<String, Class<? extends PaymentProcessor>> processors = new HashMap<>();
    
    static {
        // TODO: classpath scanning을 통한 자동 등록 구현
        // 힌트: @PaymentProcessorProduct 어노테이션이 붙은 클래스들을 찾아서 등록
    }
    
    public PaymentProcessor createProcessor(String type, String region) {
        // TODO: 타입과 지역에 맞는 프로세서 생성
        return null;
    }
}

// TODO 10: 테스트 코드 작성
public class PaymentFactoryTest {
    @Test
    public void testSimpleFactory() {
        // TODO: Simple Factory 테스트
    }
    
    @Test
    public void testFactoryMethod() {
        // TODO: Factory Method 테스트
    }
    
    @Test
    public void testAbstractFactory() {
        // TODO: Abstract Factory 테스트
    }
    
    @Test
    public void testAutoFactory() {
        // TODO: 자동 등록 Factory 테스트
    }
}
```

## 실습 2: 게임 캐릭터 생성 시스템

### 과제 설명
MMORPG 게임의 캐릭터 생성 시스템을 구현합니다. 다양한 직업(전사, 마법사, 궁수)과 종족(인간, 엘프, 드워프)의 조합을 지원해야 합니다.

### 코드 템플릿

```java
// TODO 1: 캐릭터 관련 클래스들 정의
public abstract class GameCharacter {
    protected String name;
    protected Race race;
    protected Job job;
    protected Stats stats;
    protected List<Skill> skills;
    protected Equipment equipment;
    
    // TODO: 캐릭터 기본 메서드들 구현
}

// TODO 2: Builder 패턴과 Factory 패턴 조합
public class CharacterFactory {
    public static CharacterBuilder builder() {
        return new CharacterBuilder();
    }
    
    // TODO: 미리 정의된 캐릭터 템플릿들
    public static GameCharacter createWarrior(String name) {
        // TODO: 전사 캐릭터 생성
        return null;
    }
    
    public static GameCharacter createMage(String name) {
        // TODO: 마법사 캐릭터 생성
        return null;
    }
    
    public static GameCharacter createArcher(String name) {
        // TODO: 궁수 캐릭터 생성
        return null;
    }
}

// TODO 3: 성능 최적화된 Flyweight + Factory 조합
public class OptimizedCharacterFactory {
    // TODO: 공통 데이터를 Flyweight로 관리
    // TODO: Object Pool 패턴으로 성능 최적화
}
```

## 실습 3: 로깅 시스템 Factory

### 과제 설명
다양한 로깅 백엔드(콘솔, 파일, 데이터베이스, 원격 서버)를 지원하는 로깅 시스템을 구현합니다.

### 코드 템플릿

```java
// TODO 1: 로거 인터페이스와 구현체들
public interface Logger {
    void log(LogLevel level, String message, Object... args);
    void log(LogLevel level, String message, Throwable throwable);
    boolean isEnabled(LogLevel level);
}

// TODO 2: 함수형 Factory 구현
public class FunctionalLoggerFactory {
    private static final Map<LoggerType, Function<LoggerConfig, Logger>> factories = Map.of(
        // TODO: 각 로거 타입별 생성 함수 등록
    );
    
    public static Logger createLogger(LoggerType type, LoggerConfig config) {
        // TODO: 함수형 스타일로 로거 생성
        return null;
    }
    
    // TODO: 복합 로거 생성 (여러 백엔드에 동시 로깅)
    public static Logger createCompositeLogger(LoggerConfig... configs) {
        // TODO: Composite 패턴과 Factory 패턴 조합
        return null;
    }
}
```

## 체크리스트

### 기본 구현
- [ ] Simple Factory로 기본적인 객체 생성 구현
- [ ] Factory Method로 확장 가능한 생성 구조 구현
- [ ] Abstract Factory로 관련 객체군 생성 구현
- [ ] 각 Factory 패턴의 차이점을 명확히 이해

### 현대적 구현
- [ ] 어노테이션 기반 자동 등록 Factory 구현
- [ ] 함수형 스타일 Factory 구현
- [ ] DI Container와 연계된 Factory 구현
- [ ] Generic을 활용한 타입 안전한 Factory 구현

### 성능 최적화
- [ ] Object Pool과 Factory 패턴 조합
- [ ] Flyweight 패턴과 Factory 조합
- [ ] Lazy initialization 구현
- [ ] 캐싱 메커니즘 적용

### 테스트 및 검증
- [ ] 단위 테스트 작성 (최소 80% 커버리지)
- [ ] 성능 벤치마크 테스트
- [ ] 메모리 사용량 분석
- [ ] 동시성 테스트 (멀티스레드 환경)

## 추가 도전

### 고급 패턴 조합
1. **Factory + Decorator**: 생성된 객체에 자동으로 기능 추가
2. **Factory + Observer**: 객체 생성 이벤트 알림 시스템
3. **Factory + Strategy**: 생성 전략을 런타임에 변경
4. **Factory + Proxy**: 생성된 객체에 자동으로 프록시 적용

### 실무 시나리오
1. **마이크로서비스 환경**에서 서비스 인스턴스 Factory
2. **Spring Framework**와 연계된 Factory Bean 구현
3. **테스트 환경**에서 Mock 객체 Factory
4. **플러그인 아키텍처**에서 동적 Factory

## 실무 적용

### 프로젝트 적용 가이드
1. **현재 프로젝트에서** 객체 생성이 복잡한 부분 식별
2. **적절한 Factory 패턴** 선택 기준 수립
3. **점진적 적용** 계획 수립
4. **팀원들과 패턴** 사용 가이드라인 공유

### 성능 고려사항
- Factory 패턴의 오버헤드 측정
- 리플렉션 사용 시 성능 영향 분석
- 메모리 사용량 모니터링
- 동시성 환경에서의 안전성 검증

---

**핵심 포인트**: Factory 패턴은 단순한 객체 생성을 넘어 시스템의 유연성과 확장성을 좌우하는 핵심 설계 요소입니다. 각 패턴의 특성을 이해하고 상황에 맞게 적용하는 것이 중요합니다. 