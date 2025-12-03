---
title: "[Algorithm] C++ 백준 1144번: 싼 비용 - Connection Profile DP"
description: "N,M ≤ 9 격자에서 상하좌우로 연결된 하나의 칸 집합을 골라 비용 합의 최솟값을 찾습니다. 연결 프로파일 DP로 상태를 라벨링·정규화해 압축하고, 고립 검사와 병합 전이로 올바름과 효율을 보장합니다. 시간·공간 복잡도, 구현 포인트, 코너 케이스까지 정리합니다."
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
- Problem-1144
- cpp
- C++
- Python
- Dynamic Programming
- 동적계획법
- Profile DP
- 프로파일 DP
- Connection Profile
- 연결 프로파일
- Grid DP
- 격자 DP
- State Compression
- 상태압축
- Connectivity
- 연결성
- Connected Component
- 연결 컴포넌트
- Component Merging
- 컴포넌트 병합
- Label Normalization
- 라벨 정규화
- Normalize
- 정규화
- Merge
- 병합
- CheckPass
- 고립 검사
- CheckValid
- 유효성 검사
- Mask DP
- 비트마스크
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
- Invariant
- 불변식
- Greedy
- 그리디
- Graph
- 그래프
- BFS
- DFS
- Shortest Path
- 최단경로
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
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/1144
- 요약: N×M 격자의 각 칸에 정수 비용이 주어질 때, 상하좌우로 연결된 칸들로 이루어진 하나의 집합을 골라 그 비용 합의 최솟값을 구한다. 크기 0의 집합(공집합)도 허용된다.
- 제한/스펙: N, M ≤ 9, 각 칸의 비용 |value| ≤ 1000, 시간 제한 2초

## 입력/출력
```
입력
N M
v[0][0] v[0][1] ... v[0][M-1]
...
v[N-1][0] ...     v[N-1][M-1]

출력
가장 싼 연결된 칸 집합의 비용 합(정수)
```

예시
```
입력
2 2
-10 1
2 -10

출력
-19
```

## 접근 개요
- **핵심 관찰**: 행 우선(좌→우, 위→아래)으로 스캔할 때, "현재 칸 위쪽에서 내려오는 연결 라벨들과 왼쪽 인접 라벨"만이 연결성 판단에 필요하다.
- **상태 정의(프로파일)**: `cur`는 최근 M칸(현재 칸의 바로 위 열까지)의 연결 컴포넌트 라벨을 문자로 저장. 같은 라벨은 같은 컴포넌트를 의미. 매 스텝마다 라벨을 정규화(normalize)하여 동치 상태를 하나로 압축.
- **전이**:
  - 미선택(skip): 현재 칸을 고르지 않음. 위에서 내려오는 열의 컴포넌트가 고립되지 않았을 때만 허용(`checkPass`).
  - 선택(take): 현재 칸을 고름. 위(up) 라벨과 좌(left) 라벨을 병합해 새 라벨 구성(`merge`).
- **종료/유효성**: 모든 칸을 처리한 뒤, 프로파일에 남아있는 개방 컴포넌트 수가 0 또는 1일 때만 유효(`checkValid`). 빈 집합 허용이므로 언제든 0과 비교해 최소 갱신.

## 알고리즘 설계
- **상태**: `DP(x, y, cur)` = (x, y)부터 끝까지 처리할 때 만들 수 있는 단일 연결 컴포넌트의 최소 비용 합.
- **정규화**: 프로파일 문자를 좌측부터 1,2,3,…로 재라벨링해 동치 상태를 하나로 만듦 → 메모리·시간 절약.
- **고립 방지(checkPass)**: 현재 칸을 건너뛰면 `up` 라벨이 좌측의 어떤 라벨과도 이어지지 않으면 위쪽이 고립됨. 이를 막아 연결성 보장.
- **병합(merge)**: 선택 시 위/좌 라벨을 규칙대로 병합. 모두 0이면 새 라벨 생성, 하나만 0이면 그 하나 사용, 둘 다 있고 다르면 전체 프로파일에서 둘을 하나로 통합.
- **정당성 스케치**: (1) 프로파일은 향후 연결성에 영향을 미치는 충분한 정보(필요조건)를 보존한다. (2) 정규화로 동치 상태를 한 상태로 모아 최적 부분구조를 유지한다. (3) `checkPass/Valid`로 위쪽 고립과 다중 컴포넌트 종료를 배제해 전역적으로 하나의 컴포넌트만 형성되도록 한다.

## 복잡도
- 상태 수는 M ≤ 9에서 가능한 연결 라벨링의 개수 T에 비례(카탈란 유사 규모). 전체 복잡도는 대략 O(N·M·T). 실측상 N,M ≤ 9에서 충분히 2초 내 동작.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int INF = 1e9;

int n, m;
int grid[9][9];
vector<vector<unordered_map<string, int>>> memo;

static inline string normalizeProfile(const string& s) {
	string normalized(s.size(), '0');
	unsigned char remap[256] = {0};
	char nextLabel = '1';
	for (size_t i = 0; i < s.size(); ++i) {
		char c = s[i];
		if (c == '0') continue;
		if (!remap[(unsigned char)c]) remap[(unsigned char)c] = nextLabel++;
		normalized[i] = remap[(unsigned char)c];
	}
	return normalized;
}

static inline bool checkPass(const string& s) {
	if (s[0] == '0') return true;
	for (size_t i = 1; i < s.size(); ++i) if (s[i] == s[0]) return true;
	return false;
}

static inline bool checkValid(const string& s) {
	bool seen[256] = {false};
	int cnt = 0;
	for (char c : s) if (c != '0' && !seen[(unsigned char)c]) {
		seen[(unsigned char)c] = true;
		if (++cnt > 1) return false;
	}
	return true;
}

static inline string mergeWithLeft(const string& s) {
	string ret = s;
	char up = s[0];
	char left = s.back();
	ret.erase(ret.begin());
	if (up == '0' && left == '0') ret.push_back('9');
	else if (up == '0') ret.push_back(left);
	else if (left == '0' || up == left) ret.push_back(up);
	else {
		for (char& c : ret) if (c == left) c = up;
		ret.push_back(up);
	}
	return normalizeProfile(ret);
}

static inline string mergeNoLeft(const string& s) {
	string ret = s; ret.erase(ret.begin());
	char up = s[0];
	ret.push_back(up == '0' ? '9' : up);
	return normalizeProfile(ret);
}

int dfs(int x, int y, string cur) {
	if (x == n) return checkValid(cur) ? 0 : INF;
	cur = normalizeProfile(cur);
	auto& cache = memo[x][y];
	if (auto it = cache.find(cur); it != cache.end()) return it->second;
	int best = INF;
	int nx = x, ny = y + 1; if (ny >= m) { nx++; ny = 0; }
	if (checkPass(cur)) {
		string nxt = cur; nxt.erase(nxt.begin()); nxt.push_back('0');
		best = min(best, dfs(nx, ny, nxt));
	}
	string nxtTake = (y ? mergeWithLeft(cur) : mergeNoLeft(cur));
	best = min(best, dfs(nx, ny, nxtTake) + grid[x][y]);
	if (checkValid(cur)) best = min(best, 0);
	return cache[cur] = best;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cin >> n >> m;
	for (int i = 0; i < n; ++i) for (int j = 0; j < m; ++j) cin >> grid[i][j];
	memo.assign(n, vector<unordered_map<string, int>>(m));
	cout << dfs(0, 0, string(m, '0')) << '\n';
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

INF = 10**9

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

from functools import lru_cache

def normalize_profile(s: str) -> str:
    remap = {}
    next_label = ord('1')
    out = []
    for ch in s:
        if ch == '0':
            out.append('0')
        else:
            if ch not in remap:
                remap[ch] = chr(next_label)
                next_label += 1
            out.append(remap[ch])
    return ''.join(out)

def check_pass(s: str) -> bool:
    if s[0] == '0':
        return True
    for i in range(1, len(s)):
        if s[i] == s[0]:
            return True
    return False

def check_valid(s: str) -> bool:
    seen = set()
    for ch in s:
        if ch != '0':
            seen.add(ch)
            if len(seen) > 1:
                return False
    return True

def merge_with_left(s: str) -> str:
    up = s[0]
    left = s[-1]
    ret = s[1:]
    if up == '0' and left == '0':
        ret += '9'
    elif up == '0':
        ret += left
    elif left == '0' or up == left:
        ret += up
    else:
        # replace all left with up
        table = str.maketrans({left: up})
        ret = ret.translate(table) + up
    return normalize_profile(ret)

def merge_no_left(s: str) -> str:
    up = s[0]
    ret = s[1:] + ('9' if up == '0' else up)
    return normalize_profile(ret)

@lru_cache(maxsize=None)
def dfs(x: int, y: int, cur: str) -> int:
    if x == n:
        return 0 if check_valid(cur) else INF
    cur = normalize_profile(cur)
    nx, ny = x, y + 1
    if ny >= m:
        nx += 1
        ny = 0
    best = INF
    if check_pass(cur):
        nxt = cur[1:] + '0'
        best = min(best, dfs(nx, ny, nxt))
    nxt_take = merge_with_left(cur) if y > 0 else merge_no_left(cur)
    best = min(best, dfs(nx, ny, nxt_take) + grid[x][y])
    if check_valid(cur):
        best = min(best, 0)
    return best

print(dfs(0, 0, '0' * m))
```

## 코너 케이스 체크리스트
- 전부 양수 → 빈 집합(0)이 최적
- 전부 음수 → 가장 큰(절댓값 큰) 음수 덩어리 선택이 최적일 수 있음(연결 제약 주의)
- 열/행 길이 1인 경우(M=1 또는 N=1) → 선형 연결만 허용되므로 프로파일 동작 점검
- 동일 라벨 다수 병합 발생 → 정규화 누락 시 중복 상태 폭증
- 스킵 전이에서 위 고립 허용하면 오답

## 제출 전 점검
- 입력/출력 형식과 개행 확인
- 64-bit 오버플로: 비용 합의 절댓값이 커질 수 있으나 본 풀이에선 INF만 1e9 사용(필요시 long long 확장 가능)
- 프로파일 길이 M 유지, 전이 후 정규화 호출 여부 검토

## 참고자료
- jh05013, "Connection Profile DP 가이드" (프로파일 DP 기본 아이디어)
- Jinhan's Note, "[BOJ] 1144번 - 싼 비용" (구현 아이디어 정리)
- 백준 1144 문제 페이지
