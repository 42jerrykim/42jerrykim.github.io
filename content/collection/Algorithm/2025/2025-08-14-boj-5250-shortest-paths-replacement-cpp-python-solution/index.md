---
title: "[Algorithm] C++/Python 백준 5250번: 최단 경로들"
description: "BOI 2012 ‘최단 경로들’. 다익스트라 2회와 최단경로 DAG에서 구간 후보를 만들고, 우선순위큐 스윕으로 각 경로 간선 폐쇄 시 a→b 대체 최단거리를 O(m log n)으로 계산합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-5250"
- "cpp"
- "python"
- "C++"
- "Python"
- "Data Structures"
- "자료구조"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Graph"
- "그래프"
- "Shortest Path"
- "최단경로"
- "Dijkstra"
- "다익스트라"
- "Replacement Paths"
- "대체 최단경로"
- "BOI"
- "BOI 2012"
- "Shortest Path DAG"
- "경로 DAG"
- "Interval Sweep"
- "구간 스윕"
- "Priority Queue"
- "우선순위큐"
- "Heap"
- "힙"
- "Weighted Graph"
- "가중그래프"
- "Undirected Graph"
- "무방향그래프"
- "Edge Deletion"
- "간선 삭제"
- "Path Interval"
- "경로 구간"
- "Index Propagation"
- "인덱스 전파"
- "Fast IO"
- "빠른입출력"
- "long long"
- "64-bit"
- "Python3"
- "C++17"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/5250
- 요약: 두 마을 `a`→`b` 사이 최단 경로가 주어졌을 때, 그 경로의 각 간선이 하루씩 폐쇄될 경우의 대체 최단거리들을 모두 구하는 문제입니다. 그래프는 무방향 가중치 그래프입니다.

## 입력/출력
```
입력
n m a b
u v w  (m줄)
k v1 v2 ... vk  (v1=a, vk=b: 주어진 최단 경로)

출력
각 t=1..k-1에 대해, 간선 (v_t, v_{t+1}) 가 막힐 때의 a→b 최단거리. 경로가 없으면 -1.
```

예시
```
입력
5 6 1 5
1 2 1
2 3 3
2 5 100
3 4 3
3 5 5
4 5 3
4 1 2 3 5

출력
-1
101
10
```

## 접근 개요
- 핵심은 Replacement Paths(대체 최단경로)입니다. a에서의 최단거리 `distA`와 b에서의 최단거리 `distB`를 각각 한 번씩 다익스트라로 구합니다.
- 최단경로 DAG 위에서, 각 정점 `x`에 대해 “원래 경로에서 어디까지 왔는지”(좌측 경계 `idxA[x]`)와 “원래 경로에서 어디서 다시 합류하는지”(우측 경계 `idxB[x]`)를 전파합니다.
- 모든 방향 간선 `u→v`에 대해 후보 값 `distA[u] + w(u,v) + distB[v]`와 유효 구간 `[l=idxA[u], r=idxB[v])`를 만들고, 시작 인덱스별로 묶어 최소값을 스윕(PQ)으로 빠르게 찾아 각 단절 간선의 답을 얻습니다.

```mermaid
flowchart TD
    A[다익스트라 from a → distA] --> C[idxA 전파(최단경로 DAG)]
    B[다익스트라 from b → distB] --> D[idxB 전파(역방향 DAG)]
    C --> E[모든 u→v에 대해
            후보 값 = distA[u]+w+distB[v],
            구간 [l=idxA[u], r=idxB[v])]
    D --> E
    E --> F[t=1..k-1에 대해 시작점별 후보를 PQ에 추가,
            r≤t 후보 제거,
            top의 값이 답]
```

## 알고리즘
1) `distA = dijkstra(a)`, `distB = dijkstra(b)`.
2) 경로 정점 `v_i`에 대해 `pos[v_i]=i`. `idxA[v_i]=i`, `idxB[v_i]=i`를 초기화.
3) 최단경로 DAG에서 `distA[u]+w=distA[v]`인 간선들로 `idxA[v]=max(idxA[v], idxA[u])`를 거리 오름차순으로 전파.
4) 역방향 DAG에서 `distB[x]=distB[y]+w`이면 `idxB[x]=min(idxB[x], idxB[y])`를 거리 오름차순으로 전파.
5) 모든 방향 간선 `(u→v)`에 대해
   - 값 = `distA[u] + w + distB[v]`
   - 구간 `[l=idxA[u], r=idxB[v])`가 유효(1≤l<r≤k)이면, 시작점 `l`에 (값, r) 후보를 추가. 단, 본래 경로 간선 `(v_t→v_{t+1})` 자체는 제외.
6) `t=1..k-1` 스윕: 시작점이 `t`인 후보들을 PQ에 넣고, `r≤t`는 제거. PQ top이 해당 `t`의 정답(없으면 -1).

## 복잡도
- 시간: O((n+m) log n) + 후보 병합 스윕 O(m log m) ≈ O(m log n)
- 공간: O(n + m)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 INF = (int64)4e18;

struct Edge { int u, v, w; };

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, a, b;
    if(!(cin >> n >> m >> a >> b)) return 0;

    vector<vector<pair<int,int>>> adj(n+1);
    vector<Edge> edges;
    edges.reserve(m);

    for(int i=0;i<m;i++){
        int u,v,w; cin >> u >> v >> w;
        adj[u].push_back({v,w});
        adj[v].push_back({u,w});
        edges.push_back({u,v,w});
    }

    int k; cin >> k;
    vector<int> path(k+1);
    for(int i=1;i<=k;i++) cin >> path[i];

    vector<int> pos(n+1, -1);
    for(int i=1;i<=k;i++) pos[path[i]] = i;

    auto dijkstra = [&](int src){
        vector<int64> dist(n+1, INF);
        priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> pq;
        dist[src] = 0;
        pq.push({0, src});
        while(!pq.empty()){
            auto [d,u] = pq.top(); pq.pop();
            if(d != dist[u]) continue;
            for(auto [v,w] : adj[u]){
                int64 nd = d + (int64)w;
                if(nd < dist[v]){ dist[v]=nd; pq.push({nd,v}); }
            }
        }
        return dist;
    };

    vector<int64> distA = dijkstra(a);
    vector<int64> distB = dijkstra(b);

    vector<int> idxA(n+1, -1);
    for(int i=1;i<=k;i++) idxA[path[i]] = i;

    vector<int> orderA(n);
    iota(orderA.begin(), orderA.end(), 1);
    sort(orderA.begin(), orderA.end(), [&](int x, int y){
        if(distA[x]==distA[y]) return x<y; return distA[x]<distA[y];
    });
    for(int u: orderA){
        if(distA[u] >= INF/2) continue;
        for(auto [v,w] : adj[u]){
            if(distA[u] + w == distA[v]){
                idxA[v] = max(idxA[v], idxA[u]);
            }
        }
    }

    vector<int> idxB(n+1, INT_MAX);
    for(int i=1;i<=k;i++) idxB[path[i]] = min(idxB[path[i]], i);

    vector<int> orderB(n);
    iota(orderB.begin(), orderB.end(), 1);
    sort(orderB.begin(), orderB.end(), [&](int x, int y){
        if(distB[x]==distB[y]) return x<y; return distB[x]<distB[y];
    });
    for(int x: orderB){
        if(distB[x] >= INF/2) continue;
        for(auto [y,w] : adj[x]){
            if(distB[x] == distB[y] + w){
                idxB[x] = min(idxB[x], idxB[y]);
            }
        }
    }

    auto enc = [&](int u, int v)->uint64_t{ return (uint64_t)u<<32 ^ (uint32_t)v; };
    unordered_set<uint64_t> pathDir; pathDir.reserve((size_t)k*2+3);
    for(int t=1;t<=k-1;t++) pathDir.insert(enc(path[t], path[t+1]));

    vector<vector<pair<long long,int>>> starts(k+2);
    auto add_interval = [&](int from, int to, int w){
        if(distA[from] >= INF/2 || distB[to] >= INF/2) return;
        int l = idxA[from];
        int r = idxB[to];
        if(l>=1 && r<=k && l<r){
            bool isPathEdge = (pos[from]>=1 && pos[to]>=1 && pos[from]+1==pos[to] && pathDir.count(enc(from,to)));
            if(!isPathEdge){
                long long val = distA[from] + (long long)w + distB[to];
                starts[l].push_back({val, r});
            }
        }
    };

    for(const auto &e: edges){
        add_interval(e.u, e.v, e.w);
        add_interval(e.v, e.u, e.w);
    }

    struct Node{ long long val; int r; };
    struct Cmp{ bool operator()(const Node&a, const Node&b) const { return a.val > b.val; } };
    priority_queue<Node, vector<Node>, Cmp> pq;
    vector<long long> ans(k, INF);

    for(int t=1;t<=k-1;t++){
        for(auto &p: starts[t]) pq.push({p.first, p.second});
        while(!pq.empty() && pq.top().r <= t) pq.pop();
        if(!pq.empty()) ans[t] = pq.top().val;
    }

    for(int t=1;t<=k-1;t++){
        if(ans[t] >= INF/2) cout << -1; else cout << ans[t];
        if(t < k-1) cout << '\n';
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
import heapq

def dijkstra(n, adj, src):
    INF = 10**30
    dist = [INF] * (n + 1)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    try:
        n = next(it); m = next(it); a = next(it); b = next(it)
    except StopIteration:
        return
    adj = [[] for _ in range(n + 1)]
    edges = []
    for _ in range(m):
        u = next(it); v = next(it); w = next(it)
        adj[u].append((v, w))
        adj[v].append((u, w))
        edges.append((u, v, w))
    k = next(it)
    path = [0] * (k + 1)
    for i in range(1, k + 1):
        path[i] = next(it)

    INF = 10**30
    distA = dijkstra(n, adj, a)
    distB = dijkstra(n, adj, b)

    pos = [-1] * (n + 1)
    for i in range(1, k + 1):
        pos[path[i]] = i

    idxA = [-1] * (n + 1)
    for i in range(1, k + 1):
        idxA[path[i]] = i
    orderA = list(range(1, n + 1))
    orderA.sort(key=lambda x: (distA[x], x))
    for u in orderA:
        if distA[u] >= INF // 2:
            continue
        for v, w in adj[u]:
            if distA[u] + w == distA[v]:
                if idxA[v] < idxA[u]:
                    idxA[v] = idxA[u]

    BIG = 10**9
    idxB = [BIG] * (n + 1)
    for i in range(1, k + 1):
        if idxB[path[i]] > i:
            idxB[path[i]] = i
    orderB = list(range(1, n + 1))
    orderB.sort(key=lambda x: (distB[x], x))
    for x in orderB:
        if distB[x] >= INF // 2:
            continue
        for y, w in adj[x]:
            if distB[x] == distB[y] + w:
                if idxB[x] > idxB[y]:
                    idxB[x] = idxB[y]

    pathDir = set((path[t], path[t+1]) for t in range(1, k))

    starts = [[] for _ in range(k + 2)]
    def add_interval(from_u, to_v, w):
        if distA[from_u] >= INF // 2 or distB[to_v] >= INF // 2:
            return
        l = idxA[from_u]
        r = idxB[to_v]
        if l >= 1 and r <= k and l < r:
            is_path_edge = (pos[from_u] >= 1 and pos[to_v] >= 1 and pos[from_u] + 1 == pos[to_v] and (from_u, to_v) in pathDir)
            if not is_path_edge:
                val = distA[from_u] + w + distB[to_v]
                starts[l].append((val, r))

    for (u, v, w) in edges:
        add_interval(u, v, w)
        add_interval(v, u, w)

    pq = []  # (val, r)
    ans = [INF] * k
    for t in range(1, k):
        for val, r in starts[t]:
            heapq.heappush(pq, (val, r))
        while pq and pq[0][1] <= t:
            heapq.heappop(pq)
        if pq:
            ans[t] = pq[0][0]

    out = []
    for t in range(1, k):
        out.append(str(-1 if ans[t] >= INF // 2 else ans[t]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 경로가 완전히 끊기는 경우(후보가 전무) → -1 출력
- 대체 경로의 길이가 기존 최단거리와 동일한 경우(동일 최단경로 존재) 처리
- 본래 경로 간선 `(v_t→v_{t+1})` 자체를 후보에서 제외했는지 확인
- `distA/distB`가 무한대(INF)인 정점 전파 배제
- 가중치 합이 32비트를 넘을 수 있으므로 64비트 정수 사용(C++: long long)
- `k=2`처럼 경로가 간선 1개인 최소 케이스
- `n=1`, `m`이 매우 작거나 큰 경우
- 동일 거리 정점의 정렬/전파 타이 관리(안정적으로 `<=`/`>=` 사용)

## 제출 전 점검
- 입력/출력 형식(개행 포함)과 자료형(64-bit) 확인
- 다익스트라 구현: 우선순위큐 팝 후 최신 거리 검사 포함 여부
- 최단경로 DAG 전파 조건 `distA[u]+w==distA[v]`, `distB[x]==distB[y]+w` 정확성
- 구간 `[l, r)` 유효성 및 스윕 시 `r≤t` 후보 제거 로직 확인

## 참고자료
- 문제: https://www.acmicpc.net/problem/5250


