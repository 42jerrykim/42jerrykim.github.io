---
image: wordcloud.png
title: "[Concurrency Patterns] 12. 코루틴 기반 비동기 재해석"
description: "C++20 코루틴으로 07장 Future/Promise와 08장 Active Object를 다시 구현합니다. co_await의 동작 원리, 스레드 재개 시 생기는 lost wakeup, 코루틴과 멀티스레딩의 관계를 다룹니다."
date: 2026-07-09
lastmod: 2026-07-09
draft: true
collection_order: 12
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - C++
  - C++20
  - Coroutine(코루틴)
  - Concurrency(동시성)
  - Async(비동기)
  - Thread
  - Synchronization
  - Condition-Variable
  - Memory-Order
  - RAII(Resource Acquisition Is Initialization)
  - Design-Pattern(디자인패턴)
  - Software-Architecture(소프트웨어아키텍처)
  - OOP(객체지향)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Best-Practices
  - Code-Quality(코드품질)
  - Compiler(컴파일러)
  - Performance(성능)
  - Reference(참고)
  - Deep-Dive
  - Technology(기술)
  - Future-Promise
  - Active-Object
  - co_await
  - Coroutine-Handle
  - Symmetric-Transfer
  - Lost-Wakeup
slug: cpp-coroutine-reinterpretation-future-active-object
---

07장의 Future/Promise와 08장의 Active Object는 모두 같은 보일러플레이트를 반복했다 — 완료 플래그, `mutex`, `condition_variable`, 결과 저장소를 손으로 조합해 "언젠가 끝나는 작업"을 표현했다. C++20 코루틴은 이 보일러플레이트의 상당 부분을 컴파일러가 대신 만들어 주는 문법이다. `co_await`로 멈추고 싶은 지점을 표시하면, 컴파일러가 함수를 "멈췄다가 나중에 이어서 실행할 수 있는 상태 머신"으로 변환해 준다. 이 장은 07~08장에서 손으로 만든 것과 정확히 같은 문제를, 코루틴이라는 다른 문법으로 다시 풀어 본다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [07장 「실행 관리 II: Future와 Promise」](/post/multithreading-patterns/cpp-future-promise-async-packaged-task/)와 [08장 「비동기 객체 (Active Object)」](/post/multithreading-patterns/cpp-active-object-async-method-invocation/)를 이미 읽었다고 가정합니다. 두 장이 `std::future`/`std::promise`와 스레드 하나짜리 작업 큐로 무엇을 해결했는지 알아야, 코루틴이 같은 문제를 어떻게 다르게 푸는지 비교할 수 있기 때문입니다. 03장의 Guarded Suspension(조건 변수로 기다리기)도 이 장 후반부의 lost wakeup 논의에 필요합니다.

**이 장의 깊이**: 이 장은 **심화(advanced)** 수준입니다. `std::coroutine_handle`과 `promise_type`을 직접 구현해 최소한의 코루틴 Task 타입을 만들고, 이를 이용해 Future/Promise와 Active Object를 재구현하는 것이 목표입니다.

**다루지 않는 것**: [00장](/post/multithreading-patterns/getting-started-multithreading-design-patterns/)에서 밝힌 대로, `std::execution`(senders/receivers, C++26)은 컴파일러 구현이 아직 없어 범위 밖입니다. 코루틴을 이용한 제너레이터(`co_yield` 기반 지연 시퀀스), 코루틴 기반 파서 같은 범용 활용도 다루지 않습니다 — 이 장은 오직 "이미 이 시리즈가 다룬 두 패턴을 코루틴으로 다시 쓰면 무엇이 달라지는가"에 집중합니다. 코루틴 프레임 할당 비용, 최적화 수준별 성능 비교 같은 정량 분석은 [Low-latency 동시성·멀티스레드 트랙](/post/concurrency-optimization/getting-started-concurrency-multithreading-performance-tuning/)의 영역입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "코루틴 핵심 개념" ~ "Future/Promise 재해석: 최소 Task 타입" | `co_await`/`promise_type`의 최소 어휘 습득 |
| **고급자** | 전체, 특히 "Active Object 재해석: 콜백으로 채우는 awaiter" | 코루틴과 스레드가 섞일 때 생기는 새로운 동시성 버그 이해 |
| **설계자** | "코루틴과 멀티스레딩의 관계" | 언제 코루틴이 유리하고, 언제 여전히 스레드 기반이 나은지 판단 |

---

## 코루틴 핵심 개념

**코루틴(coroutine)**은 실행을 중간에 멈췄다가(suspend) 나중에 그 지점부터 다시 실행할 수 있는(resume) 함수다. 일반 함수는 호출-실행-반환이 한 번에 끝나지만, 코루틴은 본문 안에 `co_await`, `co_yield`, `co_return` 중 하나라도 있으면 컴파일러가 그 함수를 "지금까지의 실행 상태를 힙에 저장한 객체(코루틴 프레임)"로 변환한다. `co_await`을 만나면 현재 지역 변수 상태를 프레임에 남긴 채 실행을 멈추고 호출자에게 제어를 돌려주며, 나중에 누군가 그 프레임에 대해 `resume()`을 호출하면 멈췄던 바로 그 지점부터 이어서 실행한다.

이 메커니즘을 실제로 쓰려면 세 가지 어휘가 필요하다. **`promise_type`**은 코루틴 하나의 상태(결과값, 예외, 그리고 "이 코루틴이 끝나면 누구를 깨울지")를 담는 객체로, 코루틴 함수마다 컴파일러가 자동으로 생성해 프레임 안에 넣는다. **`std::coroutine_handle`**은 이 프레임을 가리키는 포인터 같은 핸들로, `.resume()`을 호출하면 멈췄던 코루틴이 다시 실행된다. **awaiter**는 `await_ready`/`await_suspend`/`await_resume` 세 메서드를 가진 객체로, `co_await`이 정확히 무엇을 할지("이미 준비됐는가?", "멈춘다면 무엇을 해야 하는가?", "재개되면 무슨 값을 돌려주는가?")를 정의한다.

가장 중요한 오해부터 바로잡는다: **코루틴은 그 자체로 멀티스레딩이 아니다.** 코루틴은 "실행을 어디서 멈추고 이어갈지"를 다루는 단일 스레드 제어 흐름 도구다. `co_await`으로 멈춘 코루틴을 누가, 어느 스레드에서 재개(`resume()`)할지는 awaiter가 정하기 나름이며, 아무 awaiter도 없으면 코루틴은 처음 실행된 바로 그 스레드 안에서만 멈췄다 이어졌다 한다. 실제 병렬성(여러 CPU 코어가 동시에 일하는 것)은 여전히 `std::thread`가 만든다 — 코루틴은 "그 스레드로 어떻게 넘어가고 돌아올지"를 표현하는 문법일 뿐이다. 이 장의 두 예제 모두, 진짜 일은 `std::thread`가 하고 코루틴은 그 결과를 기다리는 방식을 표현하는 역할만 한다.

## Future/Promise 재해석: 최소 Task 타입

07장의 `std::future<T>`가 하던 일 — "언젠가 나올 값을 핸들로 표현하고, 다른 스레드에서 그 값을 채우면 기다리던 쪽이 받는다" — 을 코루틴으로 표현하려면, `co_await`으로 기다릴 수 있는 자체 타입이 필요하다. 아래 `Task<T>`는 이런 타입의 최소 구현이다. 코루틴 함수가 `Task<int>`를 반환 타입으로 선언하면, 컴파일러는 `Task<int>::promise_type`을 이용해 코루틴 프레임을 관리한다.

```cpp
// coro_future_promise.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 -g coro_future_promise.cpp -o coro_demo
// (GCC 10/11 일부 버전은 -std=c++20에 -fcoroutines 플래그가 추가로 필요할 수 있다)
#include <chrono>
#include <condition_variable>
#include <coroutine>
#include <functional>
#include <iostream>
#include <mutex>
#include <optional>
#include <thread>
#include <utility>

template <typename T>
class Task {
public:
    struct promise_type {
        std::optional<T> result;
        std::coroutine_handle<> continuation;   // 이 Task를 co_await한 코루틴
        std::function<void()> doneCallback;     // main처럼 코루틴이 아닌 코드가 기다릴 때 쓴다

        Task get_return_object() {
            return Task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }

        struct FinalAwaiter {
            bool await_ready() noexcept { return false; }
            std::coroutine_handle<> await_suspend(
                std::coroutine_handle<promise_type> h) noexcept {
                auto& p = h.promise();
                if (p.continuation) return p.continuation;  // 대칭 전이로 이어서 재개
                if (p.doneCallback) p.doneCallback();
                return std::noop_coroutine();
            }
            void await_resume() noexcept {}
        };
        FinalAwaiter final_suspend() noexcept { return {}; }
        void return_value(T value) { result = std::move(value); }
        void unhandled_exception() { std::terminate(); }  // 교육용: 예외 전파는 생략
    };

    explicit Task(std::coroutine_handle<promise_type> h) : handle_(h) {}
    Task(Task&& other) noexcept : handle_(std::exchange(other.handle_, {})) {}
    Task(const Task&) = delete;
    ~Task() { if (handle_) handle_.destroy(); }

    // 다른 코루틴에서 `co_await someTask()`로 기다릴 때 쓰는 3종 세트.
    bool await_ready() const noexcept { return false; }
    std::coroutine_handle<> await_suspend(std::coroutine_handle<> awaiting) noexcept {
        handle_.promise().continuation = awaiting;
        return handle_;  // 아직 시작 안 한 이 Task를 대칭 전이로 시작시킨다
    }
    T await_resume() { return std::move(*handle_.promise().result); }

    // main처럼 코루틴이 아닌 코드에서 이 Task를 끝까지 구동할 때 쓰는 진입점.
    void runAndNotify(std::function<void()> onDone) {
        handle_.promise().doneCallback = std::move(onDone);
        handle_.resume();
    }
    T& result() { return *handle_.promise().result; }

private:
    std::coroutine_handle<promise_type> handle_;
};
```

`promise_type::continuation`과 `doneCallback`은 "이 Task가 끝나면 누구를 깨울지"를 표현하는 두 가지 경로다. 다른 코루틴이 `co_await`으로 기다렸다면 `continuation`에 그 코루틴의 핸들이 들어 있고, `final_suspend`가 대칭 전이(symmetric transfer)로 그 핸들을 직접 재개한다. 아무도 `co_await`하지 않고 `runAndNotify`로 구동했다면 `doneCallback`이 대신 호출된다. 이 두 경로를 갈라 둔 이유는 `main` 같은 최상위 진입점은 코루틴이 아니라서 `co_await`을 쓸 수 없기 때문이다.

**왜 `continuation.resume()`을 직접 호출하지 않고 핸들을 반환할까?** `await_suspend`나 `final_suspend`의 `await_suspend`가 다른 코루틴 핸들을 직접 `.resume()`으로 호출하면, 그 재개된 코루틴이 다시 `co_return`하며 또 다른 코루틴을 재개하고, 그 코루틴이 또 재개하고… 하는 식으로 `co_await` 체인이 길어질수록 함수 호출이 계속 중첩된다 — 재귀 호출과 똑같이 스택 프레임이 계속 쌓이므로, 체인이 충분히 길면 스택 오버플로가 날 수 있다. 반면 `await_suspend`가 **핸들을 반환**하면(그리고 반환 타입이 `std::coroutine_handle<>`이면), 컴파일러는 이를 "재귀 호출"이 아니라 "제어를 다음 코루틴으로 그대로 넘겨라"는 뜻으로 해석해 현재 스택 프레임을 정리한 뒤 넘긴다 — 이것이 **대칭 전이(symmetric transfer)**이며, 체인이 아무리 길어도 스택 깊이가 늘지 않는다. `Task::await_suspend`(마지막 줄에서 `handle_`을 반환)와 `FinalAwaiter::await_suspend`(continuation을 반환) 둘 다 이 방식을 쓰는 이유가 여기에 있다.

이제 이 `Task<T>`가 실제로 다른 스레드로 넘어가게 만드는 awaiter가 필요하다. 아래 `RunOnThread`는 `co_await` 지점에서 백그라운드 스레드를 하나 띄우고, 그 스레드가 작업을 마치면 직접 코루틴을 재개한다 — 이것이 07장에서 `std::promise::set_value`가 하던 일을 코루틴 방식으로 표현한 것이다.

```cpp
// 코루틴을 백그라운드 스레드로 넘기는 awaiter.
struct RunOnThread {
    bool await_ready() const noexcept { return false; }
    void await_suspend(std::coroutine_handle<> handle) const {
        std::thread([handle] {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));  // 무거운 작업 흉내
            handle.resume();  // 워커 스레드가 코루틴을 재개한다
        }).detach();
    }
    void await_resume() const noexcept {}
};

Task<int> computeAsync(int x) {
    co_await RunOnThread{};   // 여기서부터는 백그라운드 스레드가 이어받는다
    co_return x * x;
}

template <typename T>
T syncWait(Task<T> task) {
    std::mutex m;
    std::condition_variable cv;
    bool done = false;

    task.runAndNotify([&] {
        std::lock_guard<std::mutex> lock(m);
        done = true;
        cv.notify_one();
    });

    std::unique_lock<std::mutex> lock(m);
    cv.wait(lock, [&] { return done; });
    return task.result();
}

int main() {
    int value = syncWait(computeAsync(7));
    std::cout << "7^2 = " << value << '\n';
    return 0;
}
```

`syncWait`의 `cv.wait`는 03장의 Guarded Suspension과 정확히 같은 구조다 — 조건(`done`)이 참이 될 때까지 기다린다. 다른 점은 기다리는 대상이 "다른 스레드가 채우는 값"이 아니라 "코루틴이 다시 스레드를 넘겨받아 끝났다는 신호"라는 것뿐이다. `computeAsync(7)`을 호출하는 시점에는 아무 코드도 실행되지 않는다 — `initial_suspend`가 `std::suspend_always`이므로, `runAndNotify`가 `handle_.resume()`을 호출하는 순간에야 비로소 함수 본문이 시작된다.

### 왜 discard가 위험한가: 원인과 수정

이 `Task<T>`를 쓸 때 흔히 저지르는 실수는 반환값을 버리는 것이다.

```cpp
void brokenFireAndForget() {
    computeAsync(7);  // 반환된 Task를 co_await도, 변수 저장도 하지 않는다
}
```

`computeAsync(7)`이 반환한 임시 `Task<int>`는 이 줄이 끝나는 즉시 소멸자가 호출되어 `handle_.destroy()`가 실행된다. 하지만 코루틴 본문은 아직 `co_await RunOnThread{}`를 통과하지 못했으므로(애초에 `runAndNotify`도, `co_await`도 호출된 적이 없어 코루틴은 `initial_suspend`에 멈춘 채 시작조차 하지 않았다) — 이 경우는 프레임이 시작 전 상태로 파괴되어 크래시로 이어지진 않지만, "코루틴을 만들어 놓고 실행은 결코 일어나지 않는" 조용한 논리 버그가 된다. 만약 `runAndNotify`로 이미 구동을 시작한 뒤 그 `Task` 객체를 백그라운드 스레드가 `resume()`을 호출하기 전에 다른 스레드가 파괴해 버리면, 이미 시작된 프레임에 대고 파괴 후 접근(use-after-free)이 발생한다. 실무 코루틴 라이브러리(cppcoro 등)가 `Task`에 `[[nodiscard]]`를 붙여 컴파일러가 discard를 경고하게 만드는 이유가 여기에 있다. 고친 버전은 다음 한 줄이다.

```cpp
template <typename T>
class [[nodiscard]] Task { /* 이하 동일 */ };
```

`[[nodiscard]]`는 런타임 동작을 바꾸지 않지만, `computeAsync(7);`처럼 반환값을 버리면 컴파일 경고를 발생시켜 이 실수를 컴파일 타임에 잡아 준다 — 03~04장에서 반복해서 강조한 "런타임에 가끔 터지는 버그보다, 컴파일 타임에 항상 잡히는 제약이 낫다"는 원칙이 코루틴에도 그대로 적용된다.

## Active Object 재해석: 콜백으로 채우는 awaiter

08장의 Active Object는 스레드 하나가 큐에서 작업을 꺼내 순서대로 처리했다. 이 구조 자체는 그대로 두고, 호출자가 결과를 받는 방식만 `std::future<T>` 대신 코루틴으로 바꿔 본다. 여기서는 `Task<T>`를 재사용할 수 없다 — 실제 계산이 코루틴 본문이 아니라 **워커 스레드의 람다** 안에서 일어나기 때문이다. 대신 워커 스레드가 외부에서 "값을 채워 넣는" 별도의 awaiter가 필요하다.

```cpp
// coro_active_object.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 -g coro_active_object.cpp -o coro_ao
#include <condition_variable>
#include <coroutine>
#include <functional>
#include <iostream>
#include <memory>
#include <mutex>
#include <optional>
#include <queue>
#include <thread>

template <typename T>
struct CoroFutureState {
    std::mutex mtx;
    std::optional<T> value;
    std::coroutine_handle<> continuation;
    bool ready = false;
};

template <typename T>
class CoroFuture {
public:
    explicit CoroFuture(std::shared_ptr<CoroFutureState<T>> state)
        : state_(std::move(state)) {}

    bool await_ready() const {
        std::lock_guard<std::mutex> lock(state_->mtx);
        return state_->ready;
    }

    // 락을 잡은 채로 ready를 다시 확인한다 — 이유는 본문 참고.
    bool await_suspend(std::coroutine_handle<> h) {
        std::lock_guard<std::mutex> lock(state_->mtx);
        if (state_->ready) return false;  // 그 사이 이미 끝났다면 즉시 재개
        state_->continuation = h;
        return true;
    }

    T await_resume() { return std::move(*state_->value); }

private:
    std::shared_ptr<CoroFutureState<T>> state_;
};

template <typename T>
void fulfill(std::shared_ptr<CoroFutureState<T>> state, T value) {
    std::coroutine_handle<> toResume;
    {
        std::lock_guard<std::mutex> lock(state->mtx);
        state->value = std::move(value);
        state->ready = true;
        toResume = state->continuation;
    }
    if (toResume) toResume.resume();
}

class ActiveCalculator {
public:
    ActiveCalculator() { worker = std::thread([this] { run(); }); }

    ~ActiveCalculator() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        cv.notify_one();
        worker.join();
    }

    // 04장 Producer-Consumer + 08장 Active Object와 동일한 큐 구조다.
    // 다른 점은 반환 타입이 std::future<int> 대신 CoroFuture<int>라는 것뿐이다.
    CoroFuture<int> square(int x) {
        auto state = std::make_shared<CoroFutureState<int>>();
        {
            std::lock_guard<std::mutex> lock(mu);
            queue.push([state, x] { fulfill(state, x * x); });
        }
        cv.notify_one();
        return CoroFuture<int>(state);
    }

private:
    void run() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !queue.empty() || shutdown; });
                if (shutdown && queue.empty()) return;
                task = std::move(queue.front());
                queue.pop();
            }
            task();  // 락 밖에서 실행 — 08장의 교훈: 락 들고 콜백 호출 금지
        }
    }

    std::mutex mu;
    std::condition_variable cv;
    std::queue<std::function<void()>> queue;
    bool shutdown = false;
    std::thread worker;  // 반드시 마지막에 선언 — 위 멤버들이 먼저 생성된 뒤 시작되어야 한다
};
```

`square(x)`를 호출하는 순간 작업은 이미 큐에 들어가고, 워커 스레드는 호출자의 코루틴이 `co_await`으로 기다리기 시작했는지와 무관하게 언제든 그 작업을 꺼내 처리할 수 있다. 이 "결과가 기다림보다 먼저 끝날 수도 있다"는 사실이 바로 07장에서 이미 본 문제이고, 여기서도 똑같이 대응해야 한다.

### 왜 lost wakeup이 발생하는가: 원인과 수정

`await_suspend`를 아래처럼 단순하게 작성하면 컴파일도 되고 대부분의 실행에서 잘 동작하는 것처럼 보인다.

```cpp
// 깨진 버전: ready를 다시 확인하지 않는다
bool await_suspend(std::coroutine_handle<> h) {
    std::lock_guard<std::mutex> lock(state_->mtx);
    state_->continuation = h;
    return true;  // 항상 멈춘다
}
```

문제는 타이밍이다. `await_ready()`가 `false`(아직 안 끝남)를 반환한 **직후**, `await_suspend()`가 락을 잡기 **전** 사이의 아주 짧은 틈에 워커 스레드가 `fulfill()`을 실행해 버릴 수 있다. 그 시점엔 `state_->continuation`이 아직 비어 있으므로 `fulfill()`은 "깨울 대상이 없다"고 판단하고 그냥 반환한다. 그 직후 `await_suspend()`가 뒤늦게 `continuation`을 채우고 코루틴을 멈추지만, 이제 그 코루틴을 깨워 줄 사람은 아무도 없다 — 03장에서 다룬 **lost wakeup**과 정확히 같은 구조의 버그이며, 여기서는 `condition_variable`의 spurious wakeup 대신 코루틴 재개가 영영 오지 않는 형태로 나타난다. 고친 버전은 `await_suspend` 안에서 락을 잡은 채로 `ready`를 한 번 더 확인한다(위 전체 코드에 이미 반영되어 있다). 그 사이 이미 끝났다면 `continuation`을 등록하지 않고 `false`를 반환해 즉시 재개하고, 아직이라면 안전하게 등록한다 — 03장의 Guarded Suspension이 조건을 "락을 잡은 채로" 확인했던 것과 같은 원리다.

### 안전성 검증

이 버그는 데이터 레이스가 아니라 **논리적인 lost wakeup**이다. `state_->continuation`과 `state_->ready`에 대한 모든 접근이 `mtx`로 보호되어 있으므로, ThreadSanitizer는 깨진 버전에서도 데이터 레이스를 보고하지 **않는다** — 메모리 접근 자체는 안전하기 때문이다. 즉 "TSAN이 조용하다"는 것이 "이 코드가 옳다"는 뜻이 아니라는 11장의 교훈이 여기서도 반복된다. 이 버그를 재현하려면 `fulfill` 호출과 `await_suspend` 호출 사이의 타이밍을 좁혀야 한다 — 예를 들어 `square()` 내부에서 큐에 넣기 직전 `std::this_thread::sleep_for`를 아주 짧게 넣어 워커 스레드가 먼저 실행되도록 강제한 뒤, 호출자 코루틴이 영원히 재개되지 않고 멈춰 있는지(프로그램이 종료되지 않는지) 관찰하는 방식이 실전에서 쓰인다. 고친 버전에서는 같은 실험을 반복해도 항상 정상 종료해야 한다.

## 코루틴과 멀티스레딩의 관계

지금까지의 두 예제를 나란히 놓고 보면 코루틴이 정확히 어디에 기여하는지가 분명해진다. 코루틴은 "결과를 어떻게 표현하고 어떻게 이어받을지"의 **문법**을 컴파일러가 생성한 상태 머신으로 대체했을 뿐, 실제로 다른 스레드에서 작업을 실행하고 그 완료를 안전하게 통지하는 책임은 여전히 `mutex`·`condition_variable`·`atomic` 같은 이 시리즈의 앞선 어휘가 진다. `RunOnThread`와 `CoroFuture`는 결국 07~08장에서 만든 것과 같은 종류의 동기화 구조를 awaiter 인터페이스 뒤로 옮겨 감춘 것이다.

이 재구성이 실질적으로 남기는 이득은 **호출부의 표현력**이다. `std::future<int> f = calc.square(7); int r = f.get();`와 `int r = co_await calc.square(7);`은 둘 다 "비동기 결과를 기다린다"는 뜻이지만, 코루틴 버전은 여러 비동기 호출을 마치 동기 코드처럼 순서대로 이어 쓸 수 있게 해 준다 — 중간에 콜백 지옥이나 명시적 `.then()` 체이닝 없이, `co_await` 세 글자로 "여기서 기다렸다가 다음 줄로" 넘어간다. 대신 그 대가로 이 장에서 본 것처럼 `promise_type`·awaiter·코루틴 프레임 수명이라는 새로운 복잡도를 감수해야 한다. Ivan Kostruba는 Active Object를 코루틴으로 재구현하는 사례를 다루며 이 표현력 이득을 "동기 코드처럼 읽히는 비동기"로 요약한다.

> "Coroutines... allow expressing asynchronous logic in a way that reads like synchronous code." — Ivan Kostruba, "Modern C++ Features and Proven Concepts: Active Object, External Polymorphism and Coroutines", DEV Community(2024)

이 트레이드오프 때문에 실무에서의 선택 기준은 명확하다. 호출 하나하나가 단순하고 콜백이 한두 단계로 끝난다면 07~08장의 스레드 기반 구현으로 충분하다 — `promise_type`을 직접 구현하는 비용이 그 이득보다 크다. 반면 여러 비동기 작업을 순차적으로 엮어야 하는 코드(예: "A를 기다린 뒤 그 결과로 B를 호출하고, 다시 그 결과로 C를 호출")가 반복된다면 코루틴이 가독성을 크게 개선한다. 다만 이 장의 `Task`/`CoroFuture`는 교육용 최소 구현이며, 프로덕션에서는 cppcoro나 각 프레임워크가 제공하는 검증된 코루틴 타입을 쓰는 것이 안전하다 — 이는 11장에서 "손으로 만든 lock-free 자료구조 대신 검증된 라이브러리를 쓰라"고 한 것과 같은 이유다.

같은 종류의 수명 문제는 언어 표준 차원에서도 여전히 논의 중이다. [00장](/post/multithreading-patterns/getting-started-multithreading-design-patterns/)에서 소개한 C++26 `std::execution`(P2300)은 `async_scope` 같은 구조로 "비동기 작업이 그 소유자보다 오래 살아남지 못하게" 강제하려 하는데, 이는 이 장에서 손으로 짚어 본 "Task를 discard하면 생기는 위험"을 언어·라이브러리 차원에서 막으려는 시도다.

## 흔한 오개념

가장 흔한 오해는 이미 앞서 짚었다 — **"코루틴을 쓰면 자동으로 병렬 처리가 된다"**는 것이다. 실제로는 `co_await`이 다른 awaiter를 통해 스레드를 넘기지 않는 한, 코루틴은 그저 같은 스레드 안에서 실행을 멈췄다 이어가는 것뿐이다. 두 번째 오해는 **"코루틴이 스레드보다 항상 가볍다"**는 것이다. 코루틴 프레임은 힙에 할당되는 것이 일반적이며(컴파일러가 최적화로 스택에 두는 경우도 있지만 보장되지 않는다), `promise_type`·awaiter 체인이 길어질수록 그 자체의 오버헤드가 쌓인다 — "가볍다"는 것은 스레드 생성·컨텍스트 스위치 비용과 비교했을 때의 상대적인 이야기이지, 공짜라는 뜻이 아니다.

## 학습 성과 평가 기준

- [ ] `promise_type`의 `initial_suspend`/`final_suspend`/`return_value`가 코루틴 생명주기의 어느 지점에 대응하는지 설명할 수 있는가?
- [ ] `Task<T>`를 구현하고, `co_await`으로 다른 코루틴에서 기다리는 경로와 `runAndNotify`로 `main`에서 구동하는 경로의 차이를 설명할 수 있는가?
- [ ] Active Object의 결과 전달을 `CoroFuture`로 재구현하고, `await_suspend`에서 `ready`를 다시 확인해야 하는 이유(lost wakeup)를 03장의 Guarded Suspension과 연결해 설명할 수 있는가?
- [ ] "코루틴은 멀티스레딩이 아니다"를 근거를 들어 설명하고, 진짜 병렬성이 어디서 만들어지는지 지적할 수 있는가?
- [ ] 언제 코루틴 기반 재구현이 스레드 기반 구현보다 나은지(호출 체이닝 vs 단순 호출) 판단 기준을 제시할 수 있는가?

## 다음 장에서는

13장에서는 11장이 "범위 밖"으로 미뤄 둔 문제 — lock-free 자료구조의 메모리 회수(reclamation) — 를 정면으로 다룬다. C++26 표준(2026년 3월 최종 확정)에 포함된 **Hazard Pointer**(P2530)와 **RCU**(P2545)의 알고리즘을 `std::atomic`만으로 직접 구현하고 검증한다.

## 참고 및 출처

- cppreference.com, "Coroutines (C++20)" — `promise_type`, awaiter, `std::coroutine_handle` 표준 문서
- Ivan Kostruba, "Modern C++ Features and Proven Concepts: Active Object, External Polymorphism and Coroutines", DEV Community(2024)
- Anthony Williams, 『C++ Concurrency in Action』(2nd ed., 2019) — Future/Promise와 스레드 기반 비동기의 원형
- POSA2(Schmidt et al., 2000) — Active Object 패턴의 원형
- Vito Gamberini, "Strong Structured Concurrency: How to Avoid Lifetime Footguns in std::execution"(2025-12) — 코루틴 프레임 수명 문제와 `std::execution`의 `async_scope`가 같은 문제를 다루는 방식
