---
title: "[Algorithm] cpp 백준 13896번: Sky Tax"
description: "트리에서 수도(루트)가 동적으로 바뀔 때 도시 X가 처리해야 할 세금 도시 수를 빠르게 구한다. 오일러 투어로 서브트리 크기를 전처리하고, 이진 승진(LCA) 계통 정보를 사용해 X가 수도의 조상인지 판정하여 경우를 분기해 O((N+Q)logN)으로 답한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Tree"
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13896
- cpp
- C++
- Implementation
- 구현
- Tree
- 트리
- LCA
- 최소공통조상
- Binary Lifting
- 이진 승진
- Jump Pointers
- 점프 포인터
- Euler Tour
- 오일러 투어
- Subtree Size
- 서브트리 크기
- Rooted Tree
- 루트 트리
- Ancestor Check
- 조상 판정
- isAncestor
- Depth
- 깊이
- Parent
- 부모
- Preprocessing
- 전처리
- DFS
- 깊이우선탐색
- Iterative DFS
- 반복 DFS
- Stack DFS
- 스택 DFS
- Queries
- 쿼리
- Online Queries
- 온라인 쿼리
- Dynamic Root
- 동적 루트
- Path
- 경로
- Path to Capital
- 수도 경로
- Tax Handling
- 세금 처리
- Component Size
- 컴포넌트 크기
- Complexity Analysis
- 복잡도 분석
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
- Implementation Details
- 구현 디테일
- Template
- 템플릿
- Testing
- 테스트
- Debugging
- 디버깅
- Invariant
- 불변식
- Graph
- 그래프
- Tree Queries
- 트리 쿼리
- Bangkok Regional
- 방콕 리저널
- ICPC
- 아이시피씨
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13896
- 요약: 연결 트리에서 수도 `R`가 수시로 바뀐다. 도시 `X`가 수도로 가는 모든 경로에 포함되는 도시들의 개수(=X가 세금을 처리해야 하는 도시 수)를 질의마다 출력한다.
- 제한: \(1 \le N \le 10^5\), \(1 \le Q \le 5\times 10^4\), 시간 1초, 메모리 512MB.

## 입력/출력
입력 형식 요약:
```
T                   # 테스트 케이스 수 (≤ 10)
N Q R               # 도시 수, 질의 수, 초기 수도
N-1개의 간선 A B     # 트리 간선
Q개의 줄 S U        # S=0: 수도를 U로 변경, S=1: 도시 U의 답을 출력
```

간단 예시:
```
1
5 5 1
1 2
1 3
3 4
3 5
1 1   # X=1의 답
1 3   # X=3의 답
0 5   # 수도를 5로 변경
1 3   # X=3의 답
1 5   # X=5의 답(=전체)
```

## 접근 개요
- 트리에서 어떤 도시 `A`가 도시 `B`의 세금을 처리한다는 것은, 단순 경로 `B → R`가 `A`를 지나감을 의미한다.
- 루트가 `R`일 때의 성질:
  - **`A`가 `R`이면** 모든 도시 경로가 `R`을 지나므로 답은 `N`.
  - **`A`가 `R`의 조상(=경로 상에 위치)** 이면, `A` 바로 아래에서 `R`으로 내려가는 자식 `v`를 찾고, `v`의 서브트리를 제외한 나머지가 `A`를 경유한다. 답 = `N - size[v]`.
  - **그 외**에는 `A`의 서브트리 내 모든 노드가 `A`를 지나 `R`로 가므로 답 = `size[A]`.
- 따라서 `size[*]`, `tin/tout`, `depth`, `up[k][*]`(이진 승진)만 준비되면 질의마다 \(O(\log N)\)으로 처리할 수 있다.

### 시각화 (Mermaid)
```mermaid
graph TD
    R[Capital R]
    A[City A]
    v[Child v on path A->R]
    subgraph Subtree of v
      X1[X]
      X2[Y]
    end
    A --> v --> R
    v --> X1
    v --> X2
    note[If A is ancestor of R, answer = N - size(v)]
```

## 알고리즘 설계
- 전처리(루트 임의 1):
  - 반복 DFS로 `tin/tout`, `depth`, `size[u]` 계산.
  - `up[k][u]`: `u`의 \(2^k\)번째 조상(없는 경우 0).
- 보조 함수:
  - `isAncestor(a, b)`: `a`가 `b`의 조상인지 (`tin[a] ≤ tin[b] ≤ tout[a]`)
  - `lift(u, k)`: `u`를 위로 `k`칸 올림(이진 승진)
- 질의 처리(`current R` 유지):
  - `S=0`: `R ← U` 갱신.
  - `S=1`(문의 도시 `U`):
    - `U==R` → `N`
    - `isAncestor(U, R)` → `v = lift(R, depth[R]-depth[U]-1)`, 답 = `N - size[v]`
    - 그 외 → `size[U]`

## 복잡도
- 전처리: \(O(N \log N)\), 질의당 \(O(\log N)\), 전체 \(O((N+Q)\log N)\). 메모리 \(O(N\log N)\).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Solver {
    int n, q, r;
    vector<vector<int>> adj;
    vector<int> tin, tout, depth, subSize;
    vector<vector<int>> up;
    int LOG;
    int timer;

    void build(int root = 1) {
        LOG = 1;
        while ((1 << LOG) <= n) ++LOG;
        up.assign(LOG, vector<int>(n + 1, 0));
        tin.assign(n + 1, 0);
        tout.assign(n + 1, 0);
        depth.assign(n + 1, 0);
        subSize.assign(n + 1, 0);
        timer = 0;

        struct Frame { int u, p; bool exit; };
        vector<int> parent0(n + 1, 0);
        vector<char> visited(n + 1, 0);
        stack<Frame> st;
        st.push({root, 0, false});
        parent0[root] = 0;
        depth[root] = 0;

        while (!st.empty()) {
            auto cur = st.top(); st.pop();
            int u = cur.u, p = cur.p;
            if (!cur.exit) {
                if (visited[u]) continue;
                visited[u] = 1;
                tin[u] = ++timer;
                st.push({u, p, true});
                for (int v : adj[u]) if (v != p) {
                    parent0[v] = u;
                    depth[v] = depth[u] + 1;
                    st.push({v, u, false});
                }
            } else {
                int total = 1;
                for (int v : adj[u]) if (v != p) total += subSize[v];
                subSize[u] = total;
                tout[u] = ++timer;
            }
        }

        up[0] = parent0;
        for (int k = 1; k < LOG; ++k) {
            for (int v = 1; v <= n; ++v) {
                int mid = up[k - 1][v];
                up[k][v] = mid ? up[k - 1][mid] : 0;
            }
        }
    }

    inline bool isAncestor(int a, int b) const {
        return tin[a] <= tin[b] && tout[b] <= tout[a];
    }

    int lift(int u, int k) const {
        for (int i = 0; i < LOG && u; ++i) {
            if (k & (1 << i)) u = up[i][u];
        }
        return u;
    }

    long long answerFor(int u) {
        if (u == r) return n;
        if (isAncestor(u, r)) {
            int diff = depth[r] - depth[u];
            int v = lift(r, diff - 1); // child of u on path to r
            return n - subSize[v];
        }
        return subSize[u];
    }

    void run() {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);

        int T; 
        if (!(cin >> T)) return;
        for (int tc = 1; tc <= T; ++tc) {
            cin >> n >> q >> r;
            adj.assign(n + 1, {});
            for (int i = 0; i < n - 1; ++i) {
                int a, b; cin >> a >> b;
                adj[a].push_back(b);
                adj[b].push_back(a);
            }
            build(1);

            cout << "Case #" << tc << ":\n";
            for (int i = 0; i < q; ++i) {
                int s, u; cin >> s >> u;
                if (s == 0) r = u;
                else cout << answerFor(u) << '\n';
            }
        }
    }
};

int main() {
    Solver().run();
    return 0;
}
```

## 정당성 스케치
- 트리에서 임의 두 점의 단순 경로는 유일하다. `A`가 `R`의 조상이면 `A`의 특정 자식 `v`를 거쳐 `R`로 내려가므로, `v` 서브트리만 `A`를 경유하지 않는다. 따라서 `N - size[v]`.
- `A`가 `R`의 조상이 아니면, `A` 서브트리 내부에서 올라오는 경로는 반드시 `A`를 지나 `R`로 간다. 따라서 `size[A]`.
- `A==R`이면 모든 경로가 `R`을 포함하므로 `N`.

## 코너 케이스 체크리스트
- `U == R`인 질의: `N` 반환
- 일자형(체인) 트리, 별(스타) 트리
- `N=1`, `Q=0` 또는 모두 `S=0`만 있는 입력
- 수도가 여러 번 왕복 변경되는 경우

## 제출 전 점검
- 입출력 포맷(특히 "Case #i:" 라인) 확인
- 64-bit 필요 여부 점검(여기서는 `int`로 충분하나 합은 `long long`으로 안전 처리)
- 인덱스/경계: `lift(r, diff-1)`에서 `diff≥1` 보장 확인(`u==r` 사전 처리)
- 전처리 후 `up` 테이블, `tin/tout` 일관성

## 참고자료
- 문제: https://www.acmicpc.net/problem/13896


