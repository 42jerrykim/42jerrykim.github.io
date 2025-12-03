---
title: "[Algorithm] C++ 백준 1210번: 마피아 - 정점 분할 최소 컷"
description: "마피아의 이동을 막기 위해 톨게이트를 최소 비용으로 점거하는 문제를 정점 가중치 s-t 최소 컷으로 모델링합니다. 각 정점을 in/out으로 분할하고 내부 간선에 비용을 두어 최대 유량=최소 컷으로 풀이하며, 시작/도착 정점 점거 허용까지 반영합니다."
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
- Problem-1210
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
- 최대 유량
- Min Cut
- 최소 컷
- Vertex Cut
- 정점 컷
- Node Splitting
- 정점 분할
- Dinic
- 디닉
- Network Flow
- 네트워크 플로우
- s-t Cut
- s-t 컷
- Undirected Graph
- 무방향 그래프
- BOI 2008
- Mafia
- 마피아
- Minimum Vertex Separator
- 최소 정점 분리집합
- Cut Recovery
- 컷 복원
- Special Judge
- 스페셜 저지
- Safety
- 안정성
- Overflow
- 오버플로
- INF
- 무한대
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/1210
- 요약: 정점에 점거 비용이 있는 무방향 그래프에서 시작점에서 도착점까지의 모든 경로를 차단하도록 정점들을 선택하되, 총 비용의 합이 최소가 되도록 한다. 선택한 정점 번호를 오름차순으로 출력한다. (스폐셜 저지)

## 입력/출력
```
입력
n m
s t
c1
c2
...
cn
u1 v1
...
um vm

제한: 1 ≤ n ≤ 200, 1 ≤ m ≤ 20000, 비용 ≤ 10^7
```
```
출력
조건을 만족하는 정점(톨게이트) 번호를 오름차순으로 공백 구분 출력
```

## 접근 개요
- 핵심 관찰: 경로를 “정점”을 통해 차단하므로 최소 정점 컷 문제다. 정점에 비용이 있으므로 “정점 용량” 최소 컷으로 변환한다.
- 모델링: 각 정점 `v`를 `v_in → v_out`으로 분할하고, 내부 간선 용량을 `cost[v]`로 둔다. 원래 무방향 간선 `(u, v)`는 `u_out → v_in`, `v_out → u_in` 으로 무한대 용량을 둔다.
- s/t 점거 허용: 시작/도착 정점도 점거할 수 있어야 하므로 소스는 `in(s)`, 싱크는 `out(t)`로 둔다. 이렇게 하면 `s`나 `t`의 내부 간선을 끊는 선택도 가능하다.
- 해법: Dinic 등 최대 유량 알고리즘으로 `maxflow = mincut`을 구한 뒤, 잔여 그래프에서 `in(v)`는 도달 가능이고 `out(v)`는 불가인 정점 `v`가 최소 정점 컷에 해당한다.

## 알고리즘 설계
1) 정점 분할: 모든 정점 `v`에 대해 `in(v) → out(v)` 간선을 용량 `cost[v]`로 추가한다.
2) 간선 처리: 각 무방향 간선 `(u, v)`에 대해 `out(u) → in(v)`와 `out(v) → in(u)`에 무한대 용량을 추가한다.
3) 소스/싱크: `S = in(s)`, `T = out(t)`.
4) 최대 유량 계산: Dinic로 `max_flow(S, T)`.
5) 컷 복원: 소스에서 잔여 용량으로 도달 가능한 집합을 `Reach`라 하면, `Reach(in(v)) = true`이면서 `Reach(out(v)) = false`인 `v`들이 해답.

올바름 근거(스케치)
- 정점 용량을 내부 간선으로 치환하면, 임의의 s-t 경로는 반드시 `v_in → v_out`을 통과한다. 해당 간선을 자르면 그 정점은 차단된다.
- 무방향 간선을 양방향 무한 용량으로 두면 원래 경로 집합과 동치인 경로 집합이 보존된다.
- 최대 유량–최소 컷 정리에 의해 계산된 컷의 용량 합이 최소이며, 복원 규칙으로 얻은 정점 집합이 그 최소 컷을 이룬다.

## 복잡도
- Dinic: `O(E * sqrt(V))`가 아닌 일반 구현 기준 `O(E * V^2)` 최악이지만, 실전에서는 빠르게 동작한다. 여기서는 `V ≈ 2n ≤ 400`, `E ≈ 2m + n` 범위로 충분히 통과한다.
- 구현 상에서는 `long long`으로 용량을 관리하고, 무한대는 `~1e18` 근처 큰 값으로 둔다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 INF = (1LL << 60);

struct Edge {
	int to, rev;
	int64 cap;
	Edge(int t, int r, int64 c) : to(t), rev(r), cap(c) {}
};

struct Dinic {
	int N;
	vector<vector<Edge>> g;
	vector<int> level, it;
	Dinic(int n) : N(n), g(n), level(n), it(n) {}
	void add_edge(int u, int v, int64 c) {
		g[u].emplace_back(v, (int)g[v].size(), c);
		g[v].emplace_back(u, (int)g[u].size()-1, 0);
	}
	bool bfs(int s, int t) {
		fill(level.begin(), level.end(), -1);
		queue<int> q; level[s] = 0; q.push(s);
		while (!q.empty()) {
			int u = q.front(); q.pop();
			for (auto &e : g[u]) if (e.cap > 0 && level[e.to] == -1) {
				level[e.to] = level[u] + 1;
				q.push(e.to);
			}
		}
		return level[t] != -1;
	}
	int64 dfs(int u, int t, int64 f) {
		if (u == t) return f;
		for (int &i = it[u]; i < (int)g[u].size(); ++i) {
			Edge &e = g[u][i];
			if (e.cap > 0 && level[e.to] == level[u] + 1) {
				int64 ret = dfs(e.to, t, min(f, e.cap));
				if (ret > 0) {
					e.cap -= ret;
					g[e.to][e.rev].cap += ret;
					return ret;
				}
			}
		}
		return 0;
	}
	int64 max_flow(int s, int t) {
		int64 flow = 0, add;
		while (bfs(s, t)) {
			fill(it.begin(), it.end(), 0);
			while ((add = dfs(s, t, INF)) > 0) flow += add;
		}
		return flow;
	}
	vector<int> reachable_from(int s) {
		vector<int> vis(N, 0);
		stack<int> st; st.push(s); vis[s] = 1;
		while (!st.empty()) {
			int u = st.top(); st.pop();
			for (auto &e : g[u]) if (e.cap > 0 && !vis[e.to]) {
				vis[e.to] = 1; st.push(e.to);
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
	int s, t; cin >> s >> t; --s; --t;

	vector<int64> cost(n);
	for (int i = 0; i < n; ++i) cin >> cost[i];

	auto in = [&](int v){ return 2*v; };
	auto out = [&](int v){ return 2*v+1; };

	Dinic dinic(2*n);

	// 모든 정점에 원래 비용을 사용 (s, t 포함해서 점거 가능)
	for (int v = 0; v < n; ++v) {
		dinic.add_edge(in(v), out(v), cost[v]);
	}

	// 무방향 간선 → 양방향 무한 용량
	for (int i = 0; i < m; ++i) {
		int u, v; cin >> u >> v; --u; --v;
		dinic.add_edge(out(u), in(v), INF);
		dinic.add_edge(out(v), in(u), INF);
	}

	int S = in(s), T = out(t);
	dinic.max_flow(S, T);

	auto reach = dinic.reachable_from(S);
	vector<int> ans;
	for (int v = 0; v < n; ++v) {
		if (reach[in(v)] && !reach[out(v)]) ans.push_back(v+1);
	}
	sort(ans.begin(), ans.end());
	for (int i = 0; i < (int)ans.size(); ++i) {
		if (i) cout << ' ';
		cout << ans[i];
	}
	cout << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- `s = t`인 경우: 내부 간선 하나를 자르면 해답이 되므로 올바르게 동작하는지 확인
- 간선이 매우 많은 그래프(최대 m)에서 성능/시간 초과 여부
- 비용이 큰 경우(최대 1e7) 합계 범위와 오버플로 방지(`long long` 사용)
- 고립 정점/단일 경로/다중 경로 등 다양한 구조

## 제출 전 점검
- 입출력 포맷 및 개행 처리 확인
- `INF`는 충분히 큰가(여기서는 `1<<60` 사용) 확인
- 소스/싱크 설정이 `S=in(s)`, `T=out(t)`인지 확인 (s/t 점거 허용)
- 컷 복원 규칙: `in` reachable ∧ `out` not reachable

## 참고자료/유사문제
- Minimum s-t Vertex Cut via Node-Splitting
- 최대 유량–최소 컷 정리
- BOI 2008 관련 자료


