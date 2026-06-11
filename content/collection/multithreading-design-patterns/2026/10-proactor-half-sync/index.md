---
title: "[Concurrency Patterns] 10. 이벤트 아키텍처 II: Proactor와 Half-Sync/Half-Async"
description: "비동기 I/O (Proactor), 멀티스레드 이벤트 처리, 그리고 동기/비동기 경계를 관리하는 Half-Sync/Half-Async 패턴을 학습합니다."
date: 2026-06-11
lastmod: 2026-06-11
draft: true
collection_order: 10
difficulty: advanced
prerequisites:
  - "09장: Reactor 패턴"
  - "비동기 I/O의 개념"
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
  - Design-Pattern
  - 디자인패턴
  - Architecture
  - Async
  - 비동기
  - Tutorial
  - Guide
slug: cpp-proactor-async-io-half-sync-half-async
---

10장은 **Reactor의 다음 단계**를 다룬다. Reactor는 준비된 소켓을 폴링했지만, Proactor는 **I/O 완료를 비동기로 통지**받는다. 또한 단일 스레드 Reactor를 여러 스레드로 확장하는 Half-Sync/Half-Async 패턴도 함께 배운다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **고급자** | "Reactor vs Proactor" ~ "Half-Sync/Half-Async 패턴" | 패턴 비교 이해 |
| **시스템 설계자** | 전체, 특히 "웹 서버 스켈레톤" | 실제 서버 설계에 적용 |

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

```cpp
class Proactor {
public:
    using CompletionHandler = std::function<void(int bytesRead, const char* data)>;

    void asyncRead(int fd, CompletionHandler handler) {
        // OS에 비동기 읽기 요청 (즉시 반환)
        osAsyncRead(fd, [handler](int bytes, const char* buf) {
            // OS가 나중에 호출: 읽기 완료
            handler(bytes, buf);
        });
    }

    void run() {
        while (true) {
            // OS가 완료된 작업 통지
            osWaitForCompletion([this](int fd, const char* data, int bytes) {
                // 콜백 호출
            });
        }
    }

private:
    void osAsyncRead(int fd, std::function<void(int, const char*)> cb);
    void osWaitForCompletion(std::function<void(int, const char*, int)> handler);
};
```

## 플랫폼별 지원

| OS | 기법 | 효율성 |
|----|----|--------|
| Windows | IOCP (I/O Completion Port) | 최고 |
| Linux | AIO (Asynchronous I/O), io_uring | 높음 |
| macOS | kqueue | 높음 |

POSIX AIO는 복잡하고 느려서, 많은 라이브러리 (Asio, libuv)는 Reactor를 선택한다.

## Half-Sync/Half-Async 패턴

**문제**: 단일 스레드 Reactor는 CPU 바운드 작업을 할 수 없다. 하나의 요청이 오래 걸리면 다른 이벤트를 처리할 수 없다.

**해결**: **비동기 계층 (이벤트 루프)** + **동기 계층 (워커 스레드)**를 분리한다.

```cpp
class HalfSyncHalfAsync {
private:
    // 비동기 계층: 이벤트 루프 (1개 스레드)
    Reactor eventLoop;
    
    // 동기 계층: 워커 스레드 풀
    ThreadPool workers;
    
    // 계층 간 통신: 큐
    BoundedQueue<Task> syncQueue;

public:
    HalfSyncHalfAsync(size_t numWorkers)
        : workers(numWorkers) {
        // 이벤트 루프와 워커 풀이 병렬 동작
        eventLoop.run();  // 비동기 계층
        startWorkers();   // 동기 계층
    }

    // I/O 이벤트: 비동기 계층에서 처리
    void onDataReady(int fd) {
        // 읽기는 빠름 (비동기)
        std::string data = readFromFd(fd);
        
        // 무거운 처리는 워커에 위임 (동기)
        syncQueue.push([data] {
            processData(data);  // 오래 걸림
        });
    }

private:
    void startWorkers() {
        for (size_t i = 0; i < workers.size(); ++i) {
            workers.enqueue([this] {
                while (true) {
                    auto task = syncQueue.pop();
                    task();
                }
            });
        }
    }
};
```

## Half-Sync/Half-Async의 구조도

```
┌─────────────────────────────────────────┐
│  Synchronous Service Layer (Workers)    │
│  - CPU-intensive processing             │
│  - Multiple threads, blocking I/O ok    │
└──────────────┬──────────────────────────┘
               │ (sync queue)
┌──────────────▼──────────────────────────┐
│  Asynchronous Service Layer (Reactor)   │
│  - Event loop, single thread            │
│  - Non-blocking I/O                     │
└─────────────────────────────────────────┘
```

## 실전: Half-Sync/Half-Async 웹 서버 스켈레톤

```cpp
class SimpleWebServer {
private:
    Reactor reactor;  // I/O 이벤트 처리
    ThreadPool workers(4);  // HTTP 처리
    BoundedQueue<std::string> requestQueue(100);

public:
    SimpleWebServer() {
        reactor.registerHandler(listenSocket, [this](int fd) {
            onNewConnection(fd);
        });
    }

    void onNewConnection(int fd) {
        // 비동기: 짧은 읽기
        reactor.asyncRead(fd, [this, fd](const char* data, int bytes) {
            onRequestReady(fd, data, bytes);
        });
    }

    void onRequestReady(int fd, const char* data, int bytes) {
        // HTTP 처리를 워커에 위임
        workers.enqueue([this, fd, data = std::string(data, bytes)] {
            std::string response = processHttpRequest(data);
            reactor.asyncWrite(fd, response);
        });
    }

private:
    std::string processHttpRequest(const std::string& request) {
        // CPU-bound: 파싱, 비즈니스 로직
        return "HTTP/1.1 200 OK\r\n...";
    }
};
```

## 선택: 단일 Reactor vs Half-Sync/Half-Async

| 시나리오 | 권장 패턴 |
|---------|----------|
| I/O 바운드, 가벼운 처리 | 단일 Reactor |
| I/O 바운드, 무거운 처리 | Half-Sync/Half-Async |
| CPU 바운드 | 스레드 풀 |
| 혼합 | Half-Sync/Half-Async + 파이프라인 |

## 학습 성과 평가 기준

- [ ] Reactor와 Proactor의 차이 (동기 vs 비동기 I/O)를 설명할 수 있는가?
- [ ] Half-Sync/Half-Async 패턴의 목표와 구조를 설명할 수 있는가?
- [ ] 비동기 계층과 동기 계층을 큐로 분리하는 이유를 이해하는가?
- [ ] 웹 서버 시나리오에서 Half-Sync/Half-Async를 설계할 수 있는가?

## 다음 장에서는

11장 **「공유 회피 (Avoiding Shared State)」**에서는 공유 자체를 없애는 전략 (불변성, Copy-on-Write, thread_local)을 다룬다.

## 참고 및 출처

- POSA2 (Schmidt et al.), Chapter 7 — Half-Sync/Half-Async 원형
- Douglas C. Schmidt, "Proactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Asynchronous Events"
- Mark Vinoski, "Boost.Asio C++ Network Programming" (2010)
