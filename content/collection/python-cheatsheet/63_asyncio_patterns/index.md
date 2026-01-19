---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 63. asyncio - 비동기 최소 패턴"
slug: "async-io-patterns-concurrency-coroutine-async-await-guide"
description: "파이썬 비동기 프로그래밍을 빠르게 시작하기 위한 치트시트입니다. async/await 기본 문법, asyncio.run/gather/create_task, 타임아웃, 동기 코드와의 혼용 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 63
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - asyncio
  - async
  - await
  - 비동기
  - asynchronous
  - coroutine
  - 코루틴
  - event-loop
  - 이벤트루프
  - gather
  - create_task
  - Task
  - Future
  - run
  - wait_for
  - timeout
  - 타임아웃
  - concurrency
  - 동시성
  - io-bound
  - networking
  - 네트워킹
  - http
  - aiohttp
  - performance
  - 성능
  - blocking
  - non-blocking
  - synchronous
  - 동기
  - sleep
  - queue
  - AsyncIterator
  - async-generator
  - context-manager
  - 컨텍스트매니저
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - debugging
  - 디버깅
  - standard-library
  - 표준라이브러리
  - python38
  - python39
  - python310
---
asyncio는 I/O 바운드 작업을 효율적으로 처리하는 파이썬의 비동기 프레임워크입니다. 이 치트시트는 async/await 기본, gather로 동시 실행, 타임아웃 처리, 동기 코드와 혼용 시 주의점을 정리합니다.

## 언제 이 치트시트를 보나?

- 네트워크 요청, 파일 I/O 등 **대기 시간이 긴 작업**을 동시에 처리하고 싶을 때
- `async def`/`await`를 처음 써보거나 문법이 헷갈릴 때

## 핵심 패턴

- 진입점: `asyncio.run(main())` (Py3.7+)
- 동시 실행: `await asyncio.gather(coro1(), coro2())`
- 백그라운드 태스크: `task = asyncio.create_task(coro())`
- 타임아웃: `await asyncio.wait_for(coro(), timeout=5.0)`
- 동기 함수 호출: `await asyncio.to_thread(blocking_func, arg)` (Py3.9+)

## 최소 예제

```python
import asyncio

async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # I/O 대기 시뮬레이션
    return f"{name} done"

async def main():
    # 동시 실행 (총 ~1초)
    results = await asyncio.gather(
        fetch("A", 1.0),
        fetch("B", 1.0),
    )
    print(results)

asyncio.run(main())
```

```python
# 타임아웃
async def main():
    try:
        result = await asyncio.wait_for(fetch("slow", 5.0), timeout=2.0)
    except asyncio.TimeoutError:
        print("timeout!")

asyncio.run(main())
```

```python
# 동기 블로킹 함수를 스레드에서 실행 (Py3.9+)
import time

def blocking_io():
    time.sleep(1)
    return "done"

async def main():
    result = await asyncio.to_thread(blocking_io)
    print(result)

asyncio.run(main())
```

## 자주 하는 실수/주의점

- **동기 함수에서 `await` 호출 불가** → `async def` 안에서만 `await` 사용
- **블로킹 코드**(time.sleep, requests 등)는 이벤트 루프를 멈춤 → `asyncio.to_thread()` 또는 비동기 라이브러리(aiohttp 등) 사용
- `asyncio.run()`은 **새 이벤트 루프를 만듦** → 이미 루프가 있는 환경(Jupyter 등)에서는 `await main()` 직접 사용
- `gather()`에서 예외가 나면 다른 태스크도 취소될 수 있음 → `return_exceptions=True` 옵션 고려

## 관련 링크(공식 문서)

- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
