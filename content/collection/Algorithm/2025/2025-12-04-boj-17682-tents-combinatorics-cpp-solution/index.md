---
title: "[Algorithm] C++ 백준 17682번 Tents"
description: "캠핑장 격자에 텐트를 배치하는 경우의 수를 구하는 조합론 문제로, 행-쌍(row-pair)과 열-쌍(column-pair), 고립 텐트를 분리하여 동적계획법으로 계산합니다. 모듈러 연산과 팩토리얼을 활용한 효율적인 풀이입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Combinatorics
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-17682
  - Tents
  - 텐트
  - 조합론
  - Combinatorics
  - 동적계획법
  - Dynamic Programming
  - DP
  - 경우의 수
  - Counting
  - 모듈로 연산
  - Modular Arithmetic
  - 모듈러 역원
  - Modular Inverse
  - 페르마의 소정리
  - Fermat's Little Theorem
  - 팩토리얼
  - Factorial
  - 이항계수
  - Binomial Coefficient
  - 조합계산
  - Combinatorial Calculation
  - 격자
  - Grid
  - 제약조건
  - Constraints
  - 방향배치
  - Direction Assignment
  - 수학
  - Mathematics
  - C++
  - Programming
  - 프로그래밍
  - 경쟁프로그래밍
  - Competitive Programming
  - JOI
  - Spring Training Camp
  - 포함배제 원리
  - Inclusion-Exclusion
  - 분할
  - Partition
  - 카운팅 문제
  - Counting Problem
  - 세트 파티션
  - Set Partition
  - 확률계산
  - Probability Calculation
  - 수열
  - Sequence
  - 최적화
  - Optimization
  - 정답코드
  - Solution Code
image: wordcloud.png
---

## 문제 요약

**문제 링크**: [https://www.acmicpc.net/problem/17682](https://www.acmicpc.net/problem/17682)

JOI-kun이 운영하는 캠핑장이 H×W 격자로 나뉘어 있습니다. 각 칸에 최대 하나의 텐트를 배치할 수 있으며, 각 텐트는 4방향(N, S, E, W) 중 하나를 향해야 합니다.

**제약조건:**
- 같은 열의 두 텐트는 위쪽이 남(S), 아래쪽이 북(N)을 향함
- 같은 행의 두 텐트는 왼쪽이 동(E), 오른쪽이 서(W)를 향함
- 최소 1개 이상의 텐트 배치

**요구사항**: 조건을 만족하는 모든 배치 방법의 수를 mod 10^9+7로 출력

## 입출력

**입력:**
```
H W
```

**출력:**
```
경우의 수 mod 1000000007
```

**예제:**
```
입력: 1 2
출력: 9

입력: 4 3
출력: 3252
```

## 접근 개요

### 핵심 관찰

1. **텐트의 분류**: 텐트들을 3가지 타입으로 분류
   - **Row-pair**: 같은 행에 있는 2개의 텐트 쌍 (방향 고정: E, W)
   - **Column-pair**: 같은 열에 있는 2개의 텐트 쌍 (방향 고정: S, N)
   - **Isolated**: 혼자 있는 텐트 (방향 4가지 선택 가능)

2. **독립성**: 
   - Row-pair가 사용하는 행들은 column-pair에 사용 불가
   - Column-pair가 사용하는 열들은 row-pair에 사용 불가
   - Isolated 텐트들은 각 행/열에 최대 1개씩만 배치 가능

### 상태 정의

- `r` = row-pair의 개수 (사용 행: 2r)
- `c` = column-pair의 개수 (사용 열: 2c)
- Isolated 영역: (H-r-2c) × (W-c-2r) 격자

### 계산 방식

각 (r, c) 쌍에 대해:
1. H개 행 중 r개 선택: C(H, r)
2. W개 열 중 c개 선택: C(W, c)
3. Row-pair: (W-c)개 열에서 2r개 선택 후, 2r개 열을 r개 행에 배정
   - = C(W-c, 2r) × (2r)! / 2^r
4. Column-pair: (H-r)개 행에서 2c개 선택 후, 2c개 행을 c개 열에 배정
   - = C(H-r, 2c) × (2c)! / 2^c
5. Isolated 영역의 배치: g[a][b] (동적계획법)

### 고립 텐트 계산 (g[a][b])

**정의**: a×b 격자에서 각 행/열마다 최대 1개의 텐트를 배치하는 방법의 수

**점화식**:
```
g[a][b] = g[a-1][b] + 4×b×g[a-1][b-1]
```

- 첫 번째 행이 비는 경우: g[a-1][b]
- 첫 번째 행에 1개 배치: 4(방향) × b(열선택) × g[a-1][b-1]

**베이스 케이스**: g[0][b] = 1, g[a][0] = 1

## 알고리즘 설계

### 단계별 계산

```
1. 팩토리얼과 역원 전처리 (O(N))
   - fact[i] = i!
   - inv_fact[i] = (i!)^(-1) mod MOD

2. 고립 텐트 DP 계산 (O(H×W))
   - g[a][b] = isolated 영역 배치 수

3. 최종 합계 (O(H×W))
   for r in 0..H:
     for c in 0..W:
       if (W-c >= 2r) and (H-r >= 2c):
         term = C(H,r) × C(W,c) × row_ways × col_ways × g[a][b]
         ans += term

4. 빈 배치 제외 (답 - 1)
```

## 복잡도 분석

- **시간 복잡도**: O(H×W) - 전처리 O(N) + DP O(H×W) + 답 계산 O(H×W)
- **공간 복잡도**: O(H×W) - g 배열 저장

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
const int MAXN = 3005;

long long fact[2 * MAXN], inv_fact[2 * MAXN];
long long inv2[MAXN];
long long g[MAXN][MAXN];

long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

long long C(int n, int k) {
    if (k < 0 || k > n) return 0;
    return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int H, W;
    cin >> H >> W;
    
    int LIMIT = 2 * max(H, W) + 5;
    
    // 팩토리얼 전처리
    fact[0] = 1;
    for (int i = 1; i < LIMIT; i++) {
        fact[i] = fact[i-1] * i % MOD;
    }
    inv_fact[LIMIT-1] = power(fact[LIMIT-1], MOD-2, MOD);
    for (int i = LIMIT-2; i >= 0; i--) {
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD;
    }
    
    // 2의 역원 전처리
    long long inv2_single = power(2, MOD-2, MOD);
    inv2[0] = 1;
    for (int i = 1; i <= max(H, W); i++) {
        inv2[i] = inv2[i-1] * inv2_single % MOD;
    }
    
    // 고립 텐트 DP
    for (int b = 0; b <= W; b++) g[0][b] = 1;
    for (int a = 1; a <= H; a++) {
        g[a][0] = 1;
        for (int b = 1; b <= W; b++) {
            g[a][b] = (g[a-1][b] + 4LL * b % MOD * g[a-1][b-1]) % MOD;
        }
    }
    
    long long ans = 0;
    
    // 모든 (r, c) 조합 탐색
    for (int r = 0; r <= H; r++) {
        for (int c = 0; c <= W; c++) {
            // Row-pair 검증: 2r개 열 필요
            if (W - c < 2 * r) continue;
            // Column-pair 검증: 2c개 행 필요
            if (H - r < 2 * c) continue;
            
            int a = H - r - 2 * c; // 고립 텐트 영역 행
            int b = W - c - 2 * r; // 고립 텐트 영역 열
            
            if (a < 0 || b < 0) continue;
            
            long long term = C(H, r) * C(W, c) % MOD;
            
            // Row-pair: C(W-c, 2r) × (2r)! / 2^r
            long long row_ways = C(W - c, 2 * r) * fact[2 * r] % MOD * inv2[r] % MOD;
            
            // Column-pair: C(H-r, 2c) × (2c)! / 2^c
            long long col_ways = C(H - r, 2 * c) * fact[2 * c] % MOD * inv2[c] % MOD;
            
            term = term * row_ways % MOD * col_ways % MOD * g[a][b] % MOD;
            
            ans = (ans + term) % MOD;
        }
    }
    
    // 빈 배치 제외
    ans = (ans - 1 + MOD) % MOD;
    
    cout << ans << "\n";
    
    return 0;
}
```

## 코너 케이스 체크리스트

| 케이스 | 설명 | 처리 |
|--------|------|------|
| H=1, W=1 | 최소 크기 | 1개 텐트만 가능 (4가지) |
| H=1, W=2 | 행 단일 | Row-pair 또는 isolated |
| H=2, W=1 | 열 단일 | Column-pair 또는 isolated |
| H=100, W=100 | 최대 크기 | 모듈로 연산 정확성 검증 |
| R+C가 홀수 | 패리티 | 정상 처리 |

## 검증 (H=1, W=2)

1. **(r=0, c=0)**: 고립 영역 1×2
   - g[1][2] = g[0][2] + 4×2×g[0][1] = 1 + 8×1 = **9**

2. **(r=1, c=0)**: Row-pair 1개
   - C(2,2) × 2!/2 × g[0][0] = 1 × 1 × 1 = **1**

3. **합계**: 10 - 1(빈 배치) = **9** ✓

## 제출 전 체크

- 모듈로 연산: 음수 처리 (`(ans - 1 + MOD) % MOD`)
- 오버플로우: long long 사용
- 초기화: g 배열 완전히 계산
- 팩토리얼 범위: 2×max(H,W) 이상 필요
- 이항계수: 범위 체크 (k > n일 때 0 반환)

## 참고자료

- **조합론 기초**: 이항계수, 포함-배제 원리
- **모듈러 역원**: 페르마의 소정리 (a^(p-1) ≡ 1 mod p)

