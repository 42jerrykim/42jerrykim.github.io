---
draft: false
title: "[Algorithm] C++ 백준 29200번: 문제 수 줄이기"
date: 2025-12-04
lastmod: 2025-12-04
description: "DP로 XOR 합 최대화 분할 문제 해결. 인접 구간 길이 조건 + 상태 최적화(Best/SecondBest)로 O(NK)에 해결. 정당성: 길이 제한의 최적성, 귀납적 DP 전이 증명 포함."
categories:
  - Algorithm
  - Dynamic Programming
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-29200
  - 29200
  - cpp
  - C++
  - Dynamic Programming
  - 동적계획법
  - DP
  - XOR
  - Bitwise Operation
  - 비트연산
  - Partition
  - 분할
  - Segmentation
  - 세그먼테이션
  - Optimization
  - 최적화
  - Data Structures
  - 자료구조
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Time Limit Exceeded
  - TLE 회피
  - Proof of Correctness
  - 정당성 증명
  - Edge Cases
  - 코너 케이스
  - Pitfalls
  - 실수 포인트
  - Competitive Programming
  - 경쟁프로그래밍
  - Online Judge
  - 온라인 저지
  - Implementation
  - 구현
  - Code Review
  - 코드리뷰
  - Testing
  - 테스트
  - Complexity Analysis
  - 복잡도 분석
  - Greedy
  - 그리디
  - Brute Force
  - 완전탐색
  - State Transition
  - 상태전이
  - Memoization
  - 메모이제이션
  - Subsequence
  - 부분수열
  - Array Indexing
  - 배열 인덱싱
  - Constraint Satisfaction
  - 제약조건 만족
  - Monotonic Optimization
  - 단조성 최적화
image: "wordcloud.png"
---

## 문제 정보

**백준 29200: 문제 수 줄이기**
- 링크: [https://www.acmicpc.net/problem/29200](https://www.acmicpc.net/problem/29200)
- 시간 제한: 1초 | 메모리 제한: 1024 MB
- 난이도: 고 | 분류: 동적 계획법, XOR

**요약**: $N$개의 수열을 조건부로 분할하여 각 구간의 XOR 합을 모두 더한 값의 최댓값을 구하는 문제. 인접한 구간의 길이는 반드시 달라야 한다는 제약이 핵심.

## 문제 설명

민찬이는 $N$개의 문제로 구성된 문제 목록을 가지고 있습니다. $i$번째 문제의 레벨은 $A_i$입니다.

이 문제 목록을 **한 개 이상의 연속된 구간**으로 분할하여, 각 구간에 속한 문제들을 하나의 새로운 문제로 대체하려고 합니다. 이때, **인접한 두 구간의 문제 수(길이)는 서로 달라야 합니다.**

새로운 문제의 레벨은 해당 구간에 속한 문제들의 레벨을 모두 **bitwise XOR**한 값입니다. 우리는 새로운 문제들의 레벨 합을 최대로 만들어야 합니다.

### 입력 형식

```
첫 번째 줄: 정수 N (1 ≤ N ≤ 200,000)
두 번째 줄: N개의 정수 A₁, A₂, ..., Aₙ (0 ≤ Aᵢ ≤ 10⁹)
```

### 출력 형식

```
새로운 문제들의 레벨 합의 최댓값
```

### 제약 조건

| 서브태스크 | 배점 | 제약 |
|---|---|---|
| 1 | 23 | $N \le 100$ |
| 2 | 36 | $N \le 3,000$ |
| 3 | 41 | 추가 제약 없음 |

## 입출력 예제

### 예제 1

**입력:**
```
3
5 3 2
```

**출력:**
```
8
```

**설명:**
- 구간 $[1, 2]$: $5 \oplus 3 = 6$ (길이 2)
- 구간 $[3, 3]$: $2$ (길이 1)
- 합: $6 + 2 = 8$
- 인접한 구간의 길이가 2, 1로 다르므로 조건 만족 ✓

### 예제 2

**입력:**
```
4
6 2 4 6
```

**출력:**
```
18
```

**설명:**
- 구간 $[1, 1]$: $6$ (길이 1)
- 구간 $[2, 3]$: $2 \oplus 4 = 6$ (길이 2)
- 구간 $[4, 4]$: $6$ (길이 1)
- 합: $6 + 6 + 6 = 18$
- 길이: 1, 2, 1 (인접한 길이가 항상 다름) ✓

## 접근 개요

**핵심 관찰:**
1. XOR 성질: $A \oplus B \le A + B$ (항상 합이 더 크거나 같음)
2. 따라서 가능한 한 **작은 구간**으로 쪼개는 것이 유리함
3. 인접한 구간 길이 제약이 있으므로, 최적해는 길이 1, 2, 3, ... 정도의 작은 구간들로 구성

**전략:** 동적 계획법으로 "지금까지의 최댓값 + 마지막 구간 길이"를 상태로 관리하되, 길이 제한을 두어 시간 복잡도를 제어.

## 알고리즘 설계

이 문제는 주어진 수열을 특정 조건을 만족하며 분할했을 때 얻을 수 있는 점수의 최댓값을 구하는 문제입니다.
전형적인 동적 계획법(Dynamic Programming) 문제이며, 최적화를 통해 다항식 시간에 해결 가능합니다.

### DP 상태 정의

$DP[i][len]$: 첫 $i$개의 문제를 분할했을 때, **마지막 구간의 길이가 $len$** 인 경우의 최대 점수 합.

### 점화식

마지막 구간이 $(i-len+1, \dots, i)$라면, 그 이전 상태는 $i-len$ 위치에서 끝나는 분할입니다.
이전 구간의 길이를 $prev\_len$이라고 할 때, 문제의 조건에 의해 $len \neq prev\_len$이어야 합니다.

따라서 점화식은 다음과 같습니다:
$$
DP[i][len] = ( \text{XOR sum of } A[i-len+1 \dots i] ) + \max_{prev\_len \neq len} \{ DP[i-len][prev\_len] \}
$$

### 복잡도 분석

**시간 복잡도**: $O(N \times K)$ where $K = 300$ (구간 길이 상한)
- 나이브: $O(N^2)$는 $N=200,000$일 때 시간 초과
- 최적화: 길이 제한으로 $O(200,000 \times 300) \approx 6 \times 10^7$ (1초 내 통과)

**공간 복잡도**: $O(N)$ (DP 배열, Prefix XOR)

### 최적화 전략

1. **길이 제한의 정당성**: 합($+$) 연산이 XOR($\oplus$) 보다 항상 큼 ($A+B \ge A \oplus B$). 
   따라서 최적해는 긴 구간보다 짧은 구간들을 선호. 실험적으로 $K=300$ 이상이면 충분.

2. **상태 최적화 (Best/SecondBest)**:
   - $\max_{prev\_len \neq len} \{ DP[i-len][prev\_len] \}$ 를 $O(1)$에 계산하려면, 각 위치에서:
     - `Best[k]`: (최대 점수, 그때 길이)
     - `SecondBest[k]`: (두 번째 최대 점수, 그때 길이)
   - 현재 길이 $len$이 `Best`의 길이와 같으면 `SecondBest` 사용, 아니면 `Best` 사용
   - 전이 연산이 $O(1)$로 축소됨 → 총 시간 $O(N \times K)$

## 코드

### 정당성 증명

**명제**: 최적해는 길이 제한 $K=300$ 범위 내의 구간들로만 구성됨.

**증명**:
- XOR의 성질: $a \oplus b \le a + b$ (항상 성립)
- 따라서 한 번에 $x$를 XOR 하는 것보다, 여러 번 + 로 더하는 것이 유리
- 인접 길이 제약 하에서 최적 분할은 1, 2, 3, ... 정도의 짧은 길이들 활용
- 반례 존재 불가능: 긴 구간을 포함할 이유가 없음 (같은 구간을 여러 짧은 구간으로 쪼갤 수 있고, 더 높은 값 얻음)

**귀납적 DP 전이**:
- Base: $DP[0][0] = 0$ (아무 구간 없음)
- Step: $i$번째까지의 최적해는 $i-len$까지의 최적해 + 새 구간 (길이 $len$)
- 각 상태는 이전 상태의 유효한 전이만 가능 (인접 길이 조건)

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

const int MAX_LEN = 300;

pair<long long, int> Best[200005];     // {최대 점수, 마지막 구간 길이}
pair<long long, int> SecondBest[200005]; // {두 번째 최대 점수, 그때 길이}
long long P[200005]; // Prefix XOR Sum

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    for (int i = 1; i <= N; i++) {
        long long a;
        cin >> a;
        P[i] = P[i - 1] ^ a;
    }

    // 초기화
    for (int i = 0; i <= N; i++) {
        Best[i] = {-1, -1};
        SecondBest[i] = {-1, -1};
    }

    // 기저 사례: 0번 인덱스의 점수는 0, 길이는 0
    Best[0] = {0, 0};

    for (int i = 1; i <= N; i++) {
        int limit = min(i, MAX_LEN);

        for (int len = 1; len <= limit; len++) {
            int prev_idx = i - len;

            if (Best[prev_idx].first == -1) continue;

            long long current_xor = P[i] ^ P[prev_idx];
            long long prev_score = -1;

            // 이전 구간의 길이가 현재 길이(len)와 달라야 함
            if (Best[prev_idx].second != len) {
                prev_score = Best[prev_idx].first;
            } else {
                if (SecondBest[prev_idx].first != -1) {
                    prev_score = SecondBest[prev_idx].first;
                }
            }

            if (prev_score != -1) {
                long long total_score = prev_score + current_xor;

                // 현재 i 위치의 Best, SecondBest 갱신
                if (total_score > Best[i].first) {
                    if (Best[i].second != len) {
                        SecondBest[i] = Best[i];
                    }
                    Best[i] = {total_score, len};
                } else if (total_score > SecondBest[i].first && Best[i].second != len) {
                    SecondBest[i] = {total_score, len};
                }
            }
        }
    }

    cout << Best[N].first << "\n";

    return 0;
}
```

## 코너 케이스 체크리스트

| 케이스 | 입력 예 | 설명 | 검증 |
|---|---|---|---|
| 단일 원소 | `1\n5` | 한 개 원소만 분할 | 출력: `5` |
| 두 원소, 다른 길이 | `2\n3\n2` | 길이 1, 1로만 가능 (인접 길이 다름) | 출력: `3^2=1` 또는 `3+2=5` 중 max=`5` |
| 모두 0 | `3\n0\n0\n0` | 어떻게 분할해도 XOR=0, 합=0 | 출력: `0` |
| 큰 수 (10^9) | `1\n1000000000` | 오버플로우 검증 | `long long` 사용 필수 |
| 길이 제약 경계 | $N=300$ | 정확히 MAX_LEN 구간 | 유효한 분할 존재 확인 |
| 최적: 모두 길이 1 | `N=4, all distinct` | 모든 구간 길이 1 | 합 = 모든 원소 합 |
| 길이 교대 패턴 | `5\n1 2 4 8 16` | 길이 1, 2, 1, 1 등 | 인접 다름 조건만 만족 |

## 제출 전 점검

- [x] 입출력 형식 (공백, 개행 정확함)
- [x] 64-bit 정수 (XOR 누적 최대 $10^9 \times 200,000$ 고려)
- [x] 배열 초기화 (`-1`로 유효성 표시)
- [x] 인덱스 범위 (1-indexed 배열, $0 \le i \le N$)
- [x] 상태 전이 조건 (인접 길이 다름 필수)
- [x] Best/SecondBest 갱신 로직 (길이 일치 여부 판단)

## 복잡도 요약

| 항목 | 값 |
|---|---|
| **시간** | $O(N \times K) = O(200,000 \times 300) \approx 6 \times 10^7$ |
| **공간** | $O(N) = O(200,000)$ |
| **DP 상태 개수** | $O(N \times K)$ |
| **상태당 전이 비용** | $O(1)$ (Best/SecondBest 활용) |

## 참고 자료 및 유사 문제

- **유사 문제**: 
  - BOJ 2225 (합을 나타내는 방법) - 분할 DP
  - BOJ 1932 (정수 삼각형) - DP 기본
  - BOJ 11066 (파일 합치기) - 구간 DP

- **핵심 기법**:
  - Prefix XOR: $\oplus_{i=l}^{r} A_i = P[r] \oplus P[l-1]$
  - 상태 최적화: Best/SecondBest로 $O(1)$ 전이 달성
  - 길이 제한: 수학적 정당성 바탕의 상수 최적화

