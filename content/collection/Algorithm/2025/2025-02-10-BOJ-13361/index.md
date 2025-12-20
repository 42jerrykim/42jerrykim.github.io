---
title: "[Algorithm] C++ 백준 13361번 : 최고인 대장장이 토르비욘"
description: "백준 13361번 '최고인 대장장이 토르비욘' 문제의 핵심 아이디어와 최적 풀이 방법을 150자 내외로 설명합니다. 각 철판 s, t 값을 그래프 형태로 모델링하고, Union-Find, 좌표 압축, 손실 비용 최소화 등 알고리즘 전략을 실전 코드 중심으로 자세히 다룹니다."
categories: 
- Algorithm
- Graph Theory
- Union-Find
tags:
- Union-Find
- Graph Theory
- Greedy
- Coordinate Compression
- Mathematical Insight
- Disjoint Set
image: "index.png"
date: 2025-02-10
---

본 포스트에서는 백준 13361번 "최고인 대장장이 토르비욘" 문제를 해결한 방법과 코드 구현 과정을 상세하게 설명하고자 한다. 문제의 요구사항과 핵심 아이디어를 이해하고, C++로 최적화된 코드를 작성한 사례를 공유할 것이다. 문제에 내포된 "뒤집어서 생각하기"라는 관점 전환 기법과 Union-Find 자료 구조를 활용한 풀이 전략에 대해 자세히 다루고자 한다.

문제 : [https://www.acmicpc.net/problem/13361](https://www.acmicpc.net/problem/13361)

## 문제 설명

이 문제는 n개의 철판이 주어졌을 때, 각 철판의 두 측면에 해당하는 s와 t라는 정수 값이 주어진다. 철판은 원래 직사각형 모양이며, 이를 한 줄로 용접하여 검을 만드는 상황을 가정한다. 단, 검을 구성하는 철판들의 폭은 반드시 감소하는 순서로 배열되어야 하며, 동일한 폭을 가지면 안 된다. 철판을 뒤집어서 사용할 경우, 철판의 폭이 t가 되고 손실 비용으로 t-s가 발생하게 된다. 반면, 철판을 그대로 사용할 경우 폭은 s가 되며 손실 비용은 발생하지 않는다. 최종적으로 검의 길이는 모든 철판의 t 값의 총합에서 뒤집은 철판들에 대한 손실 비용의 총합을 뺀 값이 된다. 문제에서는 모든 철판을 반드시 사용해야 하며, 유효한 배치가 존재함이 보장된다. 문제의 핵심은 철판의 방향 선택을 어떻게 하느냐에 따라, 폭이 서로 겹치지 않도록 하면서 전체 손실 비용을 최소화하고, 따라서 최종 검의 길이를 최대화하는 방법을 찾는 것이다. 이 문제는 철판의 s와 t를 각각 정점으로 보고, 철판 하나를 두 정점을 잇는 간선으로 표현하는 그래프 문제로도 해석할 수 있다. 연결된 컴포넌트가 트리 형태일 경우 그룹 내 모든 정점의 합에서 최대값을 빼주고, 사이클이 존재하는 경우 그룹 내 모든 값의 합을 손실 비용으로 계산하는 방식으로 문제를 해결할 수 있다. 이러한 아이디어는 "뒤집어서 생각하기" 기법을 응용한 것으로, 문제 해결의 관점을 전환하는 핵심 포인트이다.

## 접근 방식

문제를 해결하기 위해 먼저 모든 철판의 s와 t 값을 합산한 후, 철판의 방향 선택에 따른 손실 비용을 최소화하는 문제로 전환할 수 있다. 이를 위해 다음과 같은 단계로 접근하였다.

1. **좌표 압축 (Coordinate Compression)**  
   철판의 s와 t 값들이 매우 클 수 있으므로, 모든 값들을 하나의 배열에 모은 후 정렬하여 중복을 제거함으로써 좌표 압축을 수행한다. 이를 통해 Union-Find 자료 구조의 인덱스로 사용할 수 있게 된다.

2. **Union-Find를 이용한 그룹화**  
   각 철판을 두 정점을 잇는 간선으로 생각하고, 좌표 압축된 값을 이용하여 두 정점을 Union-Find로 연결한다. 이때 같은 그룹에 속한 정점들은 철판의 방향 선택이 서로 영향을 미치게 된다. 그룹 내에서 사이클이 형성되었는지 여부에 따라 손실 비용 계산 방식이 달라진다.

3. **손실 비용 계산**  
   그룹별로 정점들의 합(sum)과 최대값(max)을 구한다. 만약 그룹이 트리 구조(사이클이 없는 경우)라면, 손실 비용은 그룹 내 합에서 최대값을 뺀 값이 된다. 사이클이 존재하는 경우에는 그룹 내 모든 값의 합이 손실 비용이 된다.

4. **최종 답 도출**  
   전체 철판의 s와 t 값의 합에서 각 그룹별 손실 비용을 차감하면, 조건에 맞게 모든 철판을 사용하여 만들 수 있는 검의 최대 길이를 구할 수 있게 된다.

이와 같이 Union-Find와 좌표 압축 기법, 그리고 "뒤집어서 생각하기" 전략을 적절히 결합하여 문제를 해결할 수 있다.

## C++ 코드와 설명

다음은 최적화된 C++ 코드이다. 각 줄별로 주석을 추가하여 코드의 동작을 상세하게 설명하고 있다.

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long

typedef long long ll;
typedef pair<ll, ll> pll;

// 전역 변수 선언이다.
int n;                              // 철판의 개수를 저장하는 변수이다.
vector<pll> plates;                 // 각 철판의 (s, t) 값을 저장하는 벡터이다.
vector<ll> comp;                    // 좌표 압축을 위한 s와 t 값들을 저장하는 벡터이다.
ll ans;                             // 최종 검의 길이를 저장할 변수이다.

int par[505050];                    // Union-Find에서 각 정점의 부모를 저장하는 배열이다.
ll mx[505050];                      // 각 그룹에서 최대값을 저장하는 배열이다.
ll sumVal[505050];                  // 각 그룹 내 정점들의 합을 저장하는 배열이다.
int cycle[505050];                  // 각 그룹에 사이클 존재 여부를 저장하는 배열이다.

// Union-Find 초기화 함수이다.
void initUnionFind(int size) {
    for (int i = 0; i < size; i++) {
        par[i] = i;               // 초기에는 자기 자신이 부모이다.
        mx[i] = comp[i];          // 초기에는 해당 정점의 값이 최대값이다.
        sumVal[i] = comp[i];      // 초기에는 해당 정점의 값이 그룹 합이다.
        cycle[i] = 0;             // 초기에는 사이클이 없다고 설정한다.
    }
}

// Union-Find의 find 함수이다. 경로 압축을 수행한다.
int findUF(int v) {
    return (v == par[v]) ? v : par[v] = findUF(par[v]);  // 부모를 재귀적으로 찾으며 경로 압축을 수행한다.
}

// 두 정점을 합치는 merge 함수이다.
// 이미 같은 그룹인 경우 false를 반환하고, 사이클 발생을 표시한다.
bool mergeUF(int u, int v) {
    u = findUF(u), v = findUF(v);
    if (u == v) return false;       // 이미 같은 그룹이면 합치지 않고 false를 반환한다.
    par[u] = v;                    // u의 부모를 v로 설정한다.
    mx[v] = max(mx[u], mx[v]);     // 그룹 v의 최대값을 갱신한다.
    sumVal[v] += sumVal[u];        // 그룹 v의 합을 갱신한다.
    cycle[v] = cycle[u] || cycle[v]; // 그룹 내 사이클 여부를 갱신한다.
    return true;                   // 합치기에 성공하면 true를 반환한다.
}

// 좌표 압축된 comp 벡터에서 값 x의 인덱스를 반환하는 함수이다.
int idx(ll x) {
    return lower_bound(comp.begin(), comp.end(), x) - comp.begin();
}

signed main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 철판의 개수를 입력받는다.
    cin >> n;
    plates.resize(n);
    comp.reserve(n * 2);
    // 각 철판의 s와 t 값을 입력받으며 좌표 압축용 벡터에 추가한다.
    for (int i = 0; i < n; i++){
        cin >> plates[i].first >> plates[i].second;
        comp.push_back(plates[i].first);
        comp.push_back(plates[i].second);
    }
    // 좌표 압축을 위해 comp 벡터를 정렬하고 중복을 제거한다.
    sort(comp.begin(), comp.end());
    comp.erase(unique(comp.begin(), comp.end()), comp.end());

    // comp 벡터의 크기만큼 Union-Find를 초기화한다.
    initUnionFind(comp.size());

    // 각 철판을 두 정점을 잇는 간선으로 보고, 해당 정점들을 Union-Find로 연결한다.
    for (int i = 0; i < n; i++){
        int u = idx(plates[i].first);
        int v = idx(plates[i].second);
        if (!mergeUF(u, v)) {       // 이미 같은 그룹인 경우라면 사이클 발생을 표시한다.
            cycle[findUF(u)] = 1;
        }
    }

    // 전체 철판의 s와 t 값의 합을 ans에 더한다.
    ans = 0;
    for (int i = 0; i < n; i++){
        ans += plates[i].first + plates[i].second;
    }

    // 각 좌표 압축된 값의 대표 그룹에 대해 손실 비용을 계산한다.
    // 그룹이 사이클이면 그룹 내 모든 값의 합이 손실 비용이다.
    // 그룹이 트리 구조이면 그룹 내 합에서 최대값을 뺀 값이 손실 비용이다.
    for (int i = 0; i < (int)comp.size(); i++){
        if (findUF(i) != i) continue;   // 대표 정점이 아니면 건너뛴다.
        if (cycle[i]) {
            ans -= sumVal[i];
        } else {
            ans -= (sumVal[i] - mx[i]);
        }
    }

    // 최종 검의 길이를 출력한다.
    cout << ans << "\n";
    return 0;
}
```

위 C++ 코드는 좌표 압축과 Union-Find 자료 구조를 이용하여 각 철판의 s와 t 값을 그룹화하고, 그룹별 손실 비용을 계산한 후 전체 손실 비용을 전체 합에서 빼어 최종 검의 길이를 구하는 방식으로 동작한다.

## 결론

본 문제는 단순해 보이지만, “뒤집어서 생각하기” 기법과 Union-Find 자료 구조를 적절히 활용하여 문제의 복잡한 조건을 간단하게 해결할 수 있음을 보여준다. 좌표 압축과 그룹별 손실 비용 계산을 통해 검의 최대 길이를 효율적으로 구할 수 있었다. 두 가지 언어로 구현한 코드를 통해 다양한 구현 방식의 장점을 확인할 수 있었으며, 추가적인 최적화 방안으로는 입력 처리 속도 개선 및 메모리 관리 기법을 고려할 수 있음을 느꼈다.
