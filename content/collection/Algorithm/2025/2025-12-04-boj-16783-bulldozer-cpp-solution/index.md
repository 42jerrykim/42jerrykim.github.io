---
title: "[Algorithm] C++ 백준 16783번: Bulldozer"
date: 2025-12-04
lastmod: 2025-12-04
draft: false
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16783
- C++
- Data Structures
- 자료구조
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
- Geometry
- 기하
- Math
- 수학
- Segment Tree
- 세그먼트 트리
- Sweepline
- 스위핑
- Maximum Subarray Sum
- 최대 부분 합
- Collinear Points
- 공선점
- Vector Operations
- 벡터 연산
- Cross Product
- 외적
- Parallel Lines
- 평행선
- Bulldozer
- 불도저
- Geometric Algorithm
- 기하 알고리즘
- Advanced Data Structure
- 고급 자료구조
- Editorial
- 에디토리얼
- Slope Calculation
- 기울기 계산
- Event Processing
- 이벤트 처리
- Permutation Reversal
- 순열 역순
- Problem Solving
- 문제 풀이
description: "기하학 기반의 스위핑 알고리즘과 세그먼트 트리를 결합해 두 평행선 사이 영역의 최대 이익을 구하는 고급 문제입니다. 모든 점의 기울기를 이벤트로 처리하고 공선점 처리를 통해 효율적으로 문제를 해결합니다."
image: "wordcloud.png"
---

## 문제 정보

- **링크**: [https://www.acmicpc.net/problem/16783](https://www.acmicpc.net/problem/16783)
- **출처**: JOI Open Contest 2017
- **시간 제한**: 2초
- **메모리 제한**: 512MB

## 문제 요약

JOI Kingdom의 $N$개 채굴 지점이 2차원 평면에 분포합니다. 각 지점은 금(양수 가치)이거나 돌(음수 비용)입니다. 두 개의 평행선을 선택하여 그 사이 영역의 모든 지점을 채굴할 때, **얻은 금의 총 가치 - 버린 돌의 총 비용**을 최대화해야 합니다.

## 입출력 형식

**입력:**
```
N
X₁ Y₁ W₁
X₂ Y₂ W₂
...
Xₙ Yₙ Wₙ
```

- $N$ (1 ≤ N ≤ 2000): 지점 개수
- Wᵢ > 0: i번 지점의 금 가치
- Wᵢ < 0: i번 지점의 돌 비용 (절댓값이 실제 비용)

**출력:**
```
최대 이익
```

## 예제

**입력 1:**
```
5
-5 5 -2
2 2 5
10 1 4
-2 4 -5
4 -2 2
```

**출력 1:**
```
19
```

## 접근 개요

이 문제의 핵심 관찰은 **평행선의 기울기가 정해지면, 모든 점을 기울기에 수직인 방향으로 정렬할 수 있다**는 것입니다. 이렇게 정렬된 순서에서 연속된 구간의 합 중 최댓값(Maximum Subarray Sum)을 구하는 문제로 축소됩니다.

**핵심 아이디어:**
1. 기울기 변화에 따라 점의 순서가 어떻게 바뀌는지 추적
2. 점 순서가 바뀌는 순간 = 두 점을 잇는 직선의 기울기와 평행할 때
3. 따라서 모든 가능한 점 쌍의 기울기를 이벤트로 사용
4. 각 기울기 상태에서 최대 부분 합을 세그먼트 트리로 계산

## 알고리즘 설계

### 상태 표현
- **점의 순열**: 현재 기울기 하에서 점들이 정렬된 순서
- **세그먼트 트리 노드**: 각 노드가 4가지 정보 유지
  - `lmax`: 왼쪽 경계에서 시작하는 최대 합
  - `rmax`: 오른쪽 경계에서 끝나는 최대 합
  - `sum`: 구간 전체 합
  - `max_val`: 구간 최대 부분 합 (Kadane 알고리즘 원리)

### 노드 병합 로직

두 구간을 병합할 때 최대 부분 합은 다음 3가지 중 하나:
1. 왼쪽 구간의 최대 부분 합
2. 오른쪽 구간의 최대 부분 합  
3. 왼쪽의 `rmax` + 오른쪽의 `lmax` (구간 경계를 넘는 경우)

### 스위핑 알고리즘

```
1. 초기 정렬: 점을 x 좌표(같으면 y 좌표) 오름차순 정렬
2. 이벤트 생성: 모든 점 쌍의 기울기를 (dx, dy) 형태로 저장
3. 이벤트 정렬: dy/dx 크기 순으로 정렬 (오버플로우 방지를 위해 교차곱 사용)
4. 각 기울기 그룹마다:
   a. 같은 기울기의 모든 점들을 직선 방정식별로 그룹화
      - 직선 방정식: dy·x - dx·y = C
   b. 각 직선의 점들이 현재 순열에서 차지하는 구간 [min_pos, max_pos] 찾기
   c. 해당 구간을 역순으로 뒤집기 (공선점 처리)
   d. 바뀐 점들의 값으로 세그먼트 트리 업데이트
   e. 현재 최대 부분 합 갱신
```

## 복잡도 분석

- **시간**: $O(N^2 \log N)$
  - 이벤트 생성: $O(N^2)$
  - 이벤트 정렬: $O(N^2 \log N)$
  - 스위핑 및 세그먼트 트리 업데이트: $O(N^2 \log N)$

- **공간**: $O(N)$ (세그먼트 트리, 점 배열, 순열 배열)

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point {
    long long x, y, w;
};

struct Event {
    int u, v;
    long long dx, dy;
    
    bool operator<(const Event& o) const {
        return dy * o.dx < o.dy * dx;
    }
    bool operator==(const Event& o) const {
        return dy * o.dx == o.dy * dx;
    }
};

struct Node {
    long long lmax, rmax, sum, max_val;
};

const int MAXN = 2005;
int N;
Point points[MAXN];
int pos[MAXN], perm[MAXN];
Node tree[MAXN * 4];

Node merge(const Node& L, const Node& R) {
    return {
        max(L.lmax, L.sum + R.lmax),
        max(R.rmax, R.sum + L.rmax),
        L.sum + R.sum,
        max({L.max_val, R.max_val, L.rmax + R.lmax})
    };
}

void update(int node, int s, int e, int idx, long long val) {
    if (s == e) {
        tree[node] = {max(0LL, val), max(0LL, val), val, max(0LL, val)};
        return;
    }
    int m = (s + e) / 2;
    if (idx <= m) update(node * 2, s, m, idx, val);
    else update(node * 2 + 1, m + 1, e, idx, val);
    tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> N;
    vector<Point> pts(N);
    for (int i = 0; i < N; ++i) {
        cin >> pts[i].x >> pts[i].y >> pts[i].w;
    }
    
    // 초기 정렬 (x, y 오름차순)
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        return a.x != b.x ? a.x < b.x : a.y < b.y;
    });
    
    for (int i = 0; i < N; ++i) {
        points[i] = pts[i];
        pos[i] = i;
        perm[i] = i;
        update(1, 0, N - 1, i, points[i].w);
    }
    
    // 이벤트 생성
    vector<Event> events;
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            events.push_back({i, j, points[j].x - points[i].x, 
                              points[j].y - points[i].y});
        }
    }
    
    sort(events.begin(), events.end());
    
    long long ans = tree[1].max_val;
    
    // 스위핑
    for (int i = 0; i < events.size(); ) {
        int j = i;
        while (j < events.size() && events[i] == events[j]) ++j;
        
        long long dx = events[i].dx, dy = events[i].dy;
        
        map<long long, vector<int>> lines;
        for (int k = i; k < j; ++k) {
            int u = events[k].u, v = events[k].v;
            long long val_u = dy * points[u].x - dx * points[u].y;
            lines[val_u].push_back(u);
            lines[val_u].push_back(v);
        }
        
        for (auto& [line_c, indices] : lines) {
            sort(indices.begin(), indices.end());
            indices.erase(unique(indices.begin(), indices.end()), indices.end());
            
            int min_p = N + 1, max_p = -1;
            for (int idx : indices) {
                min_p = min(min_p, pos[idx]);
                max_p = max(max_p, pos[idx]);
            }
            
            // 구간 뒤집기
            for (int l = 0; l <= (max_p - min_p) / 2; ++l) {
                int p1 = min_p + l, p2 = max_p - l;
                int id1 = perm[p1], id2 = perm[p2];
                
                swap(perm[p1], perm[p2]);
                swap(pos[id1], pos[id2]);
                
                update(1, 0, N - 1, p1, points[id2].w);
                update(1, 0, N - 1, p2, points[id1].w);
            }
        }
        
        ans = max(ans, tree[1].max_val);
        i = j;
    }
    
    cout << ans << "\n";
    return 0;
}
```

## 코너 케이스 체크리스트

- **빈 영역 선택**: 어떤 점도 포함하지 않는 평행선 영역 (이익 = 0)
- **단일 지점**: N=1일 때 해당 지점만 고려
- **모두 같은 x/y 좌표**: 수직/수평 직선만 가능
- **공선점(collinear points)**: 여러 점이 일직선 위에 있을 때 그룹 처리 필수
- **음수만 존재**: 아무것도 채굴하지 않는 것이 최적
- **좌표 범위**: $±10^9$로 오버플로우 주의 (long long 사용)

## 제출 전 점검

- [ ] 오버플로우: 교차곱 계산 시 long long 사용
- [ ] 세그먼트 트리: merge 함수의 4가지 경우 모두 처리
- [ ] 공선점: 직선 방정식으로 그룹화 (단순 min/max 사용 안 됨)
- [ ] 초기화: pos[], perm[] 배열 정확히 관리
- [ ] 기울기 비교: 정수 범위 내에서 정확한 대소비교

## 정당성 증명

**핵심 불변식**: 매 스위핑 단계에서 점의 순열은 실제 기울기 변화를 정확히 반영합니다.

1. **기울기 변화의 이산성**: 점 순서가 바뀌는 순간은 정확히 두 점을 잇는 직선의 기울기와 평행할 때만 발생
2. **공선점 처리의 정확성**: 같은 직선 위의 점들은 기울기 변화 순간에 함께 역순 배열되므로, 직선 방정식으로 그룹화하면 정확히 어떤 점들이 바뀔지 파악 가능
3. **최대 부분 합의 최적성**: 세그먼트 트리의 merge 함수가 Kadane 알고리즘의 원리를 구현하므로, 각 기울기 상태에서 현재 최적해를 올바르게 계산

따라서 모든 기울기 상태를 순회하면서 최댓값을 갱신하면, 전역 최적해를 보장합니다.
