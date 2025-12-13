---
title: "[Algorithm] C++ 백준 14959번: Slot Machines - KMP로 최소 주기 O(n)"
description: "관측 수열 T[1..n]이 시점 k 이후 주기 p로 반복될 때, k+p 최소(동률 시 p 최소)인 (k,p)를 구한다. 역수열에 KMP 접두사함수를 적용해 접미사 최소 주기 p=L-pi를 O(n)에 계산하고 최적 해를 도출한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- String
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14959
- cpp
- C++
- python
- Python
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
- String
- 문자열
- KMP
- Prefix Function
- 접두사함수
- Border
- 경계
- Period
- 주기
- Minimal Period
- 최소 주기
- Period Finding
- 주기 추정
- Eventually Periodic
- Slot Machines
- Sequence
- 배열
- Pattern
- 패턴
- Reverse Trick
- 역배열
- ICPC
- ICPC 2017 Daejeon
- Asia Regional
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14959
- 요약: 길이 \(n\)의 관측 수열 \(T[1..n]\)이 존재하며, 어떤 시점 \(k\) 이후에는 길이 \(p\)의 주기로 반복된다고 할 때, 조건을 만족하는 모든 \((k,p)\) 중 \(k+p\)가 최소가 되는 해(동률이면 \(p\)가 최소)를 구한다.
- 제한/스펙: \(1 \le n \le 10^6\), 각 값은 0..999999, 시간 2초, 메모리 512MB.

## 입력/출력 형식
```
입력
n
T[1] T[2] ... T[n]

출력
k p
```

예시
```
입력: 6
612534 3157 423 3157 423 3157
출력: 1 2
```

## 접근 개요
- \(k\) 이후 부분수열 \(S=T[k+1..n]\)이 주기 \(p\)를 가진다는 것은, 문자열(수열) 의미에서 \(S\)의 period가 \(p\)라는 뜻이다. 즉 \(1 \le i \le |S|-p\)에 대해 \(S[i]=S[i+p]\).
- 모든 접미사에 대해 “최소 주기”를 알 수 있으면, 각 접미사 길이 \(L\)에 대한 후보 비용은 \(k+p = (n-L) + p_{min}\). 여기서 KMP 접두사함수 \(\pi\)의 성질로 \(p_{min} = L - \pi[L-1]\) 이므로 비용은 \(n - \pi[L-1]\)로 정리된다.
- 따라서 전체에서 \(\pi[L-1]\)이 최대가 되는 접미사를 고르면 \(k+p\)가 최소가 된다. 동률이면 \(p=L-\pi\)를 최소화하려면 \(L\)이 작은 쪽을 선택한다.
- “접미사에 대한 \(\pi\)”를 얻기 위해 수열을 뒤집어(Reverse) 놓고, 뒤집힌 수열의 모든 prefix에 대해 KMP 접두사함수를 계산한다. 길이 \(L\) prefix의 \(\pi\) 값은 원래 수열 길이 \(L\) 접미사의 \(\pi\)와 동일하다.

## 알고리즘
1. 수열 \(T\)를 뒤집어 \(R\) 생성
2. \(R\)에 대해 접두사함수 \(\pi\)를 O(n)으로 계산
3. 모든 길이 \(L=1..n\)에 대해 \(b=\pi[L-1]\), 비용 \(n-b\)를 평가
   - 최댓값 \(b\)를 갖는 \(L\)을 선택, 동률이면 \(L\) 최소를 선택
4. \(k = n - L\), \(p = L - b\) 출력

## 복잡도
- 시간: O(n)
- 공간: O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    vector<int> r(n);
    for (int i = 0; i < n; ++i) r[i] = a[n - 1 - i];

    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        while (j > 0 && r[i] != r[j]) j = pi[j - 1];
        if (r[i] == r[j]) ++j;
        pi[i] = j;
    }

    int bestB = -1;
    int bestL = 1;
    for (int i = 0; i < n; ++i) {
        int L = i + 1;
        int b = pi[i];
        if (b > bestB || (b == bestB && L < bestL)) {
            bestB = b;
            bestL = L;
        }
    }

    int k = n - bestL;
    int p = bestL - max(bestB, 0);
    cout << k << ' ' << p << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    r = a[::-1]
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and r[i] != r[j]:
            j = pi[j - 1]
        if r[i] == r[j]:
            j += 1
        pi[i] = j

    bestB = -1
    bestL = 1
    for i in range(n):
        L = i + 1
        b = pi[i]
        if b > bestB or (b == bestB and L < bestL):
            bestB = b
            bestL = L

    k = n - bestL
    p = bestL - max(bestB, 0)
    print(k, p)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 모든 값이 서로 다름: 어떤 접미사도 내부 반복이 없어 \(p=L\)이 되고, 보통 \(k+p=n\)
- 완전 주기열(처음부터 반복): \(k=0\), 최소 주기 \(p\) 반환
- 짧은 주기가 이어지다 마지막에 일부만 관측: \(L\)과 \(\pi\) 계산으로 자동 처리
- \(n=1\): \(k=0, p=1\)

## 제출 전 점검
- 입력 파싱(대용량)과 출력 형식 확인
- 64-bit 오버플로 문제 없음(Int 범위)
- KMP 경계 조건(while 탈출, 인덱스) 확인

## 참고자료
- KMP 접두사함수와 최소 주기: \(p = L - \pi[L-1]\)
- 문제 출처: ICPC Asia Regional Daejeon 2017 I


