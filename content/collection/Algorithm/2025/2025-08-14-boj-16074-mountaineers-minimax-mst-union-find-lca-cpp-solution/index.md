---
title: "[Algorithm] cpp 백준 16074번: Mountaineers - Minimax MST·LCA"
description: "격자 지도에서 출발→도착까지 필요한 최소 ‘최고 고도’(minimax 경로)를 구합니다. Kruskal+유니온파인드로 MST를 구성하고 LCA 이진 리프팅으로 경로 최대 가중치를 O(logV)로 질의합니다. 올바름 근거·코너 케이스 점검을 포함해 제출 안정성을 높입니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16074
- cpp
- C++
- Graph
- 그래프
- Grid
- 격자
- Minimum Spanning Tree
- MST
- 최소스패닝트리
- Kruskal
- 크루스칼
- Disjoint Set Union
- 유니온파인드
- Union Find
- LCA
- Lowest Common Ancestor
- 이진리프팅
- Binary Lifting
- Bottleneck Path
- 병목경로
- Minimax
- 최소최대경로
- Connectivity
- 연결성
- Offline Queries
- 오프라인 쿼리
- Tree
- 트리
- BFS
- 너비우선탐색
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Implementation
- 구현
- Data Structures
- 자료구조
- Union-Find Tree
- 경로최대질의
- Binary Search
- 이분탐색
- Shortest Path
- 최단경로
- String
- 문자열
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16074
- 요약: m×n 격자에서 상하좌우로만 이동할 수 있고, 각 칸에는 고도가 주어집니다. (x1,y1)에서 (x2,y2)로 이동하려면 경로 상에서 마주치는 칸들의 고도 중 최대값이 최소가 되도록 해야 합니다. 각 질의마다 이 최소 가능한 최대 고도를 출력합니다.

## 입력/출력
```
<입력>
m n q
height[1][1..n]
...
height[m][1..n]
q개의 줄: x1 y1 x2 y2

<출력>
각 질의에 대한 최소 가능한 최대 고도(정수)
```

예시
```
입력
3 5 3
1 3 2 1 3
2 4 5 4 4
2 1 3 2 2
1 1 3 2
2 4 2 2
1 4 3 4

출력
2
4
3
```

## 접근 개요
- 핵심 관찰: 원하는 값은 경로 상의 최대 고도를 최소화한 값(최소-최대, minimax)입니다. 이는 그래프에서 간선 가중치를 `max(h[u], h[v])`로 정의했을 때의 병목(bottleneck) 경로 최소화와 동치이며, MST에서 두 정점 사이 경로의 최대 간선 가중치로 계산할 수 있습니다.
- 전략: 격자 그래프의 모든 칸을 높이 오름차순으로 활성화하면서, 이미 활성화된 인접 칸과만 연결하는 Kruskal 스타일의 유니온파인드로 MST를 구성합니다. 간선 가중치는 `max(h[u], h[v])`를 사용합니다.
- 질의 처리: 구성된 MST 위에서 LCA(이진 리프팅)를 준비하여, 두 정점 경로의 최대 간선 가중치를 O(log V)에 구합니다. 같은 칸일 때는 그 칸의 높이가 답입니다.

## 알고리즘
1) 그래프 구성 및 MST
- 정점: 각 칸 (i,j) → id = i·n + j
- 간선: 상하좌우 인접 쌍 (u,v), 가중치 w = max(h[u], h[v])
- 구현: 칸들을 높이 오름차순으로 활성화. 새로 활성화된 칸 u에 대해, 이미 활성화된 인접 v와만 `unite(u,v)` 수행. `unite`가 성공할 때만 간선을 MST에 채택하고 가중치를 기록.

2) LCA 준비(이진 리프팅)
- MST는 트리이므로 임의 루트에서 BFS로 깊이와 1번 조상을 채웁니다.
- `up[v][k]` = v의 2^k번째 조상, `mx[v][k]` = 루트 방향으로 2^k만큼 올릴 때 거치는 간선들의 최대값.

3) 질의(u,v) 처리
- 깊이를 맞추며 올라가며 최대값을 갱신.
- 공통 조상 직전까지 동시에 점프하며 최대값을 갱신.
- 마지막으로 부모 간선 2개를 반영해 답을 얻음. u==v면 0이 나오므로 `max(0, h[u], h[v])`로 보정.

## 올바름 근거(요지)
- Kruskal의 컷 성질: 간선 가중치가 `max(h[u],h[v])`인 그래프의 MST에서 두 점 사이 경로의 최대 간선 가중치는 원 그래프에서 가능한 경로들 중 최소의 병목값과 같습니다. 따라서 LCA로 얻는 최대 간선값이 곧 요구하는 최소-최대 고도입니다.
- 활성화 방식은 모든 간선을 가중치 오름차순으로 본 것과 동치이며, `unite` 시에만 간선을 채택하므로 정확히 MST를 생성합니다.

## 복잡도
- V = m·n, E ≈ 2mn. 정렬 O(V log V). 유니온파인드로 MST 구성 O(E α(V)).
- LCA 전처리 O(V log V), 질의당 O(log V). 전체 O(V log V + E α(V) + q log V).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> parent, compSize;
    DSU(int n) : parent(n), compSize(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (compSize[a] < compSize[b]) swap(a, b);
        parent[b] = a;
        compSize[a] += compSize[b];
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n, q;
    if (!(cin >> m >> n >> q)) return 0;
    const int N = m * n;

    vector<int> height(N);
    vector<pair<int,int>> cells; cells.reserve(N);
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            int h; cin >> h;
            int id = i * n + j;
            height[id] = h;
            cells.emplace_back(h, id);
        }
    }

    vector<pair<int,int>> query_pairs(q);
    for (int i = 0; i < q; ++i) {
        int x1, y1, x2, y2; 
        cin >> x1 >> y1 >> x2 >> y2;
        --x1; --y1; --x2; --y2;
        query_pairs[i] = {x1 * n + y1, x2 * n + y2};
    }

    sort(cells.begin(), cells.end()); // by height asc

    DSU dsu(N);
    vector<char> active(N, 0);
    vector<vector<pair<int,int>>> adj(N);
    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};

    for (auto &p : cells) {
        int id = p.second;
        int r = id / n, c = id % n;
        active[id] = 1;
        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            int nid = nr * n + nc;
            if (!active[nid]) continue;
            int w = max(height[id], height[nid]);
            if (dsu.unite(id, nid)) {
                adj[id].push_back({nid, w});
                adj[nid].push_back({id, w});
            }
        }
    }

    const int LOG = 20;
    vector<int> depth(N, -1);
    vector<array<int,LOG>> up(N);
    vector<array<int,LOG>> mx(N);
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < LOG; ++k) {
            up[i][k] = -1;
            mx[i][k] = 0;
        }
    }

    // BFS to set depth and 1st ancestors
    queue<int> qu;
    int root = 0;
    depth[root] = 0;
    qu.push(root);
    while (!qu.empty()) {
        int u = qu.front(); qu.pop();
        for (auto &e : adj[u]) {
            int v = e.first, w = e.second;
            if (depth[v] != -1) continue;
            depth[v] = depth[u] + 1;
            up[v][0] = u;
            mx[v][0] = w;
            qu.push(v);
        }
    }

    // Binary lifting tables
    for (int k = 1; k < LOG; ++k) {
        for (int v = 0; v < N; ++v) {
            if (up[v][0] == -1) continue;
            int mid = up[v][k - 1];
            if (mid == -1) continue;
            up[v][k] = up[mid][k - 1];
            mx[v][k] = max(mx[v][k - 1], mx[mid][k - 1]);
        }
    }

    auto maxOnPath = [&](int u, int v) {
        if (u == v) return 0;
        int ans = 0;
        if (depth[u] < depth[v]) swap(u, v);
        int diff = depth[u] - depth[v];
        for (int k = 0; k < LOG; ++k) {
            if (diff & (1 << k)) {
                ans = max(ans, mx[u][k]);
                u = up[u][k];
            }
        }
        if (u == v) return ans;
        for (int k = LOG - 1; k >= 0; --k) {
            if (up[u][k] != -1 && up[u][k] != up[v][k]) {
                ans = max(ans, mx[u][k]);
                ans = max(ans, mx[v][k]);
                u = up[u][k];
                v = up[v][k];
            }
        }
        ans = max(ans, mx[u][0]);
        ans = max(ans, mx[v][0]);
        return ans;
    };

    ostringstream out;
    for (int i = 0; i < q; ++i) {
        int s = query_pairs[i].first, t = query_pairs[i].second;
        int bottleneck = maxOnPath(s, t);
        int ans = max(bottleneck, max(height[s], height[t]));
        out << ans << '\n';
    }
    cout << out.str();
    return 0;
}
```

## 코너 케이스 체크리스트
- 시작과 도착이 같은 칸(s==t): 답은 해당 칸의 고도
- 단조/균일 고도(모두 동일하거나 계단식 증가/감소)
- 가장자리/모서리 칸(인접 범위 체크)
- 큰 입력에서 빠른 입출력과 O(q log V) 질의 처리 확인

## 제출 전 점검
- 간선 가중치가 `max(h[u],h[v])`인지 확인(Kruskal 컷 성질 전제)
- LCA 테이블 채움 순서와 깊이 맞추기 로직 점검
- 인덱스 변환: (x,y) → id = (x-1)·n + (y-1)
- I/O: `sync_with_stdio(false)`, `tie(nullptr)` 적용

## 참고자료/유사문제
- Minimix/Bottleneck Path와 MST의 관계(컷/사이클 성질)
- LCA 이진 리프팅 표준 구현


