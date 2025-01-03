---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- SparseTable
- RangeQuery
- Preprocessing
- DataStructures
- SegmentTree
- RMQ
title: '[Algorithm] C++/Python 백준 2357번 : 최솟값과 최댓값'
---

이번 포스팅에서는 백준 온라인 저지의 2357번 문제인 **"최솟값과 최댓값"**을 다뤄보겠다. 이 문제는 수열에서 여러 구간에 대한 최솟값과 최댓값을 효율적으로 구하는 알고리즘을 요구한다. 수열의 크기가 매우 크기 때문에 단순한 방법으로는 시간 내에 해결하기 어렵다. 따라서 **Sparse Table**과 같은 효율적인 자료 구조를 활용하여 문제를 해결해보자.

문제 : [https://www.acmicpc.net/problem/2357](https://www.acmicpc.net/problem/2357)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

N개의 정수로 이루어진 수열이 주어진다. 이 수열에서 M개의 쿼리가 주어지는데, 각 쿼리는 구간 [a, b]에 대해 그 구간에 포함된 정수들의 **최솟값**과 **최댓값**을 구하는 것이다. 여기서 a번째와 b번째는 수열이 입력된 순서를 의미한다.

**제약 조건은 다음과 같다:**

- **N (1 ≤ N ≤ 100,000)**: 수열의 원소 개수
- **M (1 ≤ M ≤ 100,000)**: 쿼리의 개수
- **각 원소의 값은 1 이상 1,000,000,000 이하의 정수**
- **각 쿼리는 [a, b] 형태로 주어지며, a ≤ b**

예를 들어, 수열이 [75, 30, 100, 38, 50, 51, 52, 20, 81, 5]로 주어지고 쿼리가 (1, 10), (3, 5), (6, 9), (8, 10)이라면, 각 구간에 대한 최솟값과 최댓값은 다음과 같다:

- (1, 10): 최솟값 5, 최댓값 100
- (3, 5): 최솟값 38, 최댓값 100
- (6, 9): 최솟값 20, 최댓값 81
- (8, 10): 최솟값 5, 최댓값 81

**문제의 핵심은 다음과 같다:**

- 수열과 쿼리의 개수가 많기 때문에, 각 쿼리마다 구간을 순회하여 최솟값과 최댓값을 구하면 **시간 초과**가 발생한다.
- 따라서, **전처리**를 통해 구간에 대한 정보를 미리 계산하여, 각 쿼리를 **효율적으로** 처리해야 한다.

## 접근 방식

이 문제를 효율적으로 해결하기 위해서는 다음과 같은 알고리즘과 자료 구조를 사용한다:

1. **Sparse Table**

   - 수열이 변경되지 않을 때, 구간의 최솟값과 최댓값을 빠르게 구하기 위한 자료 구조이다.
   - 전처리에 O(N log N)의 시간이 걸리며, 각 쿼리는 O(1)에 처리할 수 있다.

2. **전처리 (Preprocessing)**

   - 구간 길이에 따른 최솟값과 최댓값을 미리 계산하여 테이블에 저장한다.
   - 로그 값을 미리 계산하여 쿼리 시 사용할 수 있도록 한다.

**구체적인 해결 방법은 다음과 같다:**

- **로그 값 계산**

  - 구간의 길이에 따른 로그 값을 미리 계산하여 배열에 저장한다.
  - 이는 쿼리 시에 사용할 적절한 k 값을 결정하기 위함이다.

- **Sparse Table 구축**

  - 각 구간 길이(2^k)에 대한 최솟값과 최댓값을 테이블에 저장한다.
  - 이를 위해 동적으로 프로그래밍하여 작은 구간부터 큰 구간까지의 값을 계산한다.

- **쿼리 처리**

  - 각 쿼리에 대해, 구간의 길이에 따른 k 값을 이용하여 두 개의 부분 구간의 최솟값과 최댓값을 비교하여 결과를 얻는다.
  - 이는 O(1)에 처리된다.

## C++ 코드와 설명

```cpp
#include <cstdio>
#include <algorithm>
using namespace std;

const int MAXN = 100000; // 수열의 최대 크기
const int MAXK = 17;     // log2(100,000) ≈ 17

int N, M;
int A[MAXN];                      // 수열을 저장할 배열
int log2[MAXN + 1];               // 로그 값을 저장할 배열
int minTable[MAXN][MAXK + 1];     // 최솟값을 저장할 Sparse Table
int maxTable[MAXN][MAXK + 1];     // 최댓값을 저장할 Sparse Table

int main() {
    scanf("%d %d", &N, &M);       // 수열의 크기 N과 쿼리의 개수 M 입력
    for(int i = 0; i < N; ++i) {
        scanf("%d", &A[i]);       // 수열 입력
    }

    // 로그 값 미리 계산
    log2[1] = 0;
    for(int i = 2; i <= N; ++i) {
        log2[i] = log2[i / 2] + 1;
    }

    // Sparse Table 초기화 (구간 길이 1인 경우)
    for(int i = 0; i < N; ++i) {
        minTable[i][0] = A[i];
        maxTable[i][0] = A[i];
    }

    // Sparse Table 구축
    for(int k = 1; (1 << k) <= N; ++k) {
        for(int i = 0; i + (1 << k) <= N; ++i) {
            minTable[i][k] = min(minTable[i][k - 1], minTable[i + (1 << (k - 1))][k - 1]);
            maxTable[i][k] = max(maxTable[i][k - 1], maxTable[i + (1 << (k - 1))][k - 1]);
        }
    }

    // 쿼리 처리
    for(int q = 0; q < M; ++q) {
        int a, b;
        scanf("%d %d", &a, &b);
        --a; --b; // 인덱스를 0부터 시작하도록 조정
        int length = b - a + 1;
        int k = log2[length]; // 구간의 길이에 따른 k 값
        // 두 부분 구간의 최솟값과 최댓값 비교
        int minVal = min(minTable[a][k], minTable[b - (1 << k) + 1][k]);
        int maxVal = max(maxTable[a][k], maxTable[b - (1 << k) + 1][k]);
        printf("%d %d\n", minVal, maxVal);
    }

    return 0;
}
```

**코드 설명:**

- **입력 및 초기화**

  - 수열의 크기 `N`과 쿼리의 개수 `M`을 입력받는다.
  - 수열 `A`를 입력받아 배열에 저장한다.

- **로그 값 계산**

  - `log2` 배열을 통해 1부터 N까지의 로그 값을 미리 계산한다.
  - 이는 구간의 길이에 따른 적절한 k 값을 빠르게 찾기 위함이다.

- **Sparse Table 구축**

  - 구간 길이 1인 경우 (`k = 0`), 각 위치의 값 자체가 최솟값이자 최댓값이다.
  - 구간 길이가 2^k인 경우, 이전 단계의 결과를 이용하여 현재 구간의 최솟값과 최댓값을 계산한다.

- **쿼리 처리**

  - 각 쿼리에 대해 구간의 길이를 계산하고, 그에 따른 k 값을 찾는다.
  - 해당 구간을 두 부분으로 나누어 각 부분의 최솟값과 최댓값을 비교하여 결과를 얻는다.
  - 인덱스 조정을 위해 입력받은 a, b에서 1을 뺀다.

- **시간 복잡도**

  - 전처리: O(N log N)
  - 각 쿼리: O(1)
  - 전체 시간 복잡도: O(N log N + M)

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

#define MAXN 100000
#define MAXK 17 // log2(100,000) ≈ 17

int N, M;
int A[MAXN];
int log2[MAXN + 1];
int minTable[MAXN][MAXK + 1];
int maxTable[MAXN][MAXK + 1];

int min(int a, int b) { return a < b ? a : b; }
int max(int a, int b) { return a > b ? a : b; }

int main() {
    scanf("%d %d", &N, &M);
    for(int i = 0; i < N; ++i) {
        scanf("%d", &A[i]);
    }

    // 로그 값 미리 계산
    log2[1] = 0;
    for(int i = 2; i <= N; ++i) {
        log2[i] = log2[i / 2] + 1;
    }

    // Sparse Table 초기화
    for(int i = 0; i < N; ++i) {
        minTable[i][0] = A[i];
        maxTable[i][0] = A[i];
    }

    // Sparse Table 구축
    for(int k = 1; (1 << k) <= N; ++k) {
        for(int i = 0; i + (1 << k) <= N; ++i) {
            minTable[i][k] = min(minTable[i][k - 1], minTable[i + (1 << (k - 1))][k - 1]);
            maxTable[i][k] = max(maxTable[i][k - 1], maxTable[i + (1 << (k - 1))][k - 1]);
        }
    }

    // 쿼리 처리
    for(int q = 0; q < M; ++q) {
        int a, b;
        scanf("%d %d", &a, &b);
        --a; --b;
        int length = b - a + 1;
        int k = log2[length];
        int minVal = min(minTable[a][k], minTable[b - (1 << k) + 1][k]);
        int maxVal = max(maxTable[a][k], maxTable[b - (1 << k) + 1][k]);
        printf("%d %d\n", minVal, maxVal);
    }

    return 0;
}
```

**코드 설명:**

- **사용된 헤더**

  - `<stdio.h>`만 사용하여 표준 입출력을 처리한다.

- **사용자 정의 함수**

  - `min`과 `max` 함수를 직접 정의하여 `algorithm` 헤더 없이 최소값과 최대값을 계산한다.

- **기타 사항**

  - 나머지 코드는 앞서 설명한 코드와 동일하며, 표준 라이브러리를 사용하지 않고 구현되었다.

## Python 코드와 설명

```python
import sys
import math

input = sys.stdin.readline

N, M = map(int, input().split())
A = [int(input()) for _ in range(N)]

log2 = [0] * (N + 1)
for i in range(2, N + 1):
    log2[i] = log2[i // 2] + 1

K = log2[N] + 1
minTable = [[0] * K for _ in range(N)]
maxTable = [[0] * K for _ in range(N)]

for i in range(N):
    minTable[i][0] = A[i]
    maxTable[i][0] = A[i]

for k in range(1, K):
    for i in range(N - (1 << k) + 1):
        minTable[i][k] = min(minTable[i][k - 1], minTable[i + (1 << (k - 1))][k - 1])
        maxTable[i][k] = max(maxTable[i][k - 1], maxTable[i + (1 << (k - 1))][k - 1])

for _ in range(M):
    a, b = map(int, input().split())
    a -= 1; b -= 1
    length = b - a + 1
    k = log2[length]
    minVal = min(minTable[a][k], minTable[b - (1 << k) + 1][k])
    maxVal = max(maxTable[a][k], maxTable[b - (1 << k) + 1][k])
    print(f"{minVal} {maxVal}")
```

**코드 설명:**

- **입력 및 초기화**

  - `sys.stdin.readline()`을 사용하여 입력을 빠르게 처리한다.
  - 수열 `A`를 입력받는다.

- **로그 값 계산**

  - `log2` 리스트에 1부터 N까지의 로그 값을 미리 계산한다.

- **Sparse Table 구축**

  - `minTable`과 `maxTable`을 2차원 리스트로 생성한다.
  - 구간 길이 2^k에 대한 최솟값과 최댓값을 계산하여 저장한다.

- **쿼리 처리**

  - 각 쿼리에 대해 구간의 길이에 따른 k 값을 계산한다.
  - 두 부분 구간의 최솟값과 최댓값을 비교하여 결과를 출력한다.

- **최적화**

  - Python에서는 재귀 호출보다 반복문이 빠르므로 반복문을 사용한다.
  - 입력을 빠르게 처리하기 위해 `sys.stdin.readline()`을 사용한다.

## 결론

이번 포스팅에서는 Sparse Table을 활용하여 구간의 최솟값과 최댓값을 효율적으로 구하는 방법을 알아보았다. 수열의 값이 변경되지 않는 상황에서 Sparse Table은 매우 효과적인 자료 구조이며, 전처리에 ```O(N log N)```의 시간이 들지만 쿼리를 ```O(1)```에 처리할 수 있다는 장점이 있다.

또한, 코드 구현 시 라이브러리 사용 여부에 따라 코드의 길이와 복잡도가 어떻게 변하는지도 살펴보았다. 라이브러리를 사용하지 않고도 효율적인 알고리즘을 구현할 수 있으나, 표준 라이브러리를 적절히 활용하면 코드의 가독성과 생산성이 향상된다는 것을 알 수 있었다.

앞으로도 다양한 문제에서 적합한 알고리즘과 자료 구조를 선택하여 효율적인 코드를 작성하도록 노력해야겠다.