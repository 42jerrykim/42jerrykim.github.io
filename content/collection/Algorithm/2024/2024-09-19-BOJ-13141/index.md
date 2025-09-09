---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-19T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- GraphTheory
- All-Pairs Shortest Path
- Floyd-Warshall
- Implementation
- Optimization
- O(N³)
- AdjacencyMatrix
- GraphTraversal
title: '[Algorithm] C++/Python 백준 13141번 : 그래프 불태우기'
---

그래프 불태우기 문제는 그래프의 모든 정점과 간선을 최소한의 시간 내에 불로 태우는 시점을 찾는 문제이다. 서훈이는 그래프의 한 정점에 불을 붙인 후, 불이 간선을 따라 전파되며, 불이 양 끝 정점에서 동시에 붙을 경우 간선의 중간 지점에서 불이 소멸된다. 이러한 특성을 고려하여 그래프 전체가 불타는 데 걸리는 최소 시간을 계산해야 한다. 문제는 주어진 그래프의 정점과 간선 정보를 바탕으로, 어떤 정점에 불을 붙였을 때 그래프 전체를 가장 빠르게 태울 수 있는지를 찾는 것이다. 이 문제는 그래프 이론과 최단 경로 알고리즘을 활용하여 해결할 수 있으며, 효율적인 구현을 통해 시간 제한 내에 정답을 도출해야 한다.

문제 : [https://www.acmicpc.net/problem/13141](https://www.acmicpc.net/problem/13141)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제를 해결하기 위해 우선 그래프의 모든 정점 간의 최단 거리를 구해야 한다. 이를 위해 플로이드-와샬(Floyd-Warshall) 알고리즘을 사용하였다. 플로이드-와샬 알고리즘은 모든 정점 쌍 간의 최단 거리를 구하는 데 효과적이며, 주어진 문제의 제약 조건 내에서 충분히 효율적이다. 모든 정점 간의 최단 거리를 계산한 후, 각 정점을 시작점으로 불을 붙였을 때 그래프 전체가 불타는 시간을 계산한다. 이때, 불이 간선을 따라 전파되며, 간선의 양 끝 정점에서 동시에 불이 붙을 경우 간선의 중간에서 불이 소멸되는 특성을 고려하여 각 간선의 불타는 시간을 계산한다. 모든 정점에 대해 이러한 계산을 수행한 후, 가장 최소의 시간을 찾으면 문제의 해답을 얻을 수 있다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<int, int> pii;

const int MAX_N = 201;
const ll INF = 1e18;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int N, M;
    cin >> N >> M;
    
    // Initialize distance matrix with INF
    vector<vector<ll>> dist(N+1, vector<ll>(N+1, INF));
    for(int i=1;i<=N;i++) dist[i][i] = 0;
    
    // Store all edges
    struct Edge {
        int u, v;
        int L;
    };
    vector<Edge> edges;
    edges.reserve(M);
    
    for(int i=0;i<M;i++){
        int u, v, L;
        cin >> u >> v >> L;
        edges.push_back(Edge{u, v, L});
        if(u != v){
            // If multiple edges exist, keep the shortest one
            if(L < dist[u][v]){
                dist[u][v] = L;
                dist[v][u] = L;
            }
        }
    }
    
    // Floyd-Warshall algorithm to compute all-pairs shortest paths
    for(int k=1;k<=N;k++){
        for(int i=1;i<=N;i++){
            if(dist[i][k] == INF) continue;
            for(int j=1;j<=N;j++){
                if(dist[k][j] == INF) continue;
                if(dist[i][j] > dist[i][k] + dist[k][j]){
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    
    double minimal_burn_time = 1e18;
    
    // Iterate through each node as the starting point
    for(int s=1;s<=N;s++){
        double current_burn_time = 0.0;
        
        // Find the maximum shortest distance from s to any node
        for(int v=1; v<=N; v++){
            if(dist[s][v] < INF){
                current_burn_time = max(current_burn_time, (double)dist[s][v]);
            }
        }
        
        // Iterate through all edges to calculate burn time
        for(auto &edge : edges){
            int u = edge.u;
            int v = edge.v;
            int L = edge.L;
            double burn_time;
            if(u == v){
                // Loop edge: burn time is distance to u plus half the length
                burn_time = (double)dist[s][u] + (double)L / 2.0;
            }
            else{
                ll Tu = dist[s][u];
                ll Tv = dist[s][v];
                if(Tu + L < Tv){
                    // Fire reaches v before coming from u
                    burn_time = (double)(Tu + L);
                }
                else if(Tv + L < Tu){
                    // Fire reaches u before coming from v
                    burn_time = (double)(Tv + L);
                }
                else{
                    // Fire meets in the middle
                    burn_time = ((double)(Tu) + (double)(Tv) + (double)(L)) / 2.0;
                }
            }
            current_burn_time = max(current_burn_time, burn_time);
        }
        
        minimal_burn_time = min(minimal_burn_time, current_burn_time);
    }
    
    // Output the result with one decimal place
    cout << fixed << setprecision(1) << minimal_burn_time;
}
```

이 코드는 다음과 같은 단계로 동작한다:

1. **입력 처리 및 초기화**: 정점 수 `N`과 간선 수 `M`을 입력받고, 모든 정점 간의 거리를 무한대로 초기화한 후, 자기 자신으로의 거리는 0으로 설정한다. 이후, 모든 간선을 입력받아 저장하며, 여러 간선이 있는 경우 가장 짧은 간선의 길이를 유지한다.

2. **플로이드-와샬 알고리즘**: 모든 정점 쌍 간의 최단 거리를 계산하기 위해 플로이드-와샬 알고리즘을 실행한다. 이 알고리즘은 세 개의 중첩된 반복문을 통해 모든 가능한 경유지를 고려하여 최단 거리를 갱신한다.

3. **불타는 시간 계산**: 각 정점을 시작점으로 불을 붙였을 때의 불타는 시간을 계산한다. 이를 위해 모든 간선을 순회하며, 간선의 양 끝 정점에서 불이 붙는 시간을 고려하여 간선의 불타는 시간을 계산한다. 이때, 루프 간선인 경우와 일반 간선인 경우를 구분하여 처리한다.

4. **최소 불타는 시간 찾기**: 모든 정점에 대해 계산된 불타는 시간 중 최소값을 찾아 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long ll;

#define MAX_N 201
#define INF 1000000000000000000LL

int main(){
    int N, M;
    scanf("%d %d", &N, &M);
    
    // Initialize distance matrix
    ll dist[MAX_N][MAX_N];
    for(int i=1;i<=N;i++) {
        for(int j=1;j<=N;j++) {
            if(i == j) dist[i][j] = 0;
            else dist[i][j] = INF;
        }
    }
    
    // Store edges
    struct Edge {
        int u, v;
        int L;
    };
    Edge *edges = (Edge*)malloc(sizeof(Edge)*M);
    
    for(int i=0;i<M;i++){
        int u, v, L;
        scanf("%d %d %d", &u, &v, &L);
        edges[i].u = u;
        edges[i].v = v;
        edges[i].L = L;
        if(u != v){
            if(L < dist[u][v]){
                dist[u][v] = L;
                dist[v][u] = L;
            }
        }
    }
    
    // Floyd-Warshall
    for(int k=1;k<=N;k++){
        for(int i=1;i<=N;i++){
            if(dist[i][k] == INF) continue;
            for(int j=1;j<=N;j++){
                if(dist[k][j] == INF) continue;
                if(dist[i][j] > dist[i][k] + dist[k][j]){
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    
    double minimal_burn_time = 1e18;
    
    // Iterate through each node
    for(int s=1;s<=N;s++){
        double current_burn_time = 0.0;
        
        // Find maximum shortest distance
        for(int v=1; v<=N; v++){
            if(dist[s][v] < INF){
                if((double)dist[s][v] > current_burn_time){
                    current_burn_time = (double)dist[s][v];
                }
            }
        }
        
        // Iterate through all edges
        for(int i=0;i<M;i++){
            int u = edges[i].u;
            int v = edges[i].v;
            int L = edges[i].L;
            double burn_time;
            if(u == v){
                // Loop edge
                burn_time = (double)dist[s][u] + (double)L / 2.0;
            }
            else{
                ll Tu = dist[s][u];
                ll Tv = dist[s][v];
                if(Tu + L < Tv){
                    burn_time = (double)(Tu + L);
                }
                else if(Tv + L < Tu){
                    burn_time = (double)(Tv + L);
                }
                else{
                    burn_time = ((double)(Tu) + (double)(Tv) + (double)(L)) / 2.0;
                }
            }
            if(burn_time > current_burn_time){
                current_burn_time = burn_time;
            }
        }
        
        if(current_burn_time < minimal_burn_time){
            minimal_burn_time = current_burn_time;
        }
    }
    
    // Print result with one decimal place
    printf("%.1lf", minimal_burn_time);
    
    free(edges);
    return 0;
}
```

이 코드는 표준 라이브러리를 사용하지 않고, `stdio.h`와 `stdlib.h`만을 사용하여 구현되었다. 주요 동작 방식은 다음과 같다:

1. **입력 및 초기화**: `scanf`를 통해 입력을 받고, 거리 행렬을 초기화한다. 루프 간선과 다중 간선에 대한 처리를 직접 수행한다.

2. **플로이드-와샬 알고리즘**: 중첩된 반복문을 통해 모든 정점 쌍 간의 최단 거리를 계산한다.

3. **불타는 시간 계산**: 각 정점에 대해 모든 간선을 순회하며, 간선의 특성에 따라 불타는 시간을 계산하고, 이를 최대값으로 업데이트한다.

4. **최소 시간 찾기 및 출력**: 모든 정점에 대해 계산된 불타는 시간 중 최소값을 찾아 `printf`를 통해 출력한다.

## Python 코드와 설명

```python
import sys

def main():
    import sys
    import math
    input = sys.stdin.readline

    N, M = map(int, sys.stdin.readline().split())
    INF = float('inf')
    dist = [[INF]*(N+1) for _ in range(N+1)]
    for i in range(1, N+1):
        dist[i][i] = 0

    edges = []
    for _ in range(M):
        u, v, L = map(int, sys.stdin.readline().split())
        edges.append((u, v, L))
        if u != v:
            if L < dist[u][v]:
                dist[u][v] = L
                dist[v][u] = L

    # Floyd-Warshall
    for k in range(1, N+1):
        for i in range(1, N+1):
            if dist[i][k] == INF:
                continue
            for j in range(1, N+1):
                if dist[k][j] == INF:
                    continue
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    minimal_burn_time = INF

    for s in range(1, N+1):
        current_burn_time = 0.0
        # Maximum shortest distance from s
        for v in range(1, N+1):
            if dist[s][v] < INF:
                current_burn_time = max(current_burn_time, float(dist[s][v]))
        # Iterate through all edges
        for (u, v, L) in edges:
            if u == v:
                burn_time = dist[s][u] + L / 2.0
            else:
                Tu = dist[s][u]
                Tv = dist[s][v]
                if Tu + L < Tv:
                    burn_time = Tu + L
                elif Tv + L < Tu:
                    burn_time = Tv + L
                else:
                    burn_time = (Tu + Tv + L) / 2.0
            current_burn_time = max(current_burn_time, burn_time)
        minimal_burn_time = min(minimal_burn_time, current_burn_time)
    
    # Print with one decimal place
    print("{0:.1f}".format(minimal_burn_time))

if __name__ == "__main__":
    main()
```

이 파이썬 코드는 C++ 코드와 유사한 논리를 따라 작성되었다. 주요 단계는 다음과 같다:

1. **입력 및 초기화**: `sys.stdin.readline`을 사용하여 입력을 효율적으로 받고, 거리 행렬을 초기화한다. 다중 간선과 루프 간선에 대한 처리를 수행한다.

2. **플로이드-와샬 알고리즘**: 이중 반복문을 통해 모든 정점 쌍 간의 최단 거리를 계산한다.

3. **불타는 시간 계산**: 각 정점에 대해 모든 간선을 순회하면서, 간선의 특성에 따라 불타는 시간을 계산하고, 이를 최대값으로 업데이트한다.

4. **최소 시간 찾기 및 출력**: 모든 정점에 대해 계산된 불타는 시간 중 최소값을 찾아 소수점 첫째 자리까지 출력한다.

## 결론

그래프 불태우기 문제는 플로이드-와샬 알고리즘을 활용하여 모든 정점 간의 최단 거리를 효율적으로 계산한 후, 각 정점을 시작점으로 불을 붙였을 때의 불타는 시간을 정확히 계산하는 것이 핵심이었다. 다양한 간선의 특성을 고려하여 불타는 시간을 정확히 산출함으로써, 최종적으로 그래프 전체를 가장 빠르게 태울 수 있는 시작점을 찾을 수 있었다. 구현 과정에서 플로이드-와샬 알고리즘의 시간 복잡도인 O(N³)이 문제의 제약 조건 내에서 충분히 효율적이었음을 확인할 수 있었다. 추가적인 최적화 방안으로는, 불필요한 간선의 처리를 줄이거나, 더 효율적인 자료 구조를 활용하는 방법이 있을 수 있으나, 현재의 접근 방식으로도 충분히 문제를 해결할 수 있었다.