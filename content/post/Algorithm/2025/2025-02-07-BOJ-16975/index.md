---
title: "[Algorithm] C++/Python 백준 16975번 : 수열과 쿼리 21"
categories: 
- Algorithm
- Platinum IV
- FenwickTree
- RangeQuery
tags:
- FenwickTree
- RangeUpdate
- Implementation
- Optimization
- O(log N)
- BinaryIndexedTree
- PrefixSum
- RangeQuery
image: "index.png"
date: 2025-02-08
---

이번 글에서는 백준 16975번 문제인 "수열과 쿼리 21"을 다룰 것이다. 이 문제는 주어진 수열에 대해 여러 번의 구간 갱신과 특정 위치의 원소 값을 빠르게 조회해야 하는 상황을 제시한다. 이러한 연산을 효율적으로 처리하기 위해 Binary Indexed Tree(BIT) 또는 Segment Tree를 적용할 수 있다.

문제 : [https://www.acmicpc.net/problem/16975](https://www.acmicpc.net/problem/16975)

## 문제 설명

길이가 N인 수열 A가 주어진다고 할 때, 두 가지 유형의 쿼리를 처리하는 문제이다. 첫 번째 유형의 쿼리는 "1 i j k"의 형태로, 이는 수열 A의 구간 [i, j]에 있는 모든 원소에 k를 더한다는 의미이다. 예컨대, A가 [1, 2, 3, 4, 5]이고 쿼리가 "1 2 4 3"이라면, A[2], A[3], A[4]에 각각 3을 더하여 최종 수열은 [1, 5, 6, 7, 5]가 되는 식이다. 두 번째 유형의 쿼리는 "2 x"의 형태로, A[x] 값을 출력하라는 의미이다. 예를 들어 두 번째 유형의 쿼리가 "2 3"이고, 현재 수열이 [1, 5, 6, 7, 5]라면 결과로 6을 출력해야 한다.

수열의 크기 N은 최대 100,000까지 가능하며, 쿼리의 개수 M 역시 최대 100,000번 주어진다. 각 쿼리마다 구간 갱신을 수행해야 하므로, 단순한 방식으로 매 쿼리마다 구간 합을 순회하며 갱신하면 O(N) 시간이 걸리게 되고, M개의 쿼리를 전부 처리하는 데에 최악의 경우 O(N*M) = 10^10 정도의 연산이 필요할 수 있어 시간 안에 해결하기 어려울 것이다. 따라서 이를 효율적으로 해결하기 위해선 빠른 갱신과 빠른 질의를 처리할 수 있는 자료 구조가 필요하다.

이에 흔히 사용하는 자료 구조가 Fenwick Tree(이진 인덱스 트리)와 Segment Tree(세그먼트 트리)이다. Fenwick Tree를 사용하면 구간 업데이트와 한 점에서의 질의를 O(log N)에 처리할 수 있고, Segment Tree에 Lazy Propagation 기법을 적용하면 구간 업데이트와 한 점 질의를 동일하게 O(log N)에 처리할 수 있다. 이 문제에서는 Fenwick Tree를 사용하여 간단하고 빠르게 구현할 수 있다.

또한 문제에서 k는 -1,000,000 이상 1,000,000 이하이므로, 수열 원소에 음수도 더해질 수 있으며, 결과적으로 수열 원소가 커질 수도 있지만 64비트 정수(long long) 범위 내에서 충분히 처리 가능하다. 쿼리의 결과를 모두 출력한 뒤 프로그램을 종료하면 문제 해결이 완료된다.

정리하자면, 이 문제는 최대 100,000 길이의 수열에 대해 100,000번의 구간 갱신과 한 점 조회를 처리해야 하는 문제이다. 따라서 효율적인 자료 구조를 이용하여 O(M log N)의 시간 복잡도로 해결하는 것이 핵심이다. 대략적인 알고리즘 아이디어는 다음과 같다: Fenwick Tree를 이용해 특정 구간 [i, j]에 k를 더할 때, Fenwick Tree에 i 위치에 k를 더하고 j+1 위치에 -k를 더함으로써 누적합의 원리를 이용하여 구간 전체가 업데이트되도록 만든다. 그 후, 특정 위치 x의 값을 조회하려 할 때는 x 위치까지의 누적합을 구하여 원본 수열 값 + 누적합을 통해 실제 값을 찾아낸다.

以上의 설명에서 볼 수 있듯이, 주어진 문제는 구현 난이도가 크게 높지 않으나, 올바른 자료 구조 선택과 구현이 관건이다. 구간 업데이트와 한 점 쿼리를 빠르게 처리하는 Fenwick Tree의 사용 원리를 잘 이해한다면, 문제를 보다 간단히 해결할 수 있다.

## 접근 방식

1. **Fenwick Tree(BIT) 활용**  
   - Fenwick Tree를 두 개 구성할 필요 없이, 하나의 Fenwick Tree에 누적합을 이용한 '차분(Difference)' 개념을 적용한다.  
   - 구간 [i, j]에 k를 더한다는 것은, Fenwick Tree에 i 위치에 k를 더해주고, (j+1) 위치에 -k를 더해주는 방식으로 처리한다(단, j < N일 때에만 j+1 위치 업데이트를 수행).
   - 이는 누적합을 구할 때, i부터 j까지는 +k, j+1부터는 -k가 반영되어 결과적으로 [i, j] 구간 전체가 k만큼 증가하는 효과를 낸다.

2. **한 점 쿼리**  
   - x 위치의 실제 값은 A[x] + Fenwick Tree에서 x까지의 누적합을 구한 결과와 같다.  
   - 초기에 주어진 수열 A의 원소들은 Fenwick Tree에 반영되어 있지 않으므로, Fenwick Tree를 통해 얻어지는 것은 '추가로 더해진 값의 합'에 불과하다. 따라서 원래 배열의 값 A[x]와 Fenwick Tree에서 얻은 누적합을 더해 최종 결과값을 얻는다.

3. **시간 복잡도**  
   - Fenwick Tree의 업데이트 연산과 누적합 계산 연산은 모두 O(log N)에 처리할 수 있다.  
   - 쿼리가 최대 100,000번 주어지므로, 전체 복잡도는 O(M log N)이 되어 제한 시간을 무난히 만족한다.

4. **자료형 주의**  
   - k가 -1,000,000 이상 1,000,000 이하이며, 최대 100,000번 갱신이 가능하므로 중간 과정에서 값이 매우 커질 수 있다.  
   - 이를 안전하게 처리하기 위해 long long(64비트 정수) 자료형을 사용한다.

## C++ 코드와 설명

아래 코드는 Fenwick Tree를 이용하여 구간 업데이트와 한 점 쿼리를 처리하는 방법을 예시로 보인 것이다. 각 줄에 주석을 달아, 핵심 동작을 상세히 설명한다.

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main(){
    ios::sync_with_stdio(false);    // C++ 입출력 동기화를 끊어 속도를 높이는 명령어이다.
    cin.tie(nullptr);               // cin과 cout의 묶임을 풀어서 입출력 성능을 향상시킨다.

    int N;
    cin >> N;                       // 수열의 크기 N을 입력받는다.
    vector<long long> arr(N+1, 0LL);

    // 초기 수열의 정보를 입력받는다.
    for(int i = 1; i <= N; i++){
        cin >> arr[i];
    }

    // Fenwick Tree(BIT)를 구현하기 위한 벡터를 선언한다.
    vector<long long> BIT(N+1, 0LL);

    // Fenwick Tree에 값을 갱신하는 함수이다.
    auto update = [&](int idx, long long val){
        while(idx <= N){
            BIT[idx] += val;
            idx += (idx & -idx); // idx의 마지막 비트를 더하여 올라간다.
        }
    };

    // Fenwick Tree에서 idx까지의 누적합을 구하는 함수이다.
    auto fenwickSum = [&](int idx){
        long long result = 0LL;
        while(idx > 0){
            result += BIT[idx];
            idx -= (idx & -idx); // idx의 마지막 비트를 빼가며 내려간다.
        }
        return result;
    };

    int M;
    cin >> M;                       // 쿼리의 개수를 입력받는다.

    while(M--){
        int type;
        cin >> type;                // 쿼리 유형(1 또는 2)을 입력받는다.

        if(type == 1){
            int i, j;
            long long k;
            cin >> i >> j >> k;
            // 구간 [i, j]에 k를 더한다.
            update(i, k);          // i 위치에 k를 더한다.
            if(j+1 <= N) {         // j+1 위치에 -k를 더해, i~j 구간만 k가 적용되도록 한다.
                update(j+1, -k);
            }
        }
        else{
            int x;
            cin >> x;
            // x 위치의 실제 값을 구한다.
            long long answer = arr[x] + fenwickSum(x);
            cout << answer << "\n";
        }
    }
    return 0;
}
```

### 코드 동작 상세

1. `arr[i]`에는 초기에 주어진 수열 A의 값이 저장되어 있다.  
2. Fenwick Tree(BIT)는 모든 원소가 0으로 시작한다.  
3. `update(i, k)`를 통해 i 이상 구간에 k만큼을 더하는 의미를 BIT에 반영한다.  
4. 만약 구간이 [i, j]라면, j+1 위치에는 `-k`를 더함으로써, 누적합 과정에서 i부터 j까지만 k가 더해진다.  
5. 쿼리 종류가 2인 경우, `arr[x]`(원래 수열의 값)에 Fenwick Tree에서 얻은 누적합(`fenwickSum(x)`)을 더해 실제 A[x] 값을 계산한다.  
6. 이러한 과정을 통해, 모든 쿼리를 O(log N)에 처리가 가능해진다.

## Python 코드와 설명

Python 코드에서도 Fenwick Tree 방식을 동일하게 사용할 수 있다. 구현 방법은 비슷하며, 주의할 점은 인덱스 처리가 C++과 다를 수 있으니 적절히 조정해 주어야 한다는 것이다.

```python
import sys
input = sys.stdin.readline

def update(BIT, idx, val, N):
    # idx부터 Fenwick Tree에 val를 더함
    while idx <= N:
        BIT[idx] += val
        idx += (idx & -idx)

def fenwick_sum(BIT, idx):
    # idx까지의 누적합을 구함
    result = 0
    while idx > 0:
        result += BIT[idx]
        idx -= (idx & -idx)
    return result

def main():
    N = int(input().strip())
    arr = [0] + list(map(int, input().split()))
    
    BIT = [0] * (N+1)
    
    M = int(input().strip())
    for _ in range(M):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # 1 i j k
            _, i, j, k = query
            update(BIT, i, k, N)       # 구간 [i, j]에 k를 더하기 위해
            if j+1 <= N:
                update(BIT, j+1, -k, N)# j+1 위치에 -k를 더한다.
        
        else:
            # 2 x
            _, x = query
            # x 위치의 값 = 초기값 arr[x] + Fenwick Tree 누적합
            print(arr[x] + fenwick_sum(BIT, x))

if __name__ == "__main__":
    main()
```

### 코드 동작 상세

1. `arr` 리스트는 1번 인덱스부터 시작하도록 하여 인덱스 처리를 통일하였다.  
2. Fenwick Tree 배열 `BIT` 역시 크기를 N+1로 두어 1번 인덱스부터 사용한다.  
3. `update()` 함수는 인덱스에 val를 더한 후, `(idx & -idx)`를 통해 Fenwick Tree의 구조에 맞게 상위 구간에 누적 적용을 해주는 원리이다.  
4. `fenwick_sum()` 함수는 idx부터 비트 마스크를 이용해 하위 구간들의 합을 점진적으로 더해 최종 누적합을 구한다.  
5. 구간 업데이트 시, [i, j]에 k를 더하기 위해 i 위치에 k를 더하고 j+1 위치에 -k를 더한다.  
6. 최종적으로 한 점 쿼리를 수행할 때, `arr[x] + fenwick_sum(BIT, x)`를 출력함으로써 구간 업데이트까지 반영된 실제 값을 얻을 수 있다.

## 결론

"수열과 쿼리 21" 문제는 구간에 특정 값을 더하고 특정 위치의 값을 빠르게 구하는 전형적인 Range Update & Point Query 문제이다. Fenwick Tree(또는 Segment Tree의 Lazy Propagation)를 통해 효율적으로 해결 가능하다. 본 문제를 통해 Fenwick Tree의 차분(Difference) 개념을 활용하는 방법을 익히면, 구간 업데이트가 등장하는 다양한 문제에 응용할 수 있다. 추가적으로, Segment Tree를 사용하면 더 일반적인 구간 쿼리(예를 들어 구간 합, 구간 최솟값 등) 문제에서도 비슷한 원리로 확장할 수 있다는 점이 유용하다. 문제를 해결하면서 자료 구조와 알고리즘의 결합이 얼마나 큰 효과를 내는지 다시금 체감할 수 있었다.