---
title: "[Algorithm] C++ 백준 17955번 Max or Min"
description: "원형 배열에서 한 칸을 골라 인접 세 수의 최소/최대로 바꾸는 연산으로 모든 값을 x로 만드는 최소 시간을 구한다. 배열에 x가 없으면 불가능(-1). 인접 쌍마다 (min+1..max-1)에 1을 더하는 차분 누적으로 ‘그룹 수’를 집계하고, 시작점을 한 칸 회전한 두 번의 집계를 취해 중복을 보정한다. 정답은 (n - cnt[x]) + max(groups1[x], groups2[x])로 계산한다. O(n + m)."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- BOJ
- Baekjoon
- 백준
- Data-Structures
- Prefix-Sum
- Segment-Tree
- 그리디
- greedy
- 구현
- implementation
- C++
- IO
- Time-Complexity
- 시간복잡도
- Complexity-Analysis
- 자료구조
- Range-Query
- Math
- editorial
- 알고리즘
- Algorithm
- array
- 배열
- ICPC
- Competitive-Programming
- Problem-Solving
- Coding-Test
- 코딩테스트
- Optimization
- 최적화
- 문제해결
- Code-Quality
- 코드품질
- Go
- .NET
- Git
- GitHub
- Space-Complexity
- 공간복잡도
- Edge-Cases
- 엣지케이스
- Testing
- 테스트
- Documentation
- 문서화
- Best-Practices
- 복잡도분석
- Debugging
- 디버깅
- Refactoring
image: "wordcloud.png"
---

문제: [BOJ 17955 - Max or Min](https://www.acmicpc.net/problem/17955)

### 아이디어 요약
- 목표: 모든 원소를 `x`로 만드는 최소 분(minute) 수를 `x = 1..m` 각각에 대해 계산.
- 불가능 조건: 배열에 `x`가 하나도 없으면 절대 만들 수 없음 → `-1`.
- 가능한 경우: 답은 두 성분의 합으로 표현됨
  - (1) `x`가 아닌 위치를 `x`로 맞추는 데 드는 기본 비용: `n - cnt[x]`.
  - (2) “상대적인 추가 비용” = 인접한 두 값 `(a[i], a[i+1])`에 대해 `x`가 그 둘의 엄격한 사이값이면 `x`를 그 구간에서 만들기 위해 추가로 1이 필요함. 이 추가 비용의 총합을 ‘그룹 수’로 셈.
- 그룹 수 계산: 모든 인접 쌍에 대해 범위 `[min(a,b)+1, max(a,b)-1]`에 +1을 더하는 차분 배열을 만든 뒤 누적합으로 복원.
- 중복 보정: 첫 쌍부터 차례대로 더해가면 바로 앞 쌍과의 겹침을 규칙적으로 깎아야 함. 또한 시작 구간 선택의 영향이 있으므로, 시작점을 원형에서 한 칸 회전해 두 번 집계한 뒤 `max(groups1[x], groups2[x])`를 사용.
- 최종식: `ans[x] = (n - cnt[x]) + max(groups1[x], groups2[x])` (단, `cnt[x] == 0`이면 `-1`).

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <bits/stdc++.h>
using namespace std;

static inline void addRange(vector<int>& diff, int l, int r, int m) {
  if (l < 1) l = 1;
  if (r > m) r = m;
  if (l <= r) {
    diff[l] += 1;
    diff[r + 1] -= 1;
  }
}

// Trim [ns, ne] to exclude overlap with [ps, pe] using the known accepted rules.
static inline void trimAgainst(int& ns, int& ne, int ps, int pe) {
  if (ne < ns) return;
  if (ps <= ns && ne <= pe) { // fully contained → drop
    ns = INT_MAX; ne = 0; return;
  }
  if (pe < ns || ne < ps) return; // disjoint
  if (pe == ne && ns < ps) {      // share right end, keep left-only extension
    ne = ps - 1; return;
  }
  if (ps == ns && pe < ne) {      // share left end, keep right-only extension
    ns = pe + 1; return;
  }
}

static vector<int> buildGroups(const vector<int>& v, int n, int m) {
  vector<int> diff(m + 3, 0);

  auto interval = [&](int x, int y) -> pair<int,int> {
    int l = min(x, y) + 1;
    int r = max(x, y) - 1;
    return {l, r};
  };

  // First pair
  auto [fs, fe] = interval(v[1], v[2]);
  addRange(diff, fs, fe, m);
  int ls = fs, le = fe;

  // Middle pairs
  for (int i = 3; i <= n; ++i) {
    auto [ns, ne] = interval(v[i - 1], v[i]);
    trimAgainst(ns, ne, ls, le);
    addRange(diff, ns, ne, m);
    ls = ns; le = ne;
  }

  // Closing pair (wrap-around)
  {
    auto [ns, ne] = interval(v[n], v[n + 1]);
    trimAgainst(ns, ne, ls, le);
    trimAgainst(ns, ne, fs, fe);
    addRange(diff, ns, ne, m);
  }

  // Prefix to counts
  vector<int> groups(m + 1, 0);
  int cur = 0;
  for (int k = 1; k <= m; ++k) {
    cur += diff[k];
    groups[k] = cur;
  }
  return groups;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m;
  if (!(cin >> n >> m)) return 0;
  vector<int> a(n + 1);
  vector<int> freq(m + 1, 0);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    if (1 <= a[i] && a[i] <= m) freq[a[i]]++;
  }

  // First pass: use original order with wrap a[n+1] = a[1]
  vector<int> v1(n + 2);
  for (int i = 1; i <= n; ++i) v1[i] = a[i];
  v1[n + 1] = v1[1];
  vector<int> g1 = buildGroups(v1, n, m);

  // Second pass: rotate start by one
  vector<int> v2(n + 2);
  for (int i = 1; i <= n; ++i) v2[i] = a[i % n + 1];
  v2[n + 1] = v2[1];
  vector<int> g2 = buildGroups(v2, n, m);

  // Answer for each k
  for (int k = 1; k <= m; ++k) {
    if (freq[k] == 0) {
      cout << -1 << (k == m ? '\n' : ' ');
    } else {
      int extra = max(g1[k], g2[k]);
      int moves = (n - freq[k]) + extra;
      cout << moves << (k == m ? '\n' : ' ');
    }
  }
  return 0;
}
```

### 복잡도
- 전처리와 두 번의 그룹 집계는 모두 `O(n + m)`.
- 메모리는 `O(m)` 차분·누적 배열과 보조 벡터에 비례.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 또는 빈 입력 | 반복문 범위·예외 처리 확인 |
| **오버플로우** | 답이 $2^{31}$ 초과 가능 | `long long` (C++) 등 사용 |
