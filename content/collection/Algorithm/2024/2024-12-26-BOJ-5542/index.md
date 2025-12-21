---
title: "[Algorithm] C++/Python 백준 5542번 : JOI 국가의 행사"
description: "여러 도시와 도로가 연결된 JOI 국가에서 축제 도시와의 최단 거리를 활용해 최적의 경로를 찾는 문제입니다. 멀티 소스 다익스트라, MST, LCA 등 다양한 알고리즘 기법을 적용하고 경로의 특성을 극대화하여 Q개의 질의에 효과적으로 답하는 방법을 다룹니다."
categories: 
- Algorithm
- Graph
- ShortestPath
tags:
- Dijkstra
- Kruskald
- DSU
- Optimization
- O(N log N)
- PriorityQueue
- GraphTheory
- GraphTraversal
image: "tmp_wordcloud.png"
date: 2024-12-26
---

JOI 국에는 여러 개의 도시가 존재하고, 이 도시들을 잇는 양방향 도로가 설정되어 있다는 흥미로운 상황이 등장한다. 축제가 열리는 K개의 도시가 있고, 또 이 축제를 싫어하는 Q명의 사람들이 있다. 문제에서는 이 사람들이 어떤 특정 도시에서 다른 도시로 이동할 때, 이동 경로 상에 위치한 모든 도시가 축제를 여는 도시와 “가장 가까운 거리”의 최솟값을 최대로 만드는 경로를 찾는 것이 목표이다. 이때 최단 경로라 함은 실제로 도시와 도시 사이에 존재하는 도로의 가중치 합이 최소가 되는 경로를 말한다. 이 문제는 효과적으로 최단 거리 계산과 그래프의 MST(Minimum Spanning Tree) 변형 개념을 섞어서 해결해야 한다는 점이 관건이다. 문제에서 묻는 핵심은 “해당 경로에서 축제를 여는 도시와 거리가 가장 가깝게 되는 값을 최대한 크게 만들기”이며, 이러한 조건을 만족하는 이동 방법을 찾아서 그 최댓값을 구해 출력하는 형태이다.

문제 : [https://www.acmicpc.net/problem/5542](https://www.acmicpc.net/problem/5542)

---

## 문제 설명

JOI 국의 도시들은 모두 연결되어 있으며, M개의 양방향 도로가 있다. 각 도로에는 양 끝 도시와 그 거리(가중치)가 주어진다. K개의 도시는 현재 축제를 열고 있는데, 축제를 싫어하는 Q명의 사람들은 출발 도시에서 도착 도시로 이동할 때, “경로 위에 등장하는 어떤 도시가 축제 도시와의 거리가 가장 가깝게 되는 값”을 최대화하고 싶어 한다. 더 구체적으로 말하면, 경로에 포함된 임의의 도시 \(x\)에 대하여, \(x\)와 축제가 열리는 도시 사이의 최단거리 \(\mathrm{dist}(x)\)를 생각했을 때, 그 중 최솟값이 커지도록 이동하고 싶다는 것이다.

이때 도시 간 거리는 주어진 도로의 가중치 합으로 계산되는 최단 경로 거리이다. 예를 들어, 축제 도시가 1번과 6번이라면, 어떤 사람이 3번 도시에서 4번 도시로 이동할 때 고려해야 할 도시는 3, 5, 4 (만일 3→5→4로 이동했다면)이며, 이 각각이 1번 혹은 6번과 떨어진 거리(최단거리) 중에서 최솟값이 최대가 되는 경로를 찾아야 한다. 문제는 이러한 계산을 Q번의 질의마다 수행해야 하므로, 즉각적인 최단 경로 탐색을 Q번 반복하는 것은 비효율적일 수 있다.  
이를 위해 다음과 같은 과정을 수행한다:  
1) 먼저 모든 도시가 축제 도시와 떨어진 최단 거리를 계산한다(멀티소스 Dijkstra).  
2) 그 거리 정보를 활용하여, 간선에 \(\min(\mathrm{dist}(u), \mathrm{dist}(v))\)를 가중치로 부여하고 최대 스패닝 트리를 구성한다.  
3) 최종적으로 s에서 t로 가는 경로는 최대 스패닝 트리 상의 경로로 제한해도 답이 유지된다. 그 경로에서의 “간선 가중치 중 최솟값”이 곧 문제에서 요구하는 ‘축제 도시와의 거리 최솟값의 최대치’를 의미한다.  

본 문제를 풀기 위해서는 다익스트라, 유니온 파인드(DSU), 최대 스패닝 트리 구성, 그리고 LCA(Lowest Common Ancestor) 기반 경로 질의 처리 등이 복합적으로 사용될 수 있으며, 정확하고 효율적인 구현이 필요하다. 이 문제의 분량 및 알고리즘 복잡도는 상당하며, 메모리 사용도 주의 깊게 확인해야 한다. 또한 Q가 많을 때 매번 경로를 직접 확인하지 않고 미리 트리 기반으로 전처리를 해두어야 한다는 점도 유의해야 한다.  
이와 같이, 단순한 최단 거리 합을 구하는 전형적인 문제와 달리, “축제 도시와의 거리 최솟값을 최대화”한다는 반전된 관점의 접근이 필요하다는 점이 이 문제의 특징이다. 위와 같은 전반적인 맥락으로 봤을 때, M, N, Q가 최대 수십만에 이를 수 있으므로 \(O((N+M)\log N)\) 수준의 다익스트라와 크루스칼, 그리고 \(O(\log N)\)의 LCA 탐색으로도 시간 내 해결해야 한다는 점에서, 각 알고리즘을 정확히 최적화해 구현해야 한다.

---

## 접근 방식

1. **다익스트라(Dijkstra) 멀티소스**  
   - 축제가 열리는 모든 도시를 우선순위 큐에 넣고, 이 도시들에서부터의 최단 거리를 한 번에 구한다. 이렇게 하면 각 도시가 축제 도시와 얼마나 떨어져 있는지가 계산된다.

2. **간선 가중치 재부여**  
   - 원래 도로의 가중치가 아닌, 각 간선(u, v)에 대해 \(\min(\mathrm{dist}(u), \mathrm{dist}(v))\)를 새로운 ‘가중치’로 사용한다. 이는 “u와 v가 축제 도시와 각각 어느 정도로 떨어져 있느냐”를 표현하고, \(\min\)값을 취함으로써 “해당 간선을 통해 갈 때, 경로에서 최솟값이 어디까지 보장되느냐”를 의미하게 된다.

3. **최대 스패닝 트리(Maximum Spanning Tree)**  
   - 위에서 재부여한 가중치로 간선을 내림차순 정렬한 뒤, 크루스칼(Kruskal) 알고리즘으로 연결한다. DSU(Disjoint Set Union, Union-Find)를 이용하여 중복 간선을 제거하고, 단일 연결 요소를 구성하는 MST를 만든다.

4. **경로 질의(쿼리) 처리**  
   - MST가 완성되면, s에서 t로의 경로에서 간선 가중치의 최솟값만 확인하면 된다. 이를 빠르게 처리하기 위해, MST에 대해 LCA(또는 유사한 희소 테이블) 전처리를 수행한다.  
   - 각 쿼리마다 s와 t의 최소 공통 조상을 찾으면서 경로에 포함된 간선들의 가중치 중 최솟값을 추출하면, 그것이 곧 문제에서 요구하는 답이다.

이 접근 방식을 통해, 매 쿼리마다 복잡한 최단 거리 계산을 반복하지 않고, 미리 한 번 전처리를 함으로써 다수의 쿼리를 효율적으로 해결할 수 있다.

---

## C++ 코드와 설명

> 아래 코드는 위 접근 방식대로 구현한 예시이다. 컴파일 에러를 최소화하기 위해 C++17 이상에서 테스트를 권장함이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// DSU(Disjoint Set Union) 구조체
struct DSU {
    int n;
    vector<int> p, r;
    DSU(int n) : n(n), p(n+1), r(n+1, 0) {
        for(int i=1; i<=n; i++){
            p[i] = i; // 초기 부모는 자기 자신
        }
    }
    int findp(int x){
        // 경로 압축(Path Compression)
        if(p[x] == x) return x;
        return p[x] = findp(p[x]);
    }
    void unite(int a, int b){
        a = findp(a); 
        b = findp(b);
        if(a == b) return;
        // union by rank
        if(r[a] < r[b]) swap(a, b);
        p[b] = a;
        if(r[a] == r[b]) r[a]++;
    }
};

static const int MAXN = 100000;
vector<pair<int,int>> adjMST[MAXN+1]; 
// MST에서 인접 리스트: (다음 정점, 간선 가중치)

int parent[20][MAXN+1];   // parent[k][v] : v의 2^k번째 조상
int minEdge[20][MAXN+1];  // minEdge[k][v] : v -> parent[k][v] 까지의 경로 최소 간선 가중치
int depth[MAXN+1];

// MST에서 DFS로 깊이와 부모, 간선 최소값 테이블 초기화
void dfs(int u, int par, int w, int d){
    parent[0][u] = par;
    minEdge[0][u] = (par == -1 ? INT_MAX : w);
    depth[u] = d;
    for(auto &nx : adjMST[u]){
        int v = nx.first;
        int w2 = nx.second;
        if(v == par) continue; // 부모로의 역방향 방지
        dfs(v, u, w2, d+1);
    }
}

// u, v 노드의 경로에서 최소 간선 가중치 구하기
int getMinEdge(int u, int v){
    int ret = INT_MAX;
    // 항상 depth[u] >= depth[v] 되도록 조정
    if(depth[u] < depth[v]) swap(u, v);

    // 1) u를 v의 깊이까지 끌어올림
    int diff = depth[u] - depth[v];
    for(int k=0; diff; k++){
        if(diff & 1){
            ret = min(ret, minEdge[k][u]);
            u = parent[k][u];
        }
        diff >>= 1;
    }

    // 만약 높이를 맞췄더니 둘이 같다면 결과 반환
    if(u == v) return ret;

    // 2) 최상단 조상 직전까지 같이 올리기
    for(int k=19; k>=0; k--){
        if(parent[k][u] != parent[k][v]){
            ret = min(ret, minEdge[k][u]);
            ret = min(ret, minEdge[k][v]);
            u = parent[k][u];
            v = parent[k][v];
        }
    }
    // 마지막으로 한 칸 더 올리기
    ret = min(ret, minEdge[0][u]);
    ret = min(ret, minEdge[0][v]);
    return ret;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, K, Q;
    cin >> N >> M >> K >> Q;

    vector<vector<pair<int,int>>> graph(N+1);
    for(int i=0; i<M; i++){
        int a, b;
        long long w;
        cin >> a >> b >> w;
        graph[a].push_back({b, w});
        graph[b].push_back({a, w});
    }

    vector<int> festival(K);
    for(int i=0; i<K; i++){
        cin >> festival[i];
    }

    vector<pair<int,int>> query(Q);
    for(int i=0; i<Q; i++){
        int s, t;
        cin >> s >> t;
        query[i] = {s, t};
    }

    // 1) 멀티소스 다익스트라로 dist[] 계산
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(N+1, INF);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;

    // 축제 도시를 모두 큐에 넣음
    for(int c : festival){
        dist[c] = 0;
        pq.push({0, c});
    }

    while(!pq.empty()){
        auto [cd, u] = pq.top();
        pq.pop();
        if(cd > dist[u]) continue;
        for(auto &nx : graph[u]){
            int v = nx.first;
            long long w = nx.second;
            if(dist[v] > dist[u] + w){
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }

    // 2) 간선 목록을 만들고, 가중치를 min(dist[u], dist[v])로 설정
    vector<tuple<long long,int,int>> edges;
    edges.reserve(M);
    for(int u=1; u<=N; u++){
        for(auto &nx : graph[u]){
            int v = nx.first;
            if(u < v){
                long long w = min(dist[u], dist[v]);
                edges.push_back({w, u, v});
            }
        }
    }

    // 3) 최대 스패닝 트리 구성 (내림차순 정렬 후 크루스칼)
    sort(edges.begin(), edges.end(), [&](auto &a, auto &b){
        return get<0>(a) > get<0>(b); 
    });

    DSU dsu(N);
    int used = 0;
    for(auto &e : edges){
        long long w; 
        int u, v;
        tie(w, u, v) = e;
        if(dsu.findp(u) != dsu.findp(v)){
            dsu.unite(u, v);
            adjMST[u].push_back({v, (int)w});
            adjMST[v].push_back({u, (int)w});
            used++;
            if(used == N-1) break;
        }
    }

    // 4) LCA 전처리
    dfs(1, -1, INT_MAX, 0);
    for(int k=1; k<20; k++){
        for(int v=1; v<=N; v++){
            int p2 = parent[k-1][v];
            if(p2 == -1){
                parent[k][v] = -1;
                minEdge[k][v] = INT_MAX;
            } else {
                parent[k][v] = parent[k-1][p2];
                minEdge[k][v] = min(minEdge[k-1][v], minEdge[k-1][p2]);
            }
        }
    }

    // 5) 쿼리 처리
    for(int i=0; i<Q; i++){
        auto [s, t] = query[i];
        int ans = getMinEdge(s, t);
        cout << ans << "\n";
    }

    return 0;
}
```

### 코드 동작 단계별 설명

1. **그래프 입력**: N개의 도시, M개의 도로를 받아서 `graph`에 저장한다.  
2. **축제 도시 dist 초기화**: 축제 도시들은 거리 0으로 시작하여, 다익스트라를 진행한다.  
3. **멀티소스 다익스트라**: 우선순위 큐를 이용해 각 도시가 축제 도시와 떨어진 최단 거리를 계산한다.  
4. **간선 배열 구성**: 기존 도로 정보를 \(\min(\mathrm{dist}[u], \mathrm{dist}[v])\) 형태의 가중치로 변환하여 `edges`에 담는다.  
5. **정렬 및 크루스칼**: 새로 만든 간선들을 내림차순 정렬한 뒤, 유니온 파인드를 사용해 최대 스패닝 트리를 만든다.  
6. **트리 DFS & LCA 준비**: MST를 DFS로 탐색하면서, 각 노드의 깊이와 부모, 최소 간선 가중치를 저장한다.  
7. **희소 테이블 구성**: `parent[k][v]`, `minEdge[k][v]`를 업데이트해, 2^k씩 거슬러 올라가며 조상을 빠르게 찾을 수 있도록 한다.  
8. **쿼리 처리**: s에서 t로 이동 시, MST 경로에서 최소 간선 가중치를 `getMinEdge`로 구하여 출력한다.


## 결론

본 문제는 단순한 최단 거리 합 계산이 아닌, “경로 위 도시들이 축제 도시와 얼마나 떨어져 있는가”라는 새로운 관점을 다룬다는 점에서 복합적인 알고리즘 활용이 요구된다. 특히 멀티소스 다익스트라와 크루스칼을 이용해 최대 스패닝 트리를 구성한 뒤, LCA를 통해 쿼리를 처리하는 과정이 핵심이다.  
이 과정을 통해 Q개의 질의에 대해 매번 별도의 최단 경로 탐색 없이도 효율적으로 답을 구할 수 있다. 추가적으로, MST를 구성하는 과정에서 노드 수가 많을 경우 시간 복잡도나 메모리 사용량을 면밀히 점검해야 한다. 더 나아가, LCA와 희소 테이블 구성 시 기저 케이스를 정확히 설정하고, 가능한 모든 간선 가중치 범위(예: INT_MAX, INF 등) 관리에도 신경 써야 한다. 이러한 최적화 아이디어와 자료 구조 활용 능력이 결합되어야 문제를 원활하게 해결할 수 있음이다.
