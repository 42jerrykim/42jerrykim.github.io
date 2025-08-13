---
title: "[Algorithm] C++ 백준 18586번 : Salty Fish"
description: "트리의 각 노드 사과를 모두 먹되, 카메라가 보는 구간(p(x,k))의 변화를 막기 위해 일부 카메라를 매수(비용 c)하거나 일부 정점을 포기하는 문제를 최소 컷으로 환원한다. 거대한 일반 네트워크 대신 트리 구조를 활용해 dp(map<depth,sum>)을 small-to-large로 병합하고, 카메라별 커버 가능한 가장 깊은 depth부터 잔여 유량을 소모해 Max-Flow=Min-Cut을 암시적으로 계산, 전체 사과 합 − 유량으로 최대 수익을 구한다. 시간복잡도는 O((n+m) log n)으로 테스트케이스 합 n,m ≤ 10^6에서도 빠르게 동작한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "18586"
- "Salty Fish"
- "Tree"
- "트리"
- "Tree DP"
- "트리 DP"
- "Small-to-Large"
- "Map Merge"
- "std::map"
- "Ordered Map"
- "Depth"
- "깊이"
- "Subtree"
- "서브트리"
- "Camera"
- "카메라"
- "Flow"
- "유량"
- "Cut"
- "컷"
- "Min-cut"
- "Minimum Cut"
- "Max-flow"
- "Maximum Flow"
- "Ford-Fulkerson"
- "Residual Capacity"
- "잔여 용량"
- "Source"
- "Sink"
- "s-t Cut"
- "INF Edge"
- "무한 용량"
- "Greedy"
- "그리디"
- "DP"
- "Dynamic Programming"
- "Algorithm"
- "알고리즘"
- "Problem Solving"
- "문제풀이"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "ICPC"
- "Petrozavodsk"
- "Programming Camp"
- "Songyang Chen Contest 2"
- "Summer 2019"
- "최대 이익"
- "최소 컷"
- "트리 병합"
- "upper_bound"
- "ordered structure"
image: "wordcloud.png"
---

문제: [BOJ 18586 - Salty Fish](https://www.acmicpc.net/problem/18586)

### 아이디어 요약
- **목표**: 전체 사과 합에서, 바뀐 사진이 없어야 하므로 일부 정점을 포기하거나 일부 카메라를 매수하여 최종 이익을 최대화.
- **모형화(최소 컷)**: 카메라를 선택하면 비용 `c`(소스→카메라), 카메라가 커버하는 정점들은 무한 용량(카메라→정점), 정점은 사과 수 `a_i`(정점→싱크). 최소 컷 값이 "지불해야 하는 총 손실"이 되고, 정답은 `sum(a) − mincut = sum(a) − maxflow`.
- **직접 네트워크 구성 대신 트리 특화 계산**: 노드 `v`에 대해 `map<depth, sumApples>`을 유지하고 자식 맵을 small-to-large로 병합. 각 카메라 `(k, c)`는 `depth ≤ dep[v]+k` 범위의 가장 깊은 depth부터 사과를 소모(유량을 흘림). 이를 통해 암시적으로 최대 유량을 계산.
- **복잡도**: 각 원소가 맵에서 상수 회 이동하며 `upper_bound`로 찾기 때문에 전체 `O((n+m) log n)`.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n, m;
        cin >> n >> m;

        vector<vector<int>> children(n + 1);
        vector<int> parent(n + 1, 0);
        for (int i = 2; i <= n; ++i) {
            int p; cin >> p;
            parent[i] = p;
            children[p].push_back(i);
        }

        vector<long long> apples(n + 1, 0);
        long long totalApples = 0;
        for (int i = 1; i <= n; ++i) {
            cin >> apples[i];
            totalApples += apples[i];
        }

        vector<vector<pair<int, long long>>> cameras(n + 1);
        for (int i = 0; i < m; ++i) {
            int x, k; long long c;
            cin >> x >> k >> c;
            cameras[x].push_back({k, c});
        }

        vector<int> depth(n + 1, 0);
        for (int i = 2; i <= n; ++i) depth[i] = depth[parent[i]] + 1;

        vector<map<int, long long>> depthToApples(n + 1);
        long long flow = 0;

        for (int v = n; v >= 1; --v) {
            depthToApples[v][depth[v]] += apples[v];

            for (int u : children[v]) {
                if (depthToApples[v].size() < depthToApples[u].size())
                    depthToApples[v].swap(depthToApples[u]);
                for (auto &kv : depthToApples[u])
                    depthToApples[v][kv.first] += kv.second;
                depthToApples[u].clear();
            }

            if (!cameras[v].empty()) {
                for (auto &cam : cameras[v]) {
                    int k = cam.first;
                    long long ff = cam.second;
                    while (ff > 0 && !depthToApples[v].empty()) {
                        auto it = depthToApples[v].upper_bound(depth[v] + k);
                        if (it == depthToApples[v].begin()) break;
                        --it;
                        long long take = min(ff, it->second);
                        flow += take;
                        ff -= take;
                        it->second -= take;
                        if (it->second == 0) depthToApples[v].erase(it);
                    }
                }
            }
        }

        cout << (totalApples - flow) << '\n';
    }
    return 0;
}
```

### 복잡도
- 시간: `O((n + m) log n)` — 각 원소는 맵에서 소수 회 이동/삭제, 카메라당 `upper_bound` 탐색.
- 공간: `O(n)` 맵의 총 원소 수(깊이별 사과 합)와 트리/카메라 입력.

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`


