---
title: "[Algorithm] C++/Python 백준 12771번: Oil"
description: "수평 선분들로 모델링된 유전을 한 번의 직선 시추로 통과하며 만나는 선분 길이 합(유전 너비 합)을 최대로 만드는 문제입니다. 각 선분의 양 끝점을 기준으로 기울기 구간을 스위프하여 포함 가중치를 갱신하고, O(n^2 log n)으로 최대 추출량을 구합니다."
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
- Problem-12771
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
- Geometry
- 기하
- Math
- 수학
- Segment Intersection
- 선분 교차
- Line Sweep
- 선형 스위프
- Slope Sweep
- 기울기 스위프
- Angle Sweep
- 각도 스위프
- Interval
- 구간
- Event Sorting
- 이벤트 정렬
- Precision
- 정밀도
- Rational
- 유리수
- Floating Point
- 부동소수점
- long double
- Oil
- 오일
- Drilling
- 시추
- Petroleum
- 석유
- Maximum Extraction
- 최대 추출량
- ICPC
- World Finals 2016
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12771
- 요약: 수평 선분(유전)을 한 번의 직선 시추선이 지나가며 만나는 모든 선분의 길이 합을 최대로 하라. 선분 끝점에 스치기만 해도 채취 가능하며, 서로 다른 선분들은 서로 만나지 않는다.

### 제한/스펙
- n ≤ 2000, 각 선분 좌표 |x| ≤ 1e6, y ∈ [1, 1e6]
- 시간 제한 10초, 메모리 512MB
- 어떤 두 선분도 서로 교차하거나 닿지 않음(같은 y여도 x구간이 겹치지 않음)

## 입력/출력 예시
```
예제 입력 1
5
100 180 20
30 60 30
70 110 40
10 40 50
0 80 70

예제 출력 1
200
```

```
예제 입력 2
3
50 60 10
-42 -42 20
25 0 10

예제 출력 2
25
```

## 접근 개요
- 선분 i의 양 끝점(앵커)에서 출발하는 모든 직선의 기울기 k를 고려하면, 다른 선분 j가 포함되기 위한 k의 범위가 닫힌 구간 [k_lo, k_hi]로 표현된다.
- 각 j에 대해 이 구간을 이벤트(시작, 끝)로 추가하고, k 축에서 시작 이벤트를 먼저 처리하는 스위프를 수행하면 해당 k에서 포함되는 선분 길이 합을 빠르게 갱신할 수 있다.
- 선분 끝점에 스쳐도 포함되므로 양 끝 이벤트는 모두 "포함(닫힌 구간)"으로 처리해야 한다. 기준 선분 i의 길이는 항상 포함(베이스 가중치).

## 알고리즘 설계
- 상태/전이
  - 기준: 각 선분 i의 좌/우 끝점 (총 2n개의 앵커)을 모두 시도
  - 다른 선분 j(≠i)에 대해 dy = y_j - y_i
    - dy = 0이면 교차 불가(문제 보장상 겹치지도 않음) → 스킵
    - k가 만족해야 할 범위: (x_jL - x_iA)/dy ≤ k ≤ (x_jR - x_iA)/dy (dy의 부호에 따라 자동 정렬되도록 lo/hi를 취함)
  - 이벤트: (k, type, weight) where type ∈ {start, end}, weight = 선분 j의 길이
  - 정렬: k 오름차순, 동일 k에서는 start 먼저 → 닫힌 구간 보장
- 절차
  1) i와 앵커 선택 → base = width(i)
  2) 모든 j에 대해 [k_lo, k_hi] 이벤트를 수집하고 정렬
  3) 스위프: start에서 더하고(best 갱신), 같은 k의 end는 그 다음에 빼기
  4) 모든 앵커에 대해 최대값 갱신 → 전역 최댓값 출력
- 올바름 근거(스케치)
  - 각 j의 포함 여부는 직선의 기울기 k에 대한 닫힌 범위로 정확히 기술된다(교차 혹은 끝점 접촉 포함).
  - 동일 k에서 start를 end보다 먼저 처리하면 경계에서도 포함이 유지되어 닫힌 구간을 충실히 반영한다.
  - 모든 앵커(양 끝점)를 시도함으로써, 최적 직선이 어떤 선분의 내부를 지나는 경우도 적어도 한 끝점을 통과하는 동등 기울기 집합으로 재현 가능하다.

## 복잡도
- 한 앵커에서 이벤트는 O(n), 정렬 O(n log n) → 앵커 2n개로 O(n^2 log n)
- 메모리 O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Segment {
    long long leftX;
    long long rightX;
    long long y;
    long long width;
};

struct Event {
    long double value;   // slope k
    int type;            // 0 = start (inclusive), 1 = end (inclusive)
    long long weight;    // segment width
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Segment> segs(n);
    for (int i = 0; i < n; ++i) {
        long long x0, x1, y;
        cin >> x0 >> x1 >> y;
        long long l = min(x0, x1);
        long long r = max(x0, x1);
        segs[i] = {l, r, y, r - l};
    }

    long long best = 0;
    for (int i = 0; i < n; ++i) {
        // Try both endpoints of segment i as the anchor point the line must pass through
        for (int endpoint = 0; endpoint < 2; ++endpoint) {
            long long anchorX = (endpoint == 0 ? segs[i].leftX : segs[i].rightX);
            long long anchorY = segs[i].y;

            vector<Event> events;
            events.reserve(2 * (n - 1));

            long long base = segs[i].width; // the line always intersects segment i at the anchor point

            for (int j = 0; j < n; ++j) {
                if (j == i) continue;
                long long dy = segs[j].y - anchorY;
                if (dy == 0) {
                    // Same y-level as anchor: cannot be hit due to non-overlap guarantee
                    continue;
                }
                // k in [ (leftX - anchorX)/dy , (rightX - anchorX)/dy ]
                long double k1 = (long double)(segs[j].leftX  - anchorX) / (long double)dy;
                long double k2 = (long double)(segs[j].rightX - anchorX) / (long double)dy;
                long double lo = min(k1, k2);
                long double hi = max(k1, k2);
                events.push_back({lo, 0, segs[j].width}); // start inclusive
                events.push_back({hi, 1, segs[j].width}); // end inclusive
            }

            sort(events.begin(), events.end(), [](const Event& a, const Event& b) {
                if (a.value != b.value) return a.value < b.value;
                return a.type < b.type; // start(0) before end(1)
            });

            long long current = base;
            best = max(best, current);

            for (size_t idx = 0; idx < events.size();) {
                long double v = events[idx].value;
                while (idx < events.size() && events[idx].value == v && events[idx].type == 0) {
                    current += events[idx].weight;
                    ++idx;
                }
                best = max(best, current);
                while (idx < events.size() && events[idx].value == v && events[idx].type == 1) {
                    current -= events[idx].weight;
                    ++idx;
                }
            }
        }
    }

    cout << best << "\n";
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from fractions import Fraction

input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    segs = []
    for _ in range(n):
        x0, x1, y = map(int, input().split())
        l, r = (x0, x1) if x0 <= x1 else (x1, x0)
        segs.append((l, r, y, r - l))

    best = 0
    for i in range(n):
        for endpoint in range(2):
            anchorX = segs[i][0] if endpoint == 0 else segs[i][1]
            anchorY = segs[i][2]
            base = segs[i][3]

            events = []  # (k: Fraction, type: 0 start / 1 end, weight)
            for j in range(n):
                if j == i:
                    continue
                dy = segs[j][2] - anchorY
                if dy == 0:
                    continue
                k1 = Fraction(segs[j][0] - anchorX, dy)
                k2 = Fraction(segs[j][1] - anchorX, dy)
                lo, hi = (k1, k2) if k1 <= k2 else (k2, k1)
                events.append((lo, 0, segs[j][3]))
                events.append((hi, 1, segs[j][3]))

            events.sort(key=lambda e: (e[0], e[1]))  # start(0) before end(1)

            cur = base
            if cur > best:
                best = cur
            idx = 0
            m = len(events)
            while idx < m:
                v = events[idx][0]
                while idx < m and events[idx][0] == v and events[idx][1] == 0:
                    cur += events[idx][2]
                    idx += 1
                if cur > best:
                    best = cur
                while idx < m and events[idx][0] == v and events[idx][1] == 1:
                    cur -= events[idx][2]
                    idx += 1

    print(best)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 같은 y의 다른 선분: 문제 보장상 겹치지 않으므로 교차 없음 → 스킵
- 경계 기울기(k = k_lo 또는 k_hi): 닫힌 구간이므로 포함 처리(start를 end보다 먼저)
- 매우 긴 구간/큰 좌표: 누적 합은 64-bit 정수(`long long`)로 처리
- 부동소수점 정밀도: C++은 `long double`로 충분하며, Python은 `Fraction` 사용으로 안전

## 제출 전 점검
- 입출력 형식/개행 확인, 64-bit 사용 여부, 이벤트 정렬에서 시작/끝 순서
- 기준 선분 길이(base) 포함 여부 확인

## 참고자료
- ICPC World Finals 2016 G - Oil 문제 설명


