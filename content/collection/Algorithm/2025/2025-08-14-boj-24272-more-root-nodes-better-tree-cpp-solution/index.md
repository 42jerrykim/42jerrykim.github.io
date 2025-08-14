---
title: "[Algorithm] cpp 백준 24272번: 루트 노드가 많은 트리일수록 좋은 트리이다"
description: "유일 경로 트리의 간선 방향을 제어하며 ‘모든 정점에 도달 가능한 루트’의 수를 유지하는 문제입니다. Euler tour로 서브트리를 구간화하고, child→parent 제약의 교집합과 parent→child 제약의 합집합을 각각 multiset과 세그먼트 트리로 관리하여 매 쿼리 O(log N)에 정답을 계산합니다. 엣지 케이스(교집합 공집합, 전역 인터벌, 무방향 전환)까지 안정적으로 처리합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
- Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-24272
- cpp
- C++
- Graph
- 그래프
- Tree
- 트리
- Orientation
- 방향 그래프
- Root
- 루트
- Reachability
- 도달성
- Euler Tour
- 오일러 순회
- Subtree Interval
- 서브트리 구간
- Segment Tree
- 세그먼트 트리
- Range Cover
- 구간 피복
- Multiset
- 멀티셋
- Set Intersection
- 교집합
- Set Union
- 합집합
- Interval Query
- 인터벌 쿼리
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
- Graph Theory
- 그래프 이론
- Tree DP
- 트리 DP
- DFS
- 깊이우선탐색
- LCA
- 최소공통조상
- Binary Lifting
- 이진 도약
- Range Update
- 구간 갱신
- Range Query
- 구간 질의
- Offline Query
- 오프라인 쿼리
- Online Query
- 온라인 쿼리
- Contest
- 대회 문제
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/24272
- 요약: 방향/무방향 간선이 혼재된 트리(방향 제거 시 트리)에서, 간선의 방향을 쿼리로 바꿔가며 “모든 정점으로의 경로가 존재하는 정점(루트)”의 개수를 매번 출력합니다. 쿼리는 간선을 u→v, u←v, 무방향으로 설정하는 세 가지입니다.

## 입력/출력
```
<입력 예시>
5
1 -- 2
2 -> 3
2 <- 4
3 -- 5
5
2 -- 4
2 -> 4
5 -> 3
2 -- 3
3 -- 5
```
```
<출력 예시>
3
2
0
1
4
```

## 접근 개요
- 트리는 유일 경로 구조이므로 각 간선은 한 쪽을 “시작 가능 집합”에서 제거하는 제약으로 해석할 수 있습니다.
- child→parent(자식에서 부모 방향) 간선은 “루트가 반드시 해당 간선의 자식 서브트리 내부에 있어야 함”을 의미합니다. 여러 개면 서브트리들의 교집합 I로 압축됩니다.
- parent→child(부모에서 자식 방향) 간선은 “루트가 해당 간식 서브트리 내부에 있으면 안 됨”을 의미합니다. 여러 개면 서브트리들의 합집합 U로 압축됩니다.
- 정답은 |I − U| = |I| − |I ∩ U| 입니다. 여기서 I는 교집합(하나의 연속 구간), U는 합집합(여러 구간의 합)입니다.
- Euler tour로 각 노드를 구간 [tin, tout]으로 매핑하면 서브트리 연산이 구간 연산으로 바뀝니다.

### 시각화(개념 다이어그램)
```mermaid
flowchart LR
  A[모든 정점 1..N] --> B[child→parent 제약 교집합 I]
  A --> C[parent→child 제약 합집합 U]
  B --> D[정답 = |I| - |I ∩ U|]
  C --> D
```

## 알고리즘
- 전처리: 임의 루트(1)에서 DFS로 Euler tour를 수행하여 각 정점의 [tin, tout]을 구합니다.
- 집합 I(교집합): child→parent 간선의 서브트리 [tin, tout]들에 대해 L = max(tin), R = min(tout)을 유지합니다. multiset 두 개로 최대 L, 최소 R을 O(log N)에 갱신합니다.
- 집합 U(합집합): parent→child 간선의 서브트리 구간들을 커버 카운트 세그먼트 트리로 관리하여, 임의 구간의 피복 길이를 O(log N)에 구합니다.
- 매 쿼리 처리:
  1) 해당 간선의 깊이에 따라 child 노드를 정하고, 설정 방향에 따라 U 또는 I에 추가/삭제합니다.
  2) I가 공집합(L > R)이면 정답 0.
  3) 아니면 |I| = R − L + 1, |I ∩ U| = seg.query(L, R). 정답 = (R − L + 1) − covered.

## 정당성(요지)
- 트리의 유일 경로 성질로 인해 각 간선 방향은 루트 후보의 위치를 “어느 서브트리 안/밖” 제약으로 등가 변환할 수 있습니다.
- child→parent는 루트가 자식 서브트리 내부에 있어야 하므로 교집합으로 축약됩니다. parent→child는 자식 서브트리를 배제하므로 합집합으로 축약됩니다.
- 두 축약 결과를 결합해 |I − U| 계산만으로 모든 제약을 반영할 수 있습니다.

## 복잡도
- 전처리 DFS: O(N)
- 각 쿼리 갱신/질의: O(log N)
- 총 시간: O((N + Q) log N), 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct SegmentTree {
    int n;
    vector<int> cover;
    vector<int> covered;

    SegmentTree() {}
    SegmentTree(int n_) { init(n_); }

    void init(int n_) {
        n = n_;
        cover.assign(4 * n + 4, 0);
        covered.assign(4 * n + 4, 0);
    }

    void pull(int idx, int l, int r) {
        if (cover[idx] > 0) {
            covered[idx] = r - l + 1;
        } else {
            if (l == r) covered[idx] = 0;
            else covered[idx] = covered[idx << 1] + covered[idx << 1 | 1];
        }
    }

    void update(int idx, int l, int r, int ql, int qr, int delta) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            cover[idx] += delta;
            pull(idx, l, r);
            return;
        }
        int m = (l + r) >> 1;
        update(idx << 1, l, m, ql, qr, delta);
        update(idx << 1 | 1, m + 1, r, ql, qr, delta);
        pull(idx, l, r);
    }

    void update(int l, int r, int delta) {
        if (l > r) return;
        update(1, 1, n, l, r, delta);
    }

    int query(int idx, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) {
            if (cover[idx] > 0) return r - l + 1;
            return covered[idx];
        }
        if (cover[idx] > 0) {
            int L = max(l, ql), R = min(r, qr);
            if (L > R) return 0;
            return R - L + 1;
        }
        int m = (l + r) >> 1;
        return query(idx << 1, l, m, ql, qr) + query(idx << 1 | 1, m + 1, r, ql, qr);
    }

    int query(int l, int r) {
        if (l > r) return 0;
        return query(1, 1, n, l, r);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    struct EdgeIn { int u, v; string d; };
    vector<EdgeIn> initialEdges;
    initialEdges.reserve(N - 1);

    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < N - 1; ++i) {
        int u, v; string d;
        cin >> u >> d >> v;
        initialEdges.push_back({u, v, d});
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // Euler tour for subtree intervals
    vector<int> tin(N + 1), tout(N + 1), depth(N + 1), parent(N + 1);
    int timer = 0;
    {
        vector<int> stackNode, stackParent, stackState;
        stackNode.push_back(1);
        stackParent.push_back(0);
        stackState.push_back(0);
        depth[0] = -1;

        while (!stackNode.empty()) {
            int u = stackNode.back(); stackNode.pop_back();
            int p = stackParent.back(); stackParent.pop_back();
            int st = stackState.back(); stackState.pop_back();

            if (st == 0) {
                parent[u] = p;
                depth[u] = depth[p] + 1;
                tin[u] = ++timer;
                stackNode.push_back(u);
                stackParent.push_back(p);
                stackState.push_back(1);
                for (int v : adj[u]) if (v != p) {
                    stackNode.push_back(v);
                    stackParent.push_back(u);
                    stackState.push_back(0);
                }
            } else {
                tout[u] = timer;
            }
        }
    }

    // type per edge keyed by child node (deeper endpoint):
    // 0: "--", 1: parent->child (U set), 2: child->parent (D set)
    vector<int> type(N + 1, 0);

    SegmentTree seg(N); // maintains union size of U-intervals
    multiset<int> D_L, D_R; // for intersection of D-intervals

    auto add_U = [&](int child) {
        seg.update(tin[child], tout[child], +1);
    };
    auto remove_U = [&](int child) {
        seg.update(tin[child], tout[child], -1);
    };
    auto add_D = [&](int child) {
        D_L.insert(tin[child]);
        D_R.insert(tout[child]);
    };
    auto remove_D = [&](int child) {
        auto itL = D_L.find(tin[child]);
        if (itL != D_L.end()) D_L.erase(itL);
        auto itR = D_R.find(tout[child]);
        if (itR != D_R.end()) D_R.erase(itR);
    };

    auto set_edge_type = [&](int u, const string& d, int v, bool apply) -> int {
        int child = (depth[u] > depth[v] ? u : v);
        int newT = 0;
        if (d == "--") {
            newT = 0;
        } else if (d == "->") {
            // u -> v
            newT = (child == v ? 1 : 2);
        } else { // "<-": v -> u
            newT = (child == u ? 1 : 2);
        }
        if (apply) {
            int prev = type[child];
            if (prev == 1) remove_U(child);
            else if (prev == 2) remove_D(child);

            if (newT == 1) add_U(child);
            else if (newT == 2) add_D(child);

            type[child] = newT;
        }
        return child;
    };

    // apply initial orientations
    for (auto &e : initialEdges) {
        set_edge_type(e.u, e.d, e.v, true);
    }

    int Q; cin >> Q;
    while (Q--) {
        int u, v; string d;
        cin >> u >> d >> v;
        int child = set_edge_type(u, d, v, true);

        int L, R;
        if (D_L.empty()) {
            L = 1; R = N;
        } else {
            L = *prev(D_L.end()); // max L
            R = *D_R.begin();     // min R
        }

        if (!D_L.empty() && L > R) {
            cout << 0 << '\n';
            continue;
        }

        int covered = seg.query(L, R);
        int ans = (R - L + 1) - covered;
        cout << ans << '\n';
    }

    return 0;
}
```

## 코너 케이스 체크리스트
- child→parent 제약이 없어 I = [1, N]인 경우
- I가 공집합이 되는 경우(L > R)
- U가 비어 있는 경우(covered = 0)
- 동일 간선의 반복 갱신(이전 상태 제거 후 신규 상태 반영)
- 리프/루트에 인접한 방향 전환

## 제출 전 점검
- 입력 파싱: 방향 문자열 "->", "<-", "--" 정확히 처리
- 64-bit 필요 여부: N, Q ≤ 1e5이므로 int 충분, 커버 길이는 N 범위
- 세그먼트 트리 인덱스: [1, N] 범위 일치 여부
- Euler tour의 tin/tout 경계 정확성(닫힌 구간 사용)

## 참고자료
- 트리의 Euler tour(서브트리 구간화) 기본 기법
- 구간 피복 길이(커버 카운트 세그먼트 트리)


