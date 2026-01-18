---
collection_order: 400
image: "wordcloud.png"
description: "세부사항의 정의와 아키텍처에서의 위치를 다룹니다. 데이터베이스, 웹, 프레임워크가 왜 세부사항이며, 비즈니스 규칙과 어떻게 분리해야 하는지 설명합니다."
title: "[Clean Architecture] 40. 세부사항 서론"
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean Architecture
  - 클린 아키텍처
  - Details
  - 세부사항
  - Database
  - 데이터베이스
  - Web
  - 웹
  - Framework
  - 프레임워크
  - UI
  - 사용자 인터페이스
  - Policy
  - 정책
  - Business Rules
  - 비즈니스 규칙
  - Plugin
  - 플러그인
  - Interchangeable
  - 교체 가능
  - Software Architecture
  - 소프트웨어 아키텍처
  - Dependency
  - 의존성
  - Abstraction
  - 추상화
  - Interface
  - 인터페이스
  - Decision Deferral
  - 결정 지연
  - Technology Choice
  - 기술 선택
  - MySQL
  - PostgreSQL
  - MongoDB
  - React
  - Angular
  - Spring
  - Django
  - Rails
  - Implementation
  - 구현
  - Infrastructure
  - 인프라스트럭처
  - Core
  - 코어
  - Adapter
  - 어댑터
  - Port
  - 포트
---

지금까지 아키텍처의 핵심 원칙들을 다루었다. 이제 **세부사항(Details)**을 살펴본다. 세부사항은 아키텍처에서 **교체 가능한** 부분들이다.

## 세부사항이란?

> **"세부사항은 정책(비즈니스 규칙)이 전혀 신경 쓰지 않아도 되는 것들이다."**
> — Robert C. Martin

```mermaid
flowchart TB
    subgraph Policy [정책 - 핵심]
        BR[비즈니스 규칙]
        UC[유스케이스]
        ENT[엔터티]
    end
    
    subgraph Details [세부사항 - 교체 가능]
        DB[(데이터베이스)]
        WEB[웹]
        FW[프레임워크]
        UI[UI]
    end
    
    Details -->|의존| Policy
```

### 세부사항의 예

| 카테고리 | 세부사항 예시 |
|----------|-------------|
| 데이터베이스 | MySQL, PostgreSQL, MongoDB, Redis |
| 웹 | HTTP, REST, GraphQL, gRPC |
| 프레임워크 | Spring, Django, Rails, Express |
| UI | React, Angular, Vue, Svelte |
| 메시징 | Kafka, RabbitMQ, SQS |
| 인프라 | AWS, GCP, Azure, Docker |

```java
// 세부사항의 예
// 비즈니스 규칙은 이것들을 모름
public class OrderService {
    // MySQL인지 MongoDB인지 모름
    private final OrderRepository repository;
    
    // HTTP인지 gRPC인지 모름
    // React인지 Angular인지 모름
    
    public Order processOrder(OrderRequest request) {
        // 순수한 비즈니스 로직만
        Order order = Order.create(request);
        order.validate();
        return repository.save(order);
    }
}
```

## 정책 vs 세부사항

```mermaid
flowchart LR
    subgraph Policy [정책]
        direction TB
        P1[비즈니스 규칙]
        P2[변경 적음]
        P3[핵심 가치]
        P4[테스트 필수]
    end
    
    subgraph Details [세부사항]
        direction TB
        D1[기술적 구현]
        D2[변경 많음]
        D3[교체 가능]
        D4[테스트 어려움]
    end
```

| 구분 | 정책 | 세부사항 |
|------|------|----------|
| 정의 | 비즈니스 규칙 | 기술적 구현 |
| 변경 빈도 | 적음 | 많음 |
| 가치 | 핵심 | 교체 가능 |
| 테스트 | 필수, 쉬움 | 어려움 |
| 의존성 | 아무것도 의존 안 함 | 정책에 의존 |

### 비즈니스 규칙 예시

```java
// 정책: 할인 규칙 (비즈니스 규칙)
public class DiscountPolicy {
    public BigDecimal calculateDiscount(Order order) {
        // 비즈니스 규칙: 10개 이상 구매 시 10% 할인
        if (order.getItemCount() >= 10) {
            return order.getSubtotal()
                .multiply(new BigDecimal("0.10"));
        }
        return BigDecimal.ZERO;
    }
}

// 이 규칙은:
// - MySQL에서 실행되든 MongoDB에서 실행되든 상관없다
// - 웹에서 호출되든 CLI에서 호출되든 상관없다
// - Spring에서 실행되든 Django에서 실행되든 상관없다
```

## 왜 세부사항을 분리하는가?

### 1. 결정 지연 (Deferring Decisions)

세부사항이 분리되면 **기술 선택을 나중에** 할 수 있다.

```mermaid
flowchart LR
    subgraph Early [조기 결정]
        E1[적은 정보]
        E2[위험한 결정]
    end
    
    subgraph Late [후기 결정]
        L1[많은 정보]
        L2[현명한 결정]
    end
    
    Early --> Late
```

```java
// 초기: DB 선택 없이 개발
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(Long id);
}

// 개발 중: 인메모리로 테스트
public class InMemoryOrderRepository implements OrderRepository {
    private final Map<Long, Order> storage = new HashMap<>();
    // ...
}

// 나중에: 실제 DB 선택
public class MySqlOrderRepository implements OrderRepository {
    // MySQL 구현
}

// 또는
public class MongoOrderRepository implements OrderRepository {
    // MongoDB 구현
}
```

### 2. 테스트 용이성

```java
// 세부사항(DB) 없이 테스트
@Test
void shouldCalculateOrderTotal() {
    // DB 없음!
    Order order = new Order();
    order.addItem(new Item("상품A", 100, 2));
    order.addItem(new Item("상품B", 200, 1));
    
    assertThat(order.getTotal()).isEqualTo(400);
    // DB 연결 없이 밀리초 만에 테스트 완료!
}

@Test
void shouldApplyDiscountForBulkOrders() {
    // 웹 서버 없음! DB 없음!
    DiscountPolicy policy = new DiscountPolicy();
    Order order = createOrderWithItems(15);  // 15개 아이템
    
    BigDecimal discount = policy.calculateDiscount(order);
    
    assertThat(discount).isGreaterThan(BigDecimal.ZERO);
}
```

### 3. 기술 변경 유연성

```mermaid
flowchart TB
    subgraph Before [MySQL 사용]
        UC1[Use Case]
        RI1[Repository Interface]
        MYSQL[(MySQL)]
        MYSQL_IMPL[MySqlRepository]
        
        UC1 --> RI1
        MYSQL_IMPL --> RI1
        MYSQL_IMPL --> MYSQL
    end
    
    subgraph After [PostgreSQL로 변경]
        UC2[Use Case]
        RI2[Repository Interface]
        PG[(PostgreSQL)]
        PG_IMPL[PostgresRepository]
        
        UC2 --> RI2
        PG_IMPL --> RI2
        PG_IMPL --> PG
    end
    
    UC1 -.->|동일| UC2
    RI1 -.->|동일| RI2
```

비즈니스 규칙(Use Case)은 **그대로**. 구현체만 교체.

## 플러그인 아키텍처

세부사항을 분리하면 **플러그인 아키텍처**가 된다.

```mermaid
flowchart TB
    subgraph Core [코어 - 변하지 않음]
        ENT[Entities]
        UC[Use Cases]
        INTF[Interfaces]
    end
    
    subgraph Plugins [플러그인 - 교체 가능]
        DB[(Database)]
        WEB[Web]
        UI[UI]
        FW[Framework]
    end
    
    DB -->|플러그인| INTF
    WEB -->|플러그인| UC
    UI -->|플러그인| UC
    FW -->|플러그인| Core
```

```java
// 플러그인처럼 교체 가능한 세부사항
public class Application {
    public static void main(String[] args) {
        // 플러그인 선택
        OrderRepository repo = selectRepository(args);
        PaymentGateway payment = selectPaymentGateway(args);
        NotificationService notification = selectNotification(args);
        
        // 코어에 플러그인 주입
        OrderService service = new OrderService(repo, payment, notification);
        
        // 실행
        new WebServer(service).start();
    }
    
    static OrderRepository selectRepository(String[] args) {
        String type = args[0];
        return switch (type) {
            case "mysql" -> new MySqlOrderRepository();
            case "postgres" -> new PostgresOrderRepository();
            case "mongo" -> new MongoOrderRepository();
            default -> new InMemoryOrderRepository();
        };
    }
}
```

## 이 파트에서 다룰 내용

```mermaid
flowchart LR
    P6[6부: 세부사항] --> C30[30장: 데이터베이스]
    P6 --> C31[31장: 웹]
    P6 --> C32[32장: 프레임워크]
    P6 --> C33[33장: 사례 연구]
    P6 --> C34[34장: 빠진 장]
```

| 장 | 제목 | 핵심 내용 |
|----|------|----------|
| 30장 | 데이터베이스는 세부사항이다 | 관계형 DB의 역사, 디스크와 RAM |
| 31장 | 웹은 세부사항이다 | GUI의 진자 운동, 클라이언트-서버 |
| 32장 | 프레임워크는 세부사항이다 | 프레임워크와 결혼의 위험 |
| 33장 | 사례 연구 | 비디오 판매 시스템 실제 설계 |
| 34장 | 빠져 있는 장 | 패키지 구조 접근법 |

## 핵심 요약

```mermaid
flowchart TB
    subgraph Summary [요약]
        S1[세부사항 = 교체 가능한 것]
        S2[정책 = 핵심 비즈니스]
        S3[세부사항이 정책에 의존]
        S4[플러그인 아키텍처]
    end
```

| 원칙 | 설명 |
|------|------|
| 세부사항의 정의 | 정책이 신경 쓰지 않아도 되는 것 |
| 의존성 방향 | 세부사항 → 정책 |
| 이점 | 결정 지연, 테스트 용이성, 기술 변경 유연성 |
| 결과 | 플러그인 아키텍처 |

> **"세부사항을 분리하면, 정책이 세부사항에 의존하지 않는다. 세부사항이 정책에 의존한다. 이것이 플러그인 아키텍처다."**
> — Robert C. Martin
