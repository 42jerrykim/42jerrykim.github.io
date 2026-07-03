---
image: wordcloud.png
title: "[Concurrency Patterns] 09. 이벤트 아키텍처 I: Reactor"
description: "단일 스레드에서 여러 이벤트 소스를 효율적으로 처리하는 Reactor 패턴을 학습합니다."
date: 2026-06-19
lastmod: 2026-06-20
draft: false
collection_order: 9
categories:
  - Design Patterns
  - Concurrency Patterns
tags:
  - Reactor
  - Event-Driven
  - Event-Demultiplexing
  - Select
  - Poll
  - Epoll
  - Kqueue
  - Synchronous-I-O
  - Event-Loop
  - Non-blocking
  - Design-Pattern(디자인패턴)
  - System-Design
  - Network
  - Server
  - Tutorial(튜토리얼)
  - Guide(가이드)
slug: cpp-reactor-event-driven-single-thread
---

09장은 **한 스레드에서 여러 I/O 이벤트를 효율적으로 처리**하는 Reactor 패턴을 다룬다. Active Object는 "객체당 스레드"였다면, Reactor는 "이벤트당 콜백"의 이벤트 기반 구조다. 연결이 수백 개일 때는 "연결마다 스레드"가 단순하고 빠르지만, 연결이 수만 개가 되는 순간 스레드 자체의 메모리(스택)와 컨텍스트 스위치 비용이 시스템을 압도한다. Reactor는 "스레드는 적게, 이벤트는 많이"라는 역전된 사고로 이 한계를 돌파한다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [08장 「비동기 객체(Active Object)」](/post/multithreading-patterns/cpp-active-object-async-method-invocation/)에서 다룬 메시지 큐와 워커 스레드 개념, 그리고 소켓 프로그래밍의 기초(파일 디스크립터, `read`/`write`, 블로킹 I/O)를 알고 있다고 가정합니다. 소켓이 익숙하지 않다면 `man 2 socket`, `man 2 read`로 기본 시스템 콜을 먼저 훑어보세요.

**이 장의 깊이**: 이 장은 **심화(advanced)** 수준입니다. POSIX `poll()`을 사용해 실제로 동작하는 최소 Reactor를 직접 구현하고, "왜 이벤트 디멀티플렉싱이 필요한가"를 코드 레벨에서 이해하는 것이 목표입니다. select/poll/epoll의 API 차이와 선택 기준까지 다룹니다.

**다루지 않는 것**: 이 장은 프로덕션 수준의 비동기 I/O 라이브러리(Boost.Asio, libuv, libevent)의 내부 구현을 재현하지 않습니다. 타이머 큐, 시그널 처리, 에러 복구, TLS 등 실전 서버에 필요한 부가 기능도 범위 밖입니다. 목표는 "Reactor 패턴의 뼈대"를 직접 손으로 만들어, 이후 어떤 라이브러리를 쓰더라도 그 내부에서 무슨 일이 벌어지는지 읽을 수 있게 하는 것입니다. 또한 이 장의 예제는 **POSIX(Linux/macOS) 전용**입니다. Windows는 `select`/`poll`/`epoll`이 없거나 제한적이며, 대신 IOCP라는 근본적으로 다른(Proactor 스타일) 모델을 사용합니다 — 이는 10장에서 다룹니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **고급자** | "문제" ~ "Reactor의 기본 구조" | Reactor 개념 이해 |
| **시스템 설계자** | 전체, 특히 "실전: poll() 기반 Reactor 구현" | select/poll/epoll 선택 기준과 실제 동작 |

---

## 문제: 스레드 풀 vs 이벤트 루프

**방식 1: 스레드 풀** (지금까지 배운 방식)
```
각 연결마다 스레드 또는 작업 생성
→ 수천 개 연결 시 스레드 오버헤드
```

**방식 2: 이벤트 루프 (Reactor)**
```
한 스레드가 "누가 데이터를 받을 준비가 되었나?"를 폴링
→ 연결 수에 관계없이 한 스레드
```

## Reactor의 기본 구조

1. **Event Demultiplexer**: OS 레벨 (select, poll, epoll, kqueue)로 "준비된 소켓" 확인
2. **Event Loop**: 준비된 소켓들을 반복 확인
3. **Event Handler**: 각 소켓 이벤트마다 호출되는 콜백

핵심은 **"누가 준비되었는가"를 애플리케이션이 직접 묻지 않고 OS에게 한 번에 묻는다**는 점이다. 다음은 깨진(작동하지 않는) 버전부터 시작한다.

### 깨진 버전: busy-polling "Reactor"

아래 코드는 "Reactor"라는 이름을 붙였지만 실제로는 이벤트 디멀티플렉싱을 전혀 하지 않는다.

```cpp
#include <map>
#include <functional>
#include <thread>
#include <unistd.h>  // read

// 깨진 버전: 디멀티플렉싱 없이 모든 fd를 순회하며 read 시도
class BrokenReactor {
public:
    using EventHandler = std::function<void(int fd)>;

private:
    std::map<int, EventHandler> handlers;
    bool running = false;

public:
    void registerHandler(int fd, EventHandler handler) {
        handlers[fd] = handler;
    }

    void run() {
        running = true;
        while (running) {
            for (auto& [fd, handler] : handlers) {
                handler(fd);  // 데이터가 없어도 무조건 호출
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }

    void stop() { running = false; }
};
```

**왜 깨졌는가?**

1. **busy-loop**: fd가 1000개면 매 10ms마다 1000개의 핸들러를 전부 호출한다. 대부분은 읽을 데이터가 없으므로 핸들러 내부에서 `read()`가 블로킹되거나(전체 루프가 멈춤), non-blocking이면 `EAGAIN`을 처리하는 코드가 핸들러마다 중복된다.
2. **OS 통지를 활용하지 않는다**: 커널은 이미 "어떤 fd가 읽기 준비됐는지"를 알고 있다. 이 정보를 묻지 않고 매번 모든 fd를 순회하는 것은 O(N) 낭비이며, fd 수가 늘어날수록 CPU 사용률이 선형으로 증가한다.
3. **단일 스레드에서 한 핸들러가 블로킹 read를 하면 전체 이벤트 루프가 멈춘다.**

올바른 Reactor는 이 "누가 준비됐는가"라는 질문을 `poll()`(또는 `select`, `epoll_wait`)로 커널에 위임한다.

## 실전: poll() 기반 Reactor 구현

다음은 실제로 컴파일·실행되는 최소 Reactor다. 데모로는 파이프(pipe) 파일 디스크립터 두 개를 사용한다 — 소켓과 동일하게 `poll()`로 다룰 수 있고, 별도의 네트워크 설정 없이 동작을 확인할 수 있기 때문이다.

```cpp
// reactor_poll.cpp
// 빌드: g++ -std=c++20 -pthread -Wall -Wextra -O2 reactor_poll.cpp -o reactor_poll
#include <iostream>
#include <map>
#include <functional>
#include <vector>
#include <poll.h>
#include <unistd.h>
#include <cstring>

class PollReactor {
public:
    using EventHandler = std::function<void(int fd)>;

    void registerHandler(int fd, EventHandler handler) {
        handlers_[fd] = std::move(handler);
    }

    void unregisterHandler(int fd) {
        handlers_.erase(fd);
    }

    void stop() { running_ = false; }

    // 한 번의 poll() 호출로 "준비된 fd만" 골라 핸들러를 호출한다.
    void run() {
        running_ = true;
        while (running_ && !handlers_.empty()) {
            std::vector<struct pollfd> pfds;
            pfds.reserve(handlers_.size());
            for (auto& [fd, handler] : handlers_) {
                pfds.push_back({fd, POLLIN, 0});
            }

            // -1: 이벤트가 생길 때까지 무한 대기 (Event Demultiplexer)
            int n = poll(pfds.data(), pfds.size(), -1);
            if (n < 0) {
                if (errno == EINTR) continue;
                std::perror("poll");
                break;
            }

            // 준비된 fd만 디스패치 — 나머지는 건드리지 않는다.
            for (auto& pfd : pfds) {
                if (pfd.revents & (POLLIN | POLLHUP | POLLERR)) {
                    auto it = handlers_.find(pfd.fd);
                    if (it != handlers_.end()) {
                        it->second(pfd.fd);
                    }
                }
            }
        }
    }

private:
    std::map<int, EventHandler> handlers_;
    bool running_ = false;
};

int main() {
    int pipeA[2], pipeB[2];
    if (pipe(pipeA) != 0 || pipe(pipeB) != 0) {
        std::perror("pipe");
        return 1;
    }

    PollReactor reactor;

    // 핸들러: 데이터를 읽고 출력. EOF(쓰기 측 fd가 닫힘)면 등록 해제.
    auto makeHandler = [&reactor](const char* name) {
        return [&reactor, name](int fd) {
            char buf[64];
            ssize_t n = read(fd, buf, sizeof(buf) - 1);
            if (n > 0) {
                buf[n] = '\0';
                std::cout << "[" << name << "] received: " << buf << '\n';
            } else {
                std::cout << "[" << name << "] closed\n";
                reactor.unregisterHandler(fd);
                close(fd);
            }
        };
    };

    reactor.registerHandler(pipeA[0], makeHandler("A"));
    reactor.registerHandler(pipeB[0], makeHandler("B"));

    // 데모: B에만 쓰기 — poll()이 B의 read 측만 ready로 보고해야 한다.
    write(pipeB[1], "hello", 5);
    close(pipeB[1]);  // EOF 유도 -> 핸들러가 호출된 뒤 등록 해제됨
    close(pipeA[1]);  // A는 곧바로 EOF -> 핸들러가 호출되어 등록 해제됨

    reactor.run();  // handlers_가 비면 자동 종료
    return 0;
}
```

실행하면 다음과 같은 출력을 볼 수 있다(순서는 커널 스케줄링에 따라 달라질 수 있다).

```
[B] received: hello
[B] closed
[A] closed
```

여기서 핵심은 `poll()` 호출 한 번이 "A와 B 중 무엇이 준비됐는가"를 커널이 직접 알려준다는 점이다. 애플리케이션은 더 이상 빈 루프를 돌며 모든 fd를 확인하지 않는다. fd가 1,000개든 10,000개든 `poll()` 호출 자체는 한 번이고, `revents`가 설정된 fd만 디스패치된다.

### 안전성 검증

이 Reactor는 단일 스레드에서만 동작하므로 데이터 레이스는 발생하지 않는다 — `handlers_` 맵은 이벤트 루프 스레드만 접근한다. 다만 **만약 다른 스레드가 `registerHandler`/`unregisterHandler`를 호출**한다면(예: Half-Sync/Half-Async에서 워커가 새 연결을 등록하는 경우) `handlers_`는 공유 상태가 되어 데이터 레이스가 생긴다. 이 경우 `std::mutex`로 보호하거나, "등록 요청"을 파이프/큐로 이벤트 루프 스레드에 위임해야 한다. TSAN으로 확인하려면 멀티스레드 버전을 `-fsanitize=thread`로 빌드해 보자 — 보호 없이 `handlers_`에 동시 접근하면 `WARNING: ThreadSanitizer: data race`가 즉시 나타난다.

## 장점과 단점

| 특성 | 스레드 풀 | Reactor |
|------|----------|---------|
| 동시 연결 | 수백 | 수만 |
| 메모리 | 많음 | 적음 |
| Context Switch | 많음 | 적음 |
| 코드 복잡도 | 낮음 | 높음 |
| I/O 바운드 | ✓ | ✓ |
| CPU 바운드 | ✓ | X |

**선택**:
- **I/O 바운드, 많은 연결**: Reactor (예: 웹 서버, 채팅 서버)
- **적은 연결, CPU 처리**: 스레드 풀 (예: 데이터 처리 서버)

## Reactor 구현 레벨

**수준 1: Select** (POSIX 표준, 느림)
```cpp
fd_set readfds;
FD_ZERO(&readfds);
for (int fd : myFds) FD_SET(fd, &readfds);
int ready = select(maxFd + 1, &readfds, NULL, NULL, &timeout);
```

**수준 2: Poll** (더 효율적)
```cpp
std::vector<struct pollfd> pollfds;
for (int fd : myFds) {
    pollfds.push_back({fd, POLLIN, 0});
}
poll(pollfds.data(), pollfds.size(), timeout);
```

**수준 3: Epoll** (Linux 전용, 가장 효율적)
```cpp
int epollFd = epoll_create1(0);
for (int fd : myFds) {
    struct epoll_event ev{};
    ev.events = EPOLLIN;
    ev.data.fd = fd;
    epoll_ctl(epollFd, EPOLL_CTL_ADD, fd, &ev);
}
struct epoll_event events[64];
int n = epoll_wait(epollFd, events, 64, timeout);
for (int i = 0; i < n; ++i) {
    int readyFd = events[i].data.fd;
    // handlers_[readyFd](readyFd) 형태로 디스패치
}
```

`select`는 fd마다 비트마스크를 매번 다시 채워야 하고 fd 개수에 `FD_SETSIZE`(보통 1024) 제한이 있다. `poll`은 이 제한이 없고 `pollfd` 배열을 재사용할 수 있지만, 여전히 매 호출마다 전체 배열을 커널에 복사하고 O(N)으로 순회한다. `epoll`은 관심 있는 fd 집합을 커널에 한 번 등록해 두고(`epoll_ctl`), `epoll_wait`는 **준비된 fd만** 반환하므로 연결 수가 많을수록(특히 대부분이 idle인 "C10K" 상황) 압도적으로 효율적이다. 앞의 poll() 예제를 epoll로 바꾸는 것은 `pfds` 배열 구성과 `poll()` 호출 부분만 `epoll_ctl`/`epoll_wait`로 교체하면 되고, 핸들러 디스패치 로직은 동일하다.

이 장에서는 패턴의 뼈대에 집중했고, 실전 프로젝트에서는 라이브러리(Asio, libuv, Boost.Asio)가 플랫폼별 최적 메커니즘(epoll/kqueue/IOCP)을 자동으로 선택해 준다.

### Windows에서는?

Windows에는 `epoll`이 없다. `select`는 지원되지만 `FD_SETSIZE` 제한과 성능 문제가 동일하게 존재하고, `poll`에 대응하는 `WSAPoll`은 있지만 널리 쓰이지 않는다. Windows의 표준 답은 **IOCP(I/O Completion Port)**인데, IOCP는 "준비됐다"가 아니라 "**완료됐다**"를 통지하는 근본적으로 다른 모델이다 — 이것이 바로 10장에서 다루는 **Proactor** 패턴이다. 즉, Linux/macOS에서 Reactor(이 장)를 선택하는 자리에 Windows는 처음부터 Proactor 스타일(IOCP)을 강제한다고 볼 수 있다.

## 학습 성과 평가 기준

- [ ] Reactor 패턴의 구조 (Event Demultiplexer, Event Loop, Handler)를 설명할 수 있는가?
- [ ] 스레드 풀 vs Reactor의 트레이드오프를 이해하는가?
- [ ] `poll()`을 사용해 실제로 동작하는 최소 Reactor를 구현할 수 있는가?
- [ ] Select, Poll, Epoll의 API 차이와 각각의 한계를 설명할 수 있는가?
- [ ] 콜백 기반 이벤트 처리의 장단점을 설명할 수 있는가?
- [ ] 단일 스레드 Reactor에 멀티스레드로 핸들러를 등록하면 왜 데이터 레이스가 생기는지 설명할 수 있는가?

## 다음 장에서는

10장 **「이벤트 아키텍처 II: Proactor와 Half-Sync/Half-Async」**에서는 비동기 I/O (Proactor)와 멀티스레드 이벤트 아키텍처를 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 5 — Reactor 원형
- Douglas C. Schmidt, "Reactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events"
- Linux man page: select(2), poll(2), epoll(7)


