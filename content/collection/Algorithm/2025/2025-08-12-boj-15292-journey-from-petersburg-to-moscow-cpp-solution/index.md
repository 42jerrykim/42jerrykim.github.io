---
title: "[Algorithm] C++ 백준 15292번 : Journey from Petersburg to Moscow"
description: "도로 네트워크에서 상트페테르부르크→모스크바 최단 경로의 ‘가장 비싼 간선 k개만 결제’ 비용을 최소화한다. 임계값 α에 대해 간선 비용을 max(0, w−α)로 변환해 다익스트라를 수행하고, k·α를 더한 값의 최소를 간선 가중치 집합(및 0)에서 탐색해 정답을 구한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- BOJ
- Baekjoon
- 백준
- 최단경로
- Shortest-Path
- Dijkstra
- Binary-Search
- Optimization
- Graph
- 그래프
- Priority-Queue
- 시간복잡도
- Complexity-Analysis
- Implementation
- 구현
- C++
- IO
- ICPC
- Editorial
- Algorithm
- 알고리즘
- Competitive-Programming
- Problem-Solving
- Time-Complexity
- Coding-Test
- 코딩테스트
- Data-Structures
- 자료구조
- 최적화
- 문제해결
- Code-Quality
- 코드품질
- Go
- .NET
- Git
- GitHub
- Queue
- Python
- Deployment
- Compiler
- Linux
- Space-Complexity
- 공간복잡도
- Edge-Cases
- 엣지케이스
- Testing
- 테스트
- Documentation
- 문서화
- Best-Practices
image: "wordcloud.png"
---

문제: [BOJ 15292 - Journey from Petersburg to Moscow](https://www.acmicpc.net/problem/15292)

### 아이디어 요약
- **핵심 변환(α 트릭)**: 임계값 `α`를 두고 간선 `w`를 비용 `max(0, w−α)`로 바꾸면, 임의의 경로 `P`에 대해
  \(k·α + \sum_{e\in P} \max(0, w_e - α)\) 의 최소값을 구하는 문제가 된다. 이 표현을 `α`에 대해 최소화하면 `P`에서 가장 비싼 간선 `k개`의 합과 같아진다.
- **전역 최적화 교환**: \(\min_P \min_α Φ_α(P) = \min_α \min_P Φ_α(P)\). 따라서 각 `α`마다 변환된 가중치로 최단경로를 구한 뒤 `k·α`를 더하고, 모든 후보 `α`에 대해 최소를 취하면 전역 최적해가 된다.
- **후보 `α` 집합**: `Φ_α`는 간선 가중치에서만 기울기가 바뀌므로 `α ∈ {0} ∪ {모든 w}`만 확인해도 충분하다.
- **알고리즘**: 각 `α`에 대해 가중치 `max(0, w−α)`로 다익스트라를 수행해 `dist[n]`을 구하고, `ans = min(ans, dist[n] + k·α)`를 갱신한다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 INF = (int64)4e18;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, k;
    if (!(cin >> n >> m >> k)) return 0;

    vector<vector<pair<int,int64>>> g(n + 1);
    vector<int64> uniqW;
    uniqW.reserve((size_t)m + 1);
    uniqW.push_back(0); // include α = 0

    for (int i = 0; i < m; ++i) {
        int u, v; int64 w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
        uniqW.push_back(w);
    }

    sort(uniqW.begin(), uniqW.end());
    uniqW.erase(unique(uniqW.begin(), uniqW.end()), uniqW.end());

    auto dijkstra = [&](int64 alpha) -> int64 {
        vector<int64> dist(n + 1, INF);
        priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> pq;
        dist[1] = 0;
        pq.push({0, 1});

        while (!pq.empty()) {
            auto [du, u] = pq.top(); pq.pop();
            if (du != dist[u]) continue;
            if (u == n) break;
            for (auto [v, w] : g[u]) {
                int64 c = (w > alpha ? w - alpha : 0);
                if (dist[v] > du + c) {
                    dist[v] = du + c;
                    pq.push({dist[v], v});
                }
            }
        }
        return dist[n];
    };

    int64 answer = INF;
    for (int64 alpha : uniqW) {
        int64 d = dijkstra(alpha);
        if (d >= INF/2) continue; // connected by problem statement
        answer = min(answer, d + (int64)k * alpha);
    }

    cout << answer << '\n';
    return 0;
}
```

### 복잡도
- `α` 후보 수 ≤ `m + 1 (가중치 종류 + 0)`
- 각 다익스트라 `O((n + m) log n)` → 전체 `O((m + 1) · (n + m) log n)`
- 제약 `n, m ≤ 3000`에서 충분히 빠르게 동작

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 또는 빈 입력 | 반복문 범위·예외 처리 확인 |
| **오버플로우** | 답이 $2^{31}$ 초과 가능 | `long long` (C++) 등 사용 |
