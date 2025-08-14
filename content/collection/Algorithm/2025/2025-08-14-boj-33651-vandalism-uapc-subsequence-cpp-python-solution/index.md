---
title: "[Algorithm] cpp-python 백준 33651번: Vandalism"
description: "UAPC에서 일부 문자를 삭제해 얻은 s가 주어지면, 빠진 문자들을 원래 순서대로 복원합니다. 두 포인터로 UAPC와 s를 한 번만 훑어 불일치만 수집해 O(|UAPC|) 시간, O(1) 공간에 안정적으로 해결합니다."
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
- Problem-33651
- cpp
- python
- C++
- Python
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
- Subsequence
- 부분수열
- UAPC
- Vandalism
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/33651
- 요약: `UAPC`에서 몇 글자를 지워 얻은 `s`가 주어질 때, 제거된 문자들을 원래 순서대로 출력.

## 입력/출력
```
입력
s  (빈 문자열 아님, 길이 ≤ 3, UAPC에서 일부를 삭제해 얻은 부분수열)

출력
UAPC에서 제거된 문자들을 원래 순서대로 이어붙인 문자열
```

예시
```
입력: UAC
출력: P

입력: P
출력: UAC

입력: UC
출력: AP
```

## 접근 개요
- 핵심 관찰: 목표는 고정 패턴 `UAPC`에서 입력 `s`를 얻기 위해 빠진 문자들의 순서를 복원하는 것.
- 두 포인터: `t = "UAPC"`를 좌→우로 순회하며 `s`와 일치하면 `s` 포인터 전진, 불일치면 해당 문자를 제거 목록에 추가.
- 고정 길이(4) 패턴이므로 한 번의 선형 스캔으로 충분하며 구현이 단순하고 안전합니다.

## 알고리즘
1) `t = "UAPC"`, `j = 0`, `removed = ""`로 초기화
2) `t`의 각 문자 `c`에 대해
   - `j < |s|`이고 `s[j] == c`라면 `j++`
   - 아니면 `removed += c`
3) `removed` 출력

정당성 요약:
- `s`는 `UAPC`의 부분수열이므로 `UAPC`를 좌→우로 훑으며 일치 문자를 건너뛰면, 건너뛰지 못한 문자들은 모두 삭제된 문자이며 그 상대적 순서도 원본 순서를 보존합니다.

## 복잡도
- 시간: O(|UAPC|) = O(1)
- 공간: O(1)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	string s;
	if (!(cin >> s)) return 0;

	string t = "UAPC", removed;
	size_t j = 0;
	for (char c : t) {
		if (j < s.size() && c == s[j]) j++;
		else removed.push_back(c);
	}
	cout << removed;
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def solve():
    s = sys.stdin.readline().strip()
    t = "UAPC"
    j = 0
    removed = []
    for c in t:
        if j < len(s) and s[j] == c:
            j += 1
        else:
            removed.append(c)
    print("".join(removed))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- `s` 길이 1: 세 문자 연속 삭제 케이스도 동일 로직으로 처리
- `s` 길이 3: 단일 문자만 삭제된 경우 확인
- 앞/중간/끝 문자 삭제: `U`, `A`, `P`, `C` 각각 삭제되는 경우 모두 동작
- 중복 문자 없음: 고정 패턴 `UAPC` 내 문자는 서로 달라 모호성 없음

## 제출 전 점검
- 입출력 개행/공백 형식 확인
- 상수 시간 구현이지만 표준 입출력 버퍼링 사용
- 코드 상단 안내 주석 삽입(요구 사항)

## 참고자료
- 공식 문제: https://www.acmicpc.net/problem/33651

