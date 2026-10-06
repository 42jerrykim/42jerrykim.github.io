---
description: "백준 17401번 일하는 세포 문제는 주기적으로 변하는 혈관 지도에서 N개의 거점과 시간 D초 후에 특정 거점에 도달할 수 있는 경로의 수를 묻는다. 행렬 곱과 거듭제곱을 이용해 행렬 곱 횟수를 O(log(D/T))로 줄여 효율적으로 계산하며, 동적 그래프와 모듈러 연산이 핵심이다."
image: "wordcloud.png"
categories: Algorithm
date: "2024-09-20T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- DP(동적계획법)
- Time-Complexity(시간복잡도)
- Graph-Theory(그래프이론)
- Optimization(최적화)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- Implementation(구현)
- Coding-Test(코딩테스트)
- Data-Structures(자료구조)
- Code-Quality(코드품질)
- Python
- Divide-and-Conquer(분할정복)
- Matrix(행렬)
- Graph(그래프)
- Simulation(시뮬레이션)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Testing(테스트)
- Modular-Arithmetic(모듈러)
- Best-Practices
- Complexity-Analysis(복잡도분석)
- Debugging(디버깅)
- Refactoring(리팩토링)
- Clean-Code(클린코드)
- Performance(성능)
- Pitfalls(함정)
- Error-Handling(에러처리)
title: '[Algorithm] C++/Python 백준 17401번 : 일하는 세포'

---

백준 17401번 문제인 "Red Blood Cell"은 적혈구가 변화하는 혈관 지도를 바탕으로 특정 시간 후에 특정 지점에 도달할 수 있는 경로의 수를 구하는 문제이다. 주어진 문제에서 우리는 N개의 거점과 그 사이의 변동하는 혈관 연결 정보를 이용하여 D초 후 특정 거점에 도달하는 경로 수를 계산해야 한다. 

주기적으로 변하는 혈관 정보가 주어지며, 이 정보를 이용하여 D초 동안 가능한 모든 경로 수를 구하는 것이 문제의 목표이다. 문제를 푸는 핵심 아이디어는 주어진 T초 주기의 혈관 지도를 반복적으로 곱하면서, 원하는 시간 D초 후에 각 거점 쌍 사이에 도달할 수 있는 경로 수를 구하는 것이다.

문제 : [https://www.acmicpc.net/problem/17401](https://www.acmicpc.net/problem/17401)

## 이 글에서 얻어 갈 것

- 인접행렬의 k제곱이 길이 k 경로의 수를 센다는 사실을 증명 스케치와 함께 이해한다.
- 시간에 따라 바뀌는 그래프를 "주기 행렬 하나"로 압축하는 곱 순서를 설명할 수 있다.
- 행렬 거듭제곱의 실제 시간 복잡도 O(N³ · log(D/T) + T · N³)를 계산한다.

## 접근 방식

이 문제는 주어진 T개의 혈관 지도에서 거점 간 이동 경로를 계산하는 문제이다. 그래프의 상태는 시간에 따라 변동하며, 이 변동이 주기적으로 반복된다는 특성을 이용해 효율적인 풀이가 가능하다. 이를 위해 우리는 **행렬 거듭제곱(Matrix Exponentiation)** 알고리즘을 활용하여 시간 복잡도를 줄인다. 각 혈관 지도는 N x N 크기의 그래프 상태를 나타내며, 이 그래프 상태를 기반으로 시간에 따른 경로 수를 행렬 곱을 통해 계산할 수 있다. 

### 해결 전략:
1. **행렬을 통한 경로 계산**: N개의 거점과 그 사이의 이동 경로를 나타내는 혈관 지도는 행렬로 표현할 수 있다. 각 시간에 따라 변동하는 지도는 주기를 가지고 있기 때문에, 매 초마다 변하는 그래프 상태를 반복적으로 곱해 나가면 D초 후의 경로 수를 구할 수 있다.
   
2. **행렬 거듭제곱**: D가 매우 큰 수이므로, 모든 시간을 직접 시뮬레이션하면 시간 초과가 발생할 수 있다. 따라서, 우리는 <strong>행렬 거듭제곱(Matrix Exponentiation)</strong>을 사용하여 곱셈 횟수를 O(log(D/T))번으로 줄인다. N×N 행렬 한 번의 곱이 O(N³)이므로 전체 시간 복잡도는 주기 행렬을 만드는 O(T · N³)와 거듭제곱의 O(N³ · log(D/T))를 합한 O(N³ · log(D/T) + T · N³)이다.

3. **모듈로 연산**: 경로의 수가 매우 커질 수 있기 때문에, 결과를 매번 1,000,000,007로 나눈 나머지를 계산해야 한다.

```mermaid
flowchart LR
    A["g₀ … g_T-1<br/>초별 인접행렬"] --> B["M = g₀·g₁·…·g_T-1<br/>한 주기 행렬"]
    B --> C["M^q<br/>이진 거듭제곱"]
    C --> D["M^q · g₀·…·g_r-1<br/>나머지 r초 반영"]
    D --> E["D초 후 경로 수 행렬"]
```

위 흐름이 세 구현 모두에 공통이다. 아래 표는 단계별 비용이다.

| 단계 | 연산 | 시간 | 추가 공간 |
|---|---|---|---|
| 주기 행렬 M 만들기 | T번의 N×N 곱 | O(T · N³) | O(T · N²) (g 보관) |
| M^q 구하기 | 이진 거듭제곱 | O(N³ · log(D/T)) | O(N²) |
| 나머지 r초 반영 | r < T번의 곱 | O(T · N³) | O(N²) |

### 왜 행렬 곱이 경로 수를 세는가

간선 가중치(같은 정점쌍을 잇는 간선의 개수)를 담은 인접행렬을 A라 하면, 곱 (A·B)[i][j] = Σₖ A[i][k]·B[k][j]는 "i에서 k까지 A의 한 걸음, k에서 j까지 B의 한 걸음"으로 이루어진 두 걸음 경로의 수를 모든 중간 정점 k에 대해 더한 값이다. 중간 정점이 다른 경로는 서로 다른 경로이므로 합이 곧 전체 경로 수가 되고, 귀납적으로 A₁·A₂·…·A_k의 (i, j) 성분은 1초에는 A₁, 2초에는 A₂, …의 간선만 쓰는 길이 k 경로의 수가 된다. 이 대응이 성립하므로 시간에 따라 바뀌는 그래프라도 초 단위 행렬을 시간 순서대로 곱하면 된다.

행렬 곱은 교환법칙이 성립하지 않으므로 곱 순서가 곧 시간 순서이다. T초짜리 한 주기의 행렬은 M = g₀·g₁·…·g_{T−1}로 정의하고, D = q·T + r이면 답은 M^q · g₀·…·g_{r−1}이다. 결합법칙은 성립하므로 M^q를 이진 거듭제곱으로 묶어 계산해도 결과가 같다. 희소 행렬이나 벡터-행렬 곱으로 바꾸면 특정 시작점 하나만 구할 때 N³을 N²로 줄일 수 있지만, 이 문제는 모든 정점쌍의 결과를 요구하므로 전체 행렬 곱을 쓴다.

## C++ 코드와 설명

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
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
`mat_mult`는 i-k-j 순서로 반복문을 돌며 a[i][k]가 0이면 안쪽 루프를 건너뛰므로, 간선이 드문 지도에서는 N³보다 빠르게 끝난다. 모듈로는 곱셈 직후마다 적용하므로 LL(64비트) 안에서 (10⁹+7)² 정도의 중간값이 넘치지 않는다. `mat_pow`는 power의 이진 표현을 아래 비트부터 읽으며 해당 비트가 1일 때만 결과에 현재 base를 곱하고, 매 단계 base를 제곱하는 분할정복이다. `main`은 입력으로 받은 g[t]를 시간 순서대로 곱해 M_cycle을 만들고, q = D / T만큼 거듭제곱한 뒤 나머지 r초 분량의 g[t]를 오른쪽에 이어 곱해 마무리한다.

한 가지 짚을 점은 이 코드에서 q가 0이어도 mat_pow가 단위행렬을 돌려주므로 D < T인 경우에 별도 분기가 필요 없다는 것이다.

## C++ without library 구현에 대하여

표준 라이브러리 없이 `stdio.h`와 `malloc.h`만 쓰는 C 스타일 구현도 구조는 위 C++ 코드와 같아서 코드는 생략하고 차이만 적는다.
이 버전은 `vector` 대신 malloc으로 N×N 배열을 직접 할당하고, 단위행렬은 `i % (N+1) == 0`인 평탄화 인덱스(대각선 위치)를 1로 두어 만든다. 로직은 C++ 버전과 같지만 `mat_mult`가 호출될 때마다 새 배열을 할당하면서 이전 포인터를 free하지 않는다. 곱 횟수가 O(T + log(D/T))이므로 누수량은 N²·8바이트에 그 횟수를 곱한 크기로 제한되지만, N이 커지면 메모리 제한에 걸릴 수 있어 실전에서는 결과를 받은 직후 이전 행렬을 해제해야 한다. 모듈로는 `>= MOD`일 때만 나머지를 구해 느린 나눗셈 연산 횟수를 줄인다.

## Python 코드와 설명

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
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
Python 버전은 2차원 리스트로 행렬을 표현하고 리스트 컴프리헨션으로 단위행렬을 만든다. 구조는 앞의 두 구현과 같지만 인터프리터 오버헤드 때문에 N³ 곱셈이 훨씬 느리다. 따라서 N이 큰 입력에서는 시간 제한을 넘길 위험이 있고, 이 경우 NumPy 같은 배열 연산 라이브러리나 C++ 구현을 쓰는 편이 안전하다. 정수 오버플로가 없는 파이썬에서도 각 곱셈 뒤 `%= MOD`를 두는 이유는 수가 불필요하게 커져 연산이 느려지는 것을 막기 위해서이다.

## 흔한 오해와 사용 판단 기준

가장 흔한 실수는 곱 순서를 뒤집는 것이다. 행렬 곱은 교환법칙이 성립하지 않아 g_{T−1}·…·g₀로 곱하면 시간이 거꾸로 흐르는 그래프의 경로 수가 나오므로, 반드시 시간 오름차순으로 곱해야 한다. 두 번째 실수는 D가 T의 배수가 아닐 때 나머지 r초를 빠뜨리거나, r초 분량을 g₀부터가 아니라 마지막 주기의 g에서 잘라 쓰는 것이다. 주기가 처음으로 돌아가므로 나머지는 항상 g₀부터 g_{r−1}까지이다.

행렬 거듭제곱은 D가 아주 커서 초 단위 시뮬레이션이 불가능하고 N이 작을 때(N³ · log가 감당 가능할 때) 쓴다. 반대로 D가 작거나, 특정 시작점 하나의 결과만 필요하면 벡터에 행렬을 곱하는 O(D · N²) 방식이 더 단순하고 빠를 수 있다. 같은 계열의 기법으로는 피보나치 수열을 2×2 행렬의 거듭제곱으로 구하는 방법이 있다.

## 결론

이 문제의 핵심은 시간에 따라 바뀌는 그래프를 한 주기 행렬로 압축하고 이를 거듭제곱하는 것이다. D가 매우 커도 행렬 곱 횟수가 로그로 줄어 O(N³ · log(D/T) + T · N³)에 풀린다. 추가적인 최적화는 메모리 사용을 줄이는 방식으로 이루어질 수 있다.

## 참고 문헌

- [Exponentiation by squaring (Wikipedia)](https://en.wikipedia.org/wiki/Exponentiation_by_squaring): 이진 거듭제곱의 원리와 행렬에 적용하는 방법
- [Binary Exponentiation (cp-algorithms)](https://cp-algorithms.com/algebra/binary-exp.html): 거듭제곱의 분할정복과 행렬·모듈로 응용 예제
- [Adjacency matrix (Wikipedia)](https://en.wikipedia.org/wiki/Adjacency_matrix): 인접행렬과 그 거듭제곱의 의미

## 코너 케이스 및 실수 포인트

아래 표는 구현할 때 확인할 항목이다.

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 또는 빈 입력 | 반복문 범위·예외 처리 확인 |
| **오버플로우** | 답이 $2^{31}$ 초과 가능 | `long long` (C++) 등 사용 |
| **D < T** | q = 0이라 한 주기도 못 채움 | mat_pow가 단위행렬을 반환하므로 r초 곱만 적용 |
| **T = 1** | 지도가 항상 같음 | M = g₀이고 r = 0, 일반 인접행렬 거듭제곱과 동일 |
| **곱 순서** | 교환법칙 불성립 | 항상 g₀부터 시간 오름차순으로 곱함 |
