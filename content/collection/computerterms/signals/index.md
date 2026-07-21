---
image: "wordcloud.png"
slug: signals
collection_order: 58
draft: false
title: "[Computer Terms] 시그널 (Signal)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "운영체제가 프로세스에 비동기 이벤트를 전달하는 시그널 메커니즘을 SIGINT·SIGTERM·SIGKILL 차이와 핸들러 등록 코드로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Operating-System(운영체제)
- Signal(시그널)
- Process(프로세스)
- Interrupt(인터럽트)
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
- Linux(리눅스)
- Kernel
- Concurrency(동시성)
- Error-Handling(에러처리)
---

## 이 장을 읽기 전에

[인터럽트와 시스템 콜](/post/computerterms/interrupts-and-system-calls/)에서 CPU가 하드웨어 이벤트에 비동기적으로 반응하는 방식을 다뤘다. 시그널은 이와 비슷한 개념을 **커널이 프로세스에게** 전달하는 소프트웨어 계층의 메커니즘이다. `Ctrl+C`를 눌렀을 때 프로그램이 즉시 멈추는 익숙한 경험의 원리이기도 하다.

## 프로세스에게 비동기적으로 이벤트를 알리는 방법

프로그램을 실행하는 도중 터미널에서 `Ctrl+C`를 누르면 대부분의 프로그램은 즉시 종료된다. 이 종료는 프로그램이 매 순간 "사용자가 취소를 눌렀는가"를 직접 검사해서 일어나는 것이 아니다. 커널이 **시그널(Signal)**이라는 짧은 알림을 해당 프로세스에 전달하고, 프로세스는 실행 중이던 코드와 **비동기적으로** 이 알림을 받아 처리한다. 시그널은 번호와 이름으로 구분되며, 각 번호는 특정 상황을 의미하도록 표준화되어 있다. 대표적으로 `SIGINT`(2번, 인터럽트 요청 — 보통 `Ctrl+C`)와 `SIGTERM`(15번, 정상적인 종료 요청)이 있다.

시그널을 받은 프로세스가 취할 수 있는 기본 동작은 세 가지로 나뉜다. 아무 처리도 등록하지 않았다면 커널이 정한 **기본 동작(default action)**을 따르는데, 대부분의 시그널은 기본 동작이 프로세스 종료다. 프로그램이 직접 **핸들러 함수를 등록**했다면 그 함수가 대신 실행된다. 또는 특정 시그널을 **무시(ignore)**하도록 설정할 수도 있다.

## SIGKILL을 막을 수 없는 이유

거의 모든 시그널은 프로그램이 핸들러를 등록해 가로채거나 무시할 수 있지만, 딱 두 개의 시그널은 예외다. `SIGKILL`(9번)과 `SIGSTOP`(19번)은 프로세스가 어떤 방법으로도 가로채거나 무시할 수 없다. 이는 우연한 제약이 아니라 **의도적인 안전장치**다. 만약 모든 프로세스가 종료 시그널을 자유롭게 가로챌 수 있다면, 무한 루프에 빠지거나 응답 없는 프로그램을 관리자가 강제로 끝낼 방법이 사라진다. 커널은 `SIGKILL`이 도착하면 해당 프로세스의 핸들러 등록 여부와 무관하게 즉시 프로세스를 종료시킨다 — 정리(cleanup) 코드를 실행할 기회조차 주지 않고 스케줄러에서 제거한다.

이 때문에 `SIGTERM`과 `SIGKILL`은 실무에서 뚜렷이 다르게 쓰인다. `SIGTERM`은 "정상적으로 종료해 달라"는 **요청**이라, 프로그램이 핸들러를 등록해 열린 파일을 닫고 진행 중인 트랜잭션을 정리한 뒤 스스로 종료할 기회를 준다. `SIGKILL`은 그 요청이 일정 시간 안에 먹히지 않을 때 쓰는 **최후 수단**이다 — `docker stop`이 내부적으로 먼저 `SIGTERM`을 보내고, 타임아웃이 지나도 프로세스가 살아 있으면 `SIGKILL`로 강제 종료하는 것이 이 구분을 그대로 반영한 설계다.

## 코드로 보는 SIGINT 핸들러 등록

시그널 핸들러를 등록하면 `Ctrl+C`가 눌렸을 때 프로그램이 즉시 죽는 대신 정리 작업을 거쳐 종료하게 만들 수 있다.

```c
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

/* volatile sig_atomic_t: 시그널 핸들러와 메인 실행 흐름이
   동시에 접근해도 안전하게 읽고 쓸 수 있는 최소 타입 */
volatile sig_atomic_t stop_requested = 0;

void handle_sigint(int signum) {
    /* 핸들러 안에서는 async-signal-safe 함수만 호출해야 하므로
       여기서는 플래그만 세우고 실제 정리는 메인 루프에서 한다 */
    (void)signum;
    stop_requested = 1;
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = handle_sigint;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction");
        return 1;
    }

    printf("Ctrl+C를 눌러도 즉시 죽지 않고 정리 후 종료합니다 (pid=%d)\n", getpid());
    while (!stop_requested) {
        sleep(1);
    }

    printf("정리 작업 수행 중...\n");
    printf("정상 종료합니다.\n");
    return 0;
}
```

`gcc sigint_demo.c -o sigint_demo && ./sigint_demo`로 실행한 뒤 `Ctrl+C`를 누르면, 프로그램이 즉시 죽는 대신 "정리 작업 수행 중..." 메시지를 출력하고서 종료된다. 반면 같은 프로그램을 실행한 상태에서 다른 터미널로 `kill -9 <pid>`(`SIGKILL`)를 보내면 이 핸들러는 전혀 호출되지 않고 프로세스가 즉시 사라진다 — `handle_sigint`가 실행될 기회 자체가 없다. 핸들러 안에서 `sig_atomic_t` 플래그만 세우고 실제 작업은 메인 루프로 미룬 것도 임의로 고른 방식이 아니다. 시그널 핸들러는 실행 중이던 코드를 임의의 지점에서 끊고 끼어들기 때문에, `printf`처럼 내부적으로 락을 쓰는 함수를 핸들러 안에서 직접 호출하면 데드락 위험이 있다 — 그래서 POSIX는 핸들러 안에서 호출해도 안전한 **async-signal-safe** 함수 목록을 별도로 규정한다.

## 비교: 주요 시그널

| 시그널 | 번호 | 기본 동작 | 가로챌 수 있는가 | 대표 발생 상황 |
|---|---|---|---|---|
| `SIGINT` | 2 | 프로세스 종료 | 가능 | `Ctrl+C` 입력 |
| `SIGTERM` | 15 | 프로세스 종료 | 가능 | `kill <pid>`, 정상 종료 요청 |
| `SIGKILL` | 9 | 프로세스 즉시 종료 | 불가능 | `kill -9 <pid>`, 강제 종료 |
| `SIGSTOP` | 19 | 프로세스 일시 정지 | 불가능 | `Ctrl+Z`와 유사한 강제 정지 |
| `SIGSEGV` | 11 | 프로세스 종료(+코어 덤프) | 가능(단, 복구는 매우 제한적) | 잘못된 메모리 접근 |

## 흔한 오개념

**"kill 명령어는 프로세스를 죽이는 명령어다"** — `kill`은 이름과 달리 임의의 시그널을 프로세스에 보내는 범용 명령어다. 인자를 생략하면 기본값인 `SIGTERM`(정상 종료 요청)을 보내지만, `kill -STOP <pid>`처럼 프로세스를 일시 정지시키거나 `kill -HUP <pid>`처럼 설정 재적재를 요청하는 용도로도 쓰인다. "죽인다"는 그 여러 용도 중 하나일 뿐이다.

**"시그널 핸들러 안에서는 아무 코드나 안전하게 실행할 수 있다"** — 위 코드 예제에서 다뤘듯, 핸들러는 프로그램의 다른 실행 흐름을 임의의 지점에서 끊고 끼어든다. 그 지점에 락이 걸려 있었다면 핸들러 안에서 같은 락을 다시 잡으려는 호출(`malloc`, `printf` 등 내부적으로 락을 쓰는 함수)이 데드락을 일으킬 수 있다. 실무에서는 핸들러를 최대한 짧게 유지하고, `sig_atomic_t` 플래그만 세운 뒤 실제 처리는 메인 루프로 미루는 패턴이 표준이다.

## 다른 개념과의 연결

`SIGCHLD` 시그널은 자식 프로세스가 종료될 때 부모에게 전달되어, [데몬과 좀비 프로세스](/post/computerterms/daemons-and-zombie-processes/)에서 다룬 `wait()` 호출 시점을 이벤트 기반으로 앞당기는 데 흔히 쓰인다. 시그널로 프로세스 간에 간단한 알림을 주고받는 것을 넘어 실제 데이터를 주고받는 방법은 다음 챕터인 프로세스 간 통신에서 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 시그널이 프로세스에 비동기적으로 전달되는 원리와 기본 동작·핸들러·무시의 세 가지 대응 방식을 설명할 수 있다. `SIGKILL`이 가로채기 불가능하도록 설계된 이유를 설명할 수 있다. `SIGINT` 핸들러를 등록해 정리 작업을 거쳐 종료하는 프로그램을 작성할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 3.3: Interprocess Communication (Signals). Wiley.

- [Linux man-pages: signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) — 표준 시그널 전체 목록과 기본 동작, async-signal-safe 함수 목록
- [Linux man-pages: sigaction(2)](https://man7.org/linux/man-pages/man2/sigaction.2.html) — 시그널 핸들러 등록 API 명세
