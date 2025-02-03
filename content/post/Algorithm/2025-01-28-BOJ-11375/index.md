---
title: "[Algorithm] C++/Python 백준 11375번 : 열혈강호"
categories: 
- Algorithm
- Graph Theory
- Bipartite Matching
tags:
- Bipartite Matching
- DFS
- Graph Traversal
- Time Complexity Optimization
- Adjacency List
- Maximum Matching Problem
- Problem Solving
image: "bipartite_graph.png"
date: 2024-06-20
---

네트워크 플로우 이론의 기본이 되는 이분 매칭 문제를 다루는 대표적인 유형입니다. 직원과 작업을 두 그룹으로 나누어 최대 매칭을 찾는 과정에서 DFS 기반의 효율적인 탐색 전략이 필요합니다.

문제 : [https://www.acmicpc.net/problem/11375](https://www.acmicpc.net/problem/11375)

## 문제 설명

N명의 직원과 M개의 작업이 주어집니다. 각 직원은 최대 1개의 작업을 할당받을 수 있으며, 각 작업은 반드시 1명의 담당자가 필요합니다. 주어진 직원-작업 가능 목록에서 최대로 매칭할 수 있는 작업의 개수를 찾는 것이 목표입니다.

입력 형식은 첫 줄에 N과 M이 주어지고, 이후 N줄에 걸쳐 각 직원이 처리 가능한 작업 개수와 번호 목록이 제공됩니다. 출력은 가능한 최대 작업 매칭 수입니다.

핵심 제약 조건은 다음과 같습니다:
- 1 ≤ N, M ≤ 1,000
- 시간 제한 2초 내에 연산 완료
- 효율적인 그래프 탐색 기법 필수

## 접근 방식

### 이분 매칭(Bipartite Matching)
두 개의 독립된 그룹(직원-작업) 간 가능한 최대 매칭을 찾는 문제입니다. DFS를 이용한 재귀적 탐색으로 다음과 같은 과정을 수행합니다:

1. **그래프 구성**: 직원 노드에서 처리 가능한 작업 노드로 방향성 간선 연결
2. **매칭 시도**: 각 직원 노드에서 DFS 탐색 진행
3. **증가 경로 탐색**: 이미 매칭된 작업의 담당자가 다른 작업을 처리할 수 있는지 재귀적 확인
4. **역추적 갱신**: 성공적인 경로 발견 시 매칭 테이블 갱신

시간 복잡도는 O(N*E)로 최악의 경우 1,000*1,000 = 1,000,000번의 연산이 예상되며, 제한 시간 내에 처리 가능합니다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

vector<int> adj[1001];  // 직원별 작업 가능 리스트
int match[1001];        // 작업별 매칭된 직원 정보
bool visited[1001];     // DFS 방문 체크

bool dfs(int emp) {
    if (visited[emp]) return false;
    visited[emp] = true;
    
    // 현재 직원이 처리 가능한 모든 작업 검토
    for (int job : adj[emp]) {
        // 작업이 매칭되지 않았거나 매칭된 직원이 다른 작업 가능한 경우
        if (!match[job] || dfs(match[job])) {
            match[job] = emp;
            return true;
        }
    }
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, M;
    cin >> N >> M;
    
    // 그래프 구성
    for (int emp = 1; emp <= N; ++emp) {
        int cnt;
        cin >> cnt;
        adj[emp].resize(cnt);
        for (int i = 0; i < cnt; ++i) {
            cin >> adj[emp][i];
        }
    }
    
    // 이분 매칭 수행
    int result = 0;
    for (int emp = 1; emp <= N; ++emp) {
        memset(visited, false, sizeof(visited));
        if (dfs(emp)) result++;
    }
    
    cout << result;
    return 0;
}
```

### 코드 동작 설명
1. **입력 가속화**: `ios_base::sync_with_stdio(false)`로 입출력 속도 향상
2. **인접 리스트 구성**: 직원 번호별로 처리 가능 작업 리스트 저장
3. **DFS 매칭 시도**: 각 직원 노드에서 DFS 시작 → 방문 체크 후 가능 작업 탐색
4. **매칭 갱신 로직**: `match[job]` 배열을 통해 작업별 매칭 상태 관리
5. **결과 집계**: 성공적인 매칭 시마다 카운트 증가

## 결론

이분 매칭 문제의 기본 구조를 이해하는 데 최적의 문제입니다. DFS를 이용한 구현 방식이 직관적이지만, 큰 입력 크기에서의 성능을 위해 방문 배열 관리와 그래프 표현 방식에 주의해야 합니다. 추가적으로 Hopcroft-Karp 알고리즘을 적용하면 O(√N*E) 시간 복잡도로 최적화가 가능하며, 대규모 데이터셋 처리 시 유용합니다. 

실제 코딩 테스트 환경에서는 재귀 스택 한도를 고려해야 합니다. 이 문제를 통해 네트워크 플로우 분야의 기본기를 다지는 것이 중요합니다.