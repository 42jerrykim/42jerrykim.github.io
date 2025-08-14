---
title: "[Algorithm] cpp 백준 3611번: 팀의 난이도"
description: "팀의 난이도(같은 팀에서 일을 못하는 쌍/인원)를 최대화하는 문제는 최대밀도부분그래프와 동치입니다. r에 대해 |E(S)|-r|S|를 최대화하는 파라메트릭 최소절단을 구성하고 이분 탐색으로 r*를 찾은 뒤, 절단의 S측에서 최적 팀을 복원합니다. n≤100, m≤1000에서 안전합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
- Flow
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-3611
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
- Graph
- 그래프
- Flow
- 플로우
- Max Flow
- 최대유량
- Min Cut
- 최소절단
- Dinic
- 디닉
- Parametric Search
- 파라메트릭 탐색
- Binary Search
- 이분탐색
- Maximum Density Subgraph
- 최대밀도부분그래프
- Densest Subgraph
- 밀도부분그래프
- Residual Graph
- 잔여그래프
- Cut
- 컷
- NEERC
- NEERC 2006
- 팀의 난이도
- 팀
- Special Judge
- 스페셜저지
- Modeling
- 모델링
- Network Flow
- 네트워크 플로우
- Set Selection
- 부분집합 선택
- Subgraph
- 부분그래프
- Construction
- 구성
- Proof Sketch
- 정당성 스케치
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3611
- 요약: 같은 팀이 되었을 때 서로 일을 못 하는 사람들의 쌍이 주어질 때, 팀의 난이도(내부 불화 간선 수/팀원 수)를 최대화하는 팀을 찾아 구성원을 출력.
- 제한: n ≤ 100, m ≤ 1000, 같은 쌍 중복 없음.

## 입력/출력
```
입력
n m
a1 b1
a2 b2
...

출력
k
v1
v2
...
vk
```

예시
```
입력
5 6
1 5
5 4
4 2
2 5
1 2
3 1

출력(가능한 해 중 하나)
4
1
2
4
5
```

## 접근 개요
- 이 문제는 최대 밀도 부분 그래프(densest subgraph) 문제와 동치입니다. 목표는 S ⊆ V에 대해 |E(S)|/|S|를 최대화하는 S를 구하는 것.
- 표준 기법: 파라메트릭 탐색. 어떤 실수 r에 대해 f(r) = max_S (|E(S)| - r·|S|)를 계산하고, f(r) ≥ 0인 최대 r = r*를 찾으면, r*가 최대 밀도입니다.
- f(r)은 s-t 최소 절단(= 최대 유량)으로 계산할 수 있으며, r에 대해 단조성이 있어 이분 탐색로 r*를 구합니다. 절단의 s-도달 집합이 곧 최적 팀 후보가 됩니다.

## Mermaid로 보는 네트워크 구성
```mermaid
graph LR
  S((source)) --> Ei[edge nodes (m개)]
  Ei --> Vj[vertex nodes (n개)]
  Vj --> T((sink))
```

구체적 간선
- S → e_i: 용량 1
- e_i → u, e_i → v: 용량 INF (간선 i = (u, v))
- 각 정점 v: v → T 용량 r

이때 최소절단 값은 m - max_S (|E(S)| - r·|S|)와 대응하여, f(r) = m - mincut(S,T)로 환원됩니다.

## 알고리즘 설계
1) r의 범위를 [0, m]로 두고 이분 탐색(고정 70~80회)합니다.
2) 각 r마다 위 네트워크를 만들고 Dinic으로 최대유량 = 최소절단을 구합니다.
3) f(r) = m - mincut. f(r) > 0이면 더 큰 r를 탐색(가능성 있음), 아니면 줄입니다.
4) r* 근방에서 s-도달 정점 집합을 읽어 최적 팀을 복원합니다. 동률이면 아무 집합이나 허용.

### 정당성(요지)
- 최대밀도부분그래프의 고전적 파라메트릭 환원입니다. f(r) = max_S (|E(S)| - r|S|)의 부호는 r ≤ |E(S)|/|S|인 S의 존재 여부와 동치이므로, r* = sup{r | f(r) ≥ 0} = max_S |E(S)|/|S|입니다. 네트워크 구성은 가중 정점 컷으로 f(r)을 정확히 계산합니다.

## 복잡도
- 이분 탐색 횟수: O(log(1/ε)) ≈ 80.
- 한 번의 유량: 정점 O(n+m), 간선 O(m+n+m) 수준. n ≤ 100, m ≤ 1000이므로 충분히 빠릅니다.
- 총합 대략: O(80 · maxflow(V,E)). 실측상 수 밀리초 내.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Dinic {
	struct Edge {
		int to, rev;
		double cap;
	};
	int N;
	vector<vector<Edge>> graph;
	vector<int> level, work;
	const double EPS = 1e-9;

	explicit Dinic(int n) : N(n), graph(n), level(n), work(n) {}

	void addEdge(int u, int v, double c) {
		Edge a{v, (int)graph[v].size(), c};
		Edge b{u, (int)graph[u].size(), 0.0};
		graph[u].push_back(a);
		graph[v].push_back(b);
	}

	bool bfs(int s, int t) {
		fill(level.begin(), level.end(), -1);
		queue<int> q;
		level[s] = 0;
		q.push(s);
		while (!q.empty()) {
			int u = q.front(); q.pop();
			for (const auto &e : graph[u]) {
				if (level[e.to] < 0 && e.cap > EPS) {
					level[e.to] = level[u] + 1;
					q.push(e.to);
				}
			}
		}
		return level[t] >= 0;
	}

	double dfs(int u, int t, double f) {
		if (u == t) return f;
		for (int &i = work[u]; i < (int)graph[u].size(); i++) {
			Edge &e = graph[u][i];
			if (e.cap > EPS && level[e.to] == level[u] + 1) {
				double ret = dfs(e.to, t, min(f, e.cap));
				if (ret > EPS) {
					e.cap -= ret;
					graph[e.to][e.rev].cap += ret;
					return ret;
				}
			}
		}
		return 0.0;
	}

	double maxflow(int s, int t) {
		double flow = 0.0;
		while (bfs(s, t)) {
			fill(work.begin(), work.end(), 0);
			while (true) {
				double pushed = dfs(s, t, 1e100);
				if (pushed <= EPS) break;
				flow += pushed;
			}
		}
		return flow;
	}

	// After running maxflow, get vertices reachable from s in residual graph
	vector<int> mincut_reachable_from_source(int s) {
		const double EPS2 = 1e-9;
		vector<int> vis(N, 0);
		queue<int> q;
		vis[s] = 1;
		q.push(s);
		while (!q.empty()) {
			int u = q.front(); q.pop();
			for (const auto &e : graph[u]) {
				if (!vis[e.to] && e.cap > EPS2) {
					vis[e.to] = 1;
					q.push(e.to);
				}
			}
		}
		return vis;
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int n, m;
	if (!(cin >> n >> m)) return 0;
	vector<pair<int,int>> edges;
	edges.reserve(m);
	for (int i = 0; i < m; i++) {
		int a, b; cin >> a >> b;
		--a; --b;
		edges.emplace_back(a, b);
	}

	// Trivial case: no edges -> any single person is optimal (ratio 0)
	if (m == 0) {
		cout << 1 << "\n" << 1 << "\n";
		return 0;
	}

	auto build_and_flow = [&](double r, bool want_set, vector<int> &out_set)->double {
		// Node indexing:
		// 0..n-1: vertex nodes
		// n..n+m-1: edge nodes
		// s = n + m, t = n + m + 1
		int S = n + m;
		int T = n + m + 1;
		int tot = n + m + 2;
		const double INF = 1e100;

		Dinic din(tot);

		// s -> edge-node (capacity 1)
		for (int i = 0; i < m; i++) {
			int eNode = n + i;
			din.addEdge(S, eNode, 1.0);
		}

		// edge-node -> endpoint vertex (INF)
		for (int i = 0; i < m; i++) {
			int u = edges[i].first;
			int v = edges[i].second;
			int eNode = n + i;
			din.addEdge(eNode, u, INF);
			din.addEdge(eNode, v, INF);
		}

		// vertex -> t (capacity r)
		for (int v = 0; v < n; v++) {
			din.addEdge(v, T, r);
		}

		double f = din.maxflow(S, T);

		if (want_set) {
			auto vis = din.mincut_reachable_from_source(S);
			vector<int> pick;
			for (int v = 0; v < n; v++) if (vis[v]) pick.push_back(v + 1); // 1-indexed
			if (pick.empty()) {
				// As a fallback to guarantee non-empty output
				pick.push_back(1);
			}
			sort(pick.begin(), pick.end());
			out_set = move(pick);
		}
		return f;
	};

	// Binary search r*: largest r with delta = m - maxflow > 0 holds for r < r*, and delta == 0 for r >= r*.
	double lo = 0.0, hi = (double)m; // ratio is in [0, m]
	for (int it = 0; it < 80; it++) {
		double mid = (lo + hi) * 0.5;
		vector<int> dummy;
		double flow = build_and_flow(mid, false, dummy);
		double delta = (double)m - flow; // max_{S} (|E(S)| - r|S|)
		if (delta > 1e-9) lo = mid; else hi = mid;
	}
	double r_star = lo;

	// Retrieve the set: bias slightly below r* to avoid tie picking the empty set
	vector<int> answerSet;
	build_and_flow(max(0.0, r_star - 1e-7), true, answerSet);

	cout << (int)answerSet.size() << "\n";
	for (int v : answerSet) cout << v << "\n";
	return 0;
}
```

## 코너 케이스 체크리스트
- m = 0이면 비율이 0이므로 임의의 단일 정점이 최적.
- 여러 최적 해 존재 시 아무 집합이나 허용(스페셜 저지). 출력은 정렬.
- 고립 정점, 매우 촘촘/성긴 그래프, n=1/2/극값 등.

## 제출 전 점검
- 출력 형식: k 후 줄바꿈, 그다음 구성원 번호를 한 줄에 하나씩 오름차순 출력.
- 1-indexed 출력 확인, 입력은 1-indexed → 내부 0-indexed 변환 주의.
- 부동소수 이분 탐색 반복 수(예: 80) 충분히 큼.

## 참고자료
- 최대 밀도 부분 그래프(Densest Subgraph)와 최소절단 파라메트릭 환원 고전 기법
- 네트워크 플로우(최대유량/최소절단, Dinic)


