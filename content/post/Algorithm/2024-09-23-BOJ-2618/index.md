---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-23T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- DynamicProgramming
- Optimization
- Memoization
- O(N^2)
- GridMovement
- PoliceDispatch
- DP
- BFS
title: '[Algorithm] C++/Python 백준 2618번 : 경찰차'
---

경찰차들은 도시의 여러 사건을 처리하기 위해 최적의 경로를 찾아야 한다. 이때 두 대의 경찰차가 이동한 거리의 합을 최소화하는 것이 목표이다. 도시의 구조와 사건의 발생 위치가 주어졌을 때, 어떻게 하면 두 경찰차의 총 이동 거리를 최소화할 수 있을까?

문제 : [https://www.acmicpc.net/problem/2618](https://www.acmicpc.net/problem/2618)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

도시는 N x N 크기의 격자 형태로 이루어져 있으며, 각 도로는 동서방향과 남북방향으로 구분된다. 동서방향 도로는 위에서부터 1부터 N까지 번호가 매겨지고, 남북방향 도로는 왼쪽에서부터 1부터 N까지 번호가 매겨진다. 도로들이 교차하는 지점은 (동서방향 도로 번호, 남북방향 도로 번호)로 표시된다.

두 대의 경찰차가 있으며, 경찰차 1은 (1, 1) 위치에서, 경찰차 2는 (N, N) 위치에서 출발한다. W개의 사건이 발생하며, 각 사건은 특정 위치에서 발생한다. 각 사건은 두 경찰차 중 하나가 처리해야 하며, 사건은 발생한 순서대로 처리해야 한다.

목표는 두 경찰차가 이동한 거리의 합을 최소화하면서 모든 사건을 처리하는 것이다. 사건을 어떤 경찰차가 처리할지 결정하고, 최소 이동 거리를 구하는 프로그램을 작성해야 한다.

## 접근 방식

이 문제는 Dynamic Programming(DP)을 활용하여 해결할 수 있다. 각 상태를 정의하고, 그 상태에서의 최소 거리를 구하는 방식으로 접근한다.

1. **상태 정의**:
   - DP 배열 `dp[i][j]`를 정의한다. 여기서 `i`는 경찰차 1이 마지막으로 처리한 사건의 번호, `j`는 경찰차 2가 마지막으로 처리한 사건의 번호를 의미한다.
   - `dp[i][j]`는 경찰차 1이 사건 `i`까지, 경찰차 2가 사건 `j`까지 처리했을 때의 최소 이동 거리의 합이다.

2. **초기화**:
   - `dp[0][0] = 0`으로 초기화한다. 아직 아무 사건도 처리하지 않은 상태이다.

3. **상태 전이**:
   - 다음 처리해야 할 사건의 번호는 `next = max(i, j) + 1`이다.
   - 경찰차 1이 다음 사건 `next`를 처리하는 경우:
     - 이전 위치에서 다음 사건 위치까지의 거리를 계산하고, `dp[next][j]`를 갱신한다.
   - 경찰차 2가 다음 사건 `next`를 처리하는 경우:
     - 마찬가지로 `dp[i][next]`를 갱신한다.

4. **최소값 선택**:
   - 모든 가능한 `i`, `j`에 대해 DP를 수행하고, 마지막에 `dp[W][j]` 또는 `dp[i][W]` 중 최소값을 선택한다.

5. **경로 추적**:
   - 부모 상태를 저장하여 어떤 경찰차가 어떤 사건을 처리했는지 추적한다.

이러한 방식으로 DP를 수행하면 시간 복잡도는 O(W^2)로, W가 최대 1,000이므로 제한 시간 내에 해결할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <climits>

using namespace std;

const int MAX_W = 1001;
const int INF = INT_MAX;

int N, W;
pair<int, int> events[MAX_W]; // 사건들의 위치를 저장
int dp[MAX_W][MAX_W]; // DP 테이블
int path[MAX_W][MAX_W]; // 경로 추적을 위한 테이블

// 두 지점 사이의 거리를 계산하는 함수
int distance(const pair<int, int>& a, const pair<int, int>& b) {
    return abs(a.first - b.first) + abs(a.second - b.second);
}

// DP 함수 선언
int solve(int car1, int car2);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> W;
    for (int i = 1; i <= W; ++i) {
        cin >> events[i].first >> events[i].second;
    }

    memset(dp, -1, sizeof(dp));

    cout << solve(0, 0) << '\n';

    int car1 = 0, car2 = 0;
    for (int i = 1; i <= W; ++i) {
        int next = path[car1][car2];
        cout << next << '\n';
        if (next == 1) {
            car1 = i;
        } else {
            car2 = i;
        }
    }

    return 0;
}

// DP 함수 구현
int solve(int car1, int car2) {
    int next = max(car1, car2) + 1;
    if (next > W) return 0;
    if (dp[car1][car2] != -1) return dp[car1][car2];

    // 경찰차 1이 사건 처리하는 경우
    int dist1;
    if (car1 == 0) {
        dist1 = distance({1, 1}, events[next]);
    } else {
        dist1 = distance(events[car1], events[next]);
    }
    int cost1 = solve(next, car2) + dist1;

    // 경찰차 2가 사건 처리하는 경우
    int dist2;
    if (car2 == 0) {
        dist2 = distance({N, N}, events[next]);
    } else {
        dist2 = distance(events[car2], events[next]);
    }
    int cost2 = solve(car1, next) + dist2;

    // 최소값 선택 및 경로 저장
    if (cost1 < cost2) {
        dp[car1][car2] = cost1;
        path[car1][car2] = 1;
    } else {
        dp[car1][car2] = cost2;
        path[car1][car2] = 2;
    }

    return dp[car1][car2];
}
```

**코드 설명**

- **입력 부분**:
  - 도시 크기 `N`과 사건의 수 `W`를 입력받는다.
  - 각 사건의 위치를 `events` 배열에 저장한다.

- **DP 초기화**:
  - `dp` 배열을 -1로 초기화하여 메모이제이션에 활용한다.

- **`solve` 함수**:
  - 재귀적으로 DP를 수행한다.
  - `car1`, `car2`는 각각 경찰차 1과 2가 마지막으로 처리한 사건 번호이다.
  - `next`는 다음에 처리해야 할 사건 번호이다.
  - 종료 조건은 `next > W`인 경우로, 모든 사건을 처리한 상태이다.

- **거리 계산**:
  - 경찰차의 현재 위치에서 다음 사건 위치까지의 거리를 계산한다.
  - 초기 위치는 각각 (1, 1)과 (N, N)이다.

- **경로 추적**:
  - `path` 배열에 어떤 경찰차가 해당 상태에서 선택되었는지 저장한다.
  - 이를 통해 나중에 어떤 경찰차가 어떤 사건을 처리했는지 알 수 있다.

- **메인 함수**:
  - `solve(0, 0)`을 호출하여 DP를 시작한다.
  - 이후 `path` 배열을 이용하여 각 사건마다 어느 경찰차가 처리했는지 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>

#define MAX_W 1001
#define INF 1000000000

int N, W;
int events[MAX_W][2]; // 사건들의 위치를 저장
int dp[MAX_W][MAX_W]; // DP 테이블
int path[MAX_W][MAX_W]; // 경로 추적을 위한 테이블

// 절댓값 함수 구현
int abs(int x) {
    return x < 0 ? -x : x;
}

// 두 지점 사이의 거리를 계산하는 함수
int distance(int a_x, int a_y, int b_x, int b_y) {
    return abs(a_x - b_x) + abs(a_y - b_y);
}

// DP 함수 선언
int solve(int car1, int car2);

int main() {
    scanf("%d %d", &N, &W);
    for (int i = 1; i <= W; ++i) {
        scanf("%d %d", &events[i][0], &events[i][1]);
    }

    for (int i = 0; i <= W; ++i)
        for (int j = 0; j <= W; ++j)
            dp[i][j] = -1;

    printf("%d\n", solve(0, 0));

    int car1 = 0, car2 = 0;
    for (int i = 1; i <= W; ++i) {
        int next = path[car1][car2];
        printf("%d\n", next);
        if (next == 1) {
            car1 = i;
        } else {
            car2 = i;
        }
    }

    return 0;
}

// DP 함수 구현
int solve(int car1, int car2) {
    int next = (car1 > car2 ? car1 : car2) + 1;
    if (next > W) return 0;
    if (dp[car1][car2] != -1) return dp[car1][car2];

    // 경찰차 1이 사건 처리하는 경우
    int dist1;
    if (car1 == 0) {
        dist1 = distance(1, 1, events[next][0], events[next][1]);
    } else {
        dist1 = distance(events[car1][0], events[car1][1], events[next][0], events[next][1]);
    }
    int cost1 = solve(next, car2) + dist1;

    // 경찰차 2가 사건 처리하는 경우
    int dist2;
    if (car2 == 0) {
        dist2 = distance(N, N, events[next][0], events[next][1]);
    } else {
        dist2 = distance(events[car2][0], events[car2][1], events[next][0], events[next][1]);
    }
    int cost2 = solve(car1, next) + dist2;

    // 최소값 선택 및 경로 저장
    if (cost1 < cost2) {
        dp[car1][car2] = cost1;
        path[car1][car2] = 1;
    } else {
        dp[car1][car2] = cost2;
        path[car1][car2] = 2;
    }

    return dp[car1][car2];
}
```

**코드 설명**

- `stdio.h`와 `stdlib.h`만을 사용하여 구현하였다.
- C 스타일의 배열과 함수만을 사용하여 이전 코드와 동일한 로직을 구현하였다.
- `abs` 함수를 직접 구현하여 사용하였다.
- 나머지 로직은 이전 C++ 코드와 동일하다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(1000000)

N = int(sys.stdin.readline())
W = int(sys.stdin.readline())
events = [None] * (W + 1)
for i in range(1, W + 1):
    x, y = map(int, sys.stdin.readline().split())
    events[i] = (x, y)

dp = [[-1] * (W + 1) for _ in range(W + 1)]
path = [[0] * (W + 1) for _ in range(W + 1)]

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve(car1, car2):
    next_event = max(car1, car2) + 1
    if next_event > W:
        return 0
    if dp[car1][car2] != -1:
        return dp[car1][car2]

    # 경찰차 1이 사건 처리하는 경우
    if car1 == 0:
        dist1 = distance((1, 1), events[next_event])
    else:
        dist1 = distance(events[car1], events[next_event])
    cost1 = solve(next_event, car2) + dist1

    # 경찰차 2가 사건 처리하는 경우
    if car2 == 0:
        dist2 = distance((N, N), events[next_event])
    else:
        dist2 = distance(events[car2], events[next_event])
    cost2 = solve(car1, next_event) + dist2

    if cost1 < cost2:
        dp[car1][car2] = cost1
        path[car1][car2] = 1
    else:
        dp[car1][car2] = cost2
        path[car1][car2] = 2

    return dp[car1][car2]

print(solve(0, 0))

car1, car2 = 0, 0
for _ in range(W):
    next_move = path[car1][car2]
    print(next_move)
    if next_move == 1:
        car1 = max(car1, car2) + 1
    else:
        car2 = max(car1, car2) + 1
```

**코드 설명**

- **입력 부분**:
  - 도시 크기 `N`과 사건의 수 `W`를 입력받는다.
  - 각 사건의 위치를 `events` 리스트에 저장한다.

- **DP 테이블 초기화**:
  - `dp`와 `path`를 2차원 리스트로 초기화한다.

- **`distance` 함수**:
  - 두 지점 사이의 거리를 계산한다.

- **`solve` 함수**:
  - 재귀적으로 DP를 수행한다.
  - 메모이제이션을 위해 `dp` 테이블을 활용한다.

- **결과 출력**:
  - `solve(0, 0)`의 결과를 출력한다.
  - `path` 테이블을 이용하여 각 사건마다 어느 경찰차가 처리했는지 출력한다.

## 결론

이 문제는 Dynamic Programming의 대표적인 예제로, 상태 정의와 메모이제이션을 통한 최적화가 중요하다. 각 상태에서의 최적해를 구하고, 이를 기반으로 전체 문제의 최적해를 도출하는 과정이 핵심이다.

문제를 풀면서 DP의 상태 설계와 재귀 함수의 작성 방법에 대해 다시 한 번 생각해볼 수 있었다. 또한, 메모이제이션을 통해 중복 계산을 방지함으로써 시간 복잡도를 효과적으로 줄일 수 있었다.

추가적인 최적화로는 DP 테이블의 크기를 줄이거나, 반복문을 활용하여 Bottom-Up 방식으로 구현하는 방법이 있다. 그러나 이 문제에서는 재귀와 메모이제이션을 통한 Top-Down 방식이 이해하기 쉽고 구현도 간단하다.

이번 문제를 통해 DP의 중요성과 활용 방법에 대해 다시 한 번 깨달을 수 있었다. 앞으로도 다양한 문제에 DP를 적용하여 최적해를 구하는 연습을 지속해야겠다.