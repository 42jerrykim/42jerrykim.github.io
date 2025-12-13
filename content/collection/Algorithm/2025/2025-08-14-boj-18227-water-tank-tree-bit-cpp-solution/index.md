---
title: "[Algorithm] C++ 백준 18227번: 성대나라의 물탱크"
description: "루트 C에서 시작하는 트리에서 \"A 도시에 물 채우기\"는 루트→A 경로의 각 정점 v에 깊이(v)+1 리터를 더합니다. 따라서 임의의 정점 v의 물의 양은 서브트리(v)에서 발생한 갱신 횟수 × (깊이(v)+1)로 환원됩니다. 오일러 투어로 트리를 평탄화하고 펜윅 트리(BIT)로 서브트리 구간의 갱신·질의를 처리해 O((N+Q)logN)에 해결합니다. 경계 입력과 64-bit 오버플로를 주의합니다."
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
- Problem-18227
- cpp
- C++
- Data Structures
- 자료구조
- Graph
- 그래프
- Tree
- 트리
- Rooted Tree
- 루트 트리
- Depth
- 깊이
- Ancestor
- 조상
- Subtree
- 서브트리
- DFS
- Euler Tour
- 오일러투어
- DFS Order
- DFS 순회
- Tree Flattening
- 트리 평탄화
- Fenwick Tree
- 펜윅트리
- BIT
- Binary Indexed Tree
- Range Sum
- 구간합
- Prefix Sum
- 누적합
- Range Query
- 구간 질의
- Subtree Query
- 서브트리 질의
- Point Update
- 점 업데이트
- Update
- 업데이트
- Query Processing
- 쿼리 처리
- Online Queries
- 온라인 처리
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Fast IO
- 빠른 입출력
- Long Long
- 64-bit
- Overflow
- 오버플로
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/18227
- 요약: 루트 `C`가 있는 트리. 쿼리 `1 A`: 루트→`A` 경로의 i번째 정점에 i 리터씩 더함(루트 1L, 다음 2L, ...). 쿼리 `2 A`: 현재 `A`에 저장된 총 물의 양을 출력.

## 입력/출력
```
<입력>
N C
N-1개의 간선
Q
Q개의 줄: (1 A) 또는 (2 A)

<출력>
각 (2 A) 쿼리의 정답을 한 줄에 하나씩 출력
```

## 접근 개요
- 관찰: 쿼리 `1 A`에서 경로 상 정점 `v`는 정확히 `depth(v)+1` 리터를 받습니다. 이는 `v`가 `A`의 조상일 때만 발생합니다.
- 따라서 임의의 정점 `v`의 총 물의 양은 `(# 서브트리(v)에서 발생한 1-쿼리 수) × (depth(v)+1)`로 표현됩니다.
- 트리를 오일러 투어로 평탄화해 `tin/tout` 구간을 만들면, "서브트리(v)에서 발생한 갱신 수"는 인덱스 구간 `[tin[v], tout[v]]`의 합으로 바뀝니다.
- 펜윅 트리(BIT) 하나로 `1 A`는 `add(tin[A], +1)`, `2 A`는 `sum(tin[A], tout[A]) × (depth[A]+1)`로 처리합니다.

## 알고리즘 설계
- 전처리: 루트 `C`에서 DFS하여 `depth[v]`, `tin[v]`, `tout[v]`를 계산합니다.
- 자료구조: 크기 `N`의 펜윅 트리 `F`.
- 연산
  - 갱신 `1 A`: `F.add(tin[A], +1)`
  - 질의 `2 A`: `cnt = F.sum(tin[A], tout[A])`, `answer = cnt * (depth[A] + 1)`
- 올바름 근거: 각 갱신은 경로 상 조상들에 동일 계수 `depth(v)+1`을 더하므로, `v`에 대한 총합은 계수×횟수의 곱입니다. 평탄화로 횟수는 서브트리 구간 합과 동치가 됩니다.

## 복잡도
- 시간: 전처리 `O(N)`, 각 쿼리 `O(log N)` → 전체 `O((N+Q) log N)`
- 공간: `O(N)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    vector<long long> bit;
    int n;
    Fenwick(int n) : n(n) { bit.assign(n + 1, 0); }
    void add(int idx, long long delta) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
    }
    long long sumPrefix(int idx) const {
        long long res = 0;
        for (; idx > 0; idx -= idx & -idx) res += bit[idx];
        return res;
    }
    long long sumRange(int l, int r) const {
        if (l > r) return 0;
        return sumPrefix(r) - sumPrefix(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int numCities, capital;
    if (!(cin >> numCities >> capital)) return 0;

    vector<vector<int>> adjacency(numCities + 1);
    for (int i = 0; i < numCities - 1; ++i) {
        int x, y; cin >> x >> y;
        adjacency[x].push_back(y);
        adjacency[y].push_back(x);
    }

    vector<int> tin(numCities + 1), tout(numCities + 1), depth(numCities + 1, 0), parent(numCities + 1, 0);
    int timer = 0;

    // Iterative DFS for Euler tour and depths
    stack<tuple<int, int, int>> dfsStack; // node, parent, state(0=enter,1=exit)
    dfsStack.emplace(capital, 0, 0);
    while (!dfsStack.empty()) {
        auto [node, par, state] = dfsStack.top();
        dfsStack.pop();
        if (state == 0) {
            parent[node] = par;
            tin[node] = ++timer;
            dfsStack.emplace(node, par, 1);
            for (int neighbor : adjacency[node]) {
                if (neighbor == par) continue;
                depth[neighbor] = depth[node] + 1;
                dfsStack.emplace(neighbor, node, 0);
            }
        } else {
            tout[node] = timer;
        }
    }

    Fenwick fenwick(numCities + 2);

    int numQueries; cin >> numQueries;
    for (int i = 0; i < numQueries; ++i) {
        int queryType, city; cin >> queryType >> city;
        if (queryType == 1) {
            fenwick.add(tin[city], 1);
        } else {
            long long countInSubtree = fenwick.sumRange(tin[city], tout[city]);
            long long answer = countInSubtree * (static_cast<long long>(depth[city]) + 1LL);
            cout << answer << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `N=1` 단일 노드, `Q`가 모두 질의 또는 모두 갱신인 경우
- 루트 `C`에 대한 갱신/질의(깊이 0 → 계수 1)
- 사슬 형태(편향 트리) 및 별형 트리에서의 성능
- 같은 정점에 대한 다중 갱신 중복 처리(선형 누적)
- 출력 범위: 누적 횟수×깊이(최대)로 64-bit 필요

## 제출 전 점검
- 입출력 버퍼 설정(`sync_with_stdio(false)`, `tie(nullptr)`) 확인
- 인덱스: `tin`은 1‑based, 펜윅 내부 일관성 유지
- 정수형: 합산은 `long long` 사용, 오버플로 방지

## 참고자료
- 트리 평탄화(Euler Tour) + Fenwick Tree로 서브트리 합 처리 기법
- Binary Indexed Tree 자료구조 기본 원리 및 구현


