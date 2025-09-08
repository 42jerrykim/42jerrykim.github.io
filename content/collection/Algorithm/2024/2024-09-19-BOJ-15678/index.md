---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-19T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- DynamicProgramming
- DataStructures
- Implementation
- Optimization
- Deque
- SlidingWindow
- DPOptimization
- O(N)
- ProblemSolving
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

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 **동적 계획법(Dynamic Programming)**을 이용하여 효율적으로 해결할 수 있다. 각 징검다리를 시작점으로 삼았을 때, 그 지점까지 올 수 있는 최대 점수를 계산하고, 이를 기반으로 전체적으로 가능한 최대 점수를 찾는 방식이다. 문제의 주요 제약 조건은 징검다리 간 점프 시 인덱스 차이가 $ D $ 이하이어야 하며, 한 번 밟은 징검다리를 다시 밟을 수 없다는 점이다.

이를 위해, 각 징검다리 $ i $까지 올 수 있는 최대 점수를 저장하는 DP 배열 $ DP[i] $를 정의한다. $ DP[i] $는 징검다리 $ i $를 밟을 때까지의 최대 점수를 의미한다. $ DP[i] $를 계산하기 위해서는 $ i-D $부터 $ i-1 $까지의 징검다리 중에서 최대 점수를 가진 징검다리를 선택하여 $ K[i] $를 더하는 방식으로 접근할 수 있다.

하지만, $ N $이 최대 $ 10^5 $이기 때문에 단순한 반복문으로는 시간 초과가 발생할 수 있다. 이를 해결하기 위해 **Deque**를 활용하여 슬라이딩 윈도우 내에서 최대 값을 효율적으로 관리한다. Deque의 front에는 현재 윈도우 내에서 최대 $ DP[j] $ 값을 가진 인덱스를 유지하며, 이를 통해 $ DP[i] $를 빠르게 계산할 수 있다.

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

1. **입력 처리**: 첫 줄에서 $ N $과 $ D $를 입력받고, 다음 $ N $개의 줄에서 각 징검다리에 쓰인 정수 $ K_i $를 입력받는다.
2. **DP 배열 초기화**: $ DP[i] $는 징검다리 $ i $를 밟을 때까지의 최대 점수를 저장한다. 초기에는 모두 0으로 설정한다.
3. **Deque 초기화**: Deque를 사용하여 현재 윈도우 내에서 최대 $ DP[j] $ 값을 가진 인덱스를 관리한다. Deque의 front는 항상 현재 윈도우에서 가장 큰 $ DP[j] $ 값을 가진 인덱스를 유지한다.
4. **DP 계산**: 각 징검다리 $ i $에 대해, $ i-D $부터 $ i-1 $까지의 징검다리 중 최대 $ DP[j] $ 값을 찾고, 이를 $ K[i] $와 더하여 $ DP[i] $를 계산한다. 만약 이전까지의 최대 값이 음수라면, 현재 징검다리 $ i $만을 선택한다.
5. **Deque 업데이트**: 현재 $ DP[i] $가 Deque의 뒤에 있는 값들보다 크거나 같으면, Deque의 뒤에서부터 제거하여 Deque가 항상 내림차순을 유지하도록 한다. 그런 다음 현재 인덱스 $ i $를 Deque에 추가한다.
6. **최대 점수 업데이트**: 각 단계에서 $ DP[i] $를 전체 최대 점수 $ max\_ans $와 비교하여 업데이트한다.
7. **결과 출력**: 최종적으로 $ max\_ans $를 출력한다.

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

이 코드는 표준 라이브러리의 `vector`, `deque`, `climits` 등을 사용하지 않고, 필요한 기능을 직접 구현하여 작성되었다. 기본적인 로직은 이전 C++ 코드와 동일하며, Deque의 기능을 구조체로 직접 구현하였다.

1. **입력 처리**: $ N $, $ D $, 그리고 각 징검다리에 쓰인 정수 $ K_i $를 입력받는다. 징검다리의 정수는 `K_arr` 배열에 저장된다.
2. **DP 배열 초기화**: `DP_arr` 배열을 사용하여 각 징검다리 $ i $를 밟을 때까지의 최대 점수를 저장한다. 초기에는 모두 0으로 설정한다.
3. **Custom Deque 구조체**: `Deque` 구조체를 정의하여, 표준 라이브러리의 `deque`를 대체한다. 배열과 포인터(`front`, `back`)를 사용하여 Deque의 기본적인 기능을 구현하였다.
    - `push_back(int x)`: Deque의 뒤에 요소를 추가한다.
    - `pop_front()`: Deque의 앞에서 요소를 제거한다.
    - `pop_back()`: Deque의 뒤에서 요소를 제거한다.
    - `get_front()`: Deque의 앞 요소를 반환한다.
    - `get_back()`: Deque의 뒤 요소를 반환한다.
    - `empty()`: Deque가 비어있는지 확인한다.
4. **DP 계산**: 각 징검다리 $ i $에 대해, $ i-D $부터 $ i-1 $까지의 징검다리 중 최대 $ DP[j] $ 값을 찾고, 이를 $ K[i] $와 더하여 $ DP[i] $를 계산한다. 만약 이전까지의 최대 값이 음수라면, 현재 징검다리 $ i $만을 선택한다.
5. **Deque 업데이트**: 현재 $ DP[i] $가 Deque의 뒤에 있는 값들보다 크거나 같으면, Deque의 뒤에서부터 제거하여 Deque가 항상 내림차순을 유지하도록 한다. 그런 다음 현재 인덱스 $ i $를 Deque에 추가한다.
6. **최대 점수 업데이트**: 각 단계에서 $ DP[i] $를 전체 최대 점수 $ max\_ans $와 비교하여 업데이트한다.
7. **결과 출력**: 최종적으로 $ max\_ans $를 출력한다.

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

Python에서는 deque를 사용하여 슬라이딩 윈도우 내에서 최대 DP[j]DP[j] 값을 효율적으로 관리한다.

1. **입력 처리**: sys.stdin.readline을 사용하여 빠르게 입력을 받는다. NN, DD, 그리고 각 징검다리에 쓰인 정수 KiKi​를 입력받는다.
2. **DP 배열 및 Deque 초기화**: DP[i]DP[i]를 저장할 리스트와 Deque를 초기화한다.
3. **DP 계산 및 Deque 업데이트**: 각 징검다리 ii에 대해 DP[i]DP[i]를 계산하고, Deque를 업데이트한다.
4. **최대 점수 업데이트**: 각 단계에서 최대 점수를 지속적으로 갱신한다.
5. **결과 출력**: 최종적으로 최대 점수를 출력한다.

## 결론

이번 문제는 동적 계획법과 효율적인 자료 구조인 Deque를 활용하여 시간 복잡도를 $ O(N) $으로 줄일 수 있었다. 슬라이딩 윈도우 내에서 최대 값을 효율적으로 관리하는 방법을 이해하는 데 도움이 되는 문제였다. 특히, 큰 입력 크기에서도 빠르게 동작하도록 최적화된 코드를 작성하는 것이 중요했으며, Deque를 활용한 최적화 기법이 매우 유용함을 다시 한번 확인할 수 있었다. 앞으로 유사한 문제를 만났을 때, 이번에 배운 접근 방식을 응용하여 효율적으로 문제를 해결할 수 있을 것이다.