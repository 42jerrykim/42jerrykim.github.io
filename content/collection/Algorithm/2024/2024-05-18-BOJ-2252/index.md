---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-05-18T00:00:00Z"
header:
  teaser: /assets/images/2024/topological_sort_process.png
tags:
- Graph
- TopologicalSort
title: '[Algorithm] C++ 백준 2252번 : 줄 세우기'
aliases: /algorithm/BOJ-2252/
---

백준 2252번 "줄 세우기" 문제는 N명의 학생을 키 순서대로 줄을 세우는 것이다. 일부 학생들의 키 비교 결과가 주어지며, 이를 바탕으로 모든 학생이 키 순서대로 줄을 서도록 정렬해야 한다. 입력으로 학생 수 N과 비교 횟수 M이 주어지고, M개의 키 비교 결과가 주어진다. 이를 위상 정렬을 통해 해결할 수 있다.

[원문 링크](https://www.acmicpc.net/problem/2206)

|![/assets/images/2024/topological_sort_process.png](/assets/images/2024/topological_sort_process.png)|
|:---:|
|이미지로 형상화|

## 문제 설명

- N명의 학생을 키 순서대로 줄을 세우려고 한다.
- 일부 학생들의 키를 비교한 결과가 주어진다.
- 모든 학생이 키 순서대로 줄을 서도록 나열하는 프로그램을 작성해야 한다.

## 입력

1. 첫 번째 줄에 학생 수 N(1 ≤ N ≤ 32,000)과 비교 횟수 M(1 ≤ M ≤ 100,000)이 주어진다.
2. 다음 M개의 줄에는 두 학생의 키를 비교한 결과 A B가 주어진다. 이는 A 학생이 B 학생보다 앞에 서야 한다는 의미이다.

## 출력
- 학생들을 키 순서대로 줄을 세운 결과를 출력한다.

## 예제 입력
```
4 2
4 2
3 1
```

## 예제 출력
```
4 2 3 1
```

## 풀이

이 문제는 위상 정렬(Topological Sorting)을 통해 해결할 수 있다. 주어진 방향 그래프에서 모든 정점을 순서대로 나열하는 것이다. 이를 위해 큐와 진입 차수를 사용하여 위상 정렬을 구현할 수 있다. 다음은 그 알고리즘의 간단한 설명이다.

1. 각 노드의 진입 차수를 계산한다.
2. 진입 차수가 0인 모든 노드를 큐에 삽입한다.
3. 큐에서 노드를 하나씩 꺼내고, 그 노드와 연결된 모든 간선을 제거한다.
4. 간선 제거 후, 새로 진입 차수가 0이 된 노드를 큐에 삽입한다.
5. 큐가 빌 때까지 3-4 과정을 반복한다.

## 문제 해결 과정

1. **입력 처리**:
   - 학생 수 \(N\)과 비교 횟수 \(M\)을 입력받는다.
   - 각 비교 결과 \(A, B\)를 입력받아 그래프를 구축한다.
   - \(A\)는 \(B\)보다 앞에 서야 하므로, 그래프에서 \(A\)에서 \(B\)로의 간선을 추가하고 \(B\)의 진입 차수를 증가시킨다.

2. **초기화**:
   - 진입 차수가 0인 모든 노드를 큐에 삽입한다. 이 노드들은 다른 노드에 앞서야 하는 학생들이다.

3. **위상 정렬 수행**:
   - 큐가 빌 때까지 다음을 반복한다.
     - 큐에서 노드를 하나 꺼내 출력 리스트에 추가한다.
     - 해당 노드와 연결된 모든 간선 제거하고, 연결된 노드들의 진입 차수를 감소시킨다.
     - 진입 차수가 0이 된 노드를 큐에 삽입한다.

4. **결과 출력**:
   - 출력 리스트를 차례로 출력하여 학생들이 키 순서대로 줄을 서게 한다.

### 코드 예시 (Python)

다음은 파이썬으로 작성한 코드 예제이다.

```python
from collections import deque

def topology_sort():
    N, M = map(int, input().split())
    indegree = [0] * (N + 1)
    graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        A, B = map(int, input().split())
        graph[A].append(B)
        indegree[B] += 1
        
    queue = deque()
    for i in range(1, N + 1):
        if indegree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        current = queue.popleft()
        result.append(current)
        for node in graph[current]:
            indegree[node] -= 1
            if indegree[node] == 0:
                queue.append(node)
    
    print(" ".join(map(str, result)))

topology_sort()
```

이 코드는 입력된 학생 수와 비교 결과를 바탕으로 그래프를 구축하고, 위상 정렬 알고리즘을 통해 올바른 순서로 학생들을 줄 세운다.


### 코드 예시 (C++)

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

void topology_sort(int N, int M, vector<vector<int>>& graph, vector<int>& indegree) {
    queue<int> q;
    for (int i = 1; i <= N; ++i) {
        if (indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int current = q.front();
        q.pop();
        cout << current << " ";
        for (int next : graph[current]) {
            if (--indegree[next] == 0) {
                q.push(next);
            }
        }
    }
}

int main() {
    int N, M;
    cin >> N >> M;
    vector<vector<int>> graph(N + 1);
    vector<int> indegree(N + 1, 0);

    for (int i = 0; i < M; ++i) {
        int A, B;
        cin >> A >> B;
        graph[A].push_back(B);
        indegree[B]++;
    }

    topology_sort(N, M, graph, indegree);
    return 0;
}
```

이 코드는 위 과정을 단계적으로 구현하여, 입력된 학생들을 키 순서대로 정렬한다.