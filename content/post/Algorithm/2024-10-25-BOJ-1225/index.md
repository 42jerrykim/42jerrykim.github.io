---
title: "[Algorithm] C++/Python 백준 1225번 : 이상한 곱셈"
categories: 
- Algorithm
- Math
- Implementation
tags:
- Mathematical Concepts
- Implementation
- Brute Force
- Time Complexity
- String Processing
- Sum of Digits
- Integer Multiplication
- Number Theory
image: "tmp_wordcloud.png"
date: 2024-10-25
---

안녕하세요! 오늘은 백준 온라인 저지의 1225번 문제, "이상한 곱셈"에 대해 알아보겠습니다. 이 문제는 두 숫자의 각 자리 숫자를 곱한 모든 조합의 합을 구하는 것으로, 큰 숫자에서도 효율적으로 해결할 수 있는 방법을 찾는 것이 중요합니다. 이제 문제를 자세히 살펴보고, 효과적인 해결 방법을 찾아보겠습니다.

문제 : [https://www.acmicpc.net/problem/1225](https://www.acmicpc.net/problem/1225)

## 문제 설명

두 개의 비음수 정수 A와 B가 주어질 때, 전통적인 곱셈 방식과는 다른 "이상한 곱셈"을 정의하려고 한다. 이 "이상한 곱셈"은 A의 각 자리 숫자와 B의 각 자리 숫자를 하나씩 선택하여 곱한 후, 가능한 모든 조합의 합을 계산하는 것이다. 예를 들어, A = 121이고 B = 34일 때:

```
1×3 + 1×4 + 2×3 + 2×4 + 1×3 + 1×4 = 28
```

즉, A가 n자리, B가 m자리 숫자라면 총 n×m개의 곱셈 조합이 존재하며, 이들의 합이 "이상한 곱셈"의 결과가 된다. 주어진 A와 B는 각각 최대 10,000자리의 숫자이므로, 효율적인 계산 방법이 요구된다.

## 접근 방식

이 문제를 효율적으로 해결하기 위해서는 모든 자리 숫자를 직접 곱한 후 합산하는 방식보다는, 두 숫자의 각 자리 숫자의 합을 구한 후 이를 곱하는 방법을 사용하는 것이 효과적이다. 이는 다음과 같은 수학적 사실에 기반한다:

\[
\left(\sum_{i=1}^{n} a_i\right) \times \left(\sum_{j=1}^{m} b_j\right) = \sum_{i=1}^{n} \sum_{j=1}^{m} (a_i \times b_j)
\]

즉, A의 모든 자리 숫자의 합과 B의 모든 자리 숫자의 합을 각각 구한 후, 이를 곱하면 "이상한 곱셈"의 결과를 얻을 수 있다. 이 방법은 두 숫자의 길이에 상관없이 O(N + M)의 시간 복잡도로 문제를 해결할 수 있어 매우 효율적이다.

## C++ 코드와 설명

다음은 최적화된 C++ 코드와 그에 대한 설명이다.

```cpp
#include <iostream>
#include <string>

using namespace std;

int main(){
    string A, B;
    cin >> A >> B;

    // A 또는 B가 "0"인 경우 결과는 0
    if(A == "0" || B == "0"){
        cout << "0";
        return 0;
    }

    // A의 각 자리 숫자의 합 계산
    long long sum_a = 0;
    for(char c : A){
        sum_a += (c - '0');
    }

    // B의 각 자리 숫자의 합 계산
    long long sum_b = 0;
    for(char c : B){
        sum_b += (c - '0');
    }

    // 결과 계산 및 출력
    long long result = sum_a * sum_b;
    cout << result;
}
```

### 코드 설명

1. **입력 처리**:
    - `cin >> A >> B;`를 통해 두 숫자를 문자열로 입력받는다.
    
2. **특별한 경우 처리**:
    - `if(A == "0" || B == "0")` 조건문을 통해 A나 B 중 하나라도 "0"인 경우, 결과는 "0"임을 출력하고 프로그램을 종료한다.
    
3. **각 자리 숫자의 합 계산**:
    - A의 각 자리 숫자를 순회하면서 `sum_a`에 더한다.
    - B의 각 자리 숫자를 순회하면서 `sum_b`에 더한다.
    
4. **결과 계산 및 출력**:
    - `sum_a * sum_b`를 계산하여 `result`에 저장한다.
    - `cout << result;`를 통해 결과를 출력한다.

이 방식은 두 숫자의 각 자리 숫자의 합을 구한 후, 이를 곱하는 단순한 계산으로 문제를 해결할 수 있어 매우 효율적이다.

## C++ without library 코드와 설명

이번에는 C++의 표준 라이브러리를 사용하지 않고, `stdio.h`와 `malloc.h`만을 사용하여 최적화된 코드를 작성해보겠다.

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(){
    char A[10005], B[10005];
    scanf("%s %s", A, B);

    // A 또는 B가 "0"인 경우 결과는 0
    if(strcmp(A, "0") == 0 || strcmp(B, "0") == 0){
        printf("0");
        return 0;
    }

    // A의 각 자리 숫자의 합 계산
    long long sum_a = 0;
    for(int i=0; i < strlen(A); i++){
        sum_a += (A[i] - '0');
    }

    // B의 각 자리 숫자의 합 계산
    long long sum_b = 0;
    for(int i=0; i < strlen(B); i++){
        sum_b += (B[i] - '0');
    }

    // 결과 계산 및 출력
    long long result = sum_a * sum_b;
    printf("%lld", result);
}
```

### 코드 설명

1. **입력 처리**:
    - `scanf("%s %s", A, B);`를 통해 두 숫자를 문자열로 입력받는다.
    
2. **특별한 경우 처리**:
    - `strcmp(A, "0") == 0 || strcmp(B, "0") == 0` 조건문을 통해 A나 B 중 하나라도 "0"인 경우, 결과는 "0"임을 출력하고 프로그램을 종료한다.
    
3. **각 자리 숫자의 합 계산**:
    - A의 각 자리 숫자를 순회하면서 `sum_a`에 더한다.
    - B의 각 자리 숫자를 순회하면서 `sum_b`에 더한다.
    
4. **결과 계산 및 출력**:
    - `sum_a * sum_b`를 계산하여 `result`에 저장한다.
    - `printf("%lld", result);`를 통해 결과를 출력한다.

이 코드 역시 표준 라이브러리를 사용하지 않고도 동일한 로직으로 문제를 해결할 수 있다.

## Python 코드와 설명

마지막으로, Python을 사용한 최적화된 코드와 그에 대한 설명이다.

```python
A, B = input().split()

# A 또는 B가 "0"인 경우 결과는 0
if A == "0" or B == "0":
    print(0)
else:
    # A의 각 자리 숫자의 합 계산
    sum_a = sum(int(c) for c in A)
    # B의 각 자리 숫자의 합 계산
    sum_b = sum(int(c) for c in B)
    # 결과 계산 및 출력
    print(sum_a * sum_b)
```

### 코드 설명

1. **입력 처리**:
    - `A, B = input().split()`을 통해 두 숫자를 문자열로 입력받는다.
    
2. **특별한 경우 처리**:
    - `if A == "0" or B == "0":` 조건문을 통해 A나 B 중 하나라도 "0"인 경우, 결과는 "0"임을 출력한다.
    
3. **각 자리 숫자의 합 계산**:
    - `sum_a = sum(int(c) for c in A)`를 통해 A의 각 자리 숫자를 정수로 변환하여 합을 구한다.
    - `sum_b = sum(int(c) for c in B)`를 통해 B의 각 자리 숫자를 정수로 변환하여 합을 구한다.
    
4. **결과 계산 및 출력**:
    - `print(sum_a * sum_b)`를 통해 두 합의 곱을 출력한다.

Python의 간결한 문법을 활용하여 동일한 로직을 더욱 간단하게 구현할 수 있다.

## 결론

이번 문제 "이상한 곱셈"은 두 숫자의 각 자리 숫자를 곱한 모든 조합의 합을 구하는 문제였다. 문제의 요구사항을 충족시키기 위해, 각 숫자의 자리 숫자 합을 구한 후 이를 곱하는 방식으로 효율적으로 문제를 해결할 수 있었다. 이 접근 방식은 두 숫자의 길이가 최대 10,000자리까지 커질 수 있다는 점을 고려할 때 매우 효과적이었다. 앞으로도 유사한 문제에서 이러한 수학적 아이디어를 활용하여 효율적인 알고리즘을 설계할 수 있을 것이다.