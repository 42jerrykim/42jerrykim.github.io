---
title: "[Algorithm] C++ 백준 7907번 : Bytean Road Race"
description: "Bytean Road Race(백준 7907)을 동/남 방향 격자 DAG로 모델링해 두 정점 p, q를 모두 지나는 경로 존재 여부를 O(1)로 판별하는 C++ 풀이. 동우선·남우선 위상정렬 두 랭크 비교와 O(N+M) 전처리로 빠르고 안정적인 질의 응답을 제공합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "7907"
- "Bytean Road Race"
- "Bytean"
- "Road"
- "Race"
- "AMPPZ"
- "AMPPZ 2011"
- "ICPC"
- "그래프"
- "Graph"
- "DAG"
- "위상정렬"
- "Topological Sort"
- "두 위상순서"
- "Left-Right Order"
- "st-planar"
- "planar DAG"
- "grid graph"
- "격자 그래프"
- "east first"
- "south first"
- "동우선"
- "남우선"
- "rank compare"
- "질의 처리"
- "Query"
- "O(1) query"
- "선형 전처리"
- "O(N+M)"
- "좌표"
- "x좌표"
- "y좌표"
- "유향 그래프"
- "Directed Graph"
- "경로 존재"
- "Reachability"
- "Partial Order"
- "부분순서"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "메모리"
- "Memory"
- "구현"
- "Implementation"
- "해설"
- "Editorial"
- "문제해설"
- "코딩테스트"
- "Competitive Programming"
- "정답률"
image: "wordcloud.png"
---

문제: [BOJ 7907 - Bytean Road Race](https://www.acmicpc.net/problem/7907)

### 아이디어 요약
- 격자 위 동/남 방향 간선만 존재하는 DAG입니다. 두 정점 `p`, `q`를 모두 지나는 경로가 존재하려면, 한쪽이 다른 쪽보다 항상 앞서는 순서 관계여야 합니다.
- 이를 위해 위상정렬을 두 번 만듭니다: 오른쪽(동) 우선 DFS와 아래(남) 우선 DFS. 각 정점의 두 위상 순위 `ordR`, `ordL`을 기록합니다.
- `ordR[p] < ordR[q]`와 `ordL[p] < ordL[q]`가 모두 참이면 `p → q` 경로 존재, 반대로 두 조건이 모두 `q`가 앞서면 `q → p` 경로 존재. 둘 다 아니면 어떤 경로로도 두 정점을 모두 지날 수 없습니다.
- 전처리 `O(N+M)`(두 번의 DFS), 질의당 `O(1)`(두 랭크 비교).

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct EdgeDir {
  int east = 0;  // neighbor to the east (x increases)
  int south = 0; // neighbor to the south (y decreases)
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m, k;
  if (!(cin >> n >> m >> k)) return 0;

  vector<long long> x(n + 1), y(n + 1);
  for (int i = 1; i <= n; ++i) cin >> x[i] >> y[i];

  vector<EdgeDir> g(n + 1);

  for (int i = 0; i < m; ++i) {
    int a, b; cin >> a >> b;
    if (x[a] == x[b]) {
      // vertical: from higher y to lower y (south)
      if (y[a] > y[b]) g[a].south = b;
      else g[b].south = a;
    } else {
      // horizontal: from smaller x to larger x (east)
      if (x[a] < x[b]) g[a].east = b;
      else g[b].east = a;
    }
  }

  auto topo_with_preference = [&](bool preferEast) {
    vector<int> order; order.reserve(n);
    vector<char> vis(n + 1, 0);
    struct Frame { int u, state; }; // state: 0 -> first, 1 -> second, 2 -> finish
    vector<Frame> st;
    // Problem guarantees every node is reachable from 1
    st.push_back({1, 0});
    vis[1] = 1;

    while (!st.empty()) {
      Frame &fr = st.back();
      int u = fr.u;
      int firstN = preferEast ? g[u].east : g[u].south;
      int secondN = preferEast ? g[u].south : g[u].east;

      if (fr.state == 0) {
        fr.state = 1;
        if (firstN && !vis[firstN]) { vis[firstN] = 1; st.push_back({firstN, 0}); }
        continue;
      }
      if (fr.state == 1) {
        fr.state = 2;
        if (secondN && !vis[secondN]) { vis[secondN] = 1; st.push_back({secondN, 0}); }
        continue;
      }
      // finish
      order.push_back(u);
      st.pop_back();
    }

    // reverse postorder -> topological order
    reverse(order.begin(), order.end());
    vector<int> rank(n + 1, 0);
    for (int i = 0; i < (int)order.size(); ++i) rank[order[i]] = i + 1;
    return rank;
  };

  // Right-first (east first), Left-first (south first)
  vector<int> ordR = topo_with_preference(true);
  vector<int> ordL = topo_with_preference(false);

  while (k--) {
    int p, q; cin >> p >> q;
    bool pBeforeQ = (ordR[p] < ordR[q]) && (ordL[p] < ordL[q]);
    bool qBeforeP = (ordR[q] < ordR[p]) && (ordL[q] < ordL[p]);
    cout << (pBeforeQ || qBeforeP ? "TAK" : "NIE") << '\n';
  }
  return 0;
}
```

### 복잡도
- 전처리: `O(N+M)` (두 번의 DFS 위상정렬)
- 질의: `O(1)` (두 랭크 비교)

### 참고
- 문제: `https://www.acmicpc.net/problem/7907`
- 아이디어: 위상정렬을 서로 다른 우선순위로 두 번 만들어 순위 쌍을 비교


