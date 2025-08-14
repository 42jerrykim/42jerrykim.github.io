---
title: "[Algorithm] cpp-python 백준 15337번: 관광열차 좌석 배치 - s1/s2 계산"
description: "정책-1(승객 자유 좌석 선택)·정책-2(운영자 일괄 배정)에서 필요한 최소 좌석 s1·s2 계산. s2는 라인 스위핑으로 최대 동시 탑승, s1은 n−endPrefix[a]−startSuffix[b]의 최댓값. [a,b) 경계·누적/접미합·빠른 I/O, 엣지·실수 포인트 점검."
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
- Problem-15337
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
- Complexity Analysis
- 복잡도 분석
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
- Testing
- 테스트
- Invariant
- 불변식
- Line Sweep
- 라인스위핑
- Prefix Sum
- 누적합
- Suffix Sum
- 접미합
- Counting
- 카운팅
- Interval
- 구간
- Interval Overlap
- 구간겹침
- Interval Scheduling
- 구간 스케줄링
- Greedy
- 그리디
- Data Structures
- 자료구조
- Array
- 배열
- Seat Assignment
- 좌석 배정
- ICPC
- Tsukuba 2017
- Scenic Railroad
- 관광열차
- Half-open Interval
- 반열린구간
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/15337
- 요약: 승객 i의 탑승역 `a_i`, 하차역 `b_i`가 주어질 때 두 정책별 필요한 좌석 수를 구합니다.
  - 정책-1: 예약 순서와 좌석 선택이 임의(승객이 남은 좌석 중 아무 좌석이나 선택). 어떤 순서/선택에서도 항상 수용 가능한 최소 좌석 수 `s1`.
  - 정책-2: 모든 예약이 끝난 후 운영자가 일괄 배정. 최적 배정으로 필요한 최소 좌석 수 `s2`.

## 입력/출력
```
<입력>
n
a1 b1
...
an bn

<출력>
s1 s2  (한 줄, 공백 구분)
```

## 접근 개요
- 좌석은 역 사이 구간을 점유하므로 구간을 `[a, b)`(하차 역에서는 좌석 재사용 가능)로 해석합니다.
- **정책-2(s2)**: 동시에 열차에 타고 있는 승객 수의 최댓값 = 구간들의 최대 겹침 수. 시작점에서 +1, 끝점에서 -1 하는 라인 스위핑으로 계산.
- **정책-1(s1)**: 예약 순서/선호가 최악이어도 항상 좌석이 남아야 합니다. 이는 어떤 특정 승객의 구간 `[L, R)`에 대해 그 구간과 겹치는 승객 수의 최댓값과 동일합니다. 
  - 한 구간 `[L,R)`과 겹치는 구간 수는 `n - (#end ≤ L) - (#start ≥ R)`이고, 이를 모든 구간에 대해 최댓값으로 취합니다.
- 구현 핵심: 끝점 누적합 `endPrefix[x] = #end ≤ x`, 시작점 접미합 `startSuffix[x] = #start ≥ x`를 구성하면 각 구간의 겹침 수를 O(1)에 계산 가능합니다.

```mermaid
flowchart LR
  A[입력: n개 구간 (a,b)] --> B[빈도 배열 시작/끝 카운팅]
  B --> C[끝점 누적합 endPrefix]
  B --> D[시작점 접미합 startSuffix]
  C --> E[각 구간 i: overlap_i = n - endPrefix[a_i] - startSuffix[b_i]]
  D --> E
  E --> F[s1 = max_i overlap_i]
  B --> G[라인 스위프: cur += start[a], cur -= end[b]]
  G --> H[s2 = max cur]
```

## 알고리즘 설계
- 자료구조
  - 정수 배열 `startCount[1..M]`, `endCount[1..M]` (M = 최대 역 번호)
  - `endPrefix[i] = endPrefix[i-1] + endCount[i]`
  - `startSuffix[i] = startSuffix[i+1] + startCount[i]`
- 계산식
  - s2: 한 번의 선형 스위핑으로 최대 동시 탑승자 수
  - s1: 각 구간 i에 대해 `overlap_i = n - endPrefix[a_i] - startSuffix[b_i]`, s1는 그 최댓값
- 올바름 근거(요지)
  - s2: `[a,b)` 해석에서 같은 역 b에서 하차 후 즉시 탑승 가능하므로, 시작점에서 +1, 끝점에서 -1의 전형적 동시성 계산과 일치합니다.
  - s1: 어떤 구간 `[L,R)`이 이미 특정 좌석을 점유 중일 때, 동시에 해당 좌석을 쓸 수 없는 승객 수가 해당 구간과 겹치는 승객 수입니다. 최악의 예약 순서/선호에서도 모두 수용하려면, 모든 구간에 대해 이 겹침 수만큼 좌석이 준비되어야 하므로 최댓값이 필요 좌석 수가 됩니다.

## 복잡도
- 시간: O(n + M)  (M ≤ 100000, n ≤ 200000)
- 공간: O(M)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; if(!(cin >> n)) return 0;
    vector<pair<int,int>> segs; segs.reserve(n);
    int maxCoord = 0;
    for(int i=0;i<n;++i){
        int a,b; cin >> a >> b;
        segs.emplace_back(a,b);
        maxCoord = max(maxCoord, max(a,b));
    }

    vector<int> startCount(maxCoord+2,0), endCount(maxCoord+2,0);
    for(auto &p: segs){
        startCount[p.first] += 1;
        endCount[p.second] += 1; // [a,b) 해석: b에서 -1
    }

    // s2: 라인 스위핑으로 최대 동시 탑승자
    int s2 = 0, cur = 0;
    for(int x=1;x<=maxCoord;++x){
        cur += startCount[x];
        cur -= endCount[x];
        if(cur > s2) s2 = cur;
    }

    // 누적/접미 합
    vector<int> endPrefix(maxCoord+2,0), startSuffix(maxCoord+3,0);
    for(int i=1;i<=maxCoord;++i) endPrefix[i] = endPrefix[i-1] + endCount[i];
    for(int i=maxCoord;i>=1;--i) startSuffix[i] = startSuffix[i+1] + startCount[i];

    int s1 = 0;
    for(auto &p: segs){
        int L = p.first, R = p.second;
        int overlap = n - endPrefix[L] - startSuffix[R];
        if(overlap > s1) s1 = overlap;
    }

    cout << s1 << ' ' << s2 << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def solve() -> None:
    data = sys.stdin.read().strip().split()
    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return

    segs = []
    max_coord = 0
    for _ in range(n):
        a = int(next(it)); b = int(next(it))
        segs.append((a,b))
        if a > max_coord: max_coord = a
        if b > max_coord: max_coord = b

    start = [0]*(max_coord+2)
    end = [0]*(max_coord+2)
    for a,b in segs:
        start[a] += 1
        end[b] += 1  # [a,b)

    # s2: line sweep
    cur = 0
    s2 = 0
    for x in range(1, max_coord+1):
        cur += start[x]
        cur -= end[x]
        if cur > s2:
            s2 = cur

    # endPrefix, startSuffix
    end_pref = [0]*(max_coord+2)
    for i in range(1, max_coord+1):
        end_pref[i] = end_pref[i-1] + end[i]

    start_suf = [0]*(max_coord+3)
    for i in range(max_coord, 0, -1):
        start_suf[i] = start_suf[i+1] + start[i]

    s1 = 0
    for a,b in segs:
        overlap = n - end_pref[a] - start_suf[b]
        if overlap > s1:
            s1 = overlap

    print(s1, s2)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 동일 구간 다수 존재(중복 입력), 단일 승객, 모든 승객이 서로 겹치지 않음/모두 겹침
- 경계 동치: 하차역에서 즉시 다른 승객 탑승 가능([a,b) 해석). 시작 또는 끝이 동일한 구간 다수
- 최대 좌표가 작을 때/클 때 빈도 배열 크기 적정성, 1-기반 인덱스 범위

## 제출 전 점검
- 빠른 I/O 사용 여부(C++: sync_with_stdio(false), tie(nullptr))
- 끝점 누적합과 시작점 접미합의 정의가 문제의 [a,b) 해석과 일치하는지 확인
- 라인 스위프에서 증가/감소 지점이 각각 a, b에 정확히 적용되는지 재검토

## 참고자료/유사문제
- 좌표 라인 스위핑으로 동시 활동 수 계산(최대 겹침)
- 구간 겹침 수를 누적합/접미합으로 O(1) 조회


