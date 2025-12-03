---
title: "[Algorithm] C++ 백준 10076번: 휴가 - 최적 풀이"
description: "IOI 2014 Holiday(휴가) 최적 풀이. 선형 도시에서 하루에 이동 또는 방문만 가능한 제약에서 방문 관광지 수를 최대화한다. 이동은 한 번의 방향 전환만 해도 충분하다는 관찰 아래 [l,r] 구간을 잡고 체류 가능일 g(l,r)을 계산한다. 분할정복+세그먼트 트리로 상위 k 합을 빠르게 질의하여 O(N log^2 N)로 해결한다. 경계·중복·음수 k 처리와 좌우 반전까지 구현 체크리스트 포함."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Data Structures"
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-10076
- cpp
- C++
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
- Segment Tree
- 세그먼트 트리
- Divide and Conquer
- 분할정복
- IOI
- Holiday
- 휴가
- Monotonicity
- 단조성
- Coordinate Compression
- 좌표압축
- Top-k Sum
- 상위-k-합
- Data Structures
- 자료구조
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/10076
- 요약: 길이 N의 선분 위 도시 0..N-1, 시작 도시 `start`, 휴가일 `d`. 하루에 인접 도시로 이동 또는 현재 도시의 관광지를 전부 방문(도시당 1회만) 중 택1. 총 `d`일 동안 방문 가능한 관광지 수의 최댓값을 구한다.
- 제한: N ≤ 100,000, 관광지 수 ≤ 1e9, 시간 5s, 메모리 64MB.

## 입력/출력
```
입력
n start d
a0 a1 ... a{n-1}

출력
최대로 방문 가능한 관광지 수
```

예시
```
입력: 5 2 7
      10 2 20 30 1
출력: 60
```

## 접근 개요
- 핵심 관찰: 이동만 놓고 보면 경로는 좌→우 또는 우→좌로 단 한 번만 방향을 바꿔도 최적을 만들 수 있다. 즉, 어떤 구간 `[l,r] (l ≤ start ≤ r)`을 정하고 그 구간 안에서만 방문한다.
- 구간이 정해지면 이동에 소모되는 날짜는 `(start-l) + (r-l)` 또는 그 대칭이며, 남는 날 만큼 도시 방문(Stay)을 할 수 있다. 이를 `g(l,r)`라 두면, 해당 구간에서 상위 `g(l,r)`개의 도시 관광지 합을 더하면 된다.
- 단, 모든 `(l,r)`을 다 보면 O(N^2)이 되므로, `l`에 대한 최적 `r`이 단조적으로 움직인다는 성질(전형적 분할정복 최적화)을 이용해 `l`을 분할정복하며 `r`의 탐색 범위를 좁힌다.
- 구간 내 상위 k 합은 값 기준으로 좌표압축 후 세그먼트 트리에서 “상위 k 합” 질의로 O(log U)에 처리한다.

## 알고리즘
1) 좌표압축: 관광지 수 배열을 정렬·중복 제거해 값 인덱스로 변환.
2) 자료구조: 세그먼트 트리 노드에 (개수, 합)을 저장. 활성화된 인덱스만 관리하면 “상위 k 합”을 트리로 O(log U)에 구한다.
3) 분할정복(DnC) over l:
   - 구간 `[s,e]`에서 `m=(s+e)/2`를 잡고, 후보 r 범위 `[kmin,kmax]`를 이용해 `l=m`에서 최적 r을 선형 스캔(활성/비활성 토글은 누적 재사용)으로 찾는다.
   - 오른쪽 재귀는 `[m+1,e]`와 `[best_r,kmax]`, 왼쪽 재귀는 `[s,m-1]`와 `[kmin,best_r]`로 줄여가며 단조성을 유지한다.
4) 경로 대칭 처리: 좌→우뿐 아니라 우→좌 경우도 동일하므로, 배열을 한 번 뒤집고 `start`를 반영해 다시 한 번 계산, 두 결과의 최댓값을 취한다.

정당성 요약:
- 이동은 단 한 번의 방향 전환만 해도 손해가 없다(여러 번 꺾는 경로는 항상 한 번만 꺾는 경로로 대체 가능).
- `l`이 커질수록 최적 `r`은 왼쪽으로 이동하지 않는 단조성이 성립하여 분할정복 최적화가 가능하다.
- 값 기준 세그먼트 트리로 “상위 k 합”을 정확하게 계산하므로, 고정된 `[l,r]`에서의 최적 방문 합을 올바르게 산출한다.

## 복잡도
- 시간: O(N log^2 N) 내외 (분할정복 단계 × 상위 k 합 질의 O(log U))
- 공간: O(U) + O(N) (U: 서로 다른 관광지 수) — 64MB 내 수용

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int n, st, d;
vector<ll> raw_values;
vector<int> a;            // compressed indices per city
vector<ll> cmp;           // sorted unique values
vector<char> active_flag; // whether index i is active in the current structure
ll ans = 0;

struct Segtree {
    vector<ll> seg;
    vector<int> cnt;
    int m = 0;

    void allocate(int size) {
        m = size;
        seg.assign(4 * m + 5, 0);
        cnt.assign(4 * m + 5, 0);
    }

    void clear() {
        fill(seg.begin(), seg.end(), 0);
        fill(cnt.begin(), cnt.end(), 0);
    }

    void upd(int now, int s, int e, int i, int v) {
        if (i < s || i > e) return;
        cnt[now] += v;
        seg[now] += (ll)v * cmp[i];
        if (s == e) return;
        int mid = (s + e) >> 1;
        upd(now << 1, s, mid, i, v);
        upd(now << 1 | 1, mid + 1, e, i, v);
    }

    // Sum of the largest k values among active elements
    ll sum_max_kth(int now, int s, int e, int k) {
        if (k <= 0 || cnt[now] == 0) return 0LL;
        if (k >= cnt[now]) return seg[now];
        if (s == e) return (ll)k * cmp[s];
        int mid = (s + e) >> 1;
        int right_count = cnt[now << 1 | 1];
        if (right_count >= k) {
            return sum_max_kth(now << 1 | 1, mid + 1, e, k);
        } else {
            return seg[now << 1 | 1] + sum_max_kth(now << 1, s, mid, k - right_count);
        }
    }
} S;

void toggle_idx(int i, int v) { // v: +1 (add) or -1 (remove)
    bool want_on = (v == 1);
    if ((active_flag[i] != 0) == want_on) return;
    active_flag[i] ^= 1;
    S.upd(1, 0, (int)cmp.size() - 1, a[i], v);
}

ll qry(int k) {
    if (k <= 0) return 0;
    return S.sum_max_kth(1, 0, (int)cmp.size() - 1, k);
}

// Divide & conquer over l in [s,e], with feasible r in [kmin,kmax]
void dnc(int s, int e, int kmin, int kmax) {
    if (s > e) return;
    int m = (s + e) >> 1;

    // Ensure [m..e] is active
    for (int i = m; i <= e; i++) toggle_idx(i, +1);

    int klim = min(kmax, 2 * m + d - st); // feasibility cap for r
    ll best_local = 0;
    int best_r = kmin;

    for (int i = kmin; i <= klim; i++) {
        toggle_idx(i, +1);
        // k = d - (st - m) - (i - m)
        ll tmp = qry(d - (st - m) - (i - m));
        if (tmp > best_local) {
            best_local = tmp;
            best_r = i;
        }
    }
    ans = max(ans, best_local);

    // Roll back [best_r..klim]
    for (int i = klim; i >= best_r; i--) toggle_idx(i, -1);

    // Recurse right half
    if (m < e) {
        int mm = (m + 1 + e) >> 1;
        for (int i = m; i <= mm; i++) toggle_idx(i, -1);
        dnc(m + 1, e, best_r, kmax);
    }

    // Fully roll back r-range additions
    for (int i = kmax; i >= kmin; i--) toggle_idx(i, -1);

    // Recurse left half
    if (s < m) {
        int ss = (s + m - 1) >> 1;
        for (int i = m; i < min(kmin, e + 1); i++) toggle_idx(i, +1);
        dnc(s, m - 1, kmin, best_r);
        for (int i = ss; i <= e; i++) toggle_idx(i, -1);
    }

    // Roll back [m..e]
    for (int i = m; i <= e; i++) toggle_idx(i, -1);
}

void solve_one_direction() {
    S.clear();
    fill(active_flag.begin(), active_flag.end(), 0);
    int l = max(0, st - d);
    dnc(l, st, st, n - 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n >> st >> d)) return 0;
    raw_values.resize(n);
    for (int i = 0; i < n; i++) cin >> raw_values[i];

    // Coordinate compression
    cmp = raw_values;
    sort(cmp.begin(), cmp.end());
    cmp.erase(unique(cmp.begin(), cmp.end()), cmp.end());

    a.resize(n);
    for (int i = 0; i < n; i++) {
        a[i] = int(lower_bound(cmp.begin(), cmp.end(), raw_values[i]) - cmp.begin());
    }

    S.allocate((int)cmp.size());
    active_flag.assign(n, 0);

    // Left-then-right case
    solve_one_direction();

    // Right-then-left case by reversing
    reverse(a.begin(), a.end());
    st = n - 1 - st;
    solve_one_direction();

    cout << ans << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `d=0` 또는 `d=1` 등 매우 작은 일수 처리
- `start`가 0 또는 N-1인 경계 위치
- 동일한 관광지 수(중복 값) 다수 — 좌표압축 및 세그먼트 트리 합산 검증
- `g(l,r) ≤ 0`가 되는 경우의 상위 k 합(0 처리)
- 큰 값(≤1e9) 합 누적 — 64-bit 사용

## 제출 전 점검
- 입출력 형식 및 개행, fast I/O 사용 여부 확인
- 인덱스 범위, 활성/비활성 토글 롤백 누락 여부 점검
- 좌우 반전 시 `start` 갱신 `st = n-1-st` 반영 확인

## 참고자료
- 문제: https://www.acmicpc.net/problem/10076
- 해설 노트: IOI 2014 Holiday 관련 정리(분할정복 최적화, 상위 k 합 세그트리)


