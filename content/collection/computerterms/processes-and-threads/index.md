---
image: "wordcloud.png"
slug: processes-and-threads
collection_order: 14
draft: false
title: "[Computer Terms] 프로세스와 스레드 (Process, Thread)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "프로세스는 독립된 메모리 공간을 가진 실행 단위이고, 스레드는 그 메모리를 공유하는 더 가벼운 실행 단위입니다. 두 단위의 자원 격리 차이를 fork와 스레드 생성 코드로 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Operating-System(운영체제)
- Process(프로세스)
- Thread(스레드)
- Concurrency(동시성)
- Memory(메모리)
- C
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Debugging(디버깅)
- Performance(성능)
- Linux(리눅스)
- Implementation(구현)
---

## 이 장을 읽기 전에

새 갈래(운영체제)의 첫 챕터로, 별도 선행 챕터를 전제하지 않는다. 다만 뒤에서 다룰 스케줄링·동시성 챕터는 이 챕터의 프로세스·스레드 구분을 전제로 한다.

## 프로그램, 프로세스, 스레드

디스크에 저장된 실행 파일은 그 자체로는 아무 일도 하지 않는 **프로그램**이다. 이 프로그램을 실행하면 운영체제가 메모리에 적재하고 실행에 필요한 자원(메모리 공간, 파일 핸들, 레지스터 상태)을 할당하는데, 이렇게 만들어진 실행 중인 인스턴스가 **프로세스(Process)**다. 같은 프로그램을 두 번 실행하면 서로 독립된 메모리 공간을 가진 별개의 프로세스 두 개가 생긴다 — 한 프로세스가 자신의 메모리를 아무리 망가뜨려도 다른 프로세스에 영향을 주지 않는다.

**스레드(Thread)**는 프로세스 내부에서 실제로 명령어를 실행하는 단위다. 하나의 프로세스는 하나 이상의 스레드를 가지며, 같은 프로세스에 속한 스레드들은 그 프로세스의 메모리 공간(전역 변수, 힙)을 **공유**한다. 반면 각 스레드는 자신만의 스택과 레지스터 상태(프로그램 카운터 등)는 독립적으로 갖는다 — 그래야 각 스레드가 서로 다른 코드 위치를 동시에 실행할 수 있다.

## 격리 비용의 차이: fork vs 스레드 생성

이 차이는 새 실행 흐름을 만드는 비용에서 뚜렷이 드러난다. 새 프로세스를 만드는 `fork()`는 부모 프로세스의 메모리 공간 전체를 복제해야 하므로(실제로는 지연 복사인 copy-on-write로 최적화하지만) 상대적으로 무겁다. 반면 새 스레드를 만드는 것은 기존 메모리 공간을 그대로 공유하고 스택만 새로 할당하면 되므로 훨씬 가볍다.

```c
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>

void *thread_work(void *arg) {
    int id = *(int *)arg;
    printf("thread %d: pid=%d (부모와 같은 PID)\n", id, getpid());
    return NULL;
}

int main(void) {
    /* fork: 완전히 독립된 메모리 공간을 가진 자식 프로세스 생성 */
    pid_t pid = fork();
    if (pid == 0) {
        printf("child process: pid=%d\n", getpid());
        return 0;
    }
    waitpid(pid, NULL, 0);

    /* pthread: 같은 프로세스 안에서 메모리를 공유하는 스레드 2개 생성 */
    pthread_t threads[2];
    int ids[2] = {1, 2};
    for (int i = 0; i < 2; i++) {
        pthread_create(&threads[i], NULL, thread_work, &ids[i]);
    }
    for (int i = 0; i < 2; i++) {
        pthread_join(threads[i], NULL);
    }
    return 0;
}
```

`gcc -pthread process_thread.c -o process_thread`로 컴파일하면, 자식 프로세스는 `fork()` 시점의 부모 메모리를 그대로 복제해 자신만의 `pid`를 갖지만, 두 스레드는 `getpid()`가 항상 부모 프로세스의 PID와 동일하게 나온다 — 스레드는 별도의 프로세스가 아니라 같은 프로세스 안의 실행 흐름이기 때문이다.

## 비교: 프로세스 vs 스레드

| 특성 | 프로세스 | 스레드 |
|---|---|---|
| 메모리 공간 | 독립 | 같은 프로세스 내에서 공유 |
| 생성 비용 | 무거움 (메모리 공간 복제) | 가벼움 (스택만 추가 할당) |
| 통신 방법 | IPC (파이프, 소켓, 공유 메모리 등) | 공유 변수에 직접 접근 |
| 하나가 죽으면 | 다른 프로세스에 영향 없음 | 같은 프로세스의 다른 스레드도 함께 종료될 수 있음 |
| 대표 문제 | 프로세스 간 통신 오버헤드 | 레이스 컨디션, 데드락 |

## 흔한 오개념

**"멀티스레드가 항상 멀티프로세스보다 빠르다"** — 스레드 생성·전환이 가볍다는 것은 맞지만, 메모리를 공유한다는 것 자체가 동시 접근 시 레이스 컨디션이라는 새로운 비용(락, 동기화)을 만든다. 격리가 중요한 작업(신뢰할 수 없는 플러그인 실행, 장애 격리가 필요한 마이크로서비스)에서는 무거워도 프로세스 분리가 더 안전한 설계다.

**"파이썬은 스레드를 못 쓴다"** — CPython은 GIL(Global Interpreter Lock) 때문에 한 번에 하나의 스레드만 파이썬 바이트코드를 실행하지만, 이는 "스레드를 못 쓴다"가 아니라 "CPU 바운드 작업에서 스레드로 병렬 속도 향상을 못 얻는다"는 것이다. I/O 대기가 많은 작업(네트워크 요청, 파일 읽기)에서는 GIL이 대기 중 풀리므로 스레드가 여전히 유효하다.

## 다른 개념과의 연결

스레드가 메모리를 공유하기 때문에 생기는 문제(레이스 컨디션, 락)는 동시성 갈래에서 자세히 다룬다. 여러 프로세스/스레드 중 어떤 것을 먼저 실행할지 결정하는 문제는 다음 챕터인 스케줄링에서 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 프로세스와 스레드가 메모리 공간을 다루는 방식의 차이를 설명할 수 있다. `fork()`와 스레드 생성의 비용 차이가 어디서 오는지 설명할 수 있다. 격리가 중요한 상황과 가벼운 동시 실행이 중요한 상황을 구분해 프로세스와 스레드 중 하나를 선택할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 3–4: Processes, Threads & Concurrency. Wiley.

- [Linux man-pages: fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html) — copy-on-write 기반 프로세스 복제의 실제 동작
- [POSIX Threads Programming (LLNL)](https://hpc-tutorials.llnl.gov/posix/) — pthread API 전체를 다루는 표준 튜토리얼
