---
title: "[Concurrency Patterns] 06. 실행 관리 I: Thread Pool"
description: "스레드 풀, 작업 큐, Work Stealing 알고리즘을 구현하고, 부하 분산과 응답성의 트레이드오프를 학습합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 6
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
    bool shutdown = false;

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
                if (shutdown) break;
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
        shutdown = true;
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

## Thread Pool with Backpressure

Bounded Queue와 같은 원리로, 큐가 가득 차면 enqueue가 블록된다.

```cpp
class ThreadPoolWithBackpressure {
private:
    // ... (위와 동일)
    size_t maxQueueSize;

public:
    ThreadPoolWithBackpressure(size_t numWorkers, size_t maxQueue)
        : maxQueueSize(maxQueue) { /* ... */ }

    void enqueue(Task task) {
        std::unique_lock<std::mutex> lock(mu);
        // 큐 크기 확인 (이상적으로는 condition_variable로)
        while (tasks.size() >= maxQueueSize) {
            // 대기 또는 거부
        }
        tasks.push(std::move(task));
        cv.notify_one();
    }
};
```

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
