---
title: "[Algorithm] BOJ 14960 - Strongly Matchable C++ 풀이 - 충돌그래프+HK"
description: "BOJ 14960 Strongly Matchable을 그래프 이론 관점에서 정리. Hall 정리 기반 조건을 ‘충돌 이분 그래프’로 환원하고, Kőnig 정리(α=|V|-ν)와 Hopcroft–Karp로 최대 독립집합 크기를 구해 강매칭성 여부를 판별하는 실전 C++ 풀이."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "14960"
- "Strongly Matchable"
- "강매칭성"
- "Graph Theory"
- "그래프 이론"
- "Matching"
- "매칭"
- "Perfect Matching"
- "완전 매칭"
- "Hall's Theorem"
- "홀의 결혼 정리"
- "Kőnig's Theorem"
- "쾨니그 정리"
- "Maximum Matching"
- "최대 매칭"
- "Maximum Independent Set"
- "최대 독립집합"
- "Bipartite Graph"
- "이분 그래프"
- "Hopcroft–Karp"
- "Hopcroft-Karp"
- "HK"
- "Network Flow"
- "네트워크 플로우"
- "Kőnig–Egerváry"
- "코니그 에게르바리"
- "Independent Set"
- "독립집합"
- "Complement"
- "여그래프"
- "Reduction"
- "환원"
- "Constructive"
- "구성적"
- "Proof Sketch"
- "증명 개요"
- "Algorithm Design"
- "알고리즘 설계"
- "Complexity"
- "시간복잡도"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Implementation"
- "구현"
- "ICPC"
- "대전 리저널"
- "2017 Daejeon"
- "조합론"
- "Combinatorics"
- "Cut Condition"
- "절단 조건"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 14960 - Strongly Matchable](https://www.acmicpc.net/problem/14960)

### 아이디어 요약
- 그래프 `G`가 strongly matchable 이려면, 모든 `|S|=|T|=n/2` 분할에 대해 `S-T` 간의 완전 매칭이 존재해야 합니다.
- 다음과 같은 필요충분 조건을 사용할 수 있습니다: 서로 간선이 전혀 없는 서로소 집합 `(A, B)`가 존재해 `|A| + |B| > n/2`이면, 어떤 분할에서는 Hall 조건이 깨져 완전 매칭이 존재하지 않습니다. 반대로 그런 `(A,B)`가 전혀 없다면 모든 분할에서 완전 매칭이 존재합니다.
- 이를 체크하기 위해 “충돌 이분 그래프” `H'`를 만듭니다.
  - 좌측 정점 `L[i]`는 "정점 i를 A에 넣기", 우측 정점 `R[j]`는 "정점 j를 B에 넣기"를 의미.
  - 간선: `(L[i], R[i])`(A와 B는 교집합 불가), 그리고 `G`의 모든 간선 `(u,v)`에 대해 `(L[u], R[v])`, `(L[v], R[u])`(A와 B 사이에 원래 간선이 있으면 불가).
  - 그러면 `H'`에서의 독립집합은 정확히 “서로 간선 없는 `(A,B)`”에 해당하며, 그 크기는 `|A|+|B|`.
- 이분 그래프의 최대 독립집합 크기 `α`는 `α = |V(H')| - ν`(최대 매칭) 이므로, Hopcroft–Karp로 `ν`를 구해 `α`를 얻을 수 있습니다.
- 단, `α`는 한쪽만 고르는 해(예: 전부 `L`)도 허용하므로 “양쪽 모두 비어있지 않은” 해가 필요한 경우를 별도로 확인합니다. 이를 위해 가능한 `(i,j)` 쌍에 대해 `L[i]`와 `R[j]`를 강제로 포함시키고, 그 이웃을 제거한 잔여 그래프에서 최대 독립집합을 다시 구해 `|A|+|B| > n/2`인지 검사합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct HopcroftKarp {
    int nL, nR;
    const vector<vector<int>> &adj; // adj[u] -> list of right nodes v
    const vector<bool> *allowL, *allowR;
    vector<int> dist, pairU, pairV;

    HopcroftKarp(int nLeft, int nRight, const vector<vector<int>> &adjRef)
        : nL(nLeft), nR(nRight), adj(adjRef),
          dist(nLeft), pairU(nLeft, -1), pairV(nRight, -1) {}

    bool bfs() {
        queue<int> q;
        for (int u = 0; u < nL; ++u) {
            if (!(*allowL)[u]) { dist[u] = -1; continue; }
            if (pairU[u] == -1) { dist[u] = 0; q.push(u); }
            else dist[u] = -1;
        }
        bool reachableFreeRight = false;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (!(*allowR)[v]) continue;
                int w = pairV[v];
                if (w != -1 && (*allowL)[w]) {
                    if (dist[w] == -1) {
                        dist[w] = dist[u] + 1;
                        q.push(w);
                    }
                } else if (w == -1) {
                    reachableFreeRight = true;
                }
            }
        }
        return reachableFreeRight;
    }

    bool dfs(int u) {
        for (int v : adj[u]) {
            if (!(*allowR)[v]) continue;
            int w = pairV[v];
            if (w == -1 || ((*allowL)[w] && dist[w] == dist[u] + 1 && dfs(w))) {
                pairU[u] = v;
                pairV[v] = u;
                return true;
            }
        }
        dist[u] = -1;
        return false;
    }

    int maxMatchingWithAllowed(const vector<bool> &allowedLeft, const vector<bool> &allowedRight) {
        allowL = &allowedLeft;
        allowR = &allowedRight;
        fill(pairU.begin(), pairU.end(), -1);
        fill(pairV.begin(), pairV.end(), -1);
        int matching = 0;
        while (bfs()) {
            for (int u = 0; u < nL; ++u) {
                if ((*allowL)[u] && pairU[u] == -1) {
                    if (dfs(u)) ++matching;
                }
            }
        }
        return matching;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<vector<int>> G(n, vector<int>(n, 0));
    for (int i = 0; i < m; ++i) {
        int u, v; cin >> u >> v; --u; --v;
        if (u == v) continue;
        G[u][v] = G[v][u] = 1;
    }

    // Build conflict bipartite graph H'
    // Left: 0..n-1, Right: 0..n-1
    vector<vector<int>> adjL(n);
    vector<vector<int>> adjR(n); // reverse neighbors for quick neighbor removal
    // (L[i], R[i])
    for (int i = 0; i < n; ++i) {
        adjL[i].push_back(i);
        adjR[i].push_back(i);
    }
    // (L[u], R[v]) if (u, v) in G
    for (int u = 0; u < n; ++u) {
        for (int v = u + 1; v < n; ++v) {
            if (G[u][v]) {
                adjL[u].push_back(v);
                adjR[v].push_back(u);
                adjL[v].push_back(u);
                adjR[u].push_back(v);
            }
        }
    }

    HopcroftKarp hk(n, n, adjL);

    // Case 1: maximum independent set size (no constraint) = 2n - maxMatching
    vector<bool> allL(n, true), allR(n, true);
    int mm_all = hk.maxMatchingWithAllowed(allL, allR);
    int alpha_all = 2 * n - mm_all;
    if (alpha_all <= n / 2) {
        cout << 1 << '\n';
        return 0;
    }

    // Case 2: enforce both sides non-empty
    int best_both = 0;
    vector<bool> allowL(n), allowR(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            // We can include L[i] and R[j] only if they are NOT adjacent in conflict graph:
            // i != j and (i, j) NOT an edge in G
            if (i == j || G[i][j]) continue;

            fill(allowL.begin(), allowL.end(), true);
            fill(allowR.begin(), allowR.end(), true);

            // Include L[i] and R[j] => remove them and all their neighbors
            allowL[i] = false; // L[i] itself removed from residual (we count +1 manually)
            allowR[j] = false; // R[j] itself removed from residual (we count +1 manually)
            // Remove neighbors of L[i] on Right
            for (int v : adjL[i]) allowR[v] = false;
            // Remove neighbors of R[j] on Left
            for (int u : adjR[j]) allowL[u] = false;

            int cntAllowed = (int)count(allowL.begin(), allowL.end(), true)
                           + (int)count(allowR.begin(), allowR.end(), true);
            int mm_res = hk.maxMatchingWithAllowed(allowL, allowR);
            int alpha_res = cntAllowed - mm_res;   // max ind. set on residual
            int alpha_candidate = 2 + alpha_res;   // +L[i] +R[j]
            if (alpha_candidate > best_both) best_both = alpha_candidate;

            if (best_both > n / 2) {
                cout << -1 << '\n';
                return 0;
            }
        }
    }

    cout << (best_both > n / 2 ? -1 : 1) << '\n';
    return 0;
}
```

### 복잡도
- `H'` 정점 수 `2n`, 간선 수 `n + 2m`. Hopcroft–Karp `O(E\sqrt{V})`. 강제 포함 쌍은 최악 `O(n^2)`개이지만 `n ≤ 100`에서 충분히 빠릅니다.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`


