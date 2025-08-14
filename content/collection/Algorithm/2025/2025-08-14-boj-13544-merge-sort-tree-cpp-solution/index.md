---
title: "[Algorithm] cpp 백준 13544번: 수열과 쿼리 3 - Merge Sort Tree"
description: "정렬된 구간 리스트를 저장한 Merge Sort Tree로 구간 [i,j]에서 k보다 큰 원소 개수를 온라인으로 계산합니다. 각 노드에서 upper_bound로 개수만 더해 O(log^2N) 질의, O(NlogN) 빌드. XOR last_ans 변형을 안전히 처리하는 구현 포인트와 엣지 케이스까지 정리합니다."
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
- Problem-13544
- cpp
- C++
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Merge Sort Tree
- 머지 소트 트리
- Merge Tree
- 머지 트리
- Range Query
- 구간 쿼리
- Online Query
- 온라인 쿼리
- XOR
- xor
- last_ans
- Binary Search
- 이분탐색
- upper_bound
- offline-vs-online
- 온라인 처리
- Query Processing
- 쿼리 처리
- Complexity Analysis
- 복잡도 분석
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
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Fast IO
- 빠른 입출력
- 1-based Index
- 1-기반 인덱스
- Sorting
- 정렬
- Vector
- 벡터
- STL
- 표준라이브러리
- upper-bound-count
- 카운팅 질의
- Greater Than
- 초과 개수
- Persistent Segment Tree
- 영속 세그먼트 트리
- Alternative Approach
- 대안 풀이
- NlogN
- log^2N
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13544
- 요약: 길이 \(N\)인 수열 `A[1..N]`이 주어질 때, 여러 쿼리마다 \([i,j]\) 구간에서 `k`보다 큰 원소의 개수를 출력합니다. 각 쿼리의 \(i, j, k\)는 입력의 \(a, b, c\)를 이전 정답 `last_ans`와 XOR하여 얻습니다(처음 `last_ans = 0`).
- 제한/스펙(요지): \(N, M \le 10^5\), 값 범위 \(\le 10^9\), 1초.

## 입력/출력
```
입력
N
A1 A2 ... AN
M
a b c  (M줄)

출력
각 쿼리마다 [i, j]에서 k보다 큰 원소의 개수를 한 줄에 하나씩 출력
```

## 접근 개요
- 정적 배열에 대한 순수 카운팅 질의이므로, 각 세그먼트 노드에 구간의 원소들을 "정렬된 리스트"로 저장하는 **Merge Sort Tree**가 적합합니다.
- 질의 \([i,j], k\)에서 커버되는 노드들의 리스트에 대해 `upper_bound(k)`로 "k보다 큰 개수"를 즉시 취합하면 됩니다.
- XOR `last_ans`로 인해 쿼리를 재정렬할 수 없으므로, **온라인 O(log^2 N)** 질의가 가능한 자료구조가 필요합니다.

```mermaid
flowchart TD
  A[Build: 각 노드에 정렬 리스트 저장] --> B[Query(i,j,k)]
  B --> C{세그먼트 분기}
  C -->|완전 포함| D[upper_bound로 개수 계산]
  C -->|부분 겹침| E[좌/우로 재귀 분기]
  E --> D
  D --> F[합산 결과 반환]
```

## 알고리즘 설계
- 빌드: 구간을 반으로 나누며 하위 노드의 정렬 리스트 두 개를 `merge`로 합성해 상위 노드를 구성합니다. 전체 \(O(N \log N)\).
- 질의: 세그먼트 트리에서 \([i,j]\)를 덮는 노드들에 대해 `upper_bound(k)` 위치부터 끝까지의 원소 개수를 더합니다. 노드 개수는 \(O(\log N)\), 각 노드에서 이분탐색 \(O(\log N)\) → 합계 \(O(\log^2 N)\).
- 정당성: 각 노드는 자신의 범위 내 값을 오름차순으로 모두 포함하며, \([i,j]\)의 분해는 서로 겹치지 않는 노드들의 합으로 표현됩니다. 따라서 노드별 "k 초과" 원소 수의 합이 정답과 일치합니다.
- 구현 포인트:
  - 입력 배열은 1-기반으로 들고, 트리도 1-기반 인덱스로 다룹니다.
  - `i > j`일 수 있으니 XOR 후 반드시 swap 처리.
  - `last_ans`는 이전 쿼리의 출력으로 갱신.
  - 값의 범위가 커도 정렬 리스트 기반이므로 좌표압축 불필요.

## 복잡도
- 빌드: \(O(N \log N)\)
- 질의: \(O(\log^2 N)\) (노드 방문 \(\log N\) × 각 노드 `upper_bound` \(\log N\))
- 공간: \(O(N \log N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct MergeSortTree {
    int n;
    vector<vector<int>> tree;

    MergeSortTree() = default;
    explicit MergeSortTree(const vector<int>& arr) { build(arr); }

    void build(const vector<int>& arr) {
        n = (int)arr.size() - 1; // arr is 1-indexed
        tree.assign(4 * n + 4, {});
        buildNode(1, 1, n, arr);
    }

    void buildNode(int node, int left, int right, const vector<int>& arr) {
        if (left == right) {
            tree[node] = { arr[left] };
            return;
        }
        int mid = (left + right) >> 1;
        buildNode(node << 1, left, mid, arr);
        buildNode(node << 1 | 1, mid + 1, right, arr);
        tree[node].resize(tree[node << 1].size() + tree[node << 1 | 1].size());
        merge(tree[node << 1].begin(), tree[node << 1].end(),
              tree[node << 1 | 1].begin(), tree[node << 1 | 1].end(),
              tree[node].begin());
    }

    // Count of elements > k in [ql, qr]
    int queryGreaterThan(int ql, int qr, int k) const {
        return queryNode(1, 1, n, ql, qr, k);
    }

    int queryNode(int node, int left, int right, int ql, int qr, int k) const {
        if (qr < left || right < ql) return 0;
        if (ql <= left && right <= qr) {
            const auto& vec = tree[node];
            auto it = upper_bound(vec.begin(), vec.end(), k);
            return (int)(vec.end() - it);
        }
        int mid = (left + right) >> 1;
        return queryNode(node << 1, left, mid, ql, qr, k)
             + queryNode(node << 1 | 1, mid + 1, right, ql, qr, k);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];

    MergeSortTree mst(a);

    int m;
    cin >> m;
    int last_ans = 0;

    while (m--) {
        int aa, bb, cc;
        cin >> aa >> bb >> cc;
        int i = aa ^ last_ans;
        int j = bb ^ last_ans;
        int k = cc ^ last_ans;
        if (i > j) swap(i, j);
        int ans = mst.queryGreaterThan(i, j, k);
        cout << ans << '\n';
        last_ans = ans;
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- XOR 후 `i > j`인 경우 swap 처리 누락 여부
- `k`가 매우 작거나 매우 큰 경우(노드 전부 또는 전무 카운트)
- 모든 값이 동일/모두 상이한 극단 패턴
- `N, M = 1` 소형 입력과 `10^5` 대규모 입력에서의 성능
- 1-기반 인덱싱 유지 일관성(입력/트리/질의 모두)

## 제출 전 점검
- 빠른 입출력 사용(`sync_with_stdio(false)`, `tie(nullptr)`) 확인
- 트리 빌드 후 즉시 질의 수행(온라인) 구조 확인
- `upper_bound` 반환값에서 개수 계산 시 캐스팅 및 오프셋 실수 방지
- 메모리 사용량(벡터 합계가 \(O(N \log N)\)) 허용 범위인지 확인

## 참고자료/유사문제
- Merge Sort Tree 개요: cp-algorithms의 Merge sort tree 설명
- 대안: Persistent Segment Tree로도 \(O(\log N)\) 질의 가능하나 구현 복잡도 증가


