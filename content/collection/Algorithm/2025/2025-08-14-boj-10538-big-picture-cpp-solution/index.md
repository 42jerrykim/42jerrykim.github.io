---
title: "[Algorithm] C++ 백준 10538번: 빅 픽쳐 - 2D 롤링 해시로 O(HW) 매칭"
description: "흑백 격자에서 작은 그림이 걸작 내에 나타나는 모든 위치를 계산합니다. 행/열 분리 2차원 롤링 해시와 이중 해싱으로 충돌을 낮추고 O(HW) 시간에 서브매트릭스 매칭을 수행하여 제한 조건을 안정적으로 만족합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- String
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-10538
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
- String
- 문자열
- Hashing
- 해싱
- Rolling Hash
- 롤링해시
- 2D Hashing
- 2차원 해싱
- Rabin-Karp
- 라빈카프
- Pattern Matching
- 패턴 매칭
- Submatrix
- 서브매트릭스
- Convolution
- 컨볼루션
- FFT
- 고속푸리에변환
- Double Hash
- 이중해싱
- Collision
- 해시충돌
- Sliding Window
- 슬라이딩윈도우
- Grid
- 격자
- Image Processing
- 영상처리
- Geometry
- 기하
- Implementation Details
- 구현 디테일
- Debugging
- 디버깅
- Big Picture
- 빅픽쳐
- Karp-Rabin
- 카프라빈
- Polynomial Hash
- 다항해시
- Modular Arithmetic
- 모듈러연산
- 64-bit
- 64비트
- Overflow
- 오버플로
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/10538
- 요약: `o/x`로 이루어진 작은 그림 `hp×wp`과 큰 걸작 `hm×wm`이 주어질 때, 작은 그림이 정확히 일치하는 시작 위치(좌상단)의 개수를 구합니다.
- 제한: 1 ≤ hp, wp, hm, wm ≤ 2000, 그리고 hm ≥ hp, wm ≥ wp.

## 입력/출력
```
<입력>
hp wp hm wm
hp줄: 사용한 그림
hm줄: 걸작 그림

<출력>
일치하는 위치의 개수
```

예시
```
입력
4 4 10 10
oxxo
xoox
xoox
oxxo
xxxxxxoxxo
oxxoooxoox
xooxxxxoox
xooxxxoxxo
oxxoxxxxxx
ooooxxxxxx
xxxoxxoxxo
oooxooxoox
oooxooxoox
xxxoxxoxxo

출력
4
```

## 접근 개요
- **핵심 아이디어**: 2차원 롤링 해시(행→열 두 단계)로 모든 `hp×wp` 서브매트릭스의 해시를 O(1)씩 갱신하며 비교합니다. 충돌은 서로 다른 두 쌍의 64-bit 기반 베이스를 사용한 이중 해시로 확률을 충분히 낮춥니다.
- **매핑**: 문자 `'o'`와 `'x'`를 서로 다른 정수 값으로 매핑해 해시를 구성합니다.
- **절차**:
  1) 각 행에서 길이 `wp`의 구간 해시를 슬라이딩으로 계산.
  2) 위 결과를 세로로 길이 `hp`만큼 다시 롤링해 각 좌상단 `(i,j)`의 2D 해시를 얻음.
  3) 패턴의 2D 해시와 이중 비교하여 일치 횟수 누적.

## 알고리즘 설계
- **행 해시(가로 롤링)**: 베이스 `Bcol`에 대해 `rowHash[i][j] = hash(M[i][j..j+wp-1])`를 전처리. 다음 열로 이동 시 맨 왼쪽 원소 제거·오른쪽 원소 추가로 O(1) 갱신.
- **열 해시(세로 롤링)**: 각 열 창 `j`마다 `v[i] = hash(rowHash[i..i+hp-1][j])`를 O(1)로 갱신.
- **패턴 해시**: 동일한 방식으로 패턴 `P`의 2D 해시 `pat` 계산.
- **이중 해시**: `(BASE_ROW_A, BASE_COL_A)`와 `(BASE_ROW_B, BASE_COL_B)` 두 체계로 각각 계산하여 충돌 확률을 낮춤.
- **값 매핑**: `'o'→1`, `'x'→2` 같은 간단·비충돌 매핑.

### 정당성(스케치)
- 2D 다항 해시는 각 원소의 위치에 따른 가중 합으로 정의되어 전이 시 이전 상태에서 일관성 있게 갱신됩니다.
- 동일 위치의 동일한 문자가 전 구간에 일치할 때만 두 해시가 동시에 일치할 확률이 높으며, 서로 독립적인 두 해시를 사용하면 충돌 확률은 실사용에서 무시 가능 수준으로 떨어집니다.

## 복잡도
- 시간: O(hm × wm)
- 공간: O(hm × (wm − wp + 1)) (행 해시 보관), 추가적으로 상수 크기 보조 배열

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using u64 = unsigned long long;

static inline u64 cellValue(char ch) {
	return ch == 'o' ? 1ULL : 2ULL; // 'o'와 'x'를 서로 다른 값으로 매핑
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int hp, wp, hm, wm;
	if (!(cin >> hp >> wp >> hm >> wm)) return 0;

	vector<string> P(hp), M(hm);
	for (int i = 0; i < hp; ++i) cin >> P[i];
	for (int i = 0; i < hm; ++i) cin >> M[i];

	// 2D Rolling Hash with double 64-bit bases (wrap-around modulo 2^64)
	const u64 BASE_COL_A = 146527ULL;
	const u64 BASE_ROW_A = 19260817ULL;
	const u64 BASE_COL_B = 911382323ULL;
	const u64 BASE_ROW_B = 972663749ULL;

	// Precompute powers
	vector<u64> powColA(wm + 1, 1), powRowA(hm + 1, 1);
	vector<u64> powColB(wm + 1, 1), powRowB(hm + 1, 1);
	for (int i = 1; i <= wm; ++i) {
		powColA[i] = powColA[i - 1] * BASE_COL_A;
		powColB[i] = powColB[i - 1] * BASE_COL_B;
	}
	for (int i = 1; i <= hm; ++i) {
		powRowA[i] = powRowA[i - 1] * BASE_ROW_A;
		powRowB[i] = powRowB[i - 1] * BASE_ROW_B;
	}

	// Pattern hash
	u64 patRowA, patRowB;
	vector<u64> patRowsA(hp), patRowsB(hp);
	for (int r = 0; r < hp; ++r) {
		u64 hA = 0, hB = 0;
		for (int c = 0; c < wp; ++c) {
			u64 v = cellValue(P[r][c]);
			hA = hA * BASE_COL_A + v;
			hB = hB * BASE_COL_B + v;
		}
		patRowsA[r] = hA;
		patRowsB[r] = hB;
	}
	u64 patA = 0, patB = 0;
	for (int r = 0; r < hp; ++r) {
		patA = patA * BASE_ROW_A + patRowsA[r];
		patB = patB * BASE_ROW_B + patRowsB[r];
	}

	// Row-wise rolling hashes for the masterpiece (width = wp)
	const int W = wm - wp + 1;
	const int H = hm - hp + 1;
	vector<vector<u64>> rowA(hm, vector<u64>(max(0, W)));
	vector<vector<u64>> rowB(hm, vector<u64>(max(0, W)));

	if (W <= 0 || H <= 0) {
		cout << 0 << '\n';
		return 0;
	}

	for (int i = 0; i < hm; ++i) {
		u64 hA = 0, hB = 0;
		for (int c = 0; c < wp; ++c) {
			u64 v = cellValue(M[i][c]);
			hA = hA * BASE_COL_A + v;
			hB = hB * BASE_COL_B + v;
		}
		rowA[i][0] = hA;
		rowB[i][0] = hB;
		for (int j = 1; j < W; ++j) {
			u64 vOut = cellValue(M[i][j - 1]);
			u64 vIn = cellValue(M[i][j + wp - 1]);
			hA = hA * BASE_COL_A + vIn - powColA[wp] * vOut;
			hB = hB * BASE_COL_B + vIn - powColB[wp] * vOut;
			rowA[i][j] = hA;
			rowB[i][j] = hB;
		}
	}

	// Vertical rolling for each column window
	long long answer = 0;
	for (int j = 0; j < W; ++j) {
		u64 vA = 0, vB = 0;
		for (int i = 0; i < hp; ++i) {
			vA = vA * BASE_ROW_A + rowA[i][j];
			vB = vB * BASE_ROW_B + rowB[i][j];
		}
		if (vA == patA && vB == patB) ++answer;
		for (int i = 1; i < H; ++i) {
			u64 outA = rowA[i - 1][j], inA = rowA[i + hp - 1][j];
			u64 outB = rowB[i - 1][j], inB = rowB[i + hp - 1][j];
			vA = vA * BASE_ROW_A + inA - powRowA[hp] * outA;
			vB = vB * BASE_ROW_B + inB - powRowB[hp] * outB;
			if (vA == patA && vB == patB) ++answer;
		}
	}

	cout << answer << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- `hp=1` 또는 `wp=1`의 1차원 특수형
- `hp=hm`, `wp=wm`로 전체 일치/불일치
- 전부 `'o'` 또는 전부 `'x'`인 균일 패턴/그림
- 반복 패턴이 많은 경우(해시 갱신이 빈번하지만 충돌은 낮음)
- 입력 최대 크기(2000×2000)에서 시간/메모리 한도 확인

## 제출 전 점검
- 입력 파싱 개행 처리, 빠른 입출력 사용 여부
- 64-bit 정수 곱셈 오버플로 특성(2^64 wrap) 고려했는지
- 베이스·거듭제곱 길이와 인덱스 경계 확인
- 패턴/그림의 크기가 같은 극단 케이스에서 정상 동작 확인
- 출력 마지막 개행 포함

## 참고자료
- 2D Rabin–Karp 및 롤링 해시 기법 개요

