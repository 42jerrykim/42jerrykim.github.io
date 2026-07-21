---
image: "wordcloud.png"
slug: design-patterns-overview
collection_order: 31
draft: false
title: "[Computer Terms] 디자인 패턴 개요 (Design Patterns)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "디자인 패턴은 반복되는 설계 문제에 대한 검증된 해법에 이름을 붙인 것입니다. GoF의 생성·구조·행동 패턴 분류와, 전략 패턴을 SOLID 원칙과 연결해 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- Design-Patterns(디자인패턴)
- SOLID
- OOP(객체지향)
- Strategy-Pattern(전략패턴)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Maintainability(유지보수성)
- Code-Quality(코드품질)
---

## 이 장을 읽기 전에

[결합도와 응집도](/post/computerterms/coupling-and-cohesion/), [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)를 안다고 가정한다. 디자인 패턴은 이 원칙들을 지키기 위한 "이름 붙은 해법"이라는 관점으로 접근한다 — 원칙이 목표라면, 패턴은 그 목표를 달성하는 재사용 가능한 방법이다.

## 왜 패턴에 이름을 붙이는가

서로 다른 프로젝트에서 반복적으로 같은 종류의 설계 문제(객체 생성 방식의 유연성, 서로 다른 객체 간 협력 구조)를 마주친다면, 그 해법에 공통된 이름을 붙여두는 것이 유용하다. "여기에 전략 패턴을 쓰자"는 한마디로 팀원 모두가 같은 구조(인터페이스로 알고리즘을 캡슐화하고 런타임에 교체 가능하게)를 떠올릴 수 있다면, 매번 설계를 처음부터 설명할 필요가 없다. **디자인 패턴**은 GoF(Gang of Four, 『Design Patterns』의 네 저자)가 1994년 정리한 23개 패턴을 계기로 널리 쓰이는 용어가 됐다.

## 세 갈래: 생성·구조·행동

GoF 패턴은 목적에 따라 세 갈래로 나뉜다. **생성 패턴(Creational)**은 객체를 만드는 방식 자체를 유연하게 만든다(팩토리 메서드, 싱글턴, 빌더). **구조 패턴(Structural)**은 클래스·객체를 조합해 더 큰 구조를 만드는 방법을 다룬다(어댑터, 데코레이터, 퍼사드). **행동 패턴(Behavioral)**은 객체 사이의 책임 분배와 상호작용 방식을 다룬다(전략, 옵저버, 커맨드).

## 전략 패턴: SOLID가 코드로 구현되는 모습

[결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 `OrderProcessor`와 `notifier` 인터페이스 예시가 사실 **전략 패턴(Strategy Pattern)**의 한 예다. 전략 패턴은 알고리즘(또는 동작 방식)을 인터페이스 뒤로 캡슐화해, 사용하는 쪽 코드를 건드리지 않고도 알고리즘을 교체할 수 있게 만든다.

```python
from abc import ABC, abstractmethod

# 전략 인터페이스: 어떤 할인 정책이든 이 형태만 지키면 됨
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price):
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, price):
        return price

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent

    def apply(self, price):
        return price * (1 - self.percent / 100)

class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        return max(0, price - self.amount)


class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.discount_strategy = discount_strategy   # 구체 클래스가 아니라 인터페이스에 의존 (DIP)

    def checkout(self, price):
        return self.discount_strategy.apply(price)


# 새 할인 정책을 추가해도 ShoppingCart는 한 줄도 안 바뀐다 (OCP)
cart = ShoppingCart(PercentageDiscount(10))
print(cart.checkout(10000))   # 9000.0

cart2 = ShoppingCart(FixedAmountDiscount(2000))
print(cart2.checkout(10000))  # 8000
```

이 코드에서 `ShoppingCart`는 [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 의존성 역전 원칙(구체 클래스가 아닌 `DiscountStrategy` 인터페이스에 의존)과 개방-폐쇄 원칙(새 할인 정책은 새 클래스 추가로만 확장, 기존 코드 수정 없음)을 동시에 만족한다. 전략 패턴은 이 두 원칙을 실현하는 구체적인 코드 구조인 셈이다.

## 비교: 세 갈래 패턴이 답하는 질문

| 갈래 | 답하는 질문 | 대표 패턴 |
|---|---|---|
| 생성 | 객체를 어떻게 유연하게 만들 것인가 | 팩토리 메서드, 빌더, 싱글턴 |
| 구조 | 서로 다른 인터페이스의 객체를 어떻게 조합할 것인가 | 어댑터, 데코레이터, 퍼사드 |
| 행동 | 객체 사이의 책임과 협력을 어떻게 분배할 것인가 | 전략, 옵저버, 커맨드 |

## 흔한 오개념

**"패턴을 많이 쓸수록 좋은 설계다"** — [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)에서 다룬 과잉 설계 문제가 패턴에도 그대로 적용된다. 정책이 하나뿐이고 바뀔 가능성이 낮은 곳에 전략 패턴을 미리 적용하면, `if-else` 한 줄이면 충분했을 코드가 인터페이스·구현 클래스 여러 개로 불어난다. 패턴은 "변경이 실제로 예상되는 지점"에 쓰는 도구이지, 코드를 있어 보이게 만드는 장식이 아니다.

**"디자인 패턴은 객체지향 언어에서만 쓸 수 있다"** — GoF 패턴은 클래스·인터페이스로 설명되지만, 그 아이디어(동작을 값으로 다루기, 생성을 캡슐화하기)는 함수형 언어에서도 일급 함수·클로저 같은 다른 형태로 나타난다. 예를 들어 위 전략 패턴은 파이썬에서 클래스 대신 함수를 인자로 넘기는 것만으로도 구현할 수 있다.

## 다른 개념과의 연결

전략 패턴은 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)의 낮은 결합도, [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 OCP·DIP가 실제 코드로 어떻게 구현되는지 보여주는 사례다. 다음 챕터에서는 이미 존재하는, 패턴이 적용되지 않은 코드를 어떻게 안전하게 개선해 나가는지(리팩토링)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 디자인 패턴이 GoF의 세 갈래(생성·구조·행동) 중 어디에 속하는지 목적에 따라 분류할 수 있다. 전략 패턴이 SOLID의 OCP·DIP를 코드로 어떻게 구현하는지 설명할 수 있다. 패턴을 적용해야 할 때와 과잉 설계가 되는 경계를 판단할 수 있다.

## 참고 자료

> Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

- [Refactoring Guru: Design Patterns](https://refactoring.guru/design-patterns) — GoF 23개 패턴을 그림과 다국어 코드 예제로 정리한 대표적인 참고 자료
- [Source Making: Design Patterns](https://sourcemaking.com/design_patterns) — 패턴별 적용 상황과 안티패턴 비교
