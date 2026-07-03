---
image: wordcloud.png
title: "[Concurrency Patterns] 11. 공유 회피"
description: "공유 상태를 애초에 없애는 전략: Immutable 패턴, Copy-on-Write, thread_local, 그리고 lock-free 자료구조의 전망을 다룹니다."
date: 2026-06-21
lastmod: 2026-06-22
draft: false
collection_order: 11
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Shared-State-Avoidance
  - Immutable
  - Copy-on-Write
  - CoW
  - thread_local
  - Lock-Free
  - Concurrency(동시성)
  - Design-Pattern(디자인패턴)
  - Performance(성능)
  - 안전
  - Functional-Programming(함수형프로그래밍)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
slug: cpp-avoiding-shared-state-immutable-cow-thread-local
---

이 시리즈의 마지막 장은 **공유 상태 자체를 없애는 전략**을 다룬다. 지금까지 "공유 상태를 보호하는 방법"을 배웠다면, 11장은 "공유하지 않는 방법"을 배운다. 이것이 가장 근본적인 해결책이다. 락은 잘 설계해도 경쟁(contention)과 데드락 위험이 남는다. 반면 "처음부터 공유하지 않는다"는 전략은 그 위험을 설계 단계에서 제거한다 — 대신 메모리와 복사라는 다른 비용을 지불할 뿐이다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [10장 「이벤트 아키텍처 II: Proactor와 Half-Sync/Half-Async」](/post/multithreading-patterns/cpp-proactor-async-io-half-sync-half-async/)까지의 전체 맥락, 특히 01장의 메모리 모델(happens-before, atomic)과 02장의 락 관용구를 알고 있다고 가정합니다. "왜 락이 필요한가"를 이해해야 "왜 락이 필요 없는 구조가 더 좋은가"를 판단할 수 있기 때문입니다.

**이 장의 깊이**: 이 장은 **심화(advanced)** 수준입니다. `std::shared_ptr`의 atomic 교체를 이용한 실전 Copy-on-Write 패턴, `thread_local`을 활용한 스레드별 자원 관리, 그리고 `std::atomic`만으로 구현하는 교육용 SPSC(Single-Producer Single-Consumer) Lock-Free 큐를 직접 구현하고 검증하는 것이 목표입니다.

**다루지 않는 것**: 이 장의 Lock-Free 큐 예제는 **교육 목적**이며, 프로덕션에서 그대로 사용하기 위한 것이 아닙니다. ABA 문제, 메모리 회수(hazard pointer, epoch-based reclamation), 다중 생산자/다중 소비자(MPMC) 큐, 범용 lock-free 자료구조의 완전한 정확성 증명은 이 장의 범위 밖입니다. 이런 자료구조가 실제로 필요하다면 Boost.Lockfree, Intel TBB, folly 같은 검증된 라이브러리를 사용해야 합니다 — 이 장의 목표는 "lock-free가 왜 어려운지"를 손으로 만들어 보며 체감하는 것입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "Immutable 패턴" ~ "thread_local" | 기본 공유 회피 기법 습득 |
| **고급자** | 전체, "Copy-on-Write" 섹션 | 패턴 간의 트레이드오프 이해 |
| **성능 전문가** | "패턴 선택 가이드" | 실제 시스템에서 어떤 패턴 쓸지 판단 |

---

## 핵심 원리

**공유 상태가 없으면 동기화도 필요 없다.** 그 대신의 비용은 메모리와 복사다. 이 트레이드오프는 상황마다 다르다.

| 패턴 | 메모리 | 성능 | 복잡도 |
|------|--------|------|--------|
| Immutable | 높음 | 빠름 (복사 비용) | 낮음 |
| Copy-on-Write | 중간 | 높음 (읽기 최적화) | 높음 |
| thread_local | 높음 | 매우 빠름 | 중간 |
| Lock-Free | 중간 | 매우 높음 (비용) | 매우 높음 |

## Immutable 패턴

**Immutable 객체**: 생성 후 상태가 바뀌지 않는 객체. 여러 스레드에서 동시에 읽어도 완전히 안전하다.

```cpp
class ImmutableString {
private:
    const std::string data;

public:
    ImmutableString(const std::string& s) : data(s) {}

    // 읽기만 가능
    std::string_view get() const { return data; }
    size_t length() const { return data.length(); }

    // "수정"은 새 객체 반환
    ImmutableString toUpper() const {
        std::string upper = data;
        std::transform(upper.begin(), upper.end(), upper.begin(),
                      [](unsigned char c) { return std::toupper(c); });
        return ImmutableString(upper);
    }
};
```

**사용**:

```cpp
ImmutableString original("hello");

std::vector<std::thread> readers;
for (int i = 0; i < 10; ++i) {
    readers.emplace_back([original] {
        // 안전: 동시에 읽어도 문제 없음
        std::cout << original.get() << '\n';
    });
}

// "수정"은 새 객체 생성
ImmutableString modified = original.toUpper();  // "HELLO"
```

**장점**:
- 동기화 불필요
- 스레드 안전성 보증 (타입 수준)
- 함수형 프로그래밍 스타일

**단점**:
- 매 수정마다 복사 비용
- 메모리 사용량 증가

## Copy-on-Write (CoW)

Immutable의 단점을 보완한다. **읽기는 공유, 쓰기는 복사**. 핵심 아이디어는 "현재 버전을 가리키는 포인터를 atomic하게 교체"하는 것이다 — `std::shared_ptr`의 atomic 연산(`std::atomic_load`/`std::atomic_store`, C++20부터는 `std::atomic<std::shared_ptr<T>>`)을 쓰면 락 없이도 안전하게 "버전 스왑"을 할 수 있다.

```cpp
// cow_config.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 cow_config.cpp -o cow_config
#include <atomic>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <thread>
#include <vector>

// 설정(Config) 객체: 한 번 만들어지면 절대 수정하지 않는다 (Immutable).
struct Config {
    std::map<std::string, std::string> values;
};

// CoW 컨테이너: "현재 설정을 가리키는 shared_ptr"을 atomic하게 교체한다.
class ConfigStore {
public:
    explicit ConfigStore(std::shared_ptr<const Config> initial)
        : current_(std::move(initial)) {}

    // 읽기: 락 없이 현재 버전의 shared_ptr을 얻는다.
    // 이후 reload()가 일어나도 이 스냅샷은 안전하게 유지된다.
    std::shared_ptr<const Config> get() const {
        return std::atomic_load_explicit(&current_, std::memory_order_acquire);
    }

    // 쓰기: 기존 설정을 복사 + 수정한 "새 객체"를 만들고, 포인터만 교체한다.
    void update(const std::string& key, const std::string& value) {
        std::shared_ptr<const Config> oldCfg, newCfg;
        do {
            oldCfg = get();
            auto copy = std::make_shared<Config>(*oldCfg);  // 복사 (Copy)
            copy->values[key] = value;                       // 수정은 복사본에
            newCfg = std::move(copy);
        } while (!std::atomic_compare_exchange_weak_explicit(
            &current_, &oldCfg, newCfg,
            std::memory_order_release, std::memory_order_relaxed));
    }

private:
    mutable std::shared_ptr<const Config> current_;
};

int main() {
    auto initial = std::make_shared<Config>();
    initial->values["timeout"] = "30s";
    ConfigStore store(initial);

    // 읽기 스레드: 락 없이 현재 설정의 스냅샷을 읽는다.
    std::vector<std::thread> readers;
    for (int i = 0; i < 4; ++i) {
        readers.emplace_back([&store, i] {
            for (int j = 0; j < 5; ++j) {
                auto cfg = store.get();  // 스냅샷 — 이후 update에 영향받지 않음
                std::cout << "reader " << i << ": timeout="
                          << cfg->values.at("timeout") << '\n';
            }
        });
    }

    // 쓰기 스레드: 새 버전을 만들어 포인터만 교체한다.
    std::thread writer([&store] {
        store.update("timeout", "60s");
    });

    for (auto& t : readers) t.join();
    writer.join();
    return 0;
}
```

**핵심**: 읽기 스레드가 `get()`으로 얻은 `shared_ptr`은 그 시점의 **불변 스냅샷**이다. `update()`가 새 `Config`를 만들어 `current_`를 교체해도, 이미 스냅샷을 들고 있는 읽기 스레드는 그 객체가 (참조 카운트 덕분에) 살아있는 동안 안전하게 사용할 수 있다 — 락도, 데이터 레이스도 없다. 대신 `update()`마다 전체 `Config` 복사가 발생하므로, **쓰기가 드물고 읽기가 압도적으로 많은** 설정 객체, 라우팅 테이블, 캐시 등에 적합하다.

### 안전성 검증

`current_`에 대한 모든 접근이 `std::atomic_load_explicit`/`compare_exchange_weak_explicit`를 거치므로, `current_` 자체에 대한 데이터 레이스는 없다. 만약 `get()`이나 `update()`에서 atomic 연산 없이 `current_ = newCfg;`처럼 직접 대입한다면, `g++ -fsanitize=thread`로 빌드한 멀티스레드 실행에서 `shared_ptr`의 내부 제어 블록 접근 지점에 `WARNING: ThreadSanitizer: data race`가 보고된다.

**어디에 유용한가?**
- 읽기가 대부분인 경우 (예: 설정 객체, 라우팅 테이블)
- 드물게 수정되는 경우

## thread_local 패턴

**각 스레드가 자신만의 복사본을 가진다.** 공유 자체가 없으므로 동기화 불필요.

가장 흔한 실전 사례 중 하나는 **스레드별 난수 생성기**다. `std::mt19937`는 내부 상태를 갖는 객체이므로, 여러 스레드가 하나의 인스턴스를 공유하면 `()` 호출이 데이터 레이스가 된다. 매번 mutex로 보호하는 대신, **각 스레드가 자신만의 엔진을 갖게** 하면 동기화 자체가 사라진다.

```cpp
// thread_local_rng.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 thread_local_rng.cpp -o tlrng
#include <iostream>
#include <random>
#include <thread>
#include <vector>

// 각 스레드가 자신만의 시드로 초기화된 엔진을 가진다.
// std::random_device로 시드를 섞어, 스레드마다 다른 시퀀스를 보장한다.
int threadLocalRandomInt(int low, int high) {
    static thread_local std::mt19937 engine{
        std::random_device{}() ^
        static_cast<unsigned>(
            std::hash<std::thread::id>{}(std::this_thread::get_id()))
    };
    std::uniform_int_distribution<int> dist(low, high);
    return dist(engine);
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([i] {
            for (int j = 0; j < 3; ++j) {
                std::cout << "thread " << i << ": "
                          << threadLocalRandomInt(1, 100) << '\n';
            }
        });
    }
    for (auto& t : threads) t.join();
    return 0;
}
```

`engine`은 함수 지역 `static thread_local` 변수이므로, 각 스레드가 **처음 이 함수를 호출할 때** 자신만의 엔진을 한 번 초기화하고, 이후 호출은 그 스레드의 엔진을 재사용한다. mutex 없이도 두 스레드가 동시에 호출해도 안전하다 — 서로 다른 메모리 위치에 접근하기 때문에 데이터 레이스의 정의(01장)를 만족하지 않는다.

같은 패턴은 **스레드별 출력 버퍼**(로그를 모아서 한 번에 flush), **스레드별 메모리 풀/할당자 캐시**(malloc 경쟁 회피) 등에도 적용된다.

### 카운터 예제와 출력 보장

가장 단순한 형태는 스레드별 카운터다.

```cpp
class ThreadLocalCounter {
private:
    static thread_local int count;

public:
    static void increment() { ++count; }  // 각 스레드만의 count
    static int get() { return count; }
};

thread_local int ThreadLocalCounter::count = 0;

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([] {
            for (int j = 0; j < 1000; ++j) ThreadLocalCounter::increment();
            std::cout << "Thread " << std::this_thread::get_id()
                      << " count: " << ThreadLocalCounter::get() << '\n';
        });
    }
    for (auto& t : threads) t.join();
    return 0;
}
```

**출력**: 각 스레드가 정확히 1000을 출력한다(동기화 불필요). `++count`는 여러 스레드에서 동시에 실행되지만, 각 스레드가 **서로 다른 `count` 인스턴스**에 접근하므로 01장에서 본 "공유 변수에 대한 읽기-수정-쓰기 레이스"는 처음부터 발생하지 않는다.

**사용처**:
- 스레드별 통계 (로깅 버퍼, 성능 카운터)
- 스레드별 상태 (random seed, 예외 정보)
- 스레드풀의 워커별 캐시

**주의점**:
- 메모리: 스레드 수 × 데이터 크기 — 스레드풀처럼 스레드 수가 고정이면 괜찮지만, 스레드를 계속 생성하는 구조에서는 메모리가 누적될 수 있다.
- 초기화: 모든 스레드에서 별도로 초기화 필요 (위 예제처럼 함수-지역 `static thread_local`로 lazy 초기화하면 이 문제를 피할 수 있다)

## Lock-Free 자료구조: 전망

**Lock-Free**: mutex를 사용하지 않고 atomic으로만 구현. 극도로 높은 성능, 극도로 높은 복잡도. 일반적인 Lock-Free 스택/큐(다중 생산자·다중 소비자, MPMC)는 메모리 회수 문제(ABA, hazard pointer) 때문에 정확하게 구현하기가 매우 어렵다. 하지만 **SPSC(Single-Producer Single-Consumer)** — "생산자 스레드 하나, 소비자 스레드 하나"로 제한하면 — 문제가 극적으로 단순해진다. 이 제약 덕분에 SPSC 큐는 lock-free 자료구조 중 가장 흔히 손으로 구현되는 형태이며, "atomic만으로 동기화가 어떻게 성립하는가"를 보여주는 좋은 교육 사례다.

> **주의**: 아래 구현은 **교육용**이다. 고정 크기 배열을 사용하며, 큐가 가득 차면 `push`가 실패를 반환한다. 프로덕션에서는 Boost.Lockfree의 `spsc_queue`, folly의 `ProducerConsumerQueue` 등 검증된 구현을 사용해야 한다.

```cpp
// spsc_queue.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 spsc_queue.cpp -o spsc
#include <array>
#include <atomic>
#include <iostream>
#include <optional>
#include <thread>

// 교육용 SPSC(Single-Producer Single-Consumer) Lock-Free 큐.
// 생산자 1개, 소비자 1개라는 전제 덕분에 head/tail을 각각
// 한 스레드만 "쓰고", 다른 스레드는 "읽기만" 한다 — 그래서
// compare_exchange 루프 없이 단순 load/store로 충분하다.
template <typename T, size_t Capacity>
class SpscQueue {
public:
    // 생산자 스레드에서만 호출
    bool push(const T& value) {
        size_t tail = tail_.load(std::memory_order_relaxed);
        size_t nextTail = (tail + 1) % Capacity;
        if (nextTail == head_.load(std::memory_order_acquire)) {
            return false;  // 큐 가득 참
        }
        buffer_[tail] = value;
        // release: 이 쓰기 이전의 모든 쓰기(buffer_[tail] 대입)가
        // consumer의 acquire 읽기에 보이도록 강제한다.
        tail_.store(nextTail, std::memory_order_release);
        return true;
    }

    // 소비자 스레드에서만 호출
    std::optional<T> pop() {
        size_t head = head_.load(std::memory_order_relaxed);
        if (head == tail_.load(std::memory_order_acquire)) {
            return std::nullopt;  // 큐 비어 있음
        }
        T value = buffer_[head];
        head_.store((head + 1) % Capacity, std::memory_order_release);
        return value;
    }

private:
    std::array<T, Capacity> buffer_{};
    std::atomic<size_t> head_{0};  // 소비자가 쓰고, 생산자가 읽음
    std::atomic<size_t> tail_{0};  // 생산자가 쓰고, 소비자가 읽음
};

int main() {
    SpscQueue<int, 1024> queue;
    constexpr int kCount = 100000;

    std::thread producer([&queue] {
        for (int i = 0; i < kCount; ++i) {
            while (!queue.push(i)) {
                std::this_thread::yield();  // 큐가 가득 차면 잠시 양보
            }
        }
    });

    std::thread consumer([&queue] {
        for (int i = 0; i < kCount; ++i) {
            std::optional<int> value;
            while (!(value = queue.pop())) {
                std::this_thread::yield();  // 큐가 비어 있으면 잠시 양보
            }
            if (*value != i) {
                std::cerr << "순서 오류: expected " << i << ", got " << *value << '\n';
                std::abort();
            }
        }
    });

    producer.join();
    consumer.join();
    std::cout << "OK: " << kCount << "개 모두 순서대로 전달됨\n";
    return 0;
}
```

**왜 이것이 "lock-free"인가**: `push`와 `pop` 어디에도 mutex나 `compare_exchange`(재시도 루프)가 없다. `head_`와 `tail_`은 각각 한쪽 스레드만 쓰고(write), 다른 쪽은 읽기만(read) 하므로 **경쟁(contention)이 구조적으로 존재하지 않는다**. `memory_order_release`/`memory_order_acquire` 쌍이 01장에서 배운 happens-before 관계를 만든다 — `tail_.store(release)`는 `buffer_[tail]`에 대한 쓰기가 `tail_.load(acquire)`를 통해 소비자에게 보이도록 보장한다. 이 release/acquire 쌍이 없다면(예: 둘 다 `relaxed`라면) 소비자가 `tail_`이 갱신된 것은 보지만 `buffer_[tail]`의 새 값은 아직 못 보는 상황이 이론적으로 가능해진다.

### 안전성 검증

이 큐를 `g++ -fsanitize=thread`로 빌드해 실행하면 정상 동작 시 TSAN 경고가 없어야 한다. 의도적으로 `memory_order_release`/`acquire`를 `memory_order_relaxed`로 바꿔서 실행해 보면 — TSAN은 이런 미묘한 순서 문제를 항상 잡아내지는 못하지만(원자성 자체는 깨지지 않으므로), **결과 값 오류**("순서 오류" 메시지)가 더 자주 관찰될 수 있다. 이것이 "lock-free가 검증하기 어렵다"는 말의 실체다 — 컴파일되고, 대부분 실행에서 통과하지만, 특정 메모리 순서/CPU/타이밍에서만 깨지는 코드가 만들어지기 쉽다.

**현실**:
- 일반적인(MPMC) lock-free 자료구조는 **책으로는 배우기 어렵고**, 보증된 라이브러리 (Boost.Lockfree, TBB, folly)를 사용할 것을 강력히 권장한다.
- 정확성 검증이 매우 어렵다 (10년 경력 해서도 버그 있음). SPSC처럼 제약이 강한 특수 케이스만 손으로 구현을 시도할 가치가 있다.
- 성능 이득이 실제로 필요한 경우는 드물다 (보통 mutex가 충분하다 — 이 시리즈의 02장에서 본 Scoped Locking으로 시작하고, 프로파일링 후에만 lock-free를 고려한다).

## 패턴 선택 가이드

```
1. 공유 상태가 필요한가?
   → 아니오: thread_local 사용
   
2. 쓰기가 드문가?
   → 예: Copy-on-Write
   
3. 쓰기가 많은가?
   → 예: mutex (이전 장들)
   
4. 극도의 성능이 필요한가?
   → 예: lock-free (라이브러리 사용)
```

## 학습 성과 평가 기준

- [ ] Immutable 패턴을 구현하고, 왜 안전한지 설명할 수 있는가?
- [ ] `std::shared_ptr`의 atomic 교체를 이용한 Copy-on-Write를 구현하고, "읽기 스냅샷이 왜 안전한가"를 설명할 수 있는가?
- [ ] `thread_local`로 스레드별 난수 생성기/버퍼를 구현하고, 언제 쓸지·메모리 비용은 어떻게 되는지 판단할 수 있는가?
- [ ] `std::atomic`만으로 SPSC Lock-Free 큐를 구현하고, `memory_order_release`/`acquire` 쌍이 왜 필요한지 설명할 수 있는가?
- [ ] Lock-Free가 왜 어렵고 위험한지, SPSC와 MPMC의 난이도 차이를 이해하는가?

## 시리즈 완수 평가 기준

이 컬렉션 전체를 완주하면 [00장 「시리즈 소개」](/post/multithreading-patterns/getting-started-multithreading-design-patterns/)에서 제시한 목표 — "락을 어디에 넣지?"가 아니라 "이 문제는 어떤 패턴의 변형이지?"라는 어휘로 사고하는 것 — 를 다음 구체적 역량으로 점검할 수 있어야 한다.

- [ ] 멀티스레드 문제를 "메모리 모델" 언어로 진단할 수 있다. (01)
- [ ] 데이터 레이스를 Scoped Locking, Monitor Object, Guarded Suspension으로 해결할 수 있다. (02~03)
- [ ] Producer-Consumer를 Bounded Buffer로 구현하고 backpressure를 제어할 수 있다. (04)
- [ ] 읽기 위주 워크로드를 shared_mutex나 call_once로 최적화할 수 있다. (05)
- [ ] Thread Pool, Future/Promise, Active Object를 설계하고 구현할 수 있다. (06~08)
- [ ] `poll()` 기반 Reactor와 Proactor(완료 통지) 의미의 차이를 코드로 구현·구분할 수 있다. (09~10)
- [ ] `condition_variable` 기반 큐로 비동기 계층과 동기 계층을 분리하는 Half-Sync/Half-Async 구조를 설계할 수 있다. (10)
- [ ] Immutable, Copy-on-Write, thread_local로 공유를 회피하고, SPSC Lock-Free 큐의 동작 원리를 설명할 수 있다. (11)
- [ ] 각 패턴의 트레이드오프(메모리, 성능, 복잡도)를 이해하고, 보호(02, 05)·대기(03)·흐름(04)·실행(06~08)·아키텍처(09~10)·회피(11)의 6개 층위로 문제를 분류해 설계 리뷰에서 대안을 제시할 수 있다.

## 마치며

[00장 「시리즈 소개」](/post/multithreading-patterns/getting-started-multithreading-design-patterns/)는 "멀티스레드 코드가 무너지는 순간은 락 문법을 몰라서가 아니라, 어디에 어떤 구조로 동기화를 배치할지 설계하지 않아서 온다"는 문제의식에서 출발했다. 11개 장을 거치며 우리는 그 질문에 답하는 어휘 체계를 하나씩 쌓았다 — 01장의 메모리 모델은 "안전하다"는 말의 정의를 주었고, 02~05장은 단일 객체를 보호하는 관용구를, 04·06~08장은 스레드 사이의 데이터 흐름과 실행 관리를, 09~10장은 시스템 수준의 이벤트 아키텍처를 다뤘다.

마지막 11장은 이 모든 것의 **전제를 뒤집는다**: 지금까지 "공유 상태를 어떻게 안전하게 보호할 것인가"를 물었다면, 이제는 "이 상태를 정말 공유해야 하는가"를 먼저 묻는다. Immutable과 Copy-on-Write는 "데이터를 공유하지만 변경 시점을 분리"하고, thread_local은 "데이터 자체를 분리"하며, Lock-Free는 "보호 메커니즘(락)을 atomic 연산으로 대체"한다. 세 전략 모두 02장에서 시작한 "락이 필요한 이유"를 거꾸로 비추는 거울이다 — 락이 왜 필요한지 모르면, 락이 왜 필요 없어지는지도 알 수 없다.

실무에서:
- **작은 시스템**: Scoped Locking + Monitor Object로 충분
- **중간 시스템**: Thread Pool + Future, Half-Sync/Half-Async 조합
- **대규모 시스템**: Event-Driven (Reactor/Proactor) + thread_local + Immutable/CoW 혼합, 핫패스에 한정해 SPSC Lock-Free 큐 검토

무엇보다 중요한 것은 **"왜 동기화가 필요한가"를 이해하고, 가장 간단한 패턴부터 시작**하는 것이다. 복잡한 패턴은 필요할 때만, 그리고 프로파일링으로 그 필요성이 증명된 뒤에만 도입한다. 이 시리즈에서 익힌 구조적 어휘를 가지고, [Low-latency 동시성·멀티스레드 트랙](/post/concurrency-optimization/getting-started-concurrency-multithreading-performance-tuning/)에서 같은 패턴들을 "비용"의 관점으로 다시 보면, 구조와 성능이라는 두 축이 맞물려 입체적인 그림이 완성된다.

## 참고 및 출처

- Brian Goetz, 『Java Concurrency in Practice』, Chapter 5 — Immutable & Thread-Safe
- Anthony Williams, 『C++ Concurrency in Action』(2nd ed., 2019) — Lock-Free 자료구조와 memory_order 실전 활용
- POSA2 (Schmidt et al.), 전체 — 모든 패턴의 원형
- C++ Standards Committee, 전체 — std::thread, mutex, atomic, shared_ptr, future documentation
- Boost.Lockfree, folly 문서 — 프로덕션 수준 Lock-Free 자료구조 참고


