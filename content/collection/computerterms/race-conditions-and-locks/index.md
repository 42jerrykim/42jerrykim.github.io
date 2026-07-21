---
image: "wordcloud.png"
slug: race-conditions-and-locks
collection_order: 20
draft: false
title: "[Computer Terms] 레이스 컨디션과 락 (Race Condition, Lock)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "레이스 컨디션은 여러 스레드가 공유 자원에 동시에 접근할 때 실행 순서에 따라 결과가 달라지는 버그입니다. 뮤텍스로 임계 구역을 보호하는 원리를 C 코드로 재현하고 고쳐봅니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Race-Condition(레이스컨디션)
- Lock(락)
- Mutex(뮤텍스)
- Thread(스레드)
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
- Operating-System(운영체제)
- Advanced
- How-To
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)에서 같은 프로세스의 스레드들이 메모리를 공유한다고 다뤘고, [CPU 스케줄링](/post/computerterms/cpu-scheduling/)에서 여러 실행 흐름이 아주 짧은 간격으로 번갈아 실행된다고 다뤘다. 이 두 사실을 합치면, 한 스레드가 공유 변수를 수정하는 도중 다른 스레드가 끼어들 수 있다는 결론에 이른다 — 이 챕터는 그 끼어듦이 만드는 버그를 다룬다.

## 왜 "동시에 실행"이 위험한가

`counter++`처럼 한 줄로 보이는 코드도 CPU 수준에서는 "값을 읽기 → 1을 더하기 → 다시 쓰기"라는 세 단계로 나뉜다. 두 스레드가 이 세 단계를 겹쳐서 실행하면, 둘 다 같은 옛 값을 읽고 각자 1을 더한 뒤 같은 새 값을 써버려 증가가 한 번만 반영되는 문제가 생긴다. 이렇게 **여러 실행 흐름의 타이밍에 따라 결과가 달라지는 버그**를 **레이스 컨디션(Race Condition)**이라 하고, 이 세 단계처럼 공유 자원에 접근하는 동안 다른 실행 흐름이 끼어들면 안 되는 코드 구간을 **임계 구역(Critical Section)**이라 한다.

```c
#include <stdio.h>
#include <pthread.h>

long counter = 0;

void *increment(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        counter++;   /* 임계 구역: 읽기-더하기-쓰기가 원자적이지 않음 */
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("counter = %ld (기대값: 2000000)\n", counter);
    return 0;
}
```

`gcc -pthread race.c -o race`로 여러 번 실행하면 `counter`가 매번 다른 값(대개 2,000,000보다 작은 값)으로 나온다. 이 코드는 실행할 때마다 스케줄러가 두 스레드를 어떻게 번갈아 실행시키는지에 따라 결과가 달라지므로, "가끔만 재현되는 버그"의 전형이다.

## 뮤텍스로 임계 구역을 보호하기

이 문제를 고치는 표준 도구가 **뮤텍스(Mutex, Mutual Exclusion)**다. 임계 구역에 들어가기 전 락을 걸고, 나올 때 락을 푼다. 다른 스레드가 이미 락을 쥐고 있다면, 락이 풀릴 때까지 대기한다 — 이 대기 덕분에 임계 구역에는 한 번에 한 스레드만 들어갈 수 있다.

```c
#include <stdio.h>
#include <pthread.h>

long counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *increment(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        pthread_mutex_lock(&lock);     /* 임계 구역 진입: 다른 스레드는 여기서 대기 */
        counter++;
        pthread_mutex_unlock(&lock);   /* 임계 구역 탈출: 대기 중인 스레드 하나가 진입 가능 */
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("counter = %ld (기대값: 2000000)\n", counter);   /* 항상 정확히 2000000 */
    return 0;
}
```

`lock`/`unlock` 사이의 `counter++`는 이제 다른 스레드의 간섭 없이 완전히 끝난 뒤에야 다음 스레드가 시작할 수 있으므로, 항상 정확한 값이 나온다. 이 안전성의 대가는 **성능**이다 — 락을 얻기 위한 대기는 스레드를 병렬로 실행하는 이점을 그만큼 깎아 먹는다. 임계 구역을 필요한 만큼만 최소화하는 것(예: 반복문 전체가 아니라 공유 변수 접근 줄만 감싸기)이 실무에서 중요한 이유다.

## 흔한 오개념

**"레이스 컨디션은 테스트하면 잡힌다"** — 레이스 컨디션은 특정 타이밍에서만 재현되므로, 같은 테스트를 여러 번 돌려도 안 보이다가 운영 환경의 다른 CPU·부하 조건에서 갑자기 나타나는 경우가 흔하다. ThreadSanitizer(`-fsanitize=thread`) 같은 동적 분석 도구로 코드 경로 자체를 검사하는 것이, 우연히 재현되길 기다리는 것보다 신뢰할 수 있는 검증 방법이다. 다만 새니타이저가 "이번 실행에서 경고가 없었다"는 것도 "이 코드에 레이스 컨디션이 없다는 증명"은 아니라는 점은 유의해야 한다 — 새니타이저가 관찰한 실행 경로에 문제가 없었을 뿐이다.

**"락을 걸면 무조건 안전하다"** — 락으로 보호해야 할 공유 자원 중 하나라도 빠뜨리면 그 부분에서 여전히 레이스 컨디션이 발생한다. 또한 서로 다른 락을 여러 개 쓰는 코드에서는 락 자체가 다음 챕터에서 다룰 데드락이라는 새로운 문제를 만들 수 있다 — "락을 건다"는 안전의 시작이지 끝이 아니다.

## 다른 개념과의 연결

[CPU 스케줄링](/post/computerterms/cpu-scheduling/)에서 다룬 우선순위 역전은 이 챕터의 뮤텍스 대기가 우선순위와 얽힐 때 발생하는 현상이다. 다음 챕터에서는 락을 여러 개 쓸 때 생기는 또 다른 문제인 데드락을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 레이스 컨디션이 발생하는 조건(공유 자원, 비원자적 연산, 동시 접근)을 설명할 수 있다. 뮤텍스가 임계 구역을 보호하는 원리와, 그 대가로 발생하는 성능 비용을 설명할 수 있다. 테스트만으로 레이스 컨디션을 완전히 검증할 수 없는 이유와, 새니타이저 같은 대안 검증 방법을 설명할 수 있다.

## 참고 자료

> Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.), Chapter 6: Synchronization Tools. Wiley.

- [POSIX Threads Programming: Mutex Variables](https://hpc-tutorials.llnl.gov/posix/mutex_variables/) — pthread 뮤텍스 API 상세
- [ThreadSanitizer documentation](https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual) — 레이스 컨디션을 정적/동적으로 탐지하는 도구 사용법
