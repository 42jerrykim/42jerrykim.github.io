---
title: "[Algorithm] C++ 백준 14177번: 티떱랜드 - 어색함 최소화 DP(DnC)"
description: "N명을 K개 연속 구간으로 나눠 구간 내 사람쌍 어색함 합을 최소화. 2D 누적합으로 cost(l,r) O(1) 계산, dp[g][i]=min(dp[g-1][j]+cost) 전이를 분할정복 최적화로 O(KN log N) 해결."
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
- Problem-14177
- cpp
- C++
- Dynamic Programming
- 동적계획법
- Divide and Conquer Optimization
- 분할정복 DP 최적화
- Divide and Conquer DP
- DnC
- Partition DP
- 그룹 분할
- Grouping
- 구간 분할
- Cost Function
- 비용 함수
- Prefix Sum
- 누적합
- 2D Prefix Sum
- 2차원 누적합
- Matrix
- 행렬
- Symmetric Matrix
- 대칭 행렬
- Quadrangle Inequality
- 사각 부등식
- Monge
- Monge Array
- Optimization
- 최적화
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
- Fast IO
- 빠른 입출력
- Memory
- 메모리
- Prefix Rectangle Sum
- 직사각형 합
- DP Transition
- DP 전이
- Train Grouping
- 열차 그룹화
- Awkwardness Minimization
- 어색함 최소화
- Editorial
- 에디토리얼
- Competitive Programming
- 경쟁프로그래밍
- Testing
- 테스트
- Debugging
- 디버깅
- Invariant
- 불변식
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14177
- 요약: 사람 `1..N`이 서 있는 순서를 바꾸지 않고 `K`개의 연속 구간으로 나눌 때, 각 구간(열차) 내 모든 사람쌍의 어색함 `u_ij` 합의 총합을 최소화합니다. 행렬 `u`는 대칭이고 대각선은 0입니다. 제약: \(1 \le N \le 4000\), \(1 \le K \le \min(N,800)\), \(0 \le u_{ij} \le 9\).

## 입력/출력
```
<입력>
N K
u11 u12 ... u1N
...
uN1 uN2 ... uNN   (대칭, uii=0)

<출력>
최소 가능한 전체 어색함 합
```

## 접근 개요
- 핵심 관찰: 구간 `[l,r]`의 어색함 비용은 \(\sum_{l \le i < j \le r} u_{ij}\). 대칭 행렬의 성질로 정사각형 부분합을 2로 나누면 빠르게 구할 수 있습니다.
- 전형적 구간 분할 DP: `dp[g][i] = min_{0<=j<i}( dp[g-1][j] + cost(j+1, i) )`.
- `cost(l,r)`가 쌍대칭 합으로 정의되어 있어 분할정복 최적화(DnC Opt)가 성립합니다. 각 단계의 최적 `j`는 단조하게 이동하므로, `O(N log N)`에 한 레벨을 계산할 수 있습니다.

```mermaid
flowchart TB
  A[입력: N, K, 대칭 행렬 u] --> B[2D Prefix Sum P 구성]
  B --> C[cost(l,r) = sum(P, [l..r]x[l..r]) / 2]
  C --> D[DP 정의: dp[g][i] = min_j dp[g-1][j] + cost(j+1,i)]
  D --> E[Divide & Conquer Optimization로 dp[g][*] 계산]
  E --> F[정답 = dp[K][N]]
```

## 알고리즘 설계
- 비용 전처리(암시적): `P[i][j]`를 `u`의 2D 누적합으로 구성. 그러면 `rect(l,l,r,r)`를 \(O(1)\)에 얻고 `cost(l,r) = rect/2`.
- DP 전이: `g`번째 그룹까지 고려해 앞에서 `i`명 채웠을 때의 최소 비용 `dp[g][i]`.
- DnC 최적화: `i`의 구간을 절반으로 쪼개며, 각 중간점의 최적 분할점 `j*`를 좌/우 재귀의 탐색 범위로 전달해 전체를 `O(N log N)`에 계산.
- 올바름 근거(요지):
  - 동일 구간에 속하는 쌍의 비용만 더하므로, 구간 분할의 국소적 선택이 전체 비용에 선형 합으로 기여(가법성).
  - 이때 최적 분할점이 단조하게 이동하는 구조(사각 부등식 계열)가 성립하여 DnC 최적화를 적용할 수 있습니다.

## 복잡도
- 시간: 전처리 `O(N^2)`(2D 누적합) + DP `O(K N log N)`
- 공간: `O(N^2)`(누적합) + `O(N)`(DP 레벨 2개)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, K;
    if (!(cin >> N >> K)) return 0;

    const int SZ = N + 1;
    // 2D prefix sum over the whole N x N matrix, flattened for cache locality
    vector<long long> psum(1LL * SZ * SZ, 0);
    auto I = [&](int r, int c) -> long long { return 1LL * r * SZ + c; };

    for (int i = 1; i <= N; ++i) {
        for (int j = 1; j <= N; ++j) {
            int x; cin >> x;
            psum[I(i, j)] = psum[I(i - 1, j)] + psum[I(i, j - 1)] - psum[I(i - 1, j - 1)] + x;
        }
    }

    auto rect = [&](int r1, int c1, int r2, int c2) -> long long {
        return psum[I(r2, c2)] - psum[I(r1 - 1, c2)] - psum[I(r2, c1 - 1)] + psum[I(r1 - 1, c1 - 1)];
    };

    auto cost = [&](int l, int r) -> long long {
        // sum of u_ij for l <= i < j <= r; diagonal is zero; matrix symmetric
        long long s = rect(l, l, r, r);
        return s >> 1; // divide by 2
    };

    const long long INF = (1LL << 62);
    vector<long long> dp_prev(SZ, INF), dp_cur(SZ, INF);
    dp_prev[0] = 0;

    for (int g = 1; g <= K; ++g) {
        fill(dp_cur.begin(), dp_cur.end(), INF);

        function<void(int,int,int,int)> solve = [&](int L, int R, int optL, int optR) {
            if (L > R) return;
            int mid = (L + R) >> 1;

            long long bestVal = INF;
            int bestK = -1;

            int jStart = max(optL, g - 1);
            int jEnd = min(optR, mid - 1);
            for (int j = jStart; j <= jEnd; ++j) {
                long long cand = dp_prev[j] + cost(j + 1, mid);
                if (cand < bestVal) {
                    bestVal = cand;
                    bestK = j;
                }
            }
            dp_cur[mid] = bestVal;

            if (L == R) return;
            solve(L, mid - 1, optL, bestK);
            solve(mid + 1, R, bestK, optR);
        };

        solve(g, N, g - 1, N - 1);
        dp_prev.swap(dp_cur);
    }

    cout << dp_prev[N] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `K = 1`(한 구간): 전체 정사각 부분합/2
- `K = N`(모두 단독): 항상 0
- 균일 행렬(모두 0 또는 모두 동일 양수)
- 극단 입력 크기: `N=4000`에서 입력 파싱 속도 및 메모리 사용(2D 누적합 약 128MB)

## 제출 전 점검
- 빠른 입출력 설정: `sync_with_stdio(false)`, `tie(nullptr)`
- 경계: `dp[g][i]`는 `i >= g`에서만 유효, `solve(g, N, g-1, N-1)` 호출
- 비용 계산: `cost(l,r)`는 `rect/2`로 계산(대칭·대각 0 가정)
- 오버플로: 누적합과 DP는 `long long` 사용

## 참고자료/유사문제
- Divide and Conquer DP Optimization 개요 및 응용
- 구간 분할 DP(Partition DP) 전형 문제군


