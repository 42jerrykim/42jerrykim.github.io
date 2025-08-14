---
title: "[Algorithm] cpp 백준 13925번: 수열과 쿼리 13 - Lazy 세그트리"
description: "구간에 대해 덧셈·곱셈·대입 3종 갱신과 합 조회를 동시에 처리하는 문제입니다. 대입이 연산을 덮어쓰는 특성을 고려해 '대입→곱→덧셈' 순서의 지연 전파를 설계하고, 합은 길이 배수로 갱신해 O((N+Q)logN)로 해결합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13925
- cpp
- C++
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Lazy Propagation
- 지연 전파
- Range Update
- 구간 갱신
- Range Sum
- 구간 합
- Range Add
- 구간 덧셈
- Range Multiply
- 구간 곱셈
- Range Assign
- 구간 대입
- Affine Transform
- 아핀 변환
- Composition
- 연산 합성
- Modular Arithmetic
- 모듈러 연산
- Mod 1e9+7
- 1e9+7
- Prefix/Suffix (Concept)
- 개념 정리
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
- Integer Overflow
- 정수 오버플로
- Fast IO
- 입출력 최적화
- Competitive Programming
- 경쟁프로그래밍
- Templates
- 템플릿
- Testing
- 테스트
- Invariant
- 불변식
- Interval Tree
- 인터벌 트리
- Range Query
- 구간 쿼리
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13925
- 요약: 길이 `N`의 수열에 대해 다음 연산을 처리한다: (1) 구간에 값 더하기, (2) 구간에 값 곱하기, (3) 구간을 특정 값으로 대입하기, (4) 구간 합 질의. 모든 연산과 답은 `1,000,000,007`로 나눈 나머지 기준.

### 제한/스펙
- `1 ≤ N, Q ≤ 100000`
- 초기 수열 값과 연산 인자는 정수, 모든 연산은 모듈러 적용
- 시간 제한 내 처리를 위해 `O((N+Q) log N)`급 자료구조 필요

## 입출력 형식/예제

예제 입력 형태(개략):
```
N Q
A1 A2 ... AN
op l r [v]
...
```

예제 출력 형태(개략):
```
<각 합 질의의 결과>
```

## 접근 개요(아이디어 스케치)
- 구간 합을 관리하는 세그먼트 트리에 지연 전파를 결합한다.
- 갱신은 세 종류: 더하기(+), 곱하기(×), 대입(=). 이들을 합성할 때 대입이 항상 우선권을 가져 기존 연산을 덮어쓴다.
- 노드별로 lazy를 "대입 여부/값", "곱 계수", "덧셈 계수"로 보관하고, 자식으로 전파 시 항상 "대입 → 곱 → 덧셈" 순서로 적용하면 합성이 일관된다.

```mermaid
flowchart TD
  A[요청 op ∈ {add, mul, assign}] --> B[노드 lazy에 합성]
  B --> C{push 필요?}
  C -- yes --> D[자식에게 '대입→곱→덧셈' 순서로 전파]
  C -- no --> E[현재 노드 합만 갱신]
  D --> F[상향 갱신: sum = L.sum + R.sum]
```

## 알고리즘 설계
- 상태: `sum`(구간 합), `lazySet(유무/값)`, `lazyMul(초기 1)`, `lazyAdd(초기 0)`.
- 적용 규칙(길이 `len`):
  - 대입: `sum = val * len`, lazy: `set=val, mul=1, add=0`.
  - 곱: `sum *= val`, lazy: `set*=val (있다면)`, 없으면 `mul*=val, add*=val`.
  - 덧셈: `sum += val * len`, lazy: `set+=val (있다면)`, 없으면 `add+=val`.
- 전파 순서: 자식에 대해 항상 `set → mul → add` 순으로 적용.
- 복잡도: 각 연산/질의 `O(log N)`.

## 복잡도
- 시간: O((N + Q) log N)
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 1000000007LL;

struct Node {
    long long sum;
    long long add;
    long long mul;
    long long setVal;
    bool hasSet;
    Node(): sum(0), add(0), mul(1), setVal(0), hasSet(false) {}
};

struct SegTree {
    int n;
    vector<Node> t;

    SegTree(int n): n(n), t(4 * n + 4) {}

    static inline long long norm(long long x) {
        x %= MOD;
        if (x < 0) x += MOD;
        return x;
    }

    void build(int idx, int l, int r, const vector<long long>& a) {
        t[idx].add = 0; t[idx].mul = 1; t[idx].hasSet = false; t[idx].setVal = 0;
        if (l == r) {
            t[idx].sum = norm(a[l]);
            return;
        }
        int m = (l + r) >> 1;
        build(idx << 1, l, m, a);
        build(idx << 1 | 1, m + 1, r, a);
        t[idx].sum = (t[idx << 1].sum + t[idx << 1 | 1].sum) % MOD;
    }

    inline void applySet(int idx, int l, int r, long long val) {
        val = norm(val);
        t[idx].sum = (val * (r - l + 1)) % MOD;
        t[idx].hasSet = true;
        t[idx].setVal = val;
        t[idx].mul = 1;
        t[idx].add = 0;
    }

    inline void applyMul(int idx, int l, int r, long long val) {
        val = norm(val);
        t[idx].sum = (t[idx].sum * val) % MOD;
        if (t[idx].hasSet) {
            t[idx].setVal = (t[idx].setVal * val) % MOD;
        } else {
            t[idx].mul = (t[idx].mul * val) % MOD;
            t[idx].add = (t[idx].add * val) % MOD;
        }
    }

    inline void applyAdd(int idx, int l, int r, long long val) {
        val = norm(val);
        t[idx].sum = (t[idx].sum + val * (r - l + 1)) % MOD;
        if (t[idx].hasSet) {
            t[idx].setVal = (t[idx].setVal + val) % MOD;
        } else {
            t[idx].add = (t[idx].add + val) % MOD;
        }
    }

    inline void push(int idx, int l, int r) {
        if (l == r) return;
        int m = (l + r) >> 1;
        int lc = idx << 1, rc = idx << 1 | 1;
        if (t[idx].hasSet) {
            applySet(lc, l, m, t[idx].setVal);
            applySet(rc, m + 1, r, t[idx].setVal);
            t[idx].hasSet = false;
        }
        if (t[idx].mul != 1) {
            applyMul(lc, l, m, t[idx].mul);
            applyMul(rc, m + 1, r, t[idx].mul);
            t[idx].mul = 1;
        }
        if (t[idx].add != 0) {
            applyAdd(lc, l, m, t[idx].add);
            applyAdd(rc, m + 1, r, t[idx].add);
            t[idx].add = 0;
        }
    }

    void rangeAdd(int idx, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyAdd(idx, l, r, v); return; }
        push(idx, l, r);
        int m = (l + r) >> 1;
        rangeAdd(idx << 1, l, m, ql, qr, v);
        rangeAdd(idx << 1 | 1, m + 1, r, ql, qr, v);
        t[idx].sum = (t[idx << 1].sum + t[idx << 1 | 1].sum) % MOD;
    }

    void rangeMul(int idx, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyMul(idx, l, r, v); return; }
        push(idx, l, r);
        int m = (l + r) >> 1;
        rangeMul(idx << 1, l, m, ql, qr, v);
        rangeMul(idx << 1 | 1, m + 1, r, ql, qr, v);
        t[idx].sum = (t[idx << 1].sum + t[idx << 1 | 1].sum) % MOD;
    }

    void rangeAssign(int idx, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applySet(idx, l, r, v); return; }
        push(idx, l, r);
        int m = (l + r) >> 1;
        rangeAssign(idx << 1, l, m, ql, qr, v);
        rangeAssign(idx << 1 | 1, m + 1, r, ql, qr, v);
        t[idx].sum = (t[idx << 1].sum + t[idx << 1 | 1].sum) % MOD;
    }

    long long rangeSum(int idx, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0LL;
        if (ql <= l && r <= qr) return t[idx].sum;
        push(idx, l, r);
        int m = (l + r) >> 1;
        long long left = rangeSum(idx << 1, l, m, ql, qr);
        long long right = rangeSum(idx << 1 | 1, m + 1, r, ql, qr);
        return (left + right) % MOD;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    if (!(cin >> N >> Q)) return 0;
    vector<long long> a(N + 1);
    for (int i = 1; i <= N; ++i) {
        long long x; cin >> x; a[i] = x % MOD;
    }
    SegTree st(N);
    st.build(1, 1, N, a);

    while (Q--) {
        int op; cin >> op;
        if (op == 1) { // add
            int l, r; long long v; cin >> l >> r >> v;
            st.rangeAdd(1, 1, N, l, r, v);
        } else if (op == 2) { // multiply
            int l, r; long long v; cin >> l >> r >> v;
            st.rangeMul(1, 1, N, l, r, v);
        } else if (op == 3) { // assign
            int l, r; long long v; cin >> l >> r >> v;
            st.rangeAssign(1, 1, N, l, r, v);
        } else if (op == 4) { // sum
            int l, r; cin >> l >> r;
            cout << st.rangeSum(1, 1, N, l, r) % MOD << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 대입 후 이어지는 덧셈/곱셈: 자식 전파 시 반드시 `대입→곱→덧셈` 순으로 적용.
- 음수 인자: 모듈러 정규화 필요(`norm`).
- 단일 구간/전구간 업데이트, `l=r`, 경계 포함성.
- 큰 입력: `ios::sync_with_stdio(false)`, `cin.tie(nullptr)`로 입출력 가속.

## 제출 전 점검
- 초기값 모듈러 처리 여부 확인.
- 대입 시 기존 `add/mul` 초기화(1, 0) 여부 확인.
- 자식 전파 순서 점검 및 상향 합 갱신.

## 참고자료/유사문제
- Lazy Segment Tree 일반론(아핀 변환 합성)
- 구간 갱신/합 질의 전형 문제군


