---
image: "wordcloud.png"
slug: coroutines-and-async-await
collection_order: 77
draft: false
title: "[Computer Terms] 코루틴과 async/await (Coroutine, async/await)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "코루틴은 OS 스레드보다 훨씬 가벼운 사용자 수준 실행 단위로, I/O 대기 중 스레드를 블로킹하지 않고 다른 작업으로 전환합니다. Python asyncio의 async/await 코드로 이벤트 루프의 전환 원리를 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Async(비동기)
- Coroutine(코루틴)
- asyncio
- Python
- Thread
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
- Debugging(디버깅)
- Performance(성능)
- Event-Loop(이벤트루프)
- Operating-System(운영체제)
- I/O(입출력)
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 OS 스레드가 커널이 관리하는 실행 단위이고, 스레드 하나를 만들고 전환하는 데도 커널 개입 비용이 든다고 다뤘다. 이 챕터는 그 비용을 줄이기 위해 등장한, 사용자 공간에서 관리되는 더 가벼운 실행 단위를 다룬다.

## 스레드가 너무 무거워지는 지점

웹 서버가 동시에 만 개의 클라이언트 연결을 처리해야 한다고 하자. 연결마다 OS 스레드를 하나씩 배정하면, 스레드마다 수백 KB에서 수 MB의 스택 메모리를 차지하고 스레드 전환마다 커널 모드 진입·컨텍스트 스위칭 비용이 든다. 게다가 각 연결의 대부분 시간은 실제 계산이 아니라 네트워크 응답을 **기다리는** 데 쓰인다 — 이 대기 중에도 스레드는 자원을 점유한 채 스케줄러의 관리 대상으로 남는다.

<strong>코루틴(Coroutine)</strong>은 이 문제를 위해 등장한, 실행을 중단했다가 나중에 정확히 그 지점부터 재개할 수 있는 함수 단위다. 스레드와 달리 커널이 아니라 언어 런타임(또는 라이브러리)이 직접 스케줄링하므로 생성·전환 비용이 훨씬 낮고, 수만 개를 동시에 띄워도 부담이 적다. 코루틴이 I/O 완료를 기다려야 할 때는 OS 스레드를 블로킹하는 대신 <strong>자신의 실행을 양보(yield)</strong>하고, 런타임은 그 스레드에서 대기 중인 다른 코루틴을 대신 실행한다 — I/O가 끝나면 원래 코루틴이 멈췄던 지점부터 다시 이어받는다. 즉 코루틴 자체는 "협력적으로 양보하는 실행 단위"라는 일반 개념이고, 스레드 위에서 여러 코루틴이 번갈아 실행되는 구조다.

## async/await: 전환을 문법으로 감추기

**`async`/`await`**는 코루틴을 다루는 문법으로, "이 지점에서 실행을 양보하고 결과가 오면 재개하라"는 지시를 명시적인 콜백 대신 마치 동기 코드처럼 순차적으로 읽히게 해준다. Python의 `asyncio`가 대표적인 구현이다.

```python
import asyncio
import time


async def fetch_data(name: str, delay: float) -> str:
    print(f"{name}: 요청 시작")
    await asyncio.sleep(delay)   # I/O 대기를 흉내: 이 지점에서 실행을 양보
    print(f"{name}: 응답 도착")
    return f"{name}의 결과"


async def main() -> None:
    start = time.perf_counter()

    # 세 코루틴을 동시에 스케줄링: 하나가 대기하는 동안 다른 것이 진행된다
    results = await asyncio.gather(
        fetch_data("A", 1.0),
        fetch_data("B", 1.0),
        fetch_data("C", 1.0),
    )

    elapsed = time.perf_counter() - start
    print(results)
    print(f"총 소요 시간: {elapsed:.1f}초")  # 3.0초가 아니라 약 1.0초


if __name__ == "__main__":
    asyncio.run(main())
```

`python coroutine_demo.py`로 실행하면 세 호출을 순서대로 `await`했다면 3초가 걸렸을 작업이 약 1초 만에 끝난다. `asyncio.sleep(delay)`를 만나는 순간 `fetch_data` 코루틴은 실행을 멈추고 제어권을 <strong>이벤트 루프(Event Loop)</strong>에 돌려준다. 이벤트 루프는 그동안 대기 상태인 다른 코루틴이 있는지 확인해 실행하고, `delay` 시간이 지나면 원래 코루틴을 정확히 `await` 다음 줄부터 재개한다. 이 모든 전환이 단일 OS 스레드 안에서 일어난다는 점이 핵심이다 — 스레드를 여러 개 만들지 않고도 동시에 여러 I/O 대기를 겹쳐 처리한 것이다.

`async def`로 선언한 함수는 호출해도 즉시 실행되지 않고 **코루틴 객체**만 생성한다는 점도 코드를 읽을 때 자주 놓치는 부분이다. 실제 실행은 `await`로 그 코루틴을 대기하거나, `asyncio.run`·`asyncio.gather`처럼 이벤트 루프에 스케줄링해야 시작된다.

| 항목 | OS 스레드 | 코루틴(async/await) |
|---|---|---|
| 스케줄러 | 커널 | 언어 런타임(이벤트 루프) |
| 전환 비용 | 상대적으로 높음(컨텍스트 스위칭) | 낮음(함수 호출 수준) |
| 동시 개수 | 수백–수천 단위에서 한계 | 수만 개 이상도 실용적 |
| 전환 시점 | 스케줄러가 강제로 뺏음(선점형) | 코루틴이 `await`에서 스스로 양보(협력형) |
| CPU 바운드 작업 | 여러 코어 활용 가능(GIL 없는 언어 기준) | 단일 스레드 이벤트 루프에서는 병렬 계산에 부적합 |

## 흔한 오개념

**"async/await를 쓰면 병렬로 실행된다"** — Python `asyncio`의 코루틴은 기본적으로 **단일 스레드**에서 번갈아 실행된다. 위 예시가 빨라진 이유는 I/O 대기 시간이 겹쳤기 때문이지, CPU 연산이 동시에 여러 코어에서 돌았기 때문이 아니다. 순수 계산량이 많은 작업(CPU 바운드)을 `async` 함수로 감싸도 이벤트 루프를 계속 점유해 다른 코루틴이 실행될 기회를 얻지 못하고, 오히려 전체 응답성이 나빠질 수 있다 — 이런 작업은 별도 스레드/프로세스로 넘기는 것이 정석이다.

**"await를 빠뜨려도 함수는 실행된다"** — `fetch_data("A", 1.0)`처럼 `await` 없이 코루틴 함수를 호출하면 코루틴 객체만 생성될 뿐 내부 코드는 한 줄도 실행되지 않는다. Python은 이 경우 "코루틴이 await되지 않았다(coroutine was never awaited)"는 런타임 경고를 출력하는데, 초심자가 이 경고를 무시하면 왜 함수가 동작하지 않는지 오래 헤매게 된다.

## 다른 개념과의 연결

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 다룬 커널 스케줄링과 이 챕터의 이벤트 루프 스케줄링은 "누가 실행 전환을 결정하는가"(커널 vs 런타임)라는 축에서 대비된다. 다음 챕터에서는 이 코루틴들이 실제로 몇 개의 OS 스레드 위에서 실행되는지를 결정하는 스레드풀을 다룬다 — 많은 비동기 런타임이 내부적으로 스레드풀 위에서 이벤트 루프를 돌린다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 코루틴이 OS 스레드보다 가벼운 이유와, I/O 대기 중 실행을 양보하는 원리를 설명할 수 있다. `async`/`await`가 콜백 대신 순차적 코드처럼 비동기 흐름을 표현하는 방식을 설명할 수 있다. async/await가 CPU 바운드 작업에는 부적합한 이유를 병렬성과 동시성의 차이로 설명할 수 있다.

## 참고 자료

> Selivanov, Y. (2015). "PEP 492 – Coroutines with async and await syntax". Python Enhancement Proposals. (BDFL Guido van Rossum이 승인.)

- [Python docs: Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — `async`/`await`, `gather`, 이벤트 루프 공식 문서
- [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/) — Python에 async/await 문법이 도입된 원 제안서
