---
title: "[Algorithm] cpp 백준 15974번: 공룡 발자국"
description: "발뒤꿈치 기준 각도 정렬과 ccw로 기하 제약을 선형화한 뒤, DP(발가락/골 상태 전이)를 슬라이딩 윈도우로 최적화하여 O(N^2 log N)에 최대 발가락 수의 발자국을 찾고, 역추적으로 꼭짓점 좌표를 출력하는 풀이입니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-15974
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
- Dynamic Programming
- 동적계획법
- Sliding Window
- 슬라이딩윈도우
- Geometry
- 기하
- CCW
- 반시계판정
- Angle Sort
- 각도정렬
- Convex Polygon
- 볼록다각형
- Reconstruction
- 역추적
- Special Judge
- 스페셜저지
- KOI
- KOI-2018
- Middle School
- 중등부
- Graph
- 그래프
- Sorting
- 정렬
- Implementation Details
- 구현 디테일
- Debugging
- 디버깅
- Long Long
- 64-bit
- Fast IO
- 빠른 입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/15974
- 요약: `N`개의 점 중 최남단 점이 발뒤꿈치로 고정된다. 발뒤꿈치에서 반시계로 순회할 때, 발가락에서는 좌회전, 골에서는 우회전을 번갈아 하는 2k각형(발뒤꿈치 1 + 발가락 k + 골 k−1)을 만드는 최대 `k`의 발자국을 구성하고 그 꼭짓점을 출력한다. 선분(발뒤꿈치-발가락)은 다각형 내부를 벗어나거나 골을 지나면 안 된다.

## 입력/출력
```
<입력>
N
x1 y1
x2 y2
...
xN yN

<출력>
T                        # 선택된 꼭짓점 수 (발뒤꿈치부터 반시계)
x1 y1
...
xT yT
```

## 접근 개요
- 최남단 점을 발뒤꿈치로 선택하고, 나머지 점을 발뒤꿈치 기준 각도순으로 정렬한다.
- 기하 제약을 `ccw`로 표현하면, 어떤 중간 점 `i`를 기준으로 이전의 후보(`k`)와 이후의 후보(`j`)에 대해 전이 가능 구간이 각도 순서로 단조롭게 이동한다.
- 이 구조를 이용해 DP 전이의 최댓값 갱신을 슬라이딩 윈도우로 처리하면 전체가 `O(N^2 log N)`(정렬 `+` 각 점 기준의 정렬 포함)로 수렴한다.

## 알고리즘 설계
- 상태 정의
  - `dp[0][i][j]`: 마지막이 `j`이고 직전이 `i`이며, `i`가 골인 상태의 최대 선택 수
  - `dp[1][i][j]`: 마지막이 `j`이고 직전이 `i`이며, `j`가 발가락인 상태의 최대 선택 수
- 전이
  - 각 기준점 `i`에 대해, `i` 이전(각도상) 후보 집합 `A`, 이후 후보 집합 `B`를 각각 `i` 기준 각도로 정렬한다.
  - `dp[1][i][j] = max_{k ∈ A, angle(k,i) < angle(j,i)} dp[0][k][i] + 1`을 투 포인터로 처리
  - 반대 방향으로 `dp[0][i][j]`도 동일하게 처리
- 시작/종료
  - 발뒤꿈치(인덱스 0) 고정, 유효한 좌회전 간선(`ccw(heel,i,j)=1`)만 최종 후보로 사용
  - 최대값 위치에서 `prv` 테이블로 역추적해 꼭짓점 순서를 재구성

## 복잡도
- 시간: `O(N^2 log N)` (발뒤꿈치 기준 1회 정렬 + 각 `i`에서의 분할 정렬 + 선형 투 포인터)
- 공간: `O(N^2)` (DP와 이전 인덱스 저장)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
using Point = pair<int64, int64>;

static int dp[2][3030][3030];
static int prvIdx[2][3030][3030];

inline int ccw(const Point& a, const Point& b, const Point& c) {
	int64 v = (b.first - a.first) * (c.second - a.second)
	        - (b.second - a.second) * (c.first - a.first);
	if (v > 0) return 1;
	if (v < 0) return -1;
	return 0;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int n;
	if (!(cin >> n)) return 0;
	vector<Point> pts(n);
	for (int i = 0; i < n; i++) cin >> pts[i].first >> pts[i].second;

	// Find heel: unique lowest y
	int heel = 0;
	for (int i = 1; i < n; i++) {
		if (pts[i].second < pts[heel].second) heel = i;
	}
	swap(pts[0], pts[heel]);

	// Sort by angle around heel (counter-clockwise)
	sort(pts.begin() + 1, pts.end(), [&](const Point& a, const Point& b) {
		return ccw(pts[0], a, b) > 0;
	});

	// DP transitions optimized with angular order + sliding window
	for (int i = 1; i < n - 1; i++) {
		vector<int> a(1), b; // a[0] = 0 (heel) as base
		for (int j = 1; j < i; j++) {
			if (ccw(pts[0], pts[j], pts[i]) != 0) a.push_back(j);
		}
		for (int j = i + 1; j < n; j++) {
			if (ccw(pts[0], pts[i], pts[j]) != 0) b.push_back(j);
		}

		sort(a.begin(), a.end(), [&](int u, int v) {
			return ccw(pts[i], pts[u], pts[v]) > 0;
		});
		sort(b.begin(), b.end(), [&](int u, int v) {
			return ccw(pts[i], pts[u], pts[v]) > 0;
		});

		// dp[1][i][j] from dp[0][k][i] while angle(k,i) < angle(j,i) around i
		int pv = 0, best = 0, bestIdx = 0;
		for (int j : b) {
			while (pv < (int)a.size() && ccw(pts[a[pv]], pts[i], pts[j]) > 0) {
				int k = a[pv++];
				if (best < dp[0][k][i] + 1) {
					best = dp[0][k][i] + 1;
					bestIdx = k;
				}
			}
			dp[1][i][j] = best;
			prvIdx[1][i][j] = bestIdx;
		}

		// Reverse sweep for dp[0][i][j] from dp[1][k][i] with opposite inequality
		pv = 0; best = 0; bestIdx = 0;
		reverse(a.begin(), a.end());
		reverse(b.begin(), b.end());
		for (int j : b) {
			while (pv < (int)a.size() && ccw(pts[a[pv]], pts[i], pts[j]) < 0) {
				int k = a[pv++];
				if (best < dp[1][k][i] + 1) {
					best = dp[1][k][i] + 1;
					bestIdx = k;
				}
			}
			dp[0][i][j] = best;
			prvIdx[0][i][j] = bestIdx;
		}
	}

	// Find best end (x -> y) respecting left turn at i around heel
	int best = 0, x = 0, y = 0;
	for (int i = 1; i < n; i++) {
		for (int j = i + 1; j < n; j++) {
			if (ccw(pts[0], pts[i], pts[j]) != 1) continue;
			if (best < dp[0][i][j]) {
				best = dp[0][i][j];
				x = i; y = j;
			}
		}
	}

	if (best == 0) {
		cout << 0;
		return 0;
	}

	// Reconstruct sequence of vertex indices starting from heel (0)
	vector<int> path;
	path.push_back(y);
	path.push_back(x);
	while (path.back() != 0) {
		int t = (int)path.size();
		int prev = prvIdx[t & 1][path[t - 1]][path[t - 2]];
		path.push_back(prev);
	}
	reverse(path.begin(), path.end());

	cout << (int)path.size() << '\n';
	for (int idx : path) {
		cout << pts[idx].first << ' ' << pts[idx].second << '\n';
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- 모든 점이 일직선(동일 각도)인 경우: `ccw = 0` 처리로 배제됨 → 정답 0 가능
- 가장 남쪽 점이 유일함이 보장되지만, 같은 `y`에서 `x`가 다른 경우 정렬 일관성
- 발뒤꿈치-발가락 선분이 다각형 밖으로 나가는 반례: `ccw` 제약으로 배제되는지 확인
- 최소 입력 `N = 4`와 작은 배치에서의 역추적 경계
- 큰 좌표 절댓값: `long long` 사용으로 오버플로 방지

## 제출 전 점검
- 입출력 버퍼링과 개행 처리 확인
- `ccw` 부호와 좌/우회전 해석 일관성
- `dp/prv` 인덱스 범위, 역추적 종료 조건(`heel=0`) 확인
- 메모리 사용량(`~200MB`)과 제한(512MB) 확인

## 참고자료/유사문제
- KOI 2018 중등부 4번: 공룡 발자국
- 각도 정렬 + 슬라이딩 윈도우 최적화 패턴


