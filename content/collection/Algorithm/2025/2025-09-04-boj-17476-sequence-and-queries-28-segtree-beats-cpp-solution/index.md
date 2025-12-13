---
title: "[Algorithm] C++ 백준 17476번: 수열과 쿼리 28"
description: "구간 덧셈, 구간 제곱근, 구간 합을 동시에 처리하는 Segment Tree Beats 풀이입니다. min/max 기반 가지치기(동일 제곱근 일괄 set, 인접값은 delta add)로 리프 하강을 크게 줄여 TLE 없이 통과합니다. 시간/공간 복잡도와 실수 포인트까지 정리했습니다."
date: 2025-09-04
lastmod: 2025-09-04
categories:
- Algorithm
- Segment Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17476
- cpp
- C++
- Segment Tree
- 세그먼트 트리
- Segment Tree Beats
- 세그먼트 트리 비츠
- Range Update
- 구간 갱신
- Range Sum
- 구간 합
- Range Add
- 구간 덧셈
- Range Sqrt
- 구간 제곱근
- Sqrt Update
- 제곱근 갱신
- Lazy Propagation
- 레이지 프로퍼게이션
- Min Max Pruning
- 가지치기
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
- Binary Search
- 이분탐색
- Data Structures
- 자료구조
- Implementation
- 구현
- Debugging
- 디버깅
- Math
- 수학
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17476
- 요약: 길이 N 수열에 대해 세 가지 연산을 처리합니다.
  - 1 L R X: 구간 [L,R]에 X 더하기
  - 2 L R: 구간 [L,R] 원소를 각각 ⌊√ai⌋로 바꾸기
  - 3 L R: 구간 [L,R] 합 출력

## 입력/출력
```text
입력 예시
5
1 2 3 4 5
5
1 3 5 2
2 1 4
3 2 4
2 3 5
3 1 5
```
```text
출력 예시
5
6
```

## 접근 개요
- 제곱근 연산은 값이 빠르게 감소해 중복된 값(또는 좁은 값 범위)이 많아집니다.
- 이를 활용해 세그먼트 트리 비츠 방식으로 구간의 `min/max`를 보고 가지치기합니다.
  - 구간 내 모든 값의 바닥제곱근이 동일하면, 해당 구간을 그 값으로 `set` (일괄 갱신).
  - `min+1==max`이며 `floor(sqrt(min))+1==floor(sqrt(max))`이면, 구간 전체에 동일한 `delta`(=sqrt(min)-min)를 `add`로 한 번에 처리.
- 덧셈은 일반 lazy add, 합은 구간 합을 유지합니다.

## 알고리즘 설계
- 노드 상태: `sum, mn, mx`를 저장. lazy는 `add`(덧셈)와 `set`(구간 동일값) 두 종류를 사용.
- `rangeSqrt` 구현의 핵심 분기:
  1) `mn==mx`이면 리프처럼 취급하여 그 값의 √로 `set`.
  2) `mx<=1`이면 변화 없음(√0=0, √1=1).
  3) `isqrt(mn)==isqrt(mx)`이면 구간 전체 `set`.
  4) `mn+1==mx`이고 `isqrt(mn)+1==isqrt(mx)`이면 구간 `add(delta)`로 처리.
  5) 위에 해당하지 않으면 자식으로 내려가 재귀 후 `pull`.

## 복잡도
- 구간 덧셈/합: O(log N).
- 구간 제곱근: 세그비츠 가지치기로 각 원소가 변하는 횟수가 매우 제한되어, 전체적으로 암묵적 상수 내에서 O(log N) 수준으로 수렴(실전에서 통과 검증).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Seg {
    struct Node {
        long long sum, mn, mx;
        long long add;
        bool hasSet;
        long long setVal;
    };

    int n;
    vector<Node> t;

    static inline long long isqrt(long long x) {
        long long r = (long long)floor(sqrt((long double)x));
        while ((r + 1) * (r + 1) <= x) ++r;
        while (r * r > x) --r;
        return r;
    }

    Seg(const vector<long long>& a) {
        n = (int)a.size() - 1; // 1-indexed
        t.assign(4 * n + 4, {0, 0, 0, 0, false, 0});
        build(1, 1, n, a);
    }

    void applySet(int idx, int l, int r, long long v) {
        Node& nd = t[idx];
        nd.sum = v * (r - l + 1);
        nd.mn = nd.mx = v;
        nd.hasSet = true;
        nd.setVal = v;
        nd.add = 0;
    }

    void applyAdd(int idx, int l, int r, long long v) {
        Node& nd = t[idx];
        nd.sum += v * (r - l + 1);
        nd.mn += v;
        nd.mx += v;
        if (nd.hasSet) nd.setVal += v;
        else nd.add += v;
    }

    void push(int idx, int l, int r) {
        if (l == r) {
            t[idx].hasSet = false;
            t[idx].add = 0;
            return;
        }
        int lc = idx << 1, rc = lc | 1;
        if (t[idx].hasSet) {
            applySet(lc, l, (l + r) >> 1, t[idx].setVal);
            applySet(rc, ((l + r) >> 1) + 1, r, t[idx].setVal);
            t[idx].hasSet = false;
        }
        if (t[idx].add != 0) {
            long long v = t[idx].add;
            applyAdd(lc, l, (l + r) >> 1, v);
            applyAdd(rc, ((l + r) >> 1) + 1, r, v);
            t[idx].add = 0;
        }
    }

    void pull(int idx) {
        t[idx].sum = t[idx<<1].sum + t[idx<<1|1].sum;
        t[idx].mn = min(t[idx<<1].mn, t[idx<<1|1].mn);
        t[idx].mx = max(t[idx<<1].mx, t[idx<<1|1].mx);
    }

    void build(int idx, int l, int r, const vector<long long>& a) {
        if (l == r) {
            t[idx].sum = t[idx].mn = t[idx].mx = a[l];
            t[idx].add = 0;
            t[idx].hasSet = false;
            return;
        }
        int m = (l + r) >> 1;
        build(idx<<1, l, m, a);
        build(idx<<1|1, m+1, r, a);
        pull(idx);
    }

    void rangeAdd(int idx, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyAdd(idx, l, r, v); return; }
        push(idx, l, r);
        int m = (l + r) >> 1;
        rangeAdd(idx<<1, l, m, ql, qr, v);
        rangeAdd(idx<<1|1, m+1, r, ql, qr, v);
        pull(idx);
    }

    void rangeSqrt(int idx, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            Node& nd = t[idx];
            if (nd.mn == nd.mx) {
                long long s = isqrt(nd.mn);
                if (s != nd.mn) applySet(idx, l, r, s);
                return;
            }
            if (nd.mx <= 1) return; // sqrt(0/1) == itself
            long long sMin = isqrt(nd.mn);
            long long sMax = isqrt(nd.mx);
            if (sMin == sMax) { // 모두 같은 값으로 수렴
                applySet(idx, l, r, sMin);
                return;
            }
            if (nd.mn + 1 == nd.mx && sMin + 1 == sMax) {
                long long delta = sMin - nd.mn;
                applyAdd(idx, l, r, delta);
                return;
            }
        }
        if (l == r) {
            long long s = isqrt(t[idx].mn);
            if (s != t[idx].mn) applySet(idx, l, r, s);
            return;
        }
        push(idx, l, r);
        int m = (l + r) >> 1;
        rangeSqrt(idx<<1, l, m, ql, qr);
        rangeSqrt(idx<<1|1, m+1, r, ql, qr);
        pull(idx);
    }

    long long rangeSum(int idx, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0LL;
        if (ql <= l && r <= qr) return t[idx].sum;
        push(idx, l, r);
        int m = (l + r) >> 1;
        return rangeSum(idx<<1, l, m, ql, qr) + rangeSum(idx<<1|1, m+1, r, ql, qr);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<long long> A(N + 1);
    for (int i = 1; i <= N; ++i) cin >> A[i];

    Seg seg(A);

    int M; cin >> M;
    while (M--) {
        int t; cin >> t;
        if (t == 1) {
            int L, R; long long X; cin >> L >> R >> X;
            if (L > R) swap(L, R);
            seg.rangeAdd(1, 1, seg.n, L, R, X);
        } else if (t == 2) {
            int L, R; cin >> L >> R;
            if (L > R) swap(L, R);
            seg.rangeSqrt(1, 1, seg.n, L, R);
        } else {
            int L, R; cin >> L >> R;
            if (L > R) swap(L, R);
            cout << seg.rangeSum(1, 1, seg.n, L, R) << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 값이 0/1인 구간(√로 불변) — 조기 종료해야 함.
- `min+1==max` 형태(예: 3/4, 8/9 등) — delta add 최적화 적용 여부.
- 큰 `X`의 반복 덧셈 후 제곱근 — 오버플로 없이 `long long` 유지.
- 쿼리 경계: L=1, R=N, 단일 원소(L=R).

## 제출 전 점검
- 출력 개행, 자료형 범위(합은 `long long`).
- lazy 순서: `set`이 `add`보다 우선, push/pull 정확성.
- 제곱근 가지치기 4가지 분기 조건 재점검.

## 참고자료
- 문제: https://www.acmicpc.net/problem/17476
- 해설(세그비츠 아이디어): https://justicehui.github.io/ps/2019/10/29/BOJ17476/


