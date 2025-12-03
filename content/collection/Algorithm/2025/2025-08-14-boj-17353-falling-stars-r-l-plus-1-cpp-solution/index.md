---
title: "[Algorithm] C++ 백준 17353번: 하늘에서 떨어지는 1, 2, ..., R-L+1개의 별"
description: "구간 [L,R]에 1..R-L+1 등차수열을 더하는 쿼리를 처리합니다. 점 X에 더해지는 합은 Σ(X−L+1)=cnt·(X+1)−ΣL로 표현되므로, 두 개의 펜윅 트리(BIT)로 [L,R]에 +1, +L을 각각 범위 업데이트하고 점 질의로 합을 계산해 O((N+Q)logN)에 해결합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17353
- cpp
- C++
- Data Structures
- 자료구조
- Fenwick Tree
- 펜윅트리
- BIT
- Binary Indexed Tree
- Difference Array
- 차분 배열
- Prefix Sum
- 누적합
- Range Update
- 구간 업데이트
- Point Query
- 점 질의
- Arithmetic Progression
- 등차수열
- Range Add
- 구간 가산
- Online Queries
- 온라인 처리
- Query Processing
- 쿼리 처리
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- BIT Tricks
- BIT 테크닉
- Range to Point
- 구간에서 점
- Math
- 수학
- Indexing
- 인덱싱
- 1-based Index
- 1-기반 인덱스
- Fast IO
- 빠른 입출력
- Long Long
- 64-bit
- Overflow
- 오버플로
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17353
- 요약: 초기 배열 `A[1..N]`이 주어지고, 쿼리 1은 연속 구간 `[L, R]`의 각 위치에 `1, 2, ..., R-L+1`을 차례로 더합니다. 쿼리 2는 특정 위치 `X`에 누적된 값을 출력합니다.

## 입력/출력
```
<입력>
N
A1 A2 ... AN
Q
각 줄에 다음 중 하나
1 L R
2 X

<출력>
모든 2번 쿼리의 답을 한 줄에 하나씩 출력
```

## 접근 개요
- 갱신 1 `[L, R]`이 `X`(L ≤ X ≤ R)에 더하는 값은 정확히 `X - L + 1`입니다.
- 여러 갱신이 있을 때 점 `X`의 총 증가분은 \(\sum_{(L,R)\ni X} (X-L+1)\) 이고, 이를 전개하면 \(\underbrace{\text{cnt}(X)}_{X를 덮는 구간 수}\cdot (X+1) - \sum L\)로 쓸 수 있습니다.
- 따라서 두 개의 펜윅 트리(BIT)를 사용해 `[L, R]`에 대해 동시에
  - `+1`(X를 덮는 구간 수)에 대한 범위 업데이트,
  - `+L`(시작점 합)에 대한 범위 업데이트
  를 수행하고, 질의 시 각각의 점값을 가져와 위 식으로 계산합니다.
- 초기값 `A[X]`는 그대로 더해주면 됩니다.

## 알고리즘 설계
- 자료구조: 차분 기법을 이용한 BIT로 "범위 업데이트 + 점 질의"를 지원합니다.
- 연산
  - 갱신 `1 L R`:
    - `coverCnt`에 `[L, R]` 범위 `+1` 적용
    - `sumStartL`에 `[L, R]` 범위 `+L` 적용
  - 질의 `2 X`:
    - `cnt = coverCnt.pointQuery(X)`
    - `sL = sumStartL.pointQuery(X)`
    - `answer = A[X] + (X+1)*cnt - sL`
- 올바름 근거: 각 구간 갱신이 X에 기여하는 양은 `(X-L+1)`이므로, 모든 갱신의 합은 `(X+1)`에 비례하는 항과 시작점 합 `ΣL`의 차로 표현됩니다. 두 BIT가 정확히 이 두 값을 독립적으로 제공합니다.

## 복잡도
- 시간: O((N + Q) log N)
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> bit;
    Fenwick(int n) : n(n), bit(n + 2, 0) {}
    void add(int idx, long long delta) {
        for (; idx <= n + 1; idx += idx & -idx) bit[idx] += delta;
    }
    long long sum(int idx) const {
        long long res = 0;
        for (; idx > 0; idx -= idx & -idx) res += bit[idx];
        return res;
    }
    void rangeAdd(int l, int r, long long delta) {
        add(l, delta);
        add(r + 1, -delta);
    }
    long long pointQuery(int idx) const { return sum(idx); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<long long> A(N + 1);
    for (int i = 1; i <= N; ++i) cin >> A[i];

    Fenwick coverCnt(N);   // number of updates covering index i
    Fenwick sumStartL(N);  // sum of L over updates covering index i

    int Q; cin >> Q;
    while (Q--) {
        int t; cin >> t;
        if (t == 1) {
            int L, R; cin >> L >> R;
            coverCnt.rangeAdd(L, R, 1);
            sumStartL.rangeAdd(L, R, L);
        } else {
            int X; cin >> X;
            long long cnt = coverCnt.pointQuery(X);
            long long sL = sumStartL.pointQuery(X);
            long long result = A[X] + (static_cast<long long>(X) + 1) * cnt - sL;
            cout << result << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `L = R`인 단일 원소 갱신이 반복되는 경우
- 동일 구간 갱신이 중복으로 들어오는 경우(선형 누적)
- `X = 1` 또는 `X = N` 경계 인덱스 질의
- 큰 입력 규모 `N, Q ≤ 1e5`에서의 성능과 64-bit 범위 확인
- 초기값 `A[i]=0` 또는 큰 값 혼재(출력 범위는 64-bit로 충분)

## 제출 전 점검
- 입출력 버퍼링 설정(`sync_with_stdio(false)`, `tie(nullptr)`) 확인
- 인덱스는 1-based로 유지, BIT 내부 업데이트/질의 일관성 점검
- 정수 자료형: 누적 합과 곱은 `long long` 사용

## 참고자료
- Binary Indexed Tree로 범위 업데이트/점 질의 처리 기법
- 차분 배열(difference array)과 BIT의 결합 아이디어


