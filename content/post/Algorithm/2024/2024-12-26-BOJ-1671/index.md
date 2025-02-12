---
title: "[Algorithm] C++/Python 백준 1671번 : 상어의 저녁식사"
categories: 
- Algorithm
- BipartiteMatching
- MaximumFlow
tags:
- bipartite
- matching
- maxflow
- optimization
- O(N^2)
- DataStructure
- GraphTheory
- DynamicProgramming
image: "tmp_wordcloud.png"
date: 2024-12-26
---

상어들 사이에서 벌어지는 포식 관계를 다루는 문제이므로, 매우 흥미롭고 직관적인 발상이 요구되는 문제이다. 한 상어가 특정 조건을 만족하면 다른 상어를 먹을 수 있고, 그 과정에서 한 상어는 최대 두 번까지 다른 상어를 잡아먹을 수 있도록 제한된다. 이러한 제약 조건을 그래프 이론에서의 Bipartite Matching으로 적절히 변형해 풀 수 있다는 점이 흥미롭다. 상어가 서로를 잡아먹는 과정을 간선으로 표현하여 최대 매칭을 구하면, 생존 상어 수의 최솟값을 효율적으로 구할 수 있다.

문제 : [https://www.acmicpc.net/problem/1671](https://www.acmicpc.net/problem/1671)

## 문제 설명

이 문제의 배경은 여러 마리의 상어들이 서로를 포식하는 상황에서, 상어들의 왕 김재홍이 “한 상어가 최대 두 마리의 상어만 잡아먹을 수 있다”는 제약을 건다는 설정이다. 각 상어는 (크기, 속도, 지능)이라는 세 가지 정수 능력치로 표현되며, 어떤 상어 A의 능력치가 상어 B의 능력치 이상(크거나 같음)일 경우 A가 B를 잡아먹을 수 있다. 단, 능력치가 모두 똑같은 경우에는 인덱스가 작은 상어가 더 큰 인덱스를 가진 상어를 먹을 수 있다는 추가 조건이 있다. 

상어가 서로 먹는 과정에서 한 번에 한 상어만이 다른 상어를 잡아먹을 수 있으며, 이미 잡아먹힌 상어는 다른 상어를 잡아먹는 행위를 할 수 없다. 이렇게 제한된 환경에서 상어들은 서로에게 유리한 방식으로 최대한 많이 먹으려고 하며, 결국 남아 있는 상어가 최소가 되도록 행동하게 된다. 우리에게 주어진 목표는 이 최종 상황에서 살아남아 있는 상어의 최소 개수를 계산하는 것이다.

N마리 상어 각각에 대해, 크기(size), 속도(speed), 지능(intelligence)는 최대 2,000,000,000까지 가능하다. 그러나 N의 최댓값은 50이므로, 상호 비교를 해도 최대 50×50의 비교만 고려하면 되며, 이분 매칭 알고리즘도 O(N^3) 정도의 연산으로 해결 가능하다. 핵심은 “한 상어가 두 마리까지 잡아먹을 수 있다”는 특수 규칙을 어떻게 구현하느냐인데, 이를 위해 왼쪽 집합에서 각 상어 노드를 두 번 복제하는 아이디어를 사용할 수 있다. 

보다 구체적으로 살펴보면 다음과 같은 점이 중요하다. 첫째, 상어 i가 상어 j를 먹을 수 있는지 여부는 (size_i ≥ size_j) ∧ (speed_i ≥ speed_j) ∧ (intel_i ≥ intel_j) 조건으로 확인한다. 둘째, 만약 이 세 능력치가 모두 같은 경우라면, i < j일 때만 i가 j를 먹을 수 있다고 처리한다. 셋째, i가 j를 먹을 수 있다면, 이분 그래프에서 왼쪽 노드 i와 i+N을 오른쪽 노드 j에 연결한다. 이렇게 하면 i라는 상어가 최대 두 번까지 다른 상어와 매칭될 수 있다. 마지막으로 최대 매칭값을 구하면 그것이 ‘잡아먹힌 상어의 총 수’가 되고, 전체 상어 수 N에서 이를 빼주면 최종적으로 남는 상어 수가 된다. 

즉, 문제를 요약하자면, 상어들을 이분 그래프로 모델링하여 “한 노드(i번 상어)가 오른쪽 노드(j번 상어)와 매칭된다”는 것을 “i번 상어가 j번 상어를 먹는 행위”로 대응시키는 것이다. i번 상어가 2마리를 먹을 수 있도록 i번 노드를 2개로 복제하여 매칭을 수행한다면, 자연스럽게 “한 상어가 최대 두 마리를 먹는다”는 조건을 충족할 수 있다. 그런 뒤에, 오그멘팅 경로를 찾는 과정으로 최대 매칭을 구하고, 매칭된 수가 잡아먹힌 상어의 수가 된다. 이 과정을 통해 안정적으로 문제를 해결할 수 있으며, N ≤ 50의 범위에서 무난히 동작한다.

## 접근 방식

1. **이분 그래프 구성**  
   - 왼쪽 집합: 상어 노드 N개를 2배로 복제한 2N개의 노드  
   - 오른쪽 집합: 원본 상어 N마리 그대로 N개의 노드  
   - 간선 연결: i번 상어가 j번 상어를 먹을 수 있으면, (i, j)와 (i+N, j)에 간선을 연결한다  

2. **포식 조건**  
   - (size_i ≥ size_j) ∧ (speed_i ≥ speed_j) ∧ (intel_i ≥ intel_j)일 때 i가 j를 먹을 수 있음  
   - 능력이 모두 같으면 i < j라는 인덱스 조건을 만족해야 i가 j를 먹는다고 간주  

3. **최대 이분 매칭**  
   - DFS 기반 알고리즘 또는 Hopkroft-Karp 알고리즘 등을 통해 최대 매칭을 구한다.  
   - 매칭된 간선의 수 = 잡아먹힌 상어의 수  

4. **결과 산출**  
   - 전체 상어 수 N에서 최대 매칭 수를 빼주면, 남는 상어 수의 최솟값이 된다.  

## C++ 코드와 설명

아래는 최적화된 C++ 코드 예시이다. 각 라인마다 주석을 달아, 코드가 어떤 식으로 동작하는지 명시하였다. N의 최댓값(50)에서 이분 매칭으로 충분히 해결 가능한 구조이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// 상어 정보 저장용 구조체
struct Shark {
    long long size;
    long long speed;
    long long intel;
};

// 전역 변수
int N;
vector<Shark> sharks;
// adj[i]: i번 왼쪽 노드가 연결될 수 있는 오른쪽 노드 목록
// 왼쪽 노드: 총 2N개 (각 상어 * 2), 오른쪽 노드: N개
vector<vector<int>> adj;
vector<int> matchR;   // 오른쪽 노드에 매칭된 왼쪽 노드 (없으면 -1)
vector<bool> visited; // 매칭 탐색 시 방문 여부

// 이분 매칭 시도 함수
bool tryMatch(int i) {
    for (int r : adj[i]) {
        // 이미 방문한 노드는 패스
        if (visited[r]) continue;
        visited[r] = true;
        // 매칭이 안 되어 있거나, 매칭된 다른 왼쪽 노드를 다른 곳으로 보낼 수 있다면
        if (matchR[r] == -1 || tryMatch(matchR[r])) {
            matchR[r] = i;
            return true;
        }
    }
    return false;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N;
    sharks.resize(N);

    // N마리 상어 정보 입력
    for(int i = 0; i < N; i++){
        cin >> sharks[i].size >> sharks[i].speed >> sharks[i].intel;
    }

    // 인접 리스트 초기화: 왼쪽 노드 2N개
    adj.assign(2*N, {});

    // i번 상어가 j번 상어를 먹을 수 있는지 판단 후, 간선 연결
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(i == j) continue; // 자기 자신은 제외
            // i가 j를 먹을 수 있는지?
            bool canEat = false;

            // 능력치가 j 이상인지 체크
            if (sharks[i].size >= sharks[j].size &&
                sharks[i].speed >= sharks[j].speed &&
                sharks[i].intel >= sharks[j].intel) {
                // 능력이 모두 동일한 경우라면 i < j인지 확인
                if (sharks[i].size == sharks[j].size &&
                    sharks[i].speed == sharks[j].speed &&
                    sharks[i].intel == sharks[j].intel) {
                    if (i < j) {
                        canEat = true;
                    }
                } else {
                    // 적어도 하나가 strictly 크면 바로 canEat = true
                    canEat = true;
                }
            }

            // canEat이면, i와 i+N에서 j로 이어지는 간선을 각각 연결
            if(canEat) {
                adj[i].push_back(j);
                adj[i + N].push_back(j);
            }
        }
    }

    // 오른쪽 노드 매칭 상태를 -1로 초기화
    matchR.assign(N, -1);

    // 최대 매칭 계산
    int matchCount = 0;
    for(int i = 0; i < 2*N; i++){
        visited.assign(N, false);
        if (tryMatch(i)) {
            matchCount++;
        }
    }

    // matchCount가 먹힌 상어 수이므로, N - matchCount가 남은 상어의 최솟값
    cout << N - matchCount << "\n";
    return 0;
}
```

### 코드 단계별 동작

1. **입력**: N마리 상어의 (크기, 속도, 지능)을 입력받아 `sharks` 벡터에 저장한다.  
2. **그래프 구성**: 왼쪽 노드는 2N개(각 상어 i, i+N), 오른쪽 노드는 N개이다. i번 상어가 j번 상어를 먹을 수 있으면, 왼쪽 노드 i와 i+N이 모두 j번 오른쪽 노드로 연결된다.  
3. **매칭 알고리즘**: `tryMatch(i)`를 수행하며, 이미 매칭된 노드를 다른 곳으로 재매칭할 수 있다면 매칭을 갱신한다.  
4. **결과 계산**: 최대 매칭 크기가 잡아먹힌 상어 수이므로, N에서 이를 빼면 생존 상어 수의 최솟값이 된다.

## Python 코드와 설명

아래는 동일한 로직을 Python으로 옮긴 예시이다. Python에서도 N이 50이하이므로, DFS 기반의 이분 매칭 알고리즘으로 충분히 해결 가능하다.

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

class Shark:
    def __init__(self, size, speed, intel):
        self.size = size
        self.speed = speed
        self.intel = intel

def try_match(i):
    for r in adj[i]:
        if visited[r]:
            continue
        visited[r] = True
        if matchR[r] == -1 or try_match(matchR[r]):
            matchR[r] = i
            return True
    return False

N = int(input().strip())
sharks = []
for _ in range(N):
    s, sp, it = map(int, input().split())
    sharks.append(Shark(s, sp, it))

# 이분 그래프 구성: 왼쪽 2N개, 오른쪽 N개
adj = [[] for _ in range(2*N)]

for i in range(N):
    for j in range(N):
        if i == j:
            continue
        canEat = False
        if (sharks[i].size >= sharks[j].size and
            sharks[i].speed >= sharks[j].speed and
            sharks[i].intel >= sharks[j].intel):
            # 능력치 동일 시, 인덱스 i < j인지 검사
            if (sharks[i].size == sharks[j].size and
                sharks[i].speed == sharks[j].speed and
                sharks[i].intel == sharks[j].intel):
                if i < j:
                    canEat = True
            else:
                canEat = True

        if canEat:
            adj[i].append(j)
            adj[i+N].append(j)

matchR = [-1] * N
match_count = 0

for i in range(2*N):
    visited = [False]*N
    if try_match(i):
        match_count += 1

print(N - match_count)
```

### 코드 단계별 동작

1. **입력 및 상어 정보 저장**: N과 각 상어의 능력치를 입력받아 `Shark` 클래스로 저장한다.  
2. **그래프 생성**: 2N개의 왼쪽 노드와 N개의 오른쪽 노드를 연결할 인접 리스트 `adj`를 준비한다.  
3. **간선 연결**: i번째 상어가 j번째 상어를 먹을 수 있으면, `adj[i]`와 `adj[i+N]`에 j를 추가한다.  
4. **이분 매칭**: `try_match(i)` 함수가 DFS로 매칭을 시도하고, 이미 매칭된 노드도 다른 매칭으로 옮길 수 있으면 옮긴다.  
5. **결과 산출**: 최종적으로 match_count가 잡아먹힌 상어 수이므로, N - match_count가 문제에서 요구하는 살아남은 상어 수의 최솟값이 된다.

## 결론

이 문제는 ‘한 상어가 최대 두 마리를 잡아먹을 수 있다’는 제약을 만족하도록 이분 매칭을 변형하는 전형적인 예시이다. 노드 복제 기법을 통해 한 노드(상어)가 두 번 매칭될 수 있도록 하고, 최대 매칭 수가 잡아먹힌 상어의 총합이 되게끔 모델링한다. 이렇게 함으로써, 매칭 문제에서 얻어진 답을 “생존 상어의 최소 수”로 자연스럽게 바꿔서 구할 수 있다.

Bipartite Matching을 구현할 때 주의해야 하는 점은, 능력치가 모두 동일할 경우에 i < j일 때만 i가 j를 먹을 수 있도록 설정하는 부분이다. 이를 놓치면, 동일 능력치 상어들 사이에서 충돌이 발생해 오답이 되기 쉽다. 또한 N이 최대 50이라는 점을 고려하면, O(N^3)에 해당하는 DFS 기반 이분 매칭 알고리즘도 시간 안에 충분히 가능하다. 문제를 통해 이분 매칭의 활용 폭을 다시금 확인할 수 있으며, 마치 유량 문제처럼 Node Duplication 기법을 쓰는 전형적인 방법론을 실습해볼 수 있다
