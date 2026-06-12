---
title: "[Concurrency Patterns] 06. 실행 관리 I: Thread Pool"
description: "스레드 풀, 작업 큐, Work Stealing 알고리즘을 구현하고, 부하 분산과 응답성의 트레이드오프를 학습합니다."
date: 2026-06-16
lastmod: 2026-06-17
draft: false
collection_order: 6
difficulty: intermediate-advanced
prerequisites:
  - "02~04장: 락, condition_variable, Producer-Consumer"
  - "std::function과 람다 표현식"
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Thread-Pool
  - Work-Queue
  - Work-Stealing
  - Task-Scheduling
  - Load-Balancing
  - Thread-Management
  - Executor
  - BoundedQueue
  - Throughput
  - Latency
  - Performance
  - 성능
  - Design-Pattern
  - 디자인패턴
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-thread-pool-work-queue-work-stealing
---

06장은 **여러 스레드를 효율적으로 관리하는 기반 구조**를 다룬다. 스레드 생성은 비싸고, 무한정 많은 스레드는 만들 수 없다. Thread Pool은 미리 정해진 수의 워커 스레드를 풀에서 유지하며, 들어오는 작업들을 큐에서 꺼내 처리한다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [04장: 데이터 흐름: Producer-Consumer](/post/multithreading-patterns/cpp-producer-consumer-bounded-buffer-backpressure/)에서 다룬 Bounded Queue와 backpressure 개념, 그리고 02장의 RAII 락 가드를 그대로 사용합니다. "작업 큐에 항목을 넣고(`enqueue`), 워커가 꺼내 실행한다"는 구조가 04장의 Producer-Consumer와 동일하다는 것을 인식하고 있으면 이 장이 훨씬 쉽게 읽힙니다.

**이 장의 깊이**: 이 장은 **중급~전문가**까지를 포괄합니다. 공유 큐 기반의 기본 Thread Pool부터 시작해, 워커별 로컬 큐와 Work Stealing, 그리고 Bounded Queue 기반 Backpressure까지 다룹니다. 전문가 구간에서는 풀 크기를 어떻게 결정할지(`hardware_concurrency()`, I/O vs CPU 바운드)와 Work Stealing 큐의 실제 구현에서 무엇이 까다로운지를 다룹니다. **다루지 않는 것**: 작업의 반환값을 받는 방법은 07장(Future/Promise)에서 다룹니다 — 이 장의 `Task`는 `void` 반환만 가정합니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "기본 Thread Pool" | 워커 스레드 풀 구현 |
| **고급자** | 전체, 특히 "Work Stealing" | 부하 분산 알고리즘 이해 |
| **시스템 설계자** | "성능 비교" ~ 마무리 | 스레드 풀 선택 기준 이해 |

---

## 기본 Thread Pool

```cpp
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <memory>
#include <functional>

class ThreadPool {
public:
    using Task = std::function<void()>;

private:
    std::vector<std::thread> workers;
    std::queue<Task> tasks;
    mutable std::mutex mu;
    std::condition_variable cv;
    bool shutdown = false;

    void workerLoop() {
        while (true) {
            Task task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !tasks.empty() || shutdown; });
                if (shutdown && tasks.empty()) break;
                if (tasks.empty()) continue;
                task = std::move(tasks.front());
                tasks.pop();
            }
            task();
        }
    }

public:
    ThreadPool(size_t numWorkers) {
        for (size_t i = 0; i < numWorkers; ++i) {
            workers.emplace_back([this] { workerLoop(); });
        }
    }

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        cv.notify_all();
        for (auto& t : workers) t.join();
    }

    void enqueue(Task task) {
        {
            std::lock_guard<std::mutex> lock(mu);
            tasks.push(std::move(task));
        }
        cv.notify_one();
    }
};
```

**사용법**:

```cpp
int main() {
    ThreadPool pool(4);  // 4개 워커 스레드

    for (int i = 0; i < 16; ++i) {
        pool.enqueue([i] {
            std::cout << "Task " << i << " on thread " << std::this_thread::get_id() << '\n';
        });
    }

    return 0;
}  // 소멸자가 모든 작업 대기
```

## Work Stealing 패턴

기본 풀은 모든 워커가 **공유 큐에서 경합**한다. 부하가 불균형하면 일부 워커는 바쁘고 일부는 유휴 상태다.

**Work Stealing**: 각 워커가 자신의 **로컬 큐**를 가지며, 자신의 큐가 비면 다른 워커의 큐에서 **작업을 훔친다**.

```cpp
#include <atomic>
#include <functional>
#include <memory>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

class WorkStealingPool {
public:
    using Task = std::function<void()>;

private:
    struct Worker {
        std::queue<Task> localQueue;
        mutable std::mutex mu;
    };

    std::vector<std::unique_ptr<Worker>> workers;
    std::vector<std::thread> threads;
    std::atomic<bool> shutdown{false};  // 여러 워커가 읽고 소멸자가 쓰므로 atomic 필요

    void workerLoop(size_t id) {
        while (true) {
            Task task;

            // 자신의 큐에서 먼저 시도
            {
                std::lock_guard<std::mutex> lock(workers[id]->mu);
                if (!workers[id]->localQueue.empty()) {
                    task = std::move(workers[id]->localQueue.front());
                    workers[id]->localQueue.pop();
                }
            }

            if (!task) {
                // 자신의 큐가 비었으면, 다른 워커에서 훔친다
                for (size_t i = 1; i < workers.size(); ++i) {
                    size_t victimId = (id + i) % workers.size();
                    std::lock_guard<std::mutex> lock(workers[victimId]->mu);
                    if (!workers[victimId]->localQueue.empty()) {
                        task = std::move(workers[victimId]->localQueue.back());
                        workers[victimId]->localQueue.pop();
                        break;
                    }
                }
            }

            if (!task) {
                // 모두 비었으면 대기 (생략)
                if (shutdown.load(std::memory_order_relaxed)) break;
                std::this_thread::yield();
                continue;
            }

            task();
        }
    }

public:
    WorkStealingPool(size_t numWorkers) : workers(numWorkers) {
        for (size_t i = 0; i < numWorkers; ++i) {
            workers[i] = std::make_unique<Worker>();
            threads.emplace_back([this, i] { workerLoop(i); });
        }
    }

    ~WorkStealingPool() {
        shutdown.store(true, std::memory_order_relaxed);
        for (auto& t : threads) t.join();
    }

    void enqueue(Task task, size_t preferredWorker = 0) {
        size_t id = preferredWorker % workers.size();
        std::lock_guard<std::mutex> lock(workers[id]->mu);
        workers[id]->localQueue.push(std::move(task));
    }
};
```

**장점**: 부하가 불균형해도 빠른 워커가 느린 워커의 작업을 도와준다 (부하 분산).

**실전에서의 함정**: 위 구현은 개념을 보여주기 위해 단순화했다. 실제 work-stealing 큐를 프로덕션에 쓰려면 다음을 고려해야 한다.

- **자기 큐는 뒤(front)에서 꺼내고, 도둑은 앞(back)에서 훔치게** 하면 자기 자신의 작업 추가/제거(LIFO, 캐시 지역성이 좋음)와 도둑의 steal(FIFO)이 서로 다른 쪽 끝을 사용해 락 경합이 줄어든다. 위 코드는 단순화를 위해 둘 다 `mutex`로 보호하지만, Chase-Lev deque 같은 알고리즘은 **owner는 락 없이, 도둑만 CAS(`compare_exchange`)로 경쟁**하게 만들어 owner 쪽 오버헤드를 거의 0으로 줄인다.
- **빈 풀에서의 busy-yield**: 위 `workerLoop`는 작업이 없으면 `yield()`로 스핀한다. 작업이 드문 워크로드에서는 CPU를 불필요하게 점유한다 — 04장의 `condition_variable` 기반 대기와 결합하거나, 일정 횟수 스핀 후 짧게 잠드는 하이브리드 전략이 흔히 쓰인다.
- **안전성 검증**: 이런 멀티-락, 멀티-큐 구조는 데드락(락 순서 역전)과 데이터 레이스(shutdown 플래그, 큐 크기 확인 시점) 둘 다의 위험이 있다. `g++ -std=c++20 -pthread -fsanitize=thread -g`로 빌드해 다수의 enqueue/steal이 동시에 일어나는 스트레스 테스트를 돌려 보는 것이 좋다.

## Thread Pool with Backpressure

Bounded Queue와 같은 원리로, 큐가 가득 차면 enqueue가 블록된다. 04장의 `BoundedQueue`와 동일한 `notFull`/`notEmpty` 조건 변수 쌍을 기본 Thread Pool에 그대로 결합하면 된다.

```cpp
#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

class ThreadPoolWithBackpressure {
public:
    using Task = std::function<void()>;

private:
    std::vector<std::thread> workers;
    std::queue<Task> tasks;
    mutable std::mutex mu;
    std::condition_variable notEmpty, notFull;
    size_t maxQueueSize;
    bool shutdown = false;

    void workerLoop() {
        while (true) {
            Task task;
            {
                std::unique_lock<std::mutex> lock(mu);
                notEmpty.wait(lock, [this] { return !tasks.empty() || shutdown; });
                if (shutdown && tasks.empty()) break;
                task = std::move(tasks.front());
                tasks.pop();
                notFull.notify_one();  // 큐에 자리가 생겼음을 enqueue 쪽에 알림
            }
            task();
        }
    }

public:
    ThreadPoolWithBackpressure(size_t numWorkers, size_t maxQueue)
        : maxQueueSize(maxQueue) {
        for (size_t i = 0; i < numWorkers; ++i) {
            workers.emplace_back([this] { workerLoop(); });
        }
    }

    ~ThreadPoolWithBackpressure() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        notEmpty.notify_all();
        for (auto& t : workers) t.join();
    }

    // 큐가 가득 차면 호출자(생산자) 스레드가 여기서 블록된다 — 04장의 backpressure와 동일한 효과
    void enqueue(Task task) {
        std::unique_lock<std::mutex> lock(mu);
        notFull.wait(lock, [this] { return tasks.size() < maxQueueSize || shutdown; });
        if (shutdown) return;
        tasks.push(std::move(task));
        notEmpty.notify_one();
    }

    // 큐가 가득 차면 즉시 false를 반환하는 비블로킹 버전 (04장의 Drop Policy와 동일)
    bool tryEnqueue(Task task) {
        std::lock_guard<std::mutex> lock(mu);
        if (tasks.size() >= maxQueueSize) return false;
        tasks.push(std::move(task));
        notEmpty.notify_one();
        return true;
    }
};
```

이 구조의 의미는 명확하다: **Thread Pool 자체가 04장의 Bounded Buffer다.** `enqueue()`를 호출하는 스레드가 프로듀서, 워커 스레드가 컨슈머다. 큐가 가득 찼을 때 `enqueue()`가 블록되면, 작업을 만들어내는 속도가 처리 속도에 자동으로 맞춰진다 — 이것이 04장에서 말한 backpressure가 Thread Pool 설계에 그대로 적용된 형태다.

## 풀 크기 결정

워커 스레드를 몇 개로 둘지는 작업의 성격에 따라 완전히 달라진다.

**CPU 바운드 작업** (계산 위주, I/O 대기 없음): 워커 수가 코어 수를 넘으면 컨텍스트 스위칭 오버헤드만 늘어난다. `std::thread::hardware_concurrency()`가 반환하는 값(논리 코어 수, 하이퍼스레딩 포함)을 그대로 쓰는 것이 보통 최적이다.

```cpp
unsigned int n = std::thread::hardware_concurrency();
if (n == 0) n = 4;  // 표준은 0(알 수 없음)을 반환할 수 있음을 허용 — 폴백 필요
ThreadPool pool(n);
```

**I/O 바운드 작업** (네트워크 응답, 디스크 읽기 대기): 워커가 I/O를 기다리는 동안 CPU는 비어 있으므로, 코어 수보다 훨씬 많은 워커를 둬도 이득이 있다. 흔히 쓰는 경험적 공식은 다음과 같다.

```
워커 수 ≈ 코어 수 × (1 + 평균 대기 시간 / 평균 계산 시간)
```

예를 들어 요청 하나당 계산은 1ms이고 DB 응답 대기는 9ms라면, 대기/계산 비율이 9이므로 코어 수의 10배 가까운 워커를 둬도 CPU는 과부하되지 않는다. 다만 워커 수가 늘어나면 스레드 자체의 메모리(스택 크기, 기본 1~8MB)와 컨텍스트 스위칭 비용이 누적되므로, 무작정 늘리기보다 측정 후 조정해야 한다.

**혼합 워크로드**: CPU 바운드 작업과 I/O 바운드 작업을 같은 풀에 섞으면, I/O 대기 중인 작업이 워커를 점유해 CPU 작업이 굶을 수 있다. 이런 경우 **풀을 분리**하는 것이 일반적이다 — CPU 작업용 풀은 `hardware_concurrency()` 크기로, I/O 작업용 풀은 더 크게(또는 09~10장에서 다룰 이벤트 기반 모델로 대체).

## 스레드 풀 선택 기준

| 특성 | 기본 풀 | Work Stealing |
|------|---------|--------------|
| 구현 복잡도 | 낮음 | 중간 |
| 부하 분산 | X | ✓ |
| 경합 | 높음 | 낮음 |
| 메모리 | 적음 | 중간 |

**선택**: 대부분의 작업이 균등하면 기본 풀, 편차가 크면 Work Stealing.

## 학습 성과 평가 기준

- [ ] 기본 Thread Pool을 구현하고, 작업 큐에서 안전하게 읽을 수 있는가?
- [ ] Work Stealing 알고리즘의 목표와 구현을 설명할 수 있는가?
- [ ] Shutdown 시 모든 작업이 완료될 때까지 대기하는 메커니즘을 이해하는가?
- [ ] Backpressure (큐 크기 제한)를 어디에 적용할지 판단할 수 있는가?

## 다음 장에서는

07장 **「실행 관리 II: Future와 Promise」**에서는 비동기 작업의 결과를 나중에 받는 Future/Promise 패턴을 다룬다.

## 참고 및 출처

- Anthony Williams, 『C++ Concurrency in Action』, Chapter 9 — Thread Pool 구현
- Herb Sutter, "Design Patterns" from GotW — Executor pattern
- Work-stealing 알고리즘은 Cilk, Intel TBB 등 업계 표준

