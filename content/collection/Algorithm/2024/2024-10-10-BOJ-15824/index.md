---
image: "tmp_wordcloud.png"
description: "이 문제는 주어진 모든 음식 조합에서 최대값과 최소값의 차이, 즉 '주헌고통지수'의 총합을 빠르고 효율적으로 구하는 수학적(조합론적) 접근을 다룬다. N이 매우 클 때도 가능한 알고리즘을 설명한다."
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Mathematics
- Sorting
- Combinatorics
- ExponentiationBySquaring
- ModuloArithmetic
- O(NlogN)
title: '[Algorithm] C++/Python 백준 15824번 : 너 봄에는 캡사이신이 맛있단다'
---

매운맛을 즐기는 주헌이가 새로운 음식점의 모든 매운맛 조합을 시도하면서 느끼는 고통지수의 합을 구하는 문제이다. 이 문제는 큰 수의 조합과 차이를 다루므로 효율적인 알고리즘이 필요하다.

문제 : [https://www.acmicpc.net/problem/15824](https://www.acmicpc.net/problem/15824)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

주헌이는 매운맛을 좋아하는 사람으로, 음식의 스코빌 지수를 통해 매운맛을 느낀다. 스코빌 지수는 고추류가 가진 매운맛의 원인인 캡사이신의 농도를 수치화한 단위이다. 주헌이가 느끼는 매운 정도는 음식의 절대적인 매운맛이 아니라 메뉴들 간의 상대적인 매운맛 차이에 기반한다.

예를 들어, 스코빌 지수가 `[5, 2, 8]`인 음식들을 먹을 때, 주헌이가 느끼는 매운 정도는 가장 높은 수치인 `8`과 가장 낮은 수치인 `2`의 차이인 `6`이다. 이러한 방식으로 메뉴들의 스코빌 지수가 주어졌을 때, 그 최댓값과 최솟값의 차이를 "주헌고통지수"라고 정의한다.

주헌이는 새로 생긴 매운맛 전문점의 모든 음식 조합을 먹어보려 한다. 이때, 각 조합에서의 주헌고통지수를 모두 합한 값을 구하고자 한다. 단, 같은 조합은 다시 먹지 않으며, 결과는 매우 커질 수 있으므로 `1,000,000,007`로 나눈 나머지를 출력해야 한다.

**입력**

- 첫 줄에 메뉴의 총 개수 `N`이 주어진다. (1 ≤ N ≤ 300,000)
- 두 번째 줄에는 `N`개의 메뉴의 스코빌 지수가 주어진다. 각 스코빌 지수는 `0` 이상 `2^{31} - 1` 이하의 정수이다.

**출력**

- 한 줄에 모든 조합의 주헌고통지수 합을 `1,000,000,007`로 나눈 나머지를 출력한다.

## 접근 방식

이 문제는 모든 부분 집합에 대해 최댓값과 최솟값의 차이의 합을 구해야 한다. 하지만 `N`이 최대 `300,000`이므로 모든 부분 집합을 직접 계산하는 것은 불가능하다. 따라서 효율적인 수학적 접근이 필요하다.

1. **정렬**: 스코빌 지수 배열을 오름차순으로 정렬한다. 이를 통해 원소들의 순서를 확정짓고 계산을 용이하게 한다.

2. **각 원소의 기여도 계산**:
   - 각 원소가 부분 집합의 **최댓값**이 되는 경우의 수와 **최솟값**이 되는 경우의 수를 계산한다.
   - 정렬된 배열에서 `i`번째 원소가 **최댓값**이 되는 부분 집합의 수는 `2^i`이다.
   - **최솟값**이 되는 부분 집합의 수는 `2^{N - i - 1}`이다.

3. **총 합 계산**:
   - 각 원소에 대해 `(최댓값으로서의 기여도 - 최솟값으로서의 기여도) * 원소의 값`을 계산하여 모두 더한다.
   - 이때, 결과값이 음수가 될 수 있으므로 모듈러 연산을 적절히 사용한다.

4. **거듭제곱 계산 최적화**:
   - 거듭제곱 계산에서 지수가 커질 수 있으므로 미리 `2^i` 값을 배열에 저장하여 사용한다.
   - 모듈러 연산의 특성을 이용하여 계산 중간에 나머지 연산을 적용한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define MOD 1000000007
typedef long long ll;
using namespace std;

int main() {
    ios::sync_with_stdio(false); // 입출력 속도 향상
    cin.tie(NULL);

    int N;
    cin >> N;
    vector<ll> A(N);
    for(int i = 0; i < N; ++i)
        cin >> A[i]; // 스코빌 지수 입력

    sort(A.begin(), A.end()); // 오름차순 정렬

    vector<ll> pow2(N);
    pow2[0] = 1;
    for(int i = 1; i < N; ++i)
        pow2[i] = (pow2[i - 1] * 2) % MOD; // 2의 거듭제곱 미리 계산

    ll total_sum = 0;
    for(int i = 0; i < N; ++i) {
        ll max_count = pow2[i]; // A[i]가 최대값이 되는 부분 집합 수
        ll min_count = pow2[N - i - 1]; // A[i]가 최소값이 되는 부분 집합 수
        ll contribution = (max_count - min_count + MOD) % MOD; // 기여도 계산
        total_sum = (total_sum + A[i] * contribution) % MOD; // 총 합에 더하기
    }

    cout << total_sum << "\n"; // 결과 출력
    return 0;
}
```

**코드 설명**

- `ios::sync_with_stdio(false);`와 `cin.tie(NULL);`를 사용하여 입출력 속도를 향상시킨다.
- 스코빌 지수를 입력받아 `A`에 저장하고 오름차순으로 정렬한다.
- `pow2` 배열을 생성하여 `2^i` 값을 미리 계산하고 모듈러 연산을 적용한다.
  - `pow2[i]`는 `2^i mod MOD`를 저장한다.
- 각 원소에 대해 최대값으로서의 기여도와 최소값으로서의 기여도를 계산하고, 이를 이용하여 총 합을 구한다.
  - `max_count`는 `A[i]`가 부분 집합의 최대값이 되는 경우의 수이다.
  - `min_count`는 `A[i]`가 부분 집합의 최소값이 되는 경우의 수이다.
  - `contribution`은 `A[i]`의 전체 기여도를 나타낸다.
  - 음수 결과를 방지하기 위해 `MOD`를 더하고 모듈러 연산을 적용한다.
- 최종 결과를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007
typedef long long ll;

int compare(const void* a, const void* b) {
    ll num1 = *(ll*)a;
    ll num2 = *(ll*)b;
    if(num1 > num2) return 1;
    else if(num1 < num2) return -1;
    else return 0;
}

int main() {
    int N;
    scanf("%d", &N);
    ll* A = (ll*)malloc(N * sizeof(ll));
    for(int i = 0; i < N; ++i)
        scanf("%lld", &A[i]); // 스코빌 지수 입력

    qsort(A, N, sizeof(ll), compare); // 오름차순 정렬

    ll* pow2 = (ll*)malloc(N * sizeof(ll));
    pow2[0] = 1;
    for(int i = 1; i < N; ++i)
        pow2[i] = (pow2[i - 1] * 2) % MOD; // 2의 거듭제곱 미리 계산

    ll total_sum = 0;
    for(int i = 0; i < N; ++i) {
        ll max_count = pow2[i]; // A[i]가 최대값이 되는 부분 집합 수
        ll min_count = pow2[N - i - 1]; // A[i]가 최소값이 되는 부분 집합 수
        ll contribution = (max_count - min_count + MOD) % MOD; // 기여도 계산
        total_sum = (total_sum + A[i] % MOD * contribution % MOD) % MOD; // 총 합에 더하기
    }

    printf("%lld\n", total_sum); // 결과 출력

    free(A);
    free(pow2);
    return 0;
}
```

**코드 설명**

- 표준 라이브러리 함수만을 사용하여 구현한다.
- `qsort` 함수를 이용하여 배열 `A`를 오름차순으로 정렬한다.
  - `compare` 함수는 `qsort`를 위한 비교 함수이다.
- `pow2` 배열을 동적 할당하여 `2^i mod MOD` 값을 계산한다.
- 각 원소에 대해 최대값과 최소값으로서의 기여도를 계산하고 총 합을 구한다.
  - 모듈러 연산을 중간중간 적용하여 오버플로우를 방지한다.
- 메모리 누수를 방지하기 위해 `free` 함수를 사용하여 동적 할당된 메모리를 해제한다.

## Python 코드와 설명

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

N = int(input())
A = list(map(int, input().split()))
A.sort()  # 오름차순 정렬

pow2 = [1] * N
for i in range(1, N):
    pow2[i] = (pow2[i - 1] * 2) % MOD  # 2의 거듭제곱 계산

total_sum = 0
for i in range(N):
    max_count = pow2[i]  # A[i]가 최대값이 되는 부분 집합 수
    min_count = pow2[N - i - 1]  # A[i]가 최소값이 되는 부분 집합 수
    contribution = (max_count - min_count) % MOD  # 기여도 계산
    total_sum = (total_sum + A[i] * contribution) % MOD  # 총 합에 더하기

print(total_sum)
```

**코드 설명**

- `sys.stdin.readline`을 사용하여 입력 속도를 향상시킨다.
- 스코빌 지수를 입력받아 리스트 `A`에 저장하고 오름차순으로 정렬한다.
- `pow2` 리스트를 생성하여 `2^i mod MOD` 값을 계산한다.
- 각 원소에 대해 최대값과 최소값으로서의 기여도를 계산하고 총 합을 구한다.
  - `contribution`은 각 원소의 전체 기여도를 나타낸다.
- 모듈러 연산을 적용하여 결과를 출력한다.

## 결론

이 문제는 모든 부분 집합에 대해 최댓값과 최솟값의 차이를 합산해야 하므로 효율적인 수학적 접근이 필요했다. 정렬과 거듭제곱의 특성을 이용하여 각 원소의 기여도를 계산함으로써 시간 복잡도를 `O(N log N)`으로 최적화할 수 있었다.

추가적인 최적화 방안으로는 모듈러 연산의 특성을 더욱 활용하여 계산량을 줄이는 방법이 있다. 또한, 메모리 사용을 최소화하기 위해 배열 대신 변수 하나로 거듭제곱을 계산하는 방법도 고려할 수 있다.

이번 문제를 통해 큰 수의 조합과 모듈러 연산을 다루는 방법을 복습할 수 있었으며, 효율적인 알고리즘 설계의 중요성을 다시 한 번 깨닫게 되었다.