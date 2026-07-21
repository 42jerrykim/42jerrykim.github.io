---
image: "wordcloud.png"
slug: union-find
collection_order: 47
draft: false
title: "[Computer Terms] 유니온-파인드 (Union-Find, Disjoint Set)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "유니온-파인드는 서로소 집합을 트리로 관리하는 자료구조입니다. Union by Rank와 Path Compression이 왜 필요한지, 크루스칼 MST에서의 활용을 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- DSU(Disjoint Set Union)
- Union-Find(유니온파인드)
- Tree(트리)
- Graph(그래프)
- Array(배열)
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
---

## 이 장을 읽기 전에

[트리](/post/computerterms/trees/)의 부모-자식 개념, [그래프](/post/computerterms/graphs/)의 정점·간선·연결 개념, [트라이](/post/computerterms/tries/)에서 본 "트리 구조를 값의 크기가 아닌 다른 목적에 쓰는 사례"를 안다고 가정한다. 유니온-파인드는 트리를 "집합의 소속 관계"를 표현하는 용도로 쓰는 자료구조다.

## 두 원소가 같은 그룹인지 빠르게 알아내기

네트워크에 새 케이블을 놓을 때마다 "이 두 컴퓨터가 이미 같은 네트워크에 속해 있는가"를 확인해야 한다고 하자. 매번 [그래프](/post/computerterms/graphs/) 전체를 BFS·DFS로 순회해 연결 여부를 확인하면 케이블을 놓을 때마다 O(V + E)가 든다. **유니온-파인드(Union-Find, Disjoint Set Union, DSU)**는 이 문제를 두 가지 연산으로 압축한다 — `find(x)`는 x가 속한 집합의 대표 원소를 반환하고, `union(x, y)`는 x와 y가 속한 두 집합을 하나로 합친다. 두 원소가 같은 집합인지는 `find(x) == find(y)`로 즉시 확인할 수 있다.

## 기본 구현: 배열로 표현하는 트리

유니온-파인드는 각 집합을 트리 하나로 표현한다. 배열 `parent[i]`에 i번 원소의 부모를 저장하고, 자기 자신이 부모인 원소(`parent[i] == i`)를 그 집합의 **루트(대표 원소)**로 삼는다. `find(x)`는 부모를 따라 루트까지 올라가고, `union(x, y)`는 한쪽 트리의 루트를 다른 쪽 루트의 자식으로 붙인다.

```c
#include <stdio.h>

#define MAX_N 100

int parent[MAX_N];
int rank_arr[MAX_N];  /* 트리의 대략적인 높이를 추적 */

void dsu_init(int n) {
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        rank_arr[i] = 0;
    }
}

/* 경로 압축 적용 find : 루트까지 가는 길의 모든 노드를 루트에 직접 연결 */
int find(int x) {
    if (parent[x] != x) {
        parent[x] = find(parent[x]);   /* path compression */
    }
    return parent[x];
}

/* rank가 낮은 트리를 rank가 높은 트리 밑에 붙인다 */
void union_sets(int x, int y) {
    int root_x = find(x);
    int root_y = find(y);
    if (root_x == root_y) return;   /* 이미 같은 집합 */

    if (rank_arr[root_x] < rank_arr[root_y]) {
        parent[root_x] = root_y;
    } else if (rank_arr[root_x] > rank_arr[root_y]) {
        parent[root_y] = root_x;
    } else {
        parent[root_y] = root_x;
        rank_arr[root_x]++;
    }
}

int main(void) {
    dsu_init(6);
    union_sets(0, 1);
    union_sets(1, 2);
    union_sets(3, 4);

    printf("0, 2 same set: %d\n", find(0) == find(2));   /* 1 */
    printf("0, 3 same set: %d\n", find(0) == find(3));   /* 0 */

    union_sets(2, 3);
    printf("0, 4 same set: %d\n", find(0) == find(4));   /* 1: 합집합 이후 연결됨 */
    return 0;
}
```

`find`가 재귀 호출 중 `parent[x] = find(parent[x])`로 자기 자신의 부모를 루트로 즉시 덮어쓰는 부분이 **경로 압축(Path Compression)**이다. 이 한 줄이 없다면 `find`는 매번 원래 트리의 깊이만큼 부모를 따라 올라가야 하지만, 한 번 압축된 이후에는 같은 노드에 대한 다음 `find` 호출이 O(1)에 가까워진다.

## 왜 최적화 없이는 O(n)까지 느려지는가

`union_sets`에서 항상 x의 루트를 y의 루트 밑에 붙이는 식으로 구현하면, 1과 2를 합치고 그 결과에 3을 합치고 다시 4를 합치는 과정을 반복할 때 트리가 한쪽으로만 길게 늘어진 사슬이 될 수 있다. 이는 [트리](/post/computerterms/trees/) 챕터에서 본 "정렬된 값을 순서대로 삽입한 BST가 연결리스트로 퇴화하는" 문제와 정확히 같은 패턴이다. 이 상태에서 `find`를 호출하면 매번 사슬 전체를 O(n)으로 훑어야 한다. **Union by Rank(또는 Size)**는 항상 더 얕은(또는 원소 수가 적은) 트리를 더 깊은 트리 밑에 붙여 트리 높이가 O(log n)을 넘지 않도록 보장하고, **경로 압축**은 `find`가 지나간 경로의 노드를 모두 루트에 직접 연결해 이후 탐색을 더 빠르게 만든다. 두 최적화를 함께 쓰면 `find`와 `union`의 상각(amortized) 시간 복잡도는 역 아커만 함수 α(n)에 수렴한다 — 사실상 모든 실용적인 n에 대해 상수 시간으로 취급해도 무방할 만큼 느리게 증가한다.

## 크루스칼 최소 신장 트리에서의 활용

유니온-파인드가 실무에서 가장 널리 쓰이는 곳 중 하나가 **크루스칼(Kruskal) 최소 신장 트리(MST) 알고리즘**이다. 크루스칼은 모든 간선을 가중치 오름차순으로 정렬한 뒤, 간선을 하나씩 검토하며 "이 간선의 양 끝 정점이 이미 같은 집합(사이클을 만듦)인지"를 확인한다. 같은 집합이면 그 간선을 버리고, 다른 집합이면 간선을 선택하고 두 집합을 `union`으로 합친다. 이 사이클 판정을 매번 [그래프](/post/computerterms/graphs/) 전체 순회로 하면 느리지만, 유니온-파인드를 쓰면 `find` 한 번으로 거의 상수 시간에 판정할 수 있어 크루스칼 알고리즘 전체가 간선 정렬 비용인 O(E log E)에 지배된다.

## 비교: 그래프 순회 vs 유니온-파인드

| 특성 | 매번 BFS/DFS로 연결 확인 | 유니온-파인드 |
|---|---|---|
| 두 원소가 같은 집합인지 확인 | O(V + E) | 상각 O(α(n)) ≈ O(1) |
| 두 집합 합치기 | 그래프에 간선만 추가하면 됨 (별도 연산 없음) | 상각 O(α(n)) |
| 집합을 다시 분리(disunion) | 가능 (간선 제거) | 기본적으로 지원 안 함 |
| 적합한 경우 | 그래프 구조 자체가 필요한 경우(경로 복원 등) | 합치기만 반복되고 분리는 없는 경우(MST, 네트워크 연결성) |

## 흔한 오개념

**"유니온-파인드는 최적화 없이도 항상 빠르다"** — `union`을 항상 같은 방향으로만 적용하면(예: x를 항상 y 밑에 붙임) 트리가 사슬 형태로 편향되어 `find`가 O(n)까지 느려질 수 있다. Union by Rank/Size 없이는 이론적으로 최악의 경우를 보장할 수 없으므로, 실무 구현에서는 항상 두 최적화를 함께 적용한다.

**"유니온-파인드는 집합의 원소 목록도 알려준다"** — `find(x)`는 x가 속한 집합의 대표 원소(루트)만 알려줄 뿐, 그 집합에 어떤 원소들이 있는지는 별도로 추적하지 않는다. 집합의 전체 원소 목록이 필요하다면 대표 원소별로 실제 원소를 저장하는 별도 자료구조(예: 대표 원소를 키로 하는 [해시테이블](/post/computerterms/hash-tables/))를 함께 유지해야 한다.

## 다른 개념과의 연결

유니온-파인드의 트리는 [트리](/post/computerterms/trees/) 챕터의 "균형이 깨지면 O(n)으로 퇴화한다"는 문제를 Union by Rank로, "매번 루트까지 다시 올라가는 비효율"을 경로 압축으로 해결한 사례다. 다음 장에서 다룰 **세그먼트 트리**는 같은 "완전 이진 트리를 배열로 표현한다"는 [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)의 아이디어를 구간 쿼리라는 다른 문제에 적용한 자료구조다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. `find`와 `union` 연산이 무엇을 하는지, 그리고 이 둘로 "같은 집합인가"를 판정하는 원리를 설명할 수 있다. Union by Rank와 경로 압축이 각각 어떤 문제(트리 편향, 반복 탐색 비용)를 해결하는지 설명할 수 있다. 유니온-파인드가 유리한 상황(집합을 합치기만 하고 분리는 없는 경우)과 그래프 순회가 필요한 상황을 구분해 선택할 수 있다.

## 참고 자료

> Tarjan, R. E. (1975). Efficiency of a Good But Not Linear Set Union Algorithm. *Journal of the ACM*, 22(2), 215–225.

- [cppreference: std::disjoint_set (boost 문서 참고)](https://www.boost.org/doc/libs/release/libs/disjoint_sets/disjoint_sets.html) — Union by Rank·경로 압축을 적용한 실제 라이브러리 구현
- [Visualgo: Union-Find Disjoint Sets](https://visualgo.net/en/ufds) — union·find 연산과 경로 압축 과정을 단계별로 시각화한 자료
