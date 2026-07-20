---
image: wordcloud.png
title: "[Concurrency Patterns] 07. 실행 관리 II: Future와 Promise"
description: "std::future, std::promise, std::async, std::packaged_task로 비동기 작업의 결과와 예외를 안전하게 전달하는 법을 다룹니다. launch policy의 함정과 Thread Pool 결합 패턴도 포함합니다."
date: 2026-06-17
lastmod: 2026-07-09
draft: false
collection_order: 7
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Future
  - Promise
  - Async(비동기)
  - packaged_task
  - Asynchronous
  - Result-Transfer
  - Exception-Handling
  - Synchronization
  - Design-Pattern(디자인패턴)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - C++
  - Concurrency(동시성)
  - Thread
  - Mutex
  - Condition-Variable
  - Memory(메모리)
  - Performance(성능)
  - Best-Practices
  - Deep-Dive
  - Testing(테스트)
  - Debugging(디버깅)
  - Software-Architecture(소프트웨어아키텍처)
  - Reference(참고)
slug: cpp-future-promise-async-packaged-task
---

06장의 Thread Pool은 "작업을 어디서 실행할지"를 해결했지만, "그 작업의 결과를 어떻게 돌려받을지"는 답하지 않았다. 작업을 큐에 넣고 끝나면 그만인 fire-and-forget이 아니라, 계산 결과나 예외를 호출자가 안전하게 받아야 하는 경우가 훨씬 흔하다. 결과를 어디에 저장할 것인가? 아직 계산이 끝나지 않았다면 호출자는 어떻게 기다려야 하는가? 작업 중 예외가 발생하면 그 예외는 어느 스레드에서 다시 던져져야 하는가? 이 질문들에 락과 조건 변수를 직접 조합해 답하려면 매번 같은 보일러플레이트(완료 플래그, mutex, condition_variable, 결과/예외 저장소)를 작성해야 한다.

07장은 이 보일러플레이트를 표준 라이브러리가 어떻게 캡슐화했는지 다룬다. **Promise**와 **Future**는 "언젠가 완료될 작업의 결과"를 핸들로 나타내고, 그 결과(또는 예외)를 한 스레드에서 설정하고 다른 스레드에서 안전하게 대기·수신할 수 있게 한다. `std::async`와 `std::packaged_task`는 이 Promise/Future 메커니즘 위에 구축된 더 편리한 API다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 06장 「[실행 관리 I: Thread Pool](/post/multithreading-patterns/cpp-thread-pool-work-queue-work-stealing/)」에서 다룬 작업 큐(work queue)와 `std::mutex`/`std::condition_variable`의 기본 동작을 이미 안다고 가정합니다. 아직이라면 06장을 먼저 읽고 오세요. 또한 01장의 happens-before 개념(`std::future::get()`이 내부적으로 동기화 지점을 제공한다는 사실의 근거)을 가볍게 복습해 두면 좋습니다.

**이 장의 깊이**: 이 장은 **중급–고급** 수준입니다. `std::promise`/`std::future`의 기본 계약, `std::async`의 launch policy가 만드는 함정, 예외 전파의 정확한 의미, 그리고 `packaged_task`를 Thread Pool과 결합해 "Future를 반환하는 작업 큐"를 만드는 실전 패턴까지 다룹니다.

**다루지 않는 것**: `std::shared_future`를 이용한 다중 소비자 브로드캐스트, `std::experimental::future`의 `.then()` 체이닝, 그리고 `std::async`의 구현별(libstdc++ vs MSVC) 스케줄링 차이의 세부 사항은 다루지 않습니다. 이 장의 보일러플레이트를 C++20 코루틴으로 다시 쓰는 방법은 [12장 「코루틴 기반 비동기 재해석」](/post/multithreading-patterns/cpp-coroutine-reinterpretation-future-active-object/)에서 다룹니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "Promise와 Future" ~ "std::async" | 비동기 결과를 핸들로 받는다는 개념 이해 |
| **중급자** | "std::async" ~ "예외 처리와 전파 의미" | launch policy의 함정과 예외 전파 의미 이해 |
| **고급자** | "packaged_task" ~ "Thread Pool과 packaged_task 결합" | Future를 반환하는 작업 큐 구현 |
| **설계자** | "여러 Future 대기" ~ "안전성 검증" | 복잡한 비동기 시나리오와 검증 전략 |

---

## Promise와 Future

**Promise**: 미래의 값을 설정하는 쪽
**Future**: 미래의 값을 받는 쪽

```cpp
#include <chrono>
#include <future>
#include <iostream>
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
- **`set_value()`도 `set_exception()`도 호출하지 않은 채 Promise가 소멸되면**(예: 워커 스레드가 예외로 죽거나 함수를 일찍 `return`해 버리면), Future 쪽의 `get()`은 값 대신 `std::future_error`(`broken_promise`)를 던진다. "약속을 어긴 Promise"라는 이름 그대로, 이 실패 모드는 실무에서 워커 스레드의 예외 처리를 빠뜨렸을 때 흔히 마주친다.

## std::async

`std::async`는 Promise/Future를 직접 다루지 않고, 함수를 비동기로 실행하고 결과의 Future를 반환한다.

```cpp
#include <chrono>
#include <future>
#include <iostream>
#include <thread>

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

**Launch Policy의 세 가지 값**:

- `std::launch::async`: **새 스레드에서 즉시 실행**을 강제한다. 호출 즉시 별도 스레드가 생성되어 작업을 시작한다.
- `std::launch::deferred`: 실행을 **지연**한다. 새 스레드를 만들지 않고, 반환된 future에서 처음 `.get()` 또는 `.wait()`가 호출되는 시점에 **호출자의 스레드에서** 동기적으로 실행된다.
- `std::launch::async | std::launch::deferred` (인자를 생략한 기본값): 둘 중 어느 것을 쓸지는 **구현이 결정**한다. 표준은 어느 쪽을 선택해도 적합하다고만 규정한다.

### Launch Policy의 함정

기본 정책(`async | deferred`)을 그대로 쓰면 다음과 같은 함정에 빠지기 쉽다.

```cpp
#include <future>
#include <iostream>
#include <chrono>
#include <thread>

int slow_compute() {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return 42;
}

int main() {
    // 정책을 지정하지 않음 -> 구현이 deferred를 선택할 수 있다
    std::future<int> fut = std::async(slow_compute);

    std::cout << "다른 작업을 하는 중...\n";
    // fut가 deferred로 평가되면, 위 출력 이후 .get()에서
    // slow_compute()가 *현재 스레드*에서 2초간 블로킹 실행된다.
    // 즉, "백그라운드에서 병렬로 실행되고 있다"는 가정이 깨질 수 있다.
    int result = fut.get();
    std::cout << "결과: " << result << '\n';
    return 0;
}
```

이 코드의 문제는 **컴파일도 되고 결과도 맞지만**, "백그라운드에서 미리 계산되고 있을 것"이라는 가정이 환경에 따라 거짓이 될 수 있다는 점이다. libstdc++/MSVC 모두 기본 정책에서 `async`를 선호하는 경향이 있지만, 표준이 보장하지 않으므로 다음 두 가지를 지켜야 한다.

1. **진짜 병렬 실행이 필요하면 `std::launch::async`를 명시한다.**
2. **`std::async`로 만든 future의 소멸자는, 그 future가 `std::launch::async`로 시작된 작업에 연결되어 있고 아직 완료되지 않았다면, 작업이 끝날 때까지 블로킹한다.** 즉 `std::async(std::launch::async, f);`처럼 반환값을 버리면, 그 임시 future의 소멸자에서 암묵적으로 `join`과 같은 대기가 발생한다 — 의도하지 않은 동기화 지점이 생기는 흔한 실수다.

```cpp
// 함정: 반환값을 버리면 다음 줄에서 암묵적으로 블로킹된다
std::async(std::launch::async, slow_compute);  // (1) 여기서 작업 시작
std::cout << "즉시 출력될 것 같지만...\n";       // (2) 실제로는 (1)의 임시 future
                                                 //     소멸자가 끝날 때까지 대기한 후 실행
```

## std::packaged_task

`std::packaged_task`는 호출 가능한 객체(함수, 람다 등)를 "패키징"해, 그 호출 결과를 `std::future`로 받을 수 있게 감싸는 래퍼다. `std::async`와 달리 **언제, 어느 스레드에서 실행할지를 호출자가 직접 제어**할 수 있어 Thread Pool과 결합하기 좋다.

```cpp
#include <future>
#include <thread>
#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    std::packaged_task<int(int, int)> task(add);
    std::future<int> fut = task.get_future();

    // packaged_task는 이동만 가능 (복사 불가)하므로 std::move로 스레드에 전달
    std::thread t(std::move(task), 5, 3);

    int result = fut.get();  // add(5, 3) == 8
    std::cout << "result: " << result << '\n';

    t.join();
    return 0;
}
```

**특징 정리**:

- `std::promise`처럼 이동만 가능, 복사 불가.
- `get_future()`는 단 한 번만 호출할 수 있다.
- 패키징된 함수가 던진 예외는 자동으로 `set_exception()`을 거쳐 future에 저장된다 (직접 try/catch로 잡아 `set_exception`을 호출할 필요가 없다).

## 예외 처리와 전파 의미

Promise/Future, `std::async`, `packaged_task`는 모두 **예외도 값처럼 전달**한다. 작업 도중 던져진 예외는 `prom.set_exception(std::current_exception())`을 통해 future의 공유 상태(shared state)에 저장되고, **`future::get()`을 호출하는 시점에 호출자의 스레드에서 다시 던져진다(rethrow)**. 이 의미를 정확히 이해하는 것이 중요하다.

```cpp
#include <future>
#include <iostream>
#include <stdexcept>
#include <thread>

int main() {
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();

    std::thread worker([prom = std::move(prom)]() mutable {
        try {
            throw std::runtime_error("작업 중 오류 발생");
        } catch (...) {
            // 예외를 잡아 future의 공유 상태에 저장한다.
            // 이 시점에 예외가 "던져지는" 것이 아니라 "보관"된다.
            prom.set_exception(std::current_exception());
        }
    });

    try {
        fut.get();  // 보관된 예외가 *이 스레드*에서 재발생(rethrow)한다.
    } catch (const std::exception& e) {
        std::cout << "Caught in main: " << e.what() << '\n';
    }

    worker.join();
    return 0;
}
```

핵심 의미는 세 가지다.

1. **예외는 스레드 경계를 넘어 전달된다.** worker 스레드에서 발생한 예외가 main 스레드의 `catch` 블록에서 잡힌다 — 일반적인 C++ 예외는 스레드를 넘지 못하지만, future는 이를 안전하게 직렬화/재던지기로 우회한다.
2. **`get()`은 한 번만 결과(또는 예외)를 반환한다.** 두 번째 `get()` 호출은 `std::future_error`를 던진다.
3. **`packaged_task`와 `std::async`도 동일한 메커니즘을 쓴다.** 패키징된 함수 내부의 예외는 자동으로 `set_exception`되므로, 다음처럼 `std::async`가 호출한 함수가 던진 예외도 `get()`에서 그대로 재발생한다.

```cpp
std::future<int> fut = std::async(std::launch::async, [] {
    throw std::logic_error("async 작업 실패");
    return 0;
});

try {
    fut.get();
} catch (const std::logic_error& e) {
    std::cout << "Caught: " << e.what() << '\n';  // "async 작업 실패"
}
```

## Thread Pool과 packaged_task 결합

06장의 Thread Pool은 `void()` 형태의 작업만 큐에 넣고 결과를 돌려주지 않았다. `packaged_task`로 작업을 감싸면, **임의의 반환형을 갖는 호출 가능 객체를 큐에 넣고 `std::future`로 결과를 받는 작업 큐**를 만들 수 있다. 이것이 다음 08장의 Active Object에서 핵심 빌딩 블록이 된다.

```cpp
#include <future>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <functional>
#include <vector>
#include <type_traits>

class FutureThreadPool {
public:
    explicit FutureThreadPool(size_t numThreads) {
        for (size_t i = 0; i < numThreads; ++i) {
            workers.emplace_back([this] { workerLoop(); });
        }
    }

    ~FutureThreadPool() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        cv.notify_all();
        for (auto& t : workers) t.join();
    }

    // F의 반환형을 그대로 future<ReturnType>으로 돌려준다.
    template<typename F>
    auto enqueue(F f) -> std::future<std::invoke_result_t<F>> {
        using ReturnType = std::invoke_result_t<F>;

        // packaged_task는 이동 전용이라, 람다 캡처로 큐에 넣으려면
        // shared_ptr로 감싸 std::function<void()>에 담는다.
        auto task = std::make_shared<std::packaged_task<ReturnType()>>(std::move(f));
        std::future<ReturnType> fut = task->get_future();

        {
            std::lock_guard<std::mutex> lock(mu);
            if (shutdown) throw std::runtime_error("enqueue on stopped pool");
            tasks.push([task] { (*task)(); });
        }
        cv.notify_one();
        return fut;
    }

private:
    void workerLoop() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !tasks.empty() || shutdown; });
                if (tasks.empty() && shutdown) return;
                task = std::move(tasks.front());
                tasks.pop();
            }
            task();  // packaged_task 호출 -> future에 결과/예외 저장
        }
    }

    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mu;
    std::condition_variable cv;
    bool shutdown = false;
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

`enqueue`가 던지는 작업이 예외를 일으켜도, `packaged_task`가 자동으로 `set_exception`하므로 `fut.get()`에서 그대로 재발생한다 — 위 "예외 처리와 전파 의미" 절의 의미가 Thread Pool 경계를 넘어서도 그대로 유지된다.

## 여러 Future 대기

여러 작업을 동시에 제출하고 모든 결과를 모으는 패턴은 매우 흔하다.

```cpp
std::vector<std::future<int>> futures;
for (int i = 0; i < 5; ++i) {
    futures.push_back(pool.enqueue([i] { return i * i; }));
}

// 모든 결과 수집 (제출 순서대로 완료를 기다림)
int sum = 0;
for (auto& f : futures) {
    sum += f.get();  // 어느 future가 먼저 끝났는지와 무관하게 순서대로 대기
}
std::cout << "Sum of squares: " << sum << '\n';  // 0+1+4+9+16 = 30
```

이 패턴은 "모든 작업이 끝나야 다음으로 진행"(fork-join)에 적합하다. 작업 중 하나라도 예외를 던지면, 해당 `f.get()`에서 예외가 재발생하므로 나머지 future들은 여전히 백그라운드에서 실행 중일 수 있다는 점에 주의한다 — 필요하면 모든 future를 먼저 `wait()`한 뒤 예외를 처리하는 식으로 순서를 바꿔야 한다.

## 안전성 검증: ThreadSanitizer

Future/Promise 기반 코드에서 가장 흔한 실수는 **`packaged_task`나 `promise`가 캡처한 `this`가 객체보다 먼저 소멸되는 경우**다. 예를 들어 위 `FutureThreadPool::enqueue`에서 `task` 람다가 `this`(풀 자체)를 캡처하지 않도록 주의해야 풀이 소멸된 뒤에도 안전하다. 의심스러운 코드는 다음과 같이 TSAN으로 점검한다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g future_pool_example.cpp -o future_pool_example
./future_pool_example
```

TSAN은 `set_value`/`set_exception`과 `get()` 사이의 happens-before 관계가 깨졌을 때(예: 공유 상태에 직접 접근하는 잘못된 수동 구현) 데이터 레이스를 보고한다. 표준 `std::future`/`std::promise` 자체는 내부적으로 적절한 동기화를 제공하므로, 이 장의 예제처럼 표준 API만 사용하면 TSAN 경고가 발생하지 않는 것이 정상이다 — 경고가 뜬다면 future로 전달해야 할 데이터를 future 밖의 동기화되지 않은 공유 변수로 우회 접근하고 있다는 신호다.

## 학습 성과 평가 기준

- [ ] Promise와 Future의 역할을 설명하고, 값을 설정/대기할 수 있는가?
- [ ] `std::async`의 launch policy(`async` vs `deferred` vs 기본값)와 그 차이가 만드는 함정을 설명할 수 있는가?
- [ ] `future::get()`이 예외를 재발생시키는 정확한 시점과 의미를 설명할 수 있는가?
- [ ] `packaged_task`로 함수를 패키징하고, Thread Pool과 결합해 임의 반환형의 결과를 `future`로 받을 수 있는가?
- [ ] 여러 future를 fork-join 방식으로 대기할 때의 예외 처리 순서를 이해하는가?

## 다음 장에서는

08장 <strong>「비동기 객체 (Active Object)」</strong>에서는 Promise/Future와 Thread Pool을 조합해 "요청-응답 큐를 가진 객체"를 만든다.

## 참고 및 출처

- Anthony Williams, 『C++ Concurrency in Action』, Chapter 4 — Future와 Promise 상세
- C++ Standards Committee, `<future>` documentation


