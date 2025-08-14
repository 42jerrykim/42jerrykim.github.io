---
title: "[Algorithm] cpp 백준 11408번: 열혈강호 5 - MCMF 최소비용 최대매칭"
description: "이 문제는 직원-일 이분 그래프에서 임금 비용을 최소화하며 가능한 한 많은 일을 배정하는 과제입니다. 최소 비용 최대 유량(MCMF)로 모델링하여 Dijkstra+잠재치(Johnson)로 음수 없는 보정 비용을 사용, 유량 1씩 확장하며 비용 합을 최소화합니다. 제약(N,M≤400, 임금≤10^4)에 맞춰 O(F·E·logV)로 안정적으로 통과합니다."
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
- Problem-11408
- cpp
- C++
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
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- Graph
- 그래프
- Flow
- 플로우
- Min-Cost Max-Flow
- 최소비용최대유량
- MCMF
- Assignment Problem
- 할당 문제
- Matching
- 매칭
- Bipartite Matching
- 이분매칭
- Hungarian
- 헝가리안
- Dijkstra
- 다익스트라
- Johnson Potential
- 잠재치
- Shortest Path
- 최단경로
- Residual Graph
- 잔여그래프
- Negative Cycle
- 음수사이클
- SPFA
- 라벨보정
- 비용흐름
- Network Flow
- 네트워크플로우
- String
- 문자열
- Math
- 수학
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11408
- 요약: N명의 직원과 M개의 일을 이분 그래프로 보고, 가능한 많은 일을 배정하면서 총 임금 합을 최소화합니다. 각 직원은 최대 1개 일, 각 일은 정확히 1명의 직원에게만 배정됩니다.

### 제한/스펙
- 시간 제한: 2초, 메모리: 256MB
- 범위: 1 ≤ N, M ≤ 400, 임금은 0 이상 10,000 이하
- 입력 크기: 각 직원 i에 대해 가능한 일의 수 K와 (일 번호, 임금) 쌍 K개

## 입력/출력 형식 및 예제
```
입력
N M
K1 j1 c1 j2 c2 ...
K2 ...
...
KN ...

출력
가능한 일의 최대 개수
최소 임금 합
```

예제
```
입력
5 5
2 1 3 2 2
1 1 5
2 2 1 3 7
3 3 9 4 9 5 9
1 1 0

출력
4
18
```

## 접근 개요
- 문제를 `Source -> 직원(i) -> 일(j) -> Sink` 네트워크로 모델링하고, 간선 비용을 임금으로 설정합니다.
- 목표는 (1) 유량 최대화(=배정 수 최대화)와 (2) 그때의 비용 최소화입니다. 이는 전형적인 최소 비용 최대 유량(MCMF) 문제입니다.
- 음수 비용이 없으므로 Dijkstra + 잠재치(Johnson reweighting)를 사용해 각 증가 경로를 최단 비용으로 찾습니다.

```mermaid
graph TD
  S["S (Source)"] -->|cap=1,cost=0| E1[직원 1]
  S -->|1,0| E2[직원 2]
  S -->|1,0| E3[직원 3]
  E1 -->|1,cost=w(1,1)| J1[일 1]
  E1 -->|1,w(1,2)| J2[일 2]
  E2 -->|1,w(2,1)| J1
  E3 -->|1,w(3,2)| J2
  J1 -->|1,0| T["T (Sink)"]
  J2 -->|1,0| T
```

## 알고리즘 설계
- 정점 구성: `S=0`, 직원 `1..N`, 일 `N+1..N+M`, `T=N+M+1`.
- 간선
  - `S -> i` 용량 1, 비용 0
  - `i -> (N+j)` 용량 1, 비용 = 해당 임금
  - `(N+j) -> T` 용량 1, 비용 0
- 반복: Dijkstra(잠재치 적용)로 `S->T` 최단 비용 증가 경로를 찾고, 가능한 만큼(여기서는 1) 흘려 비용을 누적합니다. 더 이상 경로가 없으면 종료.
- 정당성: 각 증가 단계가 현재 남아 있는 잔여 그래프에서 비용 최소의 단위 유량을 보장하므로, 유량을 최대화한 시점의 총 비용은 전역 최소가 됩니다.

### 의사코드
```
while (S->T 최단 비용 경로 존재):
  path = shortest_path_with_potential()
  send 1 unit along path
  update residual graph and potentials
```

## 복잡도
- 한 번의 증가에서 Dijkstra: O(E log V)
- 증가 횟수 F ≤ min(N, M)
- 전체: O(F · E · log V). 최악의 경우 E ≈ N·M + N + M ≤ 160000 + 800 정도로 2초 내 충분합니다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge {
	int to;
	int cap;
	int cost;
	int rev;
	Edge(int t, int c, int w, int r) : to(t), cap(c), cost(w), rev(r) {}
};

struct MinCostMaxFlow {
	int n;
	vector<vector<Edge>> graph;
	MinCostMaxFlow(int n_) : n(n_), graph(n_) {}

	void addEdge(int u, int v, int cap, int cost) {
		graph[u].emplace_back(v, cap, cost, (int)graph[v].size());
		graph[v].emplace_back(u, 0, -cost, (int)graph[u].size() - 1);
	}

	pair<int, long long> minCostMaxFlow(int s, int t) {
		const long long INF = (1LL << 60);
		vector<long long> potential(n, 0), dist(n);
		vector<int> prevNode(n), prevEdge(n);

		int flow = 0;
		long long cost = 0;

		while (true) {
			fill(dist.begin(), dist.end(), INF);
			dist[s] = 0;
			priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
			pq.push({0, s});

			while (!pq.empty()) {
				auto [d, u] = pq.top(); pq.pop();
				if (d != dist[u]) continue;
				for (int i = 0; i < (int)graph[u].size(); ++i) {
					Edge const &e = graph[u][i];
					if (e.cap <= 0) continue;
					long long nd = d + (long long)e.cost + potential[u] - potential[e.to];
					if (nd < dist[e.to]) {
						dist[e.to] = nd;
						prevNode[e.to] = u;
						prevEdge[e.to] = i;
						pq.push({nd, e.to});
					}
				}
			}
			if (dist[t] == INF) break;

			for (int v = 0; v < n; ++v) {
				if (dist[v] < INF) potential[v] += dist[v];
			}

			int addFlow = INT_MAX;
			for (int v = t; v != s; v = prevNode[v]) {
				Edge const &e = graph[prevNode[v]][prevEdge[v]];
				addFlow = min(addFlow, e.cap);
			}
			long long addCost = 0;
			for (int v = t; v != s; v = prevNode[v]) {
				Edge &e = graph[prevNode[v]][prevEdge[v]];
				addCost += (long long)e.cost * addFlow;
				e.cap -= addFlow;
				graph[v][e.rev].cap += addFlow;
			}
			flow += addFlow;
			cost += addCost;
		}
		return {flow, cost};
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, M;
	if (!(cin >> N >> M)) return 0;

	int S = 0;
	int T = N + M + 1;
	MinCostMaxFlow mcmf(T + 1);

	// Source -> Employees
	for (int i = 1; i <= N; ++i) {
		mcmf.addEdge(S, i, 1, 0);
	}

	// Jobs -> Sink
	for (int j = 1; j <= M; ++j) {
		int jobNode = N + j;
		mcmf.addEdge(jobNode, T, 1, 0);
	}

	// Employee lines
	for (int i = 1; i <= N; ++i) {
		int K; cin >> K;
		for (int k = 0; k < K; ++k) {
			int job, wage; cin >> job >> wage;
			int jobNode = N + job;
			mcmf.addEdge(i, jobNode, 1, wage);
		}
	}

	auto [maxJobs, minWage] = mcmf.minCostMaxFlow(S, T);
	cout << maxJobs << ' ' << minWage << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- 한 직원도 할 수 있는 일이 없는 경우 (K=0)
- 임금 0인 간선 존재
- 여러 직원이 동일한 일만 가능 (경쟁 발생)
- 모든 직원이 모든 일을 할 수 있는 경우(완전 이분 그래프)
- N ≠ M, 한쪽이 더 클 때 최대 유량이 min(N, M)로 제한
- 큰 임금 값(=10000)만 존재하여 비용 누적이 큰 경우의 오버플로 방지(long long)

## 제출 전 점검
- 입출력 포맷 및 개행 확인
- `long long`으로 비용 누적 처리
- 정점 인덱싱: `i`, `N+j` 구분 정확성
- 잠재치 갱신 및 잔여 용량(역간선) 갱신 누락 여부
- 경로 복원 시 `prevNode/prevEdge` 초기화 및 사용 범위 확인

## 참고자료 / 유사문제
- 최소 비용 최대 유량(MCMF) 개요: 잠재치(Johnson) 기반 재가중치와 Dijkstra 결합
- BOJ 11408 "열혈강호 5" 문제 페이지


