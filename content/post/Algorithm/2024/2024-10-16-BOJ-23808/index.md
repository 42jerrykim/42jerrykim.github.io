---

title: "[Algorithm] C++/Python 백준 23808번 : 골뱅이 찍기 - ㅂ"
categories: Algorithm
tags:
- Implementation
- PatternPrinting
- StringManipulation
- Loops
image: "tmp_wordcloud.png"
date: 2024-10-16
---

오늘은 백준 온라인 저지의 23808번 문제인 "골뱅이 찍기 - ㅂ"을 풀어보려고 한다. 이 문제는 특정한 패턴을 출력하는 구현 문제로, 주어진 조건에 따라 정확한 형태의 출력을 만드는 것이 핵심이다.

문제 : [https://www.acmicpc.net/problem/23808](https://www.acmicpc.net/problem/23808)

## 문제 설명

서준이는 아빠로부터 골뱅이가 들어 있는 상자를 생일 선물로 받았다. 상자 안에는 ㅂ자 모양의 골뱅이가 들어있다. ㅂ자 모양은 가로 및 세로로 각각 5개의 셀로 구성되어 있다. 상자에는 정사각형 모양의 셀의 크기를 나타내는 숫자 하나가 적혀있다.

셀의 크기 \( N \)이 주어지면 예제 출력과 같은 방식으로 골뱅이 모양을 출력하시오.

**입력**

첫째 줄에 정수 \( N \) (\( 1 \leq N \leq 100 \))이 주어진다.

**출력**

셀의 크기가 \( N \)인 골뱅이를 출력한다.

**예제 입력 1**

```
1
```

**예제 출력 1**

```
@   @
@   @
@@@@@
@   @
@@@@@
```

**예제 입력 2**

```
3
```

**예제 출력 2**

```
@@@         @@@
@@@         @@@
@@@         @@@
@@@         @@@
@@@         @@@
@@@         @@@
@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@
@@@         @@@
@@@         @@@
@@@         @@@
@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@
```

## 접근 방식

이 문제는 주어진 \( N \) 값에 따라 특정한 패턴을 출력하는 구현 문제이다. 출력해야 하는 모양은 한글 자음 'ㅂ'을 '@' 문자로 그린 형태이다. 전체 패턴은 총 5개의 블록으로 구성되어 있으며, 각 블록은 높이가 \( N \)인 행들로 이루어져 있다.

1. **블록 1 (\( 1 \)번째부터 \( N \)번째 줄):** 좌우에 '@' 문자가 있고, 그 사이에 공백이 있는 패턴이다.
2. **블록 2 (\( N+1 \)번째부터 \( 2N \)번째 줄):** 블록 1과 동일하다.
3. **블록 3 (\( 2N+1 \)번째부터 \( 3N \)번째 줄):** '@' 문자로 가득 찬 가로선이다.
4. **블록 4 (\( 3N+1 \)번째부터 \( 4N \)번째 줄):** 블록 1과 동일하다.
5. **블록 5 (\( 4N+1 \)번째부터 \( 5N \)번째 줄):** 블록 3과 동일하다.

각 블록의 패턴을 정확하게 구현하기 위해서는 반복문과 문자열 조작이 필요하다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <string> // 문자열 조작을 위한 헤더 파일
using namespace std;

int main() {
    int N;
    cin >> N; // 셀의 크기 입력 받기

    int totalLines = 5 * N; // 총 출력해야 하는 줄 수
    for (int i = 1; i <= totalLines; ++i) {
        if (i <= N || (i > N && i <= 2 * N) || (i > 3 * N && i <= 4 * N)) {
            // 블록 1, 2, 4에 해당하는 줄
            cout << string(N, '@');           // 왼쪽 '@' 문자 출력
            cout << string(3 * N, ' ');       // 가운데 공백 출력
            cout << string(N, '@') << '\n';   // 오른쪽 '@' 문자 출력 후 줄바꿈
        } else {
            // 블록 3, 5에 해당하는 줄
            cout << string(5 * N, '@') << '\n'; // '@' 문자로 가득 찬 줄 출력
        }
    }
    return 0;
}
```

**코드 설명**

1. **입력 받기**
   - `int N; cin >> N;`을 통해 셀의 크기 \( N \)을 입력 받는다.

2. **총 줄 수 계산**
   - `int totalLines = 5 * N;`을 통해 전체 출력해야 할 줄 수를 계산한다.

3. **반복문을 통한 패턴 출력**
   - `for` 문을 사용하여 `1`부터 `totalLines`까지 반복한다.
   - 각 줄에서 현재 줄 번호 `i`에 따라 출력할 내용을 결정한다.

4. **조건문을 통한 블록 구분**
   - `if` 문에서 `i`의 값에 따라 블록을 구분한다.
   - 블록 1, 2, 4에 해당하는 줄에서는 좌우에 '@' 문자를 출력하고 가운데는 공백으로 채운다.
   - 블록 3, 5에 해당하는 줄에서는 '@' 문자로 가득 찬 줄을 출력한다.

5. **문자열 생성과 출력**
   - `string(N, '@')`는 '@' 문자를 `N`번 반복하여 문자열을 생성한다.
   - `string(3 * N, ' ')`는 공백을 `3N`번 반복하여 문자열을 생성한다.
   - 각 부분을 `cout`을 통해 출력하고, `'\n'`으로 줄바꿈을 한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h> // 입출력을 위한 헤더 파일

int main() {
    int N;
    scanf("%d", &N); // 셀의 크기 입력 받기

    int totalLines = 5 * N; // 총 출력해야 하는 줄 수
    for (int i = 1; i <= totalLines; ++i) {
        if (i <= N || (i > N && i <= 2 * N) || (i > 3 * N && i <= 4 * N)) {
            // 블록 1, 2, 4에 해당하는 줄
            for (int j = 0; j < N; ++j) putchar('@');      // 왼쪽 '@' 문자 출력
            for (int j = 0; j < 3 * N; ++j) putchar(' ');  // 가운데 공백 출력
            for (int j = 0; j < N; ++j) putchar('@');      // 오른쪽 '@' 문자 출력
            putchar('\n'); // 줄바꿈
        } else {
            // 블록 3, 5에 해당하는 줄
            for (int j = 0; j < 5 * N; ++j) putchar('@'); // '@' 문자로 가득 찬 줄 출력
            putchar('\n'); // 줄바꿈
        }
    }
    return 0;
}
```

**코드 설명**

1. **입력 받기**
   - `scanf("%d", &N);`을 통해 셀의 크기 \( N \)을 입력 받는다.

2. **총 줄 수 계산**
   - `int totalLines = 5 * N;`을 통해 전체 출력해야 할 줄 수를 계산한다.

3. **반복문을 통한 패턴 출력**
   - `for` 문을 사용하여 `1`부터 `totalLines`까지 반복한다.

4. **조건문을 통한 블록 구분**
   - `if` 문에서 `i`의 값에 따라 블록을 구분한다.

5. **내부 반복문을 통한 문자 출력**
   - `for` 문을 사용하여 필요한 만큼의 '@' 문자와 공백을 출력한다.
   - `putchar()` 함수를 사용하여 문자를 출력한다.
   - 줄이 끝날 때마다 `putchar('\n');`을 통해 줄바꿈을 한다.

## Python 코드와 설명

```python
N = int(input())  # 셀의 크기 입력 받기

total_lines = 5 * N  # 총 출력해야 하는 줄 수
for i in range(1, total_lines + 1):
    if i <= N or (N < i <= 2 * N) or (3 * N < i <= 4 * N):
        # 블록 1, 2, 4에 해당하는 줄
        print('@' * N + ' ' * (3 * N) + '@' * N)
    else:
        # 블록 3, 5에 해당하는 줄
        print('@' * (5 * N))
```

**코드 설명**

1. **입력 받기**
   - `N = int(input())`을 통해 셀의 크기 \( N \)을 입력 받는다.

2. **총 줄 수 계산**
   - `total_lines = 5 * N`을 통해 전체 출력해야 할 줄 수를 계산한다.

3. **반복문을 통한 패턴 출력**
   - `for` 문을 사용하여 `1`부터 `total_lines`까지 반복한다.

4. **조건문을 통한 블록 구분**
   - `if` 문에서 `i`의 값에 따라 블록을 구분한다.

5. **문자열 생성과 출력**
   - `'@' * N`은 '@' 문자를 `N`번 반복한 문자열을 생성한다.
   - `' ' * (3 * N)`은 공백을 `3N`번 반복한 문자열을 생성한다.
   - 각 부분을 연결하여 `print()` 함수를 통해 출력한다.

## 결론

이번 문제는 특별한 알고리즘을 요구하지 않는 구현 문제로, 주어진 패턴을 정확하게 출력하는 것이 핵심이다. 반복문과 조건문을 적절히 활용하여 패턴을 구성하였다. 이러한 유형의 문제는 세부 조건을 놓치기 쉽기 때문에, 각 블록의 범위와 출력 형태를 명확히 파악하는 것이 중요하다. 앞으로도 구현 문제에서는 문제의 요구 사항을 꼼꼼히 읽고 구현하는 연습을 지속해야겠다.

---