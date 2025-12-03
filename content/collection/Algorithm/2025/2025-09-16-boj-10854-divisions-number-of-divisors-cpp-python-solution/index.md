---
title: "[Algorithm] C++/Python 백준 10854번: Divisions - 약수 개수"
description: "N(≤1e18)의 양의 약수 개수를 구하는 문제입니다. N을 소인수분해한 뒤 (지수+1)의 곱으로 약수 개수를 계산합니다. Pollard's Rho + Miller–Rabin을 이용해 64비트 범위를 안정적으로 처리하고, 오버플로·64비트 연산·N=1 등 엣지 케이스를 점검합니다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- Algorithm
- Math
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-10854
- cpp-python
- C++
- Python
- Data Structures
- 자료구조
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Math
- 수학
- Number Theory
- 정수론
- Divisors
- 약수
- Divisor Function
- 약수함수
- tau(n)
- Factorization
- 소인수분해
- Pollard Rho
- 폴라드로
- Miller Rabin
- 밀러라빈
- Primality Test
- 소수판정
- Modular Arithmetic
- 모듈러연산
- 64-bit
- 64비트
- __int128
- unsigned__int128
- Fast Power
- 빠른 거듭제곱
- GCD
- 최대공약수
- Randomized
- 무작위화
- Deterministic
- 결정론적
- Overflow
- 오버플로
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제 정보
- 문제: `https://www.acmicpc.net/problem/10854`
- 요약: 하나의 정수 N(1 ≤ N ≤ 10^18)이 주어질 때, N을 어떤 양의 정수 d로 나누었을 때 나누어떨어지는 모든 양의 정수 d의 개수, 즉 N의 양의 약수 개수 τ(N)를 출력합니다.
- 제한/스펙: 시간 1초, 메모리 256MB. 입력은 단일 정수 N. 64비트 정수 범위이므로 일반적인 체나 완전 탐색은 비현실적이며 빠른 소인수분해가 필요합니다.

## 입출력 형식/예제
- 입력: 한 줄에 N
- 출력: N의 양의 약수 개수

예제 1
```
입력
12

출력
6
```

예제 2
```
입력
999999999999999989

출력
2
```

예제 3
```
입력
100000007700000049

출력
4
```

## 접근 개요(아이디어 스케치)
- 소인수분해 관찰: \(N = \prod p_i^{e_i}\)이면 약수 개수 \(\tau(N) = \prod (e_i + 1)\).
- 64비트 정수 N에 대해 결정론적 Miller–Rabin 소수 판정과 Pollard's Rho 랜덤화 인수분해를 사용하면 1e18 범위를 매우 빠르게 분해 가능합니다.
- 분해된 소인수들을 정렬해 지수별로 묶고, (지수+1)을 곱해 답을 구합니다. N=1인 경우 결과는 1입니다.

```mermaid
flowchart TD
  A[입력 N] --> B{N == 1?}
  B -- 예 --> C[정답 1]
  B -- 아니오 --> D[분해: factor(N)]
  D --> E[소인수 목록 정렬]
  E --> F[(연속 같은 소인수 개수 = 지수)]
  F --> G[(답 *= (지수+1))]
  G --> H[출력]
```

## 알고리즘 설계
- 소수 판정(Miller–Rabin, 64-bit): 몇 개의 고정 밑(예: 2,3,5,7,11,13,17)에 대해 거듭제곱 모듈러 연산으로 합성수 여부를 검사. 64비트 범위에서 결정론적으로 동작하는 알려진 밑을 사용.
- 인수분해(Pollard's Rho): \(f(x) = x^2 + c \bmod n\) 순열에서 사이클을 빠르게 찾아 비자명한 약수 \(\gcd(|x-y|, n)\)를 얻음. 재귀적으로 분해.
- 구현 포인트:
  - 곱셈 모듈러는 C++에서 `__int128`, Python에서 내장 큰정수 사용.
  - 난수 시드/상수 c를 바꿔 충돌을 피함. d==n이면 재시도.
  - 분해 결과를 벡터에 담아 정렬하고, 구간 길이로 지수 계산.
  - 오버플로 방지: 곱셈 모듈러와 128비트 사용.

의사코드
```
if N == 1: return 1
fs = factor(N)            # Pollard's Rho + Miller–Rabin
sort(fs)
ans = 1
for 각 서로 같은 소인수 구간 길이 len:
    ans *= (len + 1)
print(ans)
```

## 복잡도
- 기대 시간: 대략 \(\tilde{O}(N^{1/4})\) 수준(실전에서는 1e18도 수 ms~수십 ms 내외). 소수 판정은 \(O(\log N)\) 거듭제곱 모듈러 반복.
- 공간: 분해 결과 저장에 \(O(k)\) (소인수 개수 k), 재귀 스택은 매우 얕음.

## 구현

### C++17 구현
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using u128 = __uint128_t;
using u64 = unsigned long long;

u64 mul_mod(u64 a, u64 b, u64 mod) {
    return (u128)a * b % mod;
}

u64 pow_mod(u64 a, u64 d, u64 mod) {
    u64 r = 1;
    while (d) {
        if (d & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        d >>= 1;
    }
    return r;
}

bool isPrime(u64 n) {
    if (n < 2) return false;
    static const u64 small_primes[] = {2,3,5,7,11,13,17,19,23,0};
    for (int i = 0; small_primes[i]; ++i) {
        if (n % small_primes[i] == 0) return n == small_primes[i];
    }

    u64 d = n - 1, s = 0;
    while ((d & 1) == 0) { d >>= 1; ++s; }

    static const u64 bases[] = {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 0ULL};
    for (int i = 0; bases[i]; ++i) {
        u64 a = bases[i];
        if (a % n == 0) continue;
        u64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool witness = true;
        for (u64 r = 1; r < s; ++r) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { witness = false; break; }
        }
        if (witness) return false;
    }
    return true;
}

u64 gcd_u64(u64 a, u64 b) {
    while (b) {
        u64 t = a % b;
        a = b; b = t;
    }
    return a;
}

u64 pollard(u64 n) {
    if ((n & 1ULL) == 0ULL) return 2ULL;
    static std::mt19937_64 rng((u64)chrono::steady_clock::now().time_since_epoch().count());
    uniform_int_distribution<u64> dist(2ULL, n - 2ULL);

    while (true) {
        u64 c = dist(rng);
        u64 x = dist(rng);
        u64 y = x;
        u64 d = 1;

        auto f = [&](u64 v) -> u64 {
            u64 t = mul_mod(v, v, n);
            t += c;
            if (t >= n) t -= n;
            return t;
        };

        while (d == 1) {
            x = f(x);
            y = f(f(y));
            u64 diff = x > y ? x - y : y - x;
            d = gcd_u64(diff, n);
        }
        if (d != n) return d;
    }
}

void factor(u64 n, vector<u64>& fac) {
    if (n == 1) return;
    if (isPrime(n)) { fac.push_back(n); return; }
    u64 d = pollard(n);
    factor(d, fac);
    factor(n / d, fac);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    u64 N;
    if (!(cin >> N)) return 0;

    if (N == 1) {
        cout << 1 << '\n';
        return 0;
    }

    vector<u64> fs;
    factor(N, fs);
    sort(fs.begin(), fs.end());

    unsigned __int128 ans = 1;
    for (size_t i = 0; i < fs.size();) {
        size_t j = i;
        while (j < fs.size() && fs[j] == fs[i]) ++j;
        ans *= (unsigned __int128)(j - i + 1);
        i = j;
    }

    unsigned long long out = (unsigned long long)ans;
    cout << out << '\n';
    return 0;
}
```

### Python3 구현
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys, random, math

def mul_mod(a: int, b: int, mod: int) -> int:
    return (a * b) % mod

def pow_mod(a: int, d: int, mod: int) -> int:
    return pow(a, d, mod)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    bases = [2, 3, 5, 7, 11, 13, 17]
    for a in bases:
        if a % n == 0:
            continue
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        witness = True
        for _ in range(1, s):
            x = mul_mod(x, x, n)
            if x == n - 1:
                witness = False
                break
        if witness:
            return False
    return True

def pollard(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(2, n - 1)
        x = random.randrange(2, n - 1)
        y = x
        d = 1
        def f(v: int) -> int:
            return (mul_mod(v, v, n) + c) % n
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n: int, acc: list):
    if n == 1:
        return
    if is_prime(n):
        acc.append(n)
        return
    d = pollard(n)
    factor(d, acc)
    factor(n // d, acc)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    if N == 1:
        print(1)
        return
    fs = []
    factor(N, fs)
    fs.sort()
    ans = 1
    i = 0
    while i < len(fs):
        j = i
        while j < len(fs) and fs[j] == fs[i]:
            j += 1
        ans *= (j - i + 1)
        i = j
    print(ans)

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- N=1 → 답 1
- N이 소수 → 답 2
- N이 거듭제곱(예: p^k) → 답 k+1
- N=p·q (p≈q≈1e9) → 분해 성공 여부와 시간
- 2의 거듭제곱, 큰 소인수 하나 + 작은 소인수들, 반복 소인수
- 우발적 충돌(ρ 함수 재시도 필요), 64비트 곱 모듈러 오버플로

## 제출 전 점검
- 표준 입출력/개행 형식 엄수
- 64비트 정수 범위 사용, C++은 `__int128` 기반 곱셈 모듈러
- 난수/상수 c 변경 로직 존재(충돌 시 재시도)
- 분해 결과 정렬 후 (지수+1) 곱 정확

## 참고자료/유사문제
- Miller–Rabin primality test (위키)
- Pollard's Rho integer factorization (위키)

