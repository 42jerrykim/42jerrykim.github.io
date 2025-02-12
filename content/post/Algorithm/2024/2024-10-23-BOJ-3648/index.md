---
title: "[Algorithm] C++/Python 백준 3648번 : 아이돌"
categories: 
- Algorithm
- Graph
- 2-SAT
- StronglyConnectedComponents
tags:
- 2-SAT
- SCC
- ImplicationGraph
- KosarajuAlgorithm
- O(N)
- Graph
- Logic
- SatisfiabilityProblem
- StronglyConnectedComponents
image: "tmp_wordcloud.png"
date: 2024-01-01
---

최근 알고리즘 문제 해결에 있어서 논리적 추론과 그래프 이론을 결합한 문제들이 많이 출제되고 있다. 특히 2-SAT 문제는 논리식의 만족 가능성을 판단하는 중요한 문제 유형 중 하나이다. 이번 포스팅에서는 백준 온라인 저지의 3648번 문제인 "아이돌"을 다루어 보려고 한다. 이 문제는 2-SAT와 강한 연결 요소(SCC)를 활용하여 해결할 수 있으며, 효율적인 알고리즘 설계를 통해 문제를 풀어볼 것이다.

문제 : [https://www.acmicpc.net/problem/3648](https://www.acmicpc.net/problem/3648)

## 문제 설명

아이돌 선발 대회에서 참가자들은 심사위원들의 투표를 통해 다음 라운드로 진출할 수 있다. 각 심사위원은 두 개의 투표를 하는데, 특정 참가자의 진출을 찬성하거나 반대하는 투표를 할 수 있다. 투표 결과에 따라 참가자들은 다음 라운드로 진출하게 되는데, 몇 명이 진출할지는 미리 정해져 있지 않다. 만약 모든 참가자가 훌륭하다면 모두 진출할 수도 있고, 반대로 모두 떨어질 수도 있다.

참가자 중 한 명인 카를은 자신의 프로그래밍 실력을 심사위원들이 인정해주지 않을 것을 걱정하여 해킹을 통해 자신이 다음 라운드에 진출하도록 시스템을 조작하려 한다. 하지만 모든 심사위원들은 자신의 두 투표 중 적어도 하나는 최종 결과와 일치하길 기대한다. 만약 심사위원의 두 투표 모두 결과와 모순된다면, 의심을 품고 조사에 들어갈 것이다.

카를은 자신이 진출하면서도 심사위원들의 의심을 사지 않도록 결과를 조작하려 한다. 이를 위해, 심사위원들의 투표 정보를 바탕으로 어떤 참가자들이 다음 라운드로 진출해야 하는지를 결정해야 한다.

**입력**

- 여러 개의 테스트 케이스로 이루어져 있으며, 각 테스트 케이스는 다음과 같다:
  - 첫 번째 줄에 참가자 수 \( n \) (\( 2 \leq n < 1000 \))와 심사위원 수 \( m \) (\( 1 \leq m < 2000 \))이 주어진다.
  - 다음 \( m \)개의 줄에는 각 심사위원의 투표가 주어진다. 각 줄은 두 개의 정수 \( a \)와 \( b \)로 이루어져 있으며, \( |a| \neq |b| \)이다. \( a \)나 \( b \)가 양수이면 해당 참가자의 진출을 찬성하는 투표이며, 음수이면 반대하는 투표이다.

- 참가자는 \( 1 \)부터 \( n \)까지 번호가 매겨져 있으며, 카를은 참가자 \( 1 \)번이다.

**출력**

- 각 테스트 케이스마다 카를이 심사위원들의 의심을 사지 않으면서 다음 라운드로 진출할 수 있으면 "yes"를, 그렇지 않으면 "no"를 출력한다.

## 접근 방식

이 문제는 **2-SAT** 문제로 모델링할 수 있다. 각 참가자에 대해 변수 \( X_i \)를 정의하고, 참가자가 다음 라운드에 진출하면 \( X_i \)를 참, 그렇지 않으면 거짓으로 나타낸다. 심사위원들의 투표는 다음과 같은 제약 조건으로 표현할 수 있다.

- 각 심사위원은 두 개의 투표를 한다. 그 중 **적어도 하나**는 결과와 일치해야 한다.
- 심사위원의 첫 번째 투표를 \( A \), 두 번째 투표를 \( B \)라고 할 때, 다음과 같은 절을 얻을 수 있다: \( A \lor B \)

여기서 \( A \)와 \( B \)는 각각 참가자의 진출(찬성 투표, \( X_i \)) 또는 탈락(반대 투표, \( \lnot X_i \))에 대한 리터럴이다.

또한, **카를(참가자 1번)은 반드시 진출해야 하므로 \( X_1 \)은 참이어야 한다**.

이를 기반으로 논리식을 구성하고, 이 논리식의 만족 가능성을 판단하기 위해 **2-SAT 알고리즘**을 적용한다. 2-SAT 문제는 임플리케이션 그래프를 생성하고, **강한 연결 요소(SCC)**를 찾아 해결할 수 있다.

## C++ 코드와 설명

임플리케이션 그래프를 생성하고 Kosaraju 알고리즘을 활용하여 SCC를 찾는 C++ 코드를 작성한다.

```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

using namespace std;

const int MAXN = 2000; // 최대 참가자 수의 두 배

int n, m; // 참가자 수, 심사위원 수
vector<int> adj[MAXN * 2]; // 임플리케이션 그래프
vector<int> radj[MAXN * 2]; // 역방향 그래프
vector<int> sccId(MAXN * 2, -1); // 각 노드의 SCC ID
vector<bool> visited(MAXN * 2, false);
vector<int> order;
int id = 0;

// 변수의 인덱스를 얻는 함수
int var(int x) {
    return (abs(x) - 1) * 2 + (x < 0);
}

// 임플리케이션 그래프의 DFS
void dfs(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v])
            dfs(v);
    }
    order.push_back(u);
}

// 역방향 그래프의 DFS
void reverseDfs(int u, int label) {
    sccId[u] = label;
    for (int v : radj[u]) {
        if (sccId[v] == -1)
            reverseDfs(v, label);
    }
}

int main() {
    while (cin >> n >> m) {
        // 초기화
        for (int i = 0; i < n * 2; ++i) {
            adj[i].clear();
            radj[i].clear();
            sccId[i] = -1;
            visited[i] = false;
        }
        id = 0;
        order.clear();
        
        // 심사위원들의 투표 입력
        for (int i = 0; i < m; ++i) {
            int a, b;
            cin >> a >> b;
            adj[var(-a)].push_back(var(b));
            radj[var(b)].push_back(var(-a));
            adj[var(-b)].push_back(var(a));
            radj[var(a)].push_back(var(-b));
        }
        
        // 카를은 반드시 진출해야 하므로 X1은 참
        adj[var(-1)].push_back(var(1));
        radj[var(1)].push_back(var(-1));
        
        // 1차 DFS로 완료 순서 저장
        for (int i = 0; i < n * 2; ++i) {
            if (!visited[i])
                dfs(i);
        }
        
        // 2차 DFS로 SCC 찾기
        int label = 0;
        for (int i = n * 2 - 1; i >= 0; --i) {
            int u = order[i];
            if (sccId[u] == -1)
                reverseDfs(u, label++);
        }
        
        // 모순 확인
        bool isPossible = true;
        for (int i = 0; i < n; ++i) {
            if (sccId[i * 2] == sccId[i * 2 + 1]) {
                isPossible = false;
                break;
            }
        }
        
        if (isPossible)
            cout << "yes" << endl;
        else
            cout << "no" << endl;
    }
    return 0;
}
```

### 코드 설명

1. **var 함수**

   ```cpp
   int var(int x) {
       return (abs(x) - 1) * 2 + (x < 0);
   }
   ```

   - 변수 \( x \)에 대한 그래프 노드의 인덱스를 계산한다.
   - 각 변수는 두 개의 노드로 표현되며, 참과 거짓에 해당한다.
   - \( x < 0 \)이면 거짓을 나타내는 노드 인덱스를 반환한다.

2. **dfs 함수**

   ```cpp
   void dfs(int u) {
       visited[u] = true;
       for (int v : adj[u]) {
           if (!visited[v])
               dfs(v);
       }
       order.push_back(u);
   }
   ```

   - 임플리케이션 그래프에서의 DFS를 수행하여 완료 순서대로 노드를 저장한다.

3. **reverseDfs 함수**

   ```cpp
   void reverseDfs(int u, int label) {
       sccId[u] = label;
       for (int v : radj[u]) {
           if (sccId[v] == -1)
               reverseDfs(v, label);
       }
   }
   ```

   - 역방향 그래프에서의 DFS를 수행하여 SCC를 찾는다.

4. **메인 함수**

   - 입력을 받아 임플리케이션 그래프와 역방향 그래프를 구성한다.
   - 카를은 반드시 진출해야 하므로 \( X_1 \)이 참이 되도록 간선을 추가한다.
   - 두 번의 DFS를 통해 SCC를 찾는다.
   - 각 변수와 그 부정이 같은 SCC에 있다면 모순이 발생하므로 불가능한 경우이다.

## C++ without library 코드와 설명

C 라이브러리만을 사용하여 동일한 기능을 구현한다.

```cpp
#include <stdio.h>
#include <stdlib.h>
#define MAXN 2000

int n, m;
int adj[MAXN * 2][MAXN * 2];
int adjSize[MAXN * 2];
int radj[MAXN * 2][MAXN * 2];
int radjSize[MAXN * 2];
int sccId[MAXN * 2];
int visited[MAXN * 2];
int stack[MAXN * 2];
int top;

int var(int x) {
    return (abs(x) - 1) * 2 + (x < 0);
}

void dfs(int u) {
    visited[u] = 1;
    for (int i = 0; i < adjSize[u]; ++i) {
        int v = adj[u][i];
        if (!visited[v])
            dfs(v);
    }
    stack[top++] = u;
}

void reverseDfs(int u, int label) {
    sccId[u] = label;
    for (int i = 0; i < radjSize[u]; ++i) {
        int v = radj[u][i];
        if (sccId[v] == -1)
            reverseDfs(v, label);
    }
}

int main() {
    while (scanf("%d %d", &n, &m) != EOF) {
        for (int i = 0; i < n * 2; ++i) {
            adjSize[i] = 0;
            radjSize[i] = 0;
            sccId[i] = -1;
            visited[i] = 0;
        }
        top = 0;
        for (int i = 0; i < m; ++i) {
            int a, b;
            scanf("%d %d", &a, &b);
            adj[var(-a)][adjSize[var(-a)]++] = var(b);
            radj[var(b)][radjSize[var(b)]++] = var(-a);
            adj[var(-b)][adjSize[var(-b)]++] = var(a);
            radj[var(a)][radjSize[var(a)]++] = var(-b);
        }
        adj[var(-1)][adjSize[var(-1)]++] = var(1);
        radj[var(1)][radjSize[var(1)]++] = var(-1);
        for (int i = 0; i < n * 2; ++i) {
            if (!visited[i])
                dfs(i);
        }
        int label = 0;
        while (top > 0) {
            int u = stack[--top];
            if (sccId[u] == -1)
                reverseDfs(u, label++);
        }
        int isPossible = 1;
        for (int i = 0; i < n; ++i) {
            if (sccId[i * 2] == sccId[i * 2 + 1]) {
                isPossible = 0;
                break;
            }
        }
        if (isPossible)
            printf("yes\n");
        else
            printf("no\n");
    }
    return 0;
}
```

### 코드 설명

- **배열 초기화**

  - 동적 배열 대신 고정 크기의 배열을 사용하여 그래프를 구현한다.
  - `adj`와 `radj` 배열은 인접 리스트를 2차원 배열로 표현한다.
  - `adjSize`와 `radjSize` 배열은 각 노드의 인접 노드 수를 저장한다.

- **dfs 함수**

  - 임플리케이션 그래프에서 DFS를 수행하여 완료 순서대로 스택에 노드를 저장한다.

- **reverseDfs 함수**

  - 역방향 그래프에서 DFS를 수행하여 SCC를 찾는다.

- **메인 함수**

  - C 스타일의 입출력을 사용하며, 메모리 할당도 `malloc` 없이 구현한다.
  - 로직은 이전의 C++ 코드와 동일하다.

## Python 코드와 설명

Python으로 동일한 알고리즘을 구현한다.

```python
import sys
sys.setrecursionlimit(1000000)

MAXN = 2000

def var(x):
    return (abs(x) - 1) * 2 + (x < 0)

def dfs(u):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs(v)
    order.append(u)

def reverse_dfs(u, label):
    scc_id[u] = label
    for v in radj[u]:
        if scc_id[v] == -1:
            reverse_dfs(v, label)

while True:
    try:
        line = ''
        while line.strip() == '':
            line = sys.stdin.readline()
            if not line:
                exit()
        n, m = map(int, line.strip().split())
        adj = [[] for _ in range(n * 2)]
        radj = [[] for _ in range(n * 2)]
        visited = [False] * (n * 2)
        scc_id = [-1] * (n * 2)
        order = []
        for _ in range(m):
            a, b = map(int, sys.stdin.readline().split())
            adj[var(-a)].append(var(b))
            radj[var(b)].append(var(-a))
            adj[var(-b)].append(var(a))
            radj[var(a)].append(var(-b))
        adj[var(-1)].append(var(1))
        radj[var(1)].append(var(-1))
        for i in range(n * 2):
            if not visited[i]:
                dfs(i)
        label = 0
        for u in reversed(order):
            if scc_id[u] == -1:
                reverse_dfs(u, label)
                label += 1
        is_possible = True
        for i in range(n):
            if scc_id[i * 2] == scc_id[i * 2 + 1]:
                is_possible = False
                break
        print("yes" if is_possible else "no")
    except EOFError:
        break
```

### 코드 설명

1. **var 함수**

   ```python
   def var(x):
       return (abs(x) - 1) * 2 + (x < 0)
   ```

   - 변수 \( x \)에 대한 노드 인덱스를 계산한다.

2. **dfs 함수**

   ```python
   def dfs(u):
       visited[u] = True
       for v in adj[u]:
           if not visited[v]:
               dfs(v)
       order.append(u)
   ```

   - 임플리케이션 그래프에서 DFS를 수행하여 완료 순서를 기록한다.

3. **reverse_dfs 함수**

   ```python
   def reverse_dfs(u, label):
       scc_id[u] = label
       for v in radj[u]:
           if scc_id[v] == -1:
               reverse_dfs(v, label)
   ```

   - 역방향 그래프에서 DFS를 수행하여 SCC를 찾는다.

4. **메인 루프**

   - 입력을 받아 그래프를 구성한다.
   - 카를이 반드시 진출하도록 간선을 추가한다.
   - 두 번의 DFS를 통해 SCC를 찾는다.
   - 모순 여부를 확인하여 결과를 출력한다.

## 결론

이번 문제는 2-SAT 알고리즘과 강한 연결 요소(SCC)를 활용하여 논리식의 만족 가능성을 판단하는 전형적인 문제였다. 임플리케이션 그래프를 구성하고, Kosaraju 알고리즘을 통해 효율적으로 해결할 수 있었다. 앞서 제공한 코드에서 역방향 그래프를 올바르게 처리하지 못한 부분이 있었는데, 이를 수정하여 문제를 해결할 수 있었다. 이러한 유형의 문제를 통해 그래프 이론과 논리식 처리에 대한 이해를 더욱 깊게 할 수 있었다. 추가적인 최적화 방안으로는 Tarjan 알고리즘을 활용하여 한 번의 DFS로 SCC를 찾는 방법도 고려할 수 있다.
