---
title: "[UnitTesting] 10. 데이터베이스 테스트하기"
description: "관계형 데이터베이스는 가장 흔한 프로세스 외부 의존성입니다. 인메모리 대체가 위험한 이유, 테스트 간 데이터 격리 전략(트랜잭션 롤백), 스키마 마이그레이션과 테스트를 함께 유지하는 아주 구체적인 실무 방법을 다룹니다."
date: 2026-07-16
lastmod: 2026-07-16
collection_order: 10
draft: false
image: "wordcloud.png"
tags:
  - Testing(테스트)
  - Database(데이터베이스)
  - Docker
  - CI-CD(Continuous Integration/Continuous Deployment)
  - pytest
  - Code-Quality(코드품질)
  - Best-Practices
  - Migration(마이그레이션)
  - Software-Architecture(소프트웨어아키텍처)
  - Reliability
  - Performance(성능)
  - Error-Handling(에러처리)
  - Maintainability
  - 단위테스트
  - 통합테스트
  - 관계형데이터베이스
  - 테스트격리
  - 트랜잭션롤백
  - 스키마마이그레이션
  - 인메모리DB
  - Coupling(결합도)
  - Debugging(디버깅)
  - Documentation(문서화)
  - 데이터베이스컨테이너
  - System-Design
---

# 10. 데이터베이스 테스트하기

08–09편에서 통합 테스트의 역할과 목의 배치 기준을 다뤘습니다. 실무에서 가장 흔한 프로세스 외부 의존성은 관계형 데이터베이스입니다. 이 편은 데이터베이스를 포함한 테스트를 안전하고 빠르게 유지하는 구체적인 방법을 다룹니다.

## 학습 목표

- 인메모리 데이터베이스로 실제 DB를 대체할 때의 위험을 설명할 수 있다.
- 테스트 간 데이터 격리 전략(트랜잭션 롤백, 컨테이너 재생성)을 비교하고 선택할 수 있다.
- 스키마 마이그레이션을 테스트 환경에서 실제 운영 환경과 동일하게 유지하는 방법을 적용할 수 있다.

## 인메모리 DB로 대체해도 될까

"테스트를 빠르게 하려고 SQLite 인메모리 DB로 실제 프로덕션 DB(예: PostgreSQL)를 대체하면 안 될까?"라는 질문을 자주 받습니다. 답은 <strong>"안 된다"</strong>에 가깝습니다. 이유는 08편에서 다룬 통합 테스트의 목적, 즉 "우리 코드와 실제 인프라가 맞물리는가"를 검증하는 데 있습니다.

```python
# 위험한 가정: SQLite와 PostgreSQL이 동일하게 동작한다고 가정
def test_order_query_with_sqlite(sqlite_session):
    repository = SqlOrderRepository(sqlite_session)
    repository.save("order-1", 10000)
    result = repository.find_orders_over_amount(5000)
    assert len(result) == 1
```

이 테스트는 SQLite에서는 통과하지만, PostgreSQL 전용 문법(예: `JSONB` 연산자, `ON CONFLICT` 절, 대소문자 구분 정책)을 쓰는 쿼리가 있다면 운영 환경에서만 실패할 수 있습니다. 데이터 타입의 정밀도, 트랜잭션 격리 수준, 대소문자 구분 규칙도 DB 엔진마다 다릅니다. **테스트 환경의 DB 엔진은 운영 환경과 동일해야 합니다.**

현실적인 대안은 **Docker 컨테이너로 실제 DB 엔진을 테스트 시점에 띄우는 것**입니다.

```python
import pytest


@pytest.fixture(scope="session")
def postgres_container():
    container = start_postgres_container(image="postgres:16")
    yield container
    container.stop()


@pytest.fixture
def db_session(postgres_container):
    engine = create_engine(postgres_container.connection_url)
    run_migrations(engine)  # 실제 운영과 동일한 마이그레이션 적용
    with engine.connect() as conn:
        yield conn
```

컨테이너 기동 비용이 있지만, `scope="session"`으로 테스트 세션당 한 번만 띄우면 개별 테스트의 속도 저하는 크지 않습니다.

## 테스트 간 데이터 격리 전략

같은 DB 컨테이너를 여러 테스트가 공유하면, 한 테스트가 남긴 데이터가 다른 테스트에 영향을 줄 수 있습니다(04편에서 다룬 "다른 테스트와 독립적으로 실행 가능"이라는 조건을 위반). 대표적인 격리 전략 두 가지를 비교합니다.

| 전략 | 방법 | 속도 | 격리 신뢰도 |
|---|---|---|---|
| 트랜잭션 롤백 | 테스트마다 트랜잭션을 시작하고, 끝나면 커밋하지 않고 롤백 | 빠름 | 높음(단, 테스트 대상 코드가 자체적으로 커밋하면 깨질 수 있음) |
| 데이터 초기화 | 테스트마다 관련 테이블을 TRUNCATE하거나 컨테이너를 재시작 | 느림 | 가장 확실함 |

```python
@pytest.fixture
def isolated_db_session(postgres_container):
    engine = create_engine(postgres_container.connection_url)
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()  # 테스트가 남긴 데이터를 되돌린다
    connection.close()
```

트랜잭션 롤백 전략은 대부분의 경우에 빠르고 안전하지만, 테스트 대상 코드가 내부적으로 별도 커넥션을 열어 커밋하는 구조라면(예: 백그라운드 작업 큐) 롤백이 그 변경까지 되돌리지 못합니다. 이런 경우는 테이블 초기화나 컨테이너 재시작이 더 안전합니다.

## 스키마 마이그레이션과 테스트를 함께 유지한다

테스트용 DB 스키마를 손으로 따로 관리하면, 실제 운영에 적용되는 마이그레이션 스크립트와 점점 어긋납니다. 테스트 환경은 **운영과 동일한 마이그레이션 도구로, 매번 처음부터 스키마를 생성**해야 합니다.

```python
def run_migrations(engine) -> None:
    # 운영 배포에 쓰는 것과 동일한 마이그레이션 스크립트를 실행
    alembic_config = Config("alembic.ini")
    alembic_config.attributes["connection"] = engine
    command.upgrade(alembic_config, "head")
```

이렇게 하면 마이그레이션 스크립트 자체의 오류(컬럼 타입 실수, 제약 조건 누락)도 테스트 단계에서 잡을 수 있습니다. 손으로 짠 `CREATE TABLE` 스크립트를 테스트에서 별도로 유지하면, 실제 마이그레이션과 점점 벌어지다가 운영 배포 시점에야 불일치가 드러납니다.

## 리포지터리 테스트는 무엇을 검증해야 하는가

리포지터리 테스트를 지나치게 세밀하게 작성하면(모든 쿼리 메서드를 모든 입력 조합으로), 07편에서 다룬 4분면의 "사족" 문제가 DB 계층에서도 똑같이 재현됩니다. 리포지터리 테스트는 다음에 집중합니다.

- 저장한 값을 그대로 조회할 수 있는가(round-trip 검증)
- 도메인 규칙과 관련된 쿼리 조건(예: "특정 상태의 주문만 조회")이 실제로 그 조건대로 동작하는가
- 동시성이 문제가 되는 지점(예: 재고 차감)에서 실제 락(lock) 동작이 의도대로 작동하는가

```python
def test_find_orders_by_status_returns_only_matching(isolated_db_session):
    repository = SqlOrderRepository(isolated_db_session)
    repository.save("order-1", 10000, status="CONFIRMED")
    repository.save("order-2", 20000, status="CANCELLED")

    result = repository.find_by_status("CONFIRMED")

    assert [o.order_id for o in result] == ["order-1"]
```

## 실무 체크리스트

- 테스트 환경의 DB 엔진이 운영 환경과 동일한가?
- 테스트 간 데이터 격리 전략(롤백/초기화)이 테스트 대상 코드의 커밋 방식과 맞는가?
- 테스트용 스키마가 실제 마이그레이션 스크립트로 생성되는가, 아니면 별도로 관리되는가?
- 리포지터리 테스트가 모든 쿼리 조합을 검증하려다 유지비만 키우고 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- 여러분의 프로젝트에서 테스트 DB가 운영 DB 엔진과 다르다면(예: SQLite vs PostgreSQL), 그 차이로 인해 놓칠 수 있는 시나리오를 3가지 적어보세요.

### 중급(★★☆)
- 트랜잭션 롤백 방식으로 리포지터리 통합 테스트를 작성하고, 테스트를 여러 번 반복 실행해도 결과가 항상 동일한지 확인해보세요.

### 고급(★★★)
- 동시에 두 트랜잭션이 같은 재고를 차감하는 상황을 통합 테스트로 재현하고, 락 전략(비관적/낙관적)에 따라 결과가 어떻게 달라지는지 비교해보세요.

## 요약

- 인메모리 DB로 실제 프로덕션 DB를 대체하면 엔진별 차이로 인한 버그를 놓칠 수 있다. 컨테이너로 동일한 엔진을 띄우는 편이 안전하다.
- 테스트 간 격리는 트랜잭션 롤백을 기본으로 하되, 테스트 대상이 별도 커밋을 한다면 데이터 초기화 전략을 쓴다.
- 테스트 스키마는 운영과 동일한 마이그레이션 도구로 매번 생성해, 마이그레이션 스크립트 자체의 오류도 검증한다.

## 참고 문헌 및 출처(추천)

- Vladimir Khorikov, 『Unit Testing: Principles, Practices, and Patterns』(Manning, 2020) — 관계형 데이터베이스 통합 테스트 전략
- Martin Fowler, "Testcontainers"(2021, martinfowler.com 관련 아티클) — 컨테이너 기반 통합 테스트 관행
- PostgreSQL 공식 문서, "Transaction Isolation" — 트랜잭션 격리 수준 레퍼런스

---

## 다음 글

- 다음: [11. 흔한 단위 테스트 안티패턴](../unit-testing-anti-patterns/)
