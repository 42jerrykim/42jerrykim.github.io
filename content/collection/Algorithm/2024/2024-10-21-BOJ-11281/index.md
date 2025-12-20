---
title: "[Algorithm] C++/Python 백준 11281번 : 2-SAT - 4"
description: "백준 11281번 2-SAT 문제는 2개의 변수로 이루어진 논리식을 모두 만족시키는 변수의 값을 결정하는 알고리즘 문제입니다. 임플리케이션 그래프와 강한 연결 요소(SCC) 탐색을 통해 논리식의 만족 가능성을 판별하고, 변수의 진리값 할당 방법을 구하는 것이 핵심입니다."
categories: 
- Algorithm
- GraphTheory
- 2-SAT
tags:
- 2-SAT
- StronglyConnectedComponents
- Kosaraju's Algorithm
- GraphTheory
- ImplicationGraph
- O(N+M)
- GraphTraversal
image: "tmp_wordcloud.png"
date: 2024-10-21
---

오늘은 백준 온라인 저지의 11281번 문제인 "2-SAT - 4"를 다뤄보겠다. 이 문제는 2-SAT 문제로, 논리 회로 및 그래프 이론의 지식을 요구한다.

문제 : [https://www.acmicpc.net/problem/11281](https://www.acmicpc.net/problem/11281)

## 문제 설명

2-SAT 문제는 \(N\)개의 불리언 변수 \(x_1, x_2, \ldots, x_N\)가 있을 때, 주어진 2-CNF(Conjunctive Normal Form) 식을 참으로 만드는 변수의 값을 찾는 문제이다. 2-CNF 식은 여러 개의 절(clause)의 논리곱(\(\land\))으로 구성되며, 각 절은 두 개의 리터럴(변수 또는 그 부정)의 논리합(\(\lor\))으로 이루어진다.

예를 들어, 다음과 같은 식을 생각해보자:

\[
(\lnot x_1 \lor x_2) \land (\lnot x_2 \lor x_3) \land (x_1 \lor x_3) \land (x_3 \lor x_2)
\]

여기서 \(\lnot\)는 NOT을, \(\lor\)는 OR을, \(\land\)는 AND를 의미한다. 이 식을 참으로 만들기 위해 각 변수에 적절한 값을 할당해야 한다.

문제는 변수의 개수 \(N\)과 절의 개수 \(M\), 그리고 각 절에 포함된 변수들이 주어졌을 때, 전체 식을 참으로 만들 수 있는지 판단하고, 가능하다면 변수들의 값을 구하는 것이다.

예를 들어, \(N = 3\), \(M = 4\)인 경우 위의 식을 참으로 만들기 위해 \(x_1 = \text{False}\), \(x_2 = \text{False}\), \(x_3 = \text{True}\)로 설정할 수 있다. 하지만 \(N = 1\), \(M = 2\), \(f = (x_1 \lor x_1) \land (\lnot x_1 \lor \lnot x_1)\)인 경우에는 \(x_1\)에 어떤 값을 할당하더라도 식을 참으로 만들 수 없다.

## 접근 방식

이 문제는 2-SAT 문제로, 선형 시간 내에 해결할 수 있다. 주요 아이디어는 **임플리케이션 그래프(Implication Graph)**를 구성하고, **강한 연결 요소(Strongly Connected Components, SCC)**를 찾는 것이다.

1. **임플리케이션 그래프 구성**:

   - 각 변수 \(x_i\)와 그 부정 \(\lnot x_i\)를 노드로 표현한다.
   - 각 절 \((A \lor B)\)는 두 개의 임플리케이션으로 변환된다:
     - \(\lnot A \rightarrow B\)
     - \(\lnot B \rightarrow A\)
   - 이로써 그래프의 간선이 정의된다.

2. **강한 연결 요소 찾기**:

   - 그래프에서 SCC를 찾기 위해 **Kosaraju's Algorithm**을 사용한다.
   - 만약 어떤 변수 \(x_i\)와 그 부정 \(\lnot x_i\)가 같은 SCC에 속한다면, 모순이 발생하므로 식을 참으로 만들 수 없다.

3. **변수 값 할당**:

   - SCC의 위상 정렬 결과를 이용하여 변수의 값을 결정한다.
   - SCC의 순서에 따라 변수를 참 또는 거짓으로 할당한다.

이러한 접근 방식은 시간 복잡도 \(O(N + M)\)으로 문제를 해결할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAX_N = 10000;

int N, M;
vector<int> adj[MAX_N * 2];       // 임플리케이션 그래프
vector<int> adj_rev[MAX_N * 2];   // 역 그래프
vector<int> order;                // 노드 방문 순서
int scc_id[MAX_N * 2];            // 각 노드의 SCC ID
bool visited[MAX_N * 2];

// 변수 번호를 인덱스로 변환
int var(int x) {
    return x > 0 ? (x - 1) * 2 : (-x - 1) * 2 + 1;
}

// 1차 DFS: 노드 방문 순서 기록
void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs1(v);
    }
    order.push_back(u);
}

// 2차 DFS: SCC 구성
void dfs2(int u, int id) {
    scc_id[u] = id;
    for (int v : adj_rev[u]) {
        if (scc_id[v] == -1) dfs2(v, id);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M;

    // 그래프 구성
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        int u = var(a);
        int v = var(b);
        // \lnot a -> b
        adj[u ^ 1].push_back(v);
        adj_rev[v].push_back(u ^ 1);
        // \lnot b -> a
        adj[v ^ 1].push_back(u);
        adj_rev[u].push_back(v ^ 1);
    }

    // 1차 DFS 수행
    for (int i = 0; i < N * 2; ++i) {
        if (!visited[i]) dfs1(i);
    }

    // SCC 초기화
    fill(scc_id, scc_id + N * 2, -1);

    // 2차 DFS 수행
    int id = 0;
    for (int i = N * 2 - 1; i >= 0; --i) {
        int u = order[i];
        if (scc_id[u] == -1) dfs2(u, id++);
    }

    // 모순 검사
    for (int i = 0; i < N; ++i) {
        if (scc_id[i * 2] == scc_id[i * 2 + 1]) {
            cout << 0 << '\n';
            return 0;
        }
    }

    // 변수 값 결정
    vector<int> result(N);
    for (int i = 0; i < N; ++i) {
        result[i] = scc_id[i * 2] > scc_id[i * 2 + 1] ? 1 : 0;
    }

    // 결과 출력
    cout << 1 << '\n';
    for (int i = 0; i < N; ++i) {
        cout << result[i] << ' ';
    }
    cout << '\n';

    return 0;
}
```

### 코드 설명

- **그래프 구성**:

  - 각 변수와 그 부정을 노드로 표현하여 \(2N\)개의 노드를 사용한다.
  - `var()` 함수는 입력된 리터럴을 노드 인덱스로 변환한다.
  - 각 절에 대해 임플리케이션 간선을 추가한다.

- **DFS를 통한 SCC 찾기**:

  - `dfs1()` 함수는 그래프를 탐색하여 노드 방문 순서를 기록한다.
  - `dfs2()` 함수는 역 그래프에서 SCC를 찾는다.
  - SCC ID를 부여하여 각 노드가 속한 SCC를 식별한다.

- **모순 검사 및 결과 결정**:

  - 각 변수와 그 부정이 같은 SCC에 속하면 모순이므로 불가능한 경우이다.
  - SCC ID를 비교하여 변수의 값을 결정한다.
    - SCC ID가 큰 쪽이 더 나중에 결정되므로, 이를 참으로 설정한다.

- **결과 출력**:

  - 식을 만족할 수 있다면 `1`을 출력하고, 각 변수의 값을 순서대로 출력한다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(1000000)

N, M = map(int, sys.stdin.readline().split())
adj = [[] for _ in range(N * 2)]
adj_rev = [[] for _ in range(N * 2)]

def var(x):
    return (abs(x) - 1) * 2 + (0 if x > 0 else 1)

for _ in range(M):
    a, b = map(int, sys.stdin.readline().split())
    u = var(a)
    v = var(b)
    adj[u ^ 1].append(v)
    adj[v ^ 1].append(u)
    adj_rev[v].append(u ^ 1)
    adj_rev[u].append(v ^ 1)

visited = [False] * (N * 2)
order = []

def dfs1(u):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs1(v)
    order.append(u)

def dfs2(u, label):
    scc_id[u] = label
    for v in adj_rev[u]:
        if scc_id[v] == -1:
            dfs2(v, label)

for i in range(N * 2):
    if not visited[i]:
        dfs1(i)

scc_id = [-1] * (N * 2)
label = 0
for u in reversed(order):
    if scc_id[u] == -1:
        dfs2(u, label)
        label += 1

for i in range(N):
    if scc_id[i * 2] == scc_id[i * 2 + 1]:
        print(0)
        sys.exit(0)

result = [0] * N
for i in range(N):
    result[i] = 1 if scc_id[i * 2] > scc_id[i * 2 + 1] else 0

print(1)
print(' '.join(map(str, result)))
```

### 코드 설명

- **그래프 구성**:

  - 리스트를 사용하여 그래프와 역 그래프를 구성한다.
  - 입력된 절을 임플리케이션으로 변환하여 간선을 추가한다.

- **DFS를 통한 SCC 찾기**:

  - 재귀 함수를 사용하여 DFS를 수행한다.
  - Python의 재귀 한도를 늘려야 하므로 `sys.setrecursionlimit`을 설정한다.

- **모순 검사 및 결과 결정**:

  - 변수와 그 부정의 SCC ID를 비교하여 모순 여부를 판단한다.
  - 변수 값은 SCC ID를 기반으로 결정한다.

- **결과 출력**:

  - 식을 만족할 수 있다면 `1`을 출력하고, 변수 값을 출력한다.

## 결론

이번 문제는 2-SAT 알고리즘의 전형적인 적용 예시였다. 임플리케이션 그래프와 SCC를 활용하여 효율적으로 해결할 수 있었다. 이러한 문제를 통해 그래프 이론과 논리 회로의 접점을 이해할 수 있었다. 추가적인 최적화 방안으로는 메모리 사용을 줄이기 위해 인접 리스트를 효율적으로 관리하는 방법 등이 있을 것이다.