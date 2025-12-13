---
title: "[Algorithm] C++ 백준 13545번: 수열과 쿼리 0"
description: "1과 -1로 이루어진 수열에서 구간 [i,j]마다 합이 0인 최장 연속 부분수열 길이를 구한다. 동일 누적합 쌍의 최대 거리를 구간 내에서 찾는 문제로 환원하고, Mo 알고리즘+좌표압축+deque와 버킷 카운팅으로 최대 길이를 O(1) 가깝게 갱신해 O((N+M)√N)로 해결한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13545
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
- Prefix Sum
- 누적합
- Mo's Algorithm
- 모스 알고리즘
- Offline Query
- 오프라인 쿼리
- Sqrt Decomposition
- 제곱근 분할
- Bucket
- 버킷
- Range Query
- 구간 쿼리
- Coordinate Compression
- 좌표압축
- Deque
- 데크
- Frequency
- 빈도
- Hashing
- 해싱
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Data Structures
- 자료구조
- Array
- 배열
- Zero Sum Subarray
- 합이 0
- Span
- 구간 길이
- Prefix Equality
- 동일 누적합
- Indexing
- 인덱싱
image: "wordcloud.png"
---

## 문제
- **링크**: [백준 13545번 수열과 쿼리 0](https://www.acmicpc.net/problem/13545)
- **요약**: 길이 N의 수열 A(각 원소는 1 또는 -1)와 M개의 구간 [i, j]가 주어질 때, 각 구간 안에서 합이 0인 가장 긴 연속 부분수열의 길이를 구한다.
- **제한**: N, M ≤ 100,000

## 입력/출력
```
입력
6
1 1 1 -1 -1 -1
4
1 3
1 4
1 5
1 6

출력
0
2
4
6
```

## 접근 개요
- 핵심 관찰: 누적합 S[k] = A[1]+…+A[k]라 하면, 부분합 A[x+1..y] = 0 ⇔ S[x] = S[y].
- 즉, 질의 [i, j]는 누적합 배열의 구간 [i-1, j]에서 같은 값이 등장하는 인덱스쌍의 최대 거리(max(y−x))를 묻는 문제로 환원된다.
- 온라인 최대거리 관리를 위해 각 질의를 Mo 알고리즘으로 오프라인 정렬하고, 현재 창(window) 내에서 값별 인덱스 등장 위치를 deque로 유지한다.
- 각 값의 span(맨뒤−맨앞)을 갱신하며, 길이별 빈도(cntLen)와 버킷을 이용해 최대 span을 O(1) 가깝게 질의한다.

```mermaid
flowchart LR
    A[원배열 A(±1)] --> B[누적합 S]
    B --> C[[쿼리 [i,j] → S에서 [i-1, j]]]
    C --> D{Mo 정렬}
    D --> E[값별 인덱스 deque 유지]
    E --> F[각 값의 span = back - front]
    F --> G[길이별 카운팅/버킷]
    G --> H[최대 span = 정답]
```

## 알고리즘
- 전처리: 누적합 S[0..N] 계산 후 좌표압축.
- 질의 변환: [i, j] → S의 구간 [i-1, j].
- Mo 알고리즘: 구간을 이동하며 아래 연산을 수행한다.
  - 왼쪽/오른쪽에 인덱스 추가/삭제 시, 해당 값의 deque 앞/뒤에 넣거나 빼고, 이전 span과 새로운 span을 길이 카운터에 반영한다.
  - 길이 카운터는 `cntLen[0..N]`와 sqrt 버킷으로 관리하여 현재 최대 길이를 빠르게 찾는다.

## 정당성(스케치)
- S[x] = S[y] ⇔ A[x+1..y]의 합이 0. 따라서 [i-1, j]에서 동일한 누적합 값의 가장 먼 두 위치의 차이가 곧 최장 0-합 부분수열의 길이이다.
- 창 크기가 변할 때마다 각 값의 front/back만이 span을 결정하므로 deque로의 상수 시간 갱신이 가능하다.
- 전 구간의 최대 길이는 길이별 빈도를 통해 상수에 가까운 시간으로 얻을 수 있다.

## 복잡도
- 시간: O((N + M) · √N) 수준 (Mo 이동 총량 × O(1) 갱신/질의)
- 공간: O(N) (좌표압축, 위치 deque, 길이 카운터)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Query {
	int L, R, idx;
	int block;
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int N;
	if (!(cin >> N)) return 0;
	vector<int> A(N + 1);
	for (int i = 1; i <= N; ++i) cin >> A[i];

	// Prefix sums S[0..N]
	vector<int> pref(N + 1, 0);
	for (int i = 1; i <= N; ++i) pref[i] = pref[i - 1] + A[i];

	// Coordinate compression of prefix sums
	vector<int> all = pref;
	sort(all.begin(), all.end());
	all.erase(unique(all.begin(), all.end()), all.end());
	int K = (int)all.size();
	vector<int> idOfIndex(N + 1);
	for (int i = 0; i <= N; ++i) {
		idOfIndex[i] = int(lower_bound(all.begin(), all.end(), pref[i]) - all.begin());
	}

	int M; cin >> M;
	vector<Query> qs(M);
	int blockSize = max(1, int(sqrt(N + 1)));
	for (int qi = 0; qi < M; ++qi) {
		int i, j; cin >> i >> j;
		// Work on prefix indices [i-1, j]
		qs[qi] = {i - 1, j, qi, (i - 1) / blockSize};
	}
	sort(qs.begin(), qs.end(), [&](const Query &a, const Query &b) {
		if (a.block != b.block) return a.block < b.block;
		if (a.block & 1) return a.R > b.R;
		return a.R < b.R;
	});

	// Data structures for Mo
	vector<deque<int>> positions(K); // positions of each compressed prefix value inside current window
	int lenBlock = max(1, int(sqrt(N + 1)));
	vector<int> cntLen(N + 1, 0); // how many values currently have span exactly d
	vector<int> bucket((N + lenBlock) / lenBlock + 2, 0); // number of d in block with cntLen[d] > 0

	auto incLen = [&](int d) {
		if (d < 0) return;
		if (++cntLen[d] == 1) bucket[d / lenBlock]++;
	};
	auto decLen = [&](int d) {
		if (d < 0) return;
		if (--cntLen[d] == 0) bucket[d / lenBlock]--;
	};
	auto spanOf = [&](const deque<int> &dq) -> int {
		if ((int)dq.size() < 2) return 0;
		return dq.back() - dq.front();
	};
	auto getMaxLen = [&]() -> int {
		for (int b = (int)bucket.size() - 1; b >= 0; --b) {
			if (bucket[b] == 0) continue;
			int start = min(N, (b + 1) * lenBlock - 1);
			int base = b * lenBlock;
			for (int d = start; d >= base; --d) {
				if (cntLen[d] > 0) return d;
			}
		}
		return 0;
	};

\tint curL = 0, curR = -1;
	vector<int> ans(M, 0);

	auto addLeft = [&](int idx) {
		int id = idOfIndex[idx];
		int oldSpan = positions[id].empty() ? -1 : spanOf(positions[id]);
		positions[id].push_front(idx);
		int newSpan = spanOf(positions[id]);
		if (oldSpan != -1) decLen(oldSpan);
		incLen(newSpan);
	};
	auto addRight = [&](int idx) {
		int id = idOfIndex[idx];
		int oldSpan = positions[id].empty() ? -1 : spanOf(positions[id]);
		positions[id].push_back(idx);
		int newSpan = spanOf(positions[id]);
		if (oldSpan != -1) decLen(oldSpan);
		incLen(newSpan);
	};
	auto removeLeft = [&](int idx) {
		int id = idOfIndex[idx];
		int oldSpan = spanOf(positions[id]); // must be present
		if (!positions[id].empty() && positions[id].front() == idx) positions[id].pop_front();
		int newSpan = positions[id].empty() ? -1 : spanOf(positions[id]);
		decLen(oldSpan);
		if (newSpan != -1) incLen(newSpan);
	};
	auto removeRight = [&](int idx) {
		int id = idOfIndex[idx];
		int oldSpan = spanOf(positions[id]);
		if (!positions[id].empty() && positions[id].back() == idx) positions[id].pop_back();
		int newSpan = positions[id].empty() ? -1 : spanOf(positions[id]);
		decLen(oldSpan);
		if (newSpan != -1) incLen(newSpan);
	};

	for (const auto &q : qs) {
		while (curL > q.L) addLeft(--curL);
		while (curR < q.R) addRight(++curR);
		while (curL < q.L) removeLeft(curL++);
		while (curR > q.R) removeRight(curR--);
		ans[q.idx] = getMaxLen();
	}

	for (int i = 0; i < M; ++i) {
		cout << ans[i] << '\n';
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- 모든 원소가 1 또는 -1로만 구성된 단조 패턴(모두 1, 모두 -1)
- 최소 구간(길이 1), 동일 인덱스(i=j)
- 정답이 0이 되는 구간(합이 0인 부분수열 없음)
- 전체가 0-합을 이루는 큰 구간
- 동일 누적합 값이 매우 많이 반복되어 span 갱신이 빈번한 경우

## 제출 전 점검
- 입력 범위(N, M ≤ 1e5) 고려해 O((N+M)√N) 내로 설계되었는가
- 누적합 좌표압축 인덱스 범위 확인, deque 비어있는 경우 처리
- 길이 카운터/버킷 인덱스 범위(0..N) 확인
- 입출력 속도 최적화(ios::sync_with_stdio, cin.tie)

## 참고자료
- Mo's Algorithm 개요: 쿼리 오프라인 정렬 및 √ 분할
- 누적합으로 0-합 부분수열 판정: S[x]=S[y] ⇔ A[x+1..y] 합 0

