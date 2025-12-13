---
title: "[Algorithm] C++ 백준 5820번: 경주 - 길이 K 최소 간선 경로"
description: "트리에서 길이 K인 경로 중 사용 간선 수가 최소인 것을 찾는다. 센트로이드 분해로 각 서브트리 거리 목록을 수집해 보완 거리(K−d)와 즉시 매칭하고, 터치된 거리만 관리해 O(N log N) 내 해결한다. 가중치 합 가지치기와 64비트 누적으로 안전성을 확보한다."
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
- Problem-5820
- cpp
- C++
- Tree
- 트리
- Weighted Tree
- 가중치 트리
- Path
- 경로
- Simple Path
- 단순 경로
- Exact Path Length
- 정확한 경로 길이
- K
- K 길이
- Centroid Decomposition
- 센트로이드 분해
- Decomposition
- 분할 정복
- Divide and Conquer on Tree
- 트리 분할정복
- Distance
- 거리
- Distance Pairing
- 거리 매칭
- Complement
- 보완 거리
- Bucket
- 버킷
- Minimal Edges
- 최소 간선 수
- Edge Count
- 간선 수
- Optimization
- 최적화
- DFS
- 깊이우선탐색
- Recursion
- 재귀
- Pruning
- 가지치기
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Fast IO
- 입출력 최적화
- 64-bit Integer
- 64비트 정수
- Long Long
- 자료구조
- Data Structures
- Touched Distances
- 업데이트 최적화
- Memory Optimization
- 메모리 최적화
- IOI
- IOI 2011
- Race
- 경주
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/5820
- 요약: `N`개의 도시와 `N-1`개의 양방향 고속도로(트리)에서 길이 합이 정확히 `K`인 단순 경로 중 사용 간선 수가 최소인 것을 찾는다. 없으면 `-1`을 출력한다.

### 제한/스펙
- `1 ≤ N ≤ 200000`, `1 ≤ K ≤ 1000000`
- 간선 가중치 `0 ≤ w ≤ 1e6` (정수), 트리 구조(임의 두 점 사이 경로 유일)
- 시간 제한 3초 → `O(N log N)` 수준 설계 필요

## 입출력 형식/예제

예제 입력 1
```
4 3
0 1 1
1 2 2
1 3 4
```

예제 출력 1
```
2
```

## 접근 개요(아이디어 스케치)
- 핵심 관찰: 경로 길이 합이 정확히 `K`가 되도록 두 구간 거리 `d`와 `K−d`를 합쳐 만들면 된다. 트리에서 이를 전역적으로 빠르게 찾으려면 한 분할 중심에서 모든 자식 서브트리의 거리 목록을 수집해 "보완 거리"를 즉시 매칭하면 된다.
- 전략: 센트로이드 분해. 센트로이드를 기준으로 각 자식 서브트리의 (거리, 사용 간선 수) 목록을 DFS로 수집하고, 이전까지 처리한 서브트리들의 거리 버킷 `bestDist[dist]`(해당 거리를 만드는 최소 간선 수)에 대해 `need = K - d`를 O(1)로 조회하여 후보 답을 갱신한다. 그 후 현재 서브트리의 거리 정보를 `bestDist`에 병합한다.
- 최적화: `bestDist`는 길이 `K+1` 배열이지만, 실제로 갱신된 인덱스만 `touched`에 기록했다가 한 센트로이드 처리가 끝나면 해당 인덱스만 초기화하여 `O(방문 수)`로 관리한다.

```mermaid
flowchart TD
  C[센트로이드 선택] --> S1[각 자식 서브트리 DFS로 (거리 d, 간선 e) 수집]
  S1 --> Q[need = K - d 조회로 즉시 매칭]
  Q --> U[bestDist[need] + e 로 최소 간선 갱신]
  U --> M[현재 서브트리의 (d,e) 들을 bestDist 에 병합]
  M --> N[다음 자식 처리]
  N -->|모두 처리| R[터치된 거리만 초기화]
  R --> D[차단 후 남은 컴포넌트 재귀 분해]
```

## 알고리즘 설계
- 상태
  - `bestDist[0..K]`: 해당 거리 달성에 필요한 최소 간선 수(미설정은 `INF`).
  - `touched`: 현 센트로이드 처리 중 갱신한 거리 인덱스 목록.
- 절차(센트로이드 `c` 기준)
  1) `bestDist[0] = 0`으로 시작(경로가 `c`에서 끊기는 경우).
  2) 각 자식 서브트리에서 DFS로 `(dist, edges)`를 수집(누적 거리가 `K`를 넘으면 가지치기).
  3) 수집된 각 `(d,e)`에 대해 `need = K - d`; `bestDist[need]`가 유효하면 `ans = min(ans, bestDist[need] + e)`.
  4) 그 후 현재 서브트리의 `(d,e)`를 `bestDist[d] = min(bestDist[d], e)`로 병합. 이때 처음 갱신하는 `d`는 `touched`에 기록.
  5) 모든 자식 처리 후 `touched`에 한해 `bestDist`를 `INF`로 복원.
  6) 센트로이드를 차단하고 각 남은 컴포넌트에 대해 재귀.
- 올바름 근거
  - 모든 경로는 어떤 센트로이드 `c`를 반드시 지난다. 그 경로는 `c` 기준으로 서로 다른 두 서브트리 경로(또는 하나의 서브트리와 빈 경로)로 분해되며, 길이 합이 `K`가 되는 두 거리 `d`와 `K−d`의 조합으로 표현된다. 각 서브트리를 순차 처리하며 기존 `bestDist`와의 매칭은 서로 다른 서브트리 쌍만 결합하게 되어 중복/자기결합이 없다.
  - 각 거리에서 최소 간선 수만 유지하므로 최종적으로 최소 간선 수가 도출된다.

## 복잡도
- 시간: 각 간선이 `O(log N)` 레벨의 센트로이드에서 한 번씩 수집/매칭되므로 총 `O(N log N)`.
- 공간: 그래프 `O(N)`, `bestDist` `O(K)`(최대 약 1e6+1), `touched`는 방문 수 만큼.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int INF = 1e9;

int N, K;
vector<vector<pair<int,int>>> graphEdges;
vector<int> subtreeSize;
vector<char> isBlocked;

vector<int> bestDist;         // bestDist[distance] = minimal edges to achieve this distance (from previous children)
vector<int> touchedDistances; // indices in bestDist that we set during current centroid processing

int answerMinEdges = INF;

int computeSubtreeSize(int node, int parent) {
    subtreeSize[node] = 1;
    for (const auto &edge : graphEdges[node]) {
        int next = edge.first;
        if (next == parent || isBlocked[next]) continue;
        subtreeSize[node] += computeSubtreeSize(next, node);
    }
    return subtreeSize[node];
}

int findCentroid(int node, int parent, int totalSize) {
    for (const auto &edge : graphEdges[node]) {
        int next = edge.first;
        if (next == parent || isBlocked[next]) continue;
        if (subtreeSize[next] * 2 > totalSize) {
            return findCentroid(next, node, totalSize);
        }
    }
    return node;
}

void collectDistances(int node, int parent, int dist, int edgesUsed, vector<pair<int,int>> &buffer) {
    if (dist > K) return;
    buffer.emplace_back(dist, edgesUsed);
    for (const auto &edge : graphEdges[node]) {
        int next = edge.first, w = edge.second;
        if (next == parent || isBlocked[next]) continue;
        int nd = dist + w;
        if (nd > K) continue; // prune
        collectDistances(next, node, nd, edgesUsed + 1, buffer);
    }
}

void decompose(int entry) {
    int total = computeSubtreeSize(entry, -1);
    int centroid = findCentroid(entry, -1, total);
    isBlocked[centroid] = 1;

    // Initialize bestDist for this centroid (distance 0 with 0 edges at the centroid itself)
    if (bestDist[0] == INF) touchedDistances.push_back(0);
    bestDist[0] = 0;

    // Process each child subtree: query against bestDist (paths via centroid), then insert this subtree's distances
    for (const auto &edge : graphEdges[centroid]) {
        int child = edge.first, w = edge.second;
        if (isBlocked[child]) continue;

        vector<pair<int,int>> collected;
        if (w <= K) collectDistances(child, centroid, w, 1, collected);

        for (const auto &p : collected) {
            int d = p.first, e = p.second;
            int need = K - d;
            if (need < 0) continue;
            if (bestDist[need] != INF) {
                answerMinEdges = min(answerMinEdges, bestDist[need] + e);
            }
        }
        for (const auto &p : collected) {
            int d = p.first, e = p.second;
            if (bestDist[d] == INF) touchedDistances.push_back(d);
            if (bestDist[d] > e) bestDist[d] = e;
        }
    }

    // Clear bestDist updates for this centroid
    for (int d : touchedDistances) bestDist[d] = INF;
    touchedDistances.clear();

    // Recurse on remaining components
    for (const auto &edge : graphEdges[centroid]) {
        int child = edge.first;
        if (!isBlocked[child]) decompose(child);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> N >> K)) return 0;
    graphEdges.assign(N, {});
    for (int i = 0; i < N - 1; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        graphEdges[a].push_back({b, w});
        graphEdges[b].push_back({a, w});
    }

    subtreeSize.assign(N, 0);
    isBlocked.assign(N, 0);
    bestDist.assign(K + 1, INF);
    touchedDistances.reserve(1 << 16);

    decompose(0);

    cout << (answerMinEdges == INF ? -1 : answerMinEdges) << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `K`가 매우 큰 경우: `bestDist`는 터치된 인덱스만 복원(전범위 초기화 금지).
- 간선 가중치가 `0`일 수 있음: 동일 거리에서 최소 간선 수 유지가 중요.
- 긴 사슬 트리: 재귀 깊이 증가 가능 → 빌드 환경에 따라 스택 여유 필요.
- 경로가 없는 경우: 끝까지 `INF` 유지되어 `-1` 출력.

## 제출 전 점검
- `need = K - d` 계산 시 음수/범위 체크.
- `collectDistances` 가지치기(`dist > K`) 정확성.
- 센트로이드별 `bestDist` 초기화가 `touched` 기반으로만 수행되는지 확인.
- 빠른 입출력 설정 및 64비트 누적은 필요 시 적용.

## 참고자료/유사문제
- IOI 2011 Race (Centroid Decomposition 고전 문제)
- 트리 경로 길이 합/정확 길이 경로 계수 문제군의 전형 해법


