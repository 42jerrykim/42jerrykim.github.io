---
image: "tmp_wordcloud.png"
description: "백준 16565번 N포커 문제는 52장의 카드 중 N장을 뽑았을 때 적어도 하나의 포카드가 포함되는 경우의 수를 구하는 조합론/포함-배제 알고리즘 문제입니다. 문제에서 요구하는 조건에 따라 수학적 사고와 원리 응용 능력이 중요합니다."
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Combinatorics
- Inclusion-Exclusion Principle
- Mathematics
- ModularArithmetic
title: '[Algorithm] C++/Python 백준 16565번 : N포커'
---

트럼프 카드로 새로운 게임을 만들기로 한 정연이의 이야기로 시작해보자. 이 게임은 딜러와 플레이어가 1:1로 플레이하며, 플레이어는 52장의 트럼프 카드 중 N장을 뽑는다. 만약 뽑은 카드들로 "포카드(four of a kind)" 족보를 만들 수 있다면 플레이어의 승리, 그렇지 않다면 딜러의 승리로 게임이 끝난다. 여기서 포카드는 같은 숫자의 카드 4장을 의미한다.

정연이는 공정한 게임을 위해 N의 값을 결정하고자 한다. 이를 위해 N장의 카드를 뽑았을 때 플레이어가 이길 수 있는 경우의 수를 구하려고 한다. 우리의 목표는 N이 주어졌을 때, 플레이어가 이기는 경우의 수를 10,007로 나눈 나머지를 구하는 것이다.

문제 : [https://www.acmicpc.net/problem/16565](https://www.acmicpc.net/problem/16565)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

52장의 트럼프 카드는 각 4개의 문양(♥, ♠, ◆, ♣)과 13개의 숫자(A, 2, 3, ..., 10, J, Q, K)로 구성되어 있다.

플레이어는 N장의 카드를 뽑는다. 뽑은 카드들 중에서 같은 숫자의 카드 4장이 존재하면 이를 "포카드(four of a kind)"라고 하며, 이 경우 플레이어가 승리한다.

정연이는 N장의 카드를 뽑았을 때 플레이어가 이기는 경우의 수를 알고 싶어한다. 즉, N장의 카드에 하나 이상의 포카드가 포함되어 있는 경우의 수를 구하는 것이다.

단, 결과를 10,007로 나눈 나머지를 출력해야 한다.

## 접근 방식

이 문제는 **조합론**과 **포함 배제의 원리**를 활용하여 풀 수 있다.

먼저, 전체 경우의 수는 52장에서 N장을 뽑는 경우의 수이다.

플레이어가 이기는 경우는 N장의 카드 중에서 적어도 하나의 포카드가 존재하는 경우이다. 여기서 중요한 점은 여러 개의 포카드가 존재할 수도 있다는 것이다.

따라서, 각 숫자에 대해 포카드를 만들 수 있는 경우를 고려하고, 포함 배제의 원리를 사용하여 중복을 제거하면서 총 경우의 수를 계산한다.

포함 배제의 원리를 적용하면 다음과 같다:

- \( S_r \): 숫자 \( r \)에 대한 포카드를 포함하는 경우의 수
- 우리가 구하고자 하는 것은 \( |S_1 \cup S_2 \cup \dots \cup S_{13}| \) 이다.

포함 배제의 공식은 다음과 같다:

\[
|\bigcup_{i=1}^{n} S_i| = \sum_{k=1}^{n} (-1)^{k+1} \left( \sum_{1 \leq i_1 < i_2 < \dots < i_k \leq n} |S_{i_1} \cap S_{i_2} \cap \dots \cap S_{i_k}| \right)
\]

이를 적용하여 계산하면:

\[
\text{결과} = \sum_{k=1}^{13} (-1)^{k+1} \binom{13}{k} \binom{52 - 4k}{N - 4k}
\]

여기서:

- \(\binom{13}{k}\): 포카드를 만들 숫자 \( k \)개 선택
- \(\binom{52 - 4k}{N - 4k}\): 선택한 포카드들을 제외한 나머지 카드 중에서 \( N - 4k \)개 선택

주의할 점은 \( N \geq 4k \)이어야 하며, \( N - 4k \leq 52 - 4k \)이어야 한다.
## C++ 코드와 설명

```cpp
#include <iostream>
using namespace std;

const int MOD = 10007;
const int MAXN = 52;

int factorial[MAXN + 1];
int inv_factorial[MAXN + 1];

// 모듈러 거듭제곱 함수: x^y mod MOD 계산
int mod_pow(int x, int y) {
    int result = 1;
    x %= MOD;
    while(y > 0) {
        if(y % 2 == 1)
            result = result * x % MOD;
        x = x * x % MOD;
        y /= 2;
    }
    return result;
}

// 모듈러 역원 계산: n^(-1) mod MOD
int mod_inv(int n) {
    return mod_pow(n, MOD - 2);
}

// 이항 계수 계산: nCr mod MOD
int nCr(int n, int r) {
    if(r < 0 || r > n) return 0;
    return factorial[n] * inv_factorial[r] % MOD * inv_factorial[n - r] % MOD;
}

int main() {
    int N;
    cin >> N;

    // 팩토리얼과 역팩토리얼 미리 계산
    factorial[0] = 1;
    for(int i = 1; i <= MAXN; ++i)
        factorial[i] = factorial[i - 1] * i % MOD;

    inv_factorial[MAXN] = mod_inv(factorial[MAXN]);
    for(int i = MAXN - 1; i >= 0; --i)
        inv_factorial[i] = inv_factorial[i + 1] * (i + 1) % MOD;

    int result = 0;
    int maxK = N / 4;
    if(maxK > 13) maxK = 13; // 최대 13개의 숫자만 존재

    for(int k = 1; k <= maxK; ++k) {
        int sign = (k % 2 == 1) ? 1 : -1; // 포함 배제의 부호 결정
        int comb1 = nCr(13, k); // 포카드로 사용할 숫자 k개 선택
        int remaining_cards = 52 - 4 * k; // 남은 카드 수
        int remaining_draws = N - 4 * k; // 남은 뽑아야 할 카드 수

        if(remaining_draws < 0 || remaining_draws > remaining_cards) continue;

        int comb2 = nCr(remaining_cards, remaining_draws); // 남은 카드에서 선택
        int term = sign * comb1 % MOD * comb2 % MOD;
        if(term < 0) term += MOD; // 음수 처리

        result = (result + term) % MOD;
    }

    cout << result << endl;
    return 0;
}
```

**코드 설명**

- **팩토리얼 및 역팩토리얼 계산**: 이항 계수를 빠르게 계산하기 위해 미리 팩토리얼과 모듈러 역원을 계산한다.
- **mod_pow 함수**: 거듭제곱을 빠르게 계산하기 위한 함수로, 모듈러 역원을 구할 때 사용된다.
- **포함 배제 계산**: $ k $개의 포카드를 선택하는 경우에 대해 포함 배제를 적용하여 총 경우의 수를 계산한다.
- **음수 처리**: 모듈러 연산에서 음수가 나올 수 있으므로, 이를 양수로 변환한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

#define MOD 10007
#define MAXN 52

int factorial[MAXN + 1];
int inv_factorial[MAXN + 1];

// 모듈러 거듭제곱 함수: x^y mod MOD 계산
int mod_pow(int x, int y) {
    int result = 1;
    x %= MOD;
    while(y > 0) {
        if(y % 2 == 1)
            result = result * x % MOD;
        x = x * x % MOD;
        y /= 2;
    }
    return result;
}

// 모듈러 역원 계산: n^(-1) mod MOD
int mod_inv(int n) {
    return mod_pow(n, MOD - 2);
}

// 이항 계수 계산: nCr mod MOD
int nCr(int n, int r) {
    if(r < 0 || r > n) return 0;
    return factorial[n] * inv_factorial[r] % MOD * inv_factorial[n - r] % MOD;
}

int main() {
    int N;
    scanf("%d", &N);

    // 팩토리얼과 역팩토리얼 미리 계산
    factorial[0] = 1;
    for(int i = 1; i <= MAXN; ++i)
        factorial[i] = factorial[i - 1] * i % MOD;

    inv_factorial[MAXN] = mod_inv(factorial[MAXN]);
    for(int i = MAXN - 1; i >= 0; --i)
        inv_factorial[i] = inv_factorial[i + 1] * (i + 1) % MOD;

    int result = 0;
    int maxK = N / 4;
    if(maxK > 13) maxK = 13; // 최대 13개의 숫자만 존재

    for(int k = 1; k <= maxK; ++k) {
        int sign = (k % 2 == 1) ? 1 : -1; // 포함 배제의 부호 결정
        int comb1 = nCr(13, k); // 포카드로 사용할 숫자 k개 선택
        int remaining_cards = 52 - 4 * k; // 남은 카드 수
        int remaining_draws = N - 4 * k; // 남은 뽑아야 할 카드 수

        if(remaining_draws < 0 || remaining_draws > remaining_cards) continue;

        int comb2 = nCr(remaining_cards, remaining_draws); // 남은 카드에서 선택
        int term = ((sign * comb1) % MOD * comb2) % MOD;
        if(term < 0) term += MOD; // 음수 처리

        result = (result + term) % MOD;
    }

    printf("%d\n", result);
    return 0;
}
```

**코드 설명**

- **`stdio.h` 사용**: 표준 입출력을 위해 `stdio.h`만 사용하였다.
- **나머지 부분은 이전 코드와 동일**: C++의 기능을 최소화하고 C 스타일로 작성하였다.
- **모든 변수와 함수는 C 스타일로 선언**: `cout`, `cin` 대신 `printf`, `scanf` 사용.

## Python 코드와 설명

```python
MOD = 10007
MAXN = 52

factorial = [1] * (MAXN + 1)
inv_factorial = [1] * (MAXN + 1)

# 모듈러 거듭제곱 함수
def mod_pow(x, y):
    result = 1
    x %= MOD
    while y > 0:
        if y % 2 == 1:
            result = result * x % MOD
        x = x * x % MOD
        y //= 2
    return result

# 모듈러 역원 계산
def mod_inv(n):
    return mod_pow(n, MOD - 2)

# 이항 계수 계산
def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return factorial[n] * inv_factorial[r] % MOD * inv_factorial[n - r] % MOD

N = int(input())

# 팩토리얼과 역팩토리얼 미리 계산
for i in range(1, MAXN + 1):
    factorial[i] = factorial[i - 1] * i % MOD

inv_factorial[MAXN] = mod_inv(factorial[MAXN])
for i in range(MAXN - 1, -1, -1):
    inv_factorial[i] = inv_factorial[i + 1] * (i + 1) % MOD

result = 0
maxK = N // 4
if maxK > 13:
    maxK = 13

for k in range(1, maxK + 1):
    sign = 1 if k % 2 == 1 else -1  # 포함 배제의 부호 결정
    comb1 = nCr(13, k)  # 포카드로 사용할 숫자 k개 선택
    remaining_cards = 52 - 4 * k  # 남은 카드 수
    remaining_draws = N - 4 * k  # 남은 뽑아야 할 카드 수

    if remaining_draws < 0 or remaining_draws > remaining_cards:
        continue

    comb2 = nCr(remaining_cards, remaining_draws)  # 남은 카드에서 선택
    term = sign * comb1 % MOD * comb2 % MOD
    result = (result + term) % MOD

print(result)
```

**코드 설명**

- **팩토리얼 및 역팩토리얼 계산**: 리스트를 이용하여 미리 계산한다.
- **`mod_pow` 함수**: 빠른 거듭제곱을 위해 반복문을 사용한다.
- **포함 배제 원리 적용**: C++ 코드와 동일한 로직을 Python으로 구현하였다.
- **음수 처리 필요 없음**: Python의 모듈러 연산은 음수를 자동으로 양수로 변환한다.

## 결론

이 문제는 포함 배제의 원리를 이용한 조합론 문제로, 정확한 경우의 수 계산이 핵심이다. 모듈러 연산을 처리하기 위해 빠른 거듭제곱과 모듈러 역원을 사용하였다. 이를 통해 시간 복잡도를 효율적으로 관리할 수 있었다. 추가로, 이항 계수를 미리 계산하여 계산 시간을 단축하였다.

이번 문제를 통해 조합론과 포함 배제의 원리를 복습할 수 있었으며, 모듈러 연산에서의 주의점도 다시 한번 상기할 수 있었다. 앞으로도 다양한 문제에 이러한 수학적 아이디어를 적용해보고자 한다.