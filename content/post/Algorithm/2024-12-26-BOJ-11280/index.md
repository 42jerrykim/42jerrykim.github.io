---
title: "[Algorithm] C++/Python 백준 11280번 : 2-SAT - 3"
categories: 
- Algorithm
- Graph
- SCC
tags:
- 2-SAT
- SCC
- Graph
- Implementation
- Complexity
- DFS
- Kosaraju
- Problem-Solving
image: "tmp_wordcloud.png"
date: 2024-12-26
---

2-SAT은 불리언 변수가 여러 개 주어졌을 때 2개의 리터럴을 OR로 묶는 절들의 AND로 이루어진 논리식을 만족하도록 변수들을 배정할 수 있는지 판별하는 문제이다. 본 문제인 2-SAT - 3(백준 11280번)은 N개의 불리언 변수와 여러 개의 절이 주어졌을 때, 논리식을 만족하는 변수 배정이 존재하면 1을, 그렇지 않으면 0을 출력하는 문제이다.

문제 : [https://www.acmicpc.net/problem/11280](https://www.acmicpc.net/problem/11280)

## 문제 설명

2-SAT - 3 문제는 다음과 같은 상황으로 구성되어 있다. 우선, 변수의 개수가 N개 존재하고, 각 변수는 참(True) 혹은 거짓(False) 값을 가질 수 있다. 식은 2-CNF 형태이며, 이는 여러 절(Clause)의 AND 연산으로 구성되어 있다. 하나의 절은 두 개의 리터럴의 OR 연산으로 이루어져 있다. 예를 들어서, 절이 \((x \lor \lnot y)\)라면 이는 “x가 True이거나 y가 False이면 참이다”라는 의미이다. 즉, 어떤 변수는 양수 형태로 나타나고, 어떤 변수는 음수(부정) 형태로 나타날 수 있는데, 입력 형식에서는 양수 i가 \(x_i\), 음수 -i가 \(\lnot x_i\)에 해당한다.

문제의 입력으로는 첫째 줄에 N과 M이 주어진다. 여기서 N은 1부터 10,000 사이의 정수이고, M은 1부터 100,000 사이의 정수이다. 다음 M개의 줄에 걸쳐 절을 이루는 두 정수 i, j가 주어진다. 예를 들어 i와 j가 모두 양수이면 절은 \((x_i \lor x_j)\)가 되고, i 또는 j 중 하나가 음수이면 절에는 \(\lnot x_k\) 형태가 포함된다. 우리가 해야 할 일은 이 M개의 절들을 모두 만족하는 변수 배정이 가능한지 판별하는 것이다.

여기서 2-SAT 문제를 푸는 핵심 아이디어는 그래프 이론의 강한 연결 요소(SCC, Strongly Connected Component) 개념을 활용하는 것이다. 두 정수 i, j가 주어졌을 때, 절 \((i \lor j)\)는 논리적으로 \((\lnot i \rightarrow j)\)와 \((\lnot j \rightarrow i)\)로 해석할 수 있다. 이를 그래프로 보면 “\(\lnot i\)에서 j로 가는 방향”과 “\(\lnot j\)에서 i로 가는 방향”의 간선이 생긴다고 생각하면 된다. 그 후 모든 변수를 정점으로 하는 그래프에 대하여 SCC를 구했을 때, 어떤 변수 \(x_i\)와 \(\lnot x_i\)가 같은 SCC에 속한다면 모순이 발생하므로 식을 만족시킬 수 없게 된다. 반대로 모든 \(x_i\)와 \(\lnot x_i\)가 서로 다른 SCC에 속하면 식을 만족하는 해가 존재한다고 결론지을 수 있다.

실제 예시를 들어보면, N=3에 대해 \((\lnot x_1 \lor x_2) \land (\lnot x_2 \lor x_3) \land (x_1 \lor x_3) \land (x_3 \lor x_2)\)라는 식이 주어졌을 때, \(x_1\)을 False, \(x_2\)를 False, \(x_3\)를 True로 설정하면 모든 절이 True로 만들어진다. 반면, 예시로 \((x_1 \lor x_1) \land (\lnot x_1 \lor \lnot x_1)\)처럼 모순되는 식이 들어오면, 어떤 값을 변수에 대입해도 만족시키기 어렵다. 본 문제에서는 이러한 상황을 포괄적으로 다루며, 코딩으로 구현하기 위해서는 간결하고 빠른 SCC 알고리즘(코사라주 또는 타잔 알고리즘)을 적용하게 된다.

위와 같은 2-SAT 문제는 그래프와 논리의 결합을 다루므로, 알고리즘 입문 단계에서 많이 다뤄지는 흥미로운 예시이기도 하다. M이 최대 100,000까지 가능하므로, 효율적인 알고리즘을 설계해야 한다. 일반적으로 O(N+M)의 시간 복잡도를 가지는 SCC 탐색 알고리즘을 사용하면 충분히 제한 시간 내에 해결할 수 있다. 2N개의 정점을 다루는 경우가 많으나, 이는 각 변수마다 x_i와 \(\lnot x_i\)가 분리되어 있기 때문이다. 이 문제는 구현의 정석을 따르거나 라이브러리를 적절히 사용하여 비교적 짧은 코드로도 해결 가능하다.

## 접근 방식

1. **리터럴 인덱스 변환**:  
   \(\lnot x_i\)와 \(x_i\)를 인접 리스트에 표현하기 위해, i를 양수/음수에 따라 적절히 변환해서 0부터 시작하는 인덱스로 매핑해야 한다. 예컨대, \(x_i\)는 \((i-1)*2\), \(\lnot x_i\)는 \((i-1)*2 + 1\) 과 같이 인덱스를 매긴다.

2. **절을 그래프로 변환**:  
   절 \((a \lor b)\)는 \((\lnot a \rightarrow b)\)와 \((\lnot b \rightarrow a)\)로 바꾼다. 양수는 그대로, 음수는 \(\lnot\) 처리된 리터럴의 인덱스에 매핑하여 그래프에 간선을 추가한다.

3. **SCC(Strongly Connected Component) 계산**:  
   그래프의 모든 정점에 대해 SCC를 구한다(코사라주 또는 타잔 알고리즘). 그 결과, 어떤 변수 \(x_i\)와 그 부정 \(\lnot x_i\)가 같은 SCC에 속하면 식을 만족할 수 없다.

4. **결과 도출**:  
   모든 i에 대해 \(x_i\)와 \(\lnot x_i\)가 같은 SCC에 속하는지 확인한다. 만약 하나라도 같은 SCC에 속한다면 0, 전혀 속하지 않는다면 1을 출력한다.

이 접근 방식은 그래프 변환 및 SCC 판별을 통해 문제를 효율적으로 해결한다. 실제 구현에서는 보통 인접 리스트를 사용하고, SCC 알고리즘 중 코사라주(Kosaraju)나 타잔(Tarjan) 방식을 적용한다.

## C++ 코드와 설명

아래 코드는 <bits/stdc++.h>를 사용하여 필요한 라이브러리를 간단히 포함한 버전이다. 2-SAT 문제 해결에 초점을 맞추어 작성하였으며, 코사라주(Kosaraju) 알고리즘 혹은 타잔(Tarjan) 알고리즘을 이용해 SCC를 구할 수 있다. 여기서는 타잔 알고리즘을 예시로 들었다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// (i > 0)  -> (i-1)*2
// (i < 0)  -> (|i|-1)*2 + 1
// 예: x1 -> 0, ¬x1 -> 1, x2 -> 2, ¬x2 -> 3 ...
int idx(int i) {
    if(i > 0) return (i - 1) << 1; 
    return ((-i) - 1) << 1 | 1;
}

// x의 부정 리터럴을 반환
int opp(int x) {
    return x ^ 1;
}

// 전역 변수
static const int MAXN = 20000 * 2; // N 최대 10,000 -> 인덱스는 2*N
vector<int> graphVec[MAXN];
int N, M;

int orderArr[MAXN], sccId[MAXN], orderCount, sccCount;
bool inStack[MAXN];
stack<int> st;

// 타잔 알고리즘을 이용해 SCC를 찾는 DFS
int dfs(int here) {
    orderArr[here] = ++orderCount;
    st.push(here);
    inStack[here] = true;

    int parent = orderArr[here];
    for (int nxt : graphVec[here]) {
        if (!orderArr[nxt]) {
            parent = min(parent, dfs(nxt));
        } else if (inStack[nxt]) {
            parent = min(parent, orderArr[nxt]);
        }
    }

    if (parent == orderArr[here]) {
        sccCount++;
        while(true) {
            int t = st.top();
            st.pop();
            inStack[t] = false;
            sccId[t] = sccCount;
            if (t == here) break;
        }
    }

    return parent;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> N >> M;
    for(int i=0; i<M; i++){
        int a, b;
        cin >> a >> b;
        int A = idx(a), B = idx(b);
        // (a ∨ b)는 (¬a → b)와 (¬b → a)로 변환
        graphVec[opp(A)].push_back(B);
        graphVec[opp(B)].push_back(A);
    }

    // 모든 정점에 대해 타잔 알고리즘으로 SCC 계산
    for(int i=0; i<2*N; i++){
        if(!orderArr[i]) dfs(i);
    }

    // x_i와 ¬x_i가 같은 SCC에 있다면 모순
    for(int i=0; i<N; i++){
        if(sccId[i<<1] == sccId[i<<1|1]){
            cout << 0 << "\n";
            return 0;
        }
    }
    cout << 1 << "\n";
    return 0;
}
```

### 코드 동작 단계별 설명

1. **idx 함수**: 입력된 정수 i가 양수인지 음수인지 판단하여 변수의 인덱스를 구한다. 음수라면 해당 변수의 부정 리터럴을 나타낸다.  
2. **opp 함수**: 어떤 인덱스 x에 대해, x의 0/1 비트를 뒤집어 x의 부정 리터럴을 찾아낸다.  
3. **그래프 구성**: \((a \lor b)\) 절을 \((\lnot a \rightarrow b)\)와 \((\lnot b \rightarrow a)\) 형태로 그래프에 간선으로 추가한다.  
4. **타잔 알고리즘을 사용한 SCC 계산**: 각 정점을 DFS로 방문하면서, 방문 순서와 스택 내부 존재 여부를 체크한다. 가장 작은 방문 순서를 계속 추적하여, 루트가 발견되면 스택에서 추출하며 SCC를 형성한다.  
5. **결과 판별**: 모든 변수 i에 대해 \(x_i\)와 \(\lnot x_i\)가 같은 SCC에 속하는지 확인하고, 모순이면 0, 그렇지 않으면 1을 출력한다.

## Python 코드와 설명

아래는 Python을 사용해 동일한 로직을 구현한 예시이다. 파이썬에서는 재귀 제한에 유의해야 하며, sys.setrecursionlimit 등을 사용하는 것이 좋다.

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def idx(i):
    # i>0 -> (i-1)*2, i<0 -> ((-i)-1)*2+1
    return (abs(i)-1)*2 + (1 if i<0 else 0)

def opp(x):
    return x^1

N, M = map(int, input().split())
graph = [[] for _ in range(2*N)]

for _ in range(M):
    a, b = map(int, input().split())
    A, B = idx(a), idx(b)
    graph[opp(A)].append(B)
    graph[opp(B)].append(A)

order = [0]*(2*N)
scc_id = [0]*(2*N)
visited = [False]*(2*N)
stack = []
order_count, scc_count = 0, 0

def dfs(here):
    global order_count, scc_count
    order_count += 1
    order[here] = order_count
    stack.append(here)
    visited[here] = True

    parent = order[here]
    for nxt in graph[here]:
        if order[nxt] == 0:
            parent = min(parent, dfs(nxt))
        elif visited[nxt]:
            parent = min(parent, order[nxt])

    if parent == order[here]:
        scc_count += 1
        while True:
            t = stack.pop()
            visited[t] = False
            scc_id[t] = scc_count
            if t == here:
                break

    return parent

for i in range(2*N):
    if order[i] == 0:
        dfs(i)

for i in range(N):
    if scc_id[i*2] == scc_id[i*2 + 1]:
        print(0)
        sys.exit(0)

print(1)
```

### 코드 동작 단계별 설명

1. **인덱스 변환**: abs 함수와 부호를 이용해 변수 i가 양수인지 음수인지 구분한다.  
2. **그래프 구성**: \((\lnot A \rightarrow B)\)와 \((\lnot B \rightarrow A)\)의 논리를 그대로 Python 리스트에 저장한다.  
3. **DFS를 통한 SCC 탐색**: order 배열에 방문 순서를 저장하며, parent를 갱신해가면서 루트 노드를 찾는다. 루트 노드가 정해지면 스택에서 해당 SCC를 모두 꺼낸다.  
4. **답 확인**: 각 변수 i의 양 리터럴(i*2)와 음 리터럴(i*2+1)이 같은 SCC에 있으면 불가능(0), 그렇지 않으면 가능(1)을 출력한다.

## 결론

2-SAT - 3(백준 11280번)은 2-CNF 형태의 식에 대해 참값 배정이 가능한지를 그래프 이론과 SCC 알고리즘을 통해 판별하는 전형적인 2-SAT 문제이다. 코드를 살펴보면, 절을 간선으로 변환할 때 \((\lnot a \rightarrow b)\), \((\lnot b \rightarrow a)\)라는 점이 핵심이다. 이를 기반으로 빠르게 SCC를 구하여, 같은 SCC 안에 모순되는 리터럴 쌍이 존재하는지 검사한다. N, M의 범위가 커도 O(N+M) 정도로 해결 가능하므로, 효율적인 방식으로 문제가 잘 해결된다. 실제로는 디테일한 구현(인덱스 변환, 타잔 알고리즘)이 조금 복잡하지만, 알고리즘 자체는 명료하며 활용 가치가 높다. 앞으로 2-SAT 문제를 접할 때, 이 아이디어와 코드를 참고한다면 상당히 수월하게 해결할 수 있을 것으로 보인다.  
