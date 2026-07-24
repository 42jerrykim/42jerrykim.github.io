---
image: "wordcloud.png"
slug: time-series-databases
collection_order: 69
draft: false
title: "[Computer Terms] 시계열 데이터베이스 (Time-Series Database)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "시계열 데이터베이스는 시간 순서로 계속 추가되기만 하는 데이터에 최적화된 저장소입니다. 시간 기준 파티셔닝과 델타 인코딩이 압축률·쓰기 처리량을 높이는 원리를 다루고, 오래된 파티션을 통째로 폐기해 삭제 비용을 줄이는 실무 이점까지 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Database(데이터베이스)
- Time-Series-Database(시계열데이터베이스)
- SQL(Structured Query Language)
- Storage(저장소)
- Monitoring(모니터링)
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
- Data-Structure(자료구조)
- Data-Integrity(데이터무결성)
- Compression(압축)
---

## 이 장을 읽기 전에

[NoSQL과 쿼리 최적화](/post/computerterms/nosql-and-query-optimization/)에서 다룬 NoSQL 네 갈래(문서·키-값·컬럼·그래프)와, [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 인덱스·B-Tree 원리를 안다고 가정한다. 이 챕터는 특정 워크로드(시간순 데이터)에 극단적으로 최적화된 별도 계열의 데이터베이스를 다룬다.

## 시계열 데이터의 독특한 접근 패턴

센서 로그, 서버 CPU 사용률, 주가처럼 **시간이 지날수록 계속 새 데이터가 추가되기만 하는 데이터**를 **시계열 데이터(Time-Series Data)**라 부른다. 이 데이터는 몇 가지 뚜렷한 접근 패턴을 갖는다. 쓰기는 거의 항상 "지금 시각"에 대한 새 행 추가이며, 이미 기록된 과거 값을 수정하는 경우는 드물다. 조회는 "최근 1시간 CPU 사용률 추이"처럼 특정 시간 구간을 범위로 묻는 경우가 대부분이고, 개별 레코드 하나를 정확히 찾는 조회는 드물다. 값 자체도 시간에 따라 완만하게 변하는 경우가 많아 이웃한 값들끼리 유사도가 높다.

일반 RDBMS는 이런 패턴에 최적화돼 있지 않다. 임의의 컬럼으로 갱신·삭제될 수 있다는 가정 위에 설계된 범용 저장 엔진과 인덱스 구조를 그대로 쓰면, 초당 수만–수십만 건씩 쏟아지는 쓰기를 감당하지 못하거나, 저장 공간이 감당하기 어려운 속도로 불어난다. **시계열 데이터베이스(Time-Series Database, TSDB)**는 이 접근 패턴 하나에 맞춰 저장 엔진 자체를 다시 설계한 시스템이다.

## 시간 기준 파티셔닝: 오래된 데이터를 통째로 다룬다

TSDB는 데이터를 시간 구간(예: 1일, 1시간) 단위의 **파티션(청크)**으로 나눠 저장한다. 새로 들어오는 데이터는 항상 가장 최근 파티션에만 쓰이므로, 쓰기가 여러 파티션에 흩어지지 않고 한 곳에 집중돼 디스크 순차 쓰기에 가까운 패턴이 된다. 조회할 때도 "최근 1시간" 같은 시간 범위 조건이 오면, 그 구간을 포함하지 않는 파티션은 아예 열어보지 않고 건너뛸 수 있어 검색 범위가 크게 줄어든다. 오래된 데이터를 삭제할 때도 개별 행을 하나씩 지우는 대신 통째로 만료된 파티션 파일을 삭제하기만 하면 되므로, 일반 RDBMS의 `DELETE` 문보다 훨씬 저렴하다.

## 델타 인코딩: 이웃한 값의 차이만 저장한다

시계열 값은 이웃한 값끼리 비슷한 경우가 많다는 성질을 압축에 활용할 수 있다. **델타 인코딩(Delta Encoding)**은 각 값을 있는 그대로 저장하는 대신, 바로 앞 값과의 **차이(delta)**만 저장한다. 타임스탬프처럼 거의 일정한 간격으로 증가하는 값은 이 차이가 대부분 같은 값으로 반복되므로 압축 효율이 매우 높아진다.

```text
원본 값(초 단위 타임스탬프): 1700000000, 1700000010, 1700000020, 1700000030
델타 인코딩:                1700000000, +10,        +10,        +10
```

측정값(예: 온도)에도 비슷한 원리가 적용된다. 값이 41.2, 41.3, 41.1처럼 완만하게 변한다면, 차이값 +0.1, -0.2만 저장하는 것이 원본 값을 매번 저장하는 것보다 훨씬 적은 바이트를 차지한다. 실제 TSDB(Prometheus, InfluxDB 등)는 델타 인코딩에 더해 XOR 기반 부동소수점 압축이나 가변 길이 정수 인코딩 같은 기법을 함께 적용해 압축률을 추가로 높인다.

## 비교: 일반 RDBMS vs 시계열 데이터베이스

| 항목 | 일반 RDBMS | 시계열 데이터베이스 |
|---|---|---|
| 주 쓰기 패턴 | 임의 위치 갱신·삭제 포함 | 최신 시점에 순차 추가 |
| 파티셔닝 | 선택 사항 | 시간 구간 기준 기본 전제 |
| 압축 | 범용 압축(선택) | 델타 인코딩 등 시계열 특화 압축 |
| 오래된 데이터 삭제 | 행 단위 `DELETE` | 파티션 단위 폐기 |
| 대표 사용처 | 트랜잭션 처리(OLTP) | 모니터링, IoT, 메트릭 저장 |

## 흔한 오개념

**"시계열 데이터베이스는 그냥 타임스탬프 컬럼이 있는 테이블이다"** — 타임스탬프 컬럼 자체는 일반 RDBMS 테이블에도 얼마든지 둘 수 있다. TSDB를 구분 짓는 것은 컬럼 유무가 아니라, 시간 기준 파티셔닝·델타 인코딩처럼 "거의 항상 최신 시점에 추가되고, 시간 범위로 조회되며, 값이 이웃끼리 유사하다"는 접근 패턴 자체를 저장 엔진 설계의 전제로 삼았는지 여부다.

**"시계열 데이터베이스는 범용 데이터베이스를 완전히 대체한다"** — TSDB는 시계열 워크로드 하나에 극단적으로 최적화된 대신, 임의의 행을 개별적으로 갱신하거나 복잡한 다중 테이블 조인이 필요한 워크로드에는 잘 맞지 않는다. 실무에서는 트랜잭션 데이터는 RDBMS에, 그 시스템에서 나오는 메트릭·로그는 TSDB에 저장하는 식으로 워크로드별로 데이터베이스를 나눠 쓰는 경우가 흔하다.

## 다른 개념과의 연결

시간 기준 파티셔닝은 [샤딩과 복제](/post/computerterms/sharding-and-replication/) 챕터에서 다룬 데이터 분산 전략의 한 형태이고, TSDB가 감당해야 하는 초당 대량 쓰기는 [캐싱과 무효화](/post/computerterms/caching-and-invalidation/) 챕터에서 다룬 쓰기 우선 워크로드의 극단적인 사례다. 데이터베이스 심화 갈래는 이 챕터로 마무리되며, 다음은 이렇게 여러 서버에 나눠 담긴 데이터가 서로 사건 발생 순서를 어떻게 판단하는지 다루는 [벡터 시계](/post/computerterms/vector-clocks/)를 시작으로 분산 시스템 갈래로 이어진다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 시계열 데이터의 접근 패턴(순차 쓰기, 시간 범위 조회, 값의 유사성)이 일반 RDBMS와 왜 잘 맞지 않는지 설명할 수 있다. 시간 기준 파티셔닝이 쓰기 처리량과 오래된 데이터 삭제 비용을 어떻게 줄이는지 설명할 수 있다. 델타 인코딩이 압축률을 높이는 원리를 예시로 설명할 수 있다. 워크로드 특성에 따라 RDBMS와 TSDB 중 무엇을 선택할지 판단할 수 있다.

## 참고 자료

> "Prometheus's local time series database stores data in a custom, highly efficient format on local storage." — Prometheus Documentation, *Storage*

- [Prometheus Documentation: Storage](https://prometheus.io/docs/prometheus/latest/storage/) — 시간 기준 블록 파티셔닝과 압축을 다루는 대표적인 오픈소스 TSDB 공식 문서
- [InfluxData: What is Time Series Data?](https://www.influxdata.com/what-is-time-series-data/) — 시계열 데이터의 특성과 전용 데이터베이스가 필요한 이유를 설명하는 자료
