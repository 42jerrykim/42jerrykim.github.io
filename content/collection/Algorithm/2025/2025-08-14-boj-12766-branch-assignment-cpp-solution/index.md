---
title: "[Algorithm] cpp 백준 12766번: 지사 배정 - D&C DP + 다익스트라"
description: "메시지를 HQ 경유로 순차 전달할 때 비용은 지사별 HQ 왕복거리 합에 (그룹 크기−1)을 곱한 합으로 환원된다. HQ 기준 다익스트라로 w를 구해 정렬·접두사합 후 분할정복 DP로 s구간 최적 분할하여 최소값을 구한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
- Dynamic Programming
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-12766
- cpp
- C++
- Graph
- 그래프
- Directed Graph
- 유향 그래프
- Weighted Graph
- 가중치 그래프
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- All-Pairs via HQ
- 본부 경유
- Prefix Sum
- 접두사 합
- Dynamic Programming
- 동적계획법
- DP Optimization
- DP 최적화
- Divide and Conquer DP
- 분할 정복 DP
- Monge
- 몽주 구조
- Quadrangle Inequality
- 사각 부등식
- Convex Optimization
- 볼록 최적화
- Greedy Structure
- 그리디 구조
- Partitioning
- 구간 분할
- Segmentation
- 구간화
- Sorting
- 정렬
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Competitive Programming
- 경쟁프로그래밍
- ICPC
- ICPC World Finals 2016
- editorial
- 에디토리얼
- Template
- 템플릿
- Testing
- 테스트
- Invariant
- 불변식
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12766
- 요약: b개의 지사를 s개 하위 프로젝트 그룹으로 나눈다. 같은 그룹의 지사들은 월말에 서로에게 메시지를 보낸다. 각 메시지는 `발신 지사 → HQ → 수신 지사`로 전달되며 운반원은 동시에 하나의 메시지만 운반할 수 있다. 전체 전달을 끝내기 위한 운반원의 최소 총 이동거리를 구한다.
- 제한: \(2 \le n \le 5000\), \(1 \le r \le 50000\), 가중치 비음수, 모든 교차로는 서로 도달 가능. 지사 1..b, HQ는 \(b+1\).

## 입력/출력
입력: \(n, b, s, r\)과 도로 \(r\)개 \((u, v, \ell)\). 출력: 최소 총 이동거리.

## 접근 개요
- 핵심 관찰: 한 그룹에서 모든 메시지를 순차적으로 수행하더라도, 다음 작업을 현 위치 지사에서 시작하도록 순서를 잡을 수 있어 추가 이동(재배치) 비용이 들지 않는다. 따라서 그룹의 총 비용은 순수히 각 메시지 경로 길이 합으로 계산된다.
- 정리: 지사 i의 왕복거리 \(w_i = d(i, HQ) + d(HQ, i)\). 크기 \(m\)인 그룹의 전체 비용은 \((m-1) \cdot \sum w_i\). 문제는 \(w\)들을 정렬한 뒤, 이를 s개의 연속 구간으로 분할하여 \(\sum_{grp} (|grp|-1) \cdot \sum_{i\in grp} w_i\)를 최소화하는 문제로 환원된다.
- 구현 계획: HQ 기준 다익스트라 2번(정방향/역방향)으로 \(w_i\) 계산 → 정렬/접두사합 → 분할 DP(모노톤) 최적화.

```mermaid
flowchart TD
    A[입력: n,b,s,r 및 도로] --> B[다익스트라: HQ→*]
    A --> C[다익스트라: *→HQ (역그래프)]
    B --> D[w_i = d(HQ,i)]
    C --> E[w_i += d(i,HQ)]
    D --> F[정렬 및 prefix]
    E --> F
    F --> G[DP[k][i] = min_j DP[k-1][j] + (i-j-1)*(S[i]-S[j])]
    G --> H[정답: DP[s][b]]
```

## 알고리즘
- 거리 전처리: HQ를 기준으로 정방향/역방향 다익스트라로 각각 \(d(HQ, i)\), \(d(i, HQ)\) 계산.
- 가중치 구성: \(w_i = d(HQ,i) + d(i,HQ)\) for i=1..b, 이후 오름차순 정렬.
- 비용식: 구간 \((j+1..i)\)의 비용은 \((i-j-1)\cdot (S[i]-S[j])\) where \(S\)는 \(w\)의 prefix sum.
- DP: `dp[k][i]` = 앞의 i개를 k구간으로 나눈 최소 비용. 점화식은 위 비용식을 사용. 모노톤성이 성립하여 분할정복 최적화로 \(O(s\,b\,\log b)\) 내 계산.

## 복잡도
- 다익스트라 2회: \(O(r \log n)\).
- DP: \(O(s\,b\,\log b)\) (실구현 상 상수 작음). 공간 \(O(b)\) 롤링.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 INF64 = (int64)4e18;

struct Edge {
    int to;
    int w;
};

vector<int64> dijkstra(int n, int src, const vector<vector<Edge>>& g) {
    vector<int64> dist(n + 1, INF64);
    priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [cd, u] = pq.top(); pq.pop();
        if (cd != dist[u]) continue;
        for (const auto& e : g[u]) {
            int v = e.to;
            int64 nd = cd + e.w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    return dist;
}

inline int64 group_cost(int j, int i, const vector<int64>& prefix) {
    return (int64)(i - j - 1) * (prefix[i] - prefix[j]);
}

void compute_dp_layer(int k, int L, int R, int optL, int optR,
                      const vector<int64>& prev, vector<int64>& cur, const vector<int64>& prefix) {
    if (L > R) return;
    int mid = (L + R) >> 1;
    pair<int64,int> best = {INF64, -1};

    int start = max(k - 1, optL);
    int end   = min(mid - 1, optR);

    for (int j = start; j <= end; ++j) {
        int64 cand = prev[j] + group_cost(j, mid, prefix);
        if (cand < best.first) best = {cand, j};
    }
    cur[mid] = best.first;

    int opt = best.second;
    compute_dp_layer(k, L, mid - 1, optL, opt, prev, cur, prefix);
    compute_dp_layer(k, mid + 1, R, opt, optR, prev, cur, prefix);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, b, s, r;
    if (!(cin >> n >> b >> s >> r)) return 0;
    const int HQ = b + 1;

    vector<vector<Edge>> g(n + 1), gr(n + 1);
    for (int i = 0; i < r; ++i) {
        int u, v, l;
        cin >> u >> v >> l;
        g[u].push_back({v, l});
        gr[v].push_back({u, l});
    }

    vector<int64> distFromHQ = dijkstra(n, HQ, g);
    vector<int64> distToHQ   = dijkstra(n, HQ, gr);

    vector<int64> w;
    w.reserve(b);
    for (int i = 1; i <= b; ++i) {
        int64 di = distToHQ[i];
        int64 dj = distFromHQ[i];
        if (di >= INF64/4 || dj >= INF64/4) {
            cout << -1 << '\n';
            return 0;
        }
        w.push_back(di + dj);
    }
    sort(w.begin(), w.end());

    vector<int64> prefix(b + 1, 0);
    for (int i = 1; i <= b; ++i) prefix[i] = prefix[i - 1] + w[i - 1];

    s = min(s, b);
    vector<int64> prev(b + 1, INF64), cur(b + 1, INF64);
    prev[0] = 0;

    for (int k = 1; k <= s; ++k) {
        for (int i = 0; i < k; ++i) cur[i] = INF64;
        compute_dp_layer(k, k, b, k - 1, b - 1, prev, cur, prefix);
        prev.swap(cur);
    }

    cout << prev[b] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- s = 1 또는 s = b (극단의 분할 수)
- r가 많고 가중치 0이 존재하는 그래프
- 모든 지사가 HQ와 같은 거리 패턴을 가지는 경우(동일 \(w_i\))
- 매우 큰 간선 가중치로 인한 64-bit 오버플로 방지

## 제출 전 점검
- 다익스트라 초기화/완화 조건 확인, 역그래프 구성 방향 확인
- `prefix[0]=0` 및 인덱스 경계 확인
- DP 범위: `j ∈ [k-1, i-1]`, `i ∈ [k, b]`
- 출력 개행/형식, `long long` 사용

## 참고자료
- ICPC WF 2016, Problem B 번역판(지사 배정)


