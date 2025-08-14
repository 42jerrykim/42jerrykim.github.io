---
title: "[Algorithm] cpp-python 백준 16404번: 주식회사 승범이네 - 서브트리 갱신·점 질의"
description: "회사 트리에서 직원 i와 그 하위 전체의 이익/손해를 일괄 반영하고 단일 직원의 잔액을 즉시 조회하는 문제입니다. 오일러 투어로 서브트리를 구간화하고 펜윅 트리 차분으로 구간 덧셈·점 질의를 O(log N)에 처리해 1초 제한을 안정적으로 통과합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16404
- cpp
- C++
- Fenwick Tree
- 펜윅트리
- Binary Indexed Tree
- 바이너리 인덱스 트리
- Euler Tour
- 오일러 투어
- 오일러 경로
- Subtree
- 서브트리
- Range Update
- 구간 갱신
- Point Query
- 점 질의
- Tree
- 트리
- DFS
- Iterative DFS
- 반복 DFS
- Graph
- 그래프
- Implementation
- 구현
- Data Structures
- 자료구조
- Prefix Sum
- 누적합
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
- Template
- 템플릿
- Testing
- 테스트
- Invariant
- 불변식
- Range Add
- 구간 추가
- Point Sum
- 점 합
- I/O Optimization
- 입출력 최적화
- Fast IO
- 빠른 입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16404
- 요약: 회사 트리가 주어지고, 명령 2가지 처리.
  - 1 i w: 직원 i와 i의 모든 부하(서브트리)에 w를 더함(손해면 음수).
  - 2 i: 직원 i의 현재 잔액을 출력.

### 제한/스펙
- N, M ≤ 100,000
- w ∈ [-10,000, 10,000]
- 루트는 1번, 2번째 줄에 각 노드의 부모(-1은 루트)

## 입출력 형식/예제
```
입력
N M
p1 p2 ... pN   # p1 = -1, pi는 i의 부모
M개의 줄의 명령: "1 i w" 또는 "2 i"

출력
각 "2 i" 명령마다 직원 i의 잔액을 한 줄에 하나씩 출력
```

예시(문제 본문 참고)

## 접근 개요(아이디어 스케치)
- 서브트리 일괄 갱신, 단일 노드 질의 → 트리의 서브트리를 연속 구간으로 펴기: 오일러 투어(진입 시간 `tin[u]`, 서브트리 끝 `tout[u]`).
- `[tin[u], tout[u]]`가 u 서브트리의 연속 구간이 된다.
- 구간 덧셈 + 점 질의는 펜윅 트리(BIT)에 차분 기법으로 구현 가능.
  - 구간 [L, R]에 +w: BIT.add(L, +w), BIT.add(R+1, -w)
  - 점 x의 값: BIT.prefix_sum(x)

### 시각화 (Mermaid)
```mermaid
flowchart TD
    A[Tree] -->|Euler Tour| B((tin/tout))
    B --> C[Subtree of u => [tin[u], tout[u]]]
    C --> D[BIT range add (diff)]
    D --> E[Query node i => prefix_sum(tin[i])]
```

## 알고리즘 설계
- 입력 트리에서 각 노드의 자식 목록을 만든 후, 루트(1)에서 DFS로 오일러 투어 인덱스 계산.
- 명령 처리:
  - 타입 1: `fw.range_add(tin[i], tout[i], w)`
  - 타입 2: `ans = fw.sum(tin[i])`
- 정당성:
  - 오일러 투어로 서브트리가 연속 구간으로 매핑되므로, 해당 구간에 동일 가중치 w를 더하면 서브트리 전체에 동일 변화를 준 것과 같다.
  - BIT의 차분 기법은 임의 점의 누적 변경량을 prefix sum으로 정확히 복원한다.

## 복잡도
- 전처리 DFS: O(N)
- 각 명령: O(log N)
- 전체: O((N + M) log N), 메모리 O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> bit;
    Fenwick(int n) : n(n), bit(n + 1, 0) {}
    void add(int idx, long long delta) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
    }
    void range_add(int l, int r, long long delta) {
        add(l, delta);
        if (r + 1 <= n) add(r + 1, -delta);
    }
    long long sum(int idx) const {
        long long res = 0;
        for (; idx > 0; idx -= idx & -idx) res += bit[idx];
        return res;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M; cin >> N >> M;
    vector<vector<int>> children(N + 1);
    for (int i = 1; i <= N; ++i) {
        int p; cin >> p;
        if (p != -1) children[p].push_back(i);
    }

    vector<int> tin(N + 1), tout(N + 1);
    int timer = 0;

    // Iterative DFS for Euler tour
    stack<pair<int,int>> st; // node, state(0=enter,1=exit)
    st.push({1, 0});
    while (!st.empty()) {
        auto [u, s] = st.top(); st.pop();
        if (s == 0) {
            tin[u] = ++timer;
            st.push({u, 1});
            for (int k = (int)children[u].size() - 1; k >= 0; --k) st.push({children[u][k], 0});
        } else {
            tout[u] = timer;
        }
    }

    Fenwick fw(N);
    for (int q = 0; q < M; ++q) {
        int t; cin >> t;
        if (t == 1) {
            int i; long long w; cin >> i >> w;
            fw.range_add(tin[i], tout[i], w);
        } else {
            int i; cin >> i;
            cout << fw.sum(tin[i]) << '\n';
        }
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def main():
    N, M = map(int, input().split())
    parents = list(map(int, input().split()))
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        p = parents[i - 1]
        if p != -1:
            children[p].append(i)

    tin = [0] * (N + 1)
    tout = [0] * (N + 1)
    timer = 0

    stack = [(1, 0)]  # (node, state) 0=enter,1=exit
    while stack:
        u, s = stack.pop()
        if s == 0:
            timer += 1
            tin[u] = timer
            stack.append((u, 1))
            for v in reversed(children[u]):
                stack.append((v, 0))
        else:
            tout[u] = timer

    bit = [0] * (N + 2)

    def add(idx, delta):
        while idx <= N:
            bit[idx] += delta
            idx += idx & -idx

    def range_add(l, r, delta):
        add(l, delta)
        if r + 1 <= N:
            add(r + 1, -delta)

    def sum_(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s

    out_lines = []
    for _ in range(M):
        parts = input().split()
        if parts[0] == '1':
            i = int(parts[1]); w = int(parts[2])
            range_add(tin[i], tout[i], w)
        else:
            i = int(parts[1])
            out_lines.append(str(sum_(tin[i])))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- N=1, M=1에서 단일 갱신/질의
- 한쪽으로 치우친 트리(체인)
- 자식이 없는 리프에 대한 갱신/질의
- w가 음수/양수/0
- 반복 갱신 후 동일 노드 질의(누적 검증)
- 입력이 최대치(N=M=1e5)에서 시간/메모리 한계 검증

## 제출 전 점검
- 오일러 투어 인덱스 범위: 1..N, `tout[u]` 포함 범위 확인
- BIT 인덱싱(1-based) 일치 여부
- 출력 개행, fast I/O 설정 확인

## 참고자료
- 펜윅 트리(BIT) 기본기: 구간 업데이트/점 질의 차분 기법
- 트리의 서브트리 쿼리와 오일러 투어 매핑


