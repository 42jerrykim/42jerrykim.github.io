---
title: "[Algorithm] cpp-python 백준 3640번: 제독 - 최소 비용 최대 유량"
description: "1에서 v까지 두 전함이 서로 다른 경로로 출발해 목적지 v에서 다시 만나야 합니다. 출발·도착을 제외한 정점/간선 겹침을 금지하기 위해 정점 분할로 정점 용량을 1로 제한하고, 1과 v만 2로 둔 뒤 최소 비용 최대 유량으로 두 경로의 포탄 수 합을 최솟값으로 구합니다."
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
- Problem-3640
- cpp
- C++
- python
- Python
- Graph
- 그래프
- Directed Graph
- 유향 그래프
- Min Cost Max Flow
- 최소비용최대유량
- MCMF
- Network Flow
- 네트워크 플로우
- Flow
- 유량
- Residual Graph
- 잔여 그래프
- Augmenting Path
- 증가 경로
- SPFA
- Dijkstra
- 다익스트라
- Johnson Potential
- 잠재값
- Reduced Cost
- 감소 비용
- Node Splitting
- 정점 분할
- Vertex Capacity
- 정점 용량
- Edge Capacity
- 간선 용량
- Edge Disjoint Paths
- 간선 분리 경로
- Vertex Disjoint Paths
- 정점 분리 경로
- Two Disjoint Paths
- 두 경로
- Shortest Path on Residual
- 최단경로
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Pitfalls
- 실수 포인트
- Edge Cases
- 코너 케이스
- Competitive Programming
- 경쟁프로그래밍
- NWERC
- NWERC 2012
- Admiral
- 제독
- Integer Weights
- 정수 가중치
- Nonnegative Costs
- 음이 아닌 비용
- EOF Input
- EOF 입력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3640
- 요약: 정점 1에서 시작해 정점 v에서 다시 만나는 두 함선의 경로를 찾습니다. 출발·도착을 제외하고 같은 정점이나 같은 간선을 공유하면 안 되며, 각 간선의 비용(포탄 수) 합을 최소화해야 합니다. 입력은 EOF까지 여러 테스트 케이스가 주어집니다.

## 입력/출력
```
<입력>
v e
a1 b1 c1
...
ae be ce
(EOF까지 반복)

<출력>
각 테스트 케이스마다 두 경로의 총 비용 최소값을 한 줄에 출력
```

## 접근 개요
- 정점·간선이 겹치지 않도록 하려면 정점 용량이 1인 흐름으로 모델링해야 합니다. 이를 위해 각 정점 i를 `i_in → i_out`으로 분할하고, `i_in→i_out` 용량을 1로 둡니다. 다만 출발점 1과 도착점 v는 두 경로가 동시에 지나갈 수 있도록 용량 2로 둡니다.
- 원래 간선 `a→b (비용 c)`는 분할 뒤 `a_out → b_in (용량 1, 비용 c)`로 둡니다. 이렇게 하면 간선/정점의 중복 사용이 금지됩니다.
- 새로 만든 소스 S에서 `1_in`으로, `v_out`에서 싱크 T로 용량 2의 간선을 연결하고, 최소 비용 최대 유량(MCMF)로 최대 2의 유량을 흘려 총 비용의 최솟값을 구합니다. 비용이 음수가 아니므로 다익스트라 + 잠재값(Johnson)으로 빠르게 해결 가능합니다.

## 알고리즘 설계
- 정점 분할: `in(i)=2*(i-1)`, `out(i)=2*(i-1)+1`로 매핑하여 총 노드는 `2*v`가 됩니다. 추가 소스/싱크 S,T를 더해 `2*v+2`개를 사용합니다.
- 용량 설정: `in(i)→out(i)` 용량은 i∈{1,v}면 2, 그 외엔 1. 원래 간선은 `out(a)→in(b)`로 용량 1, 비용 c.
- 최단 경로: 잠재값을 사용한 다익스트라로 감소 비용이 비음수가 되도록 유지하고, 경로를 2번(또는 가능한 만큼) 찾아 누적 비용을 더합니다.
- 올바름 근거: 각 정점 내부 간선 용량이 경로 수를 제한하므로 중간 정점 공유가 불가능하며, 모든 원래 간선 용량이 1이므로 간선 공유도 불가. 최소 비용 최대 유량은 모든 1→v 경로 쌍 중 비용 합이 최소인 두 경로를 선택합니다.

## 복잡도
- 시간: O(F · E log V) ≈ O(E log V) (여기서 F=2)
- 공간: O(V + E)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge {
	int to;
	int rev;
	int cap;
	long long cost;
};

struct MinCostMaxFlow {
	int n;
	vector<vector<Edge>> graph;
	vector<long long> potential;
	vector<long long> dist;
	vector<int> prevVertex;
	vector<int> prevEdge;

	MinCostMaxFlow(int n_) : n(n_), graph(n_), potential(n_, 0), dist(n_), prevVertex(n_), prevEdge(n_) {}

	void addEdge(int u, int v, int cap, long long cost) {
		Edge a{v, (int)graph[v].size(), cap, cost};
		Edge b{u, (int)graph[u].size(), 0, -cost};
		graph[u].push_back(a);
		graph[v].push_back(b);
	}

	pair<int, long long> minCostMaxFlow(int s, int t, int maxFlow) {
		const long long INF = (long long)4e18;
		int flowSent = 0;
		long long costAcc = 0;

		fill(potential.begin(), potential.end(), 0);

		while (flowSent < maxFlow) {
			fill(dist.begin(), dist.end(), INF);
			dist[s] = 0;
			priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
			pq.push({0, s});

			while (!pq.empty()) {
				auto [d, u] = pq.top(); pq.pop();
				if (d != dist[u]) continue;
				for (int i = 0; i < (int)graph[u].size(); ++i) {
					const Edge &e = graph[u][i];
					if (e.cap <= 0) continue;
					long long nd = d + e.cost + potential[u] - potential[e.to];
					if (nd < dist[e.to]) {
						dist[e.to] = nd;
						prevVertex[e.to] = u;
						prevEdge[e.to] = i;
						pq.push({nd, e.to});
					}
				}
			}

			if (dist[t] == INF) break;

			for (int v = 0; v < n; ++v) if (dist[v] < INF) potential[v] += dist[v];

			int addFlow = maxFlow - flowSent;
			for (int v = t; v != s; v = prevVertex[v]) {
				const Edge &e = graph[prevVertex[v]][prevEdge[v]];
				addFlow = min(addFlow, e.cap);
			}
			for (int v = t; v != s; v = prevVertex[v]) {
				Edge &e = graph[prevVertex[v]][prevEdge[v]];
				Edge &r = graph[v][e.rev];
				e.cap -= addFlow;
				r.cap += addFlow;
				costAcc += (long long)addFlow * e.cost;
			}
			flowSent += addFlow;
		}
		return {flowSent, costAcc};
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int v, e;
	while (cin >> v >> e) {
		auto inId = [&](int x) { return 2 * (x - 1); };
		auto outId = [&](int x) { return 2 * (x - 1) + 1; };

		int S = 2 * v;
		int T = 2 * v + 1;
		MinCostMaxFlow mcmf(2 * v + 2);

		for (int i = 1; i <= v; ++i) {
			int cap = (i == 1 || i == v) ? 2 : 1;
			mcmf.addEdge(inId(i), outId(i), cap, 0);
		}

		for (int i = 0; i < e; ++i) {
			int a, b, c;
			cin >> a >> b >> c;
			mcmf.addEdge(outId(a), inId(b), 1, c);
		}

		mcmf.addEdge(S, inId(1), 2, 0);
		mcmf.addEdge(outId(v), T, 2, 0);

		auto [flow, cost] = mcmf.minCostMaxFlow(S, T, 2);
		cout << cost << '\n';
	}
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
import heapq

def add_edge(graph, u, v, cap, cost):
    graph[u].append([v, cap, cost, len(graph[v])])
    graph[v].append([u, 0, -cost, len(graph[u]) - 1])

def min_cost_max_flow(graph, s, t, max_flow):
    n = len(graph)
    INF = 10**18
    potential = [0] * n
    flow_sent = 0
    cost_acc = 0

    while flow_sent < max_flow:
        dist = [INF] * n
        dist[s] = 0
        prev_v = [-1] * n
        prev_e = [-1] * n
        pq = [(0, s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for i, (to, cap, cost, rev) in enumerate(graph[u]):
                if cap <= 0:
                    continue
                nd = d + cost + potential[u] - potential[to]
                if nd < dist[to]:
                    dist[to] = nd
                    prev_v[to] = u
                    prev_e[to] = i
                    heapq.heappush(pq, (nd, to))

        if dist[t] == INF:
            break

        for i in range(n):
            if dist[i] < INF:
                potential[i] += dist[i]

        addf = max_flow - flow_sent
        v = t
        while v != s:
            u = prev_v[v]
            ei = prev_e[v]
            addf = min(addf, graph[u][ei][1])
            v = u
        v = t
        while v != s:
            u = prev_v[v]
            ei = prev_e[v]
            to, cap, cost, rev = graph[u][ei]
            graph[u][ei][1] -= addf
            graph[v][rev][1] += addf
            cost_acc += addf * cost
            v = u
        flow_sent += addf
    return flow_sent, cost_acc

def solve():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    out_lines = []
    for v_str in it:
        v = int(v_str)
        e = int(next(it))
        # node splitting
        def in_id(x):
            return 2 * (x - 1)
        def out_id(x):
            return 2 * (x - 1) + 1
        S = 2 * v
        T = 2 * v + 1
        n = 2 * v + 2
        graph = [[] for _ in range(n)]

        for i in range(1, v + 1):
            cap = 2 if (i == 1 or i == v) else 1
            add_edge(graph, in_id(i), out_id(i), cap, 0)

        for _ in range(e):
            a = int(next(it)); b = int(next(it)); c = int(next(it))
            add_edge(graph, out_id(a), in_id(b), 1, c)

        add_edge(graph, S, in_id(1), 2, 0)
        add_edge(graph, out_id(v), T, 2, 0)

        _, cost = min_cost_max_flow(graph, S, T, 2)
        out_lines.append(str(cost))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 단일 경로 비용이 매우 큰 간선만 존재하는 경우(대체 경로 선택 여부)
- 1과 v에서만 중복 통과가 가능해야 함: 내부 정점 용량이 1로 설정되어 있는지 확인
- 다중 테스트 케이스: 입력 EOF 처리(빈 줄 포함) 안정성
- 간선 비용이 모두 양수이므로 잠재값 초기화를 0으로 두어도 안전함

## 제출 전 점검
- 정점 분할 인덱스 계산 `in/out`의 off-by-one 여부
- 소스/싱크 연결 용량 2 설정 누락 여부
- 비용 누적 시 64-bit 사용(C++ `long long`, Python 정수 자동 확장)
- 입출력: EOF까지 반복 처리 확실히 구현

## 참고자료
- 최소 비용 최대 유량(Johnson 잠재값, Dijkstra) 기본 구현 노트
- 정점 분할(node splitting)로 정점 용량을 표현하는 표준 기법


