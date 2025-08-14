---
title: "[Algorithm] cpp 백준 17104번: 골드바흐 파티션 2"
description: "FFT 컨볼루션으로 모든 짝수 N(2<N≤1e6)의 골드바흐 파티션 개수를 한 번에 전처리하고 각 쿼리를 O(1)에 답합니다. 에라토스테네스의 체, llround 반올림, p=q 대칭 보정, 0.5초/512MB 제약 대응 구현."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Number Theory
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17104
- cpp
- C++
- Number Theory
- 정수론
- Goldbach
- 골드바흐
- Goldbach Partition
- 골드바흐 파티션
- Prime
- 소수
- Sieve of Eratosthenes
- 에라토스테네스의 체
- FFT
- Fast Fourier Transform
- 빠른 푸리에 변환
- Convolution
- 컨볼루션
- Polynomial
- 다항식
- NTT
- Number Theoretic Transform
- 복소 FFT
- Complex FFT
- Precision
- 반올림 오차
- llround
- Double Precision
- 실수 연산
- Big O
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Precomputation
- 전처리
- O(N log N)
- O(1) Query
- Query Processing
- 쿼리 처리
- Unordered Pairs
- 순서 무관 쌍
- Ordered Pairs
- 순서 있는 쌍
- Symmetry Correction
- 대칭 보정
- p equals q
- p=q 대칭
- 2 as Prime
- 소수 2 처리
- Edge Cases
- 코너 케이스
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Implementation Details
- 구현 디테일
- Fast IO
- 입출력 최적화
- Memory
- 메모리 관리
- Rounding
- 반올림
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17104
- 요약: 짝수 `N`을 두 소수의 합으로 나타내는 표현(골드바흐 파티션)의 개수를 구한다. 순서만 다른 것은 같은 파티션으로 본다.

### 제한/스펙
- 테스트케이스 `T (1 ≤ T ≤ 100000)`
- 각 `N`은 짝수이며 `2 < N ≤ 1,000,000`
- 시간 0.5초, 메모리 512MB

## 입출력 형식/예제

예제 입력 1
```
5
6
8
10
12
100
```

예제 출력 1
```
1
1
2
1
6
```

## 접근 개요(아이디어 스케치)
- 핵심 아이디어: 모든 `N`에 대해 한 번의 FFT 컨볼루션으로 “두 소수의 합이 `N`이 되는 ordered 쌍 수”를 전 범위에서 동시에 계산한다.
- `A[x] = 1`(x가 소수)인 지시 배열의 자기 컨볼루션 `C = A * A`에서 `C[N]`은 `(p, q)`(순서 있는) 소수 쌍의 개수다. 순서 무관 파티션 개수는 `(C[N] + [N/2가 소수]) / 2`로 얻는다.
- 예외 `N=4`는 `(2,2)` 단 한 가지이며 위 공식에 자연스럽게 포함된다. 대부분의 짝수 `N`에서는 `2`가 관여하는 쌍이 없으므로(짝수−2는 짝수) 보정은 `N/2` 소수 여부만 필요하다.

```mermaid
flowchart TD
  A[에라토스테네스의 체로 소수 배열 is_prime] --> B[A[x]=1 if prime]
  B --> C[FFT(A)]
  C --> D[성분별 제곱 (A의 자기 컨볼루션)]
  D --> E[IFFT -> conv]
  E --> F[반올림 llround]
  F --> G[정답: (conv[N] + is_prime[N/2]) / 2]
```

## 알고리즘 설계
- 전처리
  - `MAXN=1e6`까지 체로 `is_prime` 구성.
  - 길이가 `≥ 2*MAXN+1`이 되는 2의 거듭제곱으로 패딩하여 `A`에 소수 지시값 채움.
  - FFT→성분별 제곱→역FFT(IFFT)로 `conv[N] ≈ ordered 쌍 수`를 획득하고 `llround`로 반올림.
- 쿼리 처리
  - 각 `N`에 대해 `ans = (conv[N] + (is_prime[N/2]?1:0)) / 2` 출력.
- 올바름 근거
  - 컨볼루션 정의상 `conv[N] = Σ_x A[x]·A[N−x]`는 `(x, N−x)` 순서쌍 개수.
  - `p ≠ q`는 두 번(순서 바뀜) 세어지므로 2로 나눔. `p = q = N/2`는 한 번만 세어지므로 보정 `+1` 후 2로 나눔.

## 복잡도
- 전처리: FFT 1회 `O(N log N)` (N≈2^21 수준 패딩)
- 쿼리: 각 `O(1)`
- 메모리: 복소 배열 수백만 원소 수준(512MB 내 동작)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using cd = complex<double>;
const double PI = acos(-1.0);
const int MAXN = 1'000'000;

static void fft(vector<cd> &a, bool invert) {
    int n = (int)a.size();
    static vector<int> rev;
    static vector<cd> roots{cd(0, 0), cd(1, 0)};

    if ((int)rev.size() != n) {
        int k = __builtin_ctz(n);
        rev.assign(n, 0);
        for (int i = 0; i < n; i++) {
            rev[i] = 0;
            for (int j = 0; j < k; j++) if (i & (1 << j))
                rev[i] |= 1 << (k - 1 - j);
        }
    }
    if ((int)roots.size() < n) {
        int k = __builtin_ctz(roots.size());
        roots.resize(n);
        while ((1 << k) < n) {
            double ang = 2 * PI / (1 << (k + 1));
            for (int i = 1 << (k - 1); i < (1 << k); i++) {
                roots[2 * i] = roots[i];
                double a = ang * (2 * i + 1 - (1 << k));
                roots[2 * i + 1] = cd(cos(a), sin(a));
            }
            k++;
        }
    }

    for (int i = 0; i < n; i++)
        if (i < rev[i]) swap(a[i], a[rev[i]]);

    for (int len = 1; len < n; len <<= 1) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; j++) {
                cd u = a[i + j];
                cd v = a[i + j + len] * roots[len + j];
                a[i + j] = u + v;
                a[i + j + len] = u - v;
            }
        }
    }

    if (invert) {
        reverse(a.begin() + 1, a.end());
        for (cd &x : a) x /= n;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Sieve up to MAXN
    vector<bool> is_prime(MAXN + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * 1LL * i <= MAXN; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= MAXN; j += i) is_prime[j] = false;
        }
    }

    // Prepare polynomial A: A[p] = 1 for all primes p (including 2)
    int need = 1;
    while (need < 2 * MAXN + 1) need <<= 1;

    vector<cd> A(need, 0);
    for (int i = 2; i <= MAXN; i++) if (is_prime[i]) A[i] = 1.0;

    // Convolution A * A via FFT
    fft(A, false);
    for (int i = 0; i < need; i++) A[i] *= A[i];
    fft(A, true);

    // Round to nearest integer
    vector<long long> conv(2 * MAXN + 1, 0);
    for (int i = 0; i <= 2 * MAXN; i++) {
        conv[i] = llround(A[i].real());
    }

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int N; cin >> N; // even, 2 < N ≤ 1e6
        // Ordered pairs from convolution = conv[N]
        // Unordered count = (conv[N] + [N/2 is prime]) / 2
        long long sym = (N % 2 == 0 && is_prime[N / 2]) ? 1 : 0;
        long long ans = (conv[N] + sym) / 2;
        cout << ans << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `N=4`: `(2,2)` 한 가지 → 보정식으로 자동 처리.
- 큰 `T`(최대 1e5): 전처리 1회 후 O(1) 응답.
- 반올림 오차: `llround` 사용, 입력이 0/1이므로 실수 오차는 안전 범위.
- 메모리: 2^21 크기 복소 배열 사용 → 512MB 내 동작.

## 제출 전 점검
- 체 범위: `MAXN=1e6`까지 정확히 마킹.
- 패딩: 길이 `≥ 2*MAXN+1`의 2의 거듭제곱으로 설정.
- 대칭 보정식: `(conv[N] + is_prime[N/2]) / 2` 사용.
- 빠른 입출력 설정 확인.

## 참고자료/유사문제
- 골드바흐의 추측 관련 문제군: ordered vs unordered 구분 주의
- FFT/컨볼루션 기본기: 폴리노미얼 곱셈으로 합의 개수 세기


