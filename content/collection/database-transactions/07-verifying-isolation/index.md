---
collection_order: 7
date: 2026-10-02T01:20:00+09:00
lastmod: 2026-10-12T00:10:00+09:00
draft: true
title: "[Database] 07. 격리 수준 검증: 재현 테스트, Hermitage, Elle"
slug: verifying-isolation-levels
description: "문서와 블로그의 격리 수준 주장을 직접 확인하는 방법을 다룹니다. 두 세션의 인터리빙을 결정론적으로 재현하는 테스트 하네스를 SQLite로 실행해 보고, Hermitage와 Elle 같은 도구와 DBMS 이전 점검표를 정리합니다."
tags:
  - Database(데이터베이스)
  - Transaction(트랜잭션)
  - SQL(Structured Query Language)
  - PostgreSQL
  - MySQL
  - Oracle
  - SQL-Server
  - SQLite
  - Isolation-Level(격리수준)
  - Snapshot-Isolation
  - Serializable
  - Write-Skew
  - Lost-Update
  - Non-Repeatable-Read
  - Phantom-Read
  - Dirty-Read
  - MVCC
  - Concurrency(동시성)
  - Lock(락)
  - Testing(테스트)
  - Test-Automation(테스트자동화)
  - Python
  - Backend(백엔드)
  - Data-Integrity(데이터무결성)
  - Software-Engineering(소프트웨어공학)
  - Best-Practices
  - Comparison(비교)
  - Troubleshooting(트러블슈팅)
  - Computer-Science(컴퓨터과학)
  - Deep-Dive
  - Advanced
image: "wordcloud.png"
---

이 시리즈의 앞 여섯 장은 공식 문서와 논문을 근거로 격리 수준의 동작을 설명했다. 그런데 문서도, 논문도, 블로그도, 이 시리즈도 틀릴 수 있다. 문서는 버전이 바뀌면 낡고, 같은 DBMS라도 설정 하나로 동작이 바뀌며, 요약 과정에서 조건이 빠지기도 한다. 동시성 보장처럼 틀렸을 때 비용이 큰 주제에서는 읽는 데서 멈추지 말고 직접 재현해 보는 습관이 필요하다. 이 장은 그 방법을 다룬다. 두 세션의 실행 순서를 정해 놓고 결과를 기록하는 테스트 하네스를 직접 만들어 실행하고, 같은 시나리오가 설정에 따라 다른 결과를 낸다는 것을 실제 출력으로 확인한다.

## 이 장을 읽기 전에

[01장](/post/database-transactions/isolation-levels-and-anomalies/)의 이상 현상 어휘와 [02장](/post/database-transactions/snapshot-isolation-and-mvcc/), [03장](/post/database-transactions/lock-based-isolation/)의 구현 설명을 알고 있어야 실행 결과를 해석할 수 있다. Python의 기본 사용법은 알고 있다고 가정한다.

이 장의 깊이는 중급이다. 하네스는 표준 라이브러리만 쓰고 SQLite로 실행하므로 별도 데이터베이스 서버가 필요 없다. 대규모 무작위 워크로드로 격리 위반을 찾는 시스템 시험(Jepsen 같은 환경 구성, 네트워크 분할 주입)은 개념만 소개하고 구축 방법은 범위 밖이다.

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 처음 배우는 독자 | "왜 직접 검증하는가", "실행 결과 읽기" | 이상 현상을 순서가 정해진 스크립트로 재현한다 |
| 실무 개발자 | "다른 DBMS에 적용하기", "DBMS 이전 점검표" | 마이그레이션과 업그레이드 때 쓸 회귀 테스트를 만든다 |
| 심화 독자 | "기존 도구들", "한눈에 보기" | 수동 시나리오와 그래프 기반 검사기의 역할을 구분한다 |

## 왜 직접 검증하는가

격리 수준에 대한 지식은 세 가지 이유로 낡거나 어긋난다. 첫째, 같은 이름이 DBMS마다 다르다. 01장에서 본 것처럼 Repeatable Read는 PostgreSQL에서는 스냅샷 격리이고 InnoDB에서는 일관 읽기와 갭 락의 조합이다. 둘째, 같은 DBMS도 설정으로 동작이 바뀐다. SQL Server의 Read Committed는 `READ_COMMITTED_SNAPSHOT` 옵션이 꺼져 있으면 락 기반이고 켜져 있으면 행 버전 기반이며, 클라우드 관리형 서비스는 기본값이 다를 수 있다. 셋째, 버전이 바뀐다. 드라이버나 프록시, 커넥션 풀이 트랜잭션 경계를 바꾸는 경우도 있다. 그러므로 중요한 불변식을 지키는 코드가 있다면, 그 코드가 의존하는 보장이 지금 환경에서 성립하는지를 테스트로 남겨 두는 것이 좋다.

동시성 이상 현상은 스레드 타이밍에 의존하는 방식으로는 신뢰성 있게 재현되지 않는다. 두 스레드를 동시에 돌리고 "가끔 실패하는지" 보는 테스트는 실패하지 않았다는 사실이 안전의 증거가 되지 못한다. 이상 현상은 본질적으로 특정한 연산 순서이므로, 순서를 코드로 못 박아 결정론적으로 재현해야 한다. "세션 A가 읽고, 세션 B가 읽고, A가 쓰고, A가 커밋하고, B가 쓴다"라는 시나리오를 단계 목록으로 표현하고, 각 단계를 정해진 순서로 실행하며 결과와 오류를 기록한다.

## 테스트 하네스 만들기

하네스의 핵심은 세 가지다. 세션마다 별도의 연결을 만들어 단계가 번갈아 실행되게 한다. 락 대기 때문에 테스트가 멈추지 않도록 대기 시간을 0으로 두어 즉시 오류가 되게 한다. 실패한 시나리오가 열어 둔 트랜잭션을 마지막에 정리해 다음 시나리오에 영향을 주지 않게 한다. 다음 코드는 Python 표준 라이브러리의 `sqlite3`로 만든 하네스이며, 02장부터 써 온 당직 의사 예제와 반복 불가능한 읽기 시나리오를 두 가지 저널 모드에서 실행한다.

```python
import os
import sqlite3
import tempfile


def make_db(mode):
    path = os.path.join(tempfile.mkdtemp(), "t.db")
    s = sqlite3.connect(path, timeout=0, isolation_level=None)
    s.execute(f"PRAGMA journal_mode={mode}")
    s.execute("CREATE TABLE doctors (name TEXT PRIMARY KEY, on_call INTEGER)")
    s.execute("INSERT INTO doctors VALUES ('alice', 1), ('bob', 1)")
    s.close()
    return path


def run(path, steps):
    """steps: (세션, SQL) 목록을 정해진 순서로 실행하고 결과·오류를 기록한다."""
    conns, log = {}, []
    for who, sql in steps:
        conn = conns.setdefault(who, sqlite3.connect(path, timeout=0, isolation_level=None))
        try:
            rows = conn.execute(sql).fetchall()
            log.append((who, sql, rows if rows else "ok"))
        except sqlite3.OperationalError as e:
            log.append((who, sql, f"오류 {e.sqlite_errorname}"))
    for conn in conns.values():          # 실패해서 열려 있는 트랜잭션은 정리한다
        if conn.in_transaction:
            conn.execute("ROLLBACK")
    final = sqlite3.connect(path).execute("SELECT SUM(on_call) FROM doctors").fetchone()[0]
    return log, final


COUNT = "SELECT SUM(on_call) FROM doctors"
ALICE_OFF = "UPDATE doctors SET on_call=0 WHERE name='alice'"
BOB_OFF = "UPDATE doctors SET on_call=0 WHERE name='bob'"
SCENARIOS = {
    "write skew, 쓰기가 겹침": [("A", "BEGIN"), ("B", "BEGIN"), ("A", COUNT), ("B", COUNT),
                              ("A", ALICE_OFF), ("B", BOB_OFF), ("A", "COMMIT"), ("B", "COMMIT")],
    "write skew, A가 먼저 커밋": [("A", "BEGIN"), ("B", "BEGIN"), ("A", COUNT), ("B", COUNT),
                              ("A", ALICE_OFF), ("A", "COMMIT"), ("B", BOB_OFF), ("B", "COMMIT")],
    "반복 불가능한 읽기": [("B", "BEGIN"), ("B", COUNT), ("A", ALICE_OFF), ("B", COUNT), ("B", "COMMIT")],
}

for mode in ("DELETE", "WAL"):
    print(f"=== journal_mode={mode}")
    for name, steps in SCENARIOS.items():
        log, final = run(make_db(mode), steps)
        errors = [f"{w}:{sql.split()[0]} -> {r}" for w, sql, r in log if str(r).startswith("오류")]
        reads = [r[0][0] for w, sql, r in log if sql == COUNT and w == "B"]
        print(f"  [{name}] B의 읽기 {reads}, 오류 {errors or '없음'}, 최종 당직자 수 {final}")
```

이 코드를 Python 3.11 이상에서 실행하면 다음 출력이 나온다. 오류 이름을 읽는 `sqlite_errorname` 속성이 3.11에 추가되었으므로 그보다 낮은 버전에서는 이 부분을 수정해야 한다.

```text
=== journal_mode=DELETE
  [write skew, 쓰기가 겹침] B의 읽기 [2], 오류 ['B:UPDATE -> 오류 SQLITE_BUSY', 'A:COMMIT -> 오류 SQLITE_BUSY'], 최종 당직자 수 2
  [write skew, A가 먼저 커밋] B의 읽기 [2], 오류 ['A:COMMIT -> 오류 SQLITE_BUSY', 'B:UPDATE -> 오류 SQLITE_BUSY'], 최종 당직자 수 2
  [반복 불가능한 읽기] B의 읽기 [2, 2], 오류 ['A:UPDATE -> 오류 SQLITE_BUSY'], 최종 당직자 수 2
=== journal_mode=WAL
  [write skew, 쓰기가 겹침] B의 읽기 [2], 오류 ['B:UPDATE -> 오류 SQLITE_BUSY'], 최종 당직자 수 1
  [write skew, A가 먼저 커밋] B의 읽기 [2], 오류 ['B:UPDATE -> 오류 SQLITE_BUSY_SNAPSHOT'], 최종 당직자 수 1
  [반복 불가능한 읽기] B의 읽기 [2, 2], 오류 없음, 최종 당직자 수 1
```

## 실행 결과 읽기

SQLite 공식 문서는 공유 캐시와 `read_uncommitted`를 함께 쓰는 경우를 제외하면 SQLite의 모든 트랜잭션이 직렬 가능(serializable) 격리를 보인다고 설명한다. 한 번에 작성자는 하나뿐이라는 직렬화된 쓰기가 그 방법이다. 따라서 이 하네스에서 어느 모드든 write skew가 일어나지 않을 것이라고 예측할 수 있고, 실제로 최종 당직자 수는 2 또는 1이다. 불변식은 지켜졌다. 흥미로운 것은 불변식이 지켜지는 모양이 모드마다 다르다는 점이다.

롤백 저널 모드(`DELETE`)에서는 쓰기가 겹치는 시나리오에서 B의 `UPDATE`가 `SQLITE_BUSY`로 실패하고 A의 `COMMIT`도 `SQLITE_BUSY`로 실패한다. B가 읽으면서 공유 락을 쥐고 있어 A가 커밋에 필요한 락을 얻지 못한 것이다. 두 트랜잭션이 서로를 막는 이 모양은 03장의 락 기반 Serializable과 같은 계열이다. 읽기가 락이라는 흔적을 남기므로 write skew는 서로를 막는 실패로 바뀐다. 최종 당직자 수가 2인 것은 A의 커밋이 끝내 성공하지 못해 아무 변경도 반영되지 않았기 때문이다.

WAL 모드에서는 모양이 달라진다. 쓰기가 겹치는 시나리오에서는 A가 쓰기 락을 쥐고 있으므로 B의 `UPDATE`가 `SQLITE_BUSY`로 실패하고 A는 정상 커밋되어 최종 값이 1이 된다. A가 먼저 커밋하는 시나리오에서는 B의 `UPDATE`가 `SQLITE_BUSY_SNAPSHOT`으로 실패한다. 문서의 설명대로 B가 보던 스냅샷이 더는 최신 버전이 아니어서 읽기 트랜잭션을 쓰기 트랜잭션으로 승격하는 시도가 실패한 것이다. 이는 02장에서 본 first-updater-wins와 닮았지만, 충돌 판정의 단위가 행이 아니라 데이터베이스 전체라는 점이 다르다. 그래서 B가 건드리려는 행이 A가 바꾼 행과 달라도 실패한다. 스냅샷 격리의 모양을 하되 write skew가 불가능한 이유가 여기 있다. SQLite는 같은 행이 아니라 어떤 행이든 스냅샷 이후 데이터베이스가 바뀌었으면 쓰기를 거부하는, 훨씬 보수적인 충돌 정의를 쓴다.

마지막 시나리오인 반복 불가능한 읽기에서는 두 모드가 모두 B의 두 번 읽기가 `[2, 2]`로 같다. 값만 보면 같지만 이유는 정반대다. 롤백 저널 모드에서는 B의 읽기가 락을 쥐고 있어 A의 `UPDATE`가 `SQLITE_BUSY`로 아예 실행되지 못했고 최종 값도 2다. WAL 모드에서는 A의 변경이 정상 커밋되어 최종 값이 1이지만, B는 읽기 시작 시점의 스냅샷을 계속 보므로 두 번 모두 2를 읽는다. 문서는 WAL 모드에서 읽기 트랜잭션이 시작 시점 스냅샷을 계속 본다고 설명한다. 이 결과는 하네스가 읽은 값만이 아니라 오류와 최종 상태까지 함께 기록해야 하는 이유를 보여 준다. 읽은 값만 비교했다면 두 모드가 같은 보장을 한다고 잘못 결론 내렸을 것이다.

이 실험이 주는 교훈은 구체적이다. 같은 엔진이라도 설정 하나(`journal_mode`)가 실패의 모양을 바꾼다. 어느 모드에서든 애플리케이션은 `SQLITE_BUSY` 계열 오류를 재시도할 수 있어야 한다. SQLite 문서는 쓰기를 할 트랜잭션이라면 `BEGIN IMMEDIATE`로 시작해 처음부터 쓰기 락을 얻으라고 권고하며, 이렇게 하면 이후 해당 트랜잭션의 어떤 연산도 `SQLITE_BUSY`로 실패하지 않는다고 설명한다. 05장에서 본 "읽고 나서 쓸 트랜잭션은 시작 시점에 의도를 선언한다"는 비관적 락의 SQLite판이다.

## 다른 DBMS에 적용하기

하네스를 PostgreSQL이나 MySQL에 적용하려면 연결을 만드는 부분과 오류 처리만 바꾸면 된다. 단, 하나의 중요한 차이가 있다. SQLite는 `timeout=0`이면 락을 만났을 때 즉시 실패하지만, PostgreSQL과 MySQL의 세션은 기본적으로 락을 기다린다. 한 스크립트에서 단계를 순서대로 실행하는 하네스는 대기 중인 단계에서 그대로 멈추게 된다. 이를 해결하는 단순한 방법은 락 대기에 상한을 두어 대기를 실패로 바꾸는 것이다. PostgreSQL에서는 세션에 `lock_timeout`을 설정하면 되고, 오류는 `lock_not_available`(SQLSTATE `55P03`)로 나온다. 다음은 PostgreSQL용 변형의 골격이다. 이 골격은 앞의 하네스와 같은 단계 목록을 받아 실행하는 형태로 작성한 것으로, PostgreSQL 서버에서 실행해 보지는 않았다.

```python
import psycopg
from psycopg import errors, pq


def run_pg(conninfo, steps):
    """steps: (세션, SQL) 목록. 락 대기는 300ms 뒤 실패로 기록한다."""
    conns, log = {}, []
    for who, sql in steps:
        if who not in conns:
            conn = psycopg.connect(conninfo, autocommit=True)  # BEGIN/COMMIT은 단계로 직접 실행
            conn.execute("SET lock_timeout = '300ms'")
            conns[who] = conn
        try:
            cur = conns[who].execute(sql)
            log.append((who, sql, cur.fetchall() if cur.description else "ok"))
        except errors.SerializationFailure:
            log.append((who, sql, "오류 40001"))
        except errors.LockNotAvailable:
            log.append((who, sql, "오류 55P03"))
    for conn in conns.values():          # 실패해서 열려 있는 트랜잭션은 정리하고 연결을 닫는다
        if conn.info.transaction_status != pq.TransactionStatus.IDLE:
            conn.execute("ROLLBACK")
        conn.close()
    return log
```

이 골격으로 시나리오 단계의 첫 줄만 `BEGIN ISOLATION LEVEL REPEATABLE READ`나 `BEGIN ISOLATION LEVEL SERIALIZABLE`로 바꿔 가며 같은 시나리오를 돌리면, 01장과 04장의 주장을 직접 확인할 수 있다. 예컨대 Repeatable Read에서는 write skew 시나리오의 두 `COMMIT`이 모두 성공해야 하고, Serializable에서는 둘 중 하나가 `40001`로 실패해야 한다. 실패하는 단계가 시나리오에 따라 `UPDATE`일 수도 `COMMIT`일 수도 있으므로 하네스는 단계별 결과를 모두 기록해야 한다. 이때 결과가 문서와 다르면 이 시리즈나 문서가 아니라 먼저 자신의 시나리오 순서와 격리 수준 설정을 의심해야 한다. 가장 흔한 실수는 `BEGIN`을 빠뜨려 각 문장이 자동 커밋으로 실행되는 것이다.

## 기존 도구들

직접 만든 하네스는 소수의 시나리오에는 충분하지만, 체계적인 검증에는 이미 만들어진 도구가 있다. **Hermitage**는 Martin Kleppmann이 『Designing Data-Intensive Applications』의 배경 연구로 만든 프로젝트로, 여러 데이터베이스가 격리 수준에서 실제로 어떻게 동작하는지 테스트 시나리오로 문서화한다. 더티 리드, lost update, 팬텀, write skew 같은 이상 현상을 PostgreSQL, MySQL, Oracle, SQL Server를 비롯한 여러 시스템에서 시험하고, 결과 표에서 write skew(G2-item)와 술어 기반 write skew(G2)를 구분해 보여 준다. 이 시리즈의 01장 표를 자신의 DBMS 버전에서 점검할 때 가장 먼저 참고할 곳이다.

수동으로 쓴 시나리오는 사람이 생각해 낸 이상 현상만 검사한다. **Elle**은 Kyle Kingsbury와 Peter Alvaro의 논문 「Elle: Inferring Isolation Anomalies from Experimental Observations」(2020)에서 소개된 접근으로, 반대 방향을 택한다. 전략적으로 설계한 무작위 워크로드를 데이터베이스에 실행하고, 관찰된 읽기와 쓰기에서 트랜잭션 사이의 의존성 그래프를 추론해, 그래프의 사이클로 이상 현상을 찾아내고 그 이유를 설명한다. 01장에서 소개한 Adya의 의존성 그래프 정의를 실제 시스템의 실행 기록에 적용한 셈이다. 논문 초록은 이 접근이 건전하고, 효율적이며, 실제 데이터베이스의 격리 위반을 찾아내는 데 효과적이라고 주장한다. Jepsen의 [일관성 모델 지도](https://jepsen.io/consistency)는 이런 검사가 확인하는 격리 수준과 일관성 모델의 관계를 한 장으로 보여 준다.

| 도구 | 방식 | 강점 | 적합한 용도 |
|---|---|---|---|
| 직접 만든 하네스 | 사람이 쓴 인터리빙 시나리오를 결정론적으로 실행 | 우리 서비스의 불변식에 맞춘 시나리오를 만들 수 있고 CI에 넣기 쉬움 | 우리 코드가 의존하는 보장의 회귀 테스트 |
| Hermitage | 표준적인 이상 현상 시나리오와 DBMS별 결과 표 | 학습과 비교, 주장의 빠른 확인 | DBMS 선정과 이전 시 사전 조사 |
| Elle·Jepsen | 무작위 워크로드와 그래프 사이클 추론 | 사람이 생각 못 한 이상까지 대규모로 탐색 | DBMS나 분산 시스템 자체의 격리 보장 시험 |

## DBMS 이전과 업그레이드 점검표

DBMS를 바꾸거나 설정을 바꿀 때는 다음 항목을 점검한다. 각 항목의 이유는 표의 근거 장에서 다뤘고, 값은 반드시 사용 중인 버전의 문서와 테스트로 확인해야 한다.

| 점검 항목 | 확인할 것 | 근거 장 |
|---|---|---|
| 기본 격리 수준 | PostgreSQL·Oracle·SQL Server는 Read Committed, InnoDB는 Repeatable Read | 01장 |
| 수준 이름의 실제 구현 | Repeatable Read가 스냅샷인지 락 조합인지, Serializable이 락 기반인지 SSI인지 | 01·03·04장 |
| 스냅샷 시점 | 트랜잭션 시작인지, 첫 문장인지, 문장마다인지 | 02장 |
| DML이 보는 데이터 | 스냅샷인지 최신 커밋인지(InnoDB의 current read) | 02장 |
| 충돌 시 동작 | 대기, 오류, 덮어쓰기 중 무엇인지 | 02·03장 |
| 재시도 대상 오류 코드 | `40001`, `40P01`, MySQL 1213 등 | 03·04장 |
| 읽기 전용 구간의 처리 | `READ ONLY`, `DEFERRABLE`, 읽기 전용 복제본 | 04장 |
| 외부 부작용의 위치 | 커밋 이후로 미뤄졌는가, 멱등한가 | 04·05·06장 |

## 한눈에 보기: 세 가지 대표 이상 현상

세 가지 대표 이상 현상이 대표적인 구현에서 어떻게 나타나는지를 정리한다. 이 표는 공식 문서의 서술에서 도출한 것으로, 사용 중인 버전과 설정에서 이 장의 하네스나 Hermitage로 직접 확인하는 것을 전제로 한다. SQL Server는 Repeatable Read의 락 기반 동작을 기준으로 했다.

| 이상 현상 | PostgreSQL Repeatable Read | InnoDB Repeatable Read | SQL Server Repeatable Read(락 기반) |
|---|---|---|---|
| Lost Update(읽고-계산하고-쓰기) | 방지: `40001`로 중단 | 가능: DML이 최신 커밋을 덮어씀 | 읽은 행에 공유 락이 남아 상대 갱신과 충돌, 데드락으로 한쪽 중단 |
| Write Skew | 가능 | 가능 | 읽은 행이 락으로 보호되어 방지 |
| Phantom | 방지(스냅샷) | 읽기는 방지, DML은 최신 커밋을 봄 | 가능 |

## 흔한 오개념

**"테스트에서 한 번도 재현되지 않았으니 안전하다."** 동시성 이상은 타이밍에 의존하므로 재현이 안 된 것은 안전의 증거가 아니다. 안전은 구현 메커니즘에 대한 이해와 순서를 고정한 결정론적 시나리오로 확인한다.

**"스레드 두 개를 동시에 돌리고 `sleep`으로 순서를 맞추면 된다."** `sleep` 기반 동기화는 부하와 환경에 따라 순서가 깨져 간헐적으로 실패하는 테스트를 만든다. 단계 목록을 한 스레드에서 순서대로 실행하고, 세션을 별도의 연결로 분리하는 방식이 안정적이다.

**"결과 값이 같으면 보장도 같다."** 반복 불가능한 읽기 시나리오가 보여 준 것처럼 값은 같아도 한쪽은 변경이 막혔고 한쪽은 변경이 일어났지만 스냅샷이 가려 준 것이다. 오류와 최종 상태까지 기록하지 않으면 메커니즘의 차이를 놓친다.

**"문서에 있으니 검증은 필요 없다."** 문서는 특정 버전과 특정 설정의 서술이다. 중요한 보장에 의존하는 코드라면 그 보장을 회귀 테스트로 남겨 두어야 업그레이드와 설정 변경 때 조용한 변화를 잡을 수 있다.

## 이 장을 읽은 후 달성해야 할 목표

이 장을 읽은 후에는 다음을 할 수 있어야 한다. 이상 현상을 연산 순서의 목록으로 표현하고 결정론적으로 재현하는 하네스를 만들 수 있다. 실행 결과에서 읽은 값, 오류 이름, 최종 상태를 함께 해석해 같은 결과 뒤의 서로 다른 메커니즘을 구분할 수 있다. 같은 시나리오를 PostgreSQL이나 MySQL에서 돌리려면 무엇을 바꿔야 하는지, 락 대기 상한이 왜 필요한지 설명할 수 있다. Hermitage와 Elle이 서로 다른 목적의 도구임을 구분하고, DBMS 이전과 업그레이드 때 점검표를 사용할 수 있다.

## 참고 자료

- [Hermitage](https://github.com/ept/hermitage) — 여러 DBMS의 격리 수준별 이상 현상 시험 결과
- [Kingsbury, Alvaro, Elle: Inferring Isolation Anomalies from Experimental Observations](https://arxiv.org/abs/2003.10554) — 의존성 그래프 기반 격리 위반 검사기
- [Jepsen: Consistency Models](https://jepsen.io/consistency) — 일관성 모델과 격리 수준의 계층도
- [SQLite: Isolation In SQLite](https://www.sqlite.org/isolation.html) — SQLite의 직렬 가능 격리와 `SQLITE_BUSY_SNAPSHOT`, `BEGIN IMMEDIATE`
- [SQLite: Write-Ahead Logging](https://www.sqlite.org/wal.html) — WAL 모드의 읽기·쓰기 동시성과 읽기 스냅샷
- [SQLite: Result and Error Codes](https://www.sqlite.org/rescode.html) — `SQLITE_BUSY`와 `SQLITE_BUSY_SNAPSHOT`
- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) — 하네스가 쓰는 표준 라이브러리 모듈
- [PostgreSQL Documentation: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — PostgreSQL 격리 수준의 기준 문서
- [Designing Data-Intensive Applications](https://dataintensive.net/) — Hermitage의 배경이 된 7장 Transactions
