---
title: "[Algorithm] CPP 백준 6567번: 팔찌"
description: "팔찌의 고유한 개수를 구하는 조합론 문제. Burnside의 보조정리와 오일러 파이 함수를 활용하여 회전과 뒤집기 대칭을 처리하는 Polya 열거 정리 풀이입니다. 조합 게임 이론의 핵심 개념을 학습할 수 있습니다."
categories:
- Algorithm
- Combinatorics
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-6567
- CPP
- C++
- Combinatorics
- 조합론
- Polya-Enumeration
- 폴리아열거정리
- Burnside-Lemma
- 번사이드보조정리
- Euler-Phi
- 오일러파이
- Symmetric-Group
- 대칭군
- Rotation-Symmetry
- 회전대칭
- Reflection-Symmetry
- 뒤집기대칭
- Bead-Necklace
- 팔찌목걸이
- Counting-Problems
- 계산문제
- Implementation
- 구현
- Time-Complexity
- 시간복잡도
- Space-Complexity
- 공간복잡도
- Competitive-Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Mathematical-Proof
- 수학증명
- Number-Theory
- 정수론
- Divisor
- 약수
- Coprimality
- 서로소
- Group-Theory
- 군론
- Mathematical-Game
- 수학게임
- Brute-Force
- 완전탐색
- Formula-Derivation
- 공식유도
- Symmetry-Breaking
- 대칭깨기
- Combinatorial-Structure
- 조합구조
- Discrete-Mathematics
- 이산수학
- Problem-Solving
- 문제해결
date: 2025-12-03
lastmod: 2025-12-03
image: "wordcloud.png"
---

## 문제 정보

더 많은 정보는 42jerrykim.github.io 에서 확인하세요.

- **문제 링크**: https://www.acmicpc.net/problem/6567
- **난이도**: Gold 2
- **카테고리**: 조합론, 수학, Polya 열거 정리

### 문제 요약

"Let it Bead" 회사는 c가지 색상의 비드로 길이 s인 팔찌를 만듭니다. 팔찌는 다음의 특징을 가집니다:

- 고리 형태로 시작과 끝이 없음
- 방향성이 없음 (회전 + 뒤집기 가능)
- 모든 색상의 비드를 무한정 사용 가능

각 테스트 케이스마다 만들 수 있는 **서로 다른 팔찌의 개수**를 구하는 문제입니다. 고유함을 판정할 때, 회전과 뒤집기로 같아지는 팔찌는 동일한 것으로 간주합니다.

**제한 조건**:
- c, s ≥ 1
- c·s ≤ 32 (c와 s의 곱이 32 이하)

### 입출력 형식

**입력**: 각 줄에 두 정수 c (색상 수), s (팔찌 길이)
- 입력은 c = s = 0일 때 종료

**출력**: 각 테스트 케이스마다 만들 수 있는 고유한 팔찌의 개수

### 예제

**입력**:
```
1 1
2 1
2 2
5 1
2 5
2 6
6 2
0 0
```

**출력**:
```
1
2
3
5
8
13
21
```

**예제 설명**:
- (1,1): 색 1개, 길이 1 → 1개 팔찌
- (2,1): 색 2개, 길이 1 → 색상 0 또는 1 → 2개 팔찌
- (2,2): 색 2개, 길이 2 → {0,0}, {1,1}, {0,1} (회전/뒤집기 동일) → 3개 팔찌
- (2,5): 색 2개, 길이 5 → 8개 팔찌

## 접근 개요

이 문제의 핵심은 **대칭을 고려한 색칠 개수 세기**입니다. 단순히 c^s를 하면 모든 경우를 세지만, 회전과 뒤집기로 동일한 것들이 여러 번 중복 계산됩니다.

**Burnside의 보조정리**를 사용하면:
- 대칭 그룹의 크기: 2s (회전 s개 + 뒤집기 s개)
- 각 대칭 변환에 대해 불변인 색칠 개수를 구함
- 평균 = (모든 변환에 대한 불변 색칠 수의 합) / (그룹 크기)

```
팔찌의 고유 개수 = (회전 불변 색칠 합 + 뒤집기 불변 색칠 합) / (2 × s)
```

### 회전 대칭 분석

길이 s인 팔찌를 k칸 회전시킬 때 불변이려면, 색 패턴이 gcd(k, s) 길이의 주기를 가져야 합니다.

d = gcd(k, s)라 하면, s/d개의 독립적인 주기 패턴이 있으므로:
- 불변인 색칠 수 = c^(s/d)

모든 회전에 대한 합:
```
Σ (k=0 to s-1) c^(gcd(k,s)) = Σ (d|s) φ(d) × c^(s/d)
```
여기서 φ는 **오일러 파이 함수**입니다.

### 뒤집기 대칭 분석

팔찌를 뒤집을 때 불변이려면 좌우 대칭이어야 합니다.

**s가 홀수인 경우**:
- 각 뒤집기 축은 정확히 1개의 비드를 지남
- 축 위의 비드: 1개 (고정)
- 양쪽 대칭 위치의 비드: (s-1)/2쌍
- 불변 색칠: c^((s+1)/2)
- s개 축 모두에 대해: s × c^((s+1)/2)

**s가 짝수인 경우**:
- **비드를 지나는 축** (s/2개): 고정된 비드 2개 + (s-2)/2쌍 → c^(s/2+1)
- **비드 사이를 지나는 축** (s/2개): s/2쌍만 있음 → c^(s/2)
- 합계: (s/2) × c^(s/2+1) + (s/2) × c^(s/2)

## 알고리즘 설계

1. **오일러 파이 함수 계산**: φ(n)을 소인수분해로 구함
2. **회전 대칭 처리**: s의 모든 약수 d에 대해 φ(d) × c^(s/d) 계산
3. **뒤집기 대칭 처리**: s의 홀짝성에 따라 경우 분류
4. **Burnside 공식 적용**: (회전 합 + 뒤집기 합) / (2s)

### 의사코드

```
1. rotation_sum = 0
   for each divisor d of s:
       rotation_sum += phi(d) * c^(s/d)

2. if s is odd:
       reflection_sum = s * c^((s+1)/2)
   else:
       reflection_sum = (s/2) * (c^(s/2+1) + c^(s/2))

3. result = (rotation_sum + reflection_sum) / (2 * s)
```

## 복잡도 분석

- **시간 복잡도**: O(√s + d(s) × log s)
  - φ(n) 계산: O(√s)
  - s의 약수 개수: d(s) ≤ 32 (충분히 작음)
  - 각 약수마다 거듭제곱: O(log s)

- **공간 복잡도**: O(1)

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
using namespace std;

// 오일러 파이 함수: n 이하의 n과 서로소인 양의 정수 개수
long long phi(long long n) {
    long long result = n;
    for (long long p = 2; p * p <= n; p++) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}

// c^k 계산
long long power(long long c, long long k) {
    long long result = 1;
    for (long long i = 0; i < k; i++) {
        result *= c;
    }
    return result;
}

int main() {
    long long c, s;
    while (cin >> c >> s) {
        if (c == 0 && s == 0) break;
        
        // 1. 회전 대칭: Σ φ(d) × c^(s/d) (d는 s의 약수)
        long long rotation = 0;
        for (long long d = 1; d <= s; d++) {
            if (s % d == 0) {
                rotation += phi(d) * power(c, s / d);
            }
        }
        
        // 2. 뒤집기 대칭
        long long reflection = 0;
        if (s % 2 == 1) {
            // s가 홀수: s개 축, 각각 c^((s+1)/2) 고정점
            reflection = s * power(c, (s + 1) / 2);
        } else {
            // s가 짝수:
            // - s/2개 축이 비드를 지남: c^(s/2+1)
            // - s/2개 축이 비드 사이를 지남: c^(s/2)
            reflection = (s / 2) * (power(c, s / 2 + 1) + power(c, s / 2));
        }
        
        // Burnside의 보조정리
        long long result = (rotation + reflection) / (2 * s);
        cout << result << endl;
    }
    return 0;
}
```

### Python 구현

```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
def phi(n):
    """오일러 파이 함수"""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def solve(c, s):
    # 회전 대칭
    rotation = 0
    d = 1
    while d * d <= s:
        if s % d == 0:
            rotation += phi(d) * (c ** (s // d))
            if d != s // d:
                rotation += phi(s // d) * (c ** d)
        d += 1
    
    # 뒤집기 대칭
    if s % 2 == 1:
        reflection = s * (c ** ((s + 1) // 2))
    else:
        reflection = (s // 2) * ((c ** (s // 2 + 1)) + (c ** (s // 2)))
    
    return (rotation + reflection) // (2 * s)

while True:
    c, s = map(int, input().split())
    if c == 0 and s == 0:
        break
    print(solve(c, s))
```

## 검증

예제 (2, 5) 검증:

**회전**:
- φ(1)=1, φ(5)=4
- rotation = 1×2^5 + 4×2^1 = 32 + 8 = 40

**뒤집기** (5는 홀수):
- reflection = 5 × 2^3 = 40

**결과**: (40 + 40) / 10 = 8 ✓

## 코너 케이스 체크리스트

- ✓ s=1: φ(1)=1 → 계산 정상
- ✓ c=1: 모든 비드가 같은 색 → 결과는 항상 1
- ✓ 큰 s: c^(s/2)가 32 이하로 제한되므로 오버플로우 없음
- ✓ 소수 vs 합성수 s: 약수 계산이 일반적으로 처리됨

## 제출 전 점검

- ✓ 입력 0 0에서 종료
- ✓ 오일러 파이 함수 소인수분해 정확성
- ✓ 회전/뒤직기 경우 분류 정확성
- ✓ 정수 나눗셈 (2*s로 정확히 나누어떨어짐)
- ✓ 거듭제곱 계산 (오버플로우 검토)

## 참고자료

- **Burnside의 보조정리**: https://en.wikipedia.org/wiki/Burnside%27s_lemma
- **Polya 열거 정리**: https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem
- **오일러 파이 함수**: https://en.wikipedia.org/wiki/Euler%27s_totient_function
- **유사 문제**: BOJ 1593 (육각형), BOJ 2110 (목걸이)

---

