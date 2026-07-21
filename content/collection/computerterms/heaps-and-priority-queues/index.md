---
image: "wordcloud.png"
slug: heaps-and-priority-queues
collection_order: 45
draft: false
title: "[Computer Terms] 힙과 우선순위 큐 (Heap, Priority Queue)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "힙은 완전 이진 트리를 배열에 담아 최솟값 삽입·삭제를 O(log n)에 처리하는 자료구조입니다. sift-up/down 원리와 우선순위 큐로서의 쓰임을 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Heap(힙)
- Priority-Queue(우선순위큐)
- Tree(트리)
- Array(배열)
- Binary-Search-Tree(이진탐색트리)
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

[배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)의 배열 인덱스 계산, [트리](/post/computerterms/trees/)의 완전 이진 트리·부모-자식 개념, [그래프](/post/computerterms/graphs/)까지 이어진 자료구조 기초를 안다고 가정한다. 힙은 트리를 배열 하나로 압축해 표현하는 자료구조이므로, "트리인데 왜 배열로 저장하는가"라는 질문에서 출발한다.

## "가장 급한 일부터" 처리하려면

작업 스케줄러가 우선순위가 높은 작업부터 실행하거나, 다익스트라 알고리즘이 현재까지 거리가 가장 짧은 정점부터 확정하는 상황을 생각해보자. 매번 "지금까지 넣은 원소 중 최솟값(또는 최댓값)을 꺼내는" 연산이 반복된다. 정렬된 배열을 쓰면 최솟값 조회는 O(1)이지만 새 원소를 삽입할 때 제자리를 찾아 뒤 원소를 밀어야 해 O(n)이 든다. 균형 [이진 탐색 트리](/post/computerterms/trees/)를 쓰면 삽입·삭제는 O(log n)이지만 포인터 3개(왼쪽·오른쪽·부모)를 매 노드마다 유지해야 하고 구현이 복잡하다. **힙(Heap)**은 "최솟값 조회"라는 한 가지 연산만 빠르게 지원하는 대신, 트리를 배열 하나로 표현해 구현을 단순화한 절충안이다.

## 힙의 정의: 완전 이진 트리 + 힙 속성

힙은 두 가지 규칙을 만족하는 [이진 트리](/post/computerterms/trees/)다. 첫째, **완전 이진 트리(Complete Binary Tree)** 규칙 — 마지막 레벨을 제외한 모든 레벨이 꽉 차 있고, 마지막 레벨은 왼쪽부터 채워진다. 둘째, **힙 속성(Heap Property)** — 최소 힙(Min-Heap)에서는 모든 부모 노드의 값이 두 자식보다 작거나 같고, 최대 힙(Max-Heap)에서는 그 반대다. 힙 속성은 형제 노드 사이의 크기 관계는 규정하지 않는다는 점에서 BST의 "왼쪽 < 부모 < 오른쪽" 전순서 규칙보다 약하다 — 이 약한 제약 덕분에 삽입·삭제가 국소적인 비교·교환만으로 끝난다.

완전 이진 트리라는 규칙 덕분에 힙은 포인터 없이 **배열**로 표현할 수 있다. 인덱스 `i`(0-based)에 저장된 노드의 부모는 `(i - 1) / 2`, 왼쪽 자식은 `2*i + 1`, 오른쪽 자식은 `2*i + 2`에 위치한다. 트리의 "빈틈없이 왼쪽부터 채운다"는 규칙이 배열의 "빈틈없이 인덱스를 채운다"는 성질과 정확히 대응하기 때문에 이 공식이 성립한다. 노드 사이를 오가는 데 포인터 역참조 대신 정수 연산만 쓰므로 캐시 지역성도 연결 기반 트리보다 유리하다.

## 삽입: sift-up으로 힙 속성 복구

새 원소는 항상 배열의 맨 끝(완전 이진 트리의 다음 빈자리)에 추가한다. 이 위치는 완전 이진 트리 규칙은 지키지만 힙 속성이 깨져 있을 수 있으므로, 새 노드를 부모와 비교해 힙 속성을 어기면 교환하고, 그 자리에서 다시 부모와 비교하는 과정을 반복한다. 이를 **sift-up**(또는 bubble-up)이라 한다. 트리의 높이가 항상 ⌊log₂ n⌋이므로, 새 노드가 교환을 반복하며 루트까지 올라가는 최악의 경우도 O(log n)번의 비교로 끝난다.

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_HEAP_SIZE 128

typedef struct {
    int data[MAX_HEAP_SIZE];
    int size;
} MinHeap;

void heap_init(MinHeap *h) {
    h->size = 0;
}

static void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/* 인덱스 i의 노드를 부모와 비교하며 위로 올린다 : O(log n) */
static void sift_up(MinHeap *h, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (h->data[parent] <= h->data[i]) break;
        swap(&h->data[parent], &h->data[i]);
        i = parent;
    }
}

void heap_insert(MinHeap *h, int value) {
    if (h->size >= MAX_HEAP_SIZE) {
        fprintf(stderr, "heap full\n");
        return;
    }
    h->data[h->size] = value;
    sift_up(h, h->size);
    h->size++;
}

int main(void) {
    MinHeap h;
    heap_init(&h);
    int values[] = {5, 3, 8, 1, 9, 2};
    for (size_t i = 0; i < sizeof(values) / sizeof(values[0]); i++) {
        heap_insert(&h, values[i]);
    }

    printf("root (min): %d\n", h.data[0]);   /* 항상 1이 출력됨 */
    printf("heap size: %d\n", h.size);
    return 0;
}
```

`sift_up`은 새로 들어온 값이 부모보다 작을 때만 교환하며 위로 이동하고, 부모보다 크거나 같아지는 순간(또는 루트에 도달하면) 멈춘다. 루프가 매 반복마다 인덱스를 부모 위치로 옮기므로 트리 높이만큼만 반복되고, 나머지 노드는 전혀 건드리지 않는다는 점이 O(n) 정렬 삽입과의 핵심 차이다.

## 삭제: sift-down으로 루트를 재구성

최소 힙에서 꺼낼 값은 항상 루트(인덱스 0)다. 루트를 제거한 뒤 트리 모양을 유지하려면, 배열의 마지막 원소를 루트 자리로 옮기고 크기를 하나 줄인 다음, 이 원소를 자식들과 비교하며 힙 속성이 회복될 때까지 아래로 내린다. 이를 **sift-down**(또는 sink)이라 한다. 두 자식 중 더 작은 쪽과 비교해 그보다 크면 교환해야 최소 힙 속성이 유지되므로, 매 단계에서 두 자식 중 작은 값을 먼저 찾는다.

```c
/* 루트에서 시작해 자식과 비교하며 아래로 내린다 : O(log n) */
static void sift_down(MinHeap *h, int i) {
    while (1) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int smallest = i;

        if (left < h->size && h->data[left] < h->data[smallest]) smallest = left;
        if (right < h->size && h->data[right] < h->data[smallest]) smallest = right;
        if (smallest == i) break;

        swap(&h->data[i], &h->data[smallest]);
        i = smallest;
    }
}

int heap_extract_min(MinHeap *h) {
    int min = h->data[0];
    h->size--;
    h->data[0] = h->data[h->size];
    sift_down(h, 0);
    return min;
}
```

`heap_extract_min`이 루트를 반환하기 전에 마지막 원소를 루트로 옮기는 것은 "완전 이진 트리 모양을 항상 유지한다"는 힙의 전제를 지키기 위해서다. 임의의 다른 노드를 루트 자리에 옮기면 마지막 레벨에 구멍이 생겨 배열 인덱스 공식(`2*i+1`, `2*i+2`)이 더는 성립하지 않는다.

## 비교: 정렬된 배열/BST/힙

| 특성 | 정렬된 배열 | 균형 BST | 힙 |
|---|---|---|---|
| 최솟값 조회 | O(1) | O(log n) | O(1) |
| 최솟값 삭제 | O(n) (이동) | O(log n) | O(log n) |
| 임의 값 삽입 | O(n) (이동) | O(log n) | O(log n) |
| 임의 값 탐색 | O(log n) | O(log n) | O(n) — 힙 속성만으론 보장 안 됨 |
| 정렬된 순서로 전체 순회 | O(n) | O(n) (중위 순회) | 지원 안 함 (매번 추출해야 함) |
| 구현 복잡도 | 낮음 | 높음 (균형 유지 로직) | 낮음 (배열 인덱스 연산만) |

힙이 "임의 값 탐색"을 지원하지 못하는 이유는 힙 속성이 형제 사이의 순서를 규정하지 않기 때문이다 — 왼쪽 자식과 오른쪽 자식 중 어느 쪽에 특정 값이 있는지 힙 구조만으로는 알 수 없어, BST처럼 한쪽을 가지치기할 수 없다. 이 트레이드오프 덕분에 힙은 "최솟값/최댓값만 반복해서 꺼낸다"는 우선순위 큐 용도에 정확히 맞을 때 균형 BST보다 구현이 단순하면서도 같은 O(log n) 삽입·삭제 성능을 낸다.

## 흔한 오개념

**"힙은 정렬된 자료구조다"** — 힙 속성은 부모-자식 관계만 규정할 뿐 형제 사이의 순서는 규정하지 않는다. 왼쪽 자식이 오른쪽 자식보다 클 수도 작을 수도 있으므로, 힙 배열을 그대로 출력해도 오름차순이 되지 않는다. 정렬된 결과가 필요하면 `extract_min`을 n번 반복해야 하며, 이 과정 자체가 힙 정렬(Heapsort)의 원리다.

**"힙에서 아무 값이나 빠르게 찾을 수 있다"** — 힙이 O(log n) 삽입·삭제를 지원한다고 해서 임의 값 탐색도 빠르다고 착각하기 쉽다. 힙은 특정 값이 왼쪽 서브트리에 있는지 오른쪽 서브트리에 있는지 판단할 근거(BST의 정렬 규칙 같은)가 없어 최악의 경우 배열 전체를 O(n)으로 훑어야 한다. 특정 값의 존재 여부를 빠르게 확인해야 한다면 힙이 아니라 [해시테이블](/post/computerterms/hash-tables/)이나 BST를 써야 한다.

## 다른 개념과의 연결

힙의 배열 기반 인덱스 공식(부모 `(i-1)/2`, 자식 `2i+1`/`2i+2`)은 [트리](/post/computerterms/trees/)의 포인터 기반 노드 구조를 배열로 압축한 것이며, sift-up·sift-down은 트리 순회의 특수한 형태다. 다음 장에서 다룰 **트라이(Trie)**는 힙과 정반대 방향의 트레이드오프를 보여준다 — 힙이 "값의 순서(최솟값)"에 최적화됐다면, 트라이는 "문자열의 접두사 구조"에 최적화된 트리다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 힙이 완전 이진 트리를 배열로 표현할 수 있는 이유와 부모/자식 인덱스 공식을 유도할 수 있다. sift-up과 sift-down이 각각 삽입·삭제 상황에서 왜 O(log n)에 끝나는지 트리 높이를 근거로 설명할 수 있다. 최솟값 반복 추출이 필요한 상황에서 정렬된 배열·균형 BST·힙 중 힙을 선택해야 하는 이유를 근거와 함께 제시할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 6: Heapsort. MIT Press.

- [cppreference: std::priority_queue](https://en.cppreference.com/w/cpp/container/priority_queue) — 힙 기반 우선순위 큐의 실제 표준 라이브러리 구현
- [Visualgo: Heap](https://visualgo.net/en/heap) — 힙 삽입·삭제 과정의 sift-up/sift-down을 단계별로 시각화한 자료
