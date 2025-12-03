---
title: "[Algorithm] C++ 백준 14166번: 로봇 소 무리 (Robotic Cow Herd)"
description: "K개의 로봇을 서로 다른 구성으로 최저 비용에 제작하는 문제. 각 위치 최소값 합을 기반으로 추가비용 배열을 구성해 임계 추가비용을 이분탐색하고, fracturing search(가지치기 열거)로 개수를 세어 K개 최소 합을 얻는다. 구현·복잡도·실수 포인트까지 정리."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14166
- cpp
- C++
- USACO
- USACO Platinum
- 2016 December
- Robotic Cow Herd
- 로봇 소 무리
- Fracturing Search
- 가지치기 열거
- Pruned DFS
- 백트래킹
- Enumeration
- 조합 열거
- Counting
- 개수 세기
- Binary Search
- 이분탐색
- Search
- 탐색
- Greedy
- 그리디
- Sorting
- 정렬
- upper_bound
- Lower/Upper Bound
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Invariant
- 불변식
- Backtracking
- DFS
- 재귀
- Pruning
- 가지치기
- Persistent Segment Tree
- 영속 세그먼트 트리
- Alternate Solution
- 대안 풀이
- Value Compression
- 값 압축
- Integer Overflow
- 오버플로
- Fast IO
- 빠른 입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14166
- 요약: N개 위치(각 위치마다 가능한 마이크로컨트롤러 모델 다수)에서 K개의 로봇을 만든다. 두 로봇은 최소 한 위치에서 모델이 달라야 하며(모든 로봇 쌍 상이), 총 제작 비용 합의 최소를 구한다. 제약: \(1\le N\le 10^5\), \(1\le K\le 10^5\), 각 위치 모델 수 \(1\le M_i\le 10\), 모델 비용 \(1\le P_{i,j}\le 10^8\).

## 입력/출력
```
<입력>
N K
M1 p1,1 p1,2 ... p1,M1
M2 p2,1 p2,2 ... p2,M2
...
MN pN,1 pN,2 ... pN,MN

<출력>
K개의 서로 다른 로봇을 만드는 최소 총 비용
```

## 접근 개요
- 기본 아이디어: 각 위치에서 가장 싼 모델만 고르면 “기본 로봇” 비용 \(base = \sum_i \min_j P_{i,j}\)을 얻는다. 이후 “업그레이드 비용(추가비용)”만 고려해 K개의 최소 추가비용 합을 더하면 된다.
- 추가비용 정규화: 각 위치 i에 대해 모든 모델 비용에서 최솟값을 빼면, 그 위치의 후보는 비음수 증가열(0 제외)로 표현된다. 길이가 1인 위치는 추가비용 후보가 없으므로 제거한다.
- Fracturing Search: 위치들을 “해당 위치의 최소 추가비용” 오름차순으로 정렬하고, 임계 추가비용 T 이하인 조합(각 위치에서 0 또는 하나의 추가비용)을 가지치기 DFS로 “개수만” 센다. T에 대해 “개수”는 단조 증가하므로 T를 이분탐색하여 K개 이상이 되는 최소 임계치를 찾는다.
- K개 최소 추가비용의 합: \(\text{sumSmallestK} = K\cdot T - \sum_{x\le T-1}(T- x)\). 후자는 동일한 DFS에 “누적 절감량(savings)”으로 계산 가능.

```mermaid
flowchart TB
  A[입력 파싱] --> B[각 위치 비용 정렬]
  B --> C[base = 각 위치 최솟값 합]
  C --> D[추가비용 배열로 변환(최솟값만큼 감산)]
  D --> E[위치들을 최소 추가비용 기준 정렬]
  E --> F[이분탐색으로 임계 T 탐색]
  F --> G[Fracturing Search로 T 이하 조합 개수 계산]
  G --> H[sumSmallestK = K*T - savings(T-1)]
  H --> I[정답 = base*K + sumSmallestK]
```

## 알고리즘 설계
- 전처리
  - 각 위치의 모델 비용 정렬 후, \(base += \text{min}\). 모델 수가 1이면 해당 위치는 제거(추가비용 후보가 없으므로).
  - 남은 각 위치에 대해 최솟값을 0으로 맞추는 추가비용 배열(오름차순) 생성. 그 중 최소 추가비용들만 따로 모아 정렬해 가지치기 시 상한을 빠르게 구한다.
- 개수 세기(count) DFS
  - 인덱스를 뒤에서 앞으로 진행하며, 현재 예산(budget)보다 큰 최소 추가비용을 갖는 뒤쪽 블록은 통째로 스킵(upper_bound로 인덱스 점프)한다.
  - 인덱스가 -1이 되면 “남은 위치는 모두 0(업그레이드 없음)”이므로 1개의 조합으로 카운트.
  - 각 위치에서 “0을 고르는 경우”와 “각 추가비용 중 budget 이하인 것 1개를 고르는 경우”를 재귀로 누적.
- 임계치 이분탐색
  - T에 대해 count(T) ≥ K인지 여부로 이분탐색. 값 범위는 각 위치 추가비용 최대들의 합으로 상계.
- K개 최소 추가비용 합 구하기
  - 동일한 DFS 틀로 budget = T-1에 대해 \(\sum (T-1 - extra)\)를 직접 누적(savings)하면, \(\sum_{K\text{개}} extra = K\cdot T - savings\)로 복원 가능.
- 올바름 근거(요지)
  - (가법성) 총비용은 base + 추가비용의 합으로 분리된다. K개 최소 추가비용만 더하면 최적.
  - (단조성) budget이 커질수록 가능한 조합 수는 감소하지 않으므로 이분탐색 가능.
  - (프루닝 유효성) 최소 추가비용 기준 정렬 후, budget보다 큰 블록은 더 내려가도 항상 불가능이므로 재귀를 가지치기해 준다.

## 복잡도
- 시간: \(O(((N + K)\log N)\cdot \log V)\) 수준. 여기서 \(V\)는 추가비용 값 범위 상계(각 위치 최대 추가비용 합). 실전에서는 매우 빠르게 동작.
- 공간: \(O(N)\) (정렬된 추가비용 저장 등)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static vector<vector<int>> increments;
static vector<int> firstIncrement;
static long long K;                  // number of robots to build
static long long totalCount;         // count of robots with extra cost <= threshold
static long long savings;            // sum of (threshold - extra) over robots with extra <= threshold

// Count how many combinations (robots) have extra cost <= budget
static void countRobots(int idx, long long budget) {
    if (totalCount >= K) return;
    if (idx != -1 && budget < increments[idx][0]) {
        // Skip blocks whose smallest increment is greater than budget
        idx = int(upper_bound(firstIncrement.begin(), firstIncrement.begin() + idx, (int)budget) - firstIncrement.begin()) - 1;
    }
    if (idx == -1) {
        // All remaining positions can stay at base (extra 0..budget)
        totalCount++;
        return;
    }
    countRobots(idx - 1, budget); // choose base at this position
    const auto& inc = increments[idx];
    for (int i = 0; i < (int)inc.size() && inc[i] <= budget; ++i) {
        countRobots(idx - 1, budget - inc[i]); // choose one upgraded model here
        if (totalCount >= K) return;
    }
}

// Sum over all combinations with extra <= budget of (budget - extra)
static void accumulateSavings(int idx, long long budget) {
    if (idx != -1 && budget < increments[idx][0]) {
        idx = int(upper_bound(firstIncrement.begin(), firstIncrement.begin() + idx, (int)budget) - firstIncrement.begin()) - 1;
    }
    if (idx == -1) {
        savings += budget + 1; // extras can be 0..budget, so contribute budget+1
        return;
    }
    accumulateSavings(idx - 1, budget); // base choice
    const auto& inc = increments[idx];
    for (int i = 0; i < (int)inc.size() && inc[i] <= budget; ++i) {
        accumulateSavings(idx - 1, budget - inc[i]); // upgraded choice
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N >> K)) return 0;

    long long baseCost = 0;
    vector<vector<int>> blocks;
    blocks.reserve(N);
    long long hi = 0; // upper bound for extra cost

    for (int i = 0; i < N; ++i) {
        int m; cin >> m;
        vector<int> v(m);
        for (int j = 0; j < m; ++j) cin >> v[j];
        sort(v.begin(), v.end());
        baseCost += v[0];
        if (m >= 2) {
            vector<int> diffs;
            diffs.reserve(m - 1);
            for (int j = 1; j < m; ++j) diffs.push_back(v[j] - v[0]);
            hi += diffs.back();
            blocks.push_back(move(diffs));
        }
    }

    int usefulN = (int)blocks.size();
    if (usefulN == 0) {
        // Every position had exactly one model; only one robot exists
        cout << baseCost * K << '\n';
        return 0;
    }

    // Sort positions by their smallest increment to enable pruning
    sort(blocks.begin(), blocks.end(),
         [](const vector<int>& a, const vector<int>& b) { return a.front() < b.front(); });

    increments = move(blocks);
    firstIncrement.resize(usefulN);
    for (int i = 0; i < usefulN; ++i) firstIncrement[i] = increments[i][0];

    // Binary search the minimal threshold 'lo' s.t. at least K robots have extra <= lo
    long long lo = 0;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        totalCount = 0;
        countRobots(usefulN - 1, mid);
        if (totalCount < K) lo = mid + 1;
        else hi = mid;
    }

    // Sum of K smallest extras = lo * K - sum_{extra <= lo-1}(lo - extra)
    savings = 0;
    if (lo > 0) accumulateSavings(usefulN - 1, lo - 1);

    long long answer = (baseCost + lo) * K - savings;
    cout << answer << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 모든 위치 \(M_i=1\): 업그레이드 불가이므로 정답은 \(base\cdot K\).
- 큰 K, 작은 추가비용: 이분탐색 하한이 0으로 수렴하는 경우 savings 계산 분기 확인.
- 한 위치에 매우 큰 모델 비용 존재: 값 범위 상계(hi) 계산은 “각 위치 최대 추가비용의 합”으로 충분.
- 오버플로: 합은 64-bit(`long long`) 사용.

## 제출 전 점검
- 입출력 버퍼링: `ios::sync_with_stdio(false); cin.tie(nullptr);`
- 정렬/upper_bound 사용 시 인덱스 경계 및 캐스팅 점검
- 단일 모델 위치 제거 로직(\(m=1\)) 적용 확인
- 이분탐색 수렴 조건과 mid 계산(무한 루프 방지)

## 참고자료/유사문제
- USACO Official Analysis: https://usaco.org/current/data/sol_roboherd_platinum_dec16.html
- Fracturing Search 설명: https://usaco.guide/adv/fracturing-search
- 관련 블로그: https://blog.cube219.me/posts/2022/fracturing-search/


