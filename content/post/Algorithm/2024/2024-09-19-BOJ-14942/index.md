---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-19T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- BinaryLifting
- TreeTraversal
- Implementation
- Optimization
- O(NlogN)
- GraphTheory
- DynamicProgramming
- GraphTraversal
title: '[Algorithm] C++/Python 백준 14942번 : 개미'
---

개미집은 n개의 방으로 구성되어 있으며, 이 방들은 1번부터 n번까지 번호가 부여되어 있다. 1번 방은 지면에 직접 연결되어 있는 방으로, 모든 개미는 이 방을 통해 지면으로 올라가고자 한다. 각 방은 서로 굴을 통해 연결되어 있으며, 굴을 이동하는 데는 굴의 길이만큼의 에너지가 소모된다. 개미들은 겨울잠에서 깨어나 지면으로 올라가기 위해 에너지를 사용하지만, 에너지가 부족하여 중간에 멈출 수 있다. 이 문제에서는 각 개미가 가진 에너지를 바탕으로, 도달할 수 있는 가장 1번 방에 가까운 방의 번호를 구하는 것이 목표이다.

문제 : [https://www.acmicpc.net/problem/14942](https://www.acmicpc.net/problem/14942)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 트리 구조에서 각 노드(방) 간의 거리를 효율적으로 계산하고, 주어진 에너지로 최대로 가까운 1번 방에 도달할 수 있는 노드를 찾는 문제이다. 트리는 사이클이 없고, 모든 노드 간의 경로가 유일하기 때문에, 각 노드에서 1번 노드로 가는 경로가 명확하다.

효율적인 해결을 위해 다음과 같은 접근 방식을 사용하였다:

1. **트리 구성 및 거리 계산**:
   - 주어진 방과 굴 정보를 바탕으로 트리를 구성한다.
   - 깊이 우선 탐색(DFS)을 통해 각 방에서 1번 방까지의 누적 거리를 계산한다.

2. **이진 승격(Binary Lifting) 기법 적용**:
   - 이진 승격을 사용하여 각 노드의 2^k 번째 조상을 미리 계산한다.
   - 이를 통해 특정 에너지 내에서 도달 가능한 가장 가까운 조상을 빠르게 찾을 수 있다.

3. **각 개미의 도달 가능한 방 찾기**:
   - 각 개미의 에너지에 따라, 해당 에너지 내에서 도달할 수 있는 가장 가까운 방을 이진 승격을 통해 탐색한다.

이진 승격 기법을 사용함으로써, 각 개미의 도달 가능한 방을 O(log N) 시간에 찾을 수 있으며, 전체적으로 O(N log N)의 시간 복잡도로 문제를 해결할 수 있다.

## C++ 코드와 설명

아래는 최적화된 C++ 코드와 각 라인에 대한 설명이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const int MAX = 100005;
const int LOG = 17; // 2^17 > 1e5

int n;
ll E_val[MAX];           // 각 방에 있는 개미의 에너지
ll dist_val[MAX];       // 1번 방부터 각 방까지의 거리
int up[LOG][MAX];       // 이진 승격을 위한 테이블
vector<pair<int, ll>> adj[MAX]; // 트리의 인접 리스트

// DFS를 통해 각 방의 부모와 거리를 계산
void dfs(int u, int p){
    up[0][u] = p;
    for(auto &[v, w] : adj[u]){
        if(v != p){
            dist_val[v] = dist_val[u] + w;
            dfs(v, u);
        }
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    cin >> n;
    for(int u=1; u<=n; u++) cin >> E_val[u];
    for(int i=0; i<n-1; i++){
        int a, b;
        ll c;
        cin >> a >> b >> c;
        adj[a].emplace_back(b, c);
        adj[b].emplace_back(a, c);
    }
    
    // 1번 방을 루트로 DFS 수행
    dist_val[1] = 0;
    dfs(1, -1);
    
    // 이진 승격 테이블 구축
    for(int k=1; k<LOG; k++){
        for(int u=1; u<=n; u++){
            if(up[k-1][u] != -1){
                up[k][u] = up[k-1][up[k-1][u]];
            }
            else{
                up[k][u] = -1;
            }
        }
    }
    
    // 특정 방 u에서 에너지 E를 사용해 도달할 수 있는 가장 가까운 방 찾기
    auto get_ancestor = [&](int u, ll E) -> int {
        ll target_dist = dist_val[u] - E;
        if(target_dist <= 0){
            return 1;
        }
        int current = u;
        for(int k=LOG-1; k>=0; k--){
            if(up[k][current] != -1 && dist_val[up[k][current]] >= target_dist){
                current = up[k][current];
            }
        }
        return current;
    };
    
    // 각 개미에 대해 결과 출력
    for(int u=1; u<=n; u++){
        int v = get_ancestor(u, E_val[u]);
        cout << v << "\n";
    }
}
```

**코드 설명**

1. **입력 처리**:
   - `n`과 각 방에 있는 개미의 에너지 값을 입력받는다.
   - `n-1`개의 굴 정보를 입력받아 트리를 인접 리스트로 구성한다.

2. **DFS를 통한 거리 및 부모 노드 계산**:
   - 1번 방을 루트로 설정하고 DFS를 수행하여 각 방까지의 거리(`dist_val`)와 부모 노드(`up[0][u]`)를 계산한다.

3. **이진 승격 테이블 구축**:
   - 각 방에 대해 2^k 번째 조상을 미리 계산하여 `up` 테이블을 구축한다. 이는 나중에 특정 에너지 내에서 빠르게 조상을 찾기 위함이다.

4. **조상 찾기 함수 `get_ancestor`**:
   - 특정 방 `u`에서 에너지 `E`를 사용하여 도달할 수 있는 방을 찾는다.
   - 목표 거리를 `dist_val[u] - E`로 설정하고, 이진 승격을 통해 해당 거리 이상을 유지하면서 가능한 가장 높은 조상을 찾는다.

5. **결과 출력**:
   - 각 방의 개미에 대해 `get_ancestor` 함수를 호출하여 도달 가능한 방을 찾고, 그 방의 번호를 출력한다.

## C++ without library 코드와 설명

이전 코드에서는 `head` 배열의 초기화 시점이 잘못되어 간선이 제대로 추가되지 않는 문제가 있었습니다. 이를 수정하여 올바르게 동작하는 코드를 제공하겠습니다.

```cpp
#include <stdio.h>
#include <stdlib.h>

typedef long long ll;

#define MAX 100005
#define LOG 17

ll E_val[MAX];
ll dist_val[MAX];
int up_table[LOG][MAX];
int head[MAX], to_arr[MAX*2], cost_arr[MAX*2], next_arr[MAX*2];
int cnt = 0;

// 간선 추가 함수
void add_edge(int a, int b, ll c){
    to_arr[cnt] = b;
    cost_arr[cnt] = c;
    next_arr[cnt] = head[a];
    head[a] = cnt++;
}

void dfs(int u, int p){
    up_table[0][u] = p;
    for(int i = head[u]; i != -1; i = next_arr[i]){
        int v = to_arr[i];
        ll w = cost_arr[i];
        if(v != p){
            dist_val[v] = dist_val[u] + w;
            dfs(v, u);
        }
    }
}

int main(){
    int n;
    scanf("%d", &n);
    
    // 에너지 값 입력
    for(int u=1; u<=n; u++) scanf("%lld", &E_val[u]);
    
    // head 배열 초기화 (간선 추가 전에 초기화해야 함)
    for(int i=1; i<=n; i++) head[i] = -1;
    
    // 간선 입력 및 추가
    for(int i=0; i<n-1; i++){
        int a, b;
        ll c;
        scanf("%d %d %lld", &a, &b, &c);
        add_edge(a, b, c);
        add_edge(b, a, c);
    }
    
    // DFS 수행하여 거리 및 부모 노드 계산
    dist_val[1] = 0;
    dfs(1, -1);
    
    // 이진 승격 테이블 구축
    for(int k=1; k<LOG; k++){
        for(int u=1; u<=n; u++){
            if(up_table[k-1][u] != -1){
                up_table[k][u] = up_table[k-1][up_table[k-1][u]];
            }
            else{
                up_table[k][u] = -1;
            }
        }
    }
    
    // 각 개미에 대해 도달 가능한 방 찾기
    for(int u=1; u<=n; u++){
        ll E = E_val[u];
        ll target_dist = dist_val[u] - E;
        if(target_dist <= 0){
            printf("1\n");
            continue;
        }
        int current = u;
        for(int k=LOG-1; k>=0; k--){
            if(up_table[k][current] != -1 && dist_val[up_table[k][current]] >= target_dist){
                current = up_table[k][current];
            }
        }
        printf("%d\n", current);
    }
}
```

**코드 설명**

1. **입력 처리 및 간선 추가**:
   - `scanf`를 사용하여 입력을 빠르게 처리한다.
   - **중요**: 간선을 추가하기 전에 `head` 배열을 `-1`로 초기화한다. 이는 간선이 올바르게 추가되도록 보장하기 위함이다.
   - `add_edge` 함수를 통해 인접 리스트를 배열로 구현한다.

2. **DFS를 통한 거리 및 부모 노드 계산**:
   - DFS를 수행하여 각 방까지의 거리(`dist_val`)와 부모 노드(`up_table[0][u]`)를 계산한다.

3. **이진 승격 테이블 구축**:
   - 표준 라이브러리를 사용하지 않고, 배열을 통해 이진 승격 테이블을 구축한다.

4. **조상 찾기 및 결과 출력**:
   - 각 방의 개미에 대해 에너지에 따라 도달 가능한 방을 찾아 `printf`로 출력한다.

**수정 사항**:
- **`head` 배열 초기화 시점 변경**: 간선을 추가하기 전에 `head[i]`를 `-1`로 초기화하도록 수정하였다. 이는 간선 추가 시 인접 리스트가 올바르게 구성되도록 보장한다.

## Python 코드와 설명

아래는 최적화된 Python 코드와 각 라인에 대한 설명이다.

```python
import sys
sys.setrecursionlimit(1 << 25)
from sys import stdin
def input():
    return sys.stdin.readline()

n = int(input())
E_val = [0] + [int(input()) for _ in range(n)]
adj = [[] for _ in range(n+1)]
for _ in range(n-1):
    a, b, c = map(int, input().split())
    adj[a].append((b, c))
    adj[b].append((a, c))

LOG = 17
up = [[-1]*(n+1) for _ in range(LOG)]
dist_val = [0]*(n+1)

def dfs(u, p):
    up[0][u] = p
    for v, w in adj[u]:
        if v != p:
            dist_val[v] = dist_val[u] + w
            dfs(v, u)

dfs(1, -1)

for k in range(1, LOG):
    for u in range(1, n+1):
        if up[k-1][u] != -1:
            up[k][u] = up[k-1][up[k-1][u]]

def get_ancestor(u, E):
    target_dist = dist_val[u] - E
    if target_dist <= 0:
        return 1
    current = u
    for k in reversed(range(LOG)):
        if up[k][current] != -1 and dist_val[up[k][current]] >= target_dist:
            current = up[k][current]
    return current

for u in range(1, n+1):
    v = get_ancestor(u, E_val[u])
    print(v)
```

**코드 설명**

1. **입력 처리**:
   - `sys.stdin.readline()`을 사용하여 빠르게 입력을 처리한다.
   - `sys.setrecursionlimit`을 설정하여 깊은 재귀를 허용한다.

2. **트리 구성 및 DFS 수행**:
   - 인접 리스트를 구성하고, DFS를 통해 각 방까지의 거리와 부모 노드를 계산한다.

3. **이진 승격 테이블 구축**:
   - 이진 승격 테이블을 리스트로 구현하여 각 노드의 2^k 번째 조상을 미리 계산한다.

4. **조상 찾기 함수 `get_ancestor`**:
   - 특정 방에서 에너지 내에서 도달 가능한 가장 가까운 조상을 이진 승격을 통해 찾는다.

5. **결과 출력**:
   - 각 방의 개미에 대해 도달 가능한 방을 출력한다.

## 결론

이번 문제는 트리 구조에서 각 노드 간의 거리를 효율적으로 계산하고, 이를 바탕으로 각 개미가 도달할 수 있는 방을 빠르게 찾는 문제였다. 이진 승격(Binary Lifting) 기법을 활용하여, 각 개미의 도달 가능한 방을 O(log N) 시간에 찾을 수 있었으며, 전체적으로 O(N log N)의 시간 복잡도로 문제를 해결할 수 있었다.

문제를 풀면서 트리 구조와 이진 승격 기법에 대한 이해를 더욱 깊게 할 수 있었으며, 이러한 기법들이 실제 문제에서 어떻게 적용될 수 있는지를 체험할 수 있었다. 추가적으로, Python과 C++ 두 가지 언어로 구현함으로써, 각 언어의 장단점을 비교해볼 수 있는 좋은 기회가 되었다. 앞으로도 다양한 트리 관련 문제를 풀면서 이진 승격을 비롯한 다양한 최적화 기법들을 익혀 나가고자 한다.