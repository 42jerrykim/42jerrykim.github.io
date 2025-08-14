---
title: "[Algorithm] cpp-python 백준 3683번: 고양이와 개 - 투표 최대 만족"
description: "고양이 선호(C×D)·개 선호(D×C) 투표를 분리해 충돌 간선으로 이분 그래프를 만들고, 최대 매칭으로 최소 제거 수를 구합니다. 코니그 정리로 정당성을 보이고 Hopcroft–Karp로 O(E√V) 내에 해결합니다. 구현·엣지 케이스까지 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-3683
- cpp
- python
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
- Graph
- 그래프
- Bipartite Matching
- 이분매칭
- Hopcroft-Karp
- Conflict Graph
- Cat vs Dog
- NWERC
- NWERC 2008
- Minimum Vertex Cover
- 최소 정점 커버
- Kőnig's Theorem
- 코니그 정리
- Maximum Independent Set
- 최대 독립 집합
- Matching
- 매칭
- Flow
- 최대유량
- String
- 문자열
- Math
- 수학
- Debugging
- 디버깅
- Implementation Details
- 구현 디테일
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 3683 고양이와 개](https://www.acmicpc.net/problem/3683)
- 요약: 각 시청자는 좋아하는 동물은 다음 라운드로 올리고 싫어하는 동물은 탈락시키라고 투표합니다. 투표가 "그대로 반영되는" 시청자 수를 최대로 하되, 서로 충돌하는 투표는 함께 만족시킬 수 없습니다.
- 제약: c, d ≤ 100, v ≤ 500, 테스트 케이스 최대 100

## 입력/출력 예시
```
입력
2
1 1 2
C1 D1
D1 C1
1 2 4
C1 D1
C1 D1
C1 D2
D2 C1

출력
1
3
```

## 접근 개요
- 핵심은 "서로 동시에 만족시킬 수 없는 투표 쌍"을 찾아 최소한만 제거하는 것입니다.
- 투표를 두 부류로 나눕니다.
  - CxD: 고양이를 올리고(keep) 개를 떨어뜨리는(remove) 투표
  - DxC: 개를 올리고(keep) 고양이를 떨어뜨리는(remove) 투표
- 이분 그래프를 구성해 한쪽을 CxD, 반대쪽을 DxC로 두고, 다음 두 경우에 간선을 잇습니다.
  - 같은 고양이에 대해 CxD는 keep, DxC는 remove를 요구
  - 같은 개에 대해 CxD는 remove, DxC는 keep을 요구
- 이렇게 만든 "충돌 그래프"에서 간선을 모두 없애려면 최소 몇 개의 정점을 지워야 하는가? → 이분 그래프의 최소 정점 커버 크기와 동일하며, 코니그 정리에 의해 최대 매칭 크기와 같습니다. 따라서, 최대 만족 수 = v − (최대 매칭).

## Mermaid로 보는 흐름
```mermaid
flowchart TD
    A[투표 입력 v개] --> B[분할: CxD / DxC]
    B --> C[충돌 조건으로 이분 그래프 간선 생성]
    C --> D[Hopcroft–Karp로 최대 매칭]
    D --> E[정답 = v - |매칭|]
```

## 알고리즘 설계
- 정점: CxD 투표 노드 L개, DxC 투표 노드 R개
- 간선: (i ∈ L, j ∈ R)이 충돌하면 간선 추가
- 계산: Hopcroft–Karp로 최대 매칭 M 계산
- 결과: v − |M|

### 정당성 요약
- 충돌 간선이 하나라도 남아 있으면 해당 두 투표는 동시에 만족 불가 → 간선을 없애려면 양끝 중 최소 하나는 제거해야 함 → 최소 제거 수는 최소 정점 커버 크기
- 이분 그래프에서 최소 정점 커버 = 최대 매칭(코니그 정리) → 최소 제거 = |M| → 최대 유지(=만족) = v − |M|

## 복잡도
- 정점 수 V ≤ v ≤ 500, 간선 수 E ≤ |CxD|×|DxC| ≤ 250×250 수준(최악)
- Hopcroft–Karp: O(E√V) → 본 문제 제약에서 충분히 여유

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Vote {
    bool keepCat; // true if keep cat, false if keep dog
    int catIndex; // cat index involved (keep if keepCat, remove if !keepCat)
    int dogIndex; // dog index involved (remove if keepCat, keep if !keepCat)
};

struct HopcroftKarp {
    int leftSize, rightSize;
    vector<vector<int>> adj;     // adj[u] = list of v on right
    vector<int> dist;            // distance for BFS layering (left side)
    vector<int> pairU, pairV;    // matches: left->right, right->left

    HopcroftKarp(int L, int R) : leftSize(L), rightSize(R) {
        adj.assign(L, {});
        pairU.assign(L, -1);
        pairV.assign(R, -1);
        dist.resize(L);
    }

    void addEdge(int u, int v) { // u in [0,L), v in [0,R)
        adj[u].push_back(v);
    }

    bool bfs() {
        queue<int> q;
        const int INF = 1e9;
        bool foundFreeOnRight = false;

        for (int u = 0; u < leftSize; ++u) {
            if (pairU[u] == -1) {
                dist[u] = 0;
                q.push(u);
            } else {
                dist[u] = INF;
            }
        }

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                int u2 = pairV[v];
                if (u2 == -1) {
                    foundFreeOnRight = true;
                } else if (dist[u2] == INF) {
                    dist[u2] = dist[u] + 1;
                    q.push(u2);
                }
            }
        }
        return foundFreeOnRight;
    }

    bool dfs(int u) {
        for (int v : adj[u]) {
            int u2 = pairV[v];
            if (u2 == -1 || (dist[u2] == dist[u] + 1 && dfs(u2))) {
                pairU[u] = v;
                pairV[v] = u;
                return true;
            }
        }
        dist[u] = INT_MAX;
        return false;
    }

    int maxMatching() {
        int matching = 0;
        while (bfs()) {
            for (int u = 0; u < leftSize; ++u) {
                if (pairU[u] == -1 && dfs(u)) {
                    ++matching;
                }
            }
        }
        return matching;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int c, d, v;
        cin >> c >> d >> v;

        vector<Vote> catLovers;  // CxD
        vector<Vote> dogLovers;  // DxC
        catLovers.reserve(v);
        dogLovers.reserve(v);

        for (int i = 0; i < v; ++i) {
            string s1, s2;
            cin >> s1 >> s2; // e.g., "C1" "D2"
            char k1 = s1[0], k2 = s2[0];
            int n1 = stoi(s1.substr(1));
            int n2 = stoi(s2.substr(1));

            if (k1 == 'C' && k2 == 'D') {
                // keep cat n1, remove dog n2
                catLovers.push_back({true, n1, n2});
            } else {
                // k1 == 'D' && k2 == 'C'
                // keep dog n1, remove cat n2
                dogLovers.push_back({false, n2, n1});
            }
        }

        int L = (int)catLovers.size();
        int R = (int)dogLovers.size();

        HopcroftKarp hk(L, R);

        // Conflict edges
        for (int i = 0; i < L; ++i) {
            for (int j = 0; j < R; ++j) {
                if (catLovers[i].catIndex == dogLovers[j].catIndex ||
                    catLovers[i].dogIndex == dogLovers[j].dogIndex) {
                    hk.addEdge(i, j);
                }
            }
        }

        int maxMatch = hk.maxMatching();
        cout << (v - maxMatch) << '\n';
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

input = sys.stdin.readline

def hopcroft_karp(adj, L, R):
    INF = 10**9
    pair_u = [-1] * L
    pair_v = [-1] * R
    dist = [INF] * L

    def bfs():
        q = deque()
        found = False
        for u in range(L):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        while q:
            u = q.popleft()
            for v in adj[u]:
                u2 = pair_v[v]
                if u2 == -1:
                    found = True
                elif dist[u2] == INF:
                    dist[u2] = dist[u] + 1
                    q.append(u2)
        return found

    def dfs(u):
        for v in adj[u]:
            u2 = pair_v[v]
            if u2 == -1 or (dist[u2] == dist[u] + 1 and dfs(u2)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = 10**18
        return False

    matching = 0
    while bfs():
        for u in range(L):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    return matching

def solve():
    t = int(input().strip())
    for _ in range(t):
        c, d, v = map(int, input().split())
        cat_lovers = []  # (cat_index, dog_index)
        dog_lovers = []  # (cat_index, dog_index) for opposing type
        for _ in range(v):
            s1, s2 = input().split()
            k1, k2 = s1[0], s2[0]
            n1, n2 = int(s1[1:]), int(s2[1:])
            if k1 == 'C' and k2 == 'D':
                cat_lovers.append((n1, n2))
            else:  # 'D' and 'C'
                dog_lovers.append((n2, n1))

        L = len(cat_lovers)
        R = len(dog_lovers)
        adj = [[] for _ in range(L)]

        for i in range(L):
            ci, di = cat_lovers[i]
            for j in range(R):
                cj, dj = dog_lovers[j]
                if ci == cj or di == dj:
                    adj[i].append(j)

        m = hopcroft_karp(adj, L, R)
        print(v - m)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- v = 0인 경우(정답 0)
- CxD만 있거나 DxC만 있는 경우(간선 0 → 정답 v)
- 동일한 투표가 여러 번 들어오는 경우(중복 노드가 생기며 그 자체로는 충돌 아님)
- 모든 투표가 상호 충돌하는 극단 케이스(매칭이 커짐 → 정답 작아짐)
- 숫자 파싱(C10, D100 등)과 입력 공백 처리

## 제출 전 점검
- 출력 개행 누락 여부
- 64-bit 정수 불필요(문제 범위 내 int로 충분)
- 인덱스 범위, 초기화 누락, 그래프 간선 조건 실수 여부

## 참고자료
- NWERC 2008 Problem C "Cat vs. Dog" (원문)
- 이분 그래프 최대 매칭, 코니그 정리 기본 이론


