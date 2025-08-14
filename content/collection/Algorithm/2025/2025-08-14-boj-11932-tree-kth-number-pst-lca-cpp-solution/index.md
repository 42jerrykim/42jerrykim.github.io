---
title: "[Algorithm] cpp 백준 11932번: 트리와 K번째 수 - PST+LCA"
description: "정점 값 좌표압축 뒤 루트→정점 경로마다 영속 세그먼트 트리를 누적 구축하고, LCA를 이용해 경로 빈도를 포함-배제로 합산해 K번째 수를 찾습니다. 세그먼트 트리에서 왼/오 자식으로 이진 하향 탐색해 순위 k를 복원하며, 전체 시간/공간은 O((N+M)logN)/O(NlogN) 수준입니다."
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
- Problem-11932
- cpp
- C++
- Tree
- 트리
- Path Query
- 경로 쿼리
- K-th
- K번째
- Order Statistics
- 순위통계
- Persistent Segment Tree
- 영속 세그먼트 트리
- PST
- Segment Tree
- 세그먼트 트리
- Lowest Common Ancestor
- 최소 공통 조상
- LCA
- Binary Lifting
- 이진 점프
- Binary Lifting LCA
- Inclusion-Exclusion
- 포함-배제
- Coordinate Compression
- 좌표압축
- Value Compression
- 값 압축
- Online Query
- 온라인 쿼리
- Query
- 쿼리
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
- Fast IO
- 빠른 입출력
- DFS
- BFS
- Rooted Tree
- 루트 트리
- K-th on Path
- 경로 K번째
- Data Structures
- 자료구조
- Competitive Programming
- 경쟁프로그래밍
- Testing
- 테스트
- Debugging
- 디버깅
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11932
- 요약: 정점 가중치가 모두 서로 다른 트리에서, 두 정점 `X, Y`를 잇는 경로 상의 정점 가중치 중 K번째로 작은 값을 여러 질의에 대해 구합니다. \(N, M \le 10^5\).

## 입력/출력
```
입력
N M
w1 w2 ... wN                  # 정점 1..N의 가중치(모두 상이, int 범위)
N-1개의 줄: u v               # 무방향 간선
M개의 줄: X Y K               # 질의

출력
각 질의에 대해 K번째로 작은 값을 한 줄에 하나씩 출력
```

## 접근 개요
- 핵심 아이디어: 경로의 값 분포를 빠르게 셀 수 있도록, 루트에서 각 정점까지의 값 빈도를 담은 "영속 세그먼트 트리(Persistent Segment Tree)" 버전을 만듭니다.
- 경로 `X–Y`의 값 빈도는 포함-배제 `ver[X] + ver[Y] - ver[LCA] - ver[parent(LCA)]`로 계산됩니다.
- 세그먼트 트리에서 왼쪽 자식(작은 값 구간)의 개수를 기준으로 이진 하향 탐색하며 K번째 값을 복원합니다.

```mermaid
flowchart LR
  A[좌표압축: 값 → 1..U] --> B[각 정점 v의 버전 ver[v] = ver[parent(v)]에서 값rank(w[v]) 1 증가]
  B --> C[LCA(X,Y) 계산 (Binary Lifting)]
  C --> D[경로 빈도 = ver[X]+ver[Y]-ver[L]-ver[parent(L)]]
  D --> E[세그먼트 트리에서 왼/오로 내려가며 k번째 복원]
```

## 알고리즘 설계
- 전처리
  - 값 좌표압축: 모든 가중치를 정렬해 순위를 부여하고, 트리의 각 정점 값은 해당 순위에 1을 더하도록 합니다.
  - 루트 선택 후 BFS/DFS로 `parent`, `depth` 설정과 동시에 `ver[v]`를 생성: `ver[v] = update(ver[parent[v]], rank(value[v]))`.
  - 이 때, 세그먼트 트리는 노드마다 `left, right, sum`을 갖고, `update` 시 새 노드만 생성하여 영속 버전을 유지합니다.
- LCA
  - Binary Lifting 표를 구성해 \(O(\log N)\)에 LCA를 구합니다.
- 질의 처리
  - `L = LCA(X,Y)`, `P = parent(L)`라 할 때, 왼자식에 존재하는 개수 `cntLeft = sum(left(VerX)) + sum(left(VerY)) - sum(left(VerL)) - sum(left(VerP))`를 구합니다.
  - `k ≤ cntLeft`면 왼쪽으로, 아니면 `k -= cntLeft` 후 오른쪽으로 이동하며 구간 경계를 좁혀 최종 리프(rank)를 얻습니다.

## 복잡도
- 시간: 전처리 \(O(N\log N)\), 각 질의 \(O(\log N)\); 전체 \(O((N+M)\log N)\)
- 공간: PST 노드 수 \(\approx N\log N\); Binary Lifting 테이블 \(O(N\log N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 100000 + 5;
static const int MAXLOG = 17;                // 2^17 = 131072 >= 100000
static const int MAXNODE = 4000000;          // ~ N * (logN + margin)

// Persistent segment tree storage
int segLeft[MAXNODE], segRight[MAXNODE], segSum[MAXNODE], segNodeCnt = 0;

// Tree/LCA storage
int n, m;
vector<int> graphAdj[MAXN];
int parentUp[MAXLOG + 1][MAXN];
int depthArr[MAXN];
int rootVer[MAXN];

// Values and compression
int nodeValue[MAXN];
vector<int> sortedVals; // for decompress

int updateVersion(int prevRoot, int left, int right, int pos) {
    int curr = ++segNodeCnt;
    segLeft[curr] = segLeft[prevRoot];
    segRight[curr] = segRight[prevRoot];
    segSum[curr] = segSum[prevRoot] + 1;
    if (left != right) {
        int mid = (left + right) >> 1;
        if (pos <= mid) {
            segLeft[curr] = updateVersion(segLeft[prevRoot], left, mid, pos);
        } else {
            segRight[curr] = updateVersion(segRight[prevRoot], mid + 1, right, pos);
        }
    }
    return curr;
}

int kthQuery(int ru, int rv, int rl, int rpl, int left, int right, int k) {
    if (left == right) return left;
    int mid = (left + right) >> 1;

    int leftCount =
        segSum[segLeft[ru]] +
        segSum[segLeft[rv]] -
        segSum[segLeft[rl]] -
        segSum[segLeft[rpl]];

    if (k <= leftCount) {
        return kthQuery(segLeft[ru], segLeft[rv], segLeft[rl], segLeft[rpl], left, mid, k);
    } else {
        return kthQuery(segRight[ru], segRight[rv], segRight[rl], segRight[rpl], mid + 1, right, k - leftCount);
    }
}

void buildParents() {
    for (int k = 1; k <= MAXLOG; ++k) {
        for (int v = 1; v <= n; ++v) {
            int mid = parentUp[k - 1][v];
            parentUp[k][v] = mid ? parentUp[k - 1][mid] : 0;
        }
    }
}

int lca(int a, int b) {
    if (depthArr[a] < depthArr[b]) swap(a, b);
    int diff = depthArr[a] - depthArr[b];

    for (int k = MAXLOG; k >= 0; --k) {
        if (diff & (1 << k)) a = parentUp[k][a];
    }
    if (a == b) return a;

    for (int k = MAXLOG; k >= 0; --k) {
        if (parentUp[k][a] != parentUp[k][b]) {
            a = parentUp[k][a];
            b = parentUp[k][b];
        }
    }
    return parentUp[0][a];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; ++i) {
        cin >> nodeValue[i];
        sortedVals.push_back(nodeValue[i]);
    }

    for (int i = 0; i < n - 1; ++i) {
        int x, y; cin >> x >> y;
        graphAdj[x].push_back(y);
        graphAdj[y].push_back(x);
    }

    // Coordinate compression
    sort(sortedVals.begin(), sortedVals.end());
    sortedVals.erase(unique(sortedVals.begin(), sortedVals.end()), sortedVals.end());
    auto getRank = [&](int v) -> int {
        return int(lower_bound(sortedVals.begin(), sortedVals.end(), v) - sortedVals.begin()) + 1;
    };
    int maxRank = (int)sortedVals.size();

    // BFS to set parent, depth, and build persistent versions
    queue<int> q;
    parentUp[0][1] = 0;
    depthArr[1] = 0;
    rootVer[0] = 0; // empty version
    q.push(1);

    vector<int> visited(n + 1, 0);
    visited[1] = 1;

    while (!q.empty()) {
        int u = q.front(); q.pop();
        rootVer[u] = updateVersion(rootVer[parentUp[0][u]], 1, maxRank, getRank(nodeValue[u]));
        for (int v : graphAdj[u]) {
            if (!visited[v]) {
                visited[v] = 1;
                parentUp[0][v] = u;
                depthArr[v] = depthArr[u] + 1;
                q.push(v);
            }
        }
    }

    // Build binary lifting table
    buildParents();

    // Handle queries
    while (m--) {
        int x, y, k; cin >> x >> y >> k;
        int L = lca(x, y);
        int pL = parentUp[0][L]; // could be 0 for root
        int rankAns = kthQuery(rootVer[x], rootVer[y], rootVer[L], rootVer[pL], 1, maxRank, k);
        int valueAns = sortedVals[rankAns - 1];
        cout << valueAns << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `X = Y`인 단일 정점 경로, `K = 1`과 경로 길이와 같은 극단 값
- 트리 루트가 LCA인 경우: `parent(LCA) = 0` 처리(빈 버전)
- 값 범위 큰 경우 좌표압축 누락/오류, 정렬 후 중복 제거 확인
- PST 노드 수 한계(메모리): 상수 배수 충분히 크게 확보

## 제출 전 점검
- 빠른 입출력 세팅(`sync_with_stdio(false)`, `tie(nullptr)`) 적용
- Binary Lifting 테이블 초기화/루트 부모 0 처리
- 포함-배제 순서 `ver[X]+ver[Y]-ver[L]-ver[parent(L)]` 검증
- 좌표압축 인덱스의 1-기반 구간 경계와 `mid` 계산 일관성

## 참고자료/유사문제
- 트리 경로 K번째 수(Persistent Segment Tree + LCA) 전형 문제
- LCA(Binary Lifting), 좌표압축, 세그먼트 트리의 영속화 기법


