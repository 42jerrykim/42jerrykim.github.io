---
title: "[Algorithm] C++ 백준 12898번 :Selling RNA Strands"
description: "백준 12898 Selling RNA Strands 문제를 접두사·접미사 조건을 각각 트라이 서브트리 구간으로 변환하고, 오일러 투어와 펜윅 트리(Fenwick/BIT)를 이용한 2D 직사각형 카운팅으로 M개의 질의를 빠르고 안정적으로 처리하는 C++ 풀이를 정리합니다. 대용량 입력을 위한 Fast I/O와 메모리 사용 최적화 포인트, 시간·공간 복잡도 분석까지 한 번에 확인할 수 있습니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "12898"
- "Selling RNA Strands"
- "RNA"
- "문자열"
- "접두사"
- "접미사"
- "Prefix"
- "Suffix"
- "Trie"
- "트라이"
- "Euler Tour"
- "오일러 투어"
- "Fenwick Tree"
- "BIT"
- "펜윅 트리"
- "2D Range Counting"
- "직사각형 카운팅"
- "오프라인 쿼리"
- "Offline Query"
- "스위핑"
- "Sweep Line"
- "자료구조"
- "Data Structure"
- "알고리즘"
- "Algorithm"
- "빠른입출력"
- "Fast IO"
- "입출력 최적화"
- "I/O Optimization"
- "구간합"
- "Prefix Sum"
- "쿼리 처리"
- "Query Processing"
- "고급자료구조"
- "Advanced Data Structures"
- "대규모입력"
- "Large Input"
- "메모리 최적화"
- "Memory Optimization"
- "C++"
- "CPP"
- "GNU++17"
- "백준해설"
- "문제해설"
- "코딩테스트"
- "Competitive Programming"
- "ICPC"
- "문자열처리"
- "String Processing"
- "접두접미"
- "Prefix Suffix"
- "N log N"
- "선형스캔"
- "Linear Scan"
- "정답률"
image: "wordcloud.png"
---

백준 문제 [Selling RNA Strands (12898)](https://www.acmicpc.net/problem/12898)는 사전에 있는 RNA 문자열들에 대해, M개의 질의마다 접두사가 `P`이고 접미사가 `Q`인 문자열의 개수를 구하는 문제입니다. 입력은 매우 크며, 문자열은 `A`, `C`, `G`, `U` 네 글자만 사용합니다.

### 문제 요약
- 입력: 사전 크기 `N`, 질의 수 `M` (각각 최대 2,000,000)
- 문자열: 사전의 각 문자열, 그리고 질의에 주어지는 `P`, `Q`의 길이는 각각 100,000 이하
- 길이 합 제약: 사전 문자열 길이 합, 모든 `P` 길이 합, 모든 `Q` 길이 합은 각각 2,000,000 이하
- 출력: 각 질의마다 조건을 만족하는 사전 문자열의 개수 (0 이상 N 이하)

### 접근
- 접두사 조건은 접두사 트라이에서 어떤 노드의 서브트리에 해당합니다.
- 접미사 조건은 문자열을 뒤집어 접미사→접두사로 바꾸고, 접미사 트라이(뒤집힌 문자열 트라이)에서 서브트리로 표현합니다.
- 각 사전 문자열을 좌표 평면의 한 점 `(x, y)`로 대응시킵니다.
  - `x`: 접두사 트라이에서 그 단어의 종착 노드 `tin`(오일러 투어 진입 시간)
  - `y`: 접미사 트라이에서 (뒤집힌) 단어의 종착 노드 `tin`
- 질의 `(P, Q)`는 두 트라이의 서브트리 구간 곱, 즉 `x ∈ [tinP, toutP]` AND `y ∈ [tinQ, toutQ]`인 점의 개수로 환원됩니다.
- 이를 오프라인으로 처리하기 위해 `x`를 스위핑하며, `y`축에 대한 펜윅 트리(BIT)로 구간 합을 질의합니다. `x` 스위프는 이벤트 버킷(정렬 없이 인덱스로 접근)으로 구현하여 추가 정렬 비용을 없앱니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

// 빠른 입력 스캐너 (대용량 입력용)
struct FastScanner {
    static constexpr size_t BUFSIZE = 1 << 20;
    char buf[BUFSIZE];
    size_t idx = 0, size = 0;

    inline char nextChar() {
        if (idx >= size) {
            size = fread(buf, 1, BUFSIZE, stdin);
            idx = 0;
            if (size == 0) return 0;
        }
        return buf[idx++];
    }

    inline void skipBlanks() {
        char c;
        while ((c = nextChar())) {
            if (!isspace(static_cast<unsigned char>(c))) { idx--; break; }
        }
    }

    template<typename T>
    inline bool nextInt(T &out) {
        skipBlanks();
        char c = nextChar();
        if (!c) return false;
        bool neg = false;
        if (c == '-') { neg = true; c = nextChar(); }
        long long val = 0;
        while (c && isdigit(static_cast<unsigned char>(c))) {
            val = val * 10 + (c - '0');
            c = nextChar();
        }
        out = neg ? -val : val;
        if (c) idx--;
        return true;
    }

    inline bool nextToken(string &s) {
        s.clear();
        skipBlanks();
        char c = nextChar();
        if (!c) return false;
        while (c && !isspace(static_cast<unsigned char>(c))) {
            s.push_back(c);
            c = nextChar();
        }
        if (c) idx--;
        return true;
    }
};

// Fenwick Tree (BIT)
struct Fenwick {
    int n; vector<int> bit;
    Fenwick() : n(0) {}
    Fenwick(int n_) { init(n_); }
    void init(int n_) { n = n_; bit.assign(n + 1, 0); }
    inline void add(int idx, int delta) { for (; idx <= n; idx += idx & -idx) bit[idx] += delta; }
    inline int sumPrefix(int idx) const { int res = 0; for (; idx > 0; idx -= idx & -idx) res += bit[idx]; return res; }
    inline int rangeSum(int l, int r) const {
        if (l > r) return 0; if (r < 1) return 0; if (l < 1) l = 1; if (r > n) r = n;
        return sumPrefix(r) - sumPrefix(l - 1);
    }
};

// {A, C, G, U} 트라이 + 오일러 투어
struct Trie {
    vector<array<int, 4>> nxt; // 자식 인덱스
    vector<int> tin, tout;     // 오일러 진입/탈출 시간

    Trie() { nxt.reserve(2000005); nxt.push_back({-1, -1, -1, -1}); }

    static inline int idxOf(char c) {
        // A->0, C->1, G->2, U->3
        if (c == 'A') return 0; if (c == 'C') return 1; if (c == 'G') return 2; return 3;
    }

    inline int insert(const string &s) {
        int u = 0;
        for (char c : s) {
            int k = idxOf(c);
            int v = nxt[u][k];
            if (v == -1) {
                v = (int)nxt.size();
                nxt[u][k] = v;
                nxt.push_back({-1, -1, -1, -1});
            }
            u = v;
        }
        return u; // 종착 노드
    }

    inline int traverse(const string &s) const {
        int u = 0;
        for (char c : s) {
            int k = idxOf(c);
            int v = nxt[u][k];
            if (v == -1) return -1;
            u = v;
        }
        return u;
    }

    void buildEuler() {
        int total = (int)nxt.size();
        tin.assign(total, 0); tout.assign(total, 0);
        int timer = 0;
        struct Frame { int node; int child; };
        vector<Frame> st; st.reserve(total);
        st.push_back({0, -1});
        while (!st.empty()) {
            auto &f = st.back();
            if (f.child == -1) { tin[f.node] = ++timer; f.child = 0; }
            else if (f.child < 4) {
                int v = nxt[f.node][f.child++];
                if (v != -1) st.push_back({v, -1});
            } else { tout[f.node] = timer; st.pop_back(); }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    FastScanner in;
    int N, M;
    if (!in.nextInt(N)) return 0; in.nextInt(M);

    Trie pref, suff;
    vector<int> termPref(N), termSuff(N);
    string s, rs; s.reserve(100000); rs.reserve(100000);

    // 사전 입력 및 트라이 구성
    for (int i = 0; i < N; ++i) {
        in.nextToken(s);
        termPref[i] = pref.insert(s);
        rs.assign(s.rbegin(), s.rend());
        termSuff[i] = suff.insert(rs);
    }

    // 오일러 투어로 서브트리 구간 계산
    pref.buildEuler(); suff.buildEuler();
    int prefNodes = (int)pref.nxt.size();
    int suffNodes = (int)suff.nxt.size();

    // 각 단어를 (x = tinPref[term], y = tinSuff[term]) 점으로 버킷에 저장
    vector<int> pointHead(prefNodes + 1, -1);
    vector<int> pointNext(N, -1);
    vector<int> pointY(N, 0);
    for (int i = 0; i < N; ++i) {
        int x = pref.tin[termPref[i]];
        int y = suff.tin[termSuff[i]];
        pointY[i] = y;
        pointNext[i] = pointHead[x];
        pointHead[x] = i;
    }

    // x-스위핑용 이벤트 저장 (정렬 없이 버킷으로 처리)
    struct Events {
        vector<int> y1, y2, qid, sign, next, head;
    } ev;
    ev.y1.reserve(2LL * M); ev.y2.reserve(2LL * M);
    ev.qid.reserve(2LL * M); ev.sign.reserve(2LL * M);
    ev.next.reserve(2LL * M); ev.head.assign(prefNodes + 1, -1);

    auto push_event = [&](int x, int y1, int y2, int q, int sgn) {
        int id = (int)ev.y1.size();
        ev.y1.push_back(y1); ev.y2.push_back(y2);
        ev.qid.push_back(q); ev.sign.push_back(sgn);
        ev.next.push_back(ev.head[x]); ev.head[x] = id;
    };

    vector<int> ans(M, 0);
    string P, Q; P.reserve(100000); Q.reserve(100000);
    for (int qi = 0; qi < M; ++qi) {
        in.nextToken(P); in.nextToken(Q);
        int u = pref.traverse(P);
        if (u == -1) continue; // 해당 접두사를 가진 단어 없음
        rs.assign(Q.rbegin(), Q.rend());
        int v = suff.traverse(rs);
        if (v == -1) continue; // 해당 접미사를 가진 단어 없음
        int x1 = pref.tin[u], x2 = pref.tout[u];
        int y1 = suff.tin[v], y2 = suff.tout[v];
        // 누적합 기법: [1..x2] 더하고 [1..x1-1] 빼기
        push_event(x2, y1, y2, qi, +1);
        int xdown = x1 - 1; if (xdown < 0) xdown = 0;
        push_event(xdown, y1, y2, qi, -1);
    }

    // x = 0..prefNodes 스위핑, y는 Fenwick로 관리
    Fenwick bit(suffNodes);
    for (int x = 0; x <= prefNodes; ++x) {
        for (int i = pointHead[x]; i != -1; i = pointNext[i]) bit.add(pointY[i], 1);
        for (int e = ev.head[x]; e != -1; e = ev.next[e]) {
            int cnt = bit.rangeSum(ev.y1[e], ev.y2[e]);
            ans[ev.qid[e]] += ev.sign[e] * cnt;
        }
    }

    // 출력
    string out; out.reserve((size_t)M * 3);
    char buf[32];
    for (int i = 0; i < M; ++i) {
        int v = ans[i]; int p = 0;
        if (v == 0) { out.push_back('0'); out.push_back('\n'); continue; }
        if (v < 0) { out.push_back('-'); v = -v; }
        while (v > 0) { buf[p++] = char('0' + (v % 10)); v /= 10; }
        while (p--) out.push_back(buf[p]);
        out.push_back('\n');
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
```

### 복잡도
- 시간: 트라이 구성 `O(사전 길이 합)`, 오일러 투어 `O(|Trie|)`, 스위핑 동안 BIT 연산 `O((N + M) log |suffixTrie|)`
- 공간: 트라이 노드 수와 질의 수에 비례 (1536MB 제한 내 충분)

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`
