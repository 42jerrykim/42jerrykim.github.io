---
image: "wordcloud.png"
slug: write-through-and-write-back
collection_order: 82
draft: false
title: "[Computer Terms] Write-Through와 Write-Back"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "캐시에 쓸 때 원본에 즉시 반영하는 Write-Through와, 캐시에만 먼저 쓰고 나중에 반영하는 Write-Back의 트레이드오프를 ACID의 영속성 개념과 연결해 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Caching(캐싱)
- Cache(캐시)
- ACID(Atomicity Consistency Isolation Durability)
- Durability(지속성)
- Redis
- Memory(메모리)
- Database(데이터베이스)
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
- Distributed-Systems(분산시스템)
- Computer-Architecture(컴퓨터구조)
- Performance(성능)
- System-Design(시스템설계)
---

## 이 장을 읽기 전에

[멀티레벨 캐싱](/post/computerterms/multilevel-caching/)에서 다룬 Cache-Aside 패턴(읽기 시 캐시를 먼저 확인하고 미스면 원본을 조회해 채우는 방식)과, [ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 영속성(Durability, 커밋된 데이터는 장애가 나도 사라지지 않아야 한다는 성질)을 안다고 가정한다. 지금까지는 "읽기"만 다뤘다면, 이 챕터는 "캐시에 쓰기"가 들어올 때 원본을 언제 갱신할지의 문제를 다룬다.

## 쓰기가 캐시에 들어오면 생기는 새로운 문제

Cache-Aside는 읽기 전용이라면 단순하다 — 캐시에 없으면 원본을 보고 채워 넣으면 그만이다. 하지만 애플리케이션이 캐시에 값을 **쓰는** 경우, 즉 사용자 프로필을 갱신하거나 장바구니에 상품을 추가하는 경우에는 새로운 질문이 생긴다. 캐시에 쓴 값을 원본(디스크, 데이터베이스)에도 반영해야 하는데, **그 반영을 언제 할 것인가**다. 이 질문에 대한 두 가지 상반된 답이 **Write-Through**와 **Write-Back**이다.

## Write-Through: 쓸 때마다 원본까지 함께 쓴다

**Write-Through**는 캐시에 값을 쓰는 동시에 원본에도 즉시 같은 값을 쓰고, 두 쓰기가 모두 끝나야 쓰기 작업이 완료된 것으로 간주한다. 이 방식의 장점은 단순함과 안전성이다 — 캐시와 원본이 항상 같은 상태를 유지하므로, 캐시가 갑자기 죽어도 원본에는 이미 최신 데이터가 있어 데이터 손실이 없다. 단점은 느리다는 것이다. 모든 쓰기 요청이 원본(대개 디스크 기반이라 느린)의 응답을 기다려야 완료되므로, 캐시를 두는 이유였던 "빠른 응답"이 쓰기 경로에서는 사라진다.

```python
def write_through_update(cache, db, key: str, value: dict) -> None:
    db.save(key, value)      # 1. 원본(디스크)에 먼저 쓰고 커밋될 때까지 대기
    cache.set(key, value)    # 2. 원본 쓰기가 성공한 뒤에야 캐시를 갱신
    # 두 쓰기가 모두 끝나야 함수가 반환된다 — 호출자는 그동안 대기한다
```

원본 쓰기를 먼저 완료한 뒤 캐시를 갱신하는 순서를 지키는 이유는, 만약 캐시를 먼저 갱신하고 원본 쓰기가 실패하면 캐시와 원본이 서로 다른 값을 갖는 불일치 상태에 빠지기 때문이다. Write-Through는 이 불일치 위험을 "느리더라도 항상 원본을 기준으로 동기화한다"는 원칙으로 없앤다.

## Write-Back: 캐시에만 먼저 쓰고 나중에 원본에 반영한다

**Write-Back(또는 Write-Behind)**은 캐시에만 값을 쓰고 즉시 쓰기 완료로 응답한 뒤, 원본에는 나중에(주기적으로, 또는 캐시에서 그 항목이 밀려날 때) 몰아서 반영한다. 장점은 빠르다는 것이다 — 쓰기 요청이 원본의 느린 디스크 I/O를 기다리지 않고 캐시(메모리)에만 쓰면 끝나므로, 응답 속도가 Write-Through보다 자릿수 단위로 빠르다. 여러 번의 쓰기를 한 번의 원본 쓰기로 묶어서(batching) 원본에 걸리는 부하도 줄일 수 있다. 단점은 **캐시가 원본에 반영되기 전에 장애로 죽으면, 아직 반영되지 않은 데이터가 영구히 사라진다**는 것이다.

```python
import time

pending_writes = {}  # 캐시에만 반영되고 원본에는 아직 안 쓰인 값들

def write_back_update(cache, key: str, value: dict) -> None:
    cache.set(key, value)          # 1. 캐시에만 쓰고 즉시 반환
    pending_writes[key] = value    # 2. 나중에 원본에 반영할 항목으로 표시

def flush_to_origin(db) -> None:
    """주기적으로(예: 5초마다) 호출해 밀린 쓰기를 원본에 한꺼번에 반영한다."""
    for key, value in list(pending_writes.items()):
        db.save(key, value)
        del pending_writes[key]
```

이 `pending_writes`에 있는 동안, 즉 `flush_to_origin`이 아직 실행되기 전에 캐시 프로세스가 크래시하면 그 데이터는 원본 어디에도 남지 않은 채 사라진다. 이것이 Write-Back의 근본적인 트레이드오프다 — 속도를 얻는 대가로 "커밋된 것처럼 보였던 데이터가 실제로는 지속되지 않을 수 있다"는 위험을 감수한다.

## ACID의 영속성과 연결해서 보면

[ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 **영속성(Durability)**은 "커밋이 완료됐다고 응답한 데이터는 이후 장애가 나도 사라지지 않아야 한다"는 보장이다. Write-Through는 원본에 쓰기가 끝나야 완료로 응답하므로 이 영속성 보장을 그대로 만족한다 — 응답을 받은 시점에 이미 데이터는 디스크에 있다. 반면 Write-Back은 캐시에만 쓴 시점에 완료로 응답하기 때문에, 그 순간의 "완료"는 영속성을 보장하지 않는 **약속 위반(또는 의도적 완화)**이다. 실무에서 Write-Back을 쓰는 시스템(예: 디스크 컨트롤러의 쓰기 캐시, 일부 데이터베이스의 비동기 복제)은 이 위험을 배터리 백업 메모리, WAL(Write-Ahead Log), 복제본 다중화 같은 별도 장치로 보완해 완화한다.

## 비교: Write-Through vs Write-Back

| 특성 | Write-Through | Write-Back |
|---|---|---|
| 쓰기 완료 시점 | 원본까지 쓴 후 | 캐시에 쓴 직후 |
| 쓰기 지연 | 높음(원본 I/O 대기) | 낮음(메모리만 대기) |
| 캐시 장애 시 데이터 손실 | 없음 | 반영 안 된 데이터 손실 가능 |
| 원본 부하 | 요청마다 발생 | 배칭으로 감소 |
| 영속성(Durability) 보장 | 응답 시점에 보장 | 응답 시점에는 보장 안 됨 |
| 대표 사례 | 은행 잔액 갱신, 결제 기록 | 디스크 컨트롤러 쓰기 캐시, 로그 수집 파이프라인 |

## 흔한 오개념

**"Write-Back은 항상 위험하니 쓰면 안 된다"** — Write-Back의 데이터 손실 위험은 "허용 가능한 손실 범위"에 따라 판단해야 하는 트레이드오프지, 절대적으로 피해야 할 결함이 아니다. 로그 수집이나 조회수 카운터처럼 몇 초 분량의 데이터가 유실돼도 치명적이지 않은 경우라면 Write-Back의 속도 이점이 훨씬 크다. 반대로 결제·재고처럼 한 건의 유실도 허용할 수 없는 데이터는 Write-Through를 쓰거나, Write-Back에 WAL 같은 보완 장치를 반드시 함께 둔다.

**"캐시에 썼으면 이미 저장된 것이다"** — 캐시(메모리)에 값이 있다는 것과, 그 값이 영속적으로 저장됐다는 것은 다른 문제다. Write-Back 구조에서는 캐시에 값이 존재해도 원본에 반영되기 전까지는 프로세스 크래시나 정전에 취약한 상태다. "저장됐다"는 표현은 항상 "어느 계층까지 저장됐는가"를 명시해야 한다.

## 다른 개념과의 연결

Write-Through와 Write-Back은 [멀티레벨 캐싱](/post/computerterms/multilevel-caching/)에서 다룬 Cache-Aside 패턴의 "쓰기 버전"에 해당하며, 그 트레이드오프의 본질은 [ACID Transactions](/post/computerterms/acid-transactions/)의 영속성 보장을 캐시 계층에서 얼마나 엄격하게 지킬 것인가의 문제로 귀결된다. 이것으로 캐싱 갈래의 세 챕터(CDN 캐싱, 멀티레벨 캐싱, Write-Through/Write-Back)는 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 시작한 "느린 원본 대신 빠른 사본을 먼저 본다"는 원리를 규모(전 세계 CDN), 구조(다단계 계층), 방향(쓰기 반영 시점)의 세 축으로 각각 확장한 셈이다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. Write-Through와 Write-Back의 쓰기 완료 시점 차이를 설명할 수 있다. 각 방식이 데이터 손실 위험과 쓰기 지연 사이에서 어떤 트레이드오프를 갖는지 비교할 수 있다. 주어진 데이터 특성(허용 가능한 손실 범위)에 따라 어느 방식을 선택할지 판단하고, 그 선택을 ACID의 영속성 개념과 연결해 설명할 수 있다.

## 참고 자료

Härder, T., & Reuter, A. (1983)는 *Principles of Transaction-Oriented Database Recovery*(ACM Computing Surveys, 15(4), 287–317)에서 ACID라는 용어를 처음 제시하며, 영속성(Durability)을 커밋된 트랜잭션의 결과가 이후 시스템 장애에도 남아있어야 하는 성질로 정의했다.

- [Redis: Caching Solutions](https://redis.io/solutions/caching/) — 애플리케이션 캐시에서의 쓰기 전략 실무 가이드
- [MDN Web Docs: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) — 캐시 쓰기·재검증 지시자에 대한 참조
