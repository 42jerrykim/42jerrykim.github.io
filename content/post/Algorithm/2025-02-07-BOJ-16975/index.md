---
title: "[Algorithm] C++/Python 백준 16975번 : 수열과 쿼리 21"
categories: 
- Algorithm
- Platinum IV
- Data Structure
- Fenwick Tree
tags:
- Fenwick Tree
- Range Update
- Lazy Propagation
- O(log N)
- Binary Indexed Tree
- Array
- Query Processing
- Simulation
image: "index.png"
date: 2025-02-07
---

이번 글에서는 백준 16975번 "수열과 쿼리 21" 문제를 다루고 있다. 본 문제는 초기 수열에 대해 구간 업데이트와 점 쿼리를 효율적으로 처리하는 방법을 요구하며, Fenwick Tree(또는 Binary Indexed Tree)를 이용하여 최적화된 알고리즘을 구현하는 문제이다. C++과 Python 두 가지 언어로 구현된 코드를 함께 소개하고 있으며, 각 코드의 동작 원리를 상세하게 설명할 것이다.

문제 : [https://www.acmicpc.net/problem/16975](https://www.acmicpc.net/problem/16975)

## 문제 설명

문제 "수열과 쿼리 21"은 길이가 N인 정수 수열 A₁, A₂, …, Aₙ이 주어지고, 이 수열에 대해 M개의 쿼리를 수행하는 문제이다. 쿼리는 두 종류로 주어진다. 첫 번째 종류의 쿼리는 "1 i j k"의 형태로, 수열의 i번째부터 j번째까지의 모든 원소에 정수 k를 더하는 연산이다. 두 번째 종류의 쿼리는 "2 x"의 형태로, 현재 수열의 x번째 원소의 값을 출력하는 연산이다. 초기 수열의 각 원소는 1 이상 1,000,000 이하의 값을 가지며, k의 값은 -1,000,000 이상 1,000,000 이하로 주어진다. N과 M의 최대 크기가 각각 100,000이므로, 매 쿼리마다 단순히 구간 내 모든 원소를 갱신하는 방식은 시간 초과를 유발할 수 있다. 따라서, 이 문제에서는 구간 업데이트와 점 쿼리를 O(log N)의 시간 복잡도로 처리할 수 있는 효율적인 자료 구조를 선택해야 한다. 대표적으로 Fenwick Tree를 이용하면 구간에 대한 누적 합 개념을 활용하여, 구간 업데이트와 점 쿼리를 빠르게 수행할 수 있다. 구간 업데이트를 위해 BIT에 두 번의 업데이트 연산(시작 인덱스에 k, j+1 인덱스에 -k)을 수행하고, 점 쿼리 시에는 해당 인덱스까지의 누적 합을 계산하여 원래의 수열 값과 더하는 방식으로 문제를 해결할 수 있다. 이와 같이 문제의 조건을 분석하고 적절한 알고리즘을 선택함으로써, 제한된 시간 내에 모든 쿼리를 처리할 수 있는 최적의 솔루션을 구현할 수 있다.

## 접근 방식

본 문제는 구간 업데이트와 점 쿼리를 빠르게 처리해야 하는 문제이다. 구간에 동일한 값을 더하는 연산을 매번 반복하여 적용하는 방식은 비효율적이므로, Fenwick Tree를 사용하여 각 업데이트와 쿼리를 O(log N) 시간 내에 수행할 수 있도록 설계하였다. 구간 업데이트의 경우, 차분 배열의 개념을 도입하여 BIT의 특정 위치에 k와 -k를 각각 업데이트하고, 점 쿼리 시에는 해당 인덱스까지의 누적 합(prefix sum)을 구하여 원래 수열의 값에 보정하는 방식으로 문제를 해결하였다. 이 방법은 구간 누적 합 문제의 전형적인 해결법이며, 대량의 쿼리에도 빠르게 대응할 수 있는 효율적인 알고리즘적 기법이다.

## C++ 코드와 설명

```cpp
#include <iostream>   // 입출력을 위한 라이브러리이다.
#include <vector>     // 동적 배열(vector)을 사용하기 위한 라이브러리이다.
using namespace std;

int main(){
    ios::sync_with_stdio(false);    // 입출력 속도 향상을 위한 설정이다.
    cin.tie(nullptr);               // 입출력 속도 향상을 위한 설정이다.
    
    int n;                        
    cin >> n;                       // 수열의 크기 n을 입력받는다.
    vector<long long> A(n+1, 0);      
    for (int i = 1; i <= n; i++){
        cin >> A[i];                // 1번 인덱스부터 n번 인덱스까지 수열의 값을 입력받는다.
    }
    
    // Fenwick Tree(BIT)를 1-indexed로 사용하기 위하여 n+1 크기의 벡터를 선언하였다이다.
    vector<long long> BIT(n+1, 0);
    
    // BIT에 값을 업데이트하는 람다 함수이다.
    auto update = [&](int idx, long long val) {
        while(idx <= n){
            BIT[idx] += val;      // BIT의 해당 인덱스에 val을 더한다.
            idx += (idx & -idx);  // 다음 업데이트할 인덱스를 계산한다.
        }
    };
    
    // BIT를 이용하여 1부터 idx까지의 누적 합을 구하는 람다 함수이다.
    auto query = [&](int idx) -> long long {
        long long sum = 0;
        while(idx > 0){
            sum += BIT[idx];      // BIT의 값을 누적한다.
            idx -= (idx & -idx);  // 다음에 방문할 인덱스를 계산한다.
        }
        return sum;               // 누적 합을 반환한다.
    };
    
    int m;
    cin >> m;                     // 쿼리의 개수 m을 입력받는다.
    while(m--){
        int type;
        cin >> type;              // 쿼리의 종류를 입력받는다.
        if(type == 1){
            int i, j;
            long long k;
            cin >> i >> j >> k;   // 구간 [i, j]와 더할 값 k를 입력받는다.
            update(i, k);         // i 위치부터 구간 업데이트를 위해 BIT에 k를 더한다.
            if(j+1 <= n)
                update(j+1, -k);  // j+1 위치에 -k를 더하여 구간 업데이트를 마감한다.
        } else { // type == 2
            int x;
            cin >> x;             // 점 쿼리를 위한 인덱스 x를 입력받는다.
            // BIT에서 구한 누적 합을 원래 수열의 값 A[x]에 더하여 결과를 출력한다.
            cout << A[x] + query(x) << "\n";
        }
    }
    
    return 0;                   // 프로그램을 종료한다.
}
```

위 C++ 코드는 Fenwick Tree를 사용하여 구간 업데이트와 점 쿼리를 O(log N) 시간 내에 처리하는 방법을 구현하였다이다. 각 쿼리마다 BIT의 업데이트와 누적 합 계산을 수행하여, 제한된 시간 내에 모든 연산을 처리할 수 있도록 설계하였다이다.

## Python 코드와 설명

```python
import sys
input = sys.stdin.readline  # 빠른 입력을 위해 sys.stdin.readline을 사용한다.

# BIT에 값을 업데이트하는 함수이다.
def update(BIT, n, idx, val):
    while idx <= n:
        BIT[idx] += val      # BIT의 해당 인덱스에 val을 더한다.
        idx += idx & -idx    # 다음 업데이트할 인덱스를 계산한다.

# BIT를 이용하여 1부터 idx까지의 누적 합을 구하는 함수이다.
def query(BIT, idx):
    s = 0
    while idx > 0:
        s += BIT[idx]        # BIT의 값을 누적한다.
        idx -= idx & -idx    # 다음에 방문할 인덱스를 계산한다.
    return s                 # 누적 합을 반환한다.

def main():
    n = int(input())         # 수열의 크기 n을 입력받는다.
    A = [0] + list(map(int, input().split()))  # 1번 인덱스부터 수열의 값을 입력받는다.
    BIT = [0] * (n + 1)      # BIT를 1-indexed로 사용하기 위해 n+1 크기의 리스트를 생성한다.
    m = int(input())         # 쿼리의 개수 m을 입력받는다.
    
    for _ in range(m):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            # 쿼리 형식이 1 i j k인 경우이다.
            _, i, j, k = tmp
            update(BIT, n, i, k)       # i 위치에 k를 더하여 구간 업데이트를 시작한다.
            if j + 1 <= n:
                update(BIT, n, j + 1, -k)  # j+1 위치에 -k를 더하여 구간 업데이트를 종료한다.
        else:
            # 쿼리 형식이 2 x인 경우이다.
            _, x = tmp
            # BIT에서 구한 누적 합을 원래 수열의 값 A[x]에 더하여 결과를 출력한다.
            print(A[x] + query(BIT, x))

if __name__ == '__main__':
    main()  # 메인 함수를 호출하여 프로그램을 실행한다.
```

위 Python 코드는 C++ 코드와 동일한 로직을 구현하였으며, sys.stdin.readline을 사용하여 빠른 입력을 지원한다. BIT를 이용한 업데이트와 쿼리 함수로 각 연산을 O(log N) 시간에 처리하며, 점 쿼리 시 원래 수열의 값에 누적 업데이트 값을 더하여 정답을 도출한다.

## 결론

본 문제는 구간 업데이트와 점 쿼리를 효율적으로 처리하기 위한 전형적인 문제로, Fenwick Tree를 활용하여 최적화된 해결법을 구현할 수 있음을 확인하였다. C++과 Python 두 가지 언어로 구현한 코드 모두, BIT를 사용하여 각 연산을 O(log N) 시간 내에 수행함으로써 대량의 쿼리에도 문제없이 대응할 수 있다. 문제 풀이를 진행하며 자료 구조의 응용과 차분 배열 개념의 중요성을 다시 한 번 깨달을 수 있었으며, 향후 유사한 문제에서 빠른 쿼리 처리를 위해 BIT 또는 Segment Tree의 활용 방안을 고려할 필요가 있음을 느꼈다.