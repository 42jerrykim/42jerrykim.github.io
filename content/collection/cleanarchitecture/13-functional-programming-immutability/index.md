---
draft: true
collection_order: 130
image: "wordcloud.png"
description: "함수형 프로그래밍의 핵심인 불변성(Immutability)을 아키텍처 관점에서 분석합니다. 람다 계산법부터 이벤트 소싱까지, 가변 상태가 없는 프로그래밍이 동시성 문제를 해결하는 원리를 가변성 분리 전략과 함께 설명합니다."
title: "[Clean Architecture] 13. 함수형 프로그래밍"
slug: functional-programming-immutability
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Functional-Programming(함수형프로그래밍)
  - Code-Quality(코드품질)
  - State
  - Concurrency(동시성)
  - CQRS(Command Query Responsibility Segregation)
  - Scala
  - Software-Architecture(소프트웨어아키텍처)
  - History(역사)
  - Async(비동기)
  - Event-Driven
  - Testing(테스트)
  - Best-Practices
  - Maintainability
  - Case-Study
  - Deep-Dive
  - Technology(기술)
  - Design-Pattern(디자인패턴)
  - Domain-Driven-Design
  - Recursion(재귀)
  - Math(수학)
  - Thread
  - Mutex
  - Synchronization
  - Refactoring(리팩토링)
  - Abstraction(추상화)
  - Database(데이터베이스)
---

함수형 프로그래밍(FP)은 세 가지 패러다임 중 가장 오래되었지만, 가장 최근에 주목받기 시작했다. 1936년 알론조 처치(Alonzo Church)의 람다 계산법에서 시작된 이 패러다임은, **불변성(Immutability)**이라는 개념을 통해 현대 소프트웨어 아키텍처에 중요한 통찰을 제공한다.

## 람다 계산법과 함수형 프로그래밍의 기원

### 튜링 이전의 계산 이론

1936년, 앨런 튜링(Alan Turing)이 튜링 기계를 발표하기 전, 알론조 처치는 **람다 계산법(Lambda Calculus)**을 발명했다. 람다 계산법은 계산 가능성을 연구하기 위한 수학적 시스템이었다.

```text
// 람다 계산법의 기본 형태
λx.x        // 항등 함수
λx.λy.x     // 첫 번째 인자를 반환
λf.λx.f(x)  // 함수를 한 번 적용
```

### LISP의 탄생

1958년, 존 매카시(John McCarthy)는 람다 계산법에 기반한 최초의 함수형 프로그래밍 언어 **LISP**를 개발했다.

```lisp
; LISP 코드 예시
(defun square (x) (* x x))
(defun sum-of-squares (x y) 
  (+ (square x) (square y)))
```

LISP는 현대까지 살아남아 Clojure, Racket 등의 형태로 사용되고 있다.

## 불변성: 함수형 프로그래밍의 핵심

### 함수형 언어에는 할당문이 없다

가장 엄격한 함수형 언어에서, **변수는 한 번 초기화되면 변경되지 않는다**.

```haskell
-- Haskell: 불변 변수
x = 5
-- x = 6  -- 오류! 재할당 불가
```

```java
// 명령형 프로그래밍: 가변 변수
int x = 5;
x = 6;  // OK: 재할당 가능
```

### 순수 함수 (Pure Function)

순수 함수는:
1. 같은 입력에 항상 같은 출력
2. 부수 효과(Side Effect)가 없음

```java
// 순수 함수
int add(int a, int b) {
    return a + b;  // 외부 상태 변경 없음
}

// 비순수 함수
int counter = 0;
int increment() {
    counter++;  // 외부 상태 변경 (부수 효과)
    return counter;
}
```

### 참조 투명성 (Referential Transparency)

순수 함수는 **참조 투명**하다. 함수 호출을 그 결과값으로 대체해도 프로그램의 의미가 변하지 않는다.

```java
// 참조 투명: add(2, 3) 호출을 그 결과값 5로 바꿔도 프로그램 의미가 같다
int result1 = add(2, 3);  // 5
int result2 = 5;          // result1과 동일한 의미

// 참조 불투명: increment() 호출을 1로 바꾸면 의미가 달라진다
int result3 = increment();  // 1
int result4 = 1;            // result3과 동일하지 않음! (다음 호출은 2를 반환)
```

## 불변성이 해결하는 문제: 동시성

### 가변 상태의 저주

현대 소프트웨어의 가장 큰 문제 중 하나는 **동시성(Concurrency)**이다. 여러 스레드가 동시에 가변 상태에 접근하면:

```java
// 동시성 문제 예시
class Counter {
    private int count = 0;
    
    void increment() {
        count++;  // 위험! 원자적 연산이 아님
    }
}
```

`count++`는 실제로 세 단계로 이루어진다:
1. count 읽기
2. 1 더하기
3. count 쓰기

두 스레드가 동시에 실행하면:

```mermaid
sequenceDiagram
    participant T1 as Thread 1
    participant M as count
    participant T2 as Thread 2
    
    Note over M: count = 0
    T1->>M: 읽기 (0)
    T2->>M: 읽기 (0)
    T1->>M: 쓰기 (1)
    T2->>M: 쓰기 (1)
    Note over M: count = 1 (기대값: 2)
```

이것이 **경쟁 조건(Race Condition)**이다.

### 전통적인 해결책: 락(Lock)

```java
class Counter {
    private int count = 0;
    private Object lock = new Object();
    
    void increment() {
        synchronized(lock) {  // 락 획득
            count++;
        }  // 락 해제
    }
}
```

그러나 락은 문제를 해결하는 대신 다른 문제로 바꿔치기한다는 근본적 한계가 있다. 락을 여러 개 잘못된 순서로 획득하면 서로 상대의 락을 기다리며 영원히 멈추고, 락 경합이 심해지면 스레드들이 대기 상태에 머무는 시간이 늘어나며, 락의 범위와 순서를 관리하는 코드 자체가 버그의 원천이 된다.

- **데드락(Deadlock)** 위험
- **성능 저하**
- **복잡성 증가**

### 함수형 해결책: 불변성

**가변 상태가 없으면, 경쟁 조건도 없다.**

```java
// 불변 클래스
final class Counter {
    private final int count;
    
    public Counter(int count) {
        this.count = count;
    }
    
    public Counter increment() {
        return new Counter(count + 1);  // 새 객체 반환
    }
    
    public int getCount() {
        return count;
    }
}
```

위 `Counter`는 `count` 필드가 `final`이라 생성된 이후 절대 바뀌지 않는다. `increment()`는 기존 객체를 수정하는 대신 새 `Counter` 객체를 만들어 반환하므로, 여러 스레드가 동시에 `increment()`를 호출해도:
- 원본 객체는 변경되지 않음
- 각 스레드는 새 객체를 받음
- 락이 필요 없음

## 아키텍처에서의 불변성

### 완전한 불변성은 가능한가?

현실적으로, 모든 상태를 불변으로 만들기는 어렵다. 프로그램은 결국:
- 파일을 쓰고
- 데이터베이스를 업데이트하고
- 네트워크로 데이터를 전송한다

### 가변성의 분리 (Segregation of Mutability)

마틴은 **가변 컴포넌트와 불변 컴포넌트를 분리**할 것을 제안한다.

```mermaid
flowchart TB
    subgraph Immutable [불변 컴포넌트]
        P[순수 함수들]
        D[불변 데이터 구조]
    end
    
    subgraph Mutable [가변 컴포넌트]
        DB[(데이터베이스)]
        S[상태 관리]
    end
    
    Immutable --> Mutable
    
    style Immutable fill:#9f9
    style Mutable fill:#f96
```

- **불변 컴포넌트**: 가능한 많이, 순수 함수로 구성
- **가변 컴포넌트**: 최소화, 격리

### 트랜잭션 메모리와 동시성

가변 컴포넌트를 완전히 없앨 수는 없지만, 최소화한 뒤 그 좁은 영역에만 동시성 제어 기법을 집중시키면 관리 범위가 크게 줄어든다. 가변 상태가 필요한 곳에서는:
- **트랜잭션 메모리** 사용
- **적절한 락** 사용
- **원자적 연산** 사용

Clojure의 예:

```clojure
; Clojure의 원자적 상태 관리
(def counter (atom 0))
(swap! counter inc)  ; 원자적 증가
```

## 이벤트 소싱 (Event Sourcing)

### 상태 대신 이벤트 저장

전통적인 방식:
- 현재 상태만 저장
- 이전 상태는 사라짐

이벤트 소싱:
- 모든 변경을 이벤트로 저장
- 현재 상태는 이벤트들의 결과

```java
// 전통적인 방식
class Account {
    private BigDecimal balance;
    
    void deposit(BigDecimal amount) {
        balance = balance.add(amount);  // 상태 변경
    }
}

// 이벤트 소싱
class AccountEventStore {
    private List<Event> events = new ArrayList<>();
    
    void deposit(BigDecimal amount) {
        events.add(new DepositEvent(amount));  // 이벤트 추가
    }
    
    BigDecimal getBalance() {
        return events.stream()
            .reduce(BigDecimal.ZERO, this::applyEvent);  // 이벤트 재생
    }
}
```

### 이벤트 소싱의 장점

```mermaid
flowchart LR
    subgraph Events [이벤트 로그]
        E1[입금 100]
        E2[출금 30]
        E3[입금 50]
        E4[출금 20]
    end
    
    subgraph States [상태 재구성]
        S1["시점1: 100"]
        S2["시점2: 70"]
        S3["시점3: 120"]
        S4["현재: 100"]
    end
    
    E1 --> S1
    E2 --> S2
    E3 --> S3
    E4 --> S4
```

1. **완전한 이력**: 모든 변경 기록 보존
2. **시점 복원**: 어떤 시점의 상태든 재구성 가능
3. **감사 추적**: 누가, 언제, 무엇을 했는지 추적
4. **디버깅**: 버그 재현이 쉬움

### 저장 공간은?

"모든 이벤트를 저장하면 공간이 부족하지 않나?"

마틴의 답은 이렇다: 저장 공간은 빠르게 저렴해지고 있으니, 더 이상 1960년대처럼 공간을 아껴야 하는 시대가 아니라는 것이다(Martin, *Clean Architecture*, 2017). 그럼에도 이벤트 양이 정말 부담이 된다면 다음 완화책을 쓸 수 있다:
- 일정 시점까지의 **스냅샷** 저장
- 오래된 이벤트 **아카이브**
- **CQRS 패턴**으로 읽기/쓰기 분리

## 세 패러다임의 교훈

```mermaid
flowchart TB
    subgraph Paradigms [세 패러다임]
        SP["구조적 프로그래밍</br>goto 제거"]
        OOP["객체 지향</br>함수 포인터 제어"]
        FP["함수형</br>할당 제한"]
    end
    
    subgraph Lessons [교훈]
        L1[제어 흐름의 직접 전환 규제]
        L2[제어 흐름의 간접 전환 규제]
        L3[할당의 규제]
    end
    
    SP --> L1
    OOP --> L2
    FP --> L3
```

| 패러다임 | 제거하는 것 | 얻는 것 |
|----------|-----------|--------|
| 구조적 | goto | 증명/테스트 가능성 |
| 객체 지향 | 함수 포인터 남용 | 의존성 제어 |
| 함수형 | 할당 | 동시성 안전 |

마틴은 이렇게 요약한다: 세 패러다임 모두 우리에게서 무언가를 빼앗는다. 권한을 부여하지 않는다(Martin, *Clean Architecture*, 2017).

## 아키텍처에 주는 교훈

### 1. 불변성을 최대화하라

```java
// 가능한 한 불변으로
public final class Order {
    private final OrderId id;
    private final List<OrderLine> lines;  // 불변 리스트
    
    public Order addLine(OrderLine line) {
        List<OrderLine> newLines = new ArrayList<>(lines);
        newLines.add(line);
        return new Order(id, Collections.unmodifiableList(newLines));
    }
}
```

### 2. 가변성을 격리하라

```mermaid
flowchart TB
    subgraph Pure [순수 영역]
        direction TB
        BL[비즈니스 로직]
        V[검증]
        C[계산]
    end
    
    subgraph Impure [불순 영역]
        direction TB
        DB[(데이터베이스)]
        API[외부 API]
        UI[UI]
    end
    
    Pure --> Impure
```

### 3. 이벤트 소싱을 고려하라

이벤트 소싱은 만능 해법이 아니라 특정 상황에 강한 도구다:

- 모든 시스템에 필요하진 않음
- 감사 추적이 중요한 도메인에 유용
- 이력과 복원이 필요한 경우 강력

## 핵심 요약

마틴은 이렇게 요약한다: 함수형 프로그래밍은 할당문에 대해 규칙을 부과한다(Martin, *Clean Architecture*, 2017).

| 항목 | 내용 |
|------|------|
| 핵심 개념 | 불변성 (Immutability) |
| 제거하는 것 | 할당문 |
| 해결하는 문제 | 동시성, 경쟁 조건 |
| 아키텍처 적용 | 가변성 분리, 이벤트 소싱 |

## 흔한 오해

**"함수형 프로그래밍은 상태를 아예 다룰 수 없다"**는 흔한 오해다. 실제로는 상태를 아예 없애는 것이 아니라, 상태 변경을 새 값 생성으로 대체하고 그 범위를 격리하는 것이다. 위 `Counter` 예제처럼 "상태가 바뀐 것처럼 보이는" 코드도, 실제로는 매번 새 불변 객체를 만들어 반환할 뿐이다. 또한 **"함수형 언어를 써야만 이 원칙을 적용할 수 있다"**는 것도 오해다 — Java, Python 등 명령형 언어에서도 `final`/불변 클래스 설계로 이 장의 원칙 대부분을 적용할 수 있다.

## 학습 목표

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 순수 함수·참조 투명성이 무엇인지, 그리고 이것이 동시성 문제를 어떻게 근본적으로 제거하는지 설명할 수 있다.
- "가변성의 분리" 전략을 자신의 코드베이스에 어떻게 적용할지 설명할 수 있다.
- 이벤트 소싱이 적합한 상황과 부적합한 상황을 구분할 수 있다.

## 참고 자료

- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
- McCarthy, J. (1960). "Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I". *Communications of the ACM*, 3(4).

다음 파트에서는 이러한 패러다임 위에 구축되는 **설계 원칙(SOLID)**을 다룬다.
