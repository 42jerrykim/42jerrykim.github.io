---
title: "[Algorithm] cpp 백준 17429번: 국제 메시 기구"
description: "트리 경로·서브트리에 더하기/곱하기(아핀) 갱신과 합 질의. HLD로 경로 분할, lazy 세그트리로 2^32 모듈러 유지하며 O(log^2 N) 처리. 구현 포인트와 엣지 케이스 체크까지 정리."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17429
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
- Tree
- 트리
- Segment Tree
- 세그먼트 트리
- Lazy Propagation
- 레이지 프로퍼게이션
- Heavy-Light Decomposition
- HLD
- 경로 질의
- Path Query
- Subtree Query
- 서브트리 질의
- Range Update
- 구간 갱신
- Affine Update
- 아핀 변환
- Euler Tour
- 오일러 투어
- Binary Lifting
- 이진 리프팅
- Modulo
- 모듈러
- 2^32
- 국제 메시 기구
- BOJ17429
- 자료구조
- Data Structures
- Math
- 수학
- String
- 문자열
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17429
- 요약: 루트가 1인 트리에서 다음 연산을 처리합니다.
  - `1 X V`: X의 서브트리 모든 정점에 V 더하기
  - `2 X Y V`: X–Y 경로 모든 정점에 V 더하기
  - `3 X V`: X의 서브트리 모든 정점에 V 곱하기
  - `4 X Y V`: X–Y 경로 모든 정점에 V 곱하기
  - `5 X`: X의 서브트리 합 출력
  - `6 X Y`: X–Y 경로 합 출력
- 출력은 모두 2^32로 나눈 나머지로 계산합니다.

## 입력/출력 형식
```
입력
N Q
N-1개의 간선 (무방향, 트리)
Q개의 명령 (타입에 따라 인자 상이)

출력
타입 5, 6 명령마다 한 줄에 결과(모듈러 2^32)
```

## 접근 개요
- **핵심 아이디어**: 값 연산은 모두 더하기와 곱하기의 조합이므로 각 원소에 대한 변환을 f(x)=a·x+b 꼴(아핀 변환)로 통합해 구간에 전파합니다.
- **경로 연산**: Heavy-Light Decomposition(HLD)로 임의 경로를 O(log N)개의 연속 구간으로 분할하여 세그먼트 트리로 처리합니다.
- **서브트리 연산**: HLD에서 부여한 위치(`pos`)와 서브트리 크기(`subtreeSize`)로 [pos[u], pos[u]+sz[u]-1] 범위를 한 번에 갱신/질의합니다.
- **모듈러**: 문제 요구대로 모든 덧셈/곱셈/합은 2^32 모듈러로 유지합니다(비용 절감을 위해 마스킹 사용).

```mermaid
flowchart TD
  A[Query t, args] --> B{t in {1,3}?}
  B -- Yes(Subtree) --> C[range on [pos[u], pos[u]+sz[u]-1]]
  B -- No(Path) --> D[split by HLD heads]
  D --> E[sum of O(log N) segments]
  C --> F[Segment Tree]
  E --> F
  F --> G{affine lazy: mul, add}
  G --> H[apply to node sum and push]
```

## 알고리즘 설계
- **HLD 전처리**: parent/depth, heavy child, head/pos, subtreeSize를 계산(반복 DFS + 비재귀 분해)합니다.
- **세그먼트 트리**: 각 노드는 구간 합을 저장하고, lazy에 (mul, add)를 유지합니다.
  - 구간에 f(x)=a·x+b 적용 시: `sum = sum*a + b*len`.
  - lazy 전파 결합: `(mul, add)` ◦ `(mul', add') = `(mul*mul', add*mul' + add')`.
- **연산 복잡도**:
  - 서브트리 갱신/질의: O(log N)
  - 경로 갱신/질의: O(log^2 N)

## 복잡도
- 시간: O((N+Q) log N) ~ 경로 연산은 O(log^2 N)
- 공간: O(N) (세그먼트 트리와 HLD 보조 배열)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

static const ull MOD_MASK = 0xFFFFFFFFULL;

struct SegmentTree {
	int n;
	vector<ull> tree;
	vector<ull> lazyMul;
	vector<ull> lazyAdd;

	SegmentTree() {}
	SegmentTree(int n_) { init(n_); }

	void init(int n_) {
		n = n_;
		tree.assign(4 * n + 4, 0);
		lazyMul.assign(4 * n + 4, 1);
		lazyAdd.assign(4 * n + 4, 0);
	}

	inline void apply(int idx, int l, int r, ull mul, ull add) {
		ull len = (ull)(r - l + 1);
		tree[idx] = (tree[idx] * mul + add * len) & MOD_MASK;
		lazyMul[idx] = (lazyMul[idx] * mul) & MOD_MASK;
		lazyAdd[idx] = (lazyAdd[idx] * mul + add) & MOD_MASK;
	}

	inline void push(int idx, int l, int r) {
		if (lazyMul[idx] == 1 && lazyAdd[idx] == 0) return;
		int mid = (l + r) >> 1;
		int L = idx << 1, R = L | 1;
		apply(L, l, mid, lazyMul[idx], lazyAdd[idx]);
		apply(R, mid + 1, r, lazyMul[idx], lazyAdd[idx]);
		lazyMul[idx] = 1;
		lazyAdd[idx] = 0;
	}

	void update(int idx, int l, int r, int ql, int qr, ull mul, ull add) {
		if (qr < l || r < ql) return;
		if (ql <= l && r <= qr) {
			apply(idx, l, r, mul, add);
			return;
		}
		push(idx, l, r);
		int mid = (l + r) >> 1;
		int L = idx << 1, R = L | 1;
		update(L, l, mid, ql, qr, mul, add);
		update(R, mid + 1, r, ql, qr, mul, add);
		tree[idx] = (tree[L] + tree[R]) & MOD_MASK;
	}

	ull query(int idx, int l, int r, int ql, int qr) {
		if (qr < l || r < ql) return 0;
		if (ql <= l && r <= qr) return tree[idx];
		push(idx, l, r);
		int mid = (l + r) >> 1;
		int L = idx << 1, R = L | 1;
		ull res = (query(L, l, mid, ql, qr) + query(R, mid + 1, r, ql, qr)) & MOD_MASK;
		return res;
	}

	inline void range_affine(int l, int r, ull mul, ull add) {
		if (l > r) return;
		update(1, 1, n, l, r, mul & MOD_MASK, add & MOD_MASK);
	}
	inline ull range_sum(int l, int r) {
		if (l > r) return 0;
		return query(1, 1, n, l, r) & MOD_MASK;
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, Q;
	if (!(cin >> N >> Q)) return 0;

	vector<vector<int>> adj(N + 1);
	for (int i = 0; i < N - 1; ++i) {
		int s, e;
		cin >> s >> e;
		adj[s].push_back(e);
		adj[e].push_back(s);
	}

	vector<int> parent(N + 1, 0), depth(N + 1, 0), heavy(N + 1, -1), subtreeSize(N + 1, 0);
	vector<int> head(N + 1, 0), pos(N + 1, 0);

	vector<int> order;
	order.reserve(N);
	{
		vector<int> st;
		st.reserve(N);
		parent[1] = 0;
		depth[1] = 0;
		st.push_back(1);
		while (!st.empty()) {
			int u = st.back(); st.pop_back();
			order.push_back(u);
			for (int v : adj[u]) {
				if (v == parent[u]) continue;
				parent[v] = u;
				depth[v] = depth[u] + 1;
				st.push_back(v);
			}
		}
	}

	for (int i = (int)order.size() - 1; i >= 0; --i) {
		int u = order[i];
		int maxSz = 0;
		subtreeSize[u] = 1;
		for (int v : adj[u]) {
			if (v == parent[u]) continue;
			subtreeSize[u] += subtreeSize[v];
			if (subtreeSize[v] > maxSz) {
				maxSz = subtreeSize[v];
				heavy[u] = v;
			}
		}
	}

	int curPos = 1;
	{
		vector<pair<int,int>> st;
		st.reserve(N);
		st.emplace_back(1, 1);
		while (!st.empty()) {
			auto [u, h] = st.back(); st.pop_back();
			int x = u;
			while (x != -1) {
				head[x] = h;
				pos[x] = curPos++;
				for (int v : adj[x]) {
					if (v == parent[x] || v == heavy[x]) continue;
					st.emplace_back(v, v);
				}
				x = heavy[x];
			}
		}
	}

	SegmentTree seg(N);

	auto update_subtree = [&](int u, ull mul, ull add) {
		int l = pos[u];
		int r = pos[u] + subtreeSize[u] - 1;
		seg.range_affine(l, r, mul, add);
	};

	function<void(int,int,ull,ull)> update_path = [&](int u, int v, ull mul, ull add) {
		while (head[u] != head[v]) {
			if (depth[head[u]] < depth[head[v]]) swap(u, v);
			int hu = head[u];
			seg.range_affine(pos[hu], pos[u], mul, add);
			u = parent[hu];
		}
		if (depth[u] > depth[v]) swap(u, v);
		seg.range_affine(pos[u], pos[v], mul, add);
	};

	auto query_subtree = [&](int u) -> ull {
		int l = pos[u];
		int r = pos[u] + subtreeSize[u] - 1;
		return seg.range_sum(l, r);
	};

	function<ull(int,int)> query_path = [&](int u, int v) -> ull {
		ull res = 0;
		while (head[u] != head[v]) {
			if (depth[head[u]] < depth[head[v]]) swap(u, v);
			int hu = head[u];
			res = (res + seg.range_sum(pos[hu], pos[u])) & MOD_MASK;
			u = parent[hu];
		}
		if (depth[u] > depth[v]) swap(u, v);
		res = (res + seg.range_sum(pos[u], pos[v])) & MOD_MASK;
		return res;
	};

	for (int i = 0; i < Q; ++i) {
		int t; cin >> t;
		if (t == 1) {
			int X; ull V; cin >> X >> V;
			update_subtree(X, 1, V & MOD_MASK);
		} else if (t == 2) {
			int X, Y; ull V; cin >> X >> Y >> V;
			update_path(X, Y, 1, V & MOD_MASK);
		} else if (t == 3) {
			int X; ull V; cin >> X >> V;
			update_subtree(X, V & MOD_MASK, 0);
		} else if (t == 4) {
			int X, Y; ull V; cin >> X >> Y >> V;
			update_path(X, Y, V & MOD_MASK, 0);
		} else if (t == 5) {
			int X; cin >> X;
			cout << (query_subtree(X) & MOD_MASK) << '\n';
		} else if (t == 6) {
			int X, Y; cin >> X >> Y;
			cout << (query_path(X, Y) & MOD_MASK) << '\n';
		}
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- V=0 곱 연산으로 구간을 전부 0으로 만드는 경우
- X=Y인 경로 연산(단일 정점)
- 루트/리프에 대한 서브트리 연산
- 깊이가 큰 경로(체인처럼 긴 트리)
- 대량 갱신 후 대량 질의 순서 섞임

## 제출 전 점검
- 모든 연산과 합을 2^32 마스킹으로 유지하는지 확인
- lazy 결합 법칙 `(mul, add)` 적용 순서 점검
- 경로 분할 시 head 비교 방향(depth 큰 쪽부터 처리) 확인
- 입출력 개행/버퍼링(`sync_with_stdio(false)`, `tie(nullptr)`) 적용

## 참고자료
- Heavy-Light Decomposition: "CP-Algorithms – Heavy-Light Decomposition"
- Segment Tree with lazy propagation: "CP-Algorithms – Segment Tree"


