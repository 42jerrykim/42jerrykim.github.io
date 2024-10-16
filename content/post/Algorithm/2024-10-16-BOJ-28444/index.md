---
title: "[Algorithm] C++/Python 백준 28444번 : HI-ARC=?"
categories: Algorithm
tags:
- Implementation
- Math
- Arithmetic
- Basic Calculation
- Problem Solving
image: "tmp_wordcloud.png"
date: 2024-10-16
---

이번 포스팅에서는 백준 온라인 저지의 28444번 문제인 "HI-ARC=?"를 다루어 보겠습니다. 이 문제는 간단한 수식을 구현하는 문제로, 기본적인 산술 연산과 입력 처리 능력을 확인할 수 있습니다.

문제 : [https://www.acmicpc.net/problem/28444](https://www.acmicpc.net/problem/28444)

## 문제 설명

HI-ARC 학회는 일상 속의 문장들을 수식으로 표현하는 것을 즐기는 특이한 문화를 가지고 있습니다. 그중에서도 최근에 개발한 HI-ARC 수식은 아래와 같은 규칙을 따릅니다:

1. **첫 번째 항**은 **H**와 **I**의 곱입니다.
2. **두 번째 항**은 **A**, **R**, **C**의 곱입니다.
3. **결과값**은 **첫 번째 항에서 두 번째 항을 뺀 값**입니다.

이를 수식으로 표현하면 다음과 같습니다:

\[
\text{결과값} = (H \times I) - (A \times R \times C)
\]

각각의 문자에 해당하는 숫자들이 입력으로 주어졌을 때, 이 수식을 계산하여 결과값을 출력하는 것이 문제의 목표입니다.

### 입력

- 첫째 줄에 **H**, **I**, **A**, **R**, **C**가 공백으로 구분되어 순서대로 주어집니다.
- 각 값은 다음 범위를 만족합니다:
  - \(0 \leq H, I, A, R, C \leq 100\)
  - 모든 값은 정수입니다.

### 출력

- 계산된 결과값을 출력합니다.

### 예제 입력 1

```
4 6 1 2 3
```

### 예제 출력 1

```
18
```

#### 예제 설명

- **첫 번째 항**: \(4 \times 6 = 24\)
- **두 번째 항**: \(1 \times 2 \times 3 = 6\)
- **결과값**: \(24 - 6 = 18\)

## 접근 방식

이 문제는 기본적인 산술 연산과 입력 처리를 요구하는 간단한 구현 문제입니다. 따라서 다음과 같은 단계로 접근할 수 있습니다:

1. **입력 처리**: 공백으로 구분된 다섯 개의 정수를 입력받습니다.
2. **첫 번째 항 계산**: **H**와 **I**를 곱하여 첫 번째 항을 계산합니다.
3. **두 번째 항 계산**: **A**, **R**, **C**를 곱하여 두 번째 항을 계산합니다.
4. **결과값 계산**: 첫 번째 항에서 두 번째 항을 빼서 결과값을 구합니다.
5. **출력**: 계산된 결과값을 출력합니다.

특별한 알고리즘이나 자료 구조가 필요하지 않으며, 자료형의 범위도 정수(int)로 충분합니다.

## C++ 코드와 설명

```cpp
#include <iostream> // 입출력을 위한 헤더 파일 사용

int main() {
    int H, I, A, R, C; // 다섯 개의 정수 변수를 선언
    std::cin >> H >> I >> A >> R >> C; // 입력받기

    int first_term = H * I; // 첫 번째 항 계산
    int second_term = A * R * C; // 두 번째 항 계산

    int result = first_term - second_term; // 결과값 계산

    std::cout << result << std::endl; // 결과값 출력

    return 0; // 프로그램 종료
}
```

### 코드의 동작 단계별 설명

1. **입력 처리**

   ```cpp
   std::cin >> H >> I >> A >> R >> C;
   ```

   - 사용자로부터 다섯 개의 정수 **H**, **I**, **A**, **R**, **C**를 입력받습니다.

2. **첫 번째 항 계산**

   ```cpp
   int first_term = H * I;
   ```

   - **H**와 **I**를 곱하여 첫 번째 항을 계산합니다.

3. **두 번째 항 계산**

   ```cpp
   int second_term = A * R * C;
   ```

   - **A**, **R**, **C**를 곱하여 두 번째 항을 계산합니다.

4. **결과값 계산**

   ```cpp
   int result = first_term - second_term;
   ```

   - 첫 번째 항에서 두 번째 항을 빼서 결과값을 구합니다.

5. **결과 출력**

   ```cpp
   std::cout << result << std::endl;
   ```

   - 계산된 결과값을 출력합니다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>  // C 표준 입출력을 위한 헤더 파일

int main() {
    int H, I, A, R, C; // 다섯 개의 정수 변수 선언
    scanf("%d %d %d %d %d", &H, &I, &A, &R, &C); // 입력받기

    int first_term = H * I; // 첫 번째 항 계산
    int second_term = A * R * C; // 두 번째 항 계산

    int result = first_term - second_term; // 결과값 계산

    printf("%d\n", result); // 결과값 출력

    return 0; // 프로그램 종료
}
```

### 코드의 동작 단계별 설명

1. **입력 처리**

   ```cpp
   scanf("%d %d %d %d %d", &H, &I, &A, &R, &C);
   ```

   - `scanf` 함수를 사용하여 사용자로부터 다섯 개의 정수를 입력받습니다.

2. **첫 번째 항 계산**

   ```cpp
   int first_term = H * I;
   ```

   - **H**와 **I**를 곱하여 첫 번째 항을 계산합니다.

3. **두 번째 항 계산**

   ```cpp
   int second_term = A * R * C;
   ```

   - **A**, **R**, **C**를 곱하여 두 번째 항을 계산합니다.

4. **결과값 계산**

   ```cpp
   int result = first_term - second_term;
   ```

   - 첫 번째 항에서 두 번째 항을 빼서 결과값을 구합니다.

5. **결과 출력**

   ```cpp
   printf("%d\n", result);
   ```

   - 계산된 결과값을 출력합니다.

## Python 코드와 설명

```python
# 입력받은 문자열을 공백 기준으로 분리하고 정수로 변환
H, I, A, R, C = map(int, input().split())

# 첫 번째 항 계산
first_term = H * I

# 두 번째 항 계산
second_term = A * R * C

# 결과값 계산
result = first_term - second_term

# 결과값 출력
print(result)
```

### 코드의 동작 단계별 설명

1. **입력 처리**

   ```python
   H, I, A, R, C = map(int, input().split())
   ```

   - `input()` 함수로 한 줄의 문자열을 입력받고, `split()` 메서드로 공백 기준으로 분리합니다.
   - `map(int, ...)`를 사용하여 분리된 문자열을 정수로 변환하고 각각의 변수에 할당합니다.

2. **첫 번째 항 계산**

   ```python
   first_term = H * I
   ```

   - **H**와 **I**를 곱하여 첫 번째 항을 계산합니다.

3. **두 번째 항 계산**

   ```python
   second_term = A * R * C
   ```

   - **A**, **R**, **C**를 곱하여 두 번째 항을 계산합니다.

4. **결과값 계산**

   ```python
   result = first_term - second_term
   ```

   - 첫 번째 항에서 두 번째 항을 빼서 결과값을 구합니다.

5. **결과 출력**

   ```python
   print(result)
   ```

   - 계산된 결과값을 출력합니다.

## 결론

이번 문제는 기본적인 산술 연산과 입력 처리를 요구하는 단순한 구현 문제였습니다. 이러한 문제는 프로그래밍 언어의 기초 문법과 입출력 방법을 숙달하는 데 도움이 됩니다. 앞으로 더 복잡한 문제를 풀기 위해서는 이러한 기초를 탄탄히 다져 놓는 것이 중요하다고 생각합니다. 또한, 코드 작성 시 가독성을 높이기 위해 변수명을 의미 있게 정하고 주석을 적절히 사용하는 습관을 들이는 것도 좋습니다.