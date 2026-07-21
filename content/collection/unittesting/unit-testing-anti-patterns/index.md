---
title: "[UnitTesting] 11. 흔한 단위 테스트 안티패턴"
description: "private 메서드 테스트, 도메인 지식 유출, 시스템 시간 직접 의존, 거대 픽스처, 테스트용 프로덕션 분기 등 반복되는 단위 테스트 안티패턴 5가지를 1–10편의 원칙으로 진단하고 개선하며 시리즈를 마무리합니다."
date: 2026-07-16
lastmod: 2026-07-16
collection_order: 11
draft: false
image: "wordcloud.png"
tags:
  - Testing(테스트)
  - Refactoring(리팩토링)
  - Code-Quality(코드품질)
  - pytest
  - Pitfalls(함정)
  - Best-Practices
  - Software-Architecture(소프트웨어아키텍처)
  - Maintainability
  - Code-Review(코드리뷰)
  - Encapsulation(캡슐화)
  - Error-Handling(에러처리)
  - Edge-Cases(엣지케이스)
  - Debugging(디버깅)
  - 단위테스트
  - 안티패턴
  - private메서드테스트
  - 도메인지식유출
  - 시간의존성
  - 거대픽스처
  - Documentation(문서화)
  - OOP(객체지향)
  - Interface(인터페이스)
  - Coupling(결합도)
  - 리팩터링내성
  - System-Design
---

# 11. 흔한 단위 테스트 안티패턴

1–10편에서 원칙을 세웠다면, 이 편은 그 원칙을 거꾸로 적용해 **실무에서 반복적으로 나타나는 실수**를 진단표로 정리합니다. 아래 패턴 중 최소 하나는 익숙하게 느껴질 것입니다.

## 학습 목표

- 흔한 단위 테스트 안티패턴 5가지를 코드로 식별할 수 있다.
- 각 안티패턴이 04편의 4대 요소 중 무엇을 해치는지 설명할 수 있다.
- 안티패턴을 발견했을 때 1–10편의 원칙을 근거로 개선 방향을 제시할 수 있다.

## 안티패턴 1: private 메서드를 직접 테스트하기

```python
class OrderValidator:
    def validate(self, order) -> bool:
        return self._check_items(order) and self._check_total(order)

    def _check_items(self, order) -> bool:
        return len(order.lines) > 0

    def _check_total(self, order) -> bool:
        return order.total() > 0
```

```python
# 안티패턴: private 메서드를 이름 맹글링을 뚫고 직접 호출
def test_check_items_directly():
    validator = OrderValidator()
    order = make_order(lines=[])
    assert validator._check_items(order) is False
```

private 메서드는 클래스의 **구현 세부사항**입니다. 03편·05편에서 반복했듯, 구현 세부사항을 직접 검증하면 내부 리팩터링만으로도 테스트가 깨집니다. private 메서드가 복잡해서 테스트하고 싶다는 마음이 든다면, 그 자체가 <strong>"이 메서드는 별도 클래스로 추출돼야 한다"</strong>는 신호입니다.

```python
# 개선: 공개 API(validate)를 통해서만 검증
def test_validate_rejects_empty_order():
    validator = OrderValidator()
    order = make_order(lines=[])
    assert validator.validate(order) is False
```

## 안티패턴 2: 도메인 지식이 테스트로 유출됨

테스트가 프로덕션 코드의 계산 로직을 **그대로 재구현**해서 비교하면, 로직에 버그가 있어도 테스트가 똑같이 틀린 값을 기대하므로 통과해버립니다.

```python
# 안티패턴: 테스트가 계산 공식을 그대로 복제함
def test_calculate_late_fee_leaks_logic():
    days_overdue = 10
    daily_rate = 500
    expected = min(days_overdue * daily_rate, 20000)  # 프로덕션 코드와 동일한 공식
    assert calculate_late_fee(days_overdue) == expected
```

프로덕션 코드의 `min(days_overdue * daily_rate, 20000)`이 잘못 구현돼 있어도, 테스트가 같은 실수를 반복하면 절대 잡히지 않습니다. **좋은 테스트는 로직을 재구현하지 않고, 구체적인 숫자로 기대값을 명시**해야 합니다.

```python
# 개선: 계산 공식이 아니라 구체적인 숫자로 기대값을 명시
def test_calculate_late_fee_explicit_expected_value():
    assert calculate_late_fee(10) == 5000
    assert calculate_late_fee(100) == 20000  # 상한선에 걸림을 명시적으로 확인
```

## 안티패턴 3: 시스템 시간에 직접 의존하기

```python
from datetime import datetime


class Membership:
    def is_expired(self, expires_at: datetime) -> bool:
        return datetime.now() > expires_at  # 시스템 시간에 직접 의존
```

```python
# 안티패턴: 테스트 실행 시점에 따라 결과가 달라짐(재현 불가능)
def test_is_expired_flaky():
    membership = Membership()
    almost_now = datetime.now()
    assert membership.is_expired(almost_now) is False  # 실행 속도에 따라 결과가 바뀔 수 있음
```

`datetime.now()`를 코드 내부에서 직접 호출하면, 테스트가 **실행되는 순간의 실제 시각**에 결과가 좌우됩니다. 이런 테스트는 어제는 통과했는데 오늘은 실패하는 식으로 불안정(flaky)해지며, 04편에서 다룬 회귀 방지력을 근본적으로 훼손합니다. 시간은 **주입 가능한 의존성**으로 다뤄야 합니다.

```python
class Membership:
    def is_expired(self, expires_at: datetime, now: datetime) -> bool:
        return now > expires_at  # 시간을 외부에서 주입받음


def test_is_expired_deterministic():
    membership = Membership()
    expires_at = datetime(2026, 1, 1)

    assert membership.is_expired(expires_at, now=datetime(2026, 1, 2)) is True
    assert membership.is_expired(expires_at, now=datetime(2025, 12, 31)) is False
```

시간을 매개변수로 주입하면 테스트가 어느 시점에 실행되든 항상 같은 결과를 냅니다. 이는 04편에서 다룬 **결정론적(deterministic) 테스트**의 기본 조건입니다.

## 안티패턴 4: 거대 픽스처(God fixture)

03편에서 픽스처 재사용의 판단 기준을 다뤘습니다. 그 기준을 무시하고 모든 테스트가 공유하는 거대한 픽스처를 만들면 새로운 문제가 생깁니다.

```python
# 안티패턴: 모든 테스트가 이 하나의 거대한 픽스처에 의존함
@pytest.fixture
def everything():
    user = make_user(role="admin", verified=True, subscription="premium")
    order = make_order(user=user, lines=[("apple", 2, 1000)], status="CONFIRMED")
    payment = make_payment(order=order, method="card", status="AUTHORIZED")
    return {"user": user, "order": order, "payment": payment}


def test_order_total(everything):
    assert everything["order"].total() == 2000
```

이 테스트는 `order.total()`만 검증하는데도 `user`와 `payment`까지 준비해야 합니다. 읽는 사람은 "이 테스트가 정말 필요로 하는 상태가 무엇인지" 거대한 픽스처 정의를 열어봐야 알 수 있습니다. 게다가 `everything` 픽스처의 아무 필드나 바뀌어도 이 픽스처를 쓰는 **모든** 테스트가 영향을 받을 수 있어, 04편의 유지보수성이 떨어집니다.

```python
# 개선: 이 테스트에 필요한 만큼만 준비
def test_order_total_focused():
    order = make_order(lines=[("apple", 2, 1000)])
    assert order.total() == 2000
```

## 안티패턴 5: 테스트를 위해 프로덕션 코드에 분기를 심기

```python
class NotificationService:
    def send(self, message: str, is_test_mode: bool = False) -> None:
        if is_test_mode:
            return  # 테스트에서만 실제 발송을 건너뛰기 위한 플래그
        self._client.send_sms(message)
```

`is_test_mode` 같은 플래그를 프로덕션 코드에 심으면, 테스트 목적의 코드 경로가 실제 배포 코드에 영구히 남습니다. 이 플래그가 실수로 운영 환경에서 `True`로 설정되면 알림이 조용히 발송되지 않는 심각한 버그가 됩니다. 05편에서 다룬 것처럼, **테스트 목적의 대체는 프로덕션 코드가 아니라 테스트 코드(목/가짜 구현체)에서 처리**해야 합니다.

```python
class NotificationService:
    def send(self, message: str) -> None:
        self._client.send_sms(message)  # 테스트 분기 없음


def test_notification_service_calls_client():
    mock_client = Mock(spec=SmsClient)
    service = NotificationService(mock_client)
    service.send("hello")
    mock_client.send_sms.assert_called_once_with("hello")
```

## 안티패턴 진단표

| 안티패턴 | 해치는 요소(04편 기준) | 근본 원인 | 개선 방향 |
|---|---|---|---|
| private 메서드 직접 테스트 | 리팩터링 내성 | 구현 세부사항 검증 | 공개 API로만 검증하거나 클래스 추출 |
| 도메인 지식 유출 | 회귀 방지 | 로직을 재구현해서 비교 | 구체적인 숫자로 기대값 명시 |
| 시스템 시간 직접 의존 | 회귀 방지(불안정) | 시간이 주입 가능한 의존성이 아님 | 시간을 매개변수로 주입 |
| 거대 픽스처 | 유지보수성 | 필요 이상으로 많은 상태 공유 | 테스트별로 필요한 만큼만 준비 |
| 테스트용 프로덕션 분기 | 회귀 방지, 안전성 | 테스트 대체를 프로덕션 코드에 심음 | 목/가짜 구현체로 테스트 쪽에서 처리 |

## 실무 체크리스트

- 테스트가 private 메서드나 내부 필드에 직접 접근하고 있지 않은가?
- 테스트의 기대값이 프로덕션 코드의 계산 공식을 그대로 복제한 것은 아닌가?
- 시간, 난수, 외부 환경에 의존하는 코드가 결정론적으로 테스트되고 있는가?
- 픽스처가 이 테스트에 필요한 것보다 훨씬 많은 상태를 준비하고 있지 않은가?
- 프로덕션 코드에 `if is_test`류의 분기가 남아 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- 여러분의 테스트 스위트에서 위 5가지 안티패턴 중 하나를 찾아보세요.

### 중급(★★☆)
- 찾은 안티패턴을 이 편에서 제시한 개선 방향으로 리팩터링해보세요.

### 고급(★★★)
- 팀 코드 리뷰 체크리스트에 이 5가지 안티패턴을 추가하고, 다음 스프린트 동안 새로 추가되는 테스트에 실제로 적용해보세요.

## 요약

- private 메서드·내부 필드를 직접 테스트하면 리팩터링 내성이 떨어진다. 공개 API로만 검증한다.
- 테스트가 프로덕션 로직을 재구현해 비교하면 같은 버그를 함께 통과시킨다. 구체적인 숫자로 기대값을 명시한다.
- 시간·난수 같은 비결정적 요소는 반드시 주입 가능하게 만들어 테스트를 재현 가능하게 유지한다.
- 픽스처와 프로덕션 코드 모두, 테스트를 위해 필요 이상으로 커지거나 오염되지 않도록 경계를 지킨다.

## 참고 문헌 및 출처(추천)

- Vladimir Khorikov, 『Unit Testing: Principles, Practices, and Patterns』(Manning, 2020) — 단위 테스트 안티패턴 논의
- Gerard Meszaros, 『xUnit Test Patterns: Refactoring Test Code』(2007) — 테스트 냄새(Test Smell) 카탈로그
- Martin Fowler, "Eradicating Non-Determinism in Tests"(martinfowler.com, 2011) — 비결정적 테스트(flaky test)의 원인과 해법

---

## UnitTesting 시리즈를 마치며

00편에서 "테스트가 있어도 프로젝트가 느려지는 이유"로 시작한 이 여정은, 이제 그 원인을 진단하고 고치는 구체적인 도구를 모두 갖췄습니다. 01편의 목표 정의부터 11편의 안티패턴 진단표까지, 이 시리즈가 반복해서 강조한 것은 한 문장으로 요약됩니다.

> **테스트는 코드와 똑같이 설계의 대상이다. "테스트가 있다"가 아니라 "이 테스트가 04편의 4대 요소를 만족하는가"로 판단하라.**

목을 쓸지 말지, 어떤 스타일을 고를지, 단위 테스트와 통합 테스트의 비중을 어떻게 나눌지 — 이 모든 판단은 결국 회귀 방지, 리팩터링 내성, 빠른 피드백, 유지보수성이라는 같은 저울 위에서 이뤄집니다. 이 저울을 실무의 매 테스트 작성·리뷰 순간에 그대로 적용해보시기 바랍니다.
