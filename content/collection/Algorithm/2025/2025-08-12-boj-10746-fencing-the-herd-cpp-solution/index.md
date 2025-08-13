---
title: "[Algorithm] C++ 백준 10746번 : Fencing the Herd"
description: "동적으로 소가 추가되는 좌표 집합에 대해 직선 울타리 Ax+By=C가 모든 소를 한쪽 반평면에 두는지 판별한다. 시간 세그먼트 트리+노드별 볼록껍질로 지지함수(min/max 내적)를 빠르게 구해 O(log^2 N)로 YES/NO를 처리한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
- "Computational Geometry"
tags:
- "BOJ"
- "백준"
- "USACO"
- "Gold"
- "Fencing the Herd"
- "10746"
- "Algorithm"
- "알고리즘"
- "Computational Geometry"
- "기하"
- "Convex Hull"
- "볼록껍질"
- "Support Function"
- "지지함수"
- "Dot Product"
- "내적"
- "Half-plane"
- "반평면"
- "Line Query"
- "직선 질의"
- "Segment Tree"
- "세그먼트 트리"
- "Offline Query"
- "오프라인 질의"
- "Dynamic Set"
- "동적 집합"
- "Range Aggregation"
- "구간 집계"
- "Max Dot"
- "Min Dot"
- "__int128"
- "정수 오버플로우 방지"
- "CCW"
- "Cross Product"
- "외적"
- "Andrew Monotone Chain"
- "모노톤 체인"
- "Time Decomposition"
- "시간 분할"
- "Data Structure"
- "자료구조"
- "Geometry Trick"
- "기하 트릭"
- "Queries"
- "질의 처리"
- "Fast IO"
- "빠른 입출력"
- "C++"
- "Cpp"
- "GCC"
- "Optimization"
- "최적화"
- "Numerical Stability"
- "정확한 계산"
- "Baekjoon"
- "Problem Solving"
- "PS"
image: "wordcloud.png"
---

### 문제 요약
- 소들의 좌표가 주어지고, 이후 두 종류의 연산을 처리한다.
  - `1 x y`: 소를 좌표 `(x, y)` 에 추가.
  - `2 A B C`: 직선 `A x + B y = C` 를 울타리로 사용할 수 있는지 질의.
- 사용 가능 조건: 모든 소가 직선의 한쪽 반평면에 있어야 하며, 직선 위에 있는 소가 하나라도 있으면 불가.

### 핵심 아이디어
- 한 시점의 소 집합 `S` 에 대해, 벡터 `v = (A, B)` 를 잡고 모든 점에 대한 내적 `v·p` 의 최소/최대값을 `m = min v·p`, `M = max v·p` 라 하자.
  - `C < m` 또는 `C > M` 이면 모든 점이 한쪽에 있으므로 "YES".
  - 그 외(특히 `m ≤ C ≤ M`) 는 어떤 점은 직선 위 또는 양쪽으로 분리되므로 "NO".
- 동적 추가 때문에 시점별로 활성 집합이 달라진다. 이를 위해 "시간에 대한 세그먼트 트리"를 만들고, 각 노드에 해당 구간에만 등장하는 점들의 볼록껍질을 저장한다.
  - 질의 시(root→leaf 경로의 O(log Q) 노드 방문)마다 해당 노드 볼록껍질에서 `max v·p` 와 `min v·p` 를 얻어 전역 범위를 갱신한다.
  - 볼록다각형의 지지함수는 법선(노멀) 각 정렬을 이용해 이진탐색 O(log N) 으로 구한다.

### 시간/공간 복잡도
- 빌드: 각 점이 O(log Q) 노드에 들어가고, 노드마다 볼록껍질 구성 `O(K log K)`.
- 질의: 경로 길이 `O(log Q)` × 각 노드 지지함수 `O(log K)` → 전체 `O(log^2 N)` 수준.

### 구현 노트
- 큰 범위 정수(최대 1e18) 연산을 위해 `__int128`을 사용해 안전하게 내적/외적을 계산.
- 직선 위 점이 존재하면 반드시 "NO" 가 되도록 `C` 가 `[min, max]` 내부(경계 포함)면 불가로 처리.
- 빠른 입출력(`ios::sync_with_stdio(false); cin.tie(nullptr);`).

### C++ 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point { long long x, y; };
using i128 = __int128_t;

static inline i128 dot_ll(const Point& p, long long A, long long B) {
    return (i128)A * p.x + (i128)B * p.y;
}
static inline i128 cross_ll(long long ax, long long ay, long long bx, long long by) {
    return (i128)ax * by - (i128)ay * bx;
}

static inline bool angleHalf(const pair<long long,long long>& v) {
    return (v.second > 0) || (v.second == 0 && v.first >= 0);
}
static inline bool angleLess(const pair<long long,long long>& a, const pair<long long,long long>& b) {
    bool ha = angleHalf(a), hb = angleHalf(b);
    if (ha != hb) return ha > hb;
    i128 cr = cross_ll(a.first, a.second, b.first, b.second);
    if (cr != 0) return cr > 0;
    __int128 la = (i128)a.first * a.first + (i128)a.second * a.second;
    __int128 lb = (i128)b.first * b.first + (i128)b.second * b.second;
    return la < lb;
}

struct Node {
    vector<Point> pts;
    vector<Point> hull;
    vector<pair<long long,long long>> normals; // outward normals of edges, angle-sorted
};

struct SegTree {
    int n; vector<Node> st;
    SegTree(int n_) : n(n_), st(4*n_+5) {}

    void addPoint(int idx, int l, int r, int ql, int qr, const Point& p) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { st[idx].pts.push_back(p); return; }
        int m = (l + r) >> 1;
        addPoint(idx<<1, l, m, ql, qr, p);
        addPoint(idx<<1|1, m+1, r, ql, qr, p);
    }

    static vector<Point> convexHull(vector<Point> pts) {
        sort(pts.begin(), pts.end(), [](const Point& a, const Point& b){
            if (a.x != b.x) return a.x < b.x; return a.y < b.y;
        });
        pts.erase(unique(pts.begin(), pts.end(), [](const Point& a, const Point& b){
            return a.x == b.x && a.y == b.y;
        }), pts.end());
        if (pts.size() <= 1) return pts;
        vector<Point> lo, up;
        for (auto& c : pts) {
            while (lo.size() >= 2) {
                Point a = lo[lo.size()-2], b = lo.back();
                if (cross_ll(b.x - a.x, b.y - a.y, c.x - b.x, c.y - b.y) > 0) break;
                lo.pop_back();
            }
            lo.push_back(c);
        }
        for (int i = (int)pts.size()-1; i >= 0; --i) {
            auto& c = pts[i];
            while (up.size() >= 2) {
                Point a = up[up.size()-2], b = up.back();
                if (cross_ll(b.x - a.x, b.y - a.y, c.x - b.x, c.y - b.y) > 0) break;
                up.pop_back();
            }
            up.push_back(c);
        }
        lo.pop_back(); up.pop_back();
        vector<Point> hull = lo; hull.insert(hull.end(), up.begin(), up.end());
        if (hull.empty() && !pts.empty()) hull.push_back(pts[0]);
        return hull;
    }

    static void prepareNode(Node& node) {
        if (node.pts.empty()) return;
        node.hull = convexHull(node.pts);
        node.pts.clear(); node.pts.shrink_to_fit();
        int h = (int)node.hull.size();
        node.normals.clear();
        if (h >= 2) {
            node.normals.resize(h);
            for (int i = 0; i < h; ++i) {
                int j = (i + 1) % h;
                long long ex = node.hull[j].x - node.hull[i].x;
                long long ey = node.hull[j].y - node.hull[i].y;
                node.normals[i] = {ey, -ex};
            }
            int minIdx = 0;
            for (int i = 1; i < h; ++i) if (angleLess(node.normals[i], node.normals[minIdx])) minIdx = i;
            auto rotN = node.normals, rotH = node.hull;
            for (int i = 0; i < h; ++i) { rotN[i] = node.normals[(minIdx+i)%h]; rotH[i] = node.hull[(minIdx+i)%h]; }
            node.normals.swap(rotN); node.hull.swap(rotH);
        }
    }

    void build(int idx, int l, int r) {
        if (!st[idx].pts.empty()) prepareNode(st[idx]);
        if (l == r) return;
        int m = (l + r) >> 1;
        build(idx<<1, l, m); build(idx<<1|1, m+1, r);
    }

    static i128 maxDotOnHull(const Node& node, long long A, long long B) {
        const auto& H = node.hull; int h = (int)H.size();
        if (h == 0) return -(((i128)1) << 120);
        if (h == 1) return dot_ll(H[0], A, B);
        const auto& N = node.normals; pair<long long,long long> v = {A, B};
        int idx = int(lower_bound(N.begin(), N.end(), v, [](const auto& a, const auto& b){ return angleLess(a,b); }) - N.begin());
        if (idx == h) idx = 0;
        return dot_ll(H[idx], A, B);
    }

    void queryPath(int idx, int l, int r, int pos, long long A, long long B, i128& gMin, i128& gMax) const {
        const Node& nd = st[idx];
        if (!nd.hull.empty()) {
            i128 mx = maxDotOnHull(nd, A, B);
            i128 mn = -maxDotOnHull(nd, -A, -B);
            gMax = max(gMax, mx); gMin = min(gMin, mn);
        }
        if (l == r) return;
        int m = (l + r) >> 1;
        if (pos <= m) queryPath(idx<<1, l, m, pos, A, B, gMin, gMax);
        else queryPath(idx<<1|1, m+1, r, pos, A, B, gMin, gMax);
    }
};

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N, Q; if (!(cin >> N >> Q)) return 0;
    vector<Point> initial(N); for (int i = 0; i < N; ++i) cin >> initial[i].x >> initial[i].y;
    struct Op { int type; long long a,b,c; };
    vector<Op> ops(Q+1);
    for (int t = 1; t <= Q; ++t) {
        int tp; cin >> tp; ops[t].type = tp;
        if (tp == 1) { cin >> ops[t].a >> ops[t].b; ops[t].c = 0; }
        else { cin >> ops[t].a >> ops[t].b >> ops[t].c; }
    }

    SegTree seg(Q);
    for (const auto& p : initial) seg.addPoint(1, 1, Q, 1, Q, p);
    for (int t = 1; t <= Q; ++t) if (ops[t].type == 1 && t < Q) seg.addPoint(1, 1, Q, t+1, Q, Point{ops[t].a, ops[t].b});
    seg.build(1, 1, Q);

    const i128 INF = ((i128)1) << 120; ostringstream out;
    for (int t = 1; t <= Q; ++t) if (ops[t].type == 2) {
        long long A = ops[t].a, B = ops[t].b; i128 C = (i128)ops[t].c;
        i128 gMin = INF, gMax = -INF; seg.queryPath(1, 1, Q, t, A, B, gMin, gMax);
        bool ok = (C < gMin) || (C > gMax); out << (ok ? "YES\n" : "NO\n");
    }
    cout << out.str();
    return 0;
}
```

### 예시
문제 예시 입력에 대해 위 코드의 출력은 다음과 같이 나옵니다.

```
YES
NO
NO
```

### 마무리
- 핵심은 "모든 점의 내적 범위와 C 의 위치 관계"입니다. 동적 추가는 시간 세그먼트 트리로 깔끔히 처리할 수 있습니다.


