---
draft: false
collection_order: 21
slug: emergent-design-simple-design-principles
title: "[Clean Code] 21장. 창발적 설계 네 가지 규칙"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "켄트 벡이 제시한 단순한 설계 네 규칙(테스트 통과, 중복 제거, 의도 표현, 클래스·메서드 최소화)을 우선순위 순서로 설명하고, 사전 설계(BDUF)와 창발적 설계 사이의 오래된 논쟁을 규칙 충돌 판단 기준과 함께 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Design-Pattern(디자인패턴)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Testing(테스트)
- TDD(Test-Driven Development)
- Software-Architecture(소프트웨어아키텍처)
- Template-Method
- Java
- Implementation(구현)
- Pitfalls(함정)
- SOLID
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- Code-Review(코드리뷰)
- Modularity
- Coupling(결합도)
- OOP(객체지향)
- System-Design
---

## 이 장을 읽기 전에

이 장은 [16~17장](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 다룬 TDD와 [18장](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룬 SOLID를 하나의 우선순위 체계로 묶는다. 이 시리즈 전반의 원칙을 이미 접했다는 전제로 진행하는 통합적인 장이다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 네 규칙 전체 | 각 규칙이 무엇을 요구하는지 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | 규칙끼리 충돌할 때 우선순위에 따라 판단한다 |

## 창발성: 단순한 규칙에서 좋은 설계가 나온다

**창발성(Emergence)**은 단순한 요소들의 상호작용에서 예상보다 복잡하고 정교한 성질이 나타나는 현상을 가리킨다. 개미 한 마리의 행동 규칙은 단순하지만, 수천 마리가 상호작용하면 정교한 군집 행동이 나타나는 것이 대표적인 예다. Kent Beck은 이 개념을 소프트웨어 설계에 적용해, 복잡한 아키텍처를 처음부터 완벽하게 설계하려 하기보다 **네 가지 단순한 규칙을 꾸준히 따르면 좋은 설계가 자연스럽게 드러난다**고 제안했다. 이 네 규칙은 우선순위 순서로 나열된다 — 뒤 규칙은 앞 규칙을 위반하지 않는 한도 내에서만 적용한다.

## 규칙 1: 모든 테스트를 통과한다

가장 먼저, 그리고 가장 우선하는 규칙은 시스템이 의도한 대로 동작함을 검증하는 테스트를 모두 통과하는 것이다. 테스트가 통과하지 않는 시스템은 애초에 "설계가 좋은가"를 논할 자격이 없다 — 검증되지 않은 코드는 그 자체로 신뢰할 수 없기 때문이다. 이 규칙은 [16장](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 다룬 TDD와 직결된다. 테스트를 통과시키려는 압박은 부수적인 효과도 낳는다 — 시스템을 테스트하기 쉽게 만들려면 자연히 클래스는 작아지고 결합도는 낮아지는 경향이 있다. 테스트 가능성을 추구하는 것만으로도 18장에서 다룬 SRP, DIP에 가까워지는 설계가 얻어지는 셈이다.

## 규칙 2: 중복을 제거한다

중복된 코드는 변경이 필요할 때 같은 수정을 여러 곳에 반복해야 하고, 한 곳이라도 빠뜨리면 버그가 된다. 중복 제거는 05장에서 다룬 함수 추출, 11장에서 다룬 다형성 등 이 시리즈 전체에서 반복적으로 등장한 기법들의 공통 목적이기도 하다.

```java
// 중복: 두 메서드가 거의 동일한 로직을 반복한다
public void printWeekdaySchedule() {
    System.out.println("=== 평일 일정 ===");
    for (Task task : weekdayTasks) {
        System.out.println(task.getTime() + " - " + task.getName());
    }
}
public void printWeekendSchedule() {
    System.out.println("=== 주말 일정 ===");
    for (Task task : weekendTasks) {
        System.out.println(task.getTime() + " - " + task.getName());
    }
}

// 중복 제거: 공통 절차는 템플릿 메서드로, 달라지는 부분만 인수로 분리
public void printSchedule(String title, List<Task> tasks) {
    System.out.println("=== " + title + " ===");
    for (Task task : tasks) {
        System.out.println(task.getTime() + " - " + task.getName());
    }
}
```

이 예제는 단순한 매개변수화로 해결됐지만, 중복되는 부분이 알고리즘의 뼈대는 같고 세부 단계만 다르다면 GoF의 **템플릿 메서드 패턴(Template Method Pattern)**을 적용해 상위 클래스가 알고리즘 구조를 정의하고 하위 클래스가 세부 단계를 채우는 방식으로 확장할 수 있다.

## 규칙 3: 프로그래머의 의도를 표현한다

코드는 동작할 뿐 아니라, 읽는 사람에게 "왜 이렇게 작성했는지"를 전달해야 한다. 이 규칙은 이 시리즈에서 이미 여러 챕터에 걸쳐 다뤄진 원칙들—[03장](/post/clean-code/meaningful-naming-conventions-variables-functions/)의 좋은 이름, [05장](/post/clean-code/clean-functions-single-responsibility-principle/)의 작은 함수, [16장](/post/clean-code/unit-testing-tdd-test-driven-development/)의 좋은 테스트—을 하나의 상위 목표로 묶는다. 잘 작성된 표준 디자인 패턴의 이름(`Factory`, `Observer`, `Strategy`)을 코드에 그대로 사용하는 것도 의도 표현에 도움이 된다 — 그 패턴을 아는 독자에게는 클래스 이름 자체가 구조에 대한 설명이 되기 때문이다.

## 규칙 4: 클래스와 메서드 수를 최소로 줄인다

앞의 세 규칙을 지키려다 보면 함수와 클래스를 계속 잘게 나누는 방향으로 흐르기 쉽다. 네 번째 규칙은 이 경향에 제동을 거는 균형추다 — 클래스와 메서드 수는 낮게 유지해야 하지만, 이는 **앞의 세 규칙(테스트 통과, 중복 제거, 의도 표현)을 해치지 않는 한도 내에서**만 적용된다. 즉 "무조건 클래스를 적게 만들라"는 뜻이 아니라, "의도 표현과 중복 제거를 위해 클래스를 나눴다면 그 이상으로 과도하게 쪼개지 말라"는 뜻이다.

## 흔한 오개념

**"창발적 설계는 사전 설계가 전혀 필요 없다는 뜻이다"**는 오해가 흔하다. 실제로 Kent Beck이 이 규칙을 제시한 맥락은 익스트림 프로그래밍(XP)의 반복적 개발 방식이며, 이는 "처음에 대략적인 방향조차 없이 무작정 코드를 작성한다"는 뜻이 아니라 "세부 설계를 한 번에 완벽하게 확정하려 하지 않고, 테스트를 통과시키고 리팩토링하는 짧은 반복을 거치며 설계를 다듬어 나간다"는 뜻이다.

**"규칙 4(클래스·메서드 최소화)가 가장 중요한 규칙이다"**는 오해도 있다. 네 규칙은 명시적으로 우선순위가 매겨져 있으며, 규칙 4는 가장 낮은 우선순위다. 클래스 수를 줄이기 위해 테스트가 깨지거나(규칙 1 위반) 중복이 다시 생기거나(규칙 2 위반) 의도가 불분명해진다면(규칙 3 위반), 그 통합은 정당화되지 않는다.

## 판단 기준: 규칙이 충돌할 때

두 규칙이 서로 다른 방향을 가리킬 때는 항상 앞선 규칙을 우선한다. 예를 들어 중복을 제거하기 위한 추상화(규칙 2)가 오히려 코드의 의도를 흐리게 만든다면(규칙 3과 충돌), 이는 "거짓 중복"—우연히 비슷해 보일 뿐 실제로는 서로 다른 개념—일 가능성이 높으므로 중복 제거를 강행하지 않는 편이 낫다. 클래스를 통합해 개수를 줄이는 것(규칙 4)이 테스트를 작성하기 어렵게 만든다면(규칙 1과 충돌), 통합을 포기한다.

## 비판적 시각

창발적 설계는 애자일·XP 진영의 산물이며, "빅 디자인 업 프론트(Big Design Up Front, BDUF)"를 지지하는 전통적 소프트웨어 공학 관점과 오랫동안 대비되어 왔다. BDUF 지지자들은 대규모 시스템, 특히 분산 시스템의 근본적인 아키텍처 결정(데이터 일관성 모델, 서비스 경계)은 나중에 리팩토링으로 되돌리기에는 비용이 너무 커서, 어느 정도의 사전 설계 없이 창발에만 의존하는 것은 위험하다고 본다. 실무에서는 두 접근이 배타적이라기보다 스케일의 문제로 다뤄진다 — 클래스·함수 수준의 세부 설계는 창발적 접근(테스트를 통과시키며 리팩토링)이 효과적이지만, 서비스 경계나 데이터 모델처럼 되돌리기 비용이 큰 결정은 최소한의 사전 설계를 거치는 절충이 널리 쓰인다.

## 다음 장에서는

[22장: 동시성 결함과 방어 원칙](/post/clean-code/concurrency-multithreading-parallel-programming/)에서는 단일 스레드를 전제로 한 지금까지의 원칙이 동시성 환경에서 어떻게 달라지는지 다룬다.

## 평가 기준

- [ ] Kent Beck의 단순한 설계 네 규칙을 우선순위 순서로 나열하고 설명할 수 있다.
- [ ] 중복 코드를 템플릿 메서드 패턴 등으로 제거할 수 있다.
- [ ] 두 규칙이 충돌하는 상황에서 우선순위에 따라 어느 쪽을 따를지 판단할 수 있다.
- [ ] 창발적 설계와 사전 설계(BDUF)가 서로 다른 스케일에 적용되는 상호보완적 접근임을 설명할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 12장.
- Beck, K. (2004). *Extreme Programming Explained: Embrace Change* (2nd ed.). Addison-Wesley.
