---
title: "[Algorithm] cpp 백준 16977번: 히스토그램에서 가장 큰 직사각형과 쿼리 - PBS+세그트리"
description: "히스토그램의 구간 [l,r]에서 너비 w가 고정일 때 최대 넓이는 길이 w 윈도우의 최솟값을 최대화하는 문제입니다. 높이 좌표압축과 임계값 단조성을 이용해 병렬 이분탐색을 수행하고, 세그먼트 트리(연속 1의 최댓값)로 검증하여 각 쿼리를 빠르게 해결합니다. 엣지 케이스와 실수 포인트까지 점검합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Segment Tree"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-16977"
- "cpp"
- "C++"
- "Python"
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
- "Binary Search"
- "이분탐색"
- "Binary Search on Answer"
- "답을 위한 이분탐색"
- "Parallel Binary Search"
- "병렬 이분탐색"
- "Segment Tree"
- "세그먼트 트리"
- "Range Query"
- "구간 질의"
- "Histogram"
- "히스토그램"
- "Largest Rectangle"
- "최대 직사각형"
- "Sliding Window"
- "슬라이딩윈도우"
- "Offline Query"
- "오프라인 쿼리"
- "Coordinate Compression"
- "좌표압축"
- "Min on Window"
- "윈도우 최솟값"
- "Consecutive Ones"
- "연속 구간"
- "Boolean Segment Tree"
- "불리언 세그먼트트리"
- "Query Optimization"
- "쿼리 최적화"
- "Range Minimum"
- "구간최솟값"
- "Monotonic Predicate"
- "단조성"
- "Max Subarray of Ones"
- "연속1최대"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16977
- 요약: 히스토그램의 높이 배열 `h[1..N]`에서 쿼리 `(l, r, w)`가 주어지면, 구간 `[l, r]` 내부의 길이 `w`인 연속 구간들 중 최솟값이 최대가 되는 값을 출력합니다. (너비가 고정이므로 넓이 최대 ≡ 높이 최대)

## 입력/출력
```
입력
7
2 1 4 5 1 3 3
8
3 4 2
4 7 2
2 5 1
2 5 2
2 5 3
2 5 4
1 3 2
6 7 2

출력
4
3
5
4
1
1
1
3
```

## 접근 개요
- 너비가 `w`로 고정되면, 최대 넓이는 곧 길이 `w` 윈도우의 최솟값을 최대화하는 문제입니다.
- 임계값 `T`를 고정했을 때, `h[i] ≥ T`인 위치를 1로 표시하면, 구간 `[l, r]` 안에 길이 `w` 이상의 연속 1 구간이 존재하는지의 여부가 단조입니다(`T`가 커질수록 성립이 어렵다).
- 이 단조성을 이용해 높이값에 대해 병렬 이분탐색(Parallel Binary Search, PBS)을 돌리고, 각 임계값 검증은 “연속 1의 최댓값”을 유지하는 세그먼트 트리로 처리합니다.

```mermaid
flowchart TD
  A[높이 좌표압축] --> B[쿼리별 T에 대한 PBS]
  B --> C{임계값 T에 대해
           h[i]≥T → 1,
           아니면 0}
  C --> D[세그트리로 [l,r]의 연속 1 최댓값 질의]
  D --> E{best ≥ w?}
  E -- 예 --> F[lo = mid]
  E -- 아니오 --> G[hi = mid - 1]
  F --> H[모든 쿼리 수렴]
  G --> H
```

## 알고리즘 설계
- 좌표압축: 높이들을 정렬·중복제거하여 인덱스화(랭크).
- PBS: 각 쿼리에 대해 높이 랭크 구간에서 이분탐색. 같은 `mid`(임계 랭크)를 요구하는 쿼리들을 버킷으로 묶어 한 번에 검증.
- 활성화 전략: 랭크가 큰 순서로 인덱스를 활성화(1로 갱신). 같은 라운드에서 임계값을 내림차순으로 처리하며, 포인터 1회 전진으로 누적 활성화 → 매 라운드 O((활성화 건수) log N + (검증 쿼리 수) log N).
- 세그트리 노드 정보: `len`, `pref`, `suff`, `best`(전체 길이, 앞/뒤 연속 1 길이, 구간 내 연속 1 최댓값). 병합 시 `best = max(left.best, right.best, left.suff + right.pref)`.
- 정당성: (1) `T`에 대한 “존재 여부”는 단조이므로 이분탐색 가능. (2) 길이 `w` 윈도우의 최솟값 ≥ `T` ⇔ 표시배열에서 연속 1 구간 길이 ≥ `w`가 존재.

## 복잡도
- 라운드 수는 O(log M) (`M`=서로 다른 높이 개수). 라운드마다 활성화/질의는 세그트리로 O(log N).
- 전체: O((N + Q) log M log N). `N, Q ≤ 1e5`에서 충분히 통과합니다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int l, r, w;
};

struct Node {
    int len, pref, suff, best;
    Node(int l=0, int p=0, int s=0, int b=0): len(l), pref(p), suff(s), best(b) {}
};

struct SegTree {
    int n;
    vector<Node> st;
    SegTree(int n=0): n(n), st(4*n+4) {}

    static Node mergeNode(const Node &a, const Node &b) {
        if (a.len == 0) return b;
        if (b.len == 0) return a;
        Node res;
        res.len = a.len + b.len;
        res.pref = (a.pref == a.len) ? (a.len + b.pref) : a.pref;
        res.suff = (b.suff == b.len) ? (b.len + a.suff) : b.suff;
        res.best = max({a.best, b.best, a.suff + b.pref});
        return res;
    }

    void build(int p, int l, int r) {
        if (l == r) {
            st[p] = Node(1, 0, 0, 0);
            return;
        }
        int m = (l + r) >> 1;
        build(p<<1, l, m);
        build(p<<1|1, m+1, r);
        st[p] = mergeNode(st[p<<1], st[p<<1|1]);
    }

    void update(int p, int l, int r, int idx) {
        if (l == r) {
            st[p] = Node(1, 1, 1, 1);
            return;
        }
        int m = (l + r) >> 1;
        if (idx <= m) update(p<<1, l, m, idx);
        else update(p<<1|1, m+1, r, idx);
        st[p] = mergeNode(st[p<<1], st[p<<1|1]);
    }

    Node query(int p, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return Node(0,0,0,0);
        if (ql <= l && r <= qr) return st[p];
        int m = (l + r) >> 1;
        Node left = query(p<<1, l, m, ql, qr);
        Node right = query(p<<1|1, m+1, r, ql, qr);
        return mergeNode(left, right);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<int> h(N+1);
    for (int i = 1; i <= N; ++i) cin >> h[i];

    int Q; cin >> Q;
    vector<Query> qs(Q);
    for (int i = 0; i < Q; ++i) {
        int l, r, w; cin >> l >> r >> w;
        qs[i] = {l, r, w};
    }

    // 좌표압축
    vector<int> vals;
    vals.reserve(N);
    for (int i = 1; i <= N; ++i) vals.push_back(h[i]);
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int M = (int)vals.size();

    vector<int> rankH(N+1);
    for (int i = 1; i <= N; ++i) {
        rankH[i] = int(lower_bound(vals.begin(), vals.end(), h[i]) - vals.begin());
    }

    // 인덱스를 높이 랭크 내림차순으로 정렬
    vector<int> order(N);
    iota(order.begin(), order.end(), 1);
    sort(order.begin(), order.end(), [&](int a, int b) {
        return rankH[a] > rankH[b];
    });

    // 병렬 이분탐색 (랭크 공간)
    vector<int> lo(Q, 0), hi(Q, M-1), mid(Q, 0);
    vector<vector<int>> bucket(M);
    vector<char> used(M, 0);
    vector<int> usedList;
    usedList.reserve(M);

    SegTree st(N);

    auto check_and_update = [&](int t) {
        for (int qi : bucket[t]) {
            const auto &qq = qs[qi];
            Node res = st.query(1, 1, N, qq.l, qq.r);
            if (res.best >= qq.w) lo[qi] = mid[qi];
            else hi[qi] = mid[qi] - 1;
        }
    };

    while (true) {
        bool any = false;
        for (int i = 0; i < Q; ++i) {
            if (lo[i] < hi[i]) {
                any = true;
                mid[i] = (lo[i] + hi[i] + 1) >> 1;
                bucket[mid[i]].push_back(i);
                if (!used[mid[i]]) {
                    used[mid[i]] = 1;
                    usedList.push_back(mid[i]);
                }
            }
        }
        if (!any) break;

        sort(usedList.begin(), usedList.end());
        // 같은 라운드: 임계 랭크 내림차순으로 처리하면서 인덱스 활성화 누적
        st.build(1, 1, N);
        int p = 0;
        for (int k = (int)usedList.size()-1; k >= 0; --k) {
            int t = usedList[k];
            while (p < N && rankH[order[p]] >= t) {
                st.update(1, 1, N, order[p]);
                ++p;
            }
            check_and_update(t);
        }

        for (int t : usedList) {
            bucket[t].clear();
            used[t] = 0;
        }
        usedList.clear();
    }

    for (int i = 0; i < Q; ++i) {
        cout << vals[lo[i]] << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `w = 1`: 정답은 `[l,r]` 내 최대 높이. 위 로직에서 자연스럽게 처리됩니다.
- 모든 높이 동일/단조: 활성화 순서·연속 1 병합이 올바르게 동작해야 합니다.
- `w = r-l+1`: 정답은 해당 구간의 최솟값입니다.
- 동일한 높이가 다수 존재: 좌표압축·랭크 비교에서 안정적으로 처리되어야 합니다.

## 제출 전 점검
- 입출력 형식 및 개행 확인(특히 다중 쿼리 출력 시 개행).
- 64-bit 오버플로 여부: 본 문제는 높이 출력(최솟값)이므로 `int`로 충분.
- 세그트리 병합 식 `best = max(left.best, right.best, left.suff + right.pref)` 확인.
- PBS 수렴 조건 `(lo < hi)`와 `mid = (lo+hi+1)/2`(상한 이분) 확인.

## 참고자료/유사문제
- 히스토그램 최대 직사각형(고정 너비 X): 1725번과 대비되는 변형. 여기서는 고정 너비 `w` + 쿼리가 핵심.


