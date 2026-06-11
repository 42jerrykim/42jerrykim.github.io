---
title: "[Concurrency Patterns] 03. 대기와 조정"
description: "Monitor Object, Guarded Suspension, Balking 패턴을 condition_variable로 구현합니다. spurious wakeup 처리와 효율적인 신호 메커니즘을 다룹니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 3
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - C++
  - Condition-Variable
  - condition_variable
  - Monitor-Object
  - Guarded-Suspension
  - Balking
  - Notify
  - Spurious-Wakeup
  - Synchronization
  - 동기화
  - Waiting
  - 대기
  - Mutex
  - Lock-Guard
  - std::condition_variable
  - notify_one
  - notify_all
  - wait
  - Predicate
  - Memory-Model
  - Design-Pattern
  - 디자인패턴
  - Code-Quality
  - 코드품질
  - Implementation
  - 구현
  - Tutorial
  - Guide
  - Reference
slug: cpp-condition-variable-monitor-object-guarded-suspension
---

03장은 **능동적으로 상태를 확인(spinning)하는 대신, 다른 스레드가 신호를 보낼 때까지 안전하게 대기**하는 패턴들을 다룬다. 이전 장의 락은 "공유 상태를 보호하는 것"에 집중했다면, 이 장의 condition variable은 **"조건이 만족될 때까지 대기"**의 효율성을 높인다.

---

## 문제: Busy-Wait의 비용

01장에서 본 패턴을 다시 보자:

```cpp
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<bool> ready(false);
int result = 0;

int main() {
    std::thread writer([] {
        result = 42;
        ready.store(true, std::memory_order_release);
    });

    std::thread reader([] {
        while (!ready.load(std::memory_order_acquire));  // busy-wait
        std::cout << result << '\n';
    });

    writer.join();
    reader.join();
    return 0;
}
```

`while (!ready.load(...))`는 **busy-wait**: CPU를 낭비하며 계속 폴링한다. 멀티코어 CPU라도 이 스레드는 100% CPU를 소비하고, 다른 스레드의 작업을 방해한다. 만약 대기 시간이 길다면 (예: 네트워크 응답 대기) 이는 매우 비효율적이다.

## Monitor Object 패턴

**Monitor Object**는 condition variable을 사용해 효율적으로 대기하는 패턴이다. 핵심은:

1. **뮤텍스**: 상태를 보호
2. **Condition Variable**: 조건 신호 송수신
3. **Predicate**: "언제 계속할 건가"의 논리

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

class DataHolder {
private:
    std::mutex mu;
    std::condition_variable cv;
    bool ready = false;
    int result = 0;

public:
    void set(int val) {
        {
            std::lock_guard<std::mutex> lock(mu);
            result = val;
            ready = true;  // 상태 변경
        }
        cv.notify_one();  // 대기 중인 스레드 하나를 깨운다
    }

    int get() {
        std::unique_lock<std::mutex> lock(mu);
        cv.wait(lock, [this] { return ready; });  // 조건이 true일 때까지 대기
        return result;
    }
};

int main() {
    DataHolder dh;

    std::thread writer([&dh] {
        dh.set(42);
    });

    std::thread reader([&dh] {
        std::cout << dh.get() << '\n';  // 42
    });

    writer.join();
    reader.join();
    return 0;
}
```

**주요 요소**:

1. **unique_lock vs lock_guard**: `cv.wait()`는 내부적으로 lock을 해제했다가 다시 획득해야 하므로, `unique_lock`이 필요하다 (lock_guard는 불가).

2. **Predicate (조건 함수)**: `cv.wait(lock, [this] { return ready; })` 람다는 깨어난 후 조건을 확인한다. 만약 조건이 거짓이면 다시 대기한다. 이것이 **spurious wakeup 처리**다.

3. **notify_one vs notify_all**: `notify_one()`은 대기 중인 스레드 하나만 깨우고, `notify_all()`은 모두를 깨운다. 한 스레드만 진행되면 충분하면 notify_one, 여러 스레드가 깨어나야 하면 notify_all을 쓴다.

### Spurious Wakeup이란?

**Spurious wakeup**: OS가 조건 신호 없이도 스레드를 깨울 수 있다는 뜻이다. 따라서 `cv.wait()`에서 깨어났다고 해서 조건이 반드시 만족된 것은 아니다. 그래서 항상 **predicate를 확인**해야 한다:

```cpp
// 나쁜 예: predicate 없음
cv.wait(lock);
// 여기서 깨어났어도 조건이 거짓일 수 있음

// 좋은 예: predicate로 확인
cv.wait(lock, [this] { return ready; });
// 조건이 true가 될 때까지 루프 형태로 동작
```

## Guarded Suspension 패턴

**Guarded Suspension**은 Monitor Object와 유사하지만, 조건이 만족되지 않으면 "대기"가 아니라 "보류(suspend)"한다. 다음은 큐의 예제다:

```cpp
#include <queue>
#include <mutex>
#include <condition_variable>

template<typename T>
class BlockingQueue {
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
        cv.notify_one();  // 대기 중인 pop()을 깨운다
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mu);
        cv.wait(lock, [this] { return !q.empty(); });  // 큐가 비어있지 않을 때까지 대기
        T val = q.front();
        q.pop();
        return val;
    }

    bool empty() const {
        std::lock_guard<std::mutex> lock(mu);
        return q.empty();
    }
};
```

Producer-Consumer 패턴에서 자주 사용된다.

```cpp
#include <thread>
#include <iostream>

int main() {
    BlockingQueue<int> q;

    std::thread producer([&q] {
        for (int i = 0; i < 5; ++i) {
            q.push(i);
            std::cout << "Produced: " << i << '\n';
        }
    });

    std::thread consumer([&q] {
        for (int i = 0; i < 5; ++i) {
            int val = q.pop();
            std::cout << "Consumed: " << val << '\n';
        }
    });

    producer.join();
    consumer.join();
    return 0;
}
```

## Balking 패턴

**Balking**은 조건이 만족되지 않으면 "대기하지 않고 즉시 포기"하는 패턴이다. Guarded Suspension의 반대다.

```cpp
class DataValidator {
private:
    std::mutex mu;
    bool validated = false;
    int value = 0;

public:
    bool validate(int val) {
        std::lock_guard<std::mutex> lock(mu);
        if (validated) return false;  // 이미 검증됨 → 포기
        value = val;
        validated = true;
        return true;
    }

    int getValue() const {
        std::lock_guard<std::mutex> lock(mu);
        return value;
    }
};
```

Balking은 **멱등성**(idempotent) 작업에 유용하다. 예: 초기화 함수가 두 번 호출되는 것을 방지.

```cpp
// Balking을 쓰면
if (data.validate(42)) {
    std::cout << "Validation succeeded\n";
} else {
    std::cout << "Already validated, skipping\n";
}
```

## 실전: Condition Variable의 올바른 패턴

### 패턴 1: Single Condition, Multiple Waiters

여러 스레드가 같은 조건을 기다린다면 `notify_all()`을 쓴다.

```cpp
class Barrier {
private:
    std::mutex mu;
    std::condition_variable cv;
    int count;
    const int total;

public:
    Barrier(int n) : count(0), total(n) {}

    void arrive() {
        std::unique_lock<std::mutex> lock(mu);
        ++count;
        if (count == total) {
            cv.notify_all();  // 모든 대기자 깨우기
        } else {
            cv.wait(lock, [this] { return count == total; });
        }
    }
};
```

### 패턴 2: 시간제한 대기

```cpp
T pop_timeout(int milliseconds) {
    std::unique_lock<std::mutex> lock(mu);
    if (!cv.wait_for(lock, std::chrono::milliseconds(milliseconds),
                     [this] { return !q.empty(); })) {
        throw std::runtime_error("Timeout");
    }
    T val = q.front();
    q.pop();
    return val;
}
```

### 패턴 3: 여러 조건 변수 (고급)

경우에 따라 여러 CV를 쓰는 게 더 효율적이다.

```cpp
class BoundedQueue {
private:
    std::mutex mu;
    std::condition_variable notFull;   // 큐가 가득 찼을 때
    std::condition_variable notEmpty;  // 큐가 비었을 때
    std::queue<int> q;
    size_t capacity;

public:
    BoundedQueue(size_t cap) : capacity(cap) {}

    void push(int val) {
        std::unique_lock<std::mutex> lock(mu);
        notFull.wait(lock, [this] { return q.size() < capacity; });
        q.push(val);
        notEmpty.notify_one();  // pop()을 깨운다
    }

    int pop() {
        std::unique_lock<std::mutex> lock(mu);
        notEmpty.wait(lock, [this] { return !q.empty(); });
        int val = q.front();
        q.pop();
        notFull.notify_one();  // push()를 깨운다
        return val;
    }
};
```

## 학습 성과 평가 기준

- [ ] Monitor Object 패턴에서 mutex, condition_variable, predicate의 역할을 설명할 수 있는가?
- [ ] Spurious wakeup이란 무엇이며, predicate를 통해 어떻게 처리하는가?
- [ ] Guarded Suspension과 Balking의 차이를 예제로 들어 설명할 수 있는가?
- [ ] BlockingQueue를 구현하고, Producer-Consumer 시나리오에서 작동시킬 수 있는가?
- [ ] Bounded Queue (용량 제한)에서 두 개의 condition_variable을 써서 구현할 수 있는가?

## 다음 장에서는

04장 **「데이터 흐름(Data Flow)」**에서는 Producer-Consumer의 심화 패턴, bounded buffer와 backpressure, 그리고 비동기 파이프라인을 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 2 & 4 — Monitor Object와 Guarded Suspension
- Anthony Williams, 『C++ Concurrency in Action』, Chapter 4 — condition_variable 상세 가이드
- C++ Standards Committee, `<condition_variable>` documentation
