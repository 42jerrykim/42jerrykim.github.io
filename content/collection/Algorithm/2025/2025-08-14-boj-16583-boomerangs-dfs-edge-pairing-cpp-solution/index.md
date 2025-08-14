---
title: "[Algorithm] cpp 백준 16583번: Boomerangs - DFS 간선 페어링"
description: "정점 기준으로 미소모 간선을 둘씩 묶어 부메랑 <u,v,w>를 최대화하는 문제. 비재귀 DFS로 즉시 페어링하고 1개는 부모 간선과 결합해 전역 최적 보장. O(N+M), 다중 컴포넌트·트리/사이클 안전."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Graph"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-16583"
- "cpp"
- "C++"
- "Python"
- "Data Structures"
- "자료구조"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Greedy"
- "그리디"
- "Graph"
- "그래프"
- "DFS"
- "BFS"
- "Matching"
- "매칭"
- "Edge Pairing"
- "간선 페어링"
- "Special Judge"
- "스페셜 저지"
- "Disjoint Paths"
- "서로소 경로"
- "Degree"
- "차수"
- "Tree"
- "트리"
- "Back Edge"
- "역방향 간선"
- "Stack DFS"
- "비재귀 DFS"
- "Pairing Strategy"
- "페어링 전략"
- "Proof"
- "증명"
- "Implementation Details"
- "구현 디테일"
- "Edge"
- "간선"
- "Vertex"
- "정점"
- "Connected Components"
- "연결 요소"
- "Adjacency List"
- "인접 리스트"
- "O(N+M)"
image: "wordcloud.png"
---

## 문제
- **링크**: [BOJ 16583 — Boomerangs](https://www.acmicpc.net/problem/16583)
- **요약**: 무방향 단순 그래프에서 정점 `v`를 공유하는 두 간선 `(u,v)`, `(v,w)`로 구성된 부메랑 `<u, v, w>`를 최대 개수로 만들기. 각 간선은 최대 한 번만 사용해야 함.

### 제한/스펙
- `1 ≤ N, M ≤ 100000`
- 간선은 입력에 한 번만 등장하며, `u < v`
- 다중 컴포넌트 가능, 평행 간선 없음

## 입출력
```
입력: N M
다음 M줄: u v (간선)
```
```
출력: K (최대 부메랑 수)
다음 K줄: u v w (부메랑)
```

예시
```
입력
5 7
1 2
1 4
2 3
2 4
2 5
3 4
3 5

출력(예)
3
4 1 2
4 3 2
2 5 3
```

## 접근 개요
- **핵심 아이디어**: 각 정점 `v`에서 아직 사용되지 않은(미소모) incident 간선들을 **둘씩** 묶으면 `<u, v, w>` 부메랑을 만들 수 있음.
- **전역 일관성**: DFS로 트리를 따라가며 각 정점에서 가능한 즉시 페어링. 미소모 간선이 홀수 개 남으면 그중 하나를 **부모로 올라온 간선**과 결합해 페어링하고, 그렇지 않으면 그 부모 간선을 상위로 "전파".
- **보장**: 한 정점당 미소모 간선이 최종적으로 0 또는 1개만 위로 전달되므로, 각 간선을 **최대 한 번**만 사용하면서도 가능한 모든 국소 페어링을 즉시 성사시켜 전역 최적(최대 개수)을 이룸.

## 알고리즘 설계
1. 간선에 ID를 부여하고, 인접 리스트에 `(이웃, 간선ID)`를 저장.
2. `visV[v]`, `visE[id]`로 정점/간선 방문 여부를 관리.
3. DFS(반복/스택 권장)로 내려가며, 이미 방문된 정점으로 향하는 간선을 `v`의 **미소모 목록**에 적재.
4. `v` 처리 종료 시:
   - 미소모 목록에서 2개씩 꺼내 `<u, v, w>`를 만들어 답에 추가.
   - 남은 1개가 있고 부모가 있으면, 그 1개와 `parentEdge`를 묶어 `<u, v, parent>`를 추가.
   - 남은 것이 없고 부모가 있으면, `parentEdge`를 부모에게 **미소모**로 전달.
5. 컴포넌트마다 시작 정점에서 위 과정을 반복.

### 올바름 근거(스케치)
- 각 간선은 최초로 처리되는 공통 정점에서만 사용되므로 **중복 사용 불가** 보장.
- 정점 기준의 **즉시 페어링**은 국소 최적이며, 미소모 1개만 상위로 전달하므로 전체적으로 **최대 수량**을 확보.
- 각 간선·정점은 O(1)회 처리되어 전체 복잡도는 O(N+M).

## 복잡도
- **시간**: O(N+M)
- **공간**: O(N+M)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Edge { int a, b; };

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M; 
    if(!(cin >> N >> M)) return 0;

    vector<Edge> edges(M);
    vector<vector<pair<int,int>>> adj(N+1);
    for(int i=0;i<M;++i){
        int u,v; cin >> u >> v;
        edges[i] = {u,v};
        adj[u].push_back({v,i});
        adj[v].push_back({u,i});
    }

    auto other = [&](int eid, int v){
        return edges[eid].a == v ? edges[eid].b : edges[eid].a;
    };

    vector<char> visV(N+1,0), visE(M,0);
    vector<vector<int>> unpaired(N+1);
    vector<array<int,3>> ans;

    struct Frame{int v,parent,parentEdge; size_t idx;};
    vector<Frame> st;

    for(int s=1;s<=N;++s){
        if(visV[s]) continue;
        st.push_back({s,-1,-1,0});
        while(!st.empty()){
            auto &f = st.back();
            if(!visV[f.v]) visV[f.v] = 1;
            if(f.idx < adj[f.v].size()){
                auto [u,eid] = adj[f.v][f.idx++];
                if(visE[eid]) continue;
                visE[eid] = 1;
                if(!visV[u]) st.push_back({u,f.v,eid,0});
                else unpaired[f.v].push_back(eid);
            }else{
                auto &vec = unpaired[f.v];
                while(vec.size() >= 2){
                    int e1 = vec.back(); vec.pop_back();
                    int e2 = vec.back(); vec.pop_back();
                    int u1 = other(e1, f.v);
                    int u2 = other(e2, f.v);
                    ans.push_back({u1, f.v, u2});
                }
                if(f.parent != -1){
                    if(!vec.empty()){
                        int e1 = vec.back(); vec.pop_back();
                        int u1 = other(e1, f.v);
                        ans.push_back({u1, f.v, f.parent});
                    }else{
                        unpaired[f.parent].push_back(f.parentEdge);
                    }
                }
                st.pop_back();
            }
        }
    }

    cout << (int)ans.size() << '\n';
    for(auto &t: ans) cout << t[0] << ' ' << t[1] << ' ' << t[2] << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    edges = [None]*M
    adj = [[] for _ in range(N+1)]
    for i in range(M):
        u, v = map(int, input().split())
        edges[i] = (u, v)
        adj[u].append((v, i))
        adj[v].append((u, i))

    def other(eid, v):
        a, b = edges[eid]
        return b if a == v else a

    visV = [False]*(N+1)
    visE = [False]*M
    unpaired = [[] for _ in range(N+1)]
    ans = []

    stack = []
    for s in range(1, N+1):
        if visV[s]:
            continue
        stack.append([s, -1, -1, 0])  # v, parent, parentEdge, idx
        while stack:
            v, parent, parentEdge, idx = stack[-1]
            if not visV[v]:
                visV[v] = True
            if idx < len(adj[v]):
                u, eid = adj[v][idx]
                stack[-1][3] += 1
                if visE[eid]:
                    continue
                visE[eid] = True
                if not visV[u]:
                    stack.append([u, v, eid, 0])
                else:
                    unpaired[v].append(eid)
            else:
                vec = unpaired[v]
                while len(vec) >= 2:
                    e1 = vec.pop()
                    e2 = vec.pop()
                    u1 = other(e1, v)
                    u2 = other(e2, v)
                    ans.append((u1, v, u2))
                if parent != -1:
                    if vec:
                        e1 = vec.pop()
                        u1 = other(e1, v)
                        ans.append((u1, v, parent))
                    else:
                        unpaired[parent].append(parentEdge)
                stack.pop()

    print(len(ans))
    for u, v, w in ans:
        print(u, v, w)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 간선이 전혀 없거나(`M=0`) 모두 매칭 불가 구조(모든 정점 차수 ≤ 1)
- 트리(사이클 없음) vs. 사이클/다중 컴포넌트 혼재
- 매우 큰 입력(`N, M = 1e5`)에 대한 비재귀 DFS 처리
- 자기 루프/평행 간선 없음 가정 준수

## 제출 전 점검
- 입출력 형식(개행/공백), 1-indexed 정점 인덱스 유지
- 방문 배열 초기화, 간선 중복 사용 금지(`visE` 필수)
- 미소모 1개 전파 로직: 부모가 없을 때는 절대 올리지 않기
- 시간·공간 O(N+M) 충족(인접 리스트, 선형 순회)

## 참고자료
- [BOJ 16583 — Boomerangs](https://www.acmicpc.net/problem/16583)


