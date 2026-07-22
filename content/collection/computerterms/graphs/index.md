---
image: "wordcloud.png"
slug: graphs
collection_order: 10
draft: false
title: "[Computer Terms] 그래프 (Graph)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "그래프는 트리의 부모-자식 제약을 없애고 임의의 노드끼리 연결한 자료구조입니다. 인접 리스트·인접 행렬 표현과 BFS·DFS 순회를 C 코드와 함께 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Graph(그래프)
- Tree(트리)
- BFS(너비우선탐색)
- DFS(깊이우선탐색)
- Array(배열)
- Linked-List(연결리스트)
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
- Performance(성능)
---

## 이 장을 읽기 전에

[트리](/post/computerterms/trees/)의 노드·간선 개념과 순회 방식(전위·중위·후위), [스택과 큐](/post/computerterms/stacks-and-queues/)의 LIFO·FIFO 자료구조를 안다고 가정한다. 그래프는 트리가 가진 "부모는 하나, 사이클 없음"이라는 제약을 없앤 것이므로, 트리를 그래프의 특수한 경우로 이해하고 시작한다.

## 트리와 그래프의 관계

[트리](/post/computerterms/trees/) 챕터에서 트리는 "사이클이 없는 계층 구조"라고 정의했다. **그래프(Graph)**는 이 정의에서 "계층"이라는 제약마저 없앤 것이다. 그래프의 노드(정점, Vertex)는 임의의 다른 노드와 몇 개든 연결(간선, Edge)될 수 있고, 사이클이 있어도 되며, 방향이 있을 수도(A→B) 없을 수도(A—B) 있다. 소셜 네트워크의 친구 관계, 도로망, 웹 페이지 간 링크가 모두 그래프로 자연스럽게 표현된다. 즉 트리는 "사이클이 없고 연결된" 그래프의 특수한 경우다.

## 그래프를 코드로 표현하는 두 가지 방법

그래프를 저장하는 방법은 **인접 행렬(Adjacency Matrix)**과 **인접 리스트(Adjacency List)** 두 가지가 대표적이다. 인접 행렬은 정점 수만큼의 정사각 배열을 만들어 `matrix[i][j] = 1`로 간선 유무를 표시한다. 임의의 두 정점이 연결됐는지 확인하는 것은 O(1)이지만, 정점이 N개면 항상 O(N²) 메모리를 쓴다. 인접 리스트는 각 정점마다 [연결리스트](/post/computerterms/arrays-and-linked-lists/)로 이웃 정점만 저장한다. 실제 존재하는 간선 수(E)만큼만 메모리를 쓰므로, 간선이 정점 수보다 훨씬 적은 **희소 그래프(Sparse Graph)**에서 인접 행렬보다 훨씬 효율적이다.

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_VERTICES 10

typedef struct AdjNode {
    int dest;
    struct AdjNode *next;
} AdjNode;

typedef struct {
    AdjNode *heads[MAX_VERTICES];
    int vertex_count;
} Graph;

void graph_init(Graph *g, int vertex_count) {
    g->vertex_count = vertex_count;
    for (int i = 0; i < vertex_count; i++) g->heads[i] = NULL;
}

/* 방향 없는 간선이므로 양쪽 인접 리스트에 모두 추가 */
void graph_add_edge(Graph *g, int src, int dest) {
    AdjNode *a = malloc(sizeof(AdjNode));
    a->dest = dest;
    a->next = g->heads[src];
    g->heads[src] = a;

    AdjNode *b = malloc(sizeof(AdjNode));
    b->dest = src;
    b->next = g->heads[dest];
    g->heads[dest] = b;
}

/* 너비 우선 탐색: 큐로 가까운 정점부터 방문 */
void bfs(Graph *g, int start) {
    int visited[MAX_VERTICES] = {0};
    int queue[MAX_VERTICES];
    int front = 0, rear = 0;

    visited[start] = 1;
    queue[rear++] = start;

    while (front < rear) {
        int current = queue[front++];
        printf("%d ", current);

        for (AdjNode *n = g->heads[current]; n != NULL; n = n->next) {
            if (!visited[n->dest]) {
                visited[n->dest] = 1;
                queue[rear++] = n->dest;
            }
        }
    }
    printf("\n");
}

int main(void) {
    Graph g;
    graph_init(&g, 6);
    graph_add_edge(&g, 0, 1);
    graph_add_edge(&g, 0, 2);
    graph_add_edge(&g, 1, 3);
    graph_add_edge(&g, 2, 4);
    graph_add_edge(&g, 3, 5);

    bfs(&g, 0);   /* 0 2 1 4 3 5 : 시작점에서 가까운 순서 (인접 리스트 삽입 순서에 따라 달라질 수 있음) */
    return 0;
}
```

## BFS와 DFS: 같은 그래프, 다른 순회 순서

**너비 우선 탐색(Breadth-First Search, BFS)**은 시작 정점에서 가까운 노드부터 차례로 방문한다. 위 코드처럼 큐에 다음 방문할 정점을 넣고 순서대로 꺼내는 방식이며, "최단 경로(간선 수 기준)"를 구할 때 쓴다. **깊이 우선 탐색(Depth-First Search, DFS)**은 한 방향으로 갈 수 있는 데까지 파고든 뒤 막히면 되돌아오며, [스택과 큐](/post/computerterms/stacks-and-queues/)에서 다룬 호출 스택(재귀) 또는 명시적 스택으로 구현한다. 두 알고리즘 모두 방문한 정점을 표시하는 `visited` 배열이 반드시 필요하다 — 그래프는 트리와 달리 사이클이 있을 수 있어서, 이 표시가 없으면 무한 루프에 빠진다.

## 비교: 인접 행렬 vs 인접 리스트

| 특성 | 인접 행렬 | 인접 리스트 |
|---|---|---|
| 메모리 | O(V²) — 정점 수의 제곱 | O(V + E) — 정점 수 + 실제 간선 수 |
| 두 정점 연결 여부 확인 | O(1) | O(degree) — 해당 정점의 이웃 수만큼 |
| 모든 이웃 순회 | O(V) — 행 전체를 훑어야 함 | O(degree) — 실제 이웃만 순회 |
| 적합한 경우 | 조밀 그래프, 빈번한 연결 여부 질의 | 희소 그래프 (대부분의 실무 그래프) |

## 흔한 오개념

**"그래프 탐색은 항상 BFS를 써야 최단 경로를 구한다"** — BFS가 최단 경로를 보장하는 것은 모든 간선의 가중치가 동일(또는 없음)할 때뿐이다. 도로망처럼 간선마다 거리·시간 같은 가중치가 다르면 BFS만으로는 최단 경로를 보장할 수 없고, 다익스트라(Dijkstra) 같은 별도의 가중치 최단 경로 알고리즘이 필요하다.

**"DFS와 재귀는 같은 것이다"** — 재귀는 DFS를 구현하는 한 가지 방법일 뿐이다. 정점 수가 매우 많은 그래프(예: 수백만 노드 그래프)에서는 재귀 호출 스택 오버플로를 피하기 위해 명시적 스택 자료구조로 DFS를 반복문으로 구현하는 것이 실무적으로 더 안전하다.

## 다른 개념과의 연결

인접 리스트는 [해시테이블](/post/computerterms/hash-tables/)의 체이닝, [연결리스트](/post/computerterms/arrays-and-linked-lists/)의 노드 구조를 그대로 재사용한 결과다. 트리의 전위·중위·후위 순회, 스택·큐 기반 순회는 모두 그래프의 DFS·BFS로 일반화된다. 다음 챕터에서는 자료구조 갈래를 이어, 우선순위에 따라 최솟값·최댓값을 O(log n)에 꺼내는 [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 트리가 그래프의 특수한 경우인 이유(사이클 없음, 부모 유일)를 설명할 수 있다. 조밀 그래프와 희소 그래프 각각에 인접 행렬·인접 리스트 중 어느 표현이 적합한지 메모리·연산 비용 근거로 선택할 수 있다. BFS가 최단 경로를 보장하는 조건(가중치 없음)과, 조건이 깨지면 왜 다른 알고리즘이 필요한지 설명할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 22: Elementary Graph Algorithms. MIT Press.

- [Visualgo: Graph Traversal](https://visualgo.net/en/dfsbfs) — BFS·DFS 방문 순서를 단계별로 시각화한 자료
- [Wikipedia: Adjacency list](https://en.wikipedia.org/wiki/Adjacency_list) — 인접 리스트·인접 행렬의 메모리·연산 복잡도 비교 표
