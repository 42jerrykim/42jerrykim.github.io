---
image: "wordcloud.png"
slug: solid-principles-overview
collection_order: 26
draft: false
title: "[Computer Terms] SOLID 원칙 개요"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "SOLID는 낮은 결합도와 높은 응집도를 실천 가능한 다섯 규칙으로 정리한 객체지향 설계 원칙입니다. 단일 책임 원칙을 중심으로 각 원칙의 목적과 흔한 오해를 코드로 다루고, 언제 적용하고 언제 과잉 설계로 흐르는지 판단 기준도 정리합니다."
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

**SOLID**는 단일 책임 원칙(Single Responsibility), 개방-폐쇄 원칙(Open-Closed), 리스코프 치환 원칙(Liskov Substitution), 인터페이스 분리 원칙(Interface Segregation), 의존성 역전 원칙(Dependency Inversion)의 앞글자를 딴 이름이다. 다섯 원칙 각각은 로버트 마틴(Robert C. Martin)이 2000년대 초 여러 글에서 정리했고, 이를 SOLID라는 하나의 약어로 묶어 부르는 방식은 이후 마이클 페더스(Michael Feathers)가 제안한 것으로 널리 알려져 있다. 다섯 원칙 모두 결국 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 "모듈이 서로 덜 알게, 각자는 하나의 일에 집중하게" 만드는 것을 목표로 하지만, 각각 "어떤 상황에서" 그것이 깨지는지를 다르게 짚는다.

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

## 개방-폐쇄 원칙(OCP): 기존 코드를 건드리지 않고 확장한다

**개방-폐쇄 원칙**은 "확장에는 열려 있고 변경에는 닫혀 있어야 한다"고 말한다. 새로운 결제 수단을 추가할 때마다 기존 결제 처리 코드에 분기를 추가해야 한다면, 그 코드는 새 결제 수단이 늘어날 때마다 계속 수정돼야 하므로 OCP를 위반한다.

```python
def charge_card(amount):
    print(f"카드로 {amount}원 결제")

def request_bank_transfer(amount):
    print(f"계좌이체로 {amount}원 요청")


# OCP 위반: 새 결제 수단이 추가될 때마다 이 함수를 계속 수정해야 함
def process_payment(method, amount):
    if method == "card":
        charge_card(amount)
    elif method == "bank_transfer":
        request_bank_transfer(amount)
    # 새 수단이 추가될 때마다 elif가 계속 늘어난다


# OCP 준수: 새 결제 수단은 새 클래스 추가만으로 확장됨, 기존 코드는 그대로
class CardPayment:
    def process(self, amount):
        charge_card(amount)

class BankTransferPayment:
    def process(self, amount):
        request_bank_transfer(amount)

def process_payment_v2(payment_method, amount):
    payment_method.process(amount)   # 새 결제 수단 클래스를 추가해도 이 함수는 그대로

process_payment_v2(CardPayment(), 10000)   # 카드로 10000원 결제
```

새 결제 수단(예: 간편결제)을 추가하려면 `SimplePayPayment` 클래스 하나만 새로 만들면 되고, `process_payment_v2` 함수와 기존 `CardPayment`·`BankTransferPayment` 코드는 한 줄도 건드리지 않는다 — 이것이 "확장에는 열려 있고 변경에는 닫혀 있다"는 OCP의 실제 의미다.

## 리스코프 치환 원칙(LSP): 자식이 부모의 약속을 깨면 안 된다

**리스코프 치환 원칙**은 "자식 클래스는 부모 클래스가 쓰이는 모든 곳에서 부모를 대체할 수 있어야 한다"고 말한다. 고전적인 위반 예시는 "정사각형은 직사각형이다"라는 상속 관계다.

```python
# LSP 위반: Square가 Rectangle의 약속(너비만 바꾸면 높이는 그대로)을 깬다
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):
    def set_width(self, w):
        self.width = self.height = w   # 너비를 바꿨는데 높이까지 바뀜

def resize_to_width_10(rect: Rectangle):
    rect.set_width(10)
    assert rect.height != 10   # Rectangle을 기대하고 짠 코드인데 Square를 넣으면 이 가정이 깨짐
```

`resize_to_width_10`은 `Rectangle`을 기대하고 작성됐지만, `Square`를 넣는 순간 "너비만 바뀐다"는 암묵적 계약이 깨진다 — 부모 타입을 다루는 코드가 자식 타입에서도 똑같이 동작해야 한다는 LSP를 위반한 것이다.

## 인터페이스 분리 원칙(ISP): 쓰지 않을 메서드까지 강제하지 않는다

**인터페이스 분리 원칙**은 "클라이언트가 쓰지 않는 메서드에 의존하도록 강제하지 말라"고 말한다 — 하나의 거대한 인터페이스보다, 필요한 기능별로 작게 나눈 인터페이스 여러 개가 낫다.

```python
from abc import ABC, abstractmethod

# ISP 위반: 프린터 기능만 필요한 장치도 스캔·팩스 메서드를 강제로 구현해야 함
class MultiFunctionDevice(ABC):
    @abstractmethod
    def print_doc(self, doc): pass
    @abstractmethod
    def scan(self, doc): pass
    @abstractmethod
    def fax(self, doc): pass

class SimplePrinter(MultiFunctionDevice):
    def print_doc(self, doc):
        print(f"인쇄: {doc}")
    def scan(self, doc):
        raise NotImplementedError("이 프린터는 스캔을 지원하지 않음")
    def fax(self, doc):
        raise NotImplementedError("이 프린터는 팩스를 지원하지 않음")


# ISP 준수: 기능별로 인터페이스를 분리해 필요한 것만 구현
class Printable(ABC):
    @abstractmethod
    def print_doc(self, doc): pass

class SimplePrinterV2(Printable):
    def print_doc(self, doc):
        print(f"인쇄: {doc}")
```

`SimplePrinterV2`는 실제로 지원하지 않는 `scan`·`fax` 메서드를 구현할 필요가 없다 — `Printable` 인터페이스는 프린터가 실제로 제공하는 기능만 요구한다.

## 의존성 역전 원칙(DIP): 구체 클래스가 아니라 추상화에 의존한다

**의존성 역전 원칙**은 "고수준 모듈이 저수준 모듈의 구체적인 구현이 아니라 추상화에 의존해야 한다"고 말한다 — [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 `OrderProcessor`가 `EmailNotifier`라는 구체 클래스 대신 "알림을 보낸다"는 인터페이스에 의존하도록 바꾼 것이 바로 이 원칙의 적용이다.

```python
# DIP 위반: OrderProcessor(고수준)가 EmailSender(저수준)의 구체 구현에 직접 의존
class EmailSender:
    def send(self, message):
        print(f"이메일 발송: {message}")

class OrderProcessor:
    def __init__(self):
        self.sender = EmailSender()   # 구체 클래스를 직접 생성 — SMS로 바꾸려면 이 클래스를 수정해야 함

    def complete(self, order_id):
        self.sender.send(f"주문 {order_id} 완료")


# DIP 준수: OrderProcessor는 추상화(Notifier)에만 의존, 구체 구현은 외부에서 주입
class Notifier(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotifier(Notifier):
    def send(self, message):
        print(f"이메일 발송: {message}")

class OrderProcessorV2:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier   # 추상화에 의존, 구체 클래스는 외부에서 주입됨

    def complete(self, order_id):
        self.notifier.send(f"주문 {order_id} 완료")

OrderProcessorV2(EmailNotifier()).complete("ORD-1")   # 이메일 발송: 주문 ORD-1 완료
```

## 비교: 다섯 원칙이 겨냥하는 문제

| 원칙 | 겨냥하는 문제 | 핵심 질문 |
|---|---|---|
| SRP | 서로 다른 이유로 바뀌는 코드가 한 곳에 뒤섞임 | 이 클래스가 바뀌는 이유가 몇 가지인가? |
| OCP | 기능 추가 때마다 기존 코드를 수정해야 함 | 새 기능을 기존 코드 수정 없이 추가할 수 있는가? |
| LSP | 자식 클래스가 부모의 계약을 깨뜨림 | 부모를 자식으로 바꿔도 기존 코드가 안전한가? |
| ISP | 쓰지 않는 메서드까지 구현하도록 강제됨 | 이 인터페이스가 너무 많은 걸 요구하지 않는가? |
| DIP | 고수준 로직이 구체적인 구현 세부사항에 얽매임 | 이 의존이 추상화를 향하는가, 구체 클래스를 향하는가? |

## 흔한 오개념

**"SRP는 클래스를 무조건 작게 쪼개라는 뜻이다"** — 위에서 다룬 대로 핵심은 "변경 이유의 개수"이지 "코드 줄 수"가 아니다. 서로 같은 이유로 바뀌는 로직을 억지로 여러 클래스에 쪼개 놓으면, 오히려 하나의 변경이 여러 파일에 흩어져 응집도가 낮아지는 역효과가 난다.

## 언제 적용하고 언제 과잉 설계가 되는가

다섯 원칙 모두 추상화 계층을 하나씩 더하는 방향으로 작동하므로, 무조건 적용하면 오히려 코드를 읽기 어렵게 만드는 **과잉 설계(Over-engineering)**가 된다. 판단 기준은 "이 부분이 실제로 바뀔 가능성이 있는가"다. 결제 수단이 하나뿐이고 앞으로도 추가될 계획이 없다면 OCP를 위해 인터페이스를 미리 만들 필요는 없다 — 실제로 두 번째 결제 수단이 필요해지는 시점에 리팩토링해도 늦지 않다. 반대로 요구사항 문서나 로드맵에 "다른 결제 수단도 지원 예정"처럼 변경이 예정된 지점이라면, 처음부터 확장 가능한 구조로 설계하는 비용이 나중에 기존 코드를 뜯어고치는 비용보다 작다. 요약하면, SOLID는 "변경이 예상되는 지점에 미리 놓는 방지턱"이지, 모든 클래스에 기계적으로 적용하는 체크리스트가 아니다.

## 다른 개념과의 연결

DIP의 "추상화에 의존"은 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 낮은 결합도의 구체적인 실천 방법이고, SRP는 높은 응집도의 실천 방법이다. 다음 챕터에서는 이 원칙들을 검증된 해법으로 구체화한 [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. SOLID 다섯 원칙 각각이 겨냥하는 구체적인 문제 상황을 설명할 수 있다. 단일 책임 원칙을 "메서드 개수"가 아니라 "변경 이유의 개수"로 올바르게 판단할 수 있다. SOLID를 과도하게 적용했을 때 발생하는 과잉 설계의 징후를 식별할 수 있다.

## 참고 자료

> Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.

- [Robert C. Martin: The Principles of OOD](https://web.archive.org/web/20150906155800/http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod) — SOLID 다섯 원칙을 처음 정리한 원 저자의 글
- [Refactoring Guru: SOLID Principles](https://refactoring.guru/design-patterns/what-is-pattern) — 다섯 원칙과 위반 코드 예시를 다룬 실무 참고 자료
