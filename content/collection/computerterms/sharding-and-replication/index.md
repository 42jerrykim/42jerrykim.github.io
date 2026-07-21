---
image: "wordcloud.png"
slug: sharding-and-replication
collection_order: 28
draft: false
title: "[Computer Terms] 샤딩과 복제 (Sharding, Replication)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "샤딩은 데이터를 여러 서버에 나눠 저장하고, 복제는 같은 데이터를 여러 서버에 복사해 둡니다. 두 기법이 각각 어떤 한계를 넓히는지, 복제 지연이 만드는 일관성 문제를 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- Sharding(샤딩)
- Replication(복제)
- Distributed-Systems(분산시스템)
- Scalability(확장성)
- Consistency(일관성)
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
- Reliability(신뢰성)
- Debugging(디버깅)
- Advanced
- How-To
---

## 이 장을 읽기 전에

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/), [로드 밸런싱](/post/computerterms/load-balancing/)에서 다룬 "서버 한 대의 한계를 여러 대로 나눠 넘어선다"는 아이디어를 안다고 가정한다. 로드 밸런싱이 요청(연산)을 나눴다면, 이 챕터는 데이터 자체를 어떻게 나누고 복사할지를 다룬다.

## 샤딩: 데이터를 쪼개 나눠 담기

**샤딩(Sharding)**은 하나의 큰 테이블을 여러 서버(샤드)에 행 단위로 분산 저장하는 기법이다. 사용자 100만 명의 데이터를 한 서버에 다 담는 대신, 사용자 ID를 기준으로 절반은 서버 A에, 절반은 서버 B에 나눠 담는 식이다. 이렇게 하면 한 서버가 감당해야 할 데이터 크기와 쿼리 부하가 줄어든다. 문제는 **어떤 기준으로 나눌 것인가**다. [해시테이블](/post/computerterms/hash-tables/)에서 다룬 해시 함수로 사용자 ID를 샤드 번호로 매핑하는 **해시 샤딩**이 가장 흔하다. 다만 이 경우 특정 샤드에만 몰리는 데이터(핫스팟)가 있으면 여전히 그 샤드에 부하가 집중된다 — 예를 들어 유명인 계정의 데이터가 다른 사용자보다 훨씬 많이 조회된다면, 해시로 분산해도 그 하나의 샤드는 여전히 뜨겁다.

```text
해시 샤딩:  shard = hash(user_id) % 샤드_수
            user_id=42 → hash(42) % 4 = 2 → 샤드 2에 저장

문제: 샤드 수를 4에서 5로 늘리면 대부분의 user_id의 나머지 값이 바뀌어
      기존 데이터 위치를 대량으로 재배치해야 한다 (재샤딩 비용)
```

샤드 수를 나중에 바꾸면 거의 모든 데이터의 위치가 바뀌는 문제를 완화하기 위해, 실무에서는 **일관 해싱(Consistent Hashing)**을 쓰기도 한다 — 샤드 하나가 추가·제거될 때 영향받는 데이터의 비율을 전체의 극히 일부로 줄이는 해싱 기법이다.

## 복제: 같은 데이터를 여러 곳에 복사하기

**복제(Replication)**는 샤딩과 다른 목적을 갖는다 — 데이터를 나누는 것이 아니라, **같은 데이터를 여러 서버에 그대로 복사**해 둔다. 원본을 담은 **주(Primary/Leader)** 서버가 쓰기를 처리하면, 그 변경 내역이 하나 이상의 **부(Replica/Follower)** 서버로 전파된다. 이렇게 하면 두 가지를 얻는다. 첫째, 주 서버가 죽어도 부 서버 중 하나를 새 주 서버로 승격시켜 서비스를 계속할 수 있다(**가용성**). 둘째, 읽기 요청을 여러 부 서버로 분산시켜 처리량을 늘릴 수 있다(부 서버는 읽기 전용으로 쓰는 것이 일반적이다).

## 복제 지연이 만드는 문제

복제는 네트워크를 거쳐 전파되므로 **복제 지연(Replication Lag)**이 필연적으로 존재한다. 주 서버에 데이터를 쓴 직후, 그 변경이 아직 부 서버에 반영되기 전에 부 서버로 읽기 요청이 가면 옛 데이터를 보게 된다. 이는 [ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 단일 서버 트랜잭션의 일관성 보장과는 다른 종류의 문제다 — 복제된 시스템에서는 "한 서버 안에서의 일관성"이 아니라 "여러 서버 사이의 일관성"을 따로 고민해야 한다. 이 트레이드오프를 다루는 대표적인 개념이 **CAP 정리**이며, 다음 챕터에서 이를 다룬다.

## 비교: 샤딩 vs 복제

| 특성 | 샤딩 | 복제 |
|---|---|---|
| 목적 | 데이터 크기·쓰기 부하 분산 | 가용성 확보, 읽기 부하 분산 |
| 각 서버가 가진 데이터 | 전체의 일부만 | 전체 데이터의 사본 |
| 한 서버 장애 시 | 그 샤드의 데이터에 접근 불가 | 다른 부 서버로 계속 서비스 가능 |
| 같이 쓰는 경우 | 각 샤드를 다시 복제해 둠(샤딩 + 복제 조합) | 단독으로도 흔히 사용 |

## 흔한 오개념

**"샤딩과 복제는 둘 중 하나만 쓰면 된다"** — 실무 대규모 시스템은 대개 두 기법을 함께 쓴다. 데이터를 여러 샤드로 나누고(샤딩), 각 샤드를 다시 여러 서버에 복제해(복제) 둔다. 샤딩만 하면 한 샤드가 죽었을 때 그 데이터 전체에 접근할 수 없고, 복제만 하면 데이터 전체 크기가 한 서버 용량을 넘을 수 없다.

**"부 서버로 읽으면 항상 최신 데이터다"** — 복제 지연 때문에 부 서버는 주 서버보다 조금 뒤처진 상태일 수 있다. "방금 내가 쓴 데이터를 곧바로 읽어야 하는" 요구(자기 자신의 쓰기 일관성)가 있는 화면에서는 그 요청만 주 서버로 보내는 등 별도 처리가 필요하다.

## 다른 개념과의 연결

일관 해싱은 [해시테이블](/post/computerterms/hash-tables/)의 해시 함수 개념을 분산 시스템 규모로 확장한 것이다. 복제 지연이 만드는 "여러 서버 사이의 일관성" 문제는 다음 챕터인 CAP 정리와 합의 알고리즘에서 이론적으로 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 샤딩과 복제가 각각 어떤 문제(데이터 크기·부하 분산 vs 가용성)를 푸는지 구분해 설명할 수 있다. 해시 샤딩에서 샤드 수를 바꿀 때 왜 대량 재배치가 필요한지, 일관 해싱이 이를 어떻게 완화하는지 설명할 수 있다. 복제 지연이 읽기 일관성에 미치는 영향과, "자기 자신의 쓰기 일관성"이 필요한 상황을 식별할 수 있다.

## 참고 자료

> Kleppmann, M. (2017). *Designing Data-Intensive Applications*, Chapter 5–6: Replication, Partitioning. O'Reilly Media.

- [MongoDB Documentation: Sharding](https://www.mongodb.com/docs/manual/sharding/) — 해시 기반·범위 기반 샤딩 전략 비교
- [PostgreSQL Documentation: High Availability, Load Balancing, and Replication](https://www.postgresql.org/docs/current/high-availability.html) — 실제 RDBMS의 복제 구성 방식
