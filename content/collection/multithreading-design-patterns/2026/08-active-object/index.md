---
title: "[Concurrency Patterns] 08. 비동기 객체 (Active Object)"
description: "스스로 스레드를 가지고 메서드 호출을 큐로 받는 Active Object 패턴을 구현합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 8
difficulty: advanced
prerequisites:
  - "06~07장: Thread Pool과 Future/Promise"
  - "메서드 호출의 직렬화 개념"
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Active-Object
  - Asynchronous-Method-Invocation
  - Actor-Model
  - Message-Queue
  - Thread-Per-Object
  - Design-Pattern
  - 디자인패턴
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-active-object-async-method-invocation
---

08장은 **각 객체가 자신만의 스레드를 가지고, 메서드 호출을 큐로 받아 처리**하는 Active Object 패턴을 다룬다. 이는 Producer-Consumer, Thread Pool, Future/Promise를 종합하는 패턴이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **고급자** | "기본 구현" | Active Object 구현 및 사용 |
| **설계자** | 전체, 특히 "고급" 섹션 | Actor 모델과의 비교, 성능 분석 |

---

## 동기 객체 vs Active 객체

**동기(Passive) 객체**: 호출자의 스레드에서 메서드를 직접 실행.

```cpp
class PassiveCounter {
private:
    int value = 0;
public:
    void increment() { ++value; }
    int getValue() { return value; }
};
```

**Active 객체**: 자신의 스레드에서 메서드를 실행. 호출자는 Future를 얻고 나중에 결과를 받음.

```cpp
class ActiveCounter {
public:
    std::future<void> increment() { /* 비동기 큐에 작업 추가 */ }
    std::future<int> getValue() { /* 비동기 결과 반환 */ }
};
```

## 기본 구현

```cpp
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <future>

class ActiveCounter {
public:
    std::future<void> increment() {
        auto task = std::make_shared<std::packaged_task<void()>>(
            [this] { ++value; }
        );
        auto fut = task->get_future();
        
        {
            std::lock_guard<std::mutex> lock(mu);
            queue.push([task] { (*task)(); });
        }
        cv.notify_one();
        return fut;
    }

    std::future<int> getValue() {
        auto task = std::make_shared<std::packaged_task<int()>>(
            [this] { return value; }
        );
        auto fut = task->get_future();
        
        {
            std::lock_guard<std::mutex> lock(mu);
            queue.push([task] { (*task)(); });
        }
        cv.notify_one();
        return fut;
    }

private:
    int value = 0;
    mutable std::mutex mu;
    std::condition_variable cv;
    std::queue<std::function<void()>> queue;
    bool shutdown = false;

    void run() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !queue.empty() || shutdown; });
                if (shutdown && queue.empty()) break;
                if (queue.empty()) continue;
                task = std::move(queue.front());
                queue.pop();
            }
            task();
        }
    }

public:
    ActiveCounter() {
        thread = std::thread([this] { run(); });
    }

    ~ActiveCounter() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        cv.notify_one();
        thread.join();
    }

private:
    std::thread thread;
};
```

**사용**:

```cpp
int main() {
    ActiveCounter ac;

    for (int i = 0; i < 5; ++i) {
        ac.increment().wait();  // 블로킹: 각 증가 대기
    }

    int final = ac.getValue().get();
    std::cout << "Final value: " << final << '\n';
    return 0;
}
```

## 고급: 메서드 타입 안전성

위의 코드는 런타임에 메서드를 큐에 추가할 때 동작하지만, 컴파일 시 타입 체크가 약하다. **Template 기반 접근**:

```cpp
template<typename T>
class ActiveObject {
private:
    T impl;
    std::queue<std::function<void()>> queue;
    std::mutex mu;
    std::condition_variable cv;
    bool shutdown = false;

    void run() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !queue.empty() || shutdown; });
                if (shutdown && queue.empty()) break;
                if (queue.empty()) continue;
                task = std::move(queue.front());
                queue.pop();
            }
            task();
        }
    }

public:
    template<typename F>
    auto call(F method) {
        using ReturnType = std::invoke_result_t<F, T&>;
        auto task = std::make_shared<std::packaged_task<ReturnType()>>(
            [this, method] { return method(impl); }
        );
        auto fut = task->get_future();
        
        {
            std::lock_guard<std::mutex> lock(mu);
            queue.push([task] { (*task)(); });
        }
        cv.notify_one();
        return fut;
    }
};

// 사용
struct Counter {
    int value = 0;
    void inc() { ++value; }
    int get() { return value; }
};

int main() {
    ActiveObject<Counter> ac;
    ac.call([](Counter& c) { c.inc(); }).wait();
    int val = ac.call([](Counter& c) { return c.get(); }).get();
    std::cout << val << '\n';
    return 0;
}
```

## Actor 모델과의 차이

Active Object와 Actor 모델은 유사하지만:

- **Active Object**: 메서드 기반. 일반 C++ 객체를 활성화.
- **Actor**: 메시지 기반. 상태 변경을 메시지로만 받음.

이 장에서는 Active Object만 다룬다. Actor는 별도 라이브러리 (예: Akka, CAF)에서 사용된다.

## 성능 고려사항

- **Context Switching**: 각 객체마다 스레드 생성 비용.
- **메모리**: 스레드당 수 MB (보통 2-8 MB).
- **사용 시점**: 객체 수가 적고 (수십 개), 각자 독립적인 작업을 할 때만.

100개 이상의 Active Object가 필요하면, 대신 Thread Pool + Future를 권장.

## 학습 성과 평가 기준

- [ ] Active Object가 Passive Object와 어떻게 다른가?
- [ ] Active Object를 구현하고, Future로 결과를 받을 수 있는가?
- [ ] 메서드 호출이 큐를 통해 직렬화되는 방식을 이해하는가?
- [ ] 언제 Active Object를 쓸지, 언제 Thread Pool을 쓸지 판단할 수 있는가?

## 다음 장에서는

09장 **「이벤트 아키텍처 I: Reactor」**에서는 네트워크 이벤트를 한 스레드에서 처리하는 Reactor 패턴을 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 6 — Active Object 원형
- Douglas C. Schmidt, "An Object Behavioral Pattern for Concurrent Processing"
