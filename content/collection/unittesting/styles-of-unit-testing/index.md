---
title: "[UnitTesting] 06. 단위 테스트의 세 가지 스타일"
description: "출력 기반, 상태 기반, 통신 기반 테스트는 같은 로직도 서로 다른 방식으로 검증합니다. 4대 요소 기준으로 비교하면 출력 기반이 가장 견고하지만, 부작용이 있는 코드에는 항상 그대로 적용할 수 있는 것이 아닙니다."
date: 2026-07-16
lastmod: 2026-07-16
collection_order: 6
draft: false
image: "wordcloud.png"
tags:
  - Testing(테스트)
  - Refactoring(리팩토링)
  - Code-Quality(코드품질)
  - pytest
  - Functional-Programming(함수형프로그래밍)
  - Best-Practices
  - Software-Architecture(소프트웨어아키텍처)
  - Maintainability
  - OOP(객체지향)
  - Interface(인터페이스)
  - Composition(합성)
  - Error-Handling(에러처리)
  - Immutability
  - 단위테스트
  - 출력기반테스트
  - 상태기반테스트
  - 통신기반테스트
  - 순수함수
  - 부작용없는코드
  - API(Application Programming Interface)
  - Cohesion(응집도)
  - Documentation(문서화)
  - 리팩터링내성
  - 테스트스타일
  - Modularity
---

# 06. 단위 테스트의 세 가지 스타일

같은 기능이라도 테스트를 작성하는 방식은 하나가 아닙니다. 함수의 반환값을 확인할 수도, 객체의 상태 변화를 확인할 수도, 협력자에게 보낸 메시지를 확인할 수도 있습니다. 이 편은 세 가지 스타일을 04편의 4대 요소로 비교하고, 코드를 어느 스타일로 짜기 쉽게 만들지를 다룹니다.

## 학습 목표

- 출력 기반, 상태 기반, 통신 기반 테스트의 차이를 코드로 구분할 수 있다.
- 세 스타일을 4대 요소(회귀 방지, 리팩터링 내성, 빠른 피드백, 유지보수성) 기준으로 비교할 수 있다.
- 출력 기반 테스트를 적용하기 쉽도록 함수형 코어를 분리하는 설계 기법을 적용할 수 있다.

## 출력 기반 테스트: 입력과 반환값만 본다

**출력 기반(output-based) 테스트**는 함수에 입력을 넣고 반환값만 확인합니다. 부작용이 없는 순수 함수에 가장 잘 맞습니다.

```python
def calculate_late_fee(days_overdue: int, daily_rate: int = 500) -> int:
    if days_overdue <= 0:
        return 0
    return min(days_overdue * daily_rate, 20000)


def test_calculate_late_fee_output_based():
    assert calculate_late_fee(10) == 5000
    assert calculate_late_fee(0) == 0
    assert calculate_late_fee(100) == 20000  # 상한선
```

이 스타일은 내부 구현을 전혀 몰라도 되므로, 함수 내부를 어떻게 리팩터링하든 입력-출력 관계만 유지되면 테스트가 깨지지 않습니다. **세 스타일 중 리팩터링 내성이 가장 높습니다.**

## 상태 기반 테스트: 실행 후 객체 상태를 본다

**상태 기반(state-based) 테스트**는 함수를 실행한 뒤 객체(또는 시스템)의 상태가 어떻게 바뀌었는지 확인합니다.

```python
class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[tuple[str, int]] = []

    def add_item(self, name: str, price: int) -> None:
        self._items.append((name, price))

    def total(self) -> int:
        return sum(price for _, price in self._items)


def test_shopping_cart_state_based():
    cart = ShoppingCart()
    cart.add_item("apple", 1000)
    cart.add_item("banana", 500)

    assert cart.total() == 1500
    assert len(cart._items) == 2  # 주의: private 필드 직접 접근은 지양
```

상태 기반 테스트는 `add_item()`처럼 부작용이 있는 메서드(반환값이 없거나 의미 없는 메서드)를 검증할 때 자연스럽습니다. 다만 05편에서 다룬 것처럼 **내부 필드에 직접 접근하면 유지보수성과 리팩터링 내성이 함께 떨어지므로**, 공개 API(`total()`)를 통해 상태를 확인하는 편이 낫습니다.

```python
# 개선: 공개 API만으로 상태를 검증
def test_shopping_cart_state_based_via_public_api():
    cart = ShoppingCart()
    cart.add_item("apple", 1000)
    cart.add_item("banana", 500)

    assert cart.total() == 1500
```

## 통신 기반 테스트: 협력자에게 보낸 메시지를 본다

**통신 기반(communication-based) 테스트**는 05편에서 다룬 목을 사용해, 테스트 대상이 협력자를 어떻게 호출했는지 검증합니다.

```python
from unittest.mock import Mock


def test_order_service_communication_based():
    mock_mailer = Mock(spec=EmailSender)
    service = OrderService(repo=FakeOrderRepository(), mailer=mock_mailer)

    service.place_order("order-1", 10000)

    mock_mailer.send.assert_called_once()
```

이 스타일은 05편에서 확인한 것처럼 **비관리 의존성(이메일 발송 등)의 호출 여부 자체가 요구사항일 때만** 리팩터링 내성을 유지합니다. 관리 의존성이나 순수 로직에 통신 기반 테스트를 적용하면 리팩터링 내성이 급격히 떨어집니다.

## 세 스타일을 4대 요소로 비교

| 스타일 | 회귀 방지 | 리팩터링 내성 | 빠른 피드백 | 유지보수성 | 적합한 대상 |
|---|---|---|---|---|---|
| 출력 기반 | 높음 | 가장 높음 | 가장 빠름 | 가장 높음(준비 코드 최소) | 순수 함수, 계산 로직 |
| 상태 기반 | 높음 | 중간(공개 API 경유 시) | 빠름 | 중간 | 상태를 가진 도메인 객체 |
| 통신 기반 | 중간 | 낮음(과용 시) | 빠름 | 낮음(목 설정 코드 필요) | 비관리 의존성 호출 검증 |

**출력 기반 테스트가 4대 요소를 가장 고르게 만족합니다.** 준비할 상태가 없고(생성자 호출만 필요), 목도 필요 없으며, 반환값만 비교하면 되기 때문입니다. 문제는 실무 코드 대부분이 부작용을 동반한다는 점입니다.

## 함수형 코어, 명령형 껍데기

출력 기반 테스트를 최대한 넓게 적용하려면, 코드 자체를 **부작용 없는 계산 로직**과 **부작용을 실행하는 얇은 껍데기**로 분리하는 설계가 도움이 됩니다. 이를 흔히 **함수형 코어, 명령형 셸(Functional Core, Imperative Shell)** 패턴이라 부릅니다.

```python
# 함수형 코어: 부작용 없음, 출력 기반으로 쉽게 테스트 가능
def decide_late_fee(days_overdue: int, daily_rate: int = 500) -> int:
    if days_overdue <= 0:
        return 0
    return min(days_overdue * daily_rate, 20000)


# 명령형 셸: 부작용(저장)을 담당, 계산 로직은 함수형 코어에 위임
class OverdueBillingService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def bill_overdue_fee(self, loan_id: str, days_overdue: int) -> None:
        fee = decide_late_fee(days_overdue)  # 계산은 순수 함수에 위임
        self._repository.record_fee(loan_id, fee)
```

`decide_late_fee()`는 출력 기반 테스트로 촘촘하게 검증하고, `bill_overdue_fee()`는 "저장이 호출됐는가" 정도만 상태/통신 기반으로 가볍게 검증합니다. 이렇게 나누면 **복잡한 분기 로직은 가장 견고한 테스트 스타일로, 부작용은 최소한의 테스트로** 검증하는 구조가 됩니다.

## 실무 체크리스트

- 복잡한 분기 로직이 부작용을 일으키는 코드와 뒤섞여 있어 출력 기반 테스트를 적용하지 못하고 있지 않은가?
- 상태 기반 테스트가 private 필드에 직접 접근하고 있지 않은가?
- 통신 기반 테스트가 관리 의존성이나 순수 로직에 걸려 있지 않은가?
- 계산 로직을 함수형 코어로 분리하면 테스트가 얼마나 단순해지는지 가늠해봤는가?

## 연습 과제

### 기초(★☆☆)
- 여러분의 프로젝트에서 계산 로직과 저장 로직이 뒤섞인 메서드를 하나 찾아, 계산 부분만 순수 함수로 분리해보세요.

### 중급(★★☆)
- 분리한 순수 함수에 대해 출력 기반 테스트를 작성하고, 기존 테스트(상태/통신 기반)와 실행 속도·코드량을 비교해보세요.

### 고급(★★★)
- 하나의 기능을 세 가지 스타일로 모두 구현해보고, 요구사항이 바뀌었을 때(예: 상한선 변경) 각 스타일에서 몇 줄을 고쳐야 하는지 비교해보세요.

## 요약

- 출력 기반 테스트가 4대 요소를 가장 고르게 만족하지만, 부작용이 있는 코드에는 적용하기 어렵다.
- 상태 기반 테스트는 공개 API를 통해서만 상태를 확인해야 리팩터링 내성을 지킬 수 있다.
- 계산 로직을 함수형 코어로 분리하면 출력 기반 테스트의 적용 범위를 넓힐 수 있다.

## 참고 문헌 및 출처(추천)

- Vladimir Khorikov, 『Unit Testing: Principles, Practices, and Patterns』(Manning, 2020) — 출력/상태/통신 기반 테스트 분류
- Gary Bernhardt, "Boundaries"(2012, 컨퍼런스 발표) — 함수형 코어·명령형 셸 개념의 대표적 정리
- Martin Fowler, "Mocks Aren't Stubs"(martinfowler.com, 2007) — 상태 검증과 상호작용 검증 비교

---

## 다음 글

- 다음: [07. 가치 있는 테스트로 리팩터링하기](../refactoring-toward-valuable-tests/)
