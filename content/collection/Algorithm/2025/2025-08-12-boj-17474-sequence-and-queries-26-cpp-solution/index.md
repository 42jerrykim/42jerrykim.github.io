---
title: "[Algorithm] C++ 백준 17474번 : 수열과 쿼리"
description: "백준 17474 수열과 쿼리 26: 구간에 X로 chmin을 적용하고 구간 최댓값/합을 질의하는 문제. Segment Tree Beats로 (max, second max, count, sum)을 유지하여 chmin을 빠르게 처리하고, 질의는 O(log N)로 응답하는 C++ 구현을 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "17474"
- "Sequence and Queries"
- "수열과 쿼리"
- "수열과-쿼리-26"
- "Range Query"
- "범위 질의"
- "Segment Tree"
- "세그먼트 트리"
- "Segment Tree Beats"
- "세그트리 비트"
- "Beats"
- "Chmin"
- "Range Chmin"
- "구간 chmin"
- "Min Cap"
- "Cap Assign"
- "Range Max"
- "구간 최댓값"
- "Range Sum"
- "구간 합"
- "Lazy Propagation"
- "지연 전파"
- "Data Structure"
- "자료 구조"
- "Second Maximum"
- "두번째 최댓값"
- "Count of Max"
- "최댓값 개수"
- "Competitive Programming"
- "컴페티티브 프로그래밍"
- "Problem Solving"
- "PS"
- "Solution Code"
- "정답 코드"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른입출력"
- "Time Complexity"
- "시간복잡도"
- "O(log N)"
- "Query Processing"
- "쿼리 처리"
- "Implementation"
- "구현"
- "Optimization"
- "최적화"
- "Large N"
- "N=1e6"
- "Memory"
- "메모리"
- "64-bit"
- "Long Long"
- "Integer Overflow"
- "정수 오버플로"
- "Range Update"
- "범위 업데이트"
image: "wordcloud.png"
---

문제: [BOJ 17474 - 수열과 쿼리 26](https://www.acmicpc.net/problem/17474)

### 아이디어 요약
- 쿼리
  - `1 L R X`: 모든 `i ∈ [L, R]`에 대해 `A[i] = min(A[i], X)` (range chmin)
  - `2 L R`: `max(A[L..R])`
  - `3 L R`: `sum(A[L..R])`
- Segment Tree Beats를 사용해 각 노드에 `(mx, se, cnt, sum)`을 유지합니다.
  - `mx`: 구간 최댓값, `se`: 구간 내 두 번째 최댓값, `cnt`: 최댓값의 개수, `sum`: 합
  - `chmin(x)`을 적용할 때 `x > se`이면 전체 노드에 한 번에 반영 가능합니다.
  - 필요 시 자식에게만 전파(`push`)하고 다시 병합(`merge`)합니다.
- 합은 `long long`으로 누적하며, 빠른 입출력으로 1e6 규모 입출력과 연산을 처리합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

#ifdef _WIN32
#define getchar_unlocked getchar
#define putchar_unlocked putchar
#endif

struct FastScanner {
  static const int BUFSIZE = 1 << 20;
  int idx = 0, size = 0;
  char buf[BUFSIZE];
  inline char read() {
    if (idx >= size) {
      size = (int)fread(buf, 1, BUFSIZE, stdin);
      idx = 0;
      if (size == 0) return 0;
    }
    return buf[idx++];
  }
  template <class T>
  bool nextInt(T &out) {
    char c; T sign = 1; T x = 0; c = read();
    if (!c) return false;
    while (c!='-' && (c<'0' || c>'9')) { c = read(); if (!c) return false; }
    if (c=='-') { sign = -1; c = read(); }
    for (; c>='0' && c<='9'; c = read()) x = x*10 + (c - '0');
    out = x * sign;
    return true;
  }
} fs;

inline void writeInt64(long long x) {
  if (x == 0) { putchar_unlocked('0'); putchar_unlocked('\n'); return; }
  if (x < 0) { putchar_unlocked('-'); x = -x; }
  char s[24]; int n = 0;
  while (x) { s[n++] = char('0' + (x % 10)); x /= 10; }
  while (n--) putchar_unlocked(s[n]);
  putchar_unlocked('\n');
}

struct Node {
  long long sum;
  int mx;
  int se;   // second max
  int cnt;  // count of max
};

static const int NEG_INF = INT_MIN;
int N;
vector<Node> seg;
vector<int> A;

inline Node mergeNode(const Node &L, const Node &R) {
  Node res;
  res.sum = L.sum + R.sum;
  if (L.mx == R.mx) {
    res.mx = L.mx;
    res.cnt = L.cnt + R.cnt;
    res.se = max(L.se, R.se);
  } else if (L.mx > R.mx) {
    res.mx = L.mx;
    res.cnt = L.cnt;
    res.se = max(L.se, R.mx);
  } else { // R.mx > L.mx
    res.mx = R.mx;
    res.cnt = R.cnt;
    res.se = max(L.mx, R.se);
  }
  return res;
}

inline void apply_chmin(int p, int x) {
  Node &u = seg[p];
  if (x >= u.mx) return;
  // This function must be called only when x > u.se
  long long dec = 1LL * (u.mx - x) * u.cnt;
  u.sum -= dec;
  u.mx = x;
}

inline void push(int p) {
  int lc = p << 1, rc = lc | 1;
  if (seg[p].mx < seg[lc].mx) apply_chmin(lc, seg[p].mx);
  if (seg[p].mx < seg[rc].mx) apply_chmin(rc, seg[p].mx);
}

void build(int p, int l, int r) {
  if (l == r) {
    seg[p].sum = A[l];
    seg[p].mx = A[l];
    seg[p].se = NEG_INF;
    seg[p].cnt = 1;
    return;
  }
  int m = (l + r) >> 1;
  build(p << 1, l, m);
  build(p << 1 | 1, m + 1, r);
  seg[p] = mergeNode(seg[p << 1], seg[p << 1 | 1]);
}

void range_chmin(int p, int l, int r, int ql, int qr, int x) {
  if (qr < l || r < ql || seg[p].mx <= x) return;
  if (ql <= l && r <= qr && seg[p].se < x) {
    apply_chmin(p, x);
    return;
  }
  push(p);
  int m = (l + r) >> 1;
  range_chmin(p << 1, l, m, ql, qr, x);
  range_chmin(p << 1 | 1, m + 1, r, ql, qr, x);
  seg[p] = mergeNode(seg[p << 1], seg[p << 1 | 1]);
}

int range_max(int p, int l, int r, int ql, int qr) {
  if (qr < l || r < ql) return INT_MIN;
  if (ql <= l && r <= qr) return seg[p].mx;
  push(p);
  int m = (l + r) >> 1;
  return max(range_max(p << 1, l, m, ql, qr),
             range_max(p << 1 | 1, m + 1, r, ql, qr));
}

long long range_sum(int p, int l, int r, int ql, int qr) {
  if (qr < l || r < ql) return 0LL;
  if (ql <= l && r <= qr) return seg[p].sum;
  push(p);
  int m = (l + r) >> 1;
  return range_sum(p << 1, l, m, ql, qr) +
         range_sum(p << 1 | 1, m + 1, r, ql, qr);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  if (!fs.nextInt(N)) return 0;
  A.assign(N + 1, 0);
  for (int i = 1; i <= N; ++i) fs.nextInt(A[i]);

  int M; fs.nextInt(M);
  seg.assign(4 * (N + 5), Node{0, 0, 0, 0});
  build(1, 1, N);

  for (int i = 0; i < M; ++i) {
    int t; fs.nextInt(t);
    if (t == 1) {
      int L, R, X; fs.nextInt(L); fs.nextInt(R); fs.nextInt(X);
      range_chmin(1, 1, N, L, R, X);
    } else if (t == 2) {
      int L, R; fs.nextInt(L); fs.nextInt(R);
      int ans = range_max(1, 1, N, L, R);
      writeInt64(ans);
    } else { // t == 3
      int L, R; fs.nextInt(L); fs.nextInt(R);
      long long ans = range_sum(1, 1, N, L, R);
      writeInt64(ans);
    }
  }
  return 0;
}
```

### 복잡도
- 각 `chmin` 업데이트는 필요 시 자식으로만 전파되어 총 활성화/감소 횟수가 제한됩니다.
- 질의/업데이트당 `O(log N)` 평균, 전체는 `O((N+M) log N)` 내외.
- 메모리 `O(N)`, 합은 `long long`으로 안전하게 처리.


