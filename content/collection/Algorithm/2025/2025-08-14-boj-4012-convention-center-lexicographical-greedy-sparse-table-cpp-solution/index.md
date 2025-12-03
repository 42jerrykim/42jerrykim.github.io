---
title: "[Algorithm] C++ 백준 4012번: 컨벤션 센터 - 사전순 최소 해 선택"
description: "회의 구간을 최대 개수로 선택하면서 사전순(lexicographical)으로 가장 이른 해를 출력하는 문제. 시작 시각 기준 정렬, 선행 회의의 이진 점프(sparse table)로 f(l,r)를 O(log n)에 계산하고, 구간 경계 map을 유지해 포함 여부를 O(log n)에 증명·선택한다. 전체 O(n log n)."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Greedy"
- "Interval Scheduling"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-4012"
- "cpp"
- "C++"
- "Greedy"
- "그리디"
- "Interval Scheduling"
- "스케줄링"
- "Scheduling"
- "Lexicographical Order"
- "사전순"
- "Sparse Table"
- "스파스 테이블"
- "Binary Lifting"
- "이진 점프"
- "Map"
- "맵"
- "Set"
- "세트"
- "Sorting"
- "정렬"
- "Two Pointers"
- "투포인터"
- "DP"
- "동적계획법"
- "Proof of Correctness"
- "정당성 증명"
- "Complexity Analysis"
- "복잡도 분석"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Implementation"
- "구현"
- "Implementation Details"
- "구현 디테일"
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
- "Testing"
- "테스트"
- "Invariant"
- "불변식"
- "Binary Search"
- "이분탐색"
- "Prefix"
- "접두어"
- "Stack"
- "스택"
- "Monotonic Stack"
- "단조 스택"
- "Interval"
- "구간"
- "APIO"
- "APIO 2009"
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 4012: 컨벤션 센터](https://www.acmicpc.net/problem/4012)
- 요약: 단체별 사용 구간이 주어질 때, 서로 겹치지 않게 최대 개수의 구간을 선택하고, 그 최대 해들 중 사전편집(lexicographical) 순으로 가장 앞서는 단체 번호 리스트를 출력한다. 끝나는 시각과 다음 시작 시각이 같아도 겹침으로 간주한다.

### 제한/스펙
- N ≤ 200,000
- 시작/끝 시각 ≤ 1e9
- 출력: 첫 줄 최대 개수 M, 둘째 줄 사전순으로 가장 이른 해의 단체 번호를 오름차순 나열

## 입력/출력 형식
```
<입력>
N
s1 e1
s2 e2
...
sN eN

<출력>
M
i1 i2 ... iM
```

## 접근 개요(아이디어 스케치)
- **최대 개수**는 구간 스케줄링의 전형이지만, **사전순 최솟값**까지 요구해 단순 그리디로는 부족.
- 핵심 함수 f(l, r): 경계 (l, r) 내부에서 선택 가능한 최대 회의 수. 이를 빠르게 구하면, 경계 map을 유지하며 특정 구간 포함의 정당성을
  f(L, R) = f(L, s) + 1 + f(e, R)로 판정해 사전순으로 가장 이른 후보를 증명하며 선택 가능.
- f(l, r) 계산을 위해 시작시각 오름차순 정렬 + 각 회의의 **직전 가능한 회의**를 가리키는 포인터에 대해 **binary lifting(sparse table)** 구성 → O(log n)에 f(l, r) 평가.
- r 직전 회의를 찾고, l보다 시작이 큰 선행자만 이진 점프로 건너뛰며 개수를 누적.

```mermaid
flowchart TD
  A[정렬 및 전처리] --> B[prev 회의 + sparse table]
  B --> C[f(l,r) 질의 O(log n)]
  C --> D{경계 map 유지}
  D -->|검사: f(L,R)=f(L,s)+1+f(e,R)| E[채택 및 경계 갱신]
  D -->|불만족| F[스킵]
```

## 알고리즘 설계
- 시작 시각 기준으로 회의 정렬, 끝 시각 정렬도 병행.
- 각 회의 x에 대해, x 시작 이전에 끝난 회의들 중 시작이 최대인 회의 prev[x]를 계산.
- prev를 기반으로 dp[x][k] = x의 2^k번째 이전 회의를 구성(없으면 0).
- f(l, r): r보다 작은 끝을 가진 마지막 회의 x를 잡고, p[x].start > l인 동안 상위 점프하며 개수를 합산.
- 사전순 선택: 구간 경계 map에 [L→R]들을 저장(초기 0→INF). 각 i에 대해 (L < s_i < e_i < R)이고 위 등식이 성립하면 i 채택 및 경계 분할.

## 복잡도
- 전처리: O(n log n) (정렬 + sparse table)
- 각 f(l, r) 질의: O(log n)
- 선형으로 i를 훑으며 map 연산 O(log n)씩 → 전체 O(n log n)
- 공간: O(n log n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	const int INF = 2000000000;

	int n;
	if (!(cin >> n)) return 0;

	vector<pair<int,int>> p(n + 1); // p[i] = {start, end}
	vector<pair<int,int>> s(n + 1), e(n + 1);
	for (int i = 1; i <= n; ++i) {
		int a, b; cin >> a >> b;
		p[i] = {a, b};
		s[i] = {a, i};
		e[i] = {b, i};
	}

	sort(s.begin() + 1, s.begin() + n + 1);
	sort(e.begin() + 1, e.begin() + n + 1);

	int K = 1;
	while ((1 << K) <= n) ++K;

	vector<vector<int>> dp(n + 1, vector<int>(K, 0));

	vector<pair<int,int>> stk; // (end, idx), strictly increasing by end
	stk.emplace_back(INT_MIN, 0); // sentinel

	int j = 1, prv = 0;
	for (int idx = 1; idx <= n; ++idx) {
		int cur = s[idx].second;

		while (j <= n && e[j].first < p[cur].first) {
			int t = e[j].second;
			if (p[prv].first < p[t].first) prv = t; // prev with maximum start among those ended
			++j;
		}

		while (!stk.empty() && stk.back().first >= p[cur].second) stk.pop_back();
		stk.emplace_back(p[cur].second, cur);

		dp[cur][0] = prv;
		for (int k = 1; k < K; ++k) dp[cur][k] = dp[dp[cur][k - 1]][k - 1];
	}

	auto f = [&](int l, int r) -> int {
		auto it = lower_bound(stk.begin(), stk.end(), make_pair(r, 0));
		if (it == stk.begin()) return 0;
		int x = prev(it)->second;
		if (p[x].first <= l) return 0;
		int ret = 1;
		for (int k = K - 1; k >= 0; --k) {
			int y = dp[x][k];
			if (p[y].first > l) {
				x = y;
				ret += (1 << k);
			}
		}
		return ret;
	};

	int M = f(0, INF);
	cout << M << "\n";

	map<int,int> mp; // boundary map: start -> end for selected intervals
	mp[0] = 0;
	mp[INF] = INF;

	bool first = true;
	for (int i = 1; i <= n; ++i) {
		auto it = mp.lower_bound(p[i].first);
		if (it == mp.end()) continue;
		auto rIt = it;
		if (it == mp.begin()) continue;
		auto lIt = prev(it);

		if (lIt->second < p[i].first && p[i].second < rIt->first) {
			int L = lIt->second, R = rIt->first;
			if (f(L, R) == f(L, p[i].first) + 1 + f(p[i].second, R)) {
				if (!first) cout << ' ';
				cout << i;
				first = false;
				mp[p[i].first] = p[i].second;
			}
		}
	}
	cout << "\n";
	return 0;
}
```

## 코너 케이스 체크리스트
- 동일 시작/끝을 가진 구간이 섞인 경우(등호 처리 유의: 끝==시작이면 겹침)
- 매우 긴 구간 사이에 짧은 구간들이 많은 경우(경계 분할 검증)
- 선택 해가 유일/여러 개인 경우의 사전순 안정성
- N이 큰 경우(2e5) 시간·메모리 한계 내 전처리/질의 수행

## 제출 전 점검
- 출력 형식(개수, 개행, 공백 분리) 확인
- 64-bit 범위 불필요(시각은 int 범위)이나 인덱스/시프트 오버플로 주의
- 정렬 안정성 무관(명시적 인덱스 사용)

## 참고자료
- [BOJ 4012: 컨벤션 센터](https://www.acmicpc.net/problem/4012)
- [Coder's Brunch: 4012번 컨벤션 센터 노트](http://codersbrunch.blogspot.com/2017/01/4012.html)


