---
title: "[Algorithm] C++ 백준 18473번 : Fast Spanning Tree"
description: "BOJ 18473 Fast Spanning Tree는 인덱스가 작은 간선부터 조건을 만족할 때만 연결하는 과정을 효율적으로 복원하는 문제입니다. DSU(Union-Find)와 small-to-large 병합, 부족분 절반 기준의 watcher, 전역 후보 우선순위 큐를 이용해 O(m log m) 내에 기록된 간선 인덱스 시퀀스를 재현하는 C++ 구현과 핵심 아이디어를 정리했습니다."
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
- "18473"
- "Fast Spanning Tree"
- "FastSpanningTree"
- "DSU"
- "Union Find"
- "Disjoint Set Union"
- "Disjoint Set"
- "Small-to-Large"
- "Merge"
- "Merge Trick"
- "Priority Queue"
- "Min-Heap"
- "Watcher"
- "Half Threshold"
- "Component"
- "컴포넌트"
- "Graph"
- "그래프"
- "Spanning Tree"
- "MST"
- "Greedy"
- "Offline"
- "Simulation"
- "Process"
- "Queue"
- "Index Order"
- "Edge Selection"
- "Edge Threshold"
- "Weight Sum"
- "Vertex Weight"
- "Sum of Weights"
- "Connectivity"
- "Connected Components"
- "Union"
- "Find"
- "Path Compression"
- "Rank"
- "시간복잡도"
- "Time Complexity"
- "O(m log m)"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Problem Solving"
- "문제풀이"
- "해설"
- "Solution"
- "Editorial"
- "Petrozavodsk"
- "Open Cup"
- "300iq"
- "Contest"
image: "wordcloud.png"
---

문제: [BOJ 18473 - Fast Spanning Tree](https://www.acmicpc.net/problem/18473)

### 아이디어 요약
- 과정은 "두 컴포넌트의 정점 가중치 합이 `s_i` 이상이 되는 간선 중, 인덱스가 가장 작은 것을 반복해서 선택"입니다.
- 컴포넌트 관리는 `DSU(Union-Find)`로 하고, 아직 조건을 못 채운 간선은 양끝 컴포넌트에 "watcher"로 걸어 둡니다.
- watcher는 "부족분의 절반(ceil((s - sumA - sumB)/2))만큼은 최소 한쪽이 커져야 재검사 가치가 생김"을 이용해, 각 컴포넌트별 `half` 임계치를 기준으로 최소 힙에 보관합니다.
- 컴포넌트가 합쳐질 때는 small-to-large로 watcher 힙을 큰 쪽에 붙이고, 성숙(half ≤ 현재 합)한 watcher만 꺼내 재검사합니다. 조건을 만족하면 전역 후보 큐(간선 인덱스 기준 최소 힙)에 넣습니다.
- 전역 후보 큐에서 항상 가장 작은 인덱스를 꺼내 DSU로 합치며 위 과정을 반복하면, 노트에 적힌 인덱스 순서를 그대로 얻습니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct CandidateEdge {
    int u;    // component root at scheduling time
    int v;    // component root at scheduling time
    int idx;  // edge index
};
struct CandidateCompare {
    bool operator()(const CandidateEdge& a, const CandidateEdge& b) const {
        return a.idx > b.idx; // min-heap by index
    }
};

struct Watcher {
    int other;       // other component root
    long long s;     // required threshold
    long long half;  // current component sum threshold to re-check
    int idx;         // edge index
};
struct WatcherHalfGreater {
    bool operator()(const Watcher& a, const Watcher& b) const {
        return a.half > b.half; // min-heap by half
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<long long> compWeight(n + 1);
    for (int i = 1; i <= n; ++i) cin >> compWeight[i];

    vector<int> parent(n + 1);
    iota(parent.begin(), parent.end(), 0);

    vector< priority_queue<Watcher, vector<Watcher>, WatcherHalfGreater> > watch(n + 1);
    priority_queue<CandidateEdge, vector<CandidateEdge>, CandidateCompare> fin; // eligible edges by smallest index

    function<int(int)> findRoot = [&](int x) -> int {
        if (parent[x] == x) return x;
        return parent[x] = findRoot(parent[x]);
    };

    auto unite = [&](int a, int b) -> int {
        a = findRoot(a);
        b = findRoot(b);
        if (a == b) return a;
        if (watch[a].size() < watch[b].size()) swap(a, b); // small-to-large by watcher heap size
        parent[b] = a;
        compWeight[a] += compWeight[b];
        while (!watch[b].empty()) { watch[a].push(watch[b].top()); watch[b].pop(); }
        return a;
    };

    function<void(int)> processComponent = [&](int root) {
        root = findRoot(root);
        while (!watch[root].empty()) {
            if (watch[root].top().half > compWeight[root]) break;
            Watcher w = watch[root].top();
            watch[root].pop();

            int other = findRoot(w.other);
            root = findRoot(root);
            if (root == other) continue;

            long long sumR = compWeight[root];
            long long sumO = compWeight[other];

            if (sumR + sumO >= w.s) {
                fin.push({root, other, w.idx});
            } else {
                long long need = (w.s - sumR - sumO + 1) / 2; // positive
                watch[root].push(Watcher{other, w.s, sumR + need, w.idx});
                watch[other].push(Watcher{root, w.s, sumO + need, w.idx});
            }
        }
    };

    for (int i = 1; i <= m; ++i) {
        int a, b; long long s; cin >> a >> b >> s;
        a = findRoot(a); b = findRoot(b);
        if (a == b) continue;
        long long sumA = compWeight[a], sumB = compWeight[b];
        if (sumA + sumB >= s) {
            fin.push({a, b, i});
        } else {
            long long need = (s - sumA - sumB + 1) / 2;
            watch[a].push(Watcher{b, s, sumA + need, i});
            watch[b].push(Watcher{a, s, sumB + need, i});
        }
    }

    vector<int> answer; answer.reserve(m);
    while (!fin.empty()) {
        CandidateEdge cur = fin.top(); fin.pop();
        int u = findRoot(cur.u), v = findRoot(cur.v);
        if (u == v) continue;
        answer.push_back(cur.idx);
        int root = unite(u, v);
        processComponent(root);
    }

    cout << (int)answer.size() << '\n';
    for (int i = 0; i < (int)answer.size(); ++i) {
        if (i) cout << ' ';
        cout << answer[i];
    }
    cout << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(m log m)` 내외 (watcher 재배치 small-to-large, 우선순위 큐 연산 포함)
- 메모리: `O(n + m)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 문제: `https://www.acmicpc.net/problem/18473`
- 출처: Petrozavodsk Programming Camp, Open Cup 2019/2020, 300iq Contest 2 F


