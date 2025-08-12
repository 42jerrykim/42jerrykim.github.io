---
title: "[Algorithm] BOJ 3527 Jungle Outpost - C++ 풀이 (HPI)"
description: "BOJ 3527 Jungle Outpost 문제를 반평면 교집합(HPI)과 이분탐색으로 해결. k개의 연속 정점 제거에도 항상 보호되는 HQ가 존재하는지 공집합 여부로 판정하고, 가장 큰 k를 찾아 k+1을 정답으로 출력하는 실전 C++ 구현과 핵심 아이디어 정리."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "3527"
- "Jungle Outpost"
- "NEERC"
- "NEERC 2010"
- "ICPC"
- "Regional"
- "Northern Eurasia"
- "Computational Geometry"
- "Geometry"
- "기하"
- "Convex Hull"
- "볼록 껍질"
- "Half-Plane Intersection"
- "반평면 교집합"
- "HPI"
- "Binary Search"
- "이분탐색"
- "Strictly Inside"
- "내부 판정"
- "Line Intersection"
- "직선 교점"
- "Orientation"
- "CCW"
- "Cross Product"
- "외적"
- "Precision"
- "부동소수"
- "Long Double"
- "EPS"
- "Numerical Stability"
- "수치 안정성"
- "Complexity"
- "시간복잡도"
- "O(n log n)"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Algorithm"
- "알고리즘"
- "Problem Solving"
- "문제풀이"
- "Convex Polygon"
- "볼록 다각형"
- "Deque"
- "덱"
- "Half-planes"
- "반평면"
- "Strict Interior"
- "보호 구역"
- "Protection"
- "Calipers"
- "회전 캘리퍼스"
- "Two-pointer"
- "두 포인터"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 3527 - Jungle Outpost](https://www.acmicpc.net/problem/3527)

### 아이디어 요약
- 시계 방향으로 주어진 볼록 다각형 정점 `a[0..n-1]`에서 HQ(본부)는 “볼록껍질 내부에 엄격히 포함될 때만” 보호됩니다.
- 적이 `k`개의 타워를 부숴도 HQ가 항상 보호되려면, 임의의 연속 `k`개 정점을 제거해도 남은 정점들의 볼록껍질에 HQ를 엄격히 포함시킬 수 있어야 합니다.
- 이를 위해 각 `k`에 대해 다음의 반평면 교집합을 구성합니다.
  - 모든 `i`에 대해 선분 `(a[i], a[i+k+1])`을 지나는 직선의 “보완 호(complement arc)” 쪽 반평면을 채택합니다. 즉, 테스트 점으로 `a[(i+k+2)%n]`을 사용해 왼쪽 반평면이 되도록 방향을 맞춥니다.
  - 이렇게 만든 `n`개의 왼쪽 반평면 교집합이 “면적을 갖는(strict)”다면, 어떤 HQ 위치가 연속 `k` 제거에서도 항상 보호됩니다 → 해당 `k`는 가능.
- `k`를 이분탐색해 가능한 최대 `k_max`를 찾은 후, 문제에서 요구하는 “안전을 깨기 위해 필요한 최소 폭파 수의 최대값”은 `k_max + 1` 입니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using ld = long double;
const ld EPS = 1e-12L;

struct Pt {
  ld x, y;
  Pt() {}
  Pt(ld _x, ld _y): x(_x), y(_y) {}
  Pt operator+(const Pt& o) const { return Pt(x + o.x, y + o.y); }
  Pt operator-(const Pt& o) const { return Pt(x - o.x, y - o.y); }
  Pt operator*(ld k) const { return Pt(x * k, y * k); }
};

ld cross(const Pt& a, const Pt& b) { return a.x * b.y - a.y * b.x; }
ld dot(const Pt& a, const Pt& b) { return a.x * b.x + a.y * b.y; }

struct Line {
  Pt p;      // point on line
  Pt v;      // direction vector
  ld ang;    // angle for sorting
  Line() {}
  Line(Pt _p, Pt _v): p(_p), v(_v) { ang = atan2l(v.y, v.x); }
};

Pt intersect(const Line& a, const Line& b) {
  ld t = cross(b.v, b.p - a.p) / cross(b.v, a.v);
  return a.p + a.v * t;
}

bool inside_strict(const Line& l, const Pt& q) { return cross(l.v, q - l.p) > EPS; }

vector<Line> normalize_lines(vector<Line>& ls) {
  sort(ls.begin(), ls.end(), [](const Line& a, const Line& b) {
    if (fabsl(a.ang - b.ang) > 1e-15L) return a.ang < b.ang;
    return cross(a.v, b.p - a.p) > 0;
  });
  vector<Line> res;
  for (const auto& L : ls) {
    if (res.empty() || fabsl(L.ang - res.back().ang) > 1e-15L) res.push_back(L);
    else if (cross(res.back().v, L.p - res.back().p) > 0) res.back() = L;
  }
  return res;
}

bool halfplane_intersection_has_area(vector<Line> ls) {
  ls = normalize_lines(ls);
  deque<Line> dq;
  deque<Pt> ip;

  auto add = [&](const Line& L) {
    while (!ip.empty() && !inside_strict(L, ip.back())) { dq.pop_back(); ip.pop_back(); }
    while (!ip.empty() && !inside_strict(L, ip.front())) { dq.pop_front(); ip.pop_front(); }
    if (!dq.empty() && fabsl(cross(dq.back().v, L.v)) < 1e-18L) {
      if (inside_strict(L, dq.back().p)) { dq.pop_back(); if (!ip.empty()) ip.pop_back(); }
      else return;
    }
    if (!dq.empty()) ip.push_back(intersect(dq.back(), L));
    dq.push_back(L);
  };

  for (const auto& L : ls) add(L);

  while (!ip.empty() && !inside_strict(dq.front(), ip.back())) { dq.pop_back(); ip.pop_back(); }
  while (!ip.empty() && !inside_strict(dq.back(), ip.front())) { dq.pop_front(); ip.pop_front(); }

  if (dq.size() < 3) return false;
  vector<Pt> poly;
  for (size_t i = 0; i + 1 < dq.size(); ++i) poly.push_back(intersect(dq[i], dq[i + 1]));
  poly.push_back(intersect(dq.back(), dq.front()));

  ld area2 = 0;
  for (size_t i = 0; i < poly.size(); ++i) {
    size_t j = (i + 1) % poly.size();
    area2 += cross(poly[i], poly[j]);
  }
  return fabsl(area2) > 1e-10L;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; if (!(cin >> n)) return 0;
  vector<Pt> a(n);
  for (int i = 0; i < n; ++i) { long long x, y; cin >> x >> y; a[i] = Pt((ld)x, (ld)y); }

  auto feasible = [&](int k)->bool {
    vector<Line> ls; ls.reserve(n);
    for (int i = 0; i < n; ++i) {
      int j = (i + k + 1) % n;
      Pt p = a[i], q = a[j];
      Pt t = a[(j + 1) % n];
      if (cross(q - p, t - p) <= 0) swap(p, q);
      ls.emplace_back(p, q - p);
    }
    return halfplane_intersection_has_area(ls);
  };

  int lo = 0, hi = max(0, n - 3), best = 0;
  while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (feasible(mid)) { best = mid; lo = mid + 1; }
    else hi = mid - 1;
  }
  cout << (best + 1) << '\n';
  return 0;
}
```

### 복잡도
- 반평면 교집합은 정렬 `O(n log n)` + 덱 유지 `O(n)`. 이를 `log n`회 이분탐색하므로 전체 `O(n log n)`에 상수배 `log n`이 곱해집니다.

### 비고
- 문제 정의가 “볼록껍질 내부(strictly inside)”임을 반영해 경계 위 점은 보호로 간주하지 않으며, 교집합의 “면적>0”로 판정합니다.
- 입력 정점이 볼록 다각형의 꼭짓점이며 시계 방향으로 주어진 전제가 핵심입니다.


