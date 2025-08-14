---
title: "[Algorithm] cpp 백준 17613번: 점프 - 구간 최대 점프넘버"
description: "KOI 2019 고등부 2번 ‘점프’를 O(log N)으로 해결합니다. 1→2→4… 두 배 점프와 재시작 규칙을 이용해 모든 N을 메르센 구간으로 분해하고, [x,y]의 최댓값은 블록 분할과 재귀적 프리픽스 최대치로 계산합니다. 엣지 케이스와 정당성 근거까지 압축 정리."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17613
- cpp
- C++
- python
- Python
- Greedy
- 그리디
- Bit
- 비트연산
- Binary Decomposition
- 이진분해
- Doubling
- 두배점프
- Mersenne
- 메르센수
- Range Maximum
- 구간최대
- Prefix Maximum
- 프리픽스최대
- Recursion
- 재귀
- Math
- 수학
- Implementation
- 구현
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
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code Review
- 코드리뷰
- Testing
- 테스트
- Invariant
- 불변식
- Binary Search
- 이분탐색
- Number Theory
- 정수론
- KOI
- 한국정보올림피아드
- 2019
- High School
- 고등부
- Interval Query
- 구간질의
- Divide and Conquer
- 분할정복
- Recurrence
- 점화식
- DP-Style
- DP스타일
- Logarithmic
- 로그시간
- Implementation Details
- 구현 디테일
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17613
- 요약: 개구리가 0에서 시작해 오른쪽으로만 점프한다. 점프 길이는 1, 2, 4, …로 두 배씩 커지며, 필요 시 언제든 간격을 1로 재시작할 수 있다. 양의 정수 \(N\)에 도달하는 최소 점프 수를 \(J(N)\)이라 할 때, 구간 \([x,y]\)에서 \(\max J(i)\)를 구한다.
- 제한: \(1\le T\le 2000\), \(1\le x\le y\le 10^9\), 시간 1초, 메모리 512 MB

## 입력/출력
```text
입력
3
1 4
7 7
12 16

출력
3
3
7
```

## 접근 개요
- 핵심 관찰: 합 \(1+2+\cdots+2^{k-1}=2^k-1\)인 메르센 구간 \(B_k=[2^k-1,\ 2^{k+1}-2]\) 내 모든 수 \(n\)에 대해 \(J(n)=k+J(n-(2^k-1))\). 즉, 첫 블록의 기여가 항상 \(k\)로 ‘고정’된다.
- 따라서 임의의 \(n\)에 대한 \(J(n)\)은 \(n\)을 반복적으로 가장 큰 메르센 합으로 ‘탑다운 분해’하는 탐욕으로 계산 가능. 이 값의 구간 최댓값은 블록 경계 기준으로 좌·중(완전 블록)·우 세 부분으로 쪼개면 된다.
- 프리픽스 최대치 \(F(y)=\max_{0\le i\le y}J(i)\)를 정의하면, \(y\in B_k\)일 때 \(F(y)=\max\{\operatorname{blockMax}(k-1),\ k+F(y-(2^k-1))\}\)로 귀납 가능.

```mermaid
flowchart TD
  A[구간 [x,y]] --> B{같은 블록?}
  B -- 예 --> C[k + R(x-start, y-start)]
  B -- 아니오 --> D[왼쪽 부분: k + R(x-start, 2^k-1)]
  D --> E[중간 완전 블록: blockMax(ky-1)]
  E --> F[오른쪽 부분: ky + F(y-startY)]
  C --> G[세 후보 중 최댓값]
  F --> G
```

## 알고리즘
1. 유틸리티
   - \(\lfloor\log_2(n)\rfloor\) 계산과 블록 시점 \(start_k=2^k-1\) 산출.
   - 단일 값 \(J(n)\): 가장 큰 \(k=\lfloor\log_2(n+1)\rfloor\)를 뽑아 \(n\leftarrow n-(2^k-1),\ res\leftarrow res+k\)를 반복.
2. 프리픽스 최대치 \(F(y)\)
   - \(y\in B_k\)라면 \(F(y)=\max\{\operatorname{blockMax}(k-1),\ k+F(y-start_k)\}\)
   - 여기서 \(\operatorname{blockMax}(k)=\max_{i\in B_k}J(i)=1+\frac{k(k+1)}{2}\)
3. 구간 최대치 \(R(x,y)\)
   - 같은 블록이면 \(R(x,y)=k+R(x-start_k,\ y-start_k)\)
   - 아니라면 세 후보의 최댓값을 취함
     - 왼쪽 부분: \(k+R(x-start_k,\ 2^k-1)\)
     - 중간 완전 블록이 존재하면 \(\operatorname{blockMax}(ky-1)\)
     - 오른쪽 부분: \(ky+F(y-start_{ky})\)

## 정당성 스케치
- 탐욕 분해의 최적성: 재시작이 자유로우므로, 첫 번째로 선택 가능한 최대 블록 합 \(2^k-1\)을 먼저 쓰는 것이 그 이후 선택의 표현력을 감소시키지 않는다. 각 단계에서 남은 문제는 동일 구조의 부분문제로 축소된다.
- 블록 단조성: \(\operatorname{blockMax}(k)\)가 \(k\)에 대해 증가하므로, 중간 완전 블록의 최댓값은 가장 큰 블록에서 달성된다.

## 복잡도
- 쿼리당 시간: \(O(\log y)\) / 메모리: \(O(1)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using u64 = unsigned long long;
using i64 = long long;

static inline int floorLog2(u64 x) {
	return 63 - __builtin_clzll(x);
}

static inline i64 blockMax(int k) {
	if (k == 0) return 0; // block [0,0] -> J(0)=0
	return 1LL + 1LL * k * (k + 1) / 2; // full block B_k = [2^k-1, 2^{k+1}-2]
}

static i64 Jvalue(u64 n) {
	i64 res = 0;
	while (n > 0) {
		int k = floorLog2(n + 1);
		res += k;
		n -= ((1ULL << k) - 1);
	}
	return res;
}

static i64 prefixMax(u64 y); // forward

static i64 rangeMax(u64 x, u64 y); // forward

static i64 prefixMax(u64 y) {
	if (y == 0) return 0;
	int ky = floorLog2(y + 1);
	u64 startKy = (1ULL << ky) - 1;
	i64 A = (ky >= 2) ? (1LL + 1LL * (ky - 1) * ky / 2) : 0; // max over full blocks B_0..B_{ky-1}
	i64 B = ky + prefixMax(y - startKy);                     // partial of B_ky
	return max(A, B);
}

static i64 rangeMax(u64 x, u64 y) {
	if (x == 0) return prefixMax(y);
	if (x == y) return Jvalue(x);

	int kx = floorLog2(x + 1);
	u64 startX = (1ULL << kx) - 1;
	u64 endX = (1ULL << (kx + 1)) - 2;

	if (y <= endX) {
		// same block
		return kx + rangeMax(x - startX, y - startX);
	}

	// split: left partial, middle full blocks, right partial
	i64 leftCandidate = kx + rangeMax(x - startX, (1ULL << kx) - 1);

	int ky = floorLog2(y + 1);
	i64 middleCandidate = (ky >= kx + 2) ? blockMax(ky - 1) : (i64)-4e18;

	u64 startY = (1ULL << ky) - 1;
	i64 rightCandidate = ky + prefixMax(y - startY);

	return max(leftCandidate, max(middleCandidate, rightCandidate));
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T;
	if (!(cin >> T)) return 0;
	while (T--) {
		u64 x, y;
		cin >> x >> y;
		cout << rangeMax(x, y) << '\n';
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- \(x=y\) 단일 원소 구간
- 같은 블록 내부 구간과 여러 블록을 가로지르는 구간
- \(x=1\), \(y=2^k-2\)처럼 블록 경계 직전/직후
- \(y=10^9\) 상한, 시프트/오버플로 점검
- 작은 값 검증: \(J(1)=1, J(3)=2, J(7)=3, J(15)=4, J(16)=5, J(19)=7\)

## 제출 전 점검
- 입출력 형식/개행, 64-bit 정수 사용 여부, 경계 처리(\(y\)가 블록 끝/시작)
- \(\operatorname{blockMax}(k)\) 및 프리픽스 재귀의 기저 조건 확인

## 참고자료
- 문제: https://www.acmicpc.net/problem/17613
- 출처: KOI 2019 고등부 2번


