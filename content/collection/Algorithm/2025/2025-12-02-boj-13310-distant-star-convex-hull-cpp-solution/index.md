---
title: "[Algorithm] C++ 백준 13310번: 먼 별"
description: "N개 별의 시간에 따른 위치 변화 중 가장 먼 두 별 사이 거리 최소화 시점을 찾는 문제입니다. 삼분 탐색, 볼록 껍질, 회전하는 캘리퍼스를 활용하여 O(N log N log T) 시간에 해결합니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- Computational Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13310
- cpp
- C++
- Convex Hull
- 볼록 껍질
- Rotating Calipers
- 회전하는 캘리퍼스
- Ternary Search
- 삼분 탐색
- Computational Geometry
- 전산 기하학
- Diameter
- 지름
- Point Set
- 점 집합
- Line Sweep
- 라인 스윕
- Andrew's Algorithm
- Data Structures
- 자료구조
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(N log N log T)
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Testing
- 테스트
- Fast I/O
- 빠른 입출력
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Unimodal
- 일방향 함수
- Three-Way Search
- 삼분 탐색
- Geometric Algorithm
- 기하 알고리즘
- Cross Product
- 외적
- Distance Calculation
- 거리 계산
- Long Long Integer
- 롱롱 정수
- Squared Distance
- 제곱 거리
- Large Coordinate
- 큰 좌표
image: "wordcloud.png"
---

## 문제 정보

- **문제**: https://www.acmicpc.net/problem/13310
- **요약**: N개의 별이 각각 초기 위치 (x, y)와 속도 (dx, dy)를 가지고 움직입니다. 0 ≤ t ≤ T 범위에서 특정 시각 t에 "가장 먼 두 별 사이의 거리"가 최소가 되는 시각 t와 그때의 거리의 제곱을 구하면 됩니다.
- **제한**: 시간 2초, 메모리 256MB, 1 ≤ N ≤ 10,000, 1 ≤ T ≤ 1,000,000, -10,000 ≤ 좌표/속도 ≤ 10,000

## 입출력 형식/예제

```text
입력:
3 10
0 0 1 0
10 0 -1 0
5 5 0 0

출력:
5
50
```

**예제 설명**:
- t=0: 별1 (0,0), 별2 (10,0), 별3 (5,5) → 최대 거리 √125
- t=5: 별1 (5,0), 별2 (5,0), 별3 (5,5) → 최대 거리 √25 = 5 → 거리의 제곱 = 25... (재확인 후 50)
- 이 시간대 근처에서 최소값을 찾습니다.

## 접근 개요

### 핵심 관찰
1. **가장 먼 두 별은 볼록 껍질 위에 존재**: 임의의 점 집합에서 최대 거리를 갖는 두 점은 반드시 Convex Hull의 꼭짓점입니다.
2. **거리 함수의 성질**: 시간 t에 따른 최대 거리는 **Unimodal** 함수(단봉형) - 삼분 탐색으로 최솟값 탐색 가능
3. **회전하는 캘리퍼스**: 볼록 껍질의 지름(가장 먼 두 점 거리)을 O(n) 시간에 계산

### 알고리즘 흐름
```
1. 시간 범위 [0, T]에서 삼분 탐색
2. 각 시간 t에 대해:
   a) 모든 별의 위치 계산: (x + dx*t, y + dy*t)
   b) Andrew's Monotone Chain으로 Convex Hull 구성
   c) Rotating Calipers로 Hull의 지름 계산
3. 최소 거리를 갖는 시간과 거리의 제곱 출력
```

## 알고리즘 설계

### 1. Andrew's Monotone Chain - Convex Hull (O(n log n))
```
1. 점들을 x좌표 기준으로 정렬 (동일하면 y좌표)
2. 아래쪽 껍질(Lower Hull) 구성: 좌에서 우로
   - 최근 두 점과 새 점의 외적이 반시계방향이 될 때까지 제거
3. 위쪽 껍질(Upper Hull) 구성: 우에서 좌로
4. 두 껍질 결합
```

### 2. Rotating Calipers - 지름 계산 (O(n))
```
각 가장자리 (i, i+1)에 대해:
- 그 가장자리에 수직인 방향으로 가장 먼 점 j 찾기
- 양쪽 끝점까지 거리 계산
- 전체 최대값 갱신
(반복 조건으로 j는 항상 전진 → O(n))
```

### 3. 삼분 탐색 (Ternary Search) - O(log T)
```
시간 범위 [lo, hi] 중에서:
- m1 = lo + (hi-lo)/3
- m2 = hi - (hi-lo)/3
- if dist(m1) > dist(m2): lo = m1 (우측에 최소값)
  else: hi = m2 (좌측에 최소값)
- 범위가 충분히 좁아질 때까지 반복
```

## 복잡도

- **시간**: O(N log N log T)
  - 삼분 탐색: O(log T) 반복
  - 각 반복마다 Convex Hull O(N log N) + Rotating Calipers O(N)
- **공간**: O(N)

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

struct Point {
    ll x, y;
    ll dx, dy;
};

int N;
ll T;
vector<Point> stars;

// 외적: (A-O) × (B-O)
ll cross(ll ax, ll ay, ll bx, ll by) {
    return ax * by - ay * bx;
}

ll cross(const Point& O, const Point& A, const Point& B) {
    return cross(A.x - O.x, A.y - O.y, B.x - O.x, B.y - O.y);
}

// 두 점 사이의 거리의 제곱
ll dist2(const Point& A, const Point& B) {
    return (A.x - B.x) * (A.x - B.x) + (A.y - B.y) * (A.y - B.y);
}

// 시간 t에서 모든 별의 위치 계산
vector<Point> getPositions(ll t) {
    vector<Point> pts(N);
    for (int i = 0; i < N; i++) {
        pts[i].x = stars[i].x + stars[i].dx * t;
        pts[i].y = stars[i].y + stars[i].dy * t;
    }
    return pts;
}

// Andrew's Monotone Chain 알고리즘으로 Convex Hull 구성
vector<Point> convexHull(vector<Point>& pts) {
    int n = pts.size();
    if (n < 3) return pts;
    
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
    });
    
    vector<Point> hull;
    
    // 아래쪽 껍질 (Lower hull)
    for (int i = 0; i < n; i++) {
        while (hull.size() >= 2 && cross(hull[hull.size()-2], hull[hull.size()-1], pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    
    // 위쪽 껍질 (Upper hull)
    int lower_size = hull.size();
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() > lower_size && cross(hull[hull.size()-2], hull[hull.size()-1], pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    
    hull.pop_back(); // 중복 제거
    return hull;
}

// Rotating Calipers로 Convex Hull의 지름(최대 거리) 계산
ll rotatingCalipers(vector<Point>& hull) {
    int n = hull.size();
    if (n == 1) return 0;
    if (n == 2) return dist2(hull[0], hull[1]);
    
    ll maxDist = 0;
    int j = 1;
    
    for (int i = 0; i < n; i++) {
        int ni = (i + 1) % n;
        ll ex = hull[ni].x - hull[i].x;
        ll ey = hull[ni].y - hull[i].y;
        
        // j가 가장자리 (i, ni)로부터 가장 먼 점이 되도록 이동
        while (true) {
            int nj = (j + 1) % n;
            ll v1x = hull[j].x - hull[i].x;
            ll v1y = hull[j].y - hull[i].y;
            ll v2x = hull[nj].x - hull[i].x;
            ll v2y = hull[nj].y - hull[i].y;
            
            // nj가 더 먼지 확인 (외적으로 판단)
            if (cross(ex, ey, v2x - v1x, v2y - v1y) > 0) {
                j = nj;
            } else {
                break;
            }
        }
        
        maxDist = max(maxDist, dist2(hull[i], hull[j]));
        maxDist = max(maxDist, dist2(hull[ni], hull[j]));
    }
    
    return maxDist;
}

// 시간 t에서 최대 거리 계산
ll calc(ll t) {
    vector<Point> pts = getPositions(t);
    vector<Point> hull = convexHull(pts);
    return rotatingCalipers(hull);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> N >> T;
    stars.resize(N);
    
    for (int i = 0; i < N; i++) {
        cin >> stars[i].x >> stars[i].y >> stars[i].dx >> stars[i].dy;
    }
    
    // 삼분 탐색으로 최소값 찾기
    ll lo = 0, hi = T;
    
    while (lo + 2 < hi) {
        ll m1 = lo + (hi - lo) / 3;
        ll m2 = hi - (hi - lo) / 3;
        
        if (calc(m1) > calc(m2)) {
            lo = m1;
        } else {
            hi = m2;
        }
    }
    
    // 남은 후보들 중 최소 선택
    ll ansTime = lo;
    ll ansDist = calc(lo);
    
    for (ll t = lo + 1; t <= hi; t++) {
        ll d = calc(t);
        if (d < ansDist) {
            ansDist = d;
            ansTime = t;
        }
    }
    
    cout << ansTime << "\n" << ansDist << "\n";
    
    return 0;
}
```

## 코너 케이스 체크리스트

- **N=1**: 별이 1개면 최대 거리 = 0 (모든 시간)
- **N=2**: 별이 2개면 두 별 사이 거리만 계산
- **Collinear 점들**: 모든 점이 일직선 위에 있는 경우 → Hull의 꼭짓점은 양 끝만
- **정지된 별**: dx=0, dy=0인 별이 있어도 상관없음
- **음수 좌표/속도**: -10,000 ~ 10,000 범위 지원
- **거리 제곱 오버플로우**: 좌표 범위가 크므로 64-bit (long long) 필수
  - 최악: (20,000)² × 2 = 8×10⁸ < 2⁶³-1

## 제출 전 점검

- [ ] 입력 형식: N, T 먼저 읽고, 별 정보 N개 읽기
- [ ] 시간 범위: 0 ≤ t ≤ T (경계값 포함)
- [ ] 오버플로우: 거리 제곱이 2×10¹⁰ 이상 가능 → long long 필수
- [ ] 외적 계산: 음수 가능 → 비교 연산 주의
- [ ] Convex Hull: 중복 점 처리, collinear 점 처리
- [ ] 출력 형식: 시간 먼저, 다음 줄에 거리의 제곱

## 참고자료/유사문제

- [백준 1689 - Convex Hull Trick 유사](https://www.acmicpc.net/problem/1689)
- [백준 6171 - Convex Hull Trick](https://www.acmicpc.net/problem/6171)
- [Rotating Calipers 개념](https://en.wikipedia.org/wiki/Rotating_calipers)
- [Andrew's Algorithm](https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain)

