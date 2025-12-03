---
title: "[Algorithm] C++/Python 백준 16998번: Mod World"
description: "p, q, n이 주어질 때 (p·i mod q)의 합을 i=1..n까지 구하는 문제입니다. 유클리드 호제법 기반 floor_sum과 주기성(서로소 시 잔여 클래스 순열)을 이용해 O(log q)로 풀며, 정당성과 경계 사례를 함께 점검합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Number Theory
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16998
- cpp
- python
- C++
- Python
- Modular Arithmetic
- 모듈러
- Number Theory
- 정수론
- Euclidean Algorithm
- 유클리드 호제법
- Floor Sum
- 합-바닥함수
- Sum of Floors
- 바닥합
- Mathematics
- 수학
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
- Arithmetic Progression
- 등차수열
- Residue Class
- 잔여류
- Chinese Remainder Insight
- 나머지 분해
- GCD Reduction
- 최대공약수 분해
- Periodicity
- 주기성
- AtCoder Library Style
- ACL 스타일
- Big Integer Safety
- 큰정수 안전성
- Overflow Guard
- 오버플로 방지
- NAIPC 2019
- Contest D
- 문제 풀이
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16998
- 요약: 정수 `p, q, n`에 대해 `S = \sum_{i=1}^{n} (p·i mod q)`를 구한다. 여러 테스트 케이스가 주어진다. 합 전체에는 모듈러를 취하지 않는다.
- 제한: `1 ≤ W ≤ 1e5`, `1 ≤ p, q, n ≤ 1e6`, 시간 5초, 메모리 512MB

## 입력/출력
```
입력
W
p q n
p q n
...

출력
각 테스트케이스에 대해 한 줄에 하나씩 S를 출력
```

예시
```
입력
3
2 7 2
1 4 5
3 8 10

출력
6
7
37
```

## 접근 개요
- 핵심 관찰: `(p·i mod q) = p·i - q·floor((p·i)/q)`. 따라서
  \[ S = p\cdot\frac{n(n+1)}{2} - q \cdot \sum_{i=1}^{n} \left\lfloor \frac{p i}{q} \right\rfloor \]
- `floor_sum(n, m, a, b) = \sum_{i=0}^{n-1} floor((a·i + b)/m)` 를 유클리드 호제법으로 O(log m)에 계산 가능.
- 또한 `g = gcd(p, q)` 로 나누어 `p = g·a`, `q = g·m` 이면 `(p·i mod q) = g·((a·i) mod m)` 이고, `gcd(a, m) = 1`일 때 길이 `m`의 완전한 주기에서 잔여 합은 `m(m-1)/2`.
- 두 방법 모두 가능: (1) 직접 floor_sum로 계산하거나, (2) `g`로 분해 후 "완전 주기 + 접두부" 합을 구한 뒤 `g`를 곱한다.

### 시각화 (개략 흐름)
```mermaid
flowchart TD
  A[입력 p,q,n] --> B{g = gcd(p,q)}
  B --> C[a = p/g, m = q/g]
  C --> D{전부 floor_sum로 계산?}
  D -- 예 --> E[p*n*(n+1)/2 - q*floor_sum(n+1,q,p,0)]
  D -- 아니오 --> F[full = n div m, rem = n mod m]
  F --> G[주기합 = m*(m-1)/2]
  G --> H[partial = sum_{i=1..rem} (a*i mod m)]
  H --> I[답 = g*(full*주기합 + partial)]
  E --> J[출력]
  I --> J[출력]
```

## 알고리즘 설계
- 방법 A: `S = p*n(n+1)/2 - q * floor_sum(n+1, q, p, 0)`
  - `floor_sum`은 표준(AtCoder Library 스타일) 재귀/반복 구현 사용.
- 방법 B: `g = gcd(p, q)`로 분해하여 길이 `m = q/g` 주기마다의 합(서로소 조건에서 `m(m-1)/2`)을 이용해 `O(1)`로 처리하고, 남은 `rem`개는 `floor_sum`으로 접두부만 계산.
- 위 두 방법의 결과는 동일하며, 구현 난이도 및 상수로 인해 A가 간결, B가 수학적 직관이 명확.

## 정당성 근거
- 분해식 `x mod q = x - q*floor(x/q)`에 의해 전체 합을 선형/바닥합으로 분리할 수 있음.
- `gcd(a, m) = 1`이면 곱셈에 의한 잔여류 순열이 성립하여 한 주기의 합이 `0..m-1`의 합과 동일(= `m(m-1)/2`).
- `floor_sum`은 유클리드 호제법으로 분자로/분모를 교환하며 문제 크기를 감소시키므로 각 단계가 `m`을 줄여서 `O(log m)`에 종료.

## 복잡도
- 시간: 케이스당 `O(log q)`
- 공간: `O(1)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
using i128 = __int128_t;

static inline int64 floor_sum(int64 n, int64 m, int64 a, int64 b) {
    int64 ans = 0;
    while (true) {
        if (a >= m) {
            ans += (int64)((i128)(n - 1) * n / 2 * (a / m));
            a %= m;
        }
        if (b >= m) {
            ans += n * (b / m);
            b %= m;
        }
        i128 y = (i128)a * n + b;
        if (y < m) break;
        n = (int64)(y / m);
        b = (int64)(y % m);
        swap(m, a);
    }
    return ans;
}

// 방법 B: gcd 분해 + 주기성 + 접두부는 floor_sum으로 처리
static inline long long solve_case(long long p, long long q, long long n) {
    if (q == 1 || n == 0) return 0;
    long long g = std::gcd(p, q);
    long long a = p / g;      // coprime with m
    long long m = q / g;      // modulus after factoring gcd

    long long full = n / m;
    long long rem  = n % m;

    long long period_sum = m * (m - 1) / 2;  // sum over one full period for coprime case
    long long partial = 0;
    if (rem > 0) {
        long long fs = floor_sum(rem + 1, m, a, 0); // sum_{i=1..rem} floor(a*i/m)
        i128 t1 = (i128)a * rem * (rem + 1) / 2;
        partial = (long long)(t1 - (i128)m * fs);
    }

    i128 reduced_total = (i128)full * period_sum + partial;
    i128 final_total = (i128)g * reduced_total;
    return (long long)final_total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int W; if (!(cin >> W)) return 0;
    while (W--) {
        long long p, q, n; cin >> p >> q >> n;
        cout << solve_case(p, q, n) << '\n';
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def floor_sum(n: int, m: int, a: int, b: int) -> int:
    # sum_{i=0..n-1} floor((a*i + b)/m)
    ans = 0
    while True:
        if a >= m:
            ans += (n - 1) * n // 2 * (a // m)
            a %= m
        if b >= m:
            ans += n * (b // m)
            b %= m
        y = a * n + b
        if y < m:
            break
        n, b, m, a = y // m, y % m, a, m
    return ans

def solve_case(p: int, q: int, n: int) -> int:
    if q == 1 or n == 0:
        return 0
    # 방법 A: 직관적 분해식
    total_linear = p * n * (n + 1) // 2
    floors = floor_sum(n + 1, q, p, 0)  # sum_{i=1..n} floor(p*i/q)
    return total_linear - q * floors

def main() -> None:
    input = sys.stdin.readline
    W = int(input().strip())
    out_lines = []
    for _ in range(W):
        p, q, n = map(int, input().split())
        out_lines.append(str(solve_case(p, q, n)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- `q = 1`이면 모든 항이 0 → 합 0
- `n < q`인 작은 접두부만 있는 경우
- `gcd(p, q) > 1`로 주기 길이가 짧아지는 경우
- 최대 경계: `p = q = n = 10^6`, `W = 10^5` (케이스당 `O(log q)` 보장 필요)
- 오버플로: C++에서는 중간 계산에 128-bit 사용, Python은 빅인트 안전

## 제출 전 점검
- 표준 입출력, 개행 형식 확인
- C++: 64-bit 범위 점검, 곱셈 중간값 i128 캐스팅 적용
- `floor_sum` 인덱스 범위 정의(0..n-1)와 사용처 일치 확인

## 참고자료
- 잔여류 주기성과 `sum of floors` 고전 테크닉
- AtCoder Library `floor_sum` 아이디어


