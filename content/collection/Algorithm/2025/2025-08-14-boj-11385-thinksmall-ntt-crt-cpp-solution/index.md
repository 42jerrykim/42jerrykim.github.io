---
title: "[Algorithm] C++ 백준 11385번: 씽크스몰 - NTT+CRT 다항식 곱셈"
description: "NTT 친화 소수 3개에서 다항식 곱셈을 수행하고 CRT로 계수를 복원해 모든 계수의 XOR을 계산합니다. N, M ≤ 1e6의 대용량 입력을 O(n log n) 시간과 선형 메모리로 안정 처리하며, 오버플로는 __int128로 방지합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Math
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-11385
- cpp
- C++
- Polynomial Multiplication
- 다항식 곱셈
- NTT
- Number Theoretic Transform
- 수론적 변환
- FFT
- Fast Fourier Transform
- Convolution
- 컨볼루션
- CRT
- Chinese Remainder Theorem
- 중국인의 나머지 정리
- Garner
- 가너 알고리즘
- Modular Arithmetic
- 모듈러 연산
- Modular Inverse
- 모듈러 역원
- Primitive Root
- 원시근
- Bit-reversal
- 비트 반전
- Iterative NTT
- 반복 NTT
- Power of Two
- 2의 거듭제곱
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Competitive Programming
- 경쟁프로그래밍
- Testing
- 테스트
- Template
- 템플릿
- 64-bit
- 64비트
- __int128
- 오버플로 방지
- XOR
- 배타적 논리합
- Large Input
- 대용량 입력
- IO Optimization
- 입출력 최적화
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11385
- 요약: 두 다항식 f(x), g(x)의 곱 h(x)=f(x)×g(x)를 구할 때, 모든 계수 c[0..L]을 출력하는 대신 `c[0] ⊕ c[1] ⊕ ... ⊕ c[L]`의 값을 출력한다. N, M ≤ 1,000,000, 계수 ≤ 1,000,000.
- 제한/스펙: 시간 10초, 메모리 512MB. 순수 O(NM)은 불가 → 고속 컨볼루션 필요.

## 입력/출력
```
입력
N M
a0 a1 ... aN
b0 b1 ... bM

출력
c0 ⊕ c1 ⊕ ... ⊕ cL (L=N+M)
```

예시(문제 본문)
```
입력
1 1
1 2
3 2

출력
15
```

## 접근 개요
- 핵심: 큰 정수 계수 다항식의 곱을 빠르게 계산하려면 FFT/NTT 기반 컨볼루션을 사용한다. 정수 정밀도 보장을 위해 NTT 친화 소수(prime) 3개에서 각각 컨볼루션을 수행한 뒤 CRT로 실제 정수를 복원한다.
- 소수 선택: 167772161, 469762049, 1224736769 (모두 3이 원시근이며 2^k로 나누어떨어지는 φ(p)). 각 소수 모듈러에서 NTT로 O(n log n) 컨볼루션.
- 복원: 각 위치 i에 대해 (r0, r1, r2)를 CRT로 결합해 실제 계수 ci(64-bit 내)로 만들고, 모든 ci를 XOR.
- 수치 안정성: N, M ≤ 1e6에서 n을 다음 2의 거듭제곱으로 올림. 세 모듈러에서의 결과 범위와 입력 상한을 고려해 최종 계수는 64-bit에 안전. 중간 계산에는 `__int128` 사용.

## 알고리즘 설계
- 단계
  1) 길이 n을 (N+M+1) 이상이 되는 최소 2의 거듭제곱으로 설정.
  2) 각 모듈러 p∈{167772161, 469762049, 1224736769}에 대해 NTT 전/후 처리로 컨볼루션을 수행하여 r_p[0..L] 획득.
  3) Garner/CRT로 x ≡ r0 (mod M0), x ≡ r1 (mod M1), x ≡ r2 (mod M2)의 해 x를 구함.
  4) 누적 XOR에 x를 반영.
- 구현 포인트
  - 비트 반전(bitreverse) 순서와 단계별 원시근 거듭제곱 프리컴퓨팅.
  - 역변환 시 1/n의 모듈러 역원 곱 적용.
  - CRT는 (M0, M1)→x01 결합 후, (x01, M2)로 확장하는 2단계로 구현. 역원은 거듭제곱으로 계산.
  - I/O 가속과 벡터 재사용으로 메모리/시간 최적화.

## 복잡도
- 시간: O(3·n log n) = O(n log n)
- 공간: O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using u32 = uint32_t;
using u64 = uint64_t;
using i64 = long long;
using i128 = __int128_t;
using u128 = __uint128_t;

template<u32 MOD, u32 PRIM_ROOT>
struct NTT {
    static u32 modpow(u32 a, u32 e) {
        u64 r = 1, x = a;
        while (e) {
            if (e & 1) r = (r * x) % MOD;
            x = (x * x) % MOD;
            e >>= 1;
        }
        return (u32)r;
    }
    static void ntt(vector<u32> &a, bool invert) {
        int n = (int)a.size();
        for (int i = 1, j = 0; i < n; i++) {
            int bit = n >> 1;
            for (; j & bit; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) swap(a[i], a[j]);
        }
        for (int len = 2; len <= n; len <<= 1) {
            u32 wlen = modpow(PRIM_ROOT, (MOD - 1) / len);
            if (invert) wlen = modpow(wlen, MOD - 2);
            for (int i = 0; i < n; i += len) {
                u32 w = 1;
                int half = len >> 1;
                for (int j = 0; j < half; j++) {
                    u32 u = a[i + j];
                    u32 v = (u64)a[i + j + half] * w % MOD;
                    u32 t = u + v;
                    a[i + j] = t >= MOD ? t - MOD : t;
                    u32 t2 = u >= v ? u - v : u + MOD - v;
                    a[i + j + half] = t2;
                    w = (u64)w * wlen % MOD;
                }
            }
        }
        if (invert) {
            u32 inv_n = modpow((u32)n, MOD - 2);
            for (int i = 0; i < n; i++) a[i] = (u64)a[i] * inv_n % MOD;
        }
    }
    static void convolution(const vector<u32>& A, const vector<u32>& B, vector<u32>& out, int need) {
        int n = 1;
        while (n < need) n <<= 1;
        vector<u32> fa(n, 0), fb(n, 0);
        for (int i = 0; i < (int)A.size(); i++) fa[i] = A[i] % MOD;
        for (int i = 0; i < (int)B.size(); i++) fb[i] = B[i] % MOD;
        ntt(fa, false); ntt(fb, false);
        for (int i = 0; i < n; i++) fa[i] = (u64)fa[i] * fb[i] % MOD;
        ntt(fa, true);
        out.assign(need, 0);
        for (int i = 0; i < need; i++) out[i] = fa[i];
    }
};

static inline u64 mod_pow_u64(u64 a, u64 e, u64 mod) {
    u128 r = 1, x = a % mod;
    while (e) {
        if (e & 1) r = (r * x) % mod;
        x = (x * x) % mod;
        e >>= 1;
    }
    return (u64)r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) return 0;
    int na = N + 1, nb = M + 1;
    vector<u32> A(na), B(nb);
    for (int i = 0; i < na; i++) cin >> A[i];
    for (int j = 0; j < nb; j++) cin >> B[j];
    int need = na + nb - 1;

    const u64 M0 = 167772161ULL;     // primitive root 3
    const u64 M1 = 469762049ULL;     // primitive root 3
    const u64 M2 = 1224736769ULL;    // primitive root 3

    vector<u32> c0, c1, c2;
    NTT<(u32)167772161, 3>::convolution(A, B, c0, need);
    NTT<(u32)469762049, 3>::convolution(A, B, c1, need);
    NTT<(u32)1224736769, 3>::convolution(A, B, c2, need);

    const u64 inv_M0_mod_M1 = mod_pow_u64(M0 % M1, M1 - 2, M1);
    const u64 M01 = M0 * M1;
    const u64 inv_M01_mod_M2 = mod_pow_u64((u64)((u128)M01 % M2), M2 - 2, M2);

    unsigned long long ans = 0ULL;
    for (int i = 0; i < need; i++) {
        u64 r0 = c0[i];
        u64 r1 = c1[i];
        u64 r2 = c2[i];

        u64 t1 = (r1 + M1 - (r0 % M1)) % M1;
        t1 = (u64)((u128)t1 * inv_M0_mod_M1 % M1);
        u128 x01 = (u128)r0 + (u128)M0 * t1; // modulo M0*M1

        u64 x01_mod_M2 = (u64)((x01 % M2 + M2) % M2);
        u64 t2 = (r2 + M2 - x01_mod_M2) % M2;
        t2 = (u64)((u128)t2 * inv_M01_mod_M2 % M2);

        u128 x = x01 + (u128)M01 * t2; // exact integer coefficient
        u64 coeff = (u64)x;
        ans ^= (unsigned long long)coeff;
    }
    cout << ans << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- N=1 또는 M=1: 패딩/NTT 길이 결정이 최소 2의 거듭제곱으로 올바르게 처리되는지 확인.
- 모든 계수=1: 정수 범위 상한 근처에서 XOR 누적이 정상 동작하는지.
- 큰 길이(N,M≈1e6): I/O 가속, 메모리 초기화 비용 최소화, 불필요한 복사를 피함.
- 홀수 길이/비대칭 차수: need=N+M+1과 패딩 길이 n 계산 정확성.

## 제출 전 점검
- 변환 길이 n은 (N+M+1) 이상의 2의 거듭제곱인지.
- 역NTT에서 1/n의 모듈러 역원을 곱했는지.
- CRT 역원/곱에서 128-bit 중간 유형을 사용했는지.
- 입출력: `ios::sync_with_stdio(false); cin.tie(nullptr);` 적용.

## 참고자료
- NTT-friendly primes: 167772161, 469762049, 1224736769 (primitive root 3)
- CP-Algorithms: Number Theoretic Transform, Chinese Remainder Theorem


