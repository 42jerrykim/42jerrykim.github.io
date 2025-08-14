---
title: "[Algorithm] cpp-python 백준 8227번: Cloakroom"
description: "시점 m에 a≤m, b>m+s인 물건만 선택 가능. 이 집합에서 합이 정확히 k가 되는지 비트셋 부분합 DP로 판정한다. 질의를 B=m+s로 그룹화해 m 오름차순으로 아이템을 추가하며 정답을 빠르게 계산한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- DP
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-8227
- cpp
- python
- C++
- Python
- Data Structures
- 자료구조
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
- Bitset
- 비트셋
- Subset Sum
- 부분합
- Knapsack
- 배낭문제
- Offline Queries
- 오프라인 질의
- Sorting
- 정렬
- Graph
- 그래프
- Math
- 수학
- String
- 문자열
- Geometry
- 기하
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- Disjoint Set Union
- 유니온파인드
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Dijkstra
- 다익스트라
- Shortest Path
- 최단경로
- POI
- POI-2012
- Cloakroom
image: "wordcloud.png"
---

## 문제
- **링크**: https://www.acmicpc.net/problem/8227
- **요약**: 시점 m에 들어가 정확히 k의 가치를 훔치고, m+s 이전(엄밀히는 m+s 시각까지) 아무도 해당 물건을 찾으러 오지 않아야 한다. 따라서 선택 가능한 물건은 a≤m이며 동시에 b>m+s인 것들뿐이다. 이 집합에서 합이 정확히 k가 되는 부분집합 존재 여부를 판별한다.

## 입력/출력
- 입력: 물건 n(≤1000)과 각 물건의 가치 c(≤1000), 맡긴 시각 a, 찾는 시각 b(≤1e9)가 주어진다. 이어서 질의 p(≤1e6)개가 주어지고, 각 질의는 (m, k, s).
- 출력: 각 질의에 대해 정확히 k를 만들 수 있으면 "TAK", 아니면 "NIE".

## 접근 개요
- **핵심 관찰**: 질의 (m, k, s)에 대해 가능한 물건은 조건 a≤m, b>m+s를 동시에 만족하는 것들이다. 이 집합에서 정확히 k를 만들 수 있는지 확인하는 문제는 전형적인 부분합(0/1 Knapsack) 존재 여부 판정이다.
- **오프라인 전략**: 질의를 B=m+s로 묶어 그룹화하면, 동일 그룹에서는 포함/제외되는 물건의 b 조건이 동일하다. 그룹 내부는 m 오름차순으로 처리하며 a≤m인 물건을 순차적으로 추가만 한다.
- **DP 기법**: 비트셋 DP. `dp[x]=1`이면 합 x를 만들 수 있음을 의미. 물건 가치 c를 처리할 때 `dp |= (dp << c)`.

```mermaid
flowchart LR
    A[모든 질의 (m,k,s)] -->|B=m+s로 그룹화| G[그룹 r]
    G -->|m 오름차순| U[아이템 추가 (a≤m, b>B)]
    U --> D[비트셋 DP 갱신]
    D --> Q[dp[k] 확인 후 TAK/NIE]
```

## 알고리즘 설계
- **그룹화 기준**: B=m+s. `r = # of items with b ≤ B`를 미리 계산하면, 같은 r을 가진 질의들은 동일한 필터 `b > B`를 공유한다. (B가 `bSorted[r-1]`과 `bSorted[r]` 사이에 있으면 동일 집합)
- **처리 순서**: 그룹별로 m 오름차순 정렬 → 포인터로 `a≤m`인 물건을 차례로 보며, 해당 그룹의 필터 `b > B`를 만족하는 경우에만 DP에 추가.
- **DP 상태**: 비트셋 dp, 초기값 dp[0]=1. 가치 c를 만나면 `dp |= dp << c` 수행.
- **정당성**: 각 질의 시점에 가능한 물건 집합은 a와 b에 의해 완전히 결정되며, 비트셋 DP는 정확히 그 집합의 부분합 가능 여부를 보존한다. 그룹화는 포함/제외 기준(b) 고정을 통해 중복 작업을 제거한다.

## 복잡도
- 비트셋 길이 L≈⌈(Kmax+1)/64⌉. 각 물건 추가는 O(L). 그룹 수 ≤ n+1, 그룹 내 물건 추가 ≤ n. 대략 O(n·(n+1)·L) + O(p) 비트연산. n=1000, Kmax≤1e5에서 고성능 C++ 비트연산으로 충분히 통과 가능.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Item { int c; int a; int b; };
struct Query { long long m; int k; int id; };

static inline void add_value_inplace(vector<unsigned long long>& dp, int shiftWords, int shiftBits) {
    int L = (int)dp.size();
    if (shiftBits == 0) {
        for (int i = L - 1; i >= shiftWords; --i) dp[i] |= dp[i - shiftWords];
    } else {
        for (int i = L - 1; i > shiftWords; --i) {
            unsigned long long hi = dp[i - shiftWords] << shiftBits;
            unsigned long long lo = dp[i - shiftWords - 1] >> (64 - shiftBits);
            dp[i] |= (hi | lo);
        }
        if (shiftWords < L) dp[shiftWords] |= (dp[0] << shiftBits);
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; if(!(cin >> n)) return 0;
    vector<Item> items(n);
    for (int i = 0; i < n; ++i) cin >> items[i].c >> items[i].a >> items[i].b;

    vector<int> idxA(n); iota(idxA.begin(), idxA.end(), 0);
    sort(idxA.begin(), idxA.end(), [&](int i, int j){ return items[i].a < items[j].a; });

    vector<long long> bSorted(n);
    for (int i = 0; i < n; ++i) bSorted[i] = items[i].b;
    sort(bSorted.begin(), bSorted.end());

    int p; cin >> p;
    vector<vector<Query>> groups(n + 1);
    int Kmax = 0;
    vector<long long> Ms(p), Ss(p); vector<int> Ks(p);
    for (int i = 0; i < p; ++i) {
        long long m, s; int k; cin >> m >> k >> s;
        Ms[i] = m; Ss[i] = s; Ks[i] = k; Kmax = max(Kmax, k);
    }
    for (int i = 0; i < p; ++i) {
        long long B = Ms[i] + Ss[i];
        int r = (int)(upper_bound(bSorted.begin(), bSorted.end(), B) - bSorted.begin());
        groups[r].push_back(Query{Ms[i], Ks[i], i});
    }

    int L = (Kmax >> 6) + 1;
    vector<unsigned long long> dp(L);
    vector<char> ans(p, 0);

    for (int r = 0; r <= n; ++r) {
        if (groups[r].empty()) continue;
        sort(groups[r].begin(), groups[r].end(), [](const Query& x, const Query& y){
            if (x.m != y.m) return x.m < y.m; return x.id < y.id;
        });
        long long Bthres = (r > 0 ? bSorted[r - 1] : LLONG_MIN);
        fill(dp.begin(), dp.end(), 0ULL); dp[0] = 1ULL;
        int pos = 0;
        for (const auto& q : groups[r]) {
            while (pos < n && (long long)items[idxA[pos]].a <= q.m) {
                const Item& it = items[idxA[pos]];
                if ((long long)it.b > Bthres) {
                    int c = it.c; int w = c >> 6, b = c & 63;
                    add_value_inplace(dp, w, b);
                }
                ++pos;
            }
            ans[q.id] = (q.k <= Kmax && ((dp[q.k >> 6] >> (q.k & 63)) & 1ULL)) ? 1 : 0;
        }
    }

    for (int i = 0; i < p; ++i) cout << (ans[i] ? "TAK\n" : "NIE\n");
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def main():
    input = sys.stdin.readline
    n = int(input().strip())
    items = [tuple(map(int, input().split())) for _ in range(n)]  # (c,a,b)
    idxA = sorted(range(n), key=lambda i: items[i][1])
    b_sorted = sorted(it[2] for it in items)

    p = int(input().strip())
    Ms, Ks, Ss = [0]*p, [0]*p, [0]*p
    Kmax = 0
    for i in range(p):
        m, k, s = map(int, input().split())
        Ms[i], Ks[i], Ss[i] = m, k, s
        if k > Kmax:
            Kmax = k

    groups = [[] for _ in range(n+1)]
    import bisect
    for i in range(p):
        B = Ms[i] + Ss[i]
        r = bisect.bisect_right(b_sorted, B)
        groups[r].append((Ms[i], Ks[i], i))

    mask = (1 << (Kmax + 1)) - 1
    ans = [False] * p

    for r in range(n+1):
        if not groups[r]:
            continue
        groups[r].sort()  # sort by m, then id implicitly
        Bthres = b_sorted[r-1] if r > 0 else -10**30
        dp = 1  # bit 0 set
        pos = 0
        for m, k, qid in groups[r]:
            while pos < n and items[idxA[pos]][1] <= m:
                c, a, b = items[idxA[pos]]
                if b > Bthres:
                    dp = (dp | (dp << c)) & mask
                pos += 1
            if k <= Kmax:
                ans[qid] = ((dp >> k) & 1) == 1

    out = []
    for i in range(p):
        out.append("TAK" if ans[i] else "NIE")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- k=0 (dp[0]=1로 항상 가능), 하지만 입력 범위상 k≥1이므로 의미 확인
- m이 매우 작아 선택 가능한 물건이 없음 → 항상 "NIE"
- s가 매우 커서 b>m+s를 만족하는 물건이 없음 → 항상 "NIE"
- 동일한 a 또는 b를 가지는 물건 다수 → 그룹화/포인터 로직이 중복 추가 없이 동작하는지
- 가치 c가 Kmax보다 커서 빗셋 경계를 넘는 경우 → 내부 마스킹/워드 경계 처리 확인

## 제출 전 점검
- 출력 개행/형식 준수("TAK"/"NIE")
- 64-bit 정수 사용(시간 합산, 비교)
- dp 초기화와 그룹별 클리어 여부 확인
- 정렬 키(a, B=m+s)에 대한 안정성

## 참고자료/유사문제
- POI 2011/2012 SZA - Cloakroom 공식 문제 설명
- 부분합 존재 여부 비트셋 기법 및 오프라인 질의 처리 패턴


