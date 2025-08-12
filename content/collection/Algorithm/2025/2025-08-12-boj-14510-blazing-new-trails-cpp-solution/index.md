---
title: "[BOJ] Blazing New Trails (14510) - C++ 풀이"
description: "특수/일반 노드 간 교차 간선을 정확히 w개 포함하는 최소 스패닝 트리. 라그랑주 가중치로 교차 간선에 x를 더해 크루스칼을 돌리고, 이분 탐색으로 w를 맞춘 뒤 비용'에서 x·w를 빼 원래 최소 비용을 복원한다. 정렬 1회, 탐색 중 두 포인터 병합으로 빠르게 처리."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "14510"
- "Blazing New Trails"
- "NAIPC 2017"
- "NAIPC"
- "North American Invitational Programming Contest"
- "MST"
- "Minimum Spanning Tree"
- "Spanning Tree"
- "Kruskal"
- "Union-Find"
- "Disjoint Set Union"
- "DSU"
- "Lagrangian"
- "라그랑주"
- "Parametric Search"
- "Binary Search"
- "이분 탐색"
- "Penalty Method"
- "Cross Edge"
- "교차 간선"
- "Special"
- "특수 노드"
- "Regular"
- "일반 노드"
- "Edge Classification"
- "간선 분류"
- "Greedy"
- "그리디"
- "Graph"
- "그래프"
- "Algorithm"
- "알고리즘"
- "Proof"
- "증명"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Time Complexity"
- "시간복잡도"
- "Solution Code"
- "정답 코드"
- "Editorial"
- "문제해설"
- "해설"
- "ICPC"
- "Open Cup"
- "Grand Prix of America"
- "Stage 16"
- "Minimum Cost"
- "최소 비용"
- "Network Design"
- "네트워크 설계"
- "Spanning"
- "트리"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 14510 - Blazing New Trails](https://www.acmicpc.net/problem/14510)

### 아이디어 요약
- **조건**: 정확히 하나의 경로(스패닝 트리), 그리고 **특수-일반 간선이 정확히 w개**.
- **라그랑주 완화**: 특수-일반(교차) 간선에 비용 `+x`를 더해 비용'으로 크루스칼을 수행하면, 선택되는 교차 간선 수 `f(x)`는 단조 비증가. 충분히 작은 `x`에선 교차 간선을 최대화, 큰 `x`에선 최소화.
- **이분 탐색**: `x`를 이분 탐색하여 어떤 `x`에서 `f_min(x) ≤ w ≤ f_max(x)`가 되면, 모든 MST의 비용' 합은 동일하며 원래 비용은 `sum' − x·w`로 복원 가능.
- **구현 팁**:
  - 간선을 교차(`special^regular`)와 비교차로 분리해 각각 비용 오름차순 정렬은 한 번만 수행.
  - 매 탐색 단계에서 두 포인터 병합 방식으로 `min(c_same, c_cross + x)`를 비교하며 크루스칼.
  - 극단 `x`로 가능한 교차 간선 수 범위 밖이면 불가능 `-1`.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> parent, rnk;
    DSU(int n = 0) { init(n); }
    void init(int n) {
        parent.resize(n + 1);
        rnk.assign(n + 1, 0);
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
        if (rnk[a] < rnk[b]) swap(a, b);
        parent[b] = a;
        if (rnk[a] == rnk[b]) rnk[a]++;
        return true;
    }
};

struct Edge { int u, v, c; };

struct RunResult {
    bool valid;
    int usedCross;
    long long sumPrime; // sum of (c + x * isCross)
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, k, w;
    if (!(cin >> n >> m >> k >> w)) return 0;

    vector<char> isSpecial(n + 1, 0);
    for (int i = 0; i < k; ++i) {
        int s; cin >> s;
        isSpecial[s] = 1;
    }

    vector<Edge> crossEdges, sameEdges;
    crossEdges.reserve(m); sameEdges.reserve(m);
    vector<pair<int,int>> allForConn; allForConn.reserve(m);

    for (int i = 0; i < m; ++i) {
        int a, b, c; cin >> a >> b >> c;
        bool cross = (isSpecial[a] ^ isSpecial[b]);
        if (cross) crossEdges.push_back({a, b, c});
        else sameEdges.push_back({a, b, c});
        allForConn.push_back({a, b});
    }

    // Connectivity quick check
    {
        DSU dsu(n);
        for (auto &p : allForConn) dsu.unite(p.first, p.second);
        int root = dsu.find(1);
        for (int i = 2; i <= n; ++i) if (dsu.find(i) != root) { cout << -1 << '\n'; return 0; }
    }

    sort(crossEdges.begin(), crossEdges.end(), [](const Edge& a, const Edge& b){ return a.c < b.c; });
    sort(sameEdges.begin(), sameEdges.end(), [](const Edge& a, const Edge& b){ return a.c < b.c; });

    auto run = [&](int x, bool wantMaxCross) -> RunResult {
        DSU dsu(n);
        int i = 0, j = 0, cnt = 0, usedCross = 0;
        long long sumPrime = 0;
        const int S = (int)sameEdges.size();
        const int C = (int)crossEdges.size();
        while (cnt < n - 1 && (i < S || j < C)) {
            bool takeCross = false;
            if (i >= S) takeCross = true;
            else if (j >= C) takeCross = false;
            else {
                long long ks = sameEdges[i].c;
                long long kc = (long long)crossEdges[j].c + (long long)x;
                if (ks < kc) takeCross = false;
                else if (ks > kc) takeCross = true;
                else takeCross = wantMaxCross; // tie-break
            }
            if (!takeCross) {
                const Edge &e = sameEdges[i++];
                if (dsu.unite(e.u, e.v)) { cnt++; sumPrime += e.c; }
            } else {
                const Edge &e = crossEdges[j++];
                if (dsu.unite(e.u, e.v)) { cnt++; usedCross++; sumPrime += (long long)e.c + (long long)x; }
            }
        }
        if (cnt != n - 1) return {false, 0, 0};
        return {true, usedCross, sumPrime};
    };

    const int INF_X = 200000; // safely beyond max edge cost
    RunResult extremeMax = run(-INF_X, true);   // cross edges cheap -> maximize cross count
    RunResult extremeMin = run(+INF_X, false);  // cross edges expensive -> minimize cross count
    if (!extremeMax.valid || !extremeMin.valid) { cout << -1 << '\n'; return 0; }
    if (w < extremeMin.usedCross || w > extremeMax.usedCross) { cout << -1 << '\n'; return 0; }

    long long answer = -1;
    int lo = -INF_X, hi = INF_X;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        RunResult rMax = run(mid, true);
        RunResult rMin = run(mid, false);
        if (!rMax.valid || !rMin.valid) { cout << -1 << '\n'; return 0; }
        if (rMin.usedCross <= w && w <= rMax.usedCross) {
            answer = rMax.sumPrime - (long long)mid * (long long)w; // any MST' works
            break;
        }
        if (rMax.usedCross < w) hi = mid - 1; else lo = mid + 1;
    }

    cout << answer << '\n';
    return 0;
}
```

### 복잡도
- 정렬 `O(m log m)` 1회. 이분 탐색 단계마다 크루스칼 병합은 `O(m α(n))`. 전체 `O(m log m + m α(n) log C)`.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`


