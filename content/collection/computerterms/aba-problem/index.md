---
image: "wordcloud.png"
slug: aba-problem
collection_order: 79
draft: false
title: "[Computer Terms] ABA 문제 (ABA Problem)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "ABA 문제는 값이 A에서 B를 거쳐 다시 A로 돌아왔을 때, CAS가 그 사이 변경이 전혀 없었다고 착각하는 현상입니다. lock-free 스택이 포인터 재사용으로 깨지는 시나리오와, 버전 태그·해저드 포인터로 막는 방법을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Concurrency(동시성)
- Synchronization
- Lock(락)
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
- Hazard-Pointer
- Stack(스택)
- Operating-System(운영체제)
---

## 이 장을 읽기 전에

[원자적 연산과 CAS](/post/computerterms/atomic-operations-and-cas/)에서 CAS가 "메모리의 현재 값이 예상값과 같으면 새 값으로 교체한다"고 다뤘고, 그 챕터 말미에서 "값이 같다"는 것이 "그 사이 한 번도 안 바뀌었다"는 뜻은 아니라고 예고했다. 이 챕터는 그 간극이 실제로 어떤 문제를 만드는지, 그리고 어떻게 막는지를 다룬다.

## "같으면 안 바뀐 것"이라는 가정이 깨지는 순간

CAS는 딱 한 가지만 확인한다 — 지금 이 순간 메모리의 값이 내가 예상한 값과 **같은가**. 그 값이 처음 읽은 이후로 **줄곧 그대로였는가**는 확인하지 않는다. 어떤 스레드가 값 A를 읽은 뒤, 다른 스레드들이 그 값을 A에서 B로 바꿨다가 다시 A로 되돌려놓으면, 원래 스레드가 뒤늦게 CAS를 실행할 때 메모리 값은 여전히 A이므로 CAS는 성공한다. 하지만 그 사이에 값이 두 번 바뀌었다는 사실은 완전히 사라졌다 — 이 현상을 <strong>ABA 문제(ABA Problem)</strong>라 부른다.

값 자체(정수 카운터 등)만 다루는 경우라면 A로 돌아왔다는 것이 "결과적으로 같은 상태"이므로 큰 문제가 되지 않을 때가 많다. 문제는 그 값이 **포인터**일 때다. lock-free 스택에서 포인터가 가리키던 노드가 한 번 pop되어 메모리가 해제(또는 재사용)됐다가, 우연히 같은 주소에 새 노드가 다시 할당되면 포인터 값(주소)은 A로 똑같이 보이지만 실제로는 완전히 다른 데이터를 가리키는 노드가 되어버린다.

```c
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

atomic_uintptr_t top = 0;   /* lock-free 스택의 top 포인터(주소값으로 다룸) */

void push(int value) {
    Node *n = malloc(sizeof(Node));
    n->value = value;
    uintptr_t old_top;
    do {
        old_top = atomic_load(&top);
        n->next = (Node *)old_top;
        /* top이 여전히 old_top이면 n으로 교체 */
    } while (!atomic_compare_exchange_weak(&top, &old_top, (uintptr_t)n));
}

Node *pop(void) {
    uintptr_t old_top;
    Node *next;
    do {
        old_top = atomic_load(&top);
        if (old_top == 0) return NULL;
        next = ((Node *)old_top)->next;   /* 위험 지점: old_top이 이미 free된 뒤라면? */
        /* top이 여전히 old_top이면 next로 교체 */
    } while (!atomic_compare_exchange_weak(&top, &old_top, (uintptr_t)next));
    return (Node *)old_top;
}
```

`pop`이 `old_top`을 읽고 `next`를 계산하는 사이, 다른 스레드가 이 노드를 pop해 `free`한 뒤 같은 주소에 새 노드를 `malloc`해 다시 push하면, 원래 스레드가 나중에 실행하는 CAS는 "top이 여전히 old_top(같은 주소)"이라고 착각해 성공해버린다. 하지만 `next`는 이미 해제된 옛 노드의 `next` 필드를 읽어 계산한 값이라 스택의 실제 구조와 어긋나고, 이후 스택은 잘못된 노드를 가리키거나 이미 반환된 노드를 다시 가리키는 상태로 망가질 수 있다. 이 시나리오는 스레드 스케줄링 타이밍에 좌우되어 재현이 매우 어렵고, 발생하더라도 즉시 크래시하지 않고 한참 뒤에 다른 증상으로 나타나는 경우가 많아 디버깅이 특히 까다롭다.

## 버전 태그로 "몇 번째 A인지" 구분하기

가장 널리 쓰이는 예방책은 포인터 값 옆에 <strong>버전 카운터(태그)</strong>를 함께 두어, "값이 A"뿐 아니라 "몇 번째로 A가 되었는지"까지 CAS로 비교하는 것이다. 포인터를 바꿀 때마다 버전 번호도 함께 1씩 증가시키면, 값이 A → B → A로 돌아와도 버전 번호는 계속 증가한 상태이므로 CAS는 이를 "다른 상태"로 정확히 구분한다. x86-64에서는 128비트 CAS(`CMPXCHG16B`)로 64비트 포인터와 64비트 버전을 한 번에 원자적으로 비교·교체하는 방식이 흔히 쓰이고, 언어·플랫폼에 따라 지원 여부와 성능이 다르므로 실제 채택 전에는 대상 환경에서 확인이 필요하다.

또 다른 접근은 노드를 **즉시 해제하지 않는** 것이다. <strong>해저드 포인터(Hazard Pointer)</strong>나 **RCU**(Read-Copy-Update) 같은 메모리 회수 기법은 어떤 스레드가 아직 접근 중일 수 있는 노드를 안전하다고 확인될 때까지 `free`를 미룬다 — 노드가 재사용되지 않으면 애초에 "같은 주소에 다른 노드"라는 상황 자체가 생기지 않는다. 언어 차원에서 가비지 컬렉터가 메모리를 관리하는 Java나 Go 같은 환경에서는 살아있는 참조가 있는 객체를 회수하지 않으므로 ABA 문제가 원천적으로 크게 완화된다는 점도 이 기법과 같은 원리다.

| 접근 | 방식 | 대가 |
|---|---|---|
| 버전 태그(Tagged Pointer) | 값+버전을 하나의 CAS로 비교 | 더 넓은 CAS 폭(예: 128비트) 필요 |
| 해저드 포인터 | 접근 중인 노드의 회수를 지연 | 스레드마다 추적 구조·검사 비용 |
| RCU | 읽기 경로는 락 없이, 회수는 유예 구간 이후 | 회수 지연으로 메모리 사용량 증가 |
| GC 언어(Java, Go 등) | 참조가 있는 객체는 회수 안 됨 | 언어 런타임 전체의 GC 비용 |

## 흔한 오개념

**"주소가 같으면 같은 객체다"** — 이 챕터의 핵심이 바로 이 가정이 깨진다는 것이다. 메모리 할당자는 해제된 블록을 자유롭게 재사용하므로, 같은 주소가 시간이 지나 완전히 다른 객체를 가리키는 것은 정상적인 동작이다. lock-free 자료구조를 다룰 때는 "포인터 값이 같다"와 "같은 논리적 상태다"를 항상 구분해서 생각해야 한다.

**"ABA 문제는 이론적인 이야기일 뿐 실제로는 잘 안 일어난다"** — 발생 확률이 낮아 보이는 것과 무관하게, 실제로 발생하면 데이터 구조가 조용히 깨지고 한참 뒤에야 관계없어 보이는 증상으로 나타나는 경우가 많아 원인 추적이 특히 어렵다. 메모리 할당자가 방금 해제한 블록을 즉시 재사용하는 경향이 있는 환경(할당 패턴이 반복적인 서버 워크로드 등)에서는 이 확률이 결코 무시할 수준이 아니며, lock-free 자료구조 라이브러리들이 예외 없이 버전 태그나 해저드 포인터 같은 방어 기법을 포함하는 이유이기도 하다.

## 다른 개념과의 연결

[원자적 연산과 CAS](/post/computerterms/atomic-operations-and-cas/)에서 다룬 "예상값과 같으면 교체"라는 CAS의 핵심 동작이, 값의 동일성만으로는 상태 변화 이력을 구분할 수 없다는 이 챕터의 한계로 이어진다. [스레드풀](/post/computerterms/thread-pools/)에서 다룬 작업 큐를 뮤텍스 대신 lock-free 큐로 구현한다면, 그 큐의 포인터 조작 역시 이 챕터의 ABA 문제를 그대로 마주하게 된다. 동시성 갈래는 이 챕터로 마무리되며, 이후 챕터들은 캐싱으로 이어진다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. CAS가 "값이 같다"만 확인하고 "변경 이력이 없다"는 보장하지 않는다는 점을 값이 A→B→A로 순환하는 시나리오로 설명할 수 있다. ABA 문제가 lock-free 스택 같은 포인터 기반 자료구조에서 실제로 어떤 손상을 일으키는지 설명할 수 있다. 버전 태그와 해저드 포인터가 각각 어떤 방식으로 ABA 문제를 막는지 구분해 설명할 수 있다.

## 참고 자료

> IBM. (1983). *IBM System/370 Extended Architecture, Principles of Operation*. IBM Corporation. (Compare Double and Swap 명령을 통해 이중 워드 비교·교체로 ABA 문제를 완화하는 초기 하드웨어 지원 사례)

- [Michael, M. M. (2004). "Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects"](https://ieeexplore.ieee.org/document/1291819). *IEEE Transactions on Parallel and Distributed Systems*, 15(6) — 해저드 포인터를 정식화한 원 논문
- [cppreference: std::atomic — ABA problem](https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange) — C++ 표준 라이브러리 문서의 CAS 및 ABA 관련 설명
