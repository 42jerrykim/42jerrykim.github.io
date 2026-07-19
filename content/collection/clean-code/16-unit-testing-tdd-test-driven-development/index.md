---
draft: false
collection_order: 16
slug: unit-testing-tdd-test-driven-development
title: "[Clean Code] 16. TDD 법칙과 F.I.R.S.T 원칙"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "테스트 코드를 먼저 작성하도록 강제하는 TDD 세 가지 법칙과 Red-Green-Refactor 사이클을 설명하고, 좋은 테스트가 갖춰야 할 F.I.R.S.T 원칙을 예제로 다룬다. 2014년 TDD 논쟁도 함께 짚는다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- TDD(Test-Driven Development)
- Testing(테스트)
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Java
- Debugging(디버깅)
- Refactoring(리팩토링)
- Implementation(구현)
- Pitfalls(함정)
- Edge-Cases(엣지케이스)
- Design-Pattern(디자인패턴)
- Code-Review(코드리뷰)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- CI-CD(Continuous Integration/Continuous Deployment)
- Readability
- Interface(인터페이스)
- OOP(객체지향)
- Dependency-Injection(의존성주입)
- Software-Architecture(소프트웨어아키텍처)
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [15장](/post/clean-code/api-boundaries-third-party-integration/)에서 다룬 학습 테스트 개념을 "테스트를 먼저 쓴다"는 개발 방법론 전체로 확장한다. 단위 테스트 프레임워크(JUnit, pytest 등)로 테스트를 한 번이라도 작성해 본 경험이 있으면 예제를 이해하기 쉽다. 테스트 코드 자체를 정리하는 실습은 [17장](/post/clean-code/unit-testing-tdd-exercises/)에서 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "TDD 세 가지 법칙"부터 "F.I.R.S.T 원칙"까지 | Red-Green-Refactor 사이클을 실제로 따라가며 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | TDD를 언제 엄격히 적용하고 언제 완화할지 판단한다 |

## TDD 세 가지 법칙

**테스트 주도 개발(Test-Driven Development, TDD)**은 Kent Beck이 『Test-Driven Development: By Example』(2002)에서 체계화한 개발 방법론으로, 세 가지 법칙으로 요약된다. 실패하는 단위 테스트를 작성하기 전에는 실제 코드를 작성하지 않는다. 컴파일은 성공하되 실행이 실패하는 정도로만 테스트를 작성한다. 현재 실패하는 테스트를 통과시킬 정도로만 실제 코드를 작성한다.

이 세 법칙을 지키면 테스트 작성과 구현이 몇 초~몇 분 단위로 짧게 맞물려 반복되며, 이 반복을 **Red-Green-Refactor** 사이클이라 부른다.

```java
// Red: 아직 존재하지 않는 Rectangle 클래스를 사용하는 실패하는 테스트를 먼저 작성
@Test
void calculatesAreaOfRectangle() {
    Rectangle rectangle = new Rectangle(2, 3);
    assertEquals(6, rectangle.getArea());
}

// Green: 테스트를 통과시킬 정도로만 최소한의 구현을 작성
class Rectangle {
    private final int width, height;
    Rectangle(int width, int height) { this.width = width; this.height = height; }
    int getArea() { return width * height; }
}

// Refactor: 테스트가 통과하는 상태를 유지하며 구조를 개선
// (이 예제는 이미 단순해 추가 리팩토링이 필요 없다)
```

이 사이클이 주는 가장 큰 이점은 "지금 작성 중인 코드가 의도대로 동작하는가"를 매 순간 확인할 수 있다는 확신이다. 테스트를 나중에 몰아서 작성하면, 코드를 "테스트하기 쉬운 구조"로 설계할 유인이 사라지고, 테스트가 실제 요구사항이 아니라 이미 작성된 구현을 그대로 따라가는 형식적인 코드가 되기 쉽다.

## 테스트도 코드다: 깨끗한 테스트 유지하기

테스트 코드는 프로덕션 코드와 마찬가지로 읽고 수정된다. 오히려 요구사항이 바뀔 때마다 테스트도 함께 바뀌어야 하므로, 지저분한 테스트 코드는 프로덕션 코드보다 더 큰 유지보수 부담이 된다. **테스트 하나는 하나의 개념만 검증해야 한다**는 원칙은 05장에서 다룬 "함수는 한 가지 일만 해야 한다"는 원칙을 테스트 코드에 적용한 것이다.

```java
// Bad: 하나의 테스트가 여러 개념(추가, 삭제, 크기 변화)을 한꺼번에 검증한다
@Test
void testCartOperations() {
    Cart cart = new Cart();
    cart.add(item1);
    assertEquals(1, cart.size());
    cart.add(item2);
    assertEquals(2, cart.size());
    cart.remove(item1);
    assertEquals(1, cart.size());
}

// Good: 각 테스트가 하나의 개념만 검증한다
@Test
void addingItemIncreasesCartSize() {
    Cart cart = new Cart();
    cart.add(item1);
    assertEquals(1, cart.size());
}

@Test
void removingItemDecreasesCartSize() {
    Cart cart = new Cart(item1, item2);
    cart.remove(item1);
    assertEquals(1, cart.size());
}
```

두 번째 버전에서는 테스트가 실패했을 때 테스트 이름만 보고도 "어떤 시나리오가 깨졌는지" 즉시 알 수 있다. 첫 번째 버전에서는 `testCartOperations`가 실패했다는 것만으로는 추가, 삭제, 크기 계산 중 무엇이 문제인지 알 수 없어 테스트 코드 내부를 다시 읽어야 한다.

## F.I.R.S.T 원칙

좋은 테스트가 갖춰야 할 다섯 가지 특성은 각 영단어의 첫 글자를 딴 **F.I.R.S.T**로 요약된다.

| 원칙 | 의미 | 위반 시 문제 |
|:--|:--|:--|
| **Fast(빠름)** | 테스트는 빠르게 실행되어야 한다 | 느리면 실행을 미루게 되고, 결국 버그를 늦게 발견한다 |
| **Independent(독립적)** | 테스트는 서로 의존하지 않아야 한다 | 한 테스트의 실패가 이후 테스트를 연쇄적으로 실패시켜 원인 파악이 어려워진다 |
| **Repeatable(반복 가능)** | 어떤 환경에서도 같은 결과를 내야 한다 | 네트워크나 실제 시간에 의존하면 "내 컴퓨터에선 통과하는데?"라는 상황이 생긴다 |
| **Self-Validating(자가 검증)** | 결과가 성공/실패로 명확히 나와야 한다 | 로그를 사람이 직접 읽고 판단해야 한다면 자동화된 게 아니다 |
| **Timely(적시)** | 테스트는 프로덕션 코드 작성 직전 또는 직후, 적절한 시점에 작성한다 | 너무 늦게 작성하면 테스트하기 어려운 구조로 이미 굳어진다 |

이 다섯 원칙 중 특히 **Independent**와 **Repeatable**은 서로 연결된다. 테스트가 실행 순서에 의존하거나(이전 테스트가 만든 데이터를 사용) 외부 시스템(실제 데이터베이스, 현재 시각)에 의존하면, 테스트를 어떤 순서로 실행하든 어떤 환경에서 실행하든 같은 결과가 나온다는 보장이 사라진다.

## 흔한 오개념

**"TDD는 테스트 커버리지를 100%로 만든다"**는 오해가 흔하다. TDD는 코드를 작성하는 순서(테스트 먼저)에 대한 규율이지, 커버리지 도구가 측정하는 수치 자체를 목표로 삼지 않는다. TDD를 철저히 따르더라도 예외적인 방어 코드나 프레임워크 통합 코드처럼 실질적으로 테스트하기 어렵거나 가치가 낮은 부분은 커버리지에서 빠질 수 있다.

**"테스트를 나중에 작성해도 TDD와 같은 효과를 낸다"**는 오해도 있다. 구현을 먼저 작성한 뒤 테스트를 붙이면, 테스트는 이미 정해진 구현 방식을 검증하는 형태로 작성되기 쉽다. 반면 테스트를 먼저 작성하면 "이 기능을 어떻게 호출하고 싶은가"라는 사용자 관점에서 인터페이스를 설계하게 되어, 결과적으로 더 사용하기 쉬운 API가 나오는 경향이 있다 — 이는 TDD의 부산물로 종종 언급되는 이점이다.

## 판단 기준

TDD의 세 법칙을 문자 그대로 매 순간 지키는 것이 항상 실용적이지는 않다. 요구사항이 명확하고 검증 가능한 로직(계산, 파싱, 상태 전이)에는 TDD 사이클을 엄격히 적용하는 것이 유리하다. 반면 UI 레이아웃처럼 "정답"을 테스트로 표현하기 어렵거나, 스파이크(spike, 탐색적 프로토타입)처럼 애초에 버려질 코드를 작성할 때는 테스트를 나중에 붙이거나 생략하는 것이 더 실용적일 수 있다. 핵심 판단 기준은 "이 코드가 프로덕션에 남을 것인가"와 "이 로직의 정답을 테스트로 명확히 표현할 수 있는가"이다.

## 비판적 시각

TDD의 효용을 둘러싼 논쟁 중 가장 널리 알려진 것은 2014년 Ruby on Rails 창시자 David Heinemeier Hansson(DHH)이 자신의 블로그에서 "TDD is dead"라는 글을 발표하며 촉발된 논쟁이다. DHH는 TDD가 과도한 모킹을 유도해 오히려 설계를 왜곡시키고("test-induced design damage"), Red-Green-Refactor 사이클이 실제로는 자신에게 맞지 않았다고 비판했다. 이후 Kent Beck, Martin Fowler와 DHH가 진행한 일련의 공개 화상 토론에서, Fowler는 DHH의 비판이 "TDD에는 반드시 무거운 모킹이 필요하다"는 전제에서 출발한 오해이며, 자가 테스트 코드(self-testing code)와 TDD 방법론 자체는 구분해야 한다고 반박했다. 이 논쟁이 남긴 실무적 교훈은, TDD를 "모든 상황에 예외 없이 적용해야 하는 절대 규칙"이 아니라 "설계 피드백을 빠르게 얻는 하나의 도구"로 보되, 그 도구가 오히려 설계를 왜곡시키는 신호(과도한 모킹, 구현 세부사항에 강하게 결합된 테스트)가 보이면 접근 방식 자체를 재검토해야 한다는 것이다.

## 다음 장에서는

[17장: 단위 테스트 리팩토링 실습](/post/clean-code/unit-testing-tdd-exercises/)에서는 F.I.R.S.T 원칙을 위반하는 테스트 코드를 실제로 정리해 본다.

## 평가 기준

- [ ] TDD의 세 법칙과 Red-Green-Refactor 사이클을 실제 코드로 재현할 수 있다.
- [ ] 하나의 테스트가 여러 개념을 검증하는 문제를 식별하고 분리할 수 있다.
- [ ] F.I.R.S.T 원칙 각각이 위반됐을 때 생기는 구체적 문제를 설명할 수 있다.
- [ ] TDD를 엄격히 적용할 상황과 완화할 상황을 구분할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 9장.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Fowler, M. *Is TDD Dead?* [https://martinfowler.com/articles/is-tdd-dead/](https://martinfowler.com/articles/is-tdd-dead/)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
