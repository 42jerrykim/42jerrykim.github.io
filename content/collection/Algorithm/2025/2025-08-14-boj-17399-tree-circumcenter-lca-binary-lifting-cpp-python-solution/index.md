---
title: "[Algorithm] C++/Python 백준 17399번: 트리의 외심"
description: "세 정점의 외심은 세 정점까지의 거리가 같으면서 그 거리가 최소가 되는 정점입니다. LCA·깊이로 세 경로의 교점 S를 찾고, 두 작은 팔 길이의 동일성과 큰 팔과의 짝수 차이를 이용해 존재·위치를 판정합니다. BFS+Binary Lifting로 O((N+Q)logN)에 해결합니다."
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
- Problem-17399
- cpp
- python
- C++
- Python
- Graph
- 그래프
- Tree
- 트리
- LCA
- Lowest Common Ancestor
- 최소 공통 조상
- Binary Lifting
- 이진 승수
- Distance
- 거리
- Distance on Tree
- 트리 거리
- Path
- 경로
- Kth Node
- k번째 노드
- BFS
- 너비우선탐색
- Depth
- 깊이
- Parent Table
- 부모 테이블
- Parity
- 짝수성
- Circumcenter
- 외심
- Median of Three
- 세 점의 중앙
- Steiner Point
- 스타이너 포인트
- Meeting Point
- 교점
- Proof of Correctness
- 정당성 증명
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Implementation
- 구현
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Testing
- 테스트
- Invariant
- 불변식
- Tree Center
- 트리 중심
- Pairwise LCA
- 쌍별 LCA
- Even Difference
- 짝수 차이
- K-Path Step
- 경로상 이동
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17399
- 요약: 트리에서 세 정점 `A, B, C`가 주어질 때, 세 정점으로부터의 거리가 모두 같으면서 그 거리를 최소화하는 정점(외심)이 존재하면 그 정점 번호를, 존재하지 않으면 `-1`을 구합니다. \(N, Q \le 10^5\).

## 입력/출력
```
<입력>
N
X Y   (N-1줄)
Q
A B C (Q줄)

<출력>
각 쿼리의 외심 정점 번호 또는 -1
```

## 접근 개요
- 세 정점의 경로가 만나는 교점 `S`는 `S = deepest(lca(A,B), lca(B,C), lca(C,A))`로 유일합니다.
- `da = dist(S,A)`, `db = dist(S,B)`, `dc = dist(S,C)`라 할 때, 두 작은 값이 같고 가장 큰 값과의 차가 짝수이면 외심이 존재합니다.
  - 가장 먼 정점 방향으로 `t = (max - equal) / 2`칸 이동한 정점이 외심입니다. (두 작은 값이 동일하지 않거나 차가 홀수인 경우 외심 없음)
- 거리·`k`번째 노드 연산을 위해 BFS로 깊이/부모를 만들고, Binary Lifting으로 LCA/점프를 O(logN)으로 처리합니다.

```mermaid
flowchart TD
  A[입력 트리] --> B[BFS로 depth, up[0] 구성]
  B --> C[Binary Lifting up[k] 테이블 전처리]
  C --> D[각 쿼리 (A,B,C)]
  D --> E[S = deepest of lca(A,B), lca(B,C), lca(C,A)]
  E --> F[팔 길이 da, db, dc = dist(S, A/B/C)]
  F --> G{두 작은 값 같고 (큰-작) 짝수?}
  G -- "No" --> H[-1]
  G -- "Yes" --> I[가장 먼 정점으로 (차/2)칸 이동]
  I --> J[해당 정점이 외심]
```

## 알고리즘 설계
- 전처리
  - 루트 1에서 BFS로 `depth[v]`, 1단계 부모 `up[0][v]` 구성
  - `up[k][v] = up[k-1][ up[k-1][v] ]`로 Binary Lifting 테이블 구축
- 질의 처리 (각 O(logN))
  - `S = argmax_depth{ lca(A,B), lca(B,C), lca(C,A) }`
  - `da, db, dc` 계산 후 오름차순 정렬: `x <= y <= z`
  - `x == y`이고 `z - x`가 짝수면, `t = (z - x) / 2`와 가장 먼 정점 `F`를 잡아 `answer = kthOnPath(S, F, t)`
  - 아니면 `-1`
- 올바름 근거(요지)
  - 세 경로의 합은 `S`를 중심으로 하는 Y-형입니다. `x == y`일 때 `S`에서 가장 긴 팔로 `t`만큼 이동하면 세 점까지의 거리가 모두 `(x + t) = (z - t)`로 일치합니다. `z - x`가 홀수면 정수 칸에서 일치 불가.

## 복잡도
- 시간: \(O((N + Q) \log N)\)
- 공간: \(O(N \log N)\)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < N - 1; ++i) {
        int x, y; cin >> x >> y;
        adj[x].push_back(y);
        adj[y].push_back(x);
    }

    int LOG = 1;
    while ((1 << LOG) <= N) ++LOG;

    vector<int> depth(N + 1, 0);
    vector<vector<int>> up(LOG, vector<int>(N + 1, 0));

    {
        queue<int> q;
        q.push(1);
        up[0][1] = 0;
        depth[1] = 0;

        vector<char> visited(N + 1, 0);
        visited[1] = 1;

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (!visited[v]) {
                    visited[v] = 1;
                    up[0][v] = u;
                    depth[v] = depth[u] + 1;
                    q.push(v);
                }
            }
        }
    }

    for (int k = 1; k < LOG; ++k) {
        for (int v = 1; v <= N; ++v) {
            int mid = up[k - 1][v];
            up[k][v] = (mid == 0 ? 0 : up[k - 1][mid]);
        }
    }

    auto lift = [&](int u, int k) {
        for (int i = 0; i < LOG && u; ++i) {
            if (k & (1 << i)) u = up[i][u];
        }
        return u;
    };

    auto lca = [&](int a, int b) {
        if (depth[a] < depth[b]) swap(a, b);
        a = lift(a, depth[a] - depth[b]);
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; --k) {
            if (up[k][a] != up[k][b]) {
                a = up[k][a];
                b = up[k][b];
            }
        }
        return up[0][a];
    };

    auto dist = [&](int a, int b) {
        int w = lca(a, b);
        return depth[a] + depth[b] - 2 * depth[w];
    };

    auto kthOnPath = [&](int u, int v, int k) {
        int w = lca(u, v);
        int du = depth[u] - depth[w];
        if (k <= du) return lift(u, k);
        int dv = depth[v] - depth[w];
        int upSteps = dv - (k - du);
        return lift(v, upSteps);
    };

    int Q; cin >> Q;
    while (Q--) {
        int a, b, c; cin >> a >> b >> c;

        int ab = lca(a, b);
        int bc = lca(b, c);
        int ca = lca(c, a);
        int s = ab;
        if (depth[bc] > depth[s]) s = bc;
        if (depth[ca] > depth[s]) s = ca;

        array<pair<int,int>,3> d = {{
            {dist(s, a), 0},
            {dist(s, b), 1},
            {dist(s, c), 2}
        }};
        sort(d.begin(), d.end());

        if (d[0].first == d[1].first) {
            if (d[2].first == d[1].first) {
                cout << s << '\n';
            } else {
                int diff = d[2].first - d[0].first;
                if (diff % 2) {
                    cout << -1 << '\n';
                } else {
                    int nodes[3] = {a, b, c};
                    int farNode = nodes[d[2].second];
                    int t = diff / 2;
                    int ans = kthOnPath(s, farNode, t);
                    cout << ans << '\n';
                }
            }
        } else {
            cout << -1 << '\n';
        }
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

def main():
    N_line = input().strip()
    if not N_line:
        return
    N = int(N_line)

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        x, y = map(int, input().split())
        adj[x].append(y)
        adj[y].append(x)

    LOG = 1
    while (1 << LOG) <= N:
        LOG += 1

    depth = [0] * (N + 1)
    up = [[0] * (N + 1) for _ in range(LOG)]

    q = deque([1])
    visited = [False] * (N + 1)
    visited[1] = True
    depth[1] = 0
    up[0][1] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                depth[v] = depth[u] + 1
                up[0][v] = u
                q.append(v)

    for k in range(1, LOG):
        for v in range(1, N + 1):
            mid = up[k - 1][v]
            up[k][v] = 0 if mid == 0 else up[k - 1][mid]

    def lift(u: int, k: int) -> int:
        i = 0
        while k and u and i < LOG:
            if k & 1:
                u = up[i][u]
            k >>= 1
            i += 1
        return u

    def lca(a: int, b: int) -> int:
        if depth[a] < depth[b]:
            a, b = b, a
        a = lift(a, depth[a] - depth[b])
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return up[0][a]

    def dist(a: int, b: int) -> int:
        w = lca(a, b)
        return depth[a] + depth[b] - 2 * depth[w]

    def kth_on_path(u: int, v: int, k: int) -> int:
        w = lca(u, v)
        du = depth[u] - depth[w]
        if k <= du:
            return lift(u, k)
        dv = depth[v] - depth[w]
        up_steps = dv - (k - du)
        return lift(v, up_steps)

    Q = int(input())
    out_lines = []
    for _ in range(Q):
        a, b, c = map(int, input().split())
        ab = lca(a, b)
        bc = lca(b, c)
        ca = lca(c, a)
        s = ab
        if depth[bc] > depth[s]:
            s = bc
        if depth[ca] > depth[s]:
            s = ca

        arr = [(dist(s, a), 0), (dist(s, b), 1), (dist(s, c), 2)]
        arr.sort()

        if arr[0][0] == arr[1][0]:
            if arr[2][0] == arr[1][0]:
                out_lines.append(str(s))
            else:
                diff = arr[2][0] - arr[0][0]
                if diff % 2 == 1:
                    out_lines.append("-1")
                else:
                    nodes = [a, b, c]
                    far_node = nodes[arr[2][1]]
                    t = diff // 2
                    ans = kth_on_path(s, far_node, t)
                    out_lines.append(str(ans))
        else:
            out_lines.append("-1")

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 세 팔 길이 `da, db, dc` 중 둘이 같은가? (두 작은 값 동일 필요)
- `z - x`의 짝/홀성 확인 (홀수면 외심 없음)
- `S` 자체가 답인 경우: `da == db == dc`
- `A=B` 또는 중복 정점 포함, `N=1,2`와 같은 극단 입력
- 큰 입력에서 빠른 입출력과 비재귀(LCA) 구현

## 제출 전 점검
- LCA 테이블 크기: `LOG` 계산과 경계(부모 0 처리) 확인
- `kthOnPath`에서 `k` 경계와 `upSteps` 음수/0 처리
- 거리/깊이 합산 시 64-bit가 필요하지 않은지 확인(여기선 간선 수이므로 `int` 가능)
- 입력 루틴(slow I/O) 최적화: C++ `sync_with_stdio(false)`, Python `sys.stdin.readline`

## 참고자료/유사문제
- 트리에서 세 점의 Y-형 구조와 LCA 성질
- LCA(Binary Lifting) 표준 구현 패턴


