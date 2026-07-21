---
image: "wordcloud.png"
slug: stacks-and-queues
collection_order: 7
draft: false
title: "[Computer Terms] 스택과 큐 (Stack, Queue)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "스택과 큐는 배열·연결리스트 위에 후입선출·선입선출이라는 접근 순서 제약을 얹은 자료구조입니다. 함수 호출, 되돌리기, 너비 우선 탐색 같은 실제 사용 사례와 함께 C 코드로 구현을 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Stack(스택)
- Queue(큐)
- Array(배열)
- Linked-List(연결리스트)
- Memory(메모리)
- C
- Time-Complexity(시간복잡도)
- Algorithm(알고리즘)
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
- Implementation(구현)
---

## 이 장을 읽기 전에

[배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/) 챕터에서 다룬 두 자료구조의 메모리 레이아웃과 삽입·삭제 비용 차이를 안다고 가정한다. 스택과 큐는 그 위에 **원소를 넣고 뺄 수 있는 위치를 제한**하는 규칙만 얹은 것이므로, 별도의 새 메모리 구조가 아니라 "배열/연결리스트를 어떻게 제약해서 쓰는가"의 문제로 접근한다.

## 스택과 큐를 왜 구분해서 배우는가

배열과 연결리스트는 임의 위치에 접근·삽입·삭제할 수 있는 범용 자료구조다. 하지만 실무의 많은 문제는 임의 접근이 아니라 **정해진 순서로만** 데이터를 넣고 빼는 것으로 충분하다. 함수 호출은 가장 최근에 호출된 함수부터 되돌아가야 하고, 프린터 작업은 먼저 요청한 순서대로 처리돼야 한다. 이런 순서 제약을 자료구조 차원에서 강제하면, 사용하는 쪽에서 "잘못된 위치에 접근하는 버그"를 원천적으로 차단할 수 있다. 스택과 큐는 이 제약을 각각 반대 방향으로 건 것이다.

## 스택: 후입선출 (LIFO)

**스택(Stack)**은 마지막에 넣은 원소가 가장 먼저 나오는 **후입선출(Last-In-First-Out, LIFO)** 구조다. 원소를 넣는 연산을 **push**, 꺼내는 연산을 **pop**이라 하며, 둘 다 한쪽 끝(top)에서만 일어난다. 배열로 구현하면 끝 인덱스에서만 추가·제거하므로 O(1)이고, 연결리스트로 구현해도 head에서만 추가·제거하므로 마찬가지로 O(1)이다 — 스택은 배열과 연결리스트 둘 다 자연스럽게 어울리는 드문 자료구조다.

```c
#include <stdio.h>

#define CAPACITY 100

typedef struct {
    int data[CAPACITY];
    int top;   /* 다음에 push할 위치. top == 0이면 비어 있음 */
} Stack;

void stack_init(Stack *s) {
    s->top = 0;
}

int stack_push(Stack *s, int value) {
    if (s->top >= CAPACITY) return -1;   /* 스택 오버플로 */
    s->data[s->top++] = value;
    return 0;
}

int stack_pop(Stack *s, int *out) {
    if (s->top == 0) return -1;          /* 스택 언더플로 */
    *out = s->data[--s->top];
    return 0;
}

int main(void) {
    Stack s;
    stack_init(&s);
    stack_push(&s, 1);
    stack_push(&s, 2);
    stack_push(&s, 3);

    int value;
    while (stack_pop(&s, &value) == 0) {
        printf("%d ", value);   /* 3 2 1 : 넣은 순서의 역순 */
    }
    printf("\n");
    return 0;
}
```

함수 호출 스택, 실행 취소(undo), 괄호 짝 검사, 깊이 우선 탐색(DFS)의 명시적 구현이 모두 이 LIFO 규칙 위에서 동작한다.

## 큐: 선입선출 (FIFO)

**큐(Queue)**는 먼저 넣은 원소가 먼저 나오는 **선입선출(First-In-First-Out, FIFO)** 구조다. 넣는 연산을 **enqueue**, 꺼내는 연산을 **dequeue**라 하며, 삽입은 뒤쪽(rear)에서, 삭제는 앞쪽(front)에서 일어난다. 여기서 배열 구현은 스택만큼 단순하지 않다 — 앞쪽에서 계속 꺼내면 배열 앞부분에 빈 공간이 쌓이는데, 이 공간을 재사용하지 않으면 뒤쪽 인덱스가 금방 배열 끝에 도달해버린다.

이 문제를 푸는 표준 해법이 **원형 큐(Circular Queue)**다. 인덱스가 배열 끝에 도달하면 나머지 연산(`% CAPACITY`)으로 다시 처음으로 돌아가게 해서, 빈 공간을 계속 재사용한다.

```c
#include <stdio.h>

#define CAPACITY 5

typedef struct {
    int data[CAPACITY];
    int front;
    int count;   /* 현재 원소 개수. rear는 front + count로 계산 가능 */
} CircularQueue;

void queue_init(CircularQueue *q) {
    q->front = 0;
    q->count = 0;
}

int queue_enqueue(CircularQueue *q, int value) {
    if (q->count == CAPACITY) return -1;              /* 큐가 가득 참 */
    int rear = (q->front + q->count) % CAPACITY;
    q->data[rear] = value;
    q->count++;
    return 0;
}

int queue_dequeue(CircularQueue *q, int *out) {
    if (q->count == 0) return -1;                     /* 큐가 비어 있음 */
    *out = q->data[q->front];
    q->front = (q->front + 1) % CAPACITY;
    q->count--;
    return 0;
}

int main(void) {
    CircularQueue q;
    queue_init(&q);
    queue_enqueue(&q, 1);
    queue_enqueue(&q, 2);
    queue_enqueue(&q, 3);

    int value;
    while (queue_dequeue(&q, &value) == 0) {
        printf("%d ", value);   /* 1 2 3 : 넣은 순서 그대로 */
    }
    printf("\n");
    return 0;
}
```

`front`와 `count`만으로 `rear` 위치를 계산해 별도 변수를 두지 않았다. 원형 큐 없이 배열 인덱스를 단순 증가만 시키는 구현은 dequeue를 반복할수록 사용 가능한 공간이 줄어드는 버그로 이어지기 쉽다 — "왜 큐가 꽉 찼다고 나오지?"라는 흔한 질문의 원인이 대개 여기 있다.

## 비교: 무엇이 다르고, 언제 무엇을 쓰는가

| 특성 | 스택 (LIFO) | 큐 (FIFO) |
|---|---|---|
| 삽입·삭제 위치 | 한쪽 끝(top) | 양쪽 끝(rear에 삽입, front에서 삭제) |
| 배열 구현 난이도 | 단순 (끝 인덱스만 관리) | 원형 큐 필요 (앞쪽 공간 재사용) |
| 대표 활용 | 함수 호출, undo, 괄호 검사, DFS | 작업 대기열, 프린터 스풀, BFS, 메시지 큐 |
| 접근 순서 | 최근 것부터 | 오래된 것부터 |

## 흔한 오개념

**"큐는 배열로 구현하면 무조건 비효율적이다"** — 원형 큐 없이 매번 배열을 앞으로 당기는(shift) 구현만 놓고 판단한 오해다. 원형 큐로 구현하면 enqueue/dequeue 모두 O(1)이며, 고정 용량이 허용되는 상황(예: 링 버퍼 기반 네트워크 패킷 큐)에서는 연결리스트 기반 큐보다 캐시 지역성이 좋아 실측 성능이 더 나은 경우가 많다.

**"재귀 함수는 스택을 안 쓴다"** — 재귀 호출도 내부적으로는 각 호출의 지역 변수와 복귀 주소를 **호출 스택(Call Stack)**에 push하고, 함수가 반환할 때 pop하는 것과 동일하다. 재귀 깊이가 과도하면 스택 오버플로가 나는 이유가 바로 이 호출 스택이 유한한 메모리를 쓰기 때문이다. 이 챕터의 스택 예제 코드는 이 호출 스택을 사용자 데이터 구조로 명시적으로 흉내 낸 것이다.

## 다른 개념과의 연결

큐는 다음에 다룰 **트리**의 너비 우선 순회(BFS)에서, 스택은 트리의 깊이 우선 순회(DFS)의 반복문 구현에서 그대로 재사용된다. 두 자료구조 모두 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)에서 다룬 임의 접근 vs 삽입·삭제 비용 트레이드오프가 "어느 쪽 구현을 고를 것인가"의 판단 기준이 된다. 다음 챕터에서는 계층 구조를 표현하는 **트리**를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 스택과 큐 중 어느 쪽이 특정 문제(실행 취소, 작업 대기열, 너비/깊이 우선 탐색)에 맞는지 이유와 함께 선택할 수 있다. 원형 큐가 필요한 이유와, 원형 큐 없이 배열로 큐를 구현했을 때 발생하는 문제를 설명할 수 있다. 함수 호출 스택과 사용자 정의 스택 자료구조가 같은 원리로 동작함을 설명할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Section 10.1: Stacks and queues. MIT Press.

- [cppreference: std::stack](https://en.cppreference.com/w/cpp/container/stack), [std::queue](https://en.cppreference.com/w/cpp/container/queue) — 컨테이너 어댑터로 구현된 실제 표준 라이브러리 설계
- [Python docs: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque) — 양쪽 끝에서 모두 O(1) 삽입·삭제를 지원하는 이중 연결리스트 기반 구현
