---
image: "wordcloud.png"
slug: normalization-and-indexes
collection_order: 18
draft: false
title: "[Computer Terms] 정규화와 인덱스 (Normalization, Index)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "정규화는 데이터 중복과 이상 현상을 줄이기 위해 테이블을 쪼개는 설계 원칙이고, 인덱스는 그렇게 나뉜 테이블에서도 빠른 조회를 보장하는 자료구조입니다. B-Tree 인덱스 원리를 SQL과 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- SQL
- Normalization(정규화)
- Index(인덱스)
- B-Tree
- Data-Structure(자료구조)
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
- Data-Integrity(데이터무결성)
- Debugging(디버깅)
- Advanced
---

## 이 장을 읽기 전에

[ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 트랜잭션의 신뢰성 보장과, [트리](/post/computerterms/trees/)에서 다룬 균형 이진 탐색 트리의 O(log n) 탐색을 안다고 가정한다. 이 챕터는 "데이터를 어떻게 나눠 저장할 것인가"(정규화)와 "그렇게 나눈 데이터를 어떻게 빠르게 찾을 것인가"(인덱스)라는, 서로 다른 목표를 가진 두 개념을 함께 다룬다.

## 정규화: 왜 테이블을 굳이 쪼개는가

주문 정보에 고객 이름·주소를 매번 함께 저장한다고 하자. 같은 고객이 열 번 주문하면 그 이름·주소가 열 번 중복 저장되고, 고객이 이사하면 열 개의 행을 전부 갱신해야 한다. 하나라도 빠뜨리면 같은 고객의 정보가 행마다 다르게 남는 **이상 현상(Anomaly)**이 생긴다. **정규화(Normalization)**는 이런 중복과 이상 현상을 줄이기 위해, 하나의 사실은 한 곳에만 저장되도록 테이블을 분해하는 설계 규칙이다.

**제1정규형(1NF)**은 각 칸에 원자적인 값만 담아 반복 그룹을 없앤다. **제2정규형(2NF)**은 기본키의 일부에만 종속된 컬럼을 별도 테이블로 분리한다. **제3정규형(3NF)**은 기본키가 아닌 컬럼이 다른 비기본키 컬럼에 종속되는 **이행적 종속(Transitive Dependency)**을 제거한다 — 위 예시에서 "고객 주소"가 "고객 ID"가 아니라 "고객 이름"에 종속돼 있다면 3NF 위반이다.

```sql
-- 정규화 전: 주문마다 고객 정보가 통째로 중복 저장됨
CREATE TABLE orders_denormalized (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_address VARCHAR(200),
    product_name VARCHAR(100),
    quantity INT
);

-- 3NF로 분해: 고객 정보는 customers 테이블에 한 번만 저장
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_address VARCHAR(200)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_name VARCHAR(100),
    quantity INT
);
```

정규화된 구조에서는 고객이 이사하면 `customers` 테이블 한 행만 갱신하면 되고, 모든 주문이 자동으로 최신 주소를 참조한다.

## 정규화의 대가: 조인

정규화의 대가는 조회할 때 여러 테이블을 **조인(JOIN)**해야 한다는 것이다. "주문 목록과 고객 이름을 함께 보고 싶다"는 흔한 조회조차 두 테이블을 연결해야 한다. 조인 자체는 느리지 않지만, 조인 조건에 쓰이는 컬럼(`customer_id`)에 대한 조회가 느리면 전체 쿼리가 느려진다. 이 문제를 푸는 것이 인덱스다.

## 인덱스: 테이블을 훑지 않고 찾는 방법

인덱스가 없으면 특정 조건(`WHERE customer_id = 42`)을 만족하는 행을 찾기 위해 테이블 전체를 처음부터 훑어야 한다(**Full Table Scan**, O(n)). **인덱스(Index)**는 특정 컬럼 값과 그 값을 가진 행의 위치를 미리 정렬된 자료구조에 저장해 둔 것으로, 대부분의 관계형 데이터베이스는 이 자료구조로 **B-Tree**(균형 트리의 한 변형)를 쓴다. [트리](/post/computerterms/trees/) 챕터에서 다룬 균형 이진 탐색 트리와 원리는 같지만, B-Tree는 노드 하나가 자식을 2개보다 훨씬 많이 가질 수 있어(수백 개) 디스크 I/O 횟수를 줄이도록 설계돼 있다 — 디스크 접근 한 번의 비용이 메모리 접근보다 훨씬 크기 때문에, 트리의 높이(디스크 접근 횟수)를 최소화하는 것이 핵심 설계 목표다.

```sql
-- customer_id로 조회가 잦다면 인덱스를 걸어 O(log n)으로 만든다
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 인덱스가 있으면 실행 계획이 Full Scan 대신 Index Seek을 쓴다
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
```

## 비교: 인덱스 있음 vs 없음

| 상황 | 인덱스 없음 | 인덱스 있음 |
|---|---|---|
| `WHERE` 조건 조회 | O(n) Full Scan | O(log n) B-Tree 탐색 |
| `INSERT`/`UPDATE` | 데이터만 추가하면 됨 | 인덱스도 함께 갱신 (추가 비용) |
| 저장 공간 | 테이블 데이터만 | 테이블 + 인덱스 구조 |
| 정렬된 컬럼 조회(`ORDER BY`) | 매번 정렬 필요 | 이미 정렬돼 있어 즉시 반환 가능 |

## 흔한 오개념

**"인덱스는 많이 걸수록 좋다"** — 인덱스는 조회를 빠르게 하는 대신, 모든 `INSERT`·`UPDATE`·`DELETE`마다 인덱스 구조도 함께 갱신해야 하므로 쓰기 성능을 떨어뜨린다. 조회가 압도적으로 많은 컬럼에만 선별적으로 인덱스를 걸어야, 읽기 속도와 쓰기 비용 사이의 균형이 맞는다.

**"정규화가 항상 정답이다"** — 3NF까지 철저히 분해하면 데이터 중복은 사라지지만, 조회할 때마다 여러 테이블을 조인해야 해서 읽기 성능이 떨어질 수 있다. 읽기가 압도적으로 많고 쓰기가 드문 분석용 시스템에서는 의도적으로 일부 중복을 허용하는 **반정규화(Denormalization)**를 쓰기도 한다 — "정규화 수준"은 고정된 정답이 아니라 읽기·쓰기 비율에 따른 선택이다.

## 다른 개념과의 연결

B-Tree 인덱스는 [트리](/post/computerterms/trees/) 챕터의 균형 이진 탐색 트리를, 조인은 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)·[해시테이블](/post/computerterms/hash-tables/) 챕터에서 다룬 탐색 전략(정렬 병합 조인, 해시 조인)을 그대로 응용한 것이다. 다음 챕터에서는 이 정규화·인덱스 모델을 완화하거나 다르게 접근하는 NoSQL과, 실제 쿼리 성능을 튜닝하는 방법을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 정규화가 줄이려는 이상 현상이 무엇인지, 왜 조인이라는 대가가 따르는지 설명할 수 있다. 인덱스가 Full Table Scan을 B-Tree 탐색으로 바꾸는 원리와, 인덱스가 쓰기 성능에 미치는 영향을 설명할 수 있다. 읽기·쓰기 비율에 따라 정규화 수준과 인덱스 개수를 조정하는 판단을 할 수 있다.

## 참고 자료

> Codd, E. F. (1970). "A Relational Model of Data for Large Shared Data Banks". *Communications of the ACM*, 13(6), 377–387.

- [Use The Index, Luke!](https://use-the-index-luke.com/) — B-Tree 인덱스 동작 원리와 SQL 튜닝을 다루는 대표적인 실무 참고 자료
- [PostgreSQL Documentation: Indexes](https://www.postgresql.org/docs/current/indexes.html) — 실제 RDBMS의 인덱스 종류와 동작 방식 상세 문서
