---
title: "[Algorithm] cpp-python 백준 16993번: 연속합과 쿼리 (세그먼트 트리)"
description: "길이 N(≤100,000) 수열에 대해 구간 [i,j]의 최대 연속합을 O(log N)으로 질의하는 세그먼트 트리 풀이입니다. 각 노드에 합·최대 접두/접미합·구간 최대합을 저장하고 병합 규칙으로 정답을 계산합니다. 음수 전용 구간·단일 원소·전부 음수인 경우를 안전하게 처리하며, 시간·공간 복잡도와 실수 포인트를 정리했습니다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- Algorithm
- Segment Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16993
- cpp
- python
- C++
- Python
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Range Query
- 구간 질의
- Maximum Subarray
- 최대 연속합
- Kadane
- 카데인
- Divide and Conquer
- 분할정복
- Merge
- 병합
- Prefix Sum
- 접두합
- Suffix Sum
- 접미합
- Subarray
- 부분배열
- Interval
- 인터벌
- Query
- 쿼리
- Offline
- 온라인 질의
- Online Query
- 온라인 쿼리
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(log N)
- 로그 시간
- O(N)
- 선형 시간
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Implementation
- 구현
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
- Sliding Window
- 슬라이딩윈도우
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
- Dijkstra
- 다익스트라
- Binary Search
- 이분탐색
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
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---
## 문제 정보
- 문제: https://www.acmicpc.net/problem/16993
- 요약: 길이 N(≤100,000)의 수열 A와 M(≤100,000)개의 질의가 주어짐. 각 질의 `i j`마다 구간 A[i..j]의 최대 연속합을 출력. 원소는 음수 포함, 부분수열은 비어 있을 수 없고 적어도 1개 원소를 선택해야 함. 인덱스는 1부터.
- 제한: 시간 2초, 메모리 512MB, |A[k]| ≤ 1000
## 입출력 형식/예제
```text
입력
N
A1 A2 ... AN
M
i1 j1
i2 j2
...
```
```text
출력
각 질의에 대한 최대 연속합을 한 줄에 하나씩
```
예시(문제 원문 참고):
```text
10
10 -4 3 1 5 6 -35 12 21 -1
10
1 1
3 4
1 6
2 6
6 6
7 7
8 9
8 10
1 10
5 8
```

## 접근 개요(아이디어)

- 구간 최대 연속합은 세그먼트 트리 노드에 4개 값을 저장하면 병합으로 구할 수 있습니다.
  - sum: 구간 합
  - pref: 구간 최대 접두합
  - suff: 구간 최대 접미합
  - best: 구간 최대 연속합
- 두 구간 L, R을 병합할 때:
  - sum = L.sum + R.sum
  - pref = max(L.pref, L.sum + R.pref)
  - suff = max(R.suff, R.sum + L.suff)
  - best = max(L.best, R.best, L.suff + R.pref)
- 질의 [i, j]는 트리에서 O(log N) 노드 병합으로 처리합니다. 모든 값이 음수인 구간도 올바르게 처리됩니다(리프가 해당 값으로 초기화되기 때문).

## 알고리즘 설계

- 자료구조: 세그먼트 트리(1-indexed)
- 노드 정의: {sum, pref, suff, best}
- 항등 노드: 쿼리에서 벗어난 구간은 `best=pref=suff=-INF, sum=0` 로 간주하여 병합 항등원 역할 수행
- 올바름 근거:
  1) 리프에서 각 값은 정의에 부합
  2) 병합 공식은 접두/접미/내부 최댓값의 완전한 분할을 포괄
  3) 귀납적으로 모든 내부 노드에서 불변 유지 → 쿼리 합성으로 정답 도출
의사코드(병합 핵심):
```text
merge(L, R):
  sum  = L.sum + R.sum
  pref = max(L.pref, L.sum + R.pref)
  suff = max(R.suff, R.sum + L.suff)
  best = max(L.best, R.best, L.suff + R.pref)
```
## 복잡도
- 전처리(빌드): O(N)
- 각 질의: O(log N)
- 공간: O(N)
## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;
struct Node {
    long long sum;
    long long pref;
    long long suff;
    long long best;
};
static const long long NEG_INF = -(long long)4e18;
Node make_leaf(long long x) { return {x, x, x, x}; }
Node identity_node() { return {0, NEG_INF, NEG_INF, NEG_INF}; }
Node merge_node(const Node& a, const Node& b) {
    if (a.best == NEG_INF) return b; // a가 항등이면 b 그대로
    if (b.best == NEG_INF) return a; // b가 항등이면 a 그대로
    Node c;
    c.sum  = a.sum + b.sum;
    c.pref = max(a.pref, a.sum + b.pref);
    c.suff = max(b.suff, b.sum + a.suff);
    c.best = max({a.best, b.best, a.suff + b.pref});
    return c;
}
struct SegTree {
    int n;
    vector<Node> st;
    SegTree() {}
    explicit SegTree(const vector<long long>& arr) { init(arr); }
    void init(const vector<long long>& arr) {
        n = (int)arr.size() - 1; // 1-indexed
        st.assign(4 * n, identity_node());
        build(1, 1, n, arr);
    }
    void build(int p, int l, int r, const vector<long long>& arr) {
        if (l == r) { st[p] = make_leaf(arr[l]); return; }
        int m = (l + r) >> 1;
        build(p << 1, l, m, arr);
        build(p << 1 | 1, m + 1, r, arr);
        st[p] = merge_node(st[p << 1], st[p << 1 | 1]);
    }
    Node query(int p, int l, int r, int ql, int qr) const {
        if (qr < l || r < ql) return identity_node();
        if (ql <= l && r <= qr) return st[p];
        int m = (l + r) >> 1;
        Node L = query(p << 1, l, m, ql, qr);
        Node R = query(p << 1 | 1, m + 1, r, ql, qr);
        return merge_node(L, R);
    }
    long long query_best(int l, int r) const { return query(1, 1, n, l, r).best; }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N; if (!(cin >> N)) return 0;
    vector<long long> A(N + 1);
    for (int i = 1; i <= N; ++i) cin >> A[i];
    SegTree seg(A);
    int M; cin >> M;
    while (M--) {
        int l, r; cin >> l >> r;
        cout << seg.query_best(l, r) << '\n';
    }
    return 0;
}
```
## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
NEG_INF = -4_000_000_000_000_000_000
class Node:
    __slots__ = ("sum", "pref", "suff", "best")
    def __init__(self, s, p, sf, b):
        self.sum = s
        self.pref = p
        self.suff = sf
        self.best = b
def make_leaf(x):
    return Node(x, x, x, x)
def identity_node():
    return Node(0, NEG_INF, NEG_INF, NEG_INF)
def merge_node(a: Node, b: Node) -> Node:
    if a.best == NEG_INF: return b
    if b.best == NEG_INF: return a
    s = a.sum + b.sum
    p = max(a.pref, a.sum + b.pref)
    sf = max(b.suff, b.sum + a.suff)
    bst = max(a.best, b.best, a.suff + b.pref)
    return Node(s, p, sf, bst)
class SegTree:
    def __init__(self, arr):
        self.n = len(arr) - 1  # 1-indexed
        self.st = [identity_node()] * (4 * self.n)
        self._build(1, 1, self.n, arr)
    def _build(self, p, l, r, arr):
        if l == r:
            self.st[p] = make_leaf(arr[l])
            return
        m = (l + r) // 2
        self._build(p * 2, l, m, arr)
        self._build(p * 2 + 1, m + 1, r, arr)
        self.st[p] = merge_node(self.st[p * 2], self.st[p * 2 + 1])
    def _query(self, p, l, r, ql, qr):
        if qr < l or r < ql:
            return identity_node()
        if ql <= l and r <= qr:
            return self.st[p]
        m = (l + r) // 2
        L = self._query(p * 2, l, m, ql, qr)
        R = self._query(p * 2 + 1, m + 1, r, ql, qr)
        return merge_node(L, R)
    def query_best(self, l, r):
        return self._query(1, 1, self.n, l, r).best
def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    try:
        N = int(next(it))
    except StopIteration:
        return
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    seg = SegTree(A)
    M = int(next(it))
    out_lines = []
    for _ in range(M):
        l = int(next(it)); r = int(next(it))
        out_lines.append(str(seg.query_best(l, r)))
    sys.stdout.write("\n".join(out_lines))
if __name__ == "__main__":
    main()
```
## 코너 케이스 체크리스트
- 단일 원소 구간(리프) 질의 — 해당 값 그대로 출력되는가
- 전부 음수인 구간 — 최댓값은 가장 덜 음수인 원소 하나가 됨
- 큰 음수/양수 교차 — `L.suff + R.pref` 가 최댓값이 되는지
- 동일 인덱스 다수 질의 — 캐시 없이도 O(log N) 이내 처리
## 제출 전 점검
- 입출력 개행/버퍼링, 64-bit 정수 사용(C++)
- 항등 노드(범위 밖) 처리 누락 여부
- 인덱스(1-indexed) 일관성 유지
## 참고자료/유사문제
- 세그먼트 트리 최대 연속합: cp-algorithms — Maximum subarray sum with segment tree
