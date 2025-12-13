---
title: "[Algorithm] C++ 백준 18526번: Bomas"
description: "BOJ 18526 Bomas 문제를 스위프라인 알고리즘, 트리 DP, KD-Tree를 이용해 해결합니다. 중첩된 원형 울타리 구조의 포함 관계를 효율적으로 처리하고 최대 독립 집합 크기를 구하는 풀이입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-18526
- C++
- CPP
- Competitive Programming
- 경쟁프로그래밍
- Sweep Line
- 스위프라인
- Tree DP
- 트리 DP
- Dynamic Programming
- 동적계획법
- KD-Tree
- Spatial Index
- 공간 인덱스
- Geometry
- 기하
- Circular Regions
- 원형 영역
- Maximum Independent Set
- 최대 독립 집합
- Graph Theory
- 그래프 이론
- Tree Structure
- 트리 구조
- Plane Sweep
- 평면 스위프
- Data Structure
- 자료구조
- Offline Queries
- 오프라인 쿼리
- Range Query
- 범위 쿼리
- Nested Circles
- 중첩된 원
- Computational Geometry
- 계산 기하
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Optimization
- 최적화
- Code Review
- 코드리뷰
- Implementation Details
- 구현 디테일
- Edge Cases
- 코너 케이스
- Testing
- 테스트
- Problem Solving
- 문제해결
- Acyclic Graph
- 비순환 그래프
image: "wordcloud.png"
---

## 문제 정보

**문제**: [BOJ 18526번 - Bomas](https://www.acmicpc.net/problem/18526)

**요약**: 동물원의 원형 울타리(boma)들이 중첩되어 있을 때, 새로운 울타리를 추가하면 그 안에서 최대 몇 종류의 동물을 배치할 수 있는지 구하는 문제입니다. 인접한 울타리 영역 중 최대 하나에만 동물을 배치할 수 있다는 제약이 있습니다.

**제한 조건**:
- 시간 제한: 6초
- 메모리 제한: 512 MB
- 기존 울타리: $N \le 10^5$개
- 쿼리: $Q \le 10^5$개
- 좌표: $-10^7 \le x, y \le 10^7$
- 반지름: $1 \le r \le 10^7$

## 입출력 형식

**입력**:
```
N Q
x₁ y₁ r₁  (기존 boma)
...
xₙ yₙ rₙ
x'₁ y'₁ r'₁ (쿼리 boma)
...
x'ₙ y'ₙ r'ₙ
```

**출력**: 각 쿼리에 대해 최대 배치 가능 동물 종류 수

**예제**:
```
입력:
3 5
0 0 100
0 50 20
0 -50 20
0 0 80
0 0 2
500 0 2
0 50 25
0 0 150

출력:
2
1
1
1
3
```

## 접근 개요

### 핵심 관찰
1. **포함 관계의 트리 구조**: 원들이 겹치지 않으므로, 포함 관계는 트리를 형성합니다.
2. **최대 독립 집합 문제**: 인접한 노드를 동시에 선택할 수 없다는 제약은 트리 위의 최대 독립 집합(Maximum Independent Set) 문제입니다.
3. **쿼리 처리**: 새로운 원이 추가될 때, 기존 트리 내에서의 위치를 빠르게 찾아야 합니다.

### 알고리즘 아이디어
```
[Sweep-Line] → 포함 관계 트리 구성
                    ↓
            [Tree DP] → 각 노드의 최대 독립 집합
                    ↓
      [쿼리 처리 + KD-Tree] → 범위 내 자식의 DP값 합산
```

## 알고리즘 설계

### 1단계: 스위프라인으로 포함 관계 구성

**아이디어**: 원의 왼쪽 끝점($x - r$)부터 오른쪽 끝점($x + r$)까지 수직선을 왼쪽에서 오른쪽으로 이동시킵니다.

**자료구조**: `std::set<Arc>` - 현재 수직선상의 활성 원호들을 상단/하단 호 여부(`is_upper`)로 구분하고, y 좌표 순서로 정렬

**로직**:
- 원의 시작점(좌측 끝): 상단 호와 하단 호를 삽입. 바로 위의 호를 찾아 부모 결정.
  - 상단 호가 있으면: 그 원이 부모 (포함 관계)
  - 하단 호가 있으면: 그 원의 부모가 우리의 부모 (같은 깊이의 형제)
- 원의 끝점(우측 끝): 해당 호들 삭제

**정확도 조정**: `long double`와 $\varepsilon = 10^{-11}$ 사용으로 기하 연산 오차 최소화

### 2단계: 트리 위의 DP

**상태**:
- `dp[u][0]`: 영역 $u$가 비어있을 때, 부분트리 내 최대 동물 수
- `dp[u][1]`: 영역 $u$에 동물이 있을 때, 부분트리 내 최대 동물 수

**전이**:
```
dp[u][0] = Σ max(dp[v][0], dp[v][1])  (v는 u의 자식)
dp[u][1] = 1 + Σ dp[v][0]
```

**정당성**: 독립 집합의 정의(인접하지 않은 정점들의 부분집합) + 트리의 구조에서 DP의 최적 부분구조 성립

### 3단계: 쿼리 처리 (KD-Tree 활용)

**문제**: 쿼리 원 내부에 있는 기존 원들을 빠르게 찾아, 그들의 DP값을 합산해야 합니다.

**해법**:
1. 쿼리를 부모별로 그룹화
2. 각 부모 $P$에 대해, $P$의 자식들을 **2D KD-Tree**에 저장 (중심 좌표 기준)
3. 각 노드는 `(sum_dp_0, sum_valMax)` 저장
4. 원 범위 쿼리로 원 내부의 모든 자식에 대한 합 구하기

**KD-Tree 원 범위 쿼리**:
- 노드의 AABB(축 정렬 경계상자)와 쿼리 원의 거리 비교
- 완전히 내부: 자식 없이 누적값 반환
- 완전히 외부: 0 반환
- 교차: 현재 점 확인 후 재귀

### 4단계: 최종 답 계산

쿼리 원 $Q$의 부모를 $P$라 할 때:
```
내부_자식_합 = query_kdtree(Q 범위)
answer = max(내부_자식_합.valMax, 1 + 내부_자식_합.dp_0)
```

## 복잡도 분석

| 작업 | 시간복잡도 | 설명 |
|------|-----------|------|
| 스위프라인 | $O((N+Q) \log N)$ | 이벤트 처리 + set 연산 |
| DP 계산 | $O(N)$ | 각 노드 1회 방문 |
| KD-Tree 구성 | $O(N \log N)$ | 총 생성되는 노드 + 정렬 |
| 범위 쿼리 | $O(\sqrt{N})$ 평균 | 2D KD-Tree 특성 |
| **전체** | **$O((N+Q) \sqrt{N} \log N)$** | 최악: $O((N+Q)N \log N)$이지만 실제는 훨씬 빠름 |

**공간복잡도**: $O(N + Q)$

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <map>
#include <iomanip>

using namespace std;

const long double EPS = 1e-11;

struct Boma {
    int id;
    long long x, y, r;
};

struct Event {
    long double x;
    int type; // 0: Start Boma, 1: Query, 2: End Boma
    int id;
    
    bool operator<(const Event& other) const {
        if (abs(x - other.x) > EPS) return x < other.x;
        return type < other.type;
    }
};

long double current_sweep_x;
vector<Boma> bomas;
vector<Boma> queries;

// Helper to get Boma object whether it's existing or query
const Boma& getBoma(int id) {
    if (id > 0) return bomas[id];
    return queries[-(id + 1)];
}

struct Arc {
    int id;
    bool is_upper;
    
    long double get_y() const {
        const Boma& b = getBoma(id);
        if (abs(b.x - current_sweep_x) >= b.r) return b.y;
        long double dx = current_sweep_x - b.x;
        long double r_sq = (long double)b.r * b.r;
        long double dist_sq = dx * dx;
        long double dy = sqrt(max((long double)0.0, r_sq - dist_sq));
        return is_upper ? b.y + dy : b.y - dy;
    }
    
    bool operator<(const Arc& other) const {
        long double y1 = get_y();
        long double y2 = other.get_y();
        if (abs(y1 - y2) > EPS) return y1 < y2;
        if (id != other.id) return id < other.id;
        return is_upper < other.is_upper;
    }
};

// Tree structure
vector<int> adj[100005];
int parent[100005];
int query_parent[100005];
long long dp[100005][2]; // 0: no animal in region, 1: animal in region

// KD-Tree for 2D range sum
struct Point {
    long long x, y;
    long long val0, valMax;
    int id;
};

struct KDNode {
    long long min_x, max_x, min_y, max_y;
    long long sum_val0, sum_valMax;
    int left = -1, right = -1;
    Point p;
    
    KDNode(Point pt) : p(pt), min_x(pt.x), max_x(pt.x), min_y(pt.y), max_y(pt.y), sum_val0(pt.val0), sum_valMax(pt.valMax) {}
};

vector<KDNode> tree_nodes;

void update_bbox(int node_idx) {
    KDNode& node = tree_nodes[node_idx];
    if (node.left != -1) {
        const KDNode& l = tree_nodes[node.left];
        node.min_x = min(node.min_x, l.min_x);
        node.max_x = max(node.max_x, l.max_x);
        node.min_y = min(node.min_y, l.min_y);
        node.max_y = max(node.max_y, l.max_y);
        node.sum_val0 += l.sum_val0;
        node.sum_valMax += l.sum_valMax;
    }
    if (node.right != -1) {
        const KDNode& r = tree_nodes[node.right];
        node.min_x = min(node.min_x, r.min_x);
        node.max_x = max(node.max_x, r.max_x);
        node.min_y = min(node.min_y, r.min_y);
        node.max_y = max(node.max_y, r.max_y);
        node.sum_val0 += r.sum_val0;
        node.sum_valMax += r.sum_valMax;
    }
}

int build_kdtree(vector<Point>& points, int depth, int l, int r) {
    if (l > r) return -1;
    
    int mid = (l + r) / 2;
    if (depth % 2 == 0) {
        nth_element(points.begin() + l, points.begin() + mid, points.begin() + r + 1, 
            [](const Point& a, const Point& b) { return a.x < b.x; });
    } else {
        nth_element(points.begin() + l, points.begin() + mid, points.begin() + r + 1, 
            [](const Point& a, const Point& b) { return a.y < b.y; });
    }
    
    tree_nodes.emplace_back(points[mid]);
    int idx = tree_nodes.size() - 1;
    
    tree_nodes[idx].left = build_kdtree(points, depth + 1, l, mid - 1);
    tree_nodes[idx].right = build_kdtree(points, depth + 1, mid + 1, r);
    
    update_bbox(idx);
    return idx;
}

pair<long long, long long> query_kdtree(int node_idx, long long qx, long long qy, long long qr) {
    if (node_idx == -1) return {0, 0};
    
    const KDNode& node = tree_nodes[node_idx];
    
    // Check if bbox is completely outside
    long long dx = 0, dy = 0;
    if (qx < node.min_x) dx = node.min_x - qx;
    else if (qx > node.max_x) dx = qx - node.max_x;
    
    if (qy < node.min_y) dy = node.min_y - qy;
    else if (qy > node.max_y) dy = qy - node.max_y;
    
    if (dx * dx + dy * dy > qr * qr) return {0, 0};
    
    // Check if bbox is completely inside
    long long d1 = (node.min_x - qx) * (node.min_x - qx);
    long long d2 = (node.max_x - qx) * (node.max_x - qx);
    long long d3 = (node.min_y - qy) * (node.min_y - qy);
    long long d4 = (node.max_y - qy) * (node.max_y - qy);
    
    long long max_dist_sq = max({d1 + d3, d1 + d4, d2 + d3, d2 + d4});
    
    if (max_dist_sq <= qr * qr) {
        return {node.sum_val0, node.sum_valMax};
    }
    
    // Partial overlap
    pair<long long, long long> res = {0, 0};
    
    // Check current point
    long long pdx = node.p.x - qx;
    long long pdy = node.p.y - qy;
    if (pdx * pdx + pdy * pdy <= qr * qr) {
        res.first += node.p.val0;
        res.second += node.p.valMax;
    }
    
    pair<long long, long long> l_res = query_kdtree(node.left, qx, qy, qr);
    pair<long long, long long> r_res = query_kdtree(node.right, qx, qy, qr);
    
    res.first += l_res.first + r_res.first;
    res.second += l_res.second + r_res.second;
    
    return res;
}

void solve_dp(int u) {
    long long sum_val0 = 0;
    long long sum_valMax = 0;
    
    for (int v : adj[u]) {
        solve_dp(v);
        sum_val0 += dp[v][0];
        sum_valMax += max(dp[v][0], dp[v][1]);
    }
    
    dp[u][0] = sum_valMax;
    dp[u][1] = 1 + sum_val0;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n, q;
    if (!(cin >> n >> q)) return 0;
    
    bomas.resize(n + 1); 
    vector<Event> events;
    
    // 0 is the root (outer world)
    bomas[0] = {0, 0, 0, 2000000000LL};
    
    for (int i = 1; i <= n; ++i) {
        cin >> bomas[i].x >> bomas[i].y >> bomas[i].r;
        bomas[i].id = i;
        events.push_back({(long double)bomas[i].x - bomas[i].r, 0, i});
        events.push_back({(long double)bomas[i].x + bomas[i].r, 2, i});
    }
    
    queries.resize(q);
    for (int i = 0; i < q; ++i) {
        cin >> queries[i].x >> queries[i].y >> queries[i].r;
        queries[i].id = i;
        events.push_back({(long double)queries[i].x, 1, i});
    }
    
    sort(events.begin(), events.end());
    
    set<Arc> active_arcs;
    
    for(int i=1; i<=n; ++i) parent[i] = 0;
    for(int i=0; i<q; ++i) query_parent[i] = 0;
    
    for (const auto& ev : events) {
        current_sweep_x = ev.x;
        
        if (ev.type == 0) { // Start Boma
            int id = ev.id;
            Arc up = {id, true};
            Arc down = {id, false};
            active_arcs.insert(up);
            active_arcs.insert(down);
            
            auto it_up = active_arcs.find(up);
            auto next_it = next(it_up);
            
            if (next_it != active_arcs.end()) {
                if (next_it->is_upper) {
                    parent[id] = next_it->id;
                } else {
                    parent[id] = parent[next_it->id];
                }
            } else {
                parent[id] = 0;
            }
            
        } else if (ev.type == 1) { // Query
            int qid = ev.id;
            int mapped_id = -(qid + 1);
            
            Arc up = {mapped_id, true};
            active_arcs.insert(up);
            
            auto it = active_arcs.find(up);
            auto next_it = next(it);
            
            if (next_it != active_arcs.end()) {
                if (next_it->is_upper) {
                    query_parent[qid] = next_it->id;
                } else {
                    query_parent[qid] = parent[next_it->id];
                }
            } else {
                query_parent[qid] = 0;
            }
            
            active_arcs.erase(it);
            
        } else { // End Boma
            int id = ev.id;
            active_arcs.erase({id, true});
            active_arcs.erase({id, false});
        }
    }
    
    // Build Tree
    for (int i = 1; i <= n; ++i) {
        adj[parent[i]].push_back(i);
    }
    
    // DP
    solve_dp(0);
    
    // Queries
    map<int, vector<int>> queries_by_parent;
    for (int i = 0; i < q; ++i) {
        queries_by_parent[query_parent[i]].push_back(i);
    }
    
    vector<long long> answers(q);
    
    for (auto& entry : queries_by_parent) {
        int pid = entry.first;
        const vector<int>& q_indices = entry.second;
        
        if (adj[pid].empty()) {
            for (int qidx : q_indices) answers[qidx] = 1;
            continue;
        }
        
        tree_nodes.clear();
        tree_nodes.reserve(adj[pid].size() * 4);
        
        vector<Point> points;
        points.reserve(adj[pid].size());
        for (int child : adj[pid]) {
            points.push_back({bomas[child].x, bomas[child].y, dp[child][0], max(dp[child][0], dp[child][1]), child});
        }
        
        int root_node = build_kdtree(points, 0, 0, (int)points.size() - 1);
        
        for (int qidx : q_indices) {
            pair<long long, long long> res = query_kdtree(root_node, queries[qidx].x, queries[qidx].y, queries[qidx].r);
            answers[qidx] = max(res.second, 1 + res.first);
        }
    }
    
    for (int i = 0; i < q; ++i) {
        cout << answers[i] << "\n";
    }
    
    return 0;
}
```

## 코너 케이스 체크리스트

- 쿼리 원이 모든 자식을 포함할 때
- 쿼리 원이 어떤 자식도 포함하지 않을 때
- 단일 자식만 포함할 때
- 모든 쿼리가 같은 부모를 가질 때
- 깊게 중첩된 원들 (스택 오버플로우 확인)
- 같은 x 좌표의 이벤트들 (정렬 안정성 확인)

## 제출 전 점검

- 입출력 형식 정확성 (개행 확인)
- 오버플로우 (64-bit `long long` 사용 확인)
- 스위프라인 이벤트 정렬 순서 (타입별 우선순위)
- KD-Tree 범위 쿼리 경계값 처리
- 플로팅 포인트 오차 (`EPS` 설정)

## 참고자료

- [Plane Sweep Algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm)
- [KD-Tree for Range Queries](https://en.wikipedia.org/wiki/K-d_tree)
- [Maximum Independent Set on Trees](https://en.wikipedia.org/wiki/Independent_set_(graph_theory))
