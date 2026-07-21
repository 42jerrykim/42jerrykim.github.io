---
image: "wordcloud.png"
slug: atomic-operations-and-cas
collection_order: 76
draft: false
title: "[Computer Terms] 원자적 연산과 CAS (Atomic Operations, Compare-And-Swap)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "CAS는 스레드를 대기시키는 뮤텍스와 달리, 락 없이 하드웨어 수준에서 예상값과 같으면 새 값으로 교체하는 lock-free 기법입니다. C11 stdatomic.h 코드로 재시도 루프 구조와 weak/strong 차이를 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Synchronization
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
- Performance(성능)
- Memory-Order
- Hardware(하드웨어)
- Operating-System(운영체제)
---

## 이 장을 읽기 전에

[레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 다룬 뮤텍스와 [세마포어와 모니터](/post/computerterms/semaphores-and-monitors/)에서 다룬 세마포어는 모두 "조건이 안 맞으면 스레드를 재우고 기다리게 한다"는 공통점이 있다. 이 챕터는 그 대기 자체를 없애고, 하드웨어가 보장하는 원자성만으로 동기화를 해결하는 접근을 다룬다.

## 락이 스레드를 재우는 대가

뮤텍스로 임계 구역을 보호하면 다른 스레드는 락이 풀릴 때까지 잠들거나(운영체제 스케줄러가 개입) 스핀하며 대기한다. 이 대기에는 비용이 따른다 — 스레드를 재우고 깨우는 컨텍스트 스위칭 비용, 그리고 락을 쥔 스레드가 어떤 이유로든 오래 지연되면(스케줄링 지연, 페이지 폴트) 나머지 스레드 전체가 함께 멈추는 문제다. `counter++`처럼 아주 짧은 연산 하나를 보호하기 위해 락 전체를 걸고 대기 큐를 관리하는 것은 과할 수 있다.

<strong>원자적 연산(Atomic Operation)</strong>은 "읽기-수정-쓰기"처럼 여러 단계로 나뉘는 연산을 CPU가 **더 이상 쪼갤 수 없는 단일 단계**로 실행하도록 보장하는 하드웨어 기능이다. 다른 스레드는 이 연산이 절반만 끝난 중간 상태를 절대 관찰할 수 없다. <strong>CAS(Compare-And-Swap)</strong>는 원자적 연산 중 가장 널리 쓰이는 것으로, "메모리의 현재 값이 예상값(expected)과 같으면 새 값(desired)으로 바꾸고, 다르면 아무것도 하지 않은 채 실제 값을 알려준다"는 동작을 원자적으로 수행한다. 이 하나의 명령으로 "내가 마지막으로 읽은 값이 그 사이에 바뀌지 않았는가"를 검증하면서 동시에 갱신까지 끝낼 수 있다.

```c
#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>

atomic_long counter = 0;

void *increment_lockfree(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        long expected = atomic_load(&counter);
        long desired;
        do {
            desired = expected + 1;
            /* expected와 counter의 실제 값이 같으면 desired로 교체하고 true 반환.
               다르면(다른 스레드가 먼저 바꿨으면) expected를 실제 값으로 갱신하고 false 반환 */
        } while (!atomic_compare_exchange_weak(&counter, &expected, desired));
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment_lockfree, NULL);
    pthread_create(&t2, NULL, increment_lockfree, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("counter = %ld (기대값: 2000000)\n", counter);
    return 0;
}
```

`gcc -std=c11 -pthread cas_counter.c -o cas_counter`로 컴파일해 실행하면 락 없이도 항상 정확히 2,000,000이 나온다. `atomic_compare_exchange_weak`가 실패하면(다른 스레드가 그 사이 값을 바꿨으면) `expected`가 실제 값으로 자동 갱신되므로, `do-while` 루프는 그 새 값을 기준으로 `desired`를 다시 계산해 재시도한다. 이 **"읽고 계산하고, 그 사이 안 바뀌었으면 반영, 바뀌었으면 재시도"** 패턴이 CAS 기반 lock-free 프로그래밍의 기본 골격이다.

## 왜 "약한(weak)" CAS인가

`stdatomic.h`는 `atomic_compare_exchange_weak`와 `atomic_compare_exchange_strong` 두 버전을 제공한다. weak 버전은 실제로 값이 같았는데도 아주 드물게 <strong>거짓 실패(Spurious Failure)</strong>를 반환할 수 있다 — 일부 CPU 아키텍처(대표적으로 ARM의 LL/SC 기반 구현)가 값 비교 자체가 아니라 "그 사이 같은 캐시 라인에 다른 간섭이 있었는가"로 성공 여부를 판단하기 때문이다. 이미 루프 안에서 반복 호출하는 경우 weak 버전이 strong 버전보다 빠른 경우가 많아 권장되고, 루프 밖에서 단발로 한 번만 시도해야 하는 상황이라면 strong 버전을 써야 한다.

| 항목 | 뮤텍스 기반 | CAS 기반(lock-free) |
|---|---|---|
| 실패 시 동작 | 스레드를 재우고 대기 | 즉시 재시도(스핀) |
| 컨텍스트 스위칭 | 발생 가능 | 없음 |
| 한 스레드가 지연되면 | 다른 스레드도 함께 멈출 수 있음 | 다른 스레드는 계속 진행 가능 |
| 구현 복잡도 | 상대적으로 단순 | 재시도 루프·ABA 문제 등 고려 필요 |
| 적합한 연산 크기 | 여러 단계로 구성된 임계 구역 | 단일 변수의 짧은 갱신 |

## 흔한 오개념

**"lock-free는 락을 안 쓰니까 항상 더 빠르다"** — 경쟁이 심한 상황(여러 스레드가 같은 변수를 동시에 갱신)에서는 CAS가 계속 실패해 재시도하느라 오히려 CPU 사이클을 낭비할 수 있다. lock-free 기법은 "한 스레드가 멈춰도 시스템 전체는 진행된다"는 **진행 보장(Progress Guarantee)** 측면에서 강점이 있는 것이지, 모든 상황에서 무조건 처리량이 높다는 뜻은 아니다. 실제 성능은 경쟁도·연산 복잡도·CPU 아키텍처에 따라 달라지므로, 벤치마크로 검증하지 않고 단정할 수 없다.

**"CAS가 성공하면 그 사이 값이 안 바뀌었다는 뜻이다"** — CAS는 "메모리의 현재 값이 예상값과 같다"만 확인할 뿐, 그 값이 **그 사이 한 번도 바뀌지 않았다**는 것까지 보장하지는 않는다. 값이 A → B → A로 바뀌었다가 우연히 원래 값으로 되돌아온 경우, CAS는 이를 "변경 없음"으로 착각하고 성공을 반환한다 — 이 현상을 다음 챕터에서 ABA 문제로 다룬다.

## 다른 개념과의 연결

[레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/)에서 다룬 뮤텍스가 "스레드를 재워서" 상호 배제를 만든다면, 이 챕터의 CAS는 하드웨어 원자성만으로 같은 목표를 재시도 루프로 이뤘다는 점이 대비된다. 다음 챕터에서는 이 CAS의 "값이 같으면 안 바뀐 것"이라는 가정이 깨지는 ABA 문제와, 이를 막는 버전 태그 기법을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. CAS가 "예상값과 같으면 교체"를 원자적으로 수행하는 원리와, 이를 락 없이 반복 재시도해 동시성을 보장하는 루프 구조를 설명할 수 있다. weak CAS와 strong CAS의 차이와 각각을 쓰는 상황을 구분할 수 있다. lock-free가 항상 더 빠르지는 않은 이유를 경쟁 상황과 연결해 설명할 수 있다.

## 참고 자료

> ISO/IEC 9899:2011 (C11), §7.17.7.4 "The atomic_compare_exchange generic functions".

- [cppreference: atomic_compare_exchange_weak, atomic_compare_exchange_strong](https://en.cppreference.com/w/c/atomic/atomic_compare_exchange) — C11 CAS API 상세 및 weak/strong 차이
- [x86 and amd64 instruction reference: CMPXCHG](https://www.felixcloutier.com/x86/cmpxchg) — Intel SDM 기반으로 정리된, CAS를 구현하는 실제 CPU 명령어(x86 CMPXCHG) 명세
