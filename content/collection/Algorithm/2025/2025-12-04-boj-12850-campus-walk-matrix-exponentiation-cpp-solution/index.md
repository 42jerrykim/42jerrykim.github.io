---
title: "[Algorithm] C++ 백준 12850번 본대 산책2"
description: "정보과학관에서 출발하여 D분 후 다시 돌아오는 경로의 수를 행렬 거듭제곱으로 O(8^3 log D)에 계산합니다. 인접 행렬의 D제곱에서 (0,0) 원소가 정답입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Graph
  - Matrix Exponentiation
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-12850
  - 본대 산책2
  - Campus Walk
  - 행렬 거듭제곱
  - Matrix Exponentiation
  - Matrix Power
  - 그래프
  - Graph
  - 인접 행렬
  - Adjacency Matrix
  - 경로 수
  - Path Counting
  - 분할 정복
  - Divide and Conquer
  - 빠른 거듭제곱
  - Fast Exponentiation
  - 모듈러 연산
  - Modular Arithmetic
  - 모듈로 연산
  - Modulo Operation
  - C++
  - Programming
  - 프로그래밍
  - 경쟁프로그래밍
  - Competitive Programming
  - 숭실대학교
  - Soongsil University
  - SCCC
  - 시간복잡도
  - Time Complexity
  - 공간복잡도
  - Space Complexity
  - O(log N)
  - 로그 시간
  - Logarithmic Time
  - 정보과학관
  - 전산관
  - 미래관
  - 신양관
  - 한경직기념관
  - 진리관
  - 형남공학관
  - 학생회관
  - 캠퍼스 지도
  - Campus Map
  - 경로 문제
  - Path Problem
  - 그래프 탐색
  - Graph Traversal
  - 정답코드
  - Solution Code
  - Editorial
  - 에디토리얼
  - 수학
  - Mathematics
  - Linear Algebra
  - 선형대수
image: wordcloud.png
---

## 문제 요약

**문제 링크**: [https://www.acmicpc.net/problem/12850](https://www.acmicpc.net/problem/12850)

숭실대학교 캠퍼스에는 8개의 건물이 있고, 서로 인접한 건물 사이를 이동하는 데 1분이 걸립니다. 정보과학관에서 출발하여 정확히 D분 후에 다시 정보과학관으로 돌아오는 경로의 수를 구하는 문제입니다.

**건물 목록:**
- 정보과학관 (시작/도착점)
- 전산관
- 미래관
- 신양관
- 한경직기념관
- 진리관
- 형남공학관
- 학생회관

## 입출력

**입력:**
```
D
```
- D: 산책 시간 (1 <= D <= 1,000,000,000)

**출력:**
```
경로의 수 mod 1,000,000,007
```

**예제:**
```
입력: 100000000
출력: 261245548
```

## 접근 개요

### 핵심 관찰

1. **그래프 모델링**: 캠퍼스를 8개의 정점과 간선으로 이루어진 그래프로 모델링
2. **인접 행렬과 경로 수**: 인접 행렬 A에서 A^D[i][j]는 정점 i에서 j로 정확히 D번 이동하는 경로의 수
3. **행렬 거듭제곱**: D가 최대 10^9이므로 O(log D) 시간에 행렬 거듭제곱 필요

### 캠퍼스 연결 구조

```
정보과학관(0) --- 전산관(1) --- 신양관(3) --- 진리관(5)
    |               |               |               |
미래관(2) -------- + ---------- 한경직(4) ----- 학생회관(7)
                                    |               |
                              형남공학관(6) ---------+
```

**인접 리스트:**
- 정보과학관(0): 전산관(1), 미래관(2)
- 전산관(1): 정보과학관(0), 미래관(2), 신양관(3)
- 미래관(2): 정보과학관(0), 전산관(1), 신양관(3), 한경직기념관(4)
- 신양관(3): 전산관(1), 미래관(2), 한경직기념관(4), 진리관(5)
- 한경직기념관(4): 미래관(2), 신양관(3), 진리관(5), 형남공학관(6)
- 진리관(5): 신양관(3), 한경직기념관(4), 학생회관(7)
- 형남공학관(6): 한경직기념관(4), 학생회관(7)
- 학생회관(7): 진리관(5), 형남공학관(6)

## 알고리즘 설계

### 행렬 거듭제곱 원리

인접 행렬 A에서:
- A[i][j] = 1이면 i와 j가 직접 연결됨
- A^k[i][j] = i에서 j로 정확히 k번 이동하는 경로의 수

**증명 (귀납법):**
- k=1: A^1[i][j] = A[i][j] (정의)
- k->k+1: A^(k+1)[i][j] = sum(A^k[i][m] * A[m][j]) for all m
  - 이는 i에서 m까지 k번 이동 후, m에서 j로 1번 이동하는 모든 경우의 합

### 빠른 거듭제곱

```
power(A, n):
    if n == 1: return A
    if n is even:
        half = power(A, n/2)
        return half * half
    else:
        return A * power(A, n-1)
```

## 복잡도 분석

- **시간 복잡도**: O(8^3 * log D) = O(512 * log D)
  - 행렬 곱셈: O(8^3)
  - 거듭제곱 횟수: O(log D)
- **공간 복잡도**: O(8^2) = O(64) - 행렬 저장

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<vector<ll>> Matrix;

const ll MOD = 1e9 + 7;
const int N = 8;

// 8x8 인접 행렬 (숭실대 캠퍼스)
Matrix adj = {
    {0, 1, 1, 0, 0, 0, 0, 0},  // 정보과학관
    {1, 0, 1, 1, 0, 0, 0, 0},  // 전산관
    {1, 1, 0, 1, 1, 0, 0, 0},  // 미래관
    {0, 1, 1, 0, 1, 1, 0, 0},  // 신양관
    {0, 0, 1, 1, 0, 1, 1, 0},  // 한경직기념관
    {0, 0, 0, 1, 1, 0, 0, 1},  // 진리관
    {0, 0, 0, 0, 1, 0, 0, 1},  // 형남공학관
    {0, 0, 0, 0, 0, 1, 1, 0}   // 학생회관
};

// 행렬 곱셈
Matrix multiply(const Matrix& A, const Matrix& B) {
    Matrix C(N, vector<ll>(N, 0));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
            }
        }
    }
    return C;
}

// 행렬 거듭제곱
Matrix power(Matrix A, ll n) {
    Matrix result(N, vector<ll>(N, 0));
    // 단위 행렬로 초기화
    for (int i = 0; i < N; i++) {
        result[i][i] = 1;
    }
    
    while (n > 0) {
        if (n & 1) {
            result = multiply(result, A);
        }
        A = multiply(A, A);
        n >>= 1;
    }
    
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    ll D;
    cin >> D;
    
    Matrix result = power(adj, D);
    
    // 정보과학관(0)에서 시작하여 정보과학관(0)으로 돌아오는 경로의 수
    cout << result[0][0] << "\n";
    
    return 0;
}
```

## 코너 케이스 체크리스트

| 케이스 | 설명 | 처리 |
|--------|------|------|
| D=1 | 최소 입력 | 정보과학관에서 1분 후 돌아올 수 없음 (0) |
| D=2 | 왕복 가능 | 전산관 왕복 또는 미래관 왕복 (2가지) |
| D=10^9 | 최대 입력 | 행렬 거듭제곱으로 O(log D)에 처리 |
| 홀수 D | 패리티 | 정상 처리 (일부 D에서는 0일 수 있음) |

## 검증 (D=2)

정보과학관(0)에서 시작:
1. 0 -> 1 -> 0 (전산관 왕복)
2. 0 -> 2 -> 0 (미래관 왕복)

총 2가지 경로 -> A^2[0][0] = 2 ✓

## 제출 전 체크

- 모듈로 연산: 모든 곱셈 후 MOD 적용
- 오버플로우: long long 사용
- 행렬 초기화: 인접 행렬 정확히 입력
- 단위 행렬: 거듭제곱 시작 시 항등원 사용
- 비트 연산: n & 1로 홀수 판별

## 관련 개념

### 행렬 거듭제곱 활용 사례

1. **피보나치 수열**: F(n)을 O(log n)에 계산
2. **그래프 경로 수**: 정확히 k번 이동하는 경로 수
3. **선형 점화식**: DP 점화식의 빠른 계산
4. **마르코프 체인**: 상태 전이 확률 계산

## 참고자료

- **SCCC 2016 Summer Contest** - 숭실대학교 프로그래밍 동아리 대회
- **행렬 거듭제곱**: 분할 정복을 이용한 O(log n) 계산
- **그래프 이론**: 인접 행렬과 경로 수의 관계

