---
title: "[Algorithm] cpp 백준 16124번: 나는 행복합니다 - 자릿수 치환 세그먼트 트리"
description: "최대 1e6자리 비밀번호에서 [i,j] 구간의 특정 숫자(from)를 다른 숫자(to)로 치환하고, 부분 문자열을 998244353으로 나눈 값을 출력합니다. 각 노드에 자릿값 가중 합을 숫자별로 분해해 저장하고, 0..9→0..9 치환을 지연 전파로 합성하는 Lazy 세그먼트 트리로 쿼리를 O(10·logN)에 처리합니다."
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
- Problem-16124
- cpp
- C++
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Lazy Propagation
- 지연 전파
- Digit Replacement
- 자릿수 치환
- Digit Mapping
- 자릿수 매핑
- Mapping Composition
- 매핑 합성
- Range Update
- 구간 업데이트
- Range Query
- 구간 질의
- Substring Modulo
- 부분 문자열 모듈러
- Modulo
- 모듈러
- Power of Ten
- 10의 거듭제곱
- Rolling Power
- 자리 가중치
- Weighted Sum
- 가중 합
- Immutable Build
- 선형 빌드
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
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Fast IO
- 빠른 입출력
- Memory
- 메모리
- Array
- 배열
- Integer String
- 숫자 문자열
- Query Processing
- 쿼리 처리
- Compose Function
- 함수 합성
- Digit Count Vector
- 자릿수 벡터
- Monoid
- 모노이드
- Offline/Online
- 온라인 처리
- 998244353
- Number Theory
- 수론
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16124
- 요약: 길이 최대 10^6의 숫자 문자열 `S`에 대해 두 가지 연산을 처리한다.
  - 연산 1: `[i, j]` 구간에서 숫자 `from`을 모두 `to`로 치환
  - 연산 2: `[i, j]` 구간을 십진수 정수로 보고 `998244353`으로 나눈 나머지 출력

## 입력/출력
```
<입력>
S
Q
각 줄에 다음 중 하나 (Q줄)
1 i j from to   # 구간 치환 (숫자)
2 i j           # 구간 모듈러 쿼리

<출력>
각 2번 쿼리의 답을 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심 아이디어: 한 구간의 값은 각 자릿수에 대한 10의 거듭제곱 가중 합으로 표현된다. 구간을 합칠 때 왼쪽 값은 오른쪽 길이만큼 `×10^{lenRight}`로 시프트된다.
- 각 노드에 숫자별 가중 합 벡터 `w[10]`를 저장한다. `w[d]`는 현재 구간에서 숫자 `d`가 만드는 10의 거듭제곱들의 합이다.
- 치환 연산은 0..9→0..9 함수 `g`로 표현되어 `w`를 `w'[g[d]] += w[d]`로 재배치한다. Lazy로 이 함수를 자식에게 전달할 때는 합성 `g ∘ f`로 갱신한다.
- 질의는 구간 병합 시 왼쪽을 `×10^{lenRight}`로 시프트해 합치고, 마지막에 `∑_{d=0..9} d·w[d] (mod M)`로 값을 복원한다.

## 알고리즘
1) 전처리: `pow10[k] = 10^k mod M`을 `k=0..N`까지 준비
2) 세그먼트 트리 빌드: 리프 `w[digit]=1`(10^0), 내부는 `left*w10[lenRight] + right`
3) 업데이트(1 i j from to): 치환 함수 `g`를 노드에 `apply`하고 Lazy에 합성(`g ∘ f`)
4) 질의(2 i j): 구간 결과 `w` 병합 후 `∑ d·w[d] mod M` 출력

## 복잡도
- 시간: 연산당 O(10 · log N)
- 공간: O(N) 노드에 상수(10)배 벡터 저장(메모리 여유: 512MB 기준 안전)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 998244353;

struct Node {
    int w[10];           // weighted sums per digit
    uint8_t lazy[10];    // digit mapping 0..9 -> 0..9
    uint8_t hasLazy;     // 0 or 1
};

string S;
int N, Q;
vector<int> pow10v; // pow10v[k] = 10^k % MOD
vector<Node> seg;

inline int addmod(int a, int b) {
    int s = a + b;
    if (s >= MOD) s -= MOD;
    return s;
}
inline int mulmod(long long a, int b) {
    return int((a * b) % MOD);
}

void applyMap(int idx, const uint8_t g[10]) {
    int tmp[10] = {0};
    for (int d = 0; d <= 9; ++d) {
        int nd = g[d];
        tmp[nd] = addmod(tmp[nd], seg[idx].w[d]);
    }
    for (int d = 0; d <= 9; ++d) seg[idx].w[d] = tmp[d];

    if (seg[idx].hasLazy) {
        uint8_t composed[10];
        for (int d = 0; d <= 9; ++d) composed[d] = g[ seg[idx].lazy[d] ];
        for (int d = 0; d <= 9; ++d) seg[idx].lazy[d] = composed[d];
    } else {
        for (int d = 0; d <= 9; ++d) seg[idx].lazy[d] = g[d];
        seg[idx].hasLazy = 1;
    }
}

void push(int idx) {
    if (!seg[idx].hasLazy) return;
    applyMap(idx << 1, seg[idx].lazy);
    applyMap(idx << 1 | 1, seg[idx].lazy);
    seg[idx].hasLazy = 0;
}

void pull(int idx, int lenRight) {
    for (int d = 0; d <= 9; ++d) {
        int leftW  = seg[idx << 1].w[d];
        int rightW = seg[idx << 1 | 1].w[d];
        seg[idx].w[d] = addmod(mulmod(leftW, pow10v[lenRight]), rightW);
    }
}

void build(int idx, int l, int r) {
    seg[idx].hasLazy = 0;
    if (l == r) {
        for (int d = 0; d <= 9; ++d) seg[idx].w[d] = 0;
        int digit = S[l - 1] - '0';
        seg[idx].w[digit] = 1; // weight 10^0
        return;
    }
    int mid = (l + r) >> 1;
    build(idx << 1, l, mid);
    build(idx << 1 | 1, mid + 1, r);
    pull(idx, r - mid);
}

void update(int idx, int l, int r, int ql, int qr, const uint8_t g[10]) {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
        applyMap(idx, g);
        return;
    }
    int mid = (l + r) >> 1;
    push(idx);
    update(idx << 1, l, mid, ql, qr, g);
    update(idx << 1 | 1, mid + 1, r, ql, qr, g);
    pull(idx, r - mid);
}

struct Res {
    int w[10];
    int len;
};
Res combine(const Res &a, const Res &b) {
    if (a.len == 0) return b;
    if (b.len == 0) return a;
    Res c;
    c.len = a.len + b.len;
    for (int d = 0; d <= 9; ++d) {
        c.w[d] = addmod(mulmod(a.w[d], pow10v[b.len]), b.w[d]);
    }
    return c;
}

Res query(int idx, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) {
        Res z; z.len = 0; for (int d = 0; d <= 9; ++d) z.w[d] = 0; return z;
    }
    if (ql <= l && r <= qr) {
        Res res; res.len = r - l + 1;
        for (int d = 0; d <= 9; ++d) res.w[d] = seg[idx].w[d];
        return res;
    }
    int mid = (l + r) >> 1;
    push(idx);
    Res left = query(idx << 1, l, mid, ql, qr);
    Res right = query(idx << 1 | 1, mid + 1, r, ql, qr);
    return combine(left, right);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> S;
    N = (int)S.size();

    pow10v.resize(N + 1);
    pow10v[0] = 1;
    for (int i = 1; i <= N; ++i) {
        pow10v[i] = (int)((pow10v[i - 1] * 10LL) % MOD);
    }

    seg.assign((N << 2) + 5, Node());
    build(1, 1, N);

    cin >> Q;
    for (int qi = 0; qi < Q; ++qi) {
        int type; cin >> type;
        if (type == 1) {
            int i, j; int from, to;
            cin >> i >> j >> from >> to;
            if (from == to) continue;
            uint8_t g[10];
            for (int d = 0; d <= 9; ++d) g[d] = (uint8_t)d;
            g[from] = (uint8_t)to;
            update(1, 1, N, i, j, g);
        } else {
            int i, j; cin >> i >> j;
            Res res = query(1, 1, N, i, j);
            long long ans = 0;
            for (int d = 0; d <= 9; ++d) {
                ans += 1LL * d * res.w[d];
                if (ans >= (1LL << 62)) ans %= MOD; // prevent overflow
            }
            cout << (ans % MOD) << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `from == to`인 무의미 치환은 무시
- 선행 0(리딩 제로): 값에는 영향을 주지 않음(모듈러 동일)
- 빈 교집합 구간 합치기: 길이 0 결과 안전 처리
- 매우 긴 문자열(N≈1e6): `pow10` 전처리와 메모리 사용량 확인
- 많은 치환 조합: Lazy 함수 합성 순서 `g ∘ f` 유지

## 제출 전 점검
- 입출력 버퍼링 설정 확인(`sync_with_stdio(false)`, `tie(nullptr)`)
- 세그 병합 시 왼쪽을 `×10^{lenRight}`로 시프트하는지
- Lazy 전파 후 `hasLazy` 클리어 여부
- `int` 모듈러 연산 범위, 누적 시 임시 `long long` 사용

## 참고자료/유사문제
- 자리수 기반 세그먼트 트리 응용 문제군
- 함수 합성 기반 Lazy Propagation 패턴


