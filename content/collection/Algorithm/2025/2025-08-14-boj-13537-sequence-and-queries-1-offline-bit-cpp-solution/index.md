---
title: "[Algorithm] C++ 백준 13537번: 수열과 쿼리 1 - 오프라인 BIT"
description: "값과 쿼리의 k를 내림차순으로 정렬해 A[i] > k인 위치만 Fenwick 트리에 활성화하고, 각 질의 [i,j,k]는 구간 합으로 k보다 큰 원소 개수를 구합니다. 전체 O((N+M)logN)로 해결하며, 1-기반 인덱스·경계·오버플로·빠른 입출력 등 실수 포인트를 점검합니다."
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
- Problem-13537
- cpp
- C++
- Data Structures
- 자료구조
- Range Query
- 구간쿼리
- Offline Queries
- 오프라인 쿼리
- Fenwick Tree
- 펜윅트리
- BIT
- Binary Indexed Tree
- Merge Sort Tree
- 머지소트트리
- Segment Tree
- 세그먼트 트리
- Count Greater Than K
- k보다큰개수
- Counting
- 카운팅
- Sorting
- 정렬
- Prefix Sum
- 누적합
- Two Pointers
- 투포인터
- Binary Search
- 이분탐색
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
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
- Testing
- 테스트
- Invariant
- 불변식
- Array
- 배열
- Query Sorting
- 쿼리정렬
- Offline Processing
- 오프라인 처리
- 1-based Index
- 1-기반 인덱스
- Fast IO
- 빠른 입출력
- 수열과 쿼리 1
- Sequence and Queries 1
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13537
- 요약: 길이 \(N\)의 수열 `A[1..N]`가 주어질 때, 각 질의 `i j k`에 대해 부분 수열 `A[i..j]`에서 `k`보다 큰 원소의 개수를 출력합니다. \(N, M \le 10^5\), 값의 범위는 최대 \(10^9\)입니다.

## 입력/출력
```
<입력>
N
A1 A2 ... AN
M
i j k   (M줄)

<출력>
각 쿼리의 정답을 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심 아이디어: 값 기준 오프라인 처리. `A`의 원소와 질의의 `k`를 모두 내림차순으로 보며, 현재 `k`보다 큰 원소들만 Fenwick 트리(BIT)에 1로 활성화합니다.
- 그러면 쿼리 `i j k`의 답은 "활성화된 인덱스의 개수"인 \(\text{sum}(j)-\text{sum}(i-1)\)이 됩니다.

```mermaid
flowchart LR
  A[배열 A를 값 내림차순 정렬] --> C
  B[쿼리 (i,j,k)들을 k 내림차순 정렬] --> C
  C{다음 쿼리의 k?} -->|A[p].val > k| D[BIT.add(A[p].idx, 1) 반복]
  D --> C
  C -->|준비 완료| E[답 = BIT.sum(j) - BIT.sum(i-1)]
```

## 알고리즘 설계
- 정렬
  - 배열 항목 `(value, index)`를 value 내림차순으로 정렬합니다.
  - 쿼리 `(i, j, k, id)`를 `k` 내림차순으로 정렬합니다.
- 처리
  - 포인터 `p`를 앞에서부터 진행시키며 `A[p].value > k`인 동안 `BIT.add(A[p].index, +1)` 수행.
  - 이후 구간 합으로 `i..j`의 활성 개수를 답으로 저장합니다.
- 올바름 근거(요지)
  - 쿼리의 `k`가 작아질수록 활성 원소(조건 `A[t] > k`를 만족)가 단조 증가합니다. 한 번 활성화한 인덱스는 이후 모든 더 작은 `k`에 대해 항상 유효하므로, 각 A[i]는 최대 1회만 `add`됩니다. 따라서 전체 시간은 \(O((N+M)\log N)\)입니다.

## 복잡도
- 시간: \(O((N + M) \log N)\)
- 공간: \(O(N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<int> bit;
    Fenwick(int n) : n(n), bit(n + 1, 0) {}
    void add(int i, int v) {
        for (; i <= n; i += i & -i) bit[i] += v;
    }
    int sum(int i) const {
        int s = 0;
        for (; i > 0; i -= i & -i) s += bit[i];
        return s;
    }
};

struct Query { int l, r, k, idx; };

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; if(!(cin >> N)) return 0;
    vector<pair<int,int>> arr(N); // {value, index(1-based)}
    for(int i=0;i<N;++i){ int a; cin >> a; arr[i] = {a, i+1}; }

    int M; cin >> M;
    vector<Query> qs(M);
    for(int i=0;i<M;++i){ int l,r,k; cin >> l >> r >> k; qs[i] = {l,r,k,i}; }

    sort(arr.begin(), arr.end(), [](const auto& x, const auto& y){ return x.first > y.first; });
    sort(qs.begin(), qs.end(), [](const Query& a, const Query& b){ return a.k > b.k; });

    Fenwick fw(N);
    vector<int> ans(M);
    int p = 0; // pointer in arr
    for(const auto& q : qs){
        while(p < N && arr[p].first > q.k){
            fw.add(arr[p].second, 1);
            ++p;
        }
        ans[q.idx] = fw.sum(q.r) - fw.sum(q.l - 1);
    }

    for(int i=0;i<M;++i) cout << ans[i] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `i = j` 단일 원소 구간, `k`가 매우 작거나 매우 큰 경우(0 또는 \(10^9\) 근처)
- 모든 값이 동일/모두 상이한 경우
- 인덱스 1-기반 일관성(`fw.sum(i-1)` 처리, `arr`의 `index = i+1`)
- 큰 입력에서 빠른 입출력 및 정렬의 안정성

## 제출 전 점검
- 입출력 형식/개행, `sync_with_stdio(false)`, `tie(nullptr)` 적용 확인
- 오프라인 정렬 순서: 값/쿼리 `k` 모두 내림차순인지 확인
- BIT 범위 및 경계: `add(1..N)`, `sum(0) = 0` 가정하에 `i-1` 처리

## 참고자료/유사문제
- Fenwick Tree(BIT), 오프라인 쿼리 처리 패턴
- 대안: Merge Sort Tree로 \(O(\log^2 N)\) 질의 처리(노드 정렬 벡터에서 `upper_bound`)


