---
image: "wordcloud.png"
slug: semaphores-and-monitors
collection_order: 75
draft: false
title: "[Computer Terms] 세마포어와 모니터 (Semaphore, Monitor)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "세마포어는 값이 0/1인 뮤텍스와 달리 정수 카운트로 여러 스레드의 동시 진입을 허용하는 동기화 도구입니다. 커넥션 풀 예시, POSIX 세마포어 코드, 락+조건 변수를 캡슐화한 모니터까지 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Synchronization
- Semaphore(세마포어)
- Monitor(모니터)
- Lock(락)
- Mutex(뮤텍스)
- Thread
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
- Connection-Pool(커넥션풀)
- Operating-System(운영체제)
---

## 이 장을 읽기 전에

[레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 뮤텍스가 "값이 0 또는 1이라 한 번에 한 스레드만 임계 구역에 들어갈 수 있는" 락이라고 다뤘다. 이 챕터는 그 값이 1이 아니라 임의의 정수일 때 어떤 일이 벌어지는지를 다룬다 — 뮤텍스를 이미 이해했다면 세마포어는 그 개념의 자연스러운 일반화다.

## 왜 "한 명만"이 아니라 "N명까지"가 필요한가

뮤텍스는 임계 구역에 정확히 한 스레드만 들어가게 강제한다. 하지만 실무에서는 "동시에 최대 N개까지만 허용"해야 하는 상황이 더 흔하다. 데이터베이스 커넥션 풀이 대표적이다 — 커넥션을 무제한으로 열면 데이터베이스 서버가 감당하지 못하므로, "최대 10개 커넥션까지만 동시 사용 허용"이라는 제약을 걸어야 한다. 뮤텍스로는 이 제약을 표현할 수 없다. 값이 0과 1 사이만 오가기 때문이다.

<strong>세마포어(Semaphore)</strong>는 이 문제를 위해 1965년 에츠허르 데이크스트라(Edsger Dijkstra)가 고안한 동기화 도구로, 내부에 음수가 아닌 정수 카운트를 갖는다. 스레드가 자원을 쓰려면 `wait`(또는 `P` 연산, POSIX에서는 `sem_wait`)를 호출해 카운트를 1 감소시키고, 카운트가 이미 0이면 다른 스레드가 `signal`(`V` 연산, `sem_post`)로 카운트를 늘릴 때까지 대기한다. 카운트의 초기값이 곧 "동시에 몇 개까지 허용할지"를 결정한다 — 초기값을 1로 두면 뮤텍스와 동일하게 동작하므로, 뮤텍스는 세마포어의 특수한 경우(**이진 세마포어**)로 볼 수 있다.

```c
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define POOL_SIZE 3
#define NUM_WORKERS 6

sem_t pool_slots;   /* 커넥션 풀의 빈 슬롯 수를 표현하는 세마포어 */

void *use_connection(void *arg) {
    long id = (long)arg;

    sem_wait(&pool_slots);   /* 슬롯을 하나 점유(카운트 -1), 없으면 대기 */
    printf("worker %ld: 커넥션 획득, 작업 중...\n", id);
    /* 커넥션을 사용하는 작업 구간 */
    printf("worker %ld: 커넥션 반납\n", id);
    sem_post(&pool_slots);   /* 슬롯 반납(카운트 +1) */

    return NULL;
}

int main(void) {
    pthread_t workers[NUM_WORKERS];

    sem_init(&pool_slots, 0, POOL_SIZE);   /* 두 번째 인자 0: 프로세스 내 스레드 간 공유 */

    for (long i = 0; i < NUM_WORKERS; i++) {
        pthread_create(&workers[i], NULL, use_connection, (void *)i);
    }
    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_join(workers[i], NULL);
    }

    sem_destroy(&pool_slots);
    return 0;
}
```

`gcc -pthread semaphore_pool.c -o semaphore_pool`로 컴파일해 실행하면, 6개 워커 중 항상 최대 3개만 "커넥션 획득" 상태에 동시에 있고 나머지는 슬롯이 반납될 때까지 대기한다. 세마포어의 카운트는 뮤텍스처럼 "누가 락을 쥐고 있는지"를 추적하지 않고 "남은 슬롯 수"만 추적한다는 점이 중요하다 — 그래서 락을 건 스레드가 아닌 다른 스레드가 `sem_post`를 호출해도 문제가 없고, 이 특성은 생산자-소비자 패턴에서 "빈 슬롯 수"와 "채워진 슬롯 수"를 각각 별도의 세마포어로 표현하는 데 활용된다.

## 모니터: 락과 조건 변수를 한데 묶기

세마포어는 강력하지만, `wait`/`signal` 호출을 어디에 놓을지 프로그래머가 직접 관리해야 하므로 실수하기 쉽다. <strong>모니터(Monitor)</strong>는 이 관리를 언어·런타임 수준으로 끌어올린 고수준 동기화 도구로, 1974년 토니 호어(C. A. R. Hoare)와 1975년 퍼 브린치 한센(Per Brinch Hansen)이 독립적으로 정식화했다. 모니터는 공유 데이터, 그 데이터를 다루는 메서드, 그리고 그 메서드들을 감싸는 락을 하나의 단위로 캡슐화한다 — 모니터 안의 메서드는 항상 한 스레드만 실행할 수 있고, 메서드가 끝나면 락이 자동으로 풀린다.

모니터는 여기에 더해 <strong>조건 변수(Condition Variable)</strong>를 제공해 "지금은 조건이 안 맞으니 기다렸다가, 조건이 맞춰지면 다시 검사"하는 패턴을 표현한다. POSIX의 `pthread_mutex_t` + `pthread_cond_t` 조합이 모니터의 대표적인 구현이고, Java의 `synchronized` 키워드와 `wait()`/`notify()`도 같은 개념을 언어 문법으로 내장한 것이다.

```c
#include <pthread.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;
int queue_size = 0;

void enqueue_item(void) {
    pthread_mutex_lock(&lock);      /* 모니터 진입: 락 획득 */
    queue_size++;
    pthread_cond_signal(&not_empty); /* 대기 중인 소비자 하나를 깨움 */
    pthread_mutex_unlock(&lock);
}

void dequeue_item(void) {
    pthread_mutex_lock(&lock);
    while (queue_size == 0) {
        /* 조건이 거짓이면 락을 풀고 대기, 깨어나면 락을 다시 잡고 재검사 */
        pthread_cond_wait(&not_empty, &lock);
    }
    queue_size--;
    pthread_mutex_unlock(&lock);
}
```

`pthread_cond_wait`는 대기에 들어가는 순간 락을 자동으로 풀고, 깨어날 때 락을 다시 잡는다는 점이 핵심이다 — 이 원자적 처리가 없으면 "락을 푼 직후, 대기에 들어가기 직전" 사이의 틈에서 신호를 놓치는 버그(lost wakeup)가 생긴다. `if`가 아니라 `while`로 조건을 재검사하는 이유는 **가짜 기상(Spurious Wakeup)** 때문이다 — 신호가 없었는데도 대기 스레드가 깨어날 수 있어, 깨어난 직후 조건을 다시 확인하지 않으면 조건이 거짓인 채로 진행해버릴 수 있다.

| 항목 | 세마포어 | 모니터(뮤텍스+조건 변수) |
|---|---|---|
| 핵심 상태 | 정수 카운트 | 락 상태 + 조건 큐 |
| "누가 풀었는지" 추적 | 안 함(카운트만 관리) | 락 소유자 개념 있음 |
| 동시 진입 허용 수 | 카운트로 N개까지 표현 가능 | 기본은 1개(추가 카운트 필요 시 직접 구현) |
| 대표 API | `sem_wait`/`sem_post` | `pthread_mutex_lock/unlock` + `pthread_cond_wait/signal` |
| 대표 활용 | 커넥션 풀, 리소스 제한 | 생산자-소비자 큐, 상태 기반 대기 |

## 흔한 오개념

**"세마포어는 뮤텍스보다 항상 안전하다"** — 세마포어의 카운트는 소유권 개념이 없어서, 락을 걸지 않은 스레드가 실수로 `sem_post`를 두 번 호출해도 컴파일러나 런타임이 막지 못한다. 이 경우 카운트가 실제 자원 수보다 많아져 허용 한도를 넘는 동시 접근이 생길 수 있다. 뮤텍스는 (구현에 따라) 락을 건 스레드만 풀 수 있도록 강제하는 경우가 많아 이런 실수를 방지하는 데는 오히려 더 유리하다.

**"조건 변수는 조건을 직접 저장한다"** — `pthread_cond_t`는 조건 자체를 갖고 있지 않고, 단지 "이 조건과 관련된 대기 스레드들을 깨우는 신호 채널"일 뿐이다. 실제 조건(`queue_size == 0` 같은)은 항상 락으로 보호되는 별도의 변수로 프로그래머가 직접 관리해야 하고, 조건 검사는 항상 락을 쥔 상태에서 이뤄져야 한다.

## 다른 개념과의 연결

[레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 다룬 뮤텍스는 이 챕터에서 세마포어의 카운트가 1인 특수 사례이자, 모니터를 구성하는 두 요소 중 하나로 다시 등장했다. 다음 챕터에서는 뮤텍스와 세마포어처럼 스레드를 아예 대기시키는 대신, 락 없이 하드웨어 수준에서 값을 원자적으로 바꾸는 CAS(Compare-And-Swap) 기법을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 세마포어의 카운트가 뮤텍스의 0/1 값을 어떻게 일반화하는지 설명할 수 있다. 커넥션 풀처럼 "동시에 N개까지 허용"해야 하는 상황에 세마포어를 적용할 수 있다. 모니터가 락과 조건 변수를 캡슐화하는 방식과, `while`로 조건을 재검사해야 하는 이유(가짜 기상)를 설명할 수 있다.

## 참고 자료

> Hoare, C. A. R. (1974). "Monitors: An Operating System Structuring Concept". *Communications of the ACM*, 17(10), 549–557.

- [POSIX.1-2017: semaphore.h](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/semaphore.h.html) — POSIX 세마포어 API 표준 정의
- [Dijkstra, E. W. (1968). "Cooperating Sequential Processes" (EWD123)](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html) — 세마포어를 최초로 정식화한 원문 노트
