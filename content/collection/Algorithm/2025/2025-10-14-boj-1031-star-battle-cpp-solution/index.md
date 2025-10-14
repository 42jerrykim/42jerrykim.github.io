---
title: "[Algorithm] C++ 백준 1031번: 스타 대결"
description: "지민 팀 N명과 한수 팀 M명의 요구 경기 수를 만족하는 N×M 0/1 대진표에서 사전순 최소를 구합니다. 각 칸을 0으로 두는 것을 우선 시도하고, 남은 차수로 유량 가능성을 판정하여 불가하면 1로 고정합니다. 합 불일치나 차수 초과 시 -1을 출력합니다."
date: 2025-10-14
lastmod: 2025-10-14
categories:
  - Algorithm
  - Graph
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Baekjoon
  - Problem-1031
  - C++
  - CPP
  - Graph
  - 그래프
  - Network Flow
  - 네트워크 플로우
  - Max Flow
  - 최대유량
  - Dinic
  - 디닉
  - Bipartite
  - 이분 그래프
  - Matching
  - 매칭
  - 0-1 Matrix
  - 0-1 행렬
  - Binary Matrix
  - 이진 행렬
  - Row Sum
  - 행 합
  - Column Sum
  - 열 합
  - Degree Sequence
  - 차수열
  - Feasibility
  - 가능성 판정
  - Greedy
  - 그리디
  - Lexicographic
  - 사전순
  - Lexicographically Smallest
  - 최소 사전순
  - Construction
  - 구성
  - Constructive Algorithm
  - 구성 알고리즘
  - Residual Graph
  - 잔여그래프
  - Level Graph
  - 레벨 그래프
  - Blocking Flow
  - 블로킹 플로우
  - BFS
  - DFS
  - Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Implementation
  - 구현
  - Edge Cases
  - 코너 케이스
  - Proof of Correctness
  - 정당성 증명
  - Editorial
  - 에디토리얼
  - Tutorial
  - 튜토리얼
  - Tips
  - 팁
  - Pitfalls
  - 실수 포인트
  - Flow Network
  - 플로우 네트워크
  - Capacity
  - 용량
  - Adjacency
  - 인접
image: "wordcloud.png"
---

## 문제 정보

- 문제: `https://www.acmicpc.net/problem/1031`
- 제목: 스타 대결
- 요약: 지민 팀(행)과 한수 팀(열)의 선수들이 해야 하는 경기 수를 각각 만족하도록 N×M 0/1 대진표를 구성합니다. 가능한 해가 여러 개라면 사전순으로 가장 앞서는 대진표를 출력합니다. 불가능하면 -1을 출력합니다.
- 제한: N, M ≤ 50, 각 필요 경기 수 ≤ 50, 시간 2초, 메모리 128MB

## 입출력 형식/예제

입력

```text
3 3
1 2 3
3 1 2
```

출력

```text
100
101
111
```

다른 예시

```text
4 4
3 2 1 1
1 3 1 2
```

가능한 사전순 최소 해 중 하나

```text
0111
0101
0100
1000
```

## 접근 개요(아이디어 스케치)

- 목표는 사전순 최소이므로, 행 우선·열 우선으로 각 칸을 0으로 두는 것을 먼저 시도합니다.
- 어떤 칸 `(i, j)`를 0으로 가정했을 때, 남은 칸들로 각 행/열의 남은 요구량을 모두 충족할 수 있는지 판정해야 합니다.
- 판정은 네트워크 플로우로 모델링합니다: `S → 행(i) → 열(j) → T`로 구성하고, `cap(S, 행 i)=남은 행 요구량`, `cap(행 i, 열 j)=1(배정 가능 칸)`, `cap(열 j, T)=남은 열 요구량`으로 두어 최대유량이 총 요구량과 같으면 가능.
- 만약 0으로 두면 불가능하다면, 해당 칸은 1로 고정하고 양쪽 요구량을 1씩 감소시킵니다.
- 추가로, 어떤 칸을 0으로 만들면 특정 행/열의 남은 칸 수보다 요구량이 커지는 즉시 모순이면 그 칸은 1로 강제합니다.

```mermaid
flowchart TD
  A[주사 순서: i=1..N, j=1..M] --> B{(i,j) 0 시도}
  B -->|가능| C[ans[i][j]=0 유지]
  B -->|불가능| D[ans[i][j]=1 고정 및 수요 감소]
  D --> A
  C --> A
```

## 알고리즘 설계

- 사전순: 행 인덱스가 작은 행부터, 같은 행에서는 열 인덱스가 작은 칸부터 결정.
- 즉시 강제 규칙: `(i,j)`를 제거하면 `rowNeed[i] > rowAllowed[i]-1` 또는 `colNeed[j] > colAllowed[j]-1`가 되면 1로 강제.
- 가능성 판정(최대유량):
  - 정점: `S`, 각 행 정점 `R_i`(N개), 각 열 정점 `C_j`(M개), `T`.
  - 간선: `S→R_i` 용량 `rowNeed[i]`, `R_i→C_j` 용량 1(남은 칸), `C_j→T` 용량 `colNeed[j]`.
  - 유량이 `sum(rowNeed)`와 같으면 배정 가능.
- 구현: Dinic(레벨 그래프 + 블로킹 플로우)로 충분. N, M ≤ 50이므로 최악의 경우에도 시간 내 가능.

## 복잡도

- 칸마다 0을 우선 시도 → 최악 `N*M`번 판정.
- 각 판정은 정점 `V ≈ N+M+2 ≤ 102`, 간선 `E ≤ N*M + N + M ≤ 2600`의 최대유량.
- 전체 시간 복잡도: 대략 `O(N*M * Dinic(V,E))` (실측으로 매우 빠름). 공간 복잡도: `O(V+E)`.

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Dinic {
    struct Edge { int to, cap, rev; };
    int N, s, t;
    vector<vector<Edge>> G;
    vector<int> level, it;
    Dinic(int n, int s_, int t_) : N(n), s(s_), t(t_), G(n), level(n), it(n) {}
    void addEdge(int u, int v, int c) {
        Edge a{v, c, (int)G[v].size()};
        Edge b{u, 0, (int)G[u].size()};
        G[u].push_back(a);
        G[v].push_back(b);
    }
    bool bfs() {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0; q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (auto &e : G[v]) if (e.cap > 0 && level[e.to] < 0) {
                level[e.to] = level[v] + 1;
                q.push(e.to);
            }
        }
        return level[t] >= 0;
    }
    int dfs(int v, int f) {
        if (v == t) return f;
        for (int &i = it[v]; i < (int)G[v].size(); ++i) {
            Edge &e = G[v][i];
            if (e.cap > 0 && level[v] < level[e.to]) {
                int d = dfs(e.to, min(f, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    G[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }
    int maxflow() {
        int flow = 0, INF = 1e9;
        while (bfs()) {
            fill(it.begin(), it.end(), 0);
            while (true) {
                int f = dfs(s, INF);
                if (!f) break;
                flow += f;
            }
        }
        return flow;
    }
};

static bool feasible(const vector<vector<int>> &allowed,
                     const vector<int> &rowNeed,
                     const vector<int> &colNeed) {
    int N = (int)rowNeed.size();
    int M = (int)colNeed.size();
    int sumR = 0, sumC = 0;
    for (int x : rowNeed) sumR += x;
    for (int x : colNeed) sumC += x;
    if (sumR != sumC) return false;

    vector<int> rowAllowed(N, 0), colAllowed(M, 0);
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < M; ++j)
            if (allowed[i][j]) {
                rowAllowed[i]++;
                colAllowed[j]++;
            }
    for (int i = 0; i < N; ++i) if (rowNeed[i] > rowAllowed[i]) return false;
    for (int j = 0; j < M; ++j) if (colNeed[j] > colAllowed[j]) return false;
    if (sumR == 0) return true;

    int S = 0, T = N + M + 1;
    Dinic din(N + M + 2, S, T);

    for (int i = 0; i < N; ++i)
        if (rowNeed[i] > 0) din.addEdge(S, 1 + i, rowNeed[i]);

    for (int i = 0; i < N; ++i) if (rowNeed[i] > 0) {
        for (int j = 0; j < M; ++j)
            if (allowed[i][j] && colNeed[j] > 0)
                din.addEdge(1 + i, 1 + N + j, 1);
    }

    for (int j = 0; j < M; ++j)
        if (colNeed[j] > 0) din.addEdge(1 + N + j, T, colNeed[j]);

    int f = din.maxflow();
    return f == sumR;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    if (!(cin >> N >> M)) return 0;
    vector<int> rowNeed(N), colNeed(M);
    for (int i = 0; i < N; ++i) cin >> rowNeed[i];
    for (int j = 0; j < M; ++j) cin >> colNeed[j];

    long long sumR = 0, sumC = 0;
    for (int x : rowNeed) { if (x < 0 || x > M) { cout << -1 << '\n'; return 0; } sumR += x; }
    for (int x : colNeed) { if (x < 0 || x > N) { cout << -1 << '\n'; return 0; } sumC += x; }
    if (sumR != sumC) { cout << -1 << '\n'; return 0; }

    vector<vector<int>> allowed(N, vector<int>(M, 1));
    if (!feasible(allowed, rowNeed, colNeed)) { cout << -1 << '\n'; return 0; }

    vector<string> ans(N, string(M, '0'));
    vector<int> rowAllowed(N, M), colAllowed(M, N);

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            if (!allowed[i][j]) continue;

            if (rowNeed[i] == 0 || colNeed[j] == 0) {
                allowed[i][j] = 0;
                rowAllowed[i]--; colAllowed[j]--;
                continue;
            }

            if (rowNeed[i] > rowAllowed[i] - 1 || colNeed[j] > colAllowed[j] - 1) {
                ans[i][j] = '1';
                rowNeed[i]--; colNeed[j]--;
                allowed[i][j] = 0;
                rowAllowed[i]--; colAllowed[j]--;
                continue;
            }

            allowed[i][j] = 0;
            rowAllowed[i]--; colAllowed[j]--;
            if (feasible(allowed, rowNeed, colNeed)) {
                // keep 0
            } else {
                allowed[i][j] = 1;
                rowAllowed[i]++; colAllowed[j]++;

                ans[i][j] = '1';
                rowNeed[i]--; colNeed[j]--;
                allowed[i][j] = 0;
                rowAllowed[i]--; colAllowed[j]--;
            }
        }
    }

    for (int x : rowNeed) if (x != 0) { cout << -1 << '\n'; return 0; }
    for (int x : colNeed) if (x != 0) { cout << -1 << '\n'; return 0; }

    for (int i = 0; i < N; ++i) {
        cout << ans[i] << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트

- `sum(rowNeed) ≠ sum(colNeed)` → 즉시 `-1`.
- 행/열 요구량이 남은 배정 가능 칸 수를 초과 → 즉시 불가능.
- 모든 요구량이 0 → 모두 0 행렬 출력.
- N=1 또는 M=1의 단순 경우 → 연속 1 배치가 사전순 최소.
- 동일한 요구량 분포가 여러 해를 허용 → 0 우선 시도로 사전순 최소 보장.

## 참고/유사 문제

- 행/열 합이 주어진 0/1 행렬 구성: 네트워크 플로우 표준 모델.
- 사전순 최소 구성은 "0 우선 시도 + 가능성 판정" 그리디로 자주 등장.


