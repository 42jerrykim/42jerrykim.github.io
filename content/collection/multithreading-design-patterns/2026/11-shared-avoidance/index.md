---
title: "[Concurrency Patterns] 11. 공유 회피"
description: "공유 상태를 애초에 없애는 전략: Immutable 패턴, Copy-on-Write, thread_local, 그리고 lock-free 자료구조의 전망을 다룹니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
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
  - Concurrency
  - 동시성
  - Design-Pattern
  - 디자인패턴
  - Performance
  - 성능
  - Safety
  - 안전
  - Functional-Programming
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-avoiding-shared-state-immutable-cow-thread-local
---

이 시리즈의 마지막 장은 **공유 상태 자체를 없애는 전략**을 다룬다. 지금까지 "공유 상태를 보호하는 방법"을 배웠다면, 11장은 "공유하지 않는 방법"을 배운다. 이것이 가장 근본적인 해결책이다.

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

Immutable의 단점을 보완한다. **읽기는 공유, 쓰기는 복사**.

```cpp
template<typename T>
class CopyOnWritePtr {
private:
    mutable std::shared_ptr<T> ptr;
    mutable std::shared_mutex mu;

public:
    CopyOnWritePtr(T* p) : ptr(p) {}

    // 읽기: 공유
    std::shared_ptr<const T> read() const {
        std::shared_lock<std::shared_mutex> lock(mu);
        return ptr;  // 공유 포인터, 복사 비용 없음
    }

    // 쓰기: 복사
    std::shared_ptr<T> write() {
        std::unique_lock<std::shared_mutex> lock(mu);
        if (ptr.use_count() > 1) {
            ptr = std::make_shared<T>(*ptr);  // 복사
        }
        return ptr;
    }
};
```

**사용**:

```cpp
CopyOnWritePtr<std::string> cowStr(new std::string("hello"));

// 읽기는 많은 스레드에서 병렬
for (int i = 0; i < 100; ++i) {
    auto readable = cowStr.read();
    std::cout << *readable << '\n';
}

// 쓰기는 복사 후 독점
auto writable = cowStr.write();
*writable = "world";
```

**어디에 유용한가?:
- 읽기가 대부분인 경우 (예: 설정 객체)
- 드물게 수정되는 경우

## thread_local 패턴

**각 스레드가 자신만의 복사본을 가진다.** 공유 자체가 없으므로 동기화 불필요.

```cpp
class ThreadLocalCounter {
private:
    static thread_local int count;

public:
    static void increment() {
        ++count;  // 각 스레드만의 count
    }

    static int get() {
        return count;
    }

    static void reset() {
        count = 0;
    }
};

thread_local int ThreadLocalCounter::count = 0;
```

**사용**:

```cpp
int main() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([] {
            for (int j = 0; j < 1000; ++j) {
                ThreadLocalCounter::increment();
            }
            std::cout << "Thread " << std::this_thread::get_id()
                      << " count: " << ThreadLocalCounter::get() << '\n';
        });
    }

    for (auto& t : threads) t.join();
    return 0;
}
```

**출력**: 각 스레드가 정확히 1000을 출력 (동기화 불필요).

**사용처**:
- 스레드별 통계 (로깅 버퍼, 성능 카운터)
- 스레드별 상태 (random seed, 예외 정보)
- 스레드풀의 워커별 캐시

**주의점**:
- 메모리: 스레드 수 × 데이터 크기
- 초기화: 모든 스레드에서 별도로 초기화 필요

## Lock-Free 자료구조: 전망

**Lock-Free**: mutex를 사용하지 않고 atomic으로만 구현. 극도로 높은 성능, 극도로 높은 복잡도.

```cpp
// Lock-Free 스택의 개념 (의사 코드)
template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        std::atomic<Node*> next;
    };
    std::atomic<Node*> head;

public:
    void push(const T& val) {
        Node* newNode = new Node{val, nullptr};
        Node* oldHead = head.load(std::memory_order_relaxed);
        do {
            newNode->next.store(oldHead, std::memory_order_relaxed);
        } while (!head.compare_exchange_weak(
            oldHead, newNode,
            std::memory_order_release,
            std::memory_order_relaxed
        ));
    }

    bool pop(T& val) {
        Node* oldHead = head.load(std::memory_order_acquire);
        while (oldHead) {
            Node* newHead = oldHead->next.load(std::memory_order_relaxed);
            if (head.compare_exchange_weak(
                oldHead, newHead,
                std::memory_order_release,
                std::memory_order_relaxed
            )) {
                val = oldHead->data;
                delete oldHead;
                return true;
            }
        }
        return false;
    }
};
```

**현실**:
- 이 패턴은 **책으로는 배우기 어렵고**, 보증된 라이브러리 (Boost, TBB, folly)를 사용할 것을 강력히 권장한다.
- 정확성 검증이 매우 어렵다 (10년 경력 해서도 버그 있음).
- 성능 이득이 실제로 필요한 경우는 드물다 (보통 mutex가 충분).

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
- [ ] Copy-on-Write의 "읽기 공유, 쓰기 복사" 원리를 이해하는가?
- [ ] thread_local을 언제 쓸지, 메모리 비용은 어떻게 되는지 판단할 수 있는가?
- [ ] Lock-Free가 왜 어렵고 위험한지 이해하는가?

## 시리즈 완수 평가 기준

이 컬렉션 전체를 완주하면 다음을 할 수 있어야 한다.

- [ ] 멀티스레드 문제를 "메모리 모델" 언어로 진단할 수 있다.
- [ ] 데이터 레이스를 Scoped Locking, Monitor Object, Guarded Suspension으로 해결할 수 있다.
- [ ] Producer-Consumer를 Bounded Buffer로 구현하고 backpressure를 제어할 수 있다.
- [ ] 읽기 위주 워크로드를 shared_mutex나 call_once로 최적화할 수 있다.
- [ ] Thread Pool, Future/Promise, Active Object를 설계하고 구현할 수 있다.
- [ ] Reactor 또는 Proactor를 선택해 이벤트 기반 아키텍처를 설계할 수 있다.
- [ ] Immutable, Copy-on-Write, thread_local로 공유를 회피할 수 있다.
- [ ] 각 패턴의 트레이드오프(메모리, 성능, 복잡도)를 이해하고 판단할 수 있다.

## 마치며

이 시리즈는 01장의 메모리 모델부터 시작해, 단일 객체 보호 → 스레드 간 협력 → 대규모 시스템 아키텍처까지 올라간다. 마지막 11장은 "보호와 협력의 필요성 자체를 없애는 방법"으로 원점으로 돌아온다.

실무에서:
- **작은 시스템**: Scoped Locking + Monitor Object로 충분
- **중간 시스템**: Thread Pool + Future, Half-Sync/Half-Async 조합
- **대규모 시스템**: Event-Driven (Reactor) + thread_local + Immutable 혼합

무엇보다 중요한 것은 **"왜 동기화가 필요한가"를 이해하고, 가장 간단한 패턴부터 시작**하는 것이다. 복잡한 패턴은 필요할 때만 사용한다.

## 참고 및 출처

- Brian Goetz, 『Java Concurrency in Practice』, Chapter 5 — Immutable & Thread-Safe
- POSA2 (Schmidt et al.), 전체 — 모든 패턴의 원형
- C++ Standards Committee, 전체 — std::thread, mutex, atomic, future documentation
