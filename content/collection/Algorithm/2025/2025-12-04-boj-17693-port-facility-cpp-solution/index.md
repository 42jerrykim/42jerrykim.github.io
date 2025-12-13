---
draft: false
title: "[Algorithm] C++ 백준 17693번: Port Facility"
description: "원형 그래프(Circle Graph)의 이분 칠하기 문제를 세그먼트 트리와 BFS로 O(NlogN)에 해결합니다. 컨테이너 입출항 교차 관계를 그래프로 모델링하고 연결 요소마다 2^c 가지 배치를 계산하는 정확한 풀이입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Graph Theory
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-17693
  - C++
  - Graph Theory
  - 그래프
  - Bipartite Graph
  - 이분그래프
  - Circle Graph
  - 원형그래프
  - Graph Coloring
  - 그래프칠하기
  - BFS
  - DFS
  - Segment Tree
  - 세그먼트트리
  - Range Query
  - 범위쿼리
  - Connected Components
  - 연결요소
  - Conflict Graph
  - 충돌그래프
  - Crossing Intervals
  - 교차구간
  - Interval Scheduling
  - 구간스케줄링
  - Stack Data Structure
  - 스택
  - Two-Coloring
  - 이색칠
  - Graph Traversal
  - 그래프순회
  - Data Structures
  - 자료구조
  - Time Complexity
  - 시간복잡도
  - O(N log N)
  - Space Complexity
  - 공간복잡도
  - Modulo Arithmetic
  - 모듈러산술
  - Combinatorics
  - 조합론
  - Competitive Programming
  - 경쟁프로그래밍
  - Problem Solving
  - 문제풀이
  - Code Implementation
  - 코드구현
  - JOI
  - 정보올림피아드
  - Spring Camp
  - 봄캠프
  - Correctness Proof
  - 정당성증명
  - Edge Cases
  - 코너케이스
  - Optimization Technique
  - 최적화기법
image: "wordcloud.png"
---

## 문제 정보

**출처**: [BOJ 17693 - Port Facility](https://www.acmicpc.net/problem/17693) (JOI Spring Training Camp 2017 1-2번)

**요약**: JOI 항구에 도착하는 $N$개의 컨테이너를 두 개의 보관 구역에 배정합니다. 각 구역은 스택(Stack)처럼 동작하므로, 같은 구역 내 두 컨테이너 $i, j$ ($A_i < A_j$)는 반드시 $B_j < B_i$를 만족해야 합니다(LIFO). 교차하는 구간($(A_i, B_i)$과 $(A_j, B_j)$가 $A_i < A_j < B_i < B_j$ 형태)은 다른 구역에 배정해야 합니다. **가능한 배정 방법의 개수를 $\bmod 10^9+7$로 구하세요**.

**제한 조건**:
- $1 \le N \le 1,000,000$
- $1 \le A_i, B_i \le 2N$, $A_i < B_i$
- 모든 $A_1, \ldots, A_N, B_1, \ldots, B_N$은 서로 다름
- 시간 제한: 4.5초, 메모리 제한: 1024 MB

## 입출력 형식 및 예제

### 입력 형식
```
N
A₁ B₁
A₂ B₂
...
Aₙ Bₙ
```

### 예제 1
**입력**:
```
4
1 3
2 5
4 8
6 7
```
**출력**:
```
4
```

**설명**: 컨테이너 1,3,4를 구역A에, 2를 구역B에 배정하거나 다양한 방식으로 배정 가능 → 4가지

### 예제 2
**입력**:
```
3
1 4
2 5
3 6
```
**출력**:
```
0
```

**설명**: 모든 구간이 교차하여 홀수 사이클을 형성 → 이분 칠하기 불가 → 0

## 접근 개요

### 핵심 관찰 (Circle Graph 이분 칠하기)

**문제 재해석**: 각 컨테이너를 시간 축 위의 구간 $[A_i, B_i)$로 모델링합니다. 두 구간이 **교차**(Crossing)하면 같은 구역에 있을 수 없습니다. 즉, 교차 관계를 간선으로 하는 **충돌 그래프(Conflict Graph)**가 이분 그래프인지 판별하고, 이분 칠하기(2-coloring)의 개수를 세는 문제입니다.

**이분 칠하기의 개수**: 그래프가 이분 그래프라면:
- 각 **연결 요소(Connected Component)**마다 두 가지 칠하기 방식 존재(색 반전)
- 총 개수 = $2^c$ (단, $c$ = 연결 요소 개수)

### 알고리즘 (Segment Tree + BFS)

$N$이 최대 100만이므로 $O(N^2)$ 간선 구성 불가. **다음 전략 사용**:

1. **세그먼트 트리 구축** (2개):
   - **Tree1**: 위치 = $A_i$, 값 = $B_i$, 범위 최댓값 쿼리
   - **Tree2**: 위치 = $B_i$, 값 = $A_i$, 범위 최솟값 쿼리

2. **BFS 색칠**:
   - 각 미방문 정점에서 BFS 시작, 연결 요소 개수 증가
   - 정점 $u$를 방문하면, "교차하는 모든 미방문 이웃"을 쿼리 + 제거
   - 이웃: Tree1 쿼리로 $(A_u, B_u)$ 범위에서 $B > B_u$ 찾기, Tree2로 $(A_u, B_u)$ 범위에서 $A < A_u$ 찾기

3. **유효성 검증** (각 색 그룹):
   - 각 색 그룹의 구간을 $A$ 정렬 후 스택으로 검증: 구간이 교차하지 않아야 함

## 알고리즘 설계

### 자료구조

1. **세그먼트 트리 2개** (총 2배 복잡도):
   - `tree1[node]`: 인덱스 = 시작 시간 $A_i$, 값 = 종료 시간 $B_i$, 범위 최댓값 유지
   - `tree2[node]`: 인덱스 = 종료 시간 $B_i$, 값 = 시작 시간 $A_i$, 범위 최솟값 유지

2. **색 배열**: `color[i]` = 0 또는 1 (미방문 = -1)

3. **매핑 배열**: 시간 좌표 ↔ 컨테이너 ID 변환

### 구현 포인트

| 항목 | 설명 |
|------|------|
| **구간 교차 판정** | $A_i < A_j < B_i < B_j$ 형태 감지 |
| **Tree 쿼리 + 제거** | 범위 쿼리 후 해당 잎 노드 값을 "무효값" 설정 + 상위 노드 업데이트 |
| **BFS 종료 조건** | 모든 정점 방문, 이분 칠하기 검증(홀수 사이클 없음) |
| **답 계산** | 이분 그래프 ⇒ $2^{\text{components}} \bmod 10^9+7$, 아니면 0 |

### 정당성

**Claim**: 그래프가 이분 그래프 ⟺ 각 색 그룹이 교차 없음(스택 정렬 가능)

**근거**: 
- 교차 없는 구간들은 완전히 중첩되거나 분리되므로 스택으로 관리 가능
- 역으로, 교차가 생기면 그래프에 홀수 사이클 발생 ⇒ 이분이 아님

**시간 복잡도 분석**:
- 각 정점은 최대 1회 큐에 삽입 (방문 시 세그먼트 트리에서 제거)
- Tree 노드 방문: 각 정점당 $O(\log N)$
- **총**: $O(N \log N)$

## 복잡도 분석

| 항목 | 복잡도 | 근거 |
|------|--------|------|
| **시간** | $O(N \log N)$ | 세그먼트 트리 구축 $O(N \log N)$ + BFS 방문 + Tree 쿼리/제거 |
| **공간** | $O(N)$ | 세그먼트 트리 (크기 $4N$) + 색/매핑 배열 |

## 실제 정답 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000000007;
const int INF = 1e9;

int N;
vector<int> posA, posB;       // ID → time
vector<int> color;             // 0/1/-1(unvisited)
vector<int> tree1, tree2;      // Segment trees
map<int, int> mapAtoID, mapBtoID;

// Tree1: Pos=A, Val=B, Range Max Query
void update1(int node, int start, int end, int idx, int val) {
    if (idx < start || idx > end) return;
    if (start == end) { tree1[node] = val; return; }
    int mid = (start + end) / 2;
    update1(node * 2, start, mid, idx, val);
    update1(node * 2 + 1, mid + 1, end, idx, val);
    tree1[node] = max(tree1[node * 2], tree1[node * 2 + 1]);
}

// Tree2: Pos=B, Val=A, Range Min Query
void update2(int node, int start, int end, int idx, int val) {
    if (idx < start || idx > end) return;
    if (start == end) { tree2[node] = val; return; }
    int mid = (start + end) / 2;
    update2(node * 2, start, mid, idx, val);
    update2(node * 2 + 1, mid + 1, end, idx, val);
    tree2[node] = min(tree2[node * 2], tree2[node * 2 + 1]);
}

// Find and remove one interval from tree1 with A in (L,R) and B > limitB
int findRemove1(int node, int start, int end, int L, int R, int limitB) {
    if (tree1[node] <= limitB) return -1;
    if (start > R || end < L) return -1;
    if (start == end) {
        int res = start;
        tree1[node] = -INF;
        return res;
    }
    int mid = (start + end) / 2;
    int res = findRemove1(node * 2, start, mid, L, R, limitB);
    if (res != -1) {
        tree1[node] = max(tree1[node * 2], tree1[node * 2 + 1]);
        return res;
    }
    res = findRemove1(node * 2 + 1, mid + 1, end, L, R, limitB);
    tree1[node] = max(tree1[node * 2], tree1[node * 2 + 1]);
    return res;
}

// Find and remove one interval from tree2 with B in (L,R) and A < limitA
int findRemove2(int node, int start, int end, int L, int R, int limitA) {
    if (tree2[node] >= limitA) return -1;
    if (start > R || end < L) return -1;
    if (start == end) {
        int res = start;
        tree2[node] = INF;
        return res;
    }
    int mid = (start + end) / 2;
    int res = findRemove2(node * 2, start, mid, L, R, limitA);
    if (res != -1) {
        tree2[node] = min(tree2[node * 2], tree2[node * 2 + 1]);
        return res;
    }
    res = findRemove2(node * 2 + 1, mid + 1, end, L, R, limitA);
    tree2[node] = min(tree2[node * 2], tree2[node * 2 + 1]);
    return res;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> N;
    posA.resize(N + 1);
    posB.resize(N + 1);
    color.assign(N + 1, -1);
    
    int maxCoord = 2 * N;
    tree1.assign(4 * maxCoord + 5, -INF);
    tree2.assign(4 * maxCoord + 5, INF);
    
    for (int i = 1; i <= N; ++i) {
        int a, b;
        cin >> a >> b;
        posA[i] = a;
        posB[i] = b;
        mapAtoID[a] = i;
        mapBtoID[b] = i;
        update1(1, 1, maxCoord, a, b);
        update2(1, 1, maxCoord, b, a);
    }
    
    int components = 0;
    bool possible = true;
    
    for (int start = 1; start <= N; ++start) {
        if (color[start] != -1) continue;
        
        components++;
        queue<int> q;
        q.push(start);
        color[start] = 0;
        update1(1, 1, maxCoord, posA[start], -INF);
        update2(1, 1, maxCoord, posB[start], INF);
        
        while (!q.empty() && possible) {
            int u = q.front();
            q.pop();
            int uA = posA[u], uB = posB[u], c = color[u];
            
            // Type 1: Find v with A_u < A_v < B_u < B_v
            while (true) {
                int vA = findRemove1(1, 1, maxCoord, uA + 1, uB - 1, uB);
                if (vA == -1) break;
                int v = mapAtoID[vA];
                if (color[v] == -1) {
                    color[v] = 1 - c;
                    update2(1, 1, maxCoord, posB[v], INF);
                    q.push(v);
                } else if (color[v] == c) {
                    possible = false;
                    break;
                }
            }
            
            // Type 2: Find v with A_v < A_u < B_v < B_u
            while (true) {
                int vB = findRemove2(1, 1, maxCoord, uA + 1, uB - 1, uA);
                if (vB == -1) break;
                int v = mapBtoID[vB];
                if (color[v] == -1) {
                    color[v] = 1 - c;
                    update1(1, 1, maxCoord, posA[v], -INF);
                    q.push(v);
                } else if (color[v] == c) {
                    possible = false;
                    break;
                }
            }
        }
        if (!possible) break;
    }
    
    // Validation: check each color group is stack-sortable
    if (possible) {
        for (int k = 0; k < 2; ++k) {
            vector<pair<int, int>> group;
            for (int i = 1; i <= N; ++i) {
                if (color[i] == k) {
                    group.push_back({posA[i], posB[i]});
                }
            }
            sort(group.begin(), group.end());
            
            vector<int> st;
            for (auto [a, b] : group) {
                while (!st.empty() && st.back() < a) st.pop_back();
                if (!st.empty() && st.back() < b) {
                    possible = false;
                    break;
                }
                st.push_back(b);
            }
            if (!possible) break;
        }
    }
    
    if (!possible) {
        cout << 0 << "\n";
    } else {
        long long ans = 1;
        for (int i = 0; i < components; ++i) {
            ans = (ans * 2) % MOD;
        }
        cout << ans << "\n";
    }
    
    return 0;
}
```

## 코너 케이스 체크리스트

| 케이스 | 처리 방법 | 예상 결과 |
|--------|---------|----------|
| **N=1** | 단일 구간, 이분 칠하기 가능 | $2^1 = 2$ |
| **완전 중첩** (e.g., $[1,8], [2,7], [3,6]$) | 모두 교차 → 홀수 사이클 → 이분 불가 | 0 |
| **분리된 구간들** (e.g., $[1,2], [3,4]$) | 교차 없음 → 독립 컴포넌트 | $2^{\text{# components}}$ |
| **경계값** (e.g., $A_i = 1, B_i = 2N$) | 전체 범위 포함 | 교차 판정 정상 작동 |
| **두 구간만** (교차) | 간선 하나 → 이분 그래프 | $2^1 = 2$ |
| **모두 교차** (홀수 사이클) | 완전 그래프 $K_3$ 이상 → 홀수 사이클 | 0 |

## 제출 전 점검

### 입출력 형식
- [ ] 입력 첫 줄: `N` (정수)
- [ ] 다음 N줄: 각 컨테이너 `A B` (공백 구분)
- [ ] 출력: 한 줄에 정수 (modulo $10^9+7$)
- [ ] 개행 문자 확인 (`"\n"` 사용)

### 오버플로우 체크
- [ ] 답 계산: $2^N$ 최대 $2^{1000000}$ → **반드시 modulo 연산**
- [ ] `ans = (ans * 2) % MOD` 형태로 매 단계 적용

### 초기화 및 범위
- [ ] `posA, posB` 인덱스: 1-indexed (컨테이너 ID)
- [ ] Tree 인덱스: 1-indexed, 좌표 범위 $[1, 2N]$
- [ ] `color[]` 초기화: -1 (미방문)
- [ ] `tree1` 초기값: -INF, `tree2` 초기값: INF

### 알고리즘 검증
- [ ] BFS 종료: 모든 정점 방문 또는 이분 칠하기 실패
- [ ] 색 충돌 감지: 같은 색 이웃 발견 시 → 홀수 사이클 → 0 반환
- [ ] 스택 정렬 검증: 각 색 그룹이 교차 없는지 최종 확인

### 세그먼트 트리 정합성
- [ ] `findRemove` 함수: 제거 후 상위 노드 업데이트 필수
- [ ] 범위 경계: `(uA + 1, uB - 1)` (strict 부등호)
- [ ] 제한 값: Tree1은 `> limitB`, Tree2는 `< limitA` 확인

## 유사 문제 및 참고 자료

- [BOJ 2610 - Hierarchy](https://www.acmicpc.net/problem/2610) (컴포넌트 개수 세기)
- [BOJ 3197 - Lake (Two Pointer + DSU)](https://www.acmicpc.net/problem/3197)
- **개념 참고**: 
  - Circle Graph Coloring, Interval Scheduling
  - Segment Tree Range Query + Lazy Deletion
  - BFS-based Graph Coloring

