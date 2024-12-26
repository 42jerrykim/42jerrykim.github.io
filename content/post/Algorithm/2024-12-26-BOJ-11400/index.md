---
title: "[Algorithm] C++/Python 백준 11400번 : 단절선"
categories: 
- Algorithm
tags:
- Implementation
- Optimization
- O(V+E)
- Graph Theory
- Graph Traversal
image: "tmp_wordcloud.png"
date: 2024-12-26
---

문제 해결에 있어 그래프 이론에서 중요한 개념 중 하나인 단절선을 찾는 문제를 다루고자 한다. 해당 문제는 간선을 제거함으로써 그래프의 연결 요소가 증가하는지를 판별해야 하며, 이 작업을 효율적으로 수행하기 위해서는 DFS(Depth First Search)를 활용한 Tarjan’s Algorithm을 적용할 수 있다. 본 글에서는 문제 설명과 알고리즘 접근 방식, C++와 Python을 이용한 예시 코드를 자세하게 소개하고자 한다.이다.

문제 : [https://www.acmicpc.net/problem/11400](https://www.acmicpc.net/problem/11400)

---

## 문제 설명

해당 문제에서는 V개의 정점과 E개의 간선으로 이루어진 연결 그래프가 주어진다. 정점은 1번부터 V번까지 존재하며, 두 정점 A와 B가 간선으로 직접 연결되어 있으면 양방향으로 인접 관계를 갖는다. 우리가 해결해야 하는 핵심 목표는 다음과 같다. 특정 간선을 제거했을 때, 전체 그래프가 여러 개의 연결 요소로 분리되는 경우가 존재한다면, 그 간선은 단절선(bridge)으로 정의된다. 문제에서는 모든 단절선을 찾아내어, 해당 간선을 오름차순(사전순)으로 정렬하여 출력해야 한다. 이때 간선 (A, B)는 A < B인 형태로만 출력하면 되며, 같은 간선을 중복으로 표기하지 않아야 한다.

그래프가 항상 연결 상태를 유지한다고 했을 때, 모든 간선에 대해 "이 간선을 제거하면 연결 요소가 증가하는가"를 단순 순회 방식으로 판별한다면, 최악의 경우 \(O(E \times (V+E))\)에 달하는 큰 시간 복잡도가 발생할 수 있다. 이는 E가 최대 1,000,000에 이르는 대규모 그래프에서 매우 비효율적인 방식이다. 따라서 더 효율적인 단절선 판별 알고리즘이 필요하다.

이를 해결하기 위해서는 DFS를 기반으로 하는 Tarjan’s Algorithm을 사용할 수 있다. DFS를 수행하면서 정점에 '방문 순서'(discovery time)를 매기고, 역방향 간선을 통해 도달할 수 있는 가장 빠른 방문 순서를 기록하여 단절선을 빠르게 찾아낼 수 있다. Tarjan’s Algorithm에서는 각 정점마다 두 가지 중요한 값을 저장한다.

1. **disc[v]**: 정점 v를 방문했을 때 부여하는 방문 순서.
2. **lowv[v]**: 정점 v에서 출발하여 v의 자손 정점들을 통해 도달할 수 있는 가장 빠른 (가장 작은) 방문 순서.

간선 (u, v)가 있을 때, lowv[v]가 disc[u]보다 크다면 간선 (u, v)는 단절선이 된다. 이는 v를 루트로 하는 서브트리에서 u보다 더 이전에 방문한 정점으로 이어지는 역방향 경로가 없음을 의미하므로, (u, v)를 제거하면 v가 포함된 부분 그래프가 분리되게 된다. 이 논리를 모든 간선에 대해 적용하면, 해당 그래프의 모든 단절선을 찾을 수 있다.

문제를 요약하자면, 넓은 범위의 V와 E가 주어지는 상황에서 가능한 한 빠른 시간 안에 모든 단절선을 찾아내고, 그 목록을 정렬하여 출력해야 한다는 것이다. 이 문제는 연결 그래프의 구조적 특성을 살펴볼 수 있으며, DFS와 같은 그래프 순회 알고리즘의 응용 능력 또한 요구한다. 또한, 메모리 제약 하에서 대규모 데이터를 효율적으로 처리하기 위한 인접 리스트 구조를 어떻게 설계하고 구현할지 고민해야 한다.이다.

---

## 접근 방식

1. **인접 리스트 구성**  
   입력받은 V와 E에 따라 각 정점에 연결된 간선 정보를 인접 리스트에 저장한다. 이는 E가 매우 큰 상황에서도 비교적 빠르게 그래프 순회를 처리하기 위함이다.

2. **DFS 기반 Tarjan’s Algorithm**  
   - 모든 정점에 대해 아직 방문하지 않았다면 DFS를 수행한다.  
   - DFS 진행 중, 현재 정점 curr에 방문 순서 disc[curr]를 할당하고, lowv[curr] 값을 disc[curr]로 초기화한다.  
   - curr와 인접한 nxt 정점을 방문할 때, nxt가 방문하지 않은 정점이면 재귀적으로 DFS를 호출하고, lowv[curr]를 lowv[nxt]와 비교하여 더 작은 값을 업데이트한다.  
   - 이미 방문한 정점이라면(역방향 간선), disc[nxt]와 lowv[curr] 중 더 작은 값을 lowv[curr]에 갱신한다.  
   - 만약 lowv[nxt]가 disc[curr]보다 크다면, (curr, nxt)는 단절선이다.  

3. **단절선 정렬 및 출력**  
   - 찾은 모든 단절선을 pair 형태로 저장하고, 오름차순으로 정렬한다.  
   - 문제의 요구사항대로 각 간선은 A < B를 만족하도록 출력한다.  

이 과정을 거치면 복잡도가 \(O(V + E)\)로 처리 가능하며, 대규모 그래프에서도 시간 내에 충분히 해결할 수 있다.이다.

---

## C++ 코드와 설명

아래 코드는 위 알고리즘을 C++로 구현한 예시이다. 각 라인별로 설명을 덧붙인다.

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAX = 100000;            // 정점의 최대 개수
vector<int> graphList[MAX + 1];    // 인접 리스트
int disc[MAX + 1], lowv[MAX + 1];  // DFS 방문 순서와 서브트리 최소 방문 순서
bool visited[MAX + 1];             // 방문 여부 체크
int orderCnt;                      // 방문 순서 부여를 위한 전역 변수
vector<pair<int,int>> bridges;     // 단절선을 저장할 벡터

// DFS 함수: (curr: 현재 정점, parent: 부모 정점)
void dfs(int curr, int parent) {
    visited[curr] = true;               // 현재 정점 방문 표시
    disc[curr] = lowv[curr] = ++orderCnt; // 방문 순서 설정

    // 현재 정점과 인접한 다음 정점들 탐색
    for(int nxt : graphList[curr]) {
        if(nxt == parent) {
            // 부모 방향 간선은 무시
            continue;
        }
        if(!visited[nxt]) {
            // 방문하지 않은 정점이면 DFS 재귀 호출
            dfs(nxt, curr);
            // 서브트리에서 올라갈 수 있는 최소 방문 순서 갱신
            lowv[curr] = min(lowv[curr], lowv[nxt]);

            // 단절선 판별: lowv[nxt]가 disc[curr]보다 크다면 단절선
            if(lowv[nxt] > disc[curr]) {
                // 오름차순을 위해 min, max로 정렬해서 저장
                bridges.push_back({min(curr, nxt), max(curr, nxt)});
            }
        } else {
            // 이미 방문한 정점(역방향 간선) -> lowv[curr] 갱신
            lowv[curr] = min(lowv[curr], disc[nxt]);
        }
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int V, E;
    cin >> V >> E;

    // 그래프 입력 받기
    for(int i=0; i<E; i++){
        int A, B;
        cin >> A >> B;
        graphList[A].push_back(B);
        graphList[B].push_back(A);
    }

    // 모든 정점을 순회하면서 DFS 수행
    for(int i = 1; i <= V; i++){
        if(!visited[i]) {
            dfs(i, 0);
        }
    }

    // 단절선 정보를 정렬
    sort(bridges.begin(), bridges.end());

    // 단절선 개수 출력
    cout << bridges.size() << "\n";
    // 단절선 목록 출력 (A < B)
    for(auto &b : bridges) {
        cout << b.first << " " << b.second << "\n";
    }

    return 0;
}
```

### 코드 동작 단계별 요약

1. **그래프 입력**  
   - 정점 수 V와 간선 수 E를 입력받아, 각 간선(A, B)을 인접 리스트에 저장한다.

2. **DFS 초기화 및 순회**  
   - 모든 정점에 대해 방문 여부를 확인하고, 방문하지 않은 정점에 대해 DFS를 수행한다.

3. **DFS 재귀 탐색**  
   - 현재 정점(curr)의 방문 순서를 disc와 lowv에 매긴 뒤, 인접한 정점을 탐색한다.  
   - 자식 정점(nxt)을 방문하지 않았다면 재귀 호출을 수행하고, 서브트리에서 올라갈 수 있는 최소 방문 순서를 curr에 반영한다.  
   - 만약 lowv[nxt] > disc[curr]를 만족한다면 (curr, nxt)는 단절선이다.

4. **결과 출력**  
   - 단절선 목록을 사전순으로 정렬하고, (A, B) 형태로 출력한다.

---

## Python 코드와 설명

아래는 동일한 알고리즘을 Python으로 구현한 예시 코드이다.이다.

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

MAX = 100000
graphList = [[] for _ in range(MAX + 1)]
disc = [0] * (MAX + 1)
lowv = [0] * (MAX + 1)
visited = [False] * (MAX + 1)
orderCnt = 0
bridges = []

def dfs(curr, parent):
    global orderCnt
    visited[curr] = True
    orderCnt += 1
    disc[curr] = orderCnt
    lowv[curr] = orderCnt

    for nxt in graphList[curr]:
        if nxt == parent:
            # 부모 정점은 무시
            continue
        if not visited[nxt]:
            # 방문하지 않은 정점이면 DFS
            dfs(nxt, curr)
            lowv[curr] = min(lowv[curr], lowv[nxt])
            # 단절선 판별
            if lowv[nxt] > disc[curr]:
                bridges.append((min(curr, nxt), max(curr, nxt)))
        else:
            # 이미 방문한 정점(역방향 간선)으로 최소 방문 순서 갱신
            lowv[curr] = min(lowv[curr], disc[nxt])

def main():
    V, E = map(int, input().split())
    for _ in range(E):
        A, B = map(int, input().split())
        graphList[A].append(B)
        graphList[B].append(A)

    for i in range(1, V + 1):
        if not visited[i]:
            dfs(i, 0)

    bridges.sort()
    print(len(bridges))
    for a, b in bridges:
        print(a, b)

if __name__ == "__main__":
    main()
```

### 코드 동작 단계별 요약

1. **그래프 입력**  
   - `V, E`를 받아 인접 리스트를 초기화하고, 간선 정보를 저장한다.

2. **DFS 함수 정의**  
   - 전역 변수 `orderCnt`를 이용해 현재 정점의 방문 순서를 기록한다.  
   - `lowv[curr]` 값은 서브트리에서 가장 먼저 방문한 정점까지 거슬러 올라갈 수 있는 최소 방문 순서를 저장한다.

3. **단절선 판별**  
   - 자식 정점 `nxt`에 대한 DFS가 끝난 뒤, `lowv[nxt]`가 `disc[curr]`보다 큰지를 확인한다.  
   - 해당 조건이 참이면 `(curr, nxt)`는 단절선으로 bridges 리스트에 저장한다.

4. **정렬 및 결과 출력**  
   - 모든 DFS가 종료된 후, bridges 리스트를 정렬하고 간선 정보를 출력한다.

## 결론

본 문제는 그래프 이론에서 중요한 개념인 단절선을 효율적으로 구하는 방법을 묻는다. 단순한 방법으로 모든 간선을 직접 제거해보는 방식은 매우 비효율적이므로, DFS 기반의 Tarjan’s Algorithm을 통해 \(O(V + E)\) 내로 문제를 해결할 수 있다. 단절점(Articulation Point)이나 단절선(Bridge)을 찾는 문제는 복잡해 보이지만, 방문 순서와 서브트리에서의 최소 방문 순서를 잘 관리하면 크게 어렵지 않게 구현 가능하다. 이를 통해 그래프의 연결 구조를 보다 깊이 있게 분석할 수 있으며, 실제 네트워크 구조나 소셜 그래프 등 다양한 분야에서 응용될 수 있다. 더불어 코드를 작성할 때는 대규모 입력에 대비한 효율적인 자료 구조(인접 리스트) 사용과, visited 배열 및 disc, lowv 배열과 같은 반복 사용 변수 관리를 주의해야 한다. 최적화와 정렬 단계를 잘 조합함으로써 제한된 시간과 메모리 내에 해결이 가능한 문제이다.이다.
