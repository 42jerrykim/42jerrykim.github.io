---
title: "[Algorithm] C++/Python 백준 15025번: Judging Moose"
description: "백준 15025번 Judging Moose 문제는 입력받은 두 값(왼쪽, 오른쪽 뿔의 가지 수)에 따라 조건문으로 무스의 포인트를 판별합니다. 두 값이 모두 0이면 무스가 아니며, 같으면 'Even', 다르면 'Odd'로 출력하는 간단한 구현 문제입니다."
categories: Algorithm
tags:
- Implementation(구현)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- C
- Python
- Time-Complexity(시간복잡도)
- Space-Complexity(공간복잡도)
- Complexity-Analysis(복잡도분석)
- Coding-Test(코딩테스트)
- Edge-Cases(엣지케이스)
- Testing(테스트)
- Debugging(디버깅)
- Best-Practices
- Clean-Code(클린코드)
- Code-Quality(코드품질)
- Readability
- Pitfalls(함정)
- Beginner
- Fundamentals(기초)
- Comparison(비교)
- Stdin
- Tutorial(튜토리얼)
- Education(교육)
- Math(수학)
image: "wordcloud.png"
date: 2024-10-16
lastmod: 2024-10-16
---

이번 포스팅에서는 백준 온라인 저지의 15025번 문제인 "Judging Moose"를 다뤄보려고 합니다. 이 문제는 간단한 조건문과 비교 연산을 활용하여 해결할 수 있는 구현 문제로, 입력이 정수 두 개뿐이라 시간·공간 복잡도가 모두 O(1)입니다. 난이도보다 조건의 순서와 출력 형식을 정확히 맞추는 데 의미가 있는 입문 문제입니다.

문제 : [https://www.acmicpc.net/problem/15025](https://www.acmicpc.net/problem/15025)

## 문제 설명

북미 지역의 큰 사슴인 무스(moose)는 나이에 따라 뿔의 가지 수가 달라집니다. 일반적으로 나이가 많은 수컷 무스일수록 뿔의 가지(tine)가 많습니다. 하지만 뿔의 가지 수만으로 정확한 나이를 판단하기는 어렵습니다. 왜냐하면 무스가 싸움을 하거나 다른 이유로 인해 뿔의 일부가 부러질 수 있기 때문입니다.

그래서 무스의 뿔을 평가할 때는 양쪽 뿔의 가지 수를 사용하여 포인트(point) 시스템을 적용합니다. 포인트 시스템은 다음과 같이 동작합니다:

- **양쪽 뿔의 가지 수가 같을 때**: "Even x"라고 표현하며, 여기서 x는 양쪽 뿔 가지 수의 합입니다. 예를 들어, 왼쪽과 오른쪽 뿔의 가지 수가 각각 3이라면 "Even 6"이 출력됩니다.
- **양쪽 뿔의 가지 수가 다를 때**: "Odd x"라고 표현하며, 여기서 x는 가지 수가 더 많은 쪽의 가지 수를 두 배한 값입니다. 예를 들어, 왼쪽 뿔의 가지 수가 5이고 오른쪽이 3이라면 "Odd 10"이 출력됩니다.
- **양쪽 뿔에 가지가 하나도 없을 때**: "Not a moose"라고 표현합니다.

입력으로 왼쪽과 오른쪽 뿔의 가지 수가 주어졌을 때, 위의 포인트 시스템에 따라 무스를 판단하는 프로그램을 작성해야 합니다.

## 접근 방식

풀이의 핵심은 판정 순서입니다. 입력으로 왼쪽 가지 수 `l`과 오른쪽 가지 수 `r`을 받은 뒤, 가장 특수한 경우인 `l`과 `r`이 모두 0인 상황을 먼저 걸러야 합니다. 이 검사를 `l == r` 뒤에 두면 `0 0`이 "Even 0"으로 잘못 출력됩니다. `0 0`은 두 값이 같기 때문에 `l == r` 조건에도 해당하므로, 더 좁은 조건이 항상 앞에 와야 합니다. 그다음 두 값이 같으면 합 `l + r`을 붙여 "Even"을, 다르면 큰 쪽의 두 배인 `2 * max(l, r)`을 붙여 "Odd"를 출력합니다. 분기가 세 개뿐이고 연산이 상수 번이므로 최적화할 여지도 필요도 없습니다.

| 조건 | 출력 | 예시 입력 | 예시 출력 |
|---|---|---|---|
| `l == 0` 이고 `r == 0` | `Not a moose` | `0 0` | `Not a moose` |
| `l == r` (0 아님) | `Even l+r` | `3 3` | `Even 6` |
| `l != r` | `Odd 2*max(l,r)` | `5 3` | `Odd 10` |

| 항목 | 값 |
|---|---|
| 시간 복잡도 | O(1) |
| 공간 복잡도 | O(1) |

## C++ 코드와 설명

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int l, r;
    cin >> l >> r; // 왼쪽과 오른쪽 뿔의 가지 수 입력

    if (l == 0 && r == 0) {
        cout << "Not a moose" << endl; // 둘 다 0이면 무스가 아님
    } else if (l == r) {
        cout << "Even " << l + r << endl; // 가지 수가 같으면 Even 출력
    } else {
        cout << "Odd " << 2 * max(l, r) << endl; // 가지 수가 다르면 Odd 출력
    }

    return 0;
}
```

### 코드 설명

`cin >> l >> r;`로 두 정수를 읽고, `if / else if / else` 사슬로 앞서 정한 순서대로 세 분기를 검사합니다. 최댓값은 `<algorithm>`의 `std::max`로 구하며, 이 헤더를 명시적으로 포함해야 컴파일러에 따라 컴파일이 실패하는 일을 피할 수 있습니다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

int main() {
    int l, r;
    scanf("%d %d", &l, &r); // 왼쪽과 오른쪽 뿔의 가지 수 입력

    if (l == 0 && r == 0) {
        printf("Not a moose\n"); // 둘 다 0이면 무스가 아님
    } else if (l == r) {
        printf("Even %d\n", l + r); // 가지 수가 같으면 Even 출력
    } else {
        int max = (l > r) ? l : r; // 더 큰 값을 찾음
        printf("Odd %d\n", 2 * max); // 가지 수가 다르면 Odd 출력
    }

    return 0;
}
```

### 코드 설명

`scanf("%d %d", &l, &r);`로 입력을 받고 분기 구조는 위 코드와 같습니다. 라이브러리 `max`를 쓰지 않고 삼항 연산자 `(l > r) ? l : r`로 큰 값을 직접 고르는 점만 다릅니다. 변수 이름 `max`는 표준 라이브러리 함수명과 겹칠 수 있으니 실무 코드에서는 `larger` 같은 이름이 안전합니다.

## Python 코드와 설명

```python
l, r = map(int, input().split())  # 왼쪽과 오른쪽 뿔의 가지 수 입력

if l == 0 and r == 0:
    print("Not a moose")  # 둘 다 0이면 무스가 아님
elif l == r:
    print(f"Even {l + r}")  # 가지 수가 같으면 Even 출력
else:
    print(f"Odd {2 * max(l, r)}")  # 가지 수가 다르면 Odd 출력
```

### 코드 설명

`map(int, input().split())`으로 한 줄을 공백 기준으로 나눠 정수 두 개로 변환하고, `f-string`으로 출력 문자열을 조립합니다. 파이썬은 `if / elif / else`로 같은 순서의 분기를 표현하며, 내장 `max`를 바로 쓸 수 있어 가장 짧습니다.

## 코너 케이스 및 실수 포인트

| 케이스 | 입력 | 기대 출력 | 주의점 |
|---|---|---|---|
| 둘 다 0 | `0 0` | `Not a moose` | `l == r`보다 먼저 검사해야 함 |
| 한쪽만 0 | `0 4` | `Odd 8` | 0이 하나여도 무스이며 Odd |
| 반대 방향 | `4 0` | `Odd 8` | `max`로 좌우 순서와 무관하게 처리 |
| 같은 값 | `3 3` | `Even 6` | 합 `l + r`이지 `l`이 아님 |
| 서로 다른 값 | `5 3` | `Odd 10` | 합이 아니라 큰 쪽의 두 배 |

입력 범위가 작아 `int`로 충분하므로 오버플로우나 빠른 입출력 설정은 필요 없습니다.

## 결론

이 문제의 함정은 알고리즘이 아니라 조건의 순서와 출력 형식에 있습니다. `0 0`을 `l == r`보다 먼저 처리하고, `Even`은 합, `Odd`는 큰 쪽의 두 배라는 차이를 구분하면 됩니다. 한쪽만 0인 입력이 Odd로 분류된다는 점을 직접 손으로 확인해 보는 것이 이 문제에서 가장 쓸모 있는 연습입니다.

## 학습 목표

- 포함 관계가 있는 조건(`0 0`이 `l == r`의 부분집합)에서 분기 순서를 정하는 기준을 설명할 수 있다.
- 입력 크기와 연산 횟수로부터 시간·공간 복잡도가 O(1)임을 근거와 함께 말할 수 있다.
- 같은 로직을 `std::max`, 삼항 연산자, 파이썬 내장 `max`로 구현하며 차이를 비교할 수 있다.
