---
title: "[BOJ] Fireworks (12736) - 트리 DP O(N log^2 N) C++"
description: "백준 12736 Fireworks(APIO 2016)는 스위치-연결점-폭약으로 이루어진 트리에서 모든 폭약의 폭발 시각을 같게 만들기 위해 도화선 길이를 조정하는 최소 비용을 구하는 문제입니다. 볼록 함수(slope trick) 기반 트리 DP와 small-to-large 우선순위 큐 합병으로 O((N+M) log^2(N+M))에 해결합니다. 구현 핵심은 기울기 변화 지점을 우선순위 큐로 관리하고, 간선 통과 시 upperize 연산으로 기울기와 절편 변화를 반영하는 것입니다. 안전한 64-bit 정수 사용과 서브트리 크기 기준 정렬로 상수 시간을 줄여 AC를 얻습니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "12736"
- "Fireworks"
- "APIO"
- "APIO-2016"
- "Asia-Pacific Informatics Olympiad"
- "Tree"
- "트리"
- "Tree-DP"
- "DP"
- "Dynamic-Programming"
- "Slope-Trick"
- "슬로프-트릭"
- "Convex-Function"
- "볼록함수"
- "Piecewise-Linear"
- "Priority-Queue"
- "우선순위-큐"
- "Small-to-Large"
- "Merge-Heaps"
- "힙-합병"
- "Subtree"
- "서브트리"
- "Rooted-Tree"
- "루트-트리"
- "DFS"
- "깊이우선탐색"
- "Edge-Weight"
- "간선-가중치"
- "Cost-Minimization"
- "최소-비용"
- "Optimization"
- "최적화"
- "Time-Complexity"
- "시간-복잡도"
- "N-log2-N"
- "O-N-log2-N"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast-IO"
- "빠른-입출력"
- "long-long"
- "64-bit"
- "정수-오버플로"
- "트리-정렬"
- "정렬"
- "서브트리-크기"
- "기울기"
- "slope"
- "에지-길이"
- "도화선"
- "동시-폭발"
- "Problem-Solving"
- "PS"
- "Competitive-Programming"
- "Solution-Code"
- "정답-코드"
- "Editorial"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 12736 - Fireworks](https://www.acmicpc.net/problem/12736)

### 아이디어 요약
- 스위치(1번)에서 각 폭약까지 도달 시간을 모두 같게 만들도록 간선 길이를 증감하는 최소 비용을 구합니다. 비용은 조정 전후 길이 차이의 절댓값 합.
- 리프(폭약) 기준으로 정의되는 DP가 볼록(piecewise linear convex) 형태가 됩니다. 기울기 변화 지점을 우선순위 큐에 저장해 함수 합과 간선 통과 연산을 빠르게 처리합니다.
- 서브트리별 구조를 `priority_queue`로 표현하고, "작은 힙을 큰 힙으로 합치는" small-to-large 기법으로 전체를 합치면 `O((N+M) log^2(N+M))`에 해결됩니다.
- 간선을 위로 타고 오를 때 수행하는 `upperize` 연산으로 기울기 상한(≤1) 유지 및 변화 지점 이동(+c) 반영을 합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using lint = long long;

const int MAXN = 300000 + 5;

int n, m, sz[MAXN];
lint dep[MAXN], c[MAXN];
vector<int> gph[MAXN];

struct Func {
    priority_queue<lint> pq;
    lint cost;
    int slope;

    void init() {
        cost = 0;
        slope = -1;
        pq.push(0);
        pq.push(0);
    }
    void upperize(int x) {
        cost += c[x];
        while (!pq.empty() && slope + (int)pq.size() > 1) {
            pq.pop();
        }
        vector<lint> v;
        while (!pq.empty() && slope + (int)pq.size() >= 0) {
            v.push_back(pq.top());
            pq.pop();
        }
        while (!v.empty()) {
            pq.push(v.back() + c[x]);
            v.pop_back();
        }
    }
} dp[MAXN];

static inline bool cmpSize(int a, int b) { return sz[a] > sz[b]; }

void dfs(int x) {
    if (x > n) { sz[x] = 1; return; }
    for (int y : gph[x]) {
        dep[y] = dep[x] + c[y];
        dfs(y);
        sz[x] += sz[y];
    }
    sort(gph[x].begin(), gph[x].end(), cmpSize);
}

int solve(int x) {
    if (x > n) { dp[x].init(); return x; }
    int ret = solve(gph[x][0]);
    dp[ret].upperize(gph[x][0]);
    for (int i = 1; i < (int)gph[x].size(); i++) {
        int t = solve(gph[x][i]);
        dp[t].upperize(gph[x][i]);
        dp[ret].cost += dp[t].cost;
        dp[ret].slope += dp[t].slope;
        while (!dp[t].pq.empty()) {
            dp[ret].pq.push(dp[t].pq.top());
            dp[t].pq.pop();
        }
    }
    return ret;
}

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 2; i <= n + m; i++) {
        int p; scanf("%d %lld", &p, &c[i]);
        gph[p].push_back(i);
    }
    dfs(1);
    Func ret = dp[solve(1)];
    ret.upperize(0);
    lint best = ret.pq.top();
    lint ans = ret.cost + best * ret.slope;
    while (!ret.pq.empty()) {
        ans += best - ret.pq.top();
        ret.pq.pop();
    }
    printf("%lld\n", ans);
    return 0;
}
```

### 복잡도
- 시간: `O((N+M) log^2 (N+M))`
- 공간: `O(N+M)`

### 참고
- 문제: `https://www.acmicpc.net/problem/12736`
- 배경: APIO 2016 Fireworks


