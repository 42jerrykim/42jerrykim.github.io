---
title: "[Algorithm] C++ 백준 11808번: 마리오와 사악한 키노피오"
description: "루트에서 시작·종료하며 루트 제외 K개 성을 주어진 순서로 방문할 때, 키노피오가 최악의 선택을 하면 총 이동 시간의 최댓값을 구한다. 2·∑w·min(s,K+1−s)를 트리 DP와 배낭 합치기로 계산하고 왕복·루트 제외를 반영한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Tree DP
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-11808
- cpp
- C++
- Tree
- 트리
- Graph
- 그래프
- Dynamic Programming
- 동적계획법
- Tree DP
- 트리 DP
- Knapsack
- 배낭합치기
- Divide and Conquer on Tree
- 트리 합치기
- Shortest Path
- 최단경로
- Path Decomposition
- 경로 분해
- Edge Contribution
- 간선 기여도
- Worst-case Order
- 최악의 순서
- Alternating Blocks
- 교대 블록
- Proof of Correctness
- 정당성 증명
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Pitfalls
- 실수 포인트
- Edge Cases
- 코너 케이스
- Tree Knapsack
- 트리 배낭
- Root Exclusion
- 루트 제외
- Return to Root
- 루트 복귀
- Weighted Tree
- 가중치 트리
- DP Merge
- DP 병합
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
- Greedy
- 그리디
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
- Mario
- Toad
- 마리오
- 키노피오
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11808
- 요약: 루트 1에서 시작·종료하며, 키노피오가 루트가 아닌 K개의 정점을 골라 순서를 정한다. 마리오는 각 구간을 항상 최단경로로 이동한다. 키노피오가 노드와 순서를 최악으로 골랐을 때 총 이동 시간을 최대화한 값을 구한다.

## 입력/출력
```
입력: T, 각 테스트케이스마다 N, K와 2..N의 (부모, 간선가중치)
출력: 각 케이스마다 "Case i: 답" 형식
```

## 접근 개요
- 핵심 관찰: 임의 간선 e = (parent, child)의 자식 쪽 서브트리에 고른 노드 수를 s라 하면, 순서를 적절히 번갈아 배치하면 e를 지나는 횟수의 최댓값은 2·min(s, K+1−s).
- 따라서 전체 최댓값은 2·∑(간선가중치 w_e · min(s_e, K+1−s_e)). 간선별 s_e의 합이 K가 되도록 트리에서 s_e를 배분하는 문제로 환원된다.
- 해결 전략: 각 서브트리에서 "정확히 t개를 고를 때 얻는 최댓 기여도"를 DP로 계산하고, 자식 DP를 배낭처럼 병합. 간선 (u,v)의 기여는 t개를 v쪽에서 고를 때 w·min(t, K+1−t)를 더한다.

## 알고리즘 설계
- 자료구조: 인접 리스트. 각 정점 u에 대해 dp[u][t] = u의 서브트리에서 정확히 t개를 고를 때의 최댓 기여도.
- 점화식:
  - 자식 v의 부분해 dp[v][t]에 간선 기여 w·min(t, K+1−t)를 더한 배열을 만든 뒤, 현재 dp와 배낭 병합.
  - 루트(1)를 제외한 정점 u 자체를 고르는 선택을 1개 추가(비용 없음)로 처리.
- 최종값: 루트의 dp[K]를 구해 간선 기여 합을 얻고, 왕복 이동 전체 거리는 이를 2배 한 값.
- 복잡도: O(N·K^2), 메모리 O(N·K). (N≤1000, K≤100에서 충분히 통과)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 NEG_INF = -(1LL<<60);

int N, K;
vector<vector<pair<int,int>>> adj;

vector<int64> dfs(int u, int parent) {
    // dp[t] = max contribution within subtree of u when exactly t nodes are chosen in this subtree
    vector<int64> dp(1, 0); // t = 0
    int currentCap = 0;     // current max t index available in dp

    for (auto [v, w] : adj[u]) {
        if (v == parent) continue;

        vector<int64> child = dfs(v, u);

        // child's contribution + edge(u-v) contribution for selecting t in v-subtree
        int childCap = (int)child.size() - 1;
        vector<int64> bestChild(childCap + 1, NEG_INF);
        for (int t = 0; t <= childCap; ++t) {
            int m = min(t, (K + 1) - t);
            bestChild[t] = child[t] + 1LL * w * m;
        }

        // knapsack merge dp with bestChild
        int newCap = min(K, currentCap + childCap);
        vector<int64> ndp(newCap + 1, NEG_INF);
        for (int a = 0; a <= currentCap; ++a) {
            if (dp[a] <= NEG_INF/2) continue;
            for (int b = 0; b <= childCap; ++b) {
                if (a + b > K) break;
                ndp[a + b] = max(ndp[a + b], dp[a] + bestChild[b]);
            }
        }
        dp.swap(ndp);
        currentCap = newCap;
    }

    // Optionally select node u itself (except root 1): increases count by 1 with no local cost
    if (u != 1) {
        int newCap = min(K, currentCap + 1);
        vector<int64> ndp(newCap + 1, NEG_INF);
        for (int t = 0; t <= currentCap; ++t) {
            // do not select u
            ndp[t] = max(ndp[t], dp[t]);
            // select u
            if (t + 1 <= K) ndp[t + 1] = max(ndp[t + 1], dp[t]);
        }
        dp.swap(ndp);
        currentCap = newCap;
    }

    return dp;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    for (int tc = 1; tc <= T; ++tc) {
        cin >> N >> K;
        adj.assign(N + 1, {});
        for (int i = 2; i <= N; ++i) {
            int p, c; 
            cin >> p >> c;
            adj[p].push_back({i, c});
            adj[i].push_back({p, c});
        }

        vector<int64> rootDP = dfs(1, 0);
        int64 best = rootDP[K];              // sum over edges of w * min(s, K+1 - s)
        int64 answer = 2 * best;             // total travel time (round trips across edges)
        cout << "Case " << tc << ": " << answer << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- K=1(단일 방문), K=N-1(최대 선택)
- 선형 트리/스타 트리 등 극단 구조
- 간선 가중치 0 포함
- 루트(1)는 선택 금지, 마지막에 반드시 루트로 복귀
- 자식 수가 많은 정점에서의 DP 병합 범위(상한 K) 유지

## 제출 전 점검
- 입출력 형식 및 "Case i:" 포맷 확인
- 64-bit 정수 사용(long long)
- DP 초기값과 음의 무한 값 처리
- 루트 제외 로직(u!=1) 누락 여부

## 참고/유사 아이디어
- 간선별 교대 블록 수 상한: blocks_B ≤ min(s, K−s+1) → 교차 횟수 2·blocks_B
- 트리 배낭 병합 표준 구현 패턴


