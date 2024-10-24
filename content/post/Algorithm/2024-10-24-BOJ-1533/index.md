---
title: "[Algorithm] C++/Python 백준 1533번 : 길의 개수"
categories: 
- Algorithm
- Graph Theory
- Matrix Exponentiation
tags:
- Graph Theory
- Matrix Exponentiation
- Linear Algebra
- Dynamic Programming
- Divide and Conquer
- Mathematics
date: 2024-10-24
image: "tmp_wordcloud.png"
---

안녕하세요! 오늘은 백준 온라인 저지의 1533번 문제인 "길의 개수"를 함께 살펴보도록 하겠습니다.

문제 : [https://www.acmicpc.net/problem/1533](https://www.acmicpc.net/problem/1533)

## 문제 설명

세준이는 친구 정문이를 공항에서 데리러 가기로 했습니다. 그런데 정문이의 비행기가 연착되어 세준이는 공항까지 정확히 \( T \)분이 걸리는 경로를 찾아서 드라이브를 하려고 합니다. 도시에는 \( N \)개의 교차점이 있으며, 각 교차점 사이에는 길이 존재할 수 있습니다. 길은 이동하는 데 1분에서 5분까지 소요될 수 있으며, 길의 정보는 인접 행렬로 주어집니다.

세준이는 현재 위치 \( S \)에서 출발하여 \( T \)분 후에 공항 위치 \( E \)에 도착하는 경로의 개수를 구하고 싶습니다. 이때 가능한 경로의 수를 1,000,003으로 나눈 나머지를 출력해야 합니다.

## 접근 방식

이 문제는 가중치가 있는 그래프에서 정확히 \( T \)분 후에 도착하는 모든 경로의 수를 구하는 문제입니다. 각 간선의 가중치는 1부터 5까지의 정수로 제한되어 있으므로, 우리는 이를 활용하여 문제를 풀 수 있습니다.

**핵심 아이디어는 다음과 같습니다:**

1. **상태 공간 확장**: 각 교차점을 1분 단위로 분할하여 새로운 그래프를 생성합니다. 하지만 이 방법은 시간 복잡도가 매우 커지므로 효율적이지 않습니다.

2. **행렬 거듭제곱 사용**: 그래프의 인접 행렬을 사용하여 거듭제곱을 통해 \( T \)분 후의 상태를 계산할 수 있습니다. 하지만 간선 가중치가 여러 가지이므로 단순한 행렬 거듭제곱으로는 해결할 수 없습니다.

3. **블록 행렬과 상태 전이 행렬 구축**: 간선 가중치를 고려한 상태 전이 행렬을 구성하고, 이 행렬을 거듭제곱하여 필요한 시간을 맞출 수 있습니다.

**구체적인 해결 방법:**

- **확장된 상태 전이 행렬 구축**: 각 교차점마다 시간을 고려하여 상태를 확장합니다. 이를 위해 원래의 인접 행렬을 기반으로 5개의 작은 행렬을 만듭니다.

- **행렬 거듭제곱을 통한 계산**: 확장된 상태 전이 행렬을 \( T \)승하여 시작점에서 도착점으로의 경로 수를 계산합니다.

- **모듈러 연산**: 결과를 1,000,003으로 나눈 나머지를 계산합니다.

## C++ 코드와 설명

아래는 최적화된 C++ 코드이며, 각 부분에 대한 주석을 포함하고 있습니다.

```cpp
#include <iostream>
#include <vector>
#include <string>

using namespace std;

const int MOD = 1000003;
const int MAX_N = 50; // 최대 교차점 수 (N * 5까지 가능)

typedef vector<vector<int>> Matrix;

int N, S, E;
long long T;
Matrix adj;

Matrix multiply(const Matrix &a, const Matrix &b) {
    int n = a.size();
    Matrix result(n, vector<int>(n, 0));
    for(int i=0; i<n; ++i) {
        for(int k=0; k<n; ++k) {
            if(a[i][k]) {
                for(int j=0; j<n; ++j) {
                    result[i][j] = (result[i][j] + (long long)a[i][k] * b[k][j]) % MOD;
                }
            }
        }
    }
    return result;
}

Matrix power(Matrix base, long long exp) {
    int n = base.size();
    Matrix result(n, vector<int>(n, 0));
    for(int i=0; i<n; ++i) result[i][i] = 1; // 단위 행렬로 초기화
    while(exp > 0) {
        if(exp % 2 == 1) result = multiply(result, base);
        base = multiply(base, base);
        exp /= 2;
    }
    return result;
}

int main() {
    cin >> N >> S >> E >> T;
    S--; E--; // 인덱스를 0부터 시작하도록 조정
    adj.resize(N * 5, vector<int>(N * 5, 0)); // 확장된 상태 전이 행렬

    // 원래의 인접 행렬 입력
    for(int i=0; i<N; ++i) {
        string s;
        cin >> s;
        for(int j=0; j<N; ++j) {
            int val = s[j] - '0';
            if(val > 0) {
                // 간선 가중치에 따라 상태 전이 설정
                int from = i * 5;
                int to = j * 5;
                for(int k=0; k<val-1; ++k) {
                    adj[from + k][from + k + 1] = 1;
                }
                adj[from + val - 1][to] = 1;
            }
        }
    }

    // 행렬 거듭제곱을 이용하여 T분 후의 상태 계산
    Matrix result = power(adj, T);

    // 시작점에서 도착점으로의 경로 수 계산
    int ans = result[S * 5][E * 5] % MOD;
    cout << ans << endl;

    return 0;
}
```

### 코드 설명

1. **입력 및 초기화**:

   - 교차점 수 \( N \), 시작점 \( S \), 도착점 \( E \), 시간 \( T \)를 입력받습니다.
   - 인덱스를 0부터 시작하도록 \( S \)와 \( E \)를 감소시킵니다.
   - 확장된 상태 전이 행렬 `adj`를 초기화합니다.

2. **인접 행렬 처리**:

   - 각 교차점마다 입력된 문자열을 읽어 간선 정보를 파악합니다.
   - 간선의 가중치에 따라 상태 전이를 설정합니다.
   - 예를 들어, 가중치가 3인 간선은 3개의 상태로 분할되어 전이됩니다.

3. **행렬 거듭제곱**:

   - `power` 함수를 통해 상태 전이 행렬을 \( T \)승 합니다.
   - 이때 모듈러 연산을 통해 값의 범위를 조절합니다.

4. **결과 출력**:

   - 시작 상태에서 도착 상태로의 값이 경로의 수가 됩니다.
   - 이를 출력합니다.

## C++ without library 코드와 설명

`stdio.h`와 `malloc.h`만을 사용하여 동일한 로직을 구현한 코드입니다.

```c
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000003
#define MAX_N 50

typedef struct {
    int n;
    int **data;
} Matrix;

Matrix* create_matrix(int n) {
    Matrix* m = (Matrix*)malloc(sizeof(Matrix));
    m->n = n;
    m->data = (int**)malloc(sizeof(int*) * n);
    for(int i=0; i<n; ++i) {
        m->data[i] = (int*)calloc(n, sizeof(int));
    }
    return m;
}

void free_matrix(Matrix* m) {
    for(int i=0; i<m->n; ++i) {
        free(m->data[i]);
    }
    free(m->data);
    free(m);
}

Matrix* multiply(Matrix* a, Matrix* b) {
    int n = a->n;
    Matrix* result = create_matrix(n);
    for(int i=0; i<n; ++i) {
        for(int k=0; k<n; ++k) {
            if(a->data[i][k]) {
                for(int j=0; j<n; ++j) {
                    result->data[i][j] = (result->data[i][j] + (long long)a->data[i][k] * b->data[k][j]) % MOD;
                }
            }
        }
    }
    return result;
}

Matrix* power(Matrix* base, long long exp) {
    int n = base->n;
    Matrix* result = create_matrix(n);
    for(int i=0; i<n; ++i) result->data[i][i] = 1;
    while(exp > 0) {
        if(exp % 2 == 1) {
            Matrix* temp = multiply(result, base);
            free_matrix(result);
            result = temp;
        }
        Matrix* temp = multiply(base, base);
        free_matrix(base);
        base = temp;
        exp /= 2;
    }
    free_matrix(base);
    return result;
}

int main() {
    int N, S, E;
    long long T;
    scanf("%d %d %d %lld", &N, &S, &E, &T);
    S--; E--;
    int size = N * 5;
    Matrix* adj = create_matrix(size);
    for(int i=0; i<N; ++i) {
        char s[11];
        scanf("%s", s);
        for(int j=0; j<N; ++j) {
            int val = s[j] - '0';
            if(val > 0) {
                int from = i * 5;
                int to = j * 5;
                for(int k=0; k<val-1; ++k) {
                    adj->data[from + k][from + k + 1] = 1;
                }
                adj->data[from + val - 1][to] = 1;
            }
        }
    }
    Matrix* result = power(adj, T);
    int ans = result->data[S * 5][E * 5] % MOD;
    printf("%d\n", ans);
    free_matrix(result);
    return 0;
}
```

### 코드 설명

- **메모리 관리**: 동적 메모리 할당을 통해 행렬을 관리하며, 사용이 끝난 행렬은 `free_matrix` 함수를 통해 해제합니다.

- **기능 구현**: C++ 코드에서 사용한 기능들을 C 스타일로 재구현하였습니다.

- **동일한 로직**: 핵심 로직은 동일하며, 라이브러리의 도움 없이 구현되었습니다.

## Python 코드와 설명

Python을 사용하여 동일한 로직을 구현한 코드입니다.

```python
MOD = 1000003

def multiply(a, b):
    n = len(a)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % MOD
    return result

def power(base, exp):
    n = len(base)
    result = [[int(i==j) for j in range(n)] for i in range(n)]
    while exp > 0:
        if exp % 2 == 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exp //= 2
    return result

N, S, E, T = map(int, input().split())
S -= 1
E -= 1
size = N * 5
adj = [[0]*size for _ in range(size)]
for i in range(N):
    s = input()
    for j in range(N):
        val = int(s[j])
        if val > 0:
            from_idx = i * 5
            to_idx = j * 5
            for k in range(val - 1):
                adj[from_idx + k][from_idx + k + 1] = 1
            adj[from_idx + val - 1][to_idx] = 1

result = power(adj, T)
ans = result[S * 5][E * 5] % MOD
print(ans)
```

### 코드 설명

- **함수 구현**: `multiply`와 `power` 함수를 통해 행렬의 곱셈과 거듭제곱을 구현하였습니다.

- **입력 처리**: 입력받은 간선 정보를 기반으로 상태 전이 행렬을 구축합니다.

- **계산 및 출력**: C++ 코드와 동일한 로직으로 결과를 계산하고 출력합니다.

## 결론

이 문제는 그래프 이론과 행렬 거듭제곱을 활용하여 해결할 수 있는 좋은 예제였습니다. 간선 가중치가 여러 가지인 상황에서 상태를 확장하여 해결하는 아이디어가 핵심이었습니다. 이러한 유형의 문제는 고급 알고리즘과 자료 구조에 대한 이해를 높이는 데 도움이 됩니다.

추가적으로, 모듈러 연산의 중요성과 대규모 행렬 계산에서의 최적화 방법에 대해서도 생각해볼 수 있었습니다.