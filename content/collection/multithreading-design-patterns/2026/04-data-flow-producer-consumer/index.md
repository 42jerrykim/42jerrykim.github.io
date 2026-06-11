---
title: "[Concurrency Patterns] 04. 데이터 흐름: Producer-Consumer"
description: "Bounded Buffer, Unbounded Queue, Backpressure 메커니즘을 통해 프로듀서-컨슈머 패턴의 확장성과 트레이드오프를 학습합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 4
difficulty: intermediate
prerequisites:
  - "02~03장: Scoped Locking과 condition_variable"
  - "std::queue 기본 사용법"
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Producer-Consumer
  - Bounded-Buffer
  - Backpressure
  - Flow-Control
  - Data-Flow
  - Queue
  - Synchronization
  - 동기화
  - Throughput
  - Latency
  - Memory
  - 메모리
  - capacity
  - blocking
  - Non-blocking
  - Design-Pattern
  - 디자인패턴
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-producer-consumer-bounded-buffer-backpressure
---

04장은 데이터가 **프로듀서(생산)에서 컨슈머(소비)로 흘러가는 구조**를 다룬다. 핵심 트레이드오프는 두 가지다:

1. **Bounded Buffer vs Unbounded**: 메모리 제한 vs 응답성
2. **Blocking Backpressure vs Dropping**: 대기 vs 손실

## 🎯 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "Unbounded Queue" ~ "Bounded Buffer" | 생산-소비 큐 구현 |
| **중급자** | 전체 (성능 섹션 제외) | Backpressure 이해 및 적용 |
| **전문가** | "성능 고려사항" ~ "다중 프로듀서/컨슈머" | Lock contention과 최적화 |

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

## Bounded Buffer (유한 버퍼)

큐의 크기를 제한한다. 가득 차면 프로듀서는 대기한다 (**backpressure**).

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

**Backpressure의 효과**: 프로듀서가 빠르고 컨슈머가 느리면, 프로듀서는 `notFull.wait()`에서 대기한다. 이는 **시스템 전체의 처리량(throughput)**을 컨슈머의 속도로 자동으로 조절한다.

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

위의 BoundedQueue는 이미 여러 스레드를 안전하게 지원한다.

```cpp
int main() {
    BoundedQueue<int> q(10);

    // 3개 프로듀서
    std::vector<std::thread> producers;
    for (int p = 0; p < 3; ++p) {
        producers.emplace_back([&q, p] {
            for (int i = 0; i < 100; ++i) {
                q.push(p * 100 + i);
            }
        });
    }

    // 2개 컨슈머
    std::vector<std::thread> consumers;
    for (int c = 0; c < 2; ++c) {
        consumers.emplace_back([&q] {
            for (int i = 0; i < 150; ++i) {
                q.pop();
            }
        });
    }

    for (auto& t : producers) t.join();
    for (auto& t : consumers) t.join();
    return 0;
}
```

## 성능 고려사항

### Lock Contention

Bounded Queue에서 단일 mutex는 push/pop 경합을 유발한다. 고성능을 위해 **두 개의 뮤텍스**를 쓸 수 있다:

```cpp
class LowContentionQueue {
private:
    struct Node { int data; };
    mutable std::mutex pushMu, popMu;
    std::queue<Node> q;  // 실제론 링 버퍼가 나음

public:
    void push(int val) {
        std::lock_guard lock(pushMu);
        // ... push 로직
    }

    int pop() {
        std::lock_guard lock(popMu);
        // ... pop 로직
    }
};
```

더 나은 방식은 **lock-free 자료구조** (11장에서 다룸)다.

## 학습 성과 평가 기준

- [ ] Unbounded vs Bounded Queue의 트레이드오프를 설명할 수 있는가?
- [ ] Backpressure가 무엇이며, 시스템 안정성에 어떻게 도움이 되는가?
- [ ] Drop Policy와 Blocking Backpressure 중 언제 각각을 쓸지 판단할 수 있는가?
- [ ] 다중 프로듀서/컨슈머 시나리오에서 BoundedQueue를 안전하게 사용할 수 있는가?

## 다음 장에서는

05장 **「읽기 최적화와 지연 초기화」**에서는 공유 데이터에서 읽기가 대부분인 경우의 최적화 (Shared Mutex, DCLP)를 다룬다.

## 참고 및 출처

- POSA2, Chapter 4 — Bounded Buffer 패턴
- Brian Goetz, 『Java Concurrency in Practice』, Chapter 12 — Testing Concurrent Programs (큐 테스트 전략)
