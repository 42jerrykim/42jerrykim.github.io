---
image: wordcloud.png
title: "[Concurrency Patterns] 04. 데이터 흐름: Producer-Consumer"
description: "Bounded Buffer, Unbounded Queue, Backpressure 메커니즘을 통해 Producer-Consumer 패턴의 확장성과 트레이드오프를 학습합니다. 다중 프로듀서/컨슈머 구조와 lock contention 최적화도 다룹니다."
date: 2026-06-14
lastmod: 2026-07-09
draft: false
collection_order: 4
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Producer-Consumer
  - Bounded-Buffer
  - Backpressure
  - Flow-Control
  - Data-Flow
  - Queue(큐)
  - Synchronization
  - Throughput
  - Latency
  - Memory(메모리)
  - capacity
  - blocking
  - Non-blocking
  - Design-Pattern(디자인패턴)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - C++
  - Concurrency(동시성)
  - Mutex
  - Condition-Variable
  - Thread
  - Scalability(확장성)
  - Best-Practices
  - Testing(테스트)
  - Deep-Dive
slug: cpp-producer-consumer-bounded-buffer-backpressure
---

생산자가 컨슈머보다 빠르면 어딘가에 데이터가 쌓인다. 그 "어딘가"를 무한히 키우면 메모리가 터지고, 무작정 막으면 생산자가 멈춘다. 이 문제는 새로운 것이 아니다 — Edsger Dijkstra가 1965년 세마포어(semaphore)를 도입하며 다룬 원래 문제가 바로 "생산자와 소비자가 유한한 버퍼를 공유할 때 서로를 어떻게 막고 깨울 것인가"였다. 04장은 그 문제를 `condition_variable` 기반으로 다시 풀며, 데이터가 **프로듀서(생산)에서 컨슈머(소비)로 흘러가는 구조**를 다룬다. 핵심 트레이드오프는 두 가지다:

1. **Bounded Buffer vs Unbounded**: 메모리 제한 vs 응답성
2. **Blocking Backpressure vs Dropping**: 대기 vs 손실

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 대기와 조정](/post/multithreading-patterns/cpp-condition-variable-monitor-object-guarded-suspension/)에서 다룬 `std::condition_variable`과 Monitor Object 패턴을 전제로 합니다. `cv.wait(lock, predicate)`가 왜 spurious wakeup에 안전한지 이해하고 있어야 이 장의 큐 구현을 읽을 수 있습니다. 아직이라면 03장을 먼저 보세요.

**이 장의 깊이**: 이 장은 **중급–전문가**까지를 포괄합니다. Unbounded/Bounded Queue의 기본 구현부터 시작해, Drop Policy·Timeout 같은 변형, 다중 프로듀서/컨슈머 환경에서의 동작, 그리고 메모리 순서 관점에서 Bounded Buffer가 왜 안전한지까지 다룹니다. **다루지 않는 것**: lock-free queue의 실제 구현(11장에서 개념만 미리보기), 분산 메시지 큐(Kafka, RabbitMQ 같은 시스템 레벨 큐)는 범위 밖입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "Unbounded Queue" ~ "Bounded Buffer" | 생산-소비 큐 구현 |
| **중급자** | 전체 (성능 섹션 제외) | Backpressure 이해 및 적용 |
| **전문가** | "다중 프로듀서/컨슈머" ~ "성능 고려사항" | Lock contention과 최적화 |

---

## Unbounded Queue (무제한 큐)

가장 단순한 형태다. 프로듀서가 얼마든 데이터를 넣을 수 있다.

```cpp
template<typename T>
class UnboundedQueue {
private:
    mutable std::mutex mu;
    std::condition_variable cv;
    std::queue<T> q;

public:
    void push(const T& val) {
        {
            std::lock_guard<std::mutex> lock(mu);
            q.push(val);
        }
        cv.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mu);
        cv.wait(lock, [this] { return !q.empty(); });
        T val = q.front();
        q.pop();
        return val;
    }
};
```

**장점**: 프로듀서가 절대 블로킹되지 않음. 응답성 우수.

**단점**: 메모리 사용량 제한 없음. 프로듀서가 매우 빠르고 컨슈머가 느리면 메모리 부족.

**흔한 실수**: `pop()`에서 `cv.wait(lock, predicate)` 대신 `if (q.empty()) cv.wait(lock);`처럼 조건 없는 `wait`를 쓰면 **lost wakeup**이 발생할 수 있다. `push()`의 `notify_one()`이 `pop()`이 `wait()`에 들어가기 *전*에 호출되면, 그 알림은 그냥 사라지고 컨슈머는 영원히 깨어나지 못한다. 위 구현처럼 술어(predicate)를 넘기는 `wait(lock, [this]{...})` 형태는 "락을 다시 잡았을 때 조건을 한 번 더 검사"하므로 이 경쟁을 원천적으로 막는다. 이 차이는 03장의 Monitor Object에서 다룬 내용 그대로다.

## Bounded Buffer (유한 버퍼)

큐의 크기를 제한한다. 가득 차면 프로듀서는 대기한다 (**backpressure**). 03장의 "실전: 여러 조건 변수" 절에서 이미 같은 이름의 `BoundedQueue`를 만들어 봤다면 낯익을 것이다 — 여기서는 그 개념을 이 장의 흐름 제어 관점에서 다시 짚는다. 다만 아래 구현은 `notify_one()`을 **락을 쥔 채로** 호출한다(03장이 "(A) 방식"이라 부른 쪽). 이 장에서는 backpressure 자체에 집중하기 위해 더 단순한 (A) 방식을 썼다 — notify를 락 해제 후로 옮기는 (B) 방식과의 트레이드오프는 03장을 참고하라.

```cpp
template<typename T>
class BoundedQueue {
private:
    std::mutex mu;
    std::condition_variable notFull, notEmpty;
    std::queue<T> q;
    size_t capacity;

public:
    BoundedQueue(size_t cap) : capacity(cap) {}

    void push(const T& val) {
        std::unique_lock<std::mutex> lock(mu);
        notFull.wait(lock, [this] { return q.size() < capacity; });
        q.push(val);
        notEmpty.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mu);
        notEmpty.wait(lock, [this] { return !q.empty(); });
        T val = q.front();
        q.pop();
        notFull.notify_one();
        return val;
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mu);
        return q.size();
    }
};
```

**Backpressure의 효과**: 프로듀서가 빠르고 컨슈머가 느리면, 프로듀서는 `notFull.wait()`에서 대기한다. 이는 <strong>시스템 전체의 처리량(throughput)</strong>을 컨슈머의 속도로 자동으로 조절한다.

```cpp
int main() {
    BoundedQueue<int> q(5);  // 용량 5

    std::thread producer([&q] {
        for (int i = 0; i < 1000; ++i) {
            q.push(i);
            std::cout << "Produced: " << i << ", queue size: " << q.size() << '\n';
        }
    });

    std::thread consumer([&q] {
        for (int i = 0; i < 1000; ++i) {
            int val = q.pop();
            std::cout << "Consumed: " << val << '\n';
            std::this_thread::sleep_for(std::chrono::milliseconds(10));  // 느린 처리
        }
    });

    producer.join();
    consumer.join();
    return 0;
}
```

프로듀서는 큐가 가득 차면 자동으로 대기하므로, 메모리는 최대 5개 아이템만 사용한다.

## 메모리 순서 관점에서 본 Bounded Buffer

01장에서 배운 happens-before 관계를 이 큐에 적용해 보자. `push()`는 `mu.lock()` 안에서 `q.push(val)`을 실행하고, `pop()`은 같은 `mu`를 잠그고 `q.front()`를 읽는다. **mutex의 unlock은 그 이후의 lock에 happens-before 관계를 만든다** — 이것이 01장에서 정리한 "Lock 획득/해제" 규칙이다. 따라서 프로듀서가 `push()` 안에서 쓴 값(`q.push(val)`이 힙에 객체를 생성하며 수행한 모든 메모리 쓰기 포함)은, 컨슈머가 같은 mutex로 보호된 `pop()`에서 `q.front()`를 읽을 때 **반드시 보인다.** 즉 `std::mutex`는 단순히 "동시 접근을 막는" 것을 넘어, 그 자체로 동기화 지점(synchronization point)으로 작동해 별도의 atomic이나 `memory_order` 지정이 필요 없다. 이것이 락 기반 큐가 "구현이 쉬운" 진짜 이유다 — 정확성의 책임을 mutex 하나에 위임할 수 있기 때문이다.

## Bounded Buffer의 변형

### 1. Drop Policy (드롭 정책)

큐가 가득 차면 대기하지 않고 데이터를 버린다.

```cpp
bool push_noblocking(const T& val) {
    std::lock_guard<std::mutex> lock(mu);
    if (q.size() >= capacity) {
        return false;  // 버림
    }
    q.push(val);
    notEmpty.notify_one();
    return true;
}
```

**사용처**: 로깅, 메트릭 수집처럼 손실 가능한 데이터.

### 2. Timeout with Overflow

시간제한 대기 후, 실패하거나 오버플로우 큐로 옮긴다.

```cpp
bool push_timeout(const T& val, int millis) {
    std::unique_lock<std::mutex> lock(mu);
    if (!notFull.wait_for(lock, std::chrono::milliseconds(millis),
                          [this] { return q.size() < capacity; })) {
        // Timeout: overflow queue로 옮기거나 드롭
        return false;
    }
    q.push(val);
    notEmpty.notify_one();
    return true;
}
```

## 트레이드오프 분석

| 특성 | Unbounded | Bounded (Blocking) | Drop Policy |
|------|-----------|-------------------|-------------|
| 메모리 | 무제한 | 제한됨 | 제한됨 |
| Backpressure | X | ✓ | X |
| 데이터 손실 | 없음 | 없음 | 있음 |
| 응답성 | 최고 | 좋음 | 최고 |

**선택 기준**:
- **신뢰성 우선** (금융, 로그): Bounded Blocking
- **응답성 우선** (게임, UI): Drop Policy
- **메모리 충분**: Unbounded

## 다중 프로듀서/컨슈머

위의 BoundedQueue는 이미 여러 스레드를 안전하게 지원한다. 처리량을 직접 눈으로 확인할 수 있도록, 3개 프로듀서와 2개 컨슈머가 각각 몇 개를 처리했는지 집계하는 벤치마크 형태로 작성해 보자.

```cpp
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    BoundedQueue<int> q(10);
    constexpr int itemsPerProducer = 100000;
    std::atomic<long long> consumedSum{0};
    std::atomic<int> consumedCount{0};
    const int totalItems = 3 * itemsPerProducer;

    auto start = std::chrono::steady_clock::now();

    // 3개 프로듀서
    std::vector<std::thread> producers;
    for (int p = 0; p < 3; ++p) {
        producers.emplace_back([&q, p] {
            for (int i = 0; i < itemsPerProducer; ++i) {
                q.push(p * itemsPerProducer + i);
            }
        });
    }

    // 2개 컨슈머: 전체 아이템 수를 알고 있으므로 종료 조건을 atomic 카운터로 판단
    std::vector<std::thread> consumers;
    for (int c = 0; c < 2; ++c) {
        consumers.emplace_back([&] {
            while (consumedCount.fetch_add(1, std::memory_order_relaxed) < totalItems) {
                int val = q.pop();
                consumedSum.fetch_add(val, std::memory_order_relaxed);
            }
        });
    }

    for (auto& t : producers) t.join();
    for (auto& t : consumers) t.join();

    auto elapsed = std::chrono::steady_clock::now() - start;
    std::cout << "처리한 합계: " << consumedSum.load() << '\n';
    std::cout << "소요 시간: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count()
              << "ms\n";
    return 0;
}
```

위 코드의 종료 조건(`consumedCount.fetch_add(...) < totalItems`)은 "전체 아이템 수를 미리 알고 있다"는 단순화다. 실전에서는 보통 <strong>종료 신호(poison pill)</strong>를 큐에 넣거나, 모든 프로듀서가 끝났음을 알리는 별도의 플래그/카운터를 두어 컨슈머가 "더 이상 올 데이터가 없음"을 판단하게 한다. 큐의 원소 타입을 `std::optional<T>`로 두면, "값이 있으면 처리할 데이터, `nullopt`면 종료 신호"라는 뜻으로 poison pill을 표현할 수 있다.

```cpp
// 프로듀서: 데이터를 다 보낸 뒤 nullopt를 넣어 "더 이상 없음"을 알린다.
void producer(BoundedQueue<std::optional<int>>& q, int count) {
    for (int i = 0; i < count; ++i) q.push(i);
    q.push(std::nullopt);  // poison pill
}

// 컨슈머: nullopt를 받으면 종료한다.
void consumer(BoundedQueue<std::optional<int>>& q) {
    while (true) {
        std::optional<int> item = q.pop();
        if (!item.has_value()) break;  // poison pill 수신 → 종료
        // item.value() 처리
    }
}
```

컨슈머가 여러 개라면 poison pill 하나로는 부족하다 — 그 pill을 받은 컨슈머 하나만 종료하고 나머지는 계속 기다리기 때문이다. 컨슈머 수만큼 pill을 넣거나, 종료 플래그와 `notify_all()`을 함께 쓰는 방식으로 확장해야 한다.

## 성능 고려사항

### Lock Contention

Bounded Queue에서 단일 mutex는 push/pop 경합을 유발한다. 프로듀서와 컨슈머가 매번 같은 mutex를 다투면, 큐 자체의 작업(원소 하나를 옮기는 것)보다 락 획득/해제 비용이 더 커지는 경우도 흔하다. 두 가지 완화 방법이 있다.

**1. 분리된 락**: push 경로와 pop 경로가 서로 다른 부분(예: 링 버퍼의 head/tail)을 건드린다면, 두 개의 mutex로 경합을 줄일 수 있다. 다만 큐가 비어 있거나 가득 찬 "경계 상황"에서는 여전히 두 락을 함께 다뤄야 하므로 구현이 까다롭다.

**2. Lock-Free SPSC 큐**: 프로듀서 1개, 컨슈머 1개(Single-Producer Single-Consumer)인 가장 흔한 경우, mutex 없이 `std::atomic`만으로 링 버퍼를 구현할 수 있다. 핵심 아이디어는 head/tail 인덱스를 각각 프로듀서와 컨슈머만 쓰고, 서로의 인덱스를 `memory_order_acquire`/`memory_order_release`로 읽고 쓰는 것이다.

```cpp
// 개념 스케치 — 11장에서 전체 구현과 검증을 다룬다
template<typename T, size_t N>
class SpscRingBuffer {
    std::array<T, N> buf;
    std::atomic<size_t> head{0};  // 컨슈머가 갱신
    std::atomic<size_t> tail{0};  // 프로듀서가 갱신

public:
    bool push(const T& val) {
        size_t t = tail.load(std::memory_order_relaxed);
        size_t h = head.load(std::memory_order_acquire);
        if ((t + 1) % N == h) return false;  // 가득 참
        buf[t] = val;
        tail.store((t + 1) % N, std::memory_order_release);
        return true;
    }

    bool pop(T& out) {
        size_t h = head.load(std::memory_order_relaxed);
        size_t t = tail.load(std::memory_order_acquire);
        if (h == t) return false;  // 비어 있음
        out = buf[h];
        head.store((h + 1) % N, std::memory_order_release);
        return true;
    }
};
```

프로듀서의 `tail.store(..., release)`와 컨슈머의 `tail.load(..., acquire)`가 짝을 이뤄 happens-before 관계를 만들고, 이 덕분에 프로듀서가 `buf[t]`에 쓴 값을 컨슈머가 안전하게 읽을 수 있다. 이 패턴이 **mutex 없이도 안전한 이유**와, 멀티 프로듀서/멀티 컨슈머(MPMC)로 확장할 때 왜 이렇게 단순하지 않은지는 11장 "공유 회피"에서 다룬다.

한 가지 주의점: `(t + 1) % N == h`로 가득 참을 판정하는 방식은 슬롯 하나를 항상 비워 둔다 — `head == tail`이 "가득 참"과 "비어 있음"을 동시에 뜻하지 않게 하려는 것이다. 그래서 이 링 버퍼가 실제로 저장할 수 있는 원소는 `N`개가 아니라 **`N - 1`개**다. 처음 접하면 흔히 놓치는 지점이라, 용량을 정확히 `N`으로 맞추려면 배열 크기를 `N + 1`로 잡거나 별도의 원소 개수 카운터를 둬야 한다.

## 학습 성과 평가 기준

- [ ] Unbounded vs Bounded Queue의 트레이드오프를 설명할 수 있는가?
- [ ] Backpressure가 무엇이며, 시스템 안정성에 어떻게 도움이 되는가?
- [ ] Drop Policy와 Blocking Backpressure 중 언제 각각을 쓸지 판단할 수 있는가?
- [ ] 다중 프로듀서/컨슈머 시나리오에서 BoundedQueue를 안전하게 사용할 수 있는가?

## 다음 장에서는

05장 <strong>「읽기 최적화와 지연 초기화」</strong>에서는 공유 데이터에서 읽기가 대부분인 경우의 최적화 (Shared Mutex, DCLP)를 다룬다.

## 참고 및 출처

- POSA2, Chapter 4 — Bounded Buffer 패턴
- Brian Goetz, 『Java Concurrency in Practice』, Chapter 12 — Testing Concurrent Programs (큐 테스트 전략)


