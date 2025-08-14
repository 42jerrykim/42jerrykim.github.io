---
title: "[Algorithm] cpp 백준 14897번: 서로 다른 수와 쿼리 1"
description: "배열에서 구간 [l, r]의 서로 다른 값 개수를 빠르게 구하는 문제입니다. r 오름차순 오프라인 처리와 각 값의 마지막 등장 위치만 활성화하는 펜윅 트리 기법으로 쿼리를 O(log N)에 해결하고, 좌표 압축으로 값 범위를 정규화합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Data Structures"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-14897"
- "cpp"
- "C++"
- "Data Structures"
- "자료구조"
- "Fenwick Tree"
- "펜윅트리"
- "Binary Indexed Tree"
- "BIT"
- "Segment Tree"
- "세그먼트 트리"
- "Offline Queries"
- "오프라인 쿼리"
- "Coordinate Compression"
- "좌표 압축"
- "Distinct Count"
- "서로 다른 수 개수"
- "Range Query"
- "구간 질의"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Greedy"
- "그리디"
- "Dynamic Programming"
- "동적계획법"
- "Graph"
- "그래프"
- "Tree"
- "트리"
- "BFS"
- "DFS"
- "Two Pointers"
- "투포인터"
- "Sliding Window"
- "슬라이딩윈도우"
- "Hashing"
- "해싱"
- "String"
- "문자열"
- "Math"
- "수학"
- "Modulo"
- "모듈러"
- "Debugging"
- "디버깅"
- "Distinct in Range"
- "쿼리"
- "수열"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14897
- 요약: 길이 N의 수열에서 Q개의 질의 (l, r)에 대해 부분구간 [l, r] 내 서로 다른 값의 개수를 출력합니다.
- 제한: N ≤ 1,000,000, Q ≤ 1,000,000, 값 ≤ 1,000,000,000, 1-indexed.

## 입력/출력 예시
```
<입력 예시>
10
1 3 2 1 3 1 3 2 1 3
10
8 9
4 7
6 8
4 6
3 7
2 10
3 8
1 10
4 7
1 7

<출력 예시>
2
2
3
2
3
3
3
3
2
3
```

## 접근 개요
- 핵심 관찰: 어떤 값 v가 여러 번 등장하면, 구간 내 서로 다른 개수를 셀 때는 "가장 오른쪽 등장 위치"만 1로 세면 충분합니다.
- 전술: 쿼리를 r 오름차순으로 정렬해 오른쪽 끝을 1→N으로 이동하며, 각 값의 "마지막 등장 위치"만 Fenwick Tree에 1로 표시합니다. 이전 마지막 위치는 0으로 되돌립니다.
- 질의 응답: 특정 시점 r까지의 "활성화된 위치 수"는 BIT의 구간합으로 얻습니다. [l, r]의 답은 sum(r) - sum(l-1).

## 알고리즘 설계
1) 좌표 압축: 값 범위가 1e9까지 크므로, 등장 값만 정렬·중복 제거하여 1..M 범위로 치환합니다.
2) 오프라인 정렬: 모든 질의를 r 오름차순으로 정렬합니다.
3) 선형 스윕 + BIT:
   - 위치 i = 1..N을 순회하며 값 v = a[i]의 직전 마지막 위치 p를 관리합니다.
   - p가 존재하면 BIT.add(p, -1)로 비활성화, i에서 BIT.add(i, +1)로 활성화, lastOcc[v]=i로 갱신합니다.
   - 쿼리 (l, r)은 처리 시점에 ans = BIT.sum(r) - BIT.sum(l-1).
4) 정당성 요약: 각 값은 해당 시점 r에서 가장 오른쪽 한 위치만 1로 유지되므로, [l, r] 내 존재 여부는 그 위치가 l 이상인지로 판정됩니다. 전 구간에 대해 중복 없이 정확히 한 번씩만 카운트됩니다.

## 복잡도
- 시간: O((N + Q) log N) — 각 원소 1회 업데이트, 각 질의 1회 구간합
- 공간: O(N + M) — 수열, 좌표 압축, 마지막 등장 인덱스, Fenwick Tree

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct FastScanner {
	static const int BUFSIZE = 1 << 20;
	int idx, size;
	char buf[BUFSIZE];
	FastScanner() : idx(0), size(0) {}
	inline char read() {
		if (idx >= size) {
			size = (int)fread(buf, 1, BUFSIZE, stdin);
			idx = 0;
			if (size == 0) return 0;
		}
		return buf[idx++];
	}
	template <typename T>
	bool nextInt(T &out) {
		char c = read();
		if (c == 0) return false;
		while (c != '-' && (c < '0' || c > '9')) {
			c = read();
			if (c == 0) return false;
		}
		T sign = 1;
		if (c == '-') {
			sign = -1;
			c = read();
		}
		T num = 0;
		for (; c >= '0' && c <= '9'; c = read()) num = num * 10 + (c - '0');
		out = num * sign;
		return true;
	}
};

struct Fenwick {
	int n;
	vector<int> t;
	Fenwick(int n = 0) : n(n), t(n + 1, 0) {}
	inline void add(int i, int v) { for (; i <= n; i += i & -i) t[i] += v; }
	inline int sum(int i) const { int r = 0; for (; i > 0; i -= i & -i) r += t[i]; return r; }
};

struct Query { int l, r, id; };

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	FastScanner fs;
	int N; if (!fs.nextInt(N)) return 0;
	vector<int> a(N + 1);
	for (int i = 1; i <= N; ++i) fs.nextInt(a[i]);

	int Q; fs.nextInt(Q);
	vector<Query> qs(Q);
	for (int i = 0; i < Q; ++i) { fs.nextInt(qs[i].l); fs.nextInt(qs[i].r); qs[i].id = i; }

	// 좌표 압축
	vector<int> comp(N);
	for (int i = 1; i <= N; ++i) comp[i - 1] = a[i];
	sort(comp.begin(), comp.end());
	comp.erase(unique(comp.begin(), comp.end()), comp.end());
	for (int i = 1; i <= N; ++i) a[i] = int(lower_bound(comp.begin(), comp.end(), a[i]) - comp.begin()) + 1;
	int M = (int)comp.size();

	// r 오름차순 정렬
	sort(qs.begin(), qs.end(), [](const Query &x, const Query &y){ return x.r < y.r; });

	Fenwick bit(N);
	vector<int> lastOcc(M + 2, 0);
	vector<int> ans(Q);

	int curR = 0;
	for (const auto &q : qs) {
		while (curR < q.r) {
			++curR;
			int v = a[curR];
			int prev = lastOcc[v];
			if (prev) bit.add(prev, -1);
			bit.add(curR, +1);
			lastOcc[v] = curR;
		}
		ans[q.id] = bit.sum(q.r) - bit.sum(q.l - 1);
	}

	for (int i = 0; i < Q; ++i) cout << ans[i] << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- N=1, Q=1 같은 최소 입력
- 모든 값이 동일 / 모두 서로 다른 값
- l=r 단일 원소 구간
- 동일한 값이 여러 구간에 걸쳐 반복 등장
- 매우 큰 N, Q에서 입출력 병목: 빠른 입력 구현 필요

## 제출 전 점검
- 1-indexed 인덱싱 일치 여부 (BIT, lastOcc, 질의)
- 좌표 압축 후 값 범위 [1..M] 보장
- 이전 마지막 위치 비활성화(bit.add(prev,-1)) 누락 여부
- 입력 파싱 속도(빠른 I/O)와 출력 개행 확인

## 참고자료
- Fenwick Tree(BIT) 기본 개념: 구간합/점갱신 자료구조
- 오프라인 쿼리 + 마지막 등장 위치 테크닉 (Distinct Values in Range)


