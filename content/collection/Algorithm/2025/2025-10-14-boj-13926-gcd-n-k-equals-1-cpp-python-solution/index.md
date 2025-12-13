---
title: "[Algorithm] C++/Python 백준 13926 gcd(n, k) = 1 — φ(n) 계산"
description: "자연수 n(≤10^18)에 대해 gcd(n, k) = 1인 1 ≤ k ≤ n의 개수, 즉 오일러 파이 함수 φ(n)를 구합니다. Miller–Rabin 소수판정과 Pollard Rho를 이용해 64비트 범위를 빠르게 소인수분해하고, φ(n)=n∏(1−1/p) 공식을 적용합니다."
date: 2025-10-14
lastmod: 2025-10-14
categories:
  - Algorithm
  - Number Theory
  - Math
  - BOJ
  - Problem Solving
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Baekjoon
  - Problem-13926
  - gcd
  - 최대공약수
  - Coprime
  - 서로소
  - Euler Totient Function
  - 오일러 파이 함수
  - EulerPhi
  - Totient
  - Number Theory
  - 정수론
  - Prime Factorization
  - 소인수분해
  - Miller Rabin
  - 밀러라빈
  - Pollard Rho
  - 폴라드 로
  - Modular Arithmetic
  - 모듈러 연산
  - Fast Power
  - 거듭제곱 빠른 제곱
  - 64-bit Integer
  - 64비트 정수
  - int64
  - long long
  - Performance
  - 성능최적화
  - Complexity
  - 시간복잡도
  - Space
  - 공간복잡도
  - C++
  - CPP
  - Python
  - 파이썬
  - Implementation
  - 구현
  - Math Problem
  - 수학 문제
  - Inclusion Exclusion
  - 포함배제
  - Multiplicative Function
  - 곱셈적 함수
  - Prime
  - 소수
  - Factorization
  - 분해
  - Deterministic
  - 결정론적
  - Randomized
  - 난수
  - Overflow Safe
  - 오버플로 방지
  - Big-O
  - O(sqrt n)
  - O(log n)
  - Edge Cases
  - 코너 케이스
  - Tutorial
  - 풀이
  - 해설
  - Sample Code
image: "wordcloud.png"
---

## 문제

- 문제: `gcd(n, k) = 1` (BOJ 13926)
- 링크: [`https://www.acmicpc.net/problem/13926`](https://www.acmicpc.net/problem/13926)
- 설명: 자연수 n이 주어졌을 때, gcd(n, k) = 1을 만족하는 1 ≤ k ≤ n의 개수를 구합니다. 이는 오일러 파이 함수 φ(n)입니다.
- 제한: 1 ≤ n ≤ 10^18, 시간 2초, 메모리 512MB

## 아이디어

- φ(n) = n × ∏(1 − 1/p) (p는 n의 서로 다른 소인수)
- 10^18까지 처리하려면 빠른 소인수분해가 필요합니다 → Miller–Rabin(64비트 결정론 세트) + Pollard Rho
- 분해된 서로 다른 소인수 집합을 이용하여 φ(n)을 계산합니다.

## 복잡도

- 소수 판정/분해: 보통 빠름 (경우에 따라 준선형), 구현상 평균적으로 10^18 범위에서도 충분
- 메모리: O(log n) 수준

## 정답 코드

### C++

```cpp
// 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;
using u128 = unsigned __int128;
using u64 = unsigned long long;
using u32 = unsigned int;

static inline u64 mul_mod(u64 a, u64 b, u64 m) {
    return (u128)a * b % m;
}

static inline u64 pow_mod(u64 a, u64 e, u64 m) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mul_mod(r, a, m);
        a = mul_mod(a, a, m);
        e >>= 1;
    }
    return r;
}

static bool is_prime(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ull,3ull,5ull,7ull,11ull,13ull,17ull,19ull,23ull,29ull,31ull,37ull}) {
        if (n % p == 0) return n == p;
    }
    u64 d = n - 1, s = 0;
    while ((d & 1) == 0) { d >>= 1; ++s; }
    // Deterministic bases for 64-bit
    for (u64 a : {2ull, 325ull, 9375ull, 28178ull, 450775ull, 9780504ull, 1795265022ull}) {
        if (a % n == 0) continue;
        u64 x = pow_mod(a % n, d, n);
        if (x == 1 || x == n - 1) continue;
        bool comp = true;
        for (u64 r = 1; r < s; ++r) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { comp = false; break; }
        }
        if (comp) return false;
    }
    return true;
}

static u64 rho(u64 n) {
    if ((n & 1ull) == 0) return 2;
    std::mt19937_64 rng((u64)chrono::high_resolution_clock::now().time_since_epoch().count());
    while (true) {
        u64 c = (rng() % (n - 2)) + 1;
        u64 x = (rng() % (n - 2)) + 2;
        u64 y = x;
        u64 d = 1;
        auto f = [&](u64 v){ return (mul_mod(v, v, n) + c) % n; };
        while (d == 1) {
            x = f(x);
            y = f(f(y));
            u64 diff = x > y ? x - y : y - x;
            d = std::gcd(diff, n);
        }
        if (d != n) return d;
    }
}

static void factor(u64 n, vector<u64>& fac) {
    if (n == 1) return;
    if (is_prime(n)) { fac.push_back(n); return; }
    u64 d = rho(n);
    factor(d, fac);
    factor(n / d, fac);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    unsigned long long n; if (!(cin >> n)) return 0;
    if (n == 0) { cout << 0 << '\n'; return 0; }
    if (n == 1) { cout << 1 << '\n'; return 0; }

    vector<u64> fac; fac.reserve(64);
    factor(n, fac);
    sort(fac.begin(), fac.end());
    fac.erase(unique(fac.begin(), fac.end()), fac.end());

    __int128 phi = n;
    for (u64 p : fac) {
        phi = phi / p * (p - 1);
    }
    unsigned long long ans = (unsigned long long)phi;
    cout << ans << '\n';
    return 0;
}
```

### Python

```python
# 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
import sys
import random
from math import gcd

def mul_mod(a, b, mod):
    return (a * b) % mod

def pow_mod(a, e, mod):
    r = 1
    a %= mod
    while e:
        if e & 1:
            r = (r * a) % mod
        a = (a * a) % mod
        e >>= 1
    return r

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0:
            continue
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        comp = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                comp = False
                break
        if comp:
            return False
    return True

def rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(2, n - 1)
        y = x
        d = 1
        def f(v):
            return (v * v + c) % n
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n: int, fac: list):
    if n == 1:
        return
    if is_prime(n):
        fac.append(n)
        return
    d = rho(n)
    factor(d, fac)
    factor(n // d, fac)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    if n == 0:
        print(0)
        return
    if n == 1:
        print(1)
        return
    fac = []
    factor(n, fac)
    fac = sorted(set(fac))
    phi = n
    for p in fac:
        phi = phi // p * (p - 1)
    print(phi)

if __name__ == "__main__":
    main()
```

## 코너 케이스

- n = 1 → φ(1) = 1
- n이 소수 → φ(n) = n − 1
- n이 소수 거듭제곱 p^k → φ(n) = n − n/p
- 서로 다른 소인수가 많은 합성수 → 모든 서로 다른 소인수만 반영

## 참고

- φ(n) 공식: n × ∏(1 − 1/p)
- Miller–Rabin 64비트 결정론적 기반 집합 사용
- Pollard Rho 난수 시드에 따라 재시도 가능
