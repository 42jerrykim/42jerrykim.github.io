---
title: "[Algorithm] C++ 백준 8131번: Ploughing - 슬라이딩 윈도우"
description: "2000×2000 격자에서 합 ≤ K인 바깥 행·열만 제거하며 제거 횟수를 최소화한다. 마지막 1×L 또는 L×1 스트립 길이 최대화로 환원하고, 2D 누적합+투포인터로 O((N+M)^2) 해결. 경계 우선 그리디 핵심."
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
- Problem-8131
- Ploughing
- POI
- POI 2005/2006
- Sliding Window
- 슬라이딩윈도우
- Two Pointers
- 투포인터
- Greedy
- 그리디
- Prefix Sum
- 누적합
- 2D Prefix Sum
- 2차원누적합
- Submatrix Sum
- 부분행렬합
- Border Removal
- 경계 제거
- Rectangle
- 직사각형
- Row Removal
- 행 제거
- Column Removal
- 열 제거
- Window Expansion
- 윈도우 확장
- Check Function
- 검증 함수
- Prefix Query
- 구간합
- O((N+M)^2)
- 시간복잡도 O((N+M)^2)
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
- Testing
- 테스트
- C++
- cpp
- Implementation
- 구현
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8131
- 요약: N×M 격자에서 한 번에 바깥쪽 네 변 중 하나(위/아래 행 또는 왼/오른 열)를 선택해 제거한다. 제거되는 원소들의 합이 항상 K 이하이어야 한다. 전부 제거하는 데 필요한 최소 횟수를 구한다. (입력은 `k m n` 순이며, 이후 n줄에 m개의 값이 주어진다.)
- 제한: 1 ≤ K ≤ 2e8, 1 ≤ M,N ≤ 2000, 각 칸의 난이도 계수는 양의 정수

## 입력/출력
```
입력
k m n
n줄에 각 줄마다 m개의 정수 (난이도 계수)

출력
최소 제거 횟수
```

## 접근 개요
- 핵심 관찰: 마지막 제거는 반드시 1×K' 또는 K'×1 형태의 "길쭉한 스트립"이 된다. 이때 총 제거 횟수는 (N−1)+(M−K') 또는 (N−K')+(M−1) 꼴이므로, 결국 K'를 최대화하는 문제가 된다.
- 판별로 바꾸기: 가로 스트립을 남기는 경우, 어떤 열 구간 [L,R]을 최종 스트립으로 만들 수 있는지 확인한다. 세로 스트립도 대칭적으로 동일하다.
- `가능성 판별(CHK)`: 현 직사각형 경계(top,bottom,left,right)를 유지하며, 합 ≤ K인 쪽을 우선적으로 깎아내는 그리디를 적용한다. 마지막 1×(R−L+1) 직사각형만 남기기까지 (N+M−(R−L+1)−1)번의 제거를 수행한 뒤, 남은 스트립의 합 ≤ K면 성공.
- 최적화: 2D 누적합으로 경계합/직사각형합을 O(1)에 구하고, [L,R]을 투포인터로 한 번씩만 확장/축소해 전체 O((N+M)^2)에 해결.

## 알고리즘 설계
- 2D Prefix Sum `S`: `sumRect(r1,c1,r2,c2)`를 O(1)로 계산.
- 가로 스트립
  - 두 포인터 L,R(열)을 유지하며, 각 [L,R]에 대해 `CHK_horizontal(L,R)` 수행.
  - `CHK_horizontal`: (1) 위/아래 행을 먼저 제거(가능할 때), (2) 남기려는 [L,R] 바깥 열만 제거. 정해진 횟수만큼 진행 후 마지막 스트립 합 ≤ K 확인.
- 세로 스트립
  - 두 포인터 T,B(행)를 유지하며, `CHK_vertical(T,B)`를 가로와 대칭적으로 수행.
- 정답은 두 경우에서의 최소 제거 횟수.

## 복잡도
- 시간: O((N+M)^2)
- 공간: O(NM)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static int numRows, numCols;
static long long limitK;
static vector<vector<long long>> prefixSum; // 1-based inclusive prefix sums

inline long long sumRect(int topRow, int leftCol, int bottomRow, int rightCol) {
    if (topRow > bottomRow || leftCol > rightCol) return 0LL;
    return prefixSum[bottomRow][rightCol]
         - prefixSum[topRow - 1][rightCol]
         - prefixSum[bottomRow][leftCol - 1]
         + prefixSum[topRow - 1][leftCol - 1];
}

// Keep columns [keepLeft, keepRight], end with 1 x (keepRight-keepLeft+1)
bool canEndWithHorizontalStripe(int keepLeft, int keepRight) {
    int top = 1, bottom = numRows, left = 1, right = numCols;
    const int targetWidth = keepRight - keepLeft + 1;
    const int stepsBeforeLast = (numRows + numCols) - targetWidth - 1;

    for (int step = 0; step < stepsBeforeLast; ++step) {
        // Prefer removing a row if possible
        if (bottom - top + 1 > 1 && sumRect(top, left, top, right) <= limitK) { top++; continue; }
        if (bottom - top + 1 > 1 && sumRect(bottom, left, bottom, right) <= limitK) { bottom--; continue; }
        // Then remove columns only outside the target interval
        if (left < keepLeft && sumRect(top, left, bottom, left) <= limitK) { left++; continue; }
        if (right > keepRight && sumRect(top, right, bottom, right) <= limitK) { right--; continue; }
        return false;
    }
    return sumRect(top, left, bottom, right) <= limitK;
}

// Keep rows [keepTop, keepBottom], end with (keepBottom-keepTop+1) x 1
bool canEndWithVerticalStripe(int keepTop, int keepBottom) {
    int top = 1, bottom = numRows, left = 1, right = numCols;
    const int targetHeight = keepBottom - keepTop + 1;
    const int stepsBeforeLast = (numRows + numCols) - targetHeight - 1;

    for (int step = 0; step < stepsBeforeLast; ++step) {
        // Prefer removing a column if possible
        if (right - left + 1 > 1 && sumRect(top, left, bottom, left) <= limitK) { left++; continue; }
        if (right - left + 1 > 1 && sumRect(top, right, bottom, right) <= limitK) { right--; continue; }
        // Then remove rows only outside the target interval
        if (top < keepTop && sumRect(top, left, top, right) <= limitK) { top++; continue; }
        if (bottom > keepBottom && sumRect(bottom, left, bottom, right) <= limitK) { bottom--; continue; }
        return false;
    }
    return sumRect(top, left, bottom, right) <= limitK;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Input: k m n (as in the official statement)
    long long kInput;
    int mInput, nInput;
    if (!(cin >> kInput >> mInput >> nInput)) return 0;
    limitK = kInput;
    numCols = mInput;
    numRows = nInput;

    prefixSum.assign(numRows + 1, vector<long long>(numCols + 1, 0));

    for (int i = 1; i <= numRows; ++i) {
        for (int j = 1; j <= numCols; ++j) {
            long long v; cin >> v;
            prefixSum[i][j] = v + prefixSum[i - 1][j] + prefixSum[i][j - 1] - prefixSum[i - 1][j - 1];
        }
    }

    int best = INT_MAX;

    // Horizontal final stripe (1 x width)
    {
        int l = 1, r = 1;
        while (true) {
            bool ok = canEndWithHorizontalStripe(l, r);
            if (ok) best = min(best, numRows + numCols - (r - l + 1));

            if (l == numCols && r == numCols) break;
            if (r == numCols) l++;
            else if (l == r) r++;
            else if (ok) r++;
            else l++;
        }
    }

    // Vertical final stripe (height x 1)
    {
        int t = 1, b = 1;
        while (true) {
            bool ok = canEndWithVerticalStripe(t, b);
            if (ok) best = min(best, numRows + numCols - (b - t + 1));

            if (t == numRows && b == numRows) break;
            if (b == numRows) t++;
            else if (t == b) b++;
            else if (ok) b++;
            else t++;
        }
    }

    cout << best << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- N=1 또는 M=1인 단일 축 스트립만 있는 경우
- K가 매우 작아 경계 한 쪽만 반복적으로 지워야 하는 경우
- 큰 값이 한쪽에 몰려 있어 특정 구간 [L,R]/[T,B]만 가능한 경우
- 모든 경계 합이 항상 K 이하/이상인 극단 케이스

## 제출 전 점검
- 입출력 순서: `k m n` 주의, 빠른 입출력 사용 여부
- 2D 누적합 인덱싱(1-based)과 `sumRect` 경계 확인
- 마지막 스트립 합 ≤ K 확인 누락 여부
- 오버플로: 누적합은 `long long` 사용

## 참고자료
- 문제: https://www.acmicpc.net/problem/8131
- 해설: JusticeHui, “백준8131 Ploughing” — https://justicehui.github.io/poi/2020/07/12/BOJ8131/
- 해설: Amel, “백준 8131 Ploughing (POI 2005/2006)” — https://amelamel.tistory.com/21


