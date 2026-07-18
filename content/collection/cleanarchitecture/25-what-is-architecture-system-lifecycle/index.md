---
draft: true
collection_order: 250
image: "wordcloud.png"
description: "아키텍처의 정의와 시스템 생명주기 전반에 걸친 목표를 다룹니다. 개발, 배포, 운영, 유지보수를 지원하는 좋은 아키텍처의 특성, 결정 지연의 가치, 정책과 세부사항의 분리를 예제와 함께 설명합니다."
title: "[Clean Architecture] 25. 아키텍처란?"
slug: what-is-architecture-system-lifecycle
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Software-Architecture(소프트웨어아키텍처)
  - Implementation(구현)
  - Deployment(배포)
  - Code-Quality(코드품질)
  - Security(보안)
  - Database(데이터베이스)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Scalability(확장성)
  - Performance(성능)
  - Coupling(결합도)
  - Modularity
  - System-Design
  - Best-Practices
  - Maintainability
  - History(역사)
  - Case-Study
  - Technology(기술)
  - Interface(인터페이스)
  - Abstraction(추상화)
  - Domain(도메인)
  - Backend(백엔드)
  - Microservices(마이크로서비스)
  - Web(웹)
  - Testing(테스트)
  - Reliability
  - DevOps
---

소프트웨어 아키텍처란 무엇인가? 마틴은 아키텍처를 시스템의 **형태를 결정**하고, 시스템의 **생명주기를 지원**하는 것으로 정의한다.

## 아키텍처의 정의

> **"시스템 아키텍처란 시스템을 구축한 사람들이 그 시스템에 부여한 형태다."**
> — Robert C. Martin

아키텍처는 시스템을:
- **컴포넌트로 분할**
- **컴포넌트를 배치**
- **컴포넌트 간 통신 정의**

```mermaid
flowchart TB
    subgraph Architecture [아키텍처의 역할]
        DIVIDE[시스템을 컴포넌트로 분할]
        ARRANGE[컴포넌트 배치]
        COMM[통신 방식 정의]
    end
    
    DIVIDE --> ARRANGE --> COMM
```

### 아키텍처의 궁극적 목표

> "아키텍처의 궁극적 목표는 시스템의 생명주기 동안 필요한 **인력을 최소화**하는 것이다."

## 아키텍트는 프로그래머다

마틴은 아키텍트의 역할에 대해 강조한다:

```mermaid
flowchart LR
    subgraph Architect [아키텍트의 역할]
        PROG[프로그래밍 계속]
        GUIDE[팀 가이드]
        DESIGN[설계 결정]
        PROD[생산성 극대화]
    end
    
    PROG --> GUIDE
    GUIDE --> DESIGN
    DESIGN --> PROD
```

> "소프트웨어 아키텍트는 **최고의 프로그래머**이며, 계속 프로그래밍 작업을 맡을 뿐 아니라 동시에 나머지 팀원들이 생산성을 극대화할 수 있는 설계를 하도록 방향을 이끌어야 한다."

### 아키텍트가 프로그래밍을 멈추면?

| 문제점 | 결과 |
|--------|------|
| 팀이 겪는 문제를 모름 | 현실과 동떨어진 설계 |
| 실제 코드를 작성하지 않음 | 팀의 신뢰 상실 |
| 생산성 향상 방법 모름 | 비효율적인 아키텍처 |

## 아키텍처의 네 가지 목표

좋은 아키텍처는 시스템 생명주기의 **네 가지 측면**을 지원한다.

```mermaid
flowchart TB
    ARCH[좋은 아키텍처]
    
    DEV[1. 개발 용이성]
    DEPLOY[2. 배포 용이성]
    OPS[3. 운영 용이성]
    MAINT[4. 유지보수 용이성]
    
    ARCH --> DEV
    ARCH --> DEPLOY
    ARCH --> OPS
    ARCH --> MAINT
```

### 1. 개발 (Development)

팀이 시스템을 **쉽게 개발**할 수 있어야 한다.

```java
// 좋은 아키텍처: 팀이 독립적으로 작업 가능
// 주문 팀
package com.example.order;
public class OrderService { }

// 결제 팀
package com.example.payment;
public class PaymentService { }

// 배송 팀
package com.example.shipping;
public class ShippingService { }
```

| 팀 규모 | 적합한 구조 | 이유 |
|--------|------------|------|
| 5인 이하 | 모놀리식도 가능 | 커뮤니케이션 오버헤드 적음 |
| 대규모 | 컴포넌트 분리 필수 | 팀 간 충돌 방지 |
| 여러 팀 | 독립 개발 가능해야 함 | 병렬 작업 가능 |

### 2. 배포 (Deployment)

> "좋은 아키텍처는 시스템을 **단일 액션**으로 쉽게 배포할 수 있게 한다."

**나쁜 배포 경험:**

```mermaid
flowchart LR
    subgraph BadDeploy [나쁜 배포]
        S1[서비스 1]
        S2[서비스 2]
        S3[서비스 3]
        CONFIG[복잡한 설정]
        ORDER[배포 순서 의존성]
    end
    
    S1 --> CONFIG
    S2 --> CONFIG
    S3 --> ORDER
```

- 수십 개의 작은 서비스를 각각 배포
- 복잡한 연결 설정
- 배포마다 문제 발생
- 수동 개입 필요

**좋은 배포 경험:**

```bash
# 이상적인 배포
$ git push origin main
# 자동으로 빌드, 테스트, 배포 완료
```

### 3. 운영 (Operation)

아키텍처는 시스템의 **운영 요구사항을 드러내야** 한다.

```mermaid
flowchart TB
    subgraph Operation [운영 관점의 아키텍처]
        VISIBLE[유스케이스가 명확히 보임]
        SCALE[확장/축소 용이]
        MONITOR[모니터링 가능]
        PERF[성능 요구사항 충족]
    end
```

좋은 아키텍처의 운영 특성:
- 시스템이 **무엇을 하는지 명확**
- 유스케이스가 **구조에 반영**됨
- **확장과 축소**가 용이
- 처리량과 응답 시간 요구사항 충족

운영 요구사항에는 성능·확장성뿐 아니라 신뢰성(장애 시 얼마나 빨리 복구되는가), 보안(인증·권한 경계가 구조에 드러나는가), 모니터링(장애를 얼마나 빨리 감지하는가)도 포함된다. 이런 비기능 요구사항을 아키텍처 설계 시점에 무시하고 나중에 덧붙이려 하면, 이미 굳어진 모듈 경계와 충돌해 코드 품질을 해치는 임시방편으로 끝나는 경우가 많다. DevOps 문화가 확산되면서 배포 자동화(CI/CD 파이프라인)와 운영 모니터링을 아키텍처 설계 단계부터 함께 고려하는 것이 모범 사례로 자리 잡았다.

### 4. 유지보수 (Maintenance)

유지보수는 소프트웨어 비용의 **대부분**을 차지한다.

```mermaid
pie title 소프트웨어 비용 분포
    "초기 개발" : 20
    "유지보수" : 80
```

| 유지보수 활동 | 좋은 아키텍처의 효과 |
|--------------|---------------------|
| 새 기능 추가 | 영향 범위 최소화 |
| 버그 수정 | 문제 위치 파악 용이 |
| 요구사항 변경 | 변경 비용 일정 |

> "유지보수의 가장 큰 비용은 **탐사(spelunking)**와 **위험 감수**에서 발생한다."

```java
// 탐사: 어디를 고쳐야 하는지 찾기
// 나쁜 아키텍처
class GodClass {
    // 10,000줄의 코드
    // 어디를 수정해야 할까?
}

// 좋은 아키텍처
class OrderProcessor { /* 주문 처리만 */ }
class PaymentProcessor { /* 결제 처리만 */ }
class ShippingProcessor { /* 배송 처리만 */ }
// 주문 관련 버그? OrderProcessor만 보면 됨
```

## 선택지를 열어두기 (결정 지연)

> **"좋은 아키텍처는 결정을 지연시킬 수 있게 해준다."**

### 왜 결정을 늦춰야 하는가?

```mermaid
flowchart LR
    EARLY[조기 결정] -->|적은 정보| RISK[위험]
    LATE[후기 결정] -->|많은 정보| BETTER[더 나은 선택]
```

늦게 결정할수록:
- 더 많은 **정보**를 바탕으로 결정
- 더 나은 **선택** 가능
- 불필요한 **제약** 방지

### 어떤 결정을 지연할 수 있는가?

| 결정 유형 | 예시 | 지연 가능? |
|----------|------|----------|
| 비즈니스 규칙 | 주문 처리 로직 | ❌ 먼저 결정 |
| 데이터베이스 | MySQL vs PostgreSQL | ✅ 지연 가능 |
| 웹 프레임워크 | Spring vs Django | ✅ 지연 가능 |
| UI 기술 | Web vs Mobile | ✅ 지연 가능 |
| 메시징 시스템 | Kafka vs RabbitMQ | ✅ 지연 가능 |

## 정책과 세부사항

마틴은 시스템을 **정책(Policy)**과 **세부사항(Details)**으로 구분한다.

```mermaid
flowchart TB
    subgraph Policy [정책 - 핵심]
        BR[비즈니스 규칙]
        UC[유스케이스]
        ENTITY[엔터티]
    end
    
    subgraph Details [세부사항 - 교체 가능]
        DB[(데이터베이스)]
        UI[사용자 인터페이스]
        FW[프레임워크]
        EXT[외부 시스템]
    end
    
    Details -->|의존| Policy
```

| 구분 | 정책 | 세부사항 |
|------|------|----------|
| 정의 | 비즈니스 규칙 | 기술적 구현 |
| 변경 빈도 | 낮음 | 높음 |
| 의존성 방향 | 없음 (핵심) | 정책에 의존 |
| 예시 | 주문 처리 규칙 | MySQL, React |
| 교체 가능성 | 어려움 | 쉬움 |

### 정책과 세부사항의 분리

좋은 아키텍처는 **정책이 세부사항에 의존하지 않게** 만든다.

```java
// 좋은 설계: 정책이 세부사항을 모름
public class OrderProcessor {
    private final OrderRepository repository; // 인터페이스
    
    public void processOrder(Order order) {
        // 비즈니스 규칙만 알고 있음
        // DB가 MySQL인지 MongoDB인지 모름
        repository.save(order);
    }
}

// 세부사항: 정책에 의존
public class MySqlOrderRepository implements OrderRepository {
    public void save(Order order) { /* MySQL 구현 */ }
}

public class MongoOrderRepository implements OrderRepository {
    public void save(Order order) { /* MongoDB 구현 */ }
}
```

## 장치 독립성

마틴은 1960년대의 경험을 공유한다. 당시 코드를 특정 장치(카드 리더, 테이프)에 직접 의존하도록 작성했다.

```mermaid
flowchart LR
    subgraph Bad1960s [1960년대 - 나쁜 예]
        CODE1[코드] --> CARD[카드 리더]
    end
    
    subgraph Good1960s [개선된 구조]
        CODE2[코드] --> IO[I/O 추상화]
        IO --> CARD2[카드 리더]
        IO --> TAPE[테이프]
        IO --> FILE[파일]
    end
```

**교훈**: 세부사항으로부터 정책을 분리하면 **장치 독립성**을 얻는다.

## 흔한 오해

"좋은 아키텍처"를 특정 기술 선택(마이크로서비스, 특정 프레임워크 등)과 동일시하는 오해가 흔하다. 그러나 이 장이 강조하듯 아키텍처의 본질은 정책과 세부사항을 분리해 결정을 지연시키는 능력이지, 특정 기술 스택이 아니다. 마이크로서비스로 시스템을 나눠도 비즈니스 규칙이 특정 데이터베이스나 메시징 기술에 강하게 결합돼 있다면 좋은 아키텍처가 아니다. 또 다른 오해는 "결정을 지연한다"를 "결정하지 않는다"로 착각하는 것이다. 비즈니스 규칙처럼 지연할 수 없는 결정도 있다(앞서 본 "어떤 결정을 지연할 수 있는가" 표 참고) — 결정 지연은 아직 확신이 없는 세부사항에 대해서만 적용되는 전략이지, 모든 결정을 미루라는 뜻이 아니다.

## 학습 목표

이 장을 읽은 후 다음을 스스로 점검한다.

- 아키텍처의 정의("시스템에 부여한 형태")와 궁극적 목표("생명주기 동안 필요한 인력 최소화")를 자신의 말로 설명할 수 있는가?
- 아키텍트가 프로그래밍을 계속해야 하는 이유를 팀 신뢰·현실 감각의 관점에서 설명할 수 있는가?
- 개발·배포·운영·유지보수 네 가지 목표가 서로 상충할 수 있는 상황을 예로 들 수 있는가?
- 어떤 결정은 지연할 수 있고 어떤 결정은 지연할 수 없는지, 그 기준을 설명할 수 있는가?
- 정책과 세부사항을 구분하는 기준(변경 빈도·의존성 방향)을 코드 예제로 설명할 수 있는가?

## 판단 기준

설계 결정을 내릴 때 다음을 확인한다.

- 이 결정이 비즈니스 규칙(정책)에 관한 것인가, 아니면 그 규칙을 구현하는 기술(세부사항)에 관한 것인가?
- 세부사항이라면, 지금 당장 확정해야 할 이유가 있는가, 아니면 인터페이스 뒤로 미뤄도 되는가?
- 이 아키텍처는 팀 규모(5인 이하 vs 대규모 다중 팀)에 맞는 구조인가?
- 배포가 단일 액션으로 가능한가, 아니면 여러 컴포넌트를 수동으로 순서에 맞춰 배포해야 하는가?

## 참고 자료

- Robert C. Martin, 『Clean Architecture』, 2017, 15장 — 아키텍처 정의·목표·정책과 세부사항 분리의 원 출처.

## 핵심 요약

| 항목 | 내용 |
|------|------|
| 아키텍처의 정의 | 시스템의 형태를 결정하는 것 |
| 궁극적 목표 | 인력 최소화 |
| 네 가지 목표 | 개발, 배포, 운영, 유지보수 용이성 |
| 핵심 전략 | 결정 지연, 선택지 열어두기 |
| 분리 원칙 | 정책(핵심)과 세부사항(교체 가능) |

마틴은 아키텍처의 목적이 시스템의 생명주기를 지원하는 것이라고 말한다. 좋은 아키텍처는 시스템을 쉽게 이해하고, 쉽게 개발하고, 쉽게 유지보수하고, 쉽게 배포하게 해준다(Martin, 『Clean Architecture』, 2017, 15장).
