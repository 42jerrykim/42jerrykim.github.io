---
title: "[Algorithm] C++/Python 백준 8885번: Pirate Chest - 수면 상승 고려 최대 체적"
description: "상자가 밀어낸 물로 수면이 R=(A·H)/(m·n)만큼 상승할 때, 윗면이 수면 아래에 엄격히 위치하도록 최대 부피 V=A·H를 구한다. 세로 슬라이딩 최소+단조 스택으로 A, H를 빠르게 계산."
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
- Problem-8885
- cpp
- C++
- python
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
- Sliding Window
- 슬라이딩윈도우
- Monotonic Queue
- 모노토닉 큐
- Histogram
- 히스토그램
- Largest Rectangle
- 최대직사각형
- Geometry
- 기하
- Math
- 수학
- Water Displacement
- 수위상승
- Volume
- 체적
- Binary Search
- 이분탐색
- Debugging
- 디버깅
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8885
- 요약: m×n 연못의 각 격자 깊이 `d[i][j]`가 주어질 때, 윗면이 a×b 이하(회전 가능)인 직사각형 상자를 바닥에 닿을 때까지 가라앉혀 숨긴다. 상자가 밀어낸 물의 체적만큼 수면이 `R = (A·H)/(m·n)` 상승하며, 상자의 윗면은 최종 수면보다 반드시 "엄격히 아래"에 있어야 한다. 그때 가능한 상자의 최대 체적 `V = A·H`를 구한다.

## 입력/출력
```
<입력>
a b m n
m개의 줄에 각 n개 정수 d[i][j]

예)
3 1 2 3
2 1 1
2 2 1

<출력>
최대 체적

예)
4
```

## 접근 개요
- 상자는 선택한 직사각형 영역의 최소 바닥 깊이 `minD`에 맞춰 바닥면이 먼저 닿는다. 초기 기준 수면을 0이라 하면, 상자 윗면의 깊이는 `minD − H`, 배수로 수면은 `R = (A·H)/(m·n)`만큼 상승한다.
- 엄격 잠수 조건: `(minD − H) + R > 0` ⇔ `H < (m·n·minD)/(m·n − A)`.
- 정수 높이 조건을 위해 `H = ⌊(m·n·minD − 1)/(m·n − A)⌋`로 계산하면 안전하다(= "strict" 보장).
- 따라서 고정된 `(h, w)`에 대해 `A = h·w`와 해당 영역의 `minD`만 알면 `V = A·H`를 즉시 계산 가능. 목표는 각 높이 `h`에서 모든 열에 대한 세로 슬라이딩 최소값을 구해 1차원 배열 `M`을 만들고, 이를 히스토그램 최대 직사각형 방식(단, 폭은 `≤ b`)으로 확장해 A를 최대로 만드는 것.

```mermaid
flowchart TD
  S[입력 a,b,m,n, depth] --> H[for h=1..min(a,m)]
  H --> VMIN[세로 슬라이딩 최소로 배열 M(폭 n) 계산]
  VMIN --> LNR[히스토그램 단조스택으로 각 칸의 왼/오른 경계]
  LNR --> WIDTH[폭 span 계산 후 w = min(span, b)]
  WIDTH --> Hcalc[H = floor((mn*minD - 1)/(mn - A))]
  Hcalc --> Vupd[V = A*H 로 최대값 갱신]
  Vupd --> H
  H --> Done[정답]
```

## 알고리즘 설계
- 세로 슬라이딩 최소값: 각 열마다 덱을 유지해 `h`높이 창의 최소값을 O(1) 평균으로 갱신 → 윗변이 행 `r`에 올 때 `M[c] = 창 최소`.
- 히스토그램 확장: `M`에 대해 단조 증가 스택으로 각 인덱스 `c`의 "자신이 최소가 되는 최대 구간" 길이 `span`을 구함. 폭은 `w = min(span, b)`로 제한해 `A = h·w` 산출.
- 높이 계산: `N = m·n`, `H = ⌊(N·M[c] − 1)/(N − A)⌋`.
- 부피 갱신: `V = A·H`의 최댓값을 전역 갱신. a×b와 b×a 양 방향 모두 실행.

## 복잡도
- 세로 슬라이딩 최소 + 히스토그램 한 번에 O(n). 이를 각 행과 `h`에 대해 수행 → 전체 대략 O(m·n·(a + b)).
- 조건 범위(`≤ 500`)에서 C++은 충분, Python은 구현 최적화 권장.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static inline long long compute_best(const vector<vector<int>>& depth, int m, int n, int HBoundIn, int WBoundIn) {
    const long long MN = 1LL * m * n;
    int HBound = min(HBoundIn, m);
    int WBound = min(WBoundIn, n);

    long long best = 0;

    vector<deque<pair<int,int>>> colDeq(n);
    vector<int> M(n), leftIdx(n), rightIdx(n), st(n);

    for (int h = 1; h <= HBound; ++h) {
        for (int c = 0; c < n; ++c) colDeq[c].clear();

        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                while (!colDeq[c].empty() && colDeq[c].back().first >= depth[r][c]) colDeq[c].pop_back();
                colDeq[c].emplace_back(depth[r][c], r);
            }
            if (r >= h - 1) {
                int start = r - h + 1;
                for (int c = 0; c < n; ++c) {
                    while (!colDeq[c].empty() && colDeq[c].front().second < start) colDeq[c].pop_front();
                    M[c] = colDeq[c].front().first;
                }

                int top = -1;
                for (int c = 0; c < n; ++c) {
                    while (top >= 0 && M[st[top]] >= M[c]) --top;
                    leftIdx[c] = (top < 0 ? -1 : st[top]);
                    st[++top] = c;
                }
                top = -1;
                for (int c = n - 1; c >= 0; --c) {
                    while (top >= 0 && M[st[top]] >= M[c]) --top;
                    rightIdx[c] = (top < 0 ? n : st[top]);
                    st[++top] = c;
                }

                for (int c = 0; c < n; ++c) {
                    int widthSpan = rightIdx[c] - leftIdx[c] - 1;
                    if (widthSpan <= 0) continue;
                    int w = widthSpan < WBound ? widthSpan : WBound;
                    if (w <= 0) continue;

                    long long A = 1LL * h * w;
                    if (A >= MN) continue;

                    long long numer = MN * (long long)M[c] - 1; // strict inequality
                    if (numer <= 0) continue;
                    long long denom = MN - A;
                    long long H = numer / denom;
                    if (H <= 0) continue;

                    long long V = A * H;
                    if (V > best) best = V;
                }
            }
        }
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a, b, m, n;
    if (!(cin >> a >> b >> m >> n)) return 0;
    vector<vector<int>> depth(m, vector<int>(n));
    for (int i = 0; i < m; ++i) for (int j = 0; j < n; ++j) cin >> depth[i][j];

    long long ans = 0;
    ans = max(ans, compute_best(depth, m, n, a, b));
    ans = max(ans, compute_best(depth, m, n, b, a));
    cout << ans << "\n";
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

input = sys.stdin.readline


def compute_best(depth, m, n, HBoundIn, WBoundIn):
    N = m * n
    HBound = min(HBoundIn, m)
    WBound = min(WBoundIn, n)

    best = 0
    col_deq = [deque() for _ in range(n)]
    M = [0] * n
    left = [0] * n
    right = [0] * n
    st = [0] * n

    for h in range(1, HBound + 1):
        for c in range(n):
            col_deq[c].clear()
        for r in range(m):
            row = depth[r]
            for c in range(n):
                dc = col_deq[c]
                val = row[c]
                while dc and dc[-1][0] >= val:
                    dc.pop()
                dc.append((val, r))
            if r >= h - 1:
                start = r - h + 1
                for c in range(n):
                    dc = col_deq[c]
                    while dc and dc[0][1] < start:
                        dc.popleft()
                    M[c] = dc[0][0]

                top = -1
                for c in range(n):
                    while top >= 0 and M[st[top]] >= M[c]:
                        top -= 1
                    left[c] = st[top] if top >= 0 else -1
                    top += 1
                    st[top] = c

                top = -1
                for c in range(n - 1, -1, -1):
                    while top >= 0 and M[st[top]] >= M[c]:
                        top -= 1
                    right[c] = st[top] if top >= 0 else n
                    top += 1
                    st[top] = c

                for c in range(n):
                    width_span = right[c] - left[c] - 1
                    if width_span <= 0:
                        continue
                    w = width_span if width_span < WBound else WBound
                    if w <= 0:
                        continue
                    A = h * w
                    if A >= N:
                        continue
                    numer = N * M[c] - 1
                    if numer <= 0:
                        continue
                    denom = N - A
                    H = numer // denom
                    if H <= 0:
                        continue
                    V = A * H
                    if V > best:
                        best = V
    return best


def main():
    a, b, m, n = map(int, input().split())
    depth = [list(map(int, input().split())) for _ in range(m)]
    ans = 0
    ans = max(ans, compute_best(depth, m, n, a, b))
    ans = max(ans, compute_best(depth, m, n, b, a))
    print(ans)


if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- `a=1` 또는 `b=1`처럼 매우 얇은 상단
- `minD=0`가 포함된 영역(정답 0 가능)
- `A`가 `m·n`에 매우 근접(분모 안정성 확인)
- 깊이가 균일/단조/체크무늬 등 패턴
- 최대치 입력(성능 확인)

## 참고자료
- 문제: https://www.acmicpc.net/problem/8885

