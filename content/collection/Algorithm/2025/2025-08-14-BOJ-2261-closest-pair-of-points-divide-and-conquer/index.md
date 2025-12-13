---
title: "[Algorithm] C++ 백준 2261번: 가장 가까운 두 점"
description: "평면 상 N개의 점에서 가장 가까운 두 점의 제곱거리를 구합니다. x좌표로 정렬해 분할정복으로 좌·우 구간을 해결하고, y정렬 병합과 좁은 스트립에서 dy 제약으로 후보만 비교해 O(N log N)에 도달합니다. 64비트 안전, 안정 병합, dy 기반 조기 중단 등 구현 디테일까지 점검합니다."
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
- Problem-2261
- cpp
- C++
- Geometry
- 기하
- Computational Geometry
- 계산기하
- Closest Pair
- 최근접점
- Closest Pair of Points
- Divide and Conquer
- 분할정복
- Strip
- 스트립
- Sorting
- 정렬
- Sorting by X
- X좌표정렬
- Merge by Y
- Y좌표정렬
- Stable Merge
- 안정 병합
- Euclidean Distance
- 유클리드거리
- Squared Distance
- 제곱거리
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(N log N)
- Proof of Correctness
- 정당성 증명
- Invariant
- 불변식
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Overflow
- 오버플로
- 64-bit
- Long Long
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- String
- 문자열
- Graph
- 그래프
- Tree
- 트리
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Disjoint Set Union
- 유니온파인드
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Modulo
- 모듈러
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/2261
- 요약: 평면에 놓인 N(≤100,000)개의 점에서 두 점 사이의 거리의 제곱이 최소가 되는 값을 구하는 문제입니다. 출력은 제곱거리 값이며, 실수 오차 없이 정수 연산으로 해결해야 합니다.

## 입력/출력
```
<입력>
N
x1 y1
x2 y2
...
xN yN

<출력>
가장 가까운 두 점 사이 거리의 제곱
```

예시
```
3
0 0
0 3
4 0
```
```
9
```

## 접근 개요
- 핵심 아이디어는 분할정복입니다. 점들을 x좌표로 정렬해 좌/우 절반으로 나눈 뒤, 각 절반의 최소 제곱거리 d를 구하고, 경계 근처(가로 거리 < √d)에 있는 점들만 y정렬된 띠(strip)에서 비교합니다.
- strip은 y 오름차순으로 정렬되어 있어 한 점당 위쪽 소수의 점(이론적으로 상수 개)만 확인하면 됩니다. y 차이가 √d 이상이 되는 순간 이후는 비교를 중단할 수 있습니다.
- 모든 비교를 정수 제곱거리로 수행해 부동소수점 오차를 제거합니다.

## 알고리즘 설계
- 전처리: 전체 점을 x, 그다음 y로 정렬합니다.
- 재귀:
  - 구간 크기가 2~3이면 완전탐색으로 최소 제곱거리를 계산하고, 반환 전에 해당 구간을 y기준으로 정렬해 둡니다.
  - 좌/우 절반을 재귀 처리하면 두 부분 구간은 각각 y정렬 상태가 됩니다. 이를 병합 정렬 방식으로 y정렬을 유지하며 합칩니다.
  - 중앙선에서 |x - midX|^2 < d를 만족하는 점들만 strip에 모으고, strip을 y정렬 상태로 순회하며 dy^2 ≥ d가 되는 지점에서 비교를 끊습니다.
- 자료구조: 보조 버퍼를 사용하여 y정렬 병합을 O(n)에 수행합니다.
- 올바름 근거: 분할정복의 표준 최근접점 정리. 좌/우 최솟값 d보다 작은 해가 존재하면 중앙선 근방 폭 √d의 띠 내부에 한 쌍이 존재하고, y정렬 상태에서 상수 개의 이웃만 보면 충분합니다.

## 복잡도
- 시간: O(N log N)
- 공간: O(N) (y정렬 병합용 버퍼)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point {
    int x;
    int y;
};

static inline long long squaredDistance(const Point& a, const Point& b) {
    long long dx = static_cast<long long>(a.x) - static_cast<long long>(b.x);
    long long dy = static_cast<long long>(a.y) - static_cast<long long>(b.y);
    return dx * dx + dy * dy;
}

// Recursively computes the closest pair distance squared on points[l, r),
// assuming points are sorted by x. As a side effect, points[l, r) will be
// sorted by y when the function returns.
long long closestPairRec(vector<Point>& points, vector<Point>& buffer, int l, int r) {
    int count = r - l;
    if (count <= 3) {
        long long best = LLONG_MAX;
        for (int i = l; i < r; ++i) {
            for (int j = i + 1; j < r; ++j) {
                best = min(best, squaredDistance(points[i], points[j]));
            }
        }
        sort(points.begin() + l, points.begin() + r, [](const Point& a, const Point& b) {
            if (a.y != b.y) return a.y < b.y;
            return a.x < b.x;
        });
        return best;
    }

    int mid = (l + r) / 2;
    int midX = points[mid].x;

    long long dLeft  = closestPairRec(points, buffer, l, mid);
    long long dRight = closestPairRec(points, buffer, mid, r);
    long long d = min(dLeft, dRight);

    // Merge by y to keep points[l, r) sorted by y
    int i = l, j = mid, k = l;
    while (i < mid && j < r) {
        if (points[i].y < points[j].y || (points[i].y == points[j].y && points[i].x <= points[j].x)) {
            buffer[k++] = points[i++];
        } else {
            buffer[k++] = points[j++];
        }
    }
    while (i < mid) buffer[k++] = points[i++];
    while (j < r)   buffer[k++] = points[j++];
    for (int t = l; t < r; ++t) points[t] = buffer[t];

    // Build strip: points within sqrt(d) in x from the dividing line, strip already sorted by y
    static vector<Point> strip;
    strip.clear();
    strip.reserve(r - l);
    for (int t = l; t < r; ++t) {
        long long dx = static_cast<long long>(points[t].x) - midX;
        if (dx * dx < d) strip.push_back(points[t]);
    }

    // Compare each point with subsequent points whose y-distance is < sqrt(d)
    for (size_t a = 0; a < strip.size(); ++a) {
        for (size_t b = a + 1; b < strip.size(); ++b) {
            long long dy = static_cast<long long>(strip[b].y) - strip[a].y;
            if (dy * dy >= d) break; // y too far; later points will be even farther in y
            d = min(d, squaredDistance(strip[a], strip[b]));
        }
    }
    return d;
}

long long closestPair(vector<Point>& points) {
    sort(points.begin(), points.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
    });
    vector<Point> buffer(points.size());
    return closestPairRec(points, buffer, 0, static_cast<int>(points.size()));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Point> points(n);
    for (int i = 0; i < n; ++i) {
        cin >> points[i].x >> points[i].y;
    }

    cout << closestPair(points) << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 같은 좌표의 점이 존재하는 경우(정답 0) 처리
- N=2 최소 크기, N이 큰 경우(1e5) 성능 확인
- 큰 좌표 범위로 인한 64-bit 오버플로 방지: 제곱 연산은 `long long`
- x가 같은 점 다수(수직 정렬)에서의 strip 구성 및 y병합 일관성

## 제출 전 점검
- 입출력 버퍼링(`sync_with_stdio(false)`, `tie(nullptr)`) 적용
- 초기 정렬은 (x, y), 부분 문제 반환 시 (y, x) 정렬 유지 확인
- dy^2 ≥ d에서 즉시 중단되어 비교 수가 제한되는지 확인

## 참고자료
- 분할정복 최근접점 알고리즘 표준 증명 및 구현 노트
- CLRS, Computational Geometry 챕터: Closest Pair of Points


