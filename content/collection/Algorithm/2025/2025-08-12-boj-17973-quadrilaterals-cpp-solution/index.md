---
title: "[Algorithm] C++ 백준 17973번 : Quadrilaterals"
description: "백준 17973 Quadrilaterals를 회전 스윕과 대각선 카운팅으로 해결합니다. 모든 대각선에 대해 반평면 점수의 곱으로 기본 점수를 합산하고, 최소 넓이 사각형은 4개 후보만 검사하여 __int128 연산으로 오버플로 없이 안정적으로 판정하는 C++ 풀이를 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "17973"
- "Quadrilaterals"
- "사각형"
- "기하"
- "Geometry"
- "Rotating Sweep"
- "Rotating Sweep Line"
- "회전 스윕"
- "대각선"
- "Diagonal"
- "Minimum Area"
- "최소 넓이"
- "Convex"
- "Concave"
- "볼록사각형"
- "오목사각형"
- "Cross Product"
- "교차곱"
- "Area"
- "면적"
- "Angle Sort"
- "각도 정렬"
- "Counting"
- "카운팅"
- "O(n^2 log n)"
- "Time Complexity"
- "시간복잡도"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른입출력"
- "__int128"
- "i128"
- "Overflow Safe"
- "오버플로 방지"
- "ICPC"
- "Seoul Regional"
- "2019 Seoul Regional"
- "Regional Contest"
- "Competitive Programming"
- "코딩테스트"
- "Problem Solving"
- "문제풀이"
- "최솟값"
- "Minimum"
- "Candidate"
- "후보 선택"
- "Two Diagonals"
- "두 대각선"
- "Adjacency Swap"
- "인접 스왑"
- "Label Maintenance"
- "라벨 유지"
- "Sorting Events"
- "이벤트 정렬"
- "Stable"
- "안정적"
- "Editorial"
- "문제해설"
- "정답 코드"
- "Solution Code"
image: "wordcloud.png"
---

문제: [BOJ 17973 - Quadrilaterals](https://www.acmicpc.net/problem/17973)

### 아이디어 요약
- 점수 체계를 재해석하면, 총점 = 모든 사각형에 대해 대각선 개수의 합(볼록=2, 오목=1) + 최소 넓이 사각형마다 추가 2점입니다.
- 회전 스윕(각도 정렬)으로 모든 선분을 기울기 순서대로 나열해 인접 스왑을 수행하면, 각 이벤트에서 대각선 `(a,b)`의 기여도는 `(pa-1) * (n-pb)`로 한 번에 더할 수 있습니다.
- 최소 넓이 사각형은 각 대각선마다 양쪽 근처 2점씩만 보며 총 4개 후보만 검사합니다. 넓이 비교는 `__int128`을 사용해 안전하게 수행하고, 오목인 경우 한 번에 +2가 되도록 보정합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using i128 = __int128_t;

struct Point {
    ll x, y;
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

// ccw using (b-a) x (c-b)
static inline i128 ccw128(const Point& a, const Point& b, const Point& c) {
    ll dx1 = b.x - a.x, dy1 = b.y - a.y;
    ll dx2 = c.x - b.x, dy2 = c.y - b.y;
    return (i128)dx1 * (i128)dy2 - (i128)dx2 * (i128)dy1;
}
static inline i128 area2(const Point& a, const Point& b, const Point& c) {
    i128 v = ccw128(a, b, c);
    return v >= 0 ? v : -v;
}

struct Line {
    int i, j;      // point IDs (1..n) in the current labeling
    ll dx, dy;     // direction normalized so that dx >= 0
    Line(int a, int b, const vector<Point>& v) : i(a), j(b) {
        dx = v[i].x - v[j].x;
        dy = v[i].y - v[j].y;
        if (dx < 0) { dx = -dx; dy = -dy; }
    }
    bool operator<(const Line& t) const {
        return (i128)dy * (i128)t.dx < (i128)t.dy * (i128)dx;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Point> v(n + 1);
    for (int i = 1; i <= n; ++i) cin >> v[i].x >> v[i].y;

    // Sort points by (x,y). Maintain idx[id] = current position of point id in v[1..n]
    sort(v.begin() + 1, v.begin() + n + 1);
    vector<int> idx(n + 1);
    for (int i = 1; i <= n; ++i) idx[i] = i;

    // Build all undirected lines (i, j) with i > j, normalized by angle (dx >= 0)
    vector<Line> lines; lines.reserve((size_t)n * (n - 1) / 2);
    for (int i = 1; i <= n; ++i) for (int j = 1; j < i; ++j) lines.emplace_back(i, j, v);
    sort(lines.begin(), lines.end());

    long long diagonalCredits = 0;         // sum over pairs L*R
    i128 minArea = -1;                     // minimal doubled area
    long long twiceMinAreaCount = 0;       // +2 per minimal quadrilateral overall

    for (const auto& e : lines) {
        int a = e.i, b = e.j;

        // Apply the adjacent swap corresponding to this line event
        swap(v[idx[a]], v[idx[b]]);
        swap(idx[a], idx[b]);

        int pa = idx[a], pb = idx[b];
        if (pa > pb) swap(pa, pb);

        // Count quadrilaterals where (a,b) is a diagonal: points strictly on each side
        diagonalCredits += 1LL * (pa - 1) * (n - pb);

        // Check 4 minimal-area candidates around the diagonal (pa,pb)
        for (int x = max(1, pa - 2); x <= pa - 1; ++x) {
            for (int y = pb + 1; y <= min(n, pb + 2); ++y) {
                i128 now = area2(v[x], v[pa], v[pb]) + area2(v[y], v[pa], v[pb]);
                if (minArea == -1 || now < minArea) { minArea = now; twiceMinAreaCount = 0; }
                if (now == minArea) {
                    ++twiceMinAreaCount; // base +1
                    i128 s1 = ccw128(v[x], v[y], v[pa]);
                    i128 s2 = ccw128(v[x], v[y], v[pb]);
                    if ((s1 > 0) == (s2 > 0)) ++twiceMinAreaCount; // non-convex adds one more
                }
            }
        }
    }

    cout << (diagonalCredits + twiceMinAreaCount) << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(n^2 log n)` (모든 선분 기울기 정렬 + 선형 스윕)
- 공간: `O(n^2)` 이벤트 저장 + `O(n)` 보조 배열

### 참고
- 문제: `https://www.acmicpc.net/problem/17973`
- 아이디어: 회전 스윕으로 대각선 기여도 누적 + 대각선 주변 4개 후보로 최소 넓이 판정


