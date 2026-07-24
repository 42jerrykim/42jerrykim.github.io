---
image: "wordcloud.png"
slug: observer-pattern
collection_order: 92
draft: false
title: "[Computer Terms] 옵저버 패턴 (Observer Pattern)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "옵저버 패턴은 주체의 상태 변화를 여러 구독자에게 통지하는 행동 패턴입니다. 프런트엔드 이벤트 리스너와 발행-구독 시스템의 근간이 되는 구조를 Python 코드로 다루고, 언제 이 패턴을 피해야 하는지도 함께 짚습니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- Design-Pattern(디자인패턴)
- Observer
- Behavioral-Pattern
- GoF(Gang of Four)
- Event-Driven
- OOP(객체지향)
- Interface(인터페이스)
- Coupling(결합도)
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
- Frontend(프론트엔드)
- Web(웹)
---

## 이 장을 읽기 전에

[디자인 패턴 개요](/post/computerterms/design-patterns-overview/)에서 다룬 생성·구조·행동 세 갈래 분류와 전략 패턴 예시를 안다고 가정한다. 이 챕터는 행동 패턴(Behavioral Pattern) 갈래를 옵저버 패턴으로 심화한다. 난이도는 초급–중급이며, 이벤트 루프 내부 구현이나 리액티브 프로그래밍(RxJS 등)의 연산자 체인 같은 고급 주제는 다루지 않는다.

## 한 객체의 변화를 여러 곳에 알려야 할 때

쇼핑몰의 재고 관리 시스템을 생각해보자. 특정 상품의 재고가 0이 되면 이메일 알림, 푸시 알림, 관리자 대시보드 갱신이 동시에 일어나야 한다. 가장 단순한 접근은 재고를 관리하는 클래스 안에 이메일 발송 코드, 푸시 발송 코드, 대시보드 갱신 코드를 모두 직접 호출하는 것이다. 하지만 이렇게 하면 재고 클래스가 이메일 서버 주소, 푸시 API 키 같은 무관한 세부사항을 알아야 하고, 새 알림 채널(예: SMS)이 추가될 때마다 재고 클래스 자체를 수정해야 한다. [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 개방-폐쇄 원칙 관점에서 보면, 재고 클래스는 "재고가 바뀌었다"는 사실만 알리고 그 사실을 누가 어떻게 처리할지는 몰라도 되도록 설계하는 것이 바람직하다.

**옵저버 패턴(Observer Pattern)**은 한 객체(주체, Subject)의 상태 변화를 그 변화에 관심 있는 여러 객체(옵저버, Observer)에게 통지하는 구조다. 주체는 옵저버 목록만 관리하고, 옵저버가 구체적으로 무엇을 하는지는 알지 못한다 — 옵저버는 공통 인터페이스(예: `update` 메서드)만 구현하면 되므로, 새 옵저버를 추가해도 주체 코드는 한 줄도 바뀌지 않는다. GoF는 이 패턴을 1994년 『Design Patterns』에서 "일대다(one-to-many) 의존 관계를 정의해, 한 객체의 상태가 바뀌면 그에 의존하는 모든 객체가 자동으로 통지받고 갱신되게 하는 것"으로 정의했다.

## Subject와 Observer의 협력 구조

옵저버 패턴은 두 역할로 구성된다. **주체(Subject)**는 옵저버 목록을 유지하고, `attach`(구독 등록)·`detach`(구독 해제)·`notify`(상태 변화 시 모든 옵저버에게 통지) 메서드를 제공한다. **옵저버(Observer)**는 주체로부터 통지를 받았을 때 실행할 동작을 정의하는 공통 인터페이스를 구현한다.

```python
from abc import ABC, abstractmethod


# 옵저버 인터페이스: 통지를 받으면 무엇을 할지는 각 구현체가 결정
class StockObserver(ABC):
    @abstractmethod
    def update(self, product_name: str, stock: int) -> None:
        pass


class EmailNotifier(StockObserver):
    def update(self, product_name: str, stock: int) -> None:
        if stock == 0:
            print(f"[이메일] {product_name} 재고 소진 알림 발송")


class DashboardUpdater(StockObserver):
    def update(self, product_name: str, stock: int) -> None:
        print(f"[대시보드] {product_name} 재고: {stock}개로 갱신")


# 주체: 옵저버가 구체적으로 무엇인지 몰라도 통지만 하면 된다
class Inventory:
    def __init__(self):
        self._observers: list[StockObserver] = []
        self._stock: dict[str, int] = {}

    def attach(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: StockObserver) -> None:
        self._observers.remove(observer)

    def set_stock(self, product_name: str, stock: int) -> None:
        self._stock[product_name] = stock
        self._notify(product_name, stock)

    def _notify(self, product_name: str, stock: int) -> None:
        for observer in self._observers:
            observer.update(product_name, stock)


inventory = Inventory()
inventory.attach(EmailNotifier())
inventory.attach(DashboardUpdater())
inventory.set_stock("무선 이어폰", 0)
# [이메일] 무선 이어폰 재고 소진 알림 발송
# [대시보드] 무선 이어폰 재고: 0개로 갱신
```

`Inventory`는 `EmailNotifier`나 `DashboardUpdater`라는 구체 클래스를 전혀 모른다 — `StockObserver` 인터페이스에만 의존한다. SMS 알림을 추가하려면 `StockObserver`를 구현한 새 클래스를 만들어 `attach`로 등록하기만 하면 되고, `Inventory` 클래스 코드는 수정할 필요가 없다. 이는 [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)의 개방-폐쇄 원칙과 의존성 역전 원칙을 동시에 만족하는 구조다.

## 실무 사례: 이벤트 리스너와 발행-구독 시스템

옵저버 패턴은 이론적인 예시로만 머무르지 않는다. 브라우저의 `addEventListener`가 대표적인 실무 구현체다. `button.addEventListener("click", handler)`를 호출하면 버튼(주체)이 클릭이라는 상태 변화가 일어날 때마다 등록된 `handler`(옵저버)를 호출한다 — 여러 핸들러를 같은 이벤트에 등록할 수 있는 것도, 주체가 옵저버 목록을 배열로 관리하는 옵저버 패턴의 구조 그대로다. Node.js의 `EventEmitter`, Python의 `logging` 모듈이 여러 핸들러(파일, 콘솔, 원격 서버)에 동시에 로그를 보내는 구조도 같은 원리다.

발행-구독(Publish-Subscribe) 시스템은 옵저버 패턴을 한 단계 더 느슨하게 만든 변형이다. 고전적인 옵저버 패턴에서는 주체가 옵저버 목록을 직접 들고 있어 둘 사이에 참조 관계가 존재하지만, 발행-구독 구조에서는 발행자와 구독자가 브로커(메시지 큐 등)를 매개로만 연결되어 서로의 존재조차 알지 못한다. 이 확장은 시스템 수준으로 옵저버 패턴을 적용한 것으로, [이벤트 드리븐 아키텍처](/post/computerterms/event-driven-architecture/) 챕터에서 다룬다.

## 비교: 옵저버 패턴이 없을 때와 있을 때

| 특성 | 직접 호출 방식 | 옵저버 패턴 |
|---|---|---|
| 주체가 아는 것 | 각 알림 방법의 구체적인 구현 | "통지한다"는 사실뿐, 구현은 모름 |
| 새 옵저버 추가 | 주체 코드 수정 필요 | 주체 코드 수정 없이 `attach`만 호출 |
| 결합도 | 높음(주체가 모든 구현에 의존) | 낮음(주체는 인터페이스에만 의존) |
| 런타임 구독 관리 | 어려움(하드코딩된 호출) | 쉬움(`attach`/`detach`로 동적 제어) |

## 흔한 오개념

**"옵저버 패턴은 항상 비동기다"** — 위 예시의 `_notify`는 동기적으로 순서대로 옵저버를 호출한다. 옵저버 패턴 자체는 통지 방식(동기/비동기)을 규정하지 않는다. 비동기 처리가 필요하다면 메시지 큐나 이벤트 루프 같은 별도 메커니즘을 결합해야 하며, 이는 패턴의 필수 요소가 아니라 구현 선택이다.

**"옵저버가 많아지면 성능에 문제가 없다"** — `notify`는 등록된 옵저버 수에 비례해 시간이 걸리고, 옵저버 하나가 느리거나 예외를 던지면(예외 처리를 하지 않았다면) 나머지 옵저버 통지가 막힐 수 있다. 옵저버 수가 많거나 옵저버 실행 시간이 길어질 것으로 예상되면, 동기 호출 대신 큐에 넣고 비동기로 처리하는 구조를 고려해야 한다.

## 언제 옵저버 패턴을 피해야 하는가

옵저버 패턴이 항상 이득인 것은 아니다. 가장 흔한 함정은 **구독 해제 누락으로 인한 메모리 누수**다 — `attach`한 옵저버를 `detach`하지 않으면, 주체가 그 옵저버에 대한 참조를 계속 들고 있어 옵저버가 더 이상 필요 없어져도 가비지 컬렉션 대상이 되지 못한다. 프런트엔드에서 컴포넌트가 언마운트될 때 이벤트 리스너를 제거하지 않으면 바로 이 문제가 발생한다. 두 번째는 **통지 순서의 비결정성**이다 — 여러 옵저버가 같은 통지에 반응할 때, 한 옵저버의 부수 효과가 다른 옵저버의 실행 결과에 영향을 줄 수 있는데도 표준 옵저버 패턴은 실행 순서를 보장하지 않는다. 순서가 결과에 영향을 미치는 로직이라면 옵저버 패턴 대신 명시적인 파이프라인(정해진 순서로 함수를 차례로 호출)이 더 안전하다. 마지막으로, 옵저버 수가 소수(한둘)이고 그 구성이 거의 바뀌지 않는다면 `attach`/`detach` 인프라 자체가 과잉 설계일 수 있다 — 이런 경우는 그냥 직접 호출하는 편이 코드를 추적하기 쉽다.

## 다른 개념과의 연결

옵저버 패턴은 [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)의 행동 패턴 갈래에 속하며, 발행-구독 구조를 통해 시스템 수준으로 확장되면 [이벤트 드리븐 아키텍처](/post/computerterms/event-driven-architecture/)가 된다. 다음 챕터에서는 생성 패턴 갈래를 심화해, 객체를 만드는 로직 자체를 캡슐화하는 팩토리 패턴을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. Subject와 Observer 각각의 책임을 설명하고, 이 구조가 왜 낮은 결합도를 달성하는지 설명할 수 있다. 프런트엔드 이벤트 리스너나 로깅 시스템이 옵저버 패턴의 실무 사례임을 식별할 수 있다. 옵저버 패턴과 발행-구독 시스템의 차이(참조 관계의 유무)를 구분할 수 있다.

## 참고 자료

> Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

- [Refactoring Guru: Observer](https://refactoring.guru/design-patterns/observer) — 옵저버 패턴의 구조와 다국어 코드 예제
- [MDN: EventTarget.addEventListener()](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) — 브라우저 이벤트 리스너가 옵저버 패턴을 구현하는 실제 API 문서
