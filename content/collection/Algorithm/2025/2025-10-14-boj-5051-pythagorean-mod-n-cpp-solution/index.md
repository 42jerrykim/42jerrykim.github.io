---
title: "[Algorithm] C++ 백준 5051번: 피타고라스의 정리 (mod n)"
description: "1 ≤ a,b,c ≤ n−1, a ≤ b, a^2+b^2 ≡ c^2 (mod n) 조건을 만족하는 삼중쌍 개수를 O(n log n) FFT 기반 순환 컨볼루션으로 계산합니다. 제곱 나머지 분포를 자기 합성해 순서쌍을 집계하고, a=b 대각선 보정으로 a≤b 조건을 정확히 반영합니다."
date: 2025-10-14
lastmod: 2025-10-14
categories:
  - Algorithm
  - Math
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Baekjoon
  - Problem-5051
  - C++
  - CPP
  - Math
  - 수학
  - Number Theory
  - 정수론
  - Modular Arithmetic
  - 모듈러 연산
  - Modulo
  - 모듈러
  - Pythagoras
  - 피타고라스
  - Pythagorean Theorem
  - 피타고라스의 정리
  - Squared Residue
  - 제곱 나머지
  - Residue Class
  - 나머지 클래스
  - Convolution
  - 컨볼루션
  - Cyclic Convolution
  - 순환 컨볼루션
  - Circular Convolution
  - 원형 컨볼루션
  - FFT
  - 고속 푸리에 변환
  - NTT
  - 폴리노미얼 곱셈
  - Polynomial Multiplication
  - Complex Numbers
  - 복소수
  - Rounding
  - 반올림
  - Precision
  - 정밀도
  - Folding
  - 접기
  - FFT Convolution
  - FFT Fold
  - Counting
  - 개수세기
  - Combinatorics
  - 조합론
  - Ordered Pairs
  - 순서쌍
  - Unordered Pairs
  - 무순서 쌍
  - a<=b
  - 대칭 보정
  - Proof of Correctness
  - 정당성 증명
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Implementation
  - 구현
  - Edge Cases
  - 코너 케이스
  - Overflow Safe
  - 오버플로 방지
  - 64-bit Integer
  - 64비트 정수
  - long long
image: "wordcloud.png"
---

## 문제 정보

- 문제: `https://www.acmicpc.net/problem/5051`
- 제목: 피타고라스의 정리
- 요약: `1 ≤ a,b,c ≤ n−1`, `a ≤ b`에서 \(a^2 + b^2 \equiv c^2 \pmod n\)를 만족하는 삼중쌍 개수를 출력합니다. `n`은 최대 500,000입니다.
- 제한: 시간 1초, 메모리 128MB, 입력 하나 `n (2 ≤ n ≤ 500000)`

## 입출력 형식/예제

입력

```text
7
```

출력

```text
18
```

또는

입력

```text
15
```

출력

```text
64
```

## 접근 개요(아이디어 스케치)

- 핵심 아이디어는 제곱 나머지 분포를 이용한 합성입니다.
  - `cntSq[r] = |{x ∈ [1..n−1] : x^2 ≡ r (mod n)}|`.
  - `A = cntSq`라 두고, `A ⊛ A`의 순환 컨볼루션은 \((a^2 \bmod n) + (b^2 \bmod n)\)의 분포를 줍니다.
- 순서가 있는 (a,b) 쌍의 총 개수: `ordered = Σ_r (A ⊛ A)[r] · A[r]` (여기서 `r = c^2 mod n`).
- `a=b`인 대각선 개수: `equal = Σ_r A[r] · A[(2r) mod n]`.
- 우리가 원하는 `a ≤ b` 개수는 대칭 보정으로 \(\frac{ordered + equal}{2}\) 입니다.
- 순환 컨볼루션은 FFT로 선형 컨볼루션을 계산한 뒤 길이 `n`에서 접기(folding)로 구현합니다: `circ[k] = conv[k] + conv[k+n]`.

```mermaid
flowchart TD
  A[제곱 나머지 분포 A[r]] --> B[선형 컨볼루션 A*A (FFT)]
  B --> C[길이 n에서 접기(순환 컨볼루션)]
  C --> D[ordered = Σ_r circ[r]·A[r]]
  A --> E[equal = Σ_r A[r]·A[2r mod n]]
  D --> F[정답 = (ordered + equal)/2]
  E --> F
```

## 알고리즘 설계

1) `cntSq`를 선형 시간에 구성: `x=1..n-1`에 대해 `r=(x*x) mod n`, `cntSq[r]++`.
2) 길이 `L=2^k ≥ 2n`로 zero-padding 하여 FFT 기반 선형 컨볼루션 `conv=A*A` 계산.
3) 순환 컨볼루션 복원: `circ[k] = conv[k] + conv[k+n] (0 ≤ k < n)`.
4) `ordered = Σ_k circ[k]·A[k]`, `equal = Σ_r A[r]·A[(2r) mod n]`.
5) `answer = (ordered + equal)/2`를 128비트 누적으로 출력.

올바름 근거(요지):
- `A⊛A`는 \((a^2 mod n)+(b^2 mod n)\)의 분포를 정확히 세며, `c` 선택은 같은 나머지 `r`의 개수 `A[r]`만큼 독립 곱으로 곱해집니다.
- 순서쌍(ordered)에서 `a≠b`는 쌍대가 존재하므로 2배, `a=b`는 1배이므로 `a≤b` 변환식 `U=(O+E)/2`가 성립합니다.

## 복잡도

- 시간: \(O(n \log n)\) (FFT 2회 + 역변환 1회)
- 공간: \(O(n)\)

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using cd = complex<double>;
const double PI = acos(-1.0);

static void fft(vector<cd>& a, bool invert) {
    int n = (int)a.size();
    static vector<int> rev;
    static vector<cd> roots{0, 1};

    if ((int)rev.size() != n) {
        int k = __builtin_ctz(n);
        rev.assign(n, 0);
        for (int i = 0; i < n; ++i)
            rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (k - 1));
    }
    if ((int)roots.size() < n) {
        int k = __builtin_ctz((int)roots.size());
        roots.resize(n);
        while ((1 << k) < n) {
            double ang = 2 * PI / (1 << (k + 1));
            for (int i = 1 << (k - 1); i < (1 << k); ++i) {
                roots[2 * i] = roots[i];
                double angle = ang * (2 * i + 1 - (1 << k));
                roots[2 * i + 1] = cd(cos(angle), sin(angle));
            }
            ++k;
        }
    }

    for (int i = 0; i < n; ++i) if (i < rev[i]) swap(a[i], a[rev[i]]);

    for (int len = 1; len < n; len <<= 1) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; ++j) {
                cd u = a[i + j];
                cd v = a[i + j + len] * roots[len + j];
                a[i + j] = u + v;
                a[i + j + len] = u - v;
            }
        }
    }
    if (invert) {
        reverse(a.begin() + 1, a.end());
        double inv_n = 1.0 / n;
        for (int i = 0; i < n; ++i) a[i] *= inv_n;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    vector<long long> cntSq(n, 0);
    for (long long x = 1; x <= n - 1; ++x) {
        long long r = (long long)((__int128)x * x % n);
        ++cntSq[(size_t)r];
    }

    size_t L = 1;
    while (L < (size_t)n * 2) L <<= 1;

    vector<cd> fa(L), fb(L);
    for (size_t i = 0; i < (size_t)n; ++i) {
        fa[i] = (double)cntSq[i];
        fb[i] = (double)cntSq[i];
    }

    fft(fa, false);
    fft(fb, false);
    for (size_t i = 0; i < L; ++i) fa[i] *= fb[i];
    fft(fa, true);

    vector<long long> conv(L, 0);
    for (size_t i = 0; i < L; ++i) {
        long long v = llround(fa[i].real());
        if (v < 0) v = 0;
        conv[i] = v;
    }

    __int128 totalOrdered = 0;
    for (size_t k = 0; k < (size_t)n; ++k) {
        long long cyc = conv[k];
        if (k + (size_t)n < L) cyc += conv[k + (size_t)n];
        totalOrdered += (__int128)cyc * cntSq[k];
    }

    __int128 totalEqual = 0;
    for (size_t r = 0; r < (size_t)n; ++r) {
        totalEqual += (__int128)cntSq[r] * cntSq[(2 * r) % (size_t)n];
    }

    __int128 answer = (totalOrdered + totalEqual) / 2;

    if (answer == 0) {
        cout << 0 << '\n';
        return 0;
    }
    string s;
    while (answer > 0) {
        int digit = (int)(answer % 10);
        s.push_back(char('0' + digit));
        answer /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트

- 작은 n (예: 2, 3, 4, 5, 6, 7)에서 직접 검증값과 비교
- `a=b` 대각선 보정: `equal = Σ_r A[r]·A[2r mod n]` 식을 별도 확인
- 부동소수점 반올림: `llround` 사용 및 음수 소수 에러 가드(`max(·,0)`) 적용
- 누적 오버플로: 합산은 `__int128` 사용, 출력 시 자리수 단위 변환

## 제출 전 점검

- 입력/출력 형식 및 개행 확인
- FFT 길이 `L`은 항상 `2n` 이상인 2의 거듭제곱인지 확인
- 순환 컨볼루션 접기(`conv[k] + conv[k+n]`) 구현 확인
- 시간/메모리 여유: `n=5e5`에서도 길이 `≈1,048,576` FFT 3회 내 처리

## 참고자료

- 순환 컨볼루션과 접기: 선형 컨볼루션 결과를 길이 `n`에서 접어 합산
- 대칭 보정: `U = (O + E) / 2` (ordered→`a≤b` 변환)


