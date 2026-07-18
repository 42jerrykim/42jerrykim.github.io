---
draft: true
collection_order: 71
title: "[Design Patterns] 07. 어댑터와 파사드: 인터페이스의 철학 — 실습"
slug: "adapter-facade-interface-philosophy-practice"
description: "Adapter와 Facade 패턴을 활용하여 레거시 시스템 통합과 복잡한 서브시스템 단순화를 실습합니다. 결제 시스템 통합, E-commerce 파사드, 데이터 소스 통합 등의 실무 시나리오를 통해 인터페이스 설계의 철학과 시스템 간 결합도를 낮추는 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-07T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Interface Design
- Practice
- System Integration
tags:
- Tutorial(튜토리얼)
- Implementation(구현)
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Microservices(마이크로서비스)
- Software-Architecture(소프트웨어아키텍처)
- Structural-Pattern
- Adapter
- Facade
- Interface(인터페이스)
- Coupling(결합도)
- OOP(객체지향)
- Clean-Architecture(클린아키텍처)
- Best-Practices
- Code-Quality(코드품질)
- Maintainability
- Refactoring(리팩토링)
- Testing(테스트)
- Guide(가이드)
- Case-Study
- Advanced
- Java
- System-Design
- Migration(마이그레이션)
- API(Application Programming Interface)
- Database(데이터베이스)
- SOLID
---

이 실습에서는 Adapter와 Facade 패턴을 통해 레거시 시스템 통합과 복잡한 서브시스템 단순화를 경험합니다.

두 패턴을 함께 다루는 이유는 실무에서 자주 짝을 이루기 때문입니다. Adapter는 "인터페이스가 서로 맞지 않는 두 코드를 변경 없이 연결"하는 문제를, Facade는 "여러 서브시스템의 호출 순서와 의존관계를 클라이언트가 몰라도 되게 감추는" 문제를 해결합니다. 레거시 시스템 통합처럼 코드를 고칠 수 없는 상황에서는 Adapter로 인터페이스 차이를 흡수하고, 그렇게 통합된 여러 컴포넌트를 다시 Facade로 묶어 하나의 단순한 진입점을 제공하는 흐름이 실무에서 반복적으로 나타납니다. 아래 실습에서는 이 두 패턴이 각각 어떤 문제를 풀기 위해 선택되는지를 코드로 직접 확인합니다.

## 실습 목표

> *"Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use."* — Facade 패턴, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)

이 실습을 마치면 다음을 스스로 확인할 수 있어야 합니다.
- 레거시 시스템(`LegacyPaymentSystem`)과 외부 API(`ExternalPaymentAPI`)를 원본 코드 수정 없이 하나의 `PaymentGateway` 인터페이스로 통합할 수 있다
- 재고 확인→결제→배송 예약→알림 발송 4단계를 `EcommerceFacade.placeOrder()` 하나의 호출로 캡슐화하고, 각 단계 실패 시 이후 단계를 진행하지 않도록 처리할 수 있다
- DB/REST API/파일 시스템처럼 서로 다른 데이터 접근 방식을 `DataRepository<T>` 인터페이스 뒤로 감춰, 서비스 계층 코드를 데이터 소스 변경 없이 유지할 수 있다
- 각 실습 코드가 별도 타입 정의 없이 컴파일된다(아래 "보조 타입 정의" 스텁 포함)

## 실습 1: 결제 시스템 Adapter

### 왜 Adapter인가

`LegacyPaymentSystem`은 "변경 불가" 조건이 붙어 있고, `ExternalPaymentAPI`는 우리가 소유하지 않은 외부 라이브러리입니다. 두 시스템 모두 시그니처를 바꿀 수 없는데 상위 코드는 하나의 `PaymentGateway` 인터페이스만 알고 싶어합니다. 상속으로 통합하려 하면 서로 다른 두 클래스 계층을 억지로 하나로 합쳐야 하지만, Adapter는 각 시스템을 감싸는 별도 클래스를 두어 원본 코드를 전혀 건드리지 않고 인터페이스 차이만 흡수합니다.

### 요구사항
서로 다른 결제 API들을 통합된 인터페이스로 제공

### 코드 템플릿

```java
// TODO 1: 통합 결제 인터페이스 정의
public interface PaymentGateway {
    PaymentResult processPayment(PaymentRequest request);
    boolean refundPayment(String transactionId, BigDecimal amount);
    PaymentStatus getPaymentStatus(String transactionId);
}

// TODO 2: 레거시 결제 시스템 (변경 불가)
public class LegacyPaymentSystem {
    public boolean makePayment(String cardNum, double amount, String currency) {
        // 기존 시스템 로직 (변경 불가)
        return true;
    }
    
    public String checkStatus(String paymentId) {
        return "SUCCESS";
    }
}

// TODO 3: 외부 Payment API (다른 인터페이스)
public class ExternalPaymentAPI {
    public PaymentResponse charge(ChargeRequest request) {
        // 외부 API 응답
        return new PaymentResponse();
    }
}

// TODO 4: Adapter 구현
public class LegacyPaymentAdapter implements PaymentGateway {
    private final LegacyPaymentSystem legacySystem;

    public LegacyPaymentAdapter(LegacyPaymentSystem legacySystem) {
        this.legacySystem = legacySystem;
    }

    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        // PaymentRequest -> 레거시 makePayment(카드번호, double 금액, 통화) 형태로 변환
        boolean success = legacySystem.makePayment(
                request.getCardNumber(),
                request.getAmount().doubleValue(),
                request.getCurrency()
        );
        return success
                ? PaymentResult.success(request.getTransactionId())
                : PaymentResult.failure("LEGACY_PAYMENT_FAILED");
    }

    @Override
    public boolean refundPayment(String transactionId, BigDecimal amount) {
        // TODO: 레거시 시스템은 환불 API를 제공하지 않으므로 별도 배치/수동 프로세스 연동 필요
        return false;
    }

    @Override
    public PaymentStatus getPaymentStatus(String transactionId) {
        // 레거시 문자열 상태값("SUCCESS" 등)을 통합 enum PaymentStatus로 변환
        String legacyStatus = legacySystem.checkStatus(transactionId);
        return PaymentStatus.fromLegacyCode(legacyStatus);
    }
}

public class ExternalPaymentAdapter implements PaymentGateway {
    private final ExternalPaymentAPI externalAPI;
    
    // TODO: 외부 API 호출을 내부 인터페이스에 맞게 변환
}

// TODO 5: 통합 테스트
public class PaymentAdapterTest {
    @Test
    public void testLegacyAdapter() {
        // TODO: 레거시 시스템 어댑터 테스트
    }
    
    @Test
    public void testExternalAdapter() {
        // TODO: 외부 API 어댑터 테스트
    }
}
```

### 보조 타입 정의 (컴파일용 최소 스텁)

위 코드가 참조하는 `PaymentRequest`/`PaymentResult`/`PaymentStatus`/`ChargeRequest`/`PaymentResponse`는 실습 편에서 처음 등장하는 타입이므로, 실제로 컴파일해보려면 최소한 아래 필드만 채운 스텁이 필요합니다. 실무에서는 각 도메인에 맞게 필드를 늘리면 됩니다.

```java
public class PaymentRequest {
    private final String transactionId;
    private final String cardNumber;
    private final BigDecimal amount;
    private final String currency;

    public PaymentRequest(String transactionId, String cardNumber, BigDecimal amount, String currency) {
        this.transactionId = transactionId;
        this.cardNumber = cardNumber;
        this.amount = amount;
        this.currency = currency;
    }

    public String getTransactionId() { return transactionId; }
    public String getCardNumber() { return cardNumber; }
    public BigDecimal getAmount() { return amount; }
    public String getCurrency() { return currency; }
}

public class PaymentResult {
    private final boolean success;
    private final String transactionId;
    private final String errorCode;

    private PaymentResult(boolean success, String transactionId, String errorCode) {
        this.success = success;
        this.transactionId = transactionId;
        this.errorCode = errorCode;
    }

    public static PaymentResult success(String transactionId) {
        return new PaymentResult(true, transactionId, null);
    }

    public static PaymentResult failure(String errorCode) {
        return new PaymentResult(false, null, errorCode);
    }

    public boolean isSuccess() { return success; }
}

public enum PaymentStatus {
    SUCCESS, FAILED, PENDING, UNKNOWN;

    public static PaymentStatus fromLegacyCode(String legacyStatus) {
        if ("SUCCESS".equals(legacyStatus)) return SUCCESS;
        if ("FAILED".equals(legacyStatus)) return FAILED;
        return UNKNOWN;
    }
}

public class ChargeRequest {
    private final BigDecimal amount;
    private final String currency;

    public ChargeRequest(BigDecimal amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public BigDecimal getAmount() { return amount; }
    public String getCurrency() { return currency; }
}

public class PaymentResponse {
    private boolean successful;
    private String transactionId;

    public boolean isSuccessful() { return successful; }
    public String getTransactionId() { return transactionId; }
}
```

## 실습 2: E-commerce Facade

### 왜 Facade인가

주문 하나를 처리하려면 재고 확인, 결제, 배송 예약, 알림 발송이라는 4개 서비스를 정해진 순서로, 각 단계의 실패를 고려해 호출해야 합니다. 이 호출 순서와 서비스 간 의존관계를 클라이언트(컨트롤러 등)가 매번 알아야 한다면, 서비스 하나만 바뀌어도 호출부 전체를 수정해야 합니다. Facade는 이 조율 로직을 한 곳(`EcommerceFacade`)에 모아 클라이언트에게는 `placeOrder()` 하나만 노출함으로써, 서브시스템 변경이 클라이언트에 전파되지 않도록 결합도를 낮춥니다.

### 요구사항
복잡한 주문 처리 과정을 단순한 인터페이스로 제공

### 코드 템플릿

```java
// TODO 1: 복잡한 서브시스템들
public class InventoryService {
    public boolean checkAvailability(String productId, int quantity) { return true; }
    public void reserveItems(String productId, int quantity) {}
}

public class PaymentService {
    public PaymentResult processPayment(PaymentInfo info) { return null; }
}

public class ShippingService {
    public String scheduleDelivery(Address address, List<String> items) { return "TRACK001"; }
}

public class NotificationService {
    public void sendOrderConfirmation(String email, String orderId) {}
}

// TODO 2: E-commerce Facade 구현
public class EcommerceFacade {
    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;
    
    // TODO: 복잡한 주문 처리 과정을 하나의 메서드로 단순화
    public OrderResult placeOrder(OrderRequest request) {
        // TODO: 1. 재고 확인
        // TODO: 2. 결제 처리
        // TODO: 3. 배송 예약
        // TODO: 4. 알림 발송
        // TODO: 5. 결과 반환
        return null;
    }
    
    // TODO: 기타 편의 메서드들
    public boolean isProductAvailable(String productId, int quantity) {
        // TODO: 단순한 재고 확인
        return false;
    }
}
```

### 보조 타입 정의 (컴파일용 최소 스텁)

`OrderRequest`/`OrderResult`/`PaymentInfo`/`Address`도 마찬가지로 아래 최소 스텁이 있어야 `EcommerceFacade`가 컴파일됩니다.

```java
public class Address {
    private final String street;
    private final String city;
    private final String zipCode;

    public Address(String street, String city, String zipCode) {
        this.street = street;
        this.city = city;
        this.zipCode = zipCode;
    }

    public String getStreet() { return street; }
    public String getCity() { return city; }
    public String getZipCode() { return zipCode; }
}

public class PaymentInfo {
    private final BigDecimal amount;
    private final String cardNumber;

    public PaymentInfo(BigDecimal amount, String cardNumber) {
        this.amount = amount;
        this.cardNumber = cardNumber;
    }

    public BigDecimal getAmount() { return amount; }
    public String getCardNumber() { return cardNumber; }
}

public class OrderRequest {
    private final String productId;
    private final int quantity;
    private final PaymentInfo paymentInfo;
    private final Address shippingAddress;
    private final String customerEmail;

    public OrderRequest(String productId, int quantity, PaymentInfo paymentInfo,
                         Address shippingAddress, String customerEmail) {
        this.productId = productId;
        this.quantity = quantity;
        this.paymentInfo = paymentInfo;
        this.shippingAddress = shippingAddress;
        this.customerEmail = customerEmail;
    }

    public String getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public PaymentInfo getPaymentInfo() { return paymentInfo; }
    public Address getShippingAddress() { return shippingAddress; }
    public String getCustomerEmail() { return customerEmail; }
}

public class OrderResult {
    private final boolean success;
    private final String orderId;
    private final String trackingNumber;
    private final String errorMessage;

    private OrderResult(boolean success, String orderId, String trackingNumber, String errorMessage) {
        this.success = success;
        this.orderId = orderId;
        this.trackingNumber = trackingNumber;
        this.errorMessage = errorMessage;
    }

    public static OrderResult success(String orderId, String trackingNumber) {
        return new OrderResult(true, orderId, trackingNumber, null);
    }

    public static OrderResult failure(String errorMessage) {
        return new OrderResult(false, null, null, errorMessage);
    }

    public boolean isSuccess() { return success; }
}
```

## 실습 3: 데이터 소스 통합 Adapter

### 왜 Adapter인가

RDB용 JPA/JDBC 호출, REST API 호출, 파일 시스템 접근은 각각 완전히 다른 방식으로 데이터를 읽고 씁니다. 상위 서비스 로직이 "지금 데이터가 DB에 있는지 REST API 뒤에 있는지"를 알아야 한다면 데이터 소스를 바꿀 때마다 서비스 코드를 고쳐야 합니다. `DataRepository<T>`라는 공통 인터페이스 뒤에 각 접근 방식을 Adapter로 감추면, 서비스 계층은 데이터 소스의 종류와 무관하게 동일한 `findById`/`save` 호출만으로 동작할 수 있습니다.

### 코드 템플릿

```java
// TODO 1: 통합 데이터 접근 인터페이스
public interface DataRepository<T> {
    T findById(String id);
    List<T> findAll();
    void save(T entity);
    void delete(String id);
}

// TODO 2: 다양한 데이터 소스 어댑터들
public class DatabaseAdapter<T> implements DataRepository<T> {
    // TODO: JPA/JDBC 어댑터 구현
}

public class RestApiAdapter<T> implements DataRepository<T> {
    // TODO: REST API 호출을 데이터 접근으로 변환
}

public class FileSystemAdapter<T> implements DataRepository<T> {
    // TODO: 파일 시스템 접근을 데이터 접근으로 변환
}

// TODO 3: 통합 데이터 서비스 Facade
public class UnifiedDataService {
    private final Map<String, DataRepository<?>> repositories;
    
    // TODO: 데이터 소스별 라우팅 로직
    public <T> T getData(String source, String id, Class<T> type) {
        // TODO: 적절한 어댑터 선택 후 데이터 조회
        return null;
    }
}
```

## 체크리스트

### Adapter 패턴
- [ ] 인터페이스 불일치 문제 해결
- [ ] 레거시 시스템 통합
- [ ] 외부 라이브러리 의존성 격리
- [ ] 데이터 형식 변환 구현

### Facade 패턴
- [ ] 복잡한 서브시스템 단순화
- [ ] 클라이언트와 서브시스템 결합도 감소
- [ ] 편의 메서드 제공
- [ ] 에러 처리 중앙화

### 통합 구현

실습 3의 `UnifiedDataService`처럼 Adapter로 개별 데이터 소스의 인터페이스 차이를 흡수한 뒤, 그 위에 Facade를 얹어 라우팅·에러 처리를 한 곳에 모으는 조합을 실제로 구현해보고, 확장 시(새 데이터 소스 추가) 기존 코드를 얼마나 건드리지 않고 처리할 수 있는지 단위 테스트와 통합 테스트로 확인합니다.

## Adapter vs Facade 비교

두 패턴은 "간접 계층을 추가한다"는 점은 같지만 목적이 다릅니다. 실습 코드에 빗대면 다음과 같이 구분할 수 있습니다.

| 비교 항목 | Adapter (실습 1, 3) | Facade (실습 2) |
|----------|---------------------|------------------|
| 감추는 대상 | 기존 클래스/외부 API의 시그니처 차이 | 여러 서비스 호출의 순서·의존관계 |
| 관계 | 1:1 (레거시 하나당 어댑터 하나) | N:1 (여러 서비스를 하나로 조합) |
| 실습 예시 | `LegacyPaymentAdapter`, `DatabaseAdapter<T>` | `EcommerceFacade.placeOrder()` |
| 변경 트리거 | 기존 시스템의 인터페이스가 바뀔 때 | 서브시스템 호출 순서나 구성이 바뀔 때 |
| 실패 시 대응 | 변환 실패를 표준 예외/결과 타입으로 전환 | 중간 단계 실패 시 이후 단계를 건너뛰고 보상 처리 |

## 추가 도전

기본 구현이 끝나면 난이도를 높여볼 수 있습니다. `PaymentGateway`를 양방향(Two-way) Adapter로 확장해 신규 시스템의 응답을 다시 레거시 형식으로 되돌리는 경로까지 구현하거나, `EcommerceFacade`를 설정값(재시도 횟수, 타임아웃)을 주입받는 Configurable Facade로 바꿔봅니다. `placeOrder()`를 `CompletableFuture` 기반 Async Facade로 전환해 응답 시간을 단축하고, 외부 결제 API 어댑터에는 Circuit Breaker를 추가해 장애가 전체 주문 흐름으로 전파되지 않도록 격리하는 것도 좋은 연습이 됩니다.

## 실무 적용

Adapter는 시스템 마이그레이션 중 신규/레거시 코드가 공존하는 기간에 인터페이스를 통일하는 용도, 외부 API를 감싸 벤더 종속성을 줄이는 용도, 서로 다른 포맷 간 데이터 변환, 그리고 테스트에서 실제 구현 대신 주입할 테스트 더블을 만드는 용도로 흔히 쓰입니다. Facade는 마이크로서비스 앞단의 API Gateway처럼 여러 서비스를 하나의 진입점으로 묶거나, 복잡하게 얽힌 비즈니스 로직을 하나의 메서드 뒤로 숨기거나, 레거시 모듈을 현대화하는 과정에서 기존 호출부를 바꾸지 않고 내부만 교체하거나, SDK/라이브러리의 공개 API 표면을 좁히는 데 사용됩니다.

## 언제 쓰면 안 되는가

Adapter와 Facade 모두 "간접 계층을 하나 추가"하는 패턴이라는 공통점이 있고, 이 간접 계층 자체가 비용입니다. 통합해야 할 인터페이스가 처음부터 하나뿐이거나, 앞으로도 두 번째 구현체가 생길 가능성이 낮다면 Adapter는 실질적인 이득 없이 호출 스택만 한 단계 늘리는 결과를 낳습니다. 이런 경우에는 어댑터 클래스를 만들기보다 호출하는 쪽 코드를 필요한 형태로 직접 맞추는 편이 더 단순합니다. "나중에 구현체가 늘어날 수도 있으니 미리 추상화한다"는 판단은 실제로 두 번째 구현체가 등장하기 전까지는 대개 근거 없는 선제적 추상화(premature abstraction)이며, YAGNI 원칙에 어긋납니다.

Facade는 클라이언트가 서브시스템을 세밀하게 제어해야 하는 상황에서 오히려 방해가 될 수 있습니다. `EcommerceFacade.placeOrder()`처럼 여러 단계를 하나로 묶으면, 재고 확인만 하고 결제는 나중에 하고 싶은 클라이언트나 배송 방식을 세밀하게 조정하려는 클라이언트는 Facade가 감춘 서브시스템 API를 별도로 다시 노출해야 합니다. 즉 Facade의 단순함은 "일반적인 흐름"에만 최적화되어 있어서, 예외적인 흐름이 잦은 도메인에서는 Facade 뒤에 숨은 서브시스템을 우회하는 코드가 늘어나며 오히려 두 개의 진입점(Facade와 서브시스템 직접 호출)을 유지보수해야 하는 부담이 생깁니다.

성능 측면에서도 각 어댑터/파사드 호출은 위임을 위한 메서드 호출과 객체 생성을 최소 한 단계 이상 추가합니다. 대부분의 I/O 바운드 작업(결제 API 호출, DB 조회)에서는 이 오버헤드가 무시할 수준이지만, 초당 수백만 번 호출되는 순수 연산 경로(예: 수치 계산 라이브러리 어댑터)에 무분별하게 적용하면 이 오버헤드가 누적되어 측정 가능한 성능 저하로 이어질 수 있습니다. 이런 경로에서는 어댑터를 두기 전에 실제 오버헤드를 벤치마크로 확인하는 것이 안전합니다.

---

**핵심 포인트**: Adapter는 호환성 문제를 해결하고, Facade는 복잡성을 숨깁니다. 두 패턴 모두 시스템 간의 결합도를 낮추고 유지보수성을 향상시킵니다. 