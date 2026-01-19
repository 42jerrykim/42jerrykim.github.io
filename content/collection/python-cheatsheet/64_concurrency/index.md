---

image: "wordcloud.png"
title: "[Python Cheatsheet] 64. Concurrency - threading/multiprocessing 선택"
slug: "concurrency-guide-threading-vs-multiprocessing-explained-fast"
description: "동시성과 병렬성을 빠르게 선택하기 위한 치트시트입니다. GIL 이해, I/O-bound vs CPU-bound 판단, ThreadPoolExecutor/ProcessPoolExecutor, 데이터 공유 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 64
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - concurrency
  - 동시성
  - parallelism
  - 병렬성
  - threading
  - 스레드
  - Thread
  - multiprocessing
  - 멀티프로세싱
  - Process
  - GIL
  - Global-Interpreter-Lock
  - io-bound
  - cpu-bound
  - ThreadPoolExecutor
  - ProcessPoolExecutor
  - concurrent.futures
  - executor
  - submit
  - map
  - Future
  - Lock
  - Queue
  - 큐
  - synchronization
  - 동기화
  - race-condition
  - 경쟁상태
  - deadlock
  - 데드락
  - shared-state
  - performance
  - 성능
  - scalability
  - 확장성
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - debugging
  - 디버깅
  - standard-library
  - 표준라이브러리
  - asyncio
  - 비동기
---
동시성(concurrency)과 병렬성(parallelism)은 성능 향상의 핵심 도구입니다. 이 치트시트는 GIL 이해, I/O vs CPU 바운드 판단, ThreadPoolExecutor/ProcessPoolExecutor 선택 기준을 정리합니다.

## 언제 이 치트시트를 보나?

- 여러 작업을 **동시에** 처리해서 속도를 올리고 싶을 때
- "threading vs multiprocessing vs asyncio" 선택이 헷갈릴 때

## 핵심 패턴

- **I/O-bound**(네트워크/파일 대기): `ThreadPoolExecutor` 또는 `asyncio`
- **CPU-bound**(계산 집약): `ProcessPoolExecutor` (GIL 우회)
- 간단한 병렬화: `concurrent.futures`의 `executor.map()` 또는 `executor.submit()`
- 데이터 공유는 최소화 → 필요하면 `Queue`, `Lock` 사용

## 최소 예제

```python
# I/O-bound: ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import time

def fetch(url: str) -> str:
    time.sleep(1)  # 네트워크 대기 시뮬레이션
    return f"fetched {url}"

with ThreadPoolExecutor(max_workers=4) as executor:
    urls = ["a", "b", "c", "d"]
    results = list(executor.map(fetch, urls))  # 병렬 실행 (~1초)
    print(results)
```

```python
# CPU-bound: ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def heavy_compute(n: int) -> int:
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        nums = [10**6, 10**6, 10**6, 10**6]
        results = list(executor.map(heavy_compute, nums))
        print(results)
```

```python
# submit + Future
from concurrent.futures import ThreadPoolExecutor, as_completed

def task(n):
    return n * 2

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, i) for i in range(5)]
    for future in as_completed(futures):
        print(future.result())
```

## GIL 이해

- **GIL(Global Interpreter Lock)**: CPython에서 한 번에 하나의 스레드만 파이썬 바이트코드 실행
- I/O 대기 중에는 GIL 해제 → **I/O-bound 작업은 threading이 효과적**
- CPU 연산 중에는 GIL 유지 → **CPU-bound 작업은 multiprocessing 필요**

## 자주 하는 실수/주의점

- **ProcessPoolExecutor**는 `if __name__ == "__main__":` 가드 필수 (Windows)
- 스레드/프로세스 간 **가변 객체 공유**는 버그 원인 → 불변 데이터 전달 또는 Queue 사용
- 프로세스는 메모리 복사 비용이 큼 → 작은 작업에는 오버헤드
- `executor.shutdown(wait=True)`는 `with` 문 사용 시 자동 호출됨

## 선택 가이드

| 상황 | 추천 |
|------|------|
| 네트워크 요청 다수 | `asyncio` 또는 `ThreadPoolExecutor` |
| 파일 I/O 다수 | `ThreadPoolExecutor` |
| CPU 계산 집약 | `ProcessPoolExecutor` |
| 간단한 백그라운드 작업 | `threading.Thread` |

## 관련 링크(공식 문서)

- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
