---
image: "wordcloud.png"
slug: solid-principles-overview
collection_order: 26
draft: false
title: "[Computer Terms] SOLID 원칙 개요"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "SOLID는 낮은 결합도와 높은 응집도를 실천 가능한 다섯 규칙으로 정리한 객체지향 설계 원칙입니다. 단일 책임 원칙을 중심으로 각 원칙의 목적과 흔한 오해를 코드로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- SOLID
- Coupling(결합도)
- Cohesion(응집도)
- Design-Patterns(디자인패턴)
- OOP(객체지향)
- Refactoring(리팩토링)
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
- Debugging(디버깅)
- Performance(성능)
---

## 이 장을 읽기 전에

[결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 "낮은 결합도, 높은 응집도"라는 기준을 안다고 가정한다. SOLID는 이 추상적인 기준을 "이런 코드를 보면 이 원칙을 적용해라"는 구체적인 다섯 가지 규칙으로 풀어놓은 것이다.

## SOLID는 왜 다섯 개로 나뉘어 있는가

**SOLID**는 로버트 마틴(Robert C. Martin)이 여러 객체지향 설계 원칙을 묶어 부른 이름으로, 단일 책임 원칙(Single Responsibility), 개방-폐쇄 원칙(Open-Closed), 리스코프 치환 원칙(Liskov Substitution), 인터페이스 분리 원칙(Interface Segregation), 의존성 역전 원칙(Dependency Inversion)의 앞글자를 딴 것이다. 다섯 원칙 모두 결국 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 "모듈이 서로 덜 알게, 각자는 하나의 일에 집중하게" 만드는 것을 목표로 하지만, 각각 "어떤 상황에서" 그것이 깨지는지를 다르게 짚는다.

## 단일 책임 원칙(SRP): 가장 오해받는 원칙

**단일 책임 원칙**은 "클래스는 변경할 이유를 하나만 가져야 한다"고 말한다. 여기서 가장 흔한 오해가 "하나의 메서드만 가져야 한다"거나 "클래스가 작아야 한다"는 것이다. 실제로는 **"변경의 이유"**가 핵심이다. [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 `OrderManager` 예시를 다시 보면, 계산 로직이 바뀌는 이유(세율 변경)와 이메일 형식이 바뀌는 이유(마케팅팀 요청)는 서로 무관한 팀·무관한 시점에 발생한다 — 이 "서로 다른 변경 이유"가 한 클래스에 뒤섞여 있다는 것이 SRP 위반의 진짜 신호다.

```python
# SRP 위반: "계산 로직 변경"과 "출력 형식 변경"이라는 서로 다른 이유로 이 클래스가 바뀐다
class Invoice:
    def calculate_total(self, items):
        return sum(item.price * item.quantity for item in items)

    def print_receipt(self, items):
        total = self.calculate_total(items)
        print(f"영수증\n총액: {total}원")


# SRP 준수: 계산과 출력을 서로 다른 클래스로 분리
class InvoiceCalculator:
    def calculate_total(self, items):
        return sum(item.price * item.quantity for item in items)


class ReceiptPrinter:
    def __init__(self, calculator):
        self.calculator = calculator

    def print_receipt(self, items):
        total = self.calculator.calculate_total(items)
        print(f"영수증\n총액: {total}원")
```

이제 영수증 형식을 HTML로 바꿔야 한다면 `ReceiptPrinter`만 건드리면 되고, 세율 계산 방식이 바뀐다면 `InvoiceCalculator`만 건드리면 된다 — 각 클래스가 변경 이유를 하나씩만 갖는다.

## 나머지 네 원칙 요약

**개방-폐쇄 원칙(OCP)**은 "확장에는 열려 있고 변경에는 닫혀 있어야 한다"고 말한다. 새로운 결제 수단을 추가할 때 기존 결제 처리 코드를 수정하는 대신, 새 결제 수단 클래스를 추가하는 것만으로 확장되도록 설계하는 것이 예다. **리스코프 치환 원칙(LSP)**은 "자식 클래스는 부모 클래스가 쓰이는 모든 곳에서 부모를 대체할 수 있어야 한다"고 말한다 — 흔한 위반 예시는 "정사각형은 직사각형이다"라는 상속 관계에서, 정사각형의 `set_width`가 높이까지 함께 바꿔버려 직사각형이 기대하는 동작(너비만 바뀜)을 깨는 경우다. **인터페이스 분리 원칙(ISP)**은 "클라이언트가 쓰지 않는 메서드에 의존하도록 강제하지 말라"고 말한다 — 하나의 거대한 인터페이스보다, 필요한 기능별로 작게 나눈 인터페이스 여러 개가 낫다. **의존성 역전 원칙(DIP)**은 "고수준 모듈이 저수준 모듈의 구체적인 구현이 아니라 추상화에 의존해야 한다"고 말한다 — [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 `OrderProcessor`가 `EmailNotifier`라는 구체 클래스 대신 "알림을 보낸다"는 인터페이스에 의존하도록 바꾼 것이 바로 이 원칙의 적용이다.

## 비교: 다섯 원칙이 겨냥하는 문제

| 원칙 | 겨냥하는 문제 | 핵심 질문 |
|---|---|---|
| SRP | 서로 다른 이유로 바뀌는 코드가 한 곳에 뒤섞임 | 이 클래스가 바뀌는 이유가 몇 가지인가? |
| OCP | 기능 추가 때마다 기존 코드를 수정해야 함 | 새 기능을 기존 코드 수정 없이 추가할 수 있는가? |
| LSP | 자식 클래스가 부모의 계약을 깨뜨림 | 부모를 자식으로 바꿔도 기존 코드가 안전한가? |
| ISP | 쓰지 않는 메서드까지 구현하도록 강제됨 | 이 인터페이스가 너무 많은 걸 요구하지 않는가? |
| DIP | 고수준 로직이 구체적인 구현 세부사항에 얽매임 | 이 의존이 추상화를 향하는가, 구체 클래스를 향하는가? |

## 흔한 오개념

**"SOLID를 지키면 무조건 좋은 설계다"** — 다섯 원칙 모두 추상화·분리 계층을 추가하는 방향으로 작동한다. 변경 가능성이 낮은 단순한 코드에 SOLID를 과도하게 적용하면, 실제로는 절대 안 바뀔 부분까지 인터페이스와 클래스를 나눠 오히려 코드를 읽기 어렵게 만드는 **과잉 설계(Over-engineering)**가 된다. 원칙은 "변경이 예상되는 지점"에 선택적으로 적용하는 것이지, 모든 클래스에 기계적으로 적용하는 체크리스트가 아니다.

**"SRP는 클래스를 무조건 작게 쪼개라는 뜻이다"** — 위에서 다룬 대로 핵심은 "변경 이유의 개수"이지 "코드 줄 수"가 아니다. 서로 같은 이유로 바뀌는 로직을 억지로 여러 클래스에 쪼개 놓으면, 오히려 하나의 변경이 여러 파일에 흩어져 응집도가 낮아지는 역효과가 난다.

## 다른 개념과의 연결

DIP의 "추상화에 의존"은 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 낮은 결합도의 구체적인 실천 방법이고, SRP는 높은 응집도의 실천 방법이다. 다음 챕터에서는 이 원칙들을 검증된 해법으로 구체화한 [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. SOLID 다섯 원칙 각각이 겨냥하는 구체적인 문제 상황을 설명할 수 있다. 단일 책임 원칙을 "메서드 개수"가 아니라 "변경 이유의 개수"로 올바르게 판단할 수 있다. SOLID를 과도하게 적용했을 때 발생하는 과잉 설계의 징후를 식별할 수 있다.

## 참고 자료

> Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.

- [Robert C. Martin: The Principles of OOD](https://web.archive.org/web/20150906155800/http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod) — SOLID 다섯 원칙을 처음 정리한 원 저자의 글
- [Refactoring Guru: SOLID Principles](https://refactoring.guru/design-patterns/what-is-pattern) — 다섯 원칙과 위반 코드 예시를 다룬 실무 참고 자료
