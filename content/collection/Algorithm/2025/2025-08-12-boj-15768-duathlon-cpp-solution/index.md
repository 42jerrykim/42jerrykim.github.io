---
title: "[Algorithm] C++ 백준 15768번 - Duathlon"
description: "APIO 2018 Duathlon(백준 15768) 문제를 Tarjan의 이중연결요소(BCC)와 Block-Cut Tree로 모델링하고, 보수계산으로 ‘불량’ 삼중쌍을 합산해 전체 경우에서 빼는 O(N+M) C++ 풀이를 정리합니다. 스택 기반 간선 추출, 서브트리 원소수 집계, 절단점-블록 기여 계산, 64비트 오버플로 주의, 샘플 검증과 빌드/실행 방법까지 포함."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "15768"
- "Duathlon"
- "APIO"
- "APIO 2018"
- "그래프"
- "Graph"
- "BCC"
- "Biconnected Components"
- "이중연결요소"
- "Block-Cut Tree"
- "Block Cut Tree"
- "BCT"
- "Articulation Point"
- "절단점"
- "Tarjan"
- "타잔"
- "Complementary Counting"
- "보수계산"
- "Counting"
- "경로"
- "Path"
- "Tree"
- "트리"
- "Forest"
- "Block-Cut Forest"
- "서브트리"
- "Subtree"
- "Edge Stack"
- "스택"
- "DFS"
- "깊이우선탐색"
- "O(N+M)"
- "시간복잡도"
- "Complexity"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Implementation"
- "구현"
- "문제해설"
- "해설"
- "Editorial"
- "에디토리얼"
- "ICPC"
- "Olympiad"
- "APIO P3"
- "카운팅"
- "조합론"
- "64-bit"
- "오버플로"
- "Block"
- "Cut"
- "Component Graph"
- "Block Graph"
- "BCC Tree"
- "2-Connected"
image: "wordcloud.png"
---

문제: [BOJ 15768 - Duathlon](https://www.acmicpc.net/problem/15768)

### 아이디어 요약
- 전체 순서 있는 삼중쌍 `(s, c, f)`의 개수에서 “불가능한(triply bad)” 삼중쌍 수를 빼는 보수계산을 사용합니다.
- Tarjan으로 이중연결요소(BCC)를 구해 원 그래프의 정점들과 BCC 노드로 이루어진 Block-Cut Tree(포리스트)를 구성합니다.
- 어떤 절단점 `P`에 대해, 인접한 각 BCC `B` 방향으로 `P`를 제거했을 때의 서브트리 내 원래 정점 수 `S(P→B)`를 구합니다.
- `c`가 `B`에 있고(`|B|-1` 가지, 절단점 `P` 제외), `s,f`가 모두 다른 가지 쪽에 있을 때 불량 삼중쌍이 됩니다. 이를 모든 `(P,B)`에 대해 합산합니다.
- 연결 성분별 전체 삼중쌍 수는 성분 내 원래 정점 수 `N`에 대해 `N*(N-1)*(N-2)`입니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Edge { int to; int id; };

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m;
  if (!(cin >> n >> m)) return 0;

  vector<vector<Edge>> graph(n + 1);
  vector<int> U(m + 1), V(m + 1);
  for (int i = 1; i <= m; ++i) {
    int a, b; cin >> a >> b;
    U[i] = a; V[i] = b;
    graph[a].push_back({b, i});
    graph[b].push_back({a, i});
  }

  // Tarjan BCC -> Block-Cut Tree
  vector<int> disc(n + 1, 0), low(n + 1, 0);
  int timer = 0;
  vector<int> edgeStack; edgeStack.reserve(m);
  vector<vector<int>> bcAdj(n + m + 5);
  vector<int> bSize(n + m + 5, 0);
  vector<int> mark(n + 1, 0);
  int markTick = 1;
  int bccCnt = 0;

  function<void(int,int)> dfs = [&](int u, int peid) {
    disc[u] = low[u] = ++timer;
    for (const auto &e : graph[u]) {
      int v = e.to, eid = e.id;
      if (eid == peid) continue;
      if (!disc[v]) {
        edgeStack.push_back(eid);
        dfs(v, eid);
        low[u] = min(low[u], low[v]);
        if (low[v] >= disc[u]) {
          ++bccCnt; int bNode = n + bccCnt;
          vector<int> compVerts;
          while (true) {
            int ce = edgeStack.back(); edgeStack.pop_back();
            int a = U[ce], b = V[ce];
            if (mark[a] != markTick) { mark[a] = markTick; compVerts.push_back(a); }
            if (mark[b] != markTick) { mark[b] = markTick; compVerts.push_back(b); }
            if (ce == eid) break;
          }
          ++markTick;
          bSize[bNode] = (int)compVerts.size();
          for (int x : compVerts) {
            bcAdj[x].push_back(bNode);
            bcAdj[bNode].push_back(x);
          }
        }
      } else if (disc[v] < disc[u]) {
        edgeStack.push_back(eid);
        low[u] = min(low[u], disc[v]);
      }
    }
  };

  for (int i = 1; i <= n; ++i) if (!disc[i]) dfs(i, 0);

  int totalNodes = n + bccCnt;

  // Tree DP on Block-Cut Forest
  vector<int> parent(totalNodes + 1, -1);
  vector<int> compId(totalNodes + 1, -1);
  vector<int64> subOrig(totalNodes + 1, 0);
  vector<int64> compOrigSum; compOrigSum.reserve(totalNodes + 1);
  int compCnt = 0;

  function<void(int,int,int)> dfsTree = [&](int u, int p, int cid) {
    parent[u] = p; compId[u] = cid;
    subOrig[u] = (u <= n ? 1LL : 0LL);
    for (int v : bcAdj[u]) if (v != p) { dfsTree(v, u, cid); subOrig[u] += subOrig[v]; }
  };

  vector<char> visited(totalNodes + 1, 0);
  for (int u = 1; u <= totalNodes; ++u) if (!visited[u]) {
    vector<int> nodes; queue<int> q; q.push(u); visited[u] = 1;
    while (!q.empty()) { int x = q.front(); q.pop(); nodes.push_back(x);
      for (int v : bcAdj[x]) if (!visited[v]) { visited[v] = 1; q.push(v); } }
    dfsTree(u, -1, compCnt);
    compOrigSum.push_back(subOrig[u]);
    ++compCnt;
  }

  // total ordered triples per connected component
  int64 totalOrderedTriples = 0;
  for (int id = 0; id < compCnt; ++id) {
    int64 N = compOrigSum[id];
    if (N >= 3) totalOrderedTriples += N * (N - 1) * (N - 2);
  }

  auto sideSize = [&](int P, int B) -> int64 {
    if (parent[B] == P) return subOrig[B];
    if (parent[P] == B) return compOrigSum[compId[P]] - subOrig[P];
    return subOrig[B];
  };

  long long bad = 0;
  for (int P = 1; P <= n; ++P) {
    if (bcAdj[P].empty()) continue;
    int64 sum1 = 0, sum2 = 0; vector<int64> S; S.reserve(bcAdj[P].size());
    for (int B : bcAdj[P]) { int64 s = sideSize(P, B); S.push_back(s); sum1 += s; sum2 += s * s; }
    for (size_t i = 0; i < bcAdj[P].size(); ++i) {
      int B = bcAdj[P][i]; int64 w = (int64)bSize[B] - 1; if (w <= 0) continue;
      int64 sB = S[i]; int64 other1 = sum1 - sB; int64 other2 = sum2 - sB * sB;
      bad += w * (other2 + other1);
    }
  }

  cout << (totalOrderedTriples - bad) << '\n';
  return 0;
}
```

### 복잡도
- 시간: `O(N + M)` (BCC 추출 + Block-Cut Tree 구성 + 트리 DP + 인접 순회)
- 공간: `O(N + M)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고자료
- USACO Guide: [Solution - Duathlon (APIO 2018)](https://usaco.guide/problems/apio-2018duathlon/solution)
- GitHub(Ava Pun): [apio18p3.cpp](https://github.com/AvaLovelace1/competitive-programming/blob/master/solutions/apio/apio18p3.cpp)


