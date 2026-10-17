---
collection_order: 0
date: 2026-10-02T00:10:00+09:00
lastmod: 2026-10-12T00:10:00+09:00
draft: true
title: "[Database] 00. Introduction: 데이터베이스 트랜잭션과 격리 수준 심화"
slug: getting-started-database-transactions
description: "격리 수준 이름만 외워서는 실제 DB에서 생기는 버그를 막을 수 없는 이유와, write skew·lost update를 다루며 PostgreSQL·MySQL·Oracle·SQL Server를 비교하는 7개 챕터 커리큘럼, 학습 목표를 정리한 시리즈 도입 챕터입니다."
tags:
  - Database(데이터베이스)
  - Transaction(트랜잭션)
  - SQL(Structured Query Language)
  - PostgreSQL
  - MySQL
  - Oracle
  - SQL-Server
  - ACID(Atomicity Consistency Isolation Durability)
  - Isolation-Level(격리수준)
  - Snapshot-Isolation
  - Serializable
  - Write-Skew
  - Lost-Update
  - Dirty-Read
  - Phantom-Read
  - MVCC
  - Concurrency(동시성)
  - Lock(락)
  - Deadlock(데드락)
  - Race-Condition(레이스컨디션)
  - Consistency(일관성)
  - Data-Integrity(데이터무결성)
  - Distributed-Systems(분산시스템)
  - Backend(백엔드)
  - Retry(재시도)
  - Computer-Science(컴퓨터과학)
  - Software-Engineering(소프트웨어공학)
  - Curriculum(커리큘럼)
  - Roadmap(로드맵)
  - Education(교육)
  - Deep-Dive
  - Advanced
  - Tutorial(튜토리얼)
image: "wordcloud.png"
---

"격리 수준을 Repeatable Read로 두었으니 동시에 들어온 요청끼리 간섭하지 않는다"는 믿음은 생각보다 많은 서비스에서 장애의 출발점이 된다. 잔액이 한 번 덜 차감되고, 당직 의사가 0명이 되고, 같은 좌석이 두 사람에게 팔리는 사고는 대부분 쿼리 문법의 오류가 아니라 **격리 수준이 실제로 무엇을 보장하고 무엇을 보장하지 않는지**에 대한 오해에서 나온다. 이 시리즈는 그 오해를 하나씩 해체한다. 이름이 같아도 DBMS마다 구현과 보장이 다르다는 점, 그리고 SQL 표준이 정의한 세 가지 이상 현상만으로는 현실의 이상 현상을 설명할 수 없다는 점이 출발점이다.

## 이 시리즈가 필요한 이유

트랜잭션의 고립성(Isolation)은 ACID 중에서 가장 오해되기 쉬운 속성이다. 원자성은 "전부 반영되거나 전부 취소된다"로, 지속성은 "커밋하면 남는다"로 비교적 선명하게 설명된다. 반면 고립성은 "동시에 실행되어도 순서대로 실행한 것처럼 보인다"는 이상적 정의와, 성능을 위해 그 이상을 단계적으로 포기한 현실의 격리 수준 사이에 큰 간격이 있다. 이 간격 안에서 write skew나 lost update 같은 이상 현상이 발생하는데, 이런 버그는 부하 테스트에서도 잘 드러나지 않고 트래픽이 몰리는 시점에야 재현된다.

사이트에는 이미 [ACID Transactions](/post/computerterms/acid-transactions/), [트랜잭션 격리 수준](/post/computerterms/transaction-isolation-levels/), [MVCC](/post/computerterms/mvcc/)를 다룬 용어 사전 항목이 있다. 그 글들은 각 개념의 정의와 한 장짜리 그림을 제공하는 것이 목적이다. 이 시리즈는 그 다음 질문에 답한다. 정의를 알고 있을 때, 실제 DBMS에서 어떤 SQL을 어떤 순서로 실행하면 어떤 결과가 나오며, 애플리케이션은 무엇을 해야 하는가.

## 학습 목표와 결과

이 시리즈를 끝까지 읽으면 다음 세 가지를 할 수 있게 되는 것을 목표로 한다. 첫째, 서비스에서 일어난 동시성 버그를 이상 현상의 이름(lost update, write skew, phantom 등)으로 분류하고, 그것이 현재 격리 수준에서 발생 가능한지 판단한다. 둘째, PostgreSQL·MySQL InnoDB·Oracle·SQL Server가 같은 격리 수준 이름 아래에서 서로 다르게 동작하는 지점을 구분하고, DBMS를 옮길 때 깨질 가정을 미리 짚는다. 셋째, 문제에 맞춰 격리 수준 상향, 행 잠금, 제약조건, 재시도 중 하나를 골라 설계하고 그 선택의 비용을 설명한다. 실무 관점에서는 결제·재고·예약·정산처럼 "한 번 틀리면 돈이 틀어지는" 도메인의 코드 리뷰에서 근거를 들어 의견을 낼 수 있게 된다는 의미다.

## 커리큘럼과 챕터별 필요성

챕터는 "현상을 분류하는 언어 → 구현 메커니즘 → 보장 수준의 한계 → 애플리케이션 설계 → 분산 환경으로의 확장" 순서로 배열했다. 앞 장이 뒷 장의 용어를 제공하므로 순서를 지키는 편이 좋고, 이미 이상 현상에 익숙한 독자는 02장부터 시작해도 된다.

| 장 | 주제 | 이 순서인 이유 | 건너뛰면 생기는 한계 |
|---|---|---|---|
| 01 | [격리 수준과 이상 현상: ANSI의 허점과 write skew](/post/database-transactions/isolation-levels-and-anomalies/) | 이후 모든 장이 쓰는 이상 현상 어휘를 먼저 정립한다 | "Repeatable Read면 안전"이라는 오해를 교정하지 못한다 |
| 02 | [스냅샷 격리와 MVCC 구현](/post/database-transactions/snapshot-isolation-and-mvcc/) | 이상 현상이 왜 그 수준에서 허용되는지 구현으로 설명한다 | 이상 현상을 외우게 될 뿐 구현이 다른 DBMS로 확장되지 않는다 |
| 03 | [락 기반 격리: 2PL, next-key lock, 데드락](/post/database-transactions/lock-based-isolation/) | MVCC와 다른 축인 락 기반 구현을 이해한다 | MySQL InnoDB의 gap lock·데드락 동작을 설명하지 못한다 |
| 04 | [Serializable의 구현: SSI와 위험한 구조](/post/database-transactions/serializable-snapshot-isolation/) | 가장 강한 수준이 실제로 어떻게 보장되는지 본다 | Serializable을 쓰고도 재시도 설계가 없어 장애가 난다 |
| 05 | [설계 패턴: 원자적 UPDATE, 낙관적 락, SKIP LOCKED](/post/database-transactions/application-design-patterns/) | 앞 장의 지식을 코드 패턴으로 바꾼다 | 격리 수준 상향만이 해법이라고 오해한다 |
| 06 | [분산 트랜잭션: 2PC, 사가, 아웃박스, 스패너](/post/database-transactions/distributed-transactions/) | 단일 노드 가정이 깨질 때의 비용을 이해한다 | 마이크로서비스에서 트랜잭션 경계를 잘못 긋는다 |
| 07 | [격리 수준 검증: 재현 테스트, Hermitage, Elle](/post/database-transactions/verifying-isolation-levels/) | 문서의 주장을 스스로 확인하는 방법을 익힌다 | 벤더 문서와 블로그 글을 검증 없이 믿게 된다 |

02장부터 07장까지의 Python 모델은 표준 라이브러리만으로 실행되며, 각 장에 실제 실행 출력을 함께 실었다. 01장의 재시도 예제(psycopg 사용)와 데이터베이스 서버가 있어야 하는 SQL 시나리오는 공식 문서의 동작 설명에서 도출한 것이므로, 사용하는 버전에서 직접 재현해 확인하기를 권한다. 07장은 그 재현을 위한 테스트 하네스를 다룬다.

## 읽기 전에 알아 둘 것

선수 지식은 `BEGIN`, `COMMIT`, `ROLLBACK`으로 구성되는 트랜잭션의 기본 사용법, 그리고 ACID의 네 속성이 각각 무엇을 뜻하는지 정도다. 부족하다면 앞서 소개한 [ACID Transactions](/post/computerterms/acid-transactions/)와 [레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)을 먼저 읽는 것이 좋다.

본문의 SQL 예제는 기본적으로 PostgreSQL 문법으로 쓰고, MySQL이나 다른 DBMS에서 결과가 달라지는 지점은 본문에서 따로 짚는다. 두 개 이상의 세션이 번갈아 실행되는 예제는 `psql` 창 두 개를 열어 직접 따라 해 보는 것이 가장 빠르다. 동시성 이상 현상은 글로 읽으면 이해한 것 같지만, 직접 두 세션에서 재현해 보기 전까지는 감이 오지 않는 주제다.

## 시리즈 전체에서 반복되는 세 가지 원칙

첫째, 이름보다 보장을 본다. "Repeatable Read"라는 이름은 표준이 정한 것이지만, 그 이름 아래에서 실제로 무엇이 막히는지는 DBMS 문서가 정한다. 둘째, 이상 현상은 "발생 가능성"으로 판단한다. 테스트에서 한 번도 재현되지 않았다는 사실은 안전의 증거가 아니다. 셋째, 격리 수준은 만능이 아니다. 낮은 격리 수준에서도 제약조건이나 행 잠금으로 해결되는 문제가 있고, 가장 높은 수준에서도 재시도 로직 없이는 서비스가 깨진다.

## 이 시리즈를 마친 뒤 할 수 있어야 하는 것

시리즈를 끝까지 읽은 독자는 다음을 할 수 있어야 한다. 서비스의 동시성 버그를 lost update, write skew, 팬텀 같은 이상 현상의 이름으로 분류하고 현재 격리 수준에서의 발생 가능성을 설명한다(01장). 스냅샷이 가시성 규칙임을 설명하고 PostgreSQL과 InnoDB의 저장 전략 차이를 비교한다(02장). 락 기반 격리와 SSI가 같은 불변식을 각각 데드락과 중단으로 지키는 방식을 비교한다(03·04장). 문제 유형에 맞는 설계 패턴을 비용과 함께 고르고 재시도를 안전하게 설계한다(05장). 서비스 경계를 넘는 일관성 전략을 2PC·사가·아웃박스 중에서 선택한다(06장). 문서의 주장을 순서가 고정된 시나리오로 직접 검증한다(07장).

## 참고 자료

- [Berenson et al., A Critique of ANSI SQL Isolation Levels (SIGMOD 1995)](https://arxiv.org/abs/cs/0701157) — ANSI 격리 수준 정의의 허점을 지적한 원전. 01장의 출발점
- [PostgreSQL Documentation: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — 시리즈 전체에서 기준으로 삼는 PostgreSQL 공식 문서
- [MySQL 8.4 Reference Manual: InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html) — InnoDB의 격리 수준별 동작
- [Oracle Database Concepts: Data Concurrency and Consistency](https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/data-concurrency-and-consistency.html) — Oracle의 격리 수준과 직렬화 실패
- [SET TRANSACTION ISOLATION LEVEL (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql) — SQL Server의 격리 수준과 스냅샷 옵션
- [Designing Data-Intensive Applications](https://dataintensive.net/) — Martin Kleppmann, 7장 Transactions가 이 시리즈의 개념적 배경
