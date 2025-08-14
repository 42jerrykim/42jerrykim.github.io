---
title: "[Algorithm] cpp 백준 2419번: 사수아탕 - 구간 DP"
description: "시간당 1씩 감소하는 사탕 바구니를 0에서 출발해 최대 섭취량을 구한다. 위치 정렬 후 0을 포함한 구간을 좌우로 확장하는 O(n^3) 구간 DP로 도착시간 합을 최소화해 K*m−Σt를 극대화한다."
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
- Problem-2419
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
- Interval DP
- 구간 DP
- Two Pointers
- 투포인터
- Greedy
- 그리디
- Graph
- 그래프
- Tree
- 트리
- BFS
- DFS
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Binary Search
- 이분탐색
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
- Modulo
- 모듈러
- Weighted Distance
- 가중 이동거리
- Left-Right DP
- 좌우 포인터 DP
- BOI 2009
- 사수아탕
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/2419
- 요약: x축의 정수 좌표에 n개의 사탕 바구니가 있고 각 바구니에는 처음에 m개의 사탕이 있다. 수아는 0에서 시작하며, 이동 속도는 1, 먹는 시간은 0이다. 시간은 거리만큼 흐르고, 모든 바구니의 사탕은 시간당 1씩 줄어든다. 방문 순서를 적절히 정해 먹을 수 있는 사탕의 최대 개수를 구한다.

### 제한/스펙
- 0 ≤ n ≤ 300, 1 ≤ m ≤ 1,000,000
- 위치 xᵢ는 −10,000 ≤ xᵢ ≤ 10,000, 모두 서로 다름
- 시작 위치는 0 (바구니 위치에 0이 포함될 수도 있음)

## 입력/출력
```
<입력 형식>
n m
x₁
x₂
...
xₙ
```
```
<출력 형식>
최대로 먹을 수 있는 사탕의 개수
```

예시
```
입력
3 15
6
-3
1

출력
25
```

## 접근 개요
- 핵심 관찰: 어떤 K개의 바구니를 방문한다고 하면, 먹는 총 사탕은 K*m − (각 방문의 도착시간 합). 따라서 도착시간 합을 최소화하는 경로를 찾고, K에 대해 최대값을 취하면 된다.
- 모델링: 좌표 0을 포함해 위치들을 정렬하고, 구간 [L..R]로 확장해 가는 "양끝 포인터" 형태의 구간 DP를 사용한다. 길이 len=R−L에서 다음 확장 한 번은 가중치 (K−len)을 가지며, 이동 거리와 곱해 누적 비용에 더한다.
- 결과적으로 K에 대해 최소 도착시간 합을 구한 뒤, K*m − 최소합의 최대를 답으로 삼는다. n ≤ 300에서 O(n³) DP로 충분히 통과한다.

```mermaid
flowchart LR
    A[시작: idx=0 포함 정렬] --> B{구간 [L..R], 위치 L/R 중 한쪽에 있음}
    B -->|왼 확장 (L-1)| C[비용 += (K-len)*dist(L-1)]
    B -->|오 확장 (R+1)| D[비용 += (K-len)*dist(R+1)]
    C --> E{len==K?}
    D --> E
    E -->|예| F[최소 비용 갱신]
    E -->|아니오| B
```

## 알고리즘 설계
- 정의: `dpLeft[L][R]` = 현재 L에 있을 때 [L..R]을 수집 완료한 상태까지의 가중 이동 비용 최소값, `dpRight[L][R]`는 현재 R에 있을 때.
- 전이: 길이 `len = R-L`에서 다음 확장 비용의 계수는 `w = K - len`.
  - L에서 왼쪽으로: `dpLeft[L-1][R] = min(dpLeft[L-1][R], dpLeft[L][R] + w * (pos[L] - pos[L-1]))`
  - L에서 오른쪽으로: `dpRight[L][R+1] = min(dpRight[L][R+1], dpLeft[L][R] + w * (pos[R+1] - pos[L]))`
  - R에서 왼쪽으로: `dpLeft[L-1][R] = min(dpLeft[L-1][R], dpRight[L][R] + w * (pos[R] - pos[L-1]))`
  - R에서 오른쪽으로: `dpRight[L][R+1] = min(dpRight[L][R+1], dpRight[L][R] + w * (pos[R+1] - pos[R]))`
- 초기값: 0을 포함한 정렬 배열에서 `L=R=zeroIdx`에서 시작.
- 종료: 길이 K가 되면 해당 `dpLeft/Right`의 최소값이 K개의 바구니에 대한 도착시간 합의 최솟값. 이를 이용해 `answer = max(answer, K*m - minSum)`.

## 복잡도
- 시간: O(n³)
- 공간: O(n²)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int n;
	long long m;
	if (!(cin >> n >> m)) return 0;

	if (n == 0) {
		cout << 0 << '\n';
		return 0;
	}

	vector<pair<long long, bool>> pts;
	pts.reserve(n + 1);
	pts.push_back({0LL, false});
	for (int i = 0; i < n; ++i) {
		long long x; cin >> x;
		pts.push_back({x, true});
	}

	sort(pts.begin(), pts.end());

	int zero = -1;
	for (int i = 0; i < (int)pts.size(); ++i) {
		if (!pts[i].second) { zero = i; break; }
	}

	vector<long long> pos(pts.size());
	for (int i = 0; i < (int)pts.size(); ++i) pos[i] = pts[i].first;

	const long long INF = (1LL << 62);
	long long best = 0;
	int N = (int)pts.size(); // n + 1

	for (int K = 1; K <= n; ++K) {
		vector<vector<long long>> L(N, vector<long long>(N, INF));
		vector<vector<long long>> R(N, vector<long long>(N, INF));
		L[zero][zero] = 0;
		R[zero][zero] = 0;

		for (int len = 0; len < K; ++len) {
			long long w = K - len;
			int minL = max(0, zero - len);
			int maxL = min(zero, N - 1 - len);
			for (int l = minL; l <= maxL; ++l) {
				int r = l + len;
				long long a = L[l][r];
				long long b = R[l][r];

				if (a < INF) {
					if (l > 0) {
						long long d = pos[l] - pos[l - 1];
						L[l - 1][r] = min(L[l - 1][r], a + w * d);
					}
					if (r + 1 < N) {
						long long d = pos[r + 1] - pos[l];
						R[l][r + 1] = min(R[l][r + 1], a + w * d);
					}
				}
				if (b < INF) {
					if (l > 0) {
						long long d = pos[r] - pos[l - 1];
						L[l - 1][r] = min(L[l - 1][r], b + w * d);
					}
					if (r + 1 < N) {
						long long d = pos[r + 1] - pos[r];
						R[l][r + 1] = min(R[l][r + 1], b + w * d);
					}
				}
			}
		}

		long long bestSum = INF;
		int minL = max(0, zero - K);
		int maxL = min(zero, N - 1 - K);
		for (int l = minL; l <= maxL; ++l) {
			int r = l + K;
			bestSum = min(bestSum, L[l][r]);
			bestSum = min(bestSum, R[l][r]);
		}

		if (bestSum < INF) {
			long long gain = 1LL * K * m - bestSum;
			best = max(best, gain);
		}
	}

	cout << max(0LL, best) << '\n';
	return 0;
}
```

## 코너 케이스 체크리스트
- n=0인 경우 즉시 0 출력
- 모든 바구니가 한쪽(음수/양수)에만 몰린 경우
- 0 위치에 바구니가 있는 경우: 시작 즉시 수거(도착시간 0)
- 매우 큰 m(최대 1e6)과 긴 이동으로 후반 도착시간이 m을 초과할 수 있는 경우: K 선택으로 자동 보정
- 좌표가 −10,000/10,000 경계에 있는 경우 거리 계산 오버플로 없이 처리

## 제출 전 점검
- 입력 형식(한 줄 n m, 이후 n줄 xᵢ) 준수 여부
- 64-bit 정수 사용(거리 가중 합이 커질 수 있음)
- dp의 인덱스 경계(l-1, r+1) 체크
- 정렬 후 0의 위치(zeroIdx) 정확히 탐색

## 참고자료
- BOI 2009 사수아탕(2419) 관련 편집 및 토론
- 구간 DP(Interval DP) 표준 전이 패턴


