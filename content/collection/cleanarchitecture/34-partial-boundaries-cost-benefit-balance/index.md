---
collection_order: 340
image: "wordcloud.png"
description: "부분적 경계 전략을 다룹니다. 완전한 경계의 비용이 부담될 때 사용할 수 있는 세 가지 부분적 경계 패턴과 각각의 장단점을 설명합니다."
title: "[Clean Architecture] 34. 부분적 경계"
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean Architecture
  - 클린 아키텍처
  - Partial Boundary
  - 부분적 경계
  - Full Boundary
  - 완전한 경계
  - Cost
  - 비용
  - YAGNI
  - You Aren't Gonna Need It
  - Strategy Pattern
  - 전략 패턴
  - Facade Pattern
  - 퍼사드 패턴
  - Skip Last Step
  - 마지막 단계 건너뛰기
  - One Dimensional Boundary
  - 단방향 경계
  - Interface
  - 인터페이스
  - Component
  - 컴포넌트
  - Deployment
  - 배포
  - Software Architecture
  - 소프트웨어 아키텍처
  - Trade off
  - 트레이드오프
  - Flexibility
  - 유연성
  - Simplicity
  - 단순성
  - Service
  - 서비스
  - Module
  - 모듈
  - Boundary
  - 경계
  - Future
  - 미래
  - Prediction
  - 예측
  - Technical Debt
  - 기술 부채
---

완전한 경계를 만드는 비용은 **상당하다**. 때로는 완전한 경계가 **과도할** 수 있다. 부분적 경계는 비용을 줄이면서 일부 이점을 얻는 방법이다.

## 완전한 경계의 비용

```mermaid
flowchart TB
    subgraph FullBoundary [완전한 경계 비용]
        INTF[양쪽에 인터페이스 정의]
        DS[양쪽에 데이터 구조]
        DEP[독립적 컴포넌트로 분리]
        MANAGE[의존성 관리]
        MAINT[지속적 유지보수]
    end
```

완전한 아키텍처 경계를 만들려면:

| 비용 항목 | 설명 |
|----------|------|
| 인터페이스 정의 | 경계 양쪽에 인터페이스 필요 |
| 데이터 구조 | 경계를 넘는 데이터 구조 정의 |
| 독립 컴포넌트 | 별도 jar/dll로 분리 |
| 의존성 관리 | 컴포넌트 간 버전 관리 |
| 유지보수 비용 | 지속적인 관리 필요 |

> "완전한 경계를 만드는 비용은 **상당하며**, 유지보수 비용도 높다."

## 부분적 경계가 필요한 상황

```mermaid
flowchart TB
    QUESTION{경계가 필요할까?}
    
    YES[확실히 필요함]
    MAYBE[필요할 수도...]
    NO[필요 없을 것 같음]
    
    QUESTION --> YES --> FULL[완전한 경계]
    QUESTION --> MAYBE --> PARTIAL[부분적 경계]
    QUESTION --> NO --> NONE[경계 없음]
```

| 상황 | 권장 전략 |
|------|----------|
| 경계가 확실히 필요 | 완전한 경계 |
| 불확실하지만 가능성 있음 | 부분적 경계 |
| YAGNI (필요 없을 것) | 경계 없음 |

## 세 가지 부분적 경계 전략

### 1. 마지막 단계 건너뛰기 (Skip the Last Step)

인터페이스는 만들지만, **별도 컴포넌트로 분리하지 않음**.

```mermaid
flowchart TB
    subgraph SameComponent [같은 컴포넌트]
        CLIENT[Client]
        INTF[Interface]
        IMPL[Implementation]
        
        CLIENT --> INTF
        IMPL -->|구현| INTF
    end
```

```java
// 같은 패키지에 있지만 인터페이스로 분리
package com.example.order;

// 인터페이스
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(Long id);
}

// 구현
public class JpaOrderRepository implements OrderRepository {
    private final EntityManager em;
    
    @Override
    public void save(Order order) {
        em.persist(OrderEntity.from(order));
    }
    
    @Override
    public Optional<Order> findById(Long id) {
        return Optional.ofNullable(em.find(OrderEntity.class, id))
            .map(OrderEntity::toDomain);
    }
}

// 나중에 필요하면 별도 jar로 분리 가능!
```

| 장점 | 단점 |
|------|------|
| 나중에 쉽게 분리 가능 | 같은 컴포넌트라 의존성 침해 가능 |
| 적은 초기 비용 | 분리를 미루다 보면 영원히 안 할 수도 |
| 인터페이스 설계 강제 | 실제 독립성은 없음 |

### 2. 단방향 경계 (One-Dimensional Boundary)

양방향 인터페이스 대신 **한쪽만** 인터페이스를 사용한다.

```mermaid
flowchart LR
    subgraph Bidirectional [양방향 - 완전한 경계]
        A1[Client] --> I1[Interface]
        I2[Interface] --> A1
        IMPL1[Impl] --> I1
        IMPL1 --> I2
    end
```

```mermaid
flowchart LR
    subgraph Unidirectional [단방향 - 부분적 경계]
        B1[Client]
        I3[Strategy Interface]
        IMPL2[Concrete Strategy]
        
        B1 --> I3
        IMPL2 -->|구현| I3
    end
```

**전략 패턴을 활용한 단방향 경계:**

```java
// 단방향 경계: 전략 패턴
public class PaymentService {
    private final PaymentStrategy strategy;  // 인터페이스
    
    public PaymentResult process(Order order) {
        return strategy.charge(order.getTotal());
    }
}

// 전략 인터페이스
public interface PaymentStrategy {
    PaymentResult charge(BigDecimal amount);
}

// 구체적인 전략들
public class StripePaymentStrategy implements PaymentStrategy {
    public PaymentResult charge(BigDecimal amount) {
        // Stripe API 호출
    }
}

public class PayPalPaymentStrategy implements PaymentStrategy {
    public PaymentResult charge(BigDecimal amount) {
        // PayPal API 호출
    }
}
```

| 장점 | 단점 |
|------|------|
| 더 간단함 | 양방향 분리 미흡 |
| 전략 교체 가능 | 클라이언트가 구현에 의존할 위험 |
| 빠른 구현 | 역방향 의존성 제어 어려움 |

### 3. 퍼사드 패턴 (Facade Pattern)

경계 없이 **퍼사드로 접근 제한**.

```mermaid
flowchart TB
    subgraph Public [외부 공개]
        FACADE[Facade]
    end
    
    subgraph Private [내부 숨김]
        S1[Service1]
        S2[Service2]
        S3[Service3]
    end
    
    CLIENT[Client] --> FACADE
    FACADE --> S1
    FACADE --> S2
    FACADE --> S3
```

```java
// 퍼사드: 내부 구현을 숨김
public class OrderFacade {
    private final OrderService orderService;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    
    // 클라이언트는 퍼사드만 사용
    public OrderResult placeOrder(OrderRequest request) {
        // 내부 서비스들 조합
        inventoryService.reserve(request.getItems());
        paymentService.charge(request.getPayment());
        return orderService.create(request);
    }
    
    public void cancelOrder(Long orderId) {
        orderService.cancel(orderId);
        paymentService.refund(orderId);
        inventoryService.release(orderId);
    }
    
    // 내부 서비스들은 외부에 노출되지 않음
}
```

| 장점 | 단점 |
|------|------|
| 가장 간단함 | 의존성 역전 없음 |
| 진입점 단일화 | 클라이언트가 내부를 직접 접근 가능 |
| 최소 비용 | 경계가 매우 약함 |

## 세 가지 전략 비교

```mermaid
flowchart LR
    subgraph Strategies [부분적 경계 전략]
        SKIP[마지막 단계<br/>건너뛰기]
        ONE[단방향<br/>경계]
        FAC[퍼사드<br/>패턴]
    end
    
    SKIP -->|"강도"| ONE -->|"강도"| FAC
    
    FULL[완전한 경계] -.-> SKIP
    NONE[경계 없음] -.-> FAC
```

| 전략 | 비용 | 유연성 | 나중에 완전한 경계로 |
|------|------|--------|---------------------|
| 마지막 단계 건너뛰기 | 중간 | 높음 | 쉬움 |
| 단방향 경계 | 낮음 | 중간 | 중간 |
| 퍼사드 | 최저 | 낮음 | 어려움 |

## 선택 가이드

```mermaid
flowchart TB
    START[부분적 경계 필요]
    
    Q1{나중에 완전한<br/>경계가 필요할<br/>가능성?}
    Q2{양방향 의존성<br/>제어 필요?}
    Q3{빠른 구현<br/>필요?}
    
    START --> Q1
    
    Q1 -->|높음| SKIP[마지막 단계 건너뛰기]
    Q1 -->|중간| Q2
    Q1 -->|낮음| Q3
    
    Q2 -->|예| SKIP
    Q2 -->|아니오| ONE[단방향 경계]
    
    Q3 -->|예| FAC[퍼사드]
    Q3 -->|아니오| ONE
```

## 코드 예시: 같은 문제, 세 가지 해법

### 문제: 알림 서비스

```java
// 완전한 경계: 별도 컴포넌트
// notification-api.jar
public interface NotificationGateway {
    void send(Notification notification);
}

// notification-email.jar (별도 배포)
public class EmailNotificationGateway implements NotificationGateway {
    public void send(Notification notification) {
        // 이메일 발송
    }
}
```

```java
// 부분적 경계 1: 마지막 단계 건너뛰기
// 같은 jar에 있지만 인터페이스 분리
package com.example.notification;

public interface NotificationGateway {
    void send(Notification notification);
}

public class EmailNotificationGateway implements NotificationGateway {
    // 같은 패키지, 나중에 분리 가능
}
```

```java
// 부분적 경계 2: 단방향 경계
public class OrderService {
    private final NotificationSender sender;  // 단방향
    
    public void placeOrder(Order order) {
        // 주문 처리
        sender.sendOrderConfirmation(order);
    }
}
```

```java
// 부분적 경계 3: 퍼사드
public class NotificationFacade {
    private final EmailService email;
    private final SmsService sms;
    private final PushService push;
    
    public void notifyOrderPlaced(Order order) {
        email.sendOrderConfirmation(order);
        if (order.getCustomer().hasMobile()) {
            sms.sendOrderConfirmation(order);
        }
    }
}
```

## 핵심 요약

| 원칙 | 설명 |
|------|------|
| 비용 고려 | 완전한 경계는 비용이 높음 |
| 미래 예측 | 나중에 필요할 가능성 평가 |
| 단계적 접근 | 부분적 경계로 시작, 필요 시 확장 |
| 트레이드오프 | 비용 vs 유연성 균형 |

> **"부분적 경계는 나중을 위한 자리 표시자다. 필요하면 완전한 경계로 발전시킬 수 있다."**
> — Robert C. Martin
