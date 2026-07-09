---
image: wordcloud.png
title: "[Concurrency Patterns] 03. 대기와 조정"
description: "Monitor Object, Guarded Suspension, Balking 패턴을 condition_variable로 구현합니다. spurious wakeup과 lost wakeup을 재현·검증하고, std::latch/barrier/semaphore와의 관계도 비교합니다."
date: 2026-06-13
lastmod: 2026-06-14
draft: false
collection_order: 3
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - C++
  - Condition-Variable
  - Monitor-Object
  - Guarded-Suspension
  - Balking
  - Notify
  - Spurious-Wakeup
  - Synchronization
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
  - Design-Pattern(디자인패턴)
  - Code-Quality(코드품질)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Reference(참고)
  - Barrier
  - Latch
  - Semaphore
  - Best-Practices
  - Testing(테스트)
slug: cpp-condition-variable-monitor-object-guarded-suspension
---

03장은 **능동적으로 상태를 확인(spinning)하는 대신, 다른 스레드가 신호를 보낼 때까지 안전하게 대기**하는 패턴들을 다룬다. 이전 장의 락은 "공유 상태를 보호하는 것"에 집중했다면, 이 장의 condition variable은 **"조건이 만족될 때까지 대기"**의 효율성을 높인다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [02장: 락 관용구](/post/multithreading-patterns/cpp-locking-idioms-scoped-locking-thread-safe-interface/)에서 다룬 `std::mutex`, `std::lock_guard`, `std::unique_lock`을 전제로 합니다. 특히 `std::unique_lock`이 `std::lock_guard`와 달리 "락을 중간에 풀고 다시 잡을 수 있다"는 점을 모른다면 02장을 먼저 보고 오세요. `std::condition_variable`을 한 번도 본 적이 없어도 괜찮습니다 — 이 장이 처음부터 설명합니다.

**이 장의 깊이**: 이 장은 **중급~전문가** 수준입니다. `std::condition_variable`로 Monitor Object, Guarded Suspension, Balking 패턴을 구현하고, **spurious wakeup**과 **lost wakeup**이라는 두 가지 흔한 버그를 코드로 재현한 뒤 고칩니다. 전문가 구간에서는 OS별 spurious wakeup의 실제 발생 메커니즘, `notify`를 락 안/밖에서 호출할 때의 트레이드오프, 그리고 다중 condition_variable을 이용한 Bounded Queue의 실전 구현까지 다룹니다. **다루지 않는 것**: `std::future`/`std::promise` 기반의 비동기 결과 전달(07장), `std::semaphore`(C++20)와 `std::barrier`/`std::latch` 같은 더 새로운 동기화 프리미티브의 일반론(이 장에서는 비교 차원에서만 짧게 언급), 그리고 Producer-Consumer의 본격적인 큐 설계와 backpressure(04장)는 다음 장으로 넘긴다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "문제" ~ "Monitor Object 패턴" | condition_variable 기본 사용법, predicate의 필요성 |
| **중급자** | "Guarded Suspension 패턴" ~ "Balking 패턴" | BlockingQueue 구현, Balking의 적용 시점 판단 |
| **전문가** | "Spurious Wakeup의 OS별 메커니즘" ~ "실전: 여러 조건 변수" | lost wakeup 진단, 다중 CV 설계, notify 위치 선택 |

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

`cv.wait(lock, pred)`는 사실 다음 코드와 동일하다 — 즉 predicate 버전은 "더 똑똑한 wait"가 아니라 **아래 루프의 축약형**이다.

```cpp
while (!pred()) {
    cv.wait(lock);  // 깨어나면 다시 pred() 확인
}
```

### Spurious Wakeup의 OS별 메커니즘 (전문가)

"OS가 신호 없이 깨운다"는 말은 추상적으로 들리지만, 실제로는 구현상의 이유가 있다.

- **Linux (futex 기반)**: glibc의 `pthread_cond_wait`는 내부적으로 `futex` 시스템 콜로 구현된다. 시그널(POSIX signal)이 대기 중인 스레드에 전달되면 `futex_wait`가 `EINTR`로 깨어날 수 있고, glibc는 이를 spurious wakeup으로 다시 사용자에게 전달한다. 또한 멀티코어 환경에서 `notify`와 `wait` 사이의 타이밍 윈도우 때문에, 구현이 "한 번의 notify로 여러 스레드를 깨우는" 경우를 허용한다(과도하게 깨우는 것이 신호를 놓치는 것보다 안전하기 때문).
- **Windows (조건 변수 + Condition Variable API)**: Win32 `SleepConditionVariableCS`/`SRW` 기반 구현은 내부적으로 커널 디스패처 객체의 알람(alertable wait)을 사용하는데, I/O completion이나 APC(Asynchronous Procedure Call)가 대기 중인 스레드를 깨울 수 있어 spurious wakeup의 원인이 된다.
- **표준의 입장**: C++ 표준은 `wait`가 spurious하게 반환될 수 있음을 **명시적으로 허용**한다(이는 버그가 아니라 명세다). 그 이유는 구현이 "신호를 절대 놓치지 않는다"를 보장하기 위해 "가끔 더 깨운다"를 허용하는 쪽이 훨씬 구현하기 쉽고 빠르기 때문이다. predicate 검사는 이 trade-off를 사용자 코드에서 흡수하는 비용이다.

### Lost Wakeup: 더 위험한 버그

Spurious wakeup은 predicate 검사로 항상 해결되지만, **lost wakeup**은 더 치명적이다 — predicate를 빠뜨려도 평소엔 잘 동작하다가 타이밍에 따라 영원히 멈춘다.

```cpp
// 깨진 코드: notify가 wait보다 먼저 일어나면 신호가 사라진다
class BrokenSignal {
    std::mutex mu;
    std::condition_variable cv;
    bool ready = false;
public:
    void set() {
        ready = true;       // (1) 락 없이 상태 변경 — 데이터 레이스이기도 함
        cv.notify_one();    // (2) 이 시점에 아직 wait()가 시작 안 됐다면 신호 소실
    }
    void waitForReady() {
        std::unique_lock<std::mutex> lock(mu);
        cv.wait(lock);      // (3) predicate 없음 + (2)가 먼저 발생하면 영원히 대기
    }
};
```

스레드 스케줄링상 `set()`이 `waitForReady()`보다 먼저 실행되면, `notify_one()`은 "아직 아무도 듣고 있지 않은 상태"에서 호출되어 그냥 사라진다. 이후 `waitForReady()`가 `cv.wait(lock)`에 들어가면 더 이상 깨워줄 신호가 없으므로 **영구 대기**한다.

```cpp
// 고친 코드: ready를 mutex로 보호하고 predicate로 확인
class FixedSignal {
    std::mutex mu;
    std::condition_variable cv;
    bool ready = false;
public:
    void set() {
        std::lock_guard<std::mutex> lock(mu);
        ready = true;
        cv.notify_one();
    }
    void waitForReady() {
        std::unique_lock<std::mutex> lock(mu);
        cv.wait(lock, [this] { return ready; });
        // set()이 wait() 이전에 호출되었어도, ready==true이므로 즉시 통과
    }
};
```

핵심은 **"상태 변경 + notify"와 "predicate 확인 + wait"가 같은 mutex로 보호되어야 한다**는 것이다. 그래야 `set()`이 먼저 실행되어도 `ready = true`가 이미 반영되어 있어 `wait`의 predicate가 즉시 true를 반환한다.

### 안전성 검증: ThreadSanitizer로 확인

`BrokenSignal`은 `ready`에 대한 비보호 읽기/쓰기가 있어 TSAN이 데이터 레이스로 잡아낸다. 또한 lost wakeup 자체는 데이터 레이스가 아니라 "타이밍에 따라 영원히 멈추는" 문제이므로, TSAN보다는 **타임아웃을 건 재현 테스트**가 효과적이다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g signal.cpp -o signal
./signal   # ready에 대한 data race를 TSAN이 보고

# lost wakeup 재현: notify가 wait보다 먼저 오도록 인위적 지연 추가 후
timeout 3 ./signal_no_predicate || echo "hang detected (lost wakeup)"
```

`FixedSignal`은 두 검사 모두 깨끗하게 통과한다.

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

## 실전: 여러 조건 변수

### notify를 락 안에서 호출할까, 밖에서 호출할까

`set()`/`push()` 예제들은 모두 `notify_one()`을 **락을 잡은 상태에서** 호출한다. 하지만 가장 앞의 `DataHolder::set()` 예제는 `notify_one()`을 **락 해제 후** 호출했다. 둘 다 정답이 될 수 있지만 트레이드오프가 다르다.

```cpp
// (A) 락 안에서 notify — 더 안전, 약간 더 비효율적
void push_A(int val) {
    std::lock_guard<std::mutex> lock(mu);
    q.push(val);
    cv.notify_one();  // 락을 쥔 채로 notify
}  // 락 해제는 notify 이후

// (B) 락 밖에서 notify — "hurry up and wait" 회피
void push_B(int val) {
    {
        std::lock_guard<std::mutex> lock(mu);
        q.push(val);
    }  // 락 먼저 해제
    cv.notify_one();  // 이제 notify
}
```

(A)는 notify된 스레드가 즉시 깨어나도 곧바로 `mu`를 다시 기다려야 하는 "hurry up and wait" 현상이 있을 수 있다(대부분의 구현은 이를 최적화하지만 표준이 보장하진 않는다). (B)는 이 낭비를 줄이지만, **notify와 unlock 사이에 컨텍스트 스위치가 끼어들 여지가 생긴다는 점에서 "더 위험해 보일 수 있다** — 그러나 predicate 기반 `wait`를 쓴다면 (B)도 안전하다. 정답이 없으므로, 측정 후 결정하되 **predicate를 항상 쓴다**는 원칙은 둘 다에서 동일하게 적용된다.

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

이 `Barrier`는 손으로 만든 교육용 축소판이다. C++20은 정확히 이 문제(N개 스레드가 모두 도착할 때까지 기다렸다가 함께 출발)를 표준 라이브러리 타입 `std::barrier`로 제공한다. `std::barrier`는 재사용 가능하다는 점에서 더 강력하다 — 위 `Barrier`는 `total`에 도달하면 그걸로 끝이지만, `std::barrier`는 각 단계(phase)가 끝날 때마다 자동으로 다음 단계를 위해 초기화되며, 마지막 도착 스레드가 실행할 완료 콜백(completion function)도 등록할 수 있다. 비슷하게, "N개 이벤트가 모두 끝날 때까지 딱 한 번만 기다린다"는 **재사용 불가능한** 대기는 `std::latch`가 더 간단하다 — `Barrier`처럼 `wait`/`arrive`를 매번 조합하지 않고 `arrive_and_wait()` 한 번으로 끝난다. 리소스 슬롯을 N개로 제한하는 카운팅 문제(예: 동시 접속 수 제한)라면 `std::counting_semaphore`가 이 장의 조건 변수 조합보다 더 적은 코드로 같은 효과를 낸다. 이 장이 조건 변수로 이 패턴들을 손수 구현하는 이유는 "왜 이 표준 타입들이 내부적으로 안전한지"를 이해하려면 그 밑바탕의 대기·통지 메커니즘을 먼저 알아야 하기 때문이다 — 실무에서 새 코드를 짤 때는 이 손수 구현 대신 표준 타입을 우선 고려해야 한다.

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

경우에 따라 여러 CV를 쓰는 게 더 효율적이다. 단일 `notEmpty` CV만 쓰면 `push()`는 깨울 대상이 없어 항상 `notify_all()`로 모든 대기자를 깨워야 하지만, "가득 찼다"와 "비었다"라는 **서로 다른 조건을 분리**하면 각각 `notify_one()`으로 정확한 대상만 깨울 수 있다.

```cpp
#include <queue>
#include <mutex>
#include <condition_variable>

template<typename T>
class BoundedQueue {
private:
    mutable std::mutex mu;
    std::condition_variable notFull;   // 큐에 자리가 생겼을 때
    std::condition_variable notEmpty;  // 큐에 항목이 들어왔을 때
    std::queue<T> q;
    const size_t capacity;

public:
    explicit BoundedQueue(size_t cap) : capacity(cap) {}

    void push(T val) {
        std::unique_lock<std::mutex> lock(mu);
        notFull.wait(lock, [this] { return q.size() < capacity; });
        q.push(std::move(val));
        lock.unlock();
        notEmpty.notify_one();  // pop()을 깨운다
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mu);
        notEmpty.wait(lock, [this] { return !q.empty(); });
        T val = std::move(q.front());
        q.pop();
        lock.unlock();
        notFull.notify_one();  // push()를 깨운다
        return val;
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mu);
        return q.size();
    }
};
```

`capacity == 1`인 `BoundedQueue<int>`는 사실상 "교대로만 진행 가능한" 동기화 채널이 되어, Producer와 Consumer가 빠르게 핑퐁하는 구조를 강제한다. `capacity`를 키우면 Producer가 일시적으로 앞서갈 수 있는 버퍼 여유가 생기는데, 이 트레이드오프(메모리 vs 처리량)는 04장 Producer-Consumer에서 본격적으로 다룬다.

### 안전성 검증: ThreadSanitizer로 확인

`BoundedQueue`는 `push`/`pop`이 항상 `mu`로 보호되므로 데이터 레이스는 없지만, **두 CV를 혼동**하면(`notFull.wait`에 `!q.empty()`를 넣는 등) lost wakeup이 발생한다. 이런 버그는 TSAN의 데이터 레이스 검출 범위 밖이므로, 단위 테스트로 "용량 1짜리 큐에 두 스레드가 핑퐁하며 1000번 주고받기"를 타임아웃과 함께 실행해 확인하는 것이 실용적이다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g bounded_queue.cpp -o bq
timeout 5 ./bq && echo OK || echo "hang or race detected"
```

## 학습 성과 평가 기준

- [ ] Monitor Object 패턴에서 mutex, condition_variable, predicate의 역할을 설명할 수 있는가?
- [ ] Spurious wakeup이란 무엇이며, predicate를 통해 어떻게 처리하는가? OS별로 왜 발생하는지 설명할 수 있는가?
- [ ] Lost wakeup을 코드로 재현하고, mutex+predicate 조합으로 고칠 수 있는가?
- [ ] Guarded Suspension과 Balking의 차이를 예제로 들어 설명할 수 있는가?
- [ ] BlockingQueue를 구현하고, Producer-Consumer 시나리오에서 작동시킬 수 있는가?
- [ ] Bounded Queue (용량 제한)에서 두 개의 condition_variable을 써서 구현하고, notify 위치(락 안/밖)의 트레이드오프를 설명할 수 있는가?

## 다음 장에서는

04장 **「데이터 흐름(Data Flow)」**에서는 Producer-Consumer의 심화 패턴, Bounded Buffer와 backpressure, 그리고 다중 프로듀서/컨슈머 구조를 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 2 & 4 — Monitor Object와 Guarded Suspension
- Anthony Williams, 『C++ Concurrency in Action』(2nd ed., 2019), Chapter 4 — condition_variable, lost wakeup, Bounded Queue 구현
- C++ Standards Committee, `<condition_variable>` documentation — wait/wait_for의 spurious wakeup 명세
- Linux man-pages, `pthread_cond_wait(3)` — futex 기반 구현과 spurious wakeup의 원인
- Microsoft Docs, "Condition Variables" (Win32 API) — alertable wait와 spurious wakeup


