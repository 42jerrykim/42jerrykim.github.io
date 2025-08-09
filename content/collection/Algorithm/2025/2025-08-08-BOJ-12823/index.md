---
title: "[Algorithm] C++ 백준 12823번 : Critical Projects"
categories:
- Algorithm
- Graph Theory
- DAG
- Topological Sort
description: "BOJ 12823 Critical Projects 문제다. DAG에서 모든 정점이 임계 정점인지 판단하는 문제다. 위상 정렬과 도달 가능성을 활용해 O(N+M) 시간복잡도로 해결한다. 차분 배열과 접두사 합으로 임계성을 효율적으로 검사한다."
tags:
  - Algorithm
  - 알고리즘
  - Graph Theory
  - 그래프 이론
  - DAG
  - 방향 비순환 그래프
  - Topological Sort
  - 위상 정렬
  - Kahn's Algorithm
  - 칸 알고리즘
  - Reachability
  - 도달 가능성
  - Difference Array
  - 차분 배열
  - Prefix Sum
  - 접두사 합
  - Suffix Sum
  - 접미사 합
  - Adjacency List
  - 인접 리스트
  - Forward-star
  - 포워드 스타
  - In-degree
  - 진입 차수
  - Out-degree
  - 진출 차수
  - Linear Time
  - 선형 시간
  - "O(N+M)"
  - 빠른 입출력
  - Fast I/O
  - getchar_unlocked
  - Critical Vertex
  - 임계 정점
  - Partial Order
  - 부분 순서
  - Transitivity
  - 추이성
  - Queue
  - 큐
  - Memory Optimization
  - 메모리 최적화
  - BOJ
  - 백준
  - "C++"
  - "C++17"
  - Topological Order
  - 위상 순서
  - Large Input
  - 대용량 입력
date: 2025-08-08
image: wordcloud.png
---

프로젝트 간 선행 관계가 주어진 DAG에서, 모든 다른 정점과 반드시 선행 관계(앞서거나 뒤서거나)가 성립하는 "critical" 정점을 찾는 문제이다. 각 정점이 critical인지 판정하려면 해당 정점에서 도달 가능한 정점들과 해당 정점으로 도달 가능한 정점들의 합이 전체 정점 수와 같은지 확인하면 된다. 이를 위해 위상 정렬과 도달 가능성 분석을 활용하여 효율적으로 해결할 수 있다.


문제: [https://www.acmicpc.net/problem/12823](https://www.acmicpc.net/problem/12823)

## 문제 요약

N개의 하위 프로젝트(정점)와 선행 관계(유향 간선)가 주어진 DAG에서, 정점 u가 다른 모든 정점 v에 대해 `u → v` 또는 `v → u` 중 하나가 반드시 성립하는 정점들을 모두 구한다. 이러한 정점을 문제에서는 “critical”이라 부른다.

- 정의
  - 직접 선행: `u → v`는 하위 프로젝트 `u`가 `v`보다 먼저 완료되어야 함을 의미한다.
  - 선행: 직접 선행의 추이적 개념으로, 어떤 `z`가 있어 `u → z`이며 `z → v`이면 `u → v`라고 본다.
  - critical 정점: 모든 다른 정점 `v`에 대해 `v → u` 또는 `u → v` 중 하나가 성립하는 정점 `u`.
  - 사이클 없음: 자기 자신으로 돌아오는 경로가 없어 전체 프로젝트를 완료할 수 있음(즉, 그래프는 DAG).

- 입력 형식
  - 첫 줄: `N M` — `1 ≤ N ≤ 100000`, `0 ≤ M ≤ 1000000`
  - 다음 `M`줄: `u v` — `1 ≤ u ≠ v ≤ N`, 여기서 `u`는 `v`의 직접 선행 관계를 의미

- 출력 형식
  - 첫 줄: critical 정점의 개수 `K`
  - 둘째 줄: critical 정점의 번호를 오름차순으로 공백으로 구분해 출력
  - critical 정점이 하나도 없으면 첫 줄에 `0`만 출력

- 제한
  - 시간 제한: 0.6초
  - 메모리 제한: 32 MB

- 예제
  - 입력

    ```text
    7 9
    1 3
    2 3
    3 4
    3 5
    4 6
    5 6
    1 7
    3 7
    7 4
    ```

  - 출력

    ```text
    2
    3 6
    ```

- 참고: 원문은 [BOJ 12823 — Critical Projects](https://www.acmicpc.net/problem/12823).

## 핵심 아이디어

- DAG의 위상 순서를 `p[1..N]`라 하자. `p[k]`가 critical이려면:
  - 앞쪽 부분 그래프 `[1..k]`에서 `p[k]`가 유일한 싱크여야 한다.
  - 뒤쪽 부분 그래프 `[k..N]`에서 `p[k]`가 유일한 소스여야 한다.
- 이를 O(N+M)으로 판정할 수 있다.
  - `pos[u]`: 위상 순서에서 u의 위치
  - `minOutIdx[u]`: 간선 `u→v`에 대해 `min(pos[v])` (없으면 `N+1`)
  - `maxInIdx[v]`: 간선 `u→v`에 대해 `max(pos[u])` (없으면 `0`)
  - k에서 프리픽스 싱크 수 = `pos[i] ≤ k`이면서 `minOutIdx[i] > k`인 i의 개수
    - 각 i는 구간 `k ∈ [pos[i], minOutIdx[i]-1]`에서 싱크에 기여 → 차분 배열로 일괄 집계
  - k에서 서픽스 소스 수 = `pos[j] ≥ k`이면서 `maxInIdx[j] < k`인 j의 개수
    - 각 j는 구간 `k ∈ [maxInIdx[j]+1, pos[j]]`에서 소스에 기여 → 차분 배열로 일괄 집계
  - 두 값이 모두 1인 k의 정점만 critical.

메모리 제약(32MB)과 M ≤ 1e6을 고려하여, forward-star 인접 리스트와 빠른 입력, O(N+M) 알고리즘으로 구현한다.

## C++17 풀이

```cpp
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 100000 + 5;
static const int MAXM = 1000000 + 5;

#ifndef _WIN32
#define GETCHAR getchar_unlocked
#else
#define GETCHAR getchar
#endif

inline int readInt() {
    int c = GETCHAR();
    while (c <= ' ') c = GETCHAR();
    int x = 0;
    while (c > ' ') {
        x = x * 10 + (c - '0');
        c = GETCHAR();
    }
    return x;
}

int N, M;

int headArr[MAXN];
int toArr[MAXM];
int nxtArr[MAXM];
int edgeCnt = 0;

int indeg[MAXN];
int orderArr[MAXN], posArr[MAXN];

int minOutIdx[MAXN];
int maxInIdx[MAXN];

int diffPref[MAXN + 5];
int diffSuf[MAXN + 5];

int qArr[MAXN];
int ansArr[MAXN];

inline void addEdge(int u, int v) {
    toArr[edgeCnt] = v;
    nxtArr[edgeCnt] = headArr[u];
    headArr[u] = edgeCnt++;
}

int main() {
    N = readInt();
    M = readInt();

    for (int i = 1; i <= N; ++i) {
        headArr[i] = -1;
        indeg[i] = 0;
    }

    for (int i = 0; i < M; ++i) {
        int u = readInt();
        int v = readInt();
        addEdge(u, v);
        ++indeg[v];
    }

    int qh = 0, qt = 0;
    for (int i = 1; i <= N; ++i) if (indeg[i] == 0) qArr[qt++] = i;

    int ordLen = 0;
    while (qh < qt) {
        int u = qArr[qh++];
        orderArr[++ordLen] = u;
        for (int e = headArr[u]; e != -1; e = nxtArr[e]) {
            int v = toArr[e];
            if (--indeg[v] == 0) qArr[qt++] = v;
        }
    }

    for (int i = 1; i <= N; ++i) posArr[orderArr[i]] = i;

    for (int i = 1; i <= N; ++i) {
        minOutIdx[i] = N + 1;
        maxInIdx[i] = 0;
    }

    for (int u = 1; u <= N; ++u) {
        for (int e = headArr[u]; e != -1; e = nxtArr[e]) {
            int v = toArr[e];
            int pu = posArr[u];
            int pv = posArr[v];
            if (pv < minOutIdx[u]) minOutIdx[u] = pv;
            if (pu > maxInIdx[v]) maxInIdx[v] = pu;
        }
    }

    for (int i = 1; i <= N; ++i) diffPref[i] = diffSuf[i] = 0;

    for (int i = 1; i <= N; ++i) {
        int l = posArr[i];
        int r = minOutIdx[i] - 1;
        if (r > N) r = N;
        if (l <= r) {
            ++diffPref[l];
            --diffPref[r + 1];
        }
    }

    for (int j = 1; j <= N; ++j) {
        int L = maxInIdx[j] + 1;
        int R = posArr[j];
        if (L < 1) L = 1;
        if (L <= R) {
            ++diffSuf[L];
            --diffSuf[R + 1];
        }
    }

    int prefCnt = 0, sufCnt = 0, ansCnt = 0;
    for (int k = 1; k <= N; ++k) {
        prefCnt += diffPref[k];
        sufCnt += diffSuf[k];
        if (prefCnt == 1 && sufCnt == 1) ansArr[ansCnt++] = orderArr[k];
    }

    if (ansCnt == 0) {
        printf("0\n");
        return 0;
    }

    sort(ansArr, ansArr + ansCnt);
    printf("%d\n", ansCnt);
    for (int i = 0; i < ansCnt; ++i) {
        if (i) putchar(' ');
        printf("%d", ansArr[i]);
    }
    putchar('\n');
    return 0;
}
```

## 복잡도

- 시간: O(N + M)
- 공간: O(N + M) — 인접 리스트(Forward-star), 각종 보조 배열

## 포인트 정리

- 위상 정렬 한 번과 간선 한 번의 순회로 `minOutIdx`, `maxInIdx` 산출
- 프리픽스 싱크/서픽스 소스의 “유일성”을 차분 배열 누적으로 O(N)에 판정
- 대규모 입력(최대 1e6 간선) 대비 빠른 입력과 저메모리 구현


