---
title: "[Algorithm] C++/Python 백준 12735번: Boat"
description: "한강 북안 N개 학교가 [ai, bi] 범위의 보트를 낼 수 있고, 선택된 각 학교의 보트 수가 이전에 선택된 모든 더 작은 번호 학교의 보트 수보다 항상 큰 경우의 수를 구합니다. 좌표압축과 구간 DP, 모듈러 역원으로 O(N^3) 카운팅을 구현합니다."
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
- Problem-12735
- cpp
- python
- C++
- Python
- Data Structures
- 자료구조
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
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
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
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Disjoint Set Union
- 유니온파인드
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
- Modulo
- 모듈러
- Debugging
- 디버깅
- Implementation Details
- 구현 디테일
- Coordinate Compression
- 좌표압축
- Counting
- 카운팅
- Combinatorics
- 조합론
- APIO
- APIO-2016
- Boat
- Strictly Increasing
- 증가수열
- Prefix Sum
- 부분합
- Modular Inverse
- 모듈러 역원
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12735
- 요약: 각 학교 i는 [ai, bi] 대수의 보트를 낼 수 있고(안 낼 수도 있음), 만약 낸다면 i보다 작은 번호 학교들이 낸 모든 수보다 더 많은 보트를 내야 합니다. 한 학교 이상이 내는 모든 배치 수를 구해 1,000,000,007로 나눈 값을 출력합니다.

## 입력/출력
```
입력
N
a1 b1
a2 b2
...
aN bN

출력
정답 (모듈러 1,000,000,007)
```

## 접근 개요
- 핵심 관찰: 선택된 학교 인덱스가 증가할수록 보트 수도 엄격히 증가해야 하므로, 최종적으로는 (인덱스, 보트 수) 쌍이 인덱스 오름차순, 보트 수 엄격 증가를 만족하는 수열의 개수 카운팅 문제입니다.
- ai, bi가 최대 1e9이므로 값의 범위가 커 직접 순회 불가. 구간의 경계만 의미 있으므로 모든 ai와 (bi+1)을 모아 좌표압축 후, 인접한 압축 좌표 [st, ed) 구간을 길이 L=ed-st로 순회합니다.
- 각 구간 [st, ed) 동안 그 구간을 완전히 덮는 후보 학교들만 고려해, 이번 구간에서 k개를 고르고 마지막 후보 인덱스가 j일 때의 조합 수를 dp2[k][j]로 누적(prefix) 계산합니다.
- 조합 항은 (L−k+1)/k가 곱해지는 형태로 나타나 모듈러 역원을 사용합니다. 이전 구간까지의 상태 dp를 부분합(pref)로 관리하여 k=1 전이도 O(1)로 처리합니다.

```mermaid
flowchart LR
    A[좌표압축된 점들 v[0..M])]
    A --> B([각 인접 구간 i: [v[i-1], v[i]) 길이 L])
    B --> C{구간을 완전히 덮는 학교 후보 cnd[] 추출}
    C --> D[dp2[k][j] 누적 전이 (모듈러 역원 사용)]
    D --> E[dp[cnd[j]] 갱신]
    E --> F[다음 구간으로]
```

## 알고리즘 설계
- 상태 정의
  - dp[j]: 지금까지 처리한 구간 전체에서 마지막으로 선택된 학교가 j일 때의 경우의 수 (dp[0]=1은 시작 상태)
  - dp2[k][j]: 현재 구간에서 k개 선택했고, 후보 배열 cnd의 j번째 학교가 마지막일 때의 누적(prefix) 합
- 전이 요약(구간 길이 L, 후보 크기 K)
  - 후보는 cnd[j]가 [st, ed) 전체를 덮는 학교만 포함
  - k=1: dp2[1][j] = dp2[1][j-1] + (sum(dp[0..cnd[j]-1]) * L)
  - k≥2: dp2[k][j] = dp2[k][j-1] + dp2[k-1][j-1] * (L - k + 1) / k  (모듈러 역원으로 나눗셈 처리)
  - 이후 dp에 이번 구간 기여를 차분(= dp2[k][j] - dp2[k][j-1])로 반영: dp[cnd[j]] += 차분값

## 복잡도
- 좌표 수는 최대 2N, 각 구간마다 후보 크기(K)와 L에 대해 위 전이를 수행합니다.
- 최악 시간 복잡도: O(N^3) (APIO 공식 풀이와 동일 추정). 공간: O(N^2) 수준(dp2).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int MOD = 1'000'000'007;

int64 modPow(int64 a, int64 e) {
	int64 r = 1;
	while (e) {
		if (e & 1) r = (r * a) % MOD;
		a = (a * a) % MOD;
		e >>= 1;
	}
	return r;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	
	int n;
	if (!(cin >> n)) return 0;
	vector<long long> a(n + 1), b(n + 1);
	vector<long long> coords;
	for (int i = 1; i <= n; ++i) {
		cin >> a[i] >> b[i];
		b[i]++; // [a, b+1) 로 변환
		coords.push_back(a[i]);
		coords.push_back(b[i]);
	}
	sort(coords.begin(), coords.end());
	coords.erase(unique(coords.begin(), coords.end()), coords.end());
	
	static long long inv[1005];
	for (int i = 1; i <= 1000; ++i) inv[i] = modPow(i, MOD - 2);

	static long long dp[505], pref[505];
	static long long dp2[505][505];
	dp[0] = 1; // 시작 상태

	for (size_t t = 1; t < coords.size(); ++t) {
		long long st = coords[t - 1], ed = coords[t];
		long long L = ed - st;
		if (L <= 0) continue;

		vector<int> cnd;
		pref[0] = 1; // dp[0] 포함
		for (int j = 1; j <= n; ++j) {
			pref[j] = (pref[j - 1] + dp[j]) % MOD;
			if (a[j] <= st && ed <= b[j]) cnd.push_back(j);
		}
		int K = (int)cnd.size();
		if (K == 0) continue;

		int upto = (int)min<long long>(K, L);
		for (int k = 1; k <= upto; ++k) {
			for (int j = k - 1; j < K; ++j) {
				if (k == 1) {
					int idx = cnd[j] - 1;
					long long val = (pref[idx] * (L % MOD)) % MOD;
					if (j) val = (val + dp2[k][j - 1]) % MOD;
					dp2[k][j] = val;
				} else {
					long long add = (dp2[k - 1][j - 1] * inv[k]) % MOD;
					add = (add * ((L - k + 1) % MOD)) % MOD;
					long long val = add;
					if (j) val = (val + dp2[k][j - 1]) % MOD;
					dp2[k][j] = val;
				}
			}
		}
		for (int k = 1; k <= upto; ++k) {
			for (int j = k - 1; j < K; ++j) {
				long long cur = dp2[k][j];
				if (j) cur = (cur - dp2[k][j - 1] + MOD) % MOD;
				dp[cnd[j]] += cur;
				if (dp[cnd[j]] >= MOD) dp[cnd[j]] -= MOD;
			}
		}
	}

	long long ans = 0;
	for (int i = 1; i <= n; ++i) {
		ans += dp[i];
		if (ans >= MOD) ans -= MOD;
	}
	cout << ans << '\n';
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

n_line = input().split()
if not n_line:
    sys.exit(0)
n = int(n_line[0])

a = [0] * (n + 1)
b = [0] * (n + 1)
coords = []
for i in range(1, n + 1):
    ai, bi = map(int, input().split())
    a[i] = ai
    b[i] = bi + 1
    coords.append(ai)
    coords.append(b[i])

coords = sorted(set(coords))

inv = [0] * 1005
for i in range(1, 1001):
    inv[i] = pow(i, MOD - 2, MOD)

dp = [0] * (n + 1)
pref = [0] * (n + 1)
dp2 = [[0] * (n + 1) for _ in range(n + 1)]
dp[0] = 1

for t in range(1, len(coords)):
    st, ed = coords[t - 1], coords[t]
    L = ed - st
    if L <= 0:
        continue

    cnd = []
    pref[0] = 1
    for j in range(1, n + 1):
        pref[j] = (pref[j - 1] + dp[j]) % MOD
        if a[j] <= st and ed <= b[j]:
            cnd.append(j)

    K = len(cnd)
    if K == 0:
        continue

    upto = min(K, L)
    for k in range(1, upto + 1):
        base = 0
        if k == 1:
            mul = L % MOD
            for j in range(k - 1, K):
                idx = cnd[j] - 1
                val = (pref[idx] * mul) % MOD
                base = (base + val) % MOD
                dp2[k][j] = base
        else:
            mul = (inv[k] * ((L - k + 1) % MOD)) % MOD
            prev_row = dp2[k - 1]
            for j in range(k - 1, K):
                val = (prev_row[j - 1] * mul) % MOD
                base = (base + val) % MOD
                dp2[k][j] = base

    for k in range(1, upto + 1):
        prev = 0
        for j in range(k - 1, K):
            cur = dp2[k][j]
            add = (cur - prev) % MOD
            dp[cnd[j]] = (dp[cnd[j]] + add) % MOD
            prev = cur

ans = sum(dp[1:]) % MOD
print(ans)
```

## 코너 케이스 체크리스트
- 구간 길이 L이 매우 큼: 좌표압축으로 처리, 조합 부분은 (L−k+1)/k 형태만 사용
- 학교를 하나도 선택하지 않는 경우는 배제되어야 함: dp 합은 j≥1만 더하므로 자동 배제
- 모든 학교가 해당 구간을 덮지 못하는 경우: cnd가 비어 있어도 안전하게 스킵
- 모듈러 나눗셈: 역원 사용(소수 MOD), 0으로 나누는 경우 없음(k≥1, L≥k에서만 사용)

## 제출 전 점검
- 좌표압축 시 중복 제거 및 정렬 확인
- dp 누적/차분 반영 구간 인덱스 오프바이원 주의
- 모듈러 음수 방지: (x - y + MOD) % MOD 패턴 사용
- Python은 최악 N=500에서 느릴 수 있음 → C++ 권장

## 참고자료
- 구사과 APIO 2016 정리: https://koosaga.com/113
- apio16_boat.cpp: https://github.com/koosaga/olympiad/blob/master/APIO/apio16_boat.cpp


