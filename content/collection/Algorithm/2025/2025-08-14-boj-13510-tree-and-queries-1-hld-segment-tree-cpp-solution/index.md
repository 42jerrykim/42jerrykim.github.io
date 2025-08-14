---
title: "[Algorithm] cpp 백준 13510번: 트리와 쿼리 1"
description: "트리에서 간선 가중치 갱신과 경로 최댓값 질의를 처리하는 최적 풀이를 정리합니다. Heavy-Light Decomposition과 세그먼트 트리를 결합해 각 쿼리를 O(log N)에 해결하고, 구현 포인트·엣지 케이스·정당성·복잡도를 점검합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Tree
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-13510"
- "cpp"
- "C++"
- "Data Structures"
- "자료구조"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Graph"
- "그래프"
- "Tree"
- "트리"
- "Segment Tree"
- "세그먼트 트리"
- "Range Maximum Query"
- "RMQ"
- "Heavy Light Decomposition"
- "HLD"
- "Path Query"
- "경로 질의"
- "Edge Update"
- "간선 갱신"
- "Iterative Segment Tree"
- "세그트리"
- "Lowest Common Ancestor"
- "LCA"
- "Chain Decomposition"
- "체인 분할"
- "Range Query"
- "쿼리"
- "RMQ Max"
- "Max Query"
- "O(log N)"
- "Static Tree"
- "트리 분해"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13510
- 요약: 정점 1..N의 트리에서 두 가지 연산을 처리한다.
  - 1 i c: i번 간선의 비용을 c로 변경
  - 2 u v: 정점 u에서 v로 가는 단순 경로의 간선 비용 중 최댓값 출력
- 제한: N, M ≤ 100,000; 간선 비용 ≤ 1,000,000; 시간 2초, 메모리 512MB

## 입력/출력
```
입력
N
u v w  (N-1줄)
M
type ... (M줄)

출력
모든 2번 쿼리의 결과를 한 줄에 하나씩 출력
```

## 접근 개요
- 경로 최댓값 질의와 간선 가중치 갱신을 모두 빠르게 처리하려면 경로를 O(log N) 구간으로 나누고 각 구간의 최대를 질의할 수 있어야 한다.
- Heavy-Light Decomposition(HLD)으로 트리를 체인으로 분해하고, 각 정점을 선형화한 위치에 매핑한다.
- 간선 값은 "부모-자식 간선의 가중치"를 자식 정점의 위치에 저장한다. 이렇게 하면 경로(u,v)의 최댓값은 체인 단위로 분할 후 세그먼트 트리의 구간 최댓값 질의로 계산된다.
- 간선 갱신 1 i c는 i번 간선의 더 깊은 쪽 정점 위치를 찾아 해당 위치 값을 갱신한다.

```mermaid
flowchart TD
  Q([query(u,v)]) --> C{head[u] == head[v]?}
  C -- no --> A[deeper head side ascend]
  A --> S[query segmax(pos(head[u]), pos(u))]
  S --> U[u = parent[head[u]]]
  U --> Q
  C -- yes --> R[segmax(pos(v)+1, pos(u))]
  R --> Ans([answer = max over parts])
```

## 알고리즘 설계
1) 전처리(DFS)
- `parent`, `depth`, `subtreeSize`, `heavyChild`를 계산해 각 정점의 가장 무거운 자식을 구한다.

2) 분해/선형화
- 새로운 체인의 머리(head)를 만나면 그 체인을 따라가며 `positionInBase`를 부여하고, 해당 위치에 간선 가중치를 기록한다(루트는 0).
- 각 간선 i에 대해 더 깊은 정점을 `edgeToDeeperNode[i]`로 매핑한다.

3) 자료구조
- 구간 최댓값을 위한 반복(iterative) 세그먼트 트리 구축.

4) 질의(query u, v)
- 두 정점의 체인 머리가 다르면 더 깊은 쪽 체인을 올리며 [pos(head), pos(node)] 범위를 segmax로 취합.
- 같은 체인이 되면 (pos(v)+1, pos(u)) 범위를 segmax.

5) 갱신(update i, c)
- `node = edgeToDeeperNode[i]`를 찾아 `positionInBase[node]` 위치를 값 c로 점 업데이트.

## 정당성(요지)
- HLD는 임의의 경로를 O(log N)개의 체인 구간으로 분할한다. 각 구간의 최댓값을 세그먼트 트리로 구하면 전체 경로 최댓값은 이들의 최댓값이다.
- 간선 값을 자식 정점 위치에 저장했으므로, 경로의 양 끝이 같은 체인에 있을 때 루트 방향으로 한 칸을 건너뛴 `(pos(v)+1, pos(u))`가 정확히 간선 집합을 반영한다.

## 복잡도
- 전처리 O(N), 세그먼트 트리 구축 O(N)
- 각 쿼리(갱신/질의) O(log N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int numNodes;
    if (!(cin >> numNodes)) return 0;

    // Adjacency: (neighbor, edgeIndex)
    vector<vector<pair<int,int>>> adjacency(numNodes + 1);
    vector<int> edgeU(numNodes), edgeV(numNodes), edgeWeight(numNodes);

    for (int i = 1; i <= numNodes - 1; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        adjacency[u].push_back({v, i});
        adjacency[v].push_back({u, i});
        edgeU[i] = u;
        edgeV[i] = v;
        edgeWeight[i] = w;
    }

    // Parent, depth, parent edge index for node (edge to its parent)
    vector<int> parent(numNodes + 1, -1);
    vector<int> depth(numNodes + 1, 0);
    vector<int> parentEdgeIndex(numNodes + 1, 0);

    // Build parent/depth iteratively (DFS order)
    vector<int> order;
    order.reserve(numNodes);
    stack<int> dfsStack;
    parent[1] = 0;
    dfsStack.push(1);

    while (!dfsStack.empty()) {
        int current = dfsStack.top();
        dfsStack.pop();
        order.push_back(current);
        for (const auto& entry : adjacency[current]) {
            int nextNode = entry.first;
            int eIdx = entry.second;
            if (nextNode == parent[current]) continue;
            if (parent[nextNode] != -1) continue;
            parent[nextNode] = current;
            parentEdgeIndex[nextNode] = eIdx;
            depth[nextNode] = depth[current] + 1;
            dfsStack.push(nextNode);
        }
    }

    // Subtree sizes and heavy child
    vector<int> subtreeSize(numNodes + 1, 1);
    vector<int> heavyChild(numNodes + 1, -1);

    for (int i = static_cast<int>(order.size()) - 1; i >= 0; --i) {
        int node = order[i];
        int maxSubtree = 0;
        for (const auto& entry : adjacency[node]) {
            int child = entry.first;
            if (child == parent[node]) continue;
            subtreeSize[node] += subtreeSize[child];
            if (subtreeSize[child] > maxSubtree) {
                maxSubtree = subtreeSize[child];
                heavyChild[node] = child;
            }
        }
    }

    // Map edge index -> deeper endpoint node
    vector<int> edgeToDeeperNode(numNodes, 0);
    for (int node = 2; node <= numNodes; ++node) {
        edgeToDeeperNode[parentEdgeIndex[node]] = node;
    }

    // Heavy-Light Decomposition: head of chain, position in base array
    vector<int> head(numNodes + 1, 0);
    vector<int> positionInBase(numNodes + 1, 0);
    vector<int> baseValue(numNodes + 1, 0);
    int currentPosition = 1;

    for (int node = 1; node <= numNodes; ++node) {
        if (parent[node] == 0 || heavyChild[parent[node]] != node) {
            // node starts a new chain
            for (int v = node; v != -1; v = heavyChild[v]) {
                head[v] = node;
                positionInBase[v] = currentPosition;
                baseValue[currentPosition] = (parent[v] == 0 ? 0 : edgeWeight[parentEdgeIndex[v]]);
                ++currentPosition;
            }
        }
    }

    // Iterative segment tree for range max
    const int baseSize = numNodes;
    int leafOffset = 1;
    while (leafOffset < baseSize) leafOffset <<= 1;
    vector<int> segTree(leafOffset * 2, 0);

    for (int i = 1; i <= baseSize; ++i) {
        segTree[leafOffset + i - 1] = baseValue[i];
    }
    for (int i = leafOffset - 1; i >= 1; --i) {
        segTree[i] = max(segTree[i << 1], segTree[i << 1 | 1]);
    }

    auto segQuery = [&](int left, int right) -> int {
        if (left > right) return 0;
        int res = 0;
        int l = left + leafOffset - 1;
        int r = right + leafOffset - 1;
        while (l <= r) {
            if (l & 1) res = max(res, segTree[l++]);
            if (!(r & 1)) res = max(res, segTree[r--]);
            l >>= 1; r >>= 1;
        }
        return res;
    };

    auto segUpdate = [&](int pos, int value) {
        int idx = pos + leafOffset - 1;
        segTree[idx] = value;
        idx >>= 1;
        while (idx >= 1) {
            segTree[idx] = max(segTree[idx << 1], segTree[idx << 1 | 1]);
            idx >>= 1;
        }
    };

    auto queryMaxOnPath = [&](int u, int v) -> int {
        int result = 0;
        while (head[u] != head[v]) {
            if (depth[head[u]] < depth[head[v]]) swap(u, v);
            int topPos = positionInBase[head[u]];
            int uPos = positionInBase[u];
            result = max(result, segQuery(topPos, uPos));
            u = parent[head[u]];
        }
        if (u == v) return result;
        if (depth[u] < depth[v]) swap(u, v);
        result = max(result, segQuery(positionInBase[v] + 1, positionInBase[u]));
        return result;
    };

    int numQueries;
    cin >> numQueries;
    for (int qi = 0; qi < numQueries; ++qi) {
        int type;
        cin >> type;
        if (type == 1) {
            int edgeIndex, newCost;
            cin >> edgeIndex >> newCost;
            int node = edgeToDeeperNode[edgeIndex];
            segUpdate(positionInBase[node], newCost);
            edgeWeight[edgeIndex] = newCost;
        } else if (type == 2) {
            int u, v;
            cin >> u >> v;
            cout << queryMaxOnPath(u, v) << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- u = v인 질의: 경로에 간선이 없어 0을 출력해야 함(위 구현은 자동 처리).
- 루트 체인 구간: 루트의 base 값은 0이므로 최댓값 계산에 영향 없음.
- 단일 체인 내부 질의: 구간을 (pos(v)+1, pos(u))로 정확히 설정.
- 간선 갱신 시 더 깊은 정점 식별 실수 방지: `edgeToDeeperNode[i]` 사용.
- N=2 최소 트리, 비용이 동일/최대치(1,000,000)인 경우.

## 제출 전 점검
- 세그먼트 트리 인덱스 보정(leafOffset-1)과 경계 포함/제외 확인.
- 깊이 비교 시 swap(u,v) 처리 누락 여부.
- 입출력 버퍼링과 개행 문자 처리(`'\n'`).
- 64-bit가 필요하지 않으므로 `int`로 충분하지만, 환경에 따라 `long long` 고려 가능.

## 참고자료
- HLD(Heavy-Light Decomposition) 관련 개념 정리 문서/블로그
- 세그먼트 트리(구간 최댓값) 표준 구현 예제


