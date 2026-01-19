---
draft: true
collection_order: 370
image: "wordcloud.png"
description: "서비스 아키텍처에 대한 오해와 진실을 다룹니다. 서비스가 아키텍처 경계가 아닐 수 있으며, 마이크로서비스가 만병통치약이 아닌 이유를 설명합니다."
title: "[Clean Architecture] 37. 서비스: 아키텍처 경계인가?"
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean Architecture
  - 클린 아키텍처
  - Service
  - 서비스
  - Microservice
  - 마이크로서비스
  - Service Oriented Architecture
  - SOA
  - 서비스 지향 아키텍처
  - Architecture Boundary
  - 아키텍처 경계
  - Decoupling
  - 디커플링
  - Independent Deployment
  - 독립 배포
  - Independent Development
  - 독립 개발
  - Network
  - 네트워크
  - Latency
  - 지연
  - Coupling
  - 결합
  - Interface
  - 인터페이스
  - Shared Data
  - 공유 데이터
  - Cross Cutting Concern
  - 횡단 관심사
  - Taxi Aggregator
  - 택시 집계
  - Software Architecture
  - 소프트웨어 아키텍처
  - Monolith
  - 모놀리스
  - Component
  - 컴포넌트
  - Function
  - 함수
  - Boundary
  - 경계
  - Fallacy
  - 오류
  - Misconception
  - 오해
---

서비스는 아키텍처에서 특별한 위치를 차지하는가? 마틴은 **서비스에 대한 오해**를 지적한다.

## 서비스에 대한 흔한 오해

마이크로서비스가 인기를 얻으면서 많은 오해가 생겼다.

```mermaid
flowchart TB
    subgraph Misconceptions [흔한 오해]
        M1[서비스는 디커플링된다]
        M2[서비스는 독립 개발/배포 가능하다]
        M3[마이크로서비스 = 좋은 아키텍처]
    end
```

### 오해 1: 서비스는 디커플링된다

네트워크로 분리되어 있으니 디커플링된 것인가?

```mermaid
flowchart LR
    SA[Service A] -->|HTTP| SB[Service B]
    
    subgraph Reality [현실]
        R1[공유 데이터 = 결합]
        R2[인터페이스 변경 = 양쪽 영향]
        R3[네트워크 오류 처리 필요]
    end
```

```java
// Service A
@RestController
public class OrderController {
    @PostMapping("/orders")
    public OrderResponse createOrder(@RequestBody OrderRequest request) {
        // Service B 호출
        CustomerResponse customer = customerClient.getCustomer(
            request.getCustomerId()
        );
        
        // CustomerResponse의 구조에 의존!
        if (customer.getStatus().equals("ACTIVE")) {
            // ...
        }
    }
}

// Service B의 응답 형식이 바뀌면?
// → Service A도 수정 필요!
// → 디커플링이 아님
```

**실제 결합 요소:**

| 결합 유형 | 설명 | 영향 |
|----------|------|------|
| 데이터 결합 | 같은 DB 공유 | 스키마 변경 시 함께 변경 |
| API 결합 | 서비스 간 API 호출 | 인터페이스 변경 시 소비자 영향 |
| 의미 결합 | 같은 개념(Customer 등) 공유 | 비즈니스 로직 변경 시 영향 |

### 오해 2: 서비스는 독립 개발/배포된다

실제로는:

```mermaid
flowchart TB
    subgraph SharedThings [공유하는 것들]
        SCHEMA[데이터 스키마]
        API[API 계약]
        MSG[메시지 형식]
    end
    
    CHANGE[변경] --> SharedThings
    SharedThings --> S1[Service A 수정]
    SharedThings --> S2[Service B 수정]
    SharedThings --> S3[Service C 수정]
```

```java
// 공유 데이터 스키마
CREATE TABLE orders (
    customer_id INT REFERENCES customers(id),
    -- customers 테이블이 바뀌면?
    -- 모든 서비스가 영향 받음!
);
```

| 공유 항목 | 변경 시 영향 |
|----------|-------------|
| 데이터 스키마 | 모든 서비스 함께 변경 |
| API 계약 | 모든 소비자 영향 |
| 메시지 형식 | 모든 구독자 영향 |
| 공유 라이브러리 | 모든 사용처 재배포 |

## 택시 집계 예제

마틴은 **택시 배차 시스템**을 예로 든다.

### 초기 설계

```mermaid
flowchart LR
    subgraph Microservices [마이크로서비스 아키텍처]
        TF[TaxiFinder<br/>택시 찾기]
        TS[TaxiSelector<br/>택시 선택]
        TD[TaxiDispatcher<br/>택시 배차]
    end
    
    USER[사용자] --> TF --> TS --> TD --> TAXI[택시]
```

각 서비스가 독립적으로 보인다...

### 새 요구사항: "고양이 운송 서비스 추가"

```mermaid
flowchart TB
    REQ[새 요구사항:<br/>고양이 운송 서비스]
    
    TF[TaxiFinder<br/>- 고양이 허용 차량 필터]
    TS[TaxiSelector<br/>- 고양이 운송료 계산]
    TD[TaxiDispatcher<br/>- 고양이 알림 전송]
    
    REQ --> TF
    REQ --> TS
    REQ --> TD
```

**모든 서비스가 변경 필요!** 왜?

```java
// 횡단 관심사: "고양이 운송"
// TaxiFinder 변경
public class TaxiFinder {
    List<Taxi> findAvailable(RideRequest request) {
        // 새로운 조건 추가
        if (request.hasCat()) {
            taxis = filterCatFriendly(taxis);
        }
    }
}

// TaxiSelector 변경
public class TaxiSelector {
    Taxi select(List<Taxi> taxis, RideRequest request) {
        // 새로운 요금 계산
        if (request.hasCat()) {
            price += catSurcharge;
        }
    }
}

// TaxiDispatcher 변경
public class TaxiDispatcher {
    void dispatch(Taxi taxi, RideRequest request) {
        // 새로운 알림
        if (request.hasCat()) {
            notifyDriver("승객이 고양이와 함께합니다");
        }
    }
}
```

> "서비스가 **횡단 관심사**를 공유하기 때문에, 기능이 여러 서비스에 걸쳐 흩어진다."

## 서비스 vs 아키텍처 경계

**중요한 통찰**: 서비스는 **프로세스 경계**이지, **아키텍처 경계**가 아니다.

```mermaid
flowchart TB
    subgraph Service [하나의 서비스]
        CTRL[Controller<br/>UI 어댑터]
        UC[Use Case<br/>비즈니스 로직]
        GW[Gateway<br/>데이터 어댑터]
        
        CTRL --> UC --> GW
    end
    
    subgraph Inside [서비스 내부에도 경계 필요]
        B1[UI ↔ 비즈니스]
        B2[비즈니스 ↔ 데이터]
    end
```

### 서비스 안에서도 Clean Architecture

```java
// 서비스 내부에도 아키텍처 경계가 있어야 함
@Service
public class TaxiFinderService {
    
    // Controller (외부 경계)
    @GetMapping("/taxis")
    public List<TaxiDTO> findTaxis(RideRequestDTO dto) {
        // DTO → 도메인 객체 변환
        RideRequest request = toRideRequest(dto);
        
        // Use Case 호출 (내부 경계)
        List<Taxi> taxis = findTaxisUseCase.execute(request);
        
        // 도메인 객체 → DTO 변환
        return toTaxiDTOs(taxis);
    }
}

// Use Case (핵심 비즈니스)
public class FindTaxisUseCase {
    private final TaxiGateway gateway;  // 인터페이스
    
    public List<Taxi> execute(RideRequest request) {
        // 비즈니스 로직
        List<Taxi> available = gateway.findAvailable(request.getLocation());
        return filterByCapacity(available, request.getPassengers());
    }
}
```

## 서비스의 진짜 가치

서비스가 제공하는 **진짜** 가치:

```mermaid
flowchart TB
    subgraph RealValue [서비스의 진짜 가치]
        SCALE[확장성<br/>여러 인스턴스]
        TEAM[팀 독립성<br/>팀별 서비스]
        TECH[기술 다양성<br/>다른 언어/DB]
        DEPLOY[배포 유연성<br/>독립 배포 가능]
    end
```

| 가치 | 설명 |
|------|------|
| 확장성 | 필요한 서비스만 인스턴스 추가 |
| 팀 독립성 | 각 팀이 자신의 서비스 소유 |
| 기술 다양성 | 서비스별 다른 기술 스택 가능 |
| 배포 유연성 | 전체 재배포 없이 일부만 |

### 하지만...

```mermaid
flowchart LR
    VALUE[이런 가치들] 
    MUST["반드시 서비스여야</br>얻는 건 아니다"]
    
    VALUE --> MUST
```

- **확장성**: 컴포넌트 분리로도 가능
- **팀 독립성**: 모듈 분리로도 가능
- **기술 다양성**: 플러그인으로도 가능

## 결론: 서비스와 아키텍처

```java
// 나쁜 예: 서비스만 믿고 내부 아키텍처 무시
@RestController
public class OrderService {
    @Autowired
    private JdbcTemplate jdbc;  // DB 직접 접근
    
    @PostMapping("/orders")
    public String create(@RequestBody Map<String, Object> body) {
        // SQL이 컨트롤러에!
        jdbc.update("INSERT INTO orders ...");
        return "OK";
    }
}

// 좋은 예: 서비스 내부에도 Clean Architecture
@RestController
public class OrderController {
    private final CreateOrderUseCase createOrder;
    
    @PostMapping("/orders")
    public OrderResponse create(@RequestBody OrderRequest request) {
        Order order = createOrder.execute(request.toDomain());
        return OrderResponse.from(order);
    }
}
```

## 핵심 요약

| 오해 | 진실 |
|------|------|
| 서비스 = 디커플링 | 공유 데이터/API로 결합됨 |
| 서비스 = 독립 배포 | 공유 요소 변경 시 함께 배포 |
| 서비스 = 아키텍처 경계 | 프로세스 경계일 뿐 |
| 마이크로서비스 = 좋은 아키텍처 | 내부 아키텍처가 더 중요 |

> **"서비스는 프로세스 경계이지, 아키텍처 경계가 아니다. 서비스 안에서도 Clean Architecture가 필요하다."**
> — Robert C. Martin
