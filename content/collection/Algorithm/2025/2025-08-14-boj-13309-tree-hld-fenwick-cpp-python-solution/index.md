---
title: "[Algorithm] cpp-python 백준 13309번: 트리 - 경로 질의와 간선 제거"
description: "트리에서 두 정점의 연결 여부를 빠르게 판별하고, 결과에 따라 부모-자식 간선을 제거하는 온라인 질의를 처리합니다. HLD와 Fenwick Tree로 경로를 O(log N)에 분해해 2e5도 안정적으로 통과합니다."
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
- Problem-13309
- cpp
- python
- C++
- Python
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
- Connectivity
- 연결성
- Path Query
- 경로 질의
- Heavy-Light Decomposition
- HLD
- Fenwick Tree
- BIT
- Binary Indexed Tree
- 세그먼트 트리
- Segment Tree
- Disjoint Set Union
- 유니온파인드
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13309
- 요약: 루트가 1인 트리에서 Q개의 온라인 질의를 처리한다. 각 질의는 두 정점 b, c가 연결되어 있는지 묻고(d=0) 또는 물은 뒤(d=1) 답이 YES이면 `parent[b]-b` 간선을, NO이면 `parent[c]-c` 간선을 제거한다. 제거는 0회 혹은 1회만 일어나며 이미 제거된 간선은 무시된다.

## 입력/출력
```
입력
N Q
parent[2]
parent[3]
...
parent[N]
b c d  (× Q)

출력
각 질의마다 연결되면 YES, 아니면 NO
```

## 접근 개요
- 핵심: 간선 제거 이후의 경로 연결성 여부는 "경로 위에 끊어진 간선이 존재하는가"로 환원된다.
- HLD(Heavy-Light Decomposition)로 임의의 경로를 O(log N)개의 연속 구간으로 분해하고, 각 간선을 "더 깊은 정점의 위치"에 매핑해 1(끊김)/0(연결) 표시한다.
- Fenwick Tree(BIT)로 구간 합을 빠르게 계산하면, 두 정점 경로 합이 0이면 연결, 1 이상이면 불연결이다.
- d=1일 때는 연결 여부에 따라 `b` 또는 `c`의 부모-자식 간선을 한 번만 1로 설정(중복 삭제 방지)하면 된다.

## 알고리즘 설계
1) 트리 입력 후, 자식 리스트 구성
2) 반복형 DFS로 `depth`, `subtree size`, `heavy child` 계산
3) 반복형 분해로 `head`, `pos`를 부여하며 선형화
4) Fenwick Tree를 크기 N으로 초기화: `pos[x]`에 간선 `(parent[x], x)`의 상태를 저장(끊김=1)
5) 경로 질의 `pathSum(u, v)`:
   - 체인이 다를 때마다 더 깊은 체인의 머리까지 합을 더하고, 부모 체인으로 점프
   - 같은 체인이 되면 `pos[lca]+1..pos[u]` 구간을 더함(LCA 정점 자체는 간선이 없음)
6) 답 출력 후 d=1이면 연결 시 b, 불연결 시 c를 선택해 해당 정점이 루트가 아니고 아직 미삭제면 `pos[x]`에 +1 업데이트

## 복잡도
- 전처리: O(N)
- 질의당: O(log N)
- 전체: O((N+Q) log N)
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
	int n;
	vector<int> bit;
	Fenwick(int n = 0) { init(n); }
	void init(int n_) { n = n_; bit.assign(n + 1, 0); }
	void add(int idx, int delta) {
		for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
	}
	int sumPrefix(int idx) const {
		int s = 0;
		for (; idx > 0; idx -= idx & -idx) s += bit[idx];
		return s;
	}
	int sumRange(int l, int r) const {
		if (l > r) return 0;
		return sumPrefix(r) - sumPrefix(l - 1);
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, Q;
	if (!(cin >> N >> Q)) return 0;

	vector<int> parent(N + 1, 0);
	vector<vector<int>> children(N + 1);
	for (int i = 2; i <= N; ++i) {
		int a; cin >> a;
		parent[i] = a;
		children[a].push_back(i);
	}

	// HLD preprocessing
	vector<int> depth(N + 1, 0), sz(N + 1, 0), heavy(N + 1, 0);
	{
		// iterative DFS to get order and depths
		vector<int> order; order.reserve(N);
		order.push_back(1);
		for (size_t i = 0; i < order.size(); ++i) {
			int u = order[i];
			for (int v : children[u]) {
				depth[v] = depth[u] + 1;
				order.push_back(v);
			}
		}
		// post-order for sizes and heavy
		for (int i = (int)order.size() - 1; i >= 0; --i) {
			int u = order[i];
			sz[u] = 1;
			int maxSize = 0, heavyChild = 0;
			for (int v : children[u]) {
				sz[u] += sz[v];
				if (sz[v] > maxSize) {
					maxSize = sz[v];
					heavyChild = v;
				}
			}
			heavy[u] = heavyChild;
		}
	}

	vector<int> head(N + 1, 0), pos(N + 1, 0);
	int curPos = 1;
	{
		// iterative decompose
		vector<pair<int,int>> st;
		st.reserve(N);
		st.emplace_back(1, 1); // (node, head)
		while (!st.empty()) {
			auto [u, h] = st.back(); st.pop_back();
			int cur = u;
			while (cur != 0) {
				head[cur] = h;
				pos[cur] = curPos++;
				for (int v : children[cur]) {
					if (v == heavy[cur]) continue;
					st.emplace_back(v, v);
				}
				cur = heavy[cur];
			}
		}
	}

	Fenwick fw(N + 2);
	vector<char> cut(N + 1, 0); // cut[x] = 1 if edge (parent[x], x) removed

	auto pathSum = [&](int u, int v) -> int {
		int res = 0;
		while (head[u] != head[v]) {
			if (depth[head[u]] < depth[head[v]]) swap(u, v);
			res += fw.sumRange(pos[head[u]], pos[u]);
			u = parent[head[u]];
		}
		if (depth[u] < depth[v]) swap(u, v);
		// exclude LCA node itself because edges are mapped to deeper nodes' positions
		res += fw.sumRange(pos[v] + 1, pos[u]);
		return res;
	};

	for (int i = 0; i < Q; ++i) {
		int b, c, d;
		cin >> b >> c >> d;
		bool connected = (pathSum(b, c) == 0);
		cout << (connected ? "YES\n" : "NO\n");
		if (d == 1) {
			int x = connected ? b : c;
			if (x != 1 && !cut[x]) {
				cut[x] = 1;
				fw.add(pos[x], 1);
			}
		}
	}
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
input = sys.stdin.readline

def main():
    N_Q = input().split()
    if not N_Q:
        return
    N, Q = map(int, N_Q)

    parent = [0] * (N + 1)
    children = [[] for _ in range(N + 1)]
    for i in range(2, N + 1):
        a = int(input())
        parent[i] = a
        children[a].append(i)

    depth = [0] * (N + 1)
    size = [0] * (N + 1)
    heavy = [0] * (N + 1)

    # BFS for depths and order
    order = [1]
    for u in order:
        for v in children[u]:
            depth[v] = depth[u] + 1
            order.append(v)
    # post-order sizes and heavy
    for u in reversed(order):
        size[u] = 1
        mxs, hv = 0, 0
        for v in children[u]:
            size[u] += size[v]
            if size[v] > mxs:
                mxs = size[v]
                hv = v
        heavy[u] = hv

    head = [0] * (N + 1)
    pos = [0] * (N + 1)
    cur_pos = 1

    stack = [(1, 1)]
    while stack:
        u, h = stack.pop()
        cur = u
        while cur:
            head[cur] = h
            pos[cur] = cur_pos
            cur_pos += 1
            for v in children[cur]:
                if v == heavy[cur]:
                    continue
                stack.append((v, v))
            cur = heavy[cur]

    class Fenwick:
        __slots__ = ("n", "bit")
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, delta):
            n = self.n
            bit = self.bit
            while i <= n:
                bit[i] += delta
                i += i & -i
        def sum_prefix(self, i):
            s = 0
            bit = self.bit
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s
        def sum_range(self, l, r):
            if l > r:
                return 0
            return self.sum_prefix(r) - self.sum_prefix(l - 1)

    fw = Fenwick(N + 2)
    cut = [False] * (N + 1)

    def path_sum(u, v):
        res = 0
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            res += fw.sum_range(pos[head[u]], pos[u])
            u = parent[head[u]]
        if depth[u] < depth[v]:
            u, v = v, u
        res += fw.sum_range(pos[v] + 1, pos[u])
        return res

    out_lines = []
    for _ in range(Q):
        b, c, d = map(int, input().split())
        connected = (path_sum(b, c) == 0)
        out_lines.append("YES" if connected else "NO")
        if d == 1:
            x = b if connected else c
            if x != 1 and not cut[x]:
                cut[x] = True
                fw.add(pos[x], 1)
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 루트(1) 관련 삭제 시도: 루트는 부모가 없으므로 무시되어야 함
- 이미 끊긴 간선 재삭제: 한 번만 반영되도록 체크 배열 필요
- b=c 같은 자기 자신 질의: 항상 YES, d=1이면 `b`가 루트가 아닌 경우에만 삭제 시도
- 체인이 자주 바뀌는 경로: HLD 점프가 O(log N) 이내로 동작하는지
- 별 모양/사슬 모양 편향 트리: 반복형 구현으로 재귀 한계 회피

## 제출 전 점검
- 입출력 버퍼링과 개행 형식 확인
- 64-bit 정수 필요 여부: 본 문제는 합이 최대 간선 수이므로 `int` 충분
- 인덱스 범위: Fenwick는 1-index, `pos`도 1부터 배정
- LCA 처리: 동일 체인 구간은 `pos[lca]+1..pos[u]`로 계산해야 함
- 중복 삭제 방지: `cut[x]` 체크 후만 업데이트

## 참고자료
- Heavy-Light Decomposition 요약: https://cp-algorithms.com/graph/hld.html

