---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-25T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Geometry
- Sorting
- ConvexHull
- Implementation
- O(N log N)
- ComputationalGeometry
title: '[Algorithm] C++/Python 백준 3679번 : 단순 다각형'
---

이번 글에서는 주어진 점들로 자기 교차 없이 단순 다각형을 구성하는 문제인 **백준 3679번 단순 다각형**을 소개하고, 이를 해결하기 위한 접근 방식과 구현 방법을 살펴보겠다. 이 문제는 기하학적 알고리즘과 정렬을 활용하여 해결할 수 있으며, 효율적인 구현이 요구된다.

## 문제 설명

평면 위에 $n$개의 점이 주어졌을 때, 이 점들을 모두 꼭짓점으로 갖는 **단순 다각형**을 만드는 문제이다. 단순 다각형이란 자기 자신과 교차하지 않는 다각형을 의미한다. 즉, 인접한 두 선분의 교점을 제외하고는 선분들이 서로 교차하지 않아야 한다. 또한, 다각형의 꼭짓점은 주어진 점들로만 구성되어야 하며, 추가적인 점을 사용할 수 없다.

항상 문제의 조건을 만족하는 다각형이 입력으로 주어지며, 가능한 다각형이 여러 개 존재할 경우 그 중 하나만 출력하면 된다. 주어진 점들 중 동일한 위치를 갖는 점은 없으며, 모든 점이 한 직선 위에 놓여 있지 않다.

문제 : [https://www.acmicpc.net/problem/3679](https://www.acmicpc.net/problem/3679)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
| |

**입력**

첫째 줄에 테스트 케이스의 개수 \( c \) \( (1 \leq c \leq 200 )\)가 주어진다. 각 테스트 케이스는 한 줄로 이루어져 있다. 각 테스트 케이스의 첫 번째 숫자는 점의 개수 $ n $ $ (3 \leq n \leq 2000) $이며, 이후에 $ n $개의 점의 좌표 $ x $와 $ y $가 공백으로 구분되어 주어진다. 좌표는 $-10,000$보다 크거나 같고, $10,000$보다 작거나 같은 정수이다.

**출력**

각 테스트 케이스마다 $ 0 $부터 $ n-1 $까지의 번호를 가진 점들의 순열 중 하나를 출력한다. 출력하는 순열은 입력으로 주어진 점들의 번호를 나타내며, 해당 순서대로 점들을 연결했을 때 올바른 단순 다각형을 이루어야 한다.

**예제 입력**

```
2
4 0 0 2 0 0 1 1 0
5 0 0 10 0 10 5 5 -1 0 5
```

**예제 출력**

```
0 3 1 2
3 1 2 4 0
```

문제 : [https://www.acmicpc.net/problem/3679](https://www.acmicpc.net/problem/3679)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 주어진 점들로 단순 다각형을 만드는 것이다. 단순 다각형을 만들기 위해서는 선분들이 서로 교차하지 않도록 점들의 순서를 정해야 한다. 이를 위해 다음과 같은 전략을 사용한다:

1. **중심점 계산**: 주어진 모든 점들의 중심점을 계산한다. 중심점은 모든 점들의 $ x $좌표의 평균과 $ y $좌표의 평균으로 구할 수 있다.

2. **각도 계산**: 각 점에서 중심점을 기준으로 한 각도를 계산한다. 이는 점과 중심점을 연결한 직선이 $ x $축과 이루는 각도를 의미하며, `atan2` 함수를 사용하여 구할 수 있다.

3. **각도에 따른 정렬**: 계산된 각도에 따라 점들을 정렬한다. 이렇게 하면 점들이 중심점을 기준으로 반시계 방향으로 정렬되어 다각형을 구성할 수 있다.

4. **점 연결**: 정렬된 순서대로 점들을 연결하여 다각형을 만든다.

이 방법은 모든 점들이 한 직선 위에 있지 않기 때문에 유효하다. 또한, 점들이 동일한 위치에 있지 않으므로 각도 계산 시 문제가 발생하지 않는다. 이 알고리즘의 시간 복잡도는 정렬에 따라 $ O(n \log n) $이다.

## C++ 코드와 설명

```cpp
#include <iostream>   // 입출력을 위한 헤더 파일
#include <vector>     // 벡터 사용을 위한 헤더 파일
#include <cmath>      // 수학 함수 사용을 위한 헤더 파일
#include <algorithm>  // 정렬을 위한 헤더 파일

using namespace std;

// 점을 표현하는 구조체
struct Point {
    int idx;        // 점의 인덱스
    double x, y;    // 점의 좌표
    double angle;   // 중심점에 대한 각도
};

int main() {
    int c;
    cin >> c;   // 테스트 케이스의 수 입력
    while (c--) {
        int n;
        cin >> n;   // 점의 개수 입력
        vector<Point> points(n);
        double sumx = 0, sumy = 0;    // x, y 좌표의 합을 저장할 변수
        for (int i = 0; i < n; ++i) {
            points[i].idx = i;        // 점의 인덱스 저장
            cin >> points[i].x >> points[i].y;   // 점의 좌표 입력
            sumx += points[i].x;      // x 좌표의 합계
            sumy += points[i].y;      // y 좌표의 합계
        }
        double cx = sumx / n;     // 중심점의 x 좌표
        double cy = sumy / n;     // 중심점의 y 좌표
        for (int i = 0; i < n; ++i) {
            // 각 점에서 중심점을 기준으로 한 각도 계산
            points[i].angle = atan2(points[i].y - cy, points[i].x - cx);
        }
        // 각도에 따라 점들을 정렬
        sort(points.begin(), points.end(), [](const Point &a, const Point &b) {
            return a.angle < b.angle;
        });
        // 정렬된 점들의 인덱스를 출력
        for (int i = 0; i < n; ++i) {
            cout << points[i].idx;
            if (i != n - 1) cout << " ";
        }
        cout << "\n";
    }
    return 0;
}
```

**코드 설명**

- **입력 처리**:
  - 테스트 케이스의 수 `c`를 입력받는다.
  - 각 테스트 케이스마다 점의 개수 `n`과 각 점의 좌표를 입력받는다.
  - 점들의 인덱스와 좌표를 `Point` 구조체에 저장하고, x와 y 좌표의 합계를 계산한다.

- **중심점 계산**:
  - 모든 점들의 x 좌표와 y 좌표의 평균을 구하여 중심점 `(cx, cy)`를 계산한다.

- **각도 계산**:
  - 각 점에서 중심점을 기준으로 한 각도를 `atan2` 함수를 사용하여 계산하고, `angle`에 저장한다.

- **정렬**:
  - 람다 함수를 이용하여 각도에 따라 점들을 정렬한다.

- **출력**:
  - 정렬된 점들의 인덱스를 순서대로 출력한다.

이렇게 정렬된 순서대로 점들을 연결하면 단순 다각형을 얻을 수 있다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>   // 입출력을 위한 헤더 파일
#include <stdlib.h>  // 동적 메모리 할당을 위한 헤더 파일
#include <math.h>    // 수학 함수를 위한 헤더 파일

// 점을 표현하는 구조체
typedef struct {
    int idx;        // 점의 인덱스
    double x, y;    // 점의 좌표
    double angle;   // 중심점에 대한 각도
} Point;

// 비교 함수 정의 (qsort를 위한)
int compare(const void *a, const void *b) {
    Point *pa = (Point*)a;
    Point *pb = (Point*)b;
    if (pa->angle < pb->angle) return -1;
    if (pa->angle > pb->angle) return 1;
    return 0;
}

int main() {
    int c;
    scanf("%d", &c);   // 테스트 케이스의 수 입력
    while (c--) {
        int n;
        scanf("%d", &n);   // 점의 개수 입력
        Point *points = (Point*)malloc(n * sizeof(Point));  // 점들을 저장할 배열 동적 할당
        double sumx = 0, sumy = 0;    // x, y 좌표의 합을 저장할 변수
        for (int i = 0; i < n; ++i) {
            points[i].idx = i;        // 점의 인덱스 저장
            scanf("%lf %lf", &points[i].x, &points[i].y);   // 점의 좌표 입력
            sumx += points[i].x;      // x 좌표의 합계
            sumy += points[i].y;      // y 좌표의 합계
        }
        double cx = sumx / n;     // 중심점의 x 좌표
        double cy = sumy / n;     // 중심점의 y 좌표
        for (int i = 0; i < n; ++i) {
            // 각 점에서 중심점을 기준으로 한 각도 계산
            points[i].angle = atan2(points[i].y - cy, points[i].x - cx);
        }
        // 각도에 따라 점들을 정렬
        qsort(points, n, sizeof(Point), compare);
        // 정렬된 점들의 인덱스를 출력
        for (int i = 0; i < n; ++i) {
            printf("%d", points[i].idx);
            if (i != n - 1) printf(" ");
        }
        printf("\n");
        free(points);  // 동적 할당한 메모리 해제
    }
    return 0;
}
```

**코드 설명**

- **입력 처리**:
  - `scanf`를 사용하여 테스트 케이스의 수와 각 점의 좌표를 입력받는다.
  - 동적 메모리 할당을 통해 점들을 저장할 배열을 생성한다.

- **중심점 계산**:
  - 모든 점들의 x 좌표와 y 좌표의 평균을 구하여 중심점 `(cx, cy)`를 계산한다.

- **각도 계산**:
  - 각 점에서 중심점을 기준으로 한 각도를 `atan2` 함수를 사용하여 계산하고, `angle`에 저장한다.

- **정렬**:
  - `qsort` 함수를 사용하여 각도에 따라 점들을 정렬한다.

- **출력**:
  - 정렬된 점들의 인덱스를 순서대로 출력한다.

- **메모리 해제**:
  - 동적 할당한 메모리를 `free` 함수를 사용하여 해제한다.

이 코드는 라이브러리의 사용을 최소화하면서도 문제를 효율적으로 해결한다.

## Python 코드와 설명

```python
import sys
import math

c = int(sys.stdin.readline())  # 테스트 케이스의 수 입력

for _ in range(c):
    # 한 줄의 입력을 받아 공백으로 분리
    tokens = sys.stdin.readline().split()
    idx = 0  # 현재 토큰의 위치
    n = int(tokens[idx])  # 점의 개수 추출
    idx += 1
    # 점들의 정보를 저장할 리스트
    points = []
    sumx = 0.0
    sumy = 0.0
    # 필요한 좌표의 총 개수는 2 * n
    while len(tokens) - idx < 2 * n:
        tokens.extend(sys.stdin.readline().split())
    for i in range(n):
        x = float(tokens[idx])
        idx += 1
        y = float(tokens[idx])
        idx += 1
        points.append({'idx': i, 'x': x, 'y': y})
        sumx += x
        sumy += y
    cx = sumx / n  # 중심점의 x 좌표
    cy = sumy / n  # 중심점의 y 좌표
    for point in points:
        # 각 점에서 중심점을 기준으로 한 각도 계산
        point['angle'] = math.atan2(point['y'] - cy, point['x'] - cx)
    # 각도에 따라 점들을 정렬
    points.sort(key=lambda p: p['angle'])
    # 정렬된 점들의 인덱스를 출력
    result = ' '.join(str(point['idx']) for point in points)
    print(result)
```

**코드 설명**

- **입력 처리**:
  - `sys.stdin.readline()`을 사용하여 입력을 받는다.
  - 테스트 케이스마다 한 줄의 입력을 받아 공백으로 분리한 후, 필요한 좌표의 개수만큼 입력을 확보하기 위해 추가적인 입력을 받는다.

- **데이터 파싱**:
  - `tokens` 리스트에서 점의 개수 `n`과 각 점의 좌표를 추출한다.
  - 각 점의 정보를 딕셔너리 형태로 `points` 리스트에 저장하고, x와 y 좌표의 합계를 계산한다.

- **중심점 계산**:
  - 모든 점들의 x 좌표와 y 좌표의 평균을 구하여 중심점 `(cx, cy)`를 계산한다.

- **각도 계산**:
  - 각 점에서 중심점을 기준으로 한 각도를 `math.atan2` 함수를 사용하여 계산하고, `angle` 키에 저장한다.

- **정렬 및 출력**:
  - 각도에 따라 점들을 정렬한다.
  - 정렬된 점들의 인덱스를 공백으로 구분하여 출력한다.

이 코드는 입력 형식에 맞게 동작하며, 런타임 에러 없이 정확한 결과를 출력한다.

## 결론

이번 문제는 주어진 점들로 단순 다각형을 만드는 것이 핵심이었다. 중심점을 기준으로 각도를 계산하여 점들을 정렬하는 방법은 구현이 간단하면서도 효율적이며, 대부분의 경우에 단순 다각형을 얻을 수 있다.

코드를 작성할 때 입력 형식에 주의해야 함을 느꼈다. 특히, 파이썬에서는 입력이 한 줄로 주어질 때 이를 적절히 파싱하는 것이 중요했다.

또한, 알고리즘의 효율성을 높이기 위해 불필요한 연산을 줄이고, 입력 데이터의 특성을 고려하여 적절한 자료 구조와 함수를 사용하는 것이 중요하다.

이번 문제를 통해 기하학적인 알고리즘의 중요성과 구현 시 고려해야 할 점들을 다시 한 번 확인할 수 있었다.