---
image: "wordcloud.png"
slug: arrays-and-linked-lists
collection_order: 6
draft: false
title: "[Computer Terms] 배열과 연결리스트 (Array, Linked List)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "배열과 연결리스트는 데이터를 순서대로 저장하는 가장 기초적인 두 자료구조입니다. 메모리 레이아웃 차이가 접근·삽입·삭제 성능과 캐시 지역성에 미치는 영향을 C 코드와 함께 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Array(배열)
- Linked-List(연결리스트)
- Memory(메모리)
- Pointer(포인터)
- C
- Time-Complexity(시간복잡도)
- Cache-Locality(캐시지역성)
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

## 왜 배열과 연결리스트부터인가

스택·큐·트리·해시테이블처럼 이후에 다룰 자료구조는 모두 내부적으로 배열 또는 연결리스트, 혹은 둘의 조합으로 구현된다. 파이썬의 `list`는 동적 배열이고, `collections.deque`는 이중 연결리스트에 가깝다. 즉 두 자료구조의 메모리 레이아웃 차이를 이해하지 못하면, 상위 자료구조를 골라 쓸 때 "왜 이 연산은 빠르고 저 연산은 느린가"를 설명할 수 없다. 이 챕터는 그 판단 근거가 되는 메모리 레이아웃 차이를 코드 수준에서 다룬다.

## 배열의 정의와 특성

**배열(Array)**은 동일한 크기의 원소들을 메모리상에 **연속된 공간**에 나열해 저장하는 자료구조다. 원소의 시작 주소와 인덱스, 원소 크기만 알면 `주소 = 시작주소 + 인덱스 × 원소크기` 공식으로 어떤 위치든 곧바로 계산해 접근할 수 있다. 이 성질을 **임의 접근(Random Access)**이라 하며, 배열이 인덱스 접근에서 O(1)을 보장하는 이유다.

반면 배열은 생성 시점에 크기를 고정해야 한다는 제약이 있다. C의 정적 배열(`int arr[10]`)이 대표적이며, 크기를 넘어서는 원소를 추가하려면 더 큰 메모리 블록을 새로 할당하고 기존 원소를 전부 복사해야 한다. 파이썬 `list`나 C++ `std::vector` 같은 **동적 배열**은 이 재할당을 내부에서 자동으로 처리해, 사용자에게는 크기 제약이 없는 것처럼 보이게 한다.

## 연결리스트의 정의와 특성

**연결리스트(Linked List)**는 각 원소(노드)가 데이터와 함께 **다음 노드를 가리키는 포인터**를 갖는 자료구조다. 노드들이 메모리상에서 연속될 필요가 없으므로, 중간에 원소를 추가·삭제할 때 뒤쪽 원소들을 옮길 필요가 없다 — 앞뒤 노드의 포인터만 바꾸면 된다. 다만 특정 인덱스의 원소에 접근하려면 첫 노드부터 포인터를 따라가며 순회해야 하므로, 임의 접근은 O(n)이다.

다음은 단일 연결리스트에 노드를 앞쪽에 삽입하고 전체를 순회하는 최소 구현이다. 배열이었다면 삽입 시 기존 원소를 한 칸씩 밀어야 하지만, 연결리스트는 새 노드의 `next`가 기존 head를 가리키게 한 뒤 head를 갱신하기만 하면 된다.

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node *push_front(Node *head, int value) {
    Node *node = malloc(sizeof(Node));
    node->data = value;
    node->next = head;      /* 새 노드가 기존 head를 가리킴 */
    return node;             /* 새 노드가 새로운 head */
}

void print_list(const Node *head) {
    for (const Node *cur = head; cur != NULL; cur = cur->next) {
        printf("%d -> ", cur->data);
    }
    printf("NULL\n");
}

void free_list(Node *head) {
    while (head != NULL) {
        Node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    Node *head = NULL;
    for (int i = 3; i >= 1; i--) {
        head = push_front(head, i);
    }
    print_list(head);   /* 1 -> 2 -> 3 -> NULL */
    free_list(head);
    return 0;
}
```

`push_front`는 리스트 길이와 무관하게 항상 O(1)이다. 반대로 같은 위치 삽입을 배열로 구현했다면, 기존 원소를 전부 한 칸씩 뒤로 옮기는 O(n) 연산이 필요하다. 이 코드는 `gcc -std=c11 -Wall linked_list.c -o linked_list`로 그대로 컴파일·실행할 수 있다.

## 비교: 무엇이 다르고, 언제 무엇을 쓰는가

| 연산/특성 | 배열 | 연결리스트 |
|---|---|---|
| 인덱스 접근 | O(1) | O(n) |
| 앞쪽 삽입/삭제 | O(n) (원소 이동) | O(1) |
| 임의 위치 삽입/삭제 | O(n) | O(1) (단, 위치를 찾는 순회는 O(n)) |
| 메모리 지역성(Cache Locality) | 높음 — 연속 메모리라 캐시 라인에 다음 원소가 이미 적재됨 | 낮음 — 노드가 메모리 곳곳에 흩어져 포인터를 따라갈 때마다 캐시 미스 가능 |
| 메모리 오버헤드 | 원소 크기만 사용 | 원소마다 포인터(8바이트, 64비트 기준) 추가 |

이 표에서 가장 실무 판단에 영향을 주는 항목은 **메모리 지역성**이다. Big-O만 보면 연결리스트의 삽입이 항상 유리해 보이지만, 실제 실행 시간은 캐시 미스 비용까지 포함한다. 원소 수가 수만 개 이하로 작고 삽입·삭제보다 순회·탐색이 잦은 경우, 이론상 O(n) 삽입인 동적 배열이 캐시 지역성 덕분에 연결리스트보다 실측 성능이 더 좋은 경우가 흔하다.

## 흔한 오개념

**"연결리스트는 삽입이 항상 배열보다 빠르다"** — 삽입 위치까지 도달하는 순회 비용을 빼먹은 채 삽입 자체의 O(1)만 보고 판단하는 오해다. 정렬된 위치에 삽입해야 하는 경우, 순회(O(n)) + 삽입(O(1))으로 총 비용은 배열과 다르지 않다. 연결리스트가 진짜 유리한 경우는 **위치를 이미 포인터로 들고 있을 때**(예: 반복자·큐의 head/tail)뿐이다.

**"동적 배열은 크기를 늘릴 때마다 O(n) 복사가 일어나므로 항상 느리다"** — `std::vector`나 파이썬 `list`는 용량이 부족할 때 현재 크기의 1.5~2배로 확장한다. 이 **상환 분석(Amortized Analysis)** 덕분에 `push_back`/`append`는 평균적으로 O(1)이다. 매 원소 추가마다 정확히 1칸씩 늘리는 구현이 아니라면 이 오해는 성립하지 않는다.

## 다른 개념과의 연결

배열은 뒤에서 다룰 **해시테이블**의 버킷 저장소로, 연결리스트는 **스택·큐**의 내부 구현과 **그래프의 인접 리스트(Adjacency List)** 표현으로 그대로 재사용된다. 시간·공간 복잡도 표기는 [시간 복잡도](/post/computerterms/time-complexity/) 챕터의 빅오 표기법을 그대로 사용하므로, 이 챕터를 먼저 읽지 않았다면 함께 참고하면 좋다. 다음 챕터에서는 배열/연결리스트 위에서 **후입선출·선입선출** 접근 순서를 강제하는 스택과 큐를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 배열과 연결리스트 중 어떤 자료구조가 특정 연산(인덱스 접근, 앞쪽 삽입, 정렬 위치 삽입)에 유리한지 이유와 함께 설명할 수 있다. "빅오가 낮으니 무조건 빠르다"는 판단이 캐시 지역성을 무시한 결과일 수 있음을 설명할 수 있다. 동적 배열의 상환 분석 개념으로 `append`/`push_back`이 평균 O(1)인 이유를 설명할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 10: Elementary Data Structures. MIT Press.

- [cppreference: std::vector](https://en.cppreference.com/w/cpp/container/vector) — 동적 배열의 상환 분석과 재할당 정책 상세
- [Python docs: list vs collections.deque](https://docs.python.org/3/library/collections.html#collections.deque) — 리스트(동적 배열)와 deque(이중 연결리스트)의 성능 특성 비교
