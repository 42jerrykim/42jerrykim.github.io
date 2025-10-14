---
title: "[Algorithm] 겹치는 구간 판별: 반열림 구간과 드모르간으로 단순화"
description: "구간 겹침은 ‘겹친다’를 직접 나열하기보다 ‘겹치지 않는다’를 부정해 얻는 식이 더 간단합니다. 반열림 [start, end) 규약과 드모르간 법칙으로 1D/2D 겹침 판별을 안정적으로 유도하고, 언어별 구현·오프바이원·시간/날짜·부동소수점 함정까지 실무 관점으로 정리합니다."
date: 2025-10-14
lastmod: 2025-10-14
categories:
  - Algorithm
  - Math
tags:
  - Interval
  - Intervals
  - Overlap
  - Overlapping
  - Interval Overlap
  - Half-open Interval
  - Closed Interval
  - Open Interval
  - De Morgan
  - De Morgan's Laws
  - Boolean Algebra
  - Case Analysis
  - Scheduling
  - Time Range
  - Date Range
  - Range Intersection
  - Segment Intersection
  - AABB
  - Axis-Aligned Bounding Box
  - Box Overlap
  - Collision Detection
  - Geometry
  - Computational Geometry
  - Algorithm
  - 알고리즘
  - 구간
  - 구간 겹침
  - 반열림 구간
  - 폐구간
  - 개구간
  - 드모르간 법칙
  - 불 대수
  - 케이스 분석
  - 스케줄링
  - 시간 구간
  - 날짜 범위
  - 교집합
  - 구간 교집합
  - 직사각형 겹침
  - 충돌 감지
  - 기하학
  - 계산기하
  - 조건식
  - 오프바이원
  - 성능 최적화
  - Robustness
  - Predicate
  - Inequality
  - Comparison
  - Python
  - C++
  - JavaScript
  - TypeScript
  - Edge Cases
  - Floating Point
  - 부동소수점
  - 정수
image: wordcloud.png
---

반복적으로 등장하지만 자주 실수하는 문제 중 하나가 “두 구간이 겹치는가?”입니다. 핵심은 반열림 규약과 부정(negation)입니다. 반열림 \([start, end)\)을 채택하면 오프바이원을 크게 줄일 수 있고, “겹친다”를 직접 나열하기보다는 “겹치지 않는다”의 부정을 통해 더 단순한 판별식을 얻을 수 있습니다. 좋은 정리는 간단한 술어(predicate)에서 시작합니다.

참고: 본 글의 구조적 아이디어와 예시는 "How to check for overlapping intervals"에서 제시한 부정 기반 접근을 바탕으로 재구성했습니다. 상세 설명과 도형은 원문을 참고하세요.

- 원문: [How to check for overlapping intervals](https://zayenz.se/blog/post/how-to-check-for-overlapping-intervals/)

## 1차원 구간: 반열림 [start, end)

두 반열림 구간 \([aStart, aEnd), [bStart, bEnd)\)이 겹치는 충분조건·필요조건은 다음과 같이 깔끔합니다.

\[ a \text{와 } b \text{가 겹침} \iff bStart < aEnd \;\land\; aStart < bEnd \]

이 식은 “겹치지 않는다”의 두 경우(\(a\)가 \(b\)보다 앞, 또는 뒤)를 부정해 얻습니다.

\[ \lnot(aEnd \le bStart \;\lor\; bEnd \le aStart) \equiv (bStart < aEnd) \land (aStart < bEnd) \]

### 파이썬

```python
def overlaps_half_open(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    # [a_start, a_end) and [b_start, b_end)
    return (b_start < a_end) and (a_start < b_end)

def overlaps_closed(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    # [a_start, a_end] and [b_start, b_end]
    return (b_start <= a_end) and (a_start <= b_end)
```

### 자바스크립트/타입스크립트

```ts
export function overlapsHalfOpen(aStart: number, aEnd: number, bStart: number, bEnd: number): boolean {
  return bStart < aEnd && aStart < bEnd;
}

export function overlapsClosed(aStart: number, aEnd: number, bStart: number, bEnd: number): boolean {
  return bStart <= aEnd && aStart <= bEnd;
}
```

### C++

```cpp
#include <algorithm>
#include <cstdint>

bool overlaps_half_open(int64_t aStart, int64_t aEnd, int64_t bStart, int64_t bEnd) {
    return (bStart < aEnd) && (aStart < bEnd);
}

bool overlaps_closed(int64_t aStart, int64_t aEnd, int64_t bStart, int64_t bEnd) {
    return (bStart <= aEnd) && (aStart <= bEnd);
}
```

### 교집합 기반 동일식

교집합을 직접 만들면 직관이 더욱 분명해집니다. 반열림 규약에서는 다음이 동치입니다.

\[ [\max(aStart,bStart),\; \min(aEnd,bEnd)) \text{가 비어있지 않다} \iff \max < \min \]

```python
def overlaps_via_intersection(a_start, a_end, b_start, b_end):
    inter_start = max(a_start, b_start)
    inter_end = min(a_end, b_end)
    return inter_start < inter_end
```

## 2차원 직사각형(AABB): 축 정렬 상자 겹침

축에 정렬된 두 상자 \(A = [Ax1, Ax2) \times [Ay1, Ay2), B = [Bx1, Bx2) \times [By1, By2)\)는 두 축 모두에서 1차원 겹침이 성립해야 겹칩니다.

\[ Bx1 < Ax2 \land Ax1 < Bx2 \land By1 < Ay2 \land Ay1 < By2 \]

```python
def box_overlaps(a, b) -> bool:
    # a, b have fields x1, x2, y1, y2 with [x1,x2), [y1,y2)
    return (b.x1 < a.x2) and (a.x1 < b.x2) and (b.y1 < a.y2) and (a.y1 < b.y2)
```

위 식은 1차원 판별의 곱(AND)입니다. 한 축이라도 겹치지 않으면 상자도 겹치지 않습니다.

## 실무 함정과 체크리스트

- 오프바이원: 정수 인덱스, 날짜 범위에서는 반열림 \([start, end)\)로 표현하면 경계 처리가 단순해집니다. 예: 하루 단위는 \([2025-01-01, 2025-01-02)\).
- 폐구간 혼용: 양쪽이 모두 폐구간이면 `<=`로 바뀝니다. 혼합 규약([start, end), [start, end])은 피하세요.
- 시간/타임존: 날짜·시간은 타임존, 서머타임 전환에 주의하세요. 가급적 UTC 타임스탬프(정수 ms/초)로 변환 후 반열림 규약을 적용합니다. 참고: [Baeldung — Check if Two Date Ranges Overlap](https://www.baeldung.com/java-check-two-date-ranges-overlap)
- 부동소수점: 경계가 부동소수점이면 정수 스케일(예: 센티초)로 변환하거나, 엄격 비교에 작은 여유(ε)를 도입합니다.
- 비정상 구간: 입력 검증으로 `start <= end`(반열림에서 빈 구간 허용 시 `start == end`)을 보장하세요.
- 성질 테스트: 대칭성, 교환 법칙(인자 순서 바뀌어도 결과 동일), 빈 교집합 판정과의 동치 등을 단위테스트에 포함합니다.

## 대량 데이터에서의 응용

- 선 스윕(sweep line): 많은 구간의 모든 겹침을 찾을 때는 시작·끝을 정렬해 선 스윕으로 \(O(n \log n + k)\)에 처리합니다.
- 인덱스 구조: 동적 질의·갱신에는 인터벌 트리, 세그먼트 트리, 구간 트리를 검토하세요.

## 요약

- 반열림 \([start, end)\)을 채택하면 경계 오류가 줄어듭니다.
- “겹치지 않는다”를 부정해 얻은 식이 가장 단순합니다: `bStart < aEnd && aStart < bEnd`.
- 2D는 축별 겹침의 AND입니다. 실제 시스템에서는 시간대·부동소수점·데이터 정합성 검증까지 포함해 방어적으로 구현하세요.

## 참고 자료

- [How to check for overlapping intervals — zayenz.se](https://zayenz.se/blog/post/how-to-check-for-overlapping-intervals/)
- [Interval (mathematics) — Wikipedia](https://en.wikipedia.org/wiki/Interval_(mathematics))
- [What's the most efficient way to test if two ranges overlap? — Stack Overflow](https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-if-two-ranges-overlap)
- [Check if Two Date Ranges Overlap — Baeldung](https://www.baeldung.com/java-check-two-date-ranges-overlap)
- [Lobsters discussion of the article](https://lobste.rs/s/cireck/how_check_for_overlapping_intervals)


