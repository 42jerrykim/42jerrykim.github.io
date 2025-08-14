---
title: "[Algorithm] cpp 백준 11933번: 공장들"
description: "트리 위 두 회사 공장 집합 A, B 사이의 최소 거리를 구하는 문제입니다. LCA 전처리 후 질의마다 A∪B와 인접 LCA들로 버추얼 트리를 만들고, 두 번의 DP로 각 정점의 A까지/ B까지 최단거리를 구해 min(dA+dB)로 답합니다. O((|A|+|B|)logN)으로 6초 제한을 안정 통과합니다."
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
- Problem-11933
- cpp
- C++
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
- Graph
- 그래프
- Tree
- 트리
- LCA
- 최소공통조상
- Binary Lifting
- 이진 도약
- Virtual Tree
- 버추얼 트리
- Distance
- 거리
- Tree DP
- 트리 DP
- Multi-source
- 다중 소스
- Shortest Path
- 최단경로
- Weighted Tree
- 가중치 트리
- JOI
- JOI 2014
- JOI Open Contest
- Set Distance
- 집합 거리
- Preprocessing
- 전처리
- DFS
- 깊이우선탐색
- Euler Tour
- 오일러 투어
- Stack
- 스택
- Sorting
- 정렬
- Unique
- 유니크
- Mapping
- 매핑
- Rooting
- 루팅
- O(log N)
- O(N)
- O(K)
- Memory
- 메모리
- Fast IO
- 빠른 입출력
- Long Long
- 64-bit
- Validation
- 검증
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11933
- 요약: 가중치 트리에서 두 회사의 공장 위치 집합 A, B가 주어질 때, A의 임의 공장과 B의 임의 공장 사이 최단 거리의 최솟값을 각 질의마다 구합니다.

## 입력/출력
```
입력
N Q
A_i B_i D_i  (간선, i=1..N-1)
각 질의마다
S T
X_0 X_1 ... X_{S-1}
Y_0 Y_1 ... Y_{T-1}

출력
각 질의의 최소 거리
```

## 접근 개요
- 핵심 정리: 트리에서 두 집합 A, B 사이의 최소 거리는 임의 정점 u에 대해 d(u,A)+d(u,B)의 최솟값과 같습니다. 최솟값은 최단쌍 경로의 어느 정점(또는 간선 중점)에서 달성됩니다.
- 질의마다 A∪B 그리고 이들을 DFS 방문순으로 이웃한 쌍의 LCA들을 모아 버추얼 트리(압축 트리)를 구성합니다. 간선 가중치는 원 트리 거리로 설정합니다.
- 버추얼 트리에서 두 번의 DP(자식→부모, 부모→자식)로 각 정점에 대한 "가까운 A까지의 거리 dA"와 "가까운 B까지의 거리 dB"를 구해, min(dA[u]+dB[u])가 정답입니다.

## 알고리즘 설계
1) 원 트리에서 이진 도약 LCA 전처리: `depth`, `tin/tout`, `up[k]`, `distRoot`(루트까지 거리).
2) 질의 처리
   - 후보 집합 `V = A ∪ B`를 `tin` 기준 정렬·중복제거.
   - 인접한 쌍의 LCA를 모두 추가해 다시 정렬·중복제거 ⇒ 버추얼 트리 정점 집합.
   - 스택으로 부모-자식 간선을 연결하고, 간선 가중치는 `dist(u,v)`로 부여.
3) 두 소스 집합에 대해 각각 버추얼 트리에서 두 번의 DP로 최근접거리 배열 `dA`, `dB` 계산.
4) 답은 `min_u (dA[u] + dB[u])`.

## 복잡도
- 전처리: O(N log N).
- 한 질의당: 정렬/구성 O(K log K) + LCA 호출 O(K log N) + DP O(K), 여기서 K = |A ∪ B ∪ LCAs|. 전체로 충분히 빠릅니다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct FastScanner {
    static const int BUFSIZE = 1 << 20;
    int idx = 0, size_ = 0;
    char buf[BUFSIZE];
    inline char getChar() {
        if (idx >= size_) {
            size_ = (int)fread(buf, 1, BUFSIZE, stdin);
            idx = 0;
            if (size_ == 0) return EOF;
        }
        return buf[idx++];
    }
    template <class T> inline bool readInt(T &out) {
        char c = getChar();
        if (c == EOF) return false;
        while (c <= ' ') {
            c = getChar();
            if (c == EOF) return false;
        }
        T sign = 1;
        if (c == '-') { sign = -1; c = getChar(); }
        T x = 0;
        for (; c >= '0' && c <= '9'; c = getChar()) x = x * 10 + (c - '0');
        out = x * sign;
        return true;
    }
} in;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    if (!in.readInt(N)) return 0;
    in.readInt(Q);

    vector<int> head(N, -1);
    vector<int> to(2 * (N - 1));
    vector<int> nxt(2 * (N - 1));
    vector<int> w(2 * (N - 1));
    int eidx = 0;
    auto add_edge = [&](int u, int v, int ww) {
        to[eidx] = v; w[eidx] = ww; nxt[eidx] = head[u]; head[u] = eidx++;
    };

    for (int i = 0; i < N - 1; ++i) {
        int A, B, D; in.readInt(A); in.readInt(B); in.readInt(D);
        add_edge(A, B, D);
        add_edge(B, A, D);
    }

    const int LOG = 20;
    vector<array<int, 20>> up(N);
    vector<int> depth(N, 0);
    vector<int> tin(N, 0), tout(N, 0);
    vector<long long> distRoot(N, 0);

    {
        vector<int> it(N, -2);
        int timer = 0;
        int root = 0;
        up[root][0] = root;
        depth[root] = 0;
        distRoot[root] = 0;
        it[root] = head[root];

        vector<int> st;
        st.reserve(N);
        st.push_back(root);
        while (!st.empty()) {
            int u = st.back();
            if (tin[u] == 0) tin[u] = ++timer;
            if (it[u] == -1) {
                tout[u] = timer;
                st.pop_back();
                continue;
            }
            if (it[u] == -2) it[u] = head[u];
            int ei = it[u];
            it[u] = (ei == -1 ? -1 : nxt[ei]);
            if (ei == -1) continue;
            int v = to[ei];
            if (v == up[u][0] && u != root) continue;
            if (u == root && tin[v] != 0) continue;
            if (tin[v] != 0 && tout[v] != 0) continue;
            up[v][0] = u;
            depth[v] = depth[u] + 1;
            distRoot[v] = distRoot[u] + (long long)w[ei];
            it[v] = head[v];
            st.push_back(v);
        }
    }

    for (int k = 1; k < LOG; ++k) {
        for (int v = 0; v < N; ++v) {
            up[v][k] = up[ up[v][k - 1] ][k - 1];
        }
    }

    auto is_ancestor = [&](int u, int v) -> bool {
        return tin[u] <= tin[v] && tout[v] <= tout[u];
    };
    function<int(int,int)> lca = [&](int a, int b) -> int {
        if (is_ancestor(a, b)) return a;
        if (is_ancestor(b, a)) return b;
        for (int k = LOG - 1; k >= 0; --k) {
            int pa = up[a][k];
            if (!is_ancestor(pa, b)) a = pa;
        }
        return up[a][0];
    };
    auto dist = [&](int a, int b) -> long long {
        int c = lca(a, b);
        return distRoot[a] + distRoot[b] - 2LL * distRoot[c];
    };

    const long long INF = (long long)4e18;
    vector<int> node2id(N, -1);

    for (int qi = 0; qi < Q; ++qi) {
        int S, T; in.readInt(S); in.readInt(T);
        vector<int> A(S), B(T);
        for (int i = 0; i < S; ++i) in.readInt(A[i]);
        for (int i = 0; i < T; ++i) in.readInt(B[i]);

        vector<int> vs;
        vs.reserve(S + T);
        for (int x : A) vs.push_back(x);
        for (int x : B) vs.push_back(x);

        auto byTin = [&](int x, int y) { return tin[x] < tin[y]; };
        sort(vs.begin(), vs.end(), byTin);
        vs.erase(unique(vs.begin(), vs.end()), vs.end());

        int K0 = (int)vs.size();
        vs.reserve(2 * K0);
        for (int i = 0; i + 1 < K0; ++i) vs.push_back(lca(vs[i], vs[i + 1]));
        sort(vs.begin(), vs.end(), byTin);
        vs.erase(unique(vs.begin(), vs.end()), vs.end());
        int K = (int)vs.size();

        for (int i = 0; i < K; ++i) node2id[vs[i]] = i;

        vector<int> vHead(K, -1);
        vector<int> vTo(2 * max(0, K - 1));
        vector<int> vNxt(2 * max(0, K - 1));
        vector<long long> vW(2 * max(0, K - 1));
        int vidx = 0;
        auto vAdd = [&](int u, int v, long long ww) {
            vTo[vidx] = v; vW[vidx] = ww; vNxt[vidx] = vHead[u]; vHead[u] = vidx++;
        };
        if (K >= 1) {
            vector<int> st;
            st.reserve(K);
            st.push_back(vs[0]);
            for (int i = 1; i < K; ++i) {
                int u = vs[i];
                while (!st.empty() && !is_ancestor(st.back(), u)) {
                    int v = st.back(); st.pop_back();
                    int p = st.back();
                    int pid = node2id[p], vid = node2id[v];
                    long long dw = dist(p, v);
                    vAdd(pid, vid, dw);
                    vAdd(vid, pid, dw);
                }
                st.push_back(u);
            }
            while ((int)st.size() > 1) {
                int v = st.back(); st.pop_back();
                int p = st.back();
                int pid = node2id[p], vid = node2id[v];
                long long dw = dist(p, v);
                vAdd(pid, vid, dw);
                vAdd(vid, pid, dw);
            }
        }

        vector<char> isA(K, 0), isB(K, 0);
        for (int x : A) isA[node2id[x]] = 1;
        for (int x : B) isB[node2id[x]] = 1;

        vector<int> parent(K, -1);
        vector<long long> pW(K, 0);
        vector<int> preorder;
        preorder.reserve(K);
        if (K >= 1) {
            int root = node2id[vs[0]];
            parent[root] = root;
            vector<int> stk; stk.reserve(K);
            stk.push_back(root);
            while (!stk.empty()) {
                int u = stk.back(); stk.pop_back();
                preorder.push_back(u);
                for (int e = vHead[u]; e != -1; e = vNxt[e]) {
                    int v = vTo[e];
                    if (v == parent[u]) continue;
                    parent[v] = u;
                    pW[v] = vW[e];
                    stk.push_back(v);
                }
            }
        }

        auto computeNearest = [&](const vector<char>& isSrc) -> vector<long long> {
            vector<long long> dp(K, INF);
            for (int i = 0; i < K; ++i) if (isSrc[i]) dp[i] = 0;
            for (int i = (int)preorder.size() - 1; i >= 0; --i) {
                int u = preorder[i];
                for (int e = vHead[u]; e != -1; e = vNxt[e]) {
                    int v = vTo[e];
                    if (v == parent[u]) continue;
                    dp[u] = min(dp[u], dp[v] + vW[e]);
                }
            }
            for (int u : preorder) {
                for (int e = vHead[u]; e != -1; e = vNxt[e]) {
                    int v = vTo[e];
                    if (v == parent[u]) continue;
                    dp[v] = min(dp[v], dp[u] + vW[e]);
                }
            }
            return dp;
        };

        long long answer = 0;
        if (K == 0) {
            answer = 0;
        } else {
            vector<long long> dA = computeNearest(isA);
            vector<long long> dB = computeNearest(isB);
            long long best = INF;
            for (int i = 0; i < K; ++i) best = min(best, dA[i] + dB[i]);
            answer = best;
        }

        cout << answer << '\n';

        for (int u : vs) node2id[u] = -1;
    }

    return 0;
}
```

## 코너 케이스 체크리스트
- `S=1` 또는 `T=1`인 단일 원소 집합
- A, B가 서로 멀리 떨어진 경우(버추얼 트리 간선이 굵어짐)
- 별/사슬 형태 편향 트리(반복형 구현으로 재귀 한계 회피)
- 큰 가중치 합(64-bit 정수 사용)

## 제출 전 점검
- 입출력 버퍼링 및 빠른 입력 사용 여부(FastScanner)
- LCA 전처리와 `tin/tout` 기반 `is_ancestor` 일관성
- 버추얼 트리 간선 가중치는 원 트리 `dist(u,v)`로 설정되었는지
- 두 번의 DP 순서(후위→전위)와 초기값(소스=0, 나머지=INF)

## 참고자료
- Virtual Tree(Compressed Tree) 테크닉 정리
- LCA(Binary Lifting), Euler Tour 개념 정리


