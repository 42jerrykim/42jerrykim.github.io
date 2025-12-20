---
title: "[Algorithm] C++/Python 백준 4792번 : 레드 블루 스패닝 트리"
description: "백준 4792번 레드 블루 스패닝 트리는 무방향 그래프에서 각 간선 색이 빨강 또는 파랑일 때, 파란 간선이 정확히 k개인 스패닝 트리의 존재 여부를 Kruskal 변형, MST와 Union-Find로 판별하는 문제로, 최소·최대 파란 간선 개수 범위 내 k의 포함 여부를 통해 풀이하며 색 기준 정렬 및 트리 구성 원리를 묻는 대표적 문제입니다."
categories: 
- Algorithm
- GraphTheory
- MinimumSpanningTree
tags:
- MST
- Graph
- Greedy
- Union-Find
- O(M log N)
- Implementation
- GraphTheory
image: "tmp_wordcloud.png"
date: 2024-12-12
---

문제 4792번은 주어진 무방향, 무가중치 연결 그래프에서 스패닝 트리를 구성하되, 트리에 포함된 파란색 간선의 수가 정확히 k개가 되는지 판별하는 문제이다. 이 문제는 MST(Minimum Spanning Tree) 변형 문제로서, 간선 색깔(빨간/파란)을 활용한 조건 판정이 핵심이다. 일반적인 MST 문제에서는 간선 가중치를 기준으로 최소 스패닝 트리를 구하지만, 여기서는 간선 색상을 기준으로 "가능한 스패닝 트리들 중 파란 간선의 최소 개수 및 최대 개수를 구한 뒤, 주어진 k가 그 범위 안에 포함되는지를 확인"하는 방식으로 문제를 접근한다. 이러한 방식으로 k가 만족 가능한지 빠르게 판정할 수 있다.

문제 : [https://www.acmicpc.net/problem/4792](https://www.acmicpc.net/problem/4792)

## 문제 설명

해당 문제에서는 정점 n개, 간선 m개로 구성된 무방향 연결 그래프가 주어진다. 각 간선은 빨간(R) 또는 파란(B) 중 하나의 색상으로 칠해져 있다. 목표는 이 그래프의 스패닝 트리(즉, n개의 정점 모두를 연결하고 사이클이 없는 n-1개의 간선 집합) 중에서 파란색 간선의 개수가 정확히 k개가 되는 스패닝 트리를 만들 수 있는지 여부를 판단하는 것이다.

문제를 자세히 살펴보면 다음과 같다. 그래프 G=(V,E)가 주어지고, 모든 간선에 색상(R 또는 B)이 지정되어 있다. 여기서 스패닝 트리란 V의 모든 정점을 포함하면서 (n-1)개의 간선만을 갖는 트리 구조를 의미한다. 

이때, 우리가 해야 할 일은 다음과 같다.  
1. 가능한 스패닝 트리가 여러 개 존재할 수 있다.  
2. 이 스패닝 트리들 중에서 파란색 간선을 포함하는 최소 갯수(minBlue)와 최대 갯수(maxBlue)를 구해야 한다.  
   - minBlue는 "파란 간선을 최소로 하는 스패닝 트리"를 찾을 때 얻을 수 있다. 파란 간선을 우선적으로 선택하는 것이 아니라, 오히려 빨간 간선을 최대한 선택하여 파란 간선을 최소화하는 식으로 생각할 수 있다. 그런데 직관적으로는 파란 간선을 우선 정렬 후 Kruskal을 실행하면 파란 간선이 최소가 아니라 최대가 될 것 같다는 의문이 생기는데, 여기서 반대로 생각해야 한다. 정렬 기준에 따라 MST 구성 시 어떤 색을 더 쉽게 포함하는지 달라진다. 이 문제의 해결책은 다음 접근 방식에서 상세히 설명한다.  
   - maxBlue는 "파란 간선을 최대한 많이 포함하는 스패닝 트리"를 찾아 얻을 수 있다.  
   
하지만 단순히 "최소"나 "최대"를 구하는 것이 아니라, 둘 다 구한 뒤 주어진 k가 그 사이에 들어 있는지를 보는 것이다. 만약 k가 minBlue와 maxBlue 사이에 존재하면 해당 k를 만족하는 스패닝 트리가 존재하는 것이고, 그렇지 않으면 존재하지 않는다.

구체적인 문제 상황을 예로 들어 생각해보자.  
- n=3, m=3, k=2라고 해보자.  
  간선이 B(1-2), B(2-3), R(3-1)로 주어진다면, 이 그래프에서 가능한 스패닝 트리는 다음과 같다:  
  - {B(1-2), B(2-3)}: 파란 간선 2개  
  - {B(1-2), R(3-1)}: 파란 간선 1개  
  - {B(2-3), R(3-1)}: 파란 간선 1개  
  가능한 파란 간선 수는 최소 1개, 최대 2개이다. 여기서 k=2이면 가능한 트리가 있으므로 결과는 1이다.

크게 문제되는 점은 MST를 구성할 때 가중치가 없고 단순히 색상 정보만 존재한다는 것이다. 이러한 경우에도 Kruskal 알고리즘의 변형을 사용할 수 있다. 정렬 기준을 적절히 활용하면 "파란 간선이 최소가 되는 MST"와 "파란 간선이 최대가 되는 MST"를 쉽게 구할 수 있다. 

정리하자면, 본 문제는 다음과 같은 전략을 취한다.  
1. 간선을 두 가지 기준으로 정렬한 뒤 Kruskal을 수행한다.  
   - 파란 간선을 우선적으로 정렬한 뒤 MST를 구하면 특정 조건에서 파란 간선을 최대 혹은 최소화할 수 있다.  
   - 빨간 간선을 우선적으로 정렬한 뒤 MST를 구하여 반대 조건으로 파란 간선의 반대 극값을 구한다.  
2. 이렇게 얻은 MST들 중 파란 간선의 개수를 각각 minBlue, maxBlue라 하자.  
3. 주어진 k가 minBlue ≤ k ≤ maxBlue 범위 안에 있다면 1을, 아니면 0을 출력한다.

다만 여기서 '파란 우선 정렬'과 '빨간 우선 정렬' 시 어떤 것이 minBlue를 주고 어떤 것이 maxBlue를 주는지 주의 깊게 생각해야 한다. 실제 구현에서는 다음과 같이 한다.

- "파란 우선 정렬": 정렬 시 파란 간선을 우선적으로 선택할 수 있는 형태의 정렬을 통해 MST를 구성하면, 결과적으로 파란 간선 수가 최소가 아니라 최대가 될 것으로 보이지만, 사실 구분을 명확히 하기 위해 두 번 다 해보고, 얻은 값들을 비교하여 minBlue와 maxBlue를 구한다.
- "빨간 우선 정렬": 반대로 빨간 간선을 먼저 선택하려는 정렬을 통해 MST를 구성해 파란 간선 개수의 다른 극값을 얻는다.

결과적으로 두 번의 Kruskal 실행으로 구한 파란 간선 수 두 값 중 작은 것을 minBlue, 큰 것을 maxBlue로 하여 k를 판정한다.


## 접근 방식

이 문제는 스패닝 트리 구성 알고리즘(Kruskal)와 Union-Find 자료 구조를 활용한다. Kruskal 알고리즘은 간선을 가중치 순으로 정렬한 뒤, 순서대로 간선을 선택하면서 사이클이 형성되지 않도록 하는 MST 알고리즘이다. 여기서는 "가중치" 대신 "색상"을 정렬 기준으로 사용한다. 또한 Union-Find(Disjoint Set) 자료 구조를 통해 두 정점이 이미 연결되어 있는지(사이클 발생 여부) 효율적으로 판단한다.

해결 절차는 다음과 같다.  
1. 간선 정보를 읽어들이고, 파란(B)간선과 빨간(R)간선을 구분한다.  
2. 파란 간선을 우선하는 정렬과 빨간 간선을 우선하는 정렬을 각각 수행한다.  
3. 각각의 정렬 기준으로 Kruskal을 실행하여 MST를 구하고, 해당 MST에서 파란 간선 개수를 센다.  
4. 두 번의 결과에서 얻은 파란 간선 개수 중 작은 값을 minBlue, 큰 값을 maxBlue라 한다.  
5. 주어진 k가 이 범위 안에 존재하면 1, 아니면 0을 출력한다.

시간 복잡도는 Kruskal 알고리즘의 복잡도인 O(M log M) 정도이며, n이 최대 1000정도이고 m도 크지 않게 주어질 수 있으므로 제한 시간 내에 충분히 해결 가능하다.

## C++ 코드와 설명

아래는 C++ 표준 라이브러리를 활용한 예시 코드이다.  
- 간선을 입력받은 뒤 두 번 정렬한다.  
- 첫 번째 정렬: 파란색(B)를 먼저, 두 번째 정렬: 빨간색(R)을 먼저  
- 두 번의 Kruskal을 통해 MST의 파란 간선 개수를 구한다.  
- 이를 바탕으로 k 판정 후 결과를 출력한다.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct UnionFind {
    vector<int> p, rankv;
    UnionFind(int n) : p(n+1), rankv(n+1,0){
        for(int i=1; i<=n; i++) p[i] = i;
    }
    int findp(int x){
        return (p[x]==x) ? x : (p[x]=findp(p[x]));
    }
    bool unite(int a,int b){
        a=findp(a);b=findp(b);
        if(a==b) return false;
        if(rankv[a]<rankv[b]) swap(a,b);
        p[b]=a;
        if(rankv[a]==rankv[b]) rankv[a]++;
        return true;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    while(true){
        int n,m,k; 
        cin >> n >> m >> k;
        if(!cin || (n==0 && m==0 && k==0)) break;
        
        vector<array<string,3>> inputEdges(m);
        for(int i=0; i<m; i++){
            string c; int f,t;
            cin >> c >> f >> t;
            inputEdges[i][0] = c;
            inputEdges[i][1] = to_string(f);
            inputEdges[i][2] = to_string(t);
        }
        
        // 파란간선 우선, 빨간간선 우선 두 가지 정렬용 벡터 준비
        vector<tuple<int,int,int>> edgesBlueFirst; 
        vector<tuple<int,int,int>> edgesRedFirst;   
        // c=='B'이면 파란간선, c=='R'이면 빨간간선
        // 파란우선: B=0, R=1
        // 빨강우선: R=0, B=1
        for (auto &e : inputEdges){
            char c = e[0][0];
            int f = stoi(e[1]), t = stoi(e[2]);
            if(c=='B'){
                edgesBlueFirst.push_back({0,f,t});
                edgesRedFirst.push_back({1,f,t});
            } else {
                edgesBlueFirst.push_back({1,f,t});
                edgesRedFirst.push_back({0,f,t});
            }
        }
        
        sort(edgesBlueFirst.begin(), edgesBlueFirst.end());
        sort(edgesRedFirst.begin(), edgesRedFirst.end());
        
        auto kruskalCountBlue = [&](vector<tuple<int,int,int>> &E, bool blueFirst) {
            UnionFind uf(n);
            int cntEdge=0, blueCount=0;
            for (auto &ed : E){
                int c = get<0>(ed);
                int f = get<1>(ed);
                int t = get<2>(ed);
                if(uf.unite(f,t)){
                    cntEdge++;
                    // blueFirst == true이면 c=0일 때 파란간선
                    // blueFirst == false이면 c=1일 때 파란간선
                    if(blueFirst && c==0) blueCount++;
                    if(!blueFirst && c==1) blueCount++;
                    if(cntEdge==n-1) break;
                }
            }
            if(cntEdge<n-1) return -1; // MST 불가능
            return blueCount;
        };
        
        int val1 = kruskalCountBlue(edgesBlueFirst,true);
        int val2 = kruskalCountBlue(edgesRedFirst,false);
        
        if(val1 == -1 || val2 == -1) {
            // MST 불가능
            cout << 0 << "\n";
        } else {
            int minBlue = min(val1,val2);
            int maxBlue = max(val1,val2);
            cout << ((k>=minBlue && k<=maxBlue) ? 1 : 0) << "\n";
        }
    }
    return 0;
}
```

### 코드 동작 단계별 설명

1. **입력 처리**: n(정점 수), m(간선 수), k(목표 파란 간선 수)를 입력받는다.  
2. **간선 분류**: 각 간선 정보(c, f, t)를 받아 "파란우선 벡터"와 "빨강우선 벡터"를 구성한다. 이때 파란우선 벡터에서는 파란간선을 0으로, 빨간간선을 1로 표시하며, 빨강우선 벡터에서는 반대로 한다.  
3. **정렬**: 파란우선 벡터와 빨강우선 벡터를 각각 정렬한다.  
4. **Kruskal 수행**:  
   - 파란우선 벡터를 사용해 MST 구성 시 파란간선 수 계산 (val1)  
   - 빨강우선 벡터를 사용해 MST 구성 시 파란간선 수 계산 (val2)  
5. **값 비교**: val1과 val2 중 작은 값은 가능한 MST 중 파란간선 개수 최소값, 큰 값은 최대값이 된다.  
6. **출력**: k가 [minBlue, maxBlue] 범위에 있으면 1, 아니면 0을 출력한다.

## Python 코드와 설명

아래는 Python을 이용한 예시 코드이다. Python에서도 동일한 접근을 취하며, Union-Find는 직접 구현한다. 파이썬에서는 정렬과 자료구조 관리가 상대적으로 간단하다.

```python
import sys
input=sys.stdin.readline

def findp(p, x):
    if p[x]!=x:
        p[x]=findp(p,p[x])
    return p[x]

def unite(p, rankv, a, b):
    a=findp(p,a)
    b=findp(p,b)
    if a==b:
        return False
    if rankv[a]<rankv[b]:
        p[a]=b
    else:
        p[b]=a
        if rankv[a]==rankv[b]:
            rankv[a]+=1
    return True

def kruskalCountBlue(edges, n, blueFirst):
    p=[i for i in range(n+1)]
    rankv=[0]*(n+1)
    cntEdge=0
    blueCount=0
    for c,f,t in edges:
        if unite(p, rankv, f, t):
            cntEdge+=1
            # blueFirst==True -> c=0일 때 파란간선
            # blueFirst==False -> c=1일 때 파란간선
            if blueFirst and c==0:
                blueCount+=1
            if (not blueFirst) and c==1:
                blueCount+=1
            if cntEdge==n-1:
                break
    if cntEdge<n-1:
        return -1
    return blueCount

while True:
    n,m,k= map(int,input().split())
    if n==0 and m==0 and k==0:
        break
    edgesBlueFirst=[]
    edgesRedFirst=[]
    for _e in range(m):
        line=input().split()
        c=line[0]
        f=int(line[1])
        t=int(line[2])
        if c=='B':
            edgesBlueFirst.append((0,f,t)) # 파란우선: B=0
            edgesRedFirst.append((1,f,t))  # 빨강우선: B=1
        else:
            edgesBlueFirst.append((1,f,t)) # 파란우선: R=1
            edgesRedFirst.append((0,f,t))  # 빨강우선: R=0
    
    edgesBlueFirst.sort(key=lambda x:(x[0],x[1],x[2]))
    edgesRedFirst.sort(key=lambda x:(x[0],x[1],x[2]))
    
    val1=kruskalCountBlue(edgesBlueFirst,n,True)
    val2=kruskalCountBlue(edgesRedFirst,n,False)
    
    if val1==-1 or val2==-1:
        print(0)
    else:
        minBlue=min(val1,val2)
        maxBlue=max(val1,val2)
        print(1 if minBlue<=k<=maxBlue else 0)
```

### 코드 동작 단계별 설명

1. **입력 처리**: n, m, k를 입력받는다.  
2. **간선 정렬 준비**: edgesBlueFirst, edgesRedFirst 리스트에 파란우선 기준과 빨강우선 기준을 각각 구성할 수 있는 c 값을 저장한다.  
3. **정렬**: 간선을 정렬한다.  
4. **Kruskal 실행**: kruskalCountBlue 함수를 통해 MST를 구성하고 파란 간선 수를 센다.  
5. **값 비교 후 출력**: 최소, 최대 파란 간선 수를 구해 k 범위를 확인한 뒤 결과를 출력한다.

## 결론

이 문제는 주어진 그래프에서 특정 색의 간선 수에 대한 조건을 만족하는 스패닝 트리가 존재하는지 판별하는 문제이다. 직접 해당 k를 만족하는 스패닝 트리를 찾아내는 대신, 파란 간선 수의 최소/최대 범위를 효율적으로 계산하여 그 범위 내에 k가 속하는지 확인하는 전략이 핵심이다.

해결 과정에서 MST 알고리즘(Kruskal)와 Union-Find 자료 구조를 활용하였고, 정렬 기준을 두 번 달리하여 파란 간선 수의 가능한 최소값과 최대값을 얻었다. 이로써 문제를 단순하고 직관적으로 해결할 수 있다.

추가적으로, 문제를 더 일반화한다면, 특정 속성을 가진 간선의 개수를 제어하는 변형된 MST 문제를 해결하는 패턴으로 확장할 수 있다. 또한, 향후에는 k에 대한 더 복잡한 조건(예: 최소/최대 값뿐 아니라 다중 제약조건)을 처리하기 위해 다른 알고리즘이나 자료구조를 고려할 여지도 있다. 그러나 현재 문제에서는 간단하고 명확한 접근으로 제한 시간 안에 해결이 가능하다.
