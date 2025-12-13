---
title: "[Algorithm] C++ 백준 13546번: 수열과 쿼리 4 - Mo+제곱근분할"
description: "구간 [L,R]에서 같은 값의 두 위치 간 최대 거리(max |x−y|, A[x]=A[y])를 묻는 질의를 Mo 알고리즘으로 처리합니다. 값별 위치 데크와 거리 빈도(√ 분할)를 유지해 추가/제거 O(1)로 갱신하고, 블록 카운팅으로 최대 거리를 즉시 찾습니다. 경계 이동 순서·인덱스 변환·거리 갱신 누락 실수를 방지하는 체크리스트까지 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Sqrt Decomposition
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13546
- cpp
- C++
- Python
- Competitive Programming
- 경쟁프로그래밍
- Mo's Algorithm
- Mo
- Sqrt Decomposition
- 제곱근분할
- Offline Queries
- 오프라인 쿼리
- Range Query
- 구간쿼리
- Range Max Distance
- 최대거리
- Distance Frequency
- 거리빈도
- Block Decomposition
- 블록분할
- Deque
- 데크
- Frequency Array
- 빈도배열
- Occurrence Positions
- 등장위치
- Positions
- 위치관리
- Add Remove
- 추가제거
- Two Pointers
- 투포인터
- Query Reordering
- 쿼리정렬
- Zigzag Order
- 지그재그정렬
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
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Array
- 배열
- Hashing
- 해싱
- Data Structures
- 자료구조
- 0-index
- 1-index
- 경계처리
- sqrt-block
- 블록카운팅
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 13546 - 수열과 쿼리 4](https://www.acmicpc.net/problem/13546)
- 요약: 길이 \(N\)의 수열과 \(M\)개의 질의가 주어질 때, 각 구간 \([L,R]\)에서 값이 같은 두 위치 \(x,y\)의 최대 거리 \(\max |x-y|\)를 구합니다. 값이 한 번만 나오면 그 값의 기여는 0입니다.
- 제한/스펙: \(N, M, K \le 10^5\), 시간 4초, 메모리 512MB. 온라인 자료구조로는 까다롭고, 오프라인 + 제곱근 분할이 적합합니다.

## 입력/출력
```
입력
N K
A1 A2 ... AN   (1 ≤ Ai ≤ K)
M
L1 R1
...
LM RM

출력
각 질의 [Li, Ri]에 대한 최대 거리 값을 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심 관찰: 구간 내 특정 값의 기여는 그 값의 가장 왼쪽/오른쪽 등장 위치 간 차이뿐입니다. 즉, 값별로 "맨 앞"과 "맨 뒤"만 알면 됩니다.
- 전략: Mo 알고리즘으로 구간을 움직이며 값별 등장 위치를 `deque`로 유지합니다. 각 값의 현재 거리(뒤−앞)를 갱신해 전역 최대를 관리합니다.
- 최대값 질의: 거리 값의 빈도 배열 `cntDist[d]`와 이를 √-분할한 블록 카운팅 `cntBlock[b]`를 함께 유지해, 최대 거리를 상위 블록부터 빠르게 찾아냅니다.

```mermaid
flowchart LR
  Q[질의 정렬 (Mo)] --> M{curL,curR}
  M -->|L--| AL[addLeft]
  M -->|--R| AR[addRight]
  M -->|L++| RL[removeLeft]
  M -->|R--| RR[removeRight]
  subgraph 값별 관리
    AL --> DQ1[occ[v].push_front]
    AR --> DQ2[occ[v].push_back]
    RL --> DQ3[occ[v].pop_front]
    RR --> DQ4[occ[v].pop_back]
  end
  DQ1 --> UPD[거리 old→new]
  DQ2 --> UPD
  DQ3 --> UPD
  DQ4 --> UPD
  UPD --> CNT[cntDist, cntBlock 갱신]
  CNT --> ANS[최대 거리 탐색]
```

## 알고리즘 설계
- 유지 구조
  - `occ[v]`: 값 `v`가 현재 구간에 등장하는 모든 인덱스를 오름차순으로 담는 `deque`.
  - `dist(v)`: `occ[v].back() - occ[v].front()` (등장 0~1회면 0).
  - `cntDist[d]`: 거리 `d`를 만드는 값의 개수.
  - `cntBlock[b]`: 거리 구간을 √-분할했을 때 블록 `b` 안에 존재하는 거리의 개수 합.
- 갱신 규칙(add/remove)
  - 값 `v`에 변화가 생기면, 변경 전 거리 `old`를 `cntDist[old]--`, `cntBlock[old/blk]--`로 제거 후, 덱을 조정하고 새 거리 `new`를 `++`합니다. `d<=0`은 생략.
- 답 구하기
  - 상위 블록부터 내려오며 `cntBlock[b]>0`인 첫 블록을 찾고, 그 블록 내부에서 `cntDist[d]>0`인 가장 큰 `d`를 반환.
- 정당성(요지)
  - Mo 순서에서 각 스텝은 좌우 1칸 이동만 수행하며, 각 이동은 특정 값 한 개의 덱 양 끝만 바꾸므로 거리 변경은 O(1)회. 최대값 질의는 블록 개수 \(\approx \sqrt{N}\)만큼 상한이 보장됩니다.

## 복잡도
- 시간: 정렬 \(O(M \log M)\) + 이동·갱신 \(O((N+M)\sqrt{N})\) + 블록 최대 탐색 \(O(\sqrt{N})\) 수준에서 실측 통과.
- 공간: \(O(N + K)\) (`occ`, `cntDist`, 보조 배열).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Query {
	int l, r, idx;
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, K;
	if (!(cin >> N >> K)) return 0;
	vector<int> A(N + 1);
	for (int i = 1; i <= N; ++i) cin >> A[i];

	int M;
	cin >> M;
	vector<Query> qs(M);
	for (int i = 0; i < M; ++i) {
		cin >> qs[i].l >> qs[i].r;
		qs[i].idx = i;
	}

	int blockSize = max(1, (int)sqrt(N));
	sort(qs.begin(), qs.end(), [&](const Query& a, const Query& b) {
		int ab = a.l / blockSize, bb = b.l / blockSize;
		if (ab != bb) return ab < bb;
		if (ab & 1) return a.r > b.r; // 지그재그로 R 이동 최소화
		return a.r < b.r;
	});

	// 값별 현재 구간 내 등장 위치들
	vector<deque<int>> occ(K + 1);

	// 거리 빈도와 √-분할 블록 카운팅
	int distBlock = max(1, (int)sqrt(N) + 1);
	vector<int> cntDist(N + 1, 0);
	vector<int> cntBlock((N / distBlock) + 3, 0);

	auto incDist = [&](int d) {
		if (d <= 0) return;
		++cntDist[d];
		++cntBlock[d / distBlock];
	};
	auto decDist = [&](int d) {
		if (d <= 0) return;
		--cntDist[d];
		--cntBlock[d / distBlock];
	};

	auto distOf = [&](int v) -> int {
		const auto& dq = occ[v];
		if ((int)dq.size() >= 2) return dq.back() - dq.front();
		return 0;
	};

	auto addLeft = [&](int idx) {
		int v = A[idx];
		int oldD = distOf(v);
		if (oldD) decDist(oldD);
		occ[v].push_front(idx);
		int newD = distOf(v);
		if (newD) incDist(newD);
	};
	auto addRight = [&](int idx) {
		int v = A[idx];
		int oldD = distOf(v);
		if (oldD) decDist(oldD);
		occ[v].push_back(idx);
		int newD = distOf(v);
		if (newD) incDist(newD);
	};
	auto removeLeft = [&](int idx) {
		int v = A[idx];
		int oldD = distOf(v);
		if (oldD) decDist(oldD);
		if (!occ[v].empty() && occ[v].front() == idx) occ[v].pop_front();
		int newD = distOf(v);
		if (newD) incDist(newD);
	};
	auto removeRight = [&](int idx) {
		int v = A[idx];
		int oldD = distOf(v);
		if (oldD) decDist(oldD);
		if (!occ[v].empty() && occ[v].back() == idx) occ[v].pop_back();
		int newD = distOf(v);
		if (newD) incDist(newD);
	};

	auto getAnswer = [&]() -> int {
		for (int b = (int)cntBlock.size() - 1; b >= 0; --b) {
			if (cntBlock[b] > 0) {
				int hi = min(N, (b + 1) * distBlock - 1);
				for (int d = hi; d >= b * distBlock; --d) {
					if (cntDist[d] > 0) return d;
				}
			}
		}
		return 0;
	};

	vector<int> ans(M, 0);
	int curL = 1, curR = 0;

	for (const auto& q : qs) {
		while (curL > q.l) addLeft(--curL);
		while (curR < q.r) addRight(++curR);
		while (curL < q.l) removeLeft(curL++);
		while (curR > q.r) removeRight(curR--);
		ans[q.idx] = getAnswer();
	}

	for (int i = 0; i < M; ++i) {
		cout << ans[i] << '\n';
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- `L == R` 단일 원소 구간은 항상 0이어야 함
- 어떤 값이 구간에 1회만 등장하는 경우 거리 0 처리 누락 여부
- 모든 값 동일/모두 상이한 극단 패턴에서 거리 갱신 일관성
- 포인터 이동 순서로 인해 덱 앞/뒤 업데이트가 어긋나지 않는지
- 최대 거리 블록 탐색 시 범위 상한(`hi`) 계산 및 경계 포함 여부

## 제출 전 점검
- 빠른 입출력 사용, 인덱스(1-index 입력 ↔ 내부 사용) 변환 확인
- `dist<=0` 필터링 누락으로 음/영 거리 갱신되는 버그 방지
- 블록 크기(`distBlock`)와 카운팅 배열 크기 산정 체크
- Mo 정렬(블록+지그재그) 구현 일치성 점검, off-by-one

## 참고자료
- cp-algorithms: `Mo's algorithm`
- 관련 블로그: 질의 오프라인 처리와 √-분할 테크닉 정리 문서들


