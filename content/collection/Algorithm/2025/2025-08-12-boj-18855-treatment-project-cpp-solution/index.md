---
title: "[Algorithm] C++ 백준 18855번 : Treatment Project"
description: "JOI 2019/2020 Day4 C, 백준 18855 Treatment Project의 정해 구현. 프로젝트들을 정점(정점 비용)으로 보고 시간-구간 제약을 불등식으로 변환해 간선을 정의, 시작(L=1)에서 종료(R=N)까지 정점 비용 최단경로를 다익스트라로 구한다. 간선 전개는 T별로 정렬해 세그트리로 한 번씩만 활성화하여 전체 O(M log M)에 해결한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
- "JOI"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "18855"
- "Treatment Project"
- "JOI"
- "JOISC"
- "JOI-2019-2020"
- "Japanese Olympiad in Informatics"
- "Graph"
- "그래프"
- "Shortest-Path"
- "최단경로"
- "Dijkstra"
- "다익스트라"
- "Segment-Tree"
- "세그먼트-트리"
- "세그트리"
- "Range-Query"
- "범위-질의"
- "Priority-Queue"
- "우선순위-큐"
- "Heap"
- "힙"
- "Coordinate-Compression"
- "좌표-압축"
- "Inequality-Graph"
- "불등식-그래프"
- "Interval"
- "구간"
- "Offline-Activation"
- "오프라인-활성화"
- "One-Pass-Activation"
- "한번씩-전개"
- "O(M-log-M)"
- "시간-복잡도"
- "Complexity"
- "Implementation"
- "구현"
- "Edge-Cases"
- "경계-처리"
- "Integer-Overflow"
- "정수-오버플로"
- "Long-Long"
- "64-bit"
- "Fast-IO"
- "빠른입출력"
- "CPP"
- "C++"
- "GNU++17"
- "Problem-Solving"
- "PS"
- "Competitive-Programming"
- "컴퓨티티브-프로그래밍"
- "Editorial"
- "해설"
- "Solution-Code"
- "정답-코드"
image: "wordcloud.png"
---

문제: [BOJ 18855 - Treatment Project](https://www.acmicpc.net/problem/18855)

### 아이디어 요약
- 모든 시민이 회복하려면 시작 경계 `1`과 끝 경계 `N`을 반드시 한 번씩 덮는 프로젝트가 필요합니다. 각 프로젝트 `i`를 정점(선택 비용 `C_i`)으로 보고, “감염 경계선”이 시간에 따라 이동할 수 있게 만드는 다음 불등식으로 간선을 정의합니다.
  - `T_i ≤ T_j`이면 `L_j + T_j ≤ R_i + T_i` (우측으로 확장 가능)
  - `T_i ≥ T_j`이면 `L_j − T_j ≤ R_i − T_i` (좌측으로 확장 가능)
- 시작 정점: `L=1`(코드에서 `L←L−1`로 half-open 처리 후 `L=0`)인 프로젝트. 종료 정점: `R=N`인 프로젝트. 시작들에서 종료들까지의 “정점 비용” 최단경로가 최소 합계 비용.
- 간선 전개 최적화: `valF=L+T`, `valB=L−T`, `thF=R+T`, `thB=R−T`를 두고 `T`별로 `valF/valB`로 정렬해 두 그룹을 만든 뒤, 다익스트라 진행 중 세그트리로 “현재 한계(thF/thB) 이하의 머리 원소”만 한 번씩 꺼내 활성화합니다. 각 정점은 많아야 한 번 활성화되어 전체 `O(M log M)`.

### 구현 메모
- 입력은 1-index `[L, R]`라서 `L ← L-1`로 half-open 처리합니다(불등식이 깔끔해짐).
- `long long`으로 안전하게 합산합니다(`C_i ≤ 1e9`, `M ≤ 1e5`).
- 시작 정점(Seed)은 우선순위 큐에 비용 `C_i`로 넣고, 그룹 활성화 목록에서는 제외해도 됩니다(시작을 중간에 다시 도달하는 것이 이득이 아님).

### C++ 풀이

```cpp
// 더 많은 알고리즘/풀이 글은 42jerrykim.github.io에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
const int64 INF = (1LL<<62);

struct Project {
    int64 T, L, R, C; // L is shifted later (L-1)
    int tpos;         // compressed T index
    int64 valF;       // L + T
    int64 valB;       // L - T
    int64 thF;        // R + T
    int64 thB;        // R - T
};

struct SegMin {
    int n; vector<int64> tree;
    SegMin() {}
    SegMin(int sz, const vector<int64>& init) { build(sz, init); }
    void build(int sz, const vector<int64>& init) {
        n = 1; while (n < sz) n <<= 1;
        tree.assign(2*n, INF);
        for (int i = 0; i < (int)init.size(); ++i) tree[n+i] = init[i];
        for (int i = n-1; i >= 1; --i) tree[i] = min(tree[i<<1], tree[i<<1|1]);
    }
    void point_set(int pos, int64 val) {
        int p = pos + n; tree[p] = val;
        for (p >>= 1; p; p >>= 1) tree[p] = min(tree[p<<1], tree[p<<1|1]);
    }
    int find_first_le(int l, int r, int64 limit) { return find_first_le_impl(1, 0, n-1, l, r, limit); }
    int find_first_le_impl(int node, int nl, int nr, int ql, int qr, int64 limit) {
        if (qr < nl || nr < ql) return -1;
        if (tree[node] > limit) return -1;
        if (nl == nr) return nl;
        int mid = (nl + nr) >> 1;
        int left = find_first_le_impl(node<<1, nl, mid, ql, qr, limit);
        if (left != -1) return left;
        return find_first_le_impl(node<<1|1, mid+1, nr, ql, qr, limit);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int64 N; int M;
    if (!(cin >> N >> M)) return 0;

    vector<Project> a(M);
    vector<int64> allT; allT.reserve(M);
    for (int i = 0; i < M; ++i) {
        cin >> a[i].T >> a[i].L >> a[i].R >> a[i].C;
        a[i].L -= 1; // make half-open
        allT.push_back(a[i].T);
    }

    sort(allT.begin(), allT.end());
    allT.erase(unique(allT.begin(), allT.end()), allT.end());
    for (int i = 0; i < M; ++i) {
        a[i].tpos = int(lower_bound(allT.begin(), allT.end(), a[i].T) - allT.begin());
        a[i].valF = a[i].L + a[i].T;
        a[i].valB = a[i].L - a[i].T;
        a[i].thF = a[i].R + a[i].T;
        a[i].thB = a[i].R - a[i].T;
    }

    int Tcnt = (int)allT.size();
    vector<vector<int>> grpF(Tcnt), grpB(Tcnt);
    vector<int> ptrF(Tcnt, 0), ptrB(Tcnt, 0);

    vector<int> seeds, exitNodes;
    seeds.reserve(M); exitNodes.reserve(M);
    for (int i = 0; i < M; ++i) {
        if (a[i].L == 0) seeds.push_back(i);
        else {
            grpF[a[i].tpos].push_back(i);
            grpB[a[i].tpos].push_back(i);
        }
        if (a[i].R == N) exitNodes.push_back(i);
    }

    if (seeds.empty() || exitNodes.empty()) {
        cout << -1 << '\n';
        return 0;
    }

    for (int t = 0; t < Tcnt; ++t) {
        sort(grpF[t].begin(), grpF[t].end(), [&](int i, int j){ return a[i].valF < a[j].valF; });
        sort(grpB[t].begin(), grpB[t].end(), [&](int i, int j){ return a[i].valB < a[j].valB; });
    }

    vector<int64> headF(Tcnt, INF), headB(Tcnt, INF);
    for (int t = 0; t < Tcnt; ++t) {
        if (!grpF[t].empty()) headF[t] = a[grpF[t][0]].valF;
        if (!grpB[t].empty()) headB[t] = a[grpB[t][0]].valB;
    }
    SegMin segF(Tcnt, headF), segB(Tcnt, headB);

    vector<int64> dist(M, INF);
    priority_queue<pair<int64,int>, vector<pair<int64,int>>, greater<pair<int64,int>>> pq;
    for (int i : seeds) { dist[i] = a[i].C; pq.push({dist[i], i}); }

    while (!pq.empty()) {
        auto [d, i] = pq.top(); pq.pop();
        if (d != dist[i]) continue;

        int tpos = a[i].tpos;

        // T_j >= T_i, activate by valF <= thF
        {
            int64 limit = a[i].thF;
            while (true) {
                int pos = segF.find_first_le(tpos, Tcnt-1, limit);
                if (pos == -1) break;
                int j = grpF[pos][ptrF[pos]++];
                int64 newHead = (ptrF[pos] < (int)grpF[pos].size()) ? a[grpF[pos][ptrF[pos]]].valF : INF;
                segF.point_set(pos, newHead);
                int64 nd = d + a[j].C;
                if (nd < dist[j]) { dist[j] = nd; pq.push({nd, j}); }
            }
        }

        // T_j <= T_i, activate by valB <= thB
        {
            int64 limit = a[i].thB;
            while (true) {
                int pos = segB.find_first_le(0, tpos, limit);
                if (pos == -1) break;
                int j = grpB[pos][ptrB[pos]++];
                int64 newHead = (ptrB[pos] < (int)grpB[pos].size()) ? a[grpB[pos][ptrB[pos]]].valB : INF;
                segB.point_set(pos, newHead);
                int64 nd = d + a[j].C;
                if (nd < dist[j]) { dist[j] = nd; pq.push({nd, j}); }
            }
        }
    }

    int64 ans = INF;
    for (int j : exitNodes) ans = min(ans, dist[j]);
    cout << (ans >= INF/2 ? -1 : ans) << '\n';
    return 0;
}
```

### 복잡도
- 전개/완화는 각 정점당 한 번씩, 세그트리/우선순위 큐 연산 `O(log M)` → 전체 `O(M log M)`
- 메모리 `O(M)`

### 참고
- JOI 공식 문제 설명(PDF): [treatment-en.pdf](https://www2.ioi-jp.org/camp/2020/2020-sp-tasks/day4/treatment-en.pdf)
- Codeforces 토론: [Japanese Olympiad in Informatics Spring Camp 2020](https://codeforces.com/blog/entry/74871) – 댓글 중 square1001의 아이디어 요지


