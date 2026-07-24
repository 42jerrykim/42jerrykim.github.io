---
image: "wordcloud.png"
slug: factory-pattern
collection_order: 93
draft: false
title: "[Computer Terms] 팩토리 패턴 (Factory Pattern)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "팩토리 패턴은 객체 생성 로직을 별도 함수나 클래스로 캡슐화해 호출부가 구체 클래스를 몰라도 되게 만드는 생성 패턴입니다. 단순 팩토리·팩토리 메서드·추상 팩토리의 차이와 흔한 오개념, 과잉 설계 판단 기준을 Python 코드로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- Design-Pattern(디자인패턴)
- Factory
- Creational-Pattern
- GoF(Gang of Four)
- SOLID
- OOP(객체지향)
- Dependency-Injection(의존성주입)
- Interface(인터페이스)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Maintainability
- Code-Quality(코드품질)
- Modularity
- Readability
- Abstraction(추상화)
---

## 이 장을 읽기 전에

[디자인 패턴 개요](/post/computerterms/design-patterns-overview/)의 세 갈래 분류와 [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 의존성 역전 원칙(DIP)을 안다고 가정한다. 이 챕터는 생성 패턴(Creational Pattern) 갈래를 팩토리 패턴으로 심화한다. 난이도는 초급–중급이며, 의존성 주입 프레임워크(Spring, .NET DI 컨테이너)의 내부 구현이나 서비스 로케이터 패턴과의 비교 같은 고급 주제는 다루지 않는다.

## 호출부가 구체 클래스를 몰라야 하는 이유

결제 시스템에서 사용자가 선택한 결제 수단(신용카드, 계좌이체, 간편결제)에 따라 서로 다른 클래스의 인스턴스를 만들어야 한다고 하자. 가장 직관적인 방법은 호출부에서 `if payment_type == "card": CardPayment()`처럼 조건문으로 직접 클래스를 선택해 생성하는 것이다. 문제는 이 조건문이 결제 수단을 사용하는 모든 곳(주문 처리, 환불 처리, 결제 내역 조회)에 중복되고, 새 결제 수단이 추가될 때마다 그 모든 곳을 찾아 수정해야 한다는 점이다.

**팩토리 패턴(Factory Pattern)**은 객체 생성 로직을 별도의 클래스나 함수로 캡슐화해, 호출부가 "무엇을 요청할지"만 알고 "어떻게 만들어지는지"는 몰라도 되게 만드는 생성 패턴이다. 객체를 직접 `new`(파이썬에서는 클래스 호출)하는 대신 팩토리에게 생성을 위임하면, 생성 로직이 바뀌거나 새 클래스가 추가돼도 팩토리 내부만 수정하면 된다.

## 팩토리 메서드로 생성 로직 캡슐화하기

```python
from abc import ABC, abstractmethod


# 생성될 제품들의 공통 인터페이스
class Payment(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str:
        pass


class CardPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"신용카드로 {amount}원 결제"


class BankTransferPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"계좌이체로 {amount}원 결제"


class SimplePayPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"간편결제로 {amount}원 결제"


# 팩토리: 생성 로직을 한 곳에 캡슐화
class PaymentFactory:
    _registry = {
        "card": CardPayment,
        "bank_transfer": BankTransferPayment,
        "simple_pay": SimplePayPayment,
    }

    @classmethod
    def create(cls, payment_type: str) -> Payment:
        payment_cls = cls._registry.get(payment_type)
        if payment_cls is None:
            raise ValueError(f"지원하지 않는 결제 수단: {payment_type}")
        return payment_cls()


# 호출부는 구체 클래스(CardPayment 등)를 전혀 몰라도 된다
payment = PaymentFactory.create("card")
print(payment.pay(10000))  # 신용카드로 10000원 결제
```

새 결제 수단(예: 가상계좌)을 추가하려면 `Payment`를 구현하는 새 클래스를 만들고 `_registry`에 한 줄 추가하면 된다 — 주문 처리, 환불 처리 등 `PaymentFactory.create`를 호출하는 다른 코드는 전혀 건드릴 필요가 없다. 이는 [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 의존성 역전 원칙과도 맞닿아 있다. 호출부는 `CardPayment`라는 구체 클래스가 아니라 `Payment` 인터페이스와 `PaymentFactory`라는 추상화에 의존하기 때문이다.

## 단순 팩토리, 팩토리 메서드, 추상 팩토리의 차이

위 `PaymentFactory` 예시는 엄밀히는 GoF가 정의한 팩토리 메서드 패턴이 아니라 **단순 팩토리(Simple Factory)**에 가깝다 — 팩토리 자체가 하나의 클래스이고, `create` 메서드 안에서 조건 분기(또는 레지스트리 조회)로 어떤 클래스를 만들지 결정한다. GoF가 정의한 **팩토리 메서드(Factory Method)**는 이 결정을 서브클래스가 오버라이드하는 메서드에 위임한다 — 예를 들어 `DomesticPaymentFactory`와 `OverseasPaymentFactory`가 같은 부모 클래스의 `create_payment` 메서드를 각자 다르게 구현하는 식이다. **추상 팩토리(Abstract Factory)**는 한 단계 더 나아가, 서로 연관된 여러 제품군(예: 카드 결제와 그에 딸린 영수증 발급 로직)을 함께 생성하는 인터페이스를 정의한다. 실무에서는 단순 팩토리만으로 충분한 경우가 대부분이며, 제품군이 여러 개 얽혀 함께 교체돼야 할 때만 추상 팩토리까지 고려한다.

## 비교: 직접 생성 vs 팩토리 패턴

| 특성 | 직접 생성(`if`로 클래스 선택) | 팩토리 패턴 |
|---|---|---|
| 호출부가 아는 것 | 모든 구체 클래스와 생성 조건 | "무엇을 요청하는지"만 |
| 새 클래스 추가 | 모든 호출부의 조건문 수정 | 팩토리 내부만 수정 |
| 코드 중복 | 조건문이 여러 곳에 반복되기 쉬움 | 생성 로직이 한 곳에 모임 |
| 테스트 용이성 | 낮음(구체 클래스에 강하게 결합) | 높음(인터페이스 기준으로 목 객체 대체 가능) |

## 흔한 오개념

**"팩토리 패턴은 `if-else`를 없애는 마법이다"** — 팩토리 패턴은 조건 분기를 없애는 것이 아니라, 그 분기를 호출부 여러 곳에서 팩토리 한 곳으로 옮기는 것이다. 위 예시의 `_registry`도 결국 "어떤 문자열이 어떤 클래스에 대응하는가"라는 매핑 로직이며, 새 결제 수단마다 이 매핑을 갱신해야 한다는 점은 동일하다. 이득은 분기 자체를 없애는 것이 아니라, 분기가 한 곳에만 존재하게 만드는 데 있다.

**"모든 객체 생성에 팩토리를 써야 한다"** — 생성자 인자가 단순하고 클래스 종류가 늘어날 가능성이 낮다면, 팩토리는 불필요한 간접 계층만 추가한다. `Point(x, y)`처럼 생성 로직에 분기나 복잡한 초기화가 없는 객체까지 팩토리로 감싸는 것은 [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)에서 짚은 과잉 설계에 해당한다. 팩토리는 "생성될 구체 클래스가 런타임 조건에 따라 달라지거나, 향후 늘어날 가능성이 있는 지점"에 쓰는 도구다.

## 다른 개념과의 연결

팩토리 패턴은 [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)의 생성 패턴 갈래를 대표하며, 호출부를 구체 클래스로부터 분리한다는 목표는 [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 DIP가 구체적인 코드로 구현된 사례다. 다음 챕터에서는 이 "핵심 로직을 외부 세부사항으로부터 분리한다"는 아이디어를 클래스 수준을 넘어 애플리케이션 아키텍처 수준으로 확장한 헥사고날 아키텍처를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 팩토리 패턴이 객체 생성 로직을 어떻게 캡슐화하고, 이것이 왜 DIP의 구체적인 구현인지 설명할 수 있다. 단순 팩토리와 GoF의 팩토리 메서드, 추상 팩토리의 차이를 구분할 수 있다. 팩토리 패턴을 적용할 지점과 과잉 설계가 되는 경계를 판단할 수 있다.

## 참고 자료

> Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

- [Refactoring Guru: Factory Method](https://refactoring.guru/design-patterns/factory-method) — 팩토리 메서드 패턴의 구조와 단순 팩토리와의 차이
- [Refactoring Guru: Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) — 추상 팩토리 패턴이 연관된 제품군을 함께 생성하는 방식
