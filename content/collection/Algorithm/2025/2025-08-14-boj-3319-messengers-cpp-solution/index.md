---
title: "[Algorithm] cpp 백준 3319번: 전령들"
description: "트리의 각 도시에서 수도까지 메시지를 가장 빨리 전달하는 최소 시간을 구하는 문제입니다. 도시 i는 출발 준비 시간 S_i와 1km당 이동 시간 V_i를 가지며, 유일한 최단 경로를 따라 이동 중 중간 도시에서 다른 전령에게 넘길 수 있습니다. dp[u]를 루트까지의 거리 dist[u]를 이용해 dp[u] = S_u + V_u·dist[u] + min_{조상 x}(dp[x] − V_u·dist[x])로 정리하고, 조상 집합에 대한 직선 최소값 질의를 처리하기 위해 Li Chao Tree(선형함수 컨벡스 헐 트릭)를 트리 경로에 영속적으로 유지(퍼시스턴스)하여 각 정점에서 O(log C)에 답합니다. 64비트 정수 및 곱셈 시 128비트 캐스팅으로 오버플로를 방지합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- DP
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-3319
- cpp
- C++
- Tree
- 트리
- DP
- 동적계획법
- Tree DP
- 트리 DP
- Path DP
- 경로 DP
- Graph
- 그래프
- Distance
- 거리
- Rooted Tree
- 루트드 트리
- Ancestor
- 조상
- Convex Hull Trick
- 컨벡스 헐 트릭
- Li Chao Tree
- 라이차오 트리
- Line Container
- 선형함수 컨테이너
- Minimum Query
- 최소 질의
- Add Line
- 직선 추가
- Persistent
- 퍼시스턴스
- Rollback
- 롤백
- Segment Tree
- 세그먼트 트리
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Invariant
- 불변식
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
- CEOI
- CEOI 2009
- Messengers
- 전령들
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3319
- 요약: `N`개 도시가 트리로 연결. 도시 `i(≥2)`에 전령이 있어 출발 준비시간 `S_i`, 1km당 이동시간 `V_i`를 가진다. 공격 도시에서 수도(정점 1)로 가는 유일한 최단 경로를 따라 이동하며, 경로상의 임의의 도시에서 해당 도시의 전령에게 넘길 수 있다. 각 도시에서 수도까지의 최소 시간을 구하라.

### 제한/스펙
- `3 ≤ N ≤ 100000`
- 간선 길이 ≤ `10000`
- `0 ≤ S_i ≤ 1e9`, `1 ≤ V_i ≤ 1e9`
- 시간 제한 1초, 메모리 128MB

## 입출력 예시

예제 입력 1
```
5
1 2 20
2 3 12
2 4 1
4 5 3
26 9
1 10
500 2
2 30
```

예제 출력 1
```
206 321 542 328
```

## 접근 개요(아이디어 스케치)
- 루트(수도) `1`에서의 거리를 `dist[u]`라 하자. 어떤 도시 `u`에서 시작해 경로상의 조상 `x`로 바통을 넘긴다면, `u`에서 `x`까지 현재 전령이 이동한 시간과 이후 `x`의 전령이 수도까지 가는 최소시간이 합쳐진다.
- 점화식: `dp[u] = min_{조상 x} (S_u + V_u·(dist[u] − dist[x]) + dp[x]) = S_u + V_u·dist[u] + min_{조상 x} (dp[x] − V_u·dist[x])`.
- 조상 `x`에 대해 `y = m·X + b` 꼴로 선을 정의하면, `m = −dist[x]`, `b = dp[x]`. 질의는 `X = V_u`에서의 최소값. 즉, 루트→u 경로 조상들의 직선 집합에서 `x = V_u`에 대한 최솟값 질의.
- 경로마다 조상 집합이 다르므로, DFS로 내려가며 라인을 추가/제거해야 한다. Li Chao Tree를 영속적으로 유지(노드 복제)하면, 각 정점에 대응하는 버전에서 `O(log C)`로 질의 가능(`C ≈ 1e9`).

## 알고리즘 설계
- 전처리: `dist[u]` (루트 1에서의 거리), 부모 `par[u]` 계산.
- Li Chao Tree(정수 좌표, 구간 `[0, 1e9]`)를 노드 복제 방식으로 퍼시스턴트하게 구현.
- DFS 스택/재귀로 내려가며 현재 버전의 Li Chao에 다음을 수행:
  - 루트(1): 직선 `y = 0` 삽입(`m = 0`, `b = 0`).
  - 그 외 `u`: `best = query(V_u)`, `dp[u] = S_u + V_u·dist[u] + best`, 이후 `y = −dist[u]·x + dp[u]` 삽입해 자식으로 전달할 새 버전 생성.
- 출력: `dp[2], dp[3], …, dp[N]`.

## 복잡도
- 시간: 각 정점당 `insert + query`가 `O(log 1e9)` → 전체 `O(N log 1e9)`.
- 공간: Li Chao 노드 복제 수가 `O(N log 1e9)` 내에서 상수 요인 작게 동작(실제 분기된 곳만 생성).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Line {
    int64 m, b; // y = m*x + b
};
struct Node {
    Line ln; // best line on this segment
    int left, right; // children indices
};

static const int64 X_MIN = 0;
static const int64 X_MAX = 1000000000LL; // V_i in [1..1e9]
static const int64 INF = (1LL << 62);

inline int64 eval(const Line &ln, int64 x) {
    return (int64)((__int128)ln.m * x + ln.b);
}

vector<Node> lichao; // 0 is null

inline int clone_node(int idx) {
    if (idx == 0) {
        lichao.push_back(Node{{0, INF}, 0, 0});
        return (int)lichao.size() - 1;
    }
    lichao.push_back(lichao[idx]);
    return (int)lichao.size() - 1;
}

int insert_line(int idx, int64 l, int64 r, Line nw) {
    int cur = clone_node(idx);
    Line lo = lichao[cur].ln, hi = nw;
    int64 mid = (l + r) >> 1;

    if (eval(lo, mid) > eval(hi, mid)) swap(lo, hi);
    lichao[cur].ln = lo;

    if (l == r) return cur;

    if (eval(lo, l) > eval(hi, l)) {
        lichao[cur].left = insert_line(lichao[cur].left, l, mid, hi);
    } else if (eval(lo, r) > eval(hi, r)) {
        lichao[cur].right = insert_line(lichao[cur].right, mid + 1, r, hi);
    }
    return cur;
}

int64 query_min(int idx, int64 l, int64 r, int64 x) {
    if (idx == 0) return INF;
    int64 res = eval(lichao[idx].ln, x);
    if (l == r) return res;
    int64 mid = (l + r) >> 1;
    if (x <= mid) return min(res, query_min(lichao[idx].left, l, mid, x));
    return min(res, query_min(lichao[idx].right, mid + 1, r, x));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<vector<pair<int,int>>> g(N + 1);
    for (int i = 0; i < N - 1; ++i) {
        int u, v, d;
        cin >> u >> v >> d;
        g[u].push_back({v, d});
        g[v].push_back({u, d});
    }

    vector<int64> S(N + 1, 0), V(N + 1, 0);
    for (int i = 2; i <= N; ++i) {
        int64 s, v;
        cin >> s >> v;
        S[i] = s; V[i] = v;
    }

    // Compute distances from root (1)
    vector<int64> dist(N + 1, 0);
    vector<int> par(N + 1, 0);
    par[1] = -1;
    vector<int> stk;
    stk.push_back(1);
    while (!stk.empty()) {
        int u = stk.back(); stk.pop_back();
        for (auto [v, w] : g[u]) if (v != par[u]) {
            par[v] = u;
            dist[v] = dist[u] + w;
            stk.push_back(v);
        }
    }

    lichao.reserve(N * 32 + 5);
    lichao.push_back(Node{{0, INF}, 0, 0}); // index 0: null

    vector<int64> dp(N + 1, 0);

    struct Frame { int u, p, root; };
    vector<Frame> dfs;
    dfs.push_back({1, 0, 0}); // start with empty structure

    while (!dfs.empty()) {
        auto [u, p, root] = dfs.back();
        dfs.pop_back();

        int nextRoot = root;
        if (u == 1) {
            dp[1] = 0;
            // Insert line for root: m = -D[1] = 0, b = dp[1] = 0
            nextRoot = insert_line(nextRoot, X_MIN, X_MAX, Line{0, 0});
        } else {
            int64 best = query_min(root, X_MIN, X_MAX, V[u]); // min_x (dp[x] - V[u]*D[x])
            dp[u] = S[u] + (int64)((__int128)V[u] * dist[u]) + best;
            // Make current node available to descendants: y = -D[u] * x + dp[u]
            nextRoot = insert_line(root, X_MIN, X_MAX, Line{-dist[u], dp[u]});
        }

        for (auto [v, w] : g[u]) if (v != p) {
            dfs.push_back({v, u, nextRoot});
        }
    }

    for (int i = 2; i <= N; ++i) {
        if (i > 2) cout << ' ';
        cout << dp[i];
    }
    cout << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `S_i = 0`이 다수인 경우: 초기 대기시간 0이라도 `V_i·dist[u]`와 조상 선택이 핵심.
- 매우 긴 경로(거리 합 최대 약 `1e9`)와 큰 `V_i(≤1e9)` 조합: 곱은 최대 `1e18` → 64비트, 곱셈은 128비트 캐스팅으로 안전.
- 모든 라인을 추가해도 질의 `x`가 동일한 값(중복 `V_i`)인 케이스: Li Chao는 동일 `x`에서도 최소값을 보장.
- 노드 수 최대(`1e5`): 비재귀 DFS 또는 재귀 한도 상향 필요. 본 구현은 스택 기반.

## 제출 전 점검
- 점화식 `dp[u] = S_u + V_u·dist[u] + min(dp[x] − V_u·dist[x])` 구현 확인.
- Li Chao Tree 좌표 구간 `[0, 1e9]` 설정, 질의/삽입 모두 64/128비트 안전성 점검.
- 출력 형식: 한 줄, `dp[2] … dp[N]`, 공백 구분.
- 빠른 입출력 설정 여부(`sync_with_stdio(false)`, `tie(nullptr)`).

## 참고자료/유사문제
- CEOI 2009 Messengers(전령들) 공식 문제.
- Li Chao Tree를 이용한 직선 최소 질의, 트리 경로 DP 응용.


