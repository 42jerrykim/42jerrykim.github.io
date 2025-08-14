---
title: "[Algorithm] cpp 백준 3295번: 단방향 링크 네트워크 - 최대 매칭"
description: "단방향 링크 네트워크를 링과 선형 배열로 분해할 때의 최대 가치는 선택된 간선 수와 동일합니다. 각 정점의 진입·진출 차수를 최대 1로 제한하는 간선 선택 문제를 좌·우 파티션으로 분리한 이분 매칭으로 모델링하고, Hopcroft–Karp 알고리즘으로 O(√V·E)에 해결합니다. 구현 포인트와 코너 케이스까지 정리했습니다."
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
- "Problem-3295"
- "cpp"
- "C++"
- "Python"
- "Graph"
- "그래프"
- "Matching"
- "매칭"
- "Maximum Matching"
- "최대 매칭"
- "Bipartite Matching"
- "이분 매칭"
- "Hopcroft–Karp"
- "Hopcroft-Karp"
- "Flow"
- "유량"
- "Directed Graph"
- "유향 그래프"
- "Ring"
- "링"
- "Linear Array"
- "선형 배열"
- "Path Decomposition"
- "분해"
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
- "BFS"
- "DFS"
- "ICPC"
- "Daejeon 2013"
- "Nationwide Internet Competition"
- "Directed Link Network"
- "Unidirectional Link Network"
- "BOJ3295"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3295
- 요약: 방향 그래프의 정점들을 서로 겹치지 않게 링(사이클) 또는 선형 배열(경로)로 분해하여 총 가치를 최대로 하라. k개 정점의 링 가치는 k, 선형 배열 가치는 k-1.

### 제한/스펙
- 시간: 1초, 메모리: 128MB
- 정점 n ≤ 1000, 간선 m ≤ 50000
- 정점은 0..n-1, 간선은 단방향 (u → v)

## 입출력 형식/예제
입력:
```
T
n m
u1 v1
...
um vm
```

출력:
```
각 테스트케이스마다 최대 가치(정수) 한 줄
```

예시:
```
입력
3
4 3
3 2
1 0
2 3
6 6
0 1
1 2
2 3
3 1
3 4
4 5
14 19
0 1
1 2
2 3
3 4
4 5
5 0
5 4
2 1
2 6
6 7
7 8
8 9
9 1
8 7
7 10
10 11
11 12
12 13
13 8

출력
3
5
13
```

## 접근 개요(아이디어 스케치)
- 관찰 1: 링은 k개의 간선을 사용하고, 선형 배열은 k-1개의 간선을 사용한다. 즉, 전체 가치는 선택된 간선 수와 정확히 일치한다.
- 관찰 2: 서로 겹치지 않는 링/경로 분해는 각 정점의 선택 간선에 대해 진출차수 ≤ 1, 진입차수 ≤ 1 제약을 의미한다.
- 모델링: 정점 집합을 좌·우 두 파트로 복제해 좌 u에서 우 v로 간선을 두면, 각 정점 당 좌/우에서 최대 1개의 매칭만 허용하는 최대 이분 매칭과 동치가 된다. 매칭의 크기 = 선택 가능한 간선 수 = 최대 가치.
- 알고리즘: 좌측을 0..n-1, 우측을 0..n-1로 두고 입력 간선(u→v)을 (u in L)→(v in R)로 추가 후 Hopcroft–Karp로 최대 매칭 계산.

## 알고리즘 설계
- 그래프 구성: 인접 리스트 adj[L_u]에 우측 정점 v를 추가.
- 최대 매칭: Hopcroft–Karp (BFS로 레이어 구성, DFS로 레벨 그래프에서 증대 경로 탐색).
- 올바름 근거:
  - 정당성(⇒): 매칭은 각 좌/우 정점을 한 번만 사용하므로 각 원 정점에서 진출·진입 간선이 최대 1개로 제한된다. 연결 성분은 경로/사이클의 합성으로 분해된다.
  - 정당성(⇐): 임의의 유효한 링/경로 분해에서 사용된 각 간선을 (u in L)–(v in R)의 매칭 한 간선으로 대응시킬 수 있다. 따라서 최적 분해의 가치 ≤ 최대 매칭 크기.
  - 양방향로 상계·하계를 맞추어 일치함을 보인다.

## 복잡도
- 시간: O(√V · E) ≈ O(√n · m)
- 공간: O(n + m)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; if(!(cin >> T)) return 0;
    while(T--){
        int n, m; cin >> n >> m;
        vector<vector<int>> adj(n);
        for(int i=0;i<m;++i){
            int u, v; cin >> u >> v;
            if(0<=u && u<n && 0<=v && v<n) adj[u].push_back(v);
        }

        vector<int> matchU(n, -1), matchV(n, -1), dist(n);

        auto bfs = [&](){
            queue<int> q;
            for(int u=0; u<n; ++u){
                if(matchU[u]==-1){ dist[u]=0; q.push(u);} else dist[u]=-1;
            }
            bool found = false;
            while(!q.empty()){
                int u=q.front(); q.pop();
                for(int v: adj[u]){
                    int u2 = matchV[v];
                    if(u2!=-1){
                        if(dist[u2]==-1){ dist[u2]=dist[u]+1; q.push(u2);}    
                    }else{
                        found = true;
                    }
                }
            }
            return found;
        };

        function<bool(int)> dfs = [&](int u){
            for(int v: adj[u]){
                int u2 = matchV[v];
                if(u2==-1 || (dist[u2]==dist[u]+1 && dfs(u2))){
                    matchU[u]=v; matchV[v]=u; return true;
                }
            }
            dist[u] = -1; return false;
        };

        int matching = 0;
        while(bfs()){
            for(int u=0; u<n; ++u) if(matchU[u]==-1) if(dfs(u)) ++matching;
        }
        cout << matching << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 간선이 전혀 없거나(정답 0), 모든 정점이 고립된 경우
- 다중 간선 입력: 매칭은 동일 쌍을 한 번만 사용하므로 안전
- 자기루프(u = v): 매칭으로는 1개 간선만 사용 가능(진입·진출 동시 충돌 없음) — 입력에 있어도 자연스럽게 처리됨
- 큰 입력(m=5e4): 입출력 최적화, 불필요한 복사 제거

## 제출 전 점검
- 입력 범위 체크(0 ≤ u,v < n)
- 매칭 초기화 및 레벨 그래프(dist) 초기화 누락 여부
- 출력 개행 및 다중 테스트케이스 누락 여부

## 참고자료/유사문제
- Hopcroft–Karp 알고리즘 설명: https://cp-algorithms.com/graph/hopcroft_karp.html
- 위키피디아: https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm


