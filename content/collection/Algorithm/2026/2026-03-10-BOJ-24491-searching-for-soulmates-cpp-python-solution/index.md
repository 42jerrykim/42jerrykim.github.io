---
title: "[Algorithm] C++ / Python 백준 24491번: Searching for Soulmates"
description: "정수 A를 B로 바꾸는 최소 연산 횟수를 구한다. 연산은 ×2, ÷2(짝수일 때), +1만 가능하다. 최적해는 나눗셈만 → 덧셈만 → 곱셈만 순서임을 이용해 O(log² max(A,B))에 해결한다. USACO 2022 Silver 공식 해설의 관찰을 적용한 C++/Python 정답 코드를 담았다."
date: 2026-03-10
lastmod: 2026-03-10
categories:
- "Algorithm"
- "BOJ"
- "Math"
- "Greedy"
tags:
- Algorithm
- 알고리즘
- BOJ
- Baekjoon
- 백준
- Math
- 수학
- Greedy
- 그리디
- Number-Theory
- 정수론
- Competitive-Programming
- 경쟁프로그래밍
- USACO
- Problem-Solving
- 문제해결
- Coding-Test
- 코딩테스트
- Implementation
- 구현
- Time-Complexity
- 시간복잡도
- Space-Complexity
- 공간복잡도
- Edge-Cases
- 엣지케이스
- Optimization
- 최적화
- C++
- Python
- 파이썬
- Recursion
- 재귀
- Simulation
- 시뮬레이션
- Complexity-Analysis
- 복잡도분석
- Code-Quality
- 코드품질
- Documentation
- 문서화
- Best-Practices
- Pitfalls
- 함정
- Data-Structures
- 자료구조
- Array
- 배열
- Debugging
- 디버깅
- Refactoring
- 리팩토링
- Testing
- 테스트
- Performance
- 성능
- Divide-and-Conquer
- 분할정복
- Modular-Arithmetic
- 모듈러
- Brute-Force
- 완전탐색
- Memoization
image: "wordcloud.png"
---

문제: [BOJ 24491 - Searching for Soulmates](https://www.acmicpc.net/problem/24491)

소의 성격 수 \(A\)를 다른 소의 성격 수 \(B\)와 같게 만들기 위한 **최소 연산 횟수**를 구하는 문제입니다.  
연산은 \(\times 2\), \(\div 2\)(짝수일 때만), \(+1\) 세 가지만 가능합니다.

## 문제 정보

**문제 링크**: [https://www.acmicpc.net/problem/24491](https://www.acmicpc.net/problem/24491)

**문제 요약**:
- \(N\)쌍의 소가 주어지고, 각 쌍마다 첫 번째 소의 성격 \(A\)를 두 번째 소의 성격 \(B\)로 바꿔야 한다.
- 연산: \(\times 2\), \(\div 2\)(\(A\)가 짝수일 때만), \(+1\).
- 각 쌍에 대해 필요한 최소 연산 횟수를 출력한다.

**제한 조건**:
- 시간 제한: 1초
- 메모리 제한: 1024MB
- \(1 \le N \le 10\), \(1 \le A, B \le 10^{18}\)

## 입출력 예제

**입력**:

```text
6
31 13
12 8
25 6
10 24
1 1
997 120
```

**출력**:

```text
8
3
8
3
0
20
```

첫 번째 케이스: \(31 \to 32 \to 16 \to 8 \to 9 \to 10 \to 11 \to 12 \to 13\) (8번).

## 접근 방식

### 핵심 관찰 (USACO 공식 해설)

1. **최적해 구조**: 최적 연산 순서는 **나눗셈만** → **덧셈만** → **곱셈만** 세 단계로 나눌 수 있다. 즉, 곱셈 뒤에 나눗셈이 오는 경우는 최적이 아니다.
2. **곱셈 횟수 \(M\) 고정**: \(B\)의 하위 \(M\)비트를 “제거”한 값 \(\texttt{prefix} = B \gg M\)까지 \(A\)를 줄인 뒤, 덧셈으로 \(\texttt{prefix}\)에 맞추고, 곱셈 \(M\)번과 하위 비트만큼 \(+1\)로 \(B\)를 만든다.
3. **\(M\) 전수 시도**: \(M = 0, 1, \ldots\) 에 대해 \(\texttt{prefix} = B \gg M > 0\)일 때만 비용을 계산하고, 그 중 최솟값이 답이다.

### 알고리즘 (요약)

- \(M\)(곱셈 횟수)을 0부터 올리면서:
  - \(\texttt{prefix} = B \gg M\).
  - \(A\)를 \(\texttt{prefix}\) 이하로 만들기: 홀수면 \(+1\) 후 \(\div 2\), 짝수면 \(\div 2\) 반복. 비용을 \(\texttt{here}\)에 누적.
  - \(\texttt{here} \mathrel{+}= \texttt{prefix} - \texttt{cow}\) (덧셈으로 \(\texttt{prefix}\)까지).
  - \(\texttt{here} \mathrel{+}= M\) (곱셈 횟수).
  - \(\texttt{here} \mathrel{+}= \operatorname{popcount}(B \mathrel{\&} (2^M - 1))\) (하위 \(M\)비트에서 1인 만큼 \(+1\)).
- 위 비용 중 최솟값을 출력.

## 복잡도 분석

| 항목 | 복잡도 | 비고 |
|------|--------|------|
| **시간 복잡도** | \(O(\log^2 \max(A,B))\) | \(M\)이 \(O(\log B)\)개, 각각 \(A\)를 줄이는 루프 \(O(\log A)\) |
| **공간 복잡도** | \(O(1)\) | 상수 개의 변수만 사용 |

## 구현 코드

### C++

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N;
    cin >> N;
    while (N--) {
        long long cow1, cow2;
        cin >> cow1 >> cow2;
        long long answer = LONG_LONG_MAX;
        for (int removed = 0; (cow2 >> removed) > 0; removed++) {
            long long prefix = cow2 >> removed;
            long long here = 0;
            long long cow = cow1;
            while (cow > prefix) {
                if (cow % 2 == 1) {
                    cow++;
                    here++;
                }
                cow /= 2;
                here++;
            }
            here += prefix - cow;
            here += removed;
            here += __builtin_popcountll(cow2 & ((1LL << removed) - 1));
            answer = min(answer, here);
        }
        cout << answer << '\n';
    }
    return 0;
}
```

### Python

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    out = []
    for _ in range(n):
        cow1, cow2 = map(int, input().split())
        answer = float('inf')
        removed = 0
        while cow2 >> removed > 0:
            prefix = cow2 >> removed
            here = 0
            cow = cow1
            while cow > prefix:
                if cow % 2 == 1:
                    cow += 1
                    here += 1
                cow //= 2
                here += 1
            here += prefix - cow
            here += removed
            here += bin(cow2 & ((1 << removed) - 1)).count('1')
            answer = min(answer, here)
            removed += 1
        out.append(str(answer))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()
```

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|--------|------|-----------|
| **A = B** | 이미 같음 | \(M=0\)에서 prefix=B, cow=A=B이면 here = 0 + 0 + 0 = 0 |
| **A &gt; B** | 나눗셈으로만 줄여야 함 | 홀수면 +1 후 /2 반복으로 prefix 이하로 감 |
| **A &lt; B** | 나눗셈 단계 후 덧셈·곱셈으로 B까지 | prefix - cow 와 하위 비트 popcount로 처리 |
| **큰 수** | \(A, B \le 10^{18}\) | C++은 `long long`, Python은 정수 그대로 사용 |

## 참고 문헌 및 출처

- [백준 24491번 Searching for Soulmates](https://www.acmicpc.net/problem/24491)
- [USACO 2022 January Contest, Silver - Problem 1](https://usaco.org/index.php?cpid=1182)
- [USACO Official Solution (sol_prob1_silver_jan22)](http://www.usaco.org/current/data/sol_prob1_silver_jan22.html)
