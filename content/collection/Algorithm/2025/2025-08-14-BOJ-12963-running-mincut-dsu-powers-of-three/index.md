---
title: "[Algorithm] C++ 백준 12963번: 달리기"
description: "도로 i의 용량이 3^i인 무향 그래프에서 0→N-1로 도달 가능한 최대 인원을 구한다. 3의 거듭제곱 가중치의 유일성으로 최소 s-t 컷이 단일해가 되며, 간선을 인덱스 내림차순으로 확인하며 DSU로 s와 t를 잇는 간선만 더해 합을 구해 1e9+7로 출력한다."
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
- Problem-12963
- cpp
- C++
- Python
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
- Greedy
- 그리디
- Graph
- 그래프
- Cut
- 컷
- Min Cut
- 최소컷
- Max Flow
- 최대유량
- Disjoint Set Union
- 유니온파인드
- DSU
- Connectivity
- 연결성
- Undirected Graph
- 무향그래프
- Unique Weights
- 유일가중치
- Powers of Three
- 3의 거듭제곱
- Kruskal-like
- 크루스칼 유사
- Modulo
- 모듈러
- 1e9+7
- Math
- 수학
- Implementation Details
- 구현 디테일
- Proof
- 증명
- S-T Cut
- s-t 컷
- Path Capacity
- 경로 용량
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12963
- 요약: 각 도로 i는 최대 3^i명이 통과 가능하다. 0번에서 N-1번으로 도달할 수 있는 사람 수의 최댓값을 1,000,000,007로 나눈 값을 구한다.
- 제한/스펙: 2 ≤ N ≤ 2000, 0 ≤ M ≤ 2000, 무향 그래프, 동일 간선 중복 없음

## 입력/출력
```
예시 입력
4 4
0 1
1 3
0 2
2 3
```
```
예시 출력
10
```

## 접근 개요
- 각 간선의 용량이 3^i로 서로 다른 자리값을 가지므로 어떤 s-t 컷의 총합은 기수 3 표현처럼 유일하다.
- 따라서 최소 s-t 컷은 “가중치가 큰 간선을 우선 고려”하는 그리디로 판별 가능하다.
- 간선을 인덱스 내림차순(i = M-1 → 0)으로 보며, 해당 간선을 추가했을 때 s와 t가 연결되면 그 간선은 컷에 포함(합에 3^i 더함), 아니면 컴포넌트를 합친다(DSU).

## 알고리즘
1. 간선을 입력 순서(= 인덱스)대로 저장하고, i = M-1..0 순으로 처리한다.
2. 현재 DSU에서 `find(0)`과 `find(N-1)`이 서로 다른 상태를 유지하며, 간선 (u,v)가 s-측과 t-측을 직접 잇는다면 컷에 포함하고 답에 3^i를 더한다.
3. 그렇지 않다면 u와 v를 유니온한다.
4. 모든 간선을 처리한 총합을 MOD=1,000,000,007로 출력한다.

올바름 근거(스케치): 3^i 가중치는 자리값이 커서 상위 인덱스를 이기는 어떤 조합도 존재하지 않으므로, 내림차순으로 “상위 간선이 컷에 들어갈지”를 그 순간의 s/t 분할로 확정해도 전역 최소 컷과 일치한다. 이는 이진(또는 기수) 유일 표현 기반의 그리디 정당화와 동일한 논리다.

## 복잡도
- 시간: O(M · α(N)) (DSU 상수 포함)
- 공간: O(N + M)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 1000000007LL;

struct DisjointSetUnion {
	vector<int> parent;
	vector<int> size;
	DisjointSetUnion(int n) : parent(n), size(n, 1) { iota(parent.begin(), parent.end(), 0); }
	int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
	bool unite(int a, int b) {
		a = find(a); b = find(b);
		if (a == b) return false;
		if (size[a] < size[b]) swap(a, b);
		parent[b] = a;
		size[a] += size[b];
		return true;
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, M;
	if (!(cin >> N >> M)) return 0;

	vector<pair<int,int>> edges(M);
	for (int i = 0; i < M; ++i) {
		int a, b; cin >> a >> b;
		edges[i] = {a, b};
	}

	vector<long long> pow3(max(1, M + 1), 1);
	for (int i = 1; i <= M; ++i) pow3[i] = (pow3[i - 1] * 3) % MOD;

	DisjointSetUnion dsu(N);
	long long answer = 0;

	for (int i = M - 1; i >= 0; --i) {
		int u = edges[i].first;
		int v = edges[i].second;
		int ru = dsu.find(u);
		int rv = dsu.find(v);
		int rs = dsu.find(0);
		int rt = dsu.find(N - 1);

		if (ru == rv) continue;

		bool connectsST = (ru == rs && rv == rt) || (ru == rt && rv == rs);
		if (connectsST) {
			answer += pow3[i];
			if (answer >= MOD) answer -= MOD;
		} else {
			dsu.unite(ru, rv);
		}
	}

	cout << (answer % MOD) << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- 경로 자체가 존재하지 않는 경우(M=0 또는 분리 그래프): 정답 0
- s=0, t=N-1이 이미 동일 컴포넌트인 경우와 아닌 경우 모두 처리
- 사이클/다중 경로가 많아도 DSU 로직에 영향 없음
- MOD 연산 누락/오버플로 방지(3의 거듭제곱 사전 계산)

## 제출 전 점검
- 입출력 개행/형식 확인, 64-bit 정수 사용, DSU 경로 압축/유니온 기준 확인
- `pow3` 인덱싱 범위, M=0 처리

## 참고자료/유사문제
- Kruskal 그리디와 s-t 컷의 유일 가중치 트릭(가중치가 2^i 또는 3^i인 경우)
- Max-Flow/Min-Cut 정리(개념 배경)


