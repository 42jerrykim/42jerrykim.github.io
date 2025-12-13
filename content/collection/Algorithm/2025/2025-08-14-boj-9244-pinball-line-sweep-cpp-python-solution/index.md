---
title: "[Algorithm] C++/Python 백준 9244번: 핀볼 - 스위프 라인"
description: "선분이 서로 교차하지 않는 핀볼 보드에서 x=x0로 공을 떨어뜨릴 때, 선분을 만난 뒤에는 더 낮은 끝점으로 흘러 다시 수직 낙하합니다. 스위프 라인과 활성 집합으로 각 선분 하단에서 바로 아래 선분을 연결해 흐름 그래프를 만든 뒤, 시작 x에서 최상단 선분부터 따라 내려가 O(N log N)으로 최종 x좌표를 구합니다. 정수 기하 비교로 오차 없이 안전하게 구현합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Geometry"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-9244"
- "cpp"
- "python"
- "C++"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
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
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Geometry"
- "기하"
- "Sweep Line"
- "스위프 라인"
- "Event Sorting"
- "이벤트 정렬"
- "Active Set"
- "활성 집합"
- "Balanced BST"
- "균형트리"
- "std::set"
- "Integer Geometry"
- "정수 기하"
- "__int128"
- "Overflow"
- "오버플로"
- "Precision"
- "정밀도"
- "Sorting"
- "정렬"
- "Coordinate"
- "좌표"
- "Line Segment"
- "선분"
- "Segment Ordering"
- "선분 정렬"
- "Downward Flow"
- "하강 흐름"
- "Pinball"
- "핀볼"
- "NCPC"
- "NCPC 2013"
- "ICPC"
- "Greedy"
- "그리디"
- "Graph"
- "그래프"
- "Directed Acyclic Graph"
- "유향 비순환 그래프"
- "Topological"
- "위상"
- "Mathematics"
- "수학"
- "Robust"
- "견고한 구현"
- "Overflow Safety"
- "오버플로 안전"
- "Deterministic"
- "결정적"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/9244
- 요약: 무한히 높은 곳에서 x = x0 지점에 공을 떨어뜨리면, 공은 수직으로 내려오다 선분을 만나면 그 선분을 아래쪽으로 따라 흐른다. 더 낮은 끝점에 도달하면 다시 수직 낙하한다. 최종적으로 공이 멈추는 x좌표를 구하라.
- 제한: N ≤ 100,000, |x|, |y| ≤ 1,000,000. 선분은 서로 교차하지 않고, 수직/수평선은 없다. 끝점도 선분에 포함된다.

## 입력/출력
```
입력
N
x1 y1 x2 y2
... (총 N줄)
x0
```
```
출력
공의 최종 위치 x좌표
```

예제 1
```
2
-1 1 1 -1
1 -2 2 -3
0
```
```
2
```

예제 2
```
3
-1 1 1 -1
1 -2 0 -3
1 -3 2 -4
0
```
```
0
```

## 접근 개요
- 선분이 서로 교차하지 않으므로 임의의 x에서 위→아래 순서는 이벤트 사이 구간에서 변하지 않는다.
- x를 왼쪽→오른쪽으로 스캔하며 활성 선분 집합을 현재 x에서의 y순(아래→위)으로 유지한다.
- 각 선분의 더 낮은 끝점 x=low_x에서, 그 시점 활성 집합에서 “해당 선분 바로 아래”를 찾으면 흘러내림 그래프의 간선을 얻는다.
- 시작 x0에서 활성 집합의 맨 위 선분을 찾고, 간선을 따라 아래로 이동하면 최종 x좌표에 도달한다.

```mermaid
flowchart TD
    A[x0에서 낙하] -->|첫 교차| S1[선분 S1]
    S1 -->|하단(low_x)| S2[선분 S2]
    S2 -->|하단(low_x)| S3[선분 S3]
    S3 --> G[지면: 더 아래 선분 없음]
    G -->|정답| X[최종 x좌표]
```

## 알고리즘
- 이벤트 정의:
  - 좌끝 x=xl: 활성 집합에 삽입
  - 하단 x=low_x: 현재 집합에서 바로 아래 선분을 찾고 nxt[i]로 기록(없으면 -1)
  - 우끝 x=xr: 활성 집합에서 제거
  - 시작 x=x0: 현재 집합의 최상단 선분을 시작점으로 기록
- 비교 함수: y(x) 비교를 부동소수점 없이 정수 교차곱(`__int128`)으로 수행해 오차를 제거.
- 활성 집합: `std::set<int, Comparator>`로 유지. 현재 x가 바뀔 때마다 비교 기준에 반영되도록 캡처 포인터 사용.
- 시작에서 `nxt`를 따라가 마지막 선분의 더 낮은 끝점 x가 정답. 시작 시 활성 집합이 비어 있으면 정답은 x0.

정당성 요약:
- 교차가 없으므로 이벤트 사이 구간에서 선분의 상하 순서가 보존된다.
- 하단점에서 바로 아래 선분으로만 흘러갈 수 있으므로, `low_x` 시점의 바로 아래 탐색이 정확하다.
- 따라서 단 한 번의 스위프로 구성한 `nxt`를 따라가면 실제 물리 흐름과 일치한다.

## 복잡도
- 이벤트 수 O(N). 각 이벤트 처리 O(log N). 전체 O(N log N), 메모리 O(N).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Segment {
    long long xl, yl, xr, yr; // xl < xr
    long long low_x, low_y;   // lower endpoint
};

struct Event {
    long long x;
    int type; // 0=insert, 1=lowpoint, 2=startQuery, 3=remove
    int id;   // segment id or -1 for startQuery
    bool operator<(const Event& other) const {
        if (x != other.x) return x < other.x;
        return type < other.type; // insert -> lowpoint -> start -> remove
    }
};

struct Comparator {
    const vector<Segment>* segs;
    const long long* currX;
    bool operator()(int a, int b) const {
        if (a == b) return false;
        const Segment& A = (*segs)[a];
        const Segment& B = (*segs)[b];
        long long x = *currX;

        __int128 dxA = (__int128)(A.xr - A.xl);
        __int128 dyA = (__int128)(A.yr - A.yl);
        __int128 dxB = (__int128)(B.xr - B.xl);
        __int128 dyB = (__int128)(B.yr - B.yl);

        // Compare y_A(x) ? y_B(x) without division:
        // y_A(x) = yl_A + dyA/dxA * (x - xl_A)
        // Compare (yl_A*dxA + dyA*(x - xl_A)) / dxA vs (yl_B*dxB + dyB*(x - xl_B)) / dxB
        __int128 valA = (__int128)A.yl * dxA + dyA * (__int128)(x - A.xl); // y(x)*dxA
        __int128 valB = (__int128)B.yl * dxB + dyB * (__int128)(x - B.xl); // y(x)*dxB

        __int128 left = valA * dxB;
        __int128 right = valB * dxA;

        if (left != right) return left < right; // ascending by y
        return a < b; // tie-break by id for stability
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<Segment> segs(N);
    for (int i = 0; i < N; ++i) {
        long long x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        if (x1 < x2) {
            segs[i].xl = x1; segs[i].yl = y1;
            segs[i].xr = x2; segs[i].yr = y2;
        } else {
            segs[i].xl = x2; segs[i].yl = y2;
            segs[i].xr = x1; segs[i].yr = y1;
        }
        if (segs[i].yl <= segs[i].yr) {
            segs[i].low_x = segs[i].xl;
            segs[i].low_y = segs[i].yl;
        } else {
            segs[i].low_x = segs[i].xr;
            segs[i].low_y = segs[i].yr;
        }
    }
    long long x0;
    cin >> x0;

    vector<Event> events;
    events.reserve(3LL * N + 1);
    for (int i = 0; i < N; ++i) {
        events.push_back({segs[i].xl, 0, i});      // insert at left
        events.push_back({segs[i].low_x, 1, i});   // lowpoint query
        events.push_back({segs[i].xr, 3, i});      // remove at right
    }
    events.push_back({x0, 2, -1});                 // start query
    sort(events.begin(), events.end());

    long long currX = 0;
    Comparator comp{&segs, &currX};
    std::set<int, Comparator> active(comp);

    vector<int> nxt(N, -1);
    int startSeg = -1;
    bool startDone = false;

    for (const auto& ev : events) {
        currX = ev.x;

        if (ev.type == 0) {
            active.insert(ev.id);
        } else if (ev.type == 1) {
            int i = ev.id;
            auto it = active.find(i);
            if (it != active.end()) {
                if (it == active.begin()) {
                    nxt[i] = -1;
                } else {
                    auto pit = prev(it);
                    nxt[i] = *pit;
                }
            } else {
                nxt[i] = -1; // safety guard
            }
        } else if (ev.type == 2) {
            if (!startDone) {
                if (active.empty()) {
                    startSeg = -1;
                } else {
                    auto it = active.end();
                    --it;
                    startSeg = *it; // topmost y at x0
                }
                startDone = true;
            }
        } else { // remove
            int i = ev.id;
            auto it = active.find(i);
            if (it != active.end()) active.erase(it);
        }
    }

    if (startSeg == -1) {
        cout << x0 << '\n';
        return 0;
    }
    int s = startSeg;
    while (nxt[s] != -1) s = nxt[s];
    cout << segs[s].low_x << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
# 참고: 본 문제의 핵심은 "현재 x에 의존하는 순서"를 유지하는 균형 BST가 필요합니다.
# 파이썬 표준 라이브러리만으로는 비교자가 동적으로 변하는 정렬 집합을 직접 제공하지 않으므로
# 실전 제출은 C++ 권장입니다. 아래는 로직 스켈레톤입니다.

import sys
input = sys.stdin.readline

def solve():
    N = int(input())
    segs = []
    for _ in range(N):
        x1, y1, x2, y2 = map(int, input().split())
        if x1 < x2:
            xl, yl, xr, yr = x1, y1, x2, y2
        else:
            xl, yl, xr, yr = x2, y2, x1, y1
        low_x, low_y = (xl, yl) if yl <= yr else (xr, yr)
        segs.append((xl, yl, xr, yr, low_x, low_y))
    x0 = int(input())

    # 이벤트 생성: (x, type, id) — type: 0 insert, 1 lowpoint, 2 start, 3 remove
    events = []
    for i, (xl, yl, xr, yr, low_x, low_y) in enumerate(segs):
        events.append((xl, 0, i))
        events.append((low_x, 1, i))
        events.append((xr, 3, i))
    events.append((x0, 2, -1))
    events.sort()

    # 실제 제출은 C++ 구현 권장.
    # 여기서는 알고리즘 개요만 유지합니다.
    print(x0)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- N=0 또는 x0 위치에서 교차 선분이 없음 → 정답은 x0
- `low_x`가 `xl`/`xr`과 같은 경우 이벤트 순서: 삽입 → 하단쿼리 → 제거
- 여러 선분의 `low_x`가 동일해도 하단에서 “바로 아래”만 참조하므로 일관성 유지
- 끝점 포함 규칙: 수직 낙하가 끝점에서 시작/종료할 수 있음 → 비교 동률 시 안정 정렬 필요
- 부동소수점 금지: 정수 교차곱과 `__int128`로 오버플로/정밀도 문제 회피

## 제출 전 점검
- 표준 입출력/개행, 64-bit 정수 사용 확인
- 이벤트 정렬 우선순위 확인(삽입→하단쿼리→시작→제거)
- 비교자가 현재 x만 참조함을 보장(교차 없음 가정하에 이벤트 사이 순서 변동 없음)

## 참고자료
- NCPC 2013 H: 핀볼 (원문 분류)
- 문제 링크: https://www.acmicpc.net/problem/9244
