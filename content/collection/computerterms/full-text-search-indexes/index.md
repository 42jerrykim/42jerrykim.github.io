---
image: "wordcloud.png"
slug: full-text-search-indexes
collection_order: 68
draft: false
title: "[Computer Terms] 전문검색 인덱스 (Full-Text Search, Inverted Index)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "B-Tree 인덱스는 정확 일치·범위 검색에 강하지만 본문 검색에는 약합니다. 역색인이 단어를 문서 목록에 매핑해 이 문제를 푸는 원리와 SQL 예시를 다루고, 토큰화·불용어 제거·형태소 분석 과정까지 함께 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- SQL(Structured Query Language)
- Index(인덱스)
- Full-Text-Search(전문검색)
- Inverted-Index(역색인)
- PostgreSQL
- Elasticsearch
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
- Data-Structure(자료구조)
- Time-Complexity(시간복잡도)
- Storage(저장소)
---

## 이 장을 읽기 전에

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 B-Tree 인덱스와, [해시테이블](/post/computerterms/hash-tables/)에서 다룬 키-값 매핑 원리를 안다고 가정한다. 이 챕터는 B-Tree 인덱스가 잘 풀지 못하는 검색 문제를 역색인이라는 다른 자료구조로 어떻게 해결하는지 다룬다.

## B-Tree가 잘 푸는 문제, 못 푸는 문제

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/) 챕터에서 다룬 B-Tree 인덱스는 컬럼 값을 정렬된 순서로 저장해, `customer_id = 42` 같은 정확 일치 조건이나 `price BETWEEN 100 AND 200` 같은 범위 조건을 O(log n)으로 찾는다. 이 구조는 값 전체를 하나의 단위로 비교할 수 있을 때 잘 동작한다.

하지만 "본문(`content` 컬럼)에 '데이터베이스'라는 단어가 포함된 문서를 찾아라" 같은 조건에는 B-Tree가 맞지 않는다. `LIKE '%데이터베이스%'` 같은 패턴 검색은 컬럼 값 전체를 정렬해 봐야 문자열 중간에 그 단어가 있는지 알 수 없으므로, 인덱스를 타지 못하고 결국 모든 행의 본문을 처음부터 훑는 Full Table Scan으로 돌아간다. 문서가 수백만 건이면 이 방식은 실용적이지 않다.

## 역색인: 단어에서 문서로 거꾸로 찾는다

**역색인(Inverted Index)**은 이 문제를 뒤집어서 접근한다. "문서에 어떤 단어들이 있는가"를 저장하는 대신, "이 단어는 어떤 문서들에 있는가"를 미리 계산해 저장한다. 각 고유 단어를 키로, 그 단어가 등장하는 문서 ID 목록을 값으로 갖는 매핑을 만들어 두면, 특정 단어를 포함한 문서를 찾는 작업이 그 단어를 키로 한 번 조회하는 것으로 끝난다. 이 매핑 구조 자체는 [해시테이블](/post/computerterms/hash-tables/) 챕터에서 다룬 키-값 조회와 원리가 같다 — 단어를 키로, 문서 ID 목록을 값으로 갖는 해시 테이블(또는 정렬된 구조)이라고 볼 수 있다.

문서를 색인에 넣는 과정은 몇 단계를 거친다. 먼저 본문을 단어 단위로 쪼개는 **토큰화(Tokenization)**를 하고, "은", "는", "the", "a" 같이 검색에 의미가 없는 **불용어(Stopword)**를 제거하며, "달리다"·"달렸다"·"달릴"처럼 같은 단어의 활용형을 하나의 **어간(Stem)**으로 통일하는 **형태소 분석(Stemming)**을 거친다. 이렇게 정제된 단어들만 역색인의 키가 된다.

## SQL에서 전문검색 사용하기

PostgreSQL은 `tsvector`(정제된 단어 목록)와 `tsquery`(검색어)라는 타입, 그리고 이를 위한 GIN(Generalized Inverted Index) 인덱스를 제공한다.

```sql
-- content 컬럼에 전문검색용 역색인(GIN)을 생성
CREATE INDEX idx_posts_content_fts
ON posts
USING GIN (to_tsvector('english', content));

-- '데이터베이스' 단어가 포함된 문서를 역색인으로 조회
-- (한국어는 별도 형태소 분석 확장이 필요하며, 여기서는 영문 예시로 원리만 보인다)
SELECT id, title
FROM posts
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'database');
```

`to_tsvector`는 본문을 토큰화·불용어 제거·어간 추출을 거쳐 정제된 단어 목록으로 변환하고, GIN 인덱스는 이 목록의 각 단어를 역색인의 키로 저장한다. `@@` 연산자는 이 인덱스를 이용해 검색어와 일치하는 문서를 O(log n)에 가까운 비용으로 찾는다 — `LIKE '%...%'`가 강제했던 Full Table Scan을 피할 수 있다.

## 비교: B-Tree 인덱스 vs 역색인

| 항목 | B-Tree 인덱스 | 역색인(Inverted Index) |
|---|---|---|
| 잘 맞는 조건 | 정확 일치, 범위 검색, 정렬 | 단어 포함 여부, 관련도 순위 |
| 저장 단위 | 컬럼 값 전체 | 토큰화된 개별 단어 |
| `LIKE '%word%'` | Full Table Scan | 인덱스로 직접 조회 |
| 대표 구현 | 대부분의 RDBMS 기본 인덱스 | PostgreSQL GIN, Elasticsearch, Lucene |

## 흔한 오개념

**"전문검색 인덱스는 B-Tree 인덱스를 대체한다"** — 둘은 서로 다른 질문에 답하는 도구다. B-Tree는 여전히 정확 일치·범위·정렬에 최적이고, 역색인은 단어 포함 여부와 관련도 순위 같은 질문에 최적이다. 실무에서는 같은 테이블에 두 종류를 함께 걸어, `customer_id` 조회는 B-Tree로, 본문 검색은 역색인으로 처리하는 경우가 흔하다.

**"단어 하나하나를 그대로 색인에 저장하면 된다"** — 정제 없이 원문 그대로 색인하면 "달리다"와 "달렸다"가 서로 다른 단어로 취급돼 검색이 누락되고, "은"·"는" 같은 조사·불용어까지 색인에 쌓여 크기만 커진다. 형태소 분석과 불용어 제거는 선택 사항이 아니라 역색인이 실용적으로 동작하기 위한 전처리 단계다.

## 다른 개념과의 연결

역색인의 단어→문서 매핑은 [해시테이블](/post/computerterms/hash-tables/) 챕터에서 다룬 키-값 조회의 응용이고, GIN 인덱스가 여러 문서 ID를 정렬된 목록으로 압축해 저장하는 방식은 [정규화와 인덱스](/post/computerterms/normalization-and-indexes/) 챕터에서 다룬 인덱스 설계의 트레이드오프(쓰기 비용 vs 조회 속도)를 그대로 따른다. 다음 챕터에서는 시간 순서로 계속 추가되기만 하는 데이터에 특화된 시계열 데이터베이스를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. B-Tree 인덱스가 본문 검색에 부적합한 이유와 `LIKE '%...%'`가 Full Table Scan으로 이어지는 과정을 설명할 수 있다. 역색인이 단어→문서 매핑으로 이 문제를 해결하는 원리와, 토큰화·불용어 제거·형태소 분석이 필요한 이유를 설명할 수 있다. 정확 일치·범위 조회에는 B-Tree를, 본문 검색에는 역색인을 선택하는 판단을 할 수 있다.

## 참고 자료

> "There are two kinds of indexes that can be used to speed up full text searches: GIN and GiST. ... GIN indexes are the preferred text search index type." — PostgreSQL Documentation, *12.9. Indexes for Text Search*

- [PostgreSQL Documentation: Full Text Search](https://www.postgresql.org/docs/current/textsearch.html) — `tsvector`/`tsquery`와 GIN 인덱스를 활용한 전문검색 공식 가이드
- [Elasticsearch Documentation: Inverted Index](https://www.elastic.co/guide/en/elasticsearch/guide/current/inverted-index.html) — 역색인 구조를 실무 검색 엔진 관점에서 설명하는 문서
