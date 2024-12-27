---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-20T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Matrix Exponentiation
- Dynamic Programming
- Modular Arithmetic
- O(log N)
- Graph Theory
- Optimization
title: '[Algorithm] C++/Python 백준 17401번 : 일하는 세포'

---

백준 17401번 문제인 "Red Blood Cell"은 적혈구가 변화하는 혈관 지도를 바탕으로 특정 시간 후에 특정 지점에 도달할 수 있는 경로의 수를 구하는 문제이다. 주어진 문제에서 우리는 N개의 거점과 그 사이의 변동하는 혈관 연결 정보를 이용하여 D초 후 특정 거점에 도달하는 경로 수를 계산해야 한다. 

주기적으로 변하는 혈관 정보가 주어지며, 이 정보를 이용하여 D초 동안 가능한 모든 경로 수를 구하는 것이 문제의 목표이다. 문제를 푸는 핵심 아이디어는 주어진 T초 주기의 혈관 지도를 반복적으로 곱하면서, 원하는 시간 D초 후에 각 거점 쌍 사이에 도달할 수 있는 경로 수를 구하는 것이다.

문제 : [https://www.acmicpc.net/problem/17401](https://www.acmicpc.net/problem/17401)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 주어진 T개의 혈관 지도에서 거점 간 이동 경로를 계산하는 문제이다. 그래프의 상태는 시간에 따라 변동하며, 이 변동이 주기적으로 반복된다는 특성을 이용해 효율적인 풀이가 가능하다. 이를 위해 우리는 **행렬 거듭제곱(Matrix Exponentiation)** 알고리즘을 활용하여 시간 복잡도를 줄인다. 각 혈관 지도는 N x N 크기의 그래프 상태를 나타내며, 이 그래프 상태를 기반으로 시간에 따른 경로 수를 행렬 곱을 통해 계산할 수 있다. 

### 해결 전략:
1. **행렬을 통한 경로 계산**: N개의 거점과 그 사이의 이동 경로를 나타내는 혈관 지도는 행렬로 표현할 수 있다. 각 시간에 따라 변동하는 지도는 주기를 가지고 있기 때문에, 매 초마다 변하는 그래프 상태를 반복적으로 곱해 나가면 D초 후의 경로 수를 구할 수 있다.
   
2. **행렬 거듭제곱**: D가 매우 큰 수이므로, 모든 시간을 직접 시뮬레이션하면 시간 초과가 발생할 수 있다. 따라서, 우리는 **행렬 거듭제곱(Matrix Exponentiation)**을 사용하여 O(log N) 시간 복잡도 내에 문제를 해결할 수 있다.

3. **모듈로 연산**: 경로의 수가 매우 커질 수 있기 때문에, 결과를 매번 1,000,000,007로 나눈 나머지를 계산해야 한다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long LL;
const LL MOD = 1000000007;

// 두 행렬을 곱하는 함수 (MOD로 나눈 나머지 연산 포함)
vector<LL> mat_mult(const vector<LL>& a, const vector<LL>& b, int N) {
    vector<LL> c(N * N, 0);
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            LL a_ik = a[i * N + k];
            if (a_ik == 0) continue;
            for (int j = 0; j < N; ++j) {
                c[i * N + j] = (c[i * N + j] + a_ik * b[k * N + j]) % MOD;
            }
        }
    }
    return c;
}

// 행렬을 거듭제곱하는 함수 (MOD로 나눈 나머지 연산 포함)
vector<LL> mat_pow(const vector<LL>& a, LL power, int N) {
    vector<LL> result(N * N, 0);
    for (int i = 0; i < N; ++i) result[i * N + i] = 1; // Identity matrix
    vector<LL> base = a;
    while (power > 0) {
        if (power & 1) result = mat_mult(result, base, N);
        base = mat_mult(base, base, N);
        power >>= 1;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int T, N;
    LL D;
    cin >> T >> N >> D;

    vector<vector<LL>> g(T, vector<LL>(N * N, 0));
    for (int t = 0; t < T; ++t) {
        int Mi;
        cin >> Mi;
        for (int m = 0; m < Mi; ++m) {
            int a, b, c;
            cin >> a >> b >> c;
            g[t][(a - 1) * N + (b - 1)] = (g[t][(a - 1) * N + (b - 1)] + c) % MOD;
        }
    }

    // 주기 행렬 M_cycle을 계산
    vector<LL> M_cycle(N * N, 0);
    for (int i = 0; i < N; ++i) M_cycle[i * N + i] = 1;
    for (int t = 0; t < T; ++t) M_cycle = mat_mult(M_cycle, g[t], N);

    // D초 동안의 이동을 계산
    LL q = D / T, r = D % T;
    vector<LL> M_total = mat_pow(M_cycle, q, N);
    for (int t = 0; t < r; ++t) M_total = mat_mult(M_total, g[t], N);

    // 결과 출력
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cout << M_total[i * N + j] << " ";
        }
        cout << "\n";
    }
}
```

**C++ 코드 설명**
- `mat_mult` 함수는 행렬의 곱셈을 수행하며, 두 행렬을 곱한 결과를 반환한다.
- `mat_pow_func`는 주어진 행렬의 거듭제곱을 효율적으로 계산하기 위해 분할정복 기법을 사용한다.
- 주어진 혈관 지도 정보를 이용해 주기적인 변동을 고려한 경로 수를 계산한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <malloc.h>

#define MOD 1000000007
typedef long long LL;

LL* mat_mult(LL* a, LL* b, int N){
    LL* c = (LL*)malloc(sizeof(LL) * N * N);
    for(int i = 0; i < N * N; i++) c[i] = 0;
    
    for(int i = 0; i < N; i++){
        for(int k = 0; k < N; k++){
            LL a_ik = a[i * N + k];
            if(a_ik == 0) continue;
            for(int j = 0; j < N; j++){
                c[i * N + j] += a_ik * b[k * N + j];
                if(c[i * N + j] >= MOD) c[i * N + j] %= MOD;
            }
        }
    }
    return c;
}

LL* mat_pow_func(LL* a, LL power, int N){
    LL* result = (LL*)malloc(sizeof(LL) * N * N);
    for(int i = 0; i < N * N; i++) result[i] = (i % (N+1) == 0) ? 1 : 0;
    
    LL* base = (LL*)malloc(sizeof(LL) * N * N);
    for(int i = 0; i < N * N; i++) base[i] = a[i];
    
    while(power > 0){
        if(power & 1){
            result = mat_mult(result, base, N);
        }
        base = mat_mult(base, base, N);
        power >>= 1;
    }
    return result;
}

int main(){
    int T, N;
    LL D;
    scanf("%d %d %lld", &T, &N, &D);
    
    LL** g = (LL**)malloc(sizeof(LL*) * T);
    for(int t = 0; t < T; t++){
        g[t] = (LL*)malloc(sizeof(LL) * N * N);
        for(int i = 0; i < N * N; i++) g[t][i] = 0;
        
        int Mi;
        scanf("%d", &Mi);
        for(int m = 0; m < Mi; m++){
            int a, b, c;
            scanf("%d %d %d", &a, &b, &c);
            g[t][(a-1) * N + (b-1)] += c;
            if(g[t][(a-1) * N + (b-1)] >= MOD) g[t][(a-1) * N + (b-1)] %= MOD

;
        }
    }
    
    LL* M_cycle = (LL*)malloc(sizeof(LL) * N * N);
    for(int i = 0; i < N * N; i++) M_cycle[i] = (i % (N+1) == 0) ? 1 : 0;
    for(int t = 0; t < T; t++){
        M_cycle = mat_mult(M_cycle, g[t], N);
    }
    
    LL q = D / T;
    LL r = D % T;
    
    LL* M_cycle_q = mat_pow_func(M_cycle, q, N);
    LL* M_r = (LL*)malloc(sizeof(LL) * N * N);
    for(int i = 0; i < N * N; i++) M_r[i] = (i % (N+1) == 0) ? 1 : 0;
    
    for(int t = 0; t < r; t++){
        M_r = mat_mult(M_r, g[t], N);
    }
    
    LL* M_total = mat_mult(M_cycle_q, M_r, N);
    
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            printf("%lld ", M_total[i * N + j]);
        }
        printf("\n");
    }
    
    return 0;
}
```

### C++ without library 코드 설명
- 표준 라이브러리 없이 `stdio.h`와 `malloc.h`만 사용하여 코드를 구현하였다.
- 메모리 할당 및 행렬 연산이 수동적으로 이루어진다.

## Python 코드와 설명

```python
MOD = 1000000007

def mat_mult(a, b, N):
    c = [[0] * N for _ in range(N)]
    for i in range(N):
        for k in range(N):
            if a[i][k] == 0: continue
            for j in range(N):
                c[i][j] += a[i][k] * b[k][j]
                c[i][j] %= MOD
    return c

def mat_pow_func(a, power, N):
    result = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    base = [row[:] for row in a]
    
    while power > 0:
        if power & 1:
            result = mat_mult(result, base, N)
        base = mat_mult(base, base, N)
        power >>= 1
    return result

def main():
    T, N, D = map(int, input().split())
    
    g = []
    for _ in range(T):
        Mi = int(input())
        mat = [[0] * N for _ in range(N)]
        for _ in range(Mi):
            a, b, c = map(int, input().split())
            mat[a-1][b-1] += c
            mat[a-1][b-1] %= MOD
        g.append(mat)
    
    M_cycle = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    for t in range(T):
        M_cycle = mat_mult(M_cycle, g[t], N)
    
    q = D // T
    r = D % T
    
    M_cycle_q = mat_pow_func(M_cycle, q, N) if q > 0 else [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    
    M_r = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    for t in range(r):
        M_r = mat_mult(M_r, g[t], N)
    
    M_total = mat_mult(M_cycle_q, M_r, N)
    
    for row in M_total:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    main()
```

### Python 코드 설명
- Python에서는 리스트 컴프리헨션을 사용하여 행렬을 생성하고, 행렬 곱셈과 거듭제곱을 구현한다.
- Python의 `list` 구조를 사용하여 간결하게 코드를 작성하였다.

## 결론

이 문제는 주기적으로 변하는 그래프의 상태를 계산하여 D초 후 특정 위치에 도달하는 경로 수를 계산하는 문제이다. 효율적인 풀이를 위해 **행렬 거듭제곱**과 **모듈로 연산**을 활용하였다. Python과 C++ 모두 적절한 자료 구조와 알고리즘을 사용하여 시간 복잡도를 줄였고, 특히 D의 값이 매우 클 경우 O(log D)의 시간 복잡도로 문제를 해결할 수 있었다. 추가적인 최적화는 메모리 사용을 줄이는 방식으로 이루어질 수 있을 것이다.
```