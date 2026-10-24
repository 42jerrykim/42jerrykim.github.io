---
title: "[PostgreSQL] Postgres가 느린 게 아니라 스토리지가 느린 것이다: EBS gp3 vs NVMe"
description: "ClickHouse가 정리한 POSETTE 2026 발표에서 같은 PostgreSQL이 EBS gp3에서 1,734 TPS, 로컬 NVMe에서 16,030 TPS를 냈다. 지연 분해로 원인을 읽고, 내구성 설계와 결과를 해석할 때의 한계를 정리한다."
date: 2026-10-25T00:30:00+09:00
lastmod: 2026-10-25
draft: false
categories:
  - PostgreSQL
  - Infrastructure
tags:
  - PostgreSQL
  - Database(데이터베이스)
  - Storage(저장소)
  - Vacuum
  - Replication(복제)
  - Backup
  - Benchmark
  - AWS(Amazon Web Services)
  - Performance(성능)
  - Latency(지연시간)
  - Case-Study
  - Deep-Dive
  - Architecture(아키텍처)
  - Linux(리눅스)
  - DevOps
  - Cloud(클라우드)
  - Optimization(최적화)
  - Open-Source(오픈소스)
  - Best-Practices
  - Scalability(확장성)
  - Reliability(신뢰성)
  - Infrastructure(인프라)
  - SQL
  - I/O
  - NVMe
  - EBS
  - WAL
  - WAL-G
  - pgbench
  - ClickHouse
  - Checkpoint
  - Fsync
  - High-Availability
  - Disaster-Recovery
  - Synchronous-Replication
  - Throughput
  - Trade-off
image: "wordcloud.png"
---

PostgreSQL이 쓰기 부하에서 느려지면 보통 인덱스를 손보거나 쿼리를 고치거나 `shared_buffers`를 올린다. ClickHouse 블로그가 2026년 8월 20일에 정리한 POSETTE 2026 발표(Sai Srirampur)는 다른 가설을 내놓는다. UPSERT 지연, P95 읽기 편차, autovacuum 지연, 느린 체크포인트, 논리 복제 지연처럼 흩어져 보이는 증상이 사실은 한 원인, 곧 스토리지 성능에서 나온다는 주장이다(출처: [ClickHouse 블로그](https://clickhouse.com/blog/posette-talk-recap-postgres-isnt-slow-your-storage-is)). 발표자가 속한 회사가 데이터베이스 벤더라는 점은 감안해야 하지만, 공개된 벤치마크 설정과 지연 분해가 구체적이라 숫자를 직접 따져 볼 수 있다. 이 글은 그 숫자가 무엇을 말하는지, 그리고 내 시스템에 옮길 때 무엇을 확인해야 하는지를 정리한다.

## 스토리지는 모두가 나눠 쓰는 예산이다

PostgreSQL 안에서 디스크를 쓰는 주체는 하나가 아니다. 클라이언트 쿼리가 데이터 페이지를 읽고, 커밋마다 WAL(Write-Ahead Log)을 `fsync`로 내려보내고, 체크포인트가 더러워진 페이지를 모아 쓰고, autovacuum이 죽은 튜플을 훑고, 논리 복제 슬롯이 WAL을 다시 읽는다. 이들은 서로 다른 프로세스지만 같은 디스크의 대역폭, IOPS, 큐 깊이를 나눠 쓴다. 한 주체가 예산을 많이 쓰면 나머지의 지연이 늘어난다.

그래서 스토리지가 느리면 증상이 여러 곳에서 동시에 나타난다. 읽기가 느려지는 것만이 아니라 커밋(WAL fsync)이 느려지고, 그 사이 락을 쥔 채 기다리는 시간이 늘고, 백그라운드 작업이 밀려 블로트가 쌓이며, 다시 읽기가 느려지는 순환이 생긴다. 발표의 핵심 논리는 이 공유 예산 구조다. 로컬 NVMe는 I/O를 없애지 않고 I/O 한 번의 비용을 줄여서 PostgreSQL이 I/O를 기다리며 보내는 시간을 줄인다(출처: 동일).

## 벤치마크 설정

비교는 동일한 클러스터 8개로 했다. 4개는 인스턴스 스토어 NVMe, 4개는 IOPS를 3,000으로 프로비저닝한 gp3 EBS를 썼고, 인스턴스는 모두 `m6id.4xlarge`(16 vCPU, 64 GiB, `shared_buffers` 16 GiB)다. 데이터는 `pgbench_accounts` 33억 행(482 GiB)이고, 64 클라이언트·16 스레드로 5분 동안 무작위 UPDATE를 실행했다. 스토리지 종류마다 4개씩 돌린 것은 실행 간 편차를 줄이려는 장치다(출처: 동일).

데이터셋 482 GiB가 메모리 캐시(`shared_buffers` 16 GiB, 인스턴스 RAM 64 GiB)보다 훨씬 크다는 점이 중요하다. 무작위로 고른 행의 페이지는 대부분 캐시에 없으므로 UPDATE마다 디스크에서 페이지를 읽어야 한다. 이 워크로드는 CPU가 아니라 스토리지의 지연을 직접 재도록 설계되어 있다.

| 지표 | NVMe | EBS gp3 | 차이 |
|------|------|---------|------|
| 중앙값 처리량 | 16,030 TPS | 1,734 TPS | 약 9.24배 |
| 중앙값 트랜잭션 지연 | 4.0 ms | 36.9 ms | 약 9.2배 |
| 10 GB 블로트 VACUUM | 366초 | 964초 | 약 2.6배 |
| 10 GB 논리 복제 백로그 해소 | 139초 | 238초 | 약 1.7배 |

(출처: ClickHouse 블로그. 배수는 표의 값에서 계산했다.)

## 숫자가 서로 맞는지 직접 확인하기

벤치마크 결과를 받으면 먼저 수치끼리 일관되는지 본다. 클라이언트가 64개이고 각자 한 트랜잭션이 끝나야 다음을 시작하는 닫힌 루프라면, 처리량은 대략 클라이언트 수를 트랜잭션 지연으로 나눈 값이 된다(리틀의 법칙). NVMe는 64 ÷ 0.0040초 = 16,000 TPS로 보고된 16,030에 맞고, EBS는 64 ÷ 0.0369초 ≈ 1,734 TPS로 보고값과 일치한다. 두 결과가 같은 식으로 설명되므로 처리량 차이의 전부가 트랜잭션당 지연의 차이다.

그렇다면 질문은 "그 36.9 ms가 어디서 오는가"로 바뀐다. 발표는 트랜잭션당 지연을 구성 요소로 분해했다.

| 구성 요소 | EBS | NVMe |
|-----------|-----|------|
| 페이지 읽기 | 약 19 ms | 약 0.3 ms |
| 커밋 시 WAL fsync | 약 11 ms | 약 1.5 ms |
| 락·스케줄러 오버헤드 | 약 5 ms | 약 0.2 ms |
| CPU 작업 | 약 2 ms | 약 2 ms |

(출처: 동일.) 합계는 EBS 약 37 ms, NVMe 약 4.0 ms로 표의 트랜잭션 지연과 맞는다. 눈여겨볼 점은 CPU 항목이 양쪽 모두 약 2 ms로 같다는 것이다. 연산량은 같고 대기만 다르다는 뜻이며, EBS에서는 지연의 절반 이상(19 ms)이 페이지 읽기이고 그다음이 WAL fsync(11 ms)다. 락·스케줄러 항목도 EBS에서 커지는데, 이는 I/O를 기다리는 동안 다른 백엔드가 쥔 락을 기다리는 시간이 늘어나기 때문으로 해석할 수 있다(이 해석은 원문이 직접 단정한 것이 아니라 항목 값에서 읽은 추론이다).

백엔드 대기 상태 스냅샷도 같은 방향이다. 특정 시점의 `pg_stat_activity`에서 64개 백엔드 중 EBS는 29개(약 45%)가 `IO:DataFileRead`를 기다렸고 NVMe는 9개(약 14%)였다. 다만 이는 한 시점의 스냅샷이지 실행 전체의 평균이 아니다. CPU 사용량도 NVMe 호스트가 약 240초 프로파일링 구간에 2,253 CPU초(코어 약 9.4개분)를 쓴 반면 EBS 호스트는 251 CPU초(약 1코어)였다(출처: 동일). EBS 쪽 CPU가 놀고 있다는 것은 병목이 CPU가 아님을 보여 주는 가장 직관적인 증거다.

## 한계: 이 숫자를 어디까지 일반화할 수 있나

원문 자신이 단서를 단다. 결과는 이 워크로드와 이 스토리지 구성에 한정되고, EBS 쪽은 3,000 IOPS의 기본 gp3였다. IOPS나 처리량을 더 높게 프로비저닝한 EBS(io2 등)는 결과가 다를 가능성이 크고, 비교가 "NVMe 대 EBS 일반"이 아니라 "NVMe 대 기본 사양 gp3"임을 기억해야 한다. 또한 작업이 무작위 UPDATE 위주라 읽기 대부분이 캐시에서 해결되는 워크로드에서는 격차가 훨씬 줄어든다. 발표도 NVMe가 I/O를 없애는 것이 아니라 비용을 줄인다고만 말한다(출처: 동일).

따라서 이 사례에서 가져갈 것은 "NVMe로 바꾸면 9배"라는 숫자가 아니라 진단 순서다. 내 시스템에서 `pg_stat_activity`의 대기 이벤트(`IO:DataFileRead`, `IO:WALSync` 등)가 두드러지고 CPU가 한가하다면 쿼리나 인덱스를 만지기 전에 스토리지 지연을 의심할 근거가 생긴다.

## 로컬 NVMe의 대가: 내구성을 어디서 확보하나

인스턴스 스토어 NVMe는 데이터 수명이 머신 수명에 묶인다. 노드를 잃으면 로컬 사본도 잃고, 인스턴스 스토어 볼륨은 EBS API로 스냅샷을 찍을 수도 없다(출처: 동일; [AWS 문서: 인스턴스 스토어](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)). 내구성을 디스크 한 장이 아니라 클러스터 단위로 올려야 한다는 뜻이다. 발표가 제안하는 구조는 세 겹이다.

- **고가용성**: 가용 영역을 나눠 배치한 스탠바이 2대와 쿼럼 기반 동기 복제를 쓴다. `synchronous_standby_names = 'ANY 1 (standby1, standby2)'`처럼 설정하면 커밋은 둘 중 하나의 확인만 기다리므로 한 스탠바이가 느려도 커밋이 멈추지 않는다(PostgreSQL의 동기 복제 설정은 [공식 문서](https://www.postgresql.org/docs/current/runtime-config-wal.html) 참고).
- **백업**: [WAL-G](https://github.com/wal-g/wal-g) 같은 도구로 물리 베이스 백업과 연속 WAL 아카이빙을 객체 스토리지로 보낸다. 목표는 초 단위 RPO와 보존 기간 내 시점 복구(PITR)다.
- **장애 도메인 분리**: 백업과 WAL은 데이터베이스 노드와 다른 장애 도메인에 둔다. 리전 전체 장애에 대비한다면 다른 리전에 사본을 더 둔다.

스탠바이는 빠른 페일오버를 맡고, 백업은 논리적 손상·운영자 실수·클러스터 전체 장애를 맡는다. 두 경로를 정기적으로 실제로 복구해 보는 것까지가 설계에 포함된다(출처: ClickHouse 블로그). 스탠바이 복제 구성의 일반 개념은 [PostgreSQL 문서의 웜 스탠바이 장](https://www.postgresql.org/docs/current/warm-standby.html)에 있다.

여기서 생기는 트레이드오프도 짚어 두자. 동기 복제를 쓰면 커밋 지연에 네트워크 왕복이 더해지므로, 로컬 fsync를 1.5 ms로 줄인 이득의 일부를 가용 영역 간 왕복 시간이 되가져갈 수 있다. 용량 계획도 달라진다. 디스크를 따로 늘릴 수 없고 인스턴스 타입이 제공하는 NVMe 용량 안에서 데이터 크기를 맞춰야 한다(출처: 동일). 이 구성은 운영 복잡도를 비용으로 내고 지연을 얻는 선택이다.

## 같은 방향의 다른 현장 사례

발표는 이미 NVMe 위에서 PostgreSQL을 운영하는 사례로 Instacart의 검색 인프라와 Datadog의 로컬 NVMe 운영을 든다. Datadog의 PGConf.US 2025 발표 자료는 [여기](https://postgresql.us/events/pgconfus2025/sessions/session/2064/slides/204/)에서 볼 수 있다. 원 발표 페이지는 [POSETTE 2026](https://posetteconf.com/2026/talks/postgres-isn-t-slow-your-storage-is/)이다. 반대 방향, 곧 객체 스토리지를 1차 저장소로 두고 계산을 분리하는 설계는 같은 공유 예산 문제를 다른 쪽에서 푸는 방식이며 최근 벡터 검색 쪽에서 많이 논의된다.

## 내 시스템에 적용하기 전 확인할 것

| 확인 항목 | 보는 방법 | 해석 |
|-----------|-----------|------|
| I/O 대기 비중 | `pg_stat_activity`의 `wait_event_type`/`wait_event`를 여러 번 샘플링 | `IO:DataFileRead`·`IO:WALSync`가 지속적으로 높으면 스토리지 의심 |
| CPU 여유 | 호스트 CPU 사용률 | 한가한데 지연이 크면 대기 병목 |
| 작업 집합 대 캐시 | 데이터 크기 대비 `shared_buffers`·RAM, 캐시 적중률 | 작업 집합이 메모리에 들어가면 스토리지 영향이 작다 |
| 프로비저닝 한도 | 볼륨의 IOPS·처리량 상한 대비 실제 사용량 | 상한에 붙어 있으면 볼륨 증설이 더 싼 처방일 수 있다 |
| 복구 절차 | 스탠바이 승격과 PITR을 실제로 수행 | 로컬 NVMe 전환의 전제 조건 |

스토리지를 바꾸기 전에 볼륨 사양을 올리는 쪽이 더 싸게 먹히는 경우도 많다. 이 발표는 "스토리지를 의심하라"는 진단 원칙을 주는 것이지, 로컬 NVMe가 항상 정답이라는 결론을 주지는 않는다.

## 정리

- 같은 PostgreSQL, 같은 인스턴스 타입에서 스토리지만 바꿔도 처리량이 약 9.24배(1,734 → 16,030 TPS), 트랜잭션 지연이 36.9 ms에서 4.0 ms로 달라졌다.
- 지연 분해에서 CPU 항목은 약 2 ms로 같았고, 차이는 페이지 읽기(19 ms 대 0.3 ms)와 WAL fsync(11 ms 대 1.5 ms)에서 났다. 보고된 처리량은 클라이언트 수 ÷ 지연으로 재현된다.
- autovacuum, 체크포인트, 논리 복제가 같은 I/O 예산을 나눠 쓰므로 스토리지 지연은 한 곳이 아니라 여러 증상으로 나타난다.
- 결과는 이 워크로드, 기본 사양 gp3(3,000 IOPS)와의 비교에 한정되며 벤더 자체 발표라는 점을 감안해야 한다.
- 로컬 NVMe는 내구성을 단일 노드가 아닌 쿼럼 동기 복제와 외부 WAL 아카이브로 옮겨야 쓸 수 있는 선택이다.

## 참고 및 출처

- [ClickHouse, "POSETTE Talk Recap - Postgres Isn't Slow. Your Storage Is" (2026-08-20)](https://clickhouse.com/blog/posette-talk-recap-postgres-isnt-slow-your-storage-is)
- [POSETTE 2026 발표 페이지](https://posetteconf.com/2026/talks/postgres-isn-t-slow-your-storage-is/)
- [Datadog, PGConf.US 2025 슬라이드](https://postgresql.us/events/pgconfus2025/sessions/session/2064/slides/204/)
- [WAL-G (GitHub)](https://github.com/wal-g/wal-g)
- [PostgreSQL 문서: WAL 설정](https://www.postgresql.org/docs/current/runtime-config-wal.html)
- [PostgreSQL 문서: 웜 스탠바이](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL 문서: pgbench](https://www.postgresql.org/docs/current/pgbench.html)
- [AWS 문서: EC2 인스턴스 스토어](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)
