---
title: "[Algorithm] C++/Python 백준 4225번 : 쓰레기 슈트"
description: "Convex Hull을 구한 뒤 모든 변에 수직인 방향으로 투영해 2차원 다각형의 최소 너비(쓰레기 슈트 너비)를 구하는 문제입니다. 변 방향 검사가 충분한 이유, O(N log N + h²) 복잡도, 올림 처리와 퇴화 입력까지 정리합니다."
categories: 
- Algorithm
- Geometry
- ConvexHull
tags:
- Time-Complexity(시간복잡도)
- Geometry
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- Python
- Implementation(구현)
- Coding-Test(코딩테스트)
- Data-Structures(자료구조)
- Optimization(최적화)
- Code-Quality(코드품질)
- Convex-Hull
- Computational-Geometry
- Sorting(정렬)
- Math(수학)
- Floating-Point(부동소수점)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Precision(정밀도)
- Monotone-Chain
- Best-Practices
- Complexity-Analysis(복잡도분석)
- Debugging(디버깅)
- Refactoring(리팩토링)
- Clean-Code(클린코드)
- Performance(성능)
- Pitfalls(함정)
- Error-Handling(에러처리)
image: "wordcloud.png"
date: 2024-01-01
lastmod: 2024-01-01
---

이번 포스팅에서는 백준 온라인 저지의 4225번 문제인 <strong>'쓰레기 슈트'</strong>를 해결해보겠다. 이 문제는 기하학적인 접근이 필요한 문제로, 다각형이 회전하여 통과할 수 있는 최소 너비의 슈트를 계산하는 문제이다. Convex Hull을 구한 뒤 hull의 모든 변 방향을 검사하는 방식으로 해결할 수 있다.

문제 : [https://www.acmicpc.net/problem/4225](https://www.acmicpc.net/problem/4225)

## 문제 설명

선영이는 빌딩에 설치할 쓰레기 슈트의 최소 너비를 구하려고 한다. 쓰레기 슈트는 일정한 너비를 가진 속이 빈 튜브로, 물체를 상단에 넣으면 회전하지 않고 일직선으로 떨어진다. 물체는 슈트에 들어갈 수 있도록 회전시킬 수 있지만, 슈트 내부에서는 회전하지 않는다.

물체는 2차원 다각형으로 모델링되며, 선영이는 이 다각형이 통과할 수 있는 가장 작은 슈트의 너비를 구하고자 한다. 슈트의 너비는 최소화되어야 하며, 이는 물체를 적절히 회전시켜 슈트를 통과시킬 수 있는 최소 너비를 찾는 문제로 귀결된다.

입력은 여러 개의 테스트 케이스로 구성되며, 각 테스트 케이스는 다각형의 꼭짓점의 개수와 각 꼭짓점의 좌표로 주어진다. 출력은 각 테스트 케이스마다 물체가 통과할 수 있는 최소 슈트의 너비를 소수점 둘째 자리까지 올림하여 출력한다.

## 접근 방식

물체가 슈트 안에서 회전하지 않고 일직선으로 떨어지므로, 필요한 슈트 너비는 물체를 어떤 방향으로 놓았을 때의 가로 폭이다. 방향을 단위 벡터 u로 두면 그 폭은 모든 꼭짓점을 u에 투영한 값의 최댓값에서 최솟값을 뺀 것이고, 이를 방향 u에서의 너비 w(u)라 한다. 문제의 답은 모든 방향에 대한 w(u)의 최솟값, 즉 다각형의 최소 너비(minimum width)다.

먼저 다각형 대신 Convex Hull만 보아도 된다. 볼록 껍질은 원래 점 집합의 모든 점을 포함하고 그 극점이 원래 점들 중에서 나오므로, 어느 방향으로 투영해도 최댓값·최솟값은 hull의 꼭짓점에서 결정된다. 따라서 w(u)는 hull로 계산해도 같다.

다음으로 검사할 방향이 무한히 많아 보이지만 hull의 변 개수 h개로 줄어든다. 방향이 조금 바뀔 때 투영의 최대·최소를 주는 꼭짓점이 고정돼 있으면 w(u)는 u에 대해 코사인 함수 형태(두 꼭짓점 차이 벡터와 u의 내적)로 움직이고, 이 함수는 극소점이 구간 내부가 아니라 구간 경계에서만 생긴다. 구간 경계는 최대 또는 최소 꼭짓점이 바뀌는 순간, 곧 u가 어떤 hull 변에 수직이 되는 순간이다. 그래서 최소 너비는 반드시 hull의 어떤 변과 평행한 두 지지선 사이의 거리로 얻어진다. 흔한 오해는 "중간 각도에서 더 좁은 너비가 나올 수 있다"는 생각인데, 위 논증에 따르면 변 방향만 검사해도 충분하다.

이 글의 구현은 다음 순서를 따른다.

1. **Convex Hull 계산**: Andrew's Monotone Chain으로 hull을 구한다. 점을 정렬하는 데 O(N log N)이 든다.

2. **변 수직 방향별 투영**: hull의 각 변 (hull[i], hull[i+1])에 대해 수직 단위 벡터를 만들고, hull의 모든 꼭짓점을 그 방향에 투영해 최댓값과 최솟값의 차를 구한다. 변이 h개이고 변마다 h개의 꼭짓점을 훑으므로 O(h²)이다.

3. **최소 선택과 올림**: 변별 너비 중 최솟값을 고른 뒤 소수점 둘째 자리로 올림해 출력한다.

시간 복잡도는 O(N log N + h²)이고 h ≤ N이다. N이 작은 이 문제에서는 충분하다. h가 큰 입력에서는 Rotating Calipers(회전 캘리퍼스)로 각 변의 반대편 꼭짓점을 두 포인터로 이동시켜 투영 단계를 O(h)로 줄일 수 있고, 이때 전체가 O(N log N)이 된다. 이 글의 코드는 그 최적화를 구현하지 않았다. 원리는 Toussaint(1983)의 "Solving Geometric Problems with the Rotating Calipers"에 정리돼 있다.

```mermaid
flowchart LR
    A["입력 점 N개"] --> B["Convex Hull 계산</br>O(N log N)"]
    B --> C["hull 변 i마다</br>수직 단위 벡터 생성"]
    C --> D["모든 hull 꼭짓점 투영</br>최댓값 − 최솟값 = 너비"]
    D --> E["너비 최솟값 갱신"]
    E --> F["소수점 둘째 자리 올림 출력"]
```

### 손으로 따라가 보기

한 변이 2인 정사각형 (0,0), (2,0), (2,2), (0,2)로 확인해 보자. hull은 네 꼭짓점 그대로이고 변은 네 개다. 변 (0,0)→(2,0)의 수직 방향은 (0,1)이며 네 꼭짓점의 투영값은 0, 0, 2, 2이므로 너비는 2다. 나머지 세 변도 대칭이라 모두 2가 나오고 답은 2.00이다. 같은 정사각형을 45도 기울인 방향으로 투영하면 너비가 대각선 길이 2√2 ≈ 2.83이 되어 더 크다. 변 방향이 최소라는 앞의 논증이 이 예에서도 맞아떨어지는 것이다. 직각 이등변삼각형 (0,0), (1,0), (0,1)에서는 빗변에 수직인 방향의 너비가 1/√2 ≈ 0.7071로 두 직각변 방향의 너비 1보다 작고, 올림하면 0.71이 출력된다. 즉 가장 긴 변이 아니라 모든 변을 검사해 최솟값을 골라야 한다는 점이 구현의 핵심이다.

### 정밀도와 구현상의 주의

이 풀이의 오차 원천은 세 가지다. 첫째, 정렬 비교와 외적 부호 판정에 EPS를 쓰므로 좌표 크기에 비해 EPS가 지나치게 작거나 크면 공선 점의 pop 여부가 달라진다. 입력이 정수 좌표라면 외적을 정수로 계산해 EPS 없이 정확히 판정하는 편이 더 안전하다. 둘째, 변 길이로 나눠 정규화한 뒤 투영하는 과정에서 부동소수점 반올림이 누적된다. 정규화하지 않고 외적 값과 변 길이의 비로 거리를 구하면 나눗셈을 한 번으로 줄일 수 있다. 셋째, 올림은 가장 민감한 단계다. 참값이 정확히 0.71인데 계산값이 0.7100000000000001이면 단순 `ceil`은 0.72를 출력한다. 그래서 `value*100`에서 EPS를 빼고 올림하는 보정을 넣었지만, 이 보정도 오차가 EPS를 넘는 입력에서는 무력하다는 한계가 있다.

복잡도 측면에서는 변 수가 h인 hull에 대해 투영 단계가 O(h²)이므로 점이 수만 개이고 대부분이 hull 위에 있는 입력(예: 원 위에 놓인 점)에서는 느려진다. 이 문제처럼 N이 작으면 단순한 전수 투영이 코드가 짧고 검증하기 쉬워 실수가 적다. 입력 상한이 커지면 Rotating Calipers로 바꾸는 것이 정답이다.

### Monotone Chain이 hull을 만드는 원리

Andrew의 Monotone Chain은 점을 x 좌표(같으면 y 좌표) 순으로 정렬한 뒤 하단 사슬과 상단 사슬을 따로 만들어 이어 붙인다. 하단 사슬은 정렬된 점을 왼쪽에서 오른쪽으로 읽으며, 새 점 P를 추가할 때 스택 맨 위 두 점 A, B와 P가 반시계 방향으로 꺾이지 않으면(외적이 0 이하) B를 버린다. B가 A와 P를 잇는 선분 위이거나 그 오른쪽에 있다면 B는 볼록 껍질의 꼭짓점이 될 수 없기 때문이다. 이 규칙으로 스택은 항상 아래로 볼록한 사슬을 유지한다. 상단 사슬은 같은 일을 오른쪽에서 왼쪽으로 반복하며, 하단 사슬이 끝난 위치를 기준으로 `t = k + 1`을 두어 하단 사슬의 점을 건드리지 않게 한다. 각 점은 스택에 한 번 들어가고 최대 한 번 나가므로 정렬 이후의 작업은 O(N)이고 전체는 정렬이 지배하는 O(N log N)이다. 외적이 0인 공선 점도 버리기 때문에 변 위의 점이 hull에 남지 않아, 뒤의 투영 단계가 같은 방향을 중복해서 검사하는 일도 없다.

### 어떤 방법을 언제 쓰는가

이 문제의 입력 규모에서는 변별 전수 투영이 가장 단순하고 안전하다. 코드가 짧아 외적 부호나 인덱스 실수가 끼어들 여지가 작고, h가 수백 이하라면 h²도 시간 제한에 영향을 주지 않는다. 반대로 h가 수만 단위로 커지거나 테스트 케이스가 매우 많다면 Rotating Calipers가 필요하다. 한 변을 고정하고 가장 멀리 있는 꼭짓점의 위치를 포인터로 들고 있다가, 변이 다음으로 넘어갈 때 그 포인터를 앞으로만 이동시키면 전체 이동 횟수가 O(h)로 묶인다. 한편 최소 너비가 아니라 최소 넓이 외접 직사각형이나 지름(가장 먼 두 점)을 구하는 문제에도 같은 캘리퍼스 구조가 쓰이므로, 이 문제는 그 기법을 익히기 전의 기준 구현으로 삼기 좋다. 또 하나 알아둘 점은 hull 단계를 생략하고 원래 다각형의 변 방향만 검사하면 안 된다는 것이다. 다각형이 오목하거나 입력이 점 집합이면 최소 너비를 주는 hull 변이 원래 다각형의 변과 일치하지 않을 수 있어 더 큰 값이 나온다. hull은 검사 대상을 줄이는 동시에 올바른 후보 방향을 얻기 위한 필수 단계다.

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
    if (n < 3) return 0.0; // 점 1개 또는 일직선: 너비 0
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

`Point` 구조체는 2차원 좌표를 담고 뺄셈과 정렬용 비교 연산자를 오버로딩한다. 비교는 x 차이가 EPS보다 크면 x로, 아니면 y로 정렬해 Monotone Chain이 요구하는 사전식 순서를 만든다. `convexHull`은 정렬한 점을 앞에서부터 훑어 하단 hull을, 뒤에서부터 훑어 상단 hull을 쌓으며, 외적이 EPS 이하인 점(시계 방향이거나 공선)은 pop한다. `minimalWidth`는 위 접근 방식의 2단계 그대로 변마다 수직 벡터를 정규화하고 모든 hull 꼭짓점을 투영해 폭을 구한다. hull 꼭짓점이 3개 미만이면(점이 하나이거나 일직선) 너비가 0이므로 곧바로 0을 반환하는데, 이 가드가 없으면 길이 0인 변으로 나누게 된다. `roundUpTo0p01`은 값에 100을 곱하고 EPS를 뺀 뒤 `ceil`로 올려 부동소수점 오차로 정확히 떨어지는 값이 한 칸 올라가는 것을 막는다.

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
    if (n < 3) return 0.0; // 점 1개 또는 일직선: 너비 0
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

이 버전은 `stdio.h`만 쓰는 제약을 가정해 `fabs`, `sqrt`, 정렬, 올림을 직접 구현했다. 표준 헤더 함수와 같은 이름으로 `fabs`·`sqrt`·`swap`을 정의하므로 컴파일러에 따라 내장 함수 충돌 경고가 날 수 있다. 제출 환경에서 문제가 되면 `my_` 접두어로 이름을 바꾼다. `qsort` 대신 직접 만든 QuickSort가 점을 정렬하고, `sqrt`는 뉴턴-랩슨 반복으로 근사한다. 이 근사는 상대 변화가 1e-10 이하가 될 때까지 반복하므로 한 변의 길이 계산에는 충분하다. `convexHull`과 `minimalWidth`의 논리는 앞의 C++ 버전과 같고, 배열 크기 `MAXN`은 점 개수 상한을 전제로 한 값이라 실제 제출 전에 문제 페이지의 입력 제한과 맞는지 확인해야 한다.

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
    if n < 3:
        return 0.0  # 점 1개 또는 일직선: 너비 0
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

Python 버전은 C++ 버전과 같은 구조다. `Point` 클래스가 뺄셈, `__lt__`, 외적을 제공하고, `convexHull`이 정렬 후 하단·상단 hull을 쌓으며, `minimalWidth`가 변 수직 방향별 투영 폭의 최솟값을 구한다. `math.hypot`으로 벡터 길이를 구하고 `math.ceil`로 올림하므로 라이브러리 구현이 필요 없다. 입력은 `sys.stdin.readlines()`로 한 번에 읽어 반복 호출 비용을 줄였다.

## 결론

최소 너비는 Convex Hull의 변과 평행한 지지선 쌍 중 가장 좁은 것으로 결정되므로, hull을 구한 뒤 변 방향만 검사하면 된다. 이 글의 구현은 O(N log N + h²)이며 Rotating Calipers로 투영 단계를 O(h)로 줄이는 것은 구현하지 않은 확장이다. 올림 처리에서는 값에 100을 곱한 뒤 EPS를 빼고 `ceil`하는 방식으로 부동소수점 오차가 결과를 한 칸 올리지 않도록 했다.

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **점 1개** | hull이 점 하나로 퇴화해 변 길이가 0 | `minimalWidth`에서 hull 꼭짓점 3개 미만이면 0 반환 |
| **모든 점이 일직선** | hull이 양 끝점 2개로 퇴화, 너비는 0 | 위 가드로 같이 처리 |
| **공선 점이 변 위에 있음** | 외적이 0인 점이 hull에 남으면 변이 쪼개져 비용만 늘어남 | `<= EPS`로 pop해 제거 |
| **올림 경계** | 정확히 소수 둘째 자리에 떨어지는 값이 오차로 한 칸 올라감 | `value*100 - EPS` 후 `ceil` |

## 이 글을 읽은 후 달성해야 할 목표

- 최소 너비가 hull 변에 수직인 방향에서 달성되는 이유를 설명할 수 있다.
- 변별 전수 투영의 O(h²)과 Rotating Calipers의 O(h)를 비교하고, 입력 크기에 따라 선택 기준을 말할 수 있다.
- 점 1개·일직선 같은 퇴화 입력과 올림 경계의 부동소수점 오차를 처리할 수 있다.
