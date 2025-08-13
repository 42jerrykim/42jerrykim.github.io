---
title: "[Algorithm] C++ 백준 15521번 : Revenge of the Broken Door"
description: "백준 15521은 하나의 간선이 공사 중일 때 최악의 총 이동 거리를 최소화하는 경로를 구하는 문제입니다. T에서 다익스트라로 SPT를 만들고 비트리 간선을 HLD+세그로 경로 최소 갱신, 이분 탐색+Dijkstra로 최적 값을 구합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "15521"
- "Revenge of the Broken Door"
- "부서진 문의 복수"
- "JAG"
- "JAG 2017"
- "ICPC"
- "Practice Contest"
- "Graph"
- "그래프"
- "Shortest Path"
- "최단경로"
- "Dijkstra"
- "다익스트라"
- "SPT"
- "Shortest Path Tree"
- "최단경로트리"
- "Heavy-Light Decomposition"
- "HLD"
- "헤비라이트 분해"
- "Lowest Common Ancestor"
- "LCA"
- "최소공통조상"
- "Segment Tree"
- "세그먼트 트리"
- "Range Min"
- "Chmin"
- "RMQ"
- "Euler Tour"
- "오일러 투어"
- "Binary Search"
- "이분 탐색"
- "Parametric Search"
- "파라메트릭 서치"
- "Robust Path"
- "Worst Case"
- "최악 경우"
- "Adversarial"
- "Edge Failure"
- "간선 고장"
- "Single Edge Removal"
- "단일 간선 제거"
- "Replacement Paths"
- "대체 경로"
- "Non-tree Edge"
- "비트리 간선"
- "Cross Edge"
- "교차 간선"
- "Cut"
- "단절"
- "Graph Theory"
- "그래프 이론"
- "Algorithms"
- "알고리즘"
- "Competitive Programming"
- "컴페티티브 프로그래밍"
- "C++"
- "CPP"
- "GNU++17"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "O((N+M)logN logAns)"
- "경로 갱신"
- "경로 최소"
- "LCA 기반 갱신"
- "HLD path update"
- "최단거리 보정"
- "dist2"
- "SPT 대체거리"
- "Baekjoon 15521"
- "BOJ 15521"
- "문제풀이"
- "Solution Code"
- "정답 코드"
- "Tutorial"
- "해설"
image: "wordcloud.png"
---

문제: [BOJ 15521 - Revenge of the Broken Door](https://www.acmicpc.net/problem/15521)

### 아이디어 요약
- 한 간선이 공사 중일 때(시도 시 양 끝점에서만 알 수 있음) 최악의 총 이동 거리를 최소화하는 경로를 찾는다.
- `T`에서 다익스트라로 최단거리 `dist`와 최단경로트리(SPT)를 구성한다.
- 비트리 간선 `(u,v)`마다 `val = dist[u] + w(u,v) + dist[v]`를 계산하고, HLD로 `u→lca(u,v)`와 `v→lca(u,v)` 경로(LCa 제외)에 대해 구간 `chmin`을 수행하여 각 노드 `p`의 `minCrossSum[p]`를 얻는다.
- SPT 상향 간선 `p→parent[p]`의 대체 최단거리 `dist2(p,parent[p]) = minCrossSum[p] - dist[p]`, 그 외 방향은 `dist2(u,v) = dist[u]`로 해석한다.
- 답 `X`에 대해 이분 탐색하며, 간선을 사용할 때마다 "해당 간선이 막혔을 때의 최악 비용" 제약 `prefix + dist2(u,v) ≤ X`를 만족하는지 다익스트라 변형으로 판정한다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
static const int64 INF = (int64)4e18;

struct Edge { int u, v; int64 w; };
struct Adj { int to; int id; int64 w; };

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int N, M, S, T;
  if (!(cin >> N >> M >> S >> T)) return 0;

  vector<Edge> edges(M);
  vector<vector<Adj>> g(N + 1);
  for (int i = 0; i < M; ++i) {
    int u, v; int64 c;
    cin >> u >> v >> c;
    edges[i] = {u, v, c};
    g[u].push_back({v, i, c});
    g[v].push_back({u, i, c});
  }

  // 1) Dijkstra from T for dist[]
  vector<int64> dist(N + 1, INF);
  priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> pq;
  dist[T] = 0;
  pq.push({0, T});
  while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    if (d != dist[u]) continue;
    for (auto &e : g[u]) {
      int v = e.to; int64 nd = d + e.w;
      if (nd < dist[v]) {
        dist[v] = nd;
        pq.push({nd, v});
      }
    }
  }

  // 2) Build one shortest path tree (SPT) rooted at T
  vector<int> parent(N + 1, -1), depth(N + 1, 0);
  vector<vector<int>> tree(N + 1);
  vector<char> isTreeEdge(M, 0);

  for (int v = 1; v <= N; ++v) {
    if (v == T) continue;
    int p = -1, peid = -1;
    for (auto &e : g[v]) {
      if (dist[v] == dist[e.to] + e.w) { p = e.to; peid = e.id; break; }
    }
    if (p == -1) { cout << -1 << '\n'; return 0; }
    parent[v] = p;
    tree[p].push_back(v);
    isTreeEdge[peid] = 1;
  }

  // 3) Heavy-Light Decomposition (HLD) on SPT
  vector<int> sz(N + 1, 0), heavy(N + 1, -1);
  function<int(int)> dfs1 = [&](int u) {
    int maxSub = 0; sz[u] = 1;
    for (int v : tree[u]) {
      depth[v] = depth[u] + 1;
      int s = dfs1(v);
      sz[u] += s;
      if (s > maxSub) { maxSub = s; heavy[u] = v; }
    }
    return sz[u];
  };
  dfs1(T);

  vector<int> head(N + 1), pos(N + 1), invPos(N + 1);
  int curPos = 0;
  function<void(int,int)> dfs2 = [&](int u, int h) {
    head[u] = h; pos[u] = ++curPos; invPos[curPos] = u;
    if (heavy[u] != -1) dfs2(heavy[u], h);
    for (int v : tree[u]) if (v != heavy[u]) dfs2(v, v);
  };
  dfs2(T, T);

  auto lca = [&](int a, int b) {
    while (head[a] != head[b]) {
      if (depth[head[a]] > depth[head[b]]) a = parent[head[a]]; else b = parent[head[b]];
    }
    return depth[a] < depth[b] ? a : b;
  };

  // Segment tree: range chmin, point query
  struct Seg {
    int n; vector<int64> tag; Seg(int n=0): n(n), tag(4*n+4, INF) {}
    void range_chmin(int node, int l, int r, int ql, int qr, int64 v){
      if (ql>r || qr<l) return; if (ql<=l && r<=qr){ tag[node]=min(tag[node],v); return; }
      int m=(l+r)>>1; range_chmin(node<<1,l,m,ql,qr,v); range_chmin(node<<1|1,m+1,r,ql,qr,v);
    }
    void range_chmin(int l,int r,int64 v){ if(l>r) return; range_chmin(1,1,n,l,r,v);}    
    int64 point_query(int node,int l,int r,int idx,int64 acc){ acc=min(acc,tag[node]);
      if(l==r) return acc; int m=(l+r)>>1; return idx<=m?point_query(node<<1,l,m,idx,acc):point_query(node<<1|1,m+1,r,idx,acc);
    }
    int64 point_query(int idx){ return point_query(1,1,n,idx,INF);}  
  } seg(N);

  auto update_path_excl_target = [&](int u, int v, int64 val){
    while (head[u] != head[v]) {
      if (depth[head[u]] < depth[head[v]]) swap(u, v);
      seg.range_chmin(pos[head[u]], pos[u], val);
      u = parent[head[u]];
    }
    if (u == v) return;
    if (depth[u] < depth[v]) swap(u, v);
    seg.range_chmin(pos[v]+1, pos[u], val);
  };

  for (int i = 0; i < M; ++i) if (!isTreeEdge[i]) {
    int u = edges[i].u, v = edges[i].v; int64 val = dist[u] + edges[i].w + dist[v];
    int L = lca(u, v);
    update_path_excl_target(u, L, val);
    update_path_excl_target(v, L, val);
  }

  vector<int64> dist2_up(N + 1, INF);
  for (int u = 1; u <= N; ++u) if (u != T) {
    int64 mc = seg.point_query(pos[u]);
    dist2_up[u] = (mc >= INF/2) ? INF : (mc - dist[u]);
  }

  auto feasible = [&](int64 X){
    vector<int64> dX(N + 1, INF);
    priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> q;
    dX[S] = 0; q.push({0, S});
    while(!q.empty()){
      auto [du,u]=q.top(); q.pop(); if(du!=dX[u]) continue; if(du>X) continue; if(u==T) return true;
      for(auto &e: g[u]){
        int v=e.to; int64 cond2 = (parent[u]==v? dist2_up[u] : dist[u]);
        if (cond2 >= INF/2) continue; if (du + cond2 > X) continue; int64 nd = du + e.w;
        if (nd <= X && nd < dX[v]){ dX[v]=nd; q.push({nd,v}); }
      }
    }
    return false;
  };

  if (!feasible((int64)4e18/8)) { cout << -1 << '\n'; return 0; }

  int64 lo = dist[S], l = lo, r = max<int64>(lo, 1), hi;
  // exponential search for hi
  hi = r;
  while (!feasible(hi)) { if (hi > (int64)2e18) break; hi = min<int64>(hi*2+1, (int64)2e18); }
  if (!feasible(hi)) { cout << -1 << '\n'; return 0; }

  int64 ans = hi;
  while (l <= hi) {
    int64 mid = l + ((hi - l) >> 1);
    if (feasible(mid)) { ans = mid; hi = mid - 1; }
    else l = mid + 1;
  }
  cout << ans << '\n';
  return 0;
}
```

### 복잡도
- 전처리: 다익스트라 `O((N+M) log N)` + HLD 빌드 `O(N)` + 비트리 간선 경로 갱신 `O(M log N)`
- 판정: 이분 탐색 × 다익스트라 변형 `O((N+M) log N · log Ans)`
- 메모리: `O(N+M)`

### 참고
- AtCoder Contest page: `https://atcoder.jp/contests/jag2017autumn`
- 해설(비공식, traP 블로그): `https://trap.jp/post/428/`

