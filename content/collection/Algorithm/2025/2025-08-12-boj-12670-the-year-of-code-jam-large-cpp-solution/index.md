---
title: "[Algorithm] C++ 백준 12670번 : The Year of Code Jam (Large)"
description: "격자 달력에서 파란날 행복도 4−이웃수의 합을 최대화하는 문제를 이분 격자 그래프 컷으로 환원한다. B측 보조 변수 y=1−x 변환과 Potts [x!=y] 간선, 단항 재매개화, 고정일(#, .)을 s-t 컷으로 구성해 Dinic으로 최적값을 빠르게 구한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "12670"
- "The Year of Code Jam"
- "Year of Code Jam"
- "Code Jam"
- "Google Code Jam"
- "Large"
- "그래프 컷"
- "Graph Cut"
- "Min-cut"
- "Minimum Cut"
- "Max-flow"
- "Maximum Flow"
- "Dinic"
- "디닉"
- "이분 그래프"
- "Bipartite"
- "격자 그래프"
- "Grid Graph"
- "Potts Model"
- "Ising"
- "Binary Labeling"
- "Energy Minimization"
- "Pairwise Potts"
- "Unary Term"
- "Pairwise Term"
- "Submodular"
- "서브모듈러"
- "Cut Capacity"
- "Capacity"
- "s-t Cut"
- "Source Sink"
- "고정 노드"
- "Hard Constraint"
- "INF Edge"
- "문제 풀이"
- "해설"
- "Algorithm"
- "알고리즘"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "시간복잡도"
- "Time Complexity"
- "구현"
- "Implementation"
- "그래프"
- "Graph"
- "최대 행복"
- "Happiness"
- "Optimization"
- "최적화"
- "Mathematical Modeling"
- "수식 변환"
- "Energy Reparametrization"
- "Labeling"
- "Checkerboard"
- "Neighbor"
- "Adjacency"
- "상하좌우"
- "2D Grid"
- "Google"
- "World Finals"
image: "wordcloud.png"
---

문제: [BOJ 12670 - The Year of Code Jam (Large)](https://www.acmicpc.net/problem/12670)

### 아이디어 요약
- **행복도 식**: 파란날 집합을 `B`라 하면 전체 행복도는 \(H = \sum_{v\in B}(4 - \#\text{blue 이웃}) = 4|B| - 2|E(B)|\). 즉, 파란날이 많을수록 좋지만 파란-파란 인접 간선마다 2씩 감점.
- **이분 격자 + 컷 환원**: 상하좌우 이웃만 가지는 격자는 체커보드 칠이 가능한 이분 그래프. 한 쪽(분할 B) 변수는 `y = 1 - x`로 보조 변환하면, 각 인접 간선은 가중치 1의 Potts 항 `[x != y]`로 표현되고, `x*y` 항은 단항(unary)으로 이관된다.
- **단항 항 구성**: 각 칸의 `w = 4 - deg`(deg는 이웃 수). 분할 A는 `-w * x` 형태, 분할 B는 `+w * y` 형태가 되어 s-t 네트워크에서 소스/싱크 간선으로 표현 가능.
- **고정 상태 반영**: 고정 파랑(`#`)과 흰색(`.`)은 `INF` 용량으로 강제 간선을 연결해 해당 라벨을 고정.
- **최소 컷 = 최적 배치**: s-t 최소 컷을 구해 라벨을 복원하고, 최종 행복도는 직접 `4|B| - 2 * (파란-파란 인접 간선 수)`로 계산.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct Dinic {
    struct Edge { int to, rev; long long cap; };
    int n, source, sink;
    vector<vector<Edge>> g;
    vector<int> level, work;
    Dinic(int n_) : n(n_), source(-1), sink(-1), g(n_), level(n_), work(n_) {}
    void setTerminals(int s, int t) { source = s; sink = t; }
    void addEdge(int u, int v, long long c) {
        Edge a{v, (int)g[v].size(), c};
        Edge b{u, (int)g[u].size(), 0};
        g[u].push_back(a); g[v].push_back(b);
    }
    void addUndirected(int u, int v, long long c) { addEdge(u, v, c); addEdge(v, u, c); }
    bool bfs() {
        fill(level.begin(), level.end(), -1);
        queue<int> q; level[source] = 0; q.push(source);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto &e : g[u]) if (e.cap > 0 && level[e.to] == -1) {
                level[e.to] = level[u] + 1; q.push(e.to);
            }
        }
        return level[sink] != -1;
    }
    long long dfs(int u, long long f) {
        if (u == sink || f == 0) return f;
        for (int &i = work[u]; i < (int)g[u].size(); ++i) {
            auto &e = g[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                long long ret = dfs(e.to, min(f, e.cap));
                if (ret > 0) { e.cap -= ret; g[e.to][e.rev].cap += ret; return ret; }
            }
        }
        return 0;
    }
    long long maxflow() {
        long long flow = 0, INF_FLOW = (long long)4e18;
        while (bfs()) { fill(work.begin(), work.end(), 0);
            while (true) { long long p = dfs(source, INF_FLOW); if (!p) break; flow += p; }
        }
        return flow;
    }
    vector<char> reachableFromSource() {
        vector<char> vis(n, 0); queue<int> q; q.push(source); vis[source] = 1;
        while (!q.empty()) { int u = q.front(); q.pop();
            for (auto &e : g[u]) if (e.cap > 0 && !vis[e.to]) { vis[e.to] = 1; q.push(e.to); }
        }
        return vis;
    }
};

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if (!(cin >> T)) return 0; const long long INF = (long long)1e12;
    while (T--) {
        int N, M; cin >> N >> M; vector<string> a(N); for (int i = 0; i < N; ++i) cin >> a[i];
        auto id = [&](int r, int c) { return r * M + c; };
        auto ok = [&](int r, int c) { return 0 <= r && r < N && 0 <= c && c < M; };
        int V = N * M, S = V, Tt = V + 1; Dinic D(V + 2); D.setTerminals(S, Tt);

        vector<int> deg(V, 0);
        for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
            int d = 0; d += ok(r, c - 1); d += ok(r, c + 1); d += ok(r - 1, c); d += ok(r + 1, c);
            deg[id(r, c)] = d;
        }

        for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
            int u = id(r, c); int w = 4 - deg[u]; bool A = ((r + c) % 2 == 0);
            if (A) {
                long long D0 = max(0,  w); // cost if x=0
                long long D1 = max(0, -w); // cost if x=1
                if (D0) D.addEdge(S, u, D0); if (D1) D.addEdge(u, Tt, D1);
                if (a[r][c] == '#') D.addEdge(S, u, INF);      // force blue (x=1)
                else if (a[r][c] == '.') D.addEdge(u, Tt, INF); // force white (x=0)
            } else {
                long long D0 = max(0, -w); // cost if y=0 (x=1)
                long long D1 = max(0,  w); // cost if y=1 (x=0)
                if (D0) D.addEdge(S, u, D0); if (D1) D.addEdge(u, Tt, D1);
                if (a[r][c] == '#') D.addEdge(u, Tt, INF); // y=0
                else if (a[r][c] == '.') D.addEdge(S, u, INF); // y=1
            }
        }

        auto add_pair = [&](int r1, int c1, int r2, int c2) {
            if (!ok(r1, c1) || !ok(r2, c2)) return; D.addUndirected(id(r1, c1), id(r2, c2), 1);
        };
        for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
            add_pair(r, c, r, c + 1); add_pair(r, c, r + 1, c);
        }

        D.maxflow(); auto reach = D.reachableFromSource();
        auto blue = [&](int r, int c) {
            int u = id(r, c); bool A = ((r + c) % 2 == 0); if (A) return (bool)reach[u];
            bool y = reach[u]; return !y;
        };
        long long Bcnt = 0, adjBB = 0;
        for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
            if (blue(r, c)) ++Bcnt;
            if (c + 1 < M && blue(r, c) && blue(r, c + 1)) ++adjBB;
            if (r + 1 < N && blue(r, c) && blue(r + 1, c)) ++adjBB;
        }
        long long H = 4LL * Bcnt - 2LL * adjBB;
        static int cs = 1; cout << "Case #" << cs++ << ": " << H << '\n';
    }
    return 0;
}
```

### 복잡도
- 정점 수 `V = N*M ≤ 2500`, 간선 수 `E ≈ 2NM`. Dinic로 `O(E√V)` 내외(실전에서는 매우 빠름).

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`


