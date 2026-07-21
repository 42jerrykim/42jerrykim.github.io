---
image: "wordcloud.png"
slug: daemons-and-zombie-processes
collection_order: 56
draft: false
title: "[Computer Terms] 데몬과 좀비 프로세스 (Daemon, Zombie Process)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "백그라운드에서 지속 실행되는 데몬 프로세스의 특징과, 자식 종료 후 부모가 wait하지 않아 남는 좀비 프로세스, 고아 프로세스가 init에 입양되는 과정을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Operating-System(운영체제)
- Process(프로세스)
- Daemon(데몬)
- Zombie-Process(좀비프로세스)
- Fork(포크)
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
- Systemd
- Init(초기화)
- Signal(시그널)
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 `fork()`로 프로세스를 만드는 기본 원리를 다뤘다. 이 챕터는 그렇게 만들어진 프로세스가 **오래도록 백그라운드에서 살아 있는 경우**(데몬)와, **부모-자식 관계가 정상적으로 정리되지 않았을 때** 생기는 문제(좀비·고아 프로세스)를 다룬다.

## 터미널 없이 사는 프로세스: 데몬

일반적인 프로그램은 사용자가 터미널에서 실행하고, 터미널을 닫으면 함께 종료된다. 반면 웹 서버(nginx)나 SSH 서버(sshd)처럼 사용자의 로그인 세션과 무관하게 계속 떠 있어야 하는 프로그램들이 있다. 이런 프로세스를 **데몬(Daemon)**이라 부른다. 데몬의 핵심 특징은 **제어 터미널로부터 분리**되어 있다는 점이다 — 터미널을 닫아도 `SIGHUP` 같은 신호로 함께 죽지 않는다. 전통적인 유닉스 방식에서는 프로세스가 스스로 `fork()`한 뒤 부모를 먼저 종료시키고, `setsid()`로 새 세션을 만들어 제어 터미널과의 연결을 끊는 절차(**데몬화, Daemonizing**)를 거쳤다.

현대 리눅스 배포판 대부분은 이 절차를 프로그램이 직접 구현하지 않고, **systemd** 같은 서비스 매니저가 대신 관리한다. systemd가 데몬을 자식으로 실행하고 감독하기 때문에, 데몬 프로세스의 부모 프로세스 ID(PPID)를 확인하면 보통 systemd(PID 1) 또는 systemd가 관리하는 상위 프로세스로 나타난다. 데몬이 크래시해도 systemd 설정에 따라 자동으로 재시작될 수 있다는 점도 직접 데몬화하던 시절과의 실무적 차이다.

## fork 이후 부모가 할 일을 안 하면: 좀비 프로세스

프로세스가 종료되면 운영체제는 그 프로세스가 쓰던 메모리·파일 디스크립터 같은 자원을 대부분 즉시 회수한다. 하지만 **종료 상태 코드(exit status)** 자체는 부모 프로세스가 `wait()` 또는 `waitpid()`를 호출해 확인할 때까지 커널이 남겨둔다. 부모가 아직 이 값을 읽지 않은, 이미 실행은 끝났지만 프로세스 테이블에 항목만 남아 있는 상태를 **좀비 프로세스(Zombie Process)**라 부른다. 좀비는 CPU도 메모리도 거의 쓰지 않지만, 프로세스 테이블의 슬롯(PID)을 계속 점유한다. 부모가 계속 `wait()`를 호출하지 않고 자식을 계속 생성하는 서버 프로그램이라면, 시간이 지나며 좀비가 쌓여 결국 PID 고갈이라는 실무 장애로 이어질 수 있다.

부모가 자식보다 먼저 죽어버리는 경우는 또 다르다. 이렇게 부모를 잃은 자식 프로세스를 **고아 프로세스(Orphan Process)**라 부르는데, 커널은 고아가 생기는 즉시 그 프로세스의 부모를 PID 1(전통적으로 `init`, 현대에는 대개 systemd)로 재지정한다. 이 과정을 **입양(reparenting)**이라 하며, init/systemd는 주기적으로 자신의 자식들에 대해 `wait()`를 호출하도록 설계되어 있어 고아가 좀비로 영구히 남는 것을 막는다. 반대로 데몬 프로세스가 자식을 만들고 바로 종료해 그 자식을 init에게 넘기는 것은 실제로 데몬화의 한 단계로 활용되기도 한다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();

    if (pid == 0) {
        /* 자식: 곧바로 종료 */
        printf("child(pid=%d) exiting\n", getpid());
        exit(0);
    }

    /* 부모: 일부러 5초간 wait()를 호출하지 않아
       자식을 좀비 상태로 관찰한다 */
    printf("parent: sleeping without wait(), check `ps -o pid,stat,cmd -p %d` now\n", pid);
    sleep(5);

    /* wait()를 호출해야 비로소 좀비가 사라진다 */
    int status;
    waitpid(pid, &status, 0);
    printf("parent: reaped child, exit status=%d\n", WEXITSTATUS(status));
    return 0;
}
```

`gcc zombie_demo.c -o zombie_demo && ./zombie_demo`로 실행한 뒤, 다른 터미널에서 `ps -o pid,ppid,stat,cmd -p <자식 PID>`를 5초 안에 실행하면 `STAT` 열에 `Z`(zombie)가 표시되는 것을 직접 관찰할 수 있다. `waitpid()`가 호출되는 순간 이 좀비 항목은 프로세스 테이블에서 사라진다 — 이것이 흔히 "좀비를 거둔다(reap)"고 부르는 동작이다.

## 비교: 데몬, 좀비, 고아

| 구분 | 상태 | 원인 | 정리 방법 |
|---|---|---|---|
| 데몬 | 정상 실행 중, 터미널과 분리됨 | 의도적인 백그라운드 서비스 설계 | 해당 없음(정상 동작) |
| 좀비 | 실행 종료, 프로세스 테이블 항목만 남음 | 부모가 `wait()`를 호출하지 않음 | 부모가 `wait()`/`waitpid()` 호출 |
| 고아 | 계속 실행 중, 원래 부모를 잃음 | 부모가 자식보다 먼저 종료 | 커널이 자동으로 init/systemd에 재부모 지정 |

## 흔한 오개념

**"좀비 프로세스는 죽여서 없앨 수 있다"** — 좀비는 이미 실행이 끝난 프로세스라 `kill`로 보낼 시그널을 처리할 실행 흐름 자체가 없다. 좀비를 없애는 유일한 방법은 부모가 `wait()`를 호출하게 만드는 것이다. 부모 프로세스가 응답하지 않는 버그 있는 프로그램이라면, 부모 프로세스 자체를 종료시켜야 좀비가 고아가 되어 init에게 거두어진다.

**"데몬은 항상 root 권한으로 위험하게 실행된다"** — 과거 일부 데몬이 관례적으로 root로 실행되긴 했지만, 이는 데몬의 정의와 무관한 별개의 설계 선택이다. 현대적인 서비스 매니저는 각 데몬을 전용 저권한 사용자 계정으로 실행하고 `systemd`의 샌드박싱 옵션(예: `ProtectSystem`, `NoNewPrivileges`)으로 권한을 더 제한하는 것이 표준 관례다.

## 다른 개념과의 연결

프로세스를 격리 단위로 감싸 데몬처럼 독립적으로 관리하는 개념은 다음 챕터인 컨테이너와 가상화에서 커널 네임스페이스로 확장된다. 부모-자식 관계 없이 서로 다른 프로세스가 데이터를 주고받는 방법은 [프로세스 간 통신](/post/computerterms/inter-process-communication/) 챕터에서 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 데몬이 일반 프로세스와 구분되는 특징(터미널 분리, 부모가 init/systemd)을 설명할 수 있다. 좀비 프로세스가 왜, 어떤 조건에서 생기는지와 그것이 왜 완전히 무해하지는 않은지 설명할 수 있다. 고아 프로세스가 init에 재부모 지정되는 과정을 `fork`/`wait` 관점에서 설명할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 3: Processes. Wiley.

- [Linux man-pages: wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html) — wait/waitpid의 좀비 회수 동작 명세
- [Linux man-pages: init(1)](https://man7.org/linux/man-pages/man1/init.1.html) — PID 1이 고아 프로세스를 입양하는 역할 설명
