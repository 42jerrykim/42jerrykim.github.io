---
title: "[Algorithm] C++/Python 백준 28702번 : FizzBuzz 스페셜 저지"
description: "백준 28702번 FizzBuzz 스페셜 저지: 연속한 세 출력 중 숫자 하나로 시작 위치를 역산해 다음 출력을 O(1)에 구하는 풀이와, 숫자가 반드시 존재한다는 증명, 15 주기 탐색이 불필요한 이유를 C++·Python 코드로 정리합니다."
categories: Algorithm
tags:
- Math(수학)
- Simulation(시뮬레이션)
- Brute-Force(완전탐색)
- Modular-Arithmetic(모듈러)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- Implementation(구현)
- Time-Complexity(시간복잡도)
- Coding-Test(코딩테스트)
- Optimization(최적화)
- Code-Quality(코드품질)
- Python
- String(문자열)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Best-Practices
- Complexity-Analysis(복잡도분석)
- Performance(성능)
- Pitfalls(함정)
- FizzBuzz
- String-Parsing
- Periodicity
- Case-Analysis
- Constant-Time
image: "wordcloud.png"
date: 2024-10-16
lastmod: 2024-10-16
---

이번 글에서는 백준 28702번 <strong>"FizzBuzz 스페셜 저지"</strong>를 다룹니다. 고전 FizzBuzz의 연속된 세 출력이 주어졌을 때 바로 다음 출력을 맞히는 문제로, 핵심은 "세 칸 안에는 반드시 숫자가 하나 이상 있다"는 사실을 알아채는 데 있습니다.

문제 : [https://www.acmicpc.net/problem/28702](https://www.acmicpc.net/problem/28702)

## 문제 설명

양의 정수 `i`를 1부터 하나씩 늘려 가며 `i`가 3과 5의 공배수이면 `FizzBuzz`, 3의 배수이면 `Fizz`, 5의 배수이면 `Buzz`, 어느 쪽도 아니면 `i` 자체를 출력하는 것이 FizzBuzz입니다. `i`가 1부터 15까지일 때의 출력은 `1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz`입니다.

입력으로는 이 수열에서 연속으로 출력된 세 문자열이 한 줄에 하나씩 주어지고, 각 문자열의 길이는 8 이하입니다. 입력은 항상 실제 FizzBuzz 수열의 연속 구간이라고 보장되므로, 구간의 시작 위치는 정확히 하나로 정해지고 그 다음 출력도 유일합니다.

예를 들어 `Fizz`, `Buzz`, `11`이 입력이면 이 구간은 9, 10, 11번째 출력이므로 답은 12번째 출력인 `Fizz`입니다. `980803`, `980804`, `FizzBuzz`가 입력이면 `FizzBuzz`는 3과 5의 공배수인 980805에 해당하므로 답은 980806, 즉 숫자 `980806`입니다.

## 접근 방식

입력에 숫자가 하나라도 있으면 시작 위치를 곧바로 역산할 수 있습니다. k번째(0부터 센다) 문자열이 숫자 `n`이라면 그 칸의 `i`는 `n`이고 구간의 시작은 `n - k`이므로, 구하는 값은 `n - k + 3`번째 출력, 곧 `n + (3 - k)`번째 출력입니다. 이후에는 `i`에 FizzBuzz 규칙을 그대로 적용하면 됩니다.

남는 질문은 "세 칸이 모두 문자열이면 어떻게 하는가"인데, 그런 입력은 존재하지 않습니다. 연속한 세 정수 중 3의 배수는 정확히 하나이고 5의 배수는 많아야 하나이므로, `Fizz`·`Buzz`·`FizzBuzz` 중 하나로 출력되는 칸은 최대 2개입니다. 예컨대 9, 10 또는 14, 15처럼 문자열이 연속으로 두 번 나오는 구간은 있어도 세 번 나오는 구간은 없습니다. 따라서 세 칸 중 적어도 한 칸은 숫자이고, "15 주기로 시작점을 전부 시험해 보는" 탐색은 이 문제에서 실행될 일이 없습니다. 이 증명을 알고 나면 일관성 검증도 필요 없습니다. 입력이 유효하다는 보장이 있으므로 숫자 하나만 믿고 역산해도 나머지 두 칸은 자동으로 맞아떨어집니다.

```mermaid
flowchart LR
    A["문자열 3개 입력"] --> B["첫 글자가 숫자인 칸 k 탐색"]
    B --> C["시작 위치 n-k 역산"]
    C --> D["fizzBuzz(n-k+3) 출력"]
```

값의 범위도 확인해 둡니다. 숫자 문자열의 길이가 8 이하이므로 `n`은 10^8 미만이고 답은 그보다 3 더 클 뿐이라 32비트 정수로도 충분합니다. 아래 코드는 습관적으로 `long long`을 쓰지만 `int`로 바꿔도 결과는 같습니다.

## C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <cctype>
#include <iostream>
#include <string>

using namespace std;

string fizzBuzz(long long i) {
    if (i % 15 == 0) return "FizzBuzz";
    if (i % 3 == 0) return "Fizz";
    if (i % 5 == 0) return "Buzz";
    return to_string(i);
}

int main() {
    string s[3];
    for (int k = 0; k < 3; ++k) cin >> s[k];

    for (int k = 0; k < 3; ++k) {
        if (isdigit(static_cast<unsigned char>(s[k][0]))) {
            long long n = stoll(s[k]);
            cout << fizzBuzz(n - k + 3) << '\n';
            return 0;
        }
    }
}
```

`fizzBuzz`는 문제 정의를 그대로 옮긴 함수이고, 15의 배수를 가장 먼저 검사해야 3의 배수 분기에서 `FizzBuzz`가 `Fizz`로 새지 않습니다. `main`은 세 문자열을 읽은 뒤 첫 글자가 숫자인 칸을 찾아 `n - k + 3`번째 출력을 내고 곧바로 종료합니다. 증명에 따라 `for` 루프 안에서 반드시 반환하므로 루프 뒤에 별도의 실패 처리를 두지 않았습니다. 숫자 판별은 `"Fizz"`, `"Buzz"`, `"FizzBuzz"`가 모두 알파벳으로 시작한다는 점을 이용해 첫 글자만 봅니다.

## Python 풀이

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
s = [input() for _ in range(3)]

def fizzbuzz(i):
    if i % 15 == 0:
        return "FizzBuzz"
    if i % 3 == 0:
        return "Fizz"
    if i % 5 == 0:
        return "Buzz"
    return str(i)

for k in range(3):
    if s[k].isdigit():
        print(fizzbuzz(int(s[k]) - k + 3))
        break
```

구조는 C++ 풀이와 같습니다. `str.isdigit()`이 숫자 칸을 걸러 주므로 `try/except`로 변환 실패를 잡을 필요가 없고, 파이썬 정수는 크기 제한이 없어 오버플로를 따로 고민하지 않아도 됩니다.

## 복잡도와 대안

| 항목 | 값 | 이유 |
|---|---|---|
| 시간 | O(1) | 고정된 3칸을 훑고 나머지 연산 몇 번 |
| 공간 | O(1) | 길이 8 이하 문자열 3개 |

대안으로는 시작 위치 `i`를 1부터 15까지 전부 대입해 세 칸이 입력과 일치하는지 검사하는 방법이 있습니다. 15 주기로 문자열 패턴이 반복되므로 숫자가 없는 입력이라면 이 방법이 필요하지만, 숫자가 있는 입력에서는 `n`이 크면 시작 위치가 1–15 범위를 벗어나므로 범위를 `n - k` 근처로 바꿔야 하고, 결국 숫자로 역산하는 것과 같아집니다. 이 문제에서는 숫자 역산이 더 단순하고 항상 정확하므로, 주기 탐색은 필요한 경우가 없는 방어 코드일 뿐입니다.

## 코너 케이스와 흔한 실수

시작 위치가 1에 가까운 경우(`1`, `2`, `Fizz`처럼 구간이 수열의 맨 앞에서 시작)에도 `n - k`가 1 이상으로 유지되므로 별도 처리가 필요하지 않습니다. 반대로 `Fizz`, `Buzz`처럼 문자열이 연속으로 나오는 입력(예: `Buzz`, `Fizz`, `7`)은 숫자가 맨 뒤에만 있으므로 `k = 2`를 `n - k`에 반영하지 않으면 답이 두 칸 어긋납니다. 또 `FizzBuzz`가 입력 끝에 있는 경우 다음 출력은 항상 숫자(15의 배수 다음은 15m+1)이므로, 출력에 따옴표나 공백을 섞지 않도록 주의합니다.

## 이 글을 읽은 후 달성해야 할 목표

- 연속한 세 정수 중 3 또는 5의 배수가 최대 두 개임을 근거로, 입력에 숫자가 반드시 존재함을 증명할 수 있다.
- 숫자 칸의 위치 `k`로 구간의 시작을 `n - k`로 역산하고 다음 출력을 `n - k + 3`번째로 계산할 수 있다.
- 15 주기 탐색이 이 문제에서 불필요한 이유와, 그것이 필요해지는 변형(숫자 없는 입력을 허용하는 경우)을 구분해 설명할 수 있다.
