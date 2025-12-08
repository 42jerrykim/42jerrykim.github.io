---
title: "[Algorithm] C++ 백준 2709번: 가장 작은 K"
description: "2^k의 마지막 R자리가 1과 2로만 구성되도록 하는 최소 지수를 찾는 문제입니다. 2^r와 5^r로 분리해 모듈러 순환을 추적하고, 주기 5배 성질을 활용한 후보 5개 탐색, CRT와 __int128으로 정확히 복원하는 O(R) 수학 풀이를 정리합니다."
date: 2025-12-08
lastmod: 2025-12-08
categories:
- Algorithm
- Number Theory
- Math
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-2709
- C++
- Number Theory
- 정수론
- Modular Arithmetic
- 모듈러 연산
- Chinese Remainder Theorem
- 중국인 나머지 정리
- Multiplicative Order
- 곱셈군
- Periodicity
- 주기
- Power of Two
- 2의 거듭제곱
- Last Digits
- 뒷자리
- Base 10
- 십진수
- CRT
- 모듈러 조합
- Fast Power
- 거듭제곱 분할정복
- Binary Exponentiation
- 이분 거듭제곱
- __int128
- 큰정수처리
- Overflow
- 오버플로
- Lifting Exponent
- 승수 리프트
- Candidate Search
- 후보 탐색
- Precomputation
- 전처리
- Complexity Analysis
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Case
- 엣지케이스
- Implementation
- 구현
- Math Proof
- 수학적 증명
- ICPC
- Greater New York
- Contest
- Problem Solving
- 문제해결
- Modular Period
- 순환 길이
- Residue Class
- 잔여 클래스
- Constraints Handling
- 제약 처리
image: "wordcloud.png"
---

## 문제 정보

**문제 링크**: [https://www.acmicpc.net/problem/2709](https://www.acmicpc.net/problem/2709)

**문제 요약**: $R(1 \le R \le 20)$이 주어질 때, $2^k$의 마지막 $R$자리가 1과 2로만 이루어지는 가장 작은 $k$를 찾는다. $T(1 \le T \le 50)$개의 테스트 케이스를 각각 처리한다.

**제한 조건**:
- 시간 제한: 1초
- 메모리 제한: 128MB
- 입력 크기: $1 \le R \le 20$, $1 \le T \le 50$

## 입출력 예제

**입력 1**:
```text
6
1
2
4
5
7
15
```

**출력 1**:
```text
1
9
89
589
3089
11687815589
```

## 접근 방식

### 핵심 관찰
1. $10^R = 2^R \cdot 5^R$이므로 모듈러를 두 부분으로 분리해 CRT로 재결합하면 큰 정수 없이 계산 가능하다.
2. $2$의 법 $5^r$에서의 위수는 $4 \cdot 5^{r-1}$이다. 자리수를 한 자리 늘릴 때 주기가 5배 커지므로 이전 답 $k_{r-1}$에 대해 $k_r$는 $k_{r-1} + t \cdot \text{ord}_{r-1}$ (0 ≤ t < 5) 중 하나만 확인하면 된다.
3. 각 후보 $k$마다 $2^k \bmod 2^r$, $2^k \bmod 5^r$를 빠른 거듭제곱으로 구한 뒤 CRT로 $2^k \bmod 10^r$를 복원하고, 하위 $R$자리가 모두 1 또는 2인지 검사한다.

### 알고리즘 설계 (Mermaid)

```mermaid
flowchart TD
    A[입력 T] --> B[각 테스트 R 수집, 최대 Rmax 계산]
    B --> C[ord[r]=4·5^(r-1) 전처리]
    C --> D[기저: k[1]=1]
    D --> E[r = 2..Rmax 반복]
    E --> F[step = ord[r-1], base = k[r-1]]
    F --> G{t = 0..4}
    G --> H[후보 cand = base + step*t]
    H --> I[mod2 = 2^cand mod 2^r]
    I --> J[mod5 = 2^cand mod 5^r]
    J --> K[CRT로 mod10 = 2^cand mod 10^r]
    K --> L{하위 r자리가 1/2?}
    L -- Yes --> M[k[r]=cand; break]
    L -- No --> G
    M --> N[모든 R 처리 후 질의별 k[R] 출력]
```

### 단계별 로직
1. **전처리**: $5^r$, $2^r$, 그리고 $2$의 법 $5^r$ 위수(순환 길이) $4 \cdot 5^{r-1}$을 $r=1..R_{\max}$까지 계산한다.
2. **답 테이블 구성**: $r=1$일 때 $k=1$. $r>1$에서는 이전 답 $k_{r-1}$을 기준으로 주기 크기만큼 5개 후보를 검사하며 처음으로 조건을 만족하는 $k_r$를 저장한다.
3. **CRT 복원**: $x \equiv a \pmod{2^r}$, $x \equiv b \pmod{5^r}$을 역원을 이용해 하나의 $x < 10^r$로 합친다.
4. **자리수 검사**: $x$의 하위 $r$자리를 확인해 1 또는 2만 포함되는지 체크한다.
5. **출력**: 테스트 케이스별로 미리 구한 $k[r]$을 O(1)로 반환한다.

## 복잡도 분석

| 항목 | 복잡도 | 비고 |
|---|---|---|
| **시간 복잡도** | $O(R_{\max} \cdot 5 \cdot \log 5^R)$ | 각 자리 증가마다 후보 5개, 모듈러 거듭제곱 |
| **공간 복잡도** | $O(R_{\max})$ | $k$, $5^r$, $2^r$, 위수 테이블 |

## 구현 코드

### C++

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;
using u128 = __int128_t;
using u64  = unsigned long long;

u64 mod_pow_u64(u64 a, u64 e, u64 mod) {
    u128 res = 1, base = a % mod;
    while (e) {
        if (e & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        e >>= 1;
    }
    return static_cast<u64>(res);
}

long long egcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) { x = 1; y = 0; return a; }
    long long x1, y1;
    long long g = egcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return g;
}

u64 mod_inv(u64 a, u64 mod) {
    long long x, y;
    egcd(static_cast<long long>(a), static_cast<long long>(mod), x, y);
    long long inv = (x % static_cast<long long>(mod) + static_cast<long long>(mod)) % static_cast<long long>(mod);
    return static_cast<u64>(inv);
}

// Combine x≡a (mod m1), x≡b (mod m2) with m1,m2 coprime
u128 crt(u64 a, u64 m1, u64 b, u64 m2) {
    u64 inv = mod_inv(m1 % m2, m2);
    u64 t = (u128((b + m2) - (a % m2)) * inv) % m2;
    return u128(a) + u128(m1) * t; // result < m1*m2
}

bool digits_ok(u128 x, int R) {
    for (int i = 0; i < R; ++i) {
        int d = int(x % 10);
        if (d != 1 && d != 2) return false;
        x /= 10;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    vector<int> R(T);
    int maxR = 0;
    for (int &r : R) { cin >> r; maxR = max(maxR, r); }

    vector<u64> pow5(maxR + 1, 1);
    for (int i = 1; i <= maxR; ++i) pow5[i] = pow5[i - 1] * 5ULL;

    vector<u64> ord(maxR + 1);
    ord[1] = 4;
    for (int i = 2; i <= maxR; ++i) ord[i] = ord[i - 1] * 5ULL;

    vector<u64> k(maxR + 1);
    k[1] = 1; // 2^1 = 2 -> 마지막 1자리가 2

    for (int r = 2; r <= maxR; ++r) {
        u64 step = ord[r - 1];   // 4 * 5^(r-2)
        u64 base = k[r - 1];
        u64 m1 = 1ULL << r;      // 2^r (r<=20)
        u64 m2 = pow5[r];        // 5^r (<= 9.5e13)

        u64 found = 0;
        for (int t = 0; t < 5; ++t) {  // 주기 5배 → 5개 후보만 검사
            u64 cand = base + step * static_cast<u64>(t);
            u64 a = mod_pow_u64(2, cand, m1);
            u64 b = mod_pow_u64(2, cand, m2);
            u128 x = crt(a, m1, b, m2); // x = 2^cand mod 10^r
            if (digits_ok(x, r)) { found = cand; break; }
        }
        k[r] = found;
    }

    for (int r : R) cout << k[r] << '\n';
    return 0;
}
```

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **R=1** | 기저 사례 | $k_1=1$로 초기화 |
| **최대 R=20** | $5^{20}$ 크기와 오버플로 | `__int128`으로 곱셈/모듈러 계산 |
| **모듈러 역원 계산** | $2^r$와 $5^r$은 서로소 | 확장 유클리드로 역원 계산 |
| **후보 없음** | 이론상 항상 존재 | 5개 후보 모두 검사 |
| **입력 다수(T)** | 중복 계산 방지 | $R_{\max}$까지 미리 DP 후 질의 응답 |

## 마무리

주기 확장 성질 덕분에 자리수를 한 칸 늘릴 때마다 단 5개 후보만 검사하면 되며, CRT로 10진 모듈러를 복원해 큰 정수 라이브러리 없이도 정확하게 답을 구할 수 있다.

