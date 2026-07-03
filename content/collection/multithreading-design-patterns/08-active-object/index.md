---
image: wordcloud.png
title: "[Concurrency Patterns] 08. 비동기 객체 (Active Object)"
description: "스스로 스레드를 가지고 메서드 호출을 큐로 받는 Active Object 패턴을 구현합니다."
date: 2026-06-18
lastmod: 2026-06-19
draft: false
collection_order: 8
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Active-Object
  - Asynchronous-Method-Invocation
  - Actor-Model
  - Message-Queue
  - Thread-Per-Object
  - Design-Pattern(디자인패턴)
  - Implementation(구현)
  - Tutorial(튜토리얼)
  - Guide(가이드)
slug: cpp-active-object-async-method-invocation
---

멀티스레드 환경에서 객체 하나를 안전하게 만드는 가장 쉬운 방법은 모든 public 메서드에 `lock_guard`를 씌우는 것이다(02장의 Thread-Safe Interface). 하지만 이 접근은 호출자의 스레드에서 메서드 본문을 **동기적으로** 실행하므로, 메서드가 오래 걸리면 호출자가 그만큼 블로킹된다. 또한 락이 보호하는 메서드끼리 서로를 호출하면 재진입 데드락 위험이 생긴다. 만약 "이 객체에 대한 모든 호출을 큐에 쌓아두고, 객체 자신의 전용 스레드가 하나씩 순서대로 처리"한다면 어떨까? 호출자는 즉시 제어권을 돌려받고(필요하면 future로 결과를 나중에 받음), 객체 내부 상태는 단일 스레드에서만 접근되므로 락 없이도 데이터 레이스가 사라진다.

08장은 이 아이디어를 구현하는 **Active Object** 패턴을 다룬다. 04장의 Producer-Consumer 큐, 06장의 Thread Pool, 07장의 Future/Promise — 이 세 가지를 한 클래스 안에 종합한 패턴이 Active Object다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 04장의 작업 큐(생산자-소비자), 06장 「[실행 관리 I: Thread Pool](/post/multithreading-design-patterns/cpp-thread-pool-work-queue-work-stealing/)」의 워커 스레드 구조, 그리고 07장 「[실행 관리 II: Future와 Promise](/post/multithreading-design-patterns/cpp-future-promise-async-packaged-task/)」의 `std::packaged_task`/`std::future` 조합을 이미 알고 있다고 가정합니다. 특히 07장의 "Thread Pool과 packaged_task 결합" 절은 이 장의 기본 구현과 거의 동일한 패턴을 사용하므로, 아직 읽지 않았다면 먼저 읽고 오세요.

**이 장의 깊이**: 이 장은 **고급(설계자)** 수준입니다. 단순히 "스레드 하나를 두고 큐로 메서드 호출을 직렬화한다"는 아이디어를 넘어, Active Object와 Actor 모델의 설계상 차이, 우선순위가 있는 메서드 요청 큐, 그리고 Active Object를 06장의 Thread Pool과 07장의 Future 위에 올리는 하이브리드 구조까지 다룹니다.

**다루지 않는 것**: 분산 시스템에서의 Actor 구현(Erlang/Akka류의 메시지 패싱, 위치 투명성, 장애 복구)은 이 시리즈의 경계 밖입니다. 이 장에서 "Actor"는 비교 대상으로만 언급되며, C++ 구현은 제공하지 않습니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "동기 객체 vs Active 객체" ~ "기본 구현" | 메서드 호출이 큐를 통해 직렬화된다는 개념 이해 |
| **고급자** | "기본 구현" ~ "고급: 메서드 타입 안전성" | Active Object 구현 및 사용 |
| **설계자** | "Actor 모델과의 차이" ~ "Active Object와 Thread Pool/Future의 통합" | Actor와의 트레이드오프, 우선순위 큐, 하이브리드 구조 |

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

위 구현에서 `value`는 **항상 `run()`을 실행하는 단일 스레드에서만** 접근된다. `increment()`와 `getValue()`는 호출자의 스레드에서 실행되지 않고 `packaged_task`를 큐에 넣기만 하므로, `value`에는 어떤 락도 필요 없다 — 이것이 Active Object가 "락 없이도 안전한 객체"를 만드는 핵심 메커니즘이다.

### 안전성 검증: ThreadSanitizer

만약 `value`를 보호 없이 직접 여러 스레드에서 건드리는 "naive" 버전(아래)과 비교하면 차이가 분명해진다.

```cpp
// 깨진 버전: 여러 스레드가 직접 increment를 호출
class NaiveCounter {
public:
    void increment() { ++value; }   // 동기화 없음
    int getValue() { return value; }
private:
    int value = 0;
};

int main() {
    NaiveCounter c;
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i)
        ts.emplace_back([&c] { for (int j = 0; j < 100000; ++j) c.increment(); });
    for (auto& t : ts) t.join();
    std::cout << c.getValue() << '\n';  // 400000이 아닌 값이 흔함
}
```

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g naive_counter.cpp -o naive_counter
./naive_counter
# WARNING: ThreadSanitizer: data race on 'value'
```

반면, `ActiveCounter`에 대해 같은 4개 스레드가 `increment()`를 호출하면(각자 `.wait()`로 동기화하든 아니든), `value`에 대한 실제 증가는 항상 Active Object의 내부 스레드 하나에서만 일어난다.

```bash
g++ -std=c++20 -pthread -fsanitize=thread -g active_counter.cpp -o active_counter
./active_counter
# (경고 없음 — value는 단일 스레드에서만 접근됨)
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

Active Object와 Actor 모델은 "자신만의 실행 흐름을 가지고, 외부로부터의 요청을 큐로 받아 직렬화한다"는 핵심 아이디어를 공유한다. 하지만 인터페이스 설계와 상태 공유 방식에서 중요한 차이가 있다.

| 비교 항목 | Active Object | Actor 모델 |
|---------|---------------|-----------|
| **인터페이스** | 일반 C++ 메서드 호출 (`obj.increment()`) — 컴파일 타임에 타입 체크됨 | 메시지 전송 (`actor.send(IncrementMsg{})`) — 보통 런타임에 디스패치 |
| **반환값** | `std::future<T>`로 결과를 동기/비동기로 받음 | 보통 응답도 별도 메시지로 비동기 전송 (콜백/메일박스) |
| **상태 공유** | 메서드가 객체의 멤버 변수에 직접 접근 (단일 스레드 보장으로 락 불필요) | 액터 간 상태를 공유하지 않음 — 모든 상호작용은 메시지 |
| **위치 투명성** | 없음 — 같은 프로세스 내 객체 | 있음 — 로컬/원격 액터를 동일하게 다룸 (Akka, CAF 등) |
| **장애 모델** | 예외는 future를 통해 호출자에게 전파 | 액터 감독(supervision) 트리, "let it crash" 철학 |
| **적합한 규모** | 객체 수십 개, 메서드 호출 빈도가 응답 지연 허용치보다 충분히 낮을 때 | 수천~수백만 개의 경량 액터, 분산 환경 |

**선택 기준**: 기존 C++ 클래스를 "스레드 안전하게 만들면서도 메서드 시그니처(타입 체크)를 유지"하고 싶다면 Active Object가 적합하다. 반면 메시지 기반의 느슨한 결합, 분산/장애 복구가 필요하면 Akka·CAF 같은 Actor 프레임워크를 쓰는 것이 낫다. 이 컬렉션은 표준 라이브러리 기반 구현에 집중하므로 Active Object만 직접 구현하고, Actor는 비교 대상으로만 다룬다.

## 메서드 요청 우선순위 큐

지금까지의 구현은 `std::queue`(FIFO)를 사용했다. 하지만 실제로는 "종료 요청은 즉시 처리하되 일반 작업은 나중에 처리"처럼 **우선순위에 따라 순서를 바꿔야** 하는 경우가 많다. `std::queue`를 `std::priority_queue`로 교체하면 된다.

```cpp
#include <queue>
#include <functional>
#include <vector>
#include <future>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <type_traits>

struct MethodRequest {
    int priority;                  // 클수록 먼저 처리
    std::function<void()> task;

    // priority_queue는 기본적으로 최대 힙이므로,
    // operator<로 "더 작은 priority가 뒤로 가도록" 정의한다.
    bool operator<(const MethodRequest& other) const {
        return priority < other.priority;
    }
};

class PriorityActiveObject {
public:
    template<typename F>
    auto call(F f, int priority = 0) -> std::future<std::invoke_result_t<F>> {
        using ReturnType = std::invoke_result_t<F>;
        auto task = std::make_shared<std::packaged_task<ReturnType()>>(std::move(f));
        auto fut = task->get_future();

        {
            std::lock_guard<std::mutex> lock(mu);
            queue.push(MethodRequest{priority, [task] { (*task)(); }});
        }
        cv.notify_one();
        return fut;
    }

    PriorityActiveObject() {
        thread = std::thread([this] { run(); });
    }

    ~PriorityActiveObject() {
        {
            std::lock_guard<std::mutex> lock(mu);
            shutdown = true;
        }
        cv.notify_one();
        thread.join();
    }

private:
    void run() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mu);
                cv.wait(lock, [this] { return !queue.empty() || shutdown; });
                if (queue.empty() && shutdown) return;
                if (queue.empty()) continue;
                // priority_queue::top()은 const 참조만 반환하므로,
                // function을 move하기 위해 const_cast가 필요하다.
                task = std::move(const_cast<MethodRequest&>(queue.top()).task);
                queue.pop();
            }
            task();
        }
    }

    std::mutex mu;
    std::condition_variable cv;
    std::priority_queue<MethodRequest> queue;
    bool shutdown = false;
    std::thread thread;
};
```

**주의**: `priority_queue::top()`이 반환하는 `const MethodRequest&`에서 `std::function`을 `move`하려면 `const_cast`가 필요하다. 이는 `std::function`을 `move` 후에도 빈 상태로 안전하게 호출 가능(`pop()` 이후 더 이상 사용 안 함)하기 때문에 정당화되지만, 더 깔끔한 대안은 `MethodRequest`를 가리키는 `std::unique_ptr`을 큐에 저장하는 것이다. 우선순위 큐를 쓸 때는 **낮은 우선순위 작업이 영원히 대기(starvation)할 수 있다**는 점도 설계에서 고려해야 한다 — 예를 들어 일정 시간 이상 대기한 작업의 우선순위를 점진적으로 올리는 aging 기법이 실무에서 쓰인다.

## Active Object와 Thread Pool/Future의 통합

"성능 고려사항"에서 다루겠지만, Active Object 하나당 전용 스레드 하나를 두는 비용은 객체 수가 늘어나면 감당하기 어렵다. 하지만 **인터페이스는 Active Object처럼(메서드 호출 + future 반환) 유지하면서, 실제 실행은 06장의 Thread Pool에 위임**하는 하이브리드 구조를 만들 수 있다. 이는 "메서드 호출의 직렬화"는 보장하지 않지만(여러 작업이 풀의 다른 스레드에서 동시에 실행될 수 있음), 스레드 자원을 공유하면서도 Active Object의 비동기 인터페이스를 재사용할 수 있다.

```cpp
#include <future>
#include <memory>
#include <mutex>
#include <iostream>
#include <vector>
#include <string>

// 07장의 FutureThreadPool을 재사용한다고 가정
// (queue<function<void()>> + packaged_task 기반, "Thread Pool과 packaged_task 결합" 절 참고)
class PooledActiveLogger {
public:
    explicit PooledActiveLogger(FutureThreadPool& pool) : pool(pool) {}

    // 로그 기록은 Thread Pool의 한 워커에서 비동기로 실행되고,
    // 호출자는 future<void>로 완료를 확인할 수 있다.
    std::future<void> log(std::string message) {
        return pool.enqueue([this, msg = std::move(message)] {
            // 실제로는 파일/네트워크 I/O 등
            std::lock_guard<std::mutex> lock(writeMu);  // 출력 자체는 직렬화 필요
            std::cout << "[LOG] " << msg << '\n';
        });
    }

private:
    FutureThreadPool& pool;
    std::mutex writeMu;  // 풀의 여러 스레드가 동시에 log()를 호출할 수 있으므로 필요
};

int main() {
    FutureThreadPool pool(4);
    PooledActiveLogger logger(pool);

    std::vector<std::future<void>> results;
    for (int i = 0; i < 10; ++i) {
        results.push_back(logger.log("message " + std::to_string(i)));
    }
    for (auto& f : results) f.get();  // 모든 로그 기록 완료 대기
    return 0;
}
```

여기서 중요한 트레이드오프가 드러난다. **순수 Active Object**(전용 스레드 1개)는 `writeMu` 같은 락이 필요 없다 — 메서드 호출이 이미 단일 스레드로 직렬화되기 때문이다. 반면 **Thread Pool 기반 하이브리드**는 풀의 여러 워커가 동시에 `log()`를 실행할 수 있으므로, 공유 자원(여기서는 표준 출력)에 대한 락이 다시 필요해진다. 즉, Thread Pool과의 통합은 스레드 자원을 절약하는 대신 "단일 스레드 직렬화"라는 Active Object의 가장 큰 장점을 일부 포기하는 선택이다. 두 방식 중 어느 것을 쓸지는 다음 절의 기준을 따른다.

## 성능 고려사항

- **Context Switching**: 각 객체마다 스레드 생성 비용.
- **메모리**: 스레드당 수 MB (보통 2-8 MB).
- **사용 시점**: 객체 수가 적고(수십 개), 각자 독립적인 작업을 하며, 메서드 호출 간 **단일 스레드 직렬화**가 의미상 필요할 때(예: 내부 상태에 락을 두지 않아야 할 때)만 순수 Active Object를 쓴다.

객체 수가 많거나(100개 이상) 단일 스레드 직렬화가 필수가 아니라면, 위 "Active Object와 Thread Pool/Future의 통합" 절처럼 06장의 Thread Pool + 07장의 Future를 직접 조합하는 것을 권장한다.

## 학습 성과 평가 기준

- [ ] Active Object가 Passive Object와 어떻게 다른가?
- [ ] Active Object를 구현하고, Future로 결과를 받을 수 있는가?
- [ ] 메서드 호출이 큐를 통해 직렬화되는 방식과, 그 덕분에 내부 상태에 락이 필요 없는 이유를 설명할 수 있는가?
- [ ] Active Object와 Actor 모델의 차이를 인터페이스·상태 공유·장애 모델 관점에서 비교할 수 있는가?
- [ ] 메서드 요청 큐에 우선순위를 도입할 때 생기는 starvation 문제를 설명할 수 있는가?
- [ ] 언제 순수 Active Object를, 언제 Thread Pool + Future 하이브리드를 쓸지 판단할 수 있는가?

## 다음 장에서는

09장 **「이벤트 아키텍처 I: Reactor」**에서는 네트워크 이벤트를 한 스레드에서 처리하는 Reactor 패턴을 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 6 — Active Object 원형
- Douglas C. Schmidt, "An Object Behavioral Pattern for Concurrent Processing"
- Carl Hewitt, "Actor Model of Computation" — Actor 모델의 이론적 기반 (비교 대상으로서의 배경)


