---
title: "[Algorithm] C++/Python 백준 18406번 : 럭키 스트레이트"
categories: Algorithm
tags:
- Implementation
- String Manipulation
- Mathematics
- Simulation
- Time Complexity O(N)
image: "tmp_wordcloud.png"
date: 2024-10-16
---

게임에서 강력한 기술을 사용할 수 있는 조건을 판별하는 문제를 풀어보자.

문제 : [https://www.acmicpc.net/problem/18406](https://www.acmicpc.net/problem/18406)

## 문제 설명

어떤 게임에서 아웃복서 캐릭터는 "럭키 스트레이트"라는 강력한 기술을 가지고 있다. 하지만 이 기술은 언제나 사용할 수 있는 것이 아니라, 현재 캐릭터의 점수가 특정 조건을 만족할 때만 사용할 수 있다.

그 조건은 현재 점수 N의 자릿수를 반으로 나누어, 왼쪽 부분의 자릿수 합과 오른쪽 부분의 자릿수 합이 동일한 경우이다. 예를 들어, 점수 N이 123402라면 왼쪽 세 자리 숫자의 합은 1 + 2 + 3 = 6이고, 오른쪽 세 자리 숫자의 합은 4 + 0 + 2 = 6이므로 두 합이 같다. 따라서 이 경우에는 "럭키 스트레이트"를 사용할 수 있다.

현재 점수 N이 주어졌을 때, "럭키 스트레이트"를 사용할 수 있는 상태인지 판별하는 프로그램을 작성하시오. 사용할 수 있다면 `"LUCKY"`를, 사용할 수 없다면 `"READY"`를 출력한다. 단, 점수 N의 자릿수는 항상 짝수이며, 10 ≤ N ≤ 99,999,999이다.

## 접근 방식

이 문제는 주어진 숫자를 문자열로 취급하여 자릿수를 쉽게 접근할 수 있다. 문자열의 길이를 절반으로 나누어, 왼쪽 부분과 오른쪽 부분의 자릿수 합을 각각 계산한다. 그 후 두 합이 동일한지 비교하면 된다.

구현 단계는 다음과 같다:

1. 입력된 숫자를 문자열로 변환한다.
2. 문자열의 길이를 구하고 절반으로 나눈다.
3. 왼쪽 부분의 자릿수 합을 계산한다.
4. 오른쪽 부분의 자릿수 합을 계산한다.
5. 두 합을 비교하여 결과를 출력한다.

시간 복잡도는 입력된 숫자의 자릿수에 비례하므로 O(N)이다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <string>

int main() {
    std::string N;
    std::cin >> N; // 점수 N을 문자열로 입력받는다.

    int length = N.length();
    int half = length / 2;
    int sum_left = 0, sum_right = 0;

    // 왼쪽 부분 자릿수 합 계산
    for (int i = 0; i < half; ++i) {
        sum_left += N[i] - '0'; // 문자형 숫자를 정수형으로 변환하여 합산
    }

    // 오른쪽 부분 자릿수 합 계산
    for (int i = half; i < length; ++i) {
        sum_right += N[i] - '0';
    }

    // 두 합을 비교하여 결과 출력
    if (sum_left == sum_right) {
        std::cout << "LUCKY" << std::endl;
    } else {
        std::cout << "READY" << std::endl;
    }

    return 0;
}
```

### 코드 설명

- **입력 받기**:
  - `std::string N;`을 선언하여 입력된 숫자를 문자열로 저장한다.
  - 문자열로 저장함으로써 각 자릿수에 쉽게 접근할 수 있다.
  
- **길이 및 절반 위치 계산**:
  - `int length = N.length();`로 문자열의 전체 길이를 구한다.
  - `int half = length / 2;`로 문자열을 반으로 나눈다.

- **왼쪽 부분 자릿수 합 계산**:
  - `for (int i = 0; i < half; ++i)` 루프를 통해 왼쪽 절반의 자릿수를 순회한다.
  - `sum_left += N[i] - '0';`에서 문자형 숫자를 정수로 변환하여 합산한다.

- **오른쪽 부분 자릿수 합 계산**:
  - `for (int i = half; i < length; ++i)` 루프로 오른쪽 절반의 자릿수를 순회한다.
  - `sum_right += N[i] - '0';`로 합산한다.

- **결과 출력**:
  - `if (sum_left == sum_right)`로 두 합을 비교한다.
  - 같으면 `"LUCKY"`를, 다르면 `"READY"`를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char N[51]; // 최대 50자리 숫자를 저장할 수 있는 배열
    scanf("%s", N); // 문자열로 입력받기

    int length = strlen(N);
    int half = length / 2;
    int sum_left = 0, sum_right = 0;

    // 왼쪽 부분 자릿수 합 계산
    for (int i = 0; i < half; ++i) {
        sum_left += N[i] - '0'; // 문자형 숫자를 정수로 변환하여 합산
    }

    // 오른쪽 부분 자릿수 합 계산
    for (int i = half; i < length; ++i) {
        sum_right += N[i] - '0';
    }

    // 두 합을 비교하여 결과 출력
    if (sum_left == sum_right) {
        printf("LUCKY\n");
    } else {
        printf("READY\n");
    }

    return 0;
}
```

### 코드 설명

- **입력 받기**:
  - `char N[51];`로 최대 50자리의 숫자를 저장할 배열을 선언한다.
  - `scanf("%s", N);`로 문자열 형태로 입력받는다.

- **문자열 길이 및 절반 위치 계산**:
  - `int length = strlen(N);`으로 문자열의 길이를 구한다.
  - `int half = length / 2;`로 문자열을 반으로 나눈다.

- **왼쪽 부분 자릿수 합 계산**:
  - `for (int i = 0; i < half; ++i)`로 왼쪽 절반을 순회한다.
  - `sum_left += N[i] - '0';`로 합산한다.

- **오른쪽 부분 자릿수 합 계산**:
  - `for (int i = half; i < length; ++i)`로 오른쪽 절반을 순회한다.
  - `sum_right += N[i] - '0';`로 합산한다.

- **결과 출력**:
  - `if (sum_left == sum_right)`로 두 합을 비교한다.
  - 같으면 `"LUCKY"`를, 다르면 `"READY"`를 출력한다.

## Python 코드와 설명

```python
N = input()  # 점수 N을 문자열로 입력받음

length = len(N)
half = length // 2
sum_left = sum(int(N[i]) for i in range(half))      # 왼쪽 부분 자릿수 합
sum_right = sum(int(N[i]) for i in range(half, length))  # 오른쪽 부분 자릿수 합

# 두 합을 비교하여 결과 출력
if sum_left == sum_right:
    print("LUCKY")
else:
    print("READY")
```

### 코드 설명

- **입력 받기**:
  - `N = input()`으로 점수를 문자열로 입력받는다.

- **길이 및 절반 위치 계산**:
  - `length = len(N)`으로 문자열의 길이를 구한다.
  - `half = length // 2`로 문자열을 반으로 나눈다.

- **왼쪽 부분 자릿수 합 계산**:
  - `sum_left = sum(int(N[i]) for i in range(half))`로 왼쪽 절반의 자릿수를 합산한다.

- **오른쪽 부분 자릿수 합 계산**:
  - `sum_right = sum(int(N[i]) for i in range(half, length))`로 오른쪽 절반의 자릿수를 합산한다.

- **결과 출력**:
  - `if sum_left == sum_right:`로 두 합을 비교한다.
  - 같으면 `"LUCKY"`를, 다르면 `"READY"`를 출력한다.

## 결론

이 문제는 문자열을 이용한 간단한 구현 문제로, 자릿수에 접근하기 위해 문자열로 변환하여 처리하였다. 각 부분의 자릿수 합을 비교하는 것이 핵심이므로 복잡한 알고리즘보다는 정확한 구현이 중요하다. 추가적인 최적화가 필요하지 않으며, 입력 값의 크기가 크지 않으므로 O(N) 시간 복잡도로 충분하다.

이를 통해 문자열 처리와 기본적인 수학 계산 능력을 다시 한 번 확인할 수 있었다. 향후 비슷한 유형의 문제를 만났을 때 빠르게 접근할 수 있을 것이다.