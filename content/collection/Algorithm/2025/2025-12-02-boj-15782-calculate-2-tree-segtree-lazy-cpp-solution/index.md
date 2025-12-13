---
title: "[Algorithm] C++ 백준 15782번: Calculate! 2"
description: "트리 구조에서 부분트리 XOR 쿼리 및 범위 업데이트를 효율적으로 처리하는 문제입니다. Euler Tour Technique으로 트리를 일렬화하고 Lazy Propagation 세그먼트 트리로 O((N+M)logN)에 해결합니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- Tree
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-15782
- cpp
- C++
- Tree
- 트리
- Segment Tree
- 세그먼트 트리
- Lazy Propagation
- 레이지 프로파게이션
- Euler Tour
- 오일러 투어
- XOR Query
- 비트연산
- Range Update
- 범위 업데이트
- Range Query
- 범위 쿼리
- Subtree Query
- 부분트리 쿼리
- DFS
- 깊이 우선 탐색
- Data Structures
- 자료구조
- Tree Flattening
- 트리 평탄화
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(N log N)
- Competitive Programming
- 경쟁프로그래밍
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Testing
- 테스트
- Fast I/O
- 빠른 입출력
- Complexity Analysis
- 복잡도 분석
- Bitwise XOR
- XOR 연산
- In-Order Traversal
- 중위 탐색
- Flatten Array
- 배열 평탄화
- Query Processing
- 쿼리 처리
- Constraint Handling
- 제약 처리
- Algorithm Design
- 알고리즘 설계
- Logic Gates
- 논리 연산
- Optimization Technique
- 최적화 기법
image: "wordcloud.png"
---

## 문제 정보

- **문제**: https://www.acmicpc.net/problem/15782
- **요약**: N개 정점의 트리(루트 1)가 주어지고, 각 정점이 가중치를 가집니다. M개의 쿼리 중 Type 1은 정점 x의 부분트리 전체 가중치의 XOR 합을 구하고, Type 2는 정점 x의 부분트리의 모든 가중치에 y를 XOR합니다.
- **제한**: 시간 1초, 메모리 512MB, 3 ≤ N ≤ 100,000, 3 ≤ M ≤ 500,000, 0 ≤ weight, y ≤ 10,000

## 입출력 형식/예제

```text
예제 입력 1:
5 4
1 2
2 3
2 4
3 5
1 2 3 4 5
1 1
2 3 100
2 1 94
1 4

예제 출력 1:
1
90
```

**예제 설명**:
- 초기 트리: 1-2-3-5, 2-4 구조, 가중치 [1,2,3,4,5]
- 쿼리 1: 노드 1의 부분트리(전체) XOR = 1^2^3^4^5 = 1
- 쿼리 2: 노드 3의 부분트리에 100 XOR → 가중치 변경
- 쿼리 4: 노드 4의 부분트리(자신뿐) = 4

## 접근 개요

**핵심 관찰**:
1. 부분트리는 연결된 구간으로, DFS 탐색 순서에서 연속된 구간을 이룹니다.
2. XOR 연산의 특성: 홀수 개 원소에만 값이 영향을 줍니다. (a ⊕ a = 0)
3. 트리를 평탄화하면 일렬 배열로 변환되어 세그먼트 트리 사용 가능합니다.

**선택 근거**:
- Naive 부분트리 순회: O(M·N) → TLE
- Euler Tour + Lazy SegTree: O((N+M)log N) → AC

## 알고리즘 설계

### 1단계: Euler Tour로 트리 평탄화

DFS 탐색을 통해 각 노드의 진입/진출 시간을 기록합니다.

- `in_time[u]`: 노드 u 방문 시 시각
- `out_time[u]`: 노드 u의 부분트리 탐색 완료 시각
- 부분트리 = 연속 구간 `[in_time[u], out_time[u]]`

```cpp
void dfs(int u, int parent) {
    in_time[u] = ++timer;
    euler_tour[timer] = u;
    for (int v : adj[u]) {
        if (v != parent) {
            dfs(v, u);
        }
    }
    out_time[u] = timer;
}
```

### 2단계: Lazy Propagation 세그먼트 트리

**핵심 문제**: XOR은 합산이 아닌 토글이므로, 원소 개수가 홀수/짝수인지가 중요합니다.

```cpp
void push(int node, int start, int end) {
    if (lazy[node] != 0) {
        // XOR 적용: 홀수 개 원소만 영향
        if ((end - start + 1) % 2 == 1) {
            tree[node] ^= lazy[node];
        }
        if (start != end) {
            lazy[node * 2] ^= lazy[node];
            lazy[node * 2 + 1] ^= lazy[node];
        }
        lazy[node] = 0;
    }
}
```

**이유**: 
- 짝수 개 원소: `a ⊕ a = 0`이므로 XOR이 상쇄됨
- 홀수 개 원소: 하나가 남아 `result ⊕ val`이 적용됨

### 쿼리 처리

1. **Type 1 (조회)**: `query(in_time[x], out_time[x])`로 부분트리 XOR 합 반환
2. **Type 2 (업데이트)**: `update(in_time[x], out_time[x], y)`로 구간에 y XOR

## 복잡도 분석

| 작업 | 시간 | 공간 |
|------|------|------|
| Euler Tour (DFS) | O(N) | O(N) |
| 세그먼트 트리 구축 | O(N log N) | O(N) |
| 각 쿼리 처리 | O(log N) | - |
| **전체** | **O((N+M) log N)** | **O(N)** |

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;

int n, m;
vector<int> adj[MAXN];
int weight[MAXN];
int in_time[MAXN], out_time[MAXN];
int euler_tour[MAXN * 2];
int timer = 0;

struct SegmentTree {
    int tree[MAXN * 8];
    int lazy[MAXN * 8];
    
    void push(int node, int start, int end) {
        if (lazy[node] != 0) {
            // XOR의 특성: 홀수 개의 원소에만 영향
            if ((end - start + 1) % 2 == 1) {
                tree[node] ^= lazy[node];
            }
            if (start != end) {
                lazy[node * 2] ^= lazy[node];
                lazy[node * 2 + 1] ^= lazy[node];
            }
            lazy[node] = 0;
        }
    }
    
    void build(int node, int start, int end) {
        if (start == end) {
            tree[node] = weight[euler_tour[start]];
        } else {
            int mid = (start + end) / 2;
            build(node * 2, start, mid);
            build(node * 2 + 1, mid + 1, end);
            tree[node] = tree[node * 2] ^ tree[node * 2 + 1];
        }
    }
    
    void update(int node, int start, int end, int l, int r, int val) {
        push(node, start, end);
        if (start > r || end < l) return;
        
        if (start >= l && end <= r) {
            lazy[node] ^= val;
            push(node, start, end);
            return;
        }
        
        int mid = (start + end) / 2;
        update(node * 2, start, mid, l, r, val);
        update(node * 2 + 1, mid + 1, end, l, r, val);
        
        push(node * 2, start, mid);
        push(node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] ^ tree[node * 2 + 1];
    }
    
    int query(int node, int start, int end, int l, int r) {
        if (start > r || end < l) return 0;
        
        push(node, start, end);
        
        if (start >= l && end <= r) {
            return tree[node];
        }
        
        int mid = (start + end) / 2;
        int left_result = query(node * 2, start, mid, l, r);
        int right_result = query(node * 2 + 1, mid + 1, end, l, r);
        return left_result ^ right_result;
    }
} seg;

void dfs(int u, int parent) {
    in_time[u] = ++timer;
    euler_tour[timer] = u;
    
    for (int v : adj[u]) {
        if (v != parent) {
            dfs(v, u);
        }
    }
    
    out_time[u] = timer;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n >> m;
    
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    
    for (int i = 1; i <= n; i++) {
        cin >> weight[i];
    }
    
    dfs(1, 0);
    
    seg.build(1, 1, n);
    
    for (int i = 0; i < m; i++) {
        int type;
        cin >> type;
        
        if (type == 1) {
            int x;
            cin >> x;
            cout << seg.query(1, 1, n, in_time[x], out_time[x]) << '\n';
        } else {
            int x, y;
            cin >> x >> y;
            seg.update(1, 1, n, in_time[x], out_time[x], y);
        }
    }
    
    return 0;
}
```

## 코너 케이스 체크리스트

| 경우 | 처리 방식 |
|------|---------|
| 리프 노드 조회 | `out_time[u] == in_time[u]` → 자신의 가중치만 반환 |
| 루트 조회 | 전체 트리 XOR 계산 |
| 전체 부분트리 업데이트 | 구간의 모든 노드 토글 |
| y = 0 업데이트 | XOR 상쇄로 변화 없음 (정상 동작) |
| 홀수/짝수 크기 구간 | push 함수에서 원소 개수로 판별 |
| 다중 업데이트 누적 | Lazy propagation으로 병합 |

## 제출 전 점검

- ✅ XOR lazy push에서 원소 개수(홀수/짝수) 확인
- ✅ in_time, out_time 초기화 및 DFS 정상 작동
- ✅ 세그먼트 트리 노드 범위 오버플로 방지 (MAXN*8)
- ✅ 각 쿼리 타입별 입력 형식 정확성
- ✅ Long long 필요 여부 검토 (10000 범위이므로 int 충분)

## 유사 문제

- **[BOJ 13925](https://www.acmicpc.net/problem/13925)**: Sequence and Queries 13 (구간 XOR/비트연산)
- **[BOJ 14504](https://www.acmicpc.net/problem/14504)**: Sequence and Queries 18 (세그먼트 트리)
- **[BOJ 29200](https://www.acmicpc.net/problem/29200)**: 정수 감소 문제 (XOR DP)

