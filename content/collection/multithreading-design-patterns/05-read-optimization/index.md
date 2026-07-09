---
image: wordcloud.png
title: "[Concurrency Patterns] 05. 읽기 최적화와 지연 초기화"
description: "shared_mutex로 읽기/쓰기 락 분리, DCLP의 함정과 해결, call_once를 통한 안전한 지연 초기화를 학습합니다."
date: 2026-06-15
lastmod: 2026-06-16
draft: false
collection_order: 5
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - shared_mutex
  - Read-Write-Lock
  - DCLP
  - Double-Checked-Locking-Pattern
  - Lazy-Initialization
  - call_once
  - once_flag
  - Read-Optimization
  - Synchronization
  - Design-Pattern(디자인패턴)
  - Performance(성능)
  - Optimization(최적화)
  - Memory-Order
  - Volatile
  - Singleton
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
slug: cpp-read-write-lock-dclp-call-once-lazy-init
---

05장은 **읽기 작업이 대부분인 시나리오**의 최적화를 다룬다. 많은 시스템에서 쓰기(변경)는 드물고 읽기는 대부분이다. 기존의 단일 mutex는 읽기들까지 직렬화하므로 비효율적이다. 이 장에서는 읽기와 쓰기를 분리하고, 초기화 비용을 한 번만 치르는 패턴을 배운다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [02장: 락 관용구](/post/multithreading-patterns/cpp-locking-idioms-scoped-locking-thread-safe-interface/)에서 다룬 `std::mutex`, `std::lock_guard`, 그리고 01장의 `memory_order_acquire`/`memory_order_release`를 전제로 합니다. 특히 DCLP 섹션은 01장의 happens-before 개념 없이는 "왜 위험했는지"가 와닿지 않으니, 아직이라면 01장과 02장을 먼저 보세요.

**이 장의 깊이**: 이 장은 **중급~전문가**까지를 포괄합니다. `std::shared_mutex`로 읽기/쓰기를 분리하는 기본기부터 시작해, DCLP의 역사적 함정과 C++11 이후의 올바른 구현, 그리고 `call_once`/정적 지연 초기화까지 다룹니다. 전문가 구간에서는 `shared_mutex`가 실제로 손해인 상황과 플랫폼별 구현 차이까지 다룹니다. **다루지 않는 것**: lock-free 읽기 전용 자료구조의 구현은 이 장에서 다루지 않는다. 11장이 그 전망만 짧게 언급하고, [13장 「Lock-Free 심화: Hazard Pointer와 RCU」](/post/multithreading-patterns/cpp-hazard-pointer-rcu-lockfree-reclamation/)에서 Hazard Pointer와 RCU를 직접 구현하며 본격적으로 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "문제" ~ "std::call_once" | shared_mutex와 call_once 사용법 |
| **고급자** | 전체, 특히 "DCLP" 섹션 | DCLP의 위험성과 올바른 구현 이해 |
| **성능 전문가** | "DCLP" ~ "성능 비교" | 각 기법의 성능 트레이드오프 분석 |

---

## 문제: Mutex의 과도한 직렬화

```cpp
class Config {
private:
    std::mutex mu;
    std::string data;

public:
    std::string read() {
        std::lock_guard<std::mutex> lock(mu);  // 읽기도 락
        return data;
    }

    void update(const std::string& val) {
        std::lock_guard<std::mutex> lock(mu);  // 쓰기도 락
        data = val;
    }
};
```

이 코드에서 **읽기가 1000번, 쓰기가 1번**이라도 모든 읽기는 같은 mutex를 기다려야 한다. CPU 시간 낭비.

## Read-Write Lock: shared_mutex

C++17부터 `std::shared_mutex`를 지원한다. **여러 읽기는 동시에**, 쓰기는 배타적으로 진행된다.

```cpp
#include <shared_mutex>

class Config {
private:
    mutable std::shared_mutex mu;
    std::string data;

public:
    std::string read() const {
        std::shared_lock<std::shared_mutex> lock(mu);  // 읽기 락
        return data;
    }

    void update(const std::string& val) {
        std::unique_lock<std::shared_mutex> lock(mu);  // 쓰기 락
        data = val;
    }
};
```

**shared_lock vs unique_lock**:

| | `std::shared_lock<std::shared_mutex>` | `std::unique_lock<std::shared_mutex>` |
|---|---|---|
| 동시 보유 | 여러 스레드 (읽기 락, "shared" 상태) | 단 하나 (쓰기 락, "exclusive" 상태) |
| 다른 shared_lock과 공존 | 가능 | 불가능 |
| 다른 unique_lock과 공존 | 불가능 | 불가능 |
| 대응 락 함수 | `mu.lock_shared()` / `unlock_shared()` | `mu.lock()` / `unlock()` |
| 02장의 대응 | `std::lock_guard<std::mutex>`와 동일한 RAII 모델 | 동일 |

두 타입 모두 02장에서 배운 RAII 락 가드와 동일한 원칙을 따른다 — 생성 시 잠기고 소멸 시 풀린다. 차이는 오직 *어떤 모드로* `shared_mutex`를 잠그느냐다.

```cpp
int main() {
    Config cfg;

    // 읽기 스레드 4개: 동시 진행
    std::vector<std::thread> readers;
    for (int i = 0; i < 4; ++i) {
        readers.emplace_back([&cfg] {
            for (int j = 0; j < 100; ++j) {
                auto val = cfg.read();
            }
        });
    }

    // 쓰기 스레드 1개: 읽기가 없을 때만 진행
    std::thread writer([&cfg] {
        for (int i = 0; i < 10; ++i) {
            cfg.update(std::to_string(i));
        }
    });

    for (auto& t : readers) t.join();
    writer.join();
    return 0;
}
```

**성능**: 읽기는 병렬화되므로 처리량 증가. 쓰기는 여전히 배타적이지만 빈번하지 않으면 괜찮음.

### shared_mutex의 실제 비용과 RW 락이 손해인 경우

`shared_mutex`는 "공짜로 빠른 락"이 아니다. 내부적으로 "현재 몇 명이 읽고 있는가"를 추적하는 카운터를 원자적으로 갱신해야 하므로, **읽기 락 자체의 획득/해제 비용은 일반 `std::mutex`의 lock/unlock보다 오히려 높다.** 여러 코어가 동시에 이 카운터를 증가/감소시키면 그 카운터가 들어 있는 캐시 라인을 두고 코어 간 핑퐁(false sharing과 유사한 현상)이 발생한다.

따라서 `shared_mutex`가 이득인 조건은 명확하다.

- **임계 구역이 충분히 길다**: 읽기 작업 자체(데이터 복사, 계산)가 락 오버헤드보다 훨씬 커야 카운터 경합 비용을 상쇄한다.
- **읽기/쓰기 비율이 매우 높다**: 읽기가 99% 이상이고 동시 읽기 스레드 수가 많을 때 병렬성의 이득이 카운터 비용을 압도한다.

반대로 다음 경우에는 **일반 `std::mutex`가 더 빠르다**:

- **임계 구역이 매우 짧다** (예: `int` 하나를 읽고 반환): mutex의 lock/unlock 한 쌍이 shared_mutex의 lock_shared/unlock_shared보다 싸다.
- **쓰기가 빈번하다** (10~20% 이상): 쓰기 락은 모든 읽기를 막아야 하므로, 읽기 병렬화의 이득보다 쓰기 대기 비용이 커진다.
- **writer starvation 위험**: 표준은 `shared_mutex`의 writer 우선순위를 규정하지 않는다. 구현에 따라 읽기 스레드가 끊임없이 들어오면 쓰기 스레드가 계속 뒤로 밀릴 수 있다(특히 일부 libstdc++/Windows 구현에서 보고된 사례). 쓰기 지연이 SLA에 영향을 준다면 벤치마크로 직접 확인해야 한다.

결론적으로 **"읽기가 많으니 일단 shared_mutex로 바꾼다"는 직관만으로 결정하지 말고, 임계 구역의 크기와 실제 읽기/쓰기 비율을 프로파일링한 뒤 적용하라.** 02장에서 배운 Strategized Locking처럼, 락 타입 자체를 정책으로 분리해두면 나중에 `mutex` ↔ `shared_mutex`를 교체하며 벤치마크하기 쉽다.

## DCLP (Double-Checked Locking Pattern)

**DCLP**는 초기화 비용을 줄이려는 패턴이지만, 잘못하면 위험하다.

### 나쁜 예: Mutex 없는 DCLP

```cpp
class Singleton {
private:
    static Singleton* instance;
    Singleton() {}

public:
    static Singleton* getInstance() {
        if (instance == nullptr) {      // 첫 번째 확인
            instance = new Singleton(); // 초기화
        }
        return instance;
    }
};
Singleton* Singleton::instance = nullptr;
```

**문제**: 여러 스레드가 동시에 `if`를 통과해 `new Singleton()`을 여러 번 호출한다. 메모리 누수 + undefined behavior.

### DCLP with Mutex (초급, 부정확)

```cpp
static std::mutex mu;

static Singleton* getInstance() {
    if (instance == nullptr) {           // (1) 첫 번째 확인 (락 없음)
        std::lock_guard<std::mutex> lock(mu);
        if (instance == nullptr) {       // (2) 두 번째 확인 (락 있음)
            instance = new Singleton();
        }
    }
    return instance;
}
```

이 코드는 **C++98에서는 위험**하다. 왜냐하면:

1. (1)에서 읽은 `instance == nullptr`이 (2)에서 보장되지 않는다 (메모리 배리어 부족).
2. CPU가 생성자 코드를 메모리 쓰기 이후로 재정렬할 수 있다.

### 올바른 DCLP (C++11 이상)

```cpp
static std::atomic<Singleton*> instance(nullptr);
static std::mutex mu;

static Singleton* getInstance() {
    Singleton* ptr = instance.load(std::memory_order_acquire);
    if (ptr == nullptr) {
        std::lock_guard<std::mutex> lock(mu);
        ptr = instance.load(std::memory_order_acquire);
        if (ptr == nullptr) {
            ptr = new Singleton();
            instance.store(ptr, std::memory_order_release);
        }
    }
    return ptr;
}
```

**왜 이게 안전한가?**:
- `acquire` 로드와 `release` 저장이 happens-before을 만든다.
- 다른 스레드의 생성자 코드가 모두 완료될 때까지 대기한다.

### 안전성 검증: ThreadSanitizer로 DCLP 비교

"DCLP with Mutex (초급, 부정확)" 버전과 "올바른 DCLP" 버전을 각각 빌드해 TSAN으로 비교하면 차이가 드러난다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g dclp_broken.cpp -o dclp_broken
./dclp_broken
# WARNING: ThreadSanitizer: data race on instance (또는 heap-use-after-free 가능)

g++ -std=c++20 -pthread -fsanitize=thread -g dclp_fixed.cpp -o dclp_fixed
./dclp_fixed
# 경고 없음
```

부정확한 버전이 실제 환경(x86)에서는 "우연히" 잘 동작하는 경우가 많다는 점이 더 위험하다. x86은 store-store, load-load 순서를 비교적 강하게 보장하기 때문에 재정렬로 인한 문제가 드물게 발생한다. 하지만 ARM 기반 서버나 모바일 환경, 또는 컴파일러가 더 적극적으로 최적화하는 빌드 옵션(`-O3`, LTO)에서는 같은 코드가 실패할 수 있다. **TSAN 경고가 없다는 것은 "이번 실행에서 못 봤다"는 뜻이지 "안전하다"는 증명이 아니다** — 따라서 `memory_order`를 직접 다루는 코드는 표준이 보장하는 패턴(`call_once`, 정적 지연 초기화)으로 대체할 수 있는지부터 검토해야 한다.

하지만 **더 좋은 방법이 있다**.

## std::call_once와 std::once_flag

C++11부터 `call_once`로 초기화를 간단하고 안전하게 한다.

```cpp
class Singleton {
private:
    static std::once_flag initFlag;
    static Singleton* instance;
    
    Singleton() {}

public:
    static Singleton* getInstance() {
        std::call_once(initFlag, [] {
            instance = new Singleton();
        });
        return instance;
    }
};

std::once_flag Singleton::initFlag;
Singleton* Singleton::instance = nullptr;
```

**장점**:
1. DCLP의 모든 복잡성을 없앤다.
2. 예외 안전성 제공.
3. 표준이 보장하는 안전성.

```cpp
int main() {
    std::vector<std::thread> workers;
    for (int i = 0; i < 10; ++i) {
        workers.emplace_back([] {
            auto s = Singleton::getInstance();
            // ...
        });
    }
    for (auto& t : workers) t.join();
    return 0;
}
```

생성자는 정확히 한 번만 호출된다.

## Lazy Initialization 패턴 변형

### 1. Per-Object Initialization

```cpp
#include <atomic>
#include <mutex>

void* allocateResource();  // 실제 리소스를 할당하는 함수

class Resource {
private:
    std::atomic<void*> ptr{nullptr};  // 괄호 초기화(ptr(nullptr))는 멤버 선언에서 사용 불가, 중괄호 사용
    mutable std::mutex initMu;

public:
    void* get() {
        void* p = ptr.load(std::memory_order_acquire);
        if (p == nullptr) {
            std::lock_guard<std::mutex> lock(initMu);
            p = ptr.load(std::memory_order_acquire);
            if (p == nullptr) {
                p = allocateResource();
                ptr.store(p, std::memory_order_release);
            }
        }
        return p;
    }
};
```

### 2. Static Initialization (가장 간단)

```cpp
class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;  // C++11: 스레드 안전한 정적 초기화
        return instance;
    }
};
```

이것이 가장 간단하고 표준이 보장한다. (C++11 이후)

## 성능 비교

| 기법 | 첫 호출 | 이후 읽기 | 메모리 |
|------|--------|----------|--------|
| mutex | 느림 | 느림 | 적음 |
| DCLP (atomic) | 느림 | 빠름 | 적음 |
| call_once | 느림 | 빠름 | 적음 |
| static (C++11) | 느림 | 매우 빠름 | 적음 |

**권장**: 단순 싱글톤은 static 사용. 복잡한 초기화는 call_once.

## 학습 성과 평가 기준

- [ ] shared_mutex에서 shared_lock (읽기)과 unique_lock (쓰기)의 차이를 설명할 수 있는가?
- [ ] 왜 DCLP가 C++98에서 위험했고, C++11에서 atomic을 사용하면 안전한가?
- [ ] call_once와 once_flag를 사용해 스레드 안전한 싱글톤을 구현할 수 있는가?
- [ ] 읽기 위주 vs 쓰기 위주 시나리오에서 어떤 락을 선택해야 하는가?

## 다음 장에서는

06장 **「실행 관리 I: Thread Pool」**에서는 스레드 풀, 작업 큐, 그리고 work stealing 알고리즘을 다룬다.

## 참고 및 출처

- Scott Meyers & Andrei Alexandrescu, "C++ and the Perils of Double-Checked Locking" (2004)
- Anthony Williams, 『C++ Concurrency in Action』, Chapter 3 & 7
- C++ Standards Committee, Static storage duration initialization rules


