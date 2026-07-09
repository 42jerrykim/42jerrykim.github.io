---
image: wordcloud.png
title: "[Concurrency Patterns] 01. 동시성 기초와 C++ 메모리 모델"
description: "멀티스레드 프로그래밍의 기반이 되는 C++ 메모리 모델을 다룹니다. 데이터 레이스, happens-before 관계, memory_order별 acquire-release/relaxed 의미, atomic 기초를 표준 문서와 컴파일 가능한 예제로 학습합니다."
date: 2026-06-11
lastmod: 2026-06-12
draft: false
collection_order: 1
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - C++
  - C++11
  - C++20
  - Thread
  - Memory(메모리)
  - Concurrency(동시성)
  - Atomic
  - Synchronization
  - Race-Condition
  - Data-Race
  - Memory-Order
  - Memory-Model
  - Sequentially-Consistent
  - Happens-Before
  - Acquire-Release
  - Relaxed-Ordering
  - Mutex
  - Lock
  - Lock-Free
  - CPU(Central Processing Unit)
  - Cache
  - Instruction-Reordering
  - Compiler-Optimization
  - UndefinedBehavior
  - std::thread
  - std::atomic
  - Standard-Library
  - Performance(성능)
  - Optimization(최적화)
  - Design-Pattern(디자인패턴)
  - Software-Architecture(소프트웨어아키텍처)
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Best-Practices
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Reference(참고)
  - Deep-Dive
  - Technology(기술)
slug: getting-started-cpp-concurrency-fundamentals-memory-model
---

멀티스레드 버그는 대부분 "락을 잘못 썼다"가 아니라 **메모리 모델이라는 하부 계층을 몰라서** 생긴다. 같은 코드가 어떤 CPU 아키텍처에서는 완벽히 작동하고, 다른 아키텍처에서는 간헐적으로 무너진다. 그 이유는 컴파일러와 CPU가 각각 "정확성을 해치지 않는다면" 코드를 얼마나 극적으로 재정렬할 수 있는지, 즉 **메모리 모델의 경계**를 정확히 이해하지 못했기 때문이다.

C++11에서 도입된 표준 메모리 모델은 이 경계를 처음으로 명확히 정의했다. 데이터 레이스가 정확히 무엇인지, 한 스레드의 쓰기가 다른 스레드에서 언제 보이는지, atomic 연산이 어떤 수준의 강제성을 제공하는지를 세밀하게 규정했다. 이 장은 그 기초 개념들을 익혀 **이후 모든 장에서 "왜 이 패턴이 안전한가"를 같은 언어로 논할 수 있게** 하는 기반을 마련한다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 std::thread의 기본 사용법을 이미 알고 있다고 가정합니다. 아직이라면 [C++ 표준 라이브러리 튜토리얼](https://en.cppreference.com/w/cpp/thread)을 먼저 보고 오세요.

**이 장의 깊이**: 이 장은 **중급** 수준입니다. 메모리 모델이 "선택지"가 아니라 "필수 어휘"라는 점을 이해하는 것이 목표입니다. 세부 CPU 아키텍처까지는 다루지 않습니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "우선, 왜 메모리 모델이 필요한가?" ~ "Happens-Before 표로 정리" | 데이터 레이스가 무엇인지 이해 |
| **중급자** | 전체 (코드 실행 제외) | atomic과 memory_order의 관계 이해 |
| **전문가** | 실전 섹션, CPU 최적화 심화 | 각 memory_order의 성능 트레이드오프 |

---

## 우선, 왜 메모리 모델이 필요한가?

멀티스레드 코드 없이도 같은 변수에 여러 스레드가 접근할 수 있는 세상을 상상하기는 어렵지만, 실제로는 흔하다. 다음 예제를 보자.

```cpp
#include <iostream>
#include <thread>
#include <atomic>

bool ready = false;
int result = 0;

int main() {
    std::thread writer([] {
        result = 42;      // (A)
        ready = true;     // (B)
    });

    std::thread reader([] {
        while (!ready);   // (C) 대기
        std::cout << result << '\n';  // (D)
    });

    writer.join();
    reader.join();
    return 0;
}
```

평소라면 (A)에서 `result`를 42로 설정하고 (B)에서 `ready`를 `true`로 하면, (C)의 대기 루프가 끝나고 (D)에서 result가 42로 읽혀야 한다. 하지만 **메모리 모델이 보장하지 않으면** 다음 일들이 일어날 수 있다.

1. **컴파일러가 (B)를 (A) 앞으로 옮길 수 있다**: 컴파일러 입장에서는 `result`와 `ready`가 서로 독립적인 변수이므로, (B)의 쓰기를 (A) 앞으로 재정렬해도 "이 스레드 내에서는" 문제가 없다. 따라서 (C)가 `ready == true`를 보게 되는 순간 (A)는 아직 실행되지 않을 수 있다.

2. **CPU가 명령을 바꿔 실행할 수 있다**: 최신 CPU(특히 ARM, PowerPC)는 메모리 배리어 명령 없이는 읽기-쓰기 순서를 강제하지 않는다. x86도 store-load 순서 정도는 보장하지 않는다.

3. **캐시 일관성 문제**: 한 CPU 코어의 캐시에 쓴 값이 다른 코어에 즉시 보이지 않을 수 있다.

이 모든 것이 C++ 표준에서 **데이터 레이스(data race)**라고 부르는 **미정의 동작(undefined behavior)**을 만든다. 미정의 동작이라는 것은 "약간 틀릴 수도, 정말 틀릴 수도, 그냥 폭발할 수도" 있다는 뜻이다.

## 데이터 레이스의 정의

C++ 표준은 데이터 레이스를 이렇게 정의한다: **같은 메모리 위치에 대한 두 접근(A 접근, B 접근)이 있을 때, (1) 최소 하나가 쓰기이고, (2) 두 접근이 **동기화(synchronize)**되지 않으면 데이터 레이스다.** "동기화된다"는 것은 표준 라이브러리의 락, atomic, 또는 표준에서 인정하는 다른 메커니즘으로 순서를 강제했다는 뜻이다.

예컨대 아래 코드는 **명확한 데이터 레이스**다:

```cpp
#include <thread>

int counter = 0;

int main() {
    std::thread t1([]{
        for(int i = 0; i < 100000; ++i) ++counter;  // (1) 쓰기
    });
    std::thread t2([]{
        for(int i = 0; i < 100000; ++i) ++counter;  // (2) 쓰기
    });
    t1.join(); t2.join();
    // counter는 200000이 될 수도, 아닐 수도
    return 0;
}
```

`++counter`는 **읽기-수정-쓰기** 세 단계를 원자적으로 수행하지 않는다. 따라서 스레드 1이 읽은 값을 수정하는 동안 스레드 2도 같은 값을 읽으면, 하나의 증가분이 유실된다. 더 나쁜 것은 C++ 표준은 이를 **미정의 동작**으로 규정하므로, 컴파일러는 이 코드에 대해 어떤 보증도 할 수 없다는 뜻이다.

## Happens-Before 관계

멀티스레드 코드의 안전성을 논하려면 "A가 B보다 먼저 완료됐다"는 개념이 필요하다. C++ 표준은 이를 **happens-before** 관계로 정의한다.

**Sequentially-Consistent (순차 일관성)** 메모리 모델에서는 모든 메모리 접근이 전역 시간 순서대로 보인다. 즉, 스레드 1의 쓰기 A가 스레드 2의 읽기 B보다 happen-before이면, B는 A가 쓴 값을 반드시 본다. 이것이 가장 직관적이고 강력한 메모리 모델이지만, 최신 CPU에서는 이를 구현하는 데 비용이 많이 든다.

C++11부터 표준은 다음과 같은 happens-before 관계를 정의한다:

1. **같은 스레드 내 순서**: 스레드 내에서 한 문장이 다음 문장보다 happen-before다.

2. **Lock 획득/해제**: mutex의 `lock()`이 이전 `unlock()` 이후의 모든 메모리 접근을 happen-before한다. 다시 말해, 락 안에서 한 스레드가 쓴 값을 락 안에서 다른 스레드가 읽으면, 쓰기 스레드의 모든 이전 쓰기가 읽기 스레드에 보인다.

3. **Atomic 연산**: `std::atomic`의 연산들은 `memory_order` 파라미터로 synchronization strength를 지정할 수 있다. `memory_order_seq_cst` (sequential consistency)는 가장 강력하고, `memory_order_acq_rel` (acquire-release)는 더 약하며, `memory_order_relaxed`는 순서 강제를 포기한다.

예를 들어, 다음 코드는 **안전**하다:

```cpp
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<bool> ready(false);
int result = 0;

int main() {
    std::thread writer([] {
        result = 42;
        ready.store(true, std::memory_order_release);  // release
    });

    std::thread reader([] {
        while (!ready.load(std::memory_order_acquire));  // acquire 대기
        std::cout << result << '\n';  // 항상 42
    });

    writer.join();
    reader.join();
    return 0;
}
```

여기서 `release` 쓰기와 `acquire` 읽기는 happens-before 관계를 만든다. 즉, `ready.store(true, release)`는 그 이전의 모든 메모리 접근(result = 42 포함)이 `ready.load(acquire)`를 통해 다른 스레드에 보이도록 강제한다.

## std::atomic 기초

`std::atomic<T>`는 **atomicity(원자성)**과 **synchronization(동기화)**을 제공하는 템플릿이다. 원자성은 "읽기-수정-쓰기 같은 복합 연산이 다른 스레드의 관찰로부터 나뉠 수 없다"는 뜻이고, 동기화는 happens-before을 만든다는 뜻이다.

### 기본 사용법

```cpp
#include <atomic>

std::atomic<int> x(0);

void writer() {
    x.store(42);                    // 쓰기
}

void reader() {
    int val = x.load();             // 읽기
    std::cout << val << '\n';       // 항상 42 (정의된 동작)
}
```

기본값(파라미터 없음)으로 `store`와 `load`를 호출하면 `memory_order_seq_cst`(sequential consistency)가 사용되므로, 모든 스레드가 일관된 순서를 본다.

### Memory Order와 비용

메모리 순서는 크게 세 가지다.

**1. Sequentially-Consistent (`memory_order_seq_cst`)**: 모든 스레드가 같은 전역 순서를 본다. 가장 강력하지만 가장 비싸다. x86에서는 거의 무료(몇 CPU 사이클), ARM에서는 명시적 배리어 명령이 필요하다.

```cpp
// 모든 atomic 연산이 동일한 순서로 보인다
x.store(1, std::memory_order_seq_cst);
y.store(2, std::memory_order_seq_cst);
// 다른 스레드는 x=1, y=2 또는 둘 다 미정, 절대 x=1, y=미정 조합 불가
```

**2. Acquire-Release (`memory_order_acquire` / `memory_order_release`)**: release 쓰기와 acquire 읽기 사이에만 synchronization을 강제한다. 다른 atomic들과의 순서는 강제하지 않는다. x86에서는 store에서 약간의 비용, ARM에서는 read의 비용을 아낄 수 있다.

```cpp
// Writer
x.store(42, std::memory_order_release);

// Reader
int val = x.load(std::memory_order_acquire);
// x의 쓰기-읽기 쌍만 동기화
```

**3. Relaxed (`memory_order_relaxed`)**: 동기화를 포기한다. 원자성만 보장한다. "여러 CPU가 동시에 같은 변수를 수정해도 중간 값이 아닌 최종 값이 보인다"는 뜻이다. 카운터 같은 곳에 사용할 수 있다.

```cpp
std::atomic<int> counter(0);
counter.fetch_add(1, std::memory_order_relaxed);  // 카운터만 증가
```

대부분의 경우 기본값 `seq_cst`로 충분하다. 성능이 병목이 된 후 프로파일링으로 acquire-release나 relaxed를 검토한다.

### Happens-Before 표로 정리

| 연산 조합 | Happens-Before 보장? | 비용 (상대적) |
|---------|-------------------|----------|
| seq_cst ↔ seq_cst | ✅ 전역 순서 | 높음 |
| release → acquire | ✅ 이 쌍 | 중간 |
| relaxed ↔ relaxed | ❌ 없음 | 낮음 |
| mutex lock/unlock | ✅ 전역 순서 | 중간 |

## Compiler & CPU 최적화의 현실

메모리 모델이 필요한 이유를 다시 보자. 

**컴파일러 최적화**: GCC나 Clang은 데이터 레이스가 없다고 가정하고 코드를 재정렬한다. 예를 들어, 두 변수가 "관련 없다"고 판단하면 순서를 바꾼다.

```cpp
x = 1;
y = 2;
// 컴파일러가 다음으로 최적화할 수 있음
y = 2;
x = 1;
```

**CPU 수행 순서**: x86-64는 store-load 순서만 보장하고, ARM과 PowerPC는 훨씬 더 느슨하다. 따라서 같은 C++ 코드도 CPU에 따라 동작이 달라질 수 있다.

**캐시 불일치**: 멀티코어 CPU에서 각 코어는 자신의 캐시를 갖는다. "cache coherency protocol"(예: MESI, MOESI)이 보장하는 것은 시간이 지나면 모든 코어가 같은 값을 보게 된다는 뜻이지, 즉시는 아니라는 뜻이다.

메모리 모델(특히 atomic과 메모리 순서)은 이 모든 불확실성 위에 **보증된 일관성**을 올린다.

## 안전성 검증: ThreadSanitizer

위험한 코드인지 확인하는 가장 실용적인 도구는 **ThreadSanitizer (TSAN)**다. GCC와 Clang 모두 지원한다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g example.cpp -o example
./example
```

TSAN이 데이터 레이스를 감지하면 즉시 경고한다:

```
WARNING: ThreadSanitizer: data race on variable at 0x... (...)
  Write at ... by thread T1
  Previous read at ... by thread T2
```

이 시리즈의 모든 "깨진 코드" 예제는 TSAN으로 검증되며, "고친 코드"도 마찬가지다.

## 실전: Atomic 카운터의 올바른 패턴

이제 애초의 증가 문제를 올바르게 풀어 보자.

```cpp
#include <iostream>
#include <thread>
#include <atomic>
#include <vector>

std::atomic<int> counter(0);

int main() {
    std::vector<std::thread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([]{
            for (int j = 0; j < 100000; ++j) {
                counter.fetch_add(1, std::memory_order_seq_cst);
            }
        });
    }
    for (auto& t : workers) t.join();
    std::cout << counter << '\n';  // 항상 400000
    return 0;
}
```

이 코드는 safe하다. `atomic<int>`의 `fetch_add`는 읽기-수정-쓰기를 원자적으로 수행하고, 기본 메모리 순서가 `seq_cst`이므로 모든 스레드가 일관된 값을 본다.

성능이 중요하면 relaxed를 쓸 수 있다:

```cpp
counter.fetch_add(1, std::memory_order_relaxed);
```

이 경우 최종 합계는 여전히 400000이지만, 진행 과정의 중간값들은 스레드 간에 일관되지 않을 수 있다. 중간값은 중요하지 않고 최종값만 필요한 경우(예: 이벤트 카운팅) relaxed가 적합하다.

## 학습 성과 평가 기준

이 장을 완주하면 다음을 할 수 있어야 한다.

- [ ] 데이터 레이스를 정의하고, 왜 C++ 표준이 이를 미정의 동작으로 규정했는지 설명할 수 있는가?
- [ ] Happens-before 관계를 예제로 들어 설명할 수 있는가? (예: "락 안의 두 쓰기가 있을 때, 다른 스레드가 락 안에서 읽으면 모두 보인다")
- [ ] `std::atomic<T>`의 `memory_order_seq_cst`, `memory_order_acquire`, `memory_order_relaxed`의 차이와 각각의 용도를 설명할 수 있는가?
- [ ] ThreadSanitizer를 써서 데이터 레이스를 감지하고, atomic 또는 mutex로 고칠 수 있는가?
- [ ] CPU 아키텍처(x86 vs ARM)에 따라 메모리 순서가 다를 수 있다는 것을 이해하는가?

## 다음 장에서는

02장 **「락 관용구(Locking Idioms)」**에서는 이 장의 메모리 모델 개념을 바탕으로, RAII 기반 Scoped Locking 패턴, 그리고 공유 상태를 보호하는 Thread-Safe Interface 패턴을 다룬다. 이 패턴들이 어떻게 happens-before을 만들고 데이터 레이스를 막는지 실제 구현으로 배우게 된다.

## 참고 및 출처

- Anthony Williams, 『C++ Concurrency in Action』(2nd ed., 2019) — Williams의 1~5장이 이 장의 주요 근거
- C++ Standards Committee, 『Working Draft, C++ Standard』 — Memory model clause (1.10 in C++11, 6.9 in C++20)
- Hans Boehm & Mark Adve, "Foundations of the C++ Concurrency Memory Model" (2008) — 표준 메모리 모델 설계의 이론적 배경
- Herb Sutter, "Atomic Weapons" (2012, GotW #86~#100) — atomic 활용법의 실전 가이드


