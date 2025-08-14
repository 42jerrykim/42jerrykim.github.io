---
title: "[Algorithm] cpp 백준 17134번: 르모앙의 추측"
description: "홀수 N을 홀수 소수 p와 짝수 세미소수 2q의 합으로 표현하는 가짓수를 구한다. 에라토스테네스의 체와 소수·2×소수 배열의 FFT 컨볼루션으로 전체 범위를 전처리하고 각 질의를 O(1)로 답한다."
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
- Problem-17134
- cpp
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
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- Graph
- 그래프
- Tree
- 트리
- BFS
- DFS
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Number Theory
- 정수론
- Prime
- 소수
- Sieve of Eratosthenes
- 에라토스테네스의 체
- Semiprime
- 세미소수
- Convolution
- 컨볼루션
- FFT
- 고속푸리에변환
- NTT
- 수학
- Modulo
- 모듈러
- Implementation Details
- 구현 디테일
- Lemoine
- 르모앙
- Lemoine's Conjecture
- 르모앙의 추측
- Counting
- 조합계산
- Signal Processing
- 신호처리
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17134
- 요약: 5보다 큰 홀수 N을 하나의 홀수 소수 p와 하나의 짝수 세미소수 s의 합 \(N = p + s\)으로 나타내는 표현의 가짓수를 구한다. 짝수 세미소수는 두 소수의 곱으로, 반드시 \(2 \times q\) 꼴(\(q\)는 소수)만 가능하다.

## 입력/출력
```
입력
T
N1
N2
...

제한: 1 ≤ T ≤ 100000, 5 < N ≤ 1000000, N은 홀수
```
```
출력
각 테스트케이스마다 표현 가짓수를 한 줄에 하나씩 출력
```

예시
```
입력
6
9
11
17
19
1929
1999

출력
2
2
4
2
65
30
```

## 접근 개요
- **핵심 관찰**: 짝수 세미소수는 반드시 \(2q\) 형태(\(q\)는 소수)이다. 따라서 문제는 \(N = p + 2q\) (\(p, q\) 모두 소수, \(p\)는 홀수 소수) 쌍의 개수 세기 문제다.
- **모델링**: 길이 \(M\)의 배열 \(A\)를 "소수 지시자"로, 배열 \(B\)를 "짝수 세미소수 지시자"로 두고, \(A * B\)의 컨볼루션 값이 \(N\)에서의 가짓수가 된다.
- **전처리 전략**: \(M = \max(N_i)\)까지 에라토스테네스의 체로 소수 마스크를 만든 뒤, FFT로 \(A\)와 \(B\)를 한 번만 컨볼브하여 모든 \(N\)의 답을 O(1)로 조회한다.

## 알고리즘 설계
1. 에라토스테네스의 체로 \([0..M]\) 소수 여부 배열 `isPrime` 생성.
2. 배열 `A[i] = 1` if `i`가 소수, `0` otherwise.
3. 배열 `B[i] = 1` if `i`가 짝수이고 `i = 2 * p` (여기서 `p`는 소수), 그렇지 않으면 `0`.
4. FFT로 `C = A (*) B`를 1회 계산. 그러면 `C[N]`이 원하는 가짓수.
5. 각 질의 `N`에 대해 정수 반올림된 `C[N]`을 출력.

### 올바름 근거 요약
- 짝수 세미소수의 정의상 짝수인 세미소수는 오직 `2 × prime` 뿐이다. 따라서 `B`의 정의가 정확하다.
- 컨볼루션의 정의에 의해 `C[N] = Σ A[i] · B[N-i]`는 곧 `(i가 소수) ∧ (N-i = 2×소수)`인 쌍의 수와 일치한다.
- `p=2`는 홀수 정답에 기여하지 않는다(`N-2`는 홀수이고 `B`는 짝수 인덱스에서만 1). 즉, 자동으로 홀수 소수만 세어진다.

## 복잡도
- 체: \(O(M \log\log M)\)
- FFT 컨볼루션: \(O(M \log M)\) (패딩된 최근접 2의 거듭제곱 크기 기준)
- 질의 응답: \(O(1)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using cd = complex<double>;
const double PI = acos(-1.0);

static void fft(vector<cd>& a, bool invert) {
    int n = (int)a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i + j];
                cd v = a[i + j + len / 2] * w;
                a[i + j] = u + v;
                a[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }

    if (invert) {
        for (cd& x : a) x /= n;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    vector<int> queries(T);
    int maxN = 0;
    for (int i = 0; i < T; i++) {
        cin >> queries[i];
        maxN = max(maxN, queries[i]);
    }
    if (maxN < 1) {
        for (int i = 0; i < T; i++) cout << 0 << '\n';
        return 0;
    }

    // Sieve up to maxN
    vector<bool> isPrime(maxN + 1, true);
    if (maxN >= 0) isPrime[0] = false;
    if (maxN >= 1) isPrime[1] = false;
    for (int i = 2; 1LL * i * i <= maxN; i++) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= maxN; j += i) {
                isPrime[(int)j] = false;
            }
        }
    }

    // Prepare arrays for convolution
    int need = (maxN + 1) + (maxN + 1) - 1;
    int nfft = 1;
    while (nfft < need) nfft <<= 1;

    vector<cd> fa(nfft), fb(nfft);
    for (int i = 2; i <= maxN; i++) {
        if (isPrime[i]) fa[i] = 1.0;
    }
    for (int p = 2; 2 * p <= maxN; p++) {
        if (isPrime[p]) fb[2 * p] = 1.0; // includes 4 (2*2)
    }

    // Convolution
    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < nfft; i++) fa[i] *= fb[i];
    fft(fa, true);

    vector<long long> ways(maxN + 1, 0);
    for (int i = 0; i <= maxN; i++) {
        long long v = llround(fa[i].real());
        if (v < 0) v = 0;
        ways[i] = v;
    }

    for (int n : queries) {
        cout << ways[n] << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 최소/최대 범위: `N=7, 9, 999999, 1000001(불가)` 등 경계값 확인
- `N`이 매우 큰 경우에도 정확히 패딩된 FFT 크기 사용 여부
- 라운딩 오차: `llround` 사용, 음수 미세 오차는 0으로 보정
- `p=2`가 기여하지 않음을 컨볼루션 인덱스 성질로 확인
- 소수 마스크 범위 초과 접근 방지 (`maxN` 기준 생성)

## 제출 전 점검
- 입출력 형식과 개행 일치 여부 확인
- 64-bit 정수 사용으로 오버플로 방지
- FFT 길이(`nfft`)가 `need` 이상인지 확인
- 체 초기화(`0,1` 비소수 처리)와 내부 루프 시작점(`i*i`) 검증

## 참고자료
- Lemoine's conjecture (자카비에츠–르모앙의 추측)
- Fast Fourier Transform 기반 컨볼루션 기법
- 에라토스테네스의 체


