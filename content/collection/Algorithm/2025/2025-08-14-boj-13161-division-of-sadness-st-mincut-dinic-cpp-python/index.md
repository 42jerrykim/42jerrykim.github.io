---
title: "[Algorithm] cpp-python 백준 13161번: 분단의 슬픔 - s-t 최소 컷"
description: "UCPC 2016 C ‘분단의 슬픔’을 s-t 최소 컷으로 푼 풀이. w[i,j]는 양방향 간선, 강제 A/B는 소스·싱크 무한 용량으로 고정. Dinic으로 최소 슬픔 합을 구하고 잔여 그래프에서 A/B를 복원한다. 모델링 근거와 컷 복원, 구현 포인트, 복잡도와 코너 케이스 점검까지 정리. C++·Python 코드 포함."
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
- Problem-13161
- cpp
- C++
- python
- Python
- Data Structures
- 자료구조
- Graph
- 그래프
- Network Flow
- 네트워크플로우
- Max Flow
- 최대유량
- Min Cut
- 최소컷
- s-t Cut
- st-컷
- Dinic
- 디닉
- Edmonds-Karp
- 에드몬즈카프
- Residual Graph
- 잔여그래프
- Level Graph
- 레벨그래프
- Blocking Flow
- 블로킹플로우
- Source
- 소스
- Sink
- 싱크
- Capacity
- 용량
- INF Edge
- 무한대간선
- Cut Capacity
- 컷용량
- Graph Cut
- 그래프컷
- Partition
- 분할
- Bipartition
- 이분분할
- Undirected Graph
- 무향그래프
- Modeling
- 모델링
- UCPC
- UCPC-2016
- Special Judge
- 스페셜저지
- Implementation
- 구현
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
- BFS
- 너비우선탐색
- Cut Recovery
- 컷복원
- Partition Recovery
- 분할복원
- UCPC-2016-C
- 분단의-슬픔
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 13161 분단의 슬픔](https://www.acmicpc.net/problem/13161)
- 요약: 사람을 두 진영 A/B로 나눌 때, 서로 다른 진영에 속하면 발생하는 슬픔 비용 `w[i,j]`의 합을 최소화하라. 일부 사람은 반드시 A 또는 B에 속해야 한다.

## 입력/출력
```
<입력>
N
g1 g2 ... gN   (gi ∈ {0,1,2}; 1=A 강제, 2=B 강제, 0=자유)
w[1,1] ... w[1,N]
  ...         ...
w[N,1] ... w[N,N]   (대칭, 대각 0)

<출력>
최소 슬픔 합
A 진영 사람 번호들 (공백 구분, 없으면 빈 줄)
B 진영 사람 번호들 (공백 구분, 없으면 빈 줄)
```

## 접근 개요
- 핵심 모델링: 무향 가중 그래프의 두 집합 분할 비용 최소화는 s-t 최소 컷으로 풀 수 있다.
  - `w[i,j]`는 간선 `i↔j` 용량 `w[i,j]`로 표현(양방향 간선 각 `w`).
  - A 강제는 `S→i`에 `INF` 용량, B 강제는 `i→T`에 `INF` 용량으로 고정.
  - 최소 컷 값 = 서로 다른 진영 간선들의 가중치 합.
- 알고리즘: Dinic(레벨 그래프 + 블로킹 플로우)로 최대 유량(=최소 컷) 계산. 잔여 그래프에서 `S`로부터 도달 가능한 정점을 A로, 나머지를 B로 복원.

```mermaid
flowchart TD
  A[입력 파싱] --> B[강제 조건: S→i (A), i→T (B) INF 간선 추가]
  B --> C[모든 i<j에 대해 i↔j 용량 w 추가]
  C --> D[Dinic으로 최대유량 계산]
  D --> E[잔여 그래프에서 S-도달 집합 = A]
  E --> F[보완 집합 = B, 최소 컷 값 출력]
```

## 알고리즘 설계
- 정점: `1..N`, 소스 `S`, 싱크 `T`.
- 간선 구성:
  - 강제 A: `S→i`에 `INF` 용량.
  - 강제 B: `i→T`에 `INF` 용량.
  - 슬픔 비용: 모든 `i<j`에 `i→j`, `j→i` 각각 용량 `w[i,j]`.
- 올바름 근거:
  - 컷이 `S-집합 | T-집합`으로 나눌 때, 임의의 `i∈S-집합`, `j∈T-집합`에 대해 `i→j`가 컷을 가로지르며 용량 `w[i,j]`가 정확히 한 번만 더해진다(반대방향 간선은 컷에 포함되지 않음). 따라서 컷 값은 서로 다른 진영 간 간선 가중치 합과 일치한다.
  - `INF` 간선은 해당 정점이 반대편으로 넘어가면 컷 값이 `INF`가 되어 최적해에서 이를 강제로 같은 편에 고정한다.

## 복잡도
- 시간: Dinic 최악 `O(V^2 E)`, 실전에서는 `O(E√V)` 근사 성능. 여기서 `V≈N+2≤502`, `E≈2·N(N-1)/2 + N ≤ 2.5e5` 규모로 C++에서 충분히 통과.
- 공간: `O(E)`.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Edge {
    int to;
    int rev;
    int64 cap;
};

struct Dinic {
    int n, s, t;
    vector<vector<Edge>> g;
    vector<int> level, work;

    Dinic(int n, int s, int t) : n(n), s(s), t(t), g(n), level(n), work(n) {}

    void addEdge(int u, int v, int64 c) {
        Edge a{v, (int)g[v].size(), c};
        Edge b{u, (int)g[u].size(), 0};
        g[u].push_back(a);
        g[v].push_back(b);
    }

    bool bfs() {
        fill(level.begin(), level.end(), -1);
        queue<int> q; level[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (const auto& e : g[u]) if (e.cap > 0 && level[e.to] == -1) {
                level[e.to] = level[u] + 1;
                q.push(e.to);
            }
        }
        return level[t] != -1;
    }

    int64 dfs(int u, int64 f) {
        if (u == t) return f;
        for (int& i = work[u]; i < (int)g[u].size(); ++i) {
            auto& e = g[u][i];
            if (e.cap <= 0 || level[e.to] != level[u] + 1) continue;
            int64 ret = dfs(e.to, min(f, e.cap));
            if (ret > 0) {
                e.cap -= ret;
                g[e.to][e.rev].cap += ret;
                return ret;
            }
        }
        return 0;
    }

    long long maxflow() {
        long long flow = 0;
        while (bfs()) {
            fill(work.begin(), work.end(), 0);
            while (true) {
                long long pushed = dfs(s, (long long)4e18);
                if (pushed == 0) break;
                flow += pushed;
            }
        }
        return flow;
    }

    vector<char> reachableFromSource() const {
        vector<char> vis(n, false);
        queue<int> q; q.push(s); vis[s] = true;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (const auto& e : g[u]) if (e.cap > 0 && !vis[e.to]) {
                vis[e.to] = true; q.push(e.to);
            }
        }
        return vis;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; if (!(cin >> N)) return 0;
    const int S = 0, T = N + 1;
    Dinic din(N + 2, S, T);

    vector<int> force(N + 1);
    for (int i = 1; i <= N; ++i) cin >> force[i];

    // 읽으면서 i<j만 처리, 무향 간선을 양방향으로 추가
    for (int i = 1; i <= N; ++i) {
        for (int j = 1; j <= N; ++j) {
            int w; cin >> w;
            if (j > i && w > 0) {
                din.addEdge(i, j, w);
                din.addEdge(j, i, w);
            }
        }
    }

    const long long INF = (long long)4e18;
    for (int i = 1; i <= N; ++i) {
        if (force[i] == 1) din.addEdge(S, i, INF);
        else if (force[i] == 2) din.addEdge(i, T, INF);
    }

    long long ans = din.maxflow();
    cout << ans << '\n';

    auto vis = din.reachableFromSource();
    bool first = true;
    for (int i = 1; i <= N; ++i) if (vis[i]) {
        if (!first) cout << ' ';
        cout << i; first = false;
    }
    cout << '\n';
    first = true;
    for (int i = 1; i <= N; ++i) if (!vis[i]) {
        if (!first) cout << ' ';
        cout << i; first = false;
    }
    cout << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

def dinic_maxflow(n, s, t, graph):
    level = [-1] * n
    work = [0] * n

    def bfs():
        for i in range(n):
            level[i] = -1
        q = deque([s])
        level[s] = 0
        while q:
            u = q.popleft()
            for v, cap, rev in graph[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] != -1

    def dfs(u, f):
        if u == t:
            return f
        i = work[u]
        while i < len(graph[u]):
            v, cap, rev = graph[u][i]
            if cap > 0 and level[v] == level[u] + 1:
                pushed = dfs(v, f if f < cap else cap)
                if pushed:
                    graph[u][i][1] -= pushed
                    graph[v][rev][1] += pushed
                    return pushed
            i += 1
            work[u] = i
        return 0

    flow = 0
    INF = 10 ** 30
    while bfs():
        for i in range(n):
            work[i] = 0
        while True:
            pushed = dfs(s, INF)
            if not pushed:
                break
            flow += pushed
    return flow

def add_edge(graph, u, v, c):
    graph[u].append([v, c, len(graph[v])])
    graph[v].append([u, 0, len(graph[u]) - 1])

def main():
    input = sys.stdin.readline
    N_line = input().strip()
    if not N_line:
        return
    N = int(N_line)
    S, T = 0, N + 1
    n = N + 2
    graph = [[] for _ in range(n)]

    force = [0] * (N + 1)
    vals = list(map(int, input().split()))
    for i in range(1, N + 1):
        force[i] = vals[i - 1]

    W = [list(map(int, input().split())) for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            w = W[i][j]
            if w:
                add_edge(graph, i + 1, j + 1, w)
                add_edge(graph, j + 1, i + 1, w)

    INF = 10 ** 30
    for i in range(1, N + 1):
        if force[i] == 1:
            add_edge(graph, S, i, INF)
        elif force[i] == 2:
            add_edge(graph, i, T, INF)

    min_cut = dinic_maxflow(n, S, T, graph)
    print(min_cut)

    # BFS on residual to get partition
    vis = [False] * n
    dq = deque([S])
    vis[S] = True
    while dq:
        u = dq.popleft()
        for v, cap, _ in graph[u]:
            if cap > 0 and not vis[v]:
                vis[v] = True
                dq.append(v)

    A = [str(i) for i in range(1, N + 1) if vis[i]]
    B = [str(i) for i in range(1, N + 1) if not vis[i]]
    print(" ".join(A))
    print(" ".join(B))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 강제 인원이 한쪽에만 몰린 경우(반대 진영이 비어도 허용, 빈 줄 출력).
- `w[i,j]=0`가 다수인 희소 케이스, 또는 모든 `w[i,j]`가 큰 촘촘한 케이스.
- `N=1` 혹은 매우 작은 입력, 대칭/대각 조건 확인(`w[i,i]=0`, `w[i,j]=w[j,i]`).
- 복원 시 잔여 간선의 양의 용량 기준으로 `S` 도달 집합을 탐색했는지 확인.

## 제출 전 점검
- `S→i`(A 강제), `i→T`(B 강제)에 충분히 큰 `INF` 적용 여부.
- 무향 간선은 양방향으로 추가했는지, `i<j`만 읽고 중복 추가 방지.
- 출력 형식(최소값 한 줄, A/B 각 한 줄)과 빈 집합 처리.
- C++: 빠른 입출력, 64-bit 용량, 오버플로 방지. Python: 재귀 없이 구현, 큐 기반 BFS/DFS.

## 참고자료
- [Minimum s-t cut (Wikipedia)](https://en.wikipedia.org/wiki/Minimum_cut)
- [Max-flow min-cut theorem (Wikipedia)](https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem)


