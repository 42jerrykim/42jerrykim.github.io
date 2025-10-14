---
title: "[Algorithm] C++ 백준 8464번: Non-Squarefree Numbers"
description: "non-squarefree의 n번째 값을 찾습니다. μ(k)로 squarefree 개수 S(x)=∑μ(k)⌊x/k²⌋를 계산하고, f(x)=x−S(x)≥n인 최소 x를 이분 탐색으로 구합니다. O(√x log x)로 1e10까지 처리."
date: 2025-10-14
lastmod: 2025-10-14
categories:
  - Algorithm
  - Number Theory
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Baekjoon
  - Problem-8464
  - C++
  - CPP
  - Math
  - 수학
  - Number Theory
  - 정수론
  - Mobius
  - Möbius
  - 모비우스
  - Inclusion Exclusion
  - 포함배제
  - Squarefree
  - 제곱인수없음
  - Non-Squarefree
  - 제곱인수있음
  - Binary Search
  - 이분탐색
  - Counting
  - 개수세기
  - Multiplicative Function
  - 곱셈적 함수
  - Floor Division
  - 내림나눗셈
  - Square
  - 제곱
  - Density
  - 밀도
  - sqrt
  - 제곱근
  - Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Implementation
  - 구현
  - Edge Cases
  - 코너 케이스
  - Proof of Correctness
  - 정당성 증명
  - Optimization
  - 최적화
  - Performance
  - 성능최적화
  - Big-O
  - O(sqrt n)
  - O(log n)
  - Inclusion-Exclusion Principle
  - 원리
  - Precomputation
  - 전처리
  - Sieve
  - 체
  - Möbius Sieve
  - 모비우스 체
  - Integer Sequences
  - 정수 수열
  - nth Element
  - n번째
  - Problem Solving
  - 문제풀이
  - Editorial
  - 에디토리얼
  - Tutorial
  - 튜토리얼
  - Tips
  - 팁
  - Pitfalls
  - 실수 포인트
  - Overflow
  - 오버플로
image: "wordcloud.png"
---

## 문제 정보

- 문제: `https://www.acmicpc.net/problem/8464`
- 제목: Non-Squarefree Numbers
- 요약: 양의 정수들 중 제곱인수(>1)의 제곱으로 나누어떨어지는 수(= 비-제곱무제수)만 모은 수열에서 n번째 수를 출력합니다.
- 제한: 입력 하나 `n (1 ≤ n ≤ 10^10)`, 시간 2초, 메모리 32MB

## 입출력 형식/예제

입력

```text
10
```

출력

```text
27
```

## 접근 개요(아이디어 스케치)

- μ(k)를 뫼비우스 함수라 할 때, `x` 이하의 제곱인수 없는 수(=squarefree)의 개수는 \( S(x) = \sum_{k\ge1} \mu(k)\,\left\lfloor \frac{x}{k^2} \right\rfloor \) 입니다.
- 비-제곱무제수(=non-squarefree) 개수는 `x - S(x)` 이므로, `f(x) = x - S(x)`라 두고 `f(x) ≥ n`을 만족하는 최소 `x`를 이분 탐색으로 찾습니다.
- `S(x)` 계산은 `k ≤ ⌊√x⌋`까지만 필요하므로, `O(√x)` 시간에 가능. 이분 탐색과 결합해 `O(√x log x)`.

```mermaid
flowchart TD
  A[입력 n] --> B[상한 hi 찾기: f(hi) ≥ n 될 때까지 두 배]
  B --> C[μ(k) 전처리: k ≤ ⌊√hi⌋]
  C --> D{이분 탐색}
  D -->|mid| E[S(mid)=∑ μ(k)⌊mid/k²⌋]
  E --> F[f(mid)=mid - S(mid)]
  F -->|f(mid) ≥ n| G[ans=mid, hi=mid-1]
  F -->|f(mid) < n| H[lo=mid+1]
  G --> D
  H --> D
  D -->|종료| I[정답 출력]
```

## 알고리즘 설계

- 뫼비우스 함수 전처리: `k ≤ ⌊√hi⌋` 범위에서 선형 체로 μ(k) 생성.
- `countNonSquarefree(x)` 구현: `r = ⌊√x⌋`, `squarefree = Σ_{k=1..r} μ(k)·⌊x/k²⌋`, 반환 `x - squarefree`.
- 상한 확장: `hi = max(6, 3n)`에서 시작해 `f(hi) < n`이면 `hi *= 2`로 확장하며 μ 재계산.
- 이분 탐색: `[lo, hi]`에서 최소 `x`를 탐색.

## 복잡도

- 시간: `O(√x log x)` (여기서 `x`는 정답), 실무상 `x ≈ n / (1 - 6/π²) ≈ 2.55n` 수준
- 공간: `O(√x)` (μ 테이블)

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static vector<int> mobiusSieve(int limit) {
    vector<int> mu(limit + 1);
    vector<int> lp(limit + 1, 0);
    vector<int> primes;
    mu[1] = 1;
    for (int i = 2; i <= limit; ++i) {
        if (lp[i] == 0) {
            lp[i] = i;
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            long long v = 1LL * p * i;
            if (v > limit) break;
            lp[(int)v] = p;
            if (i % p == 0) {
                mu[(int)v] = 0;
                break;
            } else {
                mu[(int)v] = -mu[i];
            }
        }
    }
    return mu;
}

static unsigned long long countNonSquarefree(unsigned long long x, const vector<int>& mu) {
    if (x == 0) return 0ULL;
    int r = (int)floor(sqrt((long double)x));
    if (r >= (int)mu.size()) r = (int)mu.size() - 1;
    long long squarefreeCount = 0;
    for (int k = 1; k <= r; ++k) {
        if (mu[k] == 0) continue;
        unsigned long long kk = 1ULL * k * k;
        squarefreeCount += 1LL * mu[k] * (x / kk);
    }
    return x - (unsigned long long)squarefreeCount;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    unsigned long long n;
    if (!(cin >> n)) return 0;

    unsigned long long hi = max(6ULL, n * 3ULL);
    int limit = (int)floor(sqrt((long double)hi));
    vector<int> mu = mobiusSieve(limit);

    while (countNonSquarefree(hi, mu) < n) {
        hi <<= 1;
        limit = (int)floor(sqrt((long double)hi));
        mu = mobiusSieve(limit);
    }

    unsigned long long lo = 1, ans = hi;
    while (lo <= hi) {
        unsigned long long mid = (lo + hi) >> 1;
        unsigned long long cnt = countNonSquarefree(mid, mu);
        if (cnt >= n) {
            ans = mid;
            if (mid == 0) break;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }

    cout << ans << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트

- `n = 1` → 정답은 4 (첫 번째 non-squarefree)
- 매우 큰 `n` (최대 10^10) → 상한 확장과 μ 재계산 동작 확인
- 경계값에서 `⌊√x⌋` 절삭, `k^2` 곱 오버플로 없음 (`unsigned long long` 사용)

## 제출 전 점검

- 표준 입출력/개행 형식 확인
- μ 테이블 범위: 항상 `k ≤ ⌊√hi⌋`을 보장
- 이분 탐색 종료 조건 및 `ans` 갱신 누락 여부 점검

## 참고자료

- Squarefree counting: `S(x) = \sum_{k≥1} μ(k) ⌊x/k²⌋`
- 밀도: squarefree 밀도 `6/π²`, non-squarefree 밀도 `1 - 6/π²`


