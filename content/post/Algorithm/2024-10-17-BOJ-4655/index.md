---
title: "[Algorithm] C++/Python 백준 4655번 : Hangover"
categories: 
- Algorithm
- Math
- Implementation
tags:
- Harmonic Series
- Greedy
- Implementation
- Iterative Summation
- Time Complexity O(N)
- Math
- Mathematical Concept
- Implementation Problem
image: "tmp_wordcloud.png"
date: 2024-01-01
---

카드를 이용하여 테이블 위로 얼마나 멀리 오버행을 만들 수 있는지에 대한 문제는 흥미로운 수학적 개념과 구현 능력을 요구한다. 이 문제는 주어진 카드의 수를 통해 최대한의 오버행을 달성하는 방법을 탐구하며, 이를 통해 조화수열의 성질을 활용한 효율적인 알고리즘을 구현할 수 있다.

문제 : [https://www.acmicpc.net/problem/4655](https://www.acmicpc.net/problem/4655)

## 문제 설명

카드를 쌓아 테이블 위로 얼마나 멀리 오버행을 만들 수 있는지 계산하는 문제이다. 카드가 한 장 있을 때, 최대 오버행 길이는 카드 길이의 절반이다. 두 장의 카드를 사용하면, 위쪽 카드가 아래쪽 카드 위로 카드 길이의 절반만큼 오버행하고, 아래쪽 카드는 테이블 위로 카드 길이의 1/3만큼 오버행하여 총 오버행 길이는 1/2 + 1/3 = 5/6 카드 길이가 된다. 일반적으로 n장의 카드를 사용할 때, 최대 오버행 길이는 1/2 + 1/3 + 1/4 + ... + 1/(n + 1) 카드 길이가 된다. 주어진 오버행 길이 c를 만족하거나 초과하기 위해 필요한 최소 카드의 수를 구하는 것이 목표이다.

입력은 여러 개의 테스트 케이스로 구성되며, 각 테스트 케이스는 0.00으로 끝난다. 각 테스트 케이스는 세 자리의 소수로 표현된 양의 부동 소수점 수 c가 주어진다. 출력은 각 테스트 케이스에 대해 최소 카드 수를 "X card(s)" 형식으로 출력한다.

## 접근 방식

이 문제를 해결하기 위해, n장의 카드로 만들 수 있는 최대 오버행 길이가 조화수열의 합으로 표현된다는 점을 이용한다. 조화수열은 무한히 증가하지만 느리게 증가하기 때문에, 원하는 오버행 길이 c에 도달하기 위해 필요한 최소 카드 수를 구하는 것은 반복적으로 조화수열의 항을 더해가는 방식으로 접근할 수 있다.

구체적인 접근 방법은 다음과 같다:

1. **초기화:** 오버행 길이를 0.0으로 초기화하고, 카드 수 n을 0으로 설정한다.
2. **반복:** 오버행 길이가 c에 도달할 때까지 n을 1씩 증가시키면서, 1/(n + 1)을 오버행에 추가한다.
3. **조건 확인:** 오버행 길이가 c 이상이 되면 현재의 n이 필요한 최소 카드 수가 된다.
4. **출력:** 해당 n을 지정된 형식으로 출력한다.

이 방법은 간단하면서도 문제의 요구사항을 정확히 만족시키며, 주어진 제약 조건 내에서 효율적으로 동작한다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    double c;
    while(cin >> c){
        if(c == 0.00) break; // 입력이 0.00이면 종료
        double overhang = 0.0;
        int n = 0;
        while(overhang < c){
            n++;
            overhang += 1.0 / (n + 1); // 조화수열의 다음 항을 추가
        }
        printf("%d card(s)\n", n); // 결과 출력
    }
}
```

### 코드 설명:

1. **입력 처리:** `while(cin >> c)`를 통해 입력을 반복적으로 받는다. 입력이 `0.00`일 경우 반복을 종료한다.
2. **오버행 계산:** `overhang`을 0.0으로 초기화하고, 카드 수 `n`을 0으로 설정한다. `while(overhang < c)` 루프를 통해 `overhang`이 목표 값 `c`에 도달할 때까지 반복한다.
3. **조화수열 합산:** 각 반복에서 `n`을 증가시키고, `1/(n + 1)`을 `overhang`에 더한다.
4. **결과 출력:** 필요한 카드 수 `n`을 형식에 맞춰 출력한다.

이 구현은 조화수열의 항을 하나씩 더해가며 목표 오버행 길이에 도달하는 최소 카드를 효율적으로 계산한다.

## Python 코드와 설명

```python
def calculate_min_cards(c):
    overhang = 0.0
    n = 0
    while overhang < c:
        n += 1
        overhang += 1.0 / (n + 1) # 조화수열의 다음 항을 추가
    return n

def main():
    import sys
    for line in sys.stdin:
        c_str = line.strip()
        if c_str == "0.00":
            break
        c = float(c_str)
        cards = calculate_min_cards(c)
        print(f"{cards} card(s)")

if __name__ == "__main__":
    main()
```

### 코드 설명:

1. **함수 `calculate_min_cards(c)`:** 오버행 길이 `c`를 받아 필요한 최소 카드 수를 계산한다. `overhang`을 0.0으로, `n`을 0으로 초기화하고, `while` 루프를 통해 `overhang`이 `c`에 도달할 때까지 `1/(n + 1)`을 더해간다.
2. **함수 `main()`:** 표준 입력으로부터 각 라인을 읽어들인다. `0.00`이 입력되면 종료하고, 그렇지 않으면 `calculate_min_cards` 함수를 호출하여 결과를 출력한다.
3. **실행:** 스크립트는 표준 입력을 통해 여러 테스트 케이스를 처리할 수 있으며, 각 테스트 케이스에 대해 필요한 카드 수를 출력한다.

이 Python 구현은 코드가 간결하며, 반복적인 합산 과정을 효율적으로 처리한다.

## 결론

이번 문제는 조화수열의 특성을 활용하여 주어진 오버행 길이를 만족하기 위한 최소 카드 수를 계산하는 문제였다. 간단한 반복 구조와 수학적 이해를 통해 효율적으로 해결할 수 있었으며, 다양한 언어로 구현하여 문제의 핵심 알고리즘을 명확히 이해할 수 있었다. 추가적인 최적화는 필요하지 않았지만, 조화수열의 누적 합이 매우 느리게 증가하는 점을 고려하면, 매우 큰 오버행에 대해서는 계산 시간이 늘어날 수 있다는 점을 염두에 두어야 한다. 이 문제를 통해 수학적 아이디어와 구현 능력을 동시에 향상시킬 수 있었으며, 유사한 문제를 해결하는 데 유용한 접근 방식을 배울 수 있었다.