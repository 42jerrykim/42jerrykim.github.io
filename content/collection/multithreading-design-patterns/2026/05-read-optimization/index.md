---
title: "[Concurrency Patterns] 05. 읽기 최적화와 지연 초기화"
description: "shared_mutex로 읽기/쓰기 락 분리, DCLP의 함정과 해결, call_once를 통한 안전한 지연 초기화를 학습합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 5
difficulty: intermediate-advanced
prerequisites:
  - "01~04장: 메모리 모델, 락, condition_variable"
  - "std::shared_mutex와 atomic 이해"
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
  - 동기화
  - Design-Pattern
  - 디자인패턴
  - Performance
  - 성능
  - Optimization
  - 최적화
  - Memory-Order
  - Volatile
  - Singleton
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-read-write-lock-dclp-call-once-lazy-init
---

05장은 **읽기 작업이 대부분인 시나리오**의 최적화를 다룬다. 많은 시스템에서 쓰기(변경)는 드물고 읽기는 대부분이다. 기존의 단일 mutex는 읽기들까지 직렬화하므로 비효율적이다. 이 장에서는 읽기와 쓰기를 분리하고, 초기화 비용을 한 번만 치르는 패턴을 배운다.

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
- `shared_lock`: 여러 스레드가 동시에 보유 가능 (읽기)
- `unique_lock`: 한 스레드만 보유 (쓰기)

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
class Resource {
private:
    std::atomic<void*> ptr(nullptr);
    mutable std::mutex initMu;

public:
    void* get() {
        void* p = ptr.load(std::memory_order_acquire);
        if (p == nullptr) {
            std::lock_guard lock(initMu);
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
