---
title: "[Algorithm] C++ 백준 7577번: 탐사"
description: "직선 도로에서 구간별 물체 개수 조건을 만족하는 배치를 찾는 문제입니다. 차분 제약 조건을 그래프로 모델링하고 SPFA로 음수 사이클을 탐지하여 O(NK) 시간에 해결합니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-7577
- cpp
- C++
- Difference Constraints
- 차분 제약
- SPFA
- Bellman-Ford
- 벨만포드
- Shortest Path
- 최단경로
- Graph
- 그래프
- Negative Cycle Detection
- 음수 사이클 탐지
- Constraint Satisfaction
- 제약 조건 만족
- Prefix Sum
- 누적합
- System of Inequalities
- 부등식 시스템
- Data Structures
- 자료구조
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(NK)
- Optimization
- 최적화
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
- Invariant
- 불변식
- Korean Olympiad
- 한국정보올림피아드
- KOI
- Regional Contest
- 지역본선
- 2013
- High School
- 고등부
- Special Judge
- 스페셜 저지
- Queue
- 큐
- Relaxation
- 완화
- Edge Weight
- 간선 가중치
- Adjacency List
- 인접 리스트
- String Output
- 문자열 출력
- Binary State
- 이진 상태
image: "wordcloud.png"
---

## 문제 정보

- **문제**: https://www.acmicpc.net/problem/7577
- **요약**: 길이 K인 직선 도로에 물체가 묻혀 있습니다. N개의 탐사 결과 Probe[x,y]=r (구간 [x,y]에 물체가 r개)가 주어질 때, 모든 조건을 만족하는 물체 배치를 찾거나, 불가능하면 "NONE"을 출력합니다.
- **제한**: 시간 1초, 메모리 128MB, 3 <= K <= 40, 2 <= N <= 1,000, 1 <= x <= y <= K, 0 <= r <= 1,000

## 입출력 형식/예제

```text
입력:
12 7
1 8 4
6 10 4
2 12 6
9 12 2
4 6 1
1 4 1
11 11 0

출력:
--#--####--#
```

```text
입력:
12 2
1 10 1
4 7 3

출력:
NONE
```

**예제 설명**:
- 예제 1: 위치 3, 6, 7, 8, 9, 12에 물체가 있는 배치가 모든 조건을 만족
- 예제 2: [4,7]에 3개 필요하지만 [1,10]에 1개만 있을 수 있으므로 모순 (4~7은 1~10의 부분집합)

## 접근 개요

### 핵심 관찰

1. **누적합으로 모델링**: S[i] = 위치 1부터 i까지 물체의 개수 (S[0] = 0)
2. **제약 조건 변환**:
   - Probe[x,y] = r => S[y] - S[x-1] = r
   - 각 위치에는 물체가 0개 또는 1개 => S[i] - S[i-1] in {0, 1}
3. **차분 제약 시스템**: 등식을 두 부등식으로 분리하여 그래프 최단경로 문제로 변환
4. **음수 사이클**: 해가 존재하지 않으면 그래프에 음수 사이클이 존재

### 알고리즘 흐름

```
1. 각 제약 조건을 그래프 간선으로 변환
   - S[y] - S[x-1] <= r: 간선 (x-1) -> y, 가중치 r
   - S[x-1] - S[y] <= -r: 간선 y -> (x-1), 가중치 -r
   - S[i] - S[i-1] <= 1: 간선 (i-1) -> i, 가중치 1
   - S[i-1] - S[i] <= 0: 간선 i -> (i-1), 가중치 0

2. 가상 시작점에서 모든 노드로 가중치 0 간선 연결

3. SPFA로 최단경로 계산, 음수 사이클 탐지

4. 음수 사이클이 없으면 S[i] - S[i-1] 값으로 결과 구성
```

## 알고리즘 설계

### 차분 제약 조건 (Difference Constraints)

차분 제약 시스템은 다음 형태의 부등식 집합입니다:
- x_j - x_i <= c_ij

이를 그래프로 모델링합니다:
- 노드: 각 변수 x_i
- 간선: i -> j, 가중치 c_ij (x_j - x_i <= c_ij 조건에서)

**정리**: 차분 제약 시스템의 해가 존재하는 필요충분조건은 대응하는 그래프에 음수 사이클이 없는 것입니다.

### SPFA (Shortest Path Faster Algorithm)

Bellman-Ford의 최적화 버전으로, 큐를 사용하여 필요한 노드만 완화합니다:
- 각 노드가 큐에 n번 이상 들어가면 음수 사이클 존재
- 평균 시간복잡도: O(E), 최악: O(VE)

### 결과 구성

SPFA 완료 후 dist[i] - dist[i-1]이 1이면 해당 위치에 물체가 있고, 0이면 없습니다.

## 복잡도

- **시간**: O(N * K) - N개 제약 조건, K개 노드에서 SPFA
- **공간**: O(K + N) - 인접 리스트와 거리 배열

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int K, N;
    cin >> K >> N;
    
    // 노드 0~K: S[i] = 위치 1~i의 물체 개수
    // 노드 K+1: 가상 시작점 (super source)
    int n = K + 1;
    vector<vector<pair<int, int>>> adj(n + 1);
    
    // 가상 시작점에서 모든 노드로 가중치 0 간선
    for (int i = 0; i <= K; i++) {
        adj[n].push_back({i, 0});
    }
    
    // 각 위치 제약: S[i] - S[i-1] in {0, 1}
    for (int i = 1; i <= K; i++) {
        adj[i-1].push_back({i, 1});   // S[i] <= S[i-1] + 1
        adj[i].push_back({i-1, 0});   // S[i-1] <= S[i]
    }
    
    // 탐사 제약 조건 입력
    for (int i = 0; i < N; i++) {
        int x, y, r;
        cin >> x >> y >> r;
        // S[y] - S[x-1] = r
        adj[x-1].push_back({y, r});    // S[y] <= S[x-1] + r
        adj[y].push_back({x-1, -r});   // S[x-1] <= S[y] - r
    }
    
    // SPFA with negative cycle detection
    vector<long long> dist(n + 1, LLONG_MAX);
    vector<int> cnt(n + 1, 0);
    vector<bool> inQueue(n + 1, false);
    queue<int> q;
    
    dist[n] = 0;
    q.push(n);
    inQueue[n] = true;
    
    bool hasNegativeCycle = false;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        inQueue[u] = false;
        
        for (auto& [v, w] : adj[u]) {
            if (dist[u] != LLONG_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (!inQueue[v]) {
                    q.push(v);
                    inQueue[v] = true;
                    cnt[v]++;
                    if (cnt[v] > n) {
                        hasNegativeCycle = true;
                        break;
                    }
                }
            }
        }
        if (hasNegativeCycle) break;
    }
    
    if (hasNegativeCycle) {
        cout << "NONE\n";
        return 0;
    }
    
    // 결과 구성
    string ans(K, '-');
    for (int i = 1; i <= K; i++) {
        long long diff = dist[i] - dist[i-1];
        if (diff == 1) {
            ans[i-1] = '#';
        }
    }
    
    cout << ans << "\n";
    
    return 0;
}
```

## 코너 케이스 체크리스트

- **상호 모순 조건**: [x1,y1]과 [x2,y2]가 포함관계인데 개수가 맞지 않는 경우 -> NONE
- **단일 위치 조건**: Probe[i,i]=0 또는 Probe[i,i]=1 -> 해당 위치 확정
- **전체 범위 조건**: Probe[1,K]=r -> 전체 물체 개수 결정
- **빈 결과**: 모든 조건에서 r=0 -> 모두 '-'
- **최대 입력**: K=40, N=1000 -> 시간 내 충분히 처리 가능

## 제출 전 점검

- [ ] 입력 형식: K, N 먼저 읽고 N개의 x y r 읽기
- [ ] 출력 형식: 길이 K인 문자열 또는 "NONE"
- [ ] 오버플로우: 거리 계산에 long long 사용
- [ ] 음수 사이클 탐지: 방문 횟수 > n 조건
- [ ] 인덱싱: 문제는 1-indexed, 코드는 0-indexed S[0] 사용

## 참고자료/유사문제

- [백준 1219 - 오민식의 고민](https://www.acmicpc.net/problem/1219) - Bellman-Ford 음수 사이클
- [백준 11657 - 타임머신](https://www.acmicpc.net/problem/11657) - Bellman-Ford 기본
- [Difference Constraints 개념](https://cp-algorithms.com/graph/system-difference-constraints.html)
- [CLRS Chapter 24.4 - Difference Constraints and Shortest Paths](https://mitpress.mit.edu/books/introduction-algorithms)

