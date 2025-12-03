---
title: "[Algorithm] C++ 백준 11407번: 책 구매하기 3"
description: "사람–서점 이분 그래프에 수요·공급·구매제한을 용량/비용으로 모델링하고, 잠재함수 기반 최단경로 반복(MCMF)로 최대 유량과 최소 비용을 동시에 달성합니다. 모델링, 정당성, 구현 포인트와 복잡도를 일목요연하게 정리했습니다."
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
- Problem-11407
- cpp
- C++
- Data Structures
- 자료구조
- Implementation
- 구현
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
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Graph
- 그래프
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Bellman-Ford
- 벨만포드
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Implementation Details
- 구현 디테일
- Flow
- Network Flow
- 네트워크플로우
- Minimum Cost Flow
- Min Cost Max Flow
- 최소비용최대유량
- MCMF
- Successive Shortest Path
- Potentials
- 잠재함수
- Johnson's Reweighting
- 존슨 재가중치
- Residual Graph
- 잔여그래프
- Augmenting Path
- 증가경로
- Transportation Problem
- 수송문제
- Supply Demand
- 공급수요
- Bipartite Graph
- 이분그래프
- Capacity
- 용량
- Cost
- 비용
- Source
- 소스
- Sink
- 싱크
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11407
- 요약: N명의 사람과 M개의 온라인 서점이 있고, 사람 j의 수요 A[j], 서점 i의 재고 B[i], 사람 j가 서점 i에서 살 수 있는 최대치 C[i][j], 1권 배송비 D[i][j]가 주어진다. 총 수요와 총 재고는 동일하다. 구매 가능한 책의 최대 권수와 그때 배송비 합의 최솟값을 구한다.
- 제한: N, M ≤ 100, A[i], B[i], C[i][j] ≤ 100, D[i][j] ≤ 1000, 시간 1초, 메모리 256MB.

## 입력/출력
```
<입력>
N M
A[1..N]
B[1..M]
C[1][1..N]
...
C[M][1..N]
D[1][1..N]
...
D[M][1..N]

<출력>
최대로 살 수 있는 책의 권수
해당 최대 구매 시 최소 배송비 합
```

예시:
```
입력
4 4
3 2 4 2
5 3 2 1
0 1 1 0
1 0 1 2
2 1 1 1
0 0 2 0
5 6 2 1
3 7 4 1
2 10 3 1
10 20 30 1

출력
8
47
```

## 접근 개요
- 사람–서점 이분 그래프를 `소스 → 서점 → 사람 → 싱크`의 네트워크로 모델링한다.
- 간선 정의: `소스→서점(i)` 용량 B[i], 비용 0 / `서점(i)→사람(j)` 용량 C[i][j], 비용 D[i][j] / `사람(j)→싱크` 용량 A[j], 비용 0.
- 이 네트워크에서 최대 유량이 곧 총 구매 권수이고, 그중 최소 비용 유량을 구하면 된다. 잠재함수(potential)를 이용한 Successive Shortest Path(MCMF)로 음수 간선 없이 매번 가중치를 재가중해 다익스트라로 최단 증가경로를 찾는다.

### Mermaid로 흐름 요약
```mermaid
flowchart LR
  S((S)) -->|B[i], 0| Store1[Store 1]
  S -->|B[i], 0| StoreM[Store M]
  Store1 -->|C[i][j], D[i][j]| P1[Person 1]
  StoreM -->|C[i][j], D[i][j]| PN[Person N]
  P1 -->|A[j], 0| T((T))
  PN -->|A[j], 0| T
```

## 알고리즘
- 모델링: 수송(Transportation) 문제의 표준 네트워크 플로우 변환.
- 알고리즘: 잠재함수로 재가중한 다익스트라 기반 MCMF.
  - 초기 잠재함수는 0으로 시작.
  - 매 증분 단계에서 비용이 최소인 증가경로를 찾고, 경로 용량만큼 한 번에 밀어준다.
  - 잠재함수 갱신으로 다음 단계에서도 비음수 간선 가중치를 유지한다.

### 정당성 스케치
- 모든 유량은 용량 제약(B, C, A)을 만족하며, 유량보존으로 각 매칭은 유효한 구매 배분이다.
- 매 단계 최단 증가경로를 선택하고, 잠재함수로 비음수화를 유지하면, 누적 비용이 최소가 되는 증가 경로 선택이 보장된다.
- 총 수요=총 공급이므로 최대 유량은 그 합과 같다. 그 중 최소 비용 해를 구하므로 출력이 문제의 정의에 부합한다.

## 복잡도
- 정점 수 V ≈ N + M + 2 ≤ 202, 간선 수 E ≈ M·N + M + N ≤ 10,200.
- 각 증분에서 다익스트라 O(E log V). 증분 횟수는 실제로는 적당히 묶여 흐르지만, 상한은 O(최대유량).
- 실전에서는 1초 제한 내에 충분히 통과한다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge { int to, rev, cap, cost; };

struct MinCostMaxFlow {
    int n; vector<vector<Edge>> g; vector<long long> pot, dist; vector<int> pv, pe;
    MinCostMaxFlow(int n_) : n(n_), g(n_), pot(n_, 0), dist(n_), pv(n_), pe(n_) {}
    void addEdge(int u, int v, int cap, int cost){
        Edge a{v, (int)g[v].size(), cap, cost};
        Edge b{u, (int)g[u].size(), 0, -cost};
        g[u].push_back(a); g[v].push_back(b);
    }
    pair<int,long long> run(int s, int t){
        const long long INF = (1LL<<60); int flow=0; long long cost=0;
        while(true){
            fill(dist.begin(), dist.end(), INF); fill(pv.begin(), pv.end(), -1); fill(pe.begin(), pe.end(), -1);
            priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
            dist[s]=0; pq.push({0,s});
            while(!pq.empty()){
                auto [d,u]=pq.top(); pq.pop(); if(d!=dist[u]) continue;
                for(int i=0;i<(int)g[u].size();++i){
                    const Edge &e=g[u][i]; if(e.cap<=0) continue;
                    long long nd=d+e.cost+pot[u]-pot[e.to];
                    if(nd<dist[e.to]){ dist[e.to]=nd; pv[e.to]=u; pe[e.to]=i; pq.push({nd,e.to}); }
                }
            }
            if(dist[t]==INF) break;
            for(int v=0; v<n; ++v) if(dist[v]<INF) pot[v]+=dist[v];
            int add=INT_MAX; for(int v=t; v!=s; v=pv[v]) add=min(add, g[pv[v]][pe[v]].cap);
            flow+=add; cost+=1LL*add*pot[t];
            for(int v=t; v!=s; v=pv[v]){ Edge &e=g[pv[v]][pe[v]]; Edge &re=g[v][e.rev]; e.cap-=add; re.cap+=add; }
        }
        return {flow,cost};
    }
};

int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N,M; if(!(cin>>N>>M)) return 0;
    vector<int>A(N),B(M); for(int i=0;i<N;++i) cin>>A[i]; for(int i=0;i<M;++i) cin>>B[i];
    vector<vector<int>> C(M, vector<int>(N)), D(M, vector<int>(N));
    for(int i=0;i<M;++i) for(int j=0;j<N;++j) cin>>C[i][j];
    for(int i=0;i<M;++i) for(int j=0;j<N;++j) cin>>D[i][j];
    int S=0, store=1, person=store+M, T=person+N; MinCostMaxFlow mcmf(T+1);
    for(int i=0;i<M;++i) if(B[i]>0) mcmf.addEdge(S, store+i, B[i], 0);
    for(int i=0;i<M;++i) for(int j=0;j<N;++j) if(C[i][j]>0) mcmf.addEdge(store+i, person+j, C[i][j], D[i][j]);
    for(int j=0;j<N;++j) if(A[j]>0) mcmf.addEdge(person+j, T, A[j], 0);
    auto [flow, cost]=mcmf.run(S,T); cout<<flow<<"\n"<<cost<<"\n"; return 0;
}
```

## 코너 케이스 체크리스트
- C[i][j]=0인 간선은 생략해야 함(용량 0은 추가하지 않음).
- 특정 사람 또는 서점의 수요/공급이 0인 경우 처리.
- 모든 수요=공급이므로 이론상 최대 유량은 총 수요와 동일. 그래도 구현은 일반 MCMF로 둠.
- 비용 합이 클 수 있으므로 64-bit 합계 사용.

## 제출 전 점검
- 입력 파싱 순서와 개행 처리 확인.
- 정점 인덱싱(소스/서점/사람/싱크) 오프셋 실수 방지.
- 다익스트라 우선순위 큐 갱신 시 잠재함수 반영 여부 확인.

## 참고자료
- 문제: https://www.acmicpc.net/problem/11407
- 최소 비용 최대 유량(SSP + Potential) 표준 구현


