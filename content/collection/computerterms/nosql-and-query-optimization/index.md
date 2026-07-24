---
image: "wordcloud.png"
slug: nosql-and-query-optimization
collection_order: 19
draft: false
title: "[Computer Terms] NoSQL과 쿼리 최적화 (NoSQL, Query Optimization)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "NoSQL은 정규화된 관계형 모델 대신 다른 자료구조로 확장성과 유연성을 얻는 데이터베이스 계열입니다. 문서·키-값·컬럼·그래프 모델을 비교하고, EXPLAIN ANALYZE 실행 계획을 읽어 쿼리를 최적화하는 방법을 실제 SQL 예제와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- NoSQL
- SQL(Structured Query Language)
- Query-Optimization(쿼리최적화)
- MongoDB
- Redis
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
- Scalability(확장성)
- Debugging(디버깅)
- Advanced
---

## 이 장을 읽기 전에

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 관계형 모델(테이블·조인·B-Tree 인덱스)을 안다고 가정한다. NoSQL은 이 관계형 모델을 대체하는 것이 아니라, 관계형 모델이 잘 맞지 않는 상황에서 선택할 수 있는 대안이라는 관점으로 접근한다.

## 관계형 모델이 항상 정답은 아니다

정규화된 관계형 모델은 데이터 무결성과 유연한 조회에 강하지만, 두 가지 상황에서 부담이 된다. 첫째, 데이터를 여러 서버에 분산 저장(**샤딩**)해야 할 만큼 규모가 커지면, 조인은 여러 서버에 걸친 데이터를 모아야 해서 급격히 느려진다. 둘째, 스키마가 자주 바뀌는 데이터(로그, 설정값처럼 구조가 문서마다 다를 수 있는 데이터)는 매번 테이블 구조를 변경(마이그레이션)해야 하는 관계형 모델과 잘 맞지 않는다. **NoSQL**은 이런 상황에서 정규화·조인을 포기하는 대신 확장성이나 스키마 유연성을 얻는 데이터베이스 계열을 통칭한다.

## NoSQL의 네 갈래

**문서(Document) DB**(MongoDB 등)는 관련 데이터를 하나의 문서(JSON과 유사한 구조)에 통째로 저장해, 조인 없이 한 번의 조회로 필요한 데이터를 모두 가져온다. [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 분리했던 `customers`와 `orders`를 문서 DB에서는 주문 문서 안에 고객 정보를 함께 내장(embed)해 저장하는 경우가 많다 — 조회는 빨라지지만, 고객 정보가 바뀌면 관련된 모든 문서를 갱신해야 하는 정규화 이전의 이상 현상이 다시 나타날 수 있다.

**키-값(Key-Value) DB**(Redis 등)는 [해시테이블](/post/computerterms/hash-tables/) 챕터에서 다룬 구조를 그대로 데이터베이스 수준으로 확장한 것이다. 복잡한 조회 없이 키로 값을 빠르게 읽고 쓰는 데 특화돼 있어, 세션 저장소나 캐시로 흔히 쓰인다. **컬럼 기반(Column-Family) DB**(Cassandra 등)는 행이 아니라 컬럼 단위로 데이터를 묶어 저장해, 특정 컬럼만 대량으로 읽는 분석 워크로드에 유리하다. **그래프 DB**(Neo4j 등)는 [그래프](/post/computerterms/graphs/) 챕터의 인접 리스트 개념을 데이터베이스 수준으로 확장해, 관계 자체가 조회의 핵심인 경우(추천 시스템, 소셜 네트워크)에 관계형 조인보다 훨씬 빠른 순회를 제공한다.

## 쿼리 최적화: 실행 계획을 읽는다

관계형이든 NoSQL이든, 같은 결과를 내는 쿼리라도 실행 방식에 따라 속도가 크게 달라진다. 대부분의 데이터베이스는 쿼리를 실제로 어떻게 실행할지 보여주는 **실행 계획(Execution Plan)**을 제공한다.

```sql
EXPLAIN ANALYZE
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id = 42;
```

이 계획에서 `orders.customer_id`에 인덱스가 없다면 "Seq Scan"(순차 스캔, [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 Full Table Scan)이 나타나고, 인덱스가 있다면 "Index Scan"이 나타난다. 쿼리 최적화의 첫 단계는 대개 이 실행 계획에서 예상보다 느린 Seq Scan을 찾아 인덱스를 추가하거나, 조인 순서를 조정하는 것이다.

## 비교: 관계형 vs NoSQL 네 갈래

| 모델 | 강점 | 대표 사용처 |
|---|---|---|
| 관계형(RDBMS) | 강한 일관성, 유연한 조회(조인), 정규화로 무결성 보장 | 금융 거래, 재고 관리 |
| 문서 DB | 스키마 유연성, 관련 데이터 한 번에 조회 | 콘텐츠 관리, 카탈로그 |
| 키-값 DB | 극도로 빠른 단순 조회 | 세션 저장, 캐시 |
| 컬럼 기반 DB | 대량 컬럼 단위 읽기·쓰기 | 시계열 데이터, 로그 분석 |
| 그래프 DB | 관계 중심 순회 | 추천, 소셜 네트워크 |

## 흔한 오개념

**"NoSQL은 SQL보다 항상 빠르다"** — NoSQL이 빠른 것은 조인·정규화를 포기해 특정 접근 패턴에 최적화됐기 때문이지, 근본적으로 더 빠른 기술이라서가 아니다. 문서 DB에 정규화 없이 저장한 데이터에서 관계형 조인 같은 복잡한 조회를 하려 하면, 애플리케이션 코드에서 여러 번 조회해 직접 조합해야 해서 오히려 관계형 DB의 단일 조인 쿼리보다 느려질 수 있다.

**"실행 계획에서 인덱스를 쓰면 항상 더 빠르다"** — 테이블이 작거나, 조건에 맞는 행이 전체의 대부분을 차지한다면 인덱스를 거쳐 각 행을 따로 찾는 것보다 순차 스캔이 오히려 빠를 수 있다. 옵티마이저가 통계를 바탕으로 Seq Scan을 선택했다면, 무조건 인덱스 사용을 강제하기보다 그 판단이 맞는지 먼저 확인해야 한다.

## 다른 개념과의 연결

키-값 DB는 [해시테이블](/post/computerterms/hash-tables/)을, 그래프 DB는 [그래프](/post/computerterms/graphs/)를 데이터베이스 수준으로 확장한 것으로, 자료구조 갈래에서 다룬 트레이드오프(정렬 유지 여부, 임의 접근 비용)가 그대로 데이터베이스 선택 기준이 된다. 다음 챕터에서는 데이터를 여러 서버로 나누는 [샤딩과 복제](/post/computerterms/sharding-and-replication/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. NoSQL의 네 갈래(문서·키-값·컬럼·그래프)가 각각 어떤 자료구조를 확장한 것인지, 어떤 접근 패턴에 유리한지 설명할 수 있다. 관계형과 NoSQL 중 데이터의 구조 변동성·조회 패턴·규모에 따라 근거를 갖고 선택할 수 있다. 실행 계획에서 Seq Scan과 Index Scan을 구분하고, 어느 쪽이 더 나은지 상황에 따라 판단할 수 있다.

## 참고 자료

> Sadalage, P. J., & Fowler, M. (2012). *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*. Addison-Wesley.

- [MongoDB Documentation: Data Modeling](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/) — 문서 DB에서 내장(embed) vs 참조(reference) 설계 트레이드오프
- [PostgreSQL Documentation: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) — 실행 계획을 읽고 쿼리를 최적화하는 공식 가이드
