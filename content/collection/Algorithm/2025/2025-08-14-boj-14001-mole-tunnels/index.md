---
title: "[Algorithm] cpp 백준 14001번 : Mole Tunnels"
description: "NEERC 2016 ‘Mole Tunnels’(BOJ 14001) 문제를 트리 위 최소 비용 흐름을 직접 쓰지 않고 잔여 네트워크를 모사해 O(m log n)으로 해결하는 방법을 정리합니다. 경로 비용 갱신, DP 구성, 구현 팁과 전체 코드 포함."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph/Tree"
tags:
- "algorithm"
- "algorithms"
- "data-structures"
- "tree"
- "binary-tree"
- "heap"
- "residual-network"
- "residual-graph"
- "min-cost-flow"
- "network-flow"
- "flow"
- "augmenting-path"
- "dp"
- "dynamic-programming"
- "greedy"
- "shortest-path"
- "path"
- "graph"
- "graphs"
- "complexity"
- "optimization"
- "implementation"
- "cplusplus"
- "c++17"
- "code"
- "solution"
- "tutorial"
- "boj"
- "baekjoon"
- "neerc"
- "icpc"
- "contest"
- "problemsolving"
- "performance"
- "tips"
- "tricks"
- "editorial"
- "proof"
- "correctness"
- "complexity-analysis"
- "logn"
- "mlogn"
- "residual"
- "tree-dp"
- "incremental-update"
- "distance"
- "parent-pointer"
- "simulation"
- "알고리즘"
- "자료구조"
- "트리"
- "이진트리"
- "힙"
- "네트워크플로우"
- "최소비용흐름"
- "잔여그래프"
- "증강경로"
- "경로"
- "거리"
- "최단거리"
- "구현"
- "최적화"
- "시간복잡도"
- "풀이"
- "해설"
- "예제"
- "백준"
- "그래프"
- "문제풀이"
- "팁"
image: "wordcloud.png"
---

### 문제 링크
- [BOJ 14001 Mole Tunnels](https://www.acmicpc.net/problem/14001)

### 문제 요약
- 구멍 `1..n`과 `i>1`에 대해 `i`와 `⌊i/2⌋`를 잇는 양방향 터널이 있어 트리가 된다.
- 각 노드 `i`에는 먹이 `c_i`가 있어 최대 `c_i`마리 두더지가 먹을 수 있다.
- `m`마리의 두더지 시작 위치 `p_i`가 주어진다. 아침에 앞의 `k`마리(1..k)가 깨어 움직이며, 총 이동 거리 합을 최소화하도록 목적지 노드를 고른다. 각 노드의 먹이 수용 한도를 넘기면 안 된다.
- 모든 `k=1..m`에 대해 최소 총 이동 거리 합을 출력한다.

### 핵심 아이디어
- 전체를 최소비용유량으로 모델링할 수 있지만 `n,m ≤ 1e5`이므로 직접 돌리기 어렵다.
- 트리가 완전 이진 힙 형태이므로, “잔여 네트워크”를 모사하며 증강을 반복한다.
  - 에지 `(parent → child)`를 아래로 보내는 비용은 기본 `+1`, 반대로 되밀면 `-1`.
  - 위로 올라가는 `(child → parent)`도 현재 흐름 방향에 따라 `±1`.
- 각 노드 `u`에 대해 서브트리 안에서 “먹이가 남아 있는” 최적 목적지까지의 최소 거리 `dis[u]`와 그 위치 `pos[u]`를 유지한다.
- 한 마리가 깨면 시작점 `x`에서 루트로 가는 경로의 조상 `z`를 모두 보며 `now(x→z) + dis[z]`가 최소인 조상 `z`를 찾고, 그 `z`의 서브트리에서 `pos[z]`로 보낸다. 이후 잔여 용량/흐름을 O(log n)만에 갱신한다.

### 알고리즘
1. `flow[u]`: 에지 `(u ↔ parent(u))`의 순방향(위로) 양을 양수로 본 순흐름. 잔여 비용 함수는
   - `costUp(u) = (flow[u] < 0 ? -1 : 1)`
   - `costDown(child) = (flow[child] > 0 ? -1 : 1)`
2. `update(u)`로 `dis[u], pos[u]`를 계산:
   - `u` 자체에 잔여 먹이가 있으면 후보 거리 0.
   - 왼/오 서브트리의 `dis[child] + costDown(child)` 후보 중 최소를 택해 반영.
3. 각 두더지 `x` 처리:
   - 조상들을 따라 올라가며 `best = min(now + dis[u])`, 그때의 `z`와 `y = pos[z]`를 결정.
   - 누적 답에 `best`를 더하고, `y`의 잔여 먹이를 1 감소.
   - 경로 `x→z`는 위로 +1, `y→z`는 위로 -1(=아래로 +1)로 `flow` 갱신.
   - 영향 경로를 따라 `update`를 올리며 `dis/pos` 갱신.

### 올바름 스케치
- 각 단계는 최소비용유량의 한 번 증강과 동치이며, 잔여 그래프의 에지 비용을 정확히 모사한다.
- `dis[u]`는 `u`에서 서브트리 목적지까지의 최단거리(잔여 비용)이고, `now + dis[u]` 최소 조상 `z`를 고르는 것은 `x`에서 목적지까지의 최단 증강경로 선택과 같다.
- 따라서 단계별 최소 증가 비용의 합을 출력하면 `k=1..m`의 정답 누적이 된다.

### 복잡도
- 각 두더지 당 상향 경로 길이는 O(log n), `update`도 경로 길이만큼만 수행 → 전체 O(m log n + n).

### 구현 팁
- 배열 인덱스는 힙처럼 `u`의 부모 `u>>1`, 자식 `2u`, `2u+1`.
- 리프 바깥(>n)의 `dis`는 `INF`로 유지.
- 정밀한 오프바이원/부호 실수를 막기 위해 `costUp/costDown`을 함수로 분리.

### C++ 전체 코드
```cpp
// 더 많은 정보와 풀이 해설은 42jerrykim.github.io에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<int> capacity(n + 1);
    for (int i = 1; i <= n; ++i) cin >> capacity[i];

    vector<int> start(m + 1);
    for (int i = 1; i <= m; ++i) cin >> start[i];

    const int MAX_IDX = 2 * n + 5;
    const int INF = 1e9;

    vector<int> remainingFood(MAX_IDX, 0);
    vector<int> bestDistanceInSubtree(MAX_IDX, INF);
    vector<int> bestNodeInSubtree(MAX_IDX, 0);
    vector<int> flowAlongEdge(MAX_IDX, 0);

    auto leftChild  = [](int u) { return u << 1; };
    auto rightChild = [](int u) { return (u << 1) | 1; };

    auto costUp = [&](int u) -> int {
        return (flowAlongEdge[u] < 0) ? -1 : 1;
    };
    auto costDown = [&](int child) -> int {
        return (flowAlongEdge[child] > 0) ? -1 : 1;
    };

    for (int i = 1; i <= n; ++i) remainingFood[i] = capacity[i];

    function<void(int)> updateNode = [&](int u) {
        int bestPos = 0;
        int bestDis = INF;
        if (u <= n && remainingFood[u] > 0) {
            bestPos = u;
            bestDis = 0;
        }
        int lc = leftChild(u);
        int cand = bestDistanceInSubtree[lc];
        if (cand < INF) {
            int v = cand + costDown(lc);
            if (v < bestDis) {
                bestDis = v;
                bestPos = bestNodeInSubtree[lc];
            }
        }
        int rc = rightChild(u);
        cand = bestDistanceInSubtree[rc];
        if (cand < INF) {
            int v = cand + costDown(rc);
            if (v < bestDis) {
                bestDis = v;
                bestPos = bestNodeInSubtree[rc];
            }
        }
        bestDistanceInSubtree[u] = bestDis;
        bestNodeInSubtree[u] = bestPos;
    };

    for (int u = n; u >= 1; --u) updateNode(u);

    long long totalCost = 0;

    for (int i = 1; i <= m; ++i) {
        int x = start[i];
        int z = 0;
        int now = 0;
        int best = INF;
        for (int u = x; u >= 1; u >>= 1) {
            int val = now + bestDistanceInSubtree[u];
            if (val < best) {
                best = val;
                z = u;
            }
            if (u > 1) now += costUp(u);
        }
        int y = bestNodeInSubtree[z];
        totalCost += best;
        --remainingFood[y];
        for (int u = x; u != z; u >>= 1) ++flowAlongEdge[u];
        for (int u = y; u != z; u >>= 1) --flowAlongEdge[u];
        for (int u = y; u != z; u >>= 1) updateNode(u);
        for (int u = x; u >= 1; u >>= 1) updateNode(u);
        if (i > 1) cout << ' ';
        cout << totalCost;
    }
    cout << '\n';
    return 0;
}
```

### 마무리
- 핵심은 “최단 증강경로”를 트리 구조와 `dis/pos` DP로 O(log n)에 찾고, 잔여 비용을 `±1`로 정확히 반영하는 데 있다.


