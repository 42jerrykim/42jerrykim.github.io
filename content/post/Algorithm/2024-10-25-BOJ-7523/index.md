---
title: "[Algorithm] C++/Python 백준 7523번 : Gauß 다국어"
categories: 
- Algorithm
- Mathematics
- Arithmetic
tags:
- Mathematics
- GaussSum
- Implementation
- Arithmetic
- Optimization
- O(1)
- Summation
- MathematicalConcepts
- MathematicalProblem
image: "tmp_wordcloud.png"
date: 2024-10-25
---

카를 프리드리히 가우스는 독일의 위대한 수학자로, 그의 이름을 딴 다양한 수학적 개념들이 존재한다. 이번 포스팅에서는 백준 온라인 저지의 7523번 문제 "Gauß 다국어"를 통해 가우스의 합 공식을 활용한 문제 해결 방법을 알아보겠다. 이 문제는 주어진 두 정수 `n`과 `m` 사이의 모든 정수의 합을 효율적으로 계산하는 것을 목표로 한다.

문제 : [https://www.acmicpc.net/problem/7523](https://www.acmicpc.net/problem/7523)

## 문제 설명

주어진 문제는 두 정수 `n`과 `m`이 주어질 때, `n`보다 크거나 같고 `m`보다 작거나 같은 모든 정수의 합을 구하는 것이다. 즉, \(\sum_{i=n}^{m} i = n + (n+1) + (n+2) + \dots + (m-1) + m\)을 계산하는 것이다. 여기서 `n`과 `m`은 -10^9 이상 10^9 이하의 정수로, `n`이 `m`보다 작거나 같은 조건이 주어진다.

예를 들어, `n=1`이고 `m=100`인 경우, 1부터 100까지의 합은 5050이 된다. 또 다른 예로, `n=-11`이고 `m=10`인 경우, 합은 -11이 된다. 이러한 합을 효율적으로 계산하기 위해서는 단순히 반복문을 사용하는 것보다 수학적 공식을 활용하는 것이 더 효율적이다.

## 접근 방식

이 문제를 해결하기 위해 가장 효율적인 방법은 가우스의 합 공식을 활용하는 것이다. 가우스의 합 공식은 연속된 정수의 합을 빠르게 계산할 수 있는 수학적 공식으로, 다음과 같이 표현된다:

\[
\sum_{i=n}^{m} i = \frac{(m - n + 1) \times (n + m)}{2}
\]

여기서 `(m - n + 1)`은 `n`부터 `m`까지의 정수 개수를 나타내며, `(n + m)`은 첫 번째 항과 마지막 항의 합이다. 이 공식을 이용하면 반복문을 사용하지 않고도 O(1)의 시간 복잡도로 합을 계산할 수 있다. 

또한, 입력으로 주어지는 `n`과 `m`의 범위가 매우 크기 때문에, 일반적인 정수형 자료형인 `int`로는 범위를 초과할 수 있다. 따라서, `long long` 자료형을 사용하여 큰 정수를 처리해야 한다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int T;
    cin >> T;
    for(int tc=1; tc<=T; tc++){
        ll n, m;
        cin >> n >> m;
        ll count = m - n + 1;
        ll sum = (count * (n + m)) / 2;
        cout << "Scenario #" << tc << ":\n" << sum << "\n\n";
    }
}
```

### 코드 설명:

1. **입출력 최적화**: `ios::sync_with_stdio(false);`와 `cin.tie(0);`을 사용하여 C++의 입출력 속도를 최적화한다.

2. **테스트 케이스 입력**: 첫 번째 줄에서 테스트 케이스의 개수 `T`를 입력받는다.

3. **각 테스트 케이스 처리**:
    - `n`과 `m`을 입력받는다.
    - `count`는 `m - n + 1`로, `n`부터 `m`까지의 정수 개수를 계산한다.
    - `sum`은 `(count * (n + m)) / 2`로 가우스의 합 공식을 사용하여 합을 계산한다.
    - 결과를 지정된 형식에 맞추어 출력한다. 각 테스트 케이스 후에는 빈 줄을 출력한다.

이 코드는 주어진 문제의 요구사항을 충족하며, 큰 범위의 정수도 정확하게 처리할 수 있다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>

typedef long long ll;

int main(){
    int T;
    scanf("%d", &T);
    for(int tc=1; tc<=T; tc++){
        ll n, m;
        scanf("%lld %lld", &n, &m);
        ll count = m - n + 1;
        ll sum = (count * (n + m)) / 2;
        printf("Scenario #%d:\n%lld\n\n", tc, sum);
    }
    return 0;
}
```

### 코드 설명:

1. **입출력 처리**: `stdio.h`를 사용하여 `scanf`와 `printf`로 입력과 출력을 처리한다. 이는 C 스타일의 입출력을 사용하여 추가적인 라이브러리 없이 코드를 작성한 것이다.

2. **테스트 케이스 입력**: `scanf`를 통해 테스트 케이스의 개수 `T`를 입력받는다.

3. **각 테스트 케이스 처리**:
    - `n`과 `m`을 `scanf`로 입력받는다.
    - `count`는 `m - n + 1`로 계산한다.
    - `sum`은 `(count * (n + m)) / 2`로 합을 계산한다.
    - `printf`를 사용하여 결과를 지정된 형식으로 출력하고, 각 테스트 케이스 후에는 빈 줄을 추가한다.

이 코드는 C++의 표준 라이브러리를 사용하지 않고도 동일한 기능을 수행하며, 메모리 사용을 최소화할 수 있다.

## Python 코드와 설명

```python
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    T = int(data[0])
    index = 1
    for tc in range(1, T + 1):
        n = int(data[index])
        m = int(data[index + 1])
        index += 2
        count = m - n + 1
        sum_result = (count * (n + m)) // 2
        print(f"Scenario #{tc}:\n{sum_result}\n")

if __name__ == "__main__":
    main()
```

### 코드 설명:

1. **입력 처리 최적화**: `sys.stdin.read`를 사용하여 모든 입력을 한 번에 읽어온 후, `split()`을 통해 공백으로 분리된 데이터를 리스트로 만든다. 이는 반복적인 `input()` 호출보다 빠르다.

2. **테스트 케이스 입력**: 첫 번째 요소를 `T`로 변환하여 테스트 케이스의 개수를 얻는다.

3. **각 테스트 케이스 처리**:
    - 리스트에서 `n`과 `m`을 차례로 가져온다.
    - `count`는 `m - n + 1`로 계산한다.
    - `sum_result`는 `(count * (n + m)) // 2`로 합을 계산한다. 정수 나눗셈을 위해 `//` 연산자를 사용한다.
    - `print`를 사용하여 지정된 형식으로 결과를 출력하고, 각 테스트 케이스 후에는 빈 줄을 추가한다.

이 Python 코드는 간결하면서도 효율적으로 문제를 해결하며, 큰 입력에도 빠르게 동작할 수 있다.

## 결론

이번 포스팅에서는 백준 7523번 "Gauß 다국어" 문제를 통해 가우스의 합 공식을 활용한 효율적인 합 계산 방법을 알아보았다. 이 문제는 단순한 수학적 공식만으로도 매우 큰 범위의 정수 합을 빠르게 계산할 수 있음을 보여준다. 특히, `long long` 자료형을 사용하여 큰 정수를 정확하게 처리하고, C++과 Python 모두에서 최적화된 코드를 작성하는 방법을 살펴보았다.

추가적으로, 이 문제를 풀면서 가우스의 합 공식이 얼마나 유용한지 다시 한 번 깨달았으며, 유사한 문제에서 반복문 대신 수학적 공식을 활용하면 시간 복잡도를 크게 줄일 수 있음을 알게 되었다. 앞으로도 이러한 수학적 아이디어를 잘 활용하여 효율적인 알고리즘을 구현하는 데 주력할 것이다.