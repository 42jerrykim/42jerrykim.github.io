---
title: "[Algorithm] C++ 백준 15737번 : 일반 그래프 매칭"
description: "Edmonds Blossom로 일반 그래프에서 최대 매칭을 구합니다. BFS 증가 경로 탐색과 블로섬 수축, LCA 기반 기저 갱신을 구현해 N≤500, M≈N(N−1)/2에서도 1초 내 통과하는 C++ 정답과 핵심 포인트를 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- BOJ
- Baekjoon
- 백준
- String
- Network-Flow
- LCA
- BFS
- 큐
- queue
- 그래프이론
- Graph-Theory
- Graph
- 그래프
- 시간복잡도
- Time-Complexity
- 구현
- Implementation
- C++
- IO
- Editorial
- Problem-Solving
- 알고리즘
- Algorithm
- ICPC
- Competitive-Programming
- 코딩테스트
- Coding-Test
- Data-Structures
- 자료구조
- Optimization
- 최적화
- 문제해결
- Code-Quality
- 코드품질
- Go
- .NET
- Git
- GitHub
- Tree
- Hardware
- Networking
- Space-Complexity
- 공간복잡도
- Edge-Cases
- 엣지케이스
- Testing
- 테스트
- Documentation
- 문서화
- Best-Practices
image: "wordcloud.png"
---

문제: [BOJ 15737 - 일반 그래프 매칭](https://www.acmicpc.net/problem/15737)

### 아이디어 요약
- **목표**: 무향 일반 그래프에서 최대 매칭 크기 계산.
- **핵심**: 이분 그래프가 아닐 수 있으므로, Edmonds의 **Blossom** 알고리즘으로 홀수 사이클(블로섬)을 하나의 정점으로 수축하며 BFS로 증가 경로를 탐색.
- **구성 요소**:
  - `match[u]`: 짝지은 정점, 없으면 0.
  - `base[u]`: 현재 수축된 나무에서의 기저 정점(사이클 대표).
  - `p[u]`: BFS 트리에서의 부모.
  - `used[u]`: BFS 방문 여부, `inBlossom[u]`: 수축에 포함되는지.
  - `lca(a,b)`: 두 정점에서 짝-부모 사슬을 따라가며 만나는 최소 공통 기저.
  - `markPath`/`blossom`: LCA까지의 경로를 표시하고 사이클을 수축하여 새로운 루트 수준에서 BFS를 이어감.
- **종료**: 루트에서 시작한 BFS가 매칭되지 않은 정점에 도달하면 경로를 뒤집어 매칭을 1 증가.
- **복잡도**: 전형적으로 `O(n^3)`, `n ≤ 500`에서도 충분히 통과.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <bits/stdc++.h>
using namespace std;

struct Blossom {
    int n;
    vector<vector<int>> g;          // adjacency list (1-indexed)
    vector<int> matchTo, parentInTree, baseVertex;
    vector<int> bfsQueue;
    vector<char> isUsedInBFS, isInBlossom;

    explicit Blossom(int n_) : n(n_), g(n_ + 1), matchTo(n_ + 1, 0),
                               parentInTree(n_ + 1, -1), baseVertex(n_ + 1),
                               isUsedInBFS(n_ + 1), isInBlossom(n_ + 1) {
        iota(baseVertex.begin(), baseVertex.end(), 0);
    }

    void addEdge(int u, int v) {
        if (u == v) return;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    int lca(int a, int b) {
        vector<char> isVisitedBase(n + 1, 0);
        while (true) {
            a = baseVertex[a];
            isVisitedBase[a] = 1;
            if (matchTo[a] == 0) break;
            a = parentInTree[matchTo[a]];
        }
        while (true) {
            b = baseVertex[b];
            if (isVisitedBase[b]) return b;
            if (matchTo[b] == 0) break;
            b = parentInTree[matchTo[b]];
        }
        return 0; // never reached
    }

    void markPath(int vertex, int commonBase, int child) {
        while (baseVertex[vertex] != commonBase) {
            isInBlossom[ baseVertex[vertex] ] = 1;
            isInBlossom[ baseVertex[ matchTo[vertex] ] ] = 1;
            parentInTree[vertex] = child;
            child = matchTo[vertex];
            vertex = parentInTree[ matchTo[vertex] ];
        }
    }

    void contractBlossom(int v, int u, int commonBase) {
        fill(isInBlossom.begin(), isInBlossom.end(), 0);
        markPath(v, commonBase, u);
        markPath(u, commonBase, v);
        for (int i = 1; i <= n; ++i) {
            if (isInBlossom[ baseVertex[i] ]) {
                baseVertex[i] = commonBase;
                if (!isUsedInBFS[i]) {
                    isUsedInBFS[i] = 1;
                    bfsQueue.push_back(i);
                }
            }
        }
    }

    int findAugmentingPath(int root) {
        fill(isUsedInBFS.begin(), isUsedInBFS.end(), 0);
        fill(parentInTree.begin(), parentInTree.end(), -1);
        iota(baseVertex.begin(), baseVertex.end(), 0);
        bfsQueue.clear();
        bfsQueue.push_back(root);
        isUsedInBFS[root] = 1;
        for (size_t head = 0; head < bfsQueue.size(); ++head) {
            int v = bfsQueue[head];
            for (int u : g[v]) {
                if (baseVertex[v] == baseVertex[u] || matchTo[v] == u) continue;
                if (u == root || (matchTo[u] && parentInTree[matchTo[u]] != -1)) {
                    int a = lca(v, u);
                    contractBlossom(v, u, a);
                } else if (parentInTree[u] == -1) {
                    parentInTree[u] = v;
                    if (matchTo[u] == 0) return u; // found exposed vertex
                    int w = matchTo[u];
                    if (!isUsedInBFS[w]) {
                        isUsedInBFS[w] = 1;
                        bfsQueue.push_back(w);
                    }
                }
            }
        }
        return 0;
    }

    int solve() {
        int matches = 0;
        for (int v = 1; v <= n; ++v) {
            if (matchTo[v] == 0) {
                int u = findAugmentingPath(v);
                if (u == 0) continue;
                ++matches;
                while (u) {
                    int pv = parentInTree[u];
                    int ppv = (pv ? matchTo[pv] : 0);
                    matchTo[u] = pv;
                    if (pv) matchTo[pv] = u;
                    u = ppv;
                }
            }
        }
        return matches;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) return 0;
    Blossom bl(N);
    for (int i = 0; i < M; ++i) {
        int u, v; cin >> u >> v;
        bl.addEdge(u, v);
    }
    cout << bl.solve() << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(n^3)` (실전에서는 매우 빠르게 동작)
- 공간: `O(n + m)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 문제: `https://www.acmicpc.net/problem/15737`
- 키워드: Edmonds, Blossom, 일반 그래프 최대 매칭, 증가 경로, 수축, LCA

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 또는 빈 입력 | 반복문 범위·예외 처리 확인 |
| **오버플로우** | 답이 $2^{31}$ 초과 가능 | `long long` (C++) 등 사용 |
