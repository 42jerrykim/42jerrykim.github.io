---
title: "[Algorithm] C++/Python 백준 15995번 : 잉여역수 구하기"
categories: 
- Algorithm
- Number Theory
- Bruteforce
- Modular Inverse
tags:
- Number Theory
- Extended Euclidean Algorithm
- Implementation
- Optimization Techniques
- O(log N)
- Mathematical Concepts
- Modular Arithmetic
- Bruteforce
- Modular Inverse
image: "tmp_wordcloud.png"
date: 2024-01-01
---

대학에서 수학을 전공하지 않는 학생들에게 정수론은 종종 어려운 과목으로 다가온다. 지민이는 정수론을 싫어하여 강의 시간에 졸다가 혁주로부터 숙제를 듣게 되었다. 혁주는 지민이에게 두 자연수 \( a \)와 \( m \)이 서로소일 때, \( a \)의 법 \( m \)에 대한 잉여역수 \( a^* \)를 구하는 문제를 내주었다. 이 글에서는 백준 온라인 저지의 문제 번호 15995번 "잉여역수 구하기"를 통해 잉여역수를 구하는 방법과 이를 구현하는 다양한 방안을 살펴보겠다.

문제 : [https://www.acmicpc.net/problem/15995](https://www.acmicpc.net/problem/15995)

## 문제 설명

두 자연수 \( a \)와 \( m \)이 서로소일 때, \( a \)의 법 \( m \)에 대한 잉여역수 \( a^* \)는 다음을 만족하는 자연수 \( x \)를 의미한다.

\[
a \times x \equiv 1 \ (\text{mod} \ m)
\]

즉, \( a \times x \)를 \( m \)으로 나눈 나머지가 1이 되는 최소의 자연수 \( x \)를 찾는 문제이다. 예를 들어, \( a = 3 \)이고 \( m = 4 \)일 때, \( 3 \times 3 = 9 \equiv 1 \ (\text{mod} \ 4) \)이므로, 잉여역수는 3이 된다. 이 문제에서는 주어진 \( a \)와 \( m \)에 대해 잉여역수 \( a^* \)를 출력해야 한다. \( a \)와 \( m \)은 서로소이며, 잉여역수는 항상 존재한다는 점이 보장된다.

## 접근 방식

잉여역수를 구하는 대표적인 방법은 **확장 유클리드 알고리즘**을 사용하는 것이다. 확장 유클리드 알고리즘을 통해 두 수 \( a \)와 \( m \)의 최대공약수(GCD)를 구함과 동시에, 베주 정리에 의해 잉여역수 \( a^* \)를 찾을 수 있다. 확장 유클리드 알고리즘은 재귀적으로 \( a \)와 \( m \)의 GCD를 구하면서, 동시에 \( x \)와 \( y \)를 찾아 \( a \times x + m \times y = \text{GCD}(a, m) \)를 만족시킨다. 여기서 \( \text{GCD}(a, m) = 1 \)이므로, \( x \)가 잉여역수가 된다. 이때 \( x \)가 음수일 수 있으므로, \( m \)을 더해 양수의 최소값을 구하면 된다.

또한, 파이썬에서는 내장 함수인 `pow(a, -1, m)`을 사용하여 잉여역수를 간단히 구할 수 있다. 이 방법은 파이썬 3.8 이상에서 지원된다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

// 확장 유클리드 알고리즘을 통해 GCD와 베주 계수를 구하는 함수
long long extended_gcd_func(long long a, long long b, long long &x, long long &y){
    if(b == 0){
        x = 1;
        y = 0;
        return a;
    }
    long long x1, y1;
    long long gcd = extended_gcd_func(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return gcd;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    long long a, m;
    cin >> a >> m;
    
    long long x, y;
    long long gcd = extended_gcd_func(a, m, x, y);
    
    // gcd가 1이 아니면 잉여역수가 존재하지 않음
    // 하지만 문제 조건에서 서로소이므로 항상 잉여역수가 존재
    // 잉여역수가 음수일 수 있으므로 m을 더해 양수로 만듦
    long long inv = (x % m + m) % m;
    cout << inv;
}
```

### 코드 설명

1. **확장 유클리드 알고리즘 함수 (`extended_gcd_func`)**:
    - 재귀적으로 \( \text{GCD}(a, b) \)를 구하면서, 베주 계수 \( x \)와 \( y \)를 찾아낸다.
    - 재귀의 기저 사례는 \( b = 0 \)일 때로, 이때 \( x = 1 \)과 \( y = 0 \)을 반환한다.
    - 재귀 호출을 통해 이전 단계의 \( x \)와 \( y \) 값을 받아와 현재 단계의 \( x \)와 \( y \)를 계산한다.

2. **메인 함수 (`main`)**:
    - 입력으로 두 자연수 \( a \)와 \( m \)을 받는다.
    - `extended_gcd_func`를 호출하여 \( \text{GCD}(a, m) \)와 \( x \), \( y \)를 구한다.
    - 문제 조건에서 \( a \)와 \( m \)은 서로소이므로 \( \text{GCD}(a, m) = 1 \)이며, 따라서 \( x \)는 잉여역수가 된다.
    - \( x \)가 음수일 경우를 대비하여 \( m \)을 더한 후 \( m \)으로 나눈 나머지를 취해 최소의 자연수 잉여역수를 구한다.
    - 최종적으로 잉여역수를 출력한다.

## Python 코드와 설명

```python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        # 잉여역수가 존재하지 않음 (문제 조건상 발생하지 않음)
        return None
    else:
        # x가 음수일 수 있으므로 m을 더해 양수로 만듦
        return x % m

# 입력 받기
a, m = map(int, input().split())

# 잉여역수 구하기
inv = modular_inverse(a, m)

# 결과 출력
print(inv)
```

### 코드 설명

1. **확장 유클리드 알고리즘 함수 (`extended_gcd`)**:
    - 재귀적으로 \( \text{GCD}(a, b) \)를 구하면서, 베주 계수 \( x \)와 \( y \)를 반환한다.
    - 기저 사례는 \( b = 0 \)일 때로, 이때 \( x = 1 \)과 \( y = 0 \)을 반환한다.
    - 재귀 호출을 통해 이전 단계의 \( x1 \)과 \( y1 \) 값을 받아와 현재 단계의 \( x \)와 \( y \)를 계산한다.

2. **모듈러 역수 함수 (`modular_inverse`)**:
    - `extended_gcd`를 호출하여 \( \text{GCD}(a, m) \)와 \( x \), \( y \)를 구한다.
    - \( \text{GCD}(a, m) \)가 1이 아니면 잉여역수가 존재하지 않음을 반환한다. 하지만 문제 조건에서 \( a \)와 \( m \)은 서로소이므로 항상 잉여역수가 존재한다.
    - \( x \)가 음수일 수 있으므로 \( m \)을 더한 후 \( m \)으로 나눈 나머지를 취해 최소의 자연수 잉여역수를 구한다.

3. **입력 및 출력**:
    - 사용자로부터 두 정수 \( a \)와 \( m \)을 입력받는다.
    - `modular_inverse` 함수를 통해 잉여역수를 구하고 출력한다.

## 결론

이번 문제를 통해 확장 유클리드 알고리즘을 이용한 잉여역수 구하는 방법을 학습할 수 있었다. 잉여역수는 암호학 등 다양한 분야에서 중요한 개념으로 활용되며, 이를 효율적으로 구현하는 것은 많은 문제 해결에 도움이 된다. C++과 Python 모두에서 확장 유클리드 알고리즘을 구현할 수 있었으며, 특히 Python의 내장 함수를 활용하면 더욱 간단하게 잉여역수를 구할 수 있음을 확인했다. 추가적인 최적화 방안으로는 반복문을 이용한 비재귀적 확장 유클리드 알고리즘을 구현하여 스택 오버플로우를 방지할 수 있으며, 이는 입력 크기가 매우 큰 경우에 유용할 것이다.