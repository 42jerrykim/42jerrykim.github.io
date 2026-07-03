---
image: wordcloud.png
title: "[Concurrency Patterns] 10. 이벤트 아키텍처 II: Proactor와 Half-Sync/Half-Async"
description: "비동기 I/O (Proactor), 멀티스레드 이벤트 처리, 그리고 동기/비동기 경계를 관리하는 Half-Sync/Half-Async 패턴을 학습합니다."
date: 2026-06-20
lastmod: 2026-06-21
draft: false
collection_order: 10
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Proactor
  - Asynchronous-I-O
  - IOCP
  - Half-Sync-Half-Async
  - Event-Architecture
  - Multi-threaded-Reactor
  - Thread-Pool
  - Design-Pattern(디자인패턴)
  - System-Design
  - Async(비동기)
  - Tutorial(튜토리얼)
  - Guide(가이드)
slug: cpp-proactor-async-io-half-sync-half-async
---

10장은 **Reactor의 다음 단계**를 다룬다. Reactor는 준비된 소켓을 폴링했지만, Proactor는 **I/O 완료를 비동기로 통지**받는다. 또한 단일 스레드 Reactor를 여러 스레드로 확장하는 Half-Sync/Half-Async 패턴도 함께 배운다. 09장에서 "한 스레드가 수만 개의 연결을 어떻게 감시하는가"를 풀었다면, 이 장은 두 가지 남은 질문을 다룬다 — "OS가 더 적극적으로 I/O를 대신해 줄 수 있는가?(Proactor)"와 "이벤트 루프가 무거운 작업을 만나면 멈춰버리는 문제는 어떻게 푸는가?(Half-Sync/Half-Async)".

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [09장 「이벤트 아키텍처 I: Reactor」](/post/multithreading-patterns/cpp-reactor-event-driven-single-thread/)에서 다룬 이벤트 디멀티플렉싱(`poll`)과 이벤트 루프 개념을 전제로 합니다. 09장을 먼저 읽고 오세요. 또한 03~04장의 `std::condition_variable` 기반 Bounded Queue를 다시 떠올릴 수 있으면 좋습니다 — 이 장의 핵심 구조 중 하나가 그 큐의 재사용이기 때문입니다.

**이 장의 깊이**: 이 장은 **심화(advanced)** 수준입니다. Proactor의 "완료 통지" 개념을 `std::async`와 콜백으로 모사한 예제, 그리고 `std::thread`/`std::queue`/`std::condition_variable`만으로 실제 컴파일되는 Half-Sync/Half-Async 서버 스켈레톤을 직접 구현하는 것이 목표입니다.

**다루지 않는 것**: 이 장은 `io_uring`이나 Windows IOCP, POSIX AIO의 실제 시스템 콜 시퀀스를 구현하지 않습니다 — 이들은 플랫폼 종속적이고 설정이 복잡해 이 시리즈의 "표준 라이브러리만" 원칙과 맞지 않습니다. 대신 **Proactor가 호출자에게 제공하는 의미(semantics)** — "요청은 즉시 반환되고, 완료는 나중에 콜백으로 통지된다" — 를 `std::async` 기반의 작은 예제로 재현해 핵심 개념을 체득하는 데 집중합니다. io_uring의 실전 활용은 이 시리즈의 범위를 넘어서며, 별도의 비동기 I/O 전문 자료(예: liburing 문서)를 참고하기 바랍니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **고급자** | "Reactor vs Proactor" ~ "Half-Sync/Half-Async 패턴" | 패턴 비교 이해 |
| **시스템 설계자** | 전체, 특히 "실전: Half-Sync/Half-Async 서버 스켈레톤" | 실제 서버 설계에 적용 |

---

## Reactor vs Proactor

**Reactor** (동기 I/O):
```
1. "읽을 데이터 있나?" 확인 (select/poll/epoll)
2. 있으면 read() 호출 (블로킹, 하지만 준비됨)
3. 데이터 처리
```

**Proactor** (비동기 I/O):
```
1. "이 소켓에서 읽어줘" 요청 (즉시 반환)
2. 나중에 OS가 "읽기 완료, 데이터 있음" 통지
3. 콜백에서 데이터 처리
```

## Proactor 개념

Proactor의 핵심 의미는 다음 세 단계다.

1. **요청**: "이 fd에서 N바이트를 읽어서, 끝나면 이 콜백을 불러줘" — 호출은 **즉시 반환**된다.
2. **수행**: 실제 읽기는 OS(또는 OS를 흉내 내는 다른 실행 주체)가 백그라운드에서 수행한다.
3. **완료 통지**: 작업이 끝나면 결과(읽은 바이트 수, 데이터)와 함께 콜백이 호출된다.

진짜 IOCP/io_uring은 커널이 이 작업을 수행하지만, **호출자 입장에서의 의미는 "비동기 요청 + 완료 콜백"으로 동일**하다. 이 의미를 표준 라이브러리만으로 재현하면 다음과 같다 — `std::async`로 "백그라운드 수행자" 역할을, 콜백으로 "완료 통지"를 모사한다.

```cpp
// proactor_sim.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 proactor_sim.cpp -o proactor_sim
#include <future>
#include <functional>
#include <iostream>
#include <thread>
#include <vector>
#include <unistd.h>

// std::async 기반으로 Proactor의 "요청 즉시 반환 + 완료 콜백" 의미를 모사한다.
// 실제 IOCP/io_uring은 커널이 I/O를 수행하지만, 호출자 인터페이스의 의미는 동일하다.
class SimulatedProactor {
public:
    using CompletionHandler = std::function<void(ssize_t bytesRead, std::string data)>;

    // 즉시 반환. 읽기는 별도 실행 흐름(std::async)에서 수행되고,
    // 끝나면 handler가 호출된다.
    void asyncRead(int fd, size_t maxBytes, CompletionHandler handler) {
        futures_.push_back(std::async(std::launch::async,
            [fd, maxBytes, handler] {
                std::string buf(maxBytes, '\0');
                ssize_t n = read(fd, buf.data(), maxBytes);
                if (n < 0) n = 0;
                buf.resize(static_cast<size_t>(n));
                handler(n, std::move(buf));  // 완료 통지
            }));
    }

    // 등록된 모든 비동기 작업의 완료를 기다린다.
    // 실제 Proactor의 run()은 이벤트 루프이지만, 데모에서는 join에 해당한다.
    void waitAll() {
        for (auto& f : futures_) f.wait();
        futures_.clear();
    }

private:
    std::vector<std::future<void>> futures_;
};

int main() {
    int fds[2];
    pipe(fds);
    write(fds[1], "async-io", 8);
    close(fds[1]);

    SimulatedProactor proactor;

    // (1) 요청: 즉시 반환된다 — read()는 아직 끝나지 않았을 수 있다.
    proactor.asyncRead(fds[0], 64, [](ssize_t bytes, std::string data) {
        // (3) 완료 통지: 별도 실행 흐름에서 호출된다.
        std::cout << "완료: " << bytes << " bytes, data=" << data << '\n';
    });

    std::cout << "요청 발행 직후 (읽기가 끝났는지 알 수 없음)\n";

    // (2) 완료 대기
    proactor.waitAll();
    close(fds[0]);
    return 0;
}
```

출력 순서는 "요청 발행 직후" 메시지가 먼저(또는 거의 동시에) 나오고, 그 후 "완료: ..." 메시지가 나온다 — Reactor의 `read()`는 "준비된 뒤 호출자가 직접 읽는" 모델이지만, Proactor는 "읽기 자체도 위임하고 결과만 받는" 모델이라는 차이가 코드 구조에 그대로 드러난다.

## 플랫폼별 지원

| OS | 기법 | 효율성 |
|----|----|--------|
| Windows | IOCP (I/O Completion Port) | 최고 |
| Linux | AIO (Asynchronous I/O), io_uring | 높음 |
| macOS | kqueue (Reactor 스타일) | 높음 |

POSIX AIO는 복잡하고 느려서, 많은 라이브러리(Asio, libuv)는 Linux/macOS에서는 epoll/kqueue 기반 Reactor를 쓰고, 그 위에 Proactor 스타일의 비동기 인터페이스(콜백, future)를 얹어 제공한다. `io_uring`(Linux 5.1+)은 진짜 커널 수준 Proactor에 가깝지만 설정과 버전 호환성이 복잡해 이 장에서는 다루지 않는다(이 장의 "다루지 않는 것" 참고). Windows의 IOCP는 처음부터 Proactor 모델로 설계되어 있어, 09장에서 본 "select/poll/epoll" 계열의 직접적인 대응이 없다.

## Half-Sync/Half-Async 패턴

**문제**: 단일 스레드 Reactor는 CPU 바운드 작업을 할 수 없다. 하나의 요청이 오래 걸리면 다른 이벤트를 처리할 수 없다.

**해결**: **비동기 계층 (이벤트 루프)** + **동기 계층 (워커 스레드)**를 분리한다. 이벤트 루프는 "데이터가 도착했다"는 사실만 빠르게 확인하고, 실제 처리(파싱, 비즈니스 로직, CPU 연산)는 03~04장에서 만든 **조건변수 기반 Bounded Queue**를 통해 워커 스레드에 넘긴다.

## Half-Sync/Half-Async의 구조도

```
┌─────────────────────────────────────────┐
│  Synchronous Service Layer (Workers)    │
│  - CPU-intensive processing             │
│  - Multiple threads, blocking I/O ok    │
└──────────────┬──────────────────────────┘
               │ (sync queue: condition_variable 기반)
┌──────────────▼──────────────────────────┐
│  Asynchronous Service Layer (Reactor)   │
│  - Event loop, single thread            │
│  - Non-blocking I/O (poll)              │
└─────────────────────────────────────────┘
```

## 실전: Half-Sync/Half-Async 서버 스켈레톤

다음 예제는 **실제로 컴파일되는** Half-Sync/Half-Async 골격이다. 비동기 계층은 09장의 `PollReactor`(파이프 fd로 데모)를, 동기 계층은 03~04장의 `condition_variable` 기반 Bounded Queue를 재사용한다.

```cpp
// half_sync_half_async.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 half_sync_half_async.cpp -o hsha
#include <atomic>
#include <condition_variable>
#include <cstring>
#include <functional>
#include <iostream>
#include <map>
#include <mutex>
#include <poll.h>
#include <queue>
#include <thread>
#include <unistd.h>
#include <vector>

// --- 동기 계층: Bounded Queue (03~04장과 동일한 패턴) ---
template <typename T>
class BoundedQueue {
public:
    explicit BoundedQueue(size_t capacity) : capacity_(capacity) {}

    void push(T item) {
        std::unique_lock<std::mutex> lock(mu_);
        notFull_.wait(lock, [this] { return queue_.size() < capacity_ || done_; });
        if (done_) return;
        queue_.push(std::move(item));
        notEmpty_.notify_one();
    }

    bool pop(T& out) {
        std::unique_lock<std::mutex> lock(mu_);
        notEmpty_.wait(lock, [this] { return !queue_.empty() || done_; });
        if (queue_.empty()) return false;  // done_ && empty -> 종료
        out = std::move(queue_.front());
        queue_.pop();
        notFull_.notify_one();
        return true;
    }

    void shutdown() {
        std::lock_guard<std::mutex> lock(mu_);
        done_ = true;
        notEmpty_.notify_all();
        notFull_.notify_all();
    }

private:
    size_t capacity_;
    std::queue<T> queue_;
    std::mutex mu_;
    std::condition_variable notEmpty_, notFull_;
    bool done_ = false;
};

// --- 비동기 계층: 09장의 PollReactor ---
class PollReactor {
public:
    using EventHandler = std::function<void(int fd)>;

    void registerHandler(int fd, EventHandler handler) {
        handlers_[fd] = std::move(handler);
    }
    void unregisterHandler(int fd) { handlers_.erase(fd); }
    void stop() { running_ = false; }

    void run() {
        running_ = true;
        while (running_ && !handlers_.empty()) {
            std::vector<struct pollfd> pfds;
            pfds.reserve(handlers_.size());
            for (auto& [fd, handler] : handlers_) pfds.push_back({fd, POLLIN, 0});

            int n = poll(pfds.data(), pfds.size(), -1);
            if (n < 0) { if (errno == EINTR) continue; break; }

            for (auto& pfd : pfds) {
                if (pfd.revents & (POLLIN | POLLHUP | POLLERR)) {
                    auto it = handlers_.find(pfd.fd);
                    if (it != handlers_.end()) it->second(pfd.fd);
                }
            }
        }
    }

private:
    std::map<int, EventHandler> handlers_;
    bool running_ = false;
};

// --- Half-Sync/Half-Async 서버 ---
class HalfSyncHalfAsyncServer {
public:
    HalfSyncHalfAsyncServer(size_t numWorkers, size_t queueCapacity)
        : taskQueue_(queueCapacity) {
        for (size_t i = 0; i < numWorkers; ++i) {
            workers_.emplace_back([this] {
                std::function<void()> task;
                while (taskQueue_.pop(task)) {
                    task();  // CPU 바운드 처리: 워커 스레드, blocking I/O 허용
                }
            });
        }
    }

    ~HalfSyncHalfAsyncServer() {
        taskQueue_.shutdown();
        for (auto& w : workers_) w.join();
    }

    // 비동기 계층: 이벤트가 도착하면 짧게 읽고, 처리는 워커에 위임한다.
    void onDataReady(int fd) {
        char buf[256];
        ssize_t n = read(fd, buf, sizeof(buf));
        if (n <= 0) {
            reactor_.unregisterHandler(fd);
            close(fd);
            return;
        }
        std::string data(buf, static_cast<size_t>(n));
        taskQueue_.push([data] {
            // 동기 계층: CPU 바운드 처리 (파싱, 비즈니스 로직)
            std::cout << "[worker " << std::this_thread::get_id()
                      << "] processed: " << data << '\n';
        });
    }

    void registerFd(int fd) {
        reactor_.registerHandler(fd, [this](int f) { onDataReady(f); });
    }

    void run() { reactor_.run(); }  // 비동기 계층: 이벤트 루프 (단일 스레드)

private:
    PollReactor reactor_;
    BoundedQueue<std::function<void()>> taskQueue_;
    std::vector<std::thread> workers_;
};

int main() {
    HalfSyncHalfAsyncServer server(/*numWorkers=*/4, /*queueCapacity=*/16);

    int fds[2];
    pipe(fds);
    write(fds[1], "request-1", 9);
    close(fds[1]);

    server.registerFd(fds[0]);
    server.run();  // handlers_가 비면 종료 (데모용)
    close(fds[0]);
    return 0;
}
```

이 스켈레톤에서 **비동기 계층(이벤트 루프)은 절대 블로킹되지 않는다** — `read()`로 짧게 데이터를 가져온 뒤 즉시 `taskQueue_.push()`로 워커에 넘긴다. **동기 계층(워커 스레드)은 자유롭게 블로킹 I/O나 무거운 연산을 수행**할 수 있다 — 이벤트 루프와 별개의 스레드이기 때문이다. `BoundedQueue`가 가득 차면 `push()`가 대기하므로(backpressure), 워커가 느릴 때 이벤트 루프가 무한정 작업을 쌓지 않는다.

### 안전성 검증

`BoundedQueue`의 모든 공유 상태(`queue_`, `done_`)는 `mu_`로 보호되고, `condition_variable`이 happens-before 관계를 만든다(01장 참고) — 이벤트 루프 스레드가 `push()`하고 워커 스레드가 `pop()`해도 데이터 레이스는 없다. 반대로 만약 `taskQueue_` 접근에서 락을 빼먹는다면(예: `queue_.push()`를 락 없이 호출) `g++ -fsanitize=thread`로 빌드해 실행했을 때 `WARNING: ThreadSanitizer: data race`가 `queue_`의 내부 포인터 조작 지점에서 보고된다. 이 시리즈의 다른 "큐" 예제들과 동일한 검증 절차다.

## 선택: 단일 Reactor vs Half-Sync/Half-Async

| 시나리오 | 권장 패턴 |
|---------|----------|
| I/O 바운드, 가벼운 처리 | 단일 Reactor |
| I/O 바운드, 무거운 처리 | Half-Sync/Half-Async |
| CPU 바운드 | 스레드 풀 |
| 혼합 | Half-Sync/Half-Async + 파이프라인 |

## 학습 성과 평가 기준

- [ ] Reactor와 Proactor의 차이 (동기 vs 비동기 I/O)를 설명할 수 있는가?
- [ ] `std::async` + 콜백으로 Proactor의 "요청 즉시 반환 + 완료 통지" 의미를 재현할 수 있는가?
- [ ] Half-Sync/Half-Async 패턴의 목표와 구조를 설명할 수 있는가?
- [ ] `condition_variable` 기반 Bounded Queue로 비동기 계층과 동기 계층을 분리하고, backpressure가 어떻게 작동하는지 설명할 수 있는가?
- [ ] 웹 서버 시나리오에서 Half-Sync/Half-Async를 설계할 수 있는가?

## 다음 장에서는

11장 **「공유 회피 (Avoiding Shared State)」**에서는 공유 자체를 없애는 전략 (불변성, Copy-on-Write, thread_local)을 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 7 — Half-Sync/Half-Async 원형
- Douglas C. Schmidt, "Proactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Asynchronous Events"
- Mark Vinoski, "Boost.Asio C++ Network Programming" (2010)


