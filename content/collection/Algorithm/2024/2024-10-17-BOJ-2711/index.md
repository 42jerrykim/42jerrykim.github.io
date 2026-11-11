---
title: "[Algorithm] C++/Python 백준 2711번 : 오타맨 고창영"
description: "백준 2711번 오타맨 고창영은 1-based 위치 P의 글자를 지워 문자열을 복구하는 구현 문제다. C++ erase, C 배열 시프트, Python 슬라이싱 세 방식의 동작과 비용을 비교하고 P-1 인덱스 변환 함정을 정리한다."
categories: 
- Algorithm
- Implementation
- String 
tags:
- Implementation(구현)
- C++
- Python
- Array(배열)
- Problem-Solving(문제해결)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Time-Complexity(시간복잡도)
- Coding-Test(코딩테스트)
- Data-Structures(자료구조)
- Optimization(최적화)
- Code-Quality(코드품질)
- String(문자열)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Testing(테스트)
- Best-Practices
- Complexity-Analysis(복잡도분석)
- Debugging(디버깅)
- Refactoring(리팩토링)
- Clean-Code(클린코드)
- Performance(성능)
- Pitfalls(함정)
- Simulation(시뮬레이션)
- Pointer(포인터)
- Memory(메모리)
- Beginner
- Tutorial(튜토리얼)
image: "wordcloud.png"
date: 2024-10-17
lastmod: 2024-10-17
---

고창영은 맨날 오타를 낸다. 이 문제는 "P번째 글자 하나를 지운 문자열을 출력하라"는 요구를 그대로 구현하면 되는 입문 수준의 문자열 문제다. 알고리즘적 난점은 없고, 위치가 1부터 시작한다는 점과 언어별 문자열 삭제 방식의 차이를 정확히 다루는 것이 핵심이다.

문제 : [https://www.acmicpc.net/problem/2711](https://www.acmicpc.net/problem/2711)

## 학습 목표

- 1-based 입력 위치를 0-based 인덱스로 바꿔 문자열의 한 글자를 삭제할 수 있다.
- C++ `erase`, C 배열 시프트, Python 슬라이싱의 동작과 비용을 비교하고 상황에 맞게 고를 수 있다.
- `P-1`을 빠뜨렸을 때 어떤 오답이 나오는지 설명할 수 있다.

## 문제 설명

테스트 케이스 개수 `T`가 먼저 주어지고, 각 케이스는 오타 위치 `P`와 문자열 `S`가 공백으로 구분된 한 줄이다. 문자열은 대문자로만 구성되며 길이는 최대 80이고, `P`는 1 이상 문자열 길이 이하라고 문제가 보장한다. 첫 글자가 1번째라는 점에 유의해 `P`번째 글자를 제거한 문자열을 케이스마다 한 줄씩 출력한다.

## 접근 방식

삭제할 글자의 0-based 인덱스는 `P-1`이다. 같은 문자열을 두 방식으로 보면 아래와 같다.

| 인덱스(0-based) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 글자 | M | I | S | **S** | P | E | L | L |
| 위치(1-based) | 1 | 2 | 3 | **4** | 5 | 6 | 7 | 8 |

`MISSPELL`에서 `P=4`이면 지울 글자는 인덱스 3의 `S`이고, 결과는 `MISPELL`이다. 만약 `P-1` 대신 `P`를 그대로 인덱스로 쓰면 인덱스 4의 `P`가 지워져 `MISSELL`이 나오는데, 이것이 이 문제에서 가장 흔한 오답이다. 케이스당 비용은 문자열 길이에 비례하는 이동 한 번이므로 전체 시간 복잡도는 O(T·N)이고, N ≤ 80이라 입력 크기와 무관하게 사실상 상수 시간이다.

## C++ 풀이

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int T;
    cin >> T;

    while(T--){
        int P;
        string S;
        cin >> P >> S;
        S.erase(P-1, 1); // 1-based 위치를 0-based 인덱스로 바꿔 한 글자 삭제
        cout << S << "\n";
    }
}
```

`string::erase(pos, count)`는 `pos`부터 `count`개 글자를 지우고 뒤쪽 글자를 앞으로 당긴다. 이 문제는 `P`가 항상 유효하다고 보장하므로 범위 검사를 두지 않았다. 범위를 벗어난 `pos`를 넘기면 `std::out_of_range` 예외가 발생하므로, 입력 보장이 없는 상황이라면 `P <= S.size()` 검사를 추가해야 한다. 입출력 동기화를 끄는 두 줄은 케이스가 많을 때 입출력 시간을 줄이는 관용 구문이다.

**예제 입력/출력** (세 풀이 모두 동일)

```
입력:             출력:
4                 MISPELL
4 MISSPELL        ROGRAMMING
1 PROGRAMMING     CONTES
7 CONTEST         BALOON
3 BALLOON
```

## C 풀이: 표준 라이브러리 없이 직접 이동

```cpp
#include <stdio.h>
#include <string.h>

int main(){
    int T;
    scanf("%d", &T);

    while(T--){
        int P;
        char S[81];
        scanf("%d %s", &P, S);

        int len = strlen(S);
        for(int i = P-1; i < len; i++){
            S[i] = S[i+1]; // 뒤 글자를 한 칸씩 앞으로 이동, 마지막에 널 문자도 함께 이동
        }
        printf("%s\n", S);
    }
}
```

C 문자열은 널 문자로 끝나는 배열이므로 삭제는 "삭제 위치 뒤의 모든 글자를 한 칸 앞으로 복사"로 구현한다. 반복 범위가 `i < len`이라 `i = len-1`일 때 `S[len]`, 즉 널 문자가 `S[len-1]`로 복사되어 문자열이 자동으로 한 글자 짧아진다. 배열 크기를 81로 잡은 것은 최대 80자와 널 문자 1개를 담기 위해서이며, 이보다 작게 잡으면 `scanf`가 버퍼를 넘겨 쓰게 된다.

## Python 풀이

```python
import sys

def main():
    data = sys.stdin.read().split()
    T = int(data[0])
    for i in range(T):
        P = int(data[1 + 2*i])
        S = data[2 + 2*i]
        print(S[:P-1] + S[P:])  # 인덱스 P-1 한 글자만 건너뛰고 이어 붙임

if __name__ == "__main__":
    main()
```

Python 문자열은 불변(immutable)이라 제자리 삭제가 불가능하다. 대신 `S[:P-1]`(삭제 위치 앞)과 `S[P:]`(삭제 위치 뒤)를 이어 붙여 새 문자열을 만든다. 슬라이싱은 범위를 벗어나도 예외 없이 빈 문자열을 돌려주므로 C++과 달리 `P`가 잘못되어도 오류 없이 원본이 그대로 나온다는 점이 다르다. 입력을 `sys.stdin.read().split()`으로 한 번에 읽어 토큰 인덱스로 접근하면 줄 단위 `input()` 호출보다 빠르다.

## 세 방식 비교와 선택 기준

| 방식 | 시간 | 추가 공간 | 원본 변경 | 비고 |
|---|---|---|---|---|
| C++ `erase` | O(N) 이동 | O(1) | 제자리 | 범위 밖이면 예외 |
| C 배열 시프트 | O(N) 이동 | O(1) | 제자리 | 버퍼 크기 직접 관리 |
| Python 슬라이싱 | O(N) 복사 | O(N) | 새 문자열 | 범위 밖이어도 예외 없음 |

세 방식 모두 점근 복잡도는 O(N)이고 N ≤ 80이므로 성능 차이는 의미가 없다. 선택 기준은 안전성과 가독성이다. C++에서는 `erase`가 의도를 가장 잘 드러내고, C에서는 시프트 루프가 널 종결 문자열의 구조를 이해하는 좋은 연습이 된다. 한 문자열에서 삭제를 여러 번 반복해야 한다면 `erase`나 시프트는 매번 O(N)이 들므로 삭제할 위치를 모아 한 번의 순회로 새 문자열을 만드는 편이 낫다. 이 문제는 문자열당 삭제가 1회뿐이라 해당하지 않는다.

## 코너 케이스 및 실수 포인트

| 케이스 | 예 | 확인할 점 |
|---|---|---|
| `P = 1` | `1 PROGRAMMING` → `ROGRAMMING` | 앞 슬라이스가 빈 문자열, `erase(0, 1)` |
| `P = 길이` | `7 CONTEST` → `CONTES` | 마지막 글자 삭제, C의 시프트 루프가 널 문자만 복사 |
| 길이 1 문자열 | `1 A` → 빈 줄 | 빈 줄을 출력해야 하며 줄바꿈을 빠뜨리지 않는다 |
| `P` 대신 `P-1` 누락 | `4 MISSPELL` → `MISSELL`(오답) | 1-based/0-based 변환 |
| 버퍼 크기 | `char S[80]` | 80자 입력 시 널 문자 자리가 없어 미정의 동작 |

## 결론

이 문제는 문자열의 한 글자를 지우는 가장 기본적인 연산을 세 언어의 문자열 모델 위에서 다시 확인하게 한다. 가변 문자열의 제자리 삭제(C++), 널 종결 배열의 직접 이동(C), 불변 문자열의 재구성(Python)이 서로 다른 방식으로 같은 결과를 내며, 공통으로 챙길 것은 위치를 `P-1`로 바꾸는 한 줄이다.
