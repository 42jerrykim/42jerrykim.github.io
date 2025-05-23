---
title: "[Algorithm] C++/Python 백준 2166번 : 다각형의 면적"
categories: 
- Algorithm
- Gold5
- Geometry
- Implementation
tags:
- Shoelace
- Implementation
- BruteForce
- Optimization
- O(N)
- Vector
- 수학
- Geometry
image: "index.png"
date: 2025-01-10
---

다각형의 면적을 구하는 문제는 기하학에서 매우 기초적이면서도 중요한 주제이다. 특히 2차원 평면 위에 임의로 주어진 꼭지점들의 좌표가 순서대로 나열되어 있을 때, 이를 사용하여 다각형의 면적을 효율적으로 구하는 알고리즘이 많이 활용된다. 본 글에서는 백준 2166번 "다각형의 면적" 문제를 다루며, 다각형의 면적을 구하는 Shoelace(슈얼레이스) 공식을 간단하게 소개하고, C++과 Python으로 구현하는 방법을 다룰 것이다.

문제 : [https://www.acmicpc.net/problem/2166](https://www.acmicpc.net/problem/2166)

## 문제 설명

백준 2166번 "다각형의 면적" 문제는 2차원 평면 위의 N개의 정점으로 구성된 다각형이 주어졌을 때, 해당 다각형의 면적을 구하는 문제이다. 정점들은 다각형을 이루는 순서대로 주어지며, 입력으로 주어진 순서 자체가 다각형의 모양을 결정한다. 구해야 하는 다각형은 볼록다각형이 될 수도 있고 오목다각형이 될 수도 있으며, 정점의 개수 N은 3 이상 10,000 이하로 주어진다.

이 문제에서 중요한 점은 다음과 같다.  
첫째, 입력으로 제공되는 좌표값의 범위가 최대 절댓값 100,000인 정수이므로, 면적 계산 시 곱셈 과정에서 수의 범위가 커질 수 있다. 따라서 넓이 계산 과정에서 중간 오버플로우를 방지하도록 주의해야 한다.  
둘째, 문제에서는 다각형의 면적을 구한 뒤, 소수점 아래 둘째 자리에서 반올림하여 첫째 자리까지 출력하라고 명시하고 있다. 예컨대 123.4567이 나오면 123.5로, 123.44가 나오면 123.4로 출력해야 한다.  
셋째, 다각형의 면적을 구하기 위해서는 여러 기하학 공식을 사용할 수 있지만, 가장 자주 쓰이는 방법 중 하나가 바로 Shoelace(슈얼레이스) 공식이다. 이 공식은 각 꼭지점의 좌표를 사용하여 면적을 빠르고 간단하게 구할 수 있으며, 실제로 축에 평행하지 않은 복잡한 다각형도 쉽고 정확하게 면적을 산출할 수 있다.

Shoelace 공식의 핵심 아이디어는 “각 변을 가로지르는 사각형(혹은 평행사변형)들의 누적된 넓이 차이”를 활용한다는 것이다. 좌표 평면에서 다각형의 꼭지점을 \((x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\)라 할 때, 다음 식으로 면적을 구한다:

\[
\text{면적} = \frac{1}{2} \Biggl|\sum_{i=1}^{N-1} (x_i \cdot y_{i+1} - x_{i+1} \cdot y_i) + (x_N \cdot y_1 - x_1 \cdot y_N)\Biggr|
\]

이처럼 \(\sum (x_i \times y_{i+1})\)에서 \(\sum (y_i \times x_{i+1})\)를 빼서 절댓값을 취하고, 그 값을 2로 나누어 주면 다각형의 면적을 쉽게 구할 수 있다. 마지막 점 \((x_N, y_N)\)과 첫 번째 점 \((x_1, y_1)\)도 연결되어 있어야 하므로, 인덱스 처리를 주의 깊게 해야 한다.  
결과적으로, 이러한 방식을 통해 N개의 점을 순회하며 넓이를 구할 수 있으며, 시간 복잡도는 O(N)에 달한다. 문제에서 N의 최댓값은 10,000이므로, 이 방식은 충분히 빠른 시간 내에 계산을 완료할 수 있다.

## 접근 방식

1. **입력 받기**  
   - 먼저 N(3 ≤ N ≤ 10,000)을 입력받는다.  
   - 이후 N개의 좌표 \((x_i, y_i)\)를 벡터나 리스트에 차례대로 저장한다.  
   - 입력되는 점들은 다각형의 꼭지점을 연결하는 순서 그대로 주어진다.  

2. **Shoelace 공식 사용**  
   - 다각형을 이루는 점들을 순회하면서 \((x_i \times y_{i+1})\)와 \((y_i \times x_{i+1})\)의 합을 각각 구한다.  
   - 이때, 인덱스를 초과하지 않도록, 마지막 점 \((x_N, y_N)\)과 첫 번째 점 \((x_1, y_1)\)을 이어주는 연산도 반드시 포함한다.  
   - 두 누적값의 차의 절댓값을 취하고 2로 나누어 주면 면적이 된다.  

3. **출력 형식**  
   - 문제에서는 소수점 아래 둘째 자리에서 반올림하여 첫째 자리까지 출력하라고 요구한다.  
   - C++의 경우 `fixed`와 `setprecision(1)`을 적절히 사용하여 반올림이 적용된 결과를 출력한다.  
   - Python의 경우 `round(값, 1)` 등을 활용하거나, `format`을 사용하여 형식에 맞게 출력한다.  

4. **시간 복잡도**  
   - Shoelace 공식은 \(\sum_{i=1}^{N} (\dots)\) 형태로 점들을 단순 순회하며 계산하므로 O(N) 시간이 걸린다.  
   - N이 최대 10,000이므로 성능상 문제가 없다.  


## C++ 코드와 설명

아래 코드는 Shoelace 공식을 이용하여 다각형의 면적을 구한 예시이다. 각 줄에 간단한 주석을 추가하였다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;  // 점의 개수 입력

    vector<long long> x(N), y(N);
    for (int i = 0; i < N; i++) {
        cin >> x[i] >> y[i];  // 각 점의 (x, y)좌표 입력
    }

    long long sum = 0;
    // Shoelace 공식 적용:
    // (x_i * y_{i+1}) - (x_{i+1} * y_i) 의 누적 합을 구한다.
    for (int i = 0; i < N - 1; i++) {
        sum += x[i] * y[i + 1] - x[i + 1] * y[i];
    }
    // 마지막 점과 첫 번째 점도 이어준다.
    sum += x[N - 1] * y[0] - x[0] * y[N - 1];

    // 면적 = 절댓값(sum) / 2
    long double area = fabsl((long double)sum) / 2.0;

    // 소수점 둘째 자리에서 반올림하여 첫째 자리까지 출력
    cout << fixed << setprecision(1) << area << "\n";

    return 0;
}
```

### 코드 동작 단계별 설명

1. **입력 처리**  
   - `cin >> N`으로 점의 개수를 읽고, `x`, `y` 벡터를 선언하여 크기를 N으로 할당한다.  
   - 이후 `for`문을 통해 N개의 `(x[i], y[i])`를 입력받는다.  

2. **넓이 계산**  
   - `sum` 변수를 선언하고 0으로 초기화한다.  
   - 첫 번째 점부터 (N-1)번째 점까지 \((x_i \times y_{i+1}) - (x_{i+1} \times y_i)\)를 반복 누적한다.  
   - 마지막으로 (N-1)번째 점과 0번째 점(처음 점)을 연결하는 부분도 포함한다.  
   - 합산된 `sum`의 절댓값을 2로 나누어 면적을 구한다.  

3. **출력**  
   - `fabsl`을 사용하여 `sum`의 절댓값을 구하고, `2.0`으로 나눠 면적을 구한다.  
   - `fixed`와 `setprecision(1)`을 통해 반올림된 결과를 소수점 한 자리까지 출력한다.  

## Python 코드와 설명

다음은 Python으로 Shoelace 공식을 구현한 예시이다. 코드에 주석을 달아 각 단계를 상세히 설명한다.

```python
import sys

def main():
    input = sys.stdin.readline
    
    N = int(input().strip())  # 점의 개수 입력
    coords = []
    
    for _ in range(N):
        x, y = map(int, input().split())
        coords.append((x, y))  # (x, y) 좌표를 리스트에 저장

    sum_area = 0
    # 0번 인덱스부터 N-2번 인덱스까지 반복
    for i in range(N - 1):
        sum_area += coords[i][0] * coords[i+1][1] - coords[i+1][0] * coords[i][1]
    # 마지막 점과 첫 번째 점 연결
    sum_area += coords[-1][0] * coords[0][1] - coords[0][0] * coords[-1][1]

    # Shoelace 공식으로 면적 계산
    area = abs(sum_area) / 2.0

    # 소수점 둘째 자리에서 반올림하여 첫째 자리까지 출력
    # round(값, 자릿수)를 사용해도 되나, 문제의 출력 방식(예: 100.0) 유지를 위해 format 사용
    print(f"{area:.1f}")

if __name__ == "__main__":
    main()
```

### 코드 동작 단계별 설명

1. **입력 처리**  
   - `N`을 입력받아 점의 개수를 저장하고, `coords` 리스트에 각 점을 튜플 형태로 보관한다.  
   - `sys.stdin.readline()`을 사용하여 입력 속도를 높인다.  

2. **Shoelace 공식 적용**  
   - `sum_area` 변수를 0으로 초기화한다.  
   - 0번 인덱스부터 (N-2)번 인덱스까지, 현재 점과 다음 점을 이용하여 \((x_i \times y_{i+1}) - (x_{i+1} \times y_i)\)를 반복 합산한다.  
   - 마지막 점 `coords[-1]`와 첫 번째 점 `coords[0]`을 연결하는 과정도 추가한다.  

3. **면적 및 출력**  
   - `abs(sum_area) / 2.0`으로 면적을 구한다.  
   - `format` 문자열을 사용해 소수점 첫째 자리까지 반올림하여 결과를 출력한다.  


## 결론

본 문제는 Shoelace 공식을 활용하면 다각형의 면적을 매우 간단하고 빠르게 구할 수 있다는 점을 잘 보여준다. 특히 다각형이 볼록이든 오목이든 상관없이 점들이 이어진 순서대로만 처리해주면 되므로, 별도의 복잡한 전처리가 필요하지 않아 효율적이다.  
추가적으로, 구현 시 주의해야 할 점은 다음과 같다.  
- 점들을 입력받을 때 순서가 꼬이지 않도록 문제에서 주어진 순서를 그대로 반영해야 한다.  
- 넓이 계산 과정에서 오버플로우가 일어나지 않도록 `long long` 또는 그 이상의 범위를 사용하거나, Python에서는 기본 정수 자료형을 활용하여 문제를 방지한다.  
- 요구된 출력 형식(소수점 아래 둘째 자리에서 반올림)에 맞춰 정확히 출력해야 한다.  

추후에는 다각형의 넓이뿐만 아니라, 선분 교차 검사, 볼록 껍질(Convex Hull) 알고리즘 등 보다 다양한 기하학 문제에서 Shoelace 공식을 응용할 수 있다. 이를 학습하여 여러 가지 기하 문제에 두루 활용해 보는 것을 추천한다.
