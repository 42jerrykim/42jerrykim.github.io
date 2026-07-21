---
image: "wordcloud.png"
slug: transaction-isolation-levels
collection_order: 65
draft: false
title: "[Computer Terms] 트랜잭션 격리 수준 (Isolation Levels)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "트랜잭션 격리 수준은 동시에 실행되는 트랜잭션이 서로의 결과를 얼마나 볼 수 있는지 정하는 규칙입니다. 4단계 표준 수준과 각 수준에서 발생하는 이상 현상을 SQL과 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- SQL(Structured Query Language)
- Concurrency(동시성)
- Isolation-Level(격리수준)
- Dirty-Read
- Phantom-Read
- PostgreSQL
- MySQL
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
- Performance(성능)
- Distributed-Systems(분산시스템)
- Data-Integrity(데이터무결성)
---

## 이 장을 읽기 전에

[ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 트랜잭션의 네 가지 속성 중 고립성(Isolation)을 구체화하는 챕터다. 트랜잭션이 원자적으로 커밋·롤백된다는 것과, 동시에 여러 트랜잭션이 실행될 때 서로의 중간 결과를 얼마나 볼 수 있는지는 별개의 문제라는 점을 먼저 이해하고 있어야 한다.

## 왜 고립성에 "수준"이 필요한가

고립성을 가장 엄격하게 지키는 방법은 간단하다. 한 번에 트랜잭션 하나만 실행되도록 하면 된다. 하지만 이렇게 하면 동시성이 완전히 사라져 처리량이 급격히 떨어진다. 반대로 트랜잭션 간의 간섭을 전혀 막지 않으면 처리량은 높아지지만, 한 트랜잭션이 다른 트랜잭션의 커밋되지 않은 중간 상태를 읽는 등 데이터 일관성이 깨질 위험이 커진다. **격리 수준(Isolation Level)**은 이 정확성과 동시성 사이에서 애플리케이션이 감내할 수 있는 위험을 선택하는 다이얼이다. SQL 표준(ANSI SQL-92)은 이 다이얼을 네 단계로 정의한다.

## 세 가지 이상 현상과 네 가지 수준

격리 수준이 낮을수록 더 많은 종류의 **이상 현상(Anomaly)**이 허용된다. **더티 리드(Dirty Read)**는 다른 트랜잭션이 아직 커밋하지 않은 값을 읽는 현상이다. 그 트랜잭션이 이후 롤백되면 방금 읽은 값은 애초에 존재한 적 없는 데이터가 된다. **반복 불가능한 읽기(Non-repeatable Read)**는 같은 트랜잭션 안에서 같은 행을 두 번 읽었는데 그 사이 다른 트랜잭션이 커밋한 변경 때문에 값이 달라지는 현상이다. **팬텀 리드(Phantom Read)**는 같은 조건으로 두 번 범위 조회를 했는데, 그 사이 다른 트랜잭션이 새 행을 삽입해 두 번째 조회에만 나타나는 행이 생기는 현상이다.

**Read Uncommitted**는 커밋되지 않은 데이터까지 읽을 수 있어 세 이상 현상을 모두 허용한다. **Read Committed**는 커밋된 데이터만 읽도록 해 더티 리드를 막지만, 트랜잭션 도중 다시 읽으면 다른 값이 나올 수 있다. **Repeatable Read**는 트랜잭션 시작 시점의 스냅샷을 유지해 반복 불가능한 읽기까지 막지만, 표준상으로는 팬텀 리드가 남는다(PostgreSQL은 구현 방식 덕분에 이 수준에서도 팬텀 리드를 막는다는 점은 뒤에서 다룬다). **Serializable**은 모든 트랜잭션이 마치 순서대로 하나씩 실행된 것과 동일한 결과를 내도록 보장해 세 이상 현상을 모두 막는다.

| 격리 수준 | Dirty Read | Non-repeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | 발생 | 발생 | 발생 |
| Read Committed | 방지 | 발생 | 발생 |
| Repeatable Read | 방지 | 방지 | 발생(표준 기준) |
| Serializable | 방지 | 방지 | 방지 |

## SQL로 격리 수준 설정하기

애플리케이션은 트랜잭션을 시작하기 전에 필요한 격리 수준을 명시적으로 지정할 수 있다. 지정하지 않으면 데이터베이스마다 다른 기본값이 적용된다(PostgreSQL·Oracle은 Read Committed, MySQL의 InnoDB는 Repeatable Read가 기본값이다).

```sql
-- 이번 트랜잭션만 Serializable로 실행
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;

SELECT balance FROM accounts WHERE account_id = 42;
-- 다른 트랜잭션이 동시에 이 행을 수정하려 하면 충돌이 감지되어
-- 둘 중 하나는 커밋 시점에 실패(serialization failure)한다
UPDATE accounts SET balance = balance - 100 WHERE account_id = 42;

COMMIT;
```

Serializable에서는 성능 대신 정확성을 최대로 얻는 대가로, 위 예시처럼 충돌이 감지된 트랜잭션이 커밋에 실패해 애플리케이션이 재시도 로직을 갖춰야 하는 경우가 생긴다. 격리 수준을 올릴수록 이런 재시도·잠금 대기 비용이 늘어나므로, 무조건 가장 엄격한 수준을 쓰기보다 애플리케이션이 실제로 어떤 이상 현상에 취약한지를 먼저 따져야 한다.

## 흔한 오개념

**"Repeatable Read를 쓰면 팬텀 리드는 신경 쓰지 않아도 된다"** — SQL 표준상 Repeatable Read는 팬텀 리드를 막는다고 보장하지 않는다. 실제로 팬텀 리드를 막는지는 구현에 따라 다르다. PostgreSQL은 Repeatable Read를 스냅샷 기반으로 구현해 사실상 팬텀 리드도 막지만, 이는 표준이 요구해서가 아니라 PostgreSQL의 구현 선택이다. 다른 데이터베이스로 마이그레이션할 때 이 가정이 깨질 수 있다.

**"격리 수준을 Serializable로 올리면 무조건 안전하다"** — Serializable은 이상 현상을 모두 막지만, 그 대가로 트랜잭션 충돌이 잦아지고 재시도가 필요해진다. 트랜잭션이 짧고 충돌이 드문 워크로드에서는 문제없지만, 동시 쓰기가 많은 시스템에서 무분별하게 적용하면 재시도 폭주로 오히려 처리량이 급락할 수 있다. 격리 수준 선택은 "가장 안전한 것"이 아니라 "필요한 만큼만 안전한 것"을 고르는 문제다.

## 다른 개념과의 연결

이 챕터에서 다룬 이상 현상들은 [레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 다룬 동시 접근 문제의 데이터베이스 버전이다. 다음 챕터에서는 락 없이도 이 격리 수준들을 구현하는 대표적인 기법인 MVCC(Multi-Version Concurrency Control)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 더티 리드·반복 불가능한 읽기·팬텀 리드 세 이상 현상을 구체적인 예로 구분해 설명할 수 있다. 네 가지 격리 수준이 각각 어떤 이상 현상을 막는지 표 없이도 설명할 수 있다. 애플리케이션의 동시성 요구에 맞게 격리 수준을 선택하고, 그 선택이 성능에 미치는 영향을 판단할 수 있다.

## 참고 자료

> "The most strict is Serializable, which is defined by the standard in a paragraph which says that any concurrent execution of a set of Serializable transactions is guaranteed to produce the same effect as running them one at a time in some order." — PostgreSQL Documentation, *13.2. Transaction Isolation*

- [PostgreSQL Documentation: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — 4단계 격리 수준과 이상 현상을 표준 및 PostgreSQL 구현 관점에서 설명하는 공식 문서
- [MySQL Documentation: InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html) — InnoDB의 기본 격리 수준과 잠금 동작 상세
