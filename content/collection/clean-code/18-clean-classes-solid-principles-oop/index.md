---
draft: false
collection_order: 18
slug: clean-classes-solid-principles-oop
title: "[Clean Code] 18. 클래스는 작아야 한다"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "클래스 크기를 책임의 개수로 측정하는 이유를 설명하고, 단일 책임 원칙과 응집도를 중심으로 SOLID 5원칙 전체를 개괄한다. God Class를 작은 클래스들로 분해하는 실전 예제와 과잉 설계 판단 기준을 포함한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- SOLID
- OOP(객체지향)
- Design-Pattern(디자인패턴)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Coupling(결합도)
- Cohesion(응집도)
- Encapsulation(캡슐화)
- Dependency-Injection(의존성주입)
- Java
- Refactoring(리팩토링)
- Implementation(구현)
- Pitfalls(함정)
- Interface(인터페이스)
- Testing(테스트)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Software-Architecture(소프트웨어아키텍처)
- Abstraction(추상화)
- Polymorphism(다형성)
---

## 이 장을 읽기 전에

이 장은 [05장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 함수 단위로 다룬 "한 가지 일만 하라"는 원칙을 클래스 단위로 확장한다. 클래스와 인터페이스를 선언해 본 경험이 필요하다. 이 장은 SOLID 중 SRP·OCP·DIP를 중심으로 다루며, 시스템 전체의 의존성 조립은 [20장](/post/clean-code/system-design-dependency-injection-architecture/)에서 확장한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "클래스 크기의 척도"부터 "응집도"까지 | 클래스가 커지는 원인(여러 책임 혼재)을 식별한다 |
| 실무자 | "판단 기준", "비판적 시각" | SOLID를 얼마나 엄격히 적용할지, 과잉 설계와의 경계를 판단한다 |

## 클래스 크기의 척도: 줄 수가 아니라 책임의 개수

함수의 크기는 물리적인 줄 수로 가늠할 수 있지만, 클래스의 크기는 다른 척도가 필요하다. 클래스가 맡은 **책임(responsibility)**의 개수, 즉 "이 클래스가 변경돼야 하는 이유가 몇 가지인가"로 크기를 측정한다. 70개가 넘는 공개 메서드를 가진 클래스라도 실제로는 서로 무관한 대여섯 가지 책임(버전 관리, 이벤트 알림, 속성 변경 알림)이 한 클래스에 뭉쳐 있을 뿐이며, 각 책임을 별도 클래스로 분리하면 원래 클래스는 자연스럽게 작아진다.

## 단일 책임 원칙(SRP)

**단일 책임 원칙(Single Responsibility Principle, SRP)**은 "클래스나 모듈을 변경할 이유는 하나, 단 하나뿐이어야 한다"는 원칙이다. 이 원칙에서 "책임"은 기능의 개수가 아니라 **변경의 이유**를 뜻한다는 점이 중요하다.

```java
// SRP 위반: 직원 정보, 급여 계산, DB 저장, 보고서 생성이라는
// 서로 다른 네 가지 변경 이유가 한 클래스에 뭉쳐 있다
public class Employee {
    private String name;
    public Money calculatePay() { /* 급여 정책이 바뀌면 여기를 고친다 */ }
    public void save() { /* DB 스키마가 바뀌면 여기를 고친다 */ }
    public String generateReport() { /* 보고서 형식이 바뀌면 여기를 고친다 */ }
}
```

급여 계산 정책이 바뀌든, 데이터베이스 스키마가 바뀌든, 보고서 형식이 바뀌든 — 이 세 가지 서로 무관한 변경이 모두 `Employee` 클래스를 건드리게 된다. 이는 급여 정책을 수정하는 담당자가 실수로 보고서 생성 로직에 영향을 줄 위험을 만든다. 책임을 변경 이유별로 분리하면 이 결합이 사라진다.

```java
// SRP 준수: 각 클래스가 하나의 변경 이유만 갖는다
public class Employee {
    private String name;
    public String getName() { return name; }
}

public class PayCalculator {
    public Money calculatePay(Employee employee) { /* 급여 정책 담당 */ }
}

public class EmployeeRepository {
    public void save(Employee employee) { /* 영속성 담당 */ }
}
```

## 응집도: 클래스가 하나의 개념으로 뭉쳐 있는가

**응집도(Cohesion)**는 클래스의 메서드와 인스턴스 변수가 서로 얼마나 밀접하게 연관돼 있는지를 나타낸다. 메서드가 클래스의 인스턴스 변수를 더 많이 사용할수록 그 클래스의 응집도는 높다고 본다.

```java
// 높은 응집도: 모든 메서드가 topOfStack, elements 두 변수를 함께 사용한다
public class Stack {
    private int topOfStack = 0;
    private List<Integer> elements = new LinkedList<>();

    public int size() { return topOfStack; }
    public void push(int element) {
        topOfStack++;
        elements.add(element);
    }
}
```

반대로 낮은 응집도를 가진 클래스는 메서드마다 서로 다른 변수 부분집합만 사용한다(예: `setName`은 `name`만, `logMessage`는 `logger`만 사용). 이런 클래스는 사실상 서로 무관한 여러 책임이 하나의 클래스 이름 아래 묶여 있을 뿐이며, 응집도가 낮다는 것은 SRP를 위반할 가능성이 높다는 신호로 읽어야 한다. 실제로 큰 함수를 작은 함수 여럿으로 쪼개다 보면, 그 과정에서 자연스럽게 응집도 높은 작은 클래스 여럿으로 나뉠 기회가 드러나는 경우가 많다.

## OCP와 DIP: 변경에는 닫히고 확장에는 열리게

**개방-폐쇄 원칙(Open-Closed Principle, OCP)**은 클래스가 확장에는 열려 있고 기존 코드 수정에는 닫혀 있어야 한다는 원칙이다. 새로운 SQL 문 유형이 추가될 때마다 하나의 `Sql` 클래스에 메서드를 계속 추가해야 한다면, 그 클래스는 변경에 닫혀 있지 않다. `Sql`을 추상 클래스로 두고 각 SQL 문 유형을 서브클래스로 분리하면, 새로운 유형을 추가할 때 기존 클래스는 전혀 건드리지 않아도 된다 — 이는 05장에서 다룬 "switch 문을 다형성으로 대체하기"와 같은 원리다.

**의존성 역전 원칙(Dependency Inversion Principle, DIP)**은 상위 수준 모듈이 하위 수준의 구체적인 구현이 아니라 추상화에 의존해야 한다는 원칙이다.

```java
// DIP 위반: Portfolio가 구체적인 TokyoStockExchange 구현에 직접 의존한다
public class Portfolio {
    private TokyoStockExchange exchange;
}

// DIP 준수: Portfolio는 인터페이스에만 의존하고, 실제 구현은 외부에서 주입된다
public interface StockExchange { Money currentPrice(String symbol); }
public class Portfolio {
    private final StockExchange exchange;
    public Portfolio(StockExchange exchange) { this.exchange = exchange; }
}
```

`StockExchange` 인터페이스에 의존하면, 테스트에서는 실제 증권거래소 대신 `MockStockExchange`를 주입해 네트워크 없이 빠르게 검증할 수 있다. 이는 16~17장에서 다룬 F.I.R.S.T 원칙(특히 Fast, Independent)을 만족하는 테스트를 가능하게 하는 구조적 전제 조건이기도 하다.

## SOLID 다섯 원칙 한눈에 보기

Robert C. Martin이 정리한 SOLID는 SRP, OCP 외에 세 원칙을 더 포함한다. **리스코프 치환 원칙(Liskov Substitution Principle, LSP)**은 상위 타입 객체를 하위 타입 객체로 바꿔도 프로그램의 정확성이 유지돼야 한다는 원칙이고, **인터페이스 분리 원칙(Interface Segregation Principle, ISP)**은 클라이언트가 자신이 사용하지 않는 메서드에 의존하지 않아야 한다는 원칙이다.

| 원칙 | 한 줄 요약 | 이 시리즈에서 |
|:--:|:--|:--|
| SRP | 변경 이유는 하나여야 한다 | 이 장에서 상세히 |
| OCP | 확장에는 열리고 수정에는 닫힌다 | 이 장 + [05장](/post/clean-code/clean-functions-single-responsibility-principle/) |
| LSP | 하위 타입은 상위 타입을 대체할 수 있어야 한다 | 이 장에서 개괄만 |
| ISP | 쓰지 않는 메서드에 의존하지 않는다 | 이 장에서 개괄만 |
| DIP | 구체가 아니라 추상에 의존한다 | 이 장 + [20장](/post/clean-code/system-design-dependency-injection-architecture/) |

LSP와 ISP는 클래스 하나의 설계보다 클래스 간 계층 구조와 인터페이스 설계 전반에 걸친 원칙이라, 이 시리즈에서는 개괄만 다루고 심화 내용은 별도 아키텍처 시리즈([Clean Architecture 컬렉션](/post/clean-architecture/00-clean-architecture-overview-introduction/))에서 다룬다.

## 흔한 오개념

**"SRP는 클래스가 메서드 하나만 가져야 한다는 뜻이다"**는 오해가 매우 흔하다. SRP는 메서드 개수가 아니라 **변경 이유의 개수**를 제한한다. `Employee` 클래스가 `getName()`, `getAddress()`, `getPhoneNumber()` 세 메서드를 갖더라도, 이 셋이 모두 "직원 신상 정보"라는 하나의 책임에 속한다면 SRP를 위반하지 않는다.

**"SOLID를 지키면 항상 더 좋은 설계다"**는 오해도 있다. 각 원칙을 기계적으로 적용하면 작은 클래스와 인터페이스가 과도하게 늘어나, 실제 로직을 이해하려면 여러 파일을 오가야 하는 부작용이 생긴다. 이는 아래 "비판적 시각"에서 더 다룬다.

## 판단 기준: 클래스를 언제 분리할까

클래스를 분리할지 판단할 때는 "이 클래스를 변경해야 하는 서로 다른 이해관계자(급여팀, DBA, 리포트 담당자)가 몇 명인가"를 묻는다. 서로 다른 이해관계자가 같은 클래스를 각자 다른 이유로 자주 수정한다면 분리 신호다. 반면 하나의 이해관계자가 항상 함께 변경하는 필드와 메서드라면, 억지로 분리하기보다 하나의 클래스에 두는 편이 오히려 응집도를 높인다.

## 비판적 시각

SOLID, 특히 SRP와 ISP를 극단까지 밀어붙이면 클래스와 인터페이스의 개수가 폭발적으로 늘어나는 부작용이 있다. 하나의 개념적 기능을 이해하기 위해 5~6개의 작은 클래스와 인터페이스를 오가며 코드를 추적해야 한다면, 이는 "책임 분리"가 아니라 "간접 계층의 과잉"이 된다. 이런 비판은 특히 자바 생태계의 과도한 "Factory Factory" 패턴 남용을 향한 오래된 농담으로도 잘 알려져 있다. 실무적으로는, 아직 실제로 두 가지 이상의 변경 이유가 관찰되지 않은 클래스를 "나중에 분리가 필요할 수도 있으니" 미리 잘게 쪼개는 것보다, 실제로 서로 다른 이유로 변경이 반복되기 시작할 때 리팩토링으로 분리하는 편이 YAGNI 원칙과 SRP를 동시에 만족시키는 절충안으로 널리 받아들여진다.

## 다음 장에서는

[19장: SOLID 원칙 리팩토링 실습](/post/clean-code/clean-classes-solid-principles-exercises/)에서는 여러 책임이 뒤섞인 God Class를 이 장의 원칙에 따라 분해해 본다.

## 평가 기준

- [ ] 클래스 크기를 "책임의 개수"로 측정하는 방법을 설명할 수 있다.
- [ ] SRP를 "메서드 개수 제한"이 아니라 "변경 이유의 개수 제한"으로 정확히 설명할 수 있다.
- [ ] OCP·DIP를 적용해 새로운 기능 추가 시 기존 코드 수정을 최소화하는 설계를 할 수 있다.
- [ ] SOLID를 과도하게 적용했을 때 생기는 부작용(간접 계층 과잉)을 판단 기준으로 설명할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 10장.
- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
