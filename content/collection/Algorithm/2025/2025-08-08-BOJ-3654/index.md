---
title: "[Algorithm] C++ 백준 3654번 : L퍼즐 실패"
categories:
- Algorithm
- Graph
- Flow
tags:
- Max Flow
- Dinic
- Bipartite Matching
- Grid
- 구현
date: 2025-08-08
draft: true
---

문제: [https://www.acmicpc.net/problem/3654](https://www.acmicpc.net/problem/3654)

검정(B) 한 칸과 흰(W) 두 칸을 덮는 L자 조각(총 3칸)으로, 주어진 격자 패턴(일부는 빈 칸 `.`)을 정확히 덮을 수 있는지 묻는 문제입니다. 조각은 회전 가능, 겹침 불가이며 `.`는 덮으면 안 됩니다.

## 핵심 아이디어

- 각 조각은 항상 B 1칸, W 2칸을 덮습니다. 따라서 필수 조건: 총 흰칸 수 `W = 2 * B`. 아니면 즉시 NO.
- 각 검정 칸은 수직 방향 인접 흰칸 1개와 수평 방향 인접 흰칸 1개가 동시에 필요합니다(조각의 두 팔을 각각 세로/가로 중 하나로 배치).
- 이를 최대 유량으로 모델링하여 충분 조건을 판정합니다.

### 네트워크 구성

- 소스 S에서 각 검정 칸의 두 슬롯으로 간선:
  - 수직 슬롯(Bv), 수평 슬롯(Bh) 각각 용량 1
- Bv → 그 검정 칸과 상/하로 인접한 흰칸들(용량 1)
- Bh → 그 검정 칸과 좌/우로 인접한 흰칸들(용량 1)
- 모든 흰칸 Wnode → 싱크 T(용량 1)

최대 유량이 흰칸 수 `W(=2*B)`와 같으면 모든 흰칸이 정확히 한 번씩 매칭되므로 YES, 아니면 NO입니다.

또한, 조기 불가능성 체크로 각 B가 최소 한 개 이상의 수직 인접 W와 수평 인접 W를 모두 갖는지 확인하면 탐색 공간을 줄일 수 있습니다.

## C++ 풀이 (Dinic)

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Dinic {
    struct Edge { int to, cap, rev; };
    int N;
    vector<vector<Edge>> G;
    vector<int> level, it;

    Dinic(int n=0) { init(n); }
    void init(int n) { N = n; G.assign(n, {}); }

    void add_edge(int u, int v, int c) {
        Edge a{v, c, (int)G[v].size()};
        Edge b{u, 0, (int)G[u].size()};
        G[u].push_back(a); G[v].push_back(b);
    }

    bool bfs(int s, int t) {
        level.assign(N, -1);
        queue<int> q; level[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto &e : G[u]) if (e.cap > 0 && level[e.to] < 0) {
                level[e.to] = level[u] + 1; q.push(e.to);
            }
        }
        return level[t] >= 0;
    }

    int dfs(int u, int t, int f) {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)G[u].size(); ++i) {
            auto &e = G[u][i];
            if (e.cap > 0 && level[u] + 1 == level[e.to]) {
                int ret = dfs(e.to, t, min(f, e.cap));
                if (ret > 0) { e.cap -= ret; G[e.to][e.rev].cap += ret; return ret; }
            }
        }
        return 0;
    }

    long long max_flow(int s, int t) {
        long long flow = 0;
        while (bfs(s, t)) {
            it.assign(N, 0);
            while (true) {
                int pushed = dfs(s, t, INT_MAX);
                if (!pushed) break;
                flow += pushed;
            }
        }
        return flow;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n, m; cin >> n >> m;
        vector<string> g(n);
        for (int i = 0; i < n; ++i) cin >> g[i];

        auto inb = [&](int r, int c){ return 0 <= r && r < n && 0 <= c && c < m; };

        vector<vector<int>> whiteId(n, vector<int>(m, -1));
        vector<vector<int>> bVertId(n, vector<int>(m, -1));
        vector<vector<int>> bHorizId(n, vector<int>(m, -1));

        int W = 0, B = 0;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j) {
                if (g[i][j] == 'W') ++W;
                else if (g[i][j] == 'B') ++B;
            }

        if (W != 2 * B) { cout << "NO\n"; continue; }

        // Early infeasibility: each black needs at least one vertical and one horizontal white neighbor
        bool ok = true;
        for (int i = 0; i < n && ok; ++i)
            for (int j = 0; j < m && ok; ++j)
                if (g[i][j] == 'B') {
                    bool hasV = false, hasH = false;
                    if (inb(i-1,j) && g[i-1][j] == 'W') hasV = true;
                    if (inb(i+1,j) && g[i+1][j] == 'W') hasV = true;
                    if (inb(i,j-1) && g[i][j-1] == 'W') hasH = true;
                    if (inb(i,j+1) && g[i][j+1] == 'W') hasH = true;
                    if (!hasV || !hasH) ok = false;
                }

        if (!ok) { cout << "NO\n"; continue; }

        // Assign ids
        int wid = 0, bidV = 0, bidH = 0;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == 'W') whiteId[i][j] = wid++;

        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == 'B') {
                    bVertId[i][j] = bidV++;
                    bHorizId[i][j] = bidH++;
                }

        // Build flow network
        // Nodes: S | Bv | Bh | W | T
        int S = 0;
        int offsetBv = 1;
        int offsetBh = offsetBv + bidV;
        int offsetW  = offsetBh + bidH;
        int Tt       = offsetW + wid;
        Dinic dinic(Tt + 1);

        // S -> Bv, S -> Bh
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == 'B') {
                    dinic.add_edge(S, offsetBv + bVertId[i][j], 1);
                    dinic.add_edge(S, offsetBh + bHorizId[i][j], 1);
                }

        auto addIfWhite = [&](int r, int c, int fromNode){
            if (inb(r,c) && g[r][c] == 'W') {
                dinic.add_edge(fromNode, offsetW + whiteId[r][c], 1);
            }
        };

        // Bv -> W (vertical neighbors), Bh -> W (horizontal neighbors)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == 'B') {
                    int vNode = offsetBv + bVertId[i][j];
                    int hNode = offsetBh + bHorizId[i][j];
                    addIfWhite(i-1, j, vNode);
                    addIfWhite(i+1, j, vNode);
                    addIfWhite(i, j-1, hNode);
                    addIfWhite(i, j+1, hNode);
                }

        // W -> T
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == 'W') {
                    dinic.add_edge(offsetW + whiteId[i][j], Tt, 1);
                }

        long long flow = dinic.max_flow(S, Tt);
        cout << (flow == W ? "YES" : "NO") << "\n";
    }
    return 0;
}
```

## 복잡도

- **시간**: Dinic로 대략 O(E √V) 수준, 그리드에서 간선 수는 색칠된 칸 수의 상수배라 5초 내 충분
- **공간**: O(V + E)

## 체크리스트

- `W != 2B` → NO
- 어떤 `B`든 수직 인접 `W`가 최소 1개, 수평 인접 `W`가 최소 1개 없으면 NO
- 위 네트워크의 최대 유량이 `W`와 같으면 YES, 아니면 NO





