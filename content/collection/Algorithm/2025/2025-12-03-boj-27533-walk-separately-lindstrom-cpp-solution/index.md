---
title: "[Algorithm] C++ 백준 27533번 따로 걸어가기"
description: "토끼 부부가 격자 위에서 만나지 않고 이동하는 경로의 수를 구하는 비교차 경로(non-intersecting paths) 문제로, Lindström-Gessel-Viennot 보조정리를 사용하여 해결합니다. 조합론과 모듈로 연산을 활용한 효율적인 풀이입니다."
tags:
  - 조합론
  - Combinatorics
  - Lindstrom-Gessel-Viennot lemma
  - LGV lemma
  - 비교차 경로
  - Non-intersecting paths
  - 격자 경로
  - Lattice paths
  - 경로 개수
  - Path counting
  - 모듈로 연산
  - Modular arithmetic
  - 모듈로 역원
  - Modular inverse
  - 팩토리얼
  - Factorial
  - 페르마의 소정리
  - Fermat's little theorem
  - 동적 계획법
  - Dynamic programming
  - 그래프 이론
  - Graph theory
  - 수학
  - Mathematics
  - 알고리즘
  - Algorithm
  - 경로
  - Path
  - 2D 격자
  - 2D grid
  - 문제 해결
  - Problem solving
  - 경우의 수
  - Permutation
  - 조합
  - Combination
  - 고급 알고리즘
  - Advanced algorithm
  - BOJ
  - Baekjoon
  - 온라인 저지
  - Online judge
  - C++
  - Programming
  - 프로그래밍
  - 비조화 경로
  - Non-crossing lattice paths
  - 행렬식
  - Determinant
  - 보조정리
  - Lemma
  - Gessel
  - Viennot
  - SUAPC
date: 2025-12-03
draft: false
image: wordcloud.png
---

## 문제 요약

문제 링크: [https://www.acmicpc.net/problem/27533](https://www.acmicpc.net/problem/27533)

토끼 부부 토순이와 토준이가 N×M 격자에서 (1,1)에서 출발하여 (N,M)으로 이동합니다. 두 토끼는:
- 오른쪽과 아래쪽으로만 이동
- 동시에 한 칸씩 이동
- 출발점과 도착점을 제외하고 중간에 만나지 않음

이러한 조건을 만족하는 경로의 수를 구하세요. (단, 두 토끼는 구별됩니다)

## 알고리즘 분석

### 핵심 개념: Lindström-Gessel-Viennot Lemma

비교차 경로(non-intersecting paths) 문제는 행렬식을 이용한 LGV 보조정리로 해결합니다.

**두 경로가 교차하지 않으려면:**
- 토순이: (1,1) → (1,2) → ... → (N-1,M) → (N,M)
- 토준이: (1,1) → (2,1) → ... → (N,M-1) → (N,M)

또는

- 토순이: (1,1) → (2,1) → ... → (N,M-1) → (N,M)
- 토준이: (1,1) → (1,2) → ... → (N-1,M) → (N,M)

### 공식 유도

LGV lemma에 따르면:

```
비교차 경로 개수 = det|C(s_i, e_j)|
```

우리의 경우:
- C(n, k) = 조합(n, k)에서 n = N+M-4 (중간 이동 단계)
- det = C(N+M-4, N-2) × C(N+M-4, M-2) - C(N+M-4, N-1) × C(N+M-4, M-1)

두 토끼를 구별하므로 **2를 곱합니다**.

## 예제 분석

### 예제 1: N=2, M=2

```
격자: 2×2
n = 2+2-4 = 0

det = C(0,0)×C(0,0) - C(0,1)×C(0,1)
    = 1×1 - 0×0 = 1

답 = 2×1 = 2
```

경로:
1. 토순이 (1,2) → (2,2), 토준이 (2,1) → (2,2)
2. 토순이 (2,1) → (2,2), 토준이 (1,2) → (2,2)

### 예제 2: N=3, M=4

```
n = 3+4-4 = 3

det = C(3,1)×C(3,2) - C(3,2)×C(3,3)
    = 3×3 - 3×1 = 9-3 = 6

답 = 2×6 = 12
```

## 구현 전략

1. **팩토리얼 전처리**: O(N+M)
2. **모듈로 역원 계산**: Fermat's little theorem 사용
3. **조합 계산**: C(n,r) = n! × (r!)^(-1) × ((n-r)!)^(-1) (mod 10^9+7)
4. **행렬식 계산**: 4개의 조합값으로 det 계산

## 코드 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인할 수 있습니다.
#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1e9 + 7;

// 모듈로 거듭제곱
long long power(long long a, long long b, long long mod) {
    long long res = 1;
    a %= mod;
    while (b > 0) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

// 모듈로 역원 (Fermat's little theorem)
long long modInv(long long a, long long mod) {
    return power(a, mod - 2, mod);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int N, M;
    cin >> N >> M;
    
    int maxVal = N + M;
    
    // 팩토리얼과 역팩토리얼 전처리
    vector<long long> fact(maxVal + 1), inv_fact(maxVal + 1);
    fact[0] = 1;
    for (int i = 1; i <= maxVal; i++) {
        fact[i] = fact[i-1] * i % MOD;
    }
    inv_fact[maxVal] = modInv(fact[maxVal], MOD);
    for (int i = maxVal - 1; i >= 0; i--) {
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD;
    }
    
    // 조합 C(n, r)
    auto comb = [&](int n, int r) -> long long {
        if (r < 0 || r > n) return 0;
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD;
    };
    
    // Lindström-Gessel-Viennot lemma 적용
    // 경로 1: (1,2) -> (N-1,M), 경로 2: (2,1) -> (N,M-1)
    int n = N + M - 4;
    
    long long c1 = comb(n, N - 2);  // (1,2) -> (N-1,M)
    long long c2 = comb(n, M - 2);  // (2,1) -> (N,M-1)
    long long c3 = comb(n, N - 1);  // (1,2) -> (N,M-1)
    long long c4 = comb(n, M - 1);  // (2,1) -> (N-1,M)
    
    // det = c1*c2 - c3*c4
    long long det = (c1 * c2 % MOD - c3 * c4 % MOD + MOD) % MOD;
    
    // 두 토끼를 구별하므로 2를 곱함
    long long answer = 2 * det % MOD;
    
    cout << answer << endl;
    
    return 0;
}
```

## 시간 복잡도 분석

| 요소 | 복잡도 |
|------|--------|
| 팩토리얼 계산 | O(N+M) |
| 역팩토리얼 계산 | O(N+M) |
| 조합 계산 | O(1) × 4회 = O(1) |
| **전체** | **O(N+M)** |

## 공간 복잡도

- 팩토리얼 배열: O(N+M)
- 기타 변수: O(1)
- **전체: O(N+M)**

## 주요 학습 포인트

1. **LGV 보조정리**: 비교차 경로 개수를 행렬식으로 표현
2. **모듈로 연산**: 큰 수 처리 및 역원 계산
3. **조합론**: 격자 경로의 개수 계산
4. **Fermat의 소정리**: 모듈로 역원 계산의 이론적 기초

## 실전 팁

1. **모듈로 음수 처리**: `(a - b + MOD) % MOD`로 음수가 되는 것을 방지
2. **오버플로우 방지**: 모든 곱셈 후 모듈로 연산
3. **팩토리얼 한계**: 대수 N, M에 대해 미리 계산해두기
4. **조합 재사용**: 한 번 계산한 조합값을 변수에 저장

## 테스트 케이스

| N | M | 예상 답 | 설명 |
|---|---|--------|------|
| 2 | 2 | 2 | 기본 예제 |
| 3 | 4 | 12 | 중간 크기 |
| 123456 | 78901 | 620455136 | 대수 (모듈로 적용) |

---

**참고 자료:**
- Lindström, B. (1985). "On the vector representation of induced matroids"
- Gessel, I., & Viennot, G. (1989). "Determinants, paths, and plane partitions"
- BOJ 27533 (SUAPC 2023 Winter L번)

