---
title: "[Concurrency Patterns] 07. 실행 관리 II: Future와 Promise"
description: "std::future, std::promise, std::async, std::packaged_task로 비동기 작업의 결과를 안전하게 전달합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 7
difficulty: intermediate-advanced
prerequisites:
  - "06장: Thread Pool"
  - "std::future, std::promise 기본 개념"
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Future
  - Promise
  - async
  - packaged_task
  - Asynchronous
  - 비동기
  - Result-Transfer
  - Exception-Handling
  - Synchronization
  - 동기화
  - Design-Pattern
  - 디자인패턴
  - Implementation
  - 구현
  - Tutorial
  - Guide
slug: cpp-future-promise-async-packaged-task
---

07장은 **비동기 작업의 결과를 안전하게 전달하는 패턴**을 다룬다. Future와 Promise는 Thread Pool과 다르게, "언젠가 완료될 작업의 결과"를 handle로 나타내고, 그 결과를 나중에 대기하며 받을 수 있다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "Promise와 Future" ~ "std::async" | 기본 사용법 습득 |
| **고급자** | 전체, "Thread Pool with Future" | Future를 Thread Pool과 조합 |
| **설계자** | "예외 처리" ~ "여러 Future 대기" | 복잡한 비동기 시나리오 관리 |

---

## Promise와 Future

**Promise**: 미래의 값을 설정하는 쪽
**Future**: 미래의 값을 받는 쪽

```cpp
#include <future>
#include <thread>

int main() {
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();

    std::thread worker([prom_move = std::move(prom)] () mutable {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        prom_move.set_value(42);  // 값 설정
    });

    std::cout << "Waiting for result...\n";
    int result = fut.get();  // 값이 설정될 때까지 대기
    std::cout << "Result: " << result << '\n';

    worker.join();
    return 0;
}
```

**특징**:
- Promise는 이동만 가능 (복사 불가).
- `set_value()` 호출 전에 `get()`을 호출하면 블로킹.
- 예외도 전달 가능: `set_exception()`.

## std::async

`std::async`는 Promise/Future를 직접 다루지 않고, 함수를 비동기로 실행하고 결과의 Future를 반환한다.

```cpp
#include <future>

int compute() {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    return 42;
}

int main() {
    std::future<int> fut = std::async(std::launch::async, compute);
    std::cout << "Task launched\n";
    int result = fut.get();
    std::cout << "Result: " << result << '\n';
    return 0;
}
```

**Launch Policy**:
- `std::launch::async`: 새 스레드에서 즉시 실행
- `std::launch::deferred`: 첫 `get()` 호출 시 현재 스레드에서 실행
- `std::launch::async | std::launch::deferred` (기본): 구현이 선택

## std::packaged_task

함수를 "패키징"해 나중에 실행 결과를 Future로 받는다. Thread Pool과 함께 사용할 때 유용하다.

```cpp
int add(int a, int b) {
    return a + b;
}

int main() {
    std::packaged_task<int(int, int)> task(add);
    std::future<int> fut = task.get_future();

    std::thread t(std::move(task), 5, 3);

    int result = fut.get();  // 40 + 5 = 45 아니라... 5 + 3 = 8
    std::cout << result << '\n';

    t.join();
    return 0;
}
```

## Thread Pool with Future

앞의 Thread Pool에 Future를 추가하면 결과를 받을 수 있다.

```cpp
class FutureThreadPool {
public:
    template<typename F>
    auto enqueue(F f) {
        using ReturnType = std::invoke_result_t<F>;
        auto task = std::make_shared<std::packaged_task<ReturnType()>>(f);
        std::future<ReturnType> fut = task->get_future();
        
        {
            std::lock_guard<std::mutex> lock(mu);
            tasks.push([task] { (*task)(); });
        }
        cv.notify_one();
        return fut;
    }

private:
    // ... (기본 Thread Pool과 동일)
};
```

**사용**:

```cpp
int main() {
    FutureThreadPool pool(4);

    auto fut1 = pool.enqueue([] { return 10; });
    auto fut2 = pool.enqueue([] { return 20; });

    int sum = fut1.get() + fut2.get();
    std::cout << "Sum: " << sum << '\n';
    return 0;
}
```

## 예외 처리

Promise와 Future는 예외도 전달할 수 있다.

```cpp
std::promise<int> prom;
std::future<int> fut = prom.get_future();

std::thread worker([prom = std::move(prom)] () mutable {
    try {
        throw std::runtime_error("Something went wrong");
    } catch (...) {
        prom.set_exception(std::current_exception());
    }
});

try {
    fut.get();  // 예외 재발생
} catch (const std::exception& e) {
    std::cout << "Caught: " << e.what() << '\n';
}

worker.join();
```

## 여러 Future 대기

```cpp
std::vector<std::future<int>> futures;
for (int i = 0; i < 5; ++i) {
    futures.push_back(pool.enqueue([i] { return i * i; }));
}

// 모든 결과 수집
int sum = 0;
for (auto& f : futures) {
    sum += f.get();
}
```

## 학습 성과 평가 기준

- [ ] Promise와 Future의 역할을 설명하고, 값을 설정/대기할 수 있는가?
- [ ] std::async의 launch policy (async vs deferred)를 이해하는가?
- [ ] packaged_task로 함수를 패키징하고 나중에 실행할 수 있는가?
- [ ] Thread Pool과 Future를 조합해 작업 결과를 안전하게 받을 수 있는가?
- [ ] 예외를 Promise를 통해 전달할 수 있는가?

## 다음 장에서는

08장 **「비동기 객체 (Active Object)」**에서는 Promise/Future와 Thread Pool을 조합해 "요청-응답 큐를 가진 객체"를 만든다.

## 참고 및 출처

- Anthony Williams, 『C++ Concurrency in Action』, Chapter 4 — Future와 Promise 상세
- C++ Standards Committee, `<future>` documentation
