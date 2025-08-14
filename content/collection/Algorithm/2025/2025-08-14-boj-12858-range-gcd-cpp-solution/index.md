---
title: "[Algorithm] cpp 백준 12858번: Range GCD - 차분+세그트리"
description: "구간 덧셈과 구간 GCD 질의를 함께 처리합니다. 차분 배열과 세그먼트 트리로 d[l+1..r]의 GCD를 유지하고, 펜윅트리로 a[l]을 복원해 정답을 gcd(|a[l]|, G)로 구해 O(logN)에 해결합니다. 경계·절댓값·64-bit 주의."
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
- Problem-12858
- cpp
- C++
- Data Structures
- 자료구조
- Range GCD
- GCD
- 최대공약수
- Number Theory
- 정수론
- Math
- 수학
- Range Query
- 구간쿼리
- Segment Tree
- 세그먼트 트리
- Difference Array
- 차분 배열
- Fenwick Tree
- 펜윅트리
- BIT
- Binary Indexed Tree
- Range Update
- 구간 업데이트
- Point Update
- 점 업데이트
- Point Query
- 점 질의
- Absolute Value
- 절댓값
- Invariant
- 불변식
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Testing
- 테스트
- Prefix Sum
- 누적합
- Query Processing
- 쿼리 처리
- Online Queries
- 온라인 처리
- 1-based Index
- 1-기반 인덱스
- Fast IO
- 빠른 입출력
- Long Long
- 64-bit
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12858
- 요약: 길이 \(N\)의 수열에 대해 두 연산을 처리합니다. (1) `T>0`이면 구간 `[A,B]`에 `T`를 더하고, (2) `T=0`이면 구간 `[A,B]`의 최대공약수(GCD)를 출력합니다.

## 입력/출력
```
<입력>
N
A1 A2 ... AN
Q
T A B   (Q줄)  // T>0: 구간 덧셈, T=0: 구간 GCD 질의

<출력>
각 T=0 질의에 대한 답을 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심 등식: \(\gcd(A[l..r]) = \gcd(|A[l]|,\ \gcd(D[l+1..r]))\) where \(D[i] = A[i] - A[i-1]\).
- 구간 덧셈 `[l,r]+=T`는 차분 배열에서 `D[l]+=T`, `D[r+1]-=T` 두 점 갱신만 수행합니다.
- 따라서 `D`의 구간 GCD를 유지하는 세그먼트 트리와, 현재 `A[l]`을 복원하는 점 조회용 펜윅트리(BIT)를 함께 사용하면 각 연산을 \(O(\log N)\)에 처리할 수 있습니다.

```mermaid
flowchart LR
  Q{연산} -->|T>0, [l,r]+=T| U[BIT.rangeAdd(l,r,T)]
  U --> D1[D[l]+=T, D[r+1]-=T]
  D1 --> S1[SegTree.pointSet(l), pointSet(r+1)]
  Q -->|T=0, GCD[l,r]?| L1[a[l]=A[l]+BIT.sum(l)]
  L1 --> G1[G = SegTree.gcd(l+1,r)]
  G1 --> A1[답 = gcd(|a[l]|, G)]
```

## 알고리즘 설계
- 자료구조
  - 세그먼트 트리: `D[i]`의 절댓값을 저장, 질의는 `[l+1, r]`의 GCD.
  - 펜윅트리(BIT): 구간 가산을 두 점 갱신으로 저장하고 `sum(l)`로 현재 `A[l]` 복원.
- 연산 처리
  - 갱신 `T>0, [A,B]+=T`:
    - `BIT.rangeAdd(A,B,T)`
    - `D[A]+=T` → 세그먼트 트리 점 갱신
    - `D[B+1]-=T`(단, `B+1<=N`) → 세그먼트 트리 점 갱신
  - 질의 `T=0, [A,B]`:
    - `base = A[A] + BIT.sum(A)`
    - `gdiff = gcd(D[A+1..B])`
    - `answer = gcd(|base|, gdiff)`
- 올바름 근거(요지)
  - 구간의 GCD는 첫 항과 인접 차분들의 GCD로 표현되며, 구간 덧셈은 차분 배열의 두 점만 변경하므로 세그먼트 트리로 빠르게 유지 가능.

## 복잡도
- 시간: \(O(\log N)\) per 연산
- 공간: \(O(N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Fenwick {
    int n;
    vector<int64> bit;
    Fenwick(int n=0): n(n), bit(n+1, 0) {}
    void add(int idx, int64 delta){
        for(; idx<=n; idx+=idx&-idx) bit[idx] += delta;
    }
    void range_add(int l, int r, int64 delta){
        add(l, delta);
        if(r+1 <= n) add(r+1, -delta);
    }
    int64 sum(int idx) const {
        int64 s = 0;
        for(; idx>0; idx-=idx&-idx) s += bit[idx];
        return s;
    }
};

struct SegTreeGCD {
    int n;
    vector<int64> tree; // stores non-negative gcds
    SegTreeGCD(int n=0): n(n), tree(4*n+4, 0) {}
    static int64 gcdll(int64 a, int64 b){
        if(a<0) a = -a;
        if(b<0) b = -b;
        return std::gcd(a, b);
    }
    void build(const vector<int64>& diff, int node, int s, int e){
        if(s==e){
            tree[node] = llabs(diff[s]);
            return;
        }
        int m=(s+e)>>1, l=node<<1, r=l|1;
        build(diff, l, s, m);
        build(diff, r, m+1, e);
        tree[node] = gcdll(tree[l], tree[r]);
    }
    void build(const vector<int64>& diff){
        if(n>0) build(diff, 1, 1, n);
    }
    void point_set(int node, int s, int e, int idx, int64 val){
        if(s==e){
            tree[node] = llabs(val);
            return;
        }
        int m=(s+e)>>1, l=node<<1, r=l|1;
        if(idx<=m) point_set(l, s, m, idx, val);
        else point_set(r, m+1, e, idx, val);
        tree[node] = gcdll(tree[l], tree[r]);
    }
    void point_set(int idx, int64 val){
        point_set(1, 1, n, idx, val);
    }
    int64 range_gcd(int node, int s, int e, int l, int r) const {
        if(r<s || e<l) return 0;
        if(l<=s && e<=r) return tree[node];
        int m=(s+e)>>1, L=node<<1, R=L|1;
        int64 g1 = range_gcd(L, s, m, l, r);
        int64 g2 = range_gcd(R, m+1, e, l, r);
        return std::gcd(g1, g2);
    }
    int64 range_gcd(int l, int r) const {
        if(l>r) return 0;
        return range_gcd(1, 1, n, l, r);
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if(!(cin >> N)) return 0;
    vector<int64> a(N+1);
    for(int i=1;i<=N;i++) cin >> a[i];

    // diff[1] = a[1], diff[i] = a[i] - a[i-1] for i>=2
    vector<int64> diff(N+1, 0);
    if(N>=1) diff[1] = a[1];
    for(int i=2;i<=N;i++) diff[i] = a[i] - a[i-1];

    SegTreeGCD seg(N);
    seg.build(diff);

    Fenwick fw(N); // holds only updates to reconstruct current a[i] = a[i]_init + fw.sum(i)

    int Q; cin >> Q;
    while(Q--){
        long long T; int A, B;
        cin >> T >> A >> B;
        if(A > B) swap(A, B);

        if(T == 0){
            int64 base = a[A] + fw.sum(A); // current a[A]
            if(A == B){
                cout << llabs(base) << '\n';
            }else{
                int64 gdiff = seg.range_gcd(A+1, B); // gcd of diff[A+1..B]
                int64 ans = std::gcd(llabs(base), gdiff);
                cout << llabs(ans) << '\n';
            }
        }else{
            // range add: update BIT and two points in diff/seg
            fw.range_add(A, B, T);

            diff[A] += T;
            seg.point_set(A, diff[A]);

            if(B+1 <= N){
                diff[B+1] -= T;
                seg.point_set(B+1, diff[B+1]);
            }
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `A=B` 단일 원소 구간의 GCD는 `|a[A]|`이 됨
- `A=1` 또는 `B=N` 경계 인덱스에서 `D[B+1]` 처리 누락 주의
- 큰 값/누적 합을 고려한 64-bit 사용(`long long`)
- 절댓값 처리: 세그먼트 노드와 최종 출력 모두 `abs` 적용

## 제출 전 점검
- 입출력 버퍼링 설정(`sync_with_stdio(false)`, `tie(nullptr)`) 확인
- 인덱스는 1-based로 유지, `BIT`/세그먼트 트리 갱신 범위 점검
- `T=0`과 `T>0` 분기, `[A,B]`에서 `A>B` 입력 시 swap 처리

## 참고자료/유사아이디어
- 차분 배열(difference array)과 구간 GCD 유지 기법
- `gcd(a[l..r]) = gcd(a[l], a[l+1]-a[l], ..., a[r]-a[r-1])`


