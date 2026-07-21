---
image: "wordcloud.png"
slug: cpu-scheduling
collection_order: 15
draft: false
title: "[Computer Terms] CPU 스케줄링 (CPU Scheduling)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "CPU 스케줄링은 제한된 CPU 코어를 여러 프로세스·스레드에 어떤 순서로 배정할지 결정하는 운영체제의 핵심 기능입니다. FCFS, SJF, 라운드 로빈을 비교하고 우선순위 역전 문제를 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Operating-System(운영체제)
- Scheduling(스케줄링)
- Process(프로세스)
- Thread(스레드)
- Concurrency(동시성)
- Time-Complexity(시간복잡도)
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
- Performance(성능)
- Queue(큐)
- Real-Time(실시간)
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 다룬 "여러 실행 흐름이 동시에 존재한다"는 전제를 안다고 가정한다. CPU 코어 수는 유한한데 실행 대기 중인 프로세스/스레드는 그보다 훨씬 많은 것이 보통이므로, 운영체제는 누구에게 언제 CPU를 줄지 결정해야 한다 — 이 결정 규칙이 스케줄링이다.

## 왜 스케줄링이 필요한가

싱글 코어 CPU에서도 우리는 여러 프로그램이 "동시에" 실행되는 것처럼 느낀다. 실제로는 운영체제가 아주 짧은 시간(타임 슬라이스)마다 실행 중인 프로세스를 바꿔가며(**컨텍스트 스위칭, Context Switching**) 번갈아 실행시키기 때문이다. 어떤 순서로, 얼마나 오래 CPU를 줄지 정하는 정책이 **CPU 스케줄링**이며, 이 정책의 선택이 응답성·공정성·처리량을 좌우한다.

## 대표적인 스케줄링 정책

**FCFS(First-Come-First-Served)**는 도착한 순서대로 처리하는 가장 단순한 정책이다. 구현이 쉽지만, 앞선 작업이 오래 걸리면 뒤 작업이 무한정 대기하는 **콘보이 효과(Convoy Effect)**가 생긴다. **SJF(Shortest Job First)**는 실행 시간이 짧은 작업을 먼저 처리해 평균 대기 시간을 이론적으로 최소화하지만, 실제 실행 시간을 미리 알아야 하고 긴 작업이 계속 밀리는 **기아(Starvation)** 문제가 있다. **라운드 로빈(Round Robin)**은 각 작업에 정해진 타임 슬라이스만큼만 CPU를 주고 다음 작업으로 넘기는 방식으로, 대화형 시스템의 응답성을 보장하는 데 널리 쓰인다.

```c
#include <stdio.h>

typedef struct {
    int id;
    int burst_time;     /* 필요한 총 실행 시간 */
    int remaining_time;
} Process;

/* 라운드 로빈: 각 프로세스에 quantum만큼만 실행하고 큐 뒤로 보낸다 */
void round_robin(Process procs[], int n, int quantum) {
    int time = 0;
    int done;
    do {
        done = 1;
        for (int i = 0; i < n; i++) {
            if (procs[i].remaining_time <= 0) continue;
            done = 0;

            int slice = procs[i].remaining_time < quantum
                            ? procs[i].remaining_time
                            : quantum;
            printf("t=%d: process %d 실행 (%d만큼)\n", time, procs[i].id, slice);
            time += slice;
            procs[i].remaining_time -= slice;
        }
    } while (!done);
}

int main(void) {
    Process procs[] = {
        {1, 10, 10},
        {2, 4, 4},
        {3, 6, 6},
    };
    round_robin(procs, 3, 4);   /* quantum = 4 */
    return 0;
}
```

이 코드에서 타임 슬라이스(`quantum`)를 지나치게 작게 잡으면 컨텍스트 스위칭 자체의 오버헤드(레지스터 저장/복원)가 실제 작업 시간을 잠식하고, 반대로 너무 크게 잡으면 FCFS와 다를 바 없어져 응답성이 떨어진다 — 라운드 로빈의 실무 튜닝은 이 두 극단 사이에서 균형을 찾는 문제다.

## 우선순위 스케줄링과 우선순위 역전

**우선순위 스케줄링**은 각 작업에 우선순위를 매겨 높은 순서대로 실행한다. 여기서 발생하는 대표적인 함정이 **우선순위 역전(Priority Inversion)**이다. 낮은 우선순위 작업 A가 공유 자원의 락을 쥐고 있는 동안, 높은 우선순위 작업 C가 그 락을 기다려야 한다면, C는 A가 락을 놓을 때까지 대기해야 한다. 만약 이 사이에 중간 우선순위 작업 B가 끼어들어 A의 실행을 계속 지연시키면, 결과적으로 가장 급한 C가 가장 늦게 실행되는 역설이 발생한다. 이 현상은 1997년 화성 탐사선 패스파인더의 실제 오작동 원인으로 알려져 있으며, 해법으로 **우선순위 상속(Priority Inheritance)**(락을 쥔 낮은 우선순위 작업의 우선순위를 일시적으로 높여줌) 프로토콜이 쓰인다.

## 비교: 세 가지 정책

| 정책 | 평균 대기 시간 | 응답성 | 약점 |
|---|---|---|---|
| FCFS | 순서에 따라 편차 큼 | 낮음 (긴 작업 뒤에서 대기) | 콘보이 효과 |
| SJF | 이론상 최소 | 중간 | 실행 시간을 미리 알아야 함, 기아 |
| 라운드 로빈 | FCFS보다 안정적 | 높음 (짧은 주기로 순환) | 타임 슬라이스 크기에 민감 |

## 흔한 오개념

**"우선순위가 높으면 항상 먼저 실행된다"** — 우선순위 역전 상황에서는 이 전제가 깨진다. 우선순위 자체가 실행 순서를 절대적으로 보장하지 않으며, 공유 자원 경쟁이 얽히면 예상과 다른 순서로 실행될 수 있다는 것을 실시간 시스템 설계자는 반드시 고려해야 한다.

**"타임 슬라이스는 작을수록 좋다"** — 타임 슬라이스를 줄이면 체감 응답성은 좋아지지만, 컨텍스트 스위칭 횟수가 늘어나 그 자체의 오버헤드가 커진다. 극단적으로 타임 슬라이스를 0에 가깝게 줄이면 실제 작업에 쓰이는 CPU 시간보다 전환 비용이 더 커지는 역효과가 난다.

## 다른 개념과의 연결

스케줄링이 여러 실행 흐름을 번갈아 실행시키기 때문에, 공유 자원에 동시에 접근하는 문제(레이스 컨디션, 락, 데드락)가 발생한다 — 이는 다음 동시성 갈래에서 다룬다. 우선순위 역전에서 다룬 락 경쟁은 동시성 갈래의 데드락 챕터와 직접 연결된다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. FCFS, SJF, 라운드 로빈 각각의 장단점과 적합한 상황을 설명할 수 있다. 타임 슬라이스 크기가 응답성과 오버헤드 사이에서 만드는 트레이드오프를 설명할 수 있다. 우선순위 역전이 발생하는 조건과, 우선순위 상속이 이를 완화하는 원리를 설명할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 5: CPU Scheduling. Wiley.

- [NASA JPL: What Really Happened on Mars Rover Pathfinder](https://www.rapitasystems.com/blog/what-really-happened-software-mars-pathfinder-spacecraft) — 우선순위 역전이 실제 우주 임무에서 일으킨 장애 사례
- [Linux CFS Scheduler documentation](https://docs.kernel.org/scheduler/sched-design-CFS.html) — 리눅스가 실제로 쓰는 완전 공정 스케줄러(CFS) 설계 문서
