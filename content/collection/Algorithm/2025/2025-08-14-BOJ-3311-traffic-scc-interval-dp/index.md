---
title: "[Algorithm] C++ 백준 3311번: Traffic - SCC 압축과 DAG 구간 전파"
description: "섬 내부 도로망은 선분 도로가 교차하지 않는 평면 그래프이므로, SCC 압축 DAG에서 각 컴포넌트가 도달할 수 있는 동쪽 경계 정점 집합은 y좌표 기준 연속 구간이 됩니다. 이를 이용해 동쪽 경계 정점(서쪽에서 실제로 도달 가능한 것만)을 y 오름차순으로 인덱싱하고, 자식 구간을 부모로 병합하는 역위상 전파로 각 서쪽 정점의 답(서쪽 정점에서 도달 가능한 동쪽 정점 수)을 O(n+m)에 계산합니다. 구현은 반복형 Kosaraju + 압축 그래프 위상정렬 기반입니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-3311
- cpp
- C++
- Graph
- 그래프
- SCC
- 강한연결요소
- Kosaraju
- 코사라주
- Tarjan
- 타잔
- DAG
- 위상정렬
- Topological Sort
- Reachability
- 도달성
- Interval DP
- 구간 DP
- Condensation Graph
- 압축그래프
- Planar Graph
- 평면그래프
- Geometry
- 기하
- Directed Graph
- 유향그래프
- Bidirectional Edge
- 양방향간선
- DFS
- BFS
- Iterative DFS
- 반복형DFS
- Stack
- 스택
- Queue
- 큐
- Sorting
- 정렬
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Competitive Programming
- 경쟁프로그래밍
- CEOI
- CEOI-2011
- Traffic
- Interval Propagation
- 구간 전파
- Condensed DAG
- 압축 DAG
- Planarity Property
- 연속구간성
- Fast IO
- 빠른입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3311
- 요약: 직사각형 섬(서쪽 x=0, 동쪽 x=A) 안의 교차하지 않는 도로망이 주어질 때, 각 서쪽 경계 교차로에서 도달 가능한 동쪽 경계 교차로의 개수를 구합니다. 출력은 서쪽 경계 교차로의 y좌표 내림차순.
- 제한/스펙: n ≤ 300,000, m ≤ 900,000, 시간 5초, 메모리 128MB. 좌표는 0 ≤ x ≤ A, 0 ≤ y ≤ B.

## 입력/출력 요약
```
입력
n m A B
x_i y_i   (i=1..n)
c_j d_j k_j   (j=1..m, k_j∈{1,2}, 1=단방향 c→d, 2=양방향)

출력
서쪽 경계(x=0) 정점을 y 내림차순으로 훑으며, 각 정점에서 도달 가능한 동쪽 경계(x=A) 정점의 수를 한 줄에 하나씩 출력
```

## 접근 개요(아이디어)
- 도로가 서로 교차하지 않는 선분이므로 그래프는 평면적 구조이며, SCC 압축 DAG에서 임의 컴포넌트가 도달 가능한 동쪽 경계 정점들의 y순서는 항상 연속 구간이 됩니다(연속구간성).
- 절차
  1) 모든 서쪽 정점에서 한 번의 BFS/DFS로 도달 표시(fromLeft).
  2) 그래프를 SCC로 압축해 DAG를 구성.
  3) 서쪽에서 실제로 도달 가능한 동쪽 경계 정점만 y 오름차순으로 정렬해 0..R-1로 인덱싱.
  4) 각 컴포넌트에 대해 포함하는 동쪽 정점 기반으로 [lo,hi] 구간 초기화.
  5) 역위상 순회로 자식 구간을 부모로 병합(최솟값/최댓값 전파).
  6) 서쪽 정점을 y 내림차순으로 출력하며, 답은 hi-lo+1(없으면 0).

## 알고리즘 설계
- **SCC**: 반복형 Kosaraju(스택 기반)로 O(n+m)에서 순서/컴포넌트 계산 → 재귀 한계 회피.
- **압축 DAG 구성**: 서로 다른 컴포넌트 간 간선만 생성. Kahn 위상정렬.
- **구간 전파**: 역위상 순서에서 부모의 [lo,hi]에 자식 구간을 병합. 초기값이 없는 경우(hi=-1)는 그대로 유지.
- **정당성**: 평면성에 의해 경계에서의 도달 집합이 끊기지 않고 연속 구간이 되며, DAG 상에서 하위 도달 집합의 합집합 역시 구간의 합집합이자 하나의 구간이 됩니다.

## 복잡도
- 시간: O(n + m)
- 공간: O(n + m)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static inline int readInt() {
    int x = 0, c = getchar_unlocked(), s = 1;
    while (c != '-' && (c < '0' || c > '9')) c = getchar_unlocked();
    if (c == '-') { s = -1; c = getchar_unlocked(); }
    for (; c >= '0' && c <= '9'; c = getchar_unlocked()) x = x * 10 + (c - '0');
    return x * s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n = readInt();
    int m = readInt();
    int A = readInt();
    int B = readInt();

    vector<int> X(n + 1), Y(n + 1);
    vector<int> leftNodes, rightNodesAll;
    for (int i = 1; i <= n; i++) {
        X[i] = readInt();
        Y[i] = readInt();
        if (X[i] == 0) leftNodes.push_back(i);
        if (X[i] == A) rightNodesAll.push_back(i);
    }

    const int Emax = 2 * m + 5;
    vector<int> head(n + 1, -1), headR(n + 1, -1);
    vector<int> to(Emax), nx(Emax), toR(Emax), nxR(Emax);
    int ePtr = 0;
    auto addEdge = [&](int u, int v) {
        to[ePtr] = v; nx[ePtr] = head[u]; head[u] = ePtr;
        toR[ePtr] = u; nxR[ePtr] = headR[v]; headR[v] = ePtr;
        ++ePtr;
    };

    for (int i = 0; i < m; i++) {
        int c = readInt(), d = readInt(), k = readInt();
        addEdge(c, d);
        if (k == 2) addEdge(d, c);
    }

    // 1) fromLeft: 서쪽에서 도달 가능한 정점 표시
    vector<char> fromLeft(n + 1, 0);
    deque<int> dq;
    for (int s : leftNodes) {
        if (!fromLeft[s]) { fromLeft[s] = 1; dq.push_back(s); }
    }
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (int ei = head[u]; ei != -1; ei = nx[ei]) {
            int v = to[ei];
            if (!fromLeft[v]) { fromLeft[v] = 1; dq.push_back(v); }
        }
    }

    // 2) SCC (iterative Kosaraju)
    vector<char> seen(n + 1, 0);
    vector<int> it(n + 1, -1), order; order.reserve(n);
    vector<int> st;

    for (int s = 1; s <= n; s++) if (!seen[s]) {
        st.clear(); st.push_back(s); seen[s] = 1; it[s] = head[s];
        while (!st.empty()) {
            int u = st.back();
            int &ei = it[u];
            while (ei != -1 && seen[to[ei]]) ei = nx[ei];
            if (ei == -1) { order.push_back(u); st.pop_back(); }
            else { int v = to[ei]; ei = nx[ei]; seen[v] = 1; it[v] = head[v]; st.push_back(v); }
        }
    }

    vector<int> comp(n + 1, -1);
    int compCnt = 0;
    for (int idx = (int)order.size() - 1; idx >= 0; idx--) {
        int s = order[idx];
        if (comp[s] != -1) continue;
        st.clear(); st.push_back(s); comp[s] = compCnt;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int ei = headR[u]; ei != -1; ei = nxR[ei]) {
                int v = toR[ei];
                if (comp[v] == -1) { comp[v] = compCnt; st.push_back(v); }
            }
        }
        ++compCnt;
    }

    // 3) 동쪽 정점 중 서쪽에서 도달 가능한 것들만 y 오름차순 인덱싱
    vector<pair<int,int>> rightFiltered; // (y, id)
    rightFiltered.reserve(rightNodesAll.size());
    for (int v : rightNodesAll) if (fromLeft[v]) rightFiltered.emplace_back(Y[v], v);
    sort(rightFiltered.begin(), rightFiltered.end());
    int R = (int)rightFiltered.size();

    const int INF = 0x3f3f3f3f;
    vector<int> lo(compCnt, INF), hi(compCnt, -1);
    for (int i = 0; i < R; i++) {
        int v = rightFiltered[i].second;
        int c = comp[v];
        lo[c] = min(lo[c], i);
        hi[c] = max(hi[c], i);
    }

    // 4) 압축 DAG 구성 및 위상정렬
    vector<int> headD(compCnt, -1), toD(Emax), nxD(Emax), indeg(compCnt, 0);
    int ePtrD = 0;
    auto addEdgeD = [&](int u, int v) {
        toD[ePtrD] = v; nxD[ePtrD] = headD[u]; headD[u] = ePtrD;
        indeg[v]++; ++ePtrD;
    };
    for (int u = 1; u <= n; u++) {
        int cu = comp[u];
        for (int ei = head[u]; ei != -1; ei = nx[ei]) {
            int v = to[ei]; int cv = comp[v];
            if (cu != cv) addEdgeD(cu, cv);
        }
    }

    deque<int> q;
    for (int i = 0; i < compCnt; i++) if (indeg[i] == 0) q.push_back(i);
    vector<int> topo; topo.reserve(compCnt);
    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        topo.push_back(u);
        for (int ei = headD[u]; ei != -1; ei = nxD[ei]) {
            int v = toD[ei];
            if (--indeg[v] == 0) q.push_back(v);
        }
    }

    // 5) 역위상에서 자식 구간을 부모로 병합
    for (int i = (int)topo.size() - 1; i >= 0; i--) {
        int u = topo[i];
        for (int ei = headD[u]; ei != -1; ei = nxD[ei]) {
            int v = toD[ei];
            if (hi[v] != -1) {
                if (hi[u] == -1) { lo[u] = lo[v]; hi[u] = hi[v]; }
                else { lo[u] = min(lo[u], lo[v]); hi[u] = max(hi[u], hi[v]); }
            }
        }
    }

    // 6) 서쪽 정점 y 내림차순 출력
    vector<pair<int,int>> leftSorted;
    leftSorted.reserve(leftNodes.size());
    for (int v : leftNodes) leftSorted.emplace_back(-Y[v], v);
    sort(leftSorted.begin(), leftSorted.end());

    ostringstream out;
    for (auto &p : leftSorted) {
        int v = p.second; int c = comp[v];
        int ans = (hi[c] == -1 ? 0 : (hi[c] - lo[c] + 1));
        out << ans << '\n';
    }
    cout << out.str();
    return 0;
}
```

## 코너 케이스 체크리스트
- 서쪽 정점에서 어떤 동쪽 정점에도 도달하지 못하는 경우 → 0 출력
- 동쪽 경계 정점이 서쪽에서 전혀 도달 불가 → 인덱싱에서 제외되어 구간에 반영되지 않음
- 다중 간선/자기 루프 존재 → SCC 단계에서 자연스럽게 흡수, DAG에는 영향 없음
- 출력 정렬 조건: 서쪽 정점 y 내림차순 보장

## 참고자료
- CEOI 2011 Booklet: http://ceoi.inf.elte.hu/probarch/11/ceoi2011booklet.pdf
- OJ.uz (CEOI 2011 Traffic): https://oj.uz/problem/view/CEOI11_tra


