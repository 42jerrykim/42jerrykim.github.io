---
title: "[Algorithm] C++ 백준 13182번 제비"
description: "제비 뽑기에서 파란 제비를 K번 뽑을 때까지의 기댓값을 구하는 확률 문제로, 선형 점화식과 페르마의 소정리를 이용한 모듈로 연산으로 해결합니다. 동적계획법으로 상태를 정의하고 거듭제곱을 활용하여 대수 계산을 단순화합니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Probability
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-13182
  - Lottery Draw
  - 제비
  - 확률
  - Probability
  - 기댓값
  - Expected Value
  - 점화식
  - Recurrence Relation
  - 동적계획법
  - Dynamic Programming
  - DP
  - 선형 점화식
  - Linear Recurrence
  - 모듈로 연산
  - Modular Arithmetic
  - 모듈러 역원
  - Modular Inverse
  - 페르마의 소정리
  - Fermat's Little Theorem
  - 거듭제곱
  - Exponentiation
  - 수학
  - Mathematics
  - 수학적 최적화
  - Mathematical Optimization
  - C++
  - Programming
  - 프로그래밍
  - 경쟁프로그래밍
  - Competitive Programming
  - 정답코드
  - Solution Code
  - 기하급수
  - Geometric Series
  - 조합론
  - Combinatorics
  - 확률론
  - Probability Theory
  - 통계
  - Statistics
  - 수열
  - Sequence
  - 최적화
  - Optimization
  - 분수 계산
  - Fraction Calculation
  - 역원 계산
  - Inverse Calculation
image: wordcloud.png
---

## 문제 요약

**문제 링크**: [https://www.acmicpc.net/problem/13182](https://www.acmicpc.net/problem/13182)

특정 빨간색(R개), 초록색(G개), 파란색(B개) 제비를 통에 넣고 차례로 뽑을 때:
- 빨간 제비: 버림
- 초록 제비: 다시 넣음
- 파란 제비: 다시 넣음 (K번 뽑으면 멈춤)

**요구사항**: 잠을 자러 갈 때까지 뽑게 될 제비 개수의 기댓값을 (a × b^(-1)) mod 10^9+7로 출력

**제한 사항**: 1 ≤ R, G, B, K ≤ 10^9, 1 ≤ T ≤ 10^3

## 입출력 예제

**입력 1:**
```
4
1 1 1 1
1 2 3 4
1000 1000 1 1000
50000 50000 50000 10000000
```

**출력 1:**
```
500000006
569010428
490804548
595034885
```

**설명**: 첫 번째 테스트 케이스는 5/2를 의미합니다.

## 접근 개요

### 핵심 관찰

상태를 "남은 빨간 제비 개수"와 "아직 뽑아야 할 파란 제비 개수"로 정의합니다.

**E(r, k)** = r개의 빨간 제비가 남아있고 k번 더 파란 제비를 뽑아야 할 때의 기댓값

### 점화식 유도

한 번의 뽑기에서:
- 빨간색 확률: r/(r+g+b) → 1번 뽑고 상태 E(r-1, k)
- 초록색 확률: g/(r+g+b) → 1번 뽑고 상태 E(r, k)
- 파란색 확률: b/(r+g+b) → 1번 뽑고 상태 E(r, k-1)

```
E(r, k) = 1 + (r/(r+g+b)) × E(r-1, k) 
            + (g/(r+g+b)) × E(r, k)
            + (b/(r+g+b)) × E(r, k-1)
```

정리하면:
```
E(r, k) = (r+g+b)/b × (1 + r/(r+g+b) × E(r-1, k) + g/(r+g+b) × E(r-1, k-1))
```

재귀적으로 풀면:
```
E(R, K) = R × (1 - (B/(B+1))^K) + K×(G+B)/B
```

### 수식 증명

**기저 단계**: E(0, k) = k × (G+B) / B

**귀납 단계**: 위 공식이 E(R, K) = Σ[i=0 to K-1] ((1 - (B/(B+1))^(i+1)) × R/(i+1)) + ... 의 기하급수로 표현될 수 있음을 보일 수 있습니다.

## 알고리즘 설계

### 수식 계산

1. **비율 계산**: ratio = B / (B+1) (mod p에서 modular inverse 사용)
2. **거듭제곱**: ratio^K 계산 (fast exponentiation)
3. **첫 항**: term1 = R × (1 - ratio^K)
4. **두 번째 항**: term2 = K × (G+B) / B
5. **최종 답**: (term1 + term2) mod p

### 모듈로 연산

- 페르마의 소정리: a^(p-1) ≡ 1 (mod p) ⟹ a^(-1) ≡ a^(p-2) (mod p)
- 거듭제곱 지수: exp mod (p-1) 적용
- 모든 나눗셈은 modular inverse 사용

## 복잡도

- **시간 복잡도**: O(T × log K) - 각 테스트마다 fast exponentiation
- **공간 복잡도**: O(1)

## 구현

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1e9 + 7;

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

long long inv(long long a) {
    return power(a, MOD - 2, MOD);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T;
    cin >> T;
    
    while (T--) {
        long long R, G, B, K;
        cin >> R >> G >> B >> K;
        
        // E(R, K) = R * (1 - (B/(B+1))^K) + K*(G+B)/B
        
        long long K_exp = K % (MOD - 1);  // 페르마 소정리: 지수는 (p-1)로 나눈 나머지
        long long K_mod = K % MOD;
        R %= MOD;
        G %= MOD;
        long long B_mod = B % MOD;
        
        long long B_plus_1 = (B_mod + 1) % MOD;
        long long ratio = B_mod * inv(B_plus_1) % MOD;
        long long ratio_K = power(ratio, K_exp, MOD);
        long long G_plus_B = (G + B_mod) % MOD;
        
        // R * (1 - ratio_K) + K*(G+B)/B
        long long term1 = R * ((1 - ratio_K + MOD) % MOD) % MOD;
        long long term2 = K_mod * G_plus_B % MOD * inv(B_mod) % MOD;
        
        long long ans = (term1 + term2) % MOD;
        cout << ans << '\n';
    }
    
    return 0;
}
```

## 코너 케이스 체크리스트

- **K = 1**: 파란 제비를 한 번만 뽑는 경우
  - 기댓값 = (R+G+B) / B
  
- **R = 0**: 빨간 제비가 없는 경우
  - 기댓값 = K × (G+B) / B (상수)
  
- **G = 0**: 초록 제비가 없는 경우
  - 기댓값 = R × (1 - (B/(B+1))^K) + K
  
- **G = B = 1000000000, K = 10000000**: 최대 입력
  - 모듈로 연산과 거듭제곱 오버플로우 주의

## 제출 전 점검 목록

- [ ] modular inverse 계산 정확성 (Fermat's Little Theorem)
- [ ] 거듭제곱 지수를 (MOD-1)로 나눔 확인
- [ ] 각 변수가 long long 타입 (10^9 초과 가능)
- [ ] 음수 mod 처리: (1 - ratio_K + MOD) % MOD
- [ ] 모든 곱셈/덧셈에 mod 적용

## 참고자료

- **Fermat's Little Theorem**: 소수 p에 대해 a^(p-1) ≡ 1 (mod p)
- **Modular Inverse**: a × a^(-1) ≡ 1 (mod p)
- **기하급수**: Σ x^i = (1 - x^(n+1)) / (1 - x)

## 유사 문제

- BOJ 10994: 별 찍기 - 19
- BOJ 13926: gcd(n, k) = 1
- BOJ 1722: 순열의 순서

---

**성공적인 제출을 위한 최종 팁:**

1. 입력 크기가 10^9이므로 모든 수를 MOD로 정규화
2. 거듭제곱에서 지수도 (MOD-1)로 나눔 (Fermat's little theorem)
3. 결과 분수를 (분자 × 분모의 역원) % MOD로 계산
4. 음수 mod 결과 처리 시 +MOD 후 mod 연산

