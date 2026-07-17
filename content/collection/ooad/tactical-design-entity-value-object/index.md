---
title: "[OOAD] 15. 전술적 설계: 엔티티와 밸류 오브젝트"
description: "엔티티와 밸류 오브젝트의 차이는 클래스 이름이 아니라 '동일성을 무엇으로 판단하는가'입니다. 식별자 기반 동일성과 구조적 동일성, 불변 객체 설계와 자가 검증 원칙을 컴파일 가능한 파이썬 예제 코드로 구분해서 정리합니다."
date: 2026-07-16
lastmod: 2026-07-16
collection_order: 15
draft: false
image: "wordcloud.png"
tags:
  - Domain-Driven-Design
  - Domain(도메인)
  - OOP(객체지향)
  - Abstraction(추상화)
  - Encapsulation(캡슐화)
  - Interface(인터페이스)
  - Testing(테스트)
  - Refactoring(리팩토링)
  - Code-Quality(코드품질)
  - Type-Safety
  - Immutability
  - Maintainability
  - Error-Handling(에러처리)
  - Best-Practices
  - Software-Architecture(소프트웨어아키텍처)
  - Composition(합성)
  - 엔티티
  - 밸류오브젝트
  - 동일성
  - 불변객체
  - 식별자
  - 부작용없는함수
  - 자가검증
  - Modularity
  - Coupling(결합도)
---

# 15. 전술적 설계: 엔티티와 밸류 오브젝트

14장에서 바운디드 컨텍스트로 "어디까지가 하나의 모델인가"를 정했다면, 15장부터는 그 경계 안에서 **모델을 실제 클래스로 어떻게 표현하는가**, 즉 전술적 설계를 다룹니다. 가장 기본이 되는 구분은 엔티티(Entity)와 밸류 오브젝트(Value Object)입니다. 두 개념의 차이는 문법이 아니라 **"두 객체가 같다는 것을 무엇으로 판단하는가"**에 있습니다.

## 학습 목표

- 엔티티와 밸류 오브젝트를 식별자 기반 동일성과 구조적 동일성의 차이로 설명할 수 있다.
- 밸류 오브젝트를 불변으로 설계해야 하는 이유를 설명할 수 있다.
- 기존 코드에서 엔티티로 잘못 다뤄지고 있는 밸류 오브젝트를 찾아 리팩토링할 수 있다.

## 동일성의 두 종류: 식별자 vs 구조

일상적인 객체지향 코드에서는 "두 객체가 같다"는 판단을 보통 필드값 비교로 처리합니다. 하지만 DDD 전술 설계에서는 이 판단 기준이 개념에 따라 달라져야 한다고 봅니다.

**엔티티**는 속성이 모두 같아도 서로 다른 두 개체일 수 있습니다. 이름과 생년월일이 완전히 같은 두 사람이 있어도 그들은 서로 다른 사람입니다. 엔티티의 동일성은 속성이 아니라 **고유한 식별자(identity)**로 판단합니다. 주문 하나가 시간이 지나며 상태(대기 → 확정 → 배송)가 바뀌어도, 식별자가 같으면 여전히 "같은 주문"입니다.

**밸류 오브젝트**는 반대로 속성 자체가 정체성입니다. "10,000원"이라는 금액은 그 자체로 의미가 있을 뿐, 어떤 고유한 식별자를 갖지 않습니다. 두 개의 `Money(10000, "KRW")` 객체는 서로 다른 메모리 주소에 있어도 개념적으로는 완전히 같은 값입니다. 밸류 오브젝트의 동일성은 **구조적 동일성**, 즉 속성값이 모두 같으면 같다고 판단합니다.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """밸류 오브젝트: 속성이 같으면 같은 값이다"""
    amount: int
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)


class Order:
    """엔티티: 식별자로만 동일성을 판단한다"""

    def __init__(self, order_id: str, total: Money) -> None:
        self.order_id = order_id
        self.total = total

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id
```

`Money(10000, "KRW") == Money(10000, "KRW")`는 `@dataclass(frozen=True)`가 자동 생성하는 구조적 `__eq__`에 의해 `True`가 됩니다. 반면 `Order`는 `order_id`가 다르면 나머지 필드가 모두 같아도 다른 주문으로 취급됩니다.

## 밸류 오브젝트는 불변이어야 한다

밸류 오브젝트를 가변으로 만들면 위험한 버그가 생깁니다. 예를 들어 `Money` 객체를 여러 주문이 공유하고 있는데, 한 주문에서 그 객체의 `amount`를 직접 수정하면 다른 주문의 금액도 의도치 않게 바뀝니다. 이런 문제를 근본적으로 막는 방법은 밸류 오브젝트를 **불변(immutable)**으로 설계하는 것입니다. 값을 바꿔야 하면 기존 객체를 수정하는 대신 새 객체를 반환합니다(위 `Money.__add__`가 새 `Money`를 반환하는 것이 그 예입니다).

불변 설계는 부수효과(side effect)가 없는 함수를 만들기 쉽게 하고, 여러 곳에서 안전하게 값을 공유할 수 있게 하며, 동시성 문제(여러 스레드가 같은 객체를 동시에 수정하는 문제)를 원천적으로 차단합니다. `frozen=True`나 언어별 불변 타입(Java의 `record`, Kotlin의 `data class val`)을 쓰면 컴파일/초기화 시점에 불변성이 강제됩니다.

## 밸류 오브젝트는 자가 검증한다

밸류 오브젝트는 단순한 데이터 묶음이 아니라, 자기 자신의 유효성을 스스로 보장해야 합니다. 예컨대 이메일 주소를 `str` 타입으로만 다루면, 형식이 잘못된 문자열도 시스템 어디서든 "이메일"인 것처럼 흘러 다닐 수 있습니다.

```python
import re


class Email:
    _PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, address: str) -> None:
        if not self._PATTERN.match(address):
            raise ValueError(f"invalid email format: {address}")
        self._address = address

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Email):
            return NotImplemented
        return self._address == other._address

    def __str__(self) -> str:
        return self._address
```

`Email` 객체가 존재한다는 사실 자체가 "형식이 유효한 이메일"임을 보장합니다. 이렇게 하면 이메일 형식 검증 로직을 시스템 곳곳에 중복해서 작성할 필요가 없어지고, 함수 시그니처에 `Email` 타입을 쓰는 것만으로 유효성이 이미 확인됐다는 문서 역할도 합니다. 이는 "원시 타입에 대한 집착(Primitive Obsession)"이라는 흔한 코드 냄새를 해소하는 대표적인 방법이기도 합니다.

## 엔티티 설계: 식별자와 생명주기

엔티티는 식별자 외에도, 시간이 지나며 상태가 바뀌는 **생명주기**를 가진다는 점이 밸류 오브젝트와 다릅니다. 엔티티를 설계할 때 흔한 실수는 식별자를 데이터베이스의 auto-increment PK와 동일시하는 것입니다. 도메인 관점에서 식별자는 저장 기술과 무관하게 의미를 가져야 하며(예: 주문번호), DB의 PK는 그 식별자를 저장하는 구현 세부사항일 뿐입니다. 08장에서 다룬 상태 다이어그램은 엔티티의 생명주기를 코드로 옮기기 전 검증하는 도구로 그대로 이어집니다.

## 흔한 오해: 필드가 여러 개면 엔티티다

"엔티티는 필드가 많고 복잡한 것, 밸류 오브젝트는 필드가 하나뿐인 단순한 것"이라는 오해가 흔합니다. 실제로는 필드 개수와 무관합니다. `Address`(도로명, 상세주소, 우편번호 3개 필드)는 식별자 없이 값 자체로 의미가 있으므로 밸류 오브젝트이고, `User`(필드가 `userId` 하나뿐이라도)는 식별자로 추적되는 생명주기가 있으므로 엔티티입니다. 판단 기준은 항상 **"이 개념이 시간에 따라 추적돼야 하는가, 아니면 특정 시점의 값 자체가 전부인가"**입니다.

또 하나 흔한 실수는 모든 것을 엔티티로 만드는 것입니다. `Money`, `Address`, `DateRange`처럼 값 자체로 의미가 끝나는 개념까지 식별자를 부여해 엔티티로 다루면, 불필요한 동일성 비교 로직과 저장소 매핑이 늘어나 15장에서 얻으려는 단순함(불변성, 자가 검증)을 잃습니다.

## 실무 체크리스트

- 이 객체는 시간이 지나며 상태가 바뀌어도 "같은 것"으로 추적돼야 하는가, 아니면 값이 바뀌면 그냥 다른 값인가?
- 밸류 오브젝트로 분류한 클래스가 실제로 불변(setter 없음)으로 구현돼 있는가?
- 원시 타입(`str`, `int`)으로 표현된 도메인 개념(이메일, 금액, 좌표) 중 자가 검증이 필요한 것이 방치돼 있지 않은가?
- 엔티티의 식별자가 DB의 PK 타입에 종속되지 않고 도메인 관점에서 의미를 갖는가?

## 연습 과제

### 기초(★☆☆)
- 여러분의 코드에서 `str`이나 `int`로만 표현된 도메인 개념(전화번호, 우편번호 등)을 하나 찾아 밸류 오브젝트로 감싸보세요.

### 중급(★★☆)
- 현재 가변(setter 존재)으로 구현된 밸류 오브젝트 후보를 찾아 불변으로 리팩토링하고, 값이 바뀌는 지점에서 새 객체를 반환하도록 수정해보세요.

### 고급(★★★)
- `Order` 엔티티와 `Money`, `Address` 밸류 오브젝트로 구성된 작은 도메인 모델을 설계하고, 각 클래스의 동일성 판단 로직(`__eq__`)을 직접 작성해 단위 테스트로 검증해보세요.

## 요약

- 엔티티는 식별자로, 밸류 오브젝트는 구조(속성값 전체)로 동일성을 판단한다.
- 밸류 오브젝트는 불변으로 설계해 공유 시 부수효과를 막고, 스스로 유효성을 검증하게 한다.
- 판단 기준은 필드 개수가 아니라 "시간에 따라 추적돼야 하는가"이다.

## 참고 문헌 및 출처(추천)

- Eric Evans, 『Domain-Driven Design』(2003) — 3부 "모델을 표현하는 요소들"에서 Entity, Value Object 정의
- Martin Fowler, "ValueObject"(martinfowler.com bliki)
- Vaughn Vernon, 『Implementing Domain-Driven Design』(2013) — 5~6장

---

## 다음 글

- 다음: [16. 애그리거트와 리포지터리 패턴](../aggregate-repository-pattern/)
