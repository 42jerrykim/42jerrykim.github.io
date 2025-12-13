---
title: "[Algorithm] C++ 백준 4001번: 미노타우르스 미궁"
description: "좌·우수법(Left/Right-hand rule)으로 정의되는 두 개의 표준 경로를 계산하고, 2차원 누적합으로 직사각형 내부 경로/장애물 포함 여부를 O(1)에 판정합니다. 각 좌표별로 ‘막히는 최소 정사각형 크기’와 ‘설치 가능한 최대 정사각형 크기’를 각각 이분 탐색해 교집합이 존재하면 정답 후보로 갱신하여, 가장 작은 변의 길이와 위치를 찾습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-4001
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
- Graph
- 그래프
- Grid
- 격자
- Maze
- 미로
- Wall Follower
- 벽따라가기
- Left-hand Rule
- 좌수법
- Right-hand Rule
- 우수법
- Prefix Sum
- 누적합
- 2D Prefix Sum
- 2차원 누적합
- Binary Search
- 이분탐색
- Rectangle Query
- 직사각형 질의
- Path Blocking
- 경로 차단
- Pathfinding
- 경로 탐색
- Special Judge
- 스페셜 저지
- NEERC
- ICPC
- Minotaur
- 미노타우르스
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 4001 - 미노타우르스 미궁](https://www.acmicpc.net/problem/4001)
- 요약: 빈 칸과 벽으로 이루어진 \(h\times w\) 격자에서, 입구 \((1,1)\)과 둥지 \((w,h)\) 사이 모든 경로를 단 하나의 정사각형 장애물로 차단하고자 합니다. 장애물은 빈 칸만 덮을 수 있으며 입구/둥지는 포함하면 안 됩니다. 가능한 경우, 가장 작은 변 길이와 그 위치를 구합니다.

## 입력/출력
```
<입력>
w h (2 ≤ w, h ≤ 1500)
h개의 줄에 길이 w의 문자열 ('.' 빈 칸, '#' 벽)
입구 (1,1), 둥지 (w,h)는 항상 빈 칸, 경로 존재 보장

<출력>
l x y  (정답 정사각형의 변 길이와 좌상단 좌표)
불가능하면 Impossible
```

## 접근 개요
- 핵심 관찰: 좌·우수법으로 얻는 두 “표준 경로”를 동시에 가로막는 정사각형이 존재하면 모든 경로를 막을 수 있습니다(공식 해설의 핵심 정리).
- 2차원 누적합을 세 종류로 구성합니다: 벽 개수, 좌수법 경로 방문 수, 우수법 경로 방문 수.
- 각 좌표 \((x,y)\)를 정사각형 좌상단으로 고정하고 두 가지를 이분 탐색합니다.
  - 막힘 최소 길이 L_min: 좌·우 경로를 동시에 포함하는 최소 \(l\).
  - 설치 가능 최대 길이 L_max: 빈 칸만 덮고 입구/둥지를 포함하지 않는 최대 \(l\).
- L_min ≤ L_max이면 해당 좌표에서 길이 L_min로 설치 가능. 모든 좌표에 대해 가장 작은 \(l\)을 선택합니다.

## 알고리즘 설계
- 좌수법/우수법 경로 생성: 시작 방향은 동(E)/남(S)으로 두고, 벽 따라가기(wall follower) 규칙으로 입구→둥지까지의 경로를 시뮬레이션합니다.
- 누적합 쿼리: 정사각형 \([y..y+l-1] \times [x..x+l-1])\)에 대해
  - 벽 합이 0 → 전부 빈 칸
  - 좌/우 경로 방문 합이 각각 > 0 → 두 경로 모두 교차
- 좌표별 이분 탐색:
  - blocks(l): 두 경로 방문 누적합이 모두 양수인지 검사(단조 증가)
  - installable(l): 벽 합=0이고 입구/둥지 미포함인지 검사(단조 감소)
  - 최소 \(l\) s.t. blocks(l), 최대 \(l\) s.t. installable(l)을 각각 이분 탐색

## 복잡도
- 경로 시뮬레이션: \(O(wh)\) 내에서 종료(안전 캡 포함)
- 누적합 전처리: \(O(wh)\)
- 좌표별 두 번의 이분 탐색: 총 \(O(wh \cdot \log \min(w,h))\)
- 전체: \(O(wh \cdot \log \min(w,h))\), 메모리 \(O(wh)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Prefix2D {
	int h, w;
	vector<int> a; // (h+1)*(w+1), 1-based prefix
	void init(int H, int W) { h = H; w = W; a.assign((h + 1) * (w + 1), 0); }
	inline int& at(int y, int x) { return a[y * (w + 1) + x]; }
	void build(const vector<vector<int>>& base) {
		for (int y = 1; y <= h; ++y) {
			int row = 0;
			for (int x = 1; x <= w; ++x) {
				row += base[y][x];
				at(y, x) = at(y - 1, x) + row;
			}
		}
	}
	inline int sum(int y1, int x1, int y2, int x2) const {
		if (y1 > y2 || x1 > x2) return 0;
		int W = w + 1;
		auto get = [&](int y, int x) -> int { return a[y * W + x]; };
		return get(y2, x2) - get(y1 - 1, x2) - get(y2, x1 - 1) + get(y1 - 1, x1 - 1);
	}
};

static const int DX[4] = {1, 0, -1, 0};  // E, S, W, N
static const int DY[4] = {0, 1, 0, -1};

vector<vector<int>> buildPathVisited(const vector<string>& g, int H, int W, int dirInit, bool leftHand) {
	vector<vector<int>> vis(H, vector<int>(W, 0));
	auto can = [&](int ny, int nx) -> bool {
		return (0 <= ny && ny < H && 0 <= nx && nx < W && g[ny][nx] == '.');
	};
	int x = 0, y = 0, dir = dirInit;
	vis[y][x] = 1;
	const long long cap = 10LL * H * W + 5;
	for (long long steps = 0; !(x == W - 1 && y == H - 1) && steps < cap; ++steps) {
		// turn towards the hand
		dir = leftHand ? (dir + 3) & 3 : (dir + 1) & 3;
		// rotate opposite way until forward is free
		for (int k = 0; k < 4; ++k) {
			int nx = x + DX[dir], ny = y + DY[dir];
			if (can(ny, nx)) break;
			dir = leftHand ? (dir + 1) & 3 : (dir + 3) & 3;
		}
		x += DX[dir];
		y += DY[dir];
		vis[y][x] = 1;
	}
	return vis;
}

inline bool contains(int topY, int topX, int L, int Y, int X) {
	return (topY <= Y && Y <= topY + L - 1 && topX <= X && X <= topX + L - 1);
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int W, H;
	if (!(cin >> W >> H)) return 0;
	vector<string> g(H);
	for (int i = 0; i < H; ++i) cin >> g[i];

	// Canonical paths
	auto visL = buildPathVisited(g, H, W, 0, true);  // start facing East
	auto visR = buildPathVisited(g, H, W, 1, false); // start facing South

	// Prefix sums
	vector<vector<int>> blk(H + 1, vector<int>(W + 1, 0));
	vector<vector<int>> lp(H + 1, vector<int>(W + 1, 0));
	vector<vector<int>> rp(H + 1, vector<int>(W + 1, 0));
	for (int y = 1; y <= H; ++y) for (int x = 1; x <= W; ++x) {
		blk[y][x] = (g[y - 1][x - 1] == '#');
		lp[y][x] = visL[y - 1][x - 1];
		rp[y][x] = visR[y - 1][x - 1];
	}
	Prefix2D psB, psL, psR; psB.init(H, W); psL.init(H, W); psR.init(H, W);
	psB.build(blk); psL.build(lp); psR.build(rp);

	auto fits = [&](int y, int x, int L) -> bool {
		return (y + L - 1 <= H && x + L - 1 <= W);
	};
	auto installable = [&](int y, int x, int L) -> bool {
		if (!fits(y, x, L)) return false;
		if (contains(y, x, L, 1, 1)) return false;
		if (contains(y, x, L, H, W)) return false;
		return psB.sum(y, x, y + L - 1, x + L - 1) == 0;
	};
	auto blocks = [&](int y, int x, int L) -> bool {
		if (!fits(y, x, L)) return false;
		if (psL.sum(y, x, y + L - 1, x + L - 1) <= 0) return false;
		if (psR.sum(y, x, y + L - 1, x + L - 1) <= 0) return false;
		return true;
	};

	int bestL = INT_MAX, bestX = -1, bestY = -1;
	for (int y = 1; y <= H; ++y) {
		for (int x = 1; x <= W; ++x) {
			if (g[y - 1][x - 1] == '#') continue; // top-left must be empty
			int hiBound = min(H - y + 1, W - x + 1);
			if (hiBound <= 0) continue;

			// 최소로 막는 길이
			int lo = 1, hi = hiBound, LminBlock = -1;
			while (lo <= hi) {
				int mid = (lo + hi) >> 1;
				if (blocks(y, x, mid)) { LminBlock = mid; hi = mid - 1; }
				else lo = mid + 1;
			}
			if (LminBlock < 0) continue;

			// 설치 가능한 최대 길이
			lo = 1; hi = hiBound; int LmaxInstall = 0;
			while (lo <= hi) {
				int mid = (lo + hi) >> 1;
				if (installable(y, x, mid)) { LmaxInstall = mid; lo = mid + 1; }
				else hi = mid - 1;
			}
			if (LminBlock <= LmaxInstall) {
				if (LminBlock < bestL) {
					bestL = LminBlock; bestX = x; bestY = y;
				}
			}
		}
	}

	if (bestL == INT_MAX) cout << "Impossible\n";
	else cout << bestL << ' ' << bestX << ' ' << bestY << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- 입구/둥지 포함 금지: 정사각형이 (1,1) 또는 (w,h)를 덮지 않도록 체크
- 정사각형 내부에 벽 존재 금지: 벽 누적합=0 확인
- 두 표준 경로 동시 차단 필요: 좌·우수법 방문 누적합 모두 양수
- 경계 좌표에서의 최대 길이 상한: `min(H−y+1, W−x+1)`로 제한
- 병목: 전좌표 탐색 × 이분탐색 → 누적합으로 O(1) 판정 유지

## 참고자료
- NEERC 2012 L - Labyrinth of the Minotaur: [DMOJ 문제](https://dmoj.ca/problem/neerc12l), [Editorial](https://dmoj.ca/problem/neerc12l/editorial)
- BOJ 4001 - 문제 페이지: [acmicpc.net/problem/4001](https://www.acmicpc.net/problem/4001)


