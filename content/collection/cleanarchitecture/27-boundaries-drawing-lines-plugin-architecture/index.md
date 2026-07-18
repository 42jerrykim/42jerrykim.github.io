---
draft: true
collection_order: 270
image: "wordcloud.png"
description: "아키텍처에서 경계를 긋는 방법과 시점을 다룹니다. 비즈니스 규칙과 세부사항 사이에 경계를 설정해 플러그인 아키텍처를 구현하는 방법을, 마틴의 FitNesse 프로젝트 실제 사례와 결제 게이트웨이 예제로 자세히 설명합니다."
title: "[Clean Architecture] 27. 경계: 선 긋기와 플러그인 아키텍처"
slug: boundaries-drawing-lines-plugin-architecture
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Software-Architecture(소프트웨어아키텍처)
  - Database(데이터베이스)
  - Frontend(프론트엔드)
  - Interface(인터페이스)
  - Dependency-Injection(의존성주입)
  - IO(Input/Output)
  - Coupling(결합도)
  - Testing(테스트)
  - Design-Pattern(디자인패턴)
  - Abstraction(추상화)
  - Modularity
  - Best-Practices
  - Maintainability
  - Refactoring(리팩토링)
  - History(역사)
  - Case-Study
  - Technology(기술)
  - Backend(백엔드)
  - API(Application Programming Interface)
  - OOP(객체지향)
  - Java
  - Domain(도메인)
  - Web(웹)
  - Encapsulation(캡슐화)
---

아키텍처에서 **경계(Boundary)**란 관심사를 분리하는 선이다. 경계의 한쪽에는 비즈니스 규칙이, 다른 쪽에는 세부사항이 있다. 경계를 제대로 그으면 **플러그인 아키텍처**가 된다.

## 경계란?

> "경계는 소프트웨어 요소를 분리하고, 한쪽이 다른 쪽을 모르게 한다."
> — Robert C. Martin

```mermaid
flowchart LR
    subgraph Left [한쪽]
        A[비즈니스 규칙]
    end
    
    BOUNDARY[경계선]
    
    subgraph Right [다른 쪽]
        B[세부사항]
    end
    
    A --- BOUNDARY --- B
```

### 어디에 경계를 긋는가?

**관련 없는 것들 사이에** 경계를 긋는다:

| 경계의 한쪽 | 경계의 다른 쪽 |
|------------|---------------|
| 비즈니스 규칙 | GUI |
| 비즈니스 규칙 | 데이터베이스 |
| 비즈니스 규칙 | 프레임워크 |
| 비즈니스 규칙 | 외부 서비스 |

```java
// 경계를 긋기 전: 모든 것이 섞여있음
public class OrderService {
    public void createOrder(Request request) {
        // GUI에 대한 지식
        String json = parseJsonFromHttpRequest(request);
        
        // 비즈니스 규칙
        Order order = new Order(json);
        order.validate();
        
        // DB에 대한 지식
        Connection conn = DriverManager.getConnection("...");
        PreparedStatement stmt = conn.prepareStatement("INSERT...");
    }
}
```

```java
// 경계를 긋고 난 후: 깔끔하게 분리됨
public class CreateOrderUseCase {
    private final OrderRepository repository;  // 인터페이스
    
    public void execute(OrderRequest request) {
        // 비즈니스 규칙만 알고 있음
        Order order = new Order(request);
        order.validate();
        repository.save(order);
        // DB가 MySQL인지, 파일인지 모름
    }
}
```

## FitNesse 사례

마틴은 자신이 개발한 **FitNesse** 프로젝트 경험을 공유한다.

### 조기 결정의 유혹

```mermaid
flowchart LR
    subgraph Temptation [유혹]
        T1[MySQL이 필요할 것 같아]
        T2[지금 당장 선택하자]
        T3[나중에 바꾸기 어려워]
    end
```

초기에 MySQL을 선택하고 싶었지만, **결정을 미뤘다**. 데이터베이스 선택 없이 개발을 진행했다.

### 경계를 먼저 그음

```java
// FitNesse의 데이터 접근 인터페이스
public interface WikiPagePersistence {
    WikiPage load(String pageName);
    void save(WikiPage page);
    List<WikiPage> findAll();
}

// 비즈니스 규칙은 이 인터페이스만 알면 됨
public class WikiPageService {
    private final WikiPagePersistence persistence;
    
    public WikiPage getPage(String name) {
        return persistence.load(name);
    }
}
```

### 결과

| 진행 단계 | 상태 |
|----------|------|
| 초기 개발 | 파일 시스템으로 구현 |
| 나중에 | MySQL 옵션 추가 |
| 최종 | 사용자가 선택 |

```java
// 파일 시스템 구현
public class FileSystemWikiPagePersistence implements WikiPagePersistence {
    public WikiPage load(String pageName) {
        // 파일에서 읽기
        return readFromFile(pageName);
    }
}

// MySQL 구현 (나중에 추가)
public class MySqlWikiPagePersistence implements WikiPagePersistence {
    public WikiPage load(String pageName) {
        // MySQL에서 읽기
        return readFromDatabase(pageName);
    }
}
```

> "놀랍게도 MySQL이 필요 없었다. 파일 시스템만으로 충분했다. 우리는 **결정을 미루는 데 성공**했고, 그 덕분에 불필요한 복잡성을 피할 수 있었다."

## 플러그인 아키텍처

경계를 제대로 그으면 **플러그인 아키텍처**가 된다.

```mermaid
flowchart TB
    subgraph Core [비즈니스 코어 - 중심]
        BR[Business Rules]
        UC[Use Cases]
        INTF[Interfaces]
    end
    
    subgraph Plugins [플러그인들 - 외곽]
        DB[(Database)]
        GUI[GUI]
        FW[Framework]
        EXT[외부 서비스]
    end
    
    DB -->|구현| INTF
    GUI --> UC
    FW --> BR
    EXT -->|구현| INTF
```

### 플러그인 아키텍처의 특징

| 특징 | 설명 |
|------|------|
| 코어 | 비즈니스 규칙, 유스케이스, 인터페이스 |
| 플러그인 | DB, GUI, 프레임워크, 외부 서비스 |
| 의존성 방향 | 플러그인 → 코어 |
| 교체 가능성 | 플러그인은 언제든 교체 가능 |

### 코드로 보는 플러그인 아키텍처

```java
// 코어: 인터페이스 정의
public interface PaymentGateway {
    PaymentResult process(Payment payment);
}

// 플러그인 1: Stripe
public class StripeGateway implements PaymentGateway {
    public PaymentResult process(Payment payment) {
        // Stripe API 호출
        return stripeApi.charge(payment);
    }
}

// 플러그인 2: PayPal
public class PayPalGateway implements PaymentGateway {
    public PaymentResult process(Payment payment) {
        // PayPal API 호출
        return paypalApi.charge(payment);
    }
}

// 플러그인 3: 테스트용 Mock
public class MockPaymentGateway implements PaymentGateway {
    public PaymentResult process(Payment payment) {
        return PaymentResult.success();
    }
}

// 비즈니스 규칙: 플러그인을 모름
public class PaymentService {
    private final PaymentGateway gateway;
    
    public void pay(Order order) {
        Payment payment = createPayment(order);
        PaymentResult result = gateway.process(payment);
        // Stripe인지 PayPal인지 모르고 처리
    }
}
```

## 경계 긋기 규칙

### 규칙 1: 비즈니스 규칙이 UI를 모르게

```mermaid
flowchart LR
    UI[UI] --> BR[비즈니스 규칙]
    BR -.->|모름| UI
```

```java
// 나쁜 예: 비즈니스 규칙이 UI를 암
public class OrderService {
    public void createOrder(HttpServletRequest request) {  // UI 기술!
        String json = request.getParameter("order");
        // ...
    }
}

// 좋은 예: UI를 모름
public class CreateOrderUseCase {
    public void execute(CreateOrderRequest request) {  // 순수 DTO
        // ...
    }
}
```

### 규칙 2: 비즈니스 규칙이 DB를 모르게

```mermaid
flowchart LR
    DB[(Database)] --> BR[비즈니스 규칙]
    BR -.->|모름| DB
```

```java
// 나쁜 예: 비즈니스 규칙이 DB를 암
public class OrderService {
    public void save(Order order) {
        Connection conn = DriverManager.getConnection("jdbc:mysql://...");
        // ...
    }
}

// 좋은 예: DB를 모름
public class OrderService {
    private final OrderRepository repository;  // 인터페이스
    
    public void save(Order order) {
        repository.save(order);  // 구체적인 DB 기술 모름
    }
}
```

### 규칙 3: 의존성은 비즈니스 규칙을 향하게

```mermaid
flowchart TB
    subgraph Outer [바깥쪽]
        UI[UI]
        DB[(DB)]
        FW[Framework]
    end
    
    subgraph Inner [안쪽]
        BR[Business Rules]
    end
    
    UI --> BR
    DB --> BR
    FW --> BR
```

## 입력과 출력은 중요치 않다

마틴은 흥미로운 관점을 제시한다:

> "입력과 출력은 중요치 않다. **비즈니스 규칙**이 중요하다."

```mermaid
flowchart LR
    INPUT[입력<br/>Web, CLI, API] --> CORE[비즈니스 규칙<br/>핵심]
    CORE --> OUTPUT[출력<br/>DB, File, API]
```

우리는 종종 시스템을 입력/출력 관점에서 생각하지만, 실제로 **가치를 창출하는 것은 비즈니스 규칙**이다.

| 관점 | 초점 |
|------|------|
| 전통적 | 입력 → 처리 → 출력 |
| 클린 아키텍처 | 비즈니스 규칙이 중심 |

## 경계를 늦게 그으면?

경계를 늦게 그으면 다음과 같은 문제가 발생한다:

```mermaid
flowchart TB
    LATE[경계를 늦게 그음]
    
    P1[코드 결합도 증가]
    P2[테스트 어려움]
    P3[변경 비용 증가]
    P4[기술 종속]
    
    LATE --> P1 --> P2 --> P3 --> P4
```

```java
// 경계 없이 시작한 코드
public class OrderController {
    public void createOrder(HttpServletRequest req) {
        // UI, 비즈니스, DB가 모두 섞임
        String name = req.getParameter("name");
        Order order = new Order(name);
        order.setTotal(order.calculateTotal());
        
        Connection conn = DriverManager.getConnection("...");
        PreparedStatement stmt = conn.prepareStatement(
            "INSERT INTO orders VALUES (?, ?)");
        stmt.setString(1, order.getName());
        stmt.setDouble(2, order.getTotal());
        stmt.execute();
        
        // 이 코드를 분리하려면? 재작성 수준의 노력 필요
    }
}
```

## 흔한 오해

경계를 "처음부터 모든 곳에 완벽하게" 그어야 한다는 오해가 흔하다. FitNesse 사례가 보여주듯, 마틴은 오히려 결정을 미룬 채로 개발을 진행했고 결과적으로 MySQL 자체가 필요 없다는 것을 발견했다. 경계를 긋는 목적은 "지금 당장 완벽한 구조를 만드는 것"이 아니라 "나중에 바꿀 수 있는 여지를 남기는 것"이다. 또 다른 오해는 입력과 출력(Web, CLI, DB, 파일)을 아키텍처의 중심으로 여기는 것이다. 이 장이 강조하듯 입력·출력은 세부사항이고, 진짜 중심은 그 사이에서 가치를 만드는 비즈니스 규칙이다 — 입출력 기술이 바뀌어도 비즈니스 규칙은 그대로여야 한다.

## 학습 목표

이 장을 읽은 후 다음을 스스로 점검한다.

- 경계가 "관심사를 분리하는 선"이라는 정의를 실제 코드(경계 전/후)로 설명할 수 있는가?
- FitNesse 사례에서 "결정을 미루는 데 성공했다"는 말이 구체적으로 무엇을 의미하는지 설명할 수 있는가?
- 플러그인 아키텍처에서 의존성이 항상 플러그인 → 코어 방향인 이유를 설명할 수 있는가?
- "입력과 출력은 중요치 않다"는 주장의 의미를, 비즈니스 규칙이 중심이라는 관점에서 설명할 수 있는가?
- 경계를 늦게 그었을 때 발생하는 구체적 문제(결합도 증가, 테스트 어려움 등)를 코드 예로 설명할 수 있는가?

## 판단 기준

새 기능이나 외부 의존성을 추가할 때 다음을 확인한다.

- 이 코드가 비즈니스 규칙과 세부사항(UI, DB, 프레임워크, 외부 서비스) 중 무엇에 속하는가?
- 비즈니스 규칙 코드에 특정 기술(HTTP 요청 객체, JDBC 커넥션 등)의 이름이 등장하는가? 등장한다면 경계가 없는 것이다.
- 이 세부사항을 나중에 다른 구현으로 교체해야 한다면, 지금 구조에서 얼마나 많은 코드를 수정해야 하는가?

## 참고 자료

- Robert C. Martin, 『Clean Architecture』, 2017, 17장 — 경계와 플러그인 아키텍처, FitNesse 사례의 원 출처.

## 핵심 요약

| 항목 | 내용 |
|------|------|
| 경계의 정의 | 관심사를 분리하는 선 |
| 경계의 위치 | 비즈니스 규칙과 세부사항 사이 |
| 플러그인 아키텍처 | 코어는 중심, 세부사항은 플러그인 |
| 의존성 방향 | 세부사항 → 비즈니스 규칙 |
| 핵심 이점 | 세부사항 교체 가능 |

마틴은 경계를 제대로 그으면 나중에 세부사항을 바꿀 수 있지만, 경계가 없으면 갇히게 된다고 말한다(Martin, 『Clean Architecture』, 2017, 17장).
