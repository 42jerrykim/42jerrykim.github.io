---
title: "[UnitTesting] 03. 단위 테스트의 구조: AAA 패턴과 픽스처"
description: "테스트 하나가 여러 단계를 뒤섞어 서술하면 읽는 사람이 의도를 파악하기 어렵습니다. 준비-실행-검증(AAA) 패턴으로 테스트 구조를 통일하고, 픽스처 재사용 판단 기준과 매개변수화 테스트로 코드 중복을 줄이는 실무적인 방법을 다룹니다."
date: 2026-07-16
lastmod: 2026-07-16
collection_order: 3
draft: false
image: "wordcloud.png"
tags:
  - Testing(테스트)
  - pytest
  - unittest
  - Code-Quality(코드품질)
  - Refactoring(리팩토링)
  - Best-Practices
  - Readability
  - Documentation(문서화)
  - Clean-Code(클린코드)
  - Code-Review(코드리뷰)
  - Maintainability
  - TDD(Test-Driven Development)
  - Naming
  - DRY(Don't Repeat Yourself)
  - Edge-Cases(엣지케이스)
  - 단위테스트
  - AAA패턴
  - 준비실행검증
  - 픽스처
  - 매개변수화테스트
  - 테스트명명법
  - 테스트가독성
  - Software-Architecture(소프트웨어아키텍처)
  - OOP(객체지향)
  - Modularity
---

# 03. 단위 테스트의 구조: AAA 패턴과 픽스처

같은 내용을 검증하는 테스트라도, 구조가 뒤섞여 있으면 읽는 사람이 "이 테스트가 정확히 무엇을 확인하는지" 파악하는 데 시간이 걸립니다. 이 편은 테스트 본문을 일관된 구조로 정리하는 방법과, 여러 테스트에서 반복되는 준비 코드를 줄이는 방법을 다룹니다.

## 학습 목표

- 준비(Arrange)-실행(Act)-검증(Assert) 패턴으로 테스트를 구조화할 수 있다.
- 픽스처(fixture)로 준비 코드 중복을 줄이되, 과도한 재사용이 가독성을 해치는 지점을 판단할 수 있다.
- 매개변수화 테스트로 같은 로직을 다른 입력값으로 반복 검증할 수 있다.

## AAA 패턴: 준비, 실행, 검증

**AAA 패턴**은 테스트 본문을 세 단계로 나눕니다.

- **Arrange(준비)**: 테스트에 필요한 객체와 입력값을 만든다.
- **Act(실행)**: 테스트 대상 동작을 호출한다.
- **Assert(검증)**: 실행 결과가 기대한 값과 일치하는지 확인한다.

```python
def test_apply_membership_discount():
    # Arrange
    calculator = DiscountCalculator()
    price = 10000

    # Act
    result = calculator.calculate(price, coupon_rate=0.1)

    # Assert
    assert result == 9000
```

세 단계를 시각적으로도 분리해두면(빈 줄이나 주석), 테스트를 처음 읽는 사람이 "무엇을 준비했고, 무엇을 실행했고, 무엇을 확인하는지"를 순서대로 따라갈 수 있습니다. 이 구조가 무너지는 대표적인 안티패턴이 있습니다.

```python
# 나쁜 예: 준비/실행/검증이 뒤섞여 있다
def test_apply_membership_discount_bad():
    calculator = DiscountCalculator()
    assert calculator.calculate(10000, coupon_rate=0.1) == 9000
    calculator2 = DiscountCalculator()
    assert calculator2.calculate(20000, coupon_rate=0.2) == 16000
```

이 테스트는 사실상 두 개의 테스트를 하나로 욱여넣은 것입니다. 이름은 하나인데 검증 대상은 두 가지 시나리오이므로, 실패했을 때 "무엇이" 실패했는지 테스트 이름만으로 알 수 없습니다. **하나의 테스트는 하나의 동작만 검증**하는 편이 실패 원인을 빠르게 좁히는 데 유리합니다.

## Act가 두 줄 이상이면 설계를 의심한다

Act 단계는 보통 한 줄이어야 합니다. 두 줄 이상이 필요하다면, 이는 테스트 대상 API가 여러 단계를 강제하고 있다는 신호이며 종종 캡슐화가 약하다는 뜻입니다.

```python
# 나쁜 예: Act가 여러 단계로 나뉜다 (캡슐화 약함)
def test_order_confirmation_bad():
    order = Order()
    order.add_line("apple", 2, 1000)
    order.validate()  # 준비의 일부인가, 실행의 일부인가?
    order.confirm()
    assert order.status == "CONFIRMED"
```

```python
# 개선: Order가 자신의 불변조건을 스스로 지키도록 캡슐화하면 Act가 한 줄로 줄어든다
def test_order_confirmation_good():
    order = Order()
    order.add_line("apple", 2, 1000)

    order.confirm()  # validate()는 confirm() 내부로 흡수

    assert order.status == "CONFIRMED"
```

Act가 한 줄로 줄어들지 않는다면, 테스트를 억지로 손보기 전에 **테스트 대상 클래스의 인터페이스를 먼저 재검토**하는 편이 근본적인 해결책입니다.

## 픽스처로 준비 코드 재사용하기

여러 테스트가 똑같은 준비 코드를 반복한다면 픽스처로 추출할 수 있습니다. pytest에서는 `@pytest.fixture`가 이 역할을 합니다.

```python
import pytest


@pytest.fixture
def sample_order():
    order = Order()
    order.add_line("apple", 2, 1000)
    order.add_line("banana", 1, 500)
    return order


def test_order_total_before_discount(sample_order):
    assert sample_order.total() == 2500


def test_order_confirmation(sample_order):
    sample_order.confirm()
    assert sample_order.status == "CONFIRMED"
```

픽스처는 준비 코드 중복을 줄이지만, **모든 준비 코드를 무조건 픽스처로 뽑는 것은 오히려 해롭습니다.** 픽스처가 많아지면 테스트를 읽는 사람이 "이 테스트가 정확히 어떤 상태에서 시작하는지" 확인하려고 픽스처 정의를 오가며 찾아야 합니다. 각 테스트가 필요로 하는 준비 상태가 **서로 다르다면**, 무리하게 공통 픽스처로 묶기보다 테스트 본문에 직접 쓰는 편이 낫습니다.

## 픽스처 재사용 판단 기준

| 상황 | 권장 |
|---|---|
| 준비 코드가 3개 이상 테스트에서 완전히 동일하게 반복됨 | 픽스처로 추출 |
| 준비 코드가 테스트마다 한두 줄씩 다름 | 픽스처보다 헬퍼 함수(매개변수를 받는 팩토리 함수)로 추출 |
| 테스트가 1~2개뿐인데 미리 픽스처부터 만듦 | 과도한 추상화. 필요해질 때까지 인라인 유지 |

헬퍼 함수 방식은 다음처럼 씁니다.

```python
def make_order(*, lines=None) -> Order:
    order = Order()
    for name, qty, price in (lines or [("apple", 2, 1000)]):
        order.add_line(name, qty, price)
    return order


def test_order_total_with_custom_lines():
    order = make_order(lines=[("apple", 3, 1000), ("banana", 2, 500)])
    assert order.total() == 4000
```

헬퍼 함수는 픽스처와 달리 **호출부에서 필요한 값만 바꿔 넘길 수 있어**, 테스트를 읽을 때 "이 테스트가 왜 이 값을 준비했는지"가 한눈에 드러납니다.

## 매개변수화 테스트로 반복 줄이기

같은 로직을 여러 입력값으로 검증해야 할 때, 테스트를 복사-붙여넣기하면 유지비가 커집니다. `pytest.mark.parametrize`로 하나의 테스트 정의에 여러 케이스를 실어 보낼 수 있습니다.

```python
import pytest


@pytest.mark.parametrize(
    "price, coupon_rate, expected",
    [
        (10000, 0.0, 10000),
        (10000, 0.1, 9000),
        (10000, 0.5, 5000),
        (0, 0.5, 0),
    ],
)
def test_discount_calculation(price, coupon_rate, expected):
    calculator = DiscountCalculator()
    assert calculator.calculate(price, coupon_rate) == expected
```

매개변수화 테스트는 **입력과 기대값의 관계가 동일한 로직을 검증할 때만** 적합합니다. 각 케이스가 서로 다른 검증 로직이나 다른 준비 단계를 필요로 한다면, 억지로 하나의 매개변수화 테스트로 합치지 말고 별도 테스트로 분리하는 편이 낫습니다. 매개변수화가 과하면 테스트 실패 메시지에서 "어떤 케이스가 실패했는지"를 파악하기 더 어려워질 수 있습니다.

## 테스트 이름 짓기

테스트 이름은 "무엇을 테스트하는지"가 아니라 **"어떤 상황에서 어떤 결과가 나와야 하는지"**를 드러내야 합니다.

```python
# 나쁜 예: 메서드 이름만 반복
def test_calculate():
    ...

# 개선: 상황과 기대 결과가 드러남
def test_calculate_returns_zero_when_price_is_zero():
    ...

def test_calculate_raises_error_when_coupon_rate_exceeds_one():
    ...
```

좋은 테스트 이름은 테스트가 실패했을 때 코드를 열어보지 않고도 "무엇이 잘못됐는지" 짐작하게 해줍니다. 이는 나중에 07편에서 다룰 "테스트를 문서로 활용하기"와도 직접 연결됩니다.

## 실무 체크리스트

- 테스트 본문에서 Arrange/Act/Assert 세 단계가 시각적으로 구분되는가?
- Act 단계가 한 줄을 넘는다면, 테스트가 아니라 테스트 대상의 캡슐화를 먼저 의심했는가?
- 픽스처가 오히려 "이 테스트가 어떤 상태에서 시작하는지"를 숨기고 있지 않은가?
- 테스트 이름만 보고 실패 원인을 짐작할 수 있는가?

## 연습 과제

### 기초(★☆☆)
- 여러분의 프로젝트에서 Arrange/Act/Assert가 뒤섞인 테스트를 하나 찾아 세 단계로 재정리해보세요.

### 중급(★★☆)
- 복사-붙여넣기로 늘어난 테스트 3개 이상을 찾아 `parametrize`로 통합해보세요.

### 고급(★★★)
- Act가 두 줄 이상인 테스트를 찾아, 테스트 대상 클래스의 인터페이스를 리팩터링해 Act를 한 줄로 줄여보세요.

## 요약

- AAA 패턴으로 테스트를 준비/실행/검증 세 단계로 명확히 나눈다.
- 픽스처는 준비 코드가 완전히 동일할 때만 쓰고, 조금씩 다르면 매개변수를 받는 헬퍼 함수를 쓴다.
- 매개변수화 테스트는 같은 로직·다른 입력값 조합에만 적용한다.

## 참고 문헌 및 출처(추천)

- Gerard Meszaros, 『xUnit Test Patterns: Refactoring Test Code』(2007) — 4-Phase Test(AAA와 동일한 구조) 및 픽스처 패턴의 원전
- pytest 공식 문서, "How to use fixtures" — `@pytest.fixture`와 `parametrize` 레퍼런스
- Kent Beck, 『Test-Driven Development: By Example』(2002) — 테스트 명명과 구조에 대한 실무 지침

---

## 다음 글

- 다음: [04. 좋은 단위 테스트를 가르는 4대 요소](../four-pillars-of-good-unit-tests/)
