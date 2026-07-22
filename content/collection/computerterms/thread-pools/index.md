---
image: "wordcloud.png"
slug: thread-pools
collection_order: 78
draft: false
title: "[Computer Terms] 스레드풀 (Thread Pool)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "스레드풀은 스레드를 미리 만들어 재사용해 매 작업마다 생성 비용을 치르지 않게 하는 패턴입니다. 작업 큐와 워커 구조를 C 코드로 구현하고, 풀 크기 설정이 병목과 컨텍스트 스위칭 사이에서 갖는 트레이드오프를 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Thread(스레드)
- Thread-Pool(스레드풀)
- Queue(큐)
- Worker(워커)
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
- Throughput
- Performance(성능)
- Scheduling(스케줄링)
- CPU(중앙처리장치)
- Operating-System(운영체제)
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 스레드를 생성하는 데 커널 개입 비용이 든다고 다뤘고, [스택과 큐](/post/computerterms/stacks-and-queues/)에서 큐가 먼저 들어온 순서대로 꺼내는 자료구조라고 다뤘다. 이 챕터는 이 두 개념을 결합해, 매 작업마다 스레드를 새로 만드는 대신 미리 만든 스레드에 작업을 큐로 흘려보내는 패턴을 다룬다.

## 매번 스레드를 만드는 비용

요청이 들어올 때마다 `pthread_create`로 새 스레드를 만들고, 작업이 끝나면 `pthread_join` 또는 detach로 정리하는 방식은 코드가 단순하지만 비용이 크다. 스레드 생성은 커널에 스택 메모리를 할당하고 스케줄러에 등록하는 시스템 콜을 수반하므로, 아주 짧은 작업(예: 몇 밀리초짜리 요청 처리) 하나를 위해 스레드를 만들고 버리는 비용이 실제 작업 자체보다 커질 수 있다. 초당 수천 건의 요청이 몰리는 서버라면 이 생성·소멸 비용이 누적되어 전체 처리량을 갉아먹는다.

<strong>스레드풀(Thread Pool)</strong>은 이 비용을 프로그램 시작 시점에 한 번만 치르도록 만든 패턴이다. 고정된 개수의 스레드(**워커**)를 미리 만들어두고, 작업이 들어오면 스레드를 새로 만드는 대신 **작업 큐**에 작업을 넣기만 한다. 각 워커는 큐가 빌 때까지 반복해서 작업을 꺼내 실행하고, 큐가 비면 새 작업이 들어올 때까지 대기한다 — 스레드 자체는 프로그램이 끝날 때까지 재사용된다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_WORKERS 4
#define QUEUE_CAPACITY 16

typedef struct {
    void (*func)(int);
    int arg;
} Task;

typedef struct {
    Task tasks[QUEUE_CAPACITY];
    int head, tail, count;
    int shutdown;
    pthread_mutex_t lock;
    pthread_cond_t not_empty;
} TaskQueue;

TaskQueue queue;

void queue_init(TaskQueue *q) {
    q->head = q->tail = q->count = q->shutdown = 0;
    pthread_mutex_init(&q->lock, NULL);
    pthread_cond_init(&q->not_empty, NULL);
}

void queue_push(TaskQueue *q, void (*func)(int), int arg) {
    pthread_mutex_lock(&q->lock);
    q->tasks[q->tail] = (Task){func, arg};
    q->tail = (q->tail + 1) % QUEUE_CAPACITY;
    q->count++;
    pthread_cond_signal(&q->not_empty);   /* 대기 중인 워커 하나를 깨움 */
    pthread_mutex_unlock(&q->lock);
}

void *worker_loop(void *arg) {
    while (1) {
        pthread_mutex_lock(&queue.lock);
        while (queue.count == 0 && !queue.shutdown) {
            pthread_cond_wait(&queue.not_empty, &queue.lock);   /* 작업이 없으면 대기 */
        }
        if (queue.count == 0 && queue.shutdown) {
            pthread_mutex_unlock(&queue.lock);
            break;   /* 큐가 비었고 종료 신호면 워커 루프 탈출 */
        }
        Task t = queue.tasks[queue.head];
        queue.head = (queue.head + 1) % QUEUE_CAPACITY;
        queue.count--;
        pthread_mutex_unlock(&queue.lock);

        t.func(t.arg);   /* 락 밖에서 실행: 작업 실행 중에는 큐를 잠그지 않음 */
    }
    return NULL;
}

void print_task(int n) {
    printf("worker가 작업 %d 처리\n", n);
}

int main(void) {
    pthread_t workers[NUM_WORKERS];
    queue_init(&queue);

    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_create(&workers[i], NULL, worker_loop, NULL);
    }
    for (int i = 0; i < 10; i++) {
        queue_push(&queue, print_task, i);   /* 작업 10개를 워커 4개가 나눠 처리 */
    }

    pthread_mutex_lock(&queue.lock);
    queue.shutdown = 1;
    pthread_cond_broadcast(&queue.not_empty);   /* 대기 중인 모든 워커를 깨워 종료시킴 */
    pthread_mutex_unlock(&queue.lock);

    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_join(workers[i], NULL);
    }
    return 0;
}
```

`gcc -pthread thread_pool.c -o thread_pool`로 컴파일해 실행하면 4개의 워커 스레드가 10개의 작업을 나눠 처리하고, 새 작업마다 스레드를 만들지 않는다. 이 구조는 [세마포어와 모니터](/post/computerterms/semaphores-and-monitors/)에서 다룬 모니터 패턴을 그대로 활용한다 — `pthread_mutex_t`로 큐를 보호하고 `pthread_cond_t`로 "작업이 생기면 깨어나라"는 대기를 구현한다. `queue_push`가 `pthread_cond_signal`로 워커 하나만 깨우는 반면, 종료 시에는 `pthread_cond_broadcast`로 대기 중인 모든 워커를 한 번에 깨운다는 차이도 눈여겨볼 부분이다 — 종료 신호는 특정 워커 하나가 아니라 전체가 알아야 하기 때문이다.

## 풀 크기를 정하는 트레이드오프

스레드풀의 워커 개수는 작을수록, 클수록 각각 다른 문제를 만든다. 워커가 너무 적으면 동시에 처리할 수 있는 작업 수가 제한되어 큐에 작업이 쌓이는 **병목**이 생긴다 — 특히 각 작업이 I/O 대기를 포함해 오래 걸리는 경우, 적은 워커 수로는 처리량을 늘릴 여지가 있는데도 활용하지 못한다. 반대로 워커가 너무 많으면 [CPU 스케줄링](/post/computerterms/cpu-scheduling/)에서 다룬 컨텍스트 스위칭 오버헤드가 커진다 — CPU 코어 수보다 훨씬 많은 스레드가 동시에 실행 가능 상태가 되면, 스케줄러가 스레드를 번갈아 실행시키는 전환 자체에 시간을 쓰느라 실제 작업 처리량이 오히려 줄어들 수 있다.

일반적인 경험칙은 작업의 성격에 따라 갈린다. 순수 계산 위주(CPU 바운드) 작업은 워커 수를 CPU 코어 수에 가깝게 맞추는 것이 컨텍스트 스위칭을 줄이는 데 유리하고, I/O 대기가 많은 작업(네트워크 요청, 디스크 읽기)은 코어 수보다 훨씬 많은 워커를 두어도 이득이 있다 — 워커가 I/O를 기다리는 동안 다른 워커가 CPU를 쓸 수 있기 때문이다. 정확한 최적값은 작업 특성과 하드웨어에 따라 달라지므로 벤치마크로 확인해야 하는 **구현·환경 의존적** 수치다.

| 항목 | 워커 개수가 적을 때 | 워커 개수가 많을 때 |
|---|---|---|
| 큐 대기 시간 | 길어짐(병목) | 짧아짐 |
| 컨텍스트 스위칭 | 적음 | 많아질 수 있음 |
| 메모리 사용(스택) | 적음 | 많음 |
| CPU 바운드 작업에 적합성 | 코어 수에 맞으면 적합 | 과도하면 역효과 |
| I/O 바운드 작업에 적합성 | 부족할 수 있음 | 코어 수 초과도 유리할 수 있음 |

## 흔한 오개념

**"워커 수는 많을수록 무조건 빠르다"** — 워커 수를 늘려도 CPU 코어 수와 메모리 대역폭이라는 물리적 한계는 그대로다. CPU 바운드 작업에서 워커 수를 코어 수보다 훨씬 많이 두면, 실제로 동시에 실행되는 스레드는 여전히 코어 수만큼이고 나머지는 대기·전환 오버헤드만 늘린다. "충분히 많은 워커"의 기준은 고정된 숫자가 아니라 작업이 CPU 바운드인지 I/O 바운드인지에 달려 있다.

**"스레드풀을 쓰면 락이 필요 없다"** — 스레드풀 자체는 스레드 생성 비용 문제를 해결할 뿐, 워커들이 공유 자원(작업 큐 포함)에 접근할 때 생기는 레이스 컨디션 문제는 그대로 남는다. 위 예시에서도 큐 접근은 여전히 뮤텍스로 보호해야 하고, 워커가 실행하는 작업 함수 내부에서 다른 공유 상태를 건드린다면 그 부분도 별도로 보호해야 한다.

## 다른 개념과의 연결

[코루틴과 async/await](/post/computerterms/coroutines-and-async-await/)에서 다룬 이벤트 루프 기반 비동기 런타임도 내부적으로는 이 챕터의 스레드풀 위에서 동작하는 경우가 많다 — 예를 들어 파일 I/O처럼 이벤트 루프가 직접 논블로킹으로 처리하기 어려운 작업을 별도 스레드풀에 위임하고, 완료되면 결과를 이벤트 루프에 돌려준다. 다음 챕터에서는 이 챕터의 스레드풀이 락 없는(lock-free) 큐로 구현될 때 CAS가 마주치는 ABA 문제를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 스레드풀이 매 작업마다 스레드를 생성하는 방식보다 유리한 이유를 생성 비용 관점에서 설명할 수 있다. 작업 큐와 워커 구조가 뮤텍스·조건 변수로 어떻게 구현되는지 설명할 수 있다. 풀 크기를 너무 작게 또는 너무 크게 설정했을 때 각각 어떤 문제가 생기는지, CPU 바운드와 I/O 바운드 작업의 차이를 들어 설명할 수 있다.

## 참고 자료

> Lea, D. (2000). "A Java Fork/Join Framework". *Proceedings of the ACM 2000 conference on Java Grande*, 36–43.

- [POSIX.1-2017: pthread_cond_wait, pthread_cond_broadcast](https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_cond_wait.html) — 조건 변수 API 표준 정의
- [Python docs: concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) — 실무에서 널리 쓰이는 스레드풀 구현체 문서
