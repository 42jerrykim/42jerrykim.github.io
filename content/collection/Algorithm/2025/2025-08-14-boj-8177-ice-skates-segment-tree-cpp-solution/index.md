---
title: "[Algorithm] C++ 백준 8177번: Ice Skates - 최대연속합 세그트리"
description: "사이즈 r인 사람은 [r, r+d]의 스케이트를 신을 수 있을 때, 매 이벤트마다 모든 사람에게 신발을 재분배할 수 있는지 판정합니다. p[i]-k 배열의 최대연속합이 d*k를 초과하는지 세그먼트 트리로 O(log N)에 확인하는 풀이를 정리합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Segment Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-8177
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
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Range Query
- 구간 질의
- Max Subarray
- 최대연속합
- Kadane
- 카데인
- Prefix Sum
- 접두사합
- Suffix Sum
- 접미사합
- Online Query
- 온라인 쿼리
- Point Update
- 점 갱신
- POI
- 폴란드 올림피아드
- Ice Skates
- 아이스 스케이트
- Array
- 배열
- Sliding Window
- 슬라이딩윈도우
- Math
- 수학
- Greedy
- 그리디
- Validation
- 검증
- Debugging
- 디버깅
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8177
- 요약: 1..n 사이즈의 스케이트가 각 k쌍씩 있고, 사이즈 r의 사람은 [r, r+d] 범위의 스케이트를 신을 수 있습니다. 사람의 출입 이벤트가 순서대로 주어질 때, 매 순간 모든 사람에게 조건을 만족하도록 재분배가 가능한지 판정합니다.

## 입력/출력
```
입력
n m k d
이후 m줄: r x   (사이즈 r의 사람이 x명 변화; x>0 입장, x<0 퇴장)

출력
각 이벤트 이후 재분배 가능하면 "TAK", 불가능하면 "NIE"
```

## 접근 개요
- 핵심 관찰: 사이즈 i를 신을 수 있는 사람 수를 p[i]라 하면, 항상 각 사이즈에 k쌍이 있으므로 q[i] = p[i] - k를 정의합니다.
- 재분배가 가능하려면 임의의 연속 구간의 초과 수요가 창고의 윈도우 폭 d로 상쇄 가능해야 합니다. 이는 q의 최대연속합이 d*k를 초과하지 않아야 함으로 귀결됩니다.
- 매 이벤트는 `p[r] += x` → `q[r] += x`의 점 갱신이므로, 세그먼트 트리로 전 구간 최대연속합을 유지하면 O(log N)으로 판정 가능합니다.

## 알고리즘 설계
- 상태: 세그먼트 트리 각 노드에서 (총합, 최대 접두사 합, 최대 접미사 합, 최대 연속합)을 유지합니다.
- 점 갱신: q[pos]에 delta를 더한 뒤, 부모로 합성합니다.
- 질의: 루트 노드의 최대 연속합이 곧 q 전체의 최대연속합입니다.
- 판정: `maxSubarray(q) > d*k` 이면 불가능("NIE"), 아니면 가능("TAK").
- 정당성 요지: 윈도우 폭 d는 한 사람의 허용 사이즈 이동 가능 범위이며, k는 각 사이즈의 공급량이다. 연속 구간의 초과 총수요가 d 구간만큼의 공급으로 흡수되지 못하면 어느 배치에서도 모순이 발생한다. 따라서 최대연속합이 임계치 d*k를 넘는지만 보면 충분하다.

## 복잡도
- 시간: O(m log n)
- 공간: O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Node {
    long long total;
    long long bestPrefix;
    long long bestSuffix;
    long long bestSubarray;
    Node(long long v = 0) : total(v), bestPrefix(v), bestSuffix(v), bestSubarray(v) {}
};

Node mergeNode(const Node& L, const Node& R) {
    Node res;
    res.total = L.total + R.total;
    res.bestPrefix = max(L.bestPrefix, L.total + R.bestPrefix);
    res.bestSuffix = max(R.bestSuffix, R.total + L.bestSuffix);
    res.bestSubarray = max({L.bestSubarray, R.bestSubarray, L.bestSuffix + R.bestPrefix});
    return res;
}

struct SegTree {
    int n;
    vector<Node> tree;
    vector<long long> val;
    SegTree(int n_, long long base) : n(n_), tree(4*n_), val(n_+1, base) {
        build(1, 1, n);
    }
    void build(int idx, int l, int r) {
        if (l == r) { tree[idx] = Node(val[l]); return; }
        int mid = (l + r) >> 1;
        build(idx<<1, l, mid);
        build(idx<<1|1, mid+1, r);
        tree[idx] = mergeNode(tree[idx<<1], tree[idx<<1|1]);
    }
    void update(int pos, long long delta) { update(1, 1, n, pos, delta); }
    void update(int idx, int l, int r, int pos, long long delta) {
        if (l == r) {
            val[pos] += delta;
            tree[idx] = Node(val[pos]);
            return;
        }
        int mid = (l + r) >> 1;
        if (pos <= mid) update(idx<<1, l, mid, pos, delta);
        else update(idx<<1|1, mid+1, r, pos, delta);
        tree[idx] = mergeNode(tree[idx<<1], tree[idx<<1|1]);
    }
    long long maxSubarray() const { return tree[1].bestSubarray; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    long long k, d;
    if (!(cin >> n >> m >> k >> d)) return 0;

    // q[i] = p[i] - k. 시작값은 -k
    SegTree st(n, -k);

    for (int i = 0; i < m; ++i) {
        int r; long long x;
        cin >> r >> x;
        st.update(r, x);
        cout << (st.maxSubarray() > k * d ? "NIE" : "TAK") << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- x<0(퇴장) 시, 해당 사이즈의 현재 인원보다 더 많이 빠지는 입력은 주어지지 않음을 가정(문제 조건).
- d=0인 극단: 모든 사람은 자신의 사이즈만 가능 → `maxSubarray(q) <= 0` 여부와 동일.
- n=1, m=1과 같은 최소값 경계.
- x의 절댓값이 커서 누적 합이 32-bit를 넘을 수 있으므로 64-bit 사용.

## 제출 전 점검
- 입출력 형식 및 개행 확인, 빠른 입출력 사용.
- 세그먼트 트리 노드 병합에서 접두/접미/최대연속합 정의 확인.
- 초기값 q[i] = -k 설정과 점 갱신 시 부호(+x) 일관성 확인.

## 참고자료
- 블로그 해설(아이디어 요지): 최대연속합 세그먼트 트리로 판정
- 세그트리 최대연속합 유지 기법: https://cp-algorithms.com/data_structures/segment_tree.html

