---
title: "[Algorithm] C++/Python 백준 20149번 : 선분 교차 3"
categories: 
- Algorithm
- Geometry
- Implementation
tags:
- CCW
- LineIntersection
- Implementation
- Pruning
- O(1)
- Vector
- Geometry
image: "index.png"
date: 2024-12-30
---

본 글에서는 백준 20149번 "선분 교차 3" 문제를 다루어보려고 한다.  
2차원 평면 위에 주어진 두 선분의 교차 여부와, 교차한다면 교차점을 구하는 문제로, 기하학(Geometry)에서 자주 등장하는 주제이다.  
직선의 교차 공식(Line Intersection Formula)과 CCW(Counter Clockwise) 연산 등을 종합적으로 사용하기에, 기하 알고리즘 연습에 좋은 예제라 할 수 있다.

문제 : [https://www.acmicpc.net/problem/20149](https://www.acmicpc.net/problem/20149)

## 문제 설명

백준 20149번 "선분 교차 3" 문제는, 2차원 좌표 평면상 두 선분이 주어졌을 때 이들이 교차하는지 판정하고, 만약 교차한다면 교차점을 출력하는 과정을 요구하는 문제이다.

구체적인 입력으로, 첫 번째 줄에 선분 \( L_1 \)의 양 끝점 \((x_1, y_1), (x_2, y_2)\), 두 번째 줄에 선분 \( L_2 \)의 양 끝점 \((x_3, y_3), (x_4, y_4)\)가 주어진다. 모든 좌표는 \(-1,000,000 \le x_i, y_i \le 1,000,000\) 범위를 만족하는 정수이다. 문제에서 ‘선분의 길이는 0보다 크다’고 명시되어 있으므로, 실제 입력된 선분이 ‘점’인 경우는 고려하지 않아도 된다.

출력은 먼저 두 선분이 교차한다면 1, 아니면 0을 한 줄에 출력한다. 만약 교차한다면, 그 교차점이 하나뿐인 경우(즉, 점 교차)에는 교차점의 \( x \)좌표와 \( y \)좌표를 10^-9 오차 범위 내에서 출력한다. 만약 두 선분이 일직선 상에 놓여 있어 선분 구간이 겹치되, 그 겹치는 구간이 한 점을 넘어서는 경우(즉, 무한히 많은 교집합)에는 교차점 좌표를 따로 출력하지 않는다.

이 문제는 여러 조건 분기와 세부 구현이 까다로운 편이다. 우선 두 직선이 기울기가 같을 수 있고(평행), 둘 중 하나가 다른 선분의 끝점 위에 놓일 수 있으며(경계 교차), 두 선분이 일직선 상에 있으면서 부분적으로만 겹칠 수도 있다. 예컨대, 두 선분이 서로 완전히 떨어져서 만날 일이 없는 경우, 정확히 끝점끼리 만나는 경우, 혹은 같은 직선 위에서 서로 교차 구간이 없는 경우 등을 제대로 처리해야 한다.

가장 핵심적으로, “두 선분이 교차한다”는 것을 판별하기 위해서는 CCW(Counter Clockwise) 기법을 사용하거나, 각 선분의 방향성을 고려한 뒤 교차하는지 확인하는 방식이 필요하다. CCW 기법을 요약하면, 세 점 \( A, B, C \)가 있을 때, 백터 \( \overrightarrow{AB} \)와 \( \overrightarrow{AC} \)의 외적을 계산하여 0보다 크면 반시계 방향, 0보다 작으면 시계 방향, 0이면 일직선이라고 판별하는 원리이다. 이를 이용해 선분 교차 판단을 다음과 같이 한다:

1. 두 선분 \( L_1(A, B) \)와 \( L_2(C, D) \)가 있을 때,  
   \(
     \text{CCW}(A, B, C) \times \text{CCW}(A, B, D) \le 0  
     \quad\text{그리고}\quad  
     \text{CCW}(C, D, A) \times \text{CCW}(C, D, B) \le 0
   \)  
   이면 교차 가능성이 있다.

2. 위 조건이 < 0인지 = 0인지에 따라, ‘실제 교차’와 ‘끝점에 걸치는지(경계 교차)’를 구분한다.

3. 만약 두 선분이 일직선상(collinear)에 있으면, 추가로 각 선분이 서로 겹치는지 x좌표와 y좌표 범위로 확인한다. 이때 범위가 한 점만 겹치면 그 점을 출력, 여러 점이 겹치면 출력 없이 교차 여부만 1을 출력한다.

이 문제는 예외적인 상황이 다수 존재하므로, 세세한 조건 분기와 구현 검증이 매우 중요하다. 게다가, 교차점 계산 시에는 분수(실수)가 나올 수 있어, 반올림 오차를 고려하거나 `double`(혹은 `long double`)을 적절히 사용해야 한다. 때문에, 문제를 꼼꼼히 분석한 뒤 ccw 함수, onSegment 함수, 그리고 두 직선의 교차점을 구하는 line-intersection 공식을 적절히 구현하는 것이 관건이다.

이처럼 “선분 교차 3” 문제는 기하 알고리즘 중에서도 필수로 공부해야 하는 CCW, Line Intersection, Edge Case 처리(끝점 포함, 일직선 상 중첩) 등을 복합적으로 다룬다. 특히, 정밀도를 요하는 교차점 출력이 필수이므로 부동소수점 연산에서도 신경써야 한다. 모든 조건을 빠짐없이 챙기다 보면 다소 길고 복잡한 코드가 될 수 있으나, 각 단계마다 철저한 검증과 디버깅을 거치면 해결 가능하다.

## 접근 방식

1. **CCW 함수 구현**  
   - 세 점 \( A, B, C \)에 대하여, 외적값 \((B - A) \times (C - A)\)의 부호를 통해 시계/반시계/일직선을 판별한다.

2. **isIntersect(두 선분 교차 판정)**  
   - 선분 \( AB \)와 \( CD \)에 대해 ccw(A,B,C)와 ccw(A,B,D)가 서로 반대 부호인지, 그리고 ccw(C,D,A)와 ccw(C,D,B)가 반대 부호인지 확인한다.  
   - 또한 ccw 값이 0인 경우, 점이 다른 선분 위에 있는지(경계 교차) 여부를 확인해 교차 여부를 결정한다.

3. **일직선 여부(collinear) 판별**  
   - 만약 네 점이 모두 ccw 결과가 0이라면, 선분이 일직선상에 있는 것이므로, x좌표와 y좌표 범위를 통해 겹침 여부와 교차 지점을 체크한다.

4. **직선 교차점 계산(Line Intersection) 공식**  
   - 평행하지 않은 두 직선 \( AB \)와 \( CD \)가 교차할 때, 교차점 \( (x, y) \)는 분수 형태로 계산한다.  
   - \(
       x = \frac{(x_1 y_2 - y_1 x_2)(x_3 - x_4) - (x_1 - x_2)(x_3 y_4 - y_3 x_4)}{\text{denom}}
     \)
   - \(
       y = \frac{(x_1 y_2 - y_1 x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 y_4 - y_3 x_4)}{\text{denom}}
     \)
     여기서 \(\text{denom} = (x_1 - x_2)(y_3 - y_4) - (y_1 - y_2)(x_3 - x_4)\)이다.

5. **출력 조건**  
   - 교차하지 않으면 0만 출력  
   - 교차한다면 1을 출력하고, 이어서 교차점이 한 점에 한정될 때만 그 점을 출력  
   - 일직선으로 겹치되 선분 구간이 여러 점에 걸쳐 있으면 교차점 출력 없음

이러한 접근 방식을 따르면, 무수히 많은 엣지 케이스에도 일관성 있게 대응할 수 있다. 핵심은 올바른 CCW 구현과 교차점 공식, 그리고 일직선상 선분 범위 비교 로직이다.

## C++ 코드와 설명

아래는 문제 해결을 위한 C++ 코드이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// 점을 표현하는 구조체이다.
struct Point {
    long long x, y;
};

// CCW 함수: 세 점 A, B, C에 대한 외적 결과의 부호를 반환한다.
long long ccw(const Point& A, const Point& B, const Point& C) {
    // (B - A) x (C - A)
    long long cross = (B.x - A.x) * (C.y - A.y)
                    - (B.y - A.y) * (C.x - A.x);
    if (cross > 0) return 1;   // 반시계
    if (cross < 0) return -1;  // 시계
    return 0;                  // 일직선
}

// 두 선분(AB, CD)의 교차 여부를 ccw 로 확인하는 함수이다.
bool isIntersect(const Point &A, const Point &B,
                 const Point &C, const Point &D) {
    long long ccwAB_C = ccw(A, B, C);
    long long ccwAB_D = ccw(A, B, D);
    long long ccwCD_A = ccw(C, D, A);
    long long ccwCD_B = ccw(C, D, B);

    // 일직선 아닌 경우
    if (ccwAB_C * ccwAB_D < 0 && ccwCD_A * ccwCD_B < 0) {
        return true;
    }

    // 이하 ccw = 0인 경우(끝점이 걸치는지)
    // 선분 AB 위에 C가 있는지
    if (ccwAB_C == 0 &&
        min(A.x,B.x) <= C.x && C.x <= max(A.x,B.x) &&
        min(A.y,B.y) <= C.y && C.y <= max(A.y,B.y)) {
        return true;
    }
    // 선분 AB 위에 D가 있는지
    if (ccwAB_D == 0 &&
        min(A.x,B.x) <= D.x && D.x <= max(A.x,B.x) &&
        min(A.y,B.y) <= D.y && D.y <= max(A.y,B.y)) {
        return true;
    }
    // 선분 CD 위에 A가 있는지
    if (ccwCD_A == 0 &&
        min(C.x,D.x) <= A.x && A.x <= max(C.x,D.x) &&
        min(C.y,D.y) <= A.y && A.y <= max(C.y,D.y)) {
        return true;
    }
    // 선분 CD 위에 B가 있는지
    if (ccwCD_B == 0 &&
        min(C.x,D.x) <= B.x && B.x <= max(C.x,D.x) &&
        min(C.y,D.y) <= B.y && B.y <= max(C.y,D.y)) {
        return true;
    }
    return false;
}

// 두 직선(AB, CD)의 교차점을 구한다(선분 아님).
// 평행하지 않다고 가정했을 때만 이 함수를 호출해야 안전하다.
bool getLineIntersection(const Point &A, const Point &B,
                         const Point &C, const Point &D,
                         long double &x, long double &y) {
    long long denom = (A.x - B.x) * (C.y - D.y)
                    - (A.y - B.y) * (C.x - D.x);
    if (denom == 0) {
        // 평행 or 일치
        return false;
    }
    long long numeratorX = ( (A.x * B.y - A.y * B.x) * (C.x - D.x)
                           - (A.x - B.x) * (C.x * D.y - C.y * D.x) );
    long long numeratorY = ( (A.x * B.y - A.y * B.x) * (C.y - D.y)
                           - (A.y - B.y) * (C.x * D.y - C.y * D.x) );

    x = (long double)numeratorX / (long double)denom;
    y = (long double)numeratorY / (long double)denom;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Point A,B,C,D;
    cin >> A.x >> A.y >> B.x >> B.y;
    cin >> C.x >> C.y >> D.x >> D.y;

    // 교차 여부 먼저 판정한다.
    bool intersect = isIntersect(A, B, C, D);

    // 교차 여부 출력
    if(!intersect) {
        cout << 0 << "\n";
        return 0;
    } 
    cout << 1 << "\n";

    // 교차한다면 점 하나에서 만나는지(=교차점이 유일한지), 아니면 선분 일부가 겹치는지 판단한다.
    // ccw 값을 다시 구해 collinear 여부를 확인한다.
    long long ccwAB_C = ccw(A, B, C);
    long long ccwAB_D = ccw(A, B, D);
    long long ccwCD_A = ccw(C, D, A);
    long long ccwCD_B = ccw(C, D, B);

    bool collinear = (ccwAB_C == 0 && ccwAB_D == 0 && ccwCD_A == 0 && ccwCD_B == 0);

    if (collinear) {
        // 일직선상에 놓여 있음: x,y 범위가 겹치는지 확인한다.
        long long leftX  = max(min(A.x,B.x), min(C.x,D.x));
        long long rightX = min(max(A.x,B.x), max(C.x,D.x));
        long long bottomY= max(min(A.y,B.y), min(C.y,D.y));
        long long topY   = min(max(A.y,B.y), max(C.y,D.y));

        // 만약 한 점에서만 만난다면(즉, x범위와 y범위가 정확히 일치하는 1점)
        if (leftX == rightX && bottomY == topY) {
            cout << fixed << setprecision(9) 
                 << (long double)leftX << " " << (long double)bottomY << "\n";
        }
        // 그 외 여러 점 겹침이면 추가 출력 없음
    } else {
        // 일직선이 아닌 상황 → 직선 교차점은 최대 1개임
        long double ix, iy;
        if (getLineIntersection(A, B, C, D, ix, iy)) {
            cout << fixed << setprecision(9) << ix << " " << iy << "\n";
        }
    }
    return 0;
}
```

### 코드 동작 단계별 설명

1. **구조체 정의**: `Point` 구조체로 2차원 정수 좌표를 표현한다.  
2. **CCW 함수**: 세 점을 받아 (B - A)와 (C - A)의 외적을 구하고, 그 부호(양수/음수/0)에 따라 반시계, 시계, 일직선을 판별한다.  
3. **isIntersect**: ccw를 사용해 두 선분이 교차하는지 `bool`로 반환한다. 여기서 끝점이 겹치는 경우에도 교차로 처리하기 위해 ccw 결과가 0일 때 세부 조건을 체크한다.  
4. **getLineIntersection**: 두 직선이 평행하지 않을 때 교차점 \((x, y)\)를 구한다. 분수 형태의 계산을 분자/분모로 나누어 정확도를 높이고, `long double`을 사용한다.  
5. **main**:  
   - 입력을 받는다.  
   - `isIntersect`로 교차 여부를 판정 후 출력(0 또는 1).  
   - 교차한다면, ccw 결과를 통해 일직선 상 겹침(collinear)인지 확인한다.  
   - 일직선(collinear)이라면 x, y의 겹치는 범위가 점 하나면 그 점을 출력, 여러 점이면 출력 없이 종료한다.  
   - 일직선이 아니면 `getLineIntersection`으로 교차점을 구해 출력한다.

## Python 코드와 설명

다음은 동일한 로직을 Python으로 옮긴 예시이다. 실수 연산은 float를 쓰지만, 파이썬은 내부적으로 double 정밀도를 가지므로 적절히 계산 가능하다. 필요한 경우 `decimal` 모듈을 사용할 수도 있다.

```python
import sys

input = sys.stdin.readline

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def ccw(A, B, C):
    # (B - A) x (C - A)
    cross = (B.x - A.x)*(C.y - A.y) - (B.y - A.y)*(C.x - A.x)
    if cross > 0:
        return 1   # 반시계
    elif cross < 0:
        return -1  # 시계
    else:
        return 0    # 일직선

def isIntersect(A, B, C, D):
    ccwAB_C = ccw(A, B, C)
    ccwAB_D = ccw(A, B, D)
    ccwCD_A = ccw(C, D, A)
    ccwCD_B = ccw(C, D, B)

    # 두 선분이 일직선이 아닌 경우
    if ccwAB_C*ccwAB_D < 0 and ccwCD_A*ccwCD_B < 0:
        return True
    
    # 일직선 or 끝점이 맞닿을 때
    if ccwAB_C == 0 and min(A.x,B.x) <= C.x <= max(A.x,B.x) and min(A.y,B.y) <= C.y <= max(A.y,B.y):
        return True
    if ccwAB_D == 0 and min(A.x,B.x) <= D.x <= max(A.x,B.x) and min(A.y,B.y) <= D.y <= max(A.y,B.y):
        return True
    if ccwCD_A == 0 and min(C.x,D.x) <= A.x <= max(C.x,D.x) and min(C.y,D.y) <= A.y <= max(C.y,D.y):
        return True
    if ccwCD_B == 0 and min(C.x,D.x) <= B.x <= max(C.x,D.x) and min(C.y,D.y) <= B.y <= max(C.y,D.y):
        return True

    return False

def getLineIntersection(A, B, C, D):
    denom = (A.x - B.x)*(C.y - D.y) - (A.y - B.y)*(C.x - D.x)
    if denom == 0:
        return None  # 평행 or 일치
    numeratorX = ((A.x*B.y - A.y*B.x)*(C.x - D.x) 
                  - (A.x - B.x)*(C.x*D.y - C.y*D.x))
    numeratorY = ((A.x*B.y - A.y*B.x)*(C.y - D.y)
                  - (A.y - B.y)*(C.x*D.y - C.y*D.x))

    x = numeratorX/denom
    y = numeratorY/denom
    return (x, y)

def main():
    x1,y1,x2,y2 = map(int, input().split())
    x3,y3,x4,y4 = map(int, input().split())

    A, B, C, D = Point(x1,y1), Point(x2,y2), Point(x3,y3), Point(x4,y4)

    intersect = isIntersect(A,B,C,D)
    if not intersect:
        print(0)
        return
    print(1)

    ccwAB_C = ccw(A,B,C)
    ccwAB_D = ccw(A,B,D)
    ccwCD_A = ccw(C,D,A)
    ccwCD_B = ccw(C,D,B)

    collinear = (ccwAB_C == 0 and ccwAB_D == 0 and ccwCD_A == 0 and ccwCD_B == 0)

    if collinear:
        leftX  = max(min(A.x,B.x), min(C.x,D.x))
        rightX = min(max(A.x,B.x), max(C.x,D.x))
        bottomY= max(min(A.y,B.y), min(C.y,D.y))
        topY   = min(max(A.y,B.y), max(C.y,D.y))

        if leftX == rightX and bottomY == topY:
            print(f"{float(leftX):.9f} {float(bottomY):.9f}")
    else:
        res = getLineIntersection(A,B,C,D)
        if res is not None:
            print(f"{res[0]:.9f} {res[1]:.9f}")

if __name__ == "__main__":
    main()
```

### 코드 동작 단계별 설명

1. `Point` 클래스로 (x, y) 좌표를 저장한다.  
2. `ccw` 함수에서 외적을 계산해 +1(반시계), -1(시계), 0(일직선)을 구분한다.  
3. `isIntersect` 함수에서 두 선분이 교차하는지 여부를 bool로 반환하며, 끝점 포함 여부도 함께 처리한다.  
4. `getLineIntersection` 함수에서 직선 교차점 \((x, y)\)를 계산하며, 만약 평행(denom=0)이면 `None`을 반환한다.  
5. `main` 함수에서 입력을 받고 교차 여부를 출력한다. 교차한다면 collinear(일직선)인지 확인 후, 일직선이면 겹치는 범위가 점 하나일 때만 출력, 그렇지 않으면 일반 교차점(한 점)을 계산해 출력한다.

## 결론

백준 20149번 "선분 교차 3" 문제는, 선분 교차 판정 알고리즘의 다양한 예외 케이스를 모두 충실하게 다뤄야 하기에 입문자에게는 난이도가 있는 편이다. 하지만 CCW 알고리즘을 제대로 이해하고, 일직선(collinear) 처리 로직 및 교차점 계산 방식을 확실히 익히면, 기하 문제 전반에 걸쳐 활용할 수 있는 유용한 템플릿을 마련할 수 있다.  

추가적으로, 같은 선분이라도 좌표가 크게 주어져 곱셈 과정에서 오버플로우 문제가 생길 수 있으니, C++에서는 long long을 적절히 사용하고 Python에서는 큰 정수(임의정밀도)를 자동 처리해주므로 오히려 편할 수 있다. 더불어, 교차점 출력 시 오차 범위를 고려하여 충분히 많은 자릿수를 표시하면 정답 처리가 무난하다.  

추후 다른 기하 문제(다각형의 교차, 반평면 교집합 등)를 풀 때도, 여기서 배운 기초 개념(CCW, 직선 교차 공식, collinear 처리)이 반복적으로 등장하므로, 본 문제를 통해 확실히 기반을 다져두는 것이 좋을 것 같다.