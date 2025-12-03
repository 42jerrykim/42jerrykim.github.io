---
title: "[Algorithm] C++ 백준 13547번: 수열과 쿼리 5 - Mo 알고리즘"
description: "Mo 알고리즘으로 구간 [L,R]의 서로 다른 값 개수를 오프라인으로 처리합니다. 좌우 포인터 이동 시 빈도와 distinct를 유지하고, 좌표압축으로 메모리를 줄입니다. 정렬 O(Q log Q), 전체 O((N+Q)√N), 경계 이동 순서·0-index 변환·freq 0↔1 갱신 실수 방지까지 정리합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Mo's Algorithm
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13547
- cpp
- C++
- Python
- Competitive Programming
- 경쟁프로그래밍
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
- Testing
- 테스트
- Code Review
- 코드리뷰
- Template
- 템플릿
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
- BFS
- DFS
- Shortest Path
- 최단경로
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
- Mo's Algorithm
- Mo
- Offline Queries
- 오프라인 쿼리
- Distinct Count
- 서로다른값개수
- Frequency Array
- 빈도배열
- Coordinate Compression
- 좌표압축
- Sqrt Decomposition
- 제곱근분할
- Query Reordering
- 쿼리정렬
- Range Query
- 구간쿼리
- Array
- 배열
- Optimization
- 최적화
image: "wordcloud.png"
---

## 문제
- **링크**: [BOJ 13547 - 수열과 쿼리 5](https://www.acmicpc.net/problem/13547)
- **요약**: 길이 \(N\)의 수열이 주어지고, 여러 구간 \([L, R]\)에 대해 그 구간 내 서로 다른 값의 개수를 질의합니다. 모든 질의를 빠르게 처리해야 합니다.
- **제한/스펙(요지)**: \(N, Q \le 10^5\) 수준, 값의 범위는 크며, 온라인 처리보다 오프라인 정렬을 활용한 고효율 알고리즘이 필요합니다.

## 입력/출력
```
입력
N
a1 a2 ... aN
Q
L1 R1
...
LQ RQ

출력
각 질의 [Li, Ri]에 대한 서로 다른 값의 개수를 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심은 구간을 움직이며 추가/제거만으로 답을 갱신하는 **Mo 알고리즘**입니다.
- 질의를 블록 단위(크기 \(\approx\sqrt{N}\))로 정렬해 **현재 구간**을 조금씩 이동시키며, 값의 **빈도 배열**과 **distinct 개수**만 업데이트합니다.
- 값 범위가 클 수 있으므로 **좌표압축**으로 메모리와 인덱싱을 안정화합니다.

```mermaid
flowchart LR
  A[질의 정렬 (Mo Order)] --> B{curL, curR}
  B -->|L 확장| C[add(a[--curL])]
  B -->|R 확장| D[add(a[++curR])]
  B -->|L 축소| E[remove(a[curL++])]
  B -->|R 축소| F[remove(a[curR--])]
  C --> G[distinct 업데이트]
  D --> G
  E --> G
  F --> G
  G --> H[정답 저장]
```

## 알고리즘 설계
- **정렬 기준**: \( (L/\text{block}, R) \) 기준으로 정렬. 같은 블록 내에서는 \(R\)을 지그재그(odd-even)로 정렬해 이동량을 줄입니다.
- **유지 정보**:
  - `freq[x]`: 현재 구간에서 값 `x`의 출현 횟수
  - `distinct`: `freq[x]`가 0에서 1이 될 때 +1, 1에서 0이 될 때 -1
- **좌표압축**: 원소들을 정렬·유일화 후 인덱스로 매핑해 `freq` 크기를 유한하게 유지.
- **정당성 요약**: 모든 질의를 동일한 규칙으로 정렬한 뒤, 각 스텝에서 add/remove는 O(1)이고, 질의마다 총 이동 횟수 합이 \(O((N+Q)\sqrt{N})\)로 수렴하므로 전체 시간 상한을 만족합니다.

## 복잡도
- 시간: \(O(Q \log Q)\) (정렬) + \(O((N+Q)\sqrt{N})\) (이동·갱신)
- 공간: \(O(N)\) (배열, 빈도, 보조 구조)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int l, r, idx, block;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    // Coordinate compression
    vector<int> comp = a;
    sort(comp.begin(), comp.end());
    comp.erase(unique(comp.begin(), comp.end()), comp.end());
    for (int i = 0; i < n; ++i) {
        a[i] = int(lower_bound(comp.begin(), comp.end(), a[i]) - comp.begin());
    }
    int m = int(comp.size());

    int q;
    cin >> q;
    vector<Query> queries(q);
    int blockSize = max(1, int(sqrt(n)));
    for (int i = 0; i < q; ++i) {
        int l, r;
        cin >> l >> r;
        --l; --r; // convert to 0-indexed
        queries[i] = {l, r, i, l / blockSize};
    }

    sort(queries.begin(), queries.end(), [&](const Query& A, const Query& B) {
        if (A.block != B.block) return A.block < B.block;
        if (A.block & 1) return A.r > B.r; // odd-even trick
        return A.r < B.r;
    });

    vector<int> freq(m, 0);
    vector<int> ans(q);
    int distinct = 0;

    auto add = [&](int x) {
        if (freq[x] == 0) ++distinct;
        ++freq[x];
    };
    auto remove = [&](int x) {
        --freq[x];
        if (freq[x] == 0) --distinct;
    };

    int curL = 0, curR = -1; // current range is empty
    for (const auto& qu : queries) {
        int L = qu.l, R = qu.r;
        while (curL > L) add(a[--curL]);
        while (curR < R) add(a[++curR]);
        while (curL < L) remove(a[curL++]);
        while (curR > R) remove(a[curR--]);
        ans[qu.idx] = distinct;
    }

    for (int i = 0; i < q; ++i) {
        cout << ans[i] << '\n';
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
def solve():
    input = sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))

    # Coordinate compression
    comp = sorted(set(a))
    comp_index = {v: i for i, v in enumerate(comp)}
    a = [comp_index[v] for v in a]
    m = len(comp)

    q = int(input().strip())
    queries = []
    import math
    block = max(1, int(math.sqrt(n)))
    for idx in range(q):
        l, r = map(int, input().split())
        l -= 1; r -= 1
        queries.append((l // block, r if (l // block) % 2 == 0 else -r, l, r, idx))

    queries.sort()

    freq = [0] * m
    ans = [0] * q
    distinct = 0

    def add(x):
        nonlocal distinct
        if freq[x] == 0:
            distinct += 1
        freq[x] += 1

    def remove(x):
        nonlocal distinct
        freq[x] -= 1
        if freq[x] == 0:
            distinct -= 1

    curL, curR = 0, -1
    for _, _, L, R, idx in queries:
        while curL > L:
            curL -= 1
            add(a[curL])
        while curR < R:
            curR += 1
            add(a[curR])
        while curL < L:
            remove(a[curL])
            curL += 1
        while curR > R:
            remove(a[curR])
            curR -= 1
        ans[idx] = distinct

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- `L == R` 단일 원소 구간
- 모든 값이 동일/모두 상이한 극단 패턴
- 구간이 배열 양 끝을 스치며 반복 이동하는 경우
- 0-index 변환 누락 및 경계 이동 순서로 인한 off-by-one
- 빈도 0→1, 1→0 전환 시 `distinct` 증감 누락

## 제출 전 점검
- 입출력 형식과 개행 확인, 빠른 입출력 사용 여부 점검
- 64-bit 정수 범위 문제는 없는지 확인(여기선 주로 int로 충분)
- 좌표압축 결과 크기(`m`)로 빈도 배열 크기 적절히 생성했는지 확인
- 질의 정렬(블록, 지그재그) 구현 일관성 확인

## 참고자료
- [cp-algorithms: Mo's algorithm](https://cp-algorithms.com/data_structures/sqrt_decomposition.html#mos-algorithm)
- [Mo's algorithm explained (blog)](https://blog.anudeep2011.com/mos-algorithm/)


