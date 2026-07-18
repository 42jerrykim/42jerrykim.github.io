---
draft: true
collection_order: 41
title: "[Design Patterns] 04. 팩토리 패턴의 진화 — 실습"
slug: "factory-patterns-evolution-practice"
description: "Simple Factory부터 Abstract Factory까지 다양한 Factory 패턴을 직접 구현하는 실습입니다. 결제 시스템과 게임 캐릭터 생성 예제로 각 패턴의 특징을 체험하고, DI Container 등 현대적 Factory 구현 기법까지 익힙니다."
image: "wordcloud.png"
date: 2024-12-04T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Creational Patterns
- Factory Patterns
- Practice
- Object Creation
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Dependency-Injection(의존성주입)
- Tutorial(튜토리얼)
- Implementation(구현)
- Software-Architecture(소프트웨어아키텍처)
- Factory
- Creational-Pattern
- OOP(객체지향)
- Interface(인터페이스)
- Abstraction(추상화)
- Encapsulation(캡슐화)
- Polymorphism(다형성)
- SOLID
- Clean-Code(클린코드)
- Best-Practices
- Code-Quality(코드품질)
- Testing(테스트)
- Performance(성능)
- Optimization(최적화)
- Refactoring(리팩토링)
- Java
- Guide(가이드)
- Case-Study
- Beginner
---

이 실습에서는 Simple Factory, Factory Method, Abstract Factory 패턴을 직접 구현하며 다양한 생성 전략을 익힙니다.

## 실습 목표
- Simple Factory, Factory Method, Abstract Factory 패턴의 차이점 이해
- 실무에서 Factory 패턴이 적용되는 다양한 상황 경험
- 현대적 Factory 패턴(DI Container, Functional Factory) 구현
- Factory 패턴의 성능 특성과 최적화 방법 학습

### 실습 1~3 비교

| 실습 | 다루는 패턴 | 핵심 학습 포인트 | 난이도 |
|------|-------------|-------------------|--------|
| 실습 1: 결제 시스템 | Simple Factory → Factory Method → Abstract Factory | 단계적 확장을 통해 OCP 위반과 그 해결 과정을 체감 | 중 |
| 실습 2: 게임 캐릭터 생성 | Factory + Builder + Flyweight | 조합 폭발 문제를 다른 패턴과의 조합으로 해결하는 감각 | 상 |
| 실습 3: 로깅 시스템 | 함수형 Factory (`Function<Config, T>`) | 클래스 계층 없이 맵 기반으로 OCP를 준수하는 방법 | 중 |

## 실습 1: 결제 시스템 Factory 패턴 적용

### 과제 설명
온라인 쇼핑몰의 결제 시스템을 구현합니다. 다양한 결제 방식(신용카드, PayPal, 암호화폐)을 지원하며, 각 결제 방식마다 다른 설정과 처리 로직이 필요합니다. Simple Factory부터 시작하는 이유는, 가장 단순한 형태의 생성 로직 중앙화를 먼저 체득한 뒤에야 Factory Method와 Abstract Factory가 해결하는 "확장성"과 "일관성" 문제를 체감할 수 있기 때문입니다. 아래 TODO들을 채워나가면서 각 단계에서 어떤 한계에 부딪히는지 직접 경험해보세요.

### 요구사항
1. **Simple Factory**: 기본적인 결제 프로세서 생성
2. **Factory Method**: 결제 서비스별 특화된 프로세서 생성
3. **Abstract Factory**: 지역별(미국, 유럽, 아시아) 결제 시스템 제공
4. **현대적 Factory**: 어노테이션 기반 자동 등록

### 코드 템플릿

아래는 `SimplePaymentFactory.createProcessor`와 `CreditCardProcessor`에 대한 완성된 참조 구현입니다. `PaymentType`, `PaymentConfig` 등 컴파일에 필요한 최소한의 보조 타입도 함께 정의했습니다. PayPal·암호화폐 프로세서, Factory Method, Abstract Factory, 어노테이션 기반 Factory, 테스트 코드는 이 참조 구현을 참고하여 직접 채워보세요.

```java
import java.util.List;

// 지원하는 결제 수단
public enum PaymentType {
    CREDIT_CARD, PAYPAL, CRYPTO
}

// Factory에 전달되는 최소 설정값
public class PaymentConfig {
    private final String apiKey;
    private final String endpoint;

    public PaymentConfig(String apiKey, String endpoint) {
        this.apiKey = apiKey;
        this.endpoint = endpoint;
    }

    public String getApiKey() { return apiKey; }
    public String getEndpoint() { return endpoint; }
}

// 결제 요청/검증/결과에 필요한 최소 데이터
public class PaymentRequest {
    private final double amount;
    private final String currency;

    public PaymentRequest(double amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public double getAmount() { return amount; }
    public String getCurrency() { return currency; }
}

public class PaymentInfo {
    private final String cardNumber;

    public PaymentInfo(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    public String getCardNumber() { return cardNumber; }
}

public class PaymentResult {
    private final boolean success;
    private final String message;

    public PaymentResult(boolean success, String message) {
        this.success = success;
        this.message = message;
    }

    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
}

// TODO 1: PaymentProcessor 인터페이스 정의 (완성됨)
public interface PaymentProcessor {
    PaymentResult processPayment(PaymentRequest request);
    boolean validatePayment(PaymentInfo info);
    String getProcessorName();
    List<String> getSupportedCurrencies();
}

// TODO 2: 구체적인 결제 프로세서들 구현
// CreditCardProcessor만 완성된 참조 구현이며, 나머지는 실습 과제로 남겨둡니다.
public class CreditCardProcessor implements PaymentProcessor {
    private final String apiKey;
    private final String endpoint;

    public CreditCardProcessor(String apiKey, String endpoint) {
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalArgumentException("apiKey는 필수입니다");
        }
        this.apiKey = apiKey;
        this.endpoint = endpoint;
    }

    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        if (!getSupportedCurrencies().contains(request.getCurrency())) {
            return new PaymentResult(false, "지원하지 않는 통화: " + request.getCurrency());
        }
        // 실제 구현에서는 endpoint로 HTTP 호출을 수행합니다.
        return new PaymentResult(true, "신용카드 결제 승인: " + request.getAmount() + " " + request.getCurrency());
    }

    @Override
    public boolean validatePayment(PaymentInfo info) {
        return info.getCardNumber() != null
            && info.getCardNumber().replaceAll("\\s", "").length() == 16;
    }

    @Override
    public String getProcessorName() {
        return "CreditCardProcessor";
    }

    @Override
    public List<String> getSupportedCurrencies() {
        return List.of("USD", "EUR", "KRW");
    }
}

public class PayPalProcessor implements PaymentProcessor {
    private final String clientId;
    private final String clientSecret;
    
    // TODO: 생성자 및 메서드 구현 (CreditCardProcessor 참고)
}

public class CryptoProcessor implements PaymentProcessor {
    private final String walletAddress;
    private final String network;
    
    // TODO: 생성자 및 메서드 구현 (CreditCardProcessor 참고)
}

// TODO 3: Simple Factory 구현 (완성됨)
// CREDIT_CARD 분기만 완전히 구현되어 있습니다. PAYPAL, CRYPTO는
// PayPalProcessor, CryptoProcessor를 완성한 뒤 동일한 방식으로 연결하세요.
public class SimplePaymentFactory {
    public static PaymentProcessor createProcessor(PaymentType type, PaymentConfig config) {
        switch (type) {
            case CREDIT_CARD:
                return new CreditCardProcessor(config.getApiKey(), config.getEndpoint());
            case PAYPAL:
                // TODO: PayPalProcessor 구현 후 연결
                throw new UnsupportedOperationException("PayPalProcessor는 아직 구현되지 않았습니다");
            case CRYPTO:
                // TODO: CryptoProcessor 구현 후 연결
                throw new UnsupportedOperationException("CryptoProcessor는 아직 구현되지 않았습니다");
            default:
                throw new IllegalArgumentException("Unsupported payment type: " + type);
        }
    }
}

// 아래 4개 타입은 TODO 4, 6에서 참조하는 최소 필드만 가진 스텁입니다.
// 실제 구현 로직은 각 TODO를 채우면서 직접 확장하세요.
public class PaymentService {
    private final PaymentProcessor processor;
    private final PaymentValidator validator;
    private final PaymentLogger logger;

    public PaymentService(PaymentProcessor processor, PaymentValidator validator, PaymentLogger logger) {
        this.processor = processor;
        this.validator = validator;
        this.logger = logger;
    }
}

public interface PaymentValidator {
    boolean validate(PaymentInfo info);
}

public interface PaymentLogger {
    void logPayment(PaymentRequest request, PaymentResult result);
}

public interface CurrencyConverter {
    double convert(double amount, String fromCurrency, String toCurrency);
}

public interface TaxCalculator {
    double calculateTax(double amount, String region);
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
MMORPG 게임의 캐릭터 생성 시스템을 구현합니다. 다양한 직업(전사, 마법사, 궁수)과 종족(인간, 엘프, 드워프)의 조합을 지원해야 합니다. 이 실습은 Factory 패턴을 Builder, Flyweight와 조합하는 경험을 목표로 합니다. 직업×종족 조합이 늘어날수록 단순 Factory만으로는 생성 로직이 기하급수적으로 복잡해지므로, 언제 다른 패턴과 조합해야 하는지 판단하는 감각을 기르는 것이 이 실습의 핵심입니다.

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
다양한 로깅 백엔드(콘솔, 파일, 데이터베이스, 원격 서버)를 지원하는 로깅 시스템을 구현합니다. 이 실습은 전통적인 클래스 기반 Factory 대신 함수(`Function<LoggerConfig, Logger>`)를 값으로 다루는 함수형 Factory를 연습하는 데 목적이 있습니다. 백엔드별 생성 로직을 맵에 등록해두면 새 백엔드 추가 시 기존 분기문을 수정하지 않아도 되는데, 이는 실습 1의 switch 기반 Simple Factory가 가진 OCP 위반 문제를 함수형 스타일로 어떻게 해결하는지 보여줍니다.

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
- [ ] Simple Factory로 기본적인 객체 생성 구현 — 생성 로직 중앙화의 기본 개념을 체득하기 위함
- [ ] Factory Method로 확장 가능한 생성 구조 구현 — Simple Factory의 OCP 위반을 해결하는 경험을 위함
- [ ] Abstract Factory로 관련 객체군 생성 구현 — 제품군 간 일관성 보장 방법을 익히기 위함
- [ ] 각 Factory 패턴의 차이점을 명확히 이해 — 상황에 맞는 패턴 선택 기준을 세우기 위함

### 현대적 구현
- [ ] 어노테이션 기반 자동 등록 Factory 구현 — 리플렉션 기반 확장 방식의 장단점을 체감하기 위함
- [ ] 함수형 스타일 Factory 구현 — 클래스 계층 없이 조합 가능한 생성 방식을 익히기 위함
- [ ] DI Container와 연계된 Factory 구현 — 실무에서 Factory가 프레임워크에 흡수되는 방식을 이해하기 위함
- [ ] Generic을 활용한 타입 안전한 Factory 구현 — 컴파일 타임에 타입 오류를 방지하기 위함

### 성능 최적화
- [ ] Object Pool과 Factory 패턴 조합 — 생성 비용이 높은 객체의 재사용 전략을 익히기 위함
- [ ] Flyweight 패턴과 Factory 조합 — 공유 가능한 상태를 분리해 메모리를 절약하기 위함
- [ ] Lazy initialization 구현 — 실제로 필요한 시점까지 생성 비용을 지연시키기 위함
- [ ] 캐싱 메커니즘 적용 — 반복 생성 비용(특히 리플렉션)을 줄이기 위함

### 테스트 및 검증
- [ ] 단위 테스트 작성 (최소 80% 커버리지) — Factory가 반환하는 객체의 정확성을 보장하기 위함
- [ ] 성능 벤치마크 테스트 — Factory 방식별 오버헤드를 실측으로 비교하기 위함
- [ ] 메모리 사용량 분석 — 풀링·Flyweight 적용 효과를 정량적으로 확인하기 위함
- [ ] 동시성 테스트 (멀티스레드 환경) — 캐시나 풀 공유 시 스레드 안전성을 검증하기 위함

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

성능 측정·메모리 분석·동시성 검증 항목은 위 체크리스트의 "성능 최적화"·"테스트 및 검증" 절을 참고하세요.

---

**핵심 포인트**: Factory 패턴은 단순한 객체 생성을 넘어 시스템의 유연성과 확장성을 좌우하는 핵심 설계 요소입니다. 각 패턴의 특성을 이해하고 상황에 맞게 적용하는 것이 중요합니다. 