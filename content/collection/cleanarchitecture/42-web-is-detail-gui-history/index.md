---
collection_order: 420
image: "wordcloud.png"
description: "웹이 왜 아키텍처의 세부사항인지 다룹니다. GUI의 역사적 진자 운동, 클라이언트-서버의 변천, 그리고 웹 기술이 비즈니스 규칙과 분리되어야 하는 이유를 설명합니다."
title: "[Clean Architecture] 42. 웹은 세부사항이다"
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean Architecture
  - 클린 아키텍처
  - Web
  - 웹
  - GUI
  - 그래픽 사용자 인터페이스
  - Client Server
  - 클라이언트 서버
  - Browser
  - 브라우저
  - HTTP
  - REST
  - GraphQL
  - HTML
  - JavaScript
  - Single Page Application
  - SPA
  - Server Side Rendering
  - SSR
  - Pendulum
  - 진자
  - Oscillation
  - 진동
  - Terminal
  - 터미널
  - Mainframe
  - 메인프레임
  - Desktop
  - 데스크톱
  - Mobile
  - 모바일
  - Software Architecture
  - 소프트웨어 아키텍처
  - Details
  - 세부사항
  - Business Rules
  - 비즈니스 규칙
  - UI
  - 사용자 인터페이스
  - Technology
  - 기술
  - History
  - 역사
  - Change
  - 변화
  - Client
  - 클라이언트
  - Server
  - 서버
  - Thick Client
  - 팻 클라이언트
  - Thin Client
  - 씬 클라이언트
---

웹은 아키텍처에서 **세부사항**이다. 비즈니스 규칙은 데이터가 웹으로 전달되는지, 콘솔로 전달되는지 **신경 쓰지 않아야** 한다.

## GUI의 진자 운동

마틴은 GUI 역사를 **진자 운동(Pendulum)**에 비유한다. 컴퓨팅 파워가 중앙과 클라이언트 사이를 **왔다 갔다** 한다.

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

```mermaid
flowchart TB
    subgraph Clients [팻 클라이언트]
        PC1[PC + GUI]
        PC2[PC + GUI]
        PC3[PC + GUI]
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

```mermaid
flowchart LR
    subgraph Hybrid [하이브리드]
        NEXT[Next.js<br/>서버 렌더링 + 클라이언트]
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
    title 웹 기술의 변천
    1990 : CGI, Perl
    1995 : PHP, JSP
    2005 : AJAX, jQuery
    2010 : Angular 1
    2013 : React
    2016 : Vue
    2020 : Next.js, SSR 회귀
    2025 : ???
```

| 트렌드 | 예측 불가 |
|--------|----------|
| 서버 렌더링 → 클라이언트 렌더링 | 또 바뀔 것 |
| REST → GraphQL | → ??? |
| React → Next.js | → ??? |

> "웹 기술은 계속 변한다. 비즈니스 규칙은 이 변화에 **영향받지 않아야** 한다."

## 아키텍처에서의 위치

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

```java
// 인터페이스: 코어에 위치
public interface OrderPresenter {
    void presentOrder(Order order);
    void presentError(String message);
}

// 웹 구현체: 세부사항
@RestController
public class WebOrderController implements OrderPresenter {
    
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

// CLI 구현체: 또 다른 세부사항
public class CliOrderController implements OrderPresenter {
    
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

```java
// Use Case: 웹이든 CLI든 동일
public class GetOrderUseCase {
    private final OrderRepository repository;
    
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

```java
// GraphQL 구현체 추가 (Use Case 변경 없음!)
@DgsComponent
public class GraphQLOrderResolver implements OrderPresenter {
    
    @DgsQuery
    public Order order(@InputArgument Long id) {
        getOrderUseCase.execute(id, this);
        return result;
    }
    
    @Override
    public void presentOrder(Order order) {
        this.result = order;
    }
}
```

## 핵심 요약

```mermaid
flowchart TB
    subgraph Summary [요약]
        S1[웹 = 세부사항]
        S2[GUI 기술은 계속 변함]
        S3[비즈니스 규칙은 불변]
        S4[입출력 방식으로 분리]
    end
```

| 원칙 | 설명 |
|------|------|
| 웹은 세부사항 | 입출력 장치일 뿐 |
| 진자 운동 | 기술은 계속 변함 |
| 비즈니스 분리 | 웹 변화에 영향 없음 |
| 교체 가능성 | REST → GraphQL도 가능 |

> **"웹은 입출력 장치일 뿐이다. 비즈니스 규칙은 데이터가 어떻게 전달되는지 알 필요 없다."**
> — Robert C. Martin
