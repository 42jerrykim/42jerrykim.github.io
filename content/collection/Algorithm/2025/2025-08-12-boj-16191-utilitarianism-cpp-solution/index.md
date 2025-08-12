---
title: "[Algorithm] BOJ 16191 - Utilitarianism C++ 풀이: 라그랑주+트리DP"
description: "트리에서 서로 인접하지 않는 k개의 간선을 골라 가중치 합을 최대로 만드는 문제. 라그랑주 최적화(λ)로 k-제약을 벌점으로 흡수하고, 노드별 상태 DP(A/B)로 F(λ)=max∑(w-λ)와 선택 간선 수를 O(n)에 계산, λ에 대한 단조성을 이용해 이분 탐색 후 F(λ)+λk의 최소값으로 정답을 복원한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
- "Tree DP"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "16191"
- "Utilitarianism"
- "Tree"
- "트리"
- "Tree DP"
- "트리 DP"
- "Matching"
- "매칭"
- "K-Matching"
- "Maximum Weight Matching"
- "최대 가중치 매칭"
- "Lagrangian Relaxation"
- "라그랑주 이완"
- "Convex Dual"
- "이중성"
- "Dynamic Programming"
- "DP"
- "Binary Search"
- "이분 탐색"
- "Monotonicity"
- "단조성"
- "Optimization"
- "최적화"
- "Greedy DP"
- "루트 트리"
- "Rooted Tree"
- "Parent Array"
- "부모 배열"
- "Iterative DFS"
- "스택 DFS"
- "Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "O(n log W)"
- "64-bit"
- "long long"
- "Overflow Safety"
- "오버플로우 방지"
- "Tie-breaking"
- "동률 처리"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "STL"
- "Fast IO"
- "빠른 입출력"
- "Competitive Programming"
- "Problem Solving"
- "PS"
- "Algorithm"
- "알고리즘"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 16191 - Utilitarianism](https://www.acmicpc.net/problem/16191)

### 문제 요약
- `n`개의 도시가 트리를 이루고, 간선마다 정수 가중치가 있다.
- 서로 정점(도시)을 공유하지 않도록 `k`개의 간선을 선택해 가중치 합을 최대화하라.
- 최대 매칭 크기 < `k`이면 Impossible.

### 핵심 아이디어 (라그랑주 최적화 + 트리 DP)
- 선택 간선 수 제약을 벌점 항으로 흡수: 임의의 실수 `λ`에 대해 `F(λ) = max Σ (w_e - λ)` 를 계산하면, 최적해의 간선 수 `m(λ)`는 `λ`가 커질수록 단조 감소한다.
- 정확히 `k`개를 고른 최대 합은 이중성으로 `min_λ [ F(λ) + λ·k ]` 로 복원된다.
- 트리 DP로 `F(λ)`와 `m(λ)`를 O(n) 계산:
  - 상태 `A(u)`: `u`가 부모와 매칭되지 않음 → 자식 중 최대 한 명과 매칭 가능.
  - 상태 `B(u)`: `u`가 부모와 매칭됨 → 자식과는 매칭 불가.
  - 각 자식에 대해 `A/B` 전이값을 모으고, `A(u)`에서는 "한 자식과 매칭"의 이득 `dpB[v] + (w-λ) - dpA[v]` 중 최댓값만 취함.
  - 동률 시 더 많은 간선을 선택하는 해를 우선해 단조성을 보장.
- 이분 탐색으로 `m(λ) ≤ k`가 처음 성립하는 최소 `λ`를 찾고, `λ`와 `λ-1`에서 `F(λ)+λk`의 최소값을 정답으로 사용.

### 시간 복잡도
- `run(λ)`가 O(n), 이분 탐색 O(log W) → 전체 O(n log W).

### C++ 구현

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct Pair { long long profit; int cnt; };

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, k; if (!(cin >> n >> k)) return 0;
  vector<vector<pair<int,long long>>> g(n+1);
  for (int i = 0; i < n-1; ++i) {
    int u, v; long long c; cin >> u >> v >> c;
    g[u].push_back({v, c}); g[v].push_back({u, c});
  }

  // Rooting and order
  vector<int> parent(n+1, 0), order; order.reserve(n);
  vector<int> st; st.reserve(n); parent[1] = -1; st.push_back(1);
  while (!st.empty()) {
    int u = st.back(); st.pop_back(); order.push_back(u);
    for (auto &e : g[u]) {
      int v = e.first; if (v == parent[u]) continue;
      if (parent[v] != 0) continue; parent[v] = u; st.push_back(v);
    }
  }

  vector<long long> dpA(n+1, 0), dpB(n+1, 0);
  vector<int> cntA(n+1, 0), cntB(n+1, 0);

  auto better = [](const Pair &a, const Pair &b) {
    if (a.profit != b.profit) return a.profit > b.profit;
    return a.cnt > b.cnt; // tie-break: prefer larger count
  };

  auto run = [&](long long lambda) -> Pair {
    for (int idx = (int)order.size() - 1; idx >= 0; --idx) {
      int u = order[idx];
      long long baseProfit = 0; int baseCnt = 0;
      for (auto &e : g[u]) {
        int v = e.first; if (v == parent[u]) continue;
        baseProfit += dpA[v]; baseCnt += cntA[v];
      }
      Pair bestDelta{0, 0};
      for (auto &e : g[u]) {
        int v = e.first; if (v == parent[u]) continue; long long w = e.second;
        long long deltaProfit = dpB[v] + (w - lambda) - dpA[v];
        int deltaCnt = cntB[v] + 1 - cntA[v];
        Pair cand{deltaProfit, deltaCnt};
        if (better(cand, bestDelta)) bestDelta = cand;
      }
      // u matched with parent → cannot match children
      dpB[u] = baseProfit; cntB[u] = baseCnt;
      // u free → at most one child match
      dpA[u] = baseProfit + bestDelta.profit; cntA[u] = baseCnt + bestDelta.cnt;
    }
    return {dpA[1], cntA[1]};
  };

  const long long LAM_INF = 1000000000000LL; // 1e12
  Pair neg = run(-LAM_INF);
  if (neg.cnt < k) { cout << "Impossible\n"; return 0; }

  long long lo = -LAM_INF, hi = LAM_INF;
  while (lo < hi) {
    long long mid = (lo + hi) >> 1;
    Pair res = run(mid);
    if (res.cnt <= k) hi = mid; else lo = mid + 1;
  }
  long long lam = lo;

  // convex dual reconstruction
  Pair r1 = run(lam); long long ans1 = r1.profit + lam * 1LL * k;
  Pair r0 = run(lam - 1); long long ans0 = r0.profit + (lam - 1) * 1LL * k;
  long long ans = min(ans0, ans1);

  cout << ans << '\n';
  return 0;
}
```

### 메모
- `λ`가 증가하면 선택 간선 수가 감소하므로 `m(λ) ≤ k`가 처음 성립하는 최소 `λ`를 찾는다.
- 최종 값은 `max`가 아니라 **`min_λ [ F(λ)+λk ]`** 임에 유의.
- `LAM_INF=1e12`는 합계 범위(최대 ≈1e17)를 고려해 64-bit 내에서 안전하게 동작.


