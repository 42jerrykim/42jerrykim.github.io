---
title: "[Algorithm] cpp 백준 13261번: 탈옥 - DP 분할정복 최적화"
description: "연속한 L칸을 G개의 구간으로 분할해 각 구간 비용을 (길이×구간합)으로 정의하고 총합을 최소화합니다. dp[g][r]=min(dp[g-1][k]+cost(k+1,r))를 이용해 분할정복 최적화로 O(G·L·logL)에 해결하며, 누적합으로 O(1) 구간비용·경계·64비트 오버플로를 꼼꼼히 점검합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Dynamic Programming
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13261
- cpp
- C++
- Dynamic Programming
- 동적계획법
- DP
- DP Optimization
- DP 최적화
- Divide and Conquer DP
- 분할정복 DP
- Divide and Conquer Optimization
- 분할정복 최적화
- DnC Optimization
- Monge
- Quadrangle Inequality
- 단조성
- Monotonicity
- Partition DP
- 구간 분할
- Grouping
- 그룹화
- Range Cost
- 구간 비용
- Prefix Sum
- 누적합
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
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
- Testing
- 테스트
- Invariant
- 불변식
- Array
- 배열
- Greedy
- 그리디
- Binary Search
- 이분탐색
- Implementation Details
- 구현 디테일
- Prison
- 탈옥
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13261
- 요약: 길이 \(L\)의 칸마다 탈옥력 \(C_i\)가 주어집니다. 간수 최대 \(G\)명을 배치해 연속 구간 단위로 감시할 때, 구간 \([l,r]\)의 비용은 \((r-l+1)\times\sum_{i=l}^{r} C_i\) 입니다. 전체 비용의 최솟값을 구합니다.

## 입력/출력
```
<입력>
L G
C1 C2 ... CL

<출력>
최솟값
```

## 접근 개요
- 핵심 관찰: 한 간수가 맡는 범위는 연속 구간이며, 구간 비용은 길이와 구간합의 곱으로 표현됩니다.
- 모델링: \(dp[g][r] =\) 처음 \(r\)칸을 \(g\)개의 구간으로 나눴을 때의 최소 비용.
- 전이: \(dp[g][r] = \min_{0\le k<r} \{ dp[g-1][k] + \text{cost}(k+1,r) \}\), \(\text{cost}(l,r)=(r-l+1)(S[r]-S[l-1])\) with \(S\) = prefix sum.
- 최적화: 비용 구조가 단조 최적해(Argmin)가 \(r\)에 대해 비내림차순이므로 Divide and Conquer Optimization 적용. 각 레이어를 \(O(L\log L)\)에 계산.

```mermaid
flowchart LR
  A[Prefix Sum S[i] 계산] --> B[비용 cost(l,r) = (r-l+1)(S[r]-S[l-1])]
  B --> C[dp[g][r] = min_k dp[g-1][k] + cost(k+1,r)]
  C --> D[Argmin 단조성]
  D --> E[Divide & Conquer Optimization로 레이어 g 계산]
```

## 알고리즘 설계
- 전처리: \(S[i]=\sum_{t=1}^{i} C_t\)
- 전이 비용: `cost(l,r) = (r-l+1) * (S[r]-S[l-1])`를 O(1)에 계산
- 점화식: `dp[g][r] = min_{k<r} dp[g-1][k] + cost(k+1, r)`
- D&C 계산: `compute(l, r, optL, optR)`로 구간의 중간 `mid` 최적 분할점 `k`를 `optL..min(mid-1,optR)`에서 찾고, 좌/우로 `opt` 범위를 좁혀 재귀
- 복원 불필요: 값만 요구되므로 경로 추적은 생략
- 자료형: 비용 상한이 약 `6.4e16`이므로 64-bit 정수 사용

## 복잡도
- 시간: \(O(G\cdot L\log L)\)
- 공간: \(O(L)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const long long INF = (1LL << 62);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int L, G;
    if (!(cin >> L >> G)) return 0;
    G = min(G, L);

    vector<long long> C(L + 1, 0);
    for (int i = 1; i <= L; ++i) cin >> C[i];

    vector<long long> S(L + 1, 0);
    for (int i = 1; i <= L; ++i) S[i] = S[i - 1] + C[i];

    auto cost = [&](int l, int r) -> long long {
        long long len = r - l + 1;
        return len * (S[r] - S[l - 1]);
    };

    vector<long long> prev(L + 1, INF), cur(L + 1, INF);
    prev[0] = 0;

    function<void(int,int,int,int)> solve = [&](int Lx, int Rx, int optL, int optR) {
        if (Lx > Rx) return;
        int mid = (Lx + Rx) >> 1;

        long long best = INF; int bestK = -1;
        int sr = min(mid - 1, optR);
        for (int k = optL; k <= sr; ++k) {
            if (prev[k] == INF) continue;
            long long cand = prev[k] + cost(k + 1, mid);
            if (cand < best) { best = cand; bestK = k; }
        }
        cur[mid] = best;

        solve(Lx, mid - 1, optL, (bestK == -1 ? optL : bestK));
        solve(mid + 1, Rx, (bestK == -1 ? sr : bestK), optR);
    };

    for (int g = 1; g <= G; ++g) {
        fill(cur.begin(), cur.end(), INF);
        solve(1, L, 0, L - 1);
        prev.swap(cur);
        prev[0] = INF; // r>=g가 아니면 사실상 불가능 상태 유지
    }

    cout << prev[L] << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
def solve():
    data = list(map(int, sys.stdin.read().strip().split()))
    if not data:
        return
    it = iter(data)
    L = next(it); G = next(it)
    G = min(G, L)
    C = [0] + [next(it) for _ in range(L)]
    S = [0]*(L+1)
    for i in range(1, L+1):
        S[i] = S[i-1] + C[i]

    INF = 1<<62
    prev = [INF]*(L+1)
    cur = [INF]*(L+1)
    prev[0] = 0

    def cost(l, r):
        return (r - l + 1) * (S[r] - S[l-1])

    sys.setrecursionlimit(1_000_000)
    def solve_layer(Lx, Rx, optL, optR):
        if Lx > Rx:
            return
        mid = (Lx + Rx) // 2
        best = INF
        best_k = -1
        sr = min(mid - 1, optR)
        for k in range(optL, sr + 1):
            if prev[k] == INF:
                continue
            cand = prev[k] + cost(k+1, mid)
            if cand < best:
                best = cand
                best_k = k
        cur[mid] = best
        solve_layer(Lx, mid-1, optL, optL if best_k == -1 else best_k)
        solve_layer(mid+1, Rx, sr if best_k == -1 else best_k, optR)

    for _ in range(G):
        for i in range(L+1):
            cur[i] = INF
        solve_layer(1, L, 0, L-1)
        prev, cur = cur, prev
        prev[0] = INF

    print(prev[L])

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- \(G\ge L\): 모든 칸 단일 구간 → 정답은 \(\sum C_i\)
- \(G=1\): 하나의 구간 → 정답은 \(L\cdot\sum C_i\)
- 큰 \(C_i\)로 인한 64-bit 범위 점검(필수)
- 빈/단일 구간 방지: 전이에서 `k < r`만 고려

## 제출 전 점검
- 빠른 입출력, 1-기반 누적합, 비용 O(1) 계산 확인
- D&C 인자: 좌/우 재귀의 `opt` 범위 축소가 올바른지 점검
- 레이어 초기화 시 `prev[0]`의 불가능 상태 유지로 과적합 방지

## 참고자료/유사문제
- Divide and Conquer Optimization 개요, 단조 최적해(Argmin Monotonicity)
- 유사: 구간 분할 DP 계열(예: 비용이 \(f(l,r)\) 형태인 분할 문제)


