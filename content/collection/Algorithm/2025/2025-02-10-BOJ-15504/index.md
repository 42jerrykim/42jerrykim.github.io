---
title: "[Algorithm] C++/Python 백준 15504번 : 프로그래밍 대결"
description: "이 글은 백준 15504번 프로그래밍 대결 문제의 조건 및 최소 비용 최대 유량 알고리즘 적용 방법, 실력/피로도/제한 조건별 그래프 모델링 전략, 난이도 포인트 계산과정, 효율적 대결 매칭을 통한 최대 대회 재미 산출법까지 150자 내외로 상세히 안내합니다."
categories: 
- Algorithm
- Maximum Flow
- Minimum Cost Flow
tags:
- MinCostFlow
- GraphTheory
- NetworkFlow
- Dijkstra
- PriorityQueue
- Greedy
- O(E * Flow)
- Simulation
- ProblemSolving
image: "index.png"
date: 2025-02-10
---

본 포스트에서는 백준 15504번 “프로그래밍 대결” 문제를 상세히 분석하고, 이를 해결하기 위한 알고리즘 접근 방식과 함께 C++ 및 Python으로 구현한 최적화 코드를 소개하고자 한다. 문제의 핵심은 참가자들의 실력, 피로도, 경기 제한 횟수를 고려하여 모든 대결에서 발생하는 흥미로움의 총합에서 참가자들의 피로도 총합을 빼, 대회의 재미를 최대화하는 것이다. 단순한 그리디나 완전 탐색으로는 풀기 어려운 문제로, 네트워크 플로우 모델링과 최소 비용 최대 유량(Minimum Cost Maximum Flow, MCMF) 알고리즘을 적용하여 해결할 수 있다.

문제 : [https://www.acmicpc.net/problem/15504](https://www.acmicpc.net/problem/15504)

## 문제 설명

백준 15504번 “프로그래밍 대결” 문제는 N명의 참가자가 참가하는 프로그래밍 대회를 모델링한 문제이다. 각 참가자는 고유의 실력 Aᵢ를 보유하고 있으며, 대회는 두 참가자가 일대일로 붙어 진행되는 총 N-1번의 대결로 구성된다. 대결에서는 항상 더 높은 실력을 가진 참가자가 승리하며, 패배한 참가자는 즉시 탈락하여 더 이상 대결에 참여할 수 없게 된다. 이때 최종 우승자는 가장 높은 실력을 보유한 참가자가 된다. 단, 모든 참가자는 제한된 횟수(Lᵢ)만큼만 대결할 수 있으며, Lᵢ는 모든 참가자에 대해 2 이상임에 유의해야 한다. 

각 대결에서 발생하는 흥미로움은 대결에 참여한 두 참가자의 실력 값에 대해 Bitwise XOR 연산을 수행한 값으로 결정된다. 반면, 참가자는 대결을 진행할 때마다 일정량(Hᵢ)의 피로도가 쌓이게 된다. 따라서 대회의 전체 재미는 “모든 대결의 흥미로움 합”에서 “모든 참가자들의 피로도 합”을 차감한 값으로 정의된다. 문제의 목표는 주어진 조건을 만족하면서 이 대회의 재미를 최대화하는 경기 진행 순서와 매칭을 찾는 것이다.

문제 해결의 핵심은, 각 참가자들이 반드시 자신보다 높은 실력을 가진 참가자와 한 번 대결해야 한다는 사실이다. 단, 가장 높은 실력을 가진 우승자를 제외한 모든 참가자는 자신보다 낮은 실력을 가진 참가자와도 제한된 횟수 내에서 추가 대결을 치를 수 있다. 이와 같이 각 참가자의 대결 횟수 제한과 피로도, 그리고 각 대결의 흥미도(실력 XOR 연산 결과)가 복합적으로 작용하는 문제는 단순한 탐욕 알고리즘이나 브루트 포스 방식으로는 효율적으로 해결하기 어렵다. 문제를 해결하기 위해서는 참가자들을 실력 순으로 정렬하고, 이를 기반으로 네트워크 플로우 그래프를 구성하여, S(출발점)에서 T(종점)로 총 N-1의 유량이 흐르도록 연결하는 최소 비용 최대 유량 알고리즘을 적용하는 방식으로 접근할 수 있다. 각 간선의 비용은 두 참가자가 대결할 때 소모되는 피로도와 흥미도 차이로 결정되며, 최종적으로 계산된 최소 비용의 부호를 반전하면 최대 대회의 재미를 구할 수 있게 된다.

## 접근 방식

문제 해결을 위한 접근 방식은 다음과 같다.

1. **참가자 정렬**  
   각 참가자를 실력 Aᵢ에 따라 오름차순으로 정렬한다. 이를 통해, 낮은 실력을 가진 참가자가 반드시 자신보다 높은 실력을 가진 참가자와 대결하도록 그래프를 구성할 수 있다.

2. **네트워크 플로우 그래프 구성**  
   그래프는 S(출발점), 왼쪽 파트(낮은 실력 참가자), 오른쪽 파트(높은 실력 참가자), T(종점)로 구성된다.  
   - S에서 왼쪽 파트로는 각 참가자(우승자를 제외한 참가자)당 1의 용량을 갖는 간선을 추가한다.  
   - 왼쪽 파트에서 오른쪽 파트로는 실력이 낮은 참가자와 높은 참가자 사이에 대결이 가능하도록 간선을 추가한다. 각 간선의 비용은 “(Hᵤ + Hᵥ) - (Aᵤ XOR Aᵥ)”로 정의된다.  
   - 오른쪽 파트에서 T로는 각 참가자의 대결 제한(L 값)을 반영하여, 우승자는 L번, 그 외 참가자는 L-1번의 대결이 가능하도록 용량을 설정한다.

3. **최소 비용 최대 유량 알고리즘 적용**  
   총 N-1번의 대결(유량)을 흘리며, 다익스트라와 potential 기법을 사용하여 각 단계에서 최소 비용 경로를 찾는다. 이때, 최종 계산된 총 비용은 “모든 대결의 흥미로움 합”과 “모든 참가자들의 피로도 합”의 차이를 음수로 표현한 값이므로, 부호를 반전하면 최대 대회의 재미를 구할 수 있다.

4. **결과 출력**  
   최종적으로 구한 최대 대회의 재미를 출력한다.

## C++ 코드와 설명

다음은 최적화된 C++ 코드이다. 각 주요 라인마다 주석을 추가하여 코드의 동작을 상세히 설명하였다.

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll INF = 1LL << 60;  // 무한대를 표현하는 상수이다.

// 간선(Edge) 구조체로, 목적지 노드, 역방향 간선 인덱스, 용량, 비용을 저장한다.
struct Edge {
    int to, rev;
    int cap;
    ll cost;
};

// 최소 비용 최대 유량(MinCostFlow) 알고리즘을 위한 클래스이다.
struct MinCostFlow {
    int n;  // 노드의 총 개수이다.
    vector<vector<Edge>> graph;  // 각 노드별 인접 리스트이다.
    vector<ll> dist, potential;  // 최단 거리와 potential 값을 저장한다.
    vector<int> parent_v, parent_e;  // 경로 복원을 위한 부모 노드와 해당 간선의 인덱스이다.

    // 생성자: 노드의 개수 n으로 초기화한다.
    MinCostFlow(int n): n(n), graph(n), dist(n), potential(n), parent_v(n), parent_e(n) {}

    // s에서 t로 cap의 유량과 cost를 갖는 간선을 추가한다.
    void add_edge(int s, int t, int cap, ll cost) {
        graph[s].push_back({t, (int)graph[t].size(), cap, cost});
        graph[t].push_back({s, (int)graph[s].size()-1, 0, -cost});
    }

    // s에서 t로 f만큼의 유량을 보내면서 최소 비용을 계산한다.
    ll min_cost_flow(int s, int t, int f) {
        ll res = 0;
        fill(potential.begin(), potential.end(), 0);
        while(f > 0) {
            // 다익스트라를 이용하여 최단 경로를 구한다.
            priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq;
            fill(dist.begin(), dist.end(), INF);
            dist[s] = 0;
            pq.push({0, s});
            while(!pq.empty()){
                auto p = pq.top();
                pq.pop();
                int v = p.second;
                if(dist[v] != p.first) continue;
                // 인접 간선을 확인하며 최단 경로를 갱신한다.
                for(int i = 0; i < graph[v].size(); i++){
                    Edge &e = graph[v][i];
                    if(e.cap > 0 && dist[e.to] > dist[v] + e.cost + potential[v] - potential[e.to]){
                        dist[e.to] = dist[v] + e.cost + potential[v] - potential[e.to];
                        parent_v[e.to] = v;
                        parent_e[e.to] = i;
                        pq.push({dist[e.to], e.to});
                    }
                }
            }
            // 목적지까지 경로가 없으면 더 이상 유량을 보낼 수 없다.
            if(dist[t] == INF) return INF;
            // potential 값을 갱신한다.
            for(int v = 0; v < n; v++){
                if(dist[v] < INF)
                    potential[v] += dist[v];
            }
            // 경로 상의 최소 잔여 용량을 구한다.
            int add_flow = f;
            for(int v = t; v != s; v = parent_v[v]){
                add_flow = min(add_flow, graph[parent_v[v]][parent_e[v]].cap);
            }
            f -= add_flow;
            res += (ll)add_flow * potential[t];
            // 경로 상의 간선 용량을 업데이트한다.
            for(int v = t; v != s; v = parent_v[v]){
                Edge &e = graph[parent_v[v]][parent_e[v]];
                e.cap -= add_flow;
                graph[v][e.rev].cap += add_flow;
            }
        }
        return res;
    }
};

// 참가자 정보를 저장하는 구조체이다.
struct Participant {
    int a, h, l;
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    vector<Participant> parts(N);
    // 각 참가자의 실력(A)을 입력받는다.
    for (int i = 0; i < N; i++){
        cin >> parts[i].a;
    }
    // 각 참가자의 피로도(H)를 입력받는다.
    for (int i = 0; i < N; i++){
        cin >> parts[i].h;
    }
    // 각 참가자의 경기 제한(L)을 입력받는다.
    for (int i = 0; i < N; i++){
        cin >> parts[i].l;
    }
    // 실력에 따라 참가자들을 오름차순 정렬한다.
    sort(parts.begin(), parts.end(), [](const Participant &p1, const Participant &p2){
        return p1.a < p2.a;
    });
    int root = N - 1;  // 최종 우승자는 가장 높은 실력을 가진 참가자이다.
    
    // 네트워크 플로우의 노드 번호 할당: S(0), 왼쪽 파트(1~N-1), 오른쪽 파트(N~2N-1), T(2N)
    int S = 0, T = 2 * N;
    int total_nodes = 2 * N + 1;
    MinCostFlow mcf(total_nodes);

    // S에서 왼쪽 파트로 각 참가자(우승자 제외)당 1의 용량으로 간선을 추가한다.
    for (int i = 1; i <= N - 1; i++){
        mcf.add_edge(S, i, 1, 0);
    }
    // 왼쪽 파트에서 오른쪽 파트로, 실력이 낮은 참가자와 높은 참가자 간의 대결 가능성을 간선으로 추가한다.
    for (int i = 1; i <= N - 1; i++){
        int u = i - 1;  // 왼쪽 파트에 대응하는 참가자 인덱스이다.
        for (int v = u + 1; v < N; v++){
            int xorVal = parts[u].a ^ parts[v].a;  // 두 참가자 간의 XOR 연산으로 흥미로움을 계산한다.
            ll cost = (ll)parts[u].h + parts[v].h - xorVal;  // 간선의 비용은 피로도 합에서 흥미로움을 차감한 값이다.
            mcf.add_edge(i, v + N, 1, cost);
        }
    }
    // 오른쪽 파트에서 T로, 각 참가자의 경기 제한을 반영하여 간선을 추가한다.
    for (int v = 0; v < N; v++){
        int cap;
        if(v == root)
            cap = parts[v].l;      // 최종 우승자는 L번의 대결이 가능하다.
        else
            cap = parts[v].l - 1;  // 나머지 참가자는 L-1번 대결이 가능하다.
        mcf.add_edge(v + N, T, cap, 0);
    }

    // 총 N-1번의 대결을 진행해야 하므로 유량은 N-1이다.
    int flowNeeded = N - 1;
    ll minCost = mcf.min_cost_flow(S, T, flowNeeded);
    // 최종 대회의 재미는 (총 흥미로움 합) - (총 피로도 합)이며, 이는 - (minCost)와 동일하다.
    ll answer = -minCost;
    cout << answer << "\n";
    return 0;
}
```

**코드 설명:**  
1. 입력 부분에서 참가자들의 실력, 피로도, 경기 제한 정보를 입력받고, 실력 기준으로 정렬한다.  
2. 네트워크 플로우 모델을 구성하여 S에서 왼쪽 파트, 왼쪽 파트에서 오른쪽 파트, 그리고 오른쪽 파트에서 T로 간선을 추가한다. 각 간선은 대결의 비용(피로도와 흥미도 차이)을 반영한다.  
3. 다익스트라와 potential 기법을 사용한 최소 비용 최대 유량 알고리즘으로 총 N-1의 유량을 흘려보내며, 최종 최소 비용을 계산한다.  
4. 계산된 최소 비용의 부호를 반전하여 최대 대회의 재미를 출력한다.

## Python 코드와 설명

다음은 동일한 알고리즘을 Python으로 구현한 코드이다. 코드 내에 각 단계별로 주석을 추가하여 동작을 상세히 설명하였다.

```python
import sys, heapq
INF = 10**18  # 무한대를 표현하는 상수이다.

# 간선(Edge) 클래스로, 목적지, 역방향 인덱스, 용량, 비용을 저장한다.
class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to = to        # 목적지 노드이다.
        self.rev = rev      # 역방향 간선의 인덱스이다.
        self.cap = cap      # 간선의 용량이다.
        self.cost = cost    # 간선의 비용이다.

# 최소 비용 최대 유량(MinCostFlow) 알고리즘을 구현한 클래스이다.
class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]      # 각 노드별 인접 리스트이다.
        self.potential = [0] * n                 # 각 노드의 potential 값을 저장한다.
        self.dist = [INF] * n                    # 최단 거리를 저장한다.
        self.parent_v = [0] * n                  # 경로 복원 시 부모 노드를 저장한다.
        self.parent_e = [0] * n                  # 경로 복원 시 해당 간선의 인덱스를 저장한다.

    # s에서 t로 cap의 용량과 cost를 가지는 간선을 추가한다.
    def add_edge(self, s, t, cap, cost):
        self.graph[s].append(Edge(t, len(self.graph[t]), cap, cost))
        self.graph[t].append(Edge(s, len(self.graph[s]) - 1, 0, -cost))

    # s에서 t로 f만큼의 유량을 보내면서 최소 비용을 계산한다.
    def min_cost_flow(self, s, t, f):
        res = 0
        self.potential = [0] * self.n
        while f:
            self.dist = [INF] * self.n
            self.dist[s] = 0
            queue = [(0, s)]
            # 다익스트라 알고리즘을 사용하여 최단 경로를 찾는다.
            while queue:
                d, v = heapq.heappop(queue)
                if self.dist[v] < d:
                    continue
                for i, e in enumerate(self.graph[v]):
                    if e.cap > 0 and self.dist[e.to] > d + e.cost + self.potential[v] - self.potential[e.to]:
                        self.dist[e.to] = d + e.cost + self.potential[v] - self.potential[e.to]
                        self.parent_v[e.to] = v
                        self.parent_e[e.to] = i
                        heapq.heappush(queue, (self.dist[e.to], e.to))
            # 목적지까지 경로가 없으면 INF를 반환한다.
            if self.dist[t] == INF:
                return INF
            # potential 값을 갱신한다.
            for v in range(self.n):
                if self.dist[v] < INF:
                    self.potential[v] += self.dist[v]
            add_flow = f
            v = t
            # 경로 상의 최소 잔여 용량을 구한다.
            while v != s:
                add_flow = min(add_flow, self.graph[self.parent_v[v]][self.parent_e[v]].cap)
                v = self.parent_v[v]
            f -= add_flow
            res += add_flow * self.potential[t]
            v = t
            # 경로 상의 간선 용량을 업데이트한다.
            while v != s:
                e = self.graph[self.parent_v[v]][self.parent_e[v]]
                e.cap -= add_flow
                self.graph[v][e.rev].cap += add_flow
                v = self.parent_v[v]
        return res

def main():
    input = sys.stdin.readline
    N = int(input())
    parts = []
    # 참가자들의 실력(A), 피로도(H), 경기 제한(L)을 입력받는다.
    A = list(map(int, input().split()))
    H = list(map(int, input().split()))
    L = list(map(int, input().split()))
    for i in range(N):
        parts.append((A[i], H[i], L[i]))
    # 실력에 따라 참가자들을 오름차순 정렬한다.
    parts.sort(key=lambda x: x[0])
    root = N - 1  # 최종 우승자는 가장 높은 실력을 가진 참가자이다.
    total_nodes = 2 * N + 1  # S, 왼쪽, 오른쪽, T를 포함한 총 노드 수이다.
    S = 0
    T = 2 * N
    mcf = MinCostFlow(total_nodes)
    
    # S에서 왼쪽 파트(1~N-1)로 간선을 추가한다.
    for i in range(1, N):
        mcf.add_edge(S, i, 1, 0)
    # 왼쪽 파트에서 오른쪽 파트로, 가능한 모든 대결 간선을 추가한다.
    for i in range(1, N):
        u = i - 1  # 왼쪽 파트에 해당하는 참가자 인덱스이다.
        for v in range(u + 1, N):
            xorVal = parts[u][0] ^ parts[v][0]  # 두 참가자 간의 XOR 연산 결과이다.
            cost = parts[u][1] + parts[v][1] - xorVal  # 간선의 비용을 계산한다.
            mcf.add_edge(i, v + N, 1, cost)
    # 오른쪽 파트에서 T로 각 참가자의 경기 제한을 반영하여 간선을 추가한다.
    for v in range(N):
        if v == root:
            cap = parts[v][2]      # 우승자는 L번의 대결이 가능하다.
        else:
            cap = parts[v][2] - 1  # 나머지 참가자는 L-1번의 대결이 가능하다.
        mcf.add_edge(v + N, T, cap, 0)
    
    flowNeeded = N - 1  # 총 N-1번의 대결이 진행되어야 한다.
    minCost = mcf.min_cost_flow(S, T, flowNeeded)
    answer = -minCost  # 대회의 재미는 - (최소 비용)이다.
    print(answer)

if __name__ == '__main__':
    main()
```

**코드 설명:**  
1. 입력받은 참가자 정보를 바탕으로 실력, 피로도, 경기 제한 정보를 리스트에 저장하고, 실력 기준으로 정렬한다.  
2. S, 왼쪽 파트, 오른쪽 파트, T로 구성된 네트워크 플로우 그래프를 구축한다. S에서 왼쪽 파트로, 왼쪽 파트에서 오른쪽 파트로, 오른쪽 파트에서 T로 간선을 추가하며, 각 간선의 비용은 두 참가자의 피로도와 XOR 연산 결과를 이용하여 계산된다.  
3. 최소 비용 최대 유량 알고리즘을 통해 총 N-1번의 대결(유량)을 흘려보내고, 계산된 최소 비용의 부호를 반전하여 최대 대회의 재미를 도출한다.

## 결론

본 문제는 참가자 간 대결의 흥미와 피로도라는 두 요소가 복합적으로 작용하는 문제로, 단순한 그리디 접근 방식으로는 해결하기 어려운 문제임을 확인할 수 있었다. 문제를 네트워크 플로우 모델로 전환하고, 최소 비용 최대 유량 알고리즘을 적용함으로써 효율적으로 문제를 해결할 수 있었다. C++와 Python 두 가지 언어로 구현한 코드는 각각의 언어적 특성을 잘 활용하여 최적화되었으며, 향후 유사한 문제에 대해 네트워크 플로우를 적용하는 좋은 예시가 될 수 있다. 추가적인 최적화 방안으로는, 입력 크기가 더 큰 경우에 대비한 자료구조 개선이나, potential 갱신 방식의 최적화를 고려할 수 있음을 느꼈다.
