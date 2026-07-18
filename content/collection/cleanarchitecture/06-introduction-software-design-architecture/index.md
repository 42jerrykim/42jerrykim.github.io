---
draft: true
collection_order: 60
image: "wordcloud.png"
description: "1부 소개에서는 소프트웨어를 단순히 '동작하게 만드는 것'과 올바르게 설계하여 '유지보수와 확장성까지 갖춘 제대로 된 시스템'을 만드는 것의 차이를 설명합니다. 경험이 부족한 개발자와 열정적인 전문가의 태도 차이, 그리고 훌륭한 아키텍처의 중요성을 다룹니다."
title: "[Clean Architecture] 06. 서론: 설계와 아키텍처"
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Software-Architecture(소프트웨어아키텍처)
  - Code-Quality(코드품질)
  - Scalability(확장성)
  - SOLID
  - Productivity(생산성)
  - Refactoring(리팩토링)
  - Best-Practices
  - Implementation(구현)
  - Ruby
  - Code-Review(코드리뷰)
  - Maintainability
  - Readability
  - Documentation(문서화)
  - Coupling(결합도)
  - Cohesion(응집도)
  - Testing(테스트)
  - TDD(Test-Driven Development)
  - Clean-Code(클린코드)
  - Career(커리어)
  - History(역사)
  - Case-Study
  - Deep-Dive
  - Technology(기술)
  - Agile(애자일)
  - Debugging(디버깅)
  - Modularity
---

**프로그램이 동작하도록 만드는 데 엄청난 수준의 지식과 기술이 필요하지는 않다.** 언제든 어린 고등학생이라도 할 수 있는 일이다.

## 동작하는 코드: 누구나 만들 수 있다

젊은 대학생도 PHP 또는 루비 코드 몇 줄을 이리저리 맞춰가며 **수억 달러 규모의 사업**을 시작한다. 전 세계의 수많은 초급 프로그래머가 칸막이로 나뉜 작은 사무실에서 이슈 추적 시스템에 등록된 거대한 요구사항 문서들을 순전히 강인한 정신력만으로 힘겹게 해결해 내면서 시스템을 '동작하도록' 만든다.

```mermaid
flowchart LR
    subgraph Reality [현실]
        JD[주니어 개발자]
        REQ[요구사항]
        CODE[코드 작성]
        WORK[동작하는 시스템]
    end
    
    JD --> REQ --> CODE --> WORK
    
    style WORK fill:#90EE90
```

이들이 작성한 코드는 그다지 깔끔하지 않을 순 있지만, **동작은 한다**. 프로그램을 동작하게 만들기는 그리 어려운 일이 아니기 때문이다.

### 동작하는 코드의 특징

```java
// 동작은 하지만... 좋은 코드인가?
public class OrderService {
    public void processOrder(String customerId, String productId, int qty) {
        // 데이터베이스 직접 접근
        Connection conn = DriverManager.getConnection("jdbc:mysql://...");
        Statement stmt = conn.createStatement();
        
        // 비즈니스 로직과 SQL이 뒤섞임
        ResultSet rs = stmt.executeQuery(
            "SELECT * FROM products WHERE id = '" + productId + "'");
        // ... 수백 줄의 코드
        
        // 에러 처리? 트랜잭션? 로깅?
        // "나중에 하자..."
    }
}
```

## 제대로 된 소프트웨어: 전문가의 영역

하지만 프로그램을 **제대로** 만드는 일은 전혀 다르다.

마틴은 이렇게 단언한다: 소프트웨어를 올바르게 만드는 일은 어렵다(Martin, *Clean Architecture*, 2017).

### 전문가가 되기 위한 요소

```mermaid
flowchart TB
    subgraph Requirements [전문가의 요건]
        K[지식과 기술]
        T[사고력과 통찰력]
        D[훈련과 헌신]
        P[열정과 열망]
    end
    
    subgraph Reality [현실]
        R1[대다수가 수준 미달]
        R2[능력 개발에 투자 안함]
        R3[필요성조차 인식 못함]
    end
    
    K --> R1
    T --> R2
    D --> R3
```

소프트웨어를 제대로 만들려면 네 가지가 함께 필요하다. **적정 수준의 지식과 기술**, **사고력과 통찰력**, **훈련과 헌신**, 그리고 **기술을 향한 열정**과 전문가가 되려는 **열망**이다. 위 다이어그램이 보여주듯, 대다수 프로그래머는 이 네 요건 중 어느 하나에서든 미달하기 쉽다 — 지식과 기술 수준 자체가 부족하거나, 그 수준에 도달할 시간을 투자하지 않거나, 애초에 그럴 필요성조차 인식하지 못한다.

## 마법과도 같은 일: 제대로 만들면

반면 소프트웨어를 제대로 만들게 되면 **마법과도 같은 일**이 벌어진다. 위 "천국과 지옥" 흐름도가 보여주듯, 좋은 설계는 단순히 코드가 예뻐지는 것을 넘어 조직 전체의 운영 방식을 바꾼다.

```mermaid
flowchart TB
    subgraph Before [나쁜 설계]
        B1[많은 프로그래머 필요]
        B2[거대한 요구사항 문서]
        B3[수없는 이슈]
        B4[휴일 없는 야근]
    end
    
    subgraph After [좋은 설계]
        A1[소수의 프로그래머]
        A2[간단한 문서]
        A3[적은 이슈]
        A4[적절한 업무량]
    end
    
    Before -->|제대로 된 설계| After
```

마틴은 이를 이렇게 요약한다: 제대로 된 소프트웨어를 만들면 아주 적은 인력만으로도 새로운 기능을 추가하거나 유지보수할 수 있다(Martin, *Clean Architecture*, 2017). 구체적으로는 아래 세 가지 결과로 나타난다.

| 좋은 설계의 결과 | 설명 |
|-----------------|------|
| 변경 용이성 | 변경은 단순해지고 빠르게 반영 가능 |
| 낮은 결함률 | 결함은 적어지고 잦아든다 |
| 높은 생산성 | 최소한의 노력으로 기능과 유연성 최대화 |

## 저자의 경험: 천국과 지옥

### 천국: 좋은 아키텍처

마틴은 자신의 수십 년 컨설팅 경력을 근거로, 다음과 같은 프로젝트를 직접 경험했다고 말한다(Martin, *Clean Architecture*, 2017):

- 제대로 만든 시스템 설계와 아키텍처 덕택에 **쉽게 구현하고 유지보수**할 수 있었던 프로젝트
- **예상보다 적은 인력**만으로 완수한 프로젝트
- **결함률이 극도로 낮은** 시스템
- 훌륭한 소프트웨어 아키텍처가 **시스템, 프로젝트, 팀에 놀라운 효과**를 가져오는 것

### 지옥: 나쁜 아키텍처

하지만 당신의 경험을 한번 보자. 전혀 반대의 상황을 겪지 않았나?

```mermaid
flowchart TB
    subgraph Problems [프로그래밍 지옥]
        P1[강하게 결합된 시스템]
        P2[사소한 변경에 몇 주]
        P3[큰 위험 감수]
        P4[잘못된 코드와 설계]
        P5[팀 사기 저하]
        P6[고객 신뢰 상실]
        P7[관리자 인내심 시험]
    end
    
    P1 --> P2 --> P3
    P4 --> P5 --> P6 --> P7
```

| 증상 | 결과 |
|------|------|
| 서로 강하게 연관되고 복잡하게 결합 | 사소한 변경에도 몇 주 소요 |
| 잘못된 코드와 끔찍한 설계 | 방해받고 진행 불가 |
| 나쁜 시스템 설계 | 팀의 사기 저하 |
| 형편없는 소프트웨어 구조 | 팀, 부서, 회사 실패 |

## 우리의 현실

마틴은 자신을 포함해 대다수의 개발자가 "천국"보다는 "지옥"에 훨씬 가까운 경험을 더 자주 한다고 인정한다(Martin, *Clean Architecture*, 2017). 아래는 그런 "지옥"의 전형적인 모습이다 — 원저자도, 리팩토링을 시도한 사람도, 지금 유지보수하는 사람도 이 코드의 전체 동작을 설명하지 못한다.

```java
// 현실: 레거시 코드와의 싸움
public class LegacyOrderProcessor {
    // 2005년에 작성됨. 아무도 이해 못함.
    // TODO: 리팩토링 필요 (2010년 작성)
    // FIXME: 왜 이게 동작하지? (2015년 작성)
    // WARNING: 절대 수정하지 마시오! (2020년 작성)

    public Receipt process(Order order, Customer customer, Inventory inventory) {
        if (order == null) throw new IllegalArgumentException("order");
        int discountCode = customer.getTier() * 7 % 13;  // 왜 13인지 아무도 모름
        if (discountCode == 4 || discountCode == 9) {
            // 2011년에 추가된 특수 할인 로직, 근거 문서 소실
            if (inventory.hasBackorder(order.getProductId())) {
                discountCode = 0;
            }
        }
        // ... 이런 식의 조건문이 18개 더 이어진다 ...
        return new Receipt(order, discountCode);
    }
}
```

훌륭한 소프트웨어 설계를 바탕으로 작업하면서 **즐거움을 느끼기보다는**, 형편없는 소프트웨어 설계와 **맞서 싸우는 일**을 훨씬 더 자주 맞닥뜨린다.

## 이 파트에서 다룰 내용

```mermaid
flowchart LR
    P1[1부: 소개] --> C1[1장: 설계와 아키텍처란?]
    P1 --> C2[2장: 두 가지 가치]
```

| 장 | 제목 | 핵심 내용 |
|----|------|----------|
| 1장 | 설계와 아키텍처란? | 둘 사이에 차이가 없다 |
| 2장 | 두 가지 가치 | 행위 vs 구조 |

## 핵심 요약

| 항목 | 동작하는 코드 | 제대로 된 소프트웨어 |
|------|--------------|-------------------|
| 난이도 | 쉬움 | 어려움 |
| 필요 역량 | 기본적인 프로그래밍 | 지식, 기술, 통찰력, 헌신 |
| 유지보수 | 악몽 | 쉽고 빠름 |
| 인력 | 많이 필요 | 적게 필요 |
| 결함률 | 높음 | 낮음 |
| 변경 비용 | 시간이 지날수록 증가 | 일정하게 유지 |

마틴은 이 책의 목표를 이렇게 정리한다: 좋은 소프트웨어 아키텍처가 무엇인지, 어떻게 만드는지를 설명하는 것이며, 비용은 최소화하고 생산성은 최대화할 수 있는 설계를 만들기 위해 알아야 할 모든 것을 다룬다(Martin, *Clean Architecture*, 2017).

## 비판적 시각

이 장의 "천국과 지옥" 대비는 극적인 효과를 위해 양 극단을 보여주는 수사적 장치에 가깝다. 실제 프로젝트 대부분은 이 두 극단 사이 어딘가에 있으며, "나쁜 설계=회사 실패"라는 인과관계도 지나친 단순화일 수 있다 — 시장 상황, 팀 역량, 자금 등 다른 요인도 함께 작용한다. 다만 "설계 품질이 나쁠수록 같은 인력으로 낼 수 있는 산출물이 줄어든다"는 방향성 자체는 이후 장들에서 다룰 구체적 근거(SOLID, 컴포넌트 원칙 등)로 뒷받침된다.

## 학습 목표

이 장을 읽은 후 다음을 할 수 있어야 한다.

- "동작하는 코드"와 "제대로 된 소프트웨어"의 차이를 필요 역량 관점에서 설명할 수 있다.
- 나쁜 설계가 왜 팀 규모를 키워도 해결되지 않는지 설명할 수 있다.
- 이 챕터의 "천국과 지옥" 대비가 갖는 수사적 성격과 한계를 인식할 수 있다.

## 판단 기준

이 장의 메시지를 팀에 전달할 때는 "우리 코드는 지옥이다"는 식의 전면 비판보다, 구체적으로 어떤 결합·중복이 변경 비용을 어떻게 늘리고 있는지 수치나 사례로 보여주는 편이 설득력이 높다. 다음 장부터 다룰 SOLID·컴포넌트 원칙은 이런 "좋은/나쁜 설계"라는 추상적 구분을 구체적으로 진단·개선하는 도구를 제공한다.

## 참고 자료

- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.

다음 장에서는 **설계와 아키텍처의 정의**와 그 **목표**에 대해 자세히 알아본다.
