---
title: "[Algorithm] C++ 백준 16877번: 핌버"
description: "핌버는 여러 돌 더미에서 한 턴에 한 더미를 골라 피보나치 수 만큼만 제거하는 님 게임 변형입니다. 피보나치 이동 집합으로 각 크기 x의 Grundy 수를 DP로 선계산하고, 모든 더미의 Grundy XOR로 승패를 판별합니다. 시간 O(U·F+N), 메모리 O(U)."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Game Theory
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16877
- cpp
- C++
- Game Theory
- 게임 이론
- Grundy
- Grundy Numbers
- Sprague-Grundy
- 스프라그-그런디
- Impartial Game
- 무정 게임
- Combinatorial Game
- 조합 게임
- Nim
- 님 게임
- Fibonacci
- 피보나치
- Fibonacci Numbers
- 피보나치 수열
- Fibonacci Nim
- 피보나치 님
- Subtraction Game
- 서브트랙션 게임
- Mex
- 멕스
- Bitmask
- 비트마스크
- Mask Optimization
- 마스크 최적화
- DP
- Dynamic Programming
- 동적계획법
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Invariant
- 불변식
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16877
- 요약: N개의 돌 더미가 있고 한 턴에 한 더미에서만 돌을 제거할 수 있으며, 제거 개수는 피보나치 수여야 합니다. 마지막 돌을 가져가는 사람이 승리합니다. 선공은 `koosaga`.

## 입력/출력
- 입력: 첫 줄 N (1 ≤ N ≤ 1e5), 둘째 줄에 각 더미 크기 P_i (1 ≤ P_i ≤ 3e6).
- 출력: 두 사람이 최적으로 플레이할 때 승자를 출력. `koosaga` 또는 `cubelover`.

## 접근 개요
- 이 게임은 각 더미가 같은 이동 집합(Fibonacci)을 공유하는 무정 님 게임입니다. 각 더미를 독립적인 서브게임으로 보고 Sprague–Grundy 정리를 적용합니다.
- 허용 이동 집합 S = {1, 2, 3, 5, 8, ...}. 각 크기 x에 대해 g(x) = mex({ g(x−f) | f ∈ S, f ≤ x }). 최종 승패는 모든 더미의 `xor` 합으로 판별합니다.
- 피보나치 수 개수는 U=3e6에서도 약 33개 수준이라, `usedMask` 비트마스크를 이용해 mex를 O(1)로 구해 전체를 O(U·|S|)에 선계산할 수 있습니다.

```mermaid
flowchart TD
    A[입력 N, P_i] --> B[피보나치 수열 S 생성 (≤ max P_i)]
    B --> C[for x=1..U: usedMask |= 1<<g(x-f) (f∈S, f≤x)]
    C --> D[mex(~usedMask)로 g(x) 계산]
    D --> E[ansXor ^= g(P_i) (모든 더미)]
    E --> F{ansXor == 0?}
    F -- 예 --> G[cubelover]
    F -- 아니오 --> H[koosaga]
```

## 알고리즘 설계
- 이동 집합: 피보나치 수열을 1, 2부터 시작해 U(=max P_i) 이하까지 생성
- Grundy DP: `g[0]=0`, `g[x]=mex({g[x-f]})`; `usedMask`로 방문한 Grundy를 표시, `__builtin_ctzll(~mask)`로 mex
- 승자 판별: `xor_{i=1..N} g[P_i] == 0` 이면 후공 승, 아니면 선공 승
- 올바름 근거: Sprague–Grundy 정리에 의해 무정 게임 합의 Grundy는 서브게임 Grundy의 XOR이며, 0이면 후공이 최적 대응으로 0 상태를 유지할 수 있습니다. `g` 정의는 귀납적으로 유일합니다.

## 복잡도
- 시간: O(U·|S| + N) ≈ O(3e6 · 33 + N)
- 공간: O(U) 바이트(Grundy를 1바이트로 보관 가능), 추가로 피보나치 목록 O(|S|)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N;
	if (!(cin >> N)) return 0;
	vector<int> piles(N);
	int maxP = 0;
	for (int i = 0; i < N; ++i) {
		cin >> piles[i];
		if (piles[i] > maxP) maxP = piles[i];
	}

	// Generate Fibonacci numbers: 1, 2, 3, 5, ...
	vector<int> fib;
	fib.reserve(50);
	fib.push_back(1);
	fib.push_back(2);
	while (true) {
		long long nxt = (long long)fib[fib.size() - 1] + fib[fib.size() - 2];
		if (nxt > maxP) break;
		fib.push_back((int)nxt);
	}

	// Sprague-Grundy for subtraction game with moves in 'fib'
	vector<unsigned char> grundy(maxP + 1, 0);
	for (int x = 1; x <= maxP; ++x) {
		unsigned long long usedMask = 0ULL;
		for (int f : fib) {
			if (f > x) break;
			usedMask |= (1ULL << grundy[x - f]);
		}
		grundy[x] = (unsigned char)__builtin_ctzll(~usedMask);
	}

	int xo = 0;
	for (int p : piles) xo ^= grundy[p];
	cout << (xo ? "koosaga" : "cubelover") << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- N=1, P_1가 작은 값(1, 2, 3) 또는 피보나치 바로 다음 수인 경우
- 모든 더미가 같은 값이거나 매우 큰 값(최대 3e6)인 경우의 성능
- 다수의 더미가 1 또는 2 같은 작은 값으로 치우친 입력
- 입력 합이 크더라도 `U=max P_i`만큼만 DP를 수행하는지 확인

## 제출 전 점검
- 입출력 버퍼링(`sync_with_stdio(false)`, `tie(nullptr)`) 적용
- `usedMask`는 64비트로 충분(이동 수 ≤ 약 33 → mex ≤ 33)
- `grundy`를 `unsigned char`로 저장해 메모리 절약
- 오버플로: 피보나치 생성 시 64비트 임시 사용 후 `int`로 캐스팅

## 참고자료
- Sprague–Grundy 정리 개요: 위키백과, CP 관련 교재
- Fibonacci nim / subtraction games 관련 노트: The On-Line Encyclopedia of Integer Sequences, Competitive Programming 블로그 자료


