---
title: "[Algorithm] cpp 백준 6171번: 땅따먹기 - 묶음 할인 최소 비용 DP+CHT"
description: "여러 직사각형 땅을 묶어 살 때 비용은 (묶음 내 최대 W)*(묶음 내 최대 H)입니다. W 오름차순 정렬 후 같은 W는 최대 H로 병합하고, 뒤에서 앞으로 보며 지배된 직사각형을 제거해 H를 단조 감소로 만듭니다. 이후 dp[i]=min(dp[k]+W[i]*H[k+1])를 단조 Convex Hull Trick으로 O(n)에 계산하며, 정수 교차 비교와 __int128 중간 연산으로 오버플로를 방지합니다."
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
- Problem-6171
- cpp
- C++
- Dynamic Programming
- 동적계획법
- DP Optimization
- DP 최적화
- Convex Hull Trick
- 컨벡스 헐 트릭
- CHT
- Monotonic CHT
- 단조 CHT
- Lines Container
- 직선 집합
- Lower Envelope
- 하한선
- Deque Optimization
- 덱 최적화
- Sorting
- 정렬
- Deduplication
- 중복제거
- Pareto
- 파레토
- Dominated
- 지배관계
- Rectangle
- 직사각형
- Greedy Filter
- 그리디 필터
- Proof of Correctness
- 정당성 증명
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- __int128
- 128-bit
- 64-bit
- 오버플로 방지
- Fast IO
- 빠른 입출력
- Land Grabbing
- 땅따먹기
- BOJ6171
- Data Structures
- 자료구조
- Binary Search
- 이분탐색
- Monotonic Queue
- 단조 큐
- Editorial
- 에디토리얼
- Testing
- 테스트
- Invariant
- 불변식
- Template
- 템플릿
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/6171
- 요약: 땅은 직사각형 `(W, H)`로 표현되고, 여러 필지를 묶어 사면 가격이 그 묶음의 `(최대 W) * (최대 H)`로 책정됩니다. 모든 땅을 최소 비용으로 사려면 어떻게 묶어야 하는지 구합니다. `N ≤ 5e4`, `W, H ≤ 1e6`.

## 입력/출력
```
<입력>
N
W1 H1
W2 H2
...
WN HN

<출력>
최소 비용
```

## 접근 개요
- 핵심 관찰: `(W, H)`를 그대로 쓰면 상태가 많습니다. 하지만 묶음 비용은 각 묶음의 최대값만 관여하므로, 지배(dominance)되는 직사각형은 제거할 수 있습니다.
- 전처리: `W` 오름차순 정렬 → 같은 `W`는 `H` 최대만 유지 → 뒤에서 앞으로 보며 지금까지의 `H` 최대보다 작거나 같은 직사각형은 제거 → 결과는 `W` 증가, `H` 엄격 감소.
- 점화식: 전처리 후 인덱스 `1..m`에 대해
  - `dp[i] = min_{0 ≤ k < i} ( dp[k] + W[i] * H[k+1] )`
  - 이는 직선 `y = (H[k+1]) * x + dp[k]`에 `x = W[i]`로 질의하는 형태입니다.
- 단조 CHT: 기울기 `H[k+1]`가 단조 감소, 질의 `x=W[i]`가 단조 증가 → 덱 기반 Convex Hull Trick으로 각 `i`를 평균 O(1)에 처리.

```mermaid
flowchart LR
  A[입력 (W,H)] --> B[W 오름차순 정렬\n같은 W는 H 최대로 병합]
  B --> C[뒤→앞 스캔으로 지배 제거\n(H 단조 감소 유지)]
  C --> D[dp[i]=min_k dp[k]+W[i]*H[k+1]]
  D --> E[직선 하한선 유지 (단조 CHT)]
  E --> F[답 = dp[m]]
```

## 알고리즘 설계
- 정렬·병합
  - `(W,H)`를 `W` 오름차순 정렬.
  - 같은 `W`는 `H`의 최댓값만 남김(같은 `W` 중 나머지는 항상 열세).
- 지배 제거(Pareto 필터)
  - 뒤에서 앞으로 스캔하며 지금까지의 `H` 최대보다 큰 경우만 유지 → 최종 `H`는 엄격 감소가 되어 기울기 단조 조건 성립.
- DP + CHT
  - 직선: `m = H[k+1]`(감소), `b = dp[k]`.
  - 질의: `x = W[i]`(증가). 덱 앞에서 최솟값을 제공, 뒤에 새 직선을 추가할 때는 삼점 불필요성 검사로 제거.
- 안전성/구현 포인트
  - 교차 비교는 정수 산술로 처리, 중간 계산은 `__int128` 사용.
  - `long long` 범위 내 결과 보장, 빠른 입출력과 인덱스 관리 일관성 유지.

## 복잡도
- 정렬·필터: `O(N log N)` (정렬 우세)
- DP/CHT: `O(m)` (`m`은 필터 후 크기, `m ≤ N`)
- 전체: `O(N log N)`, 추가 공간 `O(N)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Line {
    int64 slope;
    int64 intercept;
    inline int64 value_at(int64 x) const { return slope * x + intercept; }
};

static inline bool is_redundant(const Line& l1, const Line& l2, const Line& l3) {
    // lower hull, decreasing slopes
    __int128 left  = (__int128)(l3.intercept - l1.intercept) * (l1.slope - l2.slope);
    __int128 right = (__int128)(l2.intercept - l1.intercept) * (l1.slope - l3.slope);
    return left <= right;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<pair<int64,int64>> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i].first >> a[i].second; // (W, H)

    // 1) Sort by W asc; deduplicate by W keeping max H
    sort(a.begin(), a.end()); // by W asc, then H asc
    vector<pair<int64,int64>> dedup;
    dedup.reserve(n);
    for (auto &p : a) {
        if (dedup.empty() || dedup.back().first != p.first) dedup.push_back(p);
        else dedup.back().second = max(dedup.back().second, p.second);
    }

    // 2) Remove dominated rectangles: scan from large W to small W keeping strictly increasing H
    vector<pair<int64,int64>> rects; // after filtering
    rects.reserve(dedup.size());
    int64 maxH = LLONG_MIN;
    for (int i = (int)dedup.size() - 1; i >= 0; --i) {
        int64 w = dedup[i].first, h = dedup[i].second;
        if (h > maxH) {
            rects.emplace_back(w, h);
            maxH = h;
        }
    }
    reverse(rects.begin(), rects.end()); // now W increasing, H strictly decreasing

    int m = (int)rects.size();
    if (m == 0) { cout << 0 << '\n'; return 0; }

    vector<int64> W(m + 1), H(m + 1);
    for (int i = 1; i <= m; ++i) {
        W[i] = rects[i - 1].first;
        H[i] = rects[i - 1].second;
    }

    // 3) DP with Convex Hull Trick:
    // dp[i] = min_{0 <= k < i} (dp[k] + W[i] * H[k+1])
    // Maintain lines: slope = H[k+1] (decreasing), intercept = dp[k]
    vector<int64> dp(m + 1, 0);
    deque<Line> hull;
    hull.push_back({H[1], 0}); // k = 0

    for (int i = 1; i <= m; ++i) {
        // Query at x = W[i], x is non-decreasing
        while (hull.size() >= 2 && hull[0].value_at(W[i]) >= hull[1].value_at(W[i])) {
            hull.pop_front();
        }
        dp[i] = hull.front().value_at(W[i]);

        // Insert new line for k = i: slope = H[i+1], intercept = dp[i]
        if (i + 1 <= m) {
            Line nl{H[i + 1], dp[i]};
            while (hull.size() >= 2 && is_redundant(hull[hull.size() - 2], hull[hull.size() - 1], nl)) {
                hull.pop_back();
            }
            hull.push_back(nl);
        }
    }

    cout << dp[m] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `N=1` 또는 전처리 후 `m=1`인 경우 → 답은 `W[1]*H[1]`이 아니라 점화식상 `dp[1]=0 + W[1]*H[1]`로 자연스럽게 계산됨
- 동일 `W`가 다수 존재 → 최대 `H` 하나만 유지(나머지는 항상 열세)
- 지배 제거가 올바른가? → 최종 `H`가 엄격 감소하면, 더 왼쪽(작은 `W`)이면서 `H`도 작거나 같으면 절대 최적 묶음의 최대가 될 수 없음
- 큰 값 곱셈 → 교차 비교·중간 계산에 `__int128` 사용하여 오버플로 방지
- 입력이 이미 정렬/역정렬된 경우에도 안정적으로 동작

## 제출 전 점검
- 정렬 후 같은 `W` 병합, 뒤→앞 지배 제거로 `H` 단조 감소 보장
- CHT 조건 확인: 기울기 단조(감소), 질의 `x` 단조(증가)
- 교차 비교 정수 산술(`__int128`) 적용 여부
- 빠른 입출력(`sync_with_stdio(false)`, `tie(nullptr)`) 적용

## 참고자료/유사문제
- Convex Hull Trick(단조 큐) 기본 원리와 구현
- USACO Gold Land Acquisition(유사 유형): 직사각형 정렬+지배 제거+CHT


