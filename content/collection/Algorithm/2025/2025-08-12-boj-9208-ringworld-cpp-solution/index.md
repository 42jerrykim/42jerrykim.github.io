---
title: "[BOJ] Ringworld (9208) - C++ 풀이"
description: "DSU로 모노톤 후보를 유지해 Hall 조건의 최대값만 추적하여 세그트리 없이 BOJ 9208 링월드를 O(n log n)으로 해결합니다. 원형 구간의 2배 선형화와 좌표압축을 결합해 TLE를 방지하고, 구현이 간결하며 안정적인 성능을 보장합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "9208"
- "Ringworld"
- "링월드"
- "ICPC"
- "GCPC"
- "GCPC 2013"
- "German Collegiate Programming Contest"
- "Interval"
- "Intervals"
- "원형 구간"
- "Circular"
- "Circular Interval"
- "좌표압축"
- "Coordinate Compression"
- "DSU"
- "Disjoint Set"
- "Union-Find"
- "모노톤"
- "Monotone"
- "스위핑"
- "Sweep Line"
- "그리디"
- "Greedy"
- "세그먼트 트리"
- "Segment Tree"
- "Lazy Propagation"
- "시간초과"
- "TLE"
- "최적화"
- "Optimization"
- "정렬"
- "Sorting"
- "이분탐색"
- "Binary Search"
- "lower_bound"
- "Hall"
- "Hall's Theorem"
- "매칭"
- "Matching"
- "할의 정리"
- "원형배열"
- "Circular Array"
- "Arc"
- "Range"
- "좌표"
- "Coordinates"
- "C++"
- "CPP"
- "GNU++17"
- "빠른입출력"
- "Fast IO"
- "구현"
- "Implementation"
- "자료구조"
- "Data Structure"
- "알고리즘"
- "Algorithm"
- "코딩테스트"
- "Competitive Programming"
- "정답률"
- "문제해설"
- "Editorial"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 9208 - 링월드](https://www.acmicpc.net/problem/9208)

### 아이디어 요약
- 원형 도시 구간을 길이 2배로 선형화하여 모든 구간을 직선 상의 구간으로 바꿉니다.
- `x`(시작), `y`(끝) 좌표를 좌표압축하고, 구간을 `y` 오름차순·`x` 내림차순으로 정렬해 한 번에 스캔합니다.
- 세그트리로 `k ≤ x` 전체에 +1을 누적하면 느리므로, 후보 `k`의 값 `val(k) = coord[k] + cnt[k]`의 최댓값만 유지합니다.
- DSU(Union-Find) 두 개로 후보를 모노톤하게 관리합니다. 지배당하는 오른쪽 후보는 "건너뛰기 DSU"로 제거하고, 왼쪽 루트에 누적합을 합칩니다.
- 각 구간 끝 `y`에서 Hall 조건 `max_k (k + #starts_in_[k, y]) ≤ y + 1`을 즉시 점검하면 가능/불가능을 판정할 수 있습니다.
- 시간복잡도: 좌표압축 정렬 `O(n log n)`, 스캔 중 DSU 합치기 암ortized 거의 선형.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

struct DisjointSkip {
    vector<int> parent;
    DisjointSkip() {}
    explicit DisjointSkip(int n) : parent(n) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
    void skip_to(int x, int y) { parent[x] = y; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        long long m; int n;
        cin >> m >> n;

        vector<pair<long long,long long>> arcs;
        arcs.reserve(2LL * n);

        for (int i = 0; i < n; ++i) {
            long long x, y; cin >> x >> y;
            if (x <= y) {
                arcs.emplace_back(x, y);
                arcs.emplace_back(x + m, y + m);
            } else {
                arcs.emplace_back(x, y + m);
            }
        }

        if ((long long)n > m) { cout << "NO\n"; continue; }

        // 좌표압축 (실제 좌표값 보존용 배열)
        vector<long long> coords; coords.reserve(2 * arcs.size() + 1);
        coords.push_back(-1); // 경계 안정화를 위한 센티넬
        for (auto &p : arcs) { coords.push_back(p.first); coords.push_back(p.second); }
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());

        auto get_idx = [&](long long v) -> int {
            return int(lower_bound(coords.begin(), coords.end(), v) - coords.begin());
        };

        // 압축된 인덱스로 치환 후 y 오름차순, x 내림차순 정렬
        vector<pair<int,int>> segs; segs.reserve(arcs.size());
        for (auto &p : arcs) segs.emplace_back(get_idx(p.first), get_idx(p.second));
        sort(segs.begin(), segs.end(), [&](const auto& a, const auto& b) {
            if (a.second != b.second) return a.second < b.second;
            return a.first > b.first;
        });

        const int S = (int)coords.size();
        DisjointSkip leftRoot(S + 2), rightNext(S + 2);
        vector<long long> addCount(S + 2, 0);

        auto find_left = [&](int x) { return leftRoot.find(x); };
        auto find_right = [&](int x) { return rightNext.find(x); };

        bool ok = true;
        for (const auto& rg : segs) {
            int a = rg.first, b = rg.second;

            int rootA = find_left(a);
            addCount[rootA] += 1; // 효과적으로 "k ≤ a"에 +1이 들어가도록 후보를 루트에 모읍니다

            // 오른쪽 후보가 지배되면 병합 (nxt ≤ b+1까지만 의미 있음)
            while (true) {
                int nxt = find_right(rootA + 1);
                if (nxt > b + 1) break;
                int nxt2 = find_right(nxt + 1);
                if (coords[rootA] + addCount[rootA] >= coords[nxt]) {
                    leftRoot.skip_to(nxt, rootA);
                    rightNext.skip_to(nxt, nxt2);
                    addCount[rootA] += addCount[nxt];
                } else {
                    break;
                }
            }

            // Hall 검사: max_k (k + cnt[k]) ≤ y + 1
            int rb = find_left(b);
            if (coords[rb] + addCount[rb] > coords[b] + 1) {
                ok = false;
                break;
            }
        }

        cout << (ok ? "YES\n" : "NO\n");
    }
    return 0;
}
```

### 복잡도
- 정렬·좌표압축: `O(n log n)`
- 스캔·DSU 합치기: 거의 선형(아몰티즈드), 전체 `O(n log n)` 내

### 참고
- 문제: [BOJ 9208 - 링월드](https://www.acmicpc.net/problem/9208)
- 해설(모노톤+DSU 아이디어): [돌이 코딩하는 방 - BOJ 9208](https://stonejjun.tistory.com/199)
- 관련 글: [백준 9208 풀이 - qwerasdfzxcl](https://qwerasdfzxcl.tistory.com/11)


