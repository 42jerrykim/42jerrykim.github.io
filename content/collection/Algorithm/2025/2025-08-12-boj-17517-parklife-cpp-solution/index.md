---
title: "[Algorithm] C++ 백준 17517번 : Parklife"
description: "BOJ 17517 Parklife는 교차하지 않는 다리들을 라미나(중첩) 구간 트리로 변환한 뒤, 자식 DP의 볼록한 차이 수열을 small-to-large로 합치고 노드 가중치를 삽입(슬로프 트릭)해 k=1..N의 최댓값을 O(N log^2 N)에 구하는 C++ 풀이를 정리합니다."
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
- "17517"
- "Parklife"
- "라미나"
- "Laminar"
- "Interval"
- "중첩 구간"
- "Non-crossing"
- "교차 없음"
- "Tree"
- "트리"
- "Tree DP"
- "트리 DP"
- "Convex DP"
- "볼록 DP"
- "Slope Trick"
- "슬로프 트릭"
- "Difference Sequence"
- "차이 수열"
- "Priority Queue"
- "우선순위 큐"
- "Small-to-Large"
- "Merge"
- "병합"
- "Max-Heap"
- "힙"
- "Stack"
- "스택"
- "Sort"
- "정렬"
- "Segment"
- "세그먼트"
- "Bridge"
- "다리"
- "Arc"
- "원호"
- "Dynamic Programming"
- "동적 계획법"
- "Greedy"
- "그리디"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Time Complexity"
- "시간복잡도"
- "O(N log^2 N)"
- "Solution"
- "해설"
- "Editorial"
- "Problem Solving"
- "문제풀이"
- "KAIST"
- "Mock Competition"
- "Open Cup"
image: "wordcloud.png"
---

문제: [BOJ 17517 - Parklife](https://www.acmicpc.net/problem/17517)

### 아이디어 요약
- 교차하지 않는 선분(다리)들은 시작·끝 점으로 만든 구간들이 서로 겹치지 않거나 포함 관계만 이루므로, 정렬+스택으로 라미나(중첩) 트리를 만들 수 있습니다.
- 각 노드 `u`에 대해, "루트에서 리프까지 임의 경로에서 선택되는 정점 수 ≤ k" 제약하의 최대 가중치 합을 함수 `F_u(k)`로 두면 볼록(차이 수열이 내림차순)입니다.
- 자식들을 모두 합친 값 `S(k) = sum F_child(k)`의 차이 수열은 자식 차이 수열들의 동일 인덱스 합입니다. 이를 우선순위 큐로 "zipped addition"(큰 것부터 짝지어 더하기, small-to-large)로 구현합니다.
- 부모 정점 `u`를 선택하는 경우는 `T(k) = w_u + S(k-1)`이며, `F_u(k) = max(S(k), T(k))`입니다. 차이 수열 관점에선 `S`의 차이 수열에 `w_u`를 하나 삽입(슬로프 트릭)하면 `F_u`가 됩니다.
- 루트의 차이 수열에서 상위 `k`개의 합이 정답 `ans[k]`이므로, 최대 `N`번까지 누적해 `k=1..N`을 출력합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int s, e;                 // interval [s, e]
    long long w;              // weight (aesthetic value)
    vector<int> child;        // children in laminar tree
    priority_queue<long long> diffs; // descending difference sequence of F_u
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; if (!(cin >> N)) return 0;
    vector<Node> a(N + 1);
    const int ROOT = 0;
    a[ROOT].s = -1; a[ROOT].e = INT_MAX; a[ROOT].w = 0;

    for (int i = 1; i <= N; ++i) {
        int S, E; long long V; cin >> S >> E >> V;
        a[i].s = S; a[i].e = E; a[i].w = V;
    }

    // Build laminar tree: sort by (s asc, e desc), stack to assign parent
    vector<int> ord(N);
    iota(ord.begin(), ord.end(), 1);
    sort(ord.begin(), ord.end(), [&](int x, int y){
        if (a[x].s != a[y].s) return a[x].s < a[y].s;
        return a[x].e > a[y].e; // longer first when start equal
    });

    vector<int> st; st.reserve(N + 1);
    st.push_back(ROOT);
    for (int id : ord) {
        while (!st.empty() && a[st.back()].e <= a[id].s) st.pop_back();
        int p = st.empty() ? ROOT : st.back();
        a[p].child.push_back(id);
        st.push_back(id);
    }

    // Postorder (iterative) to process children before parent
    vector<int> post; post.reserve(N + 1);
    vector<pair<int,int>> dfs; dfs.reserve(N + 1);
    dfs.push_back({ROOT, 0});
    while (!dfs.empty()) {
        auto [u, t] = dfs.back(); dfs.pop_back();
        if (t == 0) {
            dfs.push_back({u, 1});
            for (int v : a[u].child) dfs.push_back({v, 0});
        } else post.push_back(u);
    }

    auto merge_into = [&](int u, int v) {
        // Pointwise add child v into u on difference sequences via zipped addition.
        // Keep u as the larger container (small-to-large) to bound complexity.
        if (a[v].diffs.size() > a[u].diffs.size()) swap(a[u].diffs, a[v].diffs);
        vector<long long> buf; buf.reserve(a[v].diffs.size());
        while (!a[v].diffs.empty()) {
            long long bv = a[v].diffs.top(); a[v].diffs.pop();
            long long au = 0;
            if (!a[u].diffs.empty()) { au = a[u].diffs.top(); a[u].diffs.pop(); }
            buf.push_back(au + bv);
        }
        for (long long x : buf) a[u].diffs.push(x);
    };

    for (int u : post) {
        // 1) Merge all children into u (S = sum of children)
        for (int v : a[u].child) merge_into(u, v);
        // 2) Insert node weight (F = max(S, w + S shifted)) => push w into diffs
        a[u].diffs.push(a[u].w);
    }

    // Root answers: prefix sums of top k differences
    vector<long long> ans(N + 1, 0);
    long long acc = 0;
    for (int k = 1; k <= N; ++k) {
        if (!a[ROOT].diffs.empty()) { acc += a[ROOT].diffs.top(); a[ROOT].diffs.pop(); }
        ans[k] = acc;
    }

    for (int k = 1; k <= N; ++k) {
        if (k > 1) cout << ' ';
        cout << ans[k];
    }
    cout << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(N log^2 N)` (small-to-large 병합 × 힙 연산)
- 메모리: `O(N)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 문제: `https://www.acmicpc.net/problem/17517`
- 대회: KAIST ICPC Mock / Open Cup Korea GP (J)


