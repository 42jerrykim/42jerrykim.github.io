---
title: "[Algorithm] BOJ 13725 - RNG C++ 풀이 - Bostan–Mori+NTT"
description: "선형 점화식 A_i = \u2211 A_{i-j}\u00B7C_j (mod 104857601)를 Bostan–Mori와 NTT로 O(k log k log N)에 계산합니다. 2^22\u00B75^2+1 소수 모듈러에서 다항식 곱셈으로 A_N을 빠르고 안정적으로 구하는 C++ 정답과 구현 포인트를 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "13725"
- "RNG"
- "Random Number Generator"
- "선형 점화식"
- "Linear Recurrence"
- "Bostan–Mori"
- "Bostan Mori"
- "NTT"
- "Number Theoretic Transform"
- "NTT Convolution"
- "Convolution"
- "Polynomial"
- "Polynomial Multiplication"
- "다항식"
- "다항식 곱셈"
- "Generating Function"
- "생성함수"
- "Formal Power Series"
- "형식적 멱급수"
- "Fast Power Series"
- "분할 정복"
- "Divide and Conquer"
- "이진 승법"
- "빠른 거듭제곱"
- "Powmod"
- "modinv"
- "Modular Inverse"
- "Modular Arithmetic"
- "모듈러 연산"
- "Prime Modulo"
- "104857601"
- "Primitive Root"
- "원시근"
- "FFT prime"
- "2^22*5^2+1"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Algorithm"
- "알고리즘"
- "Competitive Programming"
- "코딩테스트"
- "Problem Solving"
- "문제풀이"
- "시간복잡도"
- "Time Complexity"
- "O(k log k log N)"
- "K up to 30000"
- "N up to 1e18"
- "Optimization"
- "최적화"
- "Implementation"
- "구현"
- "정답 코드"
- "Solution Code"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 13725 - RNG](https://www.acmicpc.net/problem/13725)

### 아이디어 요약
- 목표: 선형 점화식 \(A_i = \sum_{j=1}^{k} C_j A_{i-j} \pmod{104857601}\)의 \(A_N\)을 \(k \le 3\times10^4\), \(N \le 10^{18}\)에서 계산.
- 생성함수 관점에서 \(A(x) = \sum a_i x^i = P(x)/Q(x)\), \(Q(x)=1-\sum_{j=1}^k C_j x^j\), \(\deg P < \deg Q\).
- Bostan–Mori: \([x^n] P/Q\)를 짝/홀 분리와 \(Q(-x)\)를 이용해 \(n\)을 절반씩 줄이며 구함. 한 단계당 다항식 곱셈 2회.
- 모듈러 104857601은 \(2^{22}\cdot 5^2+1\) 형태의 소수로 NTT 기반 다항식 곱셈이 가능. 전체 복잡도 \(O(k \log k \log N)\).
- 인덱스는 입력이 1-based이므로 최종 목표는 \(n = N-1\)의 계수.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 104857601; // prime

inline int addmod(int a, int b) {
    int s = a + b;
    if (s >= MOD) s -= MOD;
    return s;
}
inline int submod(int a, int b) {
    int s = a - b;
    if (s < 0) s += MOD;
    return s;
}
int modpow(int a, long long e) {
    long long r = 1, x = a;
    while (e > 0) {
        if (e & 1) r = (r * x) % MOD;
        x = (x * x) % MOD;
        e >>= 1;
    }
    return (int)r;
}
int modinv(int a) { return modpow(a, MOD - 2); }

// Find primitive root of MOD (MOD prime), using prime factors of MOD-1 = 2^22 * 5^2
int primitive_root() {
    int phi = MOD - 1;
    vector<int> primes = {2, 5};
    for (int g = 2;; ++g) {
        bool ok = true;
        for (int p : primes) if (modpow(g, phi / p) == 1) { ok = false; break; }
        if (ok) return g;
    }
}

void ntt(vector<int> &a, bool invert) {
    int n = (int)a.size();
    static int g = -1;
    if (g == -1) g = primitive_root();

    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j |= bit;
        if (i < j) swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        int wlen = modpow(g, (MOD - 1) / len);
        if (invert) wlen = modinv(wlen);
        for (int i = 0; i < n; i += len) {
            long long w = 1;
            int half = len >> 1;
            for (int j = 0; j < half; ++j) {
                int u = a[i + j];
                int v = int((w * a[i + j + half]) % MOD);
                int x = u + v; if (x >= MOD) x -= MOD;
                int y = u - v; if (y < 0) y += MOD;
                a[i + j] = x;
                a[i + j + half] = y;
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        int inv_n = modinv(n);
        for (int &x : a) x = int((1LL * x * inv_n) % MOD);
    }
}

vector<int> convolution(const vector<int> &a, const vector<int> &b) {
    if (a.empty() || b.empty()) return {};
    int need = (int)a.size() + (int)b.size() - 1;
    int n = 1; while (n < need) n <<= 1;
    vector<int> fa(n, 0), fb(n, 0);
    for (int i = 0; i < (int)a.size(); ++i) fa[i] = a[i];
    for (int i = 0; i < (int)b.size(); ++i) fb[i] = b[i];
    ntt(fa, false); ntt(fb, false);
    for (int i = 0; i < n; ++i) fa[i] = int((1LL * fa[i] * fb[i]) % MOD);
    ntt(fa, true);
    fa.resize(need);
    return fa;
}

// Bostan–Mori: compute coefficient [x^n] of P(x)/Q(x), with deg P < deg Q, Q[0] != 0
int bostan_mori(vector<int> P, vector<int> Q, long long n) {
    while (n > 0) {
        vector<int> Qm(Q.size());
        for (int i = 0; i < (int)Q.size(); ++i) Qm[i] = (i & 1) ? (MOD - Q[i]) % MOD : Q[i];
        vector<int> S = convolution(Q, Qm); // Q * Q(-x)
        vector<int> R = convolution(P, Qm); // P * Q(-x)
        vector<int> Qn((S.size() + 1) >> 1);
        for (int i = 0; i < (int)Qn.size(); ++i) Qn[i] = S[i << 1];
        vector<int> Pn;
        if ((n & 1) == 0) {
            Pn.resize((R.size() + 1) >> 1);
            for (int i = 0; i < (int)Pn.size(); ++i) Pn[i] = R[i << 1];
        } else {
            Pn.resize(R.size() >> 1);
            for (int i = 0; i < (int)Pn.size(); ++i) Pn[i] = R[(i << 1) + 1];
        }
        P.swap(Pn); Q.swap(Qn); n >>= 1;
    }
    return int(1LL * P[0] * modinv(Q[0]) % MOD);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k; long long N;
    if (!(cin >> k >> N)) return 0;
    vector<int> A(k), C(k);
    for (int i = 0; i < k; ++i) { long long x; cin >> x; A[i] = int(x % MOD); }
    for (int i = 0; i < k; ++i) { long long x; cin >> x; C[i] = int(x % MOD); }

    if (N <= k) { cout << A[N - 1] % MOD << '\n'; return 0; }

    // Q(x) = 1 - c1 x - c2 x^2 - ... - ck x^k
    vector<int> Q(k + 1, 0); Q[0] = 1;
    for (int i = 1; i <= k; ++i) Q[i] = (MOD - C[i - 1]) % MOD;

    // P[n] = a_n - sum_{i=1..min(n,k)} c_i * a_{n-i}
    vector<int> P(k, 0);
    for (int n = 0; n < k; ++n) {
        long long val = A[n];
        for (int i = 1; i <= n && i <= k; ++i) {
            val -= 1LL * C[i - 1] * A[n - i] % MOD;
            if (val < 0) val += MOD;
        }
        P[n] = int(val % MOD);
    }

    long long target = N - 1; // 1-based to 0-based index
    int ans = bostan_mori(P, Q, target);
    cout << ans << '\n';
    return 0;
}
```

### 복잡도
- 시간: \(O(k \log k \log N)\) — 단계마다 NTT \(O(k \log k)\), 전체 \(\log N\) 단계.
- 공간: \(O(k)\) 다항식 벡터 3~4개.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 문제: `https://www.acmicpc.net/problem/13725`
- 키워드: Bostan–Mori, NTT, 선형 점화식, 생성함수


