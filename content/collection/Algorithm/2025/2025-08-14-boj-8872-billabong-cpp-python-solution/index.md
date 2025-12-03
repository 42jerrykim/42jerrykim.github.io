---
title: "[Algorithm] C++/Python 백준 8872번: 빌라봉"
description: "가중 무방향 그래프의 각 연결요소에서 지름과 반지름을 구한 뒤, 길이 L의 간선을 N−M−1개 추가해 전체 지름을 최소화한다. 해답은 기존 지름과 r1+L+r2, r2+2L+r3 후보의 최댓값으로 결정된다. 구현, 정당성, 복잡도, 코너 케이스까지 정리."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph"
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-8872
- cpp
- python
- Graph
- 그래프
- Tree
- 트리
- Diameter
- 지름
- Radius
- 반지름
- Graph Center
- 그래프 중심
- Component
- 연결요소
- Bridge
- 브리지
- Shortest Path
- 최단경로
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
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
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- BFS
- DFS
- Union-Find
- 유니온파인드
- Tree Diameter
- 트리 지름
- Tree Radius
- 트리 반지름
- IOI
- IOI-2013
- Dreaming
- 빌라봉
- Fixed-Length Edge
- 고정 길이 간선
- Graph Construction
- 그래프 구성
- Connectivity
- 연결성
- Centers
- 센터
- Two-Pass BFS
- 두 번의 BFS
- Depth-First Search
- 깊이우선탐색
- Stack-Based DFS
- 스택 DFS
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8872
- 요약: 가중 무방향 그래프에서 `N−M−1`개의 길이 `L`인 간선을 추가하여 모든 정점을 연결할 때, 두 정점 간 최단거리의 최댓값(그래프 지름)을 최소화하는 값을 구한다.

## 입력/출력
```
입력: N M L, 이어서 M개의 줄에 A B T (무방향 간선, 가중치 T)
출력: 간선 추가 후 최소 가능한 최대 통행 시간(최소 지름)
```

예제(문서화):
```
입력
12 8 2
0 8 4
8 2 2
2 7 4
5 11 3
5 1 7
1 3 1
1 9 5
10 6 3

출력
18
```

## 접근 개요
- 각 연결요소를 독립적인 트리(사이클 없음, 문제 조건상 임의 쌍 최단 경로가 0개 또는 1개)로 본다.
- 연결요소마다 두 번의 DFS/BFS로 지름(가장 먼 두 정점 사이 최단거리)과 반지름(최소 이심도: `min_x max(dist(x,u), dist(x,v))`)을 구한다.
- 길이 `L`의 간선으로 연결요소들을 사슬처럼 잇는 최적 설계에서 최종 지름 후보는 아래 3가지의 최댓값으로 귀결된다.
  - 기존 컴포넌트 지름들의 최댓값
  - `r1 + L + r2` (가장 큰 반지름 두 개를 연결)
  - `r2 + 2L + r3` (세 개 이상일 때 가운데 요소를 통해 양끝으로 가장 벌어지는 경우)
- 정답은 위 후보들의 최댓값이다.

## 알고리즘
1) 모든 정점에 대해 미방문이면 그 정점이 속한 연결요소를 탐색한다.
2) 한 연결요소에서 임의 정점 `s`에서 가장 먼 정점 `u`를 찾고, `u`에서 가장 먼 정점 `v`를 찾아 지름 `diam`을 구한다(두 번의 DFS/BFS).
3) `u`에서의 거리 배열 `du`, `v`에서의 거리 배열 `dv`를 이용해 각 정점의 이심도 `max(du[x], dv[x])`의 최소값을 반지름으로 기록한다.
4) 모든 연결요소의 `diam` 최댓값과 반지름 배열을 모아 내림차순 정렬한다.
5) 정답은 `max( max_diam, r[0]+L+r[1], r[1]+2L+r[2] )` (각 항은 존재할 때만 평가)이다.

### 정당성(스케치)
- 트리에서 임의 두 점 간 최단거리는 지름 경로를 기준으로 평가할 수 있으며, 중심(반지름을 달성하는 정점)에 새 간선을 연결하는 것이 최적이다.
- 여러 트리를 길이 `L` 간선으로 잇는 최적 구조는 반지름이 큰 컴포넌트부터 직렬로 잇는 형태로 환원된다. 이때 최장 경로는 (1) 기존 내부 지름, (2) 가장 큰 두 반지름을 잇는 경로, (3) 세 개 이상일 때 양끝 컴포넌트를 거치는 경로 중 하나로 나타난다.

## 복잡도
- 시간: O(N + M)
- 공간: O(N + M)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge { int to; int w; };

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M; long long L;
    if(!(cin >> N >> M >> L)) return 0;
    vector<vector<Edge>> g(N);
    for(int i=0;i<M;++i){
        int a,b,t; cin >> a >> b >> t;
        g[a].push_back({b,t}); g[b].push_back({a,t});
    }

    vector<char> compVisited(N,0);
    vector<long long> dist(N,0), du(N,0), dv(N,0);
    vector<int> seen(N,0); int tok=0;

    auto dfs_collect_and_farthest = [&](int s, vector<int>& comp){
        ++tok; int curTok=tok;
        stack<int> st; st.push(s); seen[s]=curTok; dist[s]=0;
        long long bestD=0; int best=s;
        while(!st.empty()){
            int u=st.top(); st.pop();
            if(!compVisited[u]){ compVisited[u]=1; comp.push_back(u); }
            if(dist[u]>bestD){ bestD=dist[u]; best=u; }
            for(auto &e:g[u]) if(seen[e.to]!=curTok){
                seen[e.to]=curTok; dist[e.to]=dist[u]+e.w; st.push(e.to);
            }
        }
        return pair<int,long long>(best,bestD);
    };

    auto dfs_farthest_and_fill = [&](int s, vector<long long>& out){
        ++tok; int curTok=tok;
        stack<int> st; st.push(s); seen[s]=curTok; dist[s]=0; out[s]=0;
        long long bestD=0; int best=s;
        while(!st.empty()){
            int u=st.top(); st.pop();
            if(dist[u]>bestD){ bestD=dist[u]; best=u; }
            for(auto &e:g[u]) if(seen[e.to]!=curTok){
                seen[e.to]=curTok; dist[e.to]=dist[u]+e.w; out[e.to]=dist[e.to]; st.push(e.to);
            }
        }
        return pair<int,long long>(best,bestD);
    };

    long long maxDiam=0; vector<long long> radii;
    for(int i=0;i<N;++i){
        if(compVisited[i]) continue;
        vector<int> comp;
        auto [u,_d0]=dfs_collect_and_farthest(i,comp);
        auto [v,diam]=dfs_farthest_and_fill(u,du);
        dfs_farthest_and_fill(v,dv);
        long long rad=LLONG_MAX;
        for(int x:comp) rad=min(rad, max(du[x], dv[x]));
        maxDiam=max(maxDiam, diam);
        radii.push_back(rad);
    }
    sort(radii.begin(), radii.end(), greater<long long>());

    long long ans=maxDiam;
    if(radii.size()>=2) ans=max(ans, radii[0]+L+radii[1]);
    if(radii.size()>=3) ans=max(ans, radii[1]+2LL*L+radii[2]);
    cout << ans << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

input = sys.stdin.readline

def farthest_and_fill(start, adj, out):
    n = len(adj)
    dist = [-1]*n
    q = deque([start])
    dist[start] = 0
    out[start] = 0
    best = start
    while q:
        u = q.popleft()
        if dist[u] > dist[best]:
            best = u
        for v,w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                out[v] = dist[v]
                q.append(v)
    return best, dist[best], dist

def collect_component(s, adj, seen):
    comp = []
    stack = [s]
    seen[s] = True
    while stack:
        u = stack.pop()
        comp.append(u)
        for v,_ in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    return comp

def solve():
    N, M, L = map(int, input().split())
    adj = [[] for _ in range(N)]
    for _ in range(M):
        a,b,t = map(int, input().split())
        adj[a].append((b,t))
        adj[b].append((a,t))

    seen = [False]*N
    max_diam = 0
    radii = []

    du = [0]*N
    dv = [0]*N

    for i in range(N):
        if seen[i]:
            continue
        comp = collect_component(i, adj, seen)
        # pick any node in comp
        s = comp[0]
        u, _, _ = farthest_and_fill(s, adj, du)
        v, diam, _ = farthest_and_fill(u, adj, du)
        _, _, _ = farthest_and_fill(v, adj, dv)
        rad = 10**30
        for x in comp:
            rad = min(rad, max(du[x], dv[x]))
        max_diam = max(max_diam, diam)
        radii.append(rad)

    radii.sort(reverse=True)
    ans = max_diam
    if len(radii) >= 2:
        ans = max(ans, radii[0] + L + radii[1])
    if len(radii) >= 3:
        ans = max(ans, radii[1] + 2*L + radii[2])
    print(ans)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- `M = 0` 혹은 단일 정점 컴포넌트 다수: 반지름이 모두 0이므로 `max(0, L, 2L)` 평가
- 두 개 컴포넌트만 존재: `max(max_diam, r1+L+r2)`만 평가됨
- 세 개 이상 컴포넌트: `r2+2L+r3` 항이 추가 후보
- 간선 가중치가 큰 경우(최대 1e4): 누적 거리형 정수 오버플로 주의(C++: 64-bit)
- 고립 정점: 반지름 0, 지름 0으로 정상 처리

## 제출 전 점검
- 입력/출력 포맷 및 개행 확인
- 거리 누적은 64-bit 정수 사용(C++)
- 방문 배열(토큰/마킹) 초기화 누락 여부
- 정렬 후 인덱싱 경계 확인(`radii` 크기별 분기)

## 참고자료
- IOI 2013 Day 1: Dreaming (문제 원형)

