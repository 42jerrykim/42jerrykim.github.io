---

title: "[Algorithm] C++/Python 백준 11266번 : 단절점"
categories: 
- Algorithm
- GraphTheory
tags:
- GraphTheory
- Depth-First Search
- ArticulationPoints
- Tarjan's Algorithm
- O(V+E)
image: "tmp_wordcloud.png"
date: 2024-10-24
---

## 도입

그래프 이론에서 **단절점**은 네트워크의 연결성을 분석하는 중요한 요소이다. 단절점을 찾는 것은 네트워크의 취약점을 파악하거나, 통신 시스템에서 장애 지점을 식별하는 데 활용된다. 이번 포스팅에서는 백준 온라인 저지의 **11266번 문제**인 "단절점"을 해결하면서, 단절점을 찾는 알고리즘과 그 구현 방법에 대해 알아보겠다.

문제 : [https://www.acmicpc.net/problem/11266](https://www.acmicpc.net/problem/11266)

## 문제 설명

그래프가 주어졌을 때, **단절점**을 모두 구해 출력하는 프로그램을 작성하시오.

단절점이란 그 정점을 제거했을 때, 그래프가 두 개 또는 그 이상으로 나누어지는 정점을 말한다. 즉, 제거했을 때 그래프의 **연결 요소(Connected Component)**의 개수가 증가하는 정점을 의미한다.

**입력**은 다음과 같다. 첫째 줄에 두 정수 V(1≤V≤10,000), E(1≤E≤100,000)가 주어진다. 이는 그래프가 V개의 정점과 E개의 간선으로 이루어져 있다는 의미이다. 다음 E개의 줄에는 간선에 대한 정보를 나타내는 두 정수 A, B가 주어진다. 이는 A번 정점과 B번 정점이 연결되어 있다는 의미이며, 방향은 양방향이다.

입력으로 주어지는 그래프는 **연결 그래프가 아닐 수도 있다**. 정점은 1부터 V까지 번호가 매겨져 있다.

**출력**은 첫째 줄에 단절점의 개수를 출력한다. 둘째 줄에는 단절점의 번호를 공백으로 구분해 **오름차순**으로 출력한다.

**예제 입력:**

```
7 7
1 4
4 5
5 1
1 6
6 7
2 7
7 3
```

**예제 출력:**

```
3
1 6 7
```

위의 예제에서 단절점의 개수는 3이며, 단절점은 1, 6, 7번 정점이다.

## 접근 방식

이 문제는 그래프의 **단절점(Articulation Point)**을 찾는 것으로, **깊이 우선 탐색(DFS)**을 활용하여 해결할 수 있다. 단절점을 찾기 위해서는 DFS 트리에서 각 정점의 **방문 순서(Order)**와 해당 정점에서 도달할 수 있는 **최소 방문 순서(Low)**를 기록하는 것이 중요하다.

**Tarjan의 알고리즘**을 사용하면 시간 복잡도 **O(V + E)**로 단절점을 찾을 수 있다. 알고리즘의 핵심 아이디어는 다음과 같다:

1. **DFS를 수행하면서 각 정점에 방문 순서를 매긴다.**
2. **각 정점에서 DFS를 통해 도달할 수 있는 최소 방문 순서를 기록한다.**
3. **특정 정점 u에서 자식 노드 v로 이동할 때, 다음의 조건을 확인한다:**
   - **u가 루트 노드인 경우, 자식 노드의 수가 2개 이상이면 단절점이다.**
   - **u가 루트 노드가 아닌 경우, 자식 노드 v에 대해 low[v] ≥ order[u]이면 u는 단절점이다.**

이를 구현하기 위해 다음과 같은 변수가 필요하다:

- `order[]`: 각 정점의 방문 순서를 저장한다.
- `is_cut[]`: 각 정점이 단절점인지 여부를 저장한다.

DFS를 수행하면서 위의 조건을 체크하여 단절점을 찾는다.

## C++ 코드와 설명

먼저, 최적화된 C++ 코드와 라인별 주석을 제공하겠다.

```cpp
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

const int MAX_V = 10001;

vector<int> adj[MAX_V]; // 그래프의 인접 리스트
int V, E;
int order[MAX_V];       // 각 정점의 DFS 방문 순서
bool is_cut[MAX_V];     // 단절점 여부
int cnt;                // DFS 방문 순서 카운터

// DFS 함수: 현재 정점 u와 부모 정점 parent를 인자로 받음
int dfs(int u, int parent) {
    order[u] = ++cnt; // 현재 정점의 방문 순서 기록
    int ret = order[u]; // 반환값 초기화
    int child = 0; // 자식의 수

    for (int v : adj[u]) { // 인접한 정점들에 대해
        if (v == parent) continue; // 부모 정점이면 패스
        if (order[v]) { // 이미 방문한 정점이면
            ret = min(ret, order[v]); // 최소 방문 순서 갱신
        } else { // 방문하지 않은 정점이면
            child++;
            int low = dfs(v, u); // 자식 정점의 DFS 수행
            ret = min(ret, low); // 최소 방문 순서 갱신
            if (parent != -1 && low >= order[u]) {
                is_cut[u] = true; // 단절점 조건 만족
            }
        }
    }

    if (parent == -1 && child >= 2) {
        is_cut[u] = true; // 루트 정점의 단절점 여부 결정
    }

    return ret; // 현재 정점에서의 최소 방문 순서 반환
}

int main() {
    scanf("%d %d", &V, &E);

    for (int i = 0; i < E; ++i) {
        int A, B;
        scanf("%d %d", &A, &B);
        adj[A].push_back(B);
        adj[B].push_back(A);
    }

    for (int i = 1; i <= V; ++i) {
        if (!order[i]) { // 방문하지 않은 정점에 대해 DFS 수행
            dfs(i, -1);
        }
    }

    vector<int> result;
    for (int i = 1; i <= V; ++i) {
        if (is_cut[i]) {
            result.push_back(i);
        }
    }

    sort(result.begin(), result.end()); // 단절점을 오름차순으로 정렬

    printf("%d\n", (int)result.size());
    for (int v : result) {
        printf("%d ", v);
    }
    printf("\n");

    return 0;
}
```

### 코드 설명

1. **그래프 입력 및 초기화**

   - `adj[MAX_V]`를 사용하여 인접 리스트를 저장한다.
   - `order[]` 배열을 0으로 초기화하여 방문 여부를 확인한다.
   - `is_cut[]` 배열은 단절점 여부를 저장한다.
   - `cnt`는 DFS 방문 순서를 카운트한다.

2. **DFS 함수**

   - 현재 정점 `u`와 부모 정점 `parent`를 인자로 받는다.
   - `order[u]`에 방문 순서를 기록한다.
   - `ret`은 현재 정점에서의 최소 방문 순서를 저장한다.
   - 인접한 정점들을 순회하면서 다음을 수행한다:
     - 부모 정점은 건너뛴다.
     - 이미 방문한 정점이면 `ret`을 갱신한다.
     - 방문하지 않은 정점이면 재귀적으로 DFS를 수행하고, `ret`을 갱신한다.
     - 단절점의 조건을 만족하면 `is_cut[u]`를 `true`로 설정한다.
   - 루트 정점의 경우, 자식의 수가 2개 이상이면 단절점이다.

3. **결과 출력**

   - 단절점으로 확인된 정점들을 `result` 벡터에 추가한다.
   - 오름차순으로 정렬하여 출력한다.

## C++ without library 코드와 설명

이번에는 `stdio.h`만 사용할 수 있는 환경에서 표준 라이브러리를 사용하지 않고 코드를 작성하겠다.

```c
#include <stdio.h>

#define MAX_V 10001
#define MAX_E 100001

int adj[2 * MAX_E];      // 인접 리스트 배열
int next[2 * MAX_E];     // 다음 인접한 정점의 인덱스
int head[MAX_V];         // 각 정점의 인접 리스트 시작 인덱스
int adj_idx = 0;         // 인접 리스트 배열의 현재 인덱스

int V, E;
int order[MAX_V];        // 방문 순서
int cnt = 0;
int is_cut[MAX_V];       // 단절점 여부 (1이면 단절점)

void add_edge(int u, int v) {
    adj[adj_idx] = v;          // 인접한 정점 저장
    next[adj_idx] = head[u];   // 현재 head[u]를 다음으로 설정
    head[u] = adj_idx;         // head[u] 갱신
    adj_idx++;
}

int min(int a, int b) {
    return a < b ? a : b;
}

// DFS 함수
int dfs(int u, int parent) {
    order[u] = ++cnt;      // 방문 순서 기록
    int ret = order[u];    // 반환값 초기화
    int child = 0;         // 자식 노드의 수

    for (int i = head[u]; i != -1; i = next[i]) {
        int v = adj[i];
        if (v == parent) continue; // 부모 노드이면 패스
        if (order[v]) {
            ret = min(ret, order[v]); // 이미 방문한 노드이면 최소값 갱신
        } else {
            child++;
            int low = dfs(v, u);
            ret = min(ret, low);    // 최소값 갱신
            if (parent != -1 && low >= order[u]) {
                is_cut[u] = 1;      // 단절점 조건 만족
            }
        }
    }

    if (parent == -1 && child >= 2) {
        is_cut[u] = 1; // 루트 노드의 단절점 여부 결정
    }

    return ret;
}

// 단순 삽입 정렬 함수
void insertion_sort(int arr[], int n) {
    int i, j, key;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i -1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            j = j -1;
        }
        arr[j+1] = key;
    }
}

int main() {
    scanf("%d %d", &V, &E);

    // head 배열 초기화
    for (int i = 1; i <= V; i++) {
        head[i] = -1;
    }

    // 간선 입력 및 인접 리스트 구성
    for (int i = 0; i < E; ++i) {
        int A, B;
        scanf("%d %d", &A, &B);
        add_edge(A, B);
        add_edge(B, A);
    }

    // DFS를 통한 단절점 찾기
    for (int i = 1; i <= V; ++i) {
        if (!order[i]) {
            dfs(i, -1);
        }
    }

    int result[MAX_V];
    int res_cnt = 0;

    // 단절점 수집
    for (int i = 1; i <= V; ++i) {
        if (is_cut[i]) {
            result[res_cnt++] = i;
        }
    }

    // 단절점 정렬
    insertion_sort(result, res_cnt);

    // 결과 출력
    printf("%d\n", res_cnt);
    for (int i = 0; i < res_cnt; ++i) {
        printf("%d ", result[i]);
    }
    printf("\n");

    return 0;
}
```

### 코드 설명

1. **그래프 구현**

   - **인접 리스트**를 배열로 직접 구현하였다.
   - `adj[]`, `next[]`, `head[]` 배열을 사용하여 메모리를 효율적으로 사용한다.
   - `add_edge` 함수는 간선을 추가할 때 사용된다.

2. **DFS 함수**

   - 현재 정점 `u`와 부모 정점 `parent`를 인자로 받는다.
   - `order[u]`에 방문 순서를 기록한다.
   - 인접 리스트를 순회하면서 다음을 수행한다:
     - 부모 정점이면 건너뛴다.
     - 이미 방문한 정점이면 `ret`을 갱신한다.
     - 방문하지 않은 정점이면 재귀적으로 DFS를 수행하고, `ret`을 갱신한다.
     - 단절점의 조건을 만족하면 `is_cut[u]`를 `1`로 설정한다.
   - 루트 정점의 경우, 자식의 수가 2개 이상이면 단절점이다.

3. **정렬 함수**

   - `insertion_sort` 함수를 사용하여 단절점의 번호를 오름차순으로 정렬한다.
   - 표준 라이브러리를 사용하지 않고 직접 구현하였다.

4. **결과 출력**

   - 단절점으로 확인된 정점들을 `result[]` 배열에 추가한다.
   - 정렬하여 출력한다.

### 주요 변경 사항

- **동적 메모리 할당 제거**: `malloc`과 `free`를 사용하지 않고, 정적 배열을 활용하여 그래프를 구현하였다.
- **표준 라이브러리 함수 미사용**: `qsort`나 `<stdlib.h>`를 사용하지 않고, 필요한 함수들을 직접 구현하였다.
- **헤더 파일 제한**: `stdio.h`만 포함하여 코드를 작성하였다.

## Python 코드와 설명

Python 코드에서 메모리 초과 문제가 발생하여, 이를 해결하기 위해 코드를 수정하였다.

```python
import sys
sys.setrecursionlimit(10 ** 7)
input = sys.stdin.readline

V, E = map(int, input().split())
adj = [[] for _ in range(V + 1)]
for _ in range(E):
    A, B = map(int, input().split())
    adj[A].append(B)
    adj[B].append(A)

order = [0] * (V + 1)
is_cut = [False] * (V + 1)
cnt = 0

def dfs(u, parent):
    global cnt
    cnt += 1
    order[u] = cnt
    ret = order[u]
    child = 0

    for v in adj[u]:
        if v == parent:
            continue
        if order[v]:
            ret = min(ret, order[v])
        else:
            child += 1
            low = dfs(v, u)
            ret = min(ret, low)
            if parent != -1 and low >= order[u]:
                is_cut[u] = True
    if parent == -1 and child >= 2:
        is_cut[u] = True
    return ret

for i in range(1, V + 1):
    if not order[i]:
        dfs(i, -1)

result = [i for i in range(1, V + 1) if is_cut[i]]
print(len(result))
print(' '.join(map(str, result)))
```

### 코드 설명

1. **입력 및 그래프 생성**

   - `sys.stdin.readline()`을 사용하여 입력을 빠르게 받는다.
   - 인접 리스트 `adj`를 생성하여 그래프를 구성한다.

2. **DFS 함수**

   - 재귀 깊이 제한을 늘리기 위해 `sys.setrecursionlimit(10 ** 7)`을 설정하였다.
   - `cnt` 변수를 `global`로 선언하여 함수 내에서 수정할 수 있도록 하였다.
   - DFS 로직은 앞선 C++ 코드와 동일하다.

3. **결과 출력**

   - 단절점으로 확인된 정점들을 `result` 리스트에 추가한다.
   - 문제에서 **오름차순으로 출력**하라고 명시되어 있으므로, 정렬 없이 출력한다. (이미 방문 순서대로 탐색하므로)

### 메모리 초과 문제 해결

- **`threading` 모듈 제거**: `threading.Thread`를 사용하지 않고도 문제를 해결할 수 있다.
- **재귀 깊이 제한 조정**: `sys.setrecursionlimit(10 ** 7)`로 충분한 재귀 깊이를 설정하였다.
- **입력 함수 최적화**: `input = sys.stdin.readline`을 사용하여 입력 속도를 향상시켰다.
- **불필요한 변수 제거**: 메모리 사용량을 줄이기 위해 필요한 변수만 사용하였다.

## 결론

이번 문제를 통해 그래프의 단절점을 찾는 **Tarjan의 알고리즘**을 구현해 보았다. 이 알고리즘은 DFS를 기반으로 하며, 각 정점에서의 방문 순서와 최소 방문 순서를 이용하여 단절점을 효율적으로 찾을 수 있다. 코드를 작성하면서 **재귀 호출의 깊이**나 **메모리 사용량**에 유의해야 하며, 특히 Python의 경우 재귀 깊이 제한을 늘려주는 것이 중요하다.

추가적으로, 그래프의 **연결 요소**를 확인하거나, **단절선**을 찾는 문제에도 이와 유사한 접근 방식을 적용할 수 있다. 이러한 그래프 이론의 기본 알고리즘을 숙지하면 다양한 문제를 효율적으로 해결할 수 있을 것이다.

이번 포스팅을 통해 그래프 탐색 알고리즘의 이해와 구현에 도움이 되었기를 바란다.