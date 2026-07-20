---
draft: false
collection_order: 420
image: "wordcloud.png"
description: "웹이 왜 아키텍처의 세부사항인지 다룹니다. GUI의 역사적 진자 운동, 클라이언트-서버의 변천, 그리고 Presenter 인터페이스로 웹·CLI·GraphQL을 비즈니스 규칙과 분리하는 컴파일 가능한 Java 예제를 설명합니다."
title: "[Clean Architecture] 42. 웹은 세부사항이다"
slug: web-is-detail-gui-history
date: 2026-01-18
lastmod: 2026-07-20
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Web(웹)
  - Frontend(프론트엔드)
  - HTTP(HyperText Transfer Protocol)
  - REST(Representational State Transfer)
  - GraphQL
  - HTML(HyperText Markup Language)
  - JavaScript
  - Terminal
  - Software-Architecture(소프트웨어아키텍처)
  - Technology(기술)
  - History(역사)
  - API(Application Programming Interface)
  - Interface(인터페이스)
  - Java
  - React
  - Vue
  - Presenter-Pattern
  - Use-Case
  - Pendulum-of-GUI
  - SPA
  - SSR-SSG
  - Angular
  - PHP
  - Next.js
  - gRPC
  - Isolation
---

[41장: 데이터베이스는 세부사항이다](/post/clean-architecture/database-is-detail-persistence/)에서 데이터 접근 기술을 Repository 인터페이스로 분리하는 원칙을 보았다. 이 장은 같은 원칙을 입출력 경로, 즉 웹에 적용한다. 웹은 아키텍처에서 **세부사항**이다. 비즈니스 규칙은 데이터가 웹으로 전달되는지, 콘솔로 전달되는지 **신경 쓰지 않아야** 한다.

## GUI의 진자 운동

마틴은 GUI 역사를 <strong>진자 운동(Pendulum)</strong>에 비유한다. 컴퓨팅 파워가 중앙과 클라이언트 사이를 **왔다 갔다** 한다.

```mermaid
flowchart LR
    subgraph Pendulum [진자 운동]
        CENTER[중앙 집중]
        CLIENT[클라이언트 분산]
        
        CENTER -->|시간 흐름| CLIENT
        CLIENT -->|시간 흐름| CENTER
    end
```

### 1960-70년대: 중앙 집중

메인프레임 시대에는 컴퓨팅 파워 자체가 비쌌기 때문에, 모든 처리를 한 대의 중앙 컴퓨터에 집중시키고 사용자는 문자만 주고받는 저렴한 단말기로 접속했다. 화면에 무엇을 어떻게 표시할지 결정하는 로직조차 클라이언트가 아니라 메인프레임에 있었다.

```mermaid
flowchart LR
    T1[터미널]
    T2[터미널]
    T3[터미널]
    MF[메인프레임]
    
    T1 --> MF
    T2 --> MF
    T3 --> MF
```

| 특징 | 설명 |
|------|------|
| 클라이언트 | 덤 터미널 (글자만 표시) |
| 처리 | 모두 메인프레임에서 |
| 네트워크 | 느린 시리얼 연결 |

```
// 터미널 화면
MAIN MENU
==========
1. VIEW ORDERS
2. PLACE ORDER
3. EXIT

ENTER CHOICE: _
```

### 1980-90년대: 클라이언트로 분산

PC의 가격이 내려가고 성능이 오르자, 진자는 반대로 움직였다. 각 PC가 자체적으로 화면을 그리고 비즈니스 로직까지 실행하는 <strong>팻 클라이언트(fat client)</strong>가 등장했고, 서버는 데이터베이스 역할만 남았다. 문제는 비즈니스 로직이 각 PC의 실행 파일 안에 흩어져, 로직을 바꾸려면 모든 사용자의 PC에 새 버전을 재배포해야 했다는 점이다.

```mermaid
flowchart TB
    subgraph Clients [팻 클라이언트]
        PC1["PC + GUI"]
        PC2["PC + GUI"]
        PC3["PC + GUI"]
    end
    
    SERVER[서버<br/>DB만]
    
    Clients --> SERVER
```

| 특징 | 설명 |
|------|------|
| 클라이언트 | 팻 클라이언트 (많은 로직) |
| 처리 | 대부분 클라이언트에서 |
| 기술 | Visual Basic, Delphi |

```vb
' Visual Basic 클라이언트 코드
Private Sub btnOrder_Click()
    ' 클라이언트에서 비즈니스 로직 실행!
    If ValidateOrder() Then
        CalculateTotal
        ApplyDiscount
        ' 서버로 결과만 전송
        SendToServer
    End If
End Sub
```

### 2000년대: 다시 중앙 집중 (웹 1.0)

배포 문제를 해결한 것은 웹 브라우저였다. 재배포 없이 URL 하나로 항상 최신 버전을 실행할 수 있다는 점이 결정적이었다. 그 대가로 처리는 다시 서버로 돌아갔다 — 브라우저는 서버가 만들어 보낸 HTML을 그대로 표시하는 <strong>씬 클라이언트(thin client)</strong>가 되었고, 페이지를 조작할 때마다 서버를 다시 왕복해야 했다.

```mermaid
flowchart LR
    subgraph Clients [씬 클라이언트]
        B1[브라우저]
        B2[브라우저]
        B3[브라우저]
    end
    
    SERVER[웹 서버<br/>모든 처리]
    
    Clients --> SERVER
```

| 특징 | 설명 |
|------|------|
| 클라이언트 | 씬 클라이언트 (HTML만 표시) |
| 처리 | 서버 사이드 렌더링 |
| 기술 | PHP, JSP, ASP |

```php
<!-- PHP: 서버에서 HTML 생성 -->
<?php
$orders = $db->query("SELECT * FROM orders");
?>
<table>
<?php foreach ($orders as $order): ?>
    <tr>
        <td><?= $order['id'] ?></td>
        <td><?= $order['total'] ?></td>
    </tr>
<?php endforeach; ?>
</table>
```

### 2010년대: 다시 클라이언트로 (SPA)

AJAX가 페이지 전체를 다시 불러오지 않고도 서버와 데이터를 주고받을 수 있게 하면서, 진자는 다시 클라이언트로 향했다. React·Angular·Vue 같은 프레임워크는 브라우저 안에서 HTML을 직접 생성하는 <strong>단일 페이지 애플리케이션(SPA)</strong>을 가능하게 했고, 서버는 화면이 아니라 데이터(JSON)만 응답하는 API로 축소되었다.

```mermaid
flowchart LR
    subgraph Clients [SPA]
        R1[React App]
        R2[Angular App]
        R3[Vue App]
    end
    
    API[REST/GraphQL<br/>API 서버]
    
    Clients --> API
```

| 특징 | 설명 |
|------|------|
| 클라이언트 | 많은 JavaScript 로직 |
| 처리 | 클라이언트에서 렌더링 |
| 기술 | React, Angular, Vue |

```javascript
// React: 클라이언트에서 렌더링
function OrderList() {
    const [orders, setOrders] = useState([]);
    
    useEffect(() => {
        // API에서 데이터만 가져옴
        fetch('/api/orders')
            .then(res => res.json())
            .then(data => setOrders(data));
    }, []);
    
    // 클라이언트에서 HTML 생성
    return (
        <table>
            {orders.map(order => (
                <tr key={order.id}>
                    <td>{order.id}</td>
                    <td>{order.total}</td>
                </tr>
            ))}
        </table>
    );
}
```

### 2020년대: 또 서버로? (SSR/SSG)

SPA는 초기 로딩이 느리고 검색 엔진이 빈 HTML만 보게 된다는 약점이 있었다. Next.js(2016년 출시)로 대표되는 **서버 사이드 렌더링(SSR)** 프레임워크는 최초 화면은 서버에서 미리 그려 보내고, 이후 상호작용은 클라이언트에서 처리하는 하이브리드 방식으로 두 세계를 절충했다. 진자가 순수 클라이언트 렌더링에서 다시 서버 쪽으로 조금 움직인 것이다.

```mermaid
flowchart LR
    subgraph Hybrid [하이브리드]
        NEXT["Next.js<br/>서버 렌더링 + 클라이언트"]
        NUXT[Nuxt.js]
        REMIX[Remix]
    end
```

| 특징 | 설명 |
|------|------|
| 렌더링 | 서버 + 클라이언트 혼합 |
| 기술 | Next.js, Nuxt.js, Remix |
| 목표 | SEO + 인터랙티브 |

## 웹은 또 바뀔 것이다

진자는 계속 흔들린다:

```mermaid
timeline
    title 웹 기술의 변천 (연도는 대표 기술의 최초 공개 시점 기준)
    1993 : CGI 명세 (NCSA)
    1995 : PHP
    1999 : JSP
    2005 : AJAX (용어 등장)
    2006 : jQuery
    2010 : Angular 1
    2013 : React
    2014 : Vue
    2016 : Next.js
    2020 : SSR 회귀 트렌드 본격화
```

각 전환은 이전 기술의 약점에 대한 반작용이었다는 공통점이 있다.

| 트렌드 | 반작용의 이유 |
|--------|----------|
| 서버 렌더링 → 클라이언트 렌더링 | 서버 왕복 없이 즉각적인 상호작용을 원했다(SPA) |
| 클라이언트 렌더링 → SSR 하이브리드 | SPA의 느린 초기 로딩과 SEO 약점을 보완하려 했다(Next.js) |
| REST → GraphQL | 클라이언트마다 다른 응답 형태 요구를 하나의 유연한 쿼리로 해결하려 했다 |

> "웹 기술은 계속 변한다. 비즈니스 규칙은 이 변화에 **영향받지 않아야** 한다."

## 아키텍처에서의 위치

지금까지 살펴본 다섯 시대는 모두 "GUI가 어디서 실행되는가"의 문제였다. 클린 아키텍처의 관점에서 보면 이 질문 자체가 세부사항이다 — 비즈니스 규칙(`Use Case`, `Entity`)은 결과를 어떻게 표현할지 정하는 `Presenter Interface`만 알면 되고, 그 인터페이스를 웹 컨트롤러가 구현하는지 CLI가 구현하는지는 알 필요가 없다.

```mermaid
flowchart TB
    subgraph Core [비즈니스 규칙]
        UC[Use Case]
        ENT[Entity]
        PI[Presenter Interface]
        
        UC --> ENT
        UC --> PI
    end
    
    subgraph Details [세부사항 - 웹]
        WEB[Web Controller<br/>REST API]
        CLI[CLI Controller]
        GQL[GraphQL Controller]
        GRPC[gRPC Controller]
    end
    
    WEB -->|구현| PI
    CLI -->|구현| PI
    GQL -->|구현| PI
    GRPC -->|구현| PI
```

### 코드 예시

`OrderPresenter` 인터페이스는 코어(비즈니스 규칙)에 위치하며, Use Case가 결과를 어떤 방식으로 표현할지는 이 인터페이스의 구현체에 위임한다. 다음은 그 인터페이스 정의다.

```java
class Order { Long getId() { return 1L; } java.math.BigDecimal getTotal() { return java.math.BigDecimal.ZERO; } }

// 인터페이스: 코어에 위치
public interface OrderPresenter {
    void presentOrder(Order order);
    void presentError(String message);
}
```

동일한 인터페이스를 웹 컨트롤러가 구현하면 REST API로, CLI 클래스가 구현하면 콘솔 출력으로 결과가 나타난다. 두 구현체 모두 `getOrderUseCase`를 호출하는 방식은 같고, 결과를 사용자에게 보여주는 방식만 다르다.

```java
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.http.ResponseEntity;

class Order { Long getId() { return 1L; } java.math.BigDecimal getTotal() { return java.math.BigDecimal.ZERO; } }
interface OrderPresenter { void presentOrder(Order order); void presentError(String message); }
class GetOrderUseCase { void execute(Long id, OrderPresenter presenter) {} }
class OrderDTO { static OrderDTO from(Order order) { return new OrderDTO(); } }

// 웹 구현체: 세부사항
@RestController
public class WebOrderController implements OrderPresenter {
    private final GetOrderUseCase getOrderUseCase;
    private ResponseEntity<?> response;

    public WebOrderController(GetOrderUseCase getOrderUseCase) {
        this.getOrderUseCase = getOrderUseCase;
    }

    @GetMapping("/orders/{id}")
    public ResponseEntity<?> getOrder(@PathVariable Long id) {
        getOrderUseCase.execute(id, this);
        return response;
    }

    @Override
    public void presentOrder(Order order) {
        response = ResponseEntity.ok(OrderDTO.from(order));
    }

    @Override
    public void presentError(String message) {
        response = ResponseEntity.badRequest().body(message);
    }
}
```

동일한 `OrderPresenter`를 CLI 클래스가 구현하면, `getOrderUseCase`를 호출하는 흐름은 그대로 두고 결과를 콘솔에 출력하는 방식만 바뀐다.

```java
class Order { Long getId() { return 1L; } java.math.BigDecimal getTotal() { return java.math.BigDecimal.ZERO; } }
interface OrderPresenter { void presentOrder(Order order); void presentError(String message); }
class GetOrderUseCase { void execute(Long id, OrderPresenter presenter) {} }

// CLI 구현체: 또 다른 세부사항
public class CliOrderController implements OrderPresenter {
    private final GetOrderUseCase getOrderUseCase;

    public CliOrderController(GetOrderUseCase getOrderUseCase) {
        this.getOrderUseCase = getOrderUseCase;
    }

    public void showOrder(Long id) {
        getOrderUseCase.execute(id, this);
    }

    @Override
    public void presentOrder(Order order) {
        System.out.println("Order: " + order.getId());
        System.out.println("Total: " + order.getTotal());
    }

    @Override
    public void presentError(String message) {
        System.err.println("Error: " + message);
    }
}
```

### Use Case는 동일

`WebOrderController`와 `CliOrderController`가 각자 다른 방식으로 결과를 표시해도, 그 결과를 만들어내는 `GetOrderUseCase`는 동일하다. Use Case는 `OrderPresenter` 인터페이스만 알 뿐, 그 뒤에 웹 컨트롤러가 있는지 CLI가 있는지 전혀 알지 못한다.

```java
import java.util.Optional;

class Order {
    void checkExpiration() {}
    Long getId() { return 1L; }
    java.math.BigDecimal getTotal() { return java.math.BigDecimal.ZERO; }
}
interface OrderPresenter { void presentOrder(Order order); void presentError(String message); }
interface OrderRepository { Optional<Order> findById(Long id); }
class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(Long id) { super("Order not found: " + id); }
}

// Use Case: 웹이든 CLI든 동일
public class GetOrderUseCase {
    private final OrderRepository repository;

    public GetOrderUseCase(OrderRepository repository) {
        this.repository = repository;
    }

    public void execute(Long id, OrderPresenter presenter) {
        try {
            Order order = repository.findById(id)
                .orElseThrow(() -> new OrderNotFoundException(id));

            // 비즈니스 규칙 적용
            order.checkExpiration();

            // 프레젠터에게 결과 전달
            presenter.presentOrder(order);
        } catch (Exception e) {
            presenter.presentError(e.getMessage());
        }
    }
}
```

## 웹 기술 교체 시나리오

앞서 41장의 DB 교체 시나리오와 같은 논리가 여기서도 성립한다. REST API를 GraphQL로 바꾸는 상황을 가정해보면, `OrderPresenter`를 구현하는 새 리졸버 하나만 추가하면 되고 `GetOrderUseCase`는 손댈 필요가 없다.

```mermaid
flowchart LR
    subgraph Before [REST API]
        UC1[Use Case]
        REST[REST Controller]
    end
    
    subgraph After [GraphQL로 변경]
        UC2[Use Case]
        GQL[GraphQL Resolver]
    end
    
    UC1 -.->|동일| UC2
```

GraphQL 리졸버도 동일한 `OrderPresenter`를 구현해 `GetOrderUseCase`를 재사용한다 — 달라지는 것은 결과를 GraphQL 응답 형태로 반환하는 방식뿐이다.

```java
import com.netflix.graphql.dgs.DgsComponent;
import com.netflix.graphql.dgs.DgsQuery;
import com.netflix.graphql.dgs.InputArgument;

class Order {}
interface OrderPresenter { void presentOrder(Order order); void presentError(String message); }
class GetOrderUseCase { void execute(Long id, OrderPresenter presenter) {} }

// GraphQL 구현체 추가 (Use Case 변경 없음!)
@DgsComponent
public class GraphQLOrderResolver implements OrderPresenter {
    private final GetOrderUseCase getOrderUseCase;
    private Order result;

    public GraphQLOrderResolver(GetOrderUseCase getOrderUseCase) {
        this.getOrderUseCase = getOrderUseCase;
    }

    @DgsQuery
    public Order order(@InputArgument Long id) {
        getOrderUseCase.execute(id, this);
        return result;
    }

    @Override
    public void presentOrder(Order order) {
        this.result = order;
    }

    @Override
    public void presentError(String message) {}
}
```

## 흔한 오해

"웹은 세부사항이다"라는 말은 웹 기술을 소홀히 다뤄도 된다는 뜻이 아니다. 사용자 경험, 접근성, 브라우저 호환성은 실무에서 여전히 중요한 과제다. 마틴이 강조하는 것은 웹의 중요도가 아니라, 비즈니스 규칙이 HTTP 요청 형식이나 특정 프론트엔드 프레임워크의 존재를 알 필요가 없다는 **의존 방향**이다. `OrderPresenter` 인터페이스가 있어도 `WebOrderController`는 여전히 신중하게 설계해야 한다.

또 다른 오해는 GUI의 진자 운동(중앙 집중 ↔ 클라이언트 분산)이 "결국 다시 원점으로 돌아온다"는 뜻이라고 해석하는 것이다. 실제로는 매번 이전 세대보다 더 나은 도구(정적 타입, 컴포넌트 모델, 서버 컴포넌트)를 갖고 돌아온다 — 반복이 아니라 나선형 발전에 가깝다. 이 장의 요지는 "웹 기술을 예측하지 말라"가 아니라, **어떤 기술이 승리하든 비즈니스 규칙 코드는 한 줄도 바뀌지 않아야 한다**는 것이다.

## 학습 목표

이 장을 읽은 후 다음을 스스로 점검한다.

- "웹은 세부사항이다"라는 명제가 웹이 중요하지 않다는 뜻이 아니라 의존 방향에 대한 명제임을 설명할 수 있는가?
- GUI 역사의 진자 운동(중앙 집중 ↔ 클라이언트 분산)을 최소 세 시기의 구체적 기술로 설명할 수 있는가?
- `OrderPresenter` 인터페이스가 어떻게 Use Case를 웹·CLI·GraphQL로부터 격리하는지 코드로 보여줄 수 있는가?
- 같은 `GetOrderUseCase`가 서로 다른 프레젠터 구현체와 함께 동작하는 이유를 설명할 수 있는가?

## 판단 기준

새 코드가 비즈니스 규칙인지 웹 세부사항인지 판단할 때 다음을 확인한다.

- 이 코드가 HTTP, REST, GraphQL, 특정 프론트엔드 프레임워크의 API를 직접 언급하는가? 그렇다면 웹 세부사항이다.
- 이 코드를 실제 브라우저나 HTTP 서버 없이 단위 테스트할 수 있는가? 그렇다면 비즈니스 규칙에 가깝다.
- 이 로직을 CLI나 배치 작업으로 옮겨도 그대로 재사용할 수 있는가? 재사용할 수 있다면 이미 웹으로부터 잘 분리된 것이다.

## 참고 자료

- Robert C. Martin, 『Clean Architecture』(2017), 31장 — "The web is a detail" 원칙의 원출처.
- Robert C. Martin, ["The Clean Architecture"](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), The Clean Code Blog (2012) — "The Web is a detail" 문장의 출처.

## 핵심 요약

| 원칙 | 설명 |
|------|------|
| 웹은 세부사항 | 입출력 장치일 뿐 |
| 진자 운동 | 기술은 계속 변함 |
| 비즈니스 분리 | 웹 변화에 영향 없음 |
| 교체 가능성 | REST → GraphQL도 가능 |

> "The GUI is a detail and the web is a GUI. ... The web is nothing more than an IO device and hence we should try to isolate it from our business logic."
> — Robert C. Martin, 『Clean Architecture』(2017), 31장
