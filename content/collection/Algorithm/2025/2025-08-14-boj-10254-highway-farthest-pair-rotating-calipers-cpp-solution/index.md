---
title: "[Algorithm] C++ 백준 10254번: 고속도로 - 회전하는 캘리퍼스"
description: "최대 20만 점에서 유클리드 최장거리 쌍을 찾습니다. 단조사슬로 볼록 껍질을 O(n log n)에 구하고, 회전하는 캘리퍼스로 지름을 O(h) 탐색합니다. 제곱거리·64비트·빠른 입출력 적용."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-10254
- cpp
- C++
- Geometry
- 기하
- Computational Geometry
- 계산기하
- Convex Hull
- 볼록 껍질
- Monotone Chain
- 단조 사슬
- Andrew
- Rotating Calipers
- 회전하는 캘리퍼스
- Diameter
- 다각형 지름
- Farthest Pair
- 최원점 쌍
- Antipodal Pairs
- 안티포달
- Euclidean Distance
- 유클리드 거리
- Squared Distance
- 제곱거리
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Testing
- 테스트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Template
- 템플릿
- Debugging
- 디버깅
- Integer Overflow
- 정수 오버플로
- 64-bit
- 64비트
- Sort
- 정렬
- Unique
- 중복제거
- O(n log n)
- 대용량 입력
- Fast IO
- 빠른입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/10254
- 요약: n개의 도시(점) 중 유클리드 거리가 가장 먼 두 도시(점) 쌍을 구해 그 좌표를 출력합니다. 여러 쌍이 가능하면 임의의 하나를 출력해도 됩니다.
- 제한: 테스트케이스 T, 각 tc마다 2 ≤ n ≤ 200,000, 좌표는 |x|, |y| ≤ 10,000,000, 모든 점은 서로 다름.

## 입력/출력
```
입력
T
n
x1 y1
... (n줄)

출력
각 테스트케이스마다 가장 먼 두 점의 좌표: x1 y1 x2 y2
```

## 접근 개요
- 핵심 관찰: 가장 먼 두 점은 항상 원 집합의 볼록 껍질 위에 존재합니다. 따라서 먼저 볼록 껍질을 구한 뒤, 껍질 위에서 지름을 찾으면 됩니다.
- 절차: (1) Andrew 단조사슬로 볼록 껍질을 O(n log n)에 계산 (중복 제거 포함) → (2) 회전하는 캘리퍼스로 껍질 지름(antipodal pair)을 O(h)로 탐색.
- 수치 안정성: 비교는 모두 제곱거리(정수)로 수행하고, 교차곱·거리 제곱은 64비트 정수 범위 내에서 안전합니다.

## 알고리즘 설계
- 상태/자료구조:
  - 점은 `(x, y)` 정수 쌍, 정렬과 중복 제거 후 단조사슬로 `lower`, `upper`를 구성합니다.
  - 교차곱 `cross(a,b,c) = (b-a)×(c-a)`의 부호로 껍질에서 오른쪽/왼쪽 회전을 판단합니다.
- 절차 요약:
  1) 점들을 `x`(우선), `y`(차선) 오름차순으로 정렬 후 중복 제거
  2) 하단 껍질 `lower`와 상단 껍질 `upper`를 각각 구축 (비반시계 유지: `cross <= 0`이면 pop)
  3) `lower.pop_back(), upper.pop_back()` 후 이어 붙여 시계방향 껍질을 완성
  4) 캘리퍼스: 각 변 `(i→i+1)`에 대해 반대편 넓이를 증가시키는 한 `j`를 전진, 각 순간 `(i,j)`와 `(i+1,j)` 거리 제곱을 후보로 갱신
- 올바름 근거(스케치):
  - 지름은 껍질 위 점들 사이의 antipodal pair 중 하나입니다. 단조 증가 성질 때문에 `j`는 전체 i 순회 동안 총 한 바퀴만 회전하므로 O(h)에 모든 antipodal 후보를 커버합니다.

## 복잡도
- 볼록 껍질: O(n log n) (정렬 우세)
- 캘리퍼스: O(h) (h는 껍질 크기, h ≤ n)
- 전체: O(n log n), 추가 공간 O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point {
    long long x, y;
    bool operator<(const Point& o) const {
        if (x != o.x) return x < o.x;
        return y < o.y;
    }
    bool operator==(const Point& o) const { return x == o.x && y == o.y; }
};

static inline long long cross(const Point& a, const Point& b, const Point& c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}
static inline long long dist2(const Point& a, const Point& b) {
    long long dx = a.x - b.x, dy = a.y - b.y;
    return dx * dx + dy * dy;
}

vector<Point> convexHull(vector<Point> pts) {
    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    int n = (int)pts.size();
    if (n <= 1) return pts;

    vector<Point> lower, upper;
    for (const auto& p : pts) {
        while ((int)lower.size() >= 2 && cross(lower[(int)lower.size()-2], lower.back(), p) <= 0) lower.pop_back();
        lower.push_back(p);
    }
    for (int i = n - 1; i >= 0; --i) {
        const auto& p = pts[i];
        while ((int)upper.size() >= 2 && cross(upper[(int)upper.size()-2], upper.back(), p) <= 0) upper.pop_back();
        upper.push_back(p);
    }
    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());
    return lower;
}

pair<Point, Point> diameterRotatingCalipers(const vector<Point>& h) {
    int m = (int)h.size();
    if (m == 1) return {h[0], h[0]};
    if (m == 2) return {h[0], h[1]};
    long long best = -1;
    pair<int,int> ans = {0, 0};
    int j = 1;
    for (int i = 0; i < m; ++i) {
        int ni = (i + 1) % m;
        while (true) {
            int nj = (j + 1) % m;
            long long cur = llabs(cross(h[i], h[ni], h[j]));
            long long nxt = llabs(cross(h[i], h[ni], h[nj]));
            if (nxt > cur) j = nj;
            else break;
        }
        long long d1 = dist2(h[i], h[j]);
        if (d1 > best) { best = d1; ans = {i, j}; }
        long long d2 = dist2(h[ni], h[j]);
        if (d2 > best) { best = d2; ans = {ni, j}; }
    }
    return {h[ans.first], h[ans.second]};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        vector<Point> pts(n);
        for (int i = 0; i < n; ++i) cin >> pts[i].x >> pts[i].y;
        vector<Point> hull = convexHull(pts);
        auto [a, b] = diameterRotatingCalipers(hull);
        cout << a.x << ' ' << a.y << ' ' << b.x << ' ' << b.y;
        if (T) cout << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 모든 점이 이미 볼록 껍질 위(예: 정다각형) → 캘리퍼스가 올바르게 한 바퀴만 순회하는지
- 점이 2개뿐인 경우 → 껍질 크기 2의 예외 처리 반환
- 좌표가 큰 정수(±1e7) → 교차곱·제곱거리 64비트 안전성 확인
- 동일 좌표 중복 입력이 없는 조건이지만, 코드 상 정렬·중복제거는 보수적으로 유지

## 제출 전 점검
- 출력 형식: 각 테스트케이스마다 `x1 y1 x2 y2` 한 줄, 마지막 줄 개행 처리
- 정렬 비교·교차곱 방향 부호와 `<= 0` 조건 일관성
- 제곱거리 비교로 실수 오차 배제, 최대값 갱신 로직 검토

## 참고자료
- Rotating Calipers 원리와 응용: Shamos, Toussaint; Antipodal pairs and the diameter of a convex polygon
- Andrew’s Monotone Chain Convex Hull


