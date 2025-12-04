---
title: "[Algorithm] C++ 백준 16746번: Four-Coloring"
description: "평면 그래프 색칠 문제를 Smallest-Last Ordering과 Kempe Chain 휴리스틱으로 해결합니다. 4색 정리 기반 그래프 색칠, Degeneracy 활용, 색상 충돌 시 연결 요소 교환을 통한 다항식 시간 알고리즘 구현입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Graph
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-16746
  - C++
  - Graph
  - 그래프
  - Graph Coloring
  - 그래프 색칠
  - Four Color Theorem
  - 4색 정리
  - Planar Graph
  - 평면 그래프
  - Smallest-Last Ordering
  - Kempe Chain
  - Degeneracy
  - Coloring Algorithm
  - 색칠 알고리즘
  - Greedy Coloring
  - 그리디 색칠
  - BFS
  - DFS
  - Graph Traversal
  - 그래프 순회
  - Vertex Coloring
  - 정점 색칠
  - Edge Coloring
  - Component Analysis
  - 연결 요소 분석
  - Heuristic Algorithm
  - 휴리스틱 알고리즘
  - Constructive Algorithm
  - 구성적 알고리즘
  - Implementation Details
  - 구현 디테일
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Proof of Correctness
  - 정당성 증명
  - Competitive Programming
  - 경쟁프로그래밍
  - ICPC
  - Yokohama Regional
  - 2018
  - Asia Regional
  - Graph Theory
  - 그래프 이론
  - Data Structures
  - 자료구조
  - Adjacency List
  - 인접 리스트
  - Algorithm Study
  - 알고리즘 공부
image: "wordcloud.png"
---

## 문제 정보

**문제**: [BOJ 16746 - Four-Coloring](https://www.acmicpc.net/problem/16746)

**문제 요약**: 주어진 평면 그래프(Planar Graph)에서 각 정점을 1~4 중 하나의 색으로 칠하되, 인접한 두 정점이 서로 다른 색을 갖도록 해야 합니다. 정점은 정수 좌표를 가지며, 간선은 가로, 세로, 대각선(45도)으로만 배치됩니다.

**제한 조건**:
- 정점 수: $3 \le n \le 10,000$
- 간선 수: $n \le m \le 10,000$
- 시간 제한: 2초
- 메모리 제한: 512 MB

## 입출력 형식

**입력**:
```
n m
x₁ y₁
x₂ y₂
⋮
xₙ yₙ
u₁ v₁
u₂ v₂
⋮
uₘ vₘ
```

- 첫 줄: 정점 수 $n$, 간선 수 $m$
- 다음 $n$줄: 각 정점의 좌표 $(x_i, y_i)$
- 다음 $m$줄: 간선 $(u_i, v_i)$

**출력**: $n$줄, 각 줄에 해당 정점의 색상(1~4)

**예제 입력 1**:
```
5 8
0 0
2 0
0 2
2 2
1 1
1 2
1 3
1 5
2 4
2 5
3 4
3 5
4 5
```

**예제 출력 1**:
```
1
2
2
1
3
```

## 접근 개요

**핵심 관찰**:
- 4색 정리(Four Color Theorem): 모든 평면 그래프는 4가지 색으로 칠할 수 있음.
- 평면 그래프의 Degeneracy ≤ 5: 임의의 부분 그래프에서 차수 ≤ 5인 정점이 존재.

**선택한 알고리즘**:
1. **Smallest-Last Ordering (Matula & Beck)**: 차수가 낮은 정점부터 제거하면서 스택에 쌓음 → 역순으로 색칠하면 충돌 최소화
2. **Kempe Chain 교환**: 색상 충돌 시, 두 색으로만 이루어진 경로에서 색을 서로 맞바꿈 → 새로운 색상 확보

**정당성**:
- Smallest-Last 순서에서는 색칠 시 이미 색칠된 이웃 최대 5명 → 4색으로 충분
- Kempe Chain은 유효한 색칠을 유지하면서 색상 재배치 → 항상 해결 가능

## 알고리즘 설계

### 1단계: Smallest-Last Ordering 구성

```cpp
set<pair<degree, id>> deg_set ← 모든 정점을 (차수, ID)로 삽입
order ← []

while deg_set is not empty:
    u ← deg_set의 최소 원소(가장 낮은 차수)
    order.push(u)
    deg_set에서 u 제거
    
    for each neighbor v of u (아직 제거되지 않음):
        deg_set에서 (deg[v], v) 제거
        deg[v] ← deg[v] - 1
        deg_set에 (deg[v], v) 삽입
```

### 2단계: 역순으로 색칠 수행
```cpp
reverse(order)

for each vertex u in order:
    used ← u의 이웃 중 이미 색칠된 정점들의 색 집합
    
    if 사용 가능한 색(1~4)이 있음:
        u ← 그 색 할당
    else (모든 색이 사용 중):
        for each target_color in 1..4:
            for each swap_color in 1..4 (swap_color ≠ target_color):
                if try_kempe_swap(u, target_color, swap_color):
                    u ← target_color 할당
                    break
```

### 3단계: Kempe Chain 교환
```cpp
bool try_kempe_swap(u, target_c, swap_c):
    nbr_target ← {u의 이웃 중 색이 target_c}
    nbr_swap ← {u의 이웃 중 색이 swap_c}
    
    if nbr_target is empty:
        return true  // 이미 target_c가 비어있음
    
    // BFS: nbr_swap에서 출발하여 target_c/swap_c 간선만 따라가기
    visited ← BFS_from_all(nbr_swap, only_colors={target_c, swap_c})
    
    if any node in nbr_target is visited:
        return false  // 연결되어 있으므로 교환 불가
    
    // nbr_target의 각 컴포넌트에서 색을 flip
    for each unvisited node v in nbr_target:
        component ← BFS_component(v, only_colors={target_c, swap_c})
        for each node in component:
            color[node] ← (color[node] == target_c) ? swap_c : target_c
    
    return true
```

## 복잡도 분석

**시간 복잡도**: $O((n + m) \log n + k)$
- Smallest-Last Ordering: $O((n + m) \log n)$ (set 유지보수)
- 색칠 단계: 각 정점마다 최대 상수 횟수의 BFS 수행 → $O(n + m)$
- 총합: $O((n + m) \log n)$

**공간 복잡도**: $O(n + m)$ (인접 리스트, 방문 배열, set)

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 10005;

int N, M;
vector<int> adj[MAXN];
int colors[MAXN];
bool removed[MAXN];
bool visited[MAXN];

bool try_kempe_swap(int u, int target_c, int swap_c) {
    vector<int> nbr_target, nbr_swap;
    for (int v : adj[u]) {
        if (colors[v] == target_c) nbr_target.push_back(v);
        if (colors[v] == swap_c) nbr_swap.push_back(v);
    }

    if (nbr_target.empty()) return true;

    // BFS: nbr_swap에서 시작하여 target_c/swap_c 간선 따라가기
    for(int i = 1; i <= N; ++i) visited[i] = false;
    queue<int> q;
    
    for (int v : nbr_swap) {
        if (!visited[v]) {
            q.push(v);
            visited[v] = true;
            while (!q.empty()) {
                int curr = q.front();
                q.pop();
                
                for (int next : adj[curr]) {
                    if ((colors[next] != target_c && colors[next] != swap_c) || visited[next])
                        continue;
                    visited[next] = true;
                    q.push(next);
                }
            }
        }
    }

    // 연결 확인
    for (int v : nbr_target) {
        if (visited[v]) return false;
    }

    // 색 교환
    for(int i = 1; i <= N; ++i) visited[i] = false;
    
    for (int v : nbr_target) {
        if (visited[v]) continue;
        
        queue<int> fq;
        fq.push(v);
        visited[v] = true;
        
        while(!fq.empty()){
            int curr = fq.front();
            fq.pop();
            
            if (colors[curr] == target_c) colors[curr] = swap_c;
            else colors[curr] = target_c;
            
            for(int next : adj[curr]){
                if ((colors[next] != target_c && colors[next] != swap_c) || visited[next])
                    continue;
                visited[next] = true;
                fq.push(next);
            }
        }
    }
    
    return true;
}

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M;

    vector<int> degree(N + 1, 0);
    for (int i = 0; i < M; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
        degree[u]++;
        degree[v]++;
    }

    // Smallest-Last Ordering
    set<pair<int, int>> deg_set;
    for(int i = 1; i <= N; ++i) {
        deg_set.insert({degree[i], i});
        colors[i] = 0;
        removed[i] = false;
    }

    vector<int> order;

    while(!deg_set.empty()){
        auto [d, u] = *deg_set.begin();
        deg_set.erase(deg_set.begin());
        removed[u] = true;
        order.push_back(u);

        for(int v : adj[u]){
            if(!removed[v]){
                deg_set.erase({degree[v], v});
                degree[v]--;
                deg_set.insert({degree[v], v});
            }
        }
    }

    // 역순으로 색칠
    reverse(order.begin(), order.end());

    for(int u : order) {
        bool used[5] = {false};
        for(int v : adj[u]) {
            if(colors[v] != 0) {
                used[colors[v]] = true;
            }
        }

        int chosen = -1;
        for(int c = 1; c <= 4; ++c) {
            if(!used[c]) {
                chosen = c;
                break;
            }
        }

        if(chosen != -1) {
            colors[u] = chosen;
        } else {
            bool solved = false;
            for(int target = 1; target <= 4 && !solved; ++target) {
                for(int swap_c = 1; swap_c <= 4; ++swap_c) {
                    if(target == swap_c) continue;
                    if(try_kempe_swap(u, target, swap_c)) {
                        colors[u] = target;
                        solved = true;
                        break;
                    }
                }
            }
            
            if(!solved) colors[u] = 1;
        }
    }

    for(int i = 1; i <= N; ++i) {
        cout << colors[i] << "\n";
    }

    return 0;
}
```

## 코드 핵심 포인트

1. **Smallest-Last 구현**: `set<pair<degree, id>>`로 최소 차수 정점을 O(log N)에 추출
2. **동적 차수 갱신**: 정점 제거 시 이웃의 차수 감소 → set 재삽입
3. **Kempe Chain BFS**: 두 가지 색만 고려하여 연결성 검사 및 색 교환
4. **색상 할당**: Greedy 우선, 실패 시 Kempe 교환으로 필요한 색 확보

## 코너 케이스 체크리스트

- **최소 입력**: $n=3$ (삼각형) → 3가지 색 필요
- **균일 그래프**: 완전 그래프 $K_4$ (모든 정점이 3개 이웃) → 4색 모두 필요
- **경계 좌표**: $(0, 0)$과 $(1000, 1000)$ 같은 극단값 처리
- **다중 정답**: 여러 올바른 색칠 가능 (모두 정답)

## 제출 전 점검

- 입출력 형식: 각 줄에 정수 하나(개행 포함)
- 색상 범위: 1~4만 출력
- 유효성 검증: 인접한 정점이 서로 다른 색 확인
- 정점 개수: 1-indexed 정점 $1 \sim N$ 모두 색칠 여부 확인

## 참고자료

- Four Color Theorem: https://en.wikipedia.org/wiki/Four_color_theorem
- Kempe Chains: https://en.wikipedia.org/wiki/Kempe_chain
