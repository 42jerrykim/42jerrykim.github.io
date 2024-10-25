---
title: "[Algorithm] C++/Python 백준 2975번 : Transactions 다국어"
categories: 
- Algorithm
- Arithmetic
- Math
tags:
- Implementation
- Simulation
- I/O Optimization
- Conditional Logic
- Basic Math
image: "tmp_wordcloud.png"
date: 2024-10-25
---

은행의 ATM을 이용할 때마다 고객의 계좌 잔액을 정확히 유지하기 위한 계산이 필요하다. 이 문제에서는 예금과 출금 거래를 처리하여 최종 잔액을 계산하는 프로그램을 작성해야 한다. 특히, 은행 규칙에 따라 고객의 잔액이 -200을 초과하여 마이너스가 되지 않도록 해야 한다. 이는 과도한 출금으로 인해 발생할 수 있는 문제를 방지하기 위한 조치이다.

문제 : [https://www.acmicpc.net/problem/2975](https://www.acmicpc.net/problem/2975)

## 문제 설명

은행의 ATM에서는 고객이 출금이나 예금을 할 때마다 계좌의 잔액을 정확하게 유지하기 위해 계산이 필요하다. 이 문제에서는 여러 개의 거래가 주어질 때, 각 거래를 순서대로 처리하여 최종 잔액을 계산하는 프로그램을 작성해야 한다. 거래는 다음과 같이 이루어진다:

- **입력 형식**: 각 거래는 세 부분으로 구성된다. 첫 번째는 시작 잔액을 나타내는 정수 (–200 이상 +10,000 이하), 두 번째는 'W' 또는 'D'로 출금(Withdrawal) 또는 예금(Deposit)을 나타내는 문자, 세 번째는 출금 또는 예금할 금액을 나타내는 정수 (5 이상 400 이하)이다. 입력은 `0 W 0`으로 끝난다.

- **출력 형식**: 각 유효한 거래에 대해 새로운 잔액을 한 줄에 출력한다. 단, 출금으로 인해 잔액이 –200을 넘어서 마이너스가 될 경우, "Not allowed"를 출력한다.

- **예시**:
    ```
    입력:
    10000 W 10
    -200 D 300
    50 W 300
    0 W 0

    출력:
    9990
    100
    Not allowed
    ```

위 예시에서 첫 번째 거래는 10,000원에서 10원을 출금하여 9,990원이 된다. 두 번째 거래는 -200원에서 300원을 예금하여 100원이 된다. 세 번째 거래는 50원에서 300원을 출금하려고 하지만, 이는 -250원이 되어 규칙을 위반하므로 "Not allowed"를 출력한다.

## 접근 방식

이 문제는 간단한 시뮬레이션 문제로, 주어진 거래들을 순서대로 처리하면서 잔액을 업데이트하는 방식으로 해결할 수 있다. 각 거래는 예금 또는 출금으로 구분되며, 출금 시 잔액이 –200 이하로 떨어지는지를 확인해야 한다. 이를 위해 다음과 같은 단계를 따른다:

1. **입력 처리**: 거래가 `0 W 0`이 될 때까지 입력을 계속 받는다.
2. **예금 처리**: 'D'가 입력되면 현재 잔액에 금액을 더한다.
3. **출금 처리**: 'W'가 입력되면 현재 잔액에서 금액을 뺀 후, 잔액이 –200 이하로 떨어지는지 확인한다. 만약 그렇다면 "Not allowed"를 출력하고, 그렇지 않다면 잔액을 업데이트한다.
4. **출력**: 각 유효한 거래 후의 잔액을 출력하거나, 규칙을 위반한 경우 "Not allowed"를 출력한다.

이러한 단계를 통해 모든 거래를 효율적으로 처리할 수 있으며, 특별한 자료 구조나 복잡한 알고리즘이 필요하지 않다. 입력의 범위가 제한적이므로 기본적인 구현으로도 문제를 해결할 수 있다.

## C++ 코드와 설명

아래는 문제를 해결하기 위한 최적화된 C++ 코드이다. 이 코드는 빠른 입력 처리를 위해 `ios::sync_with_stdio(false)`와 `cin.tie(0)`을 사용하였다. 각 거래를 읽고, 예금 또는 출금에 따라 잔액을 업데이트하며, 출금 시 잔액이 –200 이하로 떨어지는지를 확인하여 적절한 출력을 한다.

```cpp
#include <iostream>
using namespace std;

int main(){
    ios::sync_with_stdio(false); // 빠른 입출력을 위해 동기화 해제
    cin.tie(0); // 입력과 출력을 분리하여 속도 향상

    long long balance, amount;
    char op;
    
    while(cin >> balance >> op >> amount){
        if(balance == 0 && op == 'W' && amount == 0){
            break; // 종료 조건
        }
        if(op == 'D'){
            balance += amount; // 예금 처리
            cout << balance << "\n";
        }
        else if(op == 'W'){
            if(balance - amount < -200){
                cout << "Not allowed\n"; // 출금 불가
            }
            else{
                balance -= amount; // 출금 처리
                cout << balance << "\n";
            }
        }
        // 유효하지 않은 연산 문자는 무시
    }
    
    return 0;
}
```

### 코드 설명

1. **입출력 최적화**:
    - `ios::sync_with_stdio(false)`와 `cin.tie(0)`을 사용하여 C++의 표준 입출력 스트림을 최적화한다. 이는 입력 속도를 크게 향상시킨다.

2. **변수 선언**:
    - `balance`: 현재 잔액을 저장하는 변수.
    - `op`: 거래 유형을 나타내는 문자 ('D' 또는 'W').
    - `amount`: 거래 금액을 저장하는 변수.

3. **반복문을 통한 거래 처리**:
    - `while(cin >> balance >> op >> amount)` 루프를 사용하여 거래를 하나씩 읽어들인다.
    - 입력이 `0 W 0`일 경우 루프를 종료한다.

4. **예금 처리**:
    - 거래 유형이 'D'인 경우, `balance`에 `amount`를 더하고 새로운 잔액을 출력한다.

5. **출금 처리**:
    - 거래 유형이 'W'인 경우, 출금 후 잔액이 –200보다 작은지 확인한다.
    - 만약 잔액이 –200보다 작아지면 "Not allowed"를 출력하고, 그렇지 않으면 `balance`에서 `amount`를 뺀 후 새로운 잔액을 출력한다.

6. **출력**:
    - 각 거래 후의 잔액 또는 "Not allowed"를 출력하여 결과를 보여준다.

## C++ without library 코드와 설명

아래는 C++에서 `stdio.h`와 `malloc.h`만을 사용하여 작성한 최적화된 코드이다. 이 코드는 C 스타일의 입출력을 사용하여 효율성을 높였다.

```cpp
#include <stdio.h>

int main(){
    long long balance, amount;
    char op;
    
    while(scanf("%lld %c %lld", &balance, &op, &amount) != EOF){
        if(balance == 0 && op == 'W' && amount == 0){
            break; // 종료 조건
        }
        if(op == 'D'){
            balance += amount; // 예금 처리
            printf("%lld\n", balance);
        }
        else if(op == 'W'){
            if(balance - amount < -200){
                printf("Not allowed\n"); // 출금 불가
            }
            else{
                balance -= amount; // 출금 처리
                printf("%lld\n", balance);
            }
        }
    }
    
    return 0;
}
```

### 코드 설명

1. **입출력 처리**:
    - `scanf`와 `printf`를 사용하여 C 스타일의 입출력을 처리한다. 이는 C++의 `cin`과 `cout`보다 빠르며, 시간 제한이 엄격한 문제에서 유리하다.

2. **변수 선언**:
    - `balance`: 현재 잔액을 저장하는 변수.
    - `op`: 거래 유형을 나타내는 문자 ('D' 또는 'W').
    - `amount`: 거래 금액을 저장하는 변수.

3. **반복문을 통한 거래 처리**:
    - `while(scanf("%lld %c %lld", &balance, &op, &amount) != EOF)` 루프를 사용하여 거래를 하나씩 읽어들인다.
    - 입력이 `0 W 0`일 경우 루프를 종료한다.

4. **예금 및 출금 처리**:
    - 거래 유형에 따라 예금 또는 출금을 처리하며, 출금 시 잔액이 –200 이하로 떨어지는지를 확인한다.
    - 적절한 결과를 `printf`로 출력한다.

## Python 코드와 설명

아래는 문제를 해결하기 위한 최적화된 Python 코드이다. Python의 간결한 문법을 사용하여 구현하였다.

```python
import sys

def main():
    for line in sys.stdin:
        balance, op, amount = line.strip().split()
        balance = int(balance)
        amount = int(amount)
        if balance == 0 and op == 'W' and amount == 0:
            break
        if op == 'D':
            balance += amount
            print(balance)
        elif op == 'W':
            if balance - amount < -200:
                print("Not allowed")
            else:
                balance -= amount
                print(balance)

if __name__ == "__main__":
    main()
```

### 코드 설명

1. **입출력 처리**:
    - `sys.stdin`을 사용하여 표준 입력을 빠르게 처리한다. 이는 큰 입력을 처리할 때 유리하다.

2. **입력 읽기 및 처리**:
    - `for line in sys.stdin` 루프를 사용하여 각 거래를 한 줄씩 읽어들인다.
    - `line.strip().split()`을 통해 각 줄을 공백으로 분리하여 `balance`, `op`, `amount`를 추출한다.
    - `balance`와 `amount`를 정수형으로 변환한다.

3. **종료 조건 확인**:
    - 입력이 `0 W 0`일 경우 루프를 종료한다.

4. **예금 및 출금 처리**:
    - 거래 유형이 'D'인 경우, `balance`에 `amount`를 더하고 새로운 잔액을 출력한다.
    - 거래 유형이 'W'인 경우, 출금 후 잔액이 –200보다 작은지 확인한다. 조건을 만족하지 않으면 "Not allowed"를 출력하고, 그렇지 않으면 `balance`에서 `amount`를 빼고 새로운 잔액을 출력한다.

## 결론

이번 문제는 간단한 시뮬레이션과 구현 능력을 평가하는 문제였다. 주어진 거래들을 순서대로 처리하면서 조건을 충족하는지를 확인하는 방식으로 접근하였다. C++과 Python 모두에서 효율적인 입출력 처리를 통해 시간 제한을 만족시킬 수 있었으며, 특별한 자료 구조나 복잡한 알고리즘이 필요 없었다. 다만, 출금 시 잔액이 –200 이하로 떨어지는 조건을 정확히 처리하는 것이 중요하였다. 앞으로 유사한 구현 문제에서는 이러한 조건 검사를 정확히 구현하는 것이 핵심임을 다시 한번 확인할 수 있었다.

또한, C++에서는 `ios::sync_with_stdio(false)`와 `cin.tie(0)`을 사용하여 입출력을 최적화함으로써 더 빠르게 처리할 수 있었으며, Python에서는 `sys.stdin`을 사용하여 입력 속도를 향상시킬 수 있었다. 이러한 입출력 최적화 기법은 문제 해결 속도를 크게 향상시킬 수 있음을 다시 한번 느꼈다.