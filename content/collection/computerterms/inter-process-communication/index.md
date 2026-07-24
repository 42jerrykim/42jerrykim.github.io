---
image: "wordcloud.png"
slug: inter-process-communication
collection_order: 59
draft: false
title: "[Computer Terms] 프로세스 간 통신 (IPC: Pipe, Shared Memory)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "독립된 메모리 공간을 가진 프로세스가 데이터를 주고받는 IPC 방식을 파이프·공유 메모리·소켓 비교로 다룹니다. pipe()와 shm_open()·세마포어 기반 동기화까지 컴파일 가능한 C 코드 예제로 자세히 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Operating-System(운영체제)
- IPC
- Pipe(파이프)
- Shared-Memory(공유메모리)
- Process(프로세스)
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
- Concurrency(동시성)
- Socket(소켓)
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 각 프로세스가 서로 격리된 독립된 메모리 공간을 갖는다고 다뤘다. 그런데 실제 시스템에서는 셸 파이프라인(`ls | grep`)처럼 서로 다른 프로세스가 데이터를 주고받아야 하는 경우가 흔하다. 이 챕터는 격리된 프로세스끼리 그 벽을 넘어 통신하는 방법들을 다룬다.

## 왜 특별한 메커니즘이 필요한가

한 프로세스의 메모리는 다른 프로세스에서 직접 읽거나 쓸 수 없다는 것이 프로세스 격리의 핵심이었다. 이 격리는 안정성과 보안을 위해 반드시 필요하지만, 동시에 서로 협력해야 하는 프로세스 사이의 데이터 교환을 막는 장벽이기도 하다. **IPC(Inter-Process Communication)**는 커널이 중개자 역할을 해 이 장벽을 안전하게 넘도록 제공하는 메커니즘들을 통칭한다. 방식마다 "얼마나 빠른가"와 "얼마나 안전한가(동기화 필요 여부)"의 트레이드오프가 다르다.

## 파이프: 단방향 바이트 스트림

**파이프(Pipe)**는 가장 단순하고 오래된 IPC 방식이다. 커널이 메모리 안에 고정 크기의 버퍼를 만들고, 한쪽 끝(쓰기 디스크립터)에 쓴 바이트가 다른 쪽 끝(읽기 디스크립터)으로 그대로 흘러나오는 **단방향 바이트 스트림**으로 동작한다. 셸에서 `ls | grep txt`를 실행하면, 셸이 `pipe()`로 파이프를 만들고 `ls`의 표준 출력을 파이프의 쓰기 쪽에, `grep`의 표준 입력을 파이프의 읽기 쪽에 연결한다. 두 프로세스는 서로의 존재를 몰라도 되고, 그저 자신의 표준 입출력에 읽고 쓰기만 하면 된다.

파이프는 커널이 버퍼를 관리하고 읽기·쓰기 호출이 시스템 콜을 거치므로, 쓰는 쪽이 다 쓰기 전에 읽는 쪽이 블록되거나 파이프 버퍼가 가득 차면 쓰는 쪽이 블록되는 흐름 제어가 자동으로 이뤄진다. 다만 이 안전성은 매 읽기·쓰기마다 커널 모드 전환([인터럽트와 시스템 콜](/post/computerterms/interrupts-and-system-calls/) 참고)이 발생한다는 비용을 동반한다.

```c
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];   /* fd[0]: 읽기 끝, fd[1]: 쓰기 끝 */
    if (pipe(fd) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();
    if (pid == 0) {
        /* 자식: 읽기 쪽만 쓰고, 쓰기 쪽은 닫는다 */
        close(fd[1]);
        char buf[64] = {0};
        read(fd[0], buf, sizeof(buf) - 1);
        printf("child received: %s\n", buf);
        close(fd[0]);
        return 0;
    }

    /* 부모: 쓰기 쪽만 쓰고, 읽기 쪽은 닫는다 */
    close(fd[0]);
    const char *msg = "hello through a pipe";
    write(fd[1], msg, strlen(msg));
    close(fd[1]);
    waitpid(pid, NULL, 0);
    return 0;
}
```

`gcc pipe_demo.c -o pipe_demo && ./pipe_demo`로 실행하면 자식 프로세스가 부모가 쓴 문자열을 그대로 읽어 출력한다. 부모와 자식이 각각 쓰지 않을 쪽 디스크립터를 즉시 닫는 것이 관례인데, 열어 둔 채로 두면 커널이 "쓰기 쪽이 아직 열려 있다"고 판단해 읽기가 EOF로 끝나지 않고 무한정 블록될 수 있기 때문이다.

## 공유 메모리: 가장 빠르지만 동기화가 필요하다

파이프는 매번 커널을 거쳐 데이터를 복사하지만, **공유 메모리(Shared Memory)**는 애초에 같은 물리 메모리 영역을 두 프로세스의 가상 주소 공간에 동시에 매핑해 둔다. 한 번 매핑되고 나면 이후의 읽기·쓰기는 일반 메모리 접근과 똑같아서 시스템 콜도, 데이터 복사도 필요 없다 — IPC 방식 중 이론적으로 가장 빠르다.

그러나 이 속도는 대가를 치른다. 파이프는 커널이 버퍼 접근을 중개하며 자연스럽게 흐름을 제어해 주지만, 공유 메모리는 두 프로세스가 같은 메모리를 **아무 때나 동시에** 읽고 쓸 수 있어 조정 장치가 전혀 없다. 한 프로세스가 절반만 쓴 데이터를 다른 프로세스가 동시에 읽으면 일관성이 깨진 값을 보게 된다. 이는 [레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 다룬 문제와 정확히 같은 종류이며, 실무에서는 세마포어나 뮤텍스를 공유 메모리 영역 자체에 함께 두어 접근을 동기화한다. "가장 빠르다"와 "가장 쓰기 쉽다"는 별개라는 점이 공유 메모리를 실무에서 파이프보다 더 조심스럽게 다루는 이유다.

다음은 POSIX 공유 메모리(`shm_open`)와 세마포어(`sem_open`)로 부모·자식이 값을 안전하게 주고받는 최소 예제다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <semaphore.h>

#define SHM_NAME "/ipc_demo_shm"
#define SEM_NAME "/ipc_demo_sem"

int main(void) {
    /* 1. 공유 메모리 객체 생성 및 크기 지정 */
    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    ftruncate(fd, sizeof(int));
    int *shared_value = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE,
                              MAP_SHARED, fd, 0);

    /* 2. 두 프로세스가 함께 쓸 세마포어 생성(초기값 0: 아직 쓰기 전) */
    sem_t *ready = sem_open(SEM_NAME, O_CREAT, 0666, 0);

    pid_t pid = fork();
    if (pid == 0) {
        /* 자식: 부모가 값을 다 쓸 때까지 세마포어로 대기 */
        sem_wait(ready);
        printf("child read: %d\n", *shared_value);
        exit(0);
    }

    /* 부모: 공유 메모리에 값을 쓴 뒤 세마포어로 자식에게 신호 */
    *shared_value = 42;
    sem_post(ready);

    waitpid(pid, NULL, 0);

    /* 3. 정리 */
    munmap(shared_value, sizeof(int));
    sem_close(ready);
    sem_unlink(SEM_NAME);
    shm_unlink(SHM_NAME);
    return 0;
}
```

`gcc ipc_shm_demo.c -o ipc_shm_demo -lrt -lpthread && ./ipc_shm_demo`로 컴파일·실행하면 `child read: 42`가 출력된다. `sem_wait(ready)`가 없다면 자식이 부모의 쓰기가 끝나기 전에 `shared_value`를 읽어버릴 수 있는데, 이것이 바로 위에서 설명한 "조정 장치가 없는" 문제의 실제 모습이다 — 세마포어가 그 조정 장치 역할을 한다.

## 비교: 파이프 vs 공유 메모리 vs 소켓

| 특성 | 파이프 | 공유 메모리 | 소켓 |
|---|---|---|---|
| 데이터 전달 방식 | 커널 버퍼를 통한 스트림 복사 | 동일 물리 메모리를 직접 공유 | 커널 버퍼를 통한 스트림/데이터그램 |
| 속도 | 중간(매 호출 시스템 콜) | 가장 빠름(매핑 후 복사 없음) | 상대적으로 느림(프로토콜 스택 경유) |
| 동기화 필요성 | 커널이 자동으로 흐름 제어 | 직접 세마포어/뮤텍스로 동기화 필요 | 커널이 자동으로 흐름 제어(TCP 등 스트림 소켓 기준. UDP는 흐름 제어 없음) |
| 통신 범위 | 대개 관련 프로세스(부모-자식) 간 | 같은 머신 내 프로세스 간 | 같은 머신 또는 네트워크 너머 |
| 대표 사용처 | 셸 파이프라인, 단순 데이터 전달 | 대용량 데이터를 빠르게 공유해야 하는 경우 | 서버-클라이언트, 원격 통신 |

소켓은 [DNS와 소켓](/post/computerterms/dns-and-sockets/) 챕터에서 다룬 대로 원래 네트워크 너머의 통신을 위해 설계됐지만, 유닉스 도메인 소켓(`AF_UNIX`)을 쓰면 같은 머신 안의 프로세스 간 통신에도 쓸 수 있다 — 다만 네트워크 프로토콜 스택을 거치는 만큼 파이프나 공유 메모리보다 오버헤드가 크다.

## 흔한 오개념

**"공유 메모리를 쓰면 항상 파이프보다 빠르다"** — 순수 메모리 접근 속도만 보면 맞지만, 실무 성능은 동기화 비용을 포함해야 한다. 락 경합이 심한 상황에서는 세마포어 대기 시간이 늘어나 오히려 파이프보다 느려질 수 있다. 게다가 공유 메모리는 설계·디버깅 복잡도가 훨씬 높으므로, 데이터량이 크지 않다면 파이프의 단순함이 실무에서 더 합리적인 선택인 경우가 많다.

**"파이프로는 양방향 통신을 할 수 없다"** — `pipe()` 하나는 단방향이 맞지만, 양방향 통신이 필요하면 파이프 두 개를 반대 방향으로 만들어 조합하면 된다(각 방향에 하나씩). 이것이 안 되는 것이 아니라, 파이프라는 기본 단위 자체의 설계가 단방향일 뿐이다. 실무에서 진짜 양방향 스트림이 필요하면 애초에 소켓(`socketpair()`)을 쓰는 것이 더 직접적인 선택이다.

## 다른 개념과의 연결

공유 메모리에서 동기화가 필요한 이유는 [레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/) 챕터의 핵심 문제와 그대로 이어진다. 프로세스가 네트워크 너머의 다른 머신과 통신할 때는 소켓이 사실상 유일한 선택지가 되며, 이는 [DNS와 소켓](/post/computerterms/dns-and-sockets/) 챕터에서 자세히 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 프로세스 격리 때문에 IPC가 필요한 이유를 설명할 수 있다. 파이프와 공유 메모리가 각각 어떤 트레이드오프(속도 대 동기화 복잡도)를 갖는지 비교할 수 있다. 데이터 규모와 동기화 요구 수준에 따라 파이프·공유 메모리·소켓 중 적절한 IPC 방식을 선택할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 3: Processes (Interprocess Communication). Wiley.

- [Linux man-pages: pipe(2)](https://man7.org/linux/man-pages/man2/pipe.2.html) — pipe() 시스템 콜의 동작과 디스크립터 관리
- [Linux man-pages: shm_overview(7)](https://man7.org/linux/man-pages/man7/shm_overview.7.html) — POSIX 공유 메모리 API 개요와 동기화 필요성
