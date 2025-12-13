---
title: "[Algorithm] C++ 백준 17526번: Star Trek"
description: "선형 행성 경로에서 환승 준비시간과 선박 속도를 고려해 1→n 최소 이동 시간을 구한다. dp[j]=min(dp[i]+p_i+s_i·(D[j]-D[i]))를 직선 최소 질의로 바꾸고 Li Chao Tree로 O(n log X)로 최적화한 정답과 증명·엣지케이스를 정리."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Dynamic Programming
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17526
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
- Dynamic Programming
- 동적계획법
- DP Optimization
- DP 최적화
- Convex Hull Trick
- 컨벡스 헐 트릭
- Li Chao Tree
- 라이차오 트리
- Line Container
- 라인 컨테이너
- Minimum Query
- 최소 질의
- Distance Prefix
- 누적거리
- Prefix Sum
- 접두사 합
- Math
- 수학
- Geometry
- 기하
- Binary Search
- 이분탐색
- Graph
- 그래프
- String
- 문자열
- Hashing
- 해싱
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Disjoint Set Union
- 유니온파인드
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17526
- 요약: 1번부터 n번까지 일렬로 이어진 행성 사이를 이동한다. 각 행성 i에는 환승 준비시간 `p_i`와 속도(페이스) `s_i`인 우주선이 있다. 한 번 탑승하면 중간 정차 없이 직진할 수 있고, 다른 행성에서 갈아타면 준비시간이 추가된다. 1번에서 n번까지 도달하는 최소 시간을 구하라.
- 제한: 3 ≤ n ≤ 100000, 거리 1..1000, 0 ≤ p_i ≤ 1e9, 1 ≤ s_i ≤ 1e5, 시간 1초, 메모리 512MB

## 입력/출력
- 입력: 첫 줄 `n`. 둘째 줄 `n-1`개의 인접 거리. 이후 `n-1`줄에 각 `p_i s_i`.
- 출력: 1에서 n까지 최소 소요 시간 정수값 1줄.

예제 1 입력
```
5
5 10 4 8
3 6
8 3
4 8
15 4
```
예제 1 출력
```
107
```

예제 2 입력
```
4
10 10 10
0 5
10 3
5 2
```
예제 2 출력
```
115
```

## 접근 개요
- 핵심 아이디어: 1→n 최소 시간을 다음 DP로 모델링한다.
  - `D[i]`: 1에서 i까지 누적 거리, `D[1]=0`.
  - `dp[j] = min_{1 ≤ i < j} ( dp[i] + p_i + s_i * (D[j] - D[i]) )`.
- 정리: `dp[j] = min_i ( (s_i) * D[j] + (dp[i] + p_i - s_i * D[i]) )` → `x=D[j]`에서의 다수 직선의 최소값 질의.
- 자료구조: 직선 추가와 점 최소 질의를 지원하는 Li Chao Tree로 `O(n log X)`에 해결. 여기서 `X = max D[i] = sum(dist)` ≤ 1e8.

## 알고리즘 설계
- 상태 정의: `dp[j]`는 j행성까지의 최소 시간.
- 전이: 위 식을 사용. 각 i(<j)로부터 기울기 `m=s_i`, 절편 `b=dp[i]+p_i - s_i*D[i]`인 직선을 추가하고, `x=D[j]`에서 최소값을 질의한다.
- 초기화: `dp[1]=0`이며, i=1의 직선 `y=s_1*x + (p_1 - s_1*D[1]) = s_1*x + p_1`을 먼저 추가.
- 구현 포인트:
  - 좌표 범위: `x ∈ [0, sum(dist)]`를 정수로 다룸. `long long` 사용.
  - Li Chao Tree는 동적 노드로 구성하여 메모리 절약. 동일 `x`에서 더 작은 값을 유지.
  - j=n인 마지막 노드는 직선 추가가 불필요.

### 올바름 근거(스케치)
- 각 선택은 “i에서 j로 직행 + i에서의 준비시간”이므로 모든 계획은 연속 구간들의 합으로 표현된다.
- 전이식은 모든 i(<j)에 대한 비용을 정확히 열거하며, 누적거리를 통해 선형항 `s_i*D[j]`로 분리된다.
- Li Chao Tree는 주어진 점 `D[j]`에서 후보 직선들의 최소값을 올바르게 계산하므로 DP의 최솟값과 일치한다.

### 의사코드
```
read n
read d[1..n-1]
D[1]=0; for j=2..n: D[j]=D[j-1]+d[j-1]
for i=1..n-1: read p[i], s[i]
add_line(m=s[1], b=p[1])
for j=2..n:
  dp[j] = query(D[j])
  if j<=n-1: add_line(m=s[j], b=dp[j] + p[j] - s[j]*D[j])
print dp[n]
```

### Mermaid 흐름
```mermaid
graph TD
A[누적거리 D 계산] --> B[Li Chao 초기화]
B --> C{i=1 직선 추가}
C --> D[for j=2..n]
D --> E[dp[j] = query(D[j])]
E --> F{j<=n-1?}
F -- yes --> G[직선 추가: m=s[j], b=dp[j]+p[j]-s[j]*D[j]] --> D
F -- no --> H[정답 출력 dp[n]]
```

## 복잡도
- 시간: `O(n log X)` (`X=sum(dist)`)  — 각 단계에서 한 번 질의, 최대 한 번 삽입
- 공간: `O(n)`  — 동적 노드 수는 삽입 직선 수에 비례

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Line {
	long long m, b; // y = m*x + b
	long long get(long long x) const { return m * x + b; }
};

struct Node {
	Line ln;
	Node *l, *r;
	Node(const Line& line) : ln(line), l(nullptr), r(nullptr) {}
};

struct LiChao {
	long long X_MIN, X_MAX;
	Node* root;
	LiChao(long long xmin, long long xmax) : X_MIN(xmin), X_MAX(xmax), root(nullptr) {}

	void add_line(Line nw) { insert(root, X_MIN, X_MAX, nw); }

	void insert(Node*& node, long long l, long long r, Line nw) {
		if (!node) { node = new Node(nw); return; }
		long long mid = (l + r) >> 1;
		bool leftBetter = nw.get(l) < node->ln.get(l);
		bool midBetter = nw.get(mid) < node->ln.get(mid);
		if (midBetter) swap(nw, node->ln);
		if (l == r) return;
		if (leftBetter != midBetter) insert(node->l, l, mid, nw);
		else insert(node->r, mid + 1, r, nw);
	}

	long long query(long long x) const { return query(root, X_MIN, X_MAX, x); }

	long long query(Node* node, long long l, long long r, long long x) const {
		if (!node) return LLONG_MAX / 4;
		long long res = node->ln.get(x);
		if (l == r) return res;
		long long mid = (l + r) >> 1;
		if (x <= mid) return min(res, query(node->l, l, mid, x));
		return min(res, query(node->r, mid + 1, r, x));
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int n;
	if (!(cin >> n)) return 0;

	vector<int> d(n - 1);
	long long totalDist = 0;
	for (int i = 0; i < n - 1; ++i) {
		cin >> d[i];
		totalDist += d[i];
	}

	// prefix distance D[i]: distance from planet 1 to planet i
	vector<long long> D(n + 1, 0); // 1-indexed, D[1]=0
	for (int i = 2; i <= n; ++i) D[i] = D[i - 1] + d[i - 2];

	vector<long long> p(n + 1, 0), s(n + 1, 0); // only 1..n-1 used
	for (int i = 1; i <= n - 1; ++i) cin >> p[i] >> s[i];

	vector<long long> dp(n + 1, 0);
	LiChao lichao(0, totalDist);

	// Start: can board at planet 1
	lichao.add_line({s[1], dp[1] + p[1] - s[1] * D[1]});

	for (int j = 2; j <= n; ++j) {
		dp[j] = lichao.query(D[j]);
		if (j <= n - 1) {
			long long b = dp[j] + p[j] - s[j] * D[j];
			lichao.add_line({s[j], b});
		}
	}

	cout << dp[n] << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- `p_i=0` 또는 `s_i=1` 같은 극단값
- 매우 큰 `p_i`로 인한 직선 절편 지배 상황
- `s_i`가 증가/감소/임의 혼합일 때도 동작 (정렬 불필요)
- 거리가 작은 케이스(`d_i=1`)와 큰 케이스 혼재
- `n=3`의 최소 크기, `sum(d)`가 큰 경우(좌표 상한 주의)
- 64-bit 오버플로 방지: 모든 합/곱을 `long long`으로 처리

## 제출 전 점검
- 입력 개행/공백 처리, 1-index/0-index 혼동 여부
- `sum(dist)`로 Li Chao 범위 설정 확인
- `j=n`에서 직선 추가 생략 확인
- 출력 개행 포함

## 참고
- BOJ 17526 Star Trek — Li Chao Tree를 이용한 직선 최소 질의 기반 DP 최적화

