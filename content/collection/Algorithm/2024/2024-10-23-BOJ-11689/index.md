---
title: "[Algorithm] C++/Python 백준 11689번 : GCD(n, k) = 1"
categories: 
- Algorithm
- NumberTheory
- Euler's Totient Function
tags:
- Euler's Totient Function
- Pollard's Rho Algorithm
- PrimalityTesting
- IntegerFactorization
- NumberTheory
- Mathematics
- Optimization
- O(log N)
- ModularArithmetic
- GreatestCommonDivisor
image: "tmp_wordcloud.png"
date: 2024-10-23
---

이번 포스팅에서는 백준 온라인 저지의 11689번 문제인 **"GCD(n, k) = 1"**을 다룬다. 이 문제는 큰 수 범위에서 서로소의 개수를 구해야 하므로, 효율적인 알고리즘과 수학적 지식을 활용하는 것이 핵심이다. 오일러 피 함수(Euler's Totient Function)와 소인수분해 알고리즘을 적용하여 문제를 해결해보자.

문제 : [https://www.acmicpc.net/problem/11689](https://www.acmicpc.net/problem/11689)

## 문제 설명

자연수 \( n \)이 주어졌을 때, \( 1 \leq k \leq n \) 범위에서 \( \gcd(n, k) = 1 \)을 만족하는 자연수 \( k \)의 개수를 구하는 문제이다.

예를 들어, \( n = 5 \)인 경우를 살펴보자.

- \( k = 1 \): \(\gcd(5, 1) = 1\)
- \( k = 2 \): \(\gcd(5, 2) = 1\)
- \( k = 3 \): \(\gcd(5, 3) = 1\)
- \( k = 4 \): \(\gcd(5, 4) = 1\)
- \( k = 5 \): \(\gcd(5, 5) = 5\)

따라서 \( \gcd(5, k) = 1 \)을 만족하는 \( k \)는 총 4개이다.

하지만 \( n \)의 범위가 최대 \( 10^{12} \)까지 주어지므로, 모든 \( k \)에 대해 \( \gcd(n, k) \)를 직접 계산하는 것은 비효율적이다. 이에 따라 효율적인 알고리즘을 사용하여 문제를 해결해야 한다.

## 접근 방식

이 문제는 **오일러 피 함수(Euler's Totient Function)**를 활용하여 해결할 수 있다. 오일러 피 함수 \( \phi(n) \)는 \( n \) 이하의 양의 정수 중에서 \( n \)과 서로소인 수의 개수를 나타낸다. 즉, 이 문제에서 구하려는 값과 일치한다.

오일러 피 함수는 다음과 같이 계산할 수 있다:

\[
\phi(n) = n \times \prod_{p \in P} \left(1 - \frac{1}{p}\right)
\]

여기서 \( P \)는 \( n \)의 서로 다른 소인수의 집합이다.

따라서 문제를 해결하기 위한 단계는 다음과 같다:

1. **\( n \)의 소인수분해**: \( n \)을 소인수분해하여 모든 서로 다른 소인수를 구한다.
2. **오일러 피 함수 계산**: 구한 소인수를 이용하여 \( \phi(n) \)을 계산한다.

그러나 \( n \)의 범위가 매우 크기 때문에 일반적인 소인수분해 알고리즘은 시간 내에 동작하지 않는다. 이를 해결하기 위해 다음의 알고리즘을 사용한다:

- **Pollard's Rho Algorithm**: 큰 수를 효율적으로 소인수분해할 수 있는 알고리즘이다.
- **Miller-Rabin Primality Test**: 주어진 수가 소수인지 빠르게 판단할 수 있는 확률적 알고리즘이다.

이 두 알고리즘을 조합하여 \( n \)을 효율적으로 소인수분해하고, 오일러 피 함수를 계산한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <map>
#include <random>

typedef unsigned long long ull;

using namespace std;

// 최대공약수를 구하는 함수
ull gcd(ull a, ull b) {
    while (b) {
        ull t = a % b;
        a = b;
        b = t;
    }
    return a;
}

// (a * b) % mod를 계산하는 함수 (오버플로우 방지)
ull mulmod(ull a, ull b, ull mod) {
    return (__uint128_t)a * b % mod;
}

// (a ^ b) % mod를 계산하는 함수 (빠른 거듭제곱)
ull powmod(ull a, ull b, ull mod) {
    ull result = 1;
    a %= mod;
    while (b) {
        if (b & 1)
            result = mulmod(result, a, mod);
        a = mulmod(a, a, mod);
        b >>= 1;
    }
    return result;
}

// Miller-Rabin 소수 판정 알고리즘
bool is_prime(ull n) {
    if (n < 2)
        return false;
    ull d = n - 1;
    ull s = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        ++s;
    }
    ull witnesses[] = {2, 3, 5, 7, 11, 13, 17};
    for (ull a : witnesses) {
        if (a >= n)
            continue;
        ull x = powmod(a, d, n);
        if (x == 1 || x == n - 1)
            continue;
        bool continue_loop = false;
        for (ull r = 1; r < s; ++r) {
            x = mulmod(x, x, n);
            if (x == n - 1) {
                continue_loop = true;
                break;
            }
        }
        if (continue_loop)
            continue;
        return false;
    }
    return true;
}

// Pollard's Rho 알고리즘을 사용한 소인수분해
ull pollards_rho(ull n) {
    if (n % 2 == 0)
        return 2;
    std::mt19937_64 rnd(random_device{}());
    ull c = rnd() % (n - 1) + 1;
    ull x = rnd() % (n - 1) + 1;
    ull y = x;
    ull d = 1;
    while (d == 1) {
        x = (mulmod(x, x, n) + c) % n;
        y = (mulmod(y, y, n) + c) % n;
        y = (mulmod(y, y, n) + c) % n;
        d = gcd((x > y) ? x - y : y - x, n);
        if (d == n)
            return pollards_rho(n);
    }
    if (is_prime(d))
        return d;
    else
        return pollards_rho(d);
}

// 소인수분해 결과를 저장하는 함수
void factorize(ull n, map<ull, int> &factors) {
    if (n == 1)
        return;
    if (is_prime(n)) {
        factors[n]++;
        return;
    }
    ull d = pollards_rho(n);
    factorize(d, factors);
    factorize(n / d, factors);
}

int main() {
    ull n;
    cin >> n;
    if (n == 1) {
        cout << 1 << endl;
        return 0;
    }
    map<ull, int> factors;
    factorize(n, factors);

    ull result = n;
    // 오일러 피 함수 계산
    for (auto &p : factors) {
        result = result / p.first * (p.first - 1);
    }
    cout << result << endl;
    return 0;
}
```

### 코드 설명

1. **입력 받기**:
   - `cin >> n;`을 통해 자연수 \( n \)을 입력받는다.

2. **소인수분해**:
   - `factorize(n, factors);`를 호출하여 \( n \)을 소인수분해한다.
   - `factorize` 함수는 재귀적으로 작동하며, \( n \)이 소수이면 `factors` 맵에 추가한다.
   - 소수가 아니면 `pollards_rho` 함수를 사용하여 인수를 찾아 다시 `factorize`를 호출한다.

3. **오일러 피 함수 계산**:
   - 초기값을 \( result = n \)으로 설정한다.
   - 각 소인수 \( p \)에 대해 \( result = result \times (1 - \frac{1}{p}) \)를 계산한다.
   - 이는 코드에서 `result = result / p.first * (p.first - 1);`로 구현된다.

4. **결과 출력**:
   - 계산된 \( result \)를 출력한다.

### 주요 함수 설명

- **gcd(a, b)**: 최대공약수를 구하는 함수이다.
- **mulmod(a, b, mod)**: 큰 수의 곱셈 연산 시 오버플로우를 방지하기 위해 사용한다.
- **powmod(a, b, mod)**: 모듈러 거듭제곱을 계산한다.
- **is_prime(n)**: Miller-Rabin 알고리즘을 사용하여 \( n \)이 소수인지 판정한다.
- **pollards_rho(n)**: Pollard's Rho 알고리즘을 사용하여 \( n \)의 인수를 찾는다.
- **factorize(n, factors)**: 재귀적으로 \( n \)을 소인수분해하여 `factors` 맵에 저장한다.


## Python 코드와 설명

```python
import sys
import random

def main():
    n = int(sys.stdin.readline())
    original_n = n  # 결과 계산을 위해 원본 n 저장
    if n == 1:
        print(1)
        return

    factors = {}

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def mulmod(a, b, mod):
        return (a * b) % mod

    def powmod(a, b, mod):
        result = 1
        a %= mod
        while b:
            if b & 1:
                result = mulmod(result, a, mod)
            a = mulmod(a, a, mod)
            b >>= 1
        return result

    def is_prime(n):
        if n < 2:
            return False
        for p in [2, 3, 5, 7, 11, 13]:
            if n % p == 0:
                return n == p
        d = n - 1
        s = 0
        while d % 2 == 0:
            d >>= 1
            s += 1
        for a in [2, 3, 5, 7, 11, 13]:
            x = powmod(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = mulmod(x, x, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def pollards_rho(n):
        if n % 2 == 0:
            return 2
        if is_prime(n):
            return n
        while True:
            c = random.randrange(1, n)
            f = lambda x: (mulmod(x, x, n) + c) % n
            x, y, d = 2, 2, 1
            while d == 1:
                x = f(x)
                y = f(f(y))
                d = gcd(abs(x - y), n)
            if d != n:
                return d

    # 재귀를 반복문으로 변경하여 소인수분해 수행
    stack = [n]
    while stack:
        num = stack.pop()
        if num == 1:
            continue
        if is_prime(num):
            factors[num] = factors.get(num, 0) + 1
            continue
        factor = pollards_rho(num)
        if factor == num:
            # 소인수분해 실패 시 소수로 간주
            factors[num] = factors.get(num, 0) + 1
            continue
        stack.append(factor)
        stack.append(num // factor)

    result = original_n
    for p in factors:
        result = result // p * (p - 1)
    print(result)

if __name__ == "__main__":
    main()
```

### 코드 설명

1. **입력 받기**:
   - `n = int(sys.stdin.readline())`로 자연수 \( n \)을 입력받는다.

2. **소인수분해**:
   - 스택 `stack`을 사용하여 반복적으로 소인수분해를 수행한다.
   - 소인수는 딕셔너리 `factors`에 저장된다.

3. **오일러 피 함수 계산**:
   - 각 소인수 \( p \)에 대해 \( result = result \times (1 - \frac{1}{p}) \)를 계산한다.

4. **결과 출력**:
   - 계산된 \( result \)를 출력한다.

### 주요 함수 설명

- **gcd(a, b)**: 최대공약수를 구하는 함수이다.
- **mulmod(a, b, mod)**: 모듈러 곱셈을 수행한다.
- **powmod(a, b, mod)**: 모듈러 거듭제곱을 계산한다.
- **is_prime(n)**: Miller-Rabin 알고리즘을 사용하여 소수 판정을 한다.
- **pollards_rho(n)**: Pollard's Rho 알고리즘을 사용하여 소인수를 찾는다.

### 최적화 및 메모리 초과 방지

- **재귀 제거**: 재귀 호출로 인한 메모리 사용 증가를 방지하기 위해 재귀를 반복문으로 변경하였다.
- **스택 사용**: 소인수분해를 위해 스택을 사용하여 메모리 사용을 최소화하였다.
- **메모리 사용 최적화**: 불필요한 변수와 데이터를 최소화하여 메모리 효율을 높였다.

## 결론

이번 문제는 큰 수의 범위에서 \( n \)과 서로소인 수의 개수를 구해야 하는 정수론 문제로, 효율적인 알고리즘이 필요하였다. 오일러 피 함수를 활용하여 문제를 간단하게 해결할 수 있었으며, 소인수분해를 위해 Pollard's Rho 알고리즘과 Miller-Rabin 소수 판정 알고리즘을 사용하였다.

이 과정에서 큰 수 연산과 모듈러 연산을 다루는 방법을 익힐 수 있었으며, 알고리즘의 최적화와 구현상의 주의점을 배울 수 있었다. 특히, 파이썬에서 재귀를 반복문으로 변경하여 메모리 초과를 방지하는 등 메모리 관리의 중요성을 깨달았다.

추가적으로, C++ 표준 라이브러리를 사용하지 않고도 문제를 해결하는 방법과 파이썬에서의 최적화 기법도 살펴보았다. 이러한 다양한 접근 방식을 통해 알고리즘 문제 해결 능력을 향상시킬 수 있었다.