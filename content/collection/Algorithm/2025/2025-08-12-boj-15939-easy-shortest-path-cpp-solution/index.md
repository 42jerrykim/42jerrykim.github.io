---
title: "[Algorithm] C++ 백준 15939번 쉬운 최단경로"
description: "UCPC 2018 B(BOJ 15939) 쉬운 최단경로 문제 풀이. 두 점의 위치(외부/내부)에 따라 3가지로 분기. 내부-내부는 선분 교차 대각선 수와 각자 외부로 나가는 비용 합 중 최솟값을 O(N)로 계산하고, 내부 판정은 O(log N)로 최적화한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
  - "Algorithm"
  - "BOJ"
  - "Computational Geometry"
  - "UCPC 2018"
tags:
  - "Algorithm"
  - "알고리즘"
  - "BOJ"
  - "백준"
  - "BOJ-15939"
  - "UCPC"
  - "UCPC-2018"
  - "Geometry"
  - "기하"
  - "Computational-Geometry"
  - "계산-기하"
  - "Convex-Polygon"
  - "볼록-다각형"
  - "Point-In-Polygon"
  - "점-다각형-포함"
  - "CCW"
  - "Half-Plane"
  - "반평면"
  - "Diagonals"
  - "대각선"
  - "Crossing"
  - "교차"
  - "Segment"
  - "선분"
  - "Intersection"
  - "교점"
  - "Two-Pointers"
  - "투포인터"
  - "Binary-Search"
  - "이분-탐색"
  - "Prefix-Sum"
  - "누적합"
  - "Difference-Array"
  - "차분-배열"
  - "Optimization"
  - "최적화"
  - "Time-Complexity"
  - "시간-복잡도"
  - "C++"
  - "CPP"
  - "Long-Long"
  - "64-bit"
  - "__int128"
  - "정수-오버플로"
  - "Fast-IO"
  - "빠른-입출력"
  - "Inside-Outside"
  - "내부-외부"
  - "Rope"
  - "밧줄"
  - "Shortest-Path"
  - "최단경로"
  - "Query"
  - "쿼리"
  - "O-N"
  - "O-logN"
  - "UCPC-본선"
  - "대회-문제"
  - "Implementation"
  - "구현"
  - "Math"
  - "수학"
image: "wordcloud.png"
---

### 개요
- **문제**: [BOJ 15939 쉬운 최단경로](https://www.acmicpc.net/problem/15939) (UCPC 2018 본선 B)
- **아이디어 요약**:
  - 두 점의 위치에 따라 세 경우로 분기
    1) 두 점 모두 다각형 외부: 답 0
    2) 한 점만 내부: 내부 점이 밖으로 나갈 때 지나야 하는 대각선 최소 개수
    3) 두 점 모두 내부: 다음 두 값의 최솟값
       - 두 점을 잇는 선분과 교차하는 대각선의 개수
       - 각 점이 외부로 나갈 때 지나야 하는 대각선 최소 개수의 합
- **복잡도**: 쿼리당 O(N). 내부/외부 판정은 O(log N)로 최적화해 상수 시간을 줄임.

### 풀이 메모
- 다각형은 반시계(CCW) 볼록다각형.
- 내부 점 p에 대해 각 정점 i에서 p 기준 왼쪽이 되는 최대 j를 투포인터로 O(N)에 구해 `nextIdx[i]`로 저장.
- 내부→외부 최소 비용은 각 변을 통해 나가는 경우를 누적합 2개(차분 배열)로 한 번에 계산해 최솟값을 취함.
- 두 내부 점의 직선 교차 대각선 수는 `sum_i |nxt1[i] - nxt2[i]| / 2`.

### 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인할 수 있습니다: https://42jerrykim.github.io
#include <bits/stdc++.h>
using namespace std;

struct Point { long long x, y; };

static inline long long cross(const Point& a, const Point& b, const Point& c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

static inline int ccw(const Point& a, const Point& b, const Point& c) {
  long long v = cross(a, b, c);
  return (v > 0) - (v < 0);
}

// O(log N) convex polygon point inclusion (vertices CCW)
static bool insideConvexLog(const vector<Point>& poly, const Point& p) {
  int n = (int)poly.size();
  if (ccw(poly[0], poly[1], p) < 0) return false;
  if (ccw(poly[0], poly[n - 1], p) > 0) return false;
  int l = 1, r = n - 1;
  while (l + 1 < r) {
    int m = (l + r) >> 1;
    if (ccw(poly[0], poly[m], p) >= 0) l = m; else r = m;
  }
  return ccw(poly[l], poly[r], p) >= 0;
}

static const int MAXN = 5000;
static const int SUMSZ = 2 * MAXN + 10;

static Point ext[2 * MAXN + 5];   // polygon duplicated
static int nxt1[MAXN + 5], nxt2[MAXN + 5];
static int sum1[SUMSZ], sum2[SUMSZ];

// For inside point p: for each i, find largest j in (i, i+n] with ccw(poly[i], poly[j], p) > 0
static void get_next(int n, const Point& p, int* arr) {
  int j = 1; // ensure j >= i+1
  for (int i = 0; i < n; ++i) {
    if (j < i + 1) j = i + 1;
    while (j + 1 < i + n && ccw(ext[i], ext[j + 1], p) > 0) ++j;
    arr[i] = j; // index in [i+1, i+n-1]
  }
}

// Both inside: number of diagonals crossed by segment p1-p2
static long long move_inside_count(int n, const int* a, const int* b) {
  long long tot = 0;
  for (int i = 0; i < n; ++i) tot += llabs((long long)a[i] - (long long)b[i]);
  return tot >> 1;
}

// Inside point p: minimal diagonals to exit polygon through some edge (then +1 boundary edge)
static int move_outside_cost(int n, const int* arr) {
  int len = 2 * n;
  memset(sum1, 0, sizeof(int) * (len + 2));
  memset(sum2, 0, sizeof(int) * (len + 2));

  for (int i = 0; i < n; ++i) {
    int j = arr[i];

    sum1[i] += j - i - 1;
    sum1[i + 1] -= j - i - 1;

    sum1[i - 1 + n] += n + i - j - 2;
    sum1[i + n] -= n + i - j - 2;

    sum1[j] -= j;
    sum1[i - 1 + n] += j;

    sum2[j] += 1;
    sum2[i - 1 + n] -= 1;

    sum1[i + 1] += j;
    sum1[j] -= j;

    sum2[i + 1] -= 1;
    sum2[j] += 1;
  }

  for (int i = 1; i < len; ++i) {
    sum1[i] += sum1[i - 1];
    sum2[i] += sum2[i - 1];
  }

  int best = INT_MAX;
  for (int i = 0; i < n; ++i) {
    int now = sum1[i] + i * sum2[i];
    now += sum1[i + n] + (i + n) * sum2[i + n];
    if (now < best) best = now;
  }
  return (best >> 1) + 1;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; 
  if (!(cin >> n)) return 0;
  vector<Point> poly(n);
  for (int i = 0; i < n; ++i) cin >> poly[i].x >> poly[i].y;

  for (int i = 0; i < n; ++i) {
    ext[i] = poly[i];
    ext[i + n] = poly[i];
  }

  int q; 
  cin >> q;
  while (q--) {
    Point p1, p2;
    cin >> p1.x >> p1.y >> p2.x >> p2.y;

    bool in1 = insideConvexLog(poly, p1);
    bool in2 = insideConvexLog(poly, p2);

    if (!in1 && !in2) {
      cout << 0 << '\n';
      continue;
    }

    if (!in1 && in2) {
      swap(p1, p2);
      swap(in1, in2);
    }

    // p1 is inside
    get_next(n, p1, nxt1);
    int t1 = move_outside_cost(n, nxt1);

    if (!in2) {
      cout << t1 << '\n';
      continue;
    }

    // both inside
    get_next(n, p2, nxt2);
    int t2 = move_outside_cost(n, nxt2);
    long long crossInside = move_inside_count(n, nxt1, nxt2);
    cout << min<long long>(crossInside, (long long)t1 + t2) << '\n';
  }
  return 0;
}
```

### 참고
- 해설: [JusticeHui - BOJ15939 쉬운 최단경로 문제](https://justicehui.github.io/ps/2020/09/13/BOJ15939/)
- 대회: [UCPC 2018](https://www.acmicpc.net/category/detail/1893)


