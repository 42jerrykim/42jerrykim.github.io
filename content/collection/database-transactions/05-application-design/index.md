---
collection_order: 5
date: 2026-10-02T01:00:00+09:00
lastmod: 2026-10-12T00:10:00+09:00
draft: true
title: "[Database] 05. 설계 패턴: 원자적 UPDATE, 낙관적 락, SKIP LOCKED"
slug: application-design-patterns
description: "격리 수준을 올리기 전에 쓸 수 있는 도구들을 정리합니다. 원자적 UPDATE, SELECT FOR UPDATE와 SKIP LOCKED, 버전 컬럼 낙관적 락, 제약조건, 어드바이저리 락, 멱등성 키와 재시도를 문제 유형별로 고르는 법을 다룹니다."
tags:
  - Database(데이터베이스)
  - Transaction(트랜잭션)
  - SQL(Structured Query Language)
  - PostgreSQL
  - MySQL
  - Isolation-Level(격리수준)
  - Serializable
  - Write-Skew
  - Lost-Update
  - Lock(락)
  - Deadlock(데드락)
  - Race-Condition(레이스컨디션)
  - Concurrency(동시성)
  - Consistency(일관성)
  - Data-Integrity(데이터무결성)
  - Retry(재시도)
  - Idempotency(멱등성)
  - Backend(백엔드)
  - Best-Practices
  - Design-Pattern(디자인패턴)
  - Software-Engineering(소프트웨어공학)
  - Performance(성능)
  - Python
  - Simulation(시뮬레이션)
  - Troubleshooting(트러블슈팅)
  - Guide(가이드)
  - Deep-Dive
  - Computer-Science(컴퓨터과학)
image: "wordcloud.png"
---

앞의 네 장은 격리 수준이 무엇을 보장하고 무엇을 보장하지 않는지를 다뤘다. 그런데 실무에서 동시성 버그를 만났을 때 가장 먼저 격리 수준을 올리는 것이 최선인 경우는 드물다. 격리 수준은 모든 문장에 일괄 적용되는 굵은 도구이고, 대부분의 문제는 문장 하나를 고치거나 제약조건 하나를 추가하는 가는 도구로 더 싸게 해결된다. 이 장은 그런 도구들을 충돌을 어디서 감지하는가를 기준으로 분류하고, 문제 유형별로 고르는 방법을 정리한다.

## 이 장을 읽기 전에

01장의 이상 현상 어휘, 02장의 스냅샷 구현, 03장의 락, 04장의 SSI를 앞서 읽었다고 가정한다. 특히 01장의 lost update와 write skew 예제가 이 장 전체의 출발점이다. 이 장은 단일 데이터베이스 안의 트랜잭션을 대상으로 하며, 여러 시스템에 걸친 일관성은 06장에서 다룬다.

이 장의 깊이는 초급에서 중급이다. 패턴들은 특정 DBMS에 종속되지 않는 원리를 먼저 설명하고, 문법은 PostgreSQL을 기준으로 쓰되 MySQL에서 다른 점을 짚는다. ORM이 제공하는 낙관적 락 어노테이션이나 분산 락 서비스(Redis, ZooKeeper 등)는 범위 밖이다.

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 처음 배우는 독자 | "도구를 고르는 기준", "원자적 UPDATE", "오개념" | 읽고-계산하고-쓰기 패턴의 위험을 피한다 |
| 실무 개발자 | "비관적 락과 SKIP LOCKED", "낙관적 락", "선택 지도" | 문제 유형에 맞는 패턴을 비용과 함께 고른다 |
| 심화 독자 | "제약조건과 어드바이저리 락", "재시도와 멱등성" | 격리 수준 상향과 다른 도구의 비용을 비교한다 |

## 도구를 고르는 기준

동시성 문제의 본질은 "두 트랜잭션이 같은 사실에 대해 서로 모른 채 결정을 내린다"는 것이다. 모든 해법은 이 모름을 어떤 지점에서 없애느냐로 갈린다. 가장 앞쪽에서는 아예 결정을 데이터베이스 안의 한 문장으로 합쳐 모를 틈을 없앤다. 그 다음은 결정에 필요한 행을 미리 잠가 상대를 기다리게 하는 비관적 방식, 갱신 시점에 읽은 때와 같은 상태인지 확인하는 낙관적 방식, 불변식을 스키마에 선언해 데이터베이스가 직접 위반을 거부하게 하는 방식이 있다. 마지막이 격리 수준을 Serializable로 올려 모든 읽기-쓰기 의존성을 DBMS가 추적하게 하는 방식이다. 앞쪽일수록 좁은 범위에 싸게 적용되고, 뒤쪽일수록 넓은 범위를 포괄하지만 비용이 크다.

이 분류가 유용한 이유는 도구마다 막을 수 있는 이상 현상이 다르기 때문이다. 원자적 UPDATE는 lost update를 막지만 write skew는 막지 못한다. 행 잠금은 읽은 행이 존재할 때 write skew를 막지만 팬텀형에는 소용이 없다. 제약조건은 선언할 수 있는 불변식만 지킨다. 따라서 도구 선택은 먼저 "이 버그가 01장의 어느 이상 현상인가"를 판정한 뒤 그 현상을 막는 가장 싼 도구를 고르는 순서가 되어야 한다.

그렇다면 모든 문제를 Serializable 하나로 푸는 것과 이런 가는 도구를 고르는 것은 무엇이 다른가. 적용 범위에서 Serializable은 트랜잭션 전체의 읽기-쓰기 의존성을 DBMS가 추적하므로 개발자가 이상 현상을 일일이 추론하지 않아도 되지만, 가는 도구는 문제가 되는 문장이나 행에만 적용된다. 비용에서 Serializable은 04장에서 본 대로 락 기반이면 읽기 대기와 데드락으로, SSI면 중단과 재시도로 나타나며 그 부담이 모든 트랜잭션에 퍼진다. 가는 도구의 비용은 해당 지점의 대기, 재시도, 인덱스 유지에 국한된다. 막지 못하는 이상 현상에서 가는 도구는 자신이 겨냥한 현상만 막는다. 원자적 UPDATE는 write skew를, 낙관적 락은 서로 다른 행을 쓰는 충돌을 막지 못한다. 반면 Serializable은 모든 이상 현상을 막는다. 따라서 불변식이 몇 개의 분명한 지점에 모여 있으면 가는 도구가, 불변식이 여러 테이블에 흩어져 있고 충돌이 드물며 재시도를 갖추었다면 Serializable이 합리적이다. 어느 쪽을 택해도 재시도는 필요하다.

## 원자적 UPDATE: 읽기-계산-쓰기를 한 문장으로

lost update의 전형적인 원인은 애플리케이션이 값을 읽어 코드에서 계산한 뒤 결과를 `UPDATE`로 덮어쓰는 것이다. 읽는 시점과 쓰는 시점 사이에 틈이 생기고, 그 틈에서 다른 트랜잭션의 갱신이 사라진다. 해법은 계산을 데이터베이스 안으로 옮기는 것이다. `UPDATE accounts SET balance = balance + 10 WHERE id = 1`은 행 락 아래서 현재 값을 읽어 갱신하므로, 01장에서 본 것처럼 어떤 격리 수준에서도 갱신이 사라지지 않는다. 다만 PostgreSQL의 Repeatable Read와 Serializable에서는 동시 갱신이 `40001` 오류로 나타나므로 그 경우 아래에서 다룰 재시도가 필요하다.

조건이 붙은 갱신에서는 이 패턴이 더욱 강력해진다. 재고 차감을 "재고를 읽고 1 이상이면 차감"으로 쓰면 두 요청이 같은 재고를 읽고 모두 통과해 음수가 될 수 있다. 같은 로직을 조건부 갱신으로 쓰면 검사와 차감이 한 문장 안에서 원자적으로 일어난다.

```sql
CREATE TABLE stock (item_id integer PRIMARY KEY, qty integer NOT NULL);

UPDATE stock
SET qty = qty - 1
WHERE item_id = 42 AND qty >= 1;
-- 영향받은 행이 1이면 성공, 0이면 재고 부족이다
```

이 패턴의 핵심은 성공 여부를 별도의 `SELECT`가 아니라 영향받은 행 수로 판단한다는 점이다. 대부분의 드라이버가 `rowcount`나 `affected rows`를 돌려주므로 애플리케이션은 0일 때 재고 부족으로 처리하면 된다. 한계는 한 문장으로 표현되는 갱신에만 쓸 수 있다는 것이다. 여러 테이블에 걸친 판단이나 외부 계산이 끼어드는 로직은 다른 도구가 필요하다.

## 비관적 락: SELECT FOR UPDATE와 SKIP LOCKED

읽은 값을 애플리케이션에서 판단해야 한다면 읽는 시점부터 행을 잠가 상대가 끼어들지 못하게 하는 방법이 있다. `SELECT ... FOR UPDATE`는 조회한 행을 갱신할 것처럼 잠그고, 공식 문서에 따르면 다른 트랜잭션이 그 행을 갱신, 삭제, 잠금하려 하면 이 트랜잭션이 끝날 때까지 대기한다. Read Committed에서는 `FOR UPDATE`가 이미 다른 트랜잭션이 잡은 락을 만나면 기다린 뒤 갱신된 행을 잠그고 돌려준다. Repeatable Read와 Serializable에서는 사정이 다르다. PostgreSQL 문서에 따르면 `FOR UPDATE`도 트랜잭션 시작 시점에 커밋된 행만 찾으므로, 그 사이 다른 트랜잭션이 갱신해 커밋한 행을 만나면 `40001` 오류로 중단되어 재시도가 필요하다. 01장의 당직 의사 예제에서 당직자 행들을 `FOR UPDATE`로 읽는 방법이 이 패턴이다. 02장에서 설명했듯 이 잠금은 PostgreSQL에서 행을 수정해 표시하는 방식이므로 디스크 쓰기를 유발할 수 있다. 읽기가 흔적을 남기게 되는 셈이다.

비관적 락은 기다리는 것이 기본이지만 기다리지 않는 선택지도 있다. `NOWAIT`는 락을 얻을 수 없으면 즉시 오류를 내고, `SKIP LOCKED`는 잠긴 행을 건너뛴다. 문서는 `SKIP LOCKED`가 데이터의 일관되지 않은 뷰를 제공하므로 범용 용도에는 적합하지 않지만, 큐처럼 여러 소비자가 같은 테이블에서 일을 가져가는 경우 락 경합을 피하는 데 쓸 수 있다고 설명한다. 작업 큐가 이 패턴의 대표적인 사용처다. 소비자 여럿이 같은 첫 번째 작업을 두고 줄을 서는 대신, 각자 다른 작업을 가져간다.

```sql
CREATE TABLE jobs (id bigserial PRIMARY KEY, status text NOT NULL DEFAULT 'pending');

-- 대기 중인 작업 하나를 가져와 실행 중으로 표시한다. 여러 워커가 동시에 실행해도 서로 다른 행을 얻는다.
WITH next AS (
    SELECT id
    FROM jobs
    WHERE status = 'pending'
    ORDER BY id
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
UPDATE jobs
SET status = 'running'
FROM next
WHERE jobs.id = next.id
RETURNING jobs.id;
```

이 쿼리는 PostgreSQL 문법이다. MySQL 8.4 문서도 `SELECT ... FOR UPDATE`와 `FOR SHARE`에서 `NOWAIT`와 `SKIP LOCKED`를 지원하며, 잠긴 행을 건너뛰면 일관되지 않은 뷰가 돌아오므로 큐처럼 여러 세션이 접근하는 테이블에 한정해 쓰라고 설명한다. 다만 `UPDATE ... FROM` 문법은 다르므로 MySQL에서는 두 단계로 나누어 써야 한다. 주의할 점이 두 가지 있다. 문서는 `LIMIT`이 있으면 요구한 행 수를 채운 시점에 잠금을 멈추지만 `OFFSET`으로 건너뛴 행도 잠긴다고 설명한다. 또 Read Committed에서 `ORDER BY`와 잠금 절을 함께 쓰면 정렬이 먼저 적용된 뒤 잠금을 기다리다 행이 정렬 순서와 어긋나게 반환될 수 있다고 문서가 경고한다. 엄격한 순서 보장이 필요한 큐라면 이 쿼리의 가정이 깨지지 않는지 따져야 한다.

비관적 락의 비용은 03장에서 다뤘다. 락을 쥔 시간만큼 다른 트랜잭션이 대기하고, 락을 거는 순서가 코드마다 다르면 데드락이 생긴다. 트랜잭션을 짧게 유지하고 락 순서를 통일하는 것이 기본 방어책이다.

## 낙관적 락: 버전 컬럼으로 충돌을 감지한다

충돌이 드물다면 미리 잠그는 비용이 아깝다. <strong>낙관적 락(optimistic locking)</strong>은 잠그지 않고 읽은 뒤, 갱신하는 순간 "내가 읽은 때와 같은 상태인가"를 조건으로 검사한다. 행에 버전 컬럼을 두고, 갱신할 때 `WHERE id = ? AND version = ?`로 읽었던 버전을 요구하며 버전을 1 올린다. 그 사이 다른 트랜잭션이 갱신했다면 버전이 달라져 영향받은 행이 0이 되고, 애플리케이션은 이를 충돌로 판단해 처음부터 재시도한다. 앞서 본 조건부 갱신과 같은 원리이되 조건이 "재고가 충분한가"가 아니라 "읽은 때와 같은가"라는 점이 다르다.

다음 코드는 Python의 `sqlite3`로 이 세 가지를 비교한다. 읽고-계산하고-쓰기를 별도 트랜잭션으로 나눈 흔한 버그, 한 문장으로 합친 원자적 갱신, 버전 컬럼 낙관적 락을 차례로 실행한다. 구체적인 DBMS는 SQLite지만 세 패턴의 논리는 어떤 DBMS에서도 같다. 문장마다 자동 커밋되도록 `isolation_level=None`으로 연결하고, 두 연결 A와 B가 번갈아 실행되는 순서를 직접 지정해 경합을 재현한다.

```python
import os
import random
import sqlite3
import tempfile
import time

path = os.path.join(tempfile.mkdtemp(), "bank.db")


def connect():
    # isolation_level=None: 파이썬이 BEGIN을 자동으로 넣지 않으므로 문장마다 자동 커밋된다.
    return sqlite3.connect(path, timeout=0, isolation_level=None)


setup = connect()
setup.execute("PRAGMA journal_mode=WAL")
setup.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER, version INTEGER)")
setup.execute("INSERT INTO accounts VALUES (1, 100, 0)")

a, b = connect(), connect()


def balance(conn):
    return conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0]


print("[1] 읽고-계산하고-쓰기를 서로 다른 트랜잭션으로 실행하면")
ra, rb = balance(a), balance(b)                      # 둘 다 100을 읽는다
a.execute("UPDATE accounts SET balance = ? WHERE id = 1", (ra + 10,))
b.execute("UPDATE accounts SET balance = ? WHERE id = 1", (rb + 20,))
print("최종 잔액:", balance(setup), "(기대값 130)")

print("\n[2] 한 문장으로 합친 원자적 갱신")
setup.execute("UPDATE accounts SET balance = 100 WHERE id = 1")
a.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
b.execute("UPDATE accounts SET balance = balance + 20 WHERE id = 1")
print("최종 잔액:", balance(setup))


def add_with_version(conn, amount, interleave=None):
    """낙관적 락: 읽은 버전이 그대로일 때만 갱신하고, 아니면 처음부터 재시도한다."""
    for attempt in range(1, 6):
        bal, ver = conn.execute("SELECT balance, version FROM accounts WHERE id = 1").fetchone()
        if interleave and attempt == 1:
            interleave()                             # 다른 트랜잭션이 끼어드는 지점
        cur = conn.execute(
            "UPDATE accounts SET balance = ?, version = version + 1 WHERE id = 1 AND version = ?",
            (bal + amount, ver))
        if cur.rowcount == 1:
            return attempt
        time.sleep(random.uniform(0, 0.01) * attempt)  # 지터가 있는 백오프
    raise RuntimeError("재시도 한도 초과")


print("\n[3] 버전 컬럼을 이용한 낙관적 락")
setup.execute("UPDATE accounts SET balance = 100, version = 0 WHERE id = 1")
tries_b = add_with_version(
    b, 20, interleave=lambda: add_with_version(a, 10))   # B가 읽은 직후 A가 먼저 커밋
print("B의 시도 횟수:", tries_b)
print("최종 잔액:", balance(setup), "(기대값 130)")
```

이 코드를 Python 3으로 실행하면 다음 출력이 나온다.

```text
[1] 읽고-계산하고-쓰기를 서로 다른 트랜잭션으로 실행하면
최종 잔액: 120 (기대값 130)

[2] 한 문장으로 합친 원자적 갱신
최종 잔액: 130

[3] 버전 컬럼을 이용한 낙관적 락
B의 시도 횟수: 2
최종 잔액: 130 (기대값 130)
```

첫 번째 결과가 lost update다. A의 +10이 B의 덮어쓰기로 사라져 130이 아닌 120이 되었다. 두 번째는 계산을 데이터베이스 안으로 옮겨 문제를 없앤다. 세 번째에서 B는 읽은 직후 A가 먼저 커밋해 버전이 바뀌었으므로 첫 시도의 갱신이 영향받은 행 0으로 실패하고, 재시도에서 새 값을 읽고 성공해 시도 횟수가 2가 된다. 두 번의 갱신이 모두 반영되어 130이 된다. 실패한 시도 사이에 지터를 둔 대기를 넣은 것은 여러 클라이언트가 동시에 재시도해 다시 충돌하는 것을 흩어 놓기 위해서다.

낙관적 락의 장점은 읽는 동안 락을 쥐지 않아 대기가 없다는 것이다. 사용자가 편집 화면을 열어 둔 채 몇 분씩 머무르는 웹 애플리케이션에서 특히 중요하다. 그 시간 동안 행 락을 쥘 수는 없기 때문이다. 한계는 충돌이 잦은 행에서 재시도가 폭증한다는 것이다. 같은 행을 모두가 갱신하는 카운터는 낙관적 락보다 원자적 `UPDATE`가 낫다. 또 낙관적 락은 같은 행에 대한 쓰기 충돌만 감지하므로 write skew처럼 서로 다른 행을 쓰는 경우에는 도움이 되지 않는다.

## 제약조건: 불변식을 스키마에 선언한다

격리 수준이나 락과 무관하게 가장 확실한 보호는 불변식을 데이터베이스가 직접 강제하게 하는 것이다. 애플리케이션이 "이미 있는지 확인하고 없으면 삽입"하는 코드는 확인과 삽입 사이의 틈에서 경합한다. 두 요청이 모두 없음을 확인하고 둘 다 삽입하면 중복이 생긴다. `UNIQUE` 제약조건은 이 틈을 닫는다. 두 번째 삽입이 위반으로 거부되기 때문이다. `CHECK` 제약조건은 행 하나의 값에 대한 불변식(`price > 0`)을 지킨다.

01장에서 잠글 행이 없어 `FOR UPDATE`가 통하지 않는다고 한 회의실 예약 같은 팬텀형 write skew에는 PostgreSQL의 <strong>배타 제약조건(exclusion constraint)</strong>이 알맞다. 문서는 배타 제약조건을 두 행을 지정한 연산자로 비교했을 때 적어도 하나는 거짓이나 널이 되어야 한다는 제약으로 정의하고, 제약조건에 지정한 인덱스가 자동으로 만들어진다고 설명한다. 같은 방, 겹치는 시간대를 막는 예약 테이블은 다음과 같이 정의한다.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE bookings (
    room_id integer   NOT NULL,
    during  tstzrange NOT NULL,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
```

이제 같은 `room_id`에서 시간 범위가 겹치는 두 번째 `INSERT`는 격리 수준과 상관없이 거부된다. 동시에 들어온 두 삽입이 서로를 보지 못해도 인덱스가 충돌을 검사하기 때문이다. 이 접근의 한계는 선언 가능한 불변식에만 적용된다는 것이다. "당직자는 최소 한 명"처럼 집계에 기반한 불변식은 제약조건으로 직접 표현하기 어렵다. 그런 경우에는 행 잠금이나 Serializable이 대안이다.

## 어드바이저리 락: 논리적 키를 잠근다

잠글 행이 없고 제약조건으로도 표현하기 어려운 경우를 위해 PostgreSQL은 <strong>어드바이저리 락(advisory lock)</strong>을 제공한다. 테이블의 행이 아니라 애플리케이션이 정한 숫자 키를 잠그는 락으로, 예를 들어 "사용자 123의 정산 작업"이라는 의미를 가진 키를 모든 코드가 같은 규칙으로 잠그기로 약속하는 방식이다. 공식 문서에 따르면 세션 수준 락은 명시적으로 풀거나 세션이 끝날 때까지 유지되고 트랜잭션 의미를 따르지 않아 롤백해도 락이 남는다. 트랜잭션 수준 락은 트랜잭션이 끝나면 자동으로 해제되며 명시적 해제가 없다. 실수로 락이 새는 것을 막으려면 트랜잭션 수준 락이 안전하다.

```sql
BEGIN;
SELECT pg_advisory_xact_lock(hashtext('settlement:user:123'));
-- 같은 키를 잠근 다른 트랜잭션은 여기서 대기한다
-- ... 정산 로직 ...
COMMIT;   -- 락이 자동으로 풀린다
```

이 락은 어디까지나 규약이다. 데이터베이스는 키의 의미를 모르므로, 같은 자원을 건드리는 모든 코드 경로가 같은 키로 락을 잡을 때만 효과가 있다. 문서는 어드바이저리 락이 일반 락과 같은 공유 메모리 풀에 저장되며 `max_locks_per_transaction`과 `max_connections` 설정이 그 크기를 정해 서버가 허용하는 락 수에 상한이 있다고 설명한다. 또 `SELECT pg_advisory_lock(id) FROM foo WHERE id > 12345 LIMIT 100`처럼 쓰면 `LIMIT`이 락 함수 실행보다 먼저 적용된다는 보장이 없어 의도보다 많은 락이 잡힐 수 있다고 경고한다. MySQL에는 비슷한 용도로 `GET_LOCK()` 함수가 있다. 문서에 따르면 이 락은 이름으로 거는 서버 전체의 협력적 락이며, 트랜잭션이 커밋하거나 롤백해도 해제되지 않고 `RELEASE_LOCK()`을 호출하거나 세션이 끝나야 풀린다. 그러므로 PostgreSQL의 트랜잭션 수준 락과 달리 해제를 코드가 직접 책임져야 한다.

## 재시도와 멱등성: 충돌을 안전하게 되풀이한다

앞의 모든 패턴은 충돌을 중단이나 실패로 알려 주고 재시도로 마무리된다. 재시도 설계의 기본 규칙은 네 가지다. 첫째, 재시도할 오류를 구분한다. 직렬화 실패(`40001`), PostgreSQL의 데드락(`40P01`), MySQL의 데드락(1213)은 트랜잭션을 다시 실행하면 성공할 수 있는 오류이고, 낙관적 락의 영향받은 행 0도 같은 부류다. PostgreSQL 문서는 `40001`을 무조건 재시도해도 좋은 오류로, `40P01`은 재시도가 권장되는 오류로 구분한다. 유일성 위반(`23505`)과 배타 제약 위반(`23P01`)은 경우에 따라 재시도가 적절하다고 설명한다. 저장된 키를 확인하고 새 기본키 값을 고르는 코드가 동시에 같은 값을 골라 생긴 유일성 위반은 실질적으로 직렬화 실패이지만, 서버가 읽기와 삽입 값의 연결을 알 수 없어 그렇게 알리지 못하기 때문이다. 반면 같은 입력이 되풀이해서 만드는 위반이나 문법 오류는 다시 해도 같은 결과이므로, 이 두 코드를 재시도할 때는 일시적인 경합인지를 따져 보는 주의가 필요하다. 둘째, 재시도 단위는 개별 문장이 아니라 트랜잭션 전체이며, 이전 시도에서 읽은 값을 재사용하지 말고 처음부터 다시 읽는다. PostgreSQL 문서도 직렬화 실패를 겪는 애플리케이션이 [트랜잭션을 재시도할 준비](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html)를 해야 한다고 설명한다. 셋째, 지터를 둔 백오프와 횟수 상한을 둔다. 앞의 낙관적 락 코드가 이 형태다. 넷째, 재시도되어도 결과가 같도록 요청을 멱등하게 만든다.


재시도가 안전하려면 같은 요청을 두 번 실행해도 결과가 한 번 실행한 것과 같아야 한다. 네트워크 타임아웃으로 클라이언트가 응답을 못 받고 재전송하는 상황도 같은 문제이므로, 재시도 설계의 마지막 조각은 <strong>멱등성(idempotency)</strong>이다. 가장 흔한 방법은 요청마다 클라이언트가 만든 고유한 멱등성 키를 받아 `UNIQUE` 제약조건으로 중복 처리를 막는 것이다.

```sql
CREATE TABLE payments (
    idempotency_key text PRIMARY KEY,
    amount          numeric NOT NULL,
    response        text,                -- 처음 처리한 결과(예: 승인 번호)
    created_at      timestamptz NOT NULL DEFAULT now()
);

INSERT INTO payments (idempotency_key, amount)
VALUES ('req-7f3a', 100)
ON CONFLICT (idempotency_key) DO NOTHING;
-- 영향받은 행이 1이면 처음 처리, 0이면 이미 처리된 요청이다

-- 처음 처리라면 같은 트랜잭션에서 결과를 기록한다
UPDATE payments SET response = 'approved:12345' WHERE idempotency_key = 'req-7f3a';

-- 중복 요청이라면 저장된 결과를 조회해 그대로 돌려준다
SELECT response FROM payments WHERE idempotency_key = 'req-7f3a';
```

이 패턴은 제약조건의 원리를 그대로 재활용한다. 같은 키로 동시에 들어온 두 요청은 기본키가 하나만 통과시키므로 정확히 한 번만 처리된다. 중복 요청에서는 저장된 `response`를 조회해 그대로 돌려주면 된다. 처음 요청이 아직 커밋되기 전이라면 결과가 정해질 때까지 중복 요청이 기다리거나 재시도해야 한다.

## 선택 지도

문제 유형에서 도구로 가는 대응을 표로 정리한다. 한 문제에 여러 도구를 겹쳐 쓰기도 한다.

| 문제 | 해당 이상 현상 | 우선 고려할 도구 | 비용 | 한계 |
|---|---|---|---|---|
| 카운터·잔액 갱신이 사라진다 | Lost Update | 원자적 `UPDATE` | 거의 없음 | 한 문장으로 표현되는 갱신만 가능 |
| 재고·한도가 음수가 된다 | Lost Update | 조건부 `UPDATE ... WHERE qty >= n` | 거의 없음 | 영향받은 행 수 확인 필요 |
| 읽은 값으로 같은 행을 판단해 갱신한다 | Lost Update | `SELECT FOR UPDATE` 또는 낙관적 락 | 대기 또는 재시도 | 충돌이 잦으면 대기·재시도 증가 |
| 작업 큐에서 여러 워커가 일을 가져간다 | 경합 | `FOR UPDATE SKIP LOCKED` | 낮음 | 일관되지 않은 뷰, 순서 보장 약함 |
| 중복 삽입을 막는다 | Phantom형 | `UNIQUE` 제약조건 | 인덱스 유지 | 선언 가능한 키에 한정 |
| 겹치는 구간 예약을 막는다 | Phantom형 write skew | 배타 제약조건 | 인덱스 유지 | PostgreSQL 전용 |
| 여러 행의 집계 불변식(최소 당직자) | Write Skew | 읽은 행 잠금 또는 Serializable | 대기 또는 재시도 | 행이 없으면 잠금 불가 |
| 논리적 자원 단위의 임계구역 | 경합 | 어드바이저리 락 | 낮음 | 모든 코드가 키 규약을 지켜야 함 |
| 재시도·재전송이 중복 처리된다 | 중복 | 멱등성 키 | 키 저장 | 클라이언트 협조 필요 |

## 흔한 오개념

**"낙관적 락은 락이 없으니 항상 더 빠르고 안전하다."** 낙관적 락은 충돌이 드물다는 가정 위에서만 이득이다. 충돌이 잦으면 실패한 시도의 계산이 모두 낭비되고 재시도가 쌓인다. 또 같은 행에 대한 충돌만 감지하므로 write skew에는 효과가 없다.

**"먼저 확인하고 삽입하면 중복을 막을 수 있다."** 확인과 삽입 사이의 틈에서 다른 트랜잭션이 끼어들 수 있다. 중복 방지는 애플리케이션의 사전 확인이 아니라 `UNIQUE` 제약조건이 해야 하고, 사전 확인은 친절한 오류 메시지를 위한 보조 수단일 뿐이다.

**"`SELECT FOR UPDATE`를 모든 조회에 붙이면 안전하다."** 모든 읽기에 락을 걸면 동시성이 크게 떨어지고 데드락이 늘어난다. 락은 이후 갱신의 근거가 되는 읽기에만 걸어야 한다.

**"`SKIP LOCKED`는 일반 조회에서도 쓸 수 있다."** 문서가 명시하듯 잠긴 행을 건너뛰면 데이터의 일관되지 않은 뷰가 돌아오므로 큐 같은 특수 용도에 한정해야 한다. 집계나 보고서에 쓰면 결과가 조용히 틀린다.

**"재시도는 오류를 숨기는 임시방편이다."** 락 기반이든 낙관적이든 Serializable이든 충돌을 중단과 재시도로 해소하는 것이 동시성 제어의 정상 동작이다. 문제는 재시도가 아니라 재시도 단위가 잘못되었거나 부작용이 멱등하지 않은 설계다.

## 이 장을 읽은 후 달성해야 할 목표

이 장을 읽은 후에는 다음을 할 수 있어야 한다. 동시성 버그를 보고 그것이 lost update인지 write skew인지 팬텀형인지 판정하고, 그 현상을 막는 가장 싼 도구를 고를 수 있다. 읽고-계산하고-쓰기를 원자적 `UPDATE`나 조건부 갱신으로 바꿀 수 있다. `SELECT FOR UPDATE`, `NOWAIT`, `SKIP LOCKED`의 차이와 큐에서의 쓰임을 설명할 수 있다. 버전 컬럼 낙관적 락을 구현하고 충돌이 잦은 경우의 한계를 설명할 수 있다. 제약조건과 어드바이저리 락이 어떤 경우에 알맞은지 구분하고, 멱등성 키로 재시도를 안전하게 만들 수 있다.

## 다음 장에서는

06장에서는 트랜잭션의 경계가 한 데이터베이스를 넘어설 때를 다룬다. 두 개 이상의 데이터베이스나 서비스에 걸친 일관성을 위해 2단계 커밋(2PC)이 어떻게 동작하고 왜 막히는지, 마이크로서비스에서는 사가(Saga)와 아웃박스 패턴이 어떻게 대안이 되는지, 구글 스패너와 퍼컬레이터 같은 분산 트랜잭션 시스템이 격리 수준을 어떻게 구현하는지를 설명한다. 이 장의 멱등성과 재시도는 분산 환경에서 훨씬 더 중요해진다.

## 참고 자료

- [PostgreSQL Documentation: SELECT, The Locking Clause](https://www.postgresql.org/docs/current/sql-select.html) — `FOR UPDATE`, `NOWAIT`, `SKIP LOCKED`와 `LIMIT`·`ORDER BY` 주의사항
- [MySQL 8.4 Reference Manual: Locking Reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html) — `NOWAIT`와 `SKIP LOCKED`
- [MySQL 8.4 Reference Manual: Locking Functions](https://dev.mysql.com/doc/refman/8.4/en/locking-functions.html) — `GET_LOCK()`과 `RELEASE_LOCK()`
- [PostgreSQL Documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) — 행 수준 락, 데드락, 어드바이저리 락
- [PostgreSQL Documentation: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) — `UNIQUE`, `CHECK`, 배타 제약조건
- [PostgreSQL Documentation: Serialization Failure Handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html) — 직렬화 실패 시 재시도
- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) — 이 장의 실행 예제가 쓰는 표준 라이브러리 모듈
- [Designing Data-Intensive Applications](https://dataintensive.net/) — 7장 Transactions: write skew의 해결책으로 소개되는 패턴들
