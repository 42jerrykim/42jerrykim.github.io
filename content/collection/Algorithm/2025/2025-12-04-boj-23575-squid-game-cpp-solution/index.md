---
title: "[Algorithm] C++ 백준 23575번: Squid Game"
lastmod: 2025-12-04
date: 2025-12-04
description: "세 물통 중 하나를 비우는 문제를 유클리드 호제법과 이진수 표현으로 해결합니다. 이진 비트 기반으로 각 단계의 붓기 연산을 결정하여 최대 1000번 이내에 빠르게 도달합니다."
categories:
  - Algorithm
  - Math
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-23575
  - Squid Game
  - 오징어 게임
  - C++
  - CPP
  - CPlusPlus
  - Euclidean Algorithm
  - 유클리드 호제법
  - GCD
  - 최대공약수
  - Binary Representation
  - 이진수 표현
  - Bitmask
  - 비트마스크
  - Math
  - 수학
  - Number Theory
  - 정수론
  - Constructive
  - 구성적
  - Simulation
  - 시뮬레이션
  - Implementation
  - 구현
  - Problem Solving
  - 문제해결
  - Competitive Programming
  - 경쟁프로그래밍
  - Water Pouring
  - 물붓기
  - Bucket Problem
  - 물통 문제
  - Puzzle
  - 퍼즐
  - Greedy
  - 탐욕법
  - Division Algorithm
  - 나눗셈 알고리즘
  - Modulo Operation
  - 모듈러 연산
  - Recursive Pattern
  - 재귀적 패턴
  - Iterative Solution
  - 반복적 해법
  - Edge Cases
  - 엣지 케이스
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Vector
  - 벡터
  - Pair
  - 페어
  - Sorting
  - 정렬
  - Sorting Algorithm
  - 정렬 알고리즘
  - Comparator
  - 비교기
  - Structure
  - 구조체
  - ICPC
  - 국제대학생프로그래밍대회
  - Regionals
  - 지역본선
  - Asia Pacific
  - Asia Regional
  - Seoul 2021
  - 서울 2021
  - Korea Regional
  - 한국 지역본선
  - Constructive Algorithm
  - 구성 알고리즘
  - Logic
  - 논리
  - Optimization
  - 최적화
  - Strategy
  - 전략
  - Verification
  - 검증
  - Code Review
  - 코드리뷰
  - Testing
  - 테스트
  - Integer Overflow
  - 정수 오버플로우
  - Long Long
  - 64비트 정수
  - Input Output
  - 입출력
  - Editorial
  - 에디토리얼
image: "wordcloud.png"
---

## 문제 요약

**문제 링크**: [https://www.acmicpc.net/problem/23575](https://www.acmicpc.net/problem/23575)

세 개의 물통에 각각 $X, Y, Z$ 리터의 물이 있습니다. 한 물통에서 다른 물통으로 붓는 연산을 수행하되, 규칙에 따라 받는 물통의 양을 정확히 두 배로 만들어야 합니다. 최대 1000번 이내에 한 물통을 완전히 비워야 합니다.

**입출력 형식:**

```
입력: X Y Z
출력: 
  m (붓기 연산 수)
  A B (각 연산: 물통 A에서 물통 B로 붓기)
  ...
```

**예제:**

| 입력 | 출력 |
|------|------|
| 1 2 3 | 2<br>3 2<br>2 3<br>1 1 |
| 1 4 6 | 3<br>2 1<br>3 1<br>1 1<br>3 1 |

## 접근 개요

### 핵심 관찰

이 문제는 **유클리드 호제법**과 **이진수 표현**을 결합한 구성적 알고리즘입니다.

1. **유클리드 호제법 유추**: 세 물통을 크기순으로 $A \le B \le C$로 정렬하면, $B$를 $A$로 나눈 몫과 나머지를 이용하여 문제를 축소할 수 있습니다.

2. **이진 분해**: $B = qA + r$ (단, $q = \lfloor B/A \rfloor$)일 때, $q$를 이진수로 표현하면:
   - 비트 1: $B$에서 $A$로 붓기 (B 감소)
   - 비트 0: $C$에서 $A$로 붓기 (B 유지, A 증가)

3. **반복**: 이 과정을 반복하면 한 물통이 0이 되는 순간이 반드시 옵니다.

### 알고리즘 핵심 로직

```
while any bucket is non-zero:
  Sort buckets: A ≤ B ≤ C
  if A = 0: DONE
  
  q = B / A
  for each bit in q (from LSB):
    if bit = 1:
      pour(B → A)  // B -= A, A *= 2
    else:
      pour(C → A)  // C -= A, A *= 2
```

## 복잡도 분석

- **시간복잡도**: $O(\log \min(X, Y, Z)^2)$  
  - 유클리드 호제법처럼 빠르게 수렴하므로 최대 1000번 이내
  - 각 단계에서 정렬: $O(\log \text{iteration})$

- **공간복잡도**: $O(m)$ (m은 붓기 연산 수)

## 구현

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct Bucket {
    long long amount;
    int index;
};

vector<pair<int, int>> result_moves;

void pour(Bucket& from, Bucket& to) {
    result_moves.push_back({from.index, to.index});
    from.amount -= to.amount;
    to.amount *= 2;
}

bool compareBuckets(const Bucket& a, const Bucket& b) {
    return a.amount < b.amount;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    vector<Bucket> buckets(3);
    for (int i = 0; i < 3; ++i) {
        cin >> buckets[i].amount;
        buckets[i].index = i + 1;
    }

    while (true) {
        sort(buckets.begin(), buckets.end(), compareBuckets);

        if (buckets[0].amount == 0) break;

        // A = buckets[0], B = buckets[1], C = buckets[2]
        long long q = buckets[1].amount / buckets[0].amount;
        
        while (q > 0) {
            if (q % 2 == 1) {
                pour(buckets[1], buckets[0]);
            } else {
                pour(buckets[2], buckets[0]);
            }
            q /= 2;
        }
    }

    cout << result_moves.size() << "\n";
    for (const auto& move : result_moves) {
        cout << move.first << " " << move.second << "\n";
    }

    return 0;
}
```

## 정당성 증명

### 종료 조건

- 유클리드 호제법의 성질에 의해, 매 반복마다 최소 한 물통의 양이 감소합니다.
- 물통의 양은 항상 음이 아닌 정수이므로, 유한 번의 반복 후 반드시 한 물통이 0이 됩니다.
- 최악의 경우도 약 $\log \max(X, Y, Z)$ 정도의 반복으로 수렴하므로 1000번 이내입니다.

### 이진 분해의 정확성

$q$의 각 비트는 "몇 배를 부을 것인가"를 나타냅니다:
- 비트 1 ($k$번째): $A$를 $2^k$배로 만들면서, $B$에서 정확히 한 번 붓습니다.
- 비트 0: $C$의 충분한 물로 $A$만 키워서 비트 건너뛰기를 구현합니다.
- $C \ge B$이므로 항상 충분한 물이 있습니다.

## 코너 케이스 체크리스트

| 케이스 | 설명 | 처리 |
|--------|------|------|
| X = Y = Z | 모두 같은 경우 | 첫 붓기로 바로 한 물통이 0 |
| X = 1 | 최소 단위 | 이진 분해가 최대 길이 |
| Z = 10^9 | 최대값 | 64비트 정수로 안전 처리 |
| 큰 몫 | q가 매우 큼 | 이진 표현이 길어도 복잡도 유지 |

## 제출 전 점검

- [ ] 정렬 후 인덱스 업데이트 확인
- [ ] 이진 분해 시 `q /= 2` 누락 확인
- [ ] 벡터 초기화 및 리셋 확인
- [ ] 오버플로우: `long long` 사용 확인
- [ ] 출력 형식: 수 + 각 연산 쌍 확인
