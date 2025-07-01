---
title: "[Algorithm] C++/Python 백준 24505번 : blobhyperthink"
categories: 
- Algorithm
- Dynamic Programming
- Data Structures
tags:
- DP
- Binary Indexed Tree
- Brute Force
- Memoization
- O(N log N)
- Fenwick Tree
- 수학적 아이디어
- Dynamic Programming
image: "index.png"
date: 2025-02-10
---

본 포스트에서는 백준 24505번 "blobhyperthink" 문제를 소개하고 해결하는 과정을 상세히 설명하고자 하다. 해당 문제는 길이가 최대 10^5인 수열에서 길이가 11인 증가 부분 수열의 개수를 구하는 문제로, 단순한 브루트포스 방식으로는 시간 제한 내 해결이 어려워 동적 계획법(Dynamic Programming)과 세그먼트 트리(여기서는 Binary Indexed Tree, 즉 Fenwick Tree)를 이용한 최적화 기법이 필요하다. 문제의 난이도가 높은 이유는 부분 수열의 길이가 11로 고정되어 있으면서, 각 단계에서 이전 값들의 누적 합을 빠르게 구해야 하기 때문이다.

문제 : [https://www.acmicpc.net/problem/24505](https://www.acmicpc.net/problem/24505)

## 문제 설명

문제는 길이가 N인 정수 수열 A가 주어질 때, 다음 조건을 만족하는 11개의 인덱스 (i, j, k, l, m, o, p, q, r, s, t)를 찾는 경우의 수를 구하는 것이다. 조건은 다음과 같다.  
1. 인덱스의 순서는 i < j < k < l < m < o < p < q < r < s < t임이 보장되어야 하며,  
2. 해당 인덱스에 대응되는 수열의 값은 A_i < A_j < A_k < A_l < A_m < A_o < A_p < A_q < A_r < A_s < A_t를 만족하여야 한다.  

즉, 수열 내에서 11개의 원소를 선택하여 오름차순을 이루는 증가 부분 수열을 구성하는 모든 경우의 수를 구하고, 그 결과를 10^9+7로 나눈 나머지를 출력하는 문제이다.  
제한 조건은 다음과 같다.  
- 1 ≤ N ≤ 10^5  
- 1 ≤ A_i ≤ N (1 ≤ i ≤ N)  

문제의 주요 난관은 N이 최대 10^5이기 때문에, 모든 가능한 11개 조합을 직접 탐색하는 O(N^11) 또는 O(N^2) 이상의 단순 DP 접근 방식으로는 시간 제한을 만족시킬 수 없다는 점이다. 이에 따라, 각 단계별로 이전에 계산된 결과들을 빠르게 누적 합산할 수 있는 Binary Indexed Tree를 활용하여 시간 복잡도를 O(N log N)으로 낮추는 방법을 적용하였다. 이 방식은 각 원소를 처리할 때 해당 원소보다 작은 값들에 대해 이전 단계의 DP 값을 누적합으로 구하는 방식으로 동작한다.

## 접근 방식

문제를 해결하기 위해 먼저 동적 계획법(DP)을 사용하여 길이가 l인 증가 부분 수열의 개수를 dp[l]로 정의하였다.  
- 길이가 1인 경우는 단순히 각 원소 자체만으로 수열을 구성할 수 있으므로 모든 원소에 대해 1로 초기화된다.  
- 길이가 l (l ≥ 2)인 경우, 현재 원소 A[i]를 끝으로 하는 증가 부분 수열의 개수는 이전 단계(l-1)에서 A[i]보다 작은 값들에 해당하는 dp 값을 누적한 합과 같다.  

이와 같은 점화식을 만족시키기 위해, Binary Indexed Tree (BIT)를 l의 각 단계별로 하나씩 생성하여, 현재 처리 중인 원소보다 작은 값을 가진 이전 원소들의 DP 값을 빠르게 구간 합으로 계산한다. 각 BIT는 인덱스 값(수열의 원소 값)을 기준으로 누적 합을 관리하게 되며, 업데이트 및 쿼리 연산은 O(log N) 시간 안에 수행된다. 전체 알고리즘의 시간 복잡도는 11단계에 대해 각 단계별 BIT 연산을 수행하므로 O(11 * N log N)으로 제한 내 해결이 가능하다.

## C++ 코드와 설명

다음은 최적화된 C++ 코드이다. 코드 내에 각 라인별로 주석을 달아 코드의 동작을 상세히 설명하였다.

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

// Binary Indexed Tree (Fenwick Tree)를 구현한 구조체이다.
struct BIT {
    int n;
    vector<int> tree;
    
    // BIT 초기화, 크기는 n으로 설정한다.
    BIT(int n): n(n) {
        tree.assign(n + 1, 0);
    }
    
    // 인덱스 i에 delta 값을 더하면서 BIT를 업데이트하는 함수이다.
    void update(int i, int delta) {
        while (i <= n) {
            tree[i] = (tree[i] + delta) % MOD;
            i += i & (-i);
        }
    }
    
    // 1부터 인덱스 i까지의 누적 합을 구하는 함수이다.
    int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum = (sum + tree[i]) % MOD;
            i -= i & (-i);
        }
        return sum;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    // 수열 A를 입력받는다.
    vector<int> A(N);
    for (int i = 0; i < N; i++){
        cin >> A[i];
    }
    
    const int L = 11;  // 찾고자 하는 증가 부분 수열의 길이이다.
    
    // 길이가 1부터 L까지의 BIT를 생성한다.
    vector<BIT> bits;
    for (int l = 0; l <= L; l++){
        bits.push_back(BIT(N));
    }
    
    // 수열의 각 원소에 대해 DP 값을 BIT를 이용하여 업데이트한다.
    for (int i = 0; i < N; i++){
        int a = A[i];
        // 길이가 1인 경우, 원소 하나만으로 이루어진 수열이므로 1을 더한다.
        bits[1].update(a, 1);
        
        // 길이가 2 이상인 경우, 이전 단계의 BIT에서 현재 원소보다 작은 값들의 누적 합을 구한다.
        for (int l = 2; l <= L; l++){
            int count = bits[l - 1].query(a - 1);
            bits[l].update(a, count);
        }
    }
    
    // 길이가 L인 증가 부분 수열의 총 개수를 구한다.
    int answer = bits[L].query(N);
    cout << answer % MOD << "\n";
    
    return 0;
}
```

코드의 동작은 다음과 같다.  
1. 입력으로 수열의 길이 N과 수열 A를 입력받는다.  
2. 길이가 1부터 11까지의 BIT를 생성하여 각 단계별로 증가 부분 수열의 개수를 저장한다.  
3. 각 원소 A[i]에 대해, 길이가 1인 경우 BIT[1]에 1을 업데이트하며, 길이가 2 이상인 경우 BIT[l-1]에서 A[i]-1까지의 누적 합을 구하여 BIT[l]을 업데이트한다.  
4. 모든 원소에 대해 처리가 완료되면 BIT[11]에 저장된 전체 누적 합을 출력한다.

## Python 코드와 설명

다음은 최적화된 Python 코드이다. 코드 내 각 라인별로 주석을 달아 동작을 상세히 설명하였다.

```python
MOD = 10**9 + 7

# sys.stdin.readline을 사용하여 빠른 입력을 받는다.
import sys
input = sys.stdin.readline

# 수열의 길이 N을 입력받는다.
N = int(input())
# 수열 A를 입력받는다.
A = list(map(int, input().split()))
L = 11  # 찾고자 하는 증가 부분 수열의 길이이다.

# Binary Indexed Tree (Fenwick Tree)를 구현한 클래스이다.
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    # BIT를 업데이트하는 함수이다.
    def update(self, i, val):
        while i <= self.n:
            self.tree[i] = (self.tree[i] + val) % MOD
            i += i & -i
    
    # BIT에서 1부터 i까지의 누적 합을 구하는 함수이다.
    def query(self, i):
        s = 0
        while i > 0:
            s = (s + self.tree[i]) % MOD
            i -= i & -i
        return s

# 길이 1부터 L까지 각각의 BIT를 리스트에 저장한다.
bits = [BIT(N) for _ in range(L + 1)]

# 수열의 각 원소에 대해 DP 값을 BIT를 이용해 업데이트한다.
for a in A:
    # 길이가 1인 경우, 자기 자신만으로 증가 부분 수열을 구성하므로 1을 업데이트한다.
    bits[1].update(a, 1)
    # 길이가 2 이상인 경우, 이전 BIT에서 현재 원소보다 작은 값들의 누적 합을 구하여 업데이트한다.
    for l in range(2, L + 1):
        count = bits[l - 1].query(a - 1)
        bits[l].update(a, count)

# 길이가 L인 증가 부분 수열의 총 개수를 출력한다.
print(bits[L].query(N) % MOD)
```

코드의 동작 과정은 다음과 같다.  
1. 입력받은 N과 수열 A를 기반으로, 길이 11의 증가 부분 수열을 구하기 위해 BIT 클래스를 사용하여 BIT 객체를 생성한다.  
2. 각 원소에 대해 길이가 1인 경우에는 BIT[1]에 1을 업데이트하며, 길이가 2 이상인 경우 BIT[l-1]에서 현재 원소보다 작은 원소들의 누적 합을 구하여 BIT[l]을 업데이트한다.  
3. 모든 처리가 완료된 후 BIT[11]의 누적 합을 출력하여 정답을 도출한다.

## 결론

본 문제는 N의 크기가 크고 부분 수열의 길이가 고정되어 있음에도 불구하고, Binary Indexed Tree를 활용한 동적 계획법으로 효율적으로 해결할 수 있음을 확인하였다. BIT를 이용하면 각 단계에서 빠른 구간 합 계산이 가능하여 전체 알고리즘의 시간 복잡도를 O(N log N)으로 줄일 수 있었다. 문제 풀이를 통해 DP와 자료 구조의 결합이 복잡한 문제에서도 강력한 해결 방법임을 다시 한 번 느낄 수 있었으며, 향후 유사한 문제들에 적용할 수 있는 최적화 기법으로 활용할 수 있음을 깨달았다.