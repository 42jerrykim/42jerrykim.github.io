---
image: "wordcloud.png"
slug: event-sourcing
collection_order: 74
draft: false
title: "[Computer Terms] 이벤트 소싱 (Event Sourcing)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "현재 상태만 저장하는 대신 상태를 바꾼 모든 이벤트를 순서대로 저장해 현재 상태를 재생으로 계산하는 이벤트 소싱의 원리와, 감사 로그·시점 복원 장점, 스키마 변경의 어려움을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Domain-Driven-Design
- CQRS(Command Query Responsibility Segregation)
- System-Design
- Database(데이터베이스)
- Software-Architecture(소프트웨어아키텍처)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Advanced
- Deep-Dive
- Case-Study
- Event-Sourcing(이벤트소싱)
- Event-Log(이벤트로그)
- Audit-Log(감사로그)
- Snapshot(스냅샷)
- Replay(재생)
- Immutability(불변성)
- Schema-Evolution(스키마진화)
- State-Reconstruction(상태재구성)
- Version-Control(버전관리)
- Command-Query-Separation
---

## 이 장을 읽기 전에

[버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 커밋 히스토리 개념과, [메시지 큐](/post/computerterms/message-queues/)에서 다룬 "상태 변화를 이벤트로 다루는" 접근을 안다고 가정한다. 이 챕터는 이 두 아이디어를 데이터 저장 방식 자체에 적용해, 애플리케이션의 상태를 어떻게 관리할지를 다룬다.

## 현재 상태만 저장하는 방식의 한계

대부분의 애플리케이션은 데이터베이스에 **현재 상태(current state)**만 저장한다. 계좌 잔액이 5만 원이면 `balance = 50000`이라는 값 하나만 테이블에 남고, 그 값이 어떤 과정을 거쳐 5만 원이 됐는지(입금 3번, 출금 1번을 거쳤는지, 아니면 한 번에 입금됐는지)는 저장되지 않는다. 이 방식은 단순하고 조회가 빠르지만 두 가지를 잃는다. 첫째, "왜 지금 이 값인가"를 설명하는 **이력**이 사라진다 — 문제가 생겼을 때(예: 잔액이 예상과 다르다는 고객 문의) 그 값이 만들어진 과정을 재구성할 방법이 없다. 둘째, 과거 특정 시점의 상태를 알고 싶어도(예: "지난달 15일의 잔액이 얼마였는가") 현재 값만 남아 있으니 답할 수 없다.

## 이벤트 소싱: 상태 대신 변화를 저장한다

**이벤트 소싱(Event Sourcing)**은 이 문제를 뒤집는 접근이다. 현재 상태를 직접 저장하는 대신, 상태를 변화시킨 **모든 이벤트를 발생한 순서대로 저장**하고, 현재 상태가 필요할 때는 그 이벤트들을 처음부터 순서대로 다시 적용해(재생, replay) 계산한다. 계좌 예제라면 `balance = 50000`이라는 값을 저장하는 대신, `계좌개설(초기잔액 0)`, `입금(30000)`, `입금(30000)`, `출금(10000)`이라는 이벤트 목록을 저장한다. 현재 잔액이 필요하면 이 이벤트들을 순서대로 적용한다: `0 + 30000 + 30000 - 10000 = 50000`.

```text
이벤트 로그 (append-only, 순서 고정):
  1. AccountOpened(initial_balance=0)
  2. MoneyDeposited(amount=30000)
  3. MoneyDeposited(amount=30000)
  4. MoneyWithdrawn(amount=10000)

현재 상태 = 이벤트를 순서대로 재생(replay)한 결과
  0 → 30000 → 60000 → 50000
```

이 접근이 [버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 Git의 커밋 히스토리와 개념적으로 닮은 이유가 여기 있다. Git도 파일의 "현재 스냅샷"만 남기지 않고, 각 커밋이 이전 상태에 어떤 변경을 가했는지를 이력으로 남기며, 특정 브랜치의 최신 상태는 그 커밋들을 순서대로 적용한 결과로 볼 수 있다. 이벤트 소싱은 이 아이디어를 애플리케이션의 도메인 데이터에 적용한 것이다 — 다만 Git의 커밋이 파일 트리의 변경을 기록한다면, 이벤트 소싱의 이벤트는 도메인에서 의미 있는 동작(입금, 출금, 주문 생성 등)을 기록한다는 점이 다르다.

## 이벤트 저장소와 불변성

이벤트 소싱에서 저장되는 이벤트는 **불변(immutable)**이다. 한 번 기록된 `MoneyDeposited(amount=30000)`은 절대 수정되거나 삭제되지 않는다. 만약 그 입금이 잘못된 것이었다면, 기존 이벤트를 고치는 대신 이를 취소하는 **새로운 이벤트**(`DepositReversed(amount=30000)`)를 추가로 기록한다. 이렇게 하면 이벤트 로그는 계속 뒤에 이벤트를 덧붙이기만 하는 **추가 전용(append-only)** 구조가 되고, 언제 어떤 일이 있었는지에 대한 기록이 절대 사라지지 않는다.

```python
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Event:
    type: str
    amount: int


class Account:
    """이벤트 로그로부터 현재 상태를 재구성하는 계좌 모델"""

    def __init__(self, events: List[Event]):
        self.balance = 0
        for event in events:
            self._apply(event)

    def _apply(self, event: Event) -> None:
        # 각 이벤트 타입이 잔액에 미치는 영향을 순서대로 적용한다
        if event.type == "MoneyDeposited":
            self.balance += event.amount
        elif event.type == "MoneyWithdrawn":
            self.balance -= event.amount
        elif event.type == "DepositReversed":
            self.balance -= event.amount


# 이벤트 로그: 실제로는 데이터베이스나 Kafka 같은 append-only 저장소에 남는다
event_log = [
    Event("MoneyDeposited", 30000),
    Event("MoneyDeposited", 30000),
    Event("MoneyWithdrawn", 10000),
]

account = Account(event_log)
assert account.balance == 50000  # 이벤트를 재생해 현재 상태를 계산
```

이 코드에서 `Account.__init__`이 이벤트 목록을 받아 순서대로 `_apply`를 호출하는 부분이 바로 "재생(replay)"이다. 실무 시스템에서는 이벤트 수가 수만~수백만 건에 이를 수 있어 매번 처음부터 재생하면 느려지므로, 특정 시점까지의 계산 결과를 **스냅샷(snapshot)**으로 저장해 두고 그 이후 이벤트만 재생하는 최적화를 함께 쓴다.

## 이벤트 소싱의 장점: 감사 로그와 시점 복원

이벤트 소싱이 현재 상태 저장 방식보다 명확히 유리한 두 지점이 있다. 첫째는 **감사 로그(Audit Log)**다. 이벤트 자체가 곧 "무엇이, 언제, 왜 일어났는가"의 완전한 기록이므로, 별도의 로깅 시스템을 추가로 구축하지 않아도 규제 준수나 분쟁 해결에 필요한 이력이 자연스럽게 남는다. 금융·의료처럼 변경 이력 추적이 법적으로 요구되는 도메인에서 이벤트 소싱이 자주 채택되는 이유다.

둘째는 **시점 복원(Point-in-Time Reconstruction)**이다. 특정 시점까지의 이벤트만 재생하면 그 시점의 상태를 정확히 재구성할 수 있다. "지난달 15일의 잔액"이 궁금하다면 그 날짜 이전의 이벤트만 순서대로 적용하면 된다. 현재 상태만 저장하는 방식에서는 이런 질문에 답하려면 별도의 스냅샷 백업이나 변경 이력 테이블을 미리 만들어 뒀어야 하지만, 이벤트 소싱에서는 이 능력이 설계 자체에 내장돼 있다.

## 트레이드오프: 이벤트 스키마 변경의 어려움

이벤트 소싱의 가장 큰 대가는 **이벤트 스키마를 바꾸기 어렵다**는 점이다. 현재 상태만 저장하는 방식에서는 데이터베이스 마이그레이션으로 기존 행(row)을 새 스키마에 맞게 한 번에 변환하면 끝이다. 하지만 이벤트 소싱에서는 과거에 기록된 수백만 건의 이벤트가 이미 옛 형식 그대로 불변으로 남아 있고, 그 이벤트들을 지금도 재생해서 현재 상태를 계산해야 한다. `MoneyDeposited` 이벤트에 나중에 `currency` 필드를 추가하기로 했다면, 그 필드가 없는 과거 이벤트들도 여전히 올바르게 재생될 수 있도록 재생 로직이 옛 형식과 새 형식을 모두 이해해야 한다.

이 문제에 대응하는 대표적인 방법은 이벤트에 **버전 번호**를 붙이고, 재생 로직이 버전별로 다른 처리(예: 옛 버전 이벤트를 읽을 때는 `currency`를 기본값 `KRW`로 간주)를 하도록 만드는 것이다. 또는 오래된 이벤트들을 새 형식으로 일괄 변환하는 **업캐스팅(upcasting)** 배치 작업을 별도로 돌리기도 한다. 어느 쪽이든, 현재 상태 저장 방식의 단순한 스키마 마이그레이션보다 설계와 운영 부담이 크다 — 이것이 이벤트 소싱을 모든 시스템에 적용하지 않고, 감사·이력 추적 가치가 큰 도메인에 선택적으로 적용하는 이유다.

## 비교: 현재 상태 저장 vs 이벤트 소싱

| 특성 | 현재 상태 저장 | 이벤트 소싱 |
|---|---|---|
| 저장하는 것 | 최신 값 | 상태를 바꾼 모든 이벤트 |
| 이력 조회 | 별도 이력 테이블 필요 | 이벤트 로그 자체가 이력 |
| 과거 시점 상태 | 별도 백업 없이는 불가 | 해당 시점까지 재생하면 가능 |
| 스키마 변경 | 마이그레이션으로 한 번에 변환 | 버전별 재생 로직 또는 업캐스팅 필요 |
| 적합한 도메인 | 이력 추적 가치가 낮은 단순 CRUD | 금융, 의료 등 감사·복원이 중요한 도메인 |

## 흔한 오개념

**"이벤트 소싱은 이벤트 기반 아키텍처(Event-Driven Architecture)와 같은 것이다"** — [메시지 큐](/post/computerterms/message-queues/)를 이용한 이벤트 기반 아키텍처는 서비스 간 **통신 방식**에 대한 것이고, 이벤트 소싱은 한 서비스 내부의 **데이터 저장 방식**에 대한 것이다. 둘은 함께 쓰이는 경우가 많지만(이벤트 소싱으로 기록한 이벤트를 메시지 큐로 다른 서비스에 전파하는 식) 서로 다른 문제를 푸는 별개의 개념이다.

**"현재 상태를 조회하려면 매번 모든 이벤트를 처음부터 재생해야 해서 느리다"** — 실무 이벤트 소싱 시스템은 매번 전체를 재생하지 않는다. 주기적으로 현재까지의 계산 결과를 스냅샷으로 저장해 두고, 조회 시에는 가장 가까운 스냅샷을 불러온 뒤 그 이후에 쌓인 이벤트만 재생한다. 또한 조회 성능이 중요한 화면에는 이벤트로부터 미리 계산해 둔 읽기 전용 뷰(CQRS의 Query 모델)를 별도로 유지해, 매 조회마다 재생 자체를 하지 않도록 설계하는 것이 일반적이다.

## 다른 개념과의 연결

이벤트 소싱은 종종 **CQRS(Command Query Responsibility Segregation)** 패턴과 함께 쓰인다 — 쓰기(Command)는 이벤트를 기록하는 이벤트 소싱 모델로, 읽기(Query)는 그 이벤트들로부터 미리 계산해 둔 조회 전용 모델로 분리해 각각을 독립적으로 최적화하는 방식이다. 이 챕터로 분산 시스템의 신뢰성 갈래(벡터 시계, 멱등성, 서킷 브레이커, 메시지 큐, 이벤트 소싱)를 마무리한다 — 다섯 챕터를 관통하는 주제는 "네트워크와 여러 노드가 만드는 불확실성을 어떻게 구조적으로 다스리는가"였다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 현재 상태만 저장하는 방식이 이력 조회와 시점 복원에서 겪는 한계를 설명할 수 있다. 이벤트 소싱에서 현재 상태가 어떻게 이벤트 재생으로 계산되는지 코드 수준에서 설명할 수 있다. 이벤트가 불변·추가 전용이어야 하는 이유와, 취소가 필요할 때 새 이벤트를 추가하는 이유를 설명할 수 있다. 이벤트 스키마 변경이 왜 어려운지, 그리고 버전 관리나 업캐스팅으로 이를 어떻게 완화하는지 설명할 수 있다. 이벤트 소싱이 모든 도메인이 아니라 감사·이력 추적 가치가 큰 도메인에 선택적으로 적합한 이유를 판단할 수 있다.

## 참고 자료

> Fowler, M. "Event Sourcing". *martinfowler.com*, Enterprise Application Architecture.

- [Fowler, M. "Event Sourcing"](https://martinfowler.com/eaaDev/EventSourcing.html) — 이벤트 소싱 패턴을 정리한 원문 글
- [Microsoft Azure Architecture Center: Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — 이벤트 소싱과 CQRS를 함께 다루는 참조 문서
