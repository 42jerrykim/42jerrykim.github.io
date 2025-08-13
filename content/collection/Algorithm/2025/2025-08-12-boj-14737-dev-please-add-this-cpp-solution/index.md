---
title: "[Algorithm] C++ 백준 14737번 Dev, Please Add This!"
description: "격자에서 공을 상하좌우로 굴려 벽이나 가장자리에 닿을 때까지 이동하는 퍼즐에서, 모든 별을 하나의 플레이 순서로 획득할 수 있는지 판정한다. 단순 커버리지가 아니라 이동 순서 제약이 존재하므로 셀 단위 이동을 단방향 그래프로 모델링하고, 강한 연결 요소(SCC)로 압축한 DAG에서 상호 비가역(서로 도달 불가)한 컴포넌트 쌍의 동시 방문을 금지하는 제약과 각 별이 있는 칸의 행/열 중 하나의 정지 컴포넌트를 반드시 방문해야 한다는 제약을 2-SAT으로 구성해 모순 여부로 YES/NO를 결정한다. Kosaraju로 SCC를 구하고 DAG 도달성은 비트셋 DP로 처리하여 50×50까지 빠르게 동작한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "14737"
- "Dev Please Add This"
- "SCC"
- "Strongly Connected Components"
- "강한연결요소"
- "2-SAT"
- "Two-SAT"
- "Implication Graph"
- "CNF"
- "Clause"
- "Satisfiability"
- "SAT"
- "DAG"
- "Directed Acyclic Graph"
- "Topological Order"
- "위상정렬"
- "Reachability"
- "Bitset"
- "Grid"
- "격자"
- "Rolling Ball"
- "Puzzle"
- "Graph"
- "Graph Theory"
- "그래프"
- "Algorithm"
- "알고리즘"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Kosaraju"
- "Tarjan"
- "Component"
- "컴포넌트"
- "State Space"
- "상태 공간"
- "ICPC"
- "KAIST"
- "Mock Competition"
- "Open Cup"
- "Problem Solving"
- "문제풀이"
- "해설"
- "Solution"
- "Editorial"
- "Constraint"
- "제약"
- "논리"
- "Logic"
- "Path Dependency"
- "순서 제약"
image: "wordcloud.png"
---

문제: [BOJ 14737 - Dev, Please Add This!](https://www.acmicpc.net/problem/14737)

### 아이디어 요약
- 단순히 “별이 한 번이라도 어떤 굴림 경로에 포함되면 OK”가 아니다. 한 번의 플레이 순서로 전부 먹을 수 있어야 하므로 순서 제약이 존재한다.
- 각 빈 칸을 정점으로 하고, 네 방향으로 굴려 도착하는 "정지 칸"으로의 간선을 두면 단방향 그래프가 된다.
- 그래프를 SCC로 압축해 DAG를 만든다. 어떤 두 컴포넌트가 서로 도달 불가능하면 한 플레이에서 두 컴포넌트를 모두 방문하는 것은 불가능하다.
- 각 별은 그 칸에서 수직/수평으로 굴러서 멈추는 정지 칸의 컴포넌트 중 적어도 하나를 방문해야 먹을 수 있다.
- 따라서 “컴포넌트 i를 방문한다/안 한다”를 변수로 잡고, 2-SAT 제약을 구성한다.
  - 시작 컴포넌트는 반드시 방문 (참 고정). 시작에서 도달 불가능한 컴포넌트는 방문 금지 (거짓 고정).
  - DAG에서 서로 도달 불가능한 두 컴포넌트 i, j는 동시에 방문 불가 → (¬A_i ∨ ¬A_j).
  - 각 별 x는 (A_row(x) ∨ A_col(x)). 여기서 row/col은 해당 칸에서 수평/수직으로 굴린 정지 칸의 컴포넌트.
- 2-SAT이 만족 가능하면 YES, 아니면 NO.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct TwoSAT {
    int numVars;
    vector<vector<int>> g, rg;
    vector<int> comp, order;

    TwoSAT(int n = 0) { init(n); }
    void init(int n) {
        numVars = n;
        g.assign(2 * n, {});
        rg.assign(2 * n, {});
    }
    static int varFalse(int i) { return 2 * i; }
    static int varTrue(int i) { return 2 * i + 1; }
    static int Not(int x) { return x ^ 1; }

    void addImp(int u, int v) { g[u].push_back(v); rg[v].push_back(u); }
    void addOr(int A, int B) { addImp(Not(A), B); addImp(Not(B), A); }
    void forceTrue(int L) { addOr(L, L); }
    void forceFalse(int L) { addOr(Not(L), Not(L)); }

    bool satisfiable(vector<int>* assignment = nullptr) {
        int N = 2 * numVars;
        vector<int> vis(N, 0); order.clear(); order.reserve(N);
        function<void(int)> dfs1 = [&](int v) {
            vis[v] = 1;
            for (int to : g[v]) if (!vis[to]) dfs1(to);
            order.push_back(v);
        };
        for (int i = 0; i < N; ++i) if (!vis[i]) dfs1(i);

        comp.assign(N, -1); int cc = 0;
        function<void(int)> dfs2 = [&](int v) {
            comp[v] = cc;
            for (int to : rg[v]) if (comp[to] == -1) dfs2(to);
        };
        for (int i = N - 1; i >= 0; --i) {
            int v = order[i];
            if (comp[v] == -1) { dfs2(v); ++cc; }
        }
        for (int i = 0; i < numVars; ++i) if (comp[2 * i] == comp[2 * i + 1]) return false;
        if (assignment) {
            assignment->assign(numVars, 0);
            for (int i = 0; i < numVars; ++i)
                (*assignment)[i] = comp[2 * i] < comp[2 * i + 1] ? 1 : 0;
        }
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int H, W; if (!(cin >> H >> W)) return 0;
    vector<string> grid(H);
    for (int i = 0; i < H; ++i) cin >> grid[i];

    const int dr[4] = {1, -1, 0, 0};
    const int dc[4] = {0, 0, 1, -1};
    auto inb = [&](int r, int c) { return 0 <= r && r < H && 0 <= c && c < W; };

    vector<int> id(H * W, -1);
    vector<pair<int,int>> cells; cells.reserve(H * W);
    pair<int,int> start = {-1, -1};
    vector<pair<int,int>> stars;

    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (grid[r][c] != '#') {
                id[r * W + c] = (int)cells.size();
                cells.push_back({r, c});
                if (grid[r][c] == 'O') start = {r, c};
                if (grid[r][c] == '*') stars.push_back({r, c});
            }
        }
    }
    int N = (int)cells.size();
    if (N == 0) { cout << "NO\n"; return 0; }

    auto rollStop = [&](int r, int c, int d) {
        int nr = r, nc = c;
        while (true) {
            int tr = nr + dr[d], tc = nc + dc[d];
            if (!inb(tr, tc) || grid[tr][tc] == '#') break;
            nr = tr; nc = tc;
        }
        return pair<int,int>{nr, nc};
    };

    vector<vector<int>> g(N), rg(N);
    vector<array<int,2>> mv(N, array<int,2>{-1, -1}); // 0: vertical, 1: horizontal

    for (int v = 0; v < N; ++v) {
        auto [r, c] = cells[v];
        for (int d = 0; d < 4; ++d) {
            auto [sr, sc] = rollStop(r, c, d);
            int u = id[sr * W + sc];
            g[v].push_back(u);
            rg[u].push_back(v);
            mv[v][d / 2] = u; // up/down -> 0, right/left -> 1
        }
    }

    // Kosaraju SCC
    vector<int> order, vis(N, 0);
    function<void(int)> dfs1 = [&](int v) {
        vis[v] = 1;
        for (int to : g[v]) if (!vis[to]) dfs1(to);
        order.push_back(v);
    };
    for (int v = 0; v < N; ++v) if (!vis[v]) dfs1(v);

    vector<int> comp(N, -1); int sccCnt = 0;
    function<void(int)> dfs2 = [&](int v) {
        comp[v] = sccCnt;
        for (int to : rg[v]) if (comp[to] == -1) dfs2(to);
    };
    for (int i = N - 1; i >= 0; --i) {
        int v = order[i];
        if (comp[v] == -1) { dfs2(v); ++sccCnt; }
    }

    // Build SCC DAG
    vector<vector<int>> dag(sccCnt);
    vector<int> indeg(sccCnt, 0);
    {
        vector<unordered_set<int>> uniq(sccCnt);
        for (int v = 0; v < N; ++v) {
            int a = comp[v];
            for (int to : g[v]) {
                int b = comp[to];
                if (a != b && uniq[a].insert(b).second) {
                    dag[a].push_back(b);
                    indeg[b]++;
                }
            }
        }
    }

    // Topological order
    queue<int> q; for (int i = 0; i < sccCnt; ++i) if (indeg[i] == 0) q.push(i);
    vector<int> topo; topo.reserve(sccCnt);
    while (!q.empty()) {
        int v = q.front(); q.pop(); topo.push_back(v);
        for (int to : dag[v]) if (--indeg[to] == 0) q.push(to);
    }

    // DAG reachability via bitset DP
    const int MAXS = 2600; // 50*50 <= 2500
    vector<bitset<MAXS>> reach(sccCnt);
    for (int i = sccCnt - 1; i >= 0; --i) {
        int v = topo[i];
        reach[v].set(v);
        for (int to : dag[v]) reach[v] |= reach[to];
    }

    // 2-SAT variables: one per SCC (Ai = visit SCC i)
    TwoSAT sat(sccCnt);

    int startId = id[start.first * W + start.second];
    int s = comp[startId];
    sat.forceTrue(TwoSAT::varTrue(s));
    for (int i = 0; i < sccCnt; ++i) if (!reach[s].test(i)) sat.forceFalse(TwoSAT::varTrue(i));

    // Incomparable pairs cannot both be visited: (¬Ai ∨ ¬Aj)
    for (int i = 0; i < sccCnt; ++i) {
        for (int j = i + 1; j < sccCnt; ++j) {
            if (!reach[i].test(j) && !reach[j].test(i)) {
                sat.addOr(TwoSAT::varFalse(i), TwoSAT::varFalse(j));
            }
        }
    }

    // For each star, must visit vertical or horizontal stopping SCC
    for (auto [r, c] : stars) {
        int v = id[r * W + c];
        int vVert = comp[mv[v][0]];
        int vHori = comp[mv[v][1]];
        sat.addOr(TwoSAT::varTrue(vVert), TwoSAT::varTrue(vHori));
    }

    cout << (sat.satisfiable() ? "YES\n" : "NO\n");
    return 0;
}
```

### 복잡도
- SCC 구성: 정점 V ≤ 2500, 간선 E ≤ 4V, `O(V+E)`.
- DAG 도달성: 비트셋 DP로 `O(S · (S/word) + E_DAG · (S/word))` 수준. S ≤ 2500이면 충분히 빠름.
- 2-SAT: 노드 2S, 간선 O(제약 수), Kosaraju로 `O(S + M)`.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 풀이 정리: [JusticeHui - BOJ14737 Dev, Please Add This!](https://justicehui.github.io/ps/2020/09/29/BOJ14737/)


