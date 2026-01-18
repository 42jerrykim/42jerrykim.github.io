---
collection_order: 71
title: "[Design Patterns] 어댑터와 파사드 패턴 실습 - 인터페이스 통합과 단순화"
description: "Adapter와 Facade 패턴을 활용하여 레거시 시스템 통합과 복잡한 서브시스템 단순화를 실습합니다. 결제 시스템 통합, E-commerce 파사드, 데이터 소스 통합 등의 실무 시나리오를 통해 인터페이스 설계의 철학과 시스템 간 결합도를 낮추는 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-07T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Interface Design
- Practice
- System Integration
tags:
- Adapter Pattern Practice
- Facade Pattern Practice
- Interface Design
- System Integration
- Legacy System
- Payment System Integration
- E-commerce Facade
- Data Source Integration
- External API Wrapper
- Subsystem Simplification
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Structural Patterns
- Design Patterns
- GoF Patterns
- API Gateway
- Microservices
- Software Architecture
- Interface Philosophy
- Compatibility Layer
- 어댑터 패턴 실습
- 파사드 패턴 실습
- 인터페이스 설계
- 시스템 통합
- 레거시 시스템
- 결제 시스템 통합
- 이커머스 파사드
- 데이터 소스 통합
- 외부 API 래퍼
- 서브시스템 단순화
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 구조 패턴
- 디자인 패턴
- GoF 패턴
- API 게이트웨이
- 마이크로서비스
- 소프트웨어 아키텍처
- 인터페이스 철학
- 호환성 계층
---

이 실습에서는 Adapter와 Facade 패턴을 통해 레거시 시스템 통합과 복잡한 서브시스템 단순화를 경험합니다.

## 실습 목표
- 레거시 시스템과 신규 시스템 통합
- 복잡한 서브시스템을 단순한 인터페이스로 래핑
- 외부 라이브러리 의존성 격리
- 다양한 데이터 소스 통합

## 실습 1: 결제 시스템 Adapter

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
    
    // TODO: 인터페이스 변환 로직 구현
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

## 실습 2: E-commerce Facade

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

## 실습 3: 데이터 소스 통합 Adapter

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
- [ ] Adapter + Facade 조합 활용
- [ ] 확장 가능한 구조 설계
- [ ] 단위 테스트 및 통합 테스트

## 추가 도전

1. **Two-way Adapter**: 양방향 어댑터 구현
2. **Configurable Facade**: 설정 가능한 파사드
3. **Async Facade**: 비동기 처리 파사드
4. **Circuit Breaker**: 장애 격리 메커니즘

## 실무 적용

### Adapter 활용 사례
- 마이그레이션 중 시스템 통합
- 외부 API 래핑
- 데이터 포맷 변환
- 테스트 더블 구현

### Facade 활용 사례
- 마이크로서비스 API Gateway
- 복잡한 비즈니스 로직 단순화
- 레거시 모듈 현대화
- SDK/라이브러리 설계

---

**핵심 포인트**: Adapter는 호환성 문제를 해결하고, Facade는 복잡성을 숨깁니다. 두 패턴 모두 시스템 간의 결합도를 낮추고 유지보수성을 향상시킵니다. 