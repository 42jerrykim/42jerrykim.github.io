---
title: "[Algorithm] C++/Python 백준 2316번: 도시 왕복하기 2 - Dinic, Node Splitting"
description: "정점 방문 제한을 정점 분할로 모델링하고, 1·2번은 무제한·나머지는 1의 용량을 부여합니다. 양방향 도로는 양방향 간선(∞)로 만들고 Dinic으로 최대 유량을 구해 왕복 가능한 최대 횟수를 계산합니다. 구현 포인트와 엣지 케이스까지 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-2316"
- "BOJ2316"
- "cpp"
- "python"
- "C++"
- "Python"
- "Graph"
- "그래프"
- "Network Flow"
- "네트워크 플로우"
- "Max Flow"
- "최대 유량"
- "Dinic"
- "디닉"
- "Edmonds-Karp"
- "에드몬드카프"
- "Blocking Flow"
- "블로킹 플로우"
- "Layered Graph"
- "레이어드 그래프"
- "Residual Graph"
- "레지듀얼 그래프"
- "Node Splitting"
- "정점 분할"
- "Vertex Capacity"
- "정점 용량"
- "Edge Capacity"
- "간선 용량"
- "Min Cut"
- "최소 컷"
- "Cut Capacity"
- "컷 용량"
- "Flow Decomposition"
- "흐름 분해"
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
- "Invariant"
- "불변식"
- "Vertex-Disjoint Paths"
- "정점 분리 경로"
- "City Round Trip"
- "도시 왕복하기"
- "도시 왕복하기 2"
- "INF"
- "Integer Flow"
- "정수 흐름"
- "Graph Modeling"
- "그래프 모델링"
- "Adjacency List"
- "인접 리스트"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/2316
- 요약: N개의 도시(정점)와 P개의 양방향 길(간선)이 주어질 때, 1번과 2번 도시를 오가며 왕복할 수 있는 최대 횟수를 구한다. 단 1·2번 도시를 제외한 나머지 도시는 전체 과정에서 한 번만 방문할 수 있다(정점 재방문 금지). 1-2 직통 길은 입력에 없다.

## 입력/출력
```
입력: N P (3 ≤ N ≤ 400, 1 ≤ P ≤ 10000)
      P줄에 걸쳐 (a b) — a와 b 사이의 양방향 길

출력: 1번 ↔ 2번 사이를 왕복할 수 있는 최대 횟수(정수)
```

## 접근 개요
- 핵심 관찰: “정점 재방문 금지”는 정점 용량 1의 제약이다. 이를 위해 각 정점을 `v_in → v_out`으로 분할하고, `cap(v_in→v_out)`을 1로 두면 그 정점은 경로에서 단 한 번만 통과 가능해진다.
- 예외: 시작(1)과 도착(2)은 여러 번 사용 가능해야 하므로 두 정점만 `cap = ∞`.
- 양방향 길 `(a, b)`는 `a_out → b_in`, `b_out → a_in` 두 간선으로 모델링하고 각 용량은 ∞로 둔다.
- 이렇게 만든 네트워크에서 `S = 1_out`, `T = 2_in`으로 두고 최대 유량을 구하면, 곧 정점 분리(정점 용량) 하에서의 최대 정점-분리 경로 수가 된다.

```mermaid
flowchart LR
  subgraph City 1
    one_in[1_in]
    one_out[1_out]
    one_in -->|∞| one_out
  end
  subgraph City v (cap=1)
    v_in[v_in]
    v_out[v_out]
    v_in -->|1| v_out
  end
  subgraph City 2
    two_in[2_in]
    two_out[2_out]
    two_in -->|∞| two_out
  end
  one_out -->|∞| v_in
  v_out -->|∞| two_in
```

## 알고리즘 설계
- 정점 분할: 모든 정점 v에 대해 `v_in(=v)`와 `v_out(=v+N)`를 만들고 `v_in→v_out` 간선 추가.
  - `cap(1_in→1_out) = cap(2_in→2_out) = ∞`, 그 외는 1.
- 양방향 길 (a,b)에 대해
  - `a_out → b_in (∞)`, `b_out → a_in (∞)` 추가.
- 소스/싱크: `S = 1_out`, `T = 2_in`.
- 최대 유량: Dinic로 계산.
- 올바름: 각 경로가 통과하는 모든 중간 정점의 `in→out` 간선이 용량 1이므로 동일 정점의 중복 사용이 불가능. 1·2번은 ∞로 중복 사용 가능. 따라서 최대 유량 = 최대 정점-분리 경로 수.

## 복잡도
- 정점 수: 약 `2N (≤ 800)`
- 간선 수: `N`(in→out) + `2P`(양방향 변환) 정도
- Dinic: 최악 O(V^2·E), 실전에서는 매우 빠르게 동작. 본 문제 제한(N≤400, P≤10^4)에서 충분히 통과.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to, rev;
    int cap;
    Edge(int t, int r, int c) : to(t), rev(r), cap(c) {}
};

struct Dinic {
    int n;
    vector<vector<Edge>> g;
    vector<int> level, it;

    Dinic(int n_) : n(n_), g(n_), level(n_), it(n_) {}

    void addEdge(int u, int v, int c) {
        g[u].emplace_back(v, (int)g[v].size(), c);
        g[v].emplace_back(u, (int)g[u].size() - 1, 0);
    }

    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto &e : g[u]) {
                if (e.cap > 0 && level[e.to] == -1) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[t] != -1;
    }

    int dfs(int u, int t, int f) {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)g[u].size(); ++i) {
            Edge &e = g[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                int ret = dfs(e.to, t, min(f, e.cap));
                if (ret > 0) {
                    e.cap -= ret;
                    g[e.to][e.rev].cap += ret;
                    return ret;
                }
            }
        }
        return 0;
    }

    long long maxFlow(int s, int t) {
        long long flow = 0;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while (true) {
                int pushed = dfs(s, t, INT_MAX);
                if (!pushed) break;
                flow += pushed;
            }
        }
        return flow;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, P; 
    if (!(cin >> N >> P)) return 0;

    const int INF = 1e9;
    auto IN  = [&](int v) { return v; };
    auto OUT = [&](int v) { return v + N; };
    int V = 2 * N + 5;

    Dinic dinic(V);

    for (int v = 1; v <= N; ++v) {
        int cap = (v == 1 || v == 2) ? INF : 1;
        dinic.addEdge(IN(v), OUT(v), cap);
    }

    for (int i = 0; i < P; ++i) {
        int a, b; cin >> a >> b;
        dinic.addEdge(OUT(a), IN(b), INF);
        dinic.addEdge(OUT(b), IN(a), INF);
    }

    int S = OUT(1);
    int T = IN(2);
    cout << dinic.maxFlow(S, T) << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

input = sys.stdin.readline

class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = [0]*n
        self.it = [0]*n

    def add_edge(self, u: int, v: int, c: int) -> None:
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s: int, t: int) -> bool:
        self.level = [-1]*self.n
        q = deque([s])
        self.level[s] = 0
        while q:
            u = q.popleft()
            for v, c, rev in self.g[u]:
                if c > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0

    def dfs(self, u: int, t: int, f: int) -> int:
        if u == t:
            return f
        i = self.it[u]
        while i < len(self.g[u]):
            self.it[u] = i
            v, c, rev = self.g[u][i]
            if c > 0 and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, c))
                if pushed:
                    self.g[u][i][1] -= pushed
                    self.g[v][rev][1] += pushed
                    return pushed
            i += 1
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        INF = 10**18
        while self.bfs(s, t):
            self.it = [0]*self.n
            while True:
                pushed = self.dfs(s, t, 10**9)
                if pushed == 0:
                    break
                flow += pushed
        return flow

def solve() -> None:
    N, P = map(int, input().split())
    INF = 10**9
    def IN(v: int) -> int:
        return v
    def OUT(v: int) -> int:
        return v + N

    V = 2*N + 5
    dinic = Dinic(V)

    for v in range(1, N+1):
        cap = INF if v in (1, 2) else 1
        dinic.add_edge(IN(v), OUT(v), cap)

    for _ in range(P):
        a, b = map(int, input().split())
        dinic.add_edge(OUT(a), IN(b), INF)
        dinic.add_edge(OUT(b), IN(a), INF)

    S = OUT(1)
    T = IN(2)
    print(dinic.max_flow(S, T))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 경로가 전혀 없을 때: 0
- 1 또는 2와만 직접 연결된 정점들로 경로가 제한될 때(중간 정점 용량 1로 인해 상한 형성)
- 중복 도로 입력이 있을 수 있어도(문제상 보장 없음/있음 상관없이) 해는 변하지 않음
- 1-2 직통이 없는 점을 이용해 최소 1개의 중간 정점을 반드시 지나게 됨

## 제출 전 점검
- 소스/싱크를 `S=1_out`, `T=2_in`으로 설정했는지 확인
- `cap(1,2)=∞`, 그 외 정점 분할 간선의 용량 1 확인
- 도로는 양방향이므로 두 방향 간선을 모두 추가했는지 확인
- 입출력 개행/버퍼링, int 범위, INF 설정 확인

## 참고자료
- Dinic’s algorithm (Blocking flow): https://cp-algorithms.com/graph/dinic.html
- Vertex capacity via node splitting: https://cp-algorithms.com/graph/flows_with_demands.html

