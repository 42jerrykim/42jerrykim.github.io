---
image: wordcloud.png
title: "[Concurrency Patterns] 02. 락 관용구"
description: "RAII 기반 Scoped Locking, Strategized Locking, Thread-Safe Interface 패턴을 구현하고, 자기 데드락과 인터페이스 위반을 코드로 재현 후 고치는 장입니다."
date: 2026-06-12
lastmod: 2026-06-13
draft: false
collection_order: 2
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - C++
  - Locking
  - Mutex
  - Lock-Guard
  - RAII(Resource Acquisition Is Initialization)
  - Scoped-Locking
  - Thread-Safe-Interface
  - Strategized-Locking
  - Deadlock
  - Self-Deadlock
  - Recursive-Mutex
  - std::mutex
  - std::lock_guard
  - std::unique_lock
  - std::scoped_lock
  - Memory-Order
  - Synchronization
  - Encapsulation(캡슐화)
  - Design-Pattern(디자인패턴)
  - Code-Quality(코드품질)
  - Best-Practices
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Reference(참고)
  - Deep-Dive
  - Concurrency(동시성)
slug: cpp-locking-idioms-scoped-locking-thread-safe-interface
---

02장의 핵심은 간단하지만 강력하다: **공유 상태를 보호하는 일을 `mutex`에만 맡기지 말고, 클래스 설계 자체에 스레드 안전성을 내장하라.** 01장에서 배운 메모리 모델은 "무엇이 safe한가"를 말했고, 이 장에서는 "어떻게 그것을 구조적으로 구현하는가"를 다룬다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [01장: 동시성 기초와 C++ 메모리 모델](/post/multithreading-patterns/getting-started-cpp-concurrency-fundamentals-memory-model/)에서 다룬 "데이터 레이스"와 "happens-before" 개념을 전제로 합니다. 아직 읽지 않았다면 먼저 보고 오세요. `std::mutex`와 `std::lock_guard`의 기본 사용법(생성하면 잠기고, 소멸하면 풀린다)을 알고 있으면 충분합니다.

**이 장의 깊이**: 이 장은 **초급~전문가**까지를 포괄합니다. RAII 기반 락 관리(Scoped Locking)부터 시작해, 클래스 설계 차원에서 자기 데드락을 막는 Thread-Safe Interface, 그리고 락 정책을 교체 가능하게 만드는 Strategized Locking까지 다룹니다. 전문가 구간에서는 `std::recursive_mutex`의 함정, 락 순서 강제, 데드락 탐지 도구까지 다룹니다. **다루지 않는 것**: 락-프리(lock-free) 자료구조, `std::shared_mutex`를 이용한 읽기-쓰기 락(05장), 그리고 스핀락의 성능 미세 튜닝([동시성 최적화 트랙](/post/concurrency-optimization/getting-started-concurrency-multithreading-performance-tuning/)에서 다룹니다).

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "문제" ~ "Scoped Locking 패턴" | lock_guard/scoped_lock 사용법 습득 |
| **중급자** | "Thread-Safe Interface 패턴" ~ "Strategized Locking 패턴" | 자기 데드락을 피하는 클래스 설계 능력 |
| **전문가** | "데드락 회피" ~ "실전: 락 순서와 진단 도구" | 멀티뮤텍스 관리, 락 정책 선택, 데드락 진단 |

---

## 문제: 깨진 Scoped Locking

먼저 틀린 코드부터 보자. 다음은 간단해 보이지만 치명적인 결함이 있는 카운터 클래스다.

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

class Counter {
private:
    mutable std::mutex mu;
    int value = 0;

public:
    int getValue() const {
        mu.lock();      // (1) 락 획득
        int v = value;
        mu.unlock();    // (2) 직접 unlock
        return v;
    }

    void increment() {
        mu.lock();      // (3) 락 획득
        ++value;
        mu.unlock();    // (4) 직접 unlock
    }
};

int main() {
    Counter c;
    std::vector<std::thread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&c]{
            for (int j = 0; j < 10000; ++j) {
                c.increment();
            }
        });
    }
    for (auto& t : workers) t.join();
    std::cout << c.getValue() << '\n';
    return 0;
}
```

이 코드는 몇 가지 문제가 있다.

**1. 예외 안전성 부족**: `lock()`과 `unlock()` 사이에 예외가 발생하면 락이 절대 해제되지 않는다. 결국 데드락.

**2. 직관성 부족**: lock/unlock을 수동으로 짝지어야 하므로 실수할 가능성이 높다.

**3. Getter와 Setter 사이의 레이스**: 다음과 같이 호출되면:

```cpp
int v1 = c.getValue();    // Thread 1: 값 읽음
c.increment();            // Thread 2: 값 증가
int v2 = c.getValue();    // Thread 1: 값 다시 읽음
```

Thread 1이 getValue() → unlock() → increment() 호출 → getValue() 사이에 Thread 2가 increment를 완료하므로, v2 > v1이지만 그사이 increment()는 호출되지 않았다. **즉, 클래스 불변식이 깨진다**.

## Scoped Locking 패턴 (RAII)

**Scoped Locking**은 RAII(Resource Acquisition Is Initialization)를 락에 적용한 패턴이다. 객체 생성 시 락을 획득하고, 소멸 시 자동으로 해제한다. C++ 표준 라이브러리에서 가장 간단한 형태는 `std::lock_guard`다.

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

class Counter {
private:
    mutable std::mutex mu;
    int value = 0;

public:
    int getValue() const {
        std::lock_guard<std::mutex> lock(mu);  // 락 획득
        return value;
        // lock_guard 소멸 시 자동 unlock
    }

    void increment() {
        std::lock_guard<std::mutex> lock(mu);  // 락 획득
        ++value;
        // lock_guard 소멸 시 자동 unlock
    }
};

int main() {
    Counter c;
    std::vector<std::thread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&c]{
            for (int j = 0; j < 10000; ++j) {
                c.increment();
            }
        });
    }
    for (auto& t : workers) t.join();
    std::cout << c.getValue() << '\n';  // 항상 40000
    return 0;
}
```

이제 코드가 훨씬 안전하다. `lock_guard`는 생성자에서 `mu.lock()`을 호출하고, 소멸자에서 자동으로 `mu.unlock()`을 한다. 예외가 발생해도 스택 언와인딩 시 `lock_guard`의 소멸자가 호출되므로 락은 해제된다.

**Scoped Locking의 세 가지 핵심**:

1. **RAII**: 락은 객체 생성 시 획득, 소멸 시 해제.
2. **예외 안전**: 예외가 발생해도 락이 자동 해제.
3. **최소 범위**: 락을 필요한 범위만 유지 → 경합(contention) 감소.

C++17 이상에서는 `std::scoped_lock<std::mutex>`도 제공되는데, 여러 mutex를 안전하게 잠글 때 편하다 (deadlock 회피).

```cpp
std::scoped_lock lock(mu1, mu2);  // 두 락을 안전한 순서로 획득
```

### 안전성 검증: ThreadSanitizer로 확인

위의 "깨진 코드"(직접 `lock()`/`unlock()`)와 "고친 코드"(`lock_guard`)는 사실 둘 다 `++value`만 보면 데이터 레이스가 없다. 하지만 직접 `lock()`/`unlock()` 버전에 예외 처리를 추가했다고 가정하고, `unlock()` 호출을 빠뜨리는 실수를 재현하면 다음과 같은 코드가 된다.

```cpp
int getValue() const {
    mu.lock();
    int v = value;
    if (v < 0) return v;  // (버그) 여기서 unlock() 없이 반환 → 영구 락 보유
    mu.unlock();
    return v;
}
```

이 버그는 데이터 레이스로 잡히지 않는다(락은 정상적으로 "잡혀" 있으므로). 대신 다음 호출에서 **데드락**으로 나타나며, TSAN은 `-fsanitize=thread`에 더해 `tsan` 옵션 `second_deadlock_stack=1`을 켜면 두 번째 lock 시도의 스택까지 보여준다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g counter.cpp -o counter
TSAN_OPTIONS="second_deadlock_stack=1" ./counter
```

반면 `lock_guard` 버전은 모든 반환 경로에서 소멸자가 호출되므로 이런 종류의 버그 자체가 **컴파일 타임에 구조적으로 차단**된다. 이것이 RAII가 "스타일"이 아니라 "정확성 보증"인 이유다.

## Thread-Safe Interface 패턴

**문제**: Scoped Locking만으로는 부족하다. 공개 메서드가 여러 개면, 메서드끼리 호출할 때 같은 mutex를 두 번 잡으려고 시도할 수 있다 (데드락). 또는 메서드들 사이의 불변식이 깨질 수 있다.

예를 들어:

```cpp
class Account {
private:
    std::mutex mu;
    int balance = 100;

public:
    void transfer(Account& other, int amount) {
        std::lock_guard<std::mutex> lock1(mu);
        std::lock_guard<std::mutex> lock2(other.mu);  // 데드락 가능!
        // Thread A: transfer(A->B)는 lock1(A), lock2(B) 순서
        // Thread B: transfer(B->A)는 lock1(B), lock2(A) 순서
        // → circular wait → deadlock
        balance -= amount;
        other.balance += amount;
    }

    bool canWithdraw(int amount) {
        std::lock_guard<std::mutex> lock(mu);
        return balance >= amount;
    }

    void withdraw(int amount) {
        std::lock_guard<std::mutex> lock(mu);
        if (balance >= amount) {
            balance -= amount;
        }
    }

    // 위험한 호출 패턴:
    void unsafeTransfer(Account& other, int amount) {
        if (canWithdraw(amount)) {  // (1) unlock
            withdraw(amount);        // (2) lock, unlock
            other.deposit(amount);   // (3) lock, unlock
        }
        // (1)과 (2) 사이에 다른 스레드가 금액을 뺄 수 있음
    }
};
```

**해결책**: **internal** 메서드(mutex 소유)와 **public** 메서드(사용자 호출)를 분리한다. internal 메서드는 락을 가정하고, public 메서드는 락을 획득해서 internal을 호출한다.

```cpp
class Account {
private:
    mutable std::mutex mu;
    int balance = 100;

    // Internal: 호출자가 이미 mu를 잠겼다고 가정
    int getBalance_unlocked() const {
        return balance;
    }

    void withdraw_unlocked(int amount) {
        if (balance >= amount) {
            balance -= amount;
        }
    }

public:
    // Public: 사용자가 호출, 내부에서 락 획득
    int getBalance() const {
        std::lock_guard<std::mutex> lock(mu);
        return getBalance_unlocked();
    }

    void withdraw(int amount) {
        std::lock_guard<std::mutex> lock(mu);
        withdraw_unlocked(amount);
    }

    void transfer(Account& other, int amount) {
        // 데드락 회피: 주소 순서로 락 획득
        Account* first = this;
        Account* second = &other;
        if (first > second) std::swap(first, second);

        std::lock_guard<std::mutex> lock1(first->mu);
        std::lock_guard<std::mutex> lock2(second->mu);

        if (this->getBalance_unlocked() >= amount) {
            this->withdraw_unlocked(amount);
            other.getBalance_unlocked();  // 읽으려면 _unlocked 호출
            // other.balance += amount; 대신 other의 내부 메서드 쓰기
        }
    }
};
```

더 나은 방식은 **공개 인터페이스와 보호 인터페이스를 명확히** 하는 것이다. 많은 라이브러리는 다음과 같이 한다:

```cpp
class Account {
private:
    std::mutex mu;
    int balance = 100;

public:
    int getBalance() const {
        std::lock_guard<std::mutex> lock(mu);
        return balance;
    }

    // 원자적 연산: 한 번에 unlock, getBalance 수행
    int withdrawAndGetBalance(int amount) {
        std::lock_guard<std::mutex> lock(mu);
        if (balance >= amount) {
            balance -= amount;
        }
        return balance;
    }

    // 또는 콜백으로 원자성 보장
    void atomicUpdate(std::function<void(Account&)> fn) {
        std::lock_guard<std::mutex> lock(mu);
        fn(*this);
    }
};
```

## Strategized Locking 패턴

한 클래스가 여러 동시성 전략을 지원해야 할 때, mutex 타입을 템플릿 파라미터로 받는다.

```cpp
template<typename LockPolicy = std::mutex>
class Counter {
private:
    mutable LockPolicy mu;
    int value = 0;

public:
    int getValue() const {
        std::lock_guard<LockPolicy> lock(mu);
        return value;
    }

    void increment() {
        std::lock_guard<LockPolicy> lock(mu);
        ++value;
    }
};

// 사용:
Counter<std::mutex> c1;           // 단순 mutex
Counter<std::recursive_mutex> c2; // 재귀적 호출 허용

// 락이 필요 없는 단일 스레드 환경에서는 no-op 정책도 가능
struct NullMutex {
    void lock() {}
    void unlock() {}
    bool try_lock() { return true; }
};
Counter<NullMutex> c3;  // 락 오버헤드 0, 단일 스레드 전용
```

이 패턴은 라이브러리 코드에서 흔하다. 사용자가 선택할 수 있도록 유연성을 제공하며, `NullMutex` 같은 정책을 추가하면 "멀티스레드 빌드"와 "싱글스레드 빌드"를 같은 코드베이스로 컴파일 타임에 분기할 수 있다(헤더 전용 라이브러리에서 흔한 기법).

### std::recursive_mutex의 함정

`Counter<std::recursive_mutex>`처럼 `recursive_mutex`를 Strategized Locking의 한 옵션으로 제공하는 것은 흔하지만, **"같은 스레드가 여러 번 lock해도 데드락이 안 난다"는 사실이 설계 문제를 가려버리는 부작용**이 있다.

```cpp
class BadDesign {
    std::recursive_mutex mu;
    int value = 0;
public:
    void increment() {
        std::lock_guard<std::recursive_mutex> lock(mu);
        ++value;
        notifyObservers();  // (위험) 락을 쥔 채 콜백 호출
    }
    void notifyObservers() {
        std::lock_guard<std::recursive_mutex> lock(mu);  // 재귀 lock: 같은 스레드라 OK
        // 만약 observer가 increment()를 다시 호출하면? 여전히 OK (재귀적이므로)
        // 하지만 이미 ++value를 두 번 실행하는 무한 재귀가 될 수 있음
    }
};
```

`recursive_mutex`는 "같은 스레드의 재진입(reentrancy)"만 허용할 뿐, **로직상의 무한 재귀나 불변식 위반을 막아주지 않는다**. 또한 일반 `mutex`보다 lock/unlock 비용이 약간 더 높다(재진입 횟수를 추적하는 카운터 관리 때문). 실무에서 `recursive_mutex`가 필요해 보이는 상황은 대부분 **internal/public 메서드 분리(Thread-Safe Interface)로 재설계하면 사라진다**. 즉 Strategized Locking에서 `recursive_mutex`를 옵션으로 "제공"하는 것과, 그것을 "기본값으로 권장"하는 것은 다르다 — 후자는 설계 결함을 감추는 안티패턴이 되기 쉽다.

## 실전: 데드락 회피 전략

**규칙 1: 락 순서 강제**

여러 락을 획득해야 할 때 항상 같은 순서로 획득한다.

```cpp
// 나쁜 예
void transfer_bad(Account& a, Account& b) {
    std::lock_guard g1(a.mu);      // a 락
    std::lock_guard g2(b.mu);      // b 락 → 데드락 가능
}

void transfer_bad_reverse(Account& a, Account& b) {
    std::lock_guard g1(b.mu);      // b 락 ← 순서 다름
    std::lock_guard g2(a.mu);      // a 락
}

// 좋은 예
void transfer_good(Account& a, Account& b) {
    Account* first = &a;
    Account* second = &b;
    if (first > second) std::swap(first, second);  // 주소로 정렬
    std::lock_guard g1(first->mu);
    std::lock_guard g2(second->mu);
}
```

또는 C++17 `std::scoped_lock`을 쓰면 자동으로 deadlock-free ordering을 보장한다:

```cpp
void transfer_best(Account& a, Account& b) {
    std::scoped_lock lock(a.mu, b.mu);  // 자동으로 안전한 순서
    // ...
}
```

**규칙 2: 홀딩 타임 최소화**

락을 잠시만 유지한다. 특히 I/O 같은 느린 작업은 락 밖에서.

```cpp
// 나쁜 예: I/O 중에 락 유지
void save() {
    std::lock_guard lock(mu);
    file << value << std::flush;  // 느림, 락 유지
}

// 좋은 예
void save() {
    int snapshot;
    {
        std::lock_guard lock(mu);
        snapshot = value;  // 빠른 복사
    }
    file << snapshot << std::flush;  // 락 해제 후 I/O
}
```

**규칙 3: 락 안에서 콜백·가상 함수 호출 금지**

```cpp
// 나쁜 예
void process() {
    std::lock_guard lock(mu);
    callback();  // 혹시 다른 뮤텍스를 잠글 수도, 데드락 위험
}

// 좋은 예
std::function<void()> cb;
{
    std::lock_guard lock(mu);
    cb = callback;
}
cb();  // 락 해제 후 호출
```

## 실전: 락 순서와 진단 도구 (전문가)

`transfer_good`처럼 "주소 순서로 락 획득"하는 방식은 객체 두 개에는 잘 동작하지만, **계층(hierarchy)이 있는 시스템**에서는 더 명시적인 규칙이 필요하다. 예를 들어 "상위 모듈의 락은 하위 모듈의 락보다 먼저 획득해야 한다"는 규칙을 코드로 강제하고 싶을 때, Anthony Williams는 **hierarchical mutex**라는 래퍼를 제안한다.

```cpp
#include <mutex>
#include <stdexcept>
#include <climits>

class HierarchicalMutex {
private:
    std::mutex internal_mutex;
    const unsigned long hierarchy_value;
    unsigned long previous_hierarchy_value = 0;

    // 스레드별로 "현재 보유한 락의 최저 계층 값"을 추적
    static thread_local unsigned long this_thread_hierarchy_value;

    void check_for_hierarchy_violation() {
        if (this_thread_hierarchy_value <= hierarchy_value) {
            throw std::logic_error("mutex hierarchy violated");
        }
    }
    void update_hierarchy_value() {
        previous_hierarchy_value = this_thread_hierarchy_value;
        this_thread_hierarchy_value = hierarchy_value;
    }

public:
    explicit HierarchicalMutex(unsigned long value) : hierarchy_value(value) {}

    void lock() {
        check_for_hierarchy_violation();
        internal_mutex.lock();
        update_hierarchy_value();
    }
    void unlock() {
        if (this_thread_hierarchy_value != hierarchy_value) {
            throw std::logic_error("mutex hierarchy violated on unlock");
        }
        this_thread_hierarchy_value = previous_hierarchy_value;
        internal_mutex.unlock();
    }
    bool try_lock() {
        check_for_hierarchy_violation();
        if (!internal_mutex.try_lock()) return false;
        update_hierarchy_value();
        return true;
    }
};

thread_local unsigned long
    HierarchicalMutex::this_thread_hierarchy_value(ULONG_MAX);

// 사용: 숫자가 클수록 "상위" 계층
HierarchicalMutex highLevelMutex(10000);
HierarchicalMutex lowLevelMutex(5000);

void doLowLevelStuff() {
    std::lock_guard<HierarchicalMutex> lock(lowLevelMutex);
    // ...
}

void doHighLevelStuff() {
    std::lock_guard<HierarchicalMutex> lock1(highLevelMutex);
    doLowLevelStuff();  // OK: 5000 < 10000, 순서 올바름
    // 만약 doLowLevelStuff()가 highLevelMutex를 다시 잠그면
    // check_for_hierarchy_violation()이 std::logic_error를 던진다
}
```

`HierarchicalMutex`는 `std::lock_guard`/`std::unique_lock`이 요구하는 `lock()`/`unlock()`/`try_lock()` 인터페이스를 만족하므로, Strategized Locking의 정책 타입으로도 그대로 쓸 수 있다(`Counter<HierarchicalMutex>`). 위반 시 즉시 `std::logic_error`로 **실행 시점에** 락 순서 위반을 잡아낸다 — 데드락이 실제로 발생하기 전에 개발/테스트 단계에서 드러나게 하는 것이 핵심이다.

**플랫폼별 진단 도구**:

- **TSAN (`-fsanitize=thread`)**: 데이터 레이스뿐 아니라 **lock-order-inversion(잠재적 데드락)**도 보고한다. 두 스레드가 `(A, B)`와 `(B, A)` 순서로 락을 잡는 패턴을 관찰하면, 실제로 데드락이 발생하지 않아도 경고를 띄운다.
- **Valgrind의 `--tool=helgrind`**: TSAN과 유사하게 락 순서 추적과 POSIX 동기화 오류를 검사한다. 컴파일러 계측 없이 동작하지만 실행 속도가 훨씬 느리다.
- **GDB**: 데드락이 실제로 걸린 후에는 `gdb -p <pid>`로 attach해 `thread apply all bt`로 모든 스레드의 백트레이스를 확인하면, 어떤 스레드가 어떤 락을 기다리는지(circular wait)가 드러난다.
- **Windows(MSVC)**: Visual Studio의 **Concurrency Visualizer**가 스레드별 대기 시간과 락 경합(contention)을 시각화한다. WinDbg의 `!locks` 확장 명령은 critical section의 소유자를 보여준다.

## 학습 성과 평가 기준

- [ ] Scoped Locking (lock_guard, scoped_lock) 패턴을 RAII 관점에서 설명할 수 있는가?
- [ ] 자기 데드락(self-deadlock) 문제를 코드로 재현하고 recursive_mutex 또는 internal/public 분리로 고칠 수 있는가?
- [ ] Thread-Safe Interface 패턴에서 internal 메서드와 public 메서드의 역할을 설명할 수 있는가?
- [ ] 여러 뮤텍스를 획득할 때 데드락을 회피하는 방법(주소 정렬, scoped_lock)을 적용할 수 있는가?
- [ ] 락 안에서 호출하면 안 되는 것들(I/O, 콜백, 가상 함수)을 식별할 수 있는가?
- [ ] `std::recursive_mutex`가 왜 "기본 권장"이 아니라 예외적 도구인지 설명할 수 있는가?
- [ ] 락 순서 위반을 실행 시점에 감지하는 방법(hierarchical mutex)과 TSAN/Helgrind 같은 도구의 차이를 설명할 수 있는가?

## 다음 장에서는

03장 **「대기와 조정(Waiting and Coordination)」**에서는 조건 변수(`std::condition_variable`)와 `spurious wakeup` 처리, Monitor Object, Guarded Suspension 패턴을 다룬다. 이 패턴들은 "값이 언제 준비될 때까지 효율적으로 기다리는가"를 구현한다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 3 — Scoped Locking 패턴의 원형
- Anthony Williams, 『C++ Concurrency in Action』(2nd ed., 2019), Chapter 3 — mutex, RAII 기반 락, hierarchical mutex 설계
- C++ Standards Committee, `<mutex>` documentation — lock_guard, scoped_lock, unique_lock, recursive_mutex
- LLVM Project, "ThreadSanitizer" documentation — lock-order-inversion 탐지와 TSAN_OPTIONS


