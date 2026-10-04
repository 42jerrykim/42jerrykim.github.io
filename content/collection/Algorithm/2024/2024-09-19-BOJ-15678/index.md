---
image: "wordcloud.png"
description: "이 문제는 동적 계획법과 데크(Deque)를 활용하여 주어진 징검다리에서 점프 제한을 지키며 얻을 수 있는 최대 점수를 효율적으로 구하는 방법을 다룹니다. 최적의 점수 계산 방법과 슬라이딩 윈도우 내에서의 최대값 관리, 시간복잡도 개선 아이디어를 배울 수 있습니다."
categories: Algorithm
date: "2024-09-19T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- DP(동적계획법)
- Data-Structures(자료구조)
- Implementation(구현)
- Optimization(최적화)
- Deque
- Time-Complexity(시간복잡도)
- Problem-Solving(문제해결)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- C++
- Coding-Test(코딩테스트)
- Python
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Complexity-Analysis(복잡도분석)
- Performance(성능)
- Pitfalls(함정)
- Sliding-Window
- Optimal-Substructure(최적부분구조)
- Two-Pointers
- Queue(큐)
- Array(배열)
- Dynamic-Programming(동적계획법)
- Segment-Tree(세그먼트트리)
title: '[Algorithm] C++/Python 백준 15678번 : 연세워터파크'
---

연세대학교에서는 매년 여름 깜짝 워터파크를 개장한다. 워터파크 개장을 막는 것이 힘들다고 판단한 학교에서는 학생들이 워터파크를 더 즐길 수 있도록 정수 $ K_i $가 쓰여진 징검다리 $ N $개를 놓아 두었다. 학생들은 이 징검다리를 이용해 게임을 진행하며, 게임의 목표는 징검다리에 쓰인 정수의 합을 최대화하는 것이다.

게임의 규칙은 다음과 같다:

1. 각 사람은 시작점으로 사용할 징검다리 하나를 아무 것이나 하나 고른다.
2. 시작점에서 출발한 뒤 계속 점프하여 징검다리를 몇 개든 마음대로 밟은 뒤, 나오고 싶을 때 나온다. 시작점에서 바로 나오는 것도 가능하다.
3. 징검다리 간 점프는 인덱스 차이가 $ D $ 이하이어야 한다.
4. 어떤 징검다리도 두 번 이상 밟을 수 없다.

이러한 규칙 하에서, 학생들이 얻을 수 있는 최대 점수를 구하는 문제이다. 점수는 시작점에서부터 밟은 모든 징검다리에 쓰여진 정수의 합으로 계산된다. 징검다리의 수 $ N $과 각 징검다리에 쓰인 정수 $ K_i $가 주어질 때, 가능한 최대 점수를 구하는 프로그램을 작성해야 한다.

문제 : [https://www.acmicpc.net/problem/15678](https://www.acmicpc.net/problem/15678)

이 글을 읽고 나면 다음을 설명할 수 있다.

- 징검다리 문제를 $ DP[i] = K[i] + \max(0, \max_{i-D \le j < i} DP[j]) $ 형태의 점화식으로 세우는 이유
- 윈도우 최댓값을 단조 감소 데크로 관리할 때 각 인덱스가 정확히 한 번 들어가고 한 번 나오는 이유와 그에 따른 $ O(N) $ 시간
- $ O(ND) $ 단순 DP, 세그먼트 트리, 단조 데크 중 제약에 맞는 방법을 고르는 기준

## 접근 방식

이 문제는 <strong>동적 계획법(Dynamic Programming)</strong>을 이용하여 효율적으로 해결할 수 있다. 각 징검다리를 시작점으로 삼았을 때, 그 지점까지 올 수 있는 최대 점수를 계산하고, 이를 기반으로 전체적으로 가능한 최대 점수를 찾는 방식이다. 문제의 주요 제약 조건은 징검다리 간 점프 시 인덱스 차이가 $ D $ 이하이어야 하며, 한 번 밟은 징검다리를 다시 밟을 수 없다는 점이다.

이를 위해, 각 징검다리 $ i $까지 올 수 있는 최대 점수를 저장하는 DP 배열 $ DP[i] $를 정의한다. $ DP[i] $는 징검다리 $ i $를 밟을 때까지의 최대 점수를 의미한다. $ DP[i] $를 계산하기 위해서는 $ i-D $부터 $ i-1 $까지의 징검다리 중에서 최대 점수를 가진 징검다리를 선택하여 $ K[i] $를 더하는 방식으로 접근할 수 있다.

하지만, $ N $이 최대 $ 10^5 $이기 때문에 단순한 반복문으로는 시간 초과가 발생할 수 있다. 이를 해결하기 위해 **Deque**를 활용하여 슬라이딩 윈도우 내에서 최대 값을 효율적으로 관리한다. Deque의 front에는 현재 윈도우 내에서 최대 $ DP[j] $ 값을 가진 인덱스를 유지하며, 이를 통해 $ DP[i] $를 빠르게 계산할 수 있다.

점화식이 옳은 이유는 다음과 같다. 징검다리는 인덱스가 증가하는 방향으로만 점프해도 최적해를 잃지 않는다. 점프 거리가 $ D $ 이하이고 같은 다리를 두 번 밟을 수 없을 때, 어떤 경로의 밟는 순서를 인덱스 오름차순으로 재배열해도 합은 같다. 오름차순으로 늘어놓은 인접한 두 다리의 간격이 $ D $를 넘는다면 그 구간을 건너뛰는 점프가 원래 경로에 없다는 뜻이므로 원래 경로가 성립하지 않는데, 이는 모순이라 오름차순 경로도 항상 유효하다. 이 가정이 문제의 의도이며 알려진 풀이도 같은 전제를 쓴다. 따라서 $ i $에서 끝나는 경로의 최대 합은 "$ i $만 밟는 경우 $ K[i] $"와 "윈도우 안의 $ j $에서 끝나는 최적 경로에 $ i $를 이어 붙이는 경우" 중 큰 값이고, 앞쪽 값이 음수이면 이어 붙이는 쪽이 손해이므로 새로 시작한다. 정답은 모든 $ i $에 대한 $ DP[i] $의 최댓값이다.

## 방법 비교와 선택 기준

| 방법 | 시간 | 공간 | 적합한 상황 |
|---|---|---|---|
| 단순 DP (윈도우 순회) | $ O(ND) $ | $ O(N) $ | $ D $가 작을 때 (최악 $ N=D=10^5 $면 $ 10^{10} $ 번 연산이라 시간 초과) |
| 세그먼트 트리 구간 최대 | $ O(N \log N) $ | $ O(N) $ | 윈도우 크기가 가변이거나 구간 질의가 임의일 때 |
| 단조 데크 | $ O(N) $ | $ O(N) $ | 윈도우가 고정 폭 $ D $로 오른쪽으로만 이동할 때 (이 문제) |

윈도우가 한 방향으로만 미끄러지므로 임의 구간 질의를 지원하는 세그먼트 트리까지 쓸 필요가 없고, 데크가 같은 일을 더 적은 상수로 한다.

## 단조 데크의 동작 추적

$ N=5, D=2, K=[3,-5,4,-1,2] $ 를 따라가 보자. 데크에는 인덱스를 두며 앞쪽이 윈도우 최대 $ DP $ 를 가진다.

| i | 윈도우 | 앞쪽 DP | $ DP[i] $ | 정리 후 데크(인덱스) |
|---|---|---|---|---|
| 1 | 없음 | - | 3 | [1] |
| 2 | [1] | 3 | -2 | [1, 2] |
| 3 | [1, 2] | 3 | 7 | [3] |
| 4 | [2, 3] | 7 | 6 | [3, 4] |
| 5 | [3, 4] | 7 | 9 | [5] |

답은 $ \max DP = 9 $ 이고, 경로는 $ 1 \to 3 \to 5 $ ($ 3+4+2 $) 이다. $ i=3 $ 에서 $ DP[3]=7 $ 이 앞선 값들을 모두 밀어내는 부분이 단조성 유지의 핵심이다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int N, D;
    cin >> N >> D;
    vector<ll> K(N+1);
    for(int i=1;i<=N;i++) cin >> K[i];
    
    // Initialize DP array
    vector<ll> DP(N+1, 0);
    // Initialize deque to store indices, front has the max DP[j]
    deque<int> dq;
    ll max_ans = LLONG_MIN;
    
    for(int i=1;i<=N;i++){
        // Remove indices out of the window [i-D, i-1]
        while(!dq.empty() && dq.front() < i - D){
            dq.pop_front();
        }
        
        // Calculate DP[i]
        if(!dq.empty()){
            ll best = DP[dq.front()];
            if(best > 0){
                DP[i] = K[i] + best;
            }
            else{
                DP[i] = K[i];
            }
        }
        else{
            DP[i] = K[i];
        }
        
        // Update the deque: remove from back while DP[j] <= DP[i]
        while(!dq.empty() && DP[dq.back()] <= DP[i]){
            dq.pop_back();
        }
        dq.push_back(i);
        
        // Update the maximum answer
        max_ans = max(max_ans, DP[i]);
    }
    
    cout << max_ans;
}
```

**코드 설명**

입력은 첫 줄에 $ N, D $, 둘째 줄에 $ K_1 \dots K_N $ 이 공백으로 주어진다. $ DP[i] $는 $ i $번 다리가 마지막인 경로의 최대 합이다. 데크에는 인덱스를 담고, 윈도우 $ [i-D, i-1] $ 에서 벗어난 앞쪽 인덱스를 먼저 버린다. 남은 앞쪽 인덱스가 윈도우 안에서 $ DP $ 가 가장 큰 후보이므로 그 값이 양수일 때만 $ K[i] $ 에 더하고, 아니면 $ K[i] $ 에서 새로 시작한다. 이후 뒤쪽에서 $ DP[i] $ 이하인 인덱스를 모두 제거하고 $ i $ 를 넣는다. 제거된 인덱스는 $ i $ 보다 일찍 만료되면서 값도 작아 앞으로 최댓값이 될 수 없기 때문에 버려도 안전하며, 이 불변식 덕분에 데크의 $ DP $ 값은 앞에서 뒤로 엄격히 감소한다. 마지막으로 모든 $ DP[i] $ 의 최댓값을 `max_ans` 로 갱신해 출력한다. 모든 $ K_i $ 가 음수이면 답은 가장 큰 $ K_i $ 하나이므로 `max_ans` 를 `LLONG_MIN` 으로 시작한다.

## C++ without library 코드와 설명

```cpp
#include <iostream>
using namespace std;

typedef long long ll;

struct Deque {
    int data[100005];
    int front;
    int back;
    
    Deque() : front(0), back(-1) {}
    
    bool empty() {
        return front > back;
    }
    
    void push_back(int x){
        back++;
        data[back] = x;
    }
    
    void pop_front(){
        front++;
    }
    
    void pop_back(){
        back--;
    }
    
    int get_front(){
        return data[front];
    }
    
    int get_back(){
        return data[back];
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int N, D;
    cin >> N >> D;
    ll K_arr[100005];
    for(int i=1;i<=N;i++) cin >> K_arr[i];
    
    // Initialize DP array
    ll DP_arr[100005];
    for(int i=0;i<=N;i++) DP_arr[i] = 0;
    
    // Initialize custom deque
    Deque dq;
    ll max_ans = -9223372036854775807LL;
    
    for(int i=1;i<=N;i++){
        // Remove indices out of the window [i-D, i-1]
        while(!dq.empty() && dq.get_front() < i - D){
            dq.pop_front();
        }
        
        // Calculate DP[i]
        if(!dq.empty()){
            ll best = DP_arr[dq.get_front()];
            if(best > 0){
                DP_arr[i] = K_arr[i] + best;
            }
            else{
                DP_arr[i] = K_arr[i];
            }
        }
        else{
            DP_arr[i] = K_arr[i];
        }
        
        // Update the deque: remove from back while DP[j] <= DP[i]
        while(!dq.empty() && DP_arr[dq.get_back()] <= DP_arr[i]){
            dq.pop_back();
        }
        dq.push_back(i);
        
        // Update the maximum answer
        if(DP_arr[i] > max_ans){
            max_ans = DP_arr[i];
        }
    }
    
    cout << max_ans;
}
```

**코드 설명**

이 코드는 `vector`, `deque`, `climits` 없이 같은 알고리즘을 쓴다. 달라지는 부분은 두 가지다. 첫째, `Deque` 구조체가 배열과 `front`/`back` 두 포인터로 `push_back`, `pop_front`, `pop_back`, `get_front`, `get_back`, `empty` 를 직접 구현한다. 각 인덱스는 한 번만 들어가므로 크기 $ 10^5+5 $ 배열이면 포인터가 넘치지 않는다. 둘째, `max_ans` 의 초기값을 `-9223372036854775807LL` 로 직접 적는다. 점화식과 데크 갱신 순서는 위 C++ 코드와 동일하다.

## Python 코드와 설명

```python
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    N, D = map(int, input().split())
    K = [0] + list(map(int, input().split()))
    
    DP = [0] * (N + 1)
    dq = deque()
    max_ans = -10**18
    
    for i in range(1, N + 1):
        # Remove indices out of the window [i-D, i-1]
        while dq and dq[0] < i - D:
            dq.popleft()
        
        # Calculate DP[i]
        if dq:
            best = DP[dq[0]]
            if best > 0:
                DP[i] = K[i] + best
            else:
                DP[i] = K[i]
        else:
            DP[i] = K[i]
        
        # Update the deque: remove from back while DP[j] <= DP[i]
        while dq and DP[dq[-1]] <= DP[i]:
            dq.pop()
        dq.append(i)
        
        # Update the maximum answer
        if DP[i] > max_ans:
            max_ans = DP[i]
    
    print(max_ans)

if __name__ == "__main__":
    main()
```
**코드 설명**

Python 코드도 같은 알고리즘이며 `sys.stdin.readline` 으로 입력을 빠르게 읽고, 둘째 줄의 $ N $ 개 정수를 한 번에 리스트로 만든다. `collections.deque` 의 `popleft` 와 `pop` 이 $ O(1) $ 이므로 C++ 구현과 연산 횟수가 같다. 파이썬 정수는 오버플로가 없어 `max_ans` 는 충분히 작은 $ -10^{18} $ 로 시작한다.

## 결론

고정 폭 윈도우의 최댓값이 필요한 DP는 이 단조 데크 패턴으로 $ O(ND) $ 를 $ O(N) $ 으로 줄일 수 있다. 같은 패턴은 BOJ 11003(최솟값 찾기)에서 확인할 수 있다.

## 복잡도 분석

| 항목 | 복잡도 | 근거 |
|---|---|---|
| 시간 | $ O(N) $ | 인덱스당 push 1회, pop 최대 1회 |
| 공간 | $ O(N) $ | $ K $, $ DP $, 데크 배열 |

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 | 반복문 범위와 데크가 빈 상태 처리 확인 |
| **모두 음수** | 답이 가장 큰 $K_i$ 하나 | `max_ans` 를 0이 아닌 최솟값으로 초기화 |
| **D=1 또는 D≥N** | 윈도우가 직전 한 칸 또는 전체 | 만료 조건 `front < i - D` 확인 |
| **오버플로우** | 합이 클 수 있음 | 합산 안전을 위해 `long long` (C++) 사용 |
