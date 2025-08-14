---
title: "[Algorithm] cpp 백준 15977번: 조화로운 행렬 - 3D LIS/CDQ"
description: "KOI 2018 ‘조화로운 행렬’ 풀이. 열-부분행렬의 등수행렬이 모든 행에서 동일해지는 최대 열 길이를 구한다. M=2는 1행 정렬 순서에서 2행 등수의 LIS, M=3은 CDQ 분할정복+펜윅 트리로 3차원 LIS를 계산한다. 증명과 엣지 케이스, 구현 포인트를 함께 정리했다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Dynamic Programming"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-15977"
- "cpp"
- "C++"
- "Data Structures"
- "자료구조"
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
- "Dynamic Programming"
- "동적계획법"
- "LIS"
- "Longest Increasing Subsequence"
- "3D LIS"
- "2D LIS"
- "CDQ Divide and Conquer"
- "CDQ"
- "Divide and Conquer"
- "분할정복"
- "Fenwick Tree"
- "펜윅트리"
- "BIT"
- "Binary Indexed Tree"
- "Order Statistics"
- "Rank Matrix"
- "등수행렬"
- "조화로운 행렬"
- "Harmonious Matrix"
- "KOI"
- "KOI 2018"
- "Coordinate Compression"
- "좌표압축"
- "Strictly Increasing"
- "증가수열"
- "Sequence"
- "수열"
- "Sorting"
- "정렬"
- "Implementation Details"
- "구현 디테일"
image: "wordcloud.png"
---

### 문제

- 링크: [BOJ 15977: 조화로운 행렬](https://www.acmicpc.net/problem/15977)
- 요약: 2×N 또는 3×N 행렬에서 열 몇 개를 골라 붙여 만든 열-부분행렬의 등수행렬이 모든 행에서 일치하도록 할 때, 가능한 최대 열 개수를 구한다. 원소는 모두 서로 다른 양의 정수이며, 등수는 각 행에서 내림차순 기준(큰 값 1등)이다.

### 입력/출력

- 입력: 첫 줄에 행의 개수 M(2 또는 3), 열의 개수 N(3 ≤ N ≤ 200,000). 이어서 M개의 줄에 각 행의 N개 원소가 주어진다.
- 출력: 조건을 만족하는 조화로운 열-부분행렬의 최대 열 개수.

예시 (문제 제공):

```
입력
3 9
10 74 41 15 89 52 16 63 75
30 53 22 33 46 45 25 47 21
29 49 13 26 59 17 62 34 19

출력
4
```

### 접근 개요

- 핵심 관찰: 선택한 열들의 각 행별 상대적 순위(등수)가 모든 행에서 동일해야 한다. 즉, 한 행을 기준으로 열을 정렬한 뒤 다른 행들의 등수열을 보면, 조화로운 부분은 모든 기준에서 동시에 증가하는 공통 순서가 된다.
- 모델링: 각 열 `j`를 각 행의 등수 `(r1[j], r2[j], r3[j])`로 표현하면, 답은 `(r1, r2)`의 증가 부분수열 길이(M=2) 또는 `(r1, r2, r3)`의 공증가 사슬 길이(M=3)와 같다. 여기서 `r1`은 정렬 기준이므로 자동 증가로 만들 수 있다.

### 알고리즘 설계

1) 행별 등수 전처리
- 각 행을 값 오름차순으로 정렬하여 열 인덱스별 등수(1..N)를 부여한다. 이때 값이 모두 다르므로 동률 등수가 없다.

2) M=2: 1차원 LIS
- 1행 등수 순서대로 열을 나열하면 2행 등수의 수열이 된다. 이 수열의 길이가 조화로운 열-부분행렬의 최대 길이와 동일하다.
- 표준 LIS(O(N log N))로 계산한다. (Strictly increasing 필요)

3) M=3: 3차원 LIS → CDQ 분할정복 + Fenwick 트리
- `(k = r1, x = r2, y = r3)` 튜플을 `k` 오름차순으로 정렬한다.
- 목표: `k1 < k2`, `x1 < x2`, `y1 < y2`를 만족하는 최대 길이 체인.
- CDQ 분할정복으로 구간을 반으로 나누고, 왼쪽의 결과를 오른쪽으로 전파한다.
  - 왼쪽/오른쪽을 `x`(=r2) 기준으로 정렬해 스위핑하며, `y`(=r3)에 대해 Fenwick에서 `dp`의 최댓값을 질의·갱신한다.
  - `x`는 왼쪽 `<` 오른쪽, `y`는 `y-1`까지 질의하여 엄격 증가를 보장한다.
- 전체 시간복잡도는 O(N log^2 N), 공간복잡도는 O(N).

### 복잡도

- M=2: 시간 O(N log N), 공간 O(N)
- M=3: 시간 O(N log^2 N), 공간 O(N)

### 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<int> bit;
    Fenwick() : n(0) {}
    explicit Fenwick(int n_) { init(n_); }
    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }
    void update(int idx, int val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] = max(bit[idx], val);
    }
    int query(int idx) const {
        int res = 0;
        for (; idx > 0; idx -= idx & -idx) res = max(res, bit[idx]);
        return res;
    }
    void clearIndex(int idx) {
        for (int i = idx; i <= n; i += i & -i) bit[i] = 0;
    }
};

struct Node {
    int k;   // rank in row1 (1..N)
    int x;   // rank in row2 (1..N)
    int y;   // rank in row3 (1..N), 0 if M=2
    int dp;  // LIS length ending here
};

int M, N;

void cdq_solve(vector<Node> &a, int l, int r, Fenwick &fw) {
    if (l == r) return;
    int mid = (l + r) >> 1;
    cdq_solve(a, l, mid, fw);

    vector<int> L, R;
    L.reserve(mid - l + 1);
    R.reserve(r - mid);
    for (int i = l; i <= mid; ++i) L.push_back(i);
    for (int i = mid + 1; i <= r; ++i) R.push_back(i);

    auto by_x = [&](int i, int j) {
        return a[i].x < a[j].x;
    };
    sort(L.begin(), L.end(), by_x);
    sort(R.begin(), R.end(), by_x);

    vector<int> updatedYs;
    updatedYs.reserve(L.size());
    int p = 0;
    for (int idx : R) {
        while (p < (int)L.size() && a[L[p]].x < a[idx].x) {
            fw.update(a[L[p]].y, a[L[p]].dp);
            updatedYs.push_back(a[L[p]].y);
            ++p;
        }
        int best = fw.query(a[idx].y - 1); // strict y_left < y_right
        a[idx].dp = max(a[idx].dp, best + 1);
    }
    if (!updatedYs.empty()) {
        sort(updatedYs.begin(), updatedYs.end());
        updatedYs.erase(unique(updatedYs.begin(), updatedYs.end()), updatedYs.end());
        for (int y : updatedYs) fw.clearIndex(y);
    }

    cdq_solve(a, mid + 1, r, fw);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> M >> N)) return 0;
    vector<vector<int>> val(M, vector<int>(N));
    for (int i = 0; i < M; ++i) {
        for (int j = 0; j < N; ++j) cin >> val[i][j];
    }

    // ranks per row: 1..N (ascending by value)
    vector<vector<int>> rankRow(M, vector<int>(N));
    for (int i = 0; i < M; ++i) {
        vector<int> idx(N);
        iota(idx.begin(), idx.end(), 0);
        sort(idx.begin(), idx.end(), [&](int a, int b) {
            return val[i][a] < val[i][b];
        });
        for (int pos = 0; pos < N; ++pos) rankRow[i][idx[pos]] = pos + 1;
    }

    // order columns by rank of row1
    vector<int> colByR1(N);
    for (int col = 0; col < N; ++col) colByR1[rankRow[0][col] - 1] = col;

    if (M == 2) {
        vector<int> seq;
        seq.reserve(N);
        for (int k = 0; k < N; ++k) {
            int col = colByR1[k];
            seq.push_back(rankRow[1][col]);
        }
        vector<int> tails;
        for (int x : seq) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x);
            else *it = x;
        }
        cout << (int)tails.size() << '\n';
        return 0;
    }

    vector<Node> nodes;
    nodes.reserve(N);
    for (int k = 0; k < N; ++k) {
        int col = colByR1[k];
        nodes.push_back(Node{ k + 1, rankRow[1][col], rankRow[2][col], 1 });
    }

    Fenwick fw(N);
    cdq_solve(nodes, 0, N - 1, fw);

    int ans = 0;
    for (const auto &nd : nodes) ans = max(ans, nd.dp);
    cout << ans << '\n';
    return 0;
}
```

### 코너 케이스 체크리스트

- M=2와 M=3 모두 동작하는지, 분기 처리 및 초기 `dp=1` 여부 확인
- N가 매우 작을 때(예: 3)와 매우 클 때(최대 200,000) 시간/메모리 통과
- 값이 모두 서로 다름(문제 보장)을 전제로 등수 동률이 발생하지 않음을 이용했는지
- 엄격 증가 조건 유지: `x_left < x_right`, `y_left < y_right`를 CDQ/Fenwick에서 보장하는지
- 입력 파싱/출력 형식, 빠른 입출력(`sync_with_stdio(false)`, `tie(nullptr)`) 적용

### 제출 전 점검

- O(N log N)/O(N log^2 N) 복잡도 구현인지 재확인
- Fenwick 트리 인덱스 범위(1..N)와 초기화/클리어 처리 누락 없음
- `vector` 예약/정렬 비교자, 경계 조건(\-1, +1 오프셋) 검토

### 참고자료/유사문제

- KOI 2018 고등부 3번 배경 문제
- 공증가 사슬(3D LIS), CDQ Divide and Conquer 관련 에디토리얼/블로그 글들


