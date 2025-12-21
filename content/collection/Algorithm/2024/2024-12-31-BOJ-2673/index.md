---
title: "[Algorithm] C++/Python 백준 2673번 : 교차하지 않는 원의 현들의 최대집합"
description: "주어진 여러 개의 원의 현들 중에서 서로 교차하지 않고, 끝점도 겹치지 않는 최대 부분집합을 찾는 문제입니다. Conflict Graph를 구성하여 Backtracking 또는 탐색 방법으로 Maximum Independent Set을 구하는 방식으로 접근합니다. 교차와 끝점 공유 조건을 정확히 구현하는 것이 핵심입니다."
categories: 
- Algorithm
- Graph
- Backtracking
tags:
- Backtracking
- Graph
- Pruning
- Maximum-Independent-Set
- Circle-Graph
- Complexity-O(2^N)
- Implementation
- Geometry
image: "index.png"
date: 2024-12-31
---

원 위에 일정 간격으로 찍힌 점들을 잇는 여러 현(Chord)이 주어졌을 때, 이 중에서 서로 교차하지 않고 끝점도 겹치지 않도록 고른 현들의 최대 개수를 구하는 문제이다.  
해당 문제는 조건만 제대로 파악한다면 Graph 혹은 Backtracking 기법을 이용하여 해결할 수 있다. 특히 현들 사이의 '교차 여부'와 '끝점 공유 여부'를 바탕으로 한 Conflict Graph를 구성하고, 그 그래프에서의 Maximum Independent Set을 찾는 방식으로 접근하는 것이 대표적이다.

문제 : [https://www.acmicpc.net/problem/2673](https://www.acmicpc.net/problem/2673)

---

## 문제 설명

원주 위에는 1부터 100까지 번호가 붙은 점들이 시계방향으로 일정 간격을 두고 놓여 있다고 가정한다. 문제에서는 이 중 임의의 두 점을 연결한 선분(이를 '현'이라고 함)이 총 \(N\)개( \(1 \leq N \leq 50\) ) 주어진다. 이때, 서로 다른 두 현이 **교차**한다는 것은, 원의 둘레를 시계방향으로 따라가면서 네 점이 번갈아 등장하는 경우를 의미한다. 예를 들어, 현 \((1, 50)\)과 현 \((20, 70)\)이 있을 때, 네 점을 시계방향으로 읽으면 1, 20, 50, 70 순으로 나타난다면 두 현은 교차하는 것이다.  
또한, 문제에서는 각 점을 최대 한 번만 사용할 수 있다고 가정하므로, 현들 중에서 점을 공유하는 것도 허용되지 않는다. 즉, 어떤 현의 한 끝점이 다른 현의 끝점과 같은 점이면, 그 둘은 함께 선택할 수 없는 충돌 관계가 된다.  

우리의 목표는, 입력으로 주어지는 \(N\)개의 현 가운데, **서로 교차하지도 않고 끝점도 겹치지 않는** 현들의 부분 집합을 골랐을 때, 그 크기가 최대가 되도록 하는 경우를 찾는 것이다. 예컨대, 현이 5개 정도만 있어도 가능한 조합이 여러 가지일 수 있는데, 교차와 공유 모두를 배제해야 하므로 조합을 일일이 확인하지 않고서는 최적 해답을 빠르게 구하기 어렵다. 그러나 \(N\)이 최대 50이므로, Backtracking을 통한 효율적인 검색(가지치기) 혹은 특수한 알고리즘을 적용하면 시간 내에 해결 가능하다.

이 문제를 좀 더 구체적으로 살펴보자.  
- 먼저 모든 현의 끝점 정보를 (a, b)로 받고, `a < b`가 되도록 정규화한다.  
- 이어서 두 현 \((a,b)\)와 \((c,d)\)에 대해, 아래 두 조건 중 하나라도 충족하면 둘은 함께 선택할 수 없다(충돌 관계).  
  1. \((a < c < b < d)\) 또는 \((c < a < d < b)\) 형태로 나타나는 **교차**  
  2. 끝점을 서로 공유(예: a == c, a == d, b == c, b == d)  

이 정보를 바탕으로 Conflict Graph를 구성하고, 해당 그래프에서의 Maximum Independent Set(즉, 충돌 간선을 공유하지 않는 최대 정점 집합)의 크기가 곧 이 문제에서 구하고자 하는 답이 된다.  

본 문제는 교차 판별과 Conflict Graph 구성에 집중하면서, 이후 Backtracking(또는 다른 방법론)을 통해 독립 집합의 최대 크기를 구해야 한다. 문제 해결을 위해서는 **조합 탐색**(Backtracking) 기법을 적용하여, 각 현을 "고른다" 또는 "고르지 않는다"로 분기하면서, 이미 고른 현과 충돌하는지 여부를 확인하는 가지치기를 수행해 나가면 된다. \(N=50\)이므로 이론상 최악의 경우 \(2^{50}\)의 탐색이 필요할 수 있지만, 올바른 가지치기 기법과 비교적 작은 입력 범위를 고려하면 제한 시간 안에 가능하다.

## 접근 방식

1. **현들의 정규화**  
   입력받은 현 \((x, y)\)에 대해, 항상 \(x < y\)가 되도록 정렬하여 저장한다.  
2. **Conflict Graph 구성**  
   - 모든 현 쌍 \((i, j)\)에 대해 교차하는지, 혹은 끝점을 공유하는지 판단한다.  
   - 만약 교차하거나 끝점을 공유한다면, 그래프 상에서 \(i\)번 정점과 \(j\)번 정점은 **충돌(Edge)** 관계로 표시한다.  
   - 이 Conflict Graph에서 "연결되지 않은" 현들끼리는 함께 선택 가능하다.  
3. **Maximum Independent Set 탐색**  
   - Conflict Graph에서 서로 간선이 없는 정점들로 이루어진 가장 큰 집합(Independent Set)의 크기를 구해야 한다.  
   - 여기서는 \(N \le 50\)이므로, Backtracking(DFS)으로 모든 조합을 따져보되, 아래 두 가지 대표적 가지치기를 적용하면 실행 시간 내에 충분히 해결 가능하다.  
     1. **Pruning1**: 현재까지 고른 현의 개수 + 앞으로 선택 가능한 최대 현 수(남은 현 수) < 이미 찾은 최적 해답 \(\rightarrow\) 더 이상 탐색 불필요  
     2. **Pruning2**: 현재 고려 중인 현이 이미 고른 현들과 충돌한다면 곧바로 "고른다" 분기를 배제  
4. **최대 개수 확인**  
   - 모든 분기를 마치면, Conflict가 없는 최대 집합의 크기가 구해지고, 이 값을 출력한다.


## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 50;

int N;
// i번째 현의 양 끝점을 (항상 first<second가 되도록) 저장
pair<int,int> chord[MAXN];

// 두 현 간 충돌 여부 저장 (교차 또는 끝점 공유)
bool conflict_[MAXN][MAXN];  

int bestAnswer = 0;  // 최대 선택 가능한 현의 개수

// 두 현 (a,b), (c,d)가 '교차하거나 공유점이 있는지' 판별
bool isConflict(int a, int b, int c, int d) {
    // 끝점이 하나라도 같으면 무조건 충돌
    if(a == c || a == d || b == c || b == d) {
        return true;
    }
    // 교차 판별 : (a < c < b < d) or (c < a < d < b) 이면 교차
    if((a < c && c < b && b < d) || (c < a && a < d && d < b)) {
        return true;
    }
    return false;
}

// 백트래킹 (idx: 현재 확인 중인 현 인덱스, chosenCount: 지금까지 고른 현의 개수, used: 어떤 현을 골랐는지 표시)
void dfs(int idx, int chosenCount, vector<bool> &used) {
    // Pruning1: 남은 현 수 + 현재까지 고른 수 <= bestAnswer 이면 더 볼 가치 없음
    int remain = N - idx;
    if(chosenCount + remain <= bestAnswer) {
        return;
    }

    // 모든 현을 다 확인했다면, 답 갱신
    if(idx == N) {
        bestAnswer = max(bestAnswer, chosenCount);
        return;
    }

    // 1) 이 현(idx)을 "고르지 않는다"
    dfs(idx + 1, chosenCount, used);

    // 2) 이 현(idx)을 "고른다" -> 이미 고른 현과 충돌하는지 확인
    bool canPick = true;
    for(int i = 0; i < idx; i++){
        if(used[i] && conflict_[i][idx]) {
            canPick = false;
            break;
        }
    }
    if(canPick) {
        used[idx] = true;
        dfs(idx + 1, chosenCount + 1, used);
        used[idx] = false;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N;
    for(int i = 0; i < N; i++){
        int x, y;
        cin >> x >> y;
        if(x > y) swap(x, y);
        chord[i] = {x, y};
    }

    // conflict 배열 초기화
    memset(conflict_, false, sizeof(conflict_));
    // 모든 현 쌍(i, j)에 대해 충돌 여부 계산
    for(int i = 0; i < N; i++){
        for(int j = i+1; j < N; j++){
            if(isConflict(chord[i].first, chord[i].second, 
                          chord[j].first, chord[j].second))
            {
                conflict_[i][j] = conflict_[j][i] = true;
            }
        }
    }

    vector<bool> used(N, false);
    dfs(0, 0, used);

    cout << bestAnswer << "\n";
    return 0;
}
```

### 코드 동작 단계별 상세 설명

1. **입력 처리**  
   - \(N\)개의 현 정보를 받되, `(x, y)`에서 `x > y`라면 `swap(x, y)`를 통해 항상 `x < y` 형태로 저장한다.  
2. **Conflict 배열 초기화**  
   - 2차원 배열 `conflict_`를 모두 `false`로 초기화한다.  
3. **충돌 여부 계산**  
   - 모든 현 쌍 `(i, j)`에 대해, `isConflict` 함수를 이용해 교차 혹은 끝점 공유를 판별한다.  
   - 만약 `true`라면 `conflict_[i][j]`와 `conflict_[j][i]`를 `true`로 설정한다.  
4. **Backtracking (dfs) 호출**  
   - `dfs(0, 0, used)`로 시작한다. 초기에는 idx=0(첫 번째 현), chosenCount=0(아직 고른 현이 없음) 상태이다.  
5. **가지치기(Pruning) 확인**  
   - `remain = N - idx`로 현재부터 끝까지 남은 현의 수를 구하고, `chosenCount + remain <= bestAnswer`이면 더 이상 탐색하지 않는다.  
6. **두 가지 분기**  
   1) 현재 현(idx)을 고르지 않음 -> `dfs(idx+1, chosenCount, used)`  
   2) 현재 현(idx)을 고른다 -> 이미 고른 현들 중에서 하나라도 `conflict_`가 `true`이면 고를 수 없음.  
      만약 고를 수 있다면 `used[idx] = true`로 표시하고 `dfs(idx+1, chosenCount+1, used)` 진행 후 복원.  
7. **최대값 갱신**  
   - `idx == N`까지 도달하면, 현재 `chosenCount`와 `bestAnswer`를 비교하여 갱신한다.  
8. **결과 출력**  
   - 최종적으로 `bestAnswer`에 저장된 값이 곧 최대 개수이다.


## Python 코드와 설명

```python
import sys
input = sys.stdin.readline

N = int(input())
chords = []
for _ in range(N):
    x, y = map(int, input().split())
    if x > y:
        x, y = y, x
    chords.append((x, y))

# 충돌 여부를 저장할 2차원 리스트
conflict = [[False]*N for _ in range(N)]

# 충돌 판별 함수
def is_conflict(a, b, c, d):
    # 끝점을 공유하면 True
    if a == c or a == d or b == c or b == d:
        return True
    # (a < c < b < d) or (c < a < d < b) 형태이면 교차
    if (a < c < b < d) or (c < a < d < b):
        return True
    return False

# 모든 현 쌍에 대해 충돌 여부 계산
for i in range(N):
    for j in range(i+1, N):
        a, b = chords[i]
        c, d = chords[j]
        if is_conflict(a, b, c, d):
            conflict[i][j] = True
            conflict[j][i] = True

best_answer = 0
used = [False]*N

def dfs(idx, chosen_count):
    global best_answer
    
    # Pruning1
    remain = N - idx
    if chosen_count + remain <= best_answer:
        return
    
    # 모든 현을 확인했다면, 최대값 갱신
    if idx == N:
        best_answer = max(best_answer, chosen_count)
        return
    
    # 1) 이 현을 "안 고른다"
    dfs(idx+1, chosen_count)
    
    # 2) 이 현을 "고른다"
    can_pick = True
    for i in range(idx):
        if used[i] and conflict[i][idx]:
            can_pick = False
            break
    
    if can_pick:
        used[idx] = True
        dfs(idx+1, chosen_count+1)
        used[idx] = False

dfs(0, 0)
print(best_answer)
```

### 코드 동작 단계별 상세 설명

1. **입력 및 정규화**  
   - 첫 줄에서 \(N\)을 읽고, 이후 \(N\)개의 줄에 걸쳐 현의 양끝점을 입력받는다.  
   - `(x, y)` 형태로 저장하되, `x > y`이면 `swap`하여 `(x, y)`가 항상 `(작은 값, 큰 값)`이 되도록 정규화한다.  
2. **충돌 정보를 담을 2차원 리스트 `conflict` 생성**  
   - 모든 값을 `False`로 초기화한다.  
3. **`is_conflict` 함수를 통한 충돌 판별**  
   - 두 현이 끝점을 공유하면 곧바로 충돌이라고 본다.  
   - 끝점을 공유하지 않는 경우, 네 점이 번갈아 등장하는( `(a < c < b < d)` 혹은 `(c < a < d < b)` ) 상태면 교차로 간주한다.  
4. **Backtracking(DFS)**  
   - `dfs(idx, chosen_count)`로 재귀를 돌면서 `idx`번째 현을 "고르지 않음" / "고름" 두 경우를 모두 탐색한다.  
   - `can_pick`을 통해 이미 고른 현들과 충돌이 있는지 체크한다. 충돌이 없다면 고를 수 있다.  
   - Pruning(가지치기)을 통해 현재까지 고른 수 + 남은 수가 이미 찾은 최고 기록보다 작으면 더 이상 진행하지 않는다.  
5. **결과 출력**  
   - 모든 분기를 마치면 `best_answer`에 최대 개수가 저장되며, 이를 출력한다.


## 결론

이상으로, 백준 2673번 **교차하지 않는 원의 현들의 최대집합** 문제를 해결하는 과정을 살펴보았다.  
이 문제는 원 위의 교차 여부 판단과 끝점 공유 문제를 동시에 처리해야 하므로, 단순한 Greedy로는 풀 수 없고, 각 현 간 충돌 관계를 명확히 정의한 뒤 Backtracking 또는 다른 알고리즘을 통해 **Maximum Independent Set**을 구해야 한다. \(N\)이 최대 50에 불과하므로 백트래킹에 적절한 가지치기를 적용하면 제한 시간 안에 충분히 가능하다.  

추가적으로, Circle Graph 기반의 알고리즘을 더 깊이 연구하거나, Dynamic Programming 기법을 변형하여 적용하는 방법도 존재할 수 있다. 그러나 여기에서는 Conflict Graph + Backtracking만으로도 문제를 충분히 해결할 수 있었다. 실제 대회나 실전 코딩 테스트에서 이와 유사한 '교차 판별' 문제를 만난다면, 가장 먼저 Conflict 관계 정리 후 **최대 독립 집합**(또는 최대 매칭, 최소 컷 등) 문제인지 확인해보는 것이 좋다.  
이로써 문제 풀이를 마쳤으며, 혹시 더 효율적인 방법이나 수학적 해법을 고민한다면, 원 위의 chord들을 이용한 Circle Graph 이론으로 확장하는 것도 또 다른 학습 방법이 될 것이다.  
