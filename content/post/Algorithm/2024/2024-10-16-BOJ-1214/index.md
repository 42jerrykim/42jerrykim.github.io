---
title: "[Algorithm] C++/Python 백준 1214번 : 쿨한 물건 구매"
categories: Algorithm
tags:
- NumberTheory
- Mathematics
- BruteForce
- Greedy
- Optimization
- Time Complexity: O(√N)
date: 2024-01-01
image: "tmp_wordcloud.png"
---

# 도입글

이번 포스팅에서는 백준 온라인 저지의 **1214번 문제 쿨한 물건 구매**를 다루어 보겠습니다. 이 문제는 제한된 종류의 지폐를 사용하여 특정 금액 이상의 최소 지불 금액을 구하는 문제로, 효율적인 알고리즘 설계와 수학적 사고가 필요한 흥미로운 문제입니다.

문제를 해결하면서 **최적화 기법**과 **수학적 아이디어**를 활용하여 시간 복잡도를 줄이는 방법에 대해 알아보겠습니다.

## 문제 : [https://www.acmicpc.net/problem/1214](https://www.acmicpc.net/problem/1214)

## 문제 설명

구사과는 지폐를 오직 두 종류만 가지고 있습니다. 바로 **P원 지폐**와 **Q원 지폐**입니다. 이 두 종류의 지폐를 구사과는 **무한히 많이** 가지고 있습니다.

오늘 구사과가 구매하려고 하는 물건의 가격은 **D원**입니다. 구사과가 이 물건을 구매하기 위해서 지불해야 하는 금액의 **최솟값**은 얼마일까요?

물건을 구매하기 위해서는 **물건의 가격보다 크거나 같은 금액**을 지불해야 합니다.

즉, 구사과는 P원 지폐와 Q원 지폐를 조합하여 D원 이상이 되는 최소의 금액을 만들어야 합니다. 이때, 각 지폐의 개수는 제한이 없으므로, 가능한 모든 조합 중에서 지불해야 하는 금액의 최솟값을 구하는 것이 문제의 목표입니다.

**입력**

첫째 줄에 **D**, **P**, **Q**가 주어집니다. 모두 \(10^9\)보다 작거나 같은 자연수입니다.

**출력**

첫째 줄에 물건을 구매하기 위해 구사과가 지불해야 하는 금액의 **최솟값**을 출력합니다.

**예제 입력 1**

```
17 7 13
```

**예제 출력 1**

```
20
```

20 = 7 × 1 + 13 × 1

**예제 입력 2**

```
21 7 13
```

**예제 출력 2**

```
21
```

21 = 7 × 3 + 13 × 0

**예제 입력 3**

```
17 7 9
```

**예제 출력 3**

```
18
```

18 = 7 × 0 + 9 × 2

**예제 입력 4**

```
37 9 17
```

**예제 출력 4**

```
43
```

43 = 9 × 1 + 17 × 2

## 접근 방식

이 문제는 두 종류의 지폐를 사용하여 원하는 금액 **D** 이상을 만들 수 있는 최소 금액을 찾는 문제입니다. 하지만 **D**, **P**, **Q**의 범위가 최대 \(10^9\)이기 때문에 모든 가능한 지폐 조합을 탐색하는 것은 **시간 초과**의 원인이 됩니다.

### 주요 아이디어

1. **반복 횟수 제한**

   지폐의 사용 횟수를 **D를 Q로 나눈 몫 근처**로 제한하여, 탐색 범위를 좁힙니다. 최적의 조합은 이 근처에서 발생할 가능성이 높기 때문입니다.

2. **두 지폐의 역할을 바꾸어 탐색**

   P와 Q의 역할을 바꾸어 두 번의 탐색을 수행하여 모든 경우의 수를 고려합니다.

3. **조기 종료 조건**

   현재 계산된 금액이 이미 최소 금액보다 크거나 같다면 더 이상의 탐색을 중단하여 불필요한 계산을 줄입니다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <algorithm>

using namespace std;

typedef long long ll;

void check(ll D, ll P, ll Q, ll &ans) {
    ll y_start = max(0LL, D / Q - 1000000); // y의 시작 범위 설정
    ll y_end = D / Q + 1000000; // y의 끝 범위 설정

    for (ll y = y_start; y <= y_end; ++y) {
        ll total_Q = y * Q;
        if (total_Q >= ans) break; // 현재 최소 금액보다 크면 종료
        if (total_Q >= D) {
            ans = min(ans, total_Q); // 최소 금액 갱신
            break;
        }
        ll rem = D - total_Q;
        ll x = (rem + P - 1) / P; // 필요한 P 지폐의 개수
        ll total_amount = total_Q + x * P;
        if (total_amount >= ans) continue;
        ans = total_amount; // 최소 금액 갱신
    }
}

int main() {
    ll D, P, Q;
    cin >> D >> P >> Q;

    ll ans = ((D + P - 1) / P) * P; // P만 사용했을 때의 최소 금액

    check(D, P, Q, ans); // 첫 번째 조합 탐색
    check(D, Q, P, ans); // 지폐를 바꿔서 두 번째 조합 탐색

    cout << ans << endl;

    return 0;
}
```

### 코드의 동작 단계별 설명

1. **함수 `check` 정의**

   - `D`: 물건의 가격
   - `P`, `Q`: 두 종류의 지폐
   - `ans`: 현재까지의 최소 지불 금액

   ```cpp
   void check(ll D, ll P, ll Q, ll &ans)
   ```

2. **반복 범위 설정**

   ```cpp
   ll y_start = max(0LL, D / Q - 1000000);
   ll y_end = D / Q + 1000000;
   ```

   - `y_start`: `D / Q - 1,000,000` (0 이상)
   - `y_end`: `D / Q + 1,000,000`

3. **메인 루프**

   ```cpp
   for (ll y = y_start; y <= y_end; ++y) {
       ll total_Q = y * Q;
       if (total_Q >= ans) break;
       if (total_Q >= D) {
           ans = min(ans, total_Q);
           break;
       }
       ll rem = D - total_Q;
       ll x = (rem + P - 1) / P;
       ll total_amount = total_Q + x * P;
       if (total_amount >= ans) continue;
       ans = total_amount;
   }
   ```

   - `total_Q`: Q 지폐로 지불한 금액
   - `rem`: 남은 금액
   - `x`: 필요한 P 지폐의 개수
   - `total_amount`: 총 지불 금액

4. **메인 함수에서의 호출**

   ```cpp
   check(D, P, Q, ans);
   check(D, Q, P, ans);
   ```

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

typedef long long ll;

void check(ll D, ll P, ll Q, ll *ans) {
    ll y_start = D / Q - 1000000;
    if (y_start < 0) y_start = 0;
    ll y_end = D / Q + 1000000;

    for (ll y = y_start; y <= y_end; ++y) {
        ll total_Q = y * Q;
        if (total_Q >= *ans) break;
        if (total_Q >= D) {
            if (total_Q < *ans) *ans = total_Q;
            break;
        }
        ll rem = D - total_Q;
        ll x = (rem + P - 1) / P;
        ll total_amount = total_Q + x * P;
        if (total_amount >= *ans) continue;
        *ans = total_amount;
    }
}

int main() {
    ll D, P, Q;
    scanf("%lld %lld %lld", &D, &P, &Q);

    ll ans = ((D + P - 1) / P) * P;

    check(D, P, Q, &ans);
    check(D, Q, P, &ans);

    printf("%lld\n", ans);

    return 0;
}
```

### 코드의 동작 단계별 설명

- **입력 처리**

  ```cpp
  scanf("%lld %lld %lld", &D, &P, &Q);
  ```

- **초기 최소 금액 설정**

  ```cpp
  ll ans = ((D + P - 1) / P) * P;
  ```

- **함수 호출 및 최소 금액 갱신**

  ```cpp
  check(D, P, Q, &ans);
  check(D, Q, P, &ans);
  ```

- **함수 `check` 내부 동작**

  - `y_start`와 `y_end`를 설정하여 반복 범위를 제한
  - 조기 종료 조건을 활용하여 불필요한 계산을 줄임

- **결과 출력**

  ```cpp
  printf("%lld\n", ans);
  ```

## Python 코드와 설명

```python
import sys

def check(D, P, Q, ans):
    y_start = max(0, D // Q - 1000000)
    y_end = D // Q + 1000000

    for y in range(y_start, y_end + 1):
        total_Q = y * Q
        if total_Q >= ans:
            break
        if total_Q >= D:
            ans = min(ans, total_Q)
            break
        rem = D - total_Q
        x = (rem + P - 1) // P
        total_amount = total_Q + x * P
        if total_amount >= ans:
            continue
        ans = total_amount
    return ans

def min_total_amount(D, P, Q):
    ans = ((D + P - 1) // P) * P  # P만 사용했을 때의 최소 금액

    ans = check(D, P, Q, ans)
    ans = check(D, Q, P, ans)

    return ans

if __name__ == "__main__":
    D_str, P_str, Q_str = sys.stdin.readline().split()
    D = int(D_str)
    P = int(P_str)
    Q = int(Q_str)
    print(min_total_amount(D, P, Q))
```

### 코드의 동작 단계별 설명

1. **입력 처리**

   ```python
   D_str, P_str, Q_str = sys.stdin.readline().split()
   D = int(D_str)
   P = int(P_str)
   Q = int(Q_str)
   ```

2. **초기 최소 금액 설정**

   ```python
   ans = ((D + P - 1) // P) * P
   ```

3. **함수 `check` 정의 및 호출**

   ```python
   def check(D, P, Q, ans):
       # 반복 범위 설정 및 최소 금액 갱신

   ans = check(D, P, Q, ans)
   ans = check(D, Q, P, ans)
   ```

4. **결과 출력**

   ```python
   print(min_total_amount(D, P, Q))
   ```

## 결론

이번 문제를 통해 제한된 종류의 지폐로 특정 금액 이상의 최소 지불 금액을 구하는 방법에 대해 알아보았습니다. 반복문의 범위를 적절히 제한하고 조기 종료 조건을 활용하여 **시간 초과** 문제를 해결할 수 있었습니다.

알고리즘 문제를 풀 때는 입력 범위와 시간 복잡도를 고려하여 최적화하는 것이 중요합니다. 이러한 접근 방식을 통해 복잡한 문제도 효율적으로 해결할 수 있습니다.