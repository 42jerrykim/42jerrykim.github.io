---
title: "[Algorithm] C++/Python 백준 4225번 : 쓰레기 슈트"
categories: 
- Algorithm
- Geometry
- Convex Hull
tags:
- Convex Hull
- Rotating Calipers
- Computational Geometry
- O(N log N)
- Geometry
image: "tmp_wordcloud.png"
date: 2024-01-01
---

이번 포스팅에서는 백준 온라인 저지의 4225번 문제인 **'쓰레기 슈트'**를 해결해보겠다. 이 문제는 기하학적인 접근이 필요한 문제로, 다각형이 회전하여 통과할 수 있는 최소 너비의 슈트를 계산하는 문제이다. Convex Hull과 Rotating Calipers 알고리즘을 활용하여 효율적으로 해결할 수 있다.

문제 : [https://www.acmicpc.net/problem/4225](https://www.acmicpc.net/problem/4225)

## 문제 설명

선영이는 빌딩에 설치할 쓰레기 슈트의 최소 너비를 구하려고 한다. 쓰레기 슈트는 일정한 너비를 가진 속이 빈 튜브로, 물체를 상단에 넣으면 회전하지 않고 일직선으로 떨어진다. 물체는 슈트에 들어갈 수 있도록 회전시킬 수 있지만, 슈트 내부에서는 회전하지 않는다.

물체는 2차원 다각형으로 모델링되며, 선영이는 이 다각형이 통과할 수 있는 가장 작은 슈트의 너비를 구하고자 한다. 슈트의 너비는 최소화되어야 하며, 이는 물체를 적절히 회전시켜 슈트를 통과시킬 수 있는 최소 너비를 찾는 문제로 귀결된다.

입력은 여러 개의 테스트 케이스로 구성되며, 각 테스트 케이스는 다각형의 꼭짓점의 개수와 각 꼭짓점의 좌표로 주어진다. 출력은 각 테스트 케이스마다 물체가 통과할 수 있는 최소 슈트의 너비를 소수점 둘째 자리까지 올림하여 출력한다.

## 접근 방식

이 문제는 주어진 다각형이 회전하여 통과할 수 있는 최소 너비를 구하는 기하학 문제이다. 이를 해결하기 위해 다음과 같은 알고리즘과 방법을 사용한다:

1. **Convex Hull 계산**: 다각형의 Convex Hull을 계산한다. Convex Hull은 다각형의 외곽을 감싸는 최소한의 볼록 다각형으로, 물체의 회전과 관계없이 최소 너비를 구하는 데 유용하다.

2. **Rotating Calipers 알고리즘**: Convex Hull의 각 변에 대해 수직 방향으로 물체를 투영하여 최소 너비를 구한다. 이때, Rotating Calipers 알고리즘을 사용하여 모든 가능한 방향에 대해 효율적으로 최소 너비를 계산한다.

3. **최소 너비 계산**: 각 투영 방향에서의 최대 거리 차이를 계산하여 그 중 최소 값을 선택한다.

시간 복잡도는 Convex Hull 계산에 O(N log N), Rotating Calipers 알고리즘에 O(N)이므로 전체 알고리즘은 O(N log N)이다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

const double EPS = 1e-10;

struct Point {
    double x, y;
    Point() {}
    Point(double x, double y) : x(x), y(y) {}
    Point operator - (const Point& p) const {
        return Point(x - p.x, y - p.y);
    }
    bool operator < (const Point& p) const {
        if (fabs(x - p.x) > EPS)
            return x < p.x;
        return y < p.y;
    }
    double cross(const Point& p) const {
        return x * p.y - y * p.x;
    }
};

typedef vector<Point> Polygon;

// 두 점과 기준점 O에서의 외적을 계산하여 반시계 방향인지 확인
double cross(const Point& O, const Point& A, const Point& B) {
    return (A - O).cross(B - O);
}

// Convex Hull을 계산하는 함수 (Andrew's Monotone Chain 알고리즘)
Polygon convexHull(vector<Point>& P) {
    int n = P.size(), k = 0;
    if (n == 1) return P;
    sort(P.begin(), P.end()); // 점들을 x, y 순으로 정렬
    Polygon H(2 * n);
    // 하단 Convex Hull 계산
    for (int i = 0; i < n; i++) {
        while (k >= 2 && cross(H[k - 2], H[k - 1], P[i]) <= EPS) k--;
        H[k++] = P[i];
    }
    // 상단 Convex Hull 계산
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross(H[k - 2], H[k - 1], P[i]) <= EPS) k--;
        H[k++] = P[i];
    }
    H.resize(k - 1);
    return H;
}

// Convex Hull에서 최소 너비를 계산하는 함수
double minimalWidth(const Polygon& hull) {
    int n = hull.size();
    double minWidth = 1e20;
    for (int i = 0; i < n; i++) {
        // 현재 변에 수직인 방향 벡터 계산
        Point edge = hull[(i + 1) % n] - hull[i];
        Point perp(-edge.y, edge.x);
        // 단위 벡터로 정규화
        double len = sqrt(perp.x * perp.x + perp.y * perp.y);
        perp.x /= len;
        perp.y /= len;
        // 모든 점을 수직 방향으로 투영하여 최대, 최소값 계산
        double minP = 1e20, maxP = -1e20;
        for (int j = 0; j < n; j++) {
            double proj = hull[j].x * perp.x + hull[j].y * perp.y;
            minP = min(minP, proj);
            maxP = max(maxP, proj);
        }
        // 현재 방향에서의 너비 계산
        double width = maxP - minP;
        minWidth = min(minWidth, width);
    }
    return minWidth;
}

// 소수점 둘째 자리까지 올림하는 함수
double roundUpTo0p01(double value) {
    return ceil(value * 100.0 - EPS) / 100.0;
}

int main() {
    int testCase = 1;
    while (true) {
        int n;
        cin >> n;
        if (n == 0) break;
        vector<Point> poly(n);
        for (int i = 0; i < n; i++) {
            double xi, yi;
            cin >> xi >> yi;
            poly[i] = Point(xi, yi);
        }
        // Convex Hull 계산
        Polygon hull = convexHull(poly);
        // 최소 너비 계산
        double minWidth = minimalWidth(hull);
        // 소수점 둘째 자리까지 올림
        minWidth = roundUpTo0p01(minWidth);
        // 결과 출력
        printf("Case %d: %.2f\n", testCase++, minWidth);
    }
    return 0;
}
```

### 코드 설명

1. **Point 구조체**: 2차원 좌표를 표현하며, 벡터 연산과 비교 연산자를 오버로딩하였다.

2. **convexHull 함수**: Andrew's Monotone Chain 알고리즘을 사용하여 Convex Hull을 계산한다. 점들을 x좌표, y좌표 순으로 정렬한 후 하단과 상단 Convex Hull을 각각 계산한다.

3. **minimalWidth 함수**: Convex Hull의 각 변에 대해 수직 벡터를 계산하고, 그 방향으로 모든 점을 투영하여 최대값과 최소값의 차이인 너비를 계산한다. 모든 변에 대해 최소 너비를 갱신한다.

4. **roundUpTo0p01 함수**: 계산된 최소 너비를 소수점 둘째 자리까지 올림한다.

5. **main 함수**: 입력을 받아 Convex Hull과 최소 너비를 계산하고 형식에 맞게 출력을 한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

#define EPS 1e-10
#define MAXN 105

typedef struct {
    double x, y;
} Point;

// 절댓값 함수 구현
double fabs(double x) {
    return x < 0 ? -x : x;
}

// 두 Point를 교환하는 함수
void swap(Point* a, Point* b) {
    Point temp = *a;
    *a = *b;
    *b = temp;
}

// Point를 비교하는 함수
int compare_points(const Point* p, const Point* q) {
    if (fabs(p->x - q->x) > EPS) {
        return (p->x > q->x) - (p->x < q->x);
    }
    return (p->y > q->y) - (p->y < q->y);
}

// QuickSort 알고리즘 구현
void quicksort(Point* P, int left, int right) {
    if (left >= right) return;
    int i = left, j = right;
    Point pivot = P[(left + right) / 2];
    while (i <= j) {
        while (compare_points(&P[i], &pivot) < 0) i++;
        while (compare_points(&P[j], &pivot) > 0) j--;
        if (i <= j) {
            swap(&P[i], &P[j]);
            i++;
            j--;
        }
    }
    if (left < j) quicksort(P, left, j);
    if (i < right) quicksort(P, i, right);
}

// 외적 계산 함수
double cross(Point O, Point A, Point B) {
    return (A.x - O.x)*(B.y - O.y) - (A.y - O.y)*(B.x - O.x);
}

// Convex Hull 계산 함수
int convexHull(Point* P, int n, Point* H) {
    int k = 0;
    quicksort(P, 0, n - 1); // 점들을 정렬
    // 하단 Convex Hull
    for (int i = 0; i < n; i++) {
        while (k >= 2 && cross(H[k - 2], H[k - 1], P[i]) <= EPS) k--;
        H[k++] = P[i];
    }
    // 상단 Convex Hull
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross(H[k - 2], H[k - 1], P[i]) <= EPS) k--;
        H[k++] = P[i];
    }
    return k - 1;
}

// 제곱근 함수 구현 (Newton-Raphson 방법)
double sqrt(double x) {
    double guess = x / 2;
    double epsilon = 1e-10;
    double diff;
    if (x == 0) return 0;
    do {
        double new_guess = (guess + x / guess) / 2;
        diff = new_guess - guess;
        if (diff < 0) diff = -diff;
        guess = new_guess;
    } while (diff > epsilon);
    return guess;
}

// 최소 너비 계산 함수
double minimalWidth(Point* hull, int n) {
    double minWidth = 1e20;
    for (int i = 0; i < n; i++) {
        // 현재 변의 수직 벡터 계산
        Point edge = {hull[(i + 1) % n].x - hull[i].x, hull[(i + 1) % n].y - hull[i].y};
        Point perp = {-edge.y, edge.x};
        // 단위 벡터로 정규화
        double len = sqrt(perp.x * perp.x + perp.y * perp.y);
        perp.x /= len;
        perp.y /= len;
        // 투영하여 최대, 최소값 계산
        double minP = 1e20, maxP = -1e20;
        for (int j = 0; j < n; j++) {
            double proj = hull[j].x * perp.x + hull[j].y * perp.y;
            if (proj < minP) minP = proj;
            if (proj > maxP) maxP = proj;
        }
        // 현재 방향에서의 너비 계산
        double width = maxP - minP;
        if (width < minWidth) minWidth = width;
    }
    return minWidth;
}

// 올림 함수 구현
double roundUpTo0p01(double value) {
    double temp = value * 100.0 - EPS;
    int int_part = (int)temp;
    if (temp > (double)int_part) int_part += 1;
    return ((double)int_part) / 100.0;
}

int main() {
    int testCase = 1;
    while (1) {
        int n;
        if (scanf("%d", &n) != 1 || n == 0) break;
        Point P[MAXN];
        for (int i = 0; i < n; i++) {
            scanf("%lf %lf", &P[i].x, &P[i].y);
        }
        Point H[2 * MAXN];
        int hn = convexHull(P, n, H);
        double minWidth = minimalWidth(H, hn);
        minWidth = roundUpTo0p01(minWidth);
        printf("Case %d: %.2f\n", testCase++, minWidth);
    }
    return 0;
}

```

### 코드 설명

- **라이브러리 제한**: `stdio.h`만 사용하여 구현하였다. `math.h`나 `stdlib.h`를 사용하지 않고 필요한 함수를 직접 구현하였다.

- **fabs 함수**: 실수의 절댓값을 계산하는 함수를 직접 구현하여 `fabs` 대체.

- **quicksort 함수**: `qsort`를 사용할 수 없으므로, 직접 QuickSort 알고리즘을 구현하여 점들을 정렬하였다.

- **sqrt 함수**: `sqrt` 함수를 사용할 수 없으므로, Newton-Raphson 방법을 사용하여 제곱근을 계산하는 함수를 구현하였다.

- **roundUpTo0p01 함수**: `ceil` 함수를 사용할 수 없으므로, 직접 올림 처리를 하는 함수를 구현하였다.

- **convexHull 함수**: Andrew's Monotone Chain 알고리즘을 사용하여 Convex Hull을 계산하였다.

- **minimalWidth 함수**: Convex Hull의 각 변에 대해 수직 벡터를 계산하고, 해당 방향으로 투영하여 최소 너비를 구하였다.

- **main 함수**: 입력을 받고 Convex Hull과 최소 너비를 계산하여 결과를 출력한다..

## Python 코드와 설명

```python
import sys
import math

EPS = 1e-10

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 벡터 뺄셈
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # 비교 연산자 오버로딩
    def __lt__(self, other):
        if abs(self.x - other.x) > EPS:
            return self.x < other.x
        return self.y < other.y

    # 외적 계산
    def cross(self, other):
        return self.x * other.y - self.y * other.x

def cross(O, A, B):
    return (A - O).cross(B - O)

def convexHull(P):
    P.sort()
    n = len(P)
    if n == 1:
        return P
    H = []
    # 하단 Convex Hull
    for p in P:
        while len(H) >= 2 and cross(H[-2], H[-1], p) <= EPS:
            H.pop()
        H.append(p)
    # 상단 Convex Hull
    t = len(H) + 1
    for p in reversed(P[:-1]):
        while len(H) >= t and cross(H[-2], H[-1], p) <= EPS:
            H.pop()
        H.append(p)
    return H[:-1]

def minimalWidth(hull):
    n = len(hull)
    minWidth = 1e20
    for i in range(n):
        edge = hull[(i + 1) % n] - hull[i]
        perp = Point(-edge.y, edge.x)
        len_perp = math.hypot(perp.x, perp.y)
        perp.x /= len_perp
        perp.y /= len_perp
        minP = 1e20
        maxP = -1e20
        for p in hull:
            proj = p.x * perp.x + p.y * perp.y
            minP = min(minP, proj)
            maxP = max(maxP, proj)
        width = maxP - minP
        minWidth = min(minWidth, width)
    return minWidth

def roundUpTo0p01(value):
    return math.ceil(value * 100.0 - EPS) / 100.0

def main():
    testCase = 1
    input_lines = sys.stdin.readlines()
    idx = 0
    while idx < len(input_lines):
        n = int(input_lines[idx])
        idx += 1
        if n == 0:
            break
        P = []
        for _ in range(n):
            x_str, y_str = input_lines[idx].split()
            idx += 1
            x, y = float(x_str), float(y_str)
            P.append(Point(x, y))
        hull = convexHull(P)
        minWidth = minimalWidth(hull)
        minWidth = roundUpTo0p01(minWidth)
        print(f"Case {testCase}: {minWidth:.2f}")
        testCase += 1

if __name__ == "__main__":
    main()
```

### 코드 설명

1. **Point 클래스**: 2차원 좌표를 나타내며, 벡터 연산과 비교 연산자를 오버로딩하였다.

2. **convexHull 함수**: 점들을 정렬한 후 Convex Hull을 계산한다.

3. **minimalWidth 함수**: Convex Hull의 각 변에 대해 수직 벡터를 계산하고, 해당 방향으로 투영하여 최소 너비를 구한다.

4. **roundUpTo0p01 함수**: 최소 너비를 소수점 둘째 자리까지 올림한다.

5. **main 함수**: 표준 입력으로부터 데이터를 받아 처리하고 결과를 출력한다.

## 결론

이 문제는 기하 알고리즘 중 Convex Hull과 Rotating Calipers를 활용하여 효율적으로 해결할 수 있었다. 회전 가능한 다각형의 최소 너비를 구하는 것은 실세계에서도 중요한 문제이며, 이러한 알고리즘의 적용 가능성을 확인할 수 있었다. 또한, 부동 소수점 연산에서의 오차를 고려하여 EPS를 사용하고, 출력 형식에 맞게 올림 처리하는 것의 중요성을 다시 한번 느꼈다. 추가적으로, 다양한 프로그래밍 언어로 구현해 봄으로써 알고리즘의 이해도를 높일 수 있었다.