---
title: "[Algorithm] cpp 백준 2626번: 헬기착륙장"
description: "N개 섬의 최적 헬기착륙장 위치를 찾는 최소 외접원(MEC) 문제입니다. Welzl의 랜덤화 선형 시간 알고리즘으로 원의 중심과 반지름을 구하고, 세 점의 외접원 계산과 일직선 처리로 견고한 기하 구현을 합니다."
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
- Problem-2626
- cpp
- C++
- Minimum Enclosing Circle
- 최소 외접원
- MEC
- Welzl Algorithm
- 웰츠 알고리즘
- Randomized Algorithm
- 랜덤화 알고리즘
- Computational Geometry
- 전산 기하학
- Circle
- 원
- Circumcircle
- 외접원
- Center
- 중심
- Radius
- 반지름
- Point Set
- 점 집합
- Smallest Enclosing
- 최소 포함
- Data Structures
- 자료구조
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(n) Expected Time
- Expected Linear Time
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Collinear Points
- 일직선 점
- Degenerate Cases
- 퇴화 사례
- Testing
- 테스트
- Fast I/O
- 빠른 입출력
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Recursion
- 재귀
- Distance Calculation
- 거리 계산
- Double Precision
- 배정도
- Floating Point
- 부동 소수점
- KOI 2002
- Korean Informatics Olympiad
- 한국정보올림피아드
- High School Division
- 고등부
- Regional Contest
- 지역본선
image: "wordcloud.png"
---

## 문제 정보

- **문제**: https://www.acmicpc.net/problem/2626
- **요약**: 바다 위 N개 섬의 좌표가 주어질 때, 모든 섬을 포함하면서 착륙장으로부터 가장 먼 섬까지의 직선거리를 최소화하는 헬기착륙장의 위치(x, y 좌표)와 그 거리를 구합니다. 이는 점 집합의 최소 외접원(Minimum Enclosing Circle)을 찾는 문제입니다.
- **제한**: 시간 1초, 메모리 128MB, 2 ≤ N ≤ 1,000, -30,000 ≤ 좌표 ≤ 30,000

## 입출력 형식/예제

```text
입력:
5
5 -2
-3 -2
-2 5
1 6
0 2

출력:
1.000 1.000
5.000
```

**예제 설명**:
- 5개 섬의 위치가 주어짐
- 최적 착륙장 위치: (1.0, 1.0)
- 이 위치에서 가장 먼 섬까지의 거리: 5.0

## 접근 개요

### 핵심 관찰

최소 외접원(MEC)의 성질:
1. **경계 점**: 원의 경계 위에는 최소 2개, 최대 3개의 점이 위치합니다
2. **2개 점**: 두 점을 지름의 양 끝으로 하는 원이 유일합니다
3. **3개 점**: 세 점을 지나는 외접원이 유일합니다 (일직선 제외)
4. **재귀 구조**: 한 점을 고정하면, 나머지 점들에 대한 더 작은 MEC 부분 문제로 분해

### Welzl 알고리즘

랜덤화 선형 시간 알고리즘으로, 기대 시간복잡도 O(n)을 달성합니다:

```
1. 점들을 랜덤하게 섞음
2. 점을 하나씩 추가 처리:
   - 현재 점이 기존 원 안에 있으면 원 유지
   - 원 밖에 있으면 해당 점이 경계에 포함되어야 함
3. 경계 점 개수에 따라 원 계산:
   - 0개: 빈 원 (반지름 0)
   - 1개: 점 자신 (반지름 0)
   - 2개: 두 점을 지름으로 하는 원
   - 3개: 세 점의 외접원
```

## 알고리즘 설계

### 기본 연산

#### 1. 두 점 사이 거리
```
distance(A, B) = sqrt((A.x - B.x)² + (A.y - B.y)²)
```

#### 2. 두 점을 지름으로 하는 원
```
center = ((A.x + B.x)/2, (A.y + B.y)/2)
radius = distance(A, center)
```

#### 3. 세 점의 외접원
세 점 A, B, C의 외접원을 구하는 방법:

벡터를 이용한 계산:
```
ax = B.x - A.x, ay = B.y - A.y
bx = C.x - A.x, by = C.y - A.y
d = 2(ax·by - ay·bx)  (외적의 z-성분 × 2)

cx = A.x + (by·(ax² + ay²) - ay·(bx² + by²)) / d
cy = A.y + (ax·(bx² + by²) - bx·(ax² + ay²)) / d
```

**일직선 처리**: 외적이 0에 가까우면 세 점이 일직선 위에 있으므로, 가장 먼 두 점을 지름으로 하는 원 사용

#### 4. 점과 원의 관계 판정
```
isInside(circle, point) ⟺ distance(circle.center, point) ≤ circle.radius + EPS
```
(부동소수점 오차 대비 작은 여유값 EPS 사용)

### Welzl 재귀 함수

```
welzl(P, R, n):
  // P: 처리할 점 배열, R: 경계 점 집합, n: 현재 인덱스
  
  base case:
    if n = 0 or |R| = 3:
      return 경계점으로부터_원_계산(R)
  
  재귀:
    1. P에서 인덱스 idx 선택 (랜덤)
    2. 해당 점 p = P[idx] 추출
    3. D = welzl(P, R, n-1)  // 나머지 점들로 재귀
    
    4. if isInside(D, p):
        return D  // p가 이미 원 안에 있음
    
    5. p를 경계 점으로 추가: R' = R ∪ {p}
    6. return welzl(P, R', n-1)  // p를 경계로 포함한 재귀
```

## 복잡도

- **시간**: O(n) 기대 시간복잡도
  - 랜덤화된 입력에 대해 평균적으로 선형 시간
  - 최악: O(n²) (매우 드문 경우)
  
- **공간**: O(n) 재귀 스택 + 점 배열

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

const double EPS = 1e-10;

struct Point {
    double x, y;
};

struct Circle {
    Point c;
    double r;
};

double dist(Point a, Point b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

// 두 점을 지름으로 하는 원
Circle makeCircle2(Point a, Point b) {
    Point c = {(a.x + b.x) / 2, (a.y + b.y) / 2};
    return {c, dist(a, c)};
}

// 세 점을 지나는 외접원
Circle makeCircle3(Point a, Point b, Point c) {
    double ax = b.x - a.x, ay = b.y - a.y;
    double bx = c.x - a.x, by = c.y - a.y;
    double d = 2 * (ax * by - ay * bx);
    
    if (abs(d) < EPS) {
        // 세 점이 일직선 - 가장 먼 두 점으로 원 생성
        double d1 = dist(a, b);
        double d2 = dist(b, c);
        double d3 = dist(c, a);
        if (d1 >= d2 && d1 >= d3) return makeCircle2(a, b);
        if (d2 >= d1 && d2 >= d3) return makeCircle2(b, c);
        return makeCircle2(c, a);
    }
    
    double s = (ax * ax + ay * ay);
    double t = (bx * bx + by * by);
    double cx = a.x + (by * s - ay * t) / d;
    double cy = a.y + (ax * t - bx * s) / d;
    
    Point center = {cx, cy};
    return {center, dist(center, a)};
}

// 점이 원 안에 있는지 확인
bool isInside(Circle cir, Point p) {
    return dist(cir.c, p) <= cir.r + EPS;
}

// 경계 점들로부터 최소 외접원 생성
Circle makeCircleFromBoundary(vector<Point>& R) {
    if (R.empty()) return {{0, 0}, 0};
    if (R.size() == 1) return {R[0], 0};
    if (R.size() == 2) return makeCircle2(R[0], R[1]);
    return makeCircle3(R[0], R[1], R[2]);
}

// Welzl 알고리즘
Circle welzl(vector<Point>& P, vector<Point> R, int n) {
    if (n == 0 || R.size() == 3) {
        return makeCircleFromBoundary(R);
    }
    
    // 랜덤하게 선택된 점 제거
    int idx = rand() % n;
    Point p = P[idx];
    swap(P[idx], P[n - 1]);
    
    Circle D = welzl(P, R, n - 1);
    
    if (isInside(D, p)) {
        swap(P[idx], P[n - 1]);
        return D;
    }
    
    R.push_back(p);
    Circle result = welzl(P, R, n - 1);
    swap(P[idx], P[n - 1]);
    return result;
}

Circle minEnclosingCircle(vector<Point>& points) {
    vector<Point> P = points;
    random_shuffle(P.begin(), P.end());
    return welzl(P, {}, P.size());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    srand(42); // 재현성을 위한 시드
    
    int n;
    cin >> n;
    
    vector<Point> points(n);
    for (int i = 0; i < n; i++) {
        cin >> points[i].x >> points[i].y;
    }
    
    Circle result = minEnclosingCircle(points);
    
    cout << fixed << setprecision(3);
    cout << result.c.x << " " << result.c.y << "\n";
    cout << result.r << "\n";
    
    return 0;
}
```

## 코너 케이스 체크리스트

- **단일 점 (N=1)**: 반지름 0인 원 (단, 문제에서 N ≥ 2)
- **두 점 (N=2)**: 두 점의 중점이 중심, 두 점 사이 거리의 절반이 반지름
- **일직선 상 점들**: 일직선 점 3개 감지 시 가장 먼 두 점으로 원 형성
- **정삼각형**: 세 외접원 계산이 정확한지 확인
- **큰 좌표 범위**: -30,000 ~ 30,000 범위의 좌표, 거리 계산에서 오버플로우 없음 (double 사용)
- **출력 정밀도**: 소수점 셋째 자리까지 정확히 반올림 (setprecision(3))
- **부동소수점 오차**: 원 내부 판정에 EPS = 1e-10 여유값 사용

## 제출 전 점검

- [ ] 입력 형식: N을 읽고 N개의 (x, y) 쌍 읽기
- [ ] 출력 형식: 중심 좌표 한 줄, 반지름 한 줄, 소수점 3자리
- [ ] 원 내부 판정: EPS 여유값으로 안정성 확보
- [ ] 세 점 외접원: 외적이 0에 가까운 일직선 경우 처리
- [ ] 랜덤 시드: 재현성을 위해 고정 시드 사용
- [ ] 부동소수점 정밀도: double 자료형으로 충분

## 참고자료/유사문제

- [Emo Welzl의 원문](https://inf.ethz.ch/personal/emo/PublDPS/smallest.pdf) - 최소 외접원 기원 논문
- [백준 17399 - 트리 외심](https://www.acmicpc.net/problem/17399) - 기하 응용
- [백준 13310 - 먼 별](https://www.acmicpc.net/problem/13310) - 볼록껍질과의 조합
- [CP-Algorithms: Minimum Enclosing Circle](https://cp-algorithms.com/geometry/minmax-circle.html)
- [쌍대성과 최소 외접원](https://en.wikipedia.org/wiki/Smallest-circle_problem)


