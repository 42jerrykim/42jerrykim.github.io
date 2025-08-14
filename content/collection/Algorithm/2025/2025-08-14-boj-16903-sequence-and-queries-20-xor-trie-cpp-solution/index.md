---
title: "[Algorithm] cpp 백준 16903번: 수열과 쿼리 20 - XOR 트라이"
description: "배열 A(초기에 0 포함)에 대해 삽입·삭제·최대 XOR 질의를 처리합니다. 비트 기반 이진 트라이에 카운트를 유지해 중복과 삭제를 안전히 지원하고, 쿼리 시 각 비트에서 상반된 가지를 우선 선택해 최댓값을 구성합니다. 각 연산은 O(30)로 1초, 512MB 제한에 안전합니다."
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
- Problem-16903
- cpp
- C++
- Data Structures
- 자료구조
- Trie
- 트라이
- Binary Trie
- 이진 트라이
- Bitwise
- 비트연산
- XOR
- 최대 XOR
- Max XOR
- Bit Tricks
- 비트 테크닉
- Greedy
- 그리디
- Online Queries
- 온라인 쿼리
- Query Processing
- 쿼리 처리
- Insertion
- 삽입
- Deletion
- 삭제
- Duplicate
- 중복
- Multiset
- 멀티셋
- Counts
- 카운트
- Frequency
- 빈도
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
- Testing
- 테스트
- Optimization
- 최적화
- Fast IO
- 빠른 입출력
- Performance
- 성능
- Baekjoon
- 수열과 쿼리
- 수열과쿼리20
- Sequence and Queries
- Sequence and Queries 20
- Array
- 배열
- Logarithmic
- 로그
- C++17
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16903
- 요약: 배열 A(초기에 0 포함)에 대해 다음 연산을 처리합니다.
  - `1 x`: A에 x 추가
  - `2 x`: A에서 x 1개 제거(항상 존재 보장)
  - `3 x`: A의 모든 원소와 x의 XOR 중 최댓값 출력
- 제한: M ≤ 200,000, x ≤ 10^9, 1초, 512MB, 3번 쿼리는 최소 1개 존재

## 입력/출력
예제 입력 1
```
10
1 8
1 9
1 11
1 6
1 1
3 3
2 8
3 3
3 8
3 11
```
예제 출력 1
```
11
10
14
13
```

## 접근 개요
- 핵심: 비트 길이 30(0..29) 기준의 이진 트라이를 구성해 각 노드에 "해당 서브트리에 포함된 원소 수(cnt)"를 저장합니다.
- 삽입/삭제: 경로를 따라 cnt를 ±1로 갱신하여 중복과 삭제를 안정적으로 지원합니다.
- 질의(최대 XOR): 상위 비트부터 현재 비트의 반대 가지가 존재하고 cnt>0이면 그쪽을, 아니면 같은 비트를 따라 내려가며 결과 비트를 세웁니다.
- 초기값: A에 0이 존재하므로 시작 시 0을 한 번 삽입해 빈 트라이에서의 질의도 안전하게 합니다.

## 알고리즘 설계
- 비트 범위: x ≤ 1e9 < 2^30 이므로 최상위 비트는 29.
- 연산 정의
  - Insert(x): 루트부터 29..0 비트를 따라 자식 노드 없으면 생성, 매 노드 cnt++.
  - Erase(x): 동일 경로로 매 노드 cnt--. (입력이 유효하므로 음수 불가)
  - Query(x): 각 비트에서 반대 비트 자식의 cnt>0이면 해당 비트에 1을 더하고 그 자식으로 이동, 아니면 같은 비트로 이동.
- 올바름 근거: XOR을 최대로 하려면 상위 비트부터 가능한 한 서로 다른 비트를 맞추는 탐욕이 전역 최적. cnt로 공집합 경로를 배제해 일관성을 유지합니다.

## 복잡도
- 시간: 각 연산 O(30) ≈ O(1) 상수배.
- 공간: 최대 노드 수 O(30 · 삽입된 고유 값 수) ≤ O(30·M).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct TrieNode {
	int child[2];
	int cnt;
	TrieNode() : child{-1, -1}, cnt(0) {}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int M;
	if (!(cin >> M)) return 0;

	const int MAX_BIT = 29; // since x ≤ 1e9 < 2^30
	vector<TrieNode> trie;
	trie.reserve(31 * (M + 2));
	trie.emplace_back(); // root

	auto insert_number = [&](int x) {
		int cur = 0;
		trie[cur].cnt++;
		for (int b = MAX_BIT; b >= 0; --b) {
			int bit = (x >> b) & 1;
			if (trie[cur].child[bit] == -1) {
				trie[cur].child[bit] = (int)trie.size();
				trie.emplace_back();
			}
			cur = trie[cur].child[bit];
			trie[cur].cnt++;
		}
	};

	auto erase_number = [&](int x) {
		int cur = 0;
		trie[cur].cnt--;
		for (int b = MAX_BIT; b >= 0; --b) {
			int bit = (x >> b) & 1;
			cur = trie[cur].child[bit];
			trie[cur].cnt--;
		}
	};

	auto query_max_xor = [&](int x) -> int {
		int cur = 0, ans = 0;
		for (int b = MAX_BIT; b >= 0; --b) {
			int bit = (x >> b) & 1;
			int want = bit ^ 1;
			int nxt = trie[cur].child[want];
			if (nxt != -1 && trie[nxt].cnt > 0) {
				ans |= (1 << b);
				cur = nxt;
			} else {
				cur = trie[cur].child[bit];
			}
		}
		return ans;
	};

	// Initial array contains 0
	insert_number(0);

	for (int i = 0; i < M; ++i) {
		int t, x;
		cin >> t >> x;
		if (t == 1) insert_number(x);
		else if (t == 2) erase_number(x);
		else cout << query_max_xor(x) << '\n';
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- 초기 A={0} 상태에서 곧바로 `3 x` 질의가 나오는 경우
- 같은 값을 여러 번 삽입/삭제하는 중복 처리와 cnt 정확성
- x=0, x가 매우 큰 값(1e9 근처)에서의 비트 경계(29비트) 처리
- 모든 원소가 동일하거나, 반대로 상위 비트가 다양한 값이 섞인 경우
- 연속된 대량 삭제 후에도 트리 경로 접근이 유효한지(cnt>0 확인으로 보장)

## 제출 전 점검
- 비트 범위는 29..0이 맞는지(x ≤ 1e9)
- 루트 포함 모든 경로에서 cnt 증감 일관성 확인(언더플로 금지)
- 빠른 입출력 설정과 개행 출력 규격 준수

## 참고자료
- 비트 트라이를 이용한 최대 XOR 질의 표준 기법(Competitive Programming 관례)
