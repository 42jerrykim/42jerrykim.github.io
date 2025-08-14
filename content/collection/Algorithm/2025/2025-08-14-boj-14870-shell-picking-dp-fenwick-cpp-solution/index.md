---
title: "[Algorithm] cpp 백준 14870번: 조개 줍기"
description: "N×N 격자에서 각 칸의 조개 최대 개수가 주어질 때, 위/왼쪽으로만 이동하는 경로 최대합 DP를 모든 시작 칸에 대해 합산하고, 단위(±1) 갱신마다 영향 범위를 ‘계단’으로 추적해 행별 Fenwick(범위가산·점질의)으로 O(N^2 log N) 시간에 합을 갱신하는 풀이를 정리합니다. 올바름 근거와 엣지 케이스 점검까지 포함했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- DP
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14870
- cpp
- C++
- Dynamic Programming
- 동적계획법
- DP
- Grid
- 격자
- Staircase
- 계단 경계
- Fenwick Tree
- 펜윅트리
- BIT
- Binary Indexed Tree
- Range Add
- 구간 가산
- Point Query
- 점 질의
- Range Update
- 구간 업데이트
- Prefix Sum
- 누적합
- Propagation
- 전파
- Monotone
- 단조 경계
- Update Propagation
- 갱신 전파
- KOI
- KOI 2017
- 한국정보올림피아드
- Subtask
- 서브태스크
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
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
- Data Structures
- 자료구조
- Grid DP
- 격자 DP
- 2D DP
- 2차원 DP
- Online Updates
- 온라인 업데이트
- Incremental Update
- 단위 갱신
- Range to Point
- 구간→점
- O(N^2 log N)
- Long Long
- 64-bit
- Fast IO
- 빠른 입출력
- Invariant
- 불변식
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14870
- 요약: `N×N` 격자에서 각 칸의 가치가 주어질 때, 각 칸에서 좌상단(수산시장)으로 위/왼쪽 이동만 허용되는 경로의 최대 누적 가치를 구한다. 모든 칸에 대해 이 최대값을 합산한 값을 출력하고, 이후 `N`개의 단위 갱신(특정 칸 값을 +1 또는 −1)에 대해 매번 갱신 반영 후 합을 다시 출력한다.

## 입력/출력
```
입력
N
v11 v12 ... v1N
...
vN1 vN2 ... vNN
op1 r1 c1
...
opN rN cN

출력
초기 합
각 갱신 후 합 (총 N줄)
```

예제
```
입력
3
3 2 7
4 2 6
5 3 8
U 1 2
D 3 2
U 1 2

출력
107
111
110
114
```

## 접근 개요
- 핵심 DP: `best[i][j] = max(best[i-1][j], best[i][j-1]) + a[i][j]`로 각 칸의 최대 누적 값을 구하고, 전 칸의 합을 취한다.
- 단위 갱신(±1) 시 영향: DP 의존성이 좌/상 방향뿐이라, 한 칸 변화의 영향은 우/하 방향으로만 전파되며 각 행에서 연속 구간으로 나타난다. 전체 영향 영역은 단조롭게 진행되는 ‘계단(staircase)’ 형태.
- 자료구조: 각 행마다 Fenwick Tree를 두어 “구간 가산, 점 질의”를 지원한다. 갱신 시 해당 행의 연속 구간에 ±1을 더하고, 합은 길이×증가량으로 보정한다.

## 알고리즘
1) 초기화
   - `dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + a[i][j]`를 O(N^2)로 계산, `total = Σ dp[i][j]` 저장.
   - 각 행 `i`에 Fenwick Tree 준비(크기 N). 초기에는 0.
2) 한 번의 갱신 `(r,c,delta)`, `delta ∈ {+1, −1}` 처리
   - `get(i,j) = dp[i][j] + add[i].point(j)`를 정의(add[i]는 i행 Fenwick). `get`은 현재까지의 누적 증가분을 포함한 DP값을 의미.
   - 우상/좌하 전이의 비교식으로 단조 경계(계단)를 따라가며, 각 행 `i`에 대해 영향 구간 `[s[i], e[i]]`를 계산.
   - 모든 `i`에 대해 `s[i] ≤ e[i]`이면 `add[i].rangeAdd(s[i], e[i], delta)` 수행, `total += delta × (e[i] − s[i] + 1)`.
3) 출력: 초기 `total`, 이후 매 갱신 후의 `total`을 즉시 출력.

올바름 근거
- `best[i][j]`는 좌/상 두 값 중 큰 쪽에 현재 칸을 더한 값이므로, 단위 변경이 영향을 미치는 경로는 비교식이 바뀌는 경계(타이브레이크 포함)로 한정된다.
- 이 경계는 오른쪽/아래로만 이동하는 단조 경로이며, 각 행에서 연속 구간이 된다. 구간에 동일한 ±1을 더하면 합은 길이에 비례해 변한다.
- 행별 Fenwick으로 구간 가산을 상수계수로 처리하고, `get` 질의는 점 질의로 O(log N)에 가능하다.

## 복잡도
- 시간: O(N^2 log N) — 갱신마다 경계 추적 O(N) × 행별 Fenwick 연산 O(log N)
- 공간: O(N^2) — `dp`와 원본 그리드 보관, + O(N^2) 미만의 Fenwick 배열

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 1515;

int n;
long long arrv[MAXN][MAXN];
long long dp[MAXN][MAXN];
long long totalSum;

struct BIT {
    long long tree[MAXN];
    void update(int l, int r, int v){
        if(l > r) return;
        for(; l <= n; l += l & -l) tree[l] += v;
        for(r++; r <= n; r += r & -r) tree[r] -= v;
    }
    long long query(int x) const {
        long long ret = 0;
        for(; x; x ^= x & -x) ret += tree[x];
        return ret;
    }
} bitRow[MAXN];

inline long long getVal(int i, int j){
    if(i <= 0 || j <= 0) return 0;
    return dp[i][j] + bitRow[i].query(j);
}

void buildDP(){
    totalSum = 0;
    for(int i = 1; i <= n; ++i){
        for(int j = 1; j <= n; ++j){
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + arrv[i][j];
            totalSum += dp[i][j];
        }
    }
}

void applyUpdate(int a, int b, int c){
    static int s[MAXN], e[MAXN];

    // initialize segments
    for(int i = a + 1; i <= n; ++i) s[i] = n + 1, e[i] = 0;
    s[a] = e[a] = b;

    // compute right boundary e[i]
    {
        int i = a, j = b;
        while(true){
            if(j < n && max(getVal(i-1, j+1), getVal(i, j)) + c ==
                        max(getVal(i-1, j+1), getVal(i, j) + c)){
                ++j;
            }else{
                ++i;
            }
            if(i > n) break;
            e[i] = j;
        }
    }

    // compute left boundary s[i]
    {
        int i = a, j = b;
        while(true){
            if(i < n && max(getVal(i+1, j-1), getVal(i, j)) + c ==
                        max(getVal(i+1, j-1), getVal(i, j) + c)){
                ++i;
            }else{
                ++j;
            }
            if(j > n || e[i] < j) break;
            s[i] = min(s[i], j);
        }
    }

    // apply row-wise range adds and fix total sum
    for(int i = a; i <= n; ++i){
        if(s[i] <= e[i]){
            bitRow[i].update(s[i], e[i], c);
            totalSum += 1LL * c * (e[i] - s[i] + 1);
        }
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if(!(cin >> n)) return 0;
    for(int i = 1; i <= n; ++i){
        for(int j = 1; j <= n; ++j){
            cin >> arrv[i][j];
        }
    }

    buildDP();
    cout << totalSum << '\n';

    for(int qi = 1; qi <= n; ++qi){
        char op; int r, c; cin >> op >> r >> c;
        applyUpdate(r, c, op == 'U' ? +1 : -1);
        cout << totalSum << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `r=c=1`(시장 위치) 갱신 포함 여부와 경계 처리(인접 참조는 0으로 가정)
- 동일 위치에 연속된 `U/D` 갱신이 섞여 오는 경우의 상쇄
- 열/행 끝(`j=n` 또는 `i=n`)에서의 경계 전파 중단 조건
- 모든 값이 0이거나 큰 값 혼재 시 `long long` 합 범위 확인

## 제출 전 점검
- 입출력 버퍼링 설정과 개행 형식 확인
- 인덱싱: 모든 배열은 1-based, Fenwick도 1-based 유지
- 비교식 동치 처리: `max` 두 항의 상대크기 변화가 경계를 정의함을 재확인

## 참고자료
- 문제: https://www.acmicpc.net/problem/14870
- 풀이 아이디어(경계 추적, 행별 Fenwick): JusticeHui 블로그 – “백준14870 조개 줍기”


