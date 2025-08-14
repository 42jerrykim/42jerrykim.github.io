---
title: "[Algorithm] cpp 백준 16367번: TV Show Game - 2-SAT 풀이"
description: "TV Show Game은 참가자마다 제출한 세 개의 (램프, 색) 예측 중 최소 두 개가 참이 되도록 램프 색을 조정할 수 있는지 판정하는 문제입니다. (a∨b)∧(a∨c)∧(b∨c) 제약을 2‑SAT로 모델링해 암시 그래프와 SCC로 가능 여부를 확인하고 해를 O(k+n)에 구성합니다."
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
- Problem-16367
- cpp
- C++
- Two SAT
- 2-SAT
- 2SAT
- Two-SAT
- SAT
- Satisfiability
- CNF
- Implication Graph
- Implication
- Graph
- 그래프
- SCC
- Strongly Connected Components
- Kosaraju
- Tarjan
- DFS
- 위상정렬
- Topological Sort
- Logical Constraints
- 논리 제약
- Constraint Satisfaction
- 제약 만족
- Boolean Logic
- 불 대수
- Bitset
- 논리식
- Modeling
- 모델링
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Pitfalls
- 실수 포인트
- Edge Cases
- 코너 케이스
- Testing
- 테스트
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Template
- 템플릿
- Debugging
- 디버깅
- Shortest Path
- 최단경로
- Disjoint Set Union
- 유니온파인드
- Binary Search
- 이분탐색
- Hashing
- 해싱
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16367
- 요약: 램프의 실제 색을 조정해 각 참가자가 제출한 세 개의 (램프, 색) 예측 중 적어도 두 개 이상이 맞도록 만들 수 있는지 여부와 한 가지 색 배치를 구합니다.

## 입력/출력
- 입력: 첫 줄에 램프 수 k (3 < k ≤ 5000), 참가자 수 n (1 ≤ n ≤ 10000). 다음 n줄에 걸쳐 세 개의 `(l, c)` 쌍이 공백으로 구분되어 주어집니다. `c`는 `B` 또는 `R`.
- 출력: 가능하면 길이 k의 문자열(각 문자는 `B` 또는 `R`)을 출력, 불가능하면 `-1`을 출력합니다.

예제 입력 1
```
7 5
3 R 5 R 6 B
1 B 2 B 3 R
4 R 5 B 6 B
5 R 6 B 7 B
1 R 2 R 4 R
```

예제 출력 1
```
BRRRBBB
```

## 접근 개요
- 각 예측 `(li, ci)`를 불리언 변수로 모델링합니다. 변수 `Xi`는 램프 i가 파란색(Blue)임을 의미하고, `¬Xi`는 빨간색(Red)을 의미하도록 둡니다.
- 한 참가자의 세 예측 `a, b, c`에 대해 "최소 두 개 참" 제약은 논리식 `(a∨b) ∧ (a∨c) ∧ (b∨c)`로 동치입니다.
- 위 식은 2-SAT의 절(OR)들의 곱 형태이므로, 암시 그래프(implication graph)를 만들고 SCC를 이용해 해를 구성합니다.

## 알고리즘 설계
- 리터럴 인덱싱: 램프 i(1-based)에 대해 `2*(i-1)`을 `Xi`(Blue), `2*(i-1)^1`을 `¬Xi`(Red)로 사용합니다.
- 절 추가: 절 `(p ∨ q)`는 암시 간선 `¬p → q`, `¬q → p`로 변환합니다. 각 참가자마다 `(a∨b)`, `(a∨c)`, `(b∨c)` 세 절을 추가합니다.
- Kosaraju(또는 Tarjan)로 SCC를 구하고, 어떤 변수 `Xi`와 `¬Xi`가 같은 SCC에 있으면 모순으로 불가능입니다.
- 위상 순서 역순으로 각 변수의 값을 할당해 한 가지 해를 복원합니다.

## 복잡도
- 절 수는 참가자당 3개, 간선은 절당 2개이므로 전체 간선은 `O(n)` 규모입니다. 변수/정점 수는 `O(k)`이므로 전체 시간 `O(k + n)`, 공간 `O(k + n)`.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct TwoSAT {
	int numVars;
	vector<vector<int>> graph, reverseGraph;
	vector<int> compId, order;
	vector<char> visited;

	TwoSAT(int n) : numVars(n) {
		graph.assign(2 * n, {});
		reverseGraph.assign(2 * n, {});
		visited.assign(2 * n, 0);
		compId.assign(2 * n, -1);
	}

	static inline int negateLiteral(int x) { return x ^ 1; }

	// Add clause (p ∨ q), where p, q are literal indices in [0, 2*numVars)
	void addOrClause(int p, int q) {
		int np = negateLiteral(p), nq = negateLiteral(q);
		graph[np].push_back(q);
		graph[nq].push_back(p);
		reverseGraph[q].push_back(np);
		reverseGraph[p].push_back(nq);
	}

	void dfs1(int v) {
		visited[v] = 1;
		for (int to : graph[v]) if (!visited[to]) dfs1(to);
		order.push_back(v);
	}
	void dfs2(int v, int cid) {
		compId[v] = cid;
		for (int to : reverseGraph[v]) if (compId[to] == -1) dfs2(to, cid);
	}

	bool satisfiable(vector<int>& assignment) {
		for (int v = 0; v < 2 * numVars; ++v) if (!visited[v]) dfs1(v);
		int cid = 0;
		for (int i = (int)order.size() - 1; i >= 0; --i) {
			int v = order[i];
			if (compId[v] == -1) dfs2(v, cid++);
		}
		assignment.assign(numVars, 0);
		for (int i = 0; i < numVars; ++i) {
			if (compId[2 * i] == compId[2 * i + 1]) return false;
			assignment[i] = compId[2 * i] > compId[2 * i + 1];
		}
		return true;
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int k, n;
	if (!(cin >> k >> n)) return 0;

	TwoSAT solver(k);

	auto literalOf = [](int lampIndex1Based, char color) {
		// Xi means lamp is Blue; ¬Xi means Red
		int base = 2 * (lampIndex1Based - 1);
		return (color == 'B') ? base : (base ^ 1);
	};

	for (int i = 0; i < n; ++i) {
		int l1, l2, l3;
		char c1, c2, c3;
		cin >> l1 >> c1 >> l2 >> c2 >> l3 >> c3;
		int a = literalOf(l1, c1);
		int b = literalOf(l2, c2);
		int c = literalOf(l3, c3);
		// At least two of (a, b, c) must be true: (a∨b) ∧ (a∨c) ∧ (b∨c)
		solver.addOrClause(a, b);
		solver.addOrClause(a, c);
		solver.addOrClause(b, c);
	}

	vector<int> assign;
	if (!solver.satisfiable(assign)) {
		cout << -1 << '\n';
		return 0;
	}

	for (int i = 0; i < k; ++i) {
		cout << (assign[i] ? 'B' : 'R');
	}
	cout << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- 모든 참가자가 같은 램프만 반복적으로 예측하는 경우(중복 리터럴)
- 상충하는 제약으로 인해 동일 변수와 부정이 동일 SCC에 들어가는 경우
- k가 작고 n이 큰 경우의 성능, 반대로 k가 크고 n이 작은 경우의 성능
- 해가 여러 개인 경우 임의 해 출력의 일관성

## 참고자료
- 2-SAT, Implication Graph, SCC 기반 해법 개요: CLRS, Competitive Programming 3 등

