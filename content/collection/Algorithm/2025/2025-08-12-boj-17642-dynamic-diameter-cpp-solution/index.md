---
title: "[Algorithm] C++ 백준 17642번 : Dynamic Diameter"
description: "가중 무향 트리에서 간선 가중치가 바뀔 때마다 지름을 출력한다. 센트로이드 분할과 지연 전파 세그트리로 업데이트를 O((log n)^2)에 처리하고, 각 센트로이드에서 두 서브트리 최댓값 합으로 전역 지름을 유지하는 정해 구현을 정리한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "17642"
- "Dynamic Diameter"
- "동적 지름"
- "Tree"
- "트리"
- "Weighted Tree"
- "가중 트리"
- "Diameter"
- "지름"
- "Update"
- "업데이트"
- "Edge Weight"
- "간선 가중치"
- "Centroid Decomposition"
- "센트로이드 분해"
- "센트로이드 분할"
- "Segment Tree"
- "Segtree"
- "세그먼트 트리"
- "세그트리"
- "Lazy Propagation"
- "지연 전파"
- "Range Add"
- "Range Max"
- "Euler Tour"
- "오일러 투어"
- "Subtree Interval"
- "서브트리 구간"
- "Multiset"
- "멀티셋"
- "Top Two"
- "최대 두 값"
- "Decomposition"
- "분할정복"
- "Tree DnC"
- "트리 분할정복"
- "CEOI"
- "CEOI 2019"
- "Olympiad"
- "올림피아드"
- "Data Structure"
- "자료구조"
- "Graph"
- "그래프"
- "Distance"
- "거리"
- "Long Long"
- "64-bit"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른입출력"
- "Implementation"
- "구현"
- "Complexity"
- "시간복잡도"
- "O(log^2 n)"
- "효율성"
- "Problem Solving"
- "PS"
- "Competitive Programming"
- "컴퓨티티브 프로그래밍"
- "Solution Code"
- "정답 코드"
- "Editorial"
- "해설"
image: "wordcloud.png"
---

문제: [BOJ 17642 - Dynamic Diameter](https://www.acmicpc.net/problem/17642)

### 아이디어 요약
- 트리의 지름은 어떤 정점 `c`(센트로이드)에 대해, `c` 기준 각 이웃 서브트리에서 `c`까지의 최장거리들 중 상위 두 개의 합으로 나타낼 수 있다.
- 센트로이드 분할을 하고, 각 센트로이드 `c`에 대해 다음을 준비한다.
  - `c`를 루트로 한 오일러 순회로 "노드→`c`까지의 거리" 배열을 만들고, 이를 대상으로 "구간 가산 + 구간 최대" 세그트리를 구축한다.
  - `c`의 각 이웃 서브트리 구간 `[L, R]`을 기록하고, 해당 구간 최대를 멀티셋에 넣어 상위 두 개 합(`bestTwoSum[c]`)을 유지한다.
- 간선 `(u, v)`의 가중치가 `Δ`만큼 변하면, 그 간선 아래 서브트리의 모든 정점에 대해 "`c`까지의 거리"가 동일하게 `±Δ` 변한다. 사전 계산한 기여 목록을 통해, 관련된 모든 센트로이드의 세그트리에 구간가산을 1회씩 적용하고, 해당 이웃 서브트리의 구간 최대만 갱신하면 된다.
- 모든 센트로이드의 `bestTwoSum` 중 최댓값이 전체 트리의 지름이므로, 전역 멀티셋의 최댓값을 매 업데이트마다 출력한다.

### C++ 풀이

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

// --------------- Segment Tree (range add, range max) ---------------
struct SegTree {
    int n;
    vector<long long> t, lz;

    SegTree() : n(0) {}
    explicit SegTree(int n_) { init(n_); }

    void init(int n_) {
        n = n_;
        t.assign(4 * n, LLONG_MIN / 4);
        lz.assign(4 * n, 0);
    }
    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) { t[p] = a[l]; return; }
        int m = (l + r) >> 1;
        build(p << 1, l, m, a);
        build(p << 1 | 1, m + 1, r, a);
        t[p] = max(t[p << 1], t[p << 1 | 1]);
    }
    void build(const vector<long long>& a) {
        init((int)a.size());
        if (n) build(1, 0, n - 1, a);
    }
    void push(int p) {
        if (lz[p] != 0) {
            for (int c : {p << 1, p << 1 | 1}) {
                t[c] += lz[p];
                lz[c] += lz[p];
            }
            lz[p] = 0;
        }
    }
    void add(int p, int l, int r, int ql, int qr, long long v) {
        if (ql > r || qr < l) return;
        if (ql <= l && r <= qr) {
            t[p] += v;
            lz[p] += v;
            return;
        }
        push(p);
        int m = (l + r) >> 1;
        add(p << 1, l, m, ql, qr, v);
        add(p << 1 | 1, m + 1, r, ql, qr, v);
        t[p] = max(t[p << 1], t[p << 1 | 1]);
    }
    void add(int l, int r, long long v) {
        if (l > r || n == 0) return;
        add(1, 0, n - 1, l, r, v);
    }
    long long query(int p, int l, int r, int ql, int qr) {
        if (ql > r || qr < l) return LLONG_MIN / 4;
        if (ql <= l && r <= qr) return t[p];
        push(p);
        int m = (l + r) >> 1;
        return max(query(p << 1, l, m, ql, qr),
                   query(p << 1 | 1, m + 1, r, ql, qr));
    }
    long long query(int l, int r) {
        if (l > r || n == 0) return LLONG_MIN / 4;
        return query(1, 0, n - 1, l, r);
    }
    long long query_all() const { return n ? t[1] : 0; }
};

// --------------- Graph and Edge ----------------
struct Edge { int u, v; long long w; };

int n, q;
long long WLim;
vector<Edge> edges; // 0..n-2
vector<vector<pair<int,int>>> g; // node -> [(to, edgeId)]

// --------------- Centroid Decomposition Data ----------------
vector<int> sz;
vector<char> dead;

struct EdgeContrib {
    int cid;       // centroid index
    int upL, upR;  // subtree interval to add on this centroid's segtree
    int neighIdx;  // which neighbor-component's max to refresh
};

struct CentroidData {
    int node;                         // real node id of this centroid
    SegTree seg;                      // distances to centroid
    vector<pair<int,int>> compRange;  // per neighbor: [L, R] interval
    vector<long long> compMax;        // per neighbor: current maximum
    multiset<long long> bag;          // multiset of compMax for top-2
    long long bestTwoSum = 0;         // sum of two largest in bag
};

vector<CentroidData> C; // indexed by cid (0..k-1)
vector<int> node2cid;   // map real node -> its centroid index (unique)
multiset<long long> globalAns; // contains bestTwoSum for each centroid

// For each edge, list of centroid-contributions to update on weight change
vector<vector<EdgeContrib>> contribs;

// --------------- Utilities ----------------
long long topTwoSum(const multiset<long long>& s) {
    if (s.empty()) return 0;
    auto it = s.end(); --it;
    long long a = max(0LL, *it);
    if (s.size() == 1) return a;
    auto it2 = it;
    --it2;
    long long b = max(0LL, *it2);
    return a + b;
}

// Compute sizes and centroid of a component (iterative, no recursion)
int get_centroid(int root) {
    vector<int> order; order.reserve(n);
    vector<int> parent(n + 1, -1);
    order.push_back(root);
    parent[root] = 0;
    for (size_t i = 0; i < order.size(); ++i) {
        int v = order[i];
        for (auto [to, eid] : g[v]) {
            if (dead[to] || to == parent[v]) continue;
            parent[to] = v;
            order.push_back(to);
        }
    }
    for (int v : order) sz[v] = 1;
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int v = order[i];
        if (parent[v]) sz[parent[v]] += sz[v];
    }
    int compSize = (int)order.size();
    int centroid = root;
    int best = INT_MAX;
    for (int v : order) {
        int mx = compSize - sz[v];
        for (auto [to, eid] : g[v]) {
            if (dead[to] || to == parent[v]) continue;
            mx = max(mx, sz[to]);
        }
        if (mx < best) { best = mx; centroid = v; }
    }
    return centroid;
}

// Build centroid data (Euler rooted at c, per-neighbor ranges, segtree, contribs)
void build_centroid_data(int c, int cid) {
    vector<pair<int,int>> neigh;
    for (auto [to, eid] : g[c]) {
        if (dead[to]) continue;
        neigh.push_back({to, eid});
    }
    int deg = (int)neigh.size();
    unordered_map<int,int> neighIndex;
    neighIndex.reserve(deg * 2);
    for (int i = 0; i < deg; ++i) neighIndex[neigh[i].first] = i;

    struct Frame { int v, p, stage, origin, eidFromParent; long long dist; int tin; };

    vector<long long> distArr; distArr.resize(0);
    int timer = 0;

    vector<Frame> st;
    st.push_back({c, 0, 0, -1, -1, 0LL, -1});

    vector<int> neighL(deg, -1), neighR(deg, -1);

    auto ensureSize = [&](int need) {
        if ((int)distArr.size() <= need) distArr.resize(need + 1, 0LL);
    };

    while (!st.empty()) {
        Frame fr = st.back(); st.pop_back();
        if (fr.stage == 0) {
            fr.stage = 1;
            fr.tin = timer++;
            ensureSize(fr.tin);
            distArr[fr.tin] = fr.dist;
            st.push_back(fr);

            if (fr.v == c) {
                for (auto [to, eid] : g[fr.v]) {
                    if (dead[to] || to == fr.p) continue;
                    st.push_back({to, fr.v, 0, to, eid, fr.dist + edges[eid].w, -1});
                }
            } else {
                for (auto [to, eid] : g[fr.v]) {
                    if (dead[to] || to == fr.p) continue;
                    st.push_back({to, fr.v, 0, fr.origin, eid, fr.dist + edges[eid].w, -1});
                }
            }

            if (fr.p == c) {
                int idx = neighIndex[fr.v];
                neighL[idx] = fr.tin;
            }
        } else {
            int tout = timer - 1;
            if (fr.p == c) {
                int idx = neighIndex[fr.v];
                neighR[idx] = tout;
            }
            if (fr.eidFromParent != -1) {
                int nidx = neighIndex[fr.origin];
                contribs[fr.eidFromParent].push_back({cid, fr.tin, tout, nidx});
            }
        }
    }

    vector<pair<int,int>> compRange(deg, {-1, -2});
    for (int i = 0; i < deg; ++i) compRange[i] = {neighL[i], neighR[i]};

    CentroidData cd;
    cd.node = c;
    cd.compRange = compRange;
    cd.seg.build(distArr);
    cd.compMax.assign(deg, 0);

    for (int i = 0; i < deg; ++i) {
        int L = cd.compRange[i].first, R = cd.compRange[i].second;
        long long v = (L <= R ? cd.seg.query(L, R) : 0LL);
        cd.compMax[i] = v;
        cd.bag.insert(v);
    }
    cd.bestTwoSum = topTwoSum(cd.bag);

    C[cid] = std::move(cd);
    globalAns.insert(C[cid].bestTwoSum);
}

// Centroid decomposition build (recursive on components)
void decompose(int root, int parentCid, int &cidCounter) {
    int c = get_centroid(root);
    int cid = cidCounter++;
    if ((int)C.size() < cidCounter) C.resize(cidCounter);
    node2cid[c] = cid;

    build_centroid_data(c, cid);

    dead[c] = 1;
    for (auto [to, eid] : g[c]) {
        if (dead[to]) continue;
        decompose(to, cid, cidCounter);
    }
}

// --------------- Updates ----------------
void apply_update_on_centroid(int cid, int neighIdx, int upL, int upR, long long delta) {
    auto itA = globalAns.find(C[cid].bestTwoSum);
    if (itA != globalAns.end()) globalAns.erase(itA);

    long long oldVal = C[cid].compMax[neighIdx];
    auto it = C[cid].bag.find(oldVal);
    if (it != C[cid].bag.end()) C[cid].bag.erase(it);

    C[cid].seg.add(upL, upR, delta);

    auto [L, R] = C[cid].compRange[neighIdx];
    long long newVal = (L <= R ? C[cid].seg.query(L, R) : 0LL);
    C[cid].compMax[neighIdx] = newVal;
    C[cid].bag.insert(newVal);

    C[cid].bestTwoSum = topTwoSum(C[cid].bag);
    globalAns.insert(C[cid].bestTwoSum);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n >> q >> WLim)) return 0;
    edges.resize(n - 1);
    g.assign(n + 1, {});
    for (int i = 0; i < n - 1; ++i) {
        int a, b; long long c;
        cin >> a >> b >> c;
        edges[i] = {a, b, c};
        g[a].push_back({b, i});
        g[b].push_back({a, i});
    }

    sz.assign(n + 1, 0);
    dead.assign(n + 1, 0);
    node2cid.assign(n + 1, -1);
    contribs.assign(n - 1, {});

    C.reserve(n);
    int cidCounter = 0;
    decompose(1, -1, cidCounter);

    long long last = 0;
    for (int i = 0; i < q; ++i) {
        long long d, e; cin >> d >> e;
        long long di = (d + last) % (n - 1);
        long long nw = (e + last) % WLim;
        int eid = (int)di;

        long long delta = nw - edges[eid].w;
        edges[eid].w = nw;

        if (delta != 0) {
            for (const auto &ct : contribs[eid]) {
                apply_update_on_centroid(ct.cid, ct.neighIdx, ct.upL, ct.upR, delta);
            }
        }

        last = (globalAns.empty() ? 0LL : *prev(globalAns.end()));
        cout << last << '\n';
    }
    return 0;
}
```

### 복잡도
- 전처리: `O(n log n)`
- 업데이트당: `O((log n)^2)` (센트로이드 깊이 × 세그트리 로그)
- 메모리: `O(n)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

### 참고
- 문제: `https://www.acmicpc.net/problem/17642`
- 출처: CEOI 2019 Day 1


