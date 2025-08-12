---
title: "[BOJ] 꽃집 (17439) - Alien’s Trick + Monotone Queue C++"
description: "가격 오름차순 N개의 꽃을 최대 K개 구간으로 연속 분할하여 ∑(구간합×구간길이)을 최소화. 추가 비용 C를 이분탐색(Alien’s trick)하고 교점 1개 성질을 이용한 단조 큐 최적화로 O(N log N log X) 해법과 C++ 구현을 정리한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "17439"
- "Flower Shop"
- "꽃집"
- "DP"
- "Dynamic Programming"
- "구간 DP"
- "Interval DP"
- "연속 구간"
- "Interval Partition"
- "분할"
- "Prefix Sum"
- "누적합"
- "Parametric Search"
- "파라메트릭 서치"
- "Aliens Trick"
- "Alien’s Trick"
- "Monotone Queue"
- "단조 큐"
- "Deque"
- "큐"
- "Cross Point"
- "교점"
- "Line Intersection"
- "교차점"
- "CHT"
- "Convex Hull Trick"
- "Li Chao Tree"
- "리차오 트리"
- "Optimization"
- "최적화"
- "Binary Search"
- "이분 탐색"
- "O(N log N)"
- "시간복잡도"
- "Complexity"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast-IO"
- "빠른입출력"
- "Problem-Solving"
- "PS"
- "Competitive-Programming"
- "컴퓨티티브-프로그래밍"
- "Editorial"
- "해설"
- "Solution-Code"
- "정답-코드"
- "Slope"
- "Slope Optimization"
- "Segment Cost"
- "구간 비용"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 17439 - 꽃집](https://www.acmicpc.net/problem/17439)

### 아이디어 요약
- 각 구간(꽃다발)의 비용은 `(구간 길이) × (구간 내 가격 합)`이다. 오름차순으로 주어지므로 원소 순서를 유지한 연속 구간 분할 문제다.
- 누적합 `S[i]`를 두면, `j < i`에서 `cost(j+1..i) = (i-j)·(S[i]-S[j])` 이다. 나이브 점화식은 다음과 같다.
  - `dp[i] = min_{0 ≤ j < i} dp[j] + (i-j)·(S[i]-S[j])` (정확히 K개 제약이 있으면 레이어를 하나 더 둬 O(N^2 K))
- N, K ≤ 5e4이므로 위 점화는 불가. Alien’s trick으로 “구간을 새로 시작할 때마다 +C 페널티”를 부여해 K 제약을 제거하고, C를 이분탐색해 사용 구간 수를 K에 맞춘다.
- 고정된 C에 대해 위 식은 “교점이 하나인” 형태로 정리되며, 답 후보 인덱스를 단조로 관리하는 Monotone Queue 최적화로 `O(N log N)`에 계산 가능하다(교점 위치를 이분탐색).
- 최종 정답은 `min(run(C*) - K·C*, run(C*-1) - K·(C*-1))`로 복원한다.

### C++ 풀이

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, K;
    if (!(cin >> N >> K)) return 0;
    K = min(K, N);
    vector<int64> v(N + 1), S(N + 1, 0);
    for (int i = 1; i <= N; ++i) {
        cin >> v[i];
        S[i] = S[i - 1] + v[i];
    }

    auto run = [&](int64 C) -> pair<int64, int> {
        // dp[i]: penalized cost up to i; cnt[i]: #segments used
        vector<int64> dp(N + 1, 0);
        vector<int> cnt(N + 1, 0);

        auto val = [&](int j, int i) -> int64 {
            return dp[j] + (int64)(i - j) * (S[i] - S[j]) + C; // start new segment at j+1
        };
        auto better = [&](int a, int b, int i) -> bool {
            return val(a, i) <= val(b, i);
        };
        auto cross = [&](int a, int b) -> int {
            // minimal i where b becomes better or equal than a
            int lo = max(a, b) + 1, hi = N, ans = N + 1;
            while (lo <= hi) {
                int mid = (lo + hi) >> 1;
                if (better(b, a, mid)) { ans = mid; hi = mid - 1; }
                else lo = mid + 1;
            }
            return ans;
        };

        struct Cand { int idx, start; };
        deque<Cand> dq;
        dq.push_back({0, 1}); // j=0 candidate becomes valid from i=1

        for (int i = 1; i <= N; ++i) {
            while ((int)dq.size() >= 2 && dq[1].start <= i) dq.pop_front();
            int j = dq.front().idx;
            dp[i] = val(j, i);
            cnt[i] = cnt[j] + 1;

            int start = 1;
            while (!dq.empty()) {
                int last = dq.back().idx;
                int t = cross(last, i);
                if (t <= dq.back().start) dq.pop_back();
                else { start = t; break; }
            }
            if (start <= N) dq.push_back({i, start});
        }
        return {dp[N], cnt[N]};
    };

    // Binary search penalty C (Alien's trick)
    int64 sumV = S[N];
    int64 lo = 0, hi = sumV * (int64)N; // safe upper bound
    int64 Cstar = hi;
    while (lo <= hi) {
        int64 mid = (lo + hi) >> 1;
        auto [costMid, cntMid] = run(mid);
        if (cntMid <= K) { Cstar = mid; hi = mid - 1; }
        else lo = mid + 1;
    }

    auto [cost1, cnt1] = run(Cstar);
    int64 ans1 = cost1 - Cstar * (int64)K;

    int64 Cprev = (Cstar == 0 ? 0 : Cstar - 1);
    auto [cost0, cnt0] = run(Cprev);
    int64 ans0 = cost0 - Cprev * (int64)K;

    cout << min(ans0, ans1) << "\n";
    return 0;
}
```

### 복잡도
- 고정 C에서 Monotone Queue + 교점 이분탐색으로 `O(N log N)`.
- C는 값 범위(≈X)에 대해 `O(log X)` 이분탐색 → 전체 `O(N log N log X)`.

### 참고
- JusticeHui: [백준17439 꽃집 — Alien’s Trick + Monoqueue](https://justicehui.github.io/ps/2020/04/21/BOJ17439/)
- 문제: `https://www.acmicpc.net/problem/17439`


