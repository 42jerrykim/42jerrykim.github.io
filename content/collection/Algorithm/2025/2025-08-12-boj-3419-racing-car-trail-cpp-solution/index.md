---
title: "[Algorithm] C++ 백준 3419번 : Racing Car Trail"
description: "백준 3419 Racing Car Trail을 격자 그래프의 이분 그래프로 모델링해 Hopcroft–Karp 최대 매칭과 Dulmage–Mendelsohn 도달성으로 각 시작 칸의 승패(A/B)를 판정합니다. O(E√V) 매칭과 O(V+E) 마킹으로 빠르게 처리하며, 구현 디테일과 복잡도까지 정리."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "3419"
- "Racing Car Trail"
- "레이싱 카 트레일"
- "Tron"
- "Game"
- "게임"
- "Game Theory"
- "게임이론"
- "Graph"
- "그래프"
- "Grid"
- "격자"
- "Bipartite Graph"
- "이분 그래프"
- "Bipartite Matching"
- "이분 매칭"
- "Maximum Matching"
- "최대매칭"
- "Minimum Vertex Cover"
- "최소 정점 커버"
- "Konig's Theorem"
- "쾨니그 정리"
- "Hopcroft-Karp"
- "홉크로프트 카프"
- "Dulmage-Mendelsohn"
- "DM Decomposition"
- "Alternating Paths"
- "증대 경로"
- "Augmenting Path"
- "Parity"
- "격자 패리티"
- "게임 그래프"
- "Impartial Game"
- "Brute Force"
- "구현"
- "Implementation"
- "C++"
- "CPP"
- "STL"
- "ios::sync_with_stdio(false)"
- "cin.tie(nullptr)"
- "Time Complexity"
- "Space Complexity"
- "시간복잡도"
- "공간복잡도"
- "O(E*sqrt(V))"
- "O(V+E)"
- "Algorithm"
- "알고리즘"
- "문제풀이"
- "풀이"
- "해설"
- "코딩테스트"
- "Competitive Programming"
- "CP"
image: "wordcloud.png"
---

백준 문제 [Racing Car Trail (3419)](https://www.acmicpc.net/problem/3419)은 장애물이 있는 \"격자(Grid)\" 위에서 한 칸씩 번갈아 이동하며 자기 궤적을 다시 밟으면 지는 게임입니다. 각 시작 칸에서 최적 플레이 시 누가 이기는지 출력합니다.

### 문제 요약
- 입력: `N x E` 격자(`.` 빈칸, `X` 장애물), 여러 테스트케이스, 마지막 `0 0`.
- 출력: 각 칸에서 시작할 때 승자 `A`(Alice) 또는 `B`(Bob), 장애물은 `X`.

### 핵심 아이디어
- 빈 칸을 패리티 `(i+j)`로 이분화해 그래프를 구성합니다.
- Hopcroft–Karp로 최대 매칭을 구한 뒤, DM 스타일의 교대 경로 도달성으로 \"일부 최대 매칭에서 자유로울 수 있는 정점\"(freeable)을 판정합니다.
- 시작 칸이 freeable이면 선공(Alice)이 이길 수 없으므로 `B`, 아니면 `A`입니다.

### C++ 풀이

```cpp
// 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct HopcroftKarp {
  int nLeft, nRight;
  vector<vector<int>> adj;
  vector<int> pairU, pairV, dist;

  HopcroftKarp(int leftSize, int rightSize)
      : nLeft(leftSize), nRight(rightSize),
        adj(leftSize), pairU(leftSize, -1), pairV(rightSize, -1),
        dist(leftSize, -1) {}

  void addEdge(int u, int v) { adj[u].push_back(v); }

  bool bfs() {
    queue<int> q;
    for (int u = 0; u < nLeft; ++u) {
      if (pairU[u] == -1) {
        dist[u] = 0;
        q.push(u);
      } else {
        dist[u] = -1;
      }
    }
    bool reachableFreeV = false;
    while (!q.empty()) {
      int u = q.front(); q.pop();
      for (int v : adj[u]) {
        int matchedU = pairV[v];
        if (matchedU != -1 && dist[matchedU] == -1) {
          dist[matchedU] = dist[u] + 1;
          q.push(matchedU);
        }
        if (matchedU == -1) reachableFreeV = true;
      }
    }
    return reachableFreeV;
  }

  bool dfs(int u) {
    for (int v : adj[u]) {
      int matchedU = pairV[v];
      if (matchedU == -1 || (dist[matchedU] == dist[u] + 1 && dfs(matchedU))) {
        pairU[u] = v;
        pairV[v] = u;
        return true;
      }
    }
    dist[u] = -1;
    return false;
  }

  int maxMatching() {
    int matching = 0;
    while (bfs()) {
      for (int u = 0; u < nLeft; ++u) {
        if (pairU[u] == -1 && dfs(u)) ++matching;
      }
    }
    return matching;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int N, E; // N: rows, E: cols
  while (cin >> N >> E) {
    if (N == 0 && E == 0) break;
    vector<string> grid(N);
    for (int i = 0; i < N; ++i) cin >> grid[i];

    vector<vector<int>> idU(N, vector<int>(E, -1));
    vector<vector<int>> idV(N, vector<int>(E, -1));
    int uCount = 0, vCount = 0;

    for (int i = 0; i < N; ++i) {
      for (int j = 0; j < E; ++j) {
        if (grid[i][j] != '.') continue;
        if (((i + j) & 1) == 0) idU[i][j] = uCount++;
        else idV[i][j] = vCount++;
      }
    }

    HopcroftKarp hk(uCount, vCount);
    vector<vector<int>> adjV(vCount);

    auto inb = [&](int r, int c) {
      return (r >= 0 && r < N && c >= 0 && c < E);
    };
    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};

    for (int i = 0; i < N; ++i) {
      for (int j = 0; j < E; ++j) {
        if (grid[i][j] != '.') continue;
        if (((i + j) & 1) == 0) {
          int u = idU[i][j];
          for (int d = 0; d < 4; ++d) {
            int ni = i + dr[d], nj = j + dc[d];
            if (!inb(ni, nj) || grid[ni][nj] != '.') continue;
            int v = idV[ni][nj];
            if (v != -1) {
              hk.addEdge(u, v);
              adjV[v].push_back(u);
            }
          }
        }
      }
    }

    hk.maxMatching();

    // Uplus: U reachable from free U by alternating paths
    vector<char> Uplus(uCount, false), Vseen1(vCount, false);
    {
      queue<int> qu;
      for (int u = 0; u < uCount; ++u) if (hk.pairU[u] == -1) { Uplus[u] = true; qu.push(u); }
      while (!qu.empty()) {
        int u = qu.front(); qu.pop();
        for (int v : hk.adj[u]) {
          if (hk.pairU[u] != v && !Vseen1[v]) { // unmatched U->V
            Vseen1[v] = true;
            int mu = hk.pairV[v];
            if (mu != -1 && !Uplus[mu]) { Uplus[mu] = true; qu.push(mu); }
          }
        }
      }
    }

    // Vminus: V reachable from free V by alternating paths
    vector<char> Vminus(vCount, false), Useen2(uCount, false);
    {
      queue<int> qv;
      for (int v = 0; v < vCount; ++v) if (hk.pairV[v] == -1) { Vminus[v] = true; qv.push(v); }
      while (!qv.empty()) {
        int v = qv.front(); qv.pop();
        for (int u : adjV[v]) {
          if (hk.pairV[v] != u && !Useen2[u]) { // unmatched V->U
            Useen2[u] = true;
            int mv = hk.pairU[u];
            if (mv != -1 && !Vminus[mv]) { Vminus[mv] = true; qv.push(mv); }
          }
        }
      }
    }

    vector<string> out(N, string(E, 'X'));
    for (int i = 0; i < N; ++i) {
      for (int j = 0; j < E; ++j) {
        if (grid[i][j] == 'X') { out[i][j] = 'X'; continue; }
        if (((i + j) & 1) == 0) {
          int u = idU[i][j];
          bool freeable = Uplus[u];
          out[i][j] = freeable ? 'B' : 'A';
        } else {
          int v = idV[i][j];
          bool freeable = Vminus[v];
          out[i][j] = freeable ? 'B' : 'A';
        }
      }
    }

    for (int i = 0; i < N; ++i) cout << out[i] << '\n';
    cout << '\n';
  }
  return 0;
}
```

### 복잡도
- 매칭: `O(E · √V)`
- 도달성 마킹: `O(V + E)`

### 참고
- 문제: [BOJ 3419](https://www.acmicpc.net/problem/3419)


