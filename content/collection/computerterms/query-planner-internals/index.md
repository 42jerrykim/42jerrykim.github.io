---
image: "wordcloud.png"
slug: query-planner-internals
collection_order: 67
draft: false
title: "[Computer Terms] 쿼리 플래너 내부 (Query Planner, Optimizer)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "쿼리 플래너는 같은 SQL을 실행하는 여러 방법 중 통계를 근거로 가장 저렴한 것을 고르는 옵티마이저입니다. 조인 알고리즘 선택과 EXPLAIN 출력 읽는 법을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- SQL(Structured Query Language)
- Query-Optimization(쿼리최적화)
- PostgreSQL
- MySQL
- Index(인덱스)
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
- Time-Complexity(시간복잡도)
- Data-Structure(자료구조)
- Algorithm(알고리즘)
- Data-Integrity(데이터무결성)
---

## 이 장을 읽기 전에

[NoSQL과 쿼리 최적화](/post/computerterms/nosql-and-query-optimization/)에서 다룬 실행 계획(Execution Plan)의 기초와, [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 B-Tree 인덱스 원리를 안다고 가정한다. 이 챕터는 그 실행 계획을 누가, 무엇을 근거로 결정하는지를 다룬다.

## SQL은 "무엇을"만 말하고, 플래너가 "어떻게"를 정한다

SQL은 **선언형(Declarative)** 언어다. `SELECT * FROM orders WHERE customer_id = 42`라는 문장은 원하는 결과가 무엇인지만 말할 뿐, 그 결과를 어떤 순서로 어떤 자료구조를 훑어 얻을지는 말하지 않는다. 이 "어떻게"를 결정하는 것이 **쿼리 플래너(Query Planner)**, 또는 **옵티마이저(Optimizer)**다. 같은 결과를 내는 실행 방법은 보통 여러 개 존재하고, 그 성능 차이는 수십–수백 배에 달할 수 있다. 플래너의 역할은 이 여러 후보 중 가장 저렴한 하나를 고르는 것이다.

## 통계 기반 비용 추정

플래너가 "저렴하다"를 판단하려면 각 실행 방법이 얼마나 걸릴지 미리 추정해야 하는데, 이를 위해 테이블의 행 수, 컬럼 값의 분포(히스토그램), 고유 값의 개수 같은 **통계(Statistics)**를 활용한다. 예를 들어 `WHERE status = 'active'` 조건에서 `status` 컬럼의 값 대부분이 `'active'`라면, 인덱스를 거쳐 하나씩 행을 찾는 것보다 테이블을 처음부터 순차적으로 훑는 것이 더 빠를 수 있다. 반대로 `'active'`인 행이 전체의 1퍼센트뿐이라면 인덱스를 쓰는 쪽이 압도적으로 유리하다. 이 통계는 데이터가 계속 바뀌므로 오래되면 부정확해지고, 대부분의 데이터베이스는 `ANALYZE` 같은 명령으로 통계를 주기적으로 갱신한다.

## 조인 순서와 조인 알고리즘

쿼리가 여러 테이블을 조인할 때, 플래너는 두 가지를 함께 결정한다. 어떤 순서로 테이블을 조인할 것인가, 그리고 각 조인 단계에서 어떤 알고리즘을 쓸 것인가다. 테이블이 세 개 이상이면 조인 순서의 조합 수가 테이블 개수에 대해 지수적으로 늘어나므로, 플래너는 모든 조합을 다 계산하지 않고 동적 계획법이나 유전 알고리즘 같은 근사 기법으로 탐색 범위를 줄인다.

조인 알고리즘은 대표적으로 세 가지다. **Nested Loop Join**은 한 테이블의 각 행마다 다른 테이블에서 일치하는 행을 찾는 방식으로, 구현이 단순하고 한쪽 테이블이 작거나 조인 컬럼에 인덱스가 있을 때 빠르다. **Hash Join**은 한쪽 테이블로 해시 테이블([해시테이블](/post/computerterms/hash-tables/) 챕터 참고)을 만들고 다른 쪽 테이블을 훑으며 매칭하는 방식으로, 인덱스가 없어도 두 테이블 모두 클 때 효율적이다. **Merge Join**은 두 테이블이 이미 조인 키로 정렬돼 있거나 정렬 비용을 감수할 수 있을 때, 두 정렬된 목록을 나란히 훑으며 병합하는 방식이다.

## EXPLAIN으로 플래너의 선택 읽기

`EXPLAIN`은 플래너가 실제로 무엇을 선택했는지 보여준다.

```sql
EXPLAIN ANALYZE
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.region = 'APAC';
```

```text
Hash Join  (cost=45.50..892.30 rows=1200 width=48) (actual time=1.2..15.8 rows=1150 loops=1)
  Hash Cond: (o.customer_id = c.customer_id)
  ->  Seq Scan on orders o  (cost=0.00..820.00 rows=40000 width=12)
  ->  Hash  (cost=40.00..40.00 rows=440 width=40)
        ->  Seq Scan on customers c  (cost=0.00..40.00 rows=440 width=40)
              Filter: (region = 'APAC')
```

이 출력은 위에서 다룬 조인 알고리즘 선택(Hash Join)과 각 단계의 접근 방식(Seq Scan)을 보여준다. `cost=45.50..892.30`은 플래너가 실행 전에 추정한 비용 범위이고, `actual time=1.2..15.8 rows=1150`은 실제로 실행해서 측정한 시간과 행 수다. 추정 비용의 `rows`(1200)와 실제 `rows`(1150)가 크게 어긋나면, 통계가 오래됐거나 플래너가 잘못된 판단을 내렸을 가능성을 의심해야 한다 — 이 차이를 확인하는 것이 쿼리 튜닝의 출발점이다.

## 비교: 세 가지 조인 알고리즘

| 알고리즘 | 적합한 상황 | 특징 |
|---|---|---|
| Nested Loop | 한쪽 테이블이 작거나 인덱스가 있음 | 구현 단순, 큰 테이블끼리는 느림 |
| Hash Join | 양쪽 모두 크고 인덱스 없음 | 해시 테이블 구축에 메모리 필요 |
| Merge Join | 이미 정렬돼 있거나 정렬 비용 감수 가능 | 정렬된 두 목록을 순차 병합 |

## 흔한 오개념

**"플래너는 항상 최적의 계획을 찾는다"** — 플래너는 최적이 아니라 통계를 근거로 한 "추정상 가장 저렴한" 계획을 찾을 뿐이다. 통계가 오래됐거나, 조인 조건이 복잡해 비용 추정 모델 자체가 부정확하면 실제로는 더 느린 계획을 고를 수 있다. `EXPLAIN ANALYZE`로 추정과 실제를 비교하는 습관이 필요한 이유다.

**"인덱스가 있으면 플래너가 무조건 그것을 쓴다"** — [NoSQL과 쿼리 최적화](/post/computerterms/nosql-and-query-optimization/) 챕터에서 다룬 것처럼, 조건에 맞는 행이 테이블 대부분을 차지한다면 인덱스를 거쳐 하나씩 찾는 것보다 순차 스캔이 더 저렴하다고 플래너가 판단할 수 있다. 인덱스의 존재는 선택지를 늘릴 뿐, 사용을 강제하지 않는다.

## 다른 개념과의 연결

Hash Join은 [해시테이블](/post/computerterms/hash-tables/)을, Merge Join은 정렬된 자료구조 순회를 그대로 응용한 것이며, 조인 순서 탐색에 쓰이는 동적 계획법은 시간 복잡도 갈래에서 다룬 최적화 기법과 같은 뿌리를 갖는다. 다음 챕터에서는 B-Tree 인덱스로는 풀기 어려운 검색 문제, 즉 "본문에 이 단어가 포함된 문서 찾기"를 해결하는 전문검색 인덱스를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 플래너가 통계를 근거로 실행 계획을 선택하는 원리를 설명할 수 있다. Nested Loop·Hash·Merge 세 조인 알고리즘이 각각 어떤 상황에 유리한지 구분할 수 있다. `EXPLAIN ANALYZE` 출력에서 추정 비용과 실제 실행 결과의 차이를 읽고, 통계가 오래됐을 가능성을 진단할 수 있다.

## 참고 자료

> "The task of the planner/optimizer is to create an optimal execution plan." — PostgreSQL Documentation, *51.5. Planner/Optimizer*

- [PostgreSQL Documentation: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) — EXPLAIN 출력 형식과 비용 추정치를 읽는 공식 가이드
- [PostgreSQL Documentation: Planner Statistics](https://www.postgresql.org/docs/current/planner-stats.html) — 플래너가 사용하는 통계의 종류와 갱신 방식
