---
title: "[Concurrency Patterns] 09. 이벤트 아키텍처 I: Reactor"
description: "단일 스레드에서 여러 이벤트 소스를 효율적으로 처리하는 Reactor 패턴을 학습합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 9
difficulty: advanced
prerequisites:
  - "01~06장: 기초부터 Thread Pool까지"
  - "이벤트 기반 시스템의 개념"
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
  - Design-Pattern
  - 디자인패턴
  - Architecture
  - Network
  - Server
  - Tutorial
  - Guide
slug: cpp-reactor-event-driven-single-thread
---

09장은 **한 스레드에서 여러 I/O 이벤트를 효율적으로 처리**하는 Reactor 패턴을 다룬다. Active Object는 "객체당 스레드"였다면, Reactor는 "이벤트당 콜백"의 이벤트 기반 구조다.

## 🎯 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **고급자** | "문제" ~ "Reactor의 기본 구조" | Reactor 개념 이해 |
| **시스템 설계자** | 전체, 특히 "구현 레벨" | select/poll/epoll 선택 기준 |

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

```cpp
#include <map>
#include <functional>
#include <iostream>

class Reactor {
public:
    using EventHandler = std::function<void(int fd)>;

private:
    std::map<int, EventHandler> handlers;
    bool running = false;

    // 실제론 select/poll/epoll 구현, 여기는 의사 코드
    std::vector<int> waitForEvents() {
        std::vector<int> readyFds;
        for (auto& [fd, handler] : handlers) {
            // OS: fd가 읽기 준비되었는가?
            if (isReadyForReading(fd)) {
                readyFds.push_back(fd);
            }
        }
        return readyFds;
    }

public:
    void registerHandler(int fd, EventHandler handler) {
        handlers[fd] = handler;
    }

    void unregisterHandler(int fd) {
        handlers.erase(fd);
    }

    void run() {
        running = true;
        while (running) {
            auto readyFds = waitForEvents();
            for (int fd : readyFds) {
                handlers[fd](fd);  // 콜백 호출
            }
        }
    }

    void stop() { running = false; }

private:
    bool isReadyForReading(int fd) {
        // select/poll/epoll 호출
        return true;  // 의사 코드
    }
};
```

## 실제 예제: Simple Echo Server

```cpp
#include <iostream>
#include <map>
#include <functional>
#include <thread>

class SimpleReactor {
private:
    std::map<int, std::function<void(int)>> handlers;
    bool running = false;
    std::thread eventThread;

public:
    void registerHandler(int fd, std::function<void(int)> handler) {
        handlers[fd] = handler;
    }

    void run() {
        running = true;
        eventThread = std::thread([this] {
            while (running) {
                for (auto& [fd, handler] : handlers) {
                    // 이 부분은 실제로 select/epoll이어야 함
                    handler(fd);
                    std::this_thread::sleep_for(
                        std::chrono::milliseconds(10)
                    );
                }
            }
        });
    }

    void stop() {
        running = false;
        if (eventThread.joinable()) eventThread.join();
    }
};
```

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

**수준 3: Epoll** (Linux, 가장 효율적)
```cpp
int epollFd = epoll_create1(0);
for (int fd : myFds) {
    struct epoll_event ev = {EPOLLIN, {.fd = fd}};
    epoll_ctl(epollFd, EPOLL_CTL_ADD, fd, &ev);
}
struct epoll_event events[64];
int n = epoll_wait(epollFd, events, 64, timeout);
```

이 장에서는 개념에 집중하고, 실제 구현은 라이브러리 (Asio, libuv, Boost.Asio)를 사용한다.

## 학습 성과 평가 기준

- [ ] Reactor 패턴의 구조 (Event Demultiplexer, Event Loop, Handler)를 설명할 수 있는가?
- [ ] 스레드 풀 vs Reactor의 트레이드오프를 이해하는가?
- [ ] Select, Poll, Epoll의 개념을 이해하는가?
- [ ] 콜백 기반 이벤트 처리의 장단점을 설명할 수 있는가?

## 다음 장에서는

10장 **「이벤트 아키텍처 II: Proactor와 Half-Sync/Half-Async」**에서는 비동기 I/O (Proactor)와 멀티스레드 이벤트 아키텍처를 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 5 — Reactor 원형
- Douglas C. Schmidt, "Reactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events"
- Linux man page: select(2), poll(2), epoll(7)
