---
title: "[Algorithm] C++/Python 백준 3830번 : 교수님은 기다리지 않는다"
categories: 
- Algorithm
- UnionFind
- DisjointSet
tags:
- UnionFind
- DisjointSet
- WeightedUnionFind
- PathCompression
- DataStructures
- O(M log N)
image: "tmp_wordcloud.png"
date: 2024-10-23
---

이번 포스팅에서는 백준 온라인 저지의 3830번 문제인 **"교수님은 기다리지 않는다"**를 다루어 보겠습니다. 이 문제는 **가중치가 있는 Union-Find(Disjoint Set Union)** 자료구조를 활용하여 해결할 수 있으며, 효율적인 자료구조 활용과 알고리즘 최적화에 대한 이해를 높일 수 있는 좋은 문제입니다.

문제 : [https://www.acmicpc.net/problem/3830](https://www.acmicpc.net/problem/3830)

## 문제 설명

상근이는 매일 아침 실험실로 출근하여 샘플의 무게를 재는 일을 합니다. 그는 두 샘플을 선택한 후 저울을 이용해 그 무게 차이를 측정합니다.

교수님의 관심을 끌기 위해 매일 아침부터 열심히 무게를 재지만, 가끔 교수님이 실험실에 들어와서 특정 두 샘플의 무게 차이를 물어보기도 합니다. 이때 상근이는 지금까지 측정한 결과를 바탕으로 대답할 수도 있고, 그렇지 못할 수도 있습니다.

상근이는 실험실에서 첫날부터 모든 결과를 공책에 기록해 왔지만, 너무 많은 양의 데이터로 인해 교수님의 질문에 신속하게 대답하기가 어렵습니다. 이러한 상근이를 돕기 위해 프로그램을 작성하고자 합니다.

**입력**

- 여러 개의 테스트 케이스로 이루어져 있습니다.
- 각 테스트 케이스의 첫째 줄에는 샘플의 종류의 개수 `N`(2 ≤ N ≤ 100,000)과 상근이가 실험실에서 한 일의 수 `M`(1 ≤ M ≤ 100,000)이 주어집니다.
- 다음 `M`개의 줄에는 상근이가 실험실에서 한 일이 주어집니다.
  - 상근이가 무게를 쟀다면, `! a b w`의 형식으로 주어집니다. 이는 `b`가 `a`보다 `w`그램 무겁다는 뜻입니다. (`a ≠ b`, `w`는 1,000,000을 넘지 않는 음이 아닌 정수)
  - 교수님의 질문은 `? a b`의 형식으로 주어집니다. 이는 `b`가 `a`보다 얼마나 무거운지를 묻는 것입니다.
- 마지막 줄에는 `0`이 두 개 주어집니다.

**출력**

- 교수님의 질문(`? a b`)이 입력될 때마다, 지금까지의 측정 결과를 바탕으로 `a`와 `b`의 무게 차이를 계산할 수 있다면, `b`가 `a`보다 얼마나 무거운지를 출력합니다.
- 무게의 차이의 절댓값이 1,000,000을 넘지 않습니다.
- 계산할 수 없다면 `"UNKNOWN"`을 출력합니다.

**예제 입력**

```
2 2
! 1 2 1
? 1 2
2 2
! 1 2 1
? 2 1
4 7
! 1 2 100
? 2 3
! 2 3 100
? 2 3
? 1 3
! 4 3 150
? 4 1
0 0
```

**예제 출력**

```
1
-1
UNKNOWN
100
200
-50
```

## 접근 방식

이 문제는 **가중치가 있는 Union-Find(Disjoint Set Union with Weights)** 자료구조를 사용하여 해결할 수 있습니다. 일반적인 Union-Find는 각 원소가 어떤 집합에 속하는지를 관리하지만, 이 문제에서는 추가로 두 원소 사이의 무게 차이(가중치)를 관리해야 합니다.

**핵심 아이디어**

- **부모 노드와의 무게 차이**를 저장합니다.
- **경로 압축(Path Compression)**을 활용하여 Union-Find의 효율성을 높입니다.
- 무게 차이를 누적하여 루트까지의 총 무게를 계산합니다.

**알고리즘 단계**

1. **초기화**: 각 샘플은 자기 자신을 부모로 갖고, 무게 차이는 0으로 설정합니다.
2. **Find 연산**: 재귀적으로 부모를 찾아가며, 경로 압축을 수행하고, 무게 차이를 누적합니다.
3. **Union 연산**: 두 샘플의 루트를 찾고, 무게 차이를 계산하여 부모를 갱신합니다.
4. **질의 처리**: 두 샘플이 같은 집합에 속한다면, 무게 차이를 계산하여 출력하고, 그렇지 않다면 `"UNKNOWN"`을 출력합니다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <string>
using namespace std;

const int MAX_N = 100005;

int parent[MAX_N];          // 각 노드의 부모를 저장하는 배열
long long weightDiff[MAX_N]; // 부모 노드와의 무게 차이를 저장하는 배열

// 초기화 함수
void init(int n) {
    for (int i = 1; i <= n; ++i) {
        parent[i] = i;
        weightDiff[i] = 0;
    }
}

// Find 함수: 경로 압축과 무게 차이 누적
int find(int x) {
    if (parent[x] != x) {
        int orig_parent = parent[x];
        parent[x] = find(parent[x]);
        weightDiff[x] += weightDiff[orig_parent];
    }
    return parent[x];
}

// Union 함수: 두 집합을 합치고 무게 차이를 갱신
void unite(int a, int b, long long w) {
    int rootA = find(a);
    int rootB = find(b);
    if (rootA == rootB) return; // 이미 같은 집합인 경우

    // 부모를 rootB로 설정하고, 무게 차이를 갱신
    weightDiff[rootA] = weightDiff[b] - weightDiff[a] - w;
    parent[rootA] = rootB;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (true) {
        int N, M;
        cin >> N >> M;
        if (N == 0 && M == 0) break;
        init(N);

        for (int i = 0; i < M; ++i) {
            string cmd;
            cin >> cmd;
            if (cmd == "!") {
                int a, b;
                long long w;
                cin >> a >> b >> w;
                unite(a, b, w);
            } else if (cmd == "?") {
                int a, b;
                cin >> a >> b;
                if (find(a) != find(b)) {
                    cout << "UNKNOWN\n";
                } else {
                    cout << weightDiff[b] - weightDiff[a] << "\n";
                }
            }
        }
    }

    return 0;
}
```

**코드 설명**

- **parent 배열**: 각 노드의 부모를 저장합니다.
- **weightDiff 배열**: 각 노드와 부모 노드 사이의 무게 차이를 저장합니다.
- **init 함수**: 각 노드를 초기화합니다.
- **find 함수**:
  - 재귀적으로 부모를 찾아갑니다.
  - 경로 압축을 수행하여 부모를 루트로 설정합니다.
  - 무게 차이를 누적하여 루트까지의 총 무게를 계산합니다.
- **unite 함수**:
  - 두 노드의 루트를 찾습니다.
  - 무게 차이를 계산하여 부모 노드의 무게 차이를 갱신합니다.
  - 부모를 갱신하여 두 집합을 합칩니다.
- **메인 함수**:
  - 입력을 받아 초기화합니다.
  - 각 명령에 따라 unite 또는 질의를 수행합니다.
  - 질의 시 두 노드가 같은 집합에 속하는지 확인하고, 무게 차이를 출력합니다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <string.h>

#define MAX_N 100005

int parent[MAX_N];
long long weightDiff[MAX_N];

void init(int n) {
    int i;
    for (i = 1; i <= n; ++i) {
        parent[i] = i;
        weightDiff[i] = 0;
    }
}

int find(int x) {
    if (parent[x] != x) {
        int orig_parent = parent[x];
        parent[x] = find(parent[x]);
        weightDiff[x] += weightDiff[orig_parent];
    }
    return parent[x];
}

void unite(int a, int b, long long w) {
    int rootA = find(a);
    int rootB = find(b);
    if (rootA == rootB) return;

    weightDiff[rootA] = weightDiff[b] - weightDiff[a] - w;
    parent[rootA] = rootB;
}

int main() {
    while (1) {
        int N, M;
        if (scanf("%d %d", &N, &M) != 2) break;
        if (N == 0 && M == 0) break;
        init(N);

        int i;
        for (i = 0; i < M; ++i) {
            char cmd[2];
            scanf("%s", cmd);
            if (cmd[0] == '!') {
                int a, b;
                long long w;
                scanf("%d %d %lld", &a, &b, &w);
                unite(a, b, w);
            } else if (cmd[0] == '?') {
                int a, b;
                scanf("%d %d", &a, &b);
                if (find(a) != find(b)) {
                    printf("UNKNOWN\n");
                } else {
                    printf("%lld\n", weightDiff[b] - weightDiff[a]);
                }
            }
        }
    }

    return 0;
}
```

**코드 설명**

- **입출력**: `stdio.h`의 `scanf`와 `printf`를 사용하여 입력과 출력을 처리합니다.
- **문자열 처리**: `string.h`의 `strcmp`를 사용하지 않고, 단순히 `cmd[0]`을 비교합니다.
- **나머지 로직**: 앞서 설명한 코드와 동일하게 동작하며, 표준 라이브러리의 사용을 최소화했습니다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(1000000)

def input():
    return sys.stdin.readline()

parent = {}
weightDiff = {}

def init(N):
    for i in range(1, N+1):
        parent[i] = i
        weightDiff[i] = 0

def find(x):
    if parent[x] != x:
        orig_parent = parent[x]
        parent[x] = find(parent[x])
        weightDiff[x] += weightDiff[orig_parent]
    return parent[x]

def unite(a, b, w):
    rootA = find(a)
    rootB = find(b)
    if rootA == rootB:
        return
    weightDiff[rootA] = weightDiff[b] - weightDiff[a] - w
    parent[rootA] = rootB

while True:
    line = input()
    if not line:
        break
    N, M = map(int, line.strip().split())
    if N == 0 and M == 0:
        break
    init(N)
    for _ in range(M):
        cmd = input().strip().split()
        if cmd[0] == '!':
            a, b, w = int(cmd[1]), int(cmd[2]), int(cmd[3])
            unite(a, b, w)
        elif cmd[0] == '?':
            a, b = int(cmd[1]), int(cmd[2])
            if find(a) != find(b):
                print("UNKNOWN")
            else:
                print(weightDiff[b] - weightDiff[a])
```

**코드 설명**

- **재귀 한도 증가**: `sys.setrecursionlimit`을 통해 재귀 한도를 늘려줍니다.
- **전역 변수 사용**: `parent`와 `weightDiff`를 전역 딕셔너리로 선언합니다.
- **init 함수**: 각 노드를 초기화합니다.
- **find 함수**:
  - 부모를 재귀적으로 찾고, 경로 압축을 수행합니다.
  - 무게 차이를 누적합니다.
- **unite 함수**:
  - 두 노드의 루트를 찾고, 무게 차이를 갱신합니다.
  - 부모를 갱신하여 집합을 합칩니다.
- **메인 루프**:
  - 입력을 받아 명령에 따라 함수를 호출합니다.
  - 질의에 대한 응답을 출력합니다.

## 결론

이 문제는 가중치가 있는 Union-Find 자료구조의 활용을 요구하는 흥미로운 문제였습니다. 일반적인 Union-Find에 비해 약간의 변형이 필요하지만, 핵심 아이디어를 이해하면 효율적으로 해결할 수 있습니다. 특히 경로 압축과 무게 차이의 누적 관리가 중요했습니다.

추가적으로, 입력 데이터의 크기가 크기 때문에 입출력 속도를 높이기 위한 최적화도 고려해야 합니다. 이를 통해 시간 복잡도를 **O(M log N)**으로 유지하며 효율적인 프로그램을 작성할 수 있었습니다.

이번 문제를 통해 가중치가 있는 Union-Find의 활용과 알고리즘 최적화의 중요성을 다시 한 번 깨달을 수 있었습니다.