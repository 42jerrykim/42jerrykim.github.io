---
draft: false
collection_order: 11
slug: objects-vs-data-structures-design-patterns
title: "[Clean Code] 11. 객체와 자료구조의 비대칭"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "객체는 동작을 노출하고 자료를 감추며, 자료구조는 자료를 노출하고 동작이 없다는 근본적 비대칭을 설명한다. 디미터 법칙, 기차 충돌 코드, DTO 설계 원칙을 실전 예제와 새 타입·새 연산 추가 트레이드오프 표로 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- OOP(객체지향)
- Encapsulation(캡슐화)
- Abstraction(추상화)
- Design-Pattern(디자인패턴)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Functional-Programming(함수형프로그래밍)
- Coupling(결합도)
- Java
- Python
- Refactoring(리팩토링)
- Implementation(구현)
- Pitfalls(함정)
- Domain-Driven-Design
- Interface(인터페이스)
- Composition(합성)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Testing(테스트)
- Type-Safety
- Software-Architecture(소프트웨어아키텍처)
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [05장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 다룬 함수 설계 원칙을 전제로 하며, 객체지향 프로그래밍에서 클래스와 필드를 선언해 본 최소한의 경험이 필요하다. 이 장은 자료를 다루는 두 가지 방식(객체, 자료구조)의 근본적 차이를 다루며, 클래스 설계 전반(SRP, SOLID)은 [18장](/post/clean-code/clean-classes-solid-principles-oop/)에서 확장한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "자료 추상화"부터 "디미터 법칙"까지 | 객체와 자료구조가 왜 반대되는 설계인지 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | 도메인 모델을 설계할 때 객체와 DTO를 언제 각각 선택할지 판단한다 |

## 자료 추상화: getter/setter는 캡슐화가 아니다

변수를 `private`으로 선언해도, 모든 값에 대해 기계적으로 `get`/`set` 메서드를 제공한다면 사실상 구현을 그대로 외부에 노출한 것과 다르지 않다. 진짜 추상화는 "이 객체가 무슨 데이터를 갖고 있는가"가 아니라 "이 객체로 무엇을 할 수 있는가"를 드러내야 한다.

```java
// 구체적인 클래스: 저장 형식(갤런 단위 double)을 그대로 노출한다
public class Vehicle {
    private double fuelTankCapacityInGallons;
    private double gallonsOfGasoline;

    public double getFuelTankCapacityInGallons() { return fuelTankCapacityInGallons; }
    public double getGallonsOfGasoline() { return gallonsOfGasoline; }
}

// 추상적인 클래스: 저장 형식을 감추고 의미(백분율)만 노출한다
public interface Vehicle {
    double getPercentFuelRemaining();
}
```

두 번째 설계에서는 연료를 리터로 저장하든 갤런으로 저장하든, 심지어 센서에서 실시간으로 읽어오든 호출자는 전혀 알 필요가 없다. 이것이 **자료 추상화**다 — 인터페이스는 "무엇을 할 수 있는가"만 약속하고, "어떻게 저장하는가"는 구현 세부사항으로 감춘다.

## 객체와 자료구조의 근본적 비대칭

<strong>객체(Object)</strong>는 동작을 공개하고 자료를 숨긴다. <strong>자료구조(Data Structure)</strong>는 자료를 공개하고 별다른 동작이 없다. 이 둘은 정확히 반대 방향으로 설계된 것이며, 이 비대칭은 "새로운 기능을 추가할 때 어느 쪽을 고쳐야 하는가"에서 극명하게 드러난다.

```java
// 절차적 코드(자료구조 + 별도 함수): 새 도형 추가는 쉽지만, 새 연산 추가는 모든 클래스를 건드려야 한다
public class Square { public Point topLeft; public double side; }
public class Circle { public Point center; public double radius; }

public class Geometry {
    public double area(Object shape) {
        if (shape instanceof Square) {
            Square s = (Square) shape;
            return s.side * s.side;
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return Math.PI * c.radius * c.radius;
        }
        throw new NoSuchShapeException();
    }
}

// 객체지향 코드(다형성): 새 연산 추가는 모든 클래스를 건드려야 하지만, 새 도형 추가는 클래스 하나만 만들면 된다
public interface Shape { double area(); }
public class Square implements Shape {
    private Point topLeft; private double side;
    public double area() { return side * side; }
}
public class Circle implements Shape {
    private Point center; private double radius;
    public double area() { return Math.PI * radius * radius; }
}
```

두 설계 모두 "완벽한 정답"이 아니라 트레이드오프다. 절차적 코드에서 `perimeter()`라는 새 연산을 추가하려면 `Geometry` 클래스 한 곳만 고치면 되지만, 새 도형 `Triangle`을 추가하려면 `area`, `perimeter` 등 모든 연산 함수를 찾아 분기를 추가해야 한다. 객체지향 코드는 정확히 반대다 — 새 도형 `Triangle`을 추가하려면 `Shape`를 구현하는 클래스 하나만 만들면 되지만, 새 연산 `perimeter()`를 추가하려면 `Square`, `Circle`을 포함한 모든 도형 클래스를 고쳐야 한다.

| 기준 | 절차적 코드 (자료구조) | 객체지향 코드 (다형성) |
|:--|:--|:--|
| 새 자료 타입 추가 | 모든 함수를 수정해야 함 | 클래스 하나만 추가하면 됨 |
| 새 함수(연산) 추가 | 함수 하나만 추가하면 됨 | 모든 클래스를 수정해야 함 |
| 적합한 상황 | 타입은 고정, 연산이 자주 추가됨 | 연산은 고정, 타입이 자주 추가됨 |

## 디미터 법칙과 기차 충돌

<strong>디미터 법칙(Law of Demeter)</strong>은 Ian Holland가 1987년 노스이스턴 대학 디미터 프로젝트에서 제안한 원칙으로, "모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다"고 요약된다. 구체적으로는 클래스 `C`의 메서드 `f`가 호출할 수 있는 대상을 `C` 자신, `f`의 인수, `f`가 생성한 객체, `C`의 인스턴스 변수로 제한한다 — 이 객체들이 반환한 객체의 메서드는 호출하지 않아야 한다.

```java
// 디미터 법칙 위반: 여러 객체를 줄줄이 파고들어 감(기차 충돌)
String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();

// 개선: 필요한 동작을 직접 요청하고, 중간 구조는 감춘다
String outputDir = ctxt.getScratchDirAbsolutePath();
```

첫 번째 코드는 흔히 <strong>기차 충돌(Train Wreck)</strong>이라 불린다. 호출자는 `ctxt`가 `Options`를 갖고, `Options`가 `ScratchDir`을 갖고, `ScratchDir`이 `AbsolutePath`를 가진다는 내부 구조를 전부 알아야 한다. 이는 `ctxt` 내부 구조가 바뀔 때마다 이 코드도 함께 깨진다는 뜻이며, 정확히 "동작을 노출하고 자료를 숨긴다"는 객체의 원칙을 위반한 것이다. 다만 디미터 법칙은 **객체**에 적용되는 원칙이며, 자료구조(순수한 필드 묶음)에는 적용되지 않는다 — 자료구조는 애초에 자료를 노출하는 것이 설계 의도이기 때문이다.

## 잡종 구조와 DTO

가장 다루기 어려운 설계는 절반은 객체, 절반은 자료구조인 <strong>잡종 구조(Hybrid)</strong>다. 중요한 함수도 있고, 공개 변수나 공개 getter/setter도 있는 클래스는 새 함수 추가와 새 자료 타입 추가 양쪽 모두 어렵게 만든다. 이런 구조는 대개 설계자가 두 접근 중 하나를 결정하지 못한 결과다.

반대로 자료를 전달하는 목적만 갖는 <strong>DTO(Data Transfer Object)</strong>는 순수한 자료구조로 설계하는 것이 맞다. DTO는 데이터베이스와 통신하거나, 소켓에서 받은 메시지의 첫 파싱 단계를 처리하는 등 자료를 옮기는 역할에 충실하며, 여기에 비즈니스 로직을 섞으면 안 된다.

```java
// DTO: 순수한 자료 전달 목적, 동작이 없다
public class OrderDto {
    public final String orderId;
    public final String customerId;
    public final BigDecimal amount;

    public OrderDto(String orderId, String customerId, BigDecimal amount) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.amount = amount;
    }
}
```

## 흔한 오개념

<strong>"getter/setter를 모두 만들면 캡슐화된 것이다"</strong>는 오해가 가장 흔하다. 실제로는 모든 필드에 기계적으로 getter/setter를 붙이는 것은 캡슐화를 흉내 낼 뿐, 구현을 그대로 노출한다는 점에서 `public` 필드와 본질적으로 다르지 않다. 진짜 캡슐화는 "이 객체가 무엇을 할 수 있는가"라는 동작을 노출하고, "어떻게 저장하는가"라는 구현은 감추는 것이다.

<strong>"객체지향이 항상 절차적 코드보다 우월하다"</strong>는 오해도 있다. 앞서 표에서 보였듯, 새로운 자료 타입이 자주 추가되고 연산 종류는 고정된 시스템(예: 다양한 파일 포맷을 지원하는 파서)은 다형성이 유리하지만, 연산 종류가 자주 늘어나고 자료 타입은 고정된 시스템(예: 고정된 도형 집합에 새로운 기하 연산을 계속 추가하는 CAD 도구)은 오히려 자료구조 + 함수 방식이 변경 비용을 줄인다.

## 판단 기준: 객체 vs 자료구조, 언제 무엇을 쓸까

새로운 "종류"가 자주 추가될 것으로 예상되면 다형성을 갖는 객체로 설계한다(새 도형, 새 결제 수단, 새 알림 채널). 새로운 "연산"이 자주 추가될 것으로 예상되면 자료구조와 별도 함수로 설계한다(고정된 데이터 모델에 계속 새로운 리포트·분석 로직이 붙는 경우). 데이터베이스 레코드, API 응답/요청, 메시지 큐 페이로드처럼 순수하게 자료를 옮기는 역할이라면 DTO로 설계하고 비즈니스 로직을 섞지 않는다.

## 비판적 시각

Clean Code가 제시하는 이 이분법은 객체지향 언어를 전제로 하지만, 함수형 프로그래밍 진영에서는 애초에 "자료구조 + 순수 함수"를 기본 설계 방식으로 삼는다. 이 관점에서는 잡종 구조를 피하기 위해 다형성 객체로 밀어붙이는 대신, 데이터는 불변 자료구조로 유지하고 연산은 별도의 순수 함수 집합으로 관리하는 편이 테스트하기 쉽고 병렬화하기도 쉽다고 본다. Martin Fowler가 지적한 **빈혈 도메인 모델(Anemic Domain Model)** 안티패턴 논의도 이와 맞닿아 있다 — 도메인 객체에 로직이 전혀 없이 getter/setter만 있고 모든 로직이 별도 서비스 계층에 있는 구조는, DDD 관점에서는 안티패턴으로 비판받지만, 자료-함수 분리를 선호하는 관점에서는 오히려 자연스러운 결과로 받아들여진다. 결국 이 선택은 팀이 어떤 패러다임을 중심에 둘지에 대한 설계 철학의 문제이지, 절대적으로 옳은 답이 있는 문제가 아니다.

## 다음 장에서는

[12장: 디미터 법칙 리팩토링 실습](/post/clean-code/objects-vs-data-structures-exercises/)에서는 기차 충돌 코드를 실제로 리팩토링해 본다.

## 평가 기준

- [ ] 객체와 자료구조가 "새 타입 추가"와 "새 연산 추가"에 대해 정반대의 트레이드오프를 갖는 이유를 설명할 수 있다.
- [ ] 기차 충돌 코드를 식별하고 디미터 법칙에 따라 리팩토링할 수 있다.
- [ ] getter/setter를 모두 제공하는 것이 왜 진짜 캡슐화가 아닌지 논증할 수 있다.
- [ ] 특정 상황에서 다형성 객체와 자료구조+함수 중 어느 쪽이 유리한지 판단할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 6장.
- Lieberherr, K., & Holland, I. (1989). "Assuring Good Style for Object-Oriented Programs." *IEEE Software*, 6(5), 38–48.
- Fowler, M. *AnemicDomainModel*. [https://martinfowler.com/bliki/AnemicDomainModel.html](https://martinfowler.com/bliki/AnemicDomainModel.html)
