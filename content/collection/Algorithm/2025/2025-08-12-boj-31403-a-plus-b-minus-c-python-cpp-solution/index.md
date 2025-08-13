---
title: "[Algorithm] C++ 백준 31403번 : A + B - C"
description: "백준 31403 A + B - C 문제를 Python과 C++로 풀이합니다. 숫자로 계산하는 A + B - C와 문자열을 이어붙인 뒤 int로 변환하여 C를 빼는 연산의 차이를 예제와 함께 설명하고, 빠른 입출력 코드, 복잡도, 테스트 팁까지 간결하게 정리했습니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "31403"
- "A + B - C"
- "문자열"
- "String"
- "Concatenation"
- "이어붙이기"
- "Parsing"
- "파싱"
- "입출력"
- "I/O"
- "Python"
- "파이썬"
- "C++"
- "CPP"
- "Implementation"
- "구현"
- "사칙연산"
- "덧셈"
- "뺄셈"
- "숫자연산"
- "정수"
- "문자열변환"
- "Type Conversion"
- "stoll"
- "stoi"
- "int"
- "문제풀이"
- "해설"
- "코딩테스트"
- "Coding Interview"
- "알고리즘"
- "기초문제"
- "쉬운문제"
- "Math"
- "수학"
- "빠른입출력"
- "Fast IO"
- "ios::sync_with_stdio(false)"
- "cin.tie(nullptr)"
- "sys.stdin.read"
- "시간복잡도"
- "공간복잡도"
- "Time Complexity"
- "Space Complexity"
- "Greedy"
- "Data Types"
- "자료형"
- "문자열처리"
- "문자열연산"
- "정수변환"
- "Edge Cases"
- "테스트케이스"
- "백준기초"
- "풀이정리"
image: "wordcloud.png"
---

백준 문제 [A + B - C (31403)](https://www.acmicpc.net/problem/31403) 는 숫자로 계산하는 `A + B - C`와 문자열로 이어붙인 뒤 수로 변환해 `- C`를 하는 두 가지 결과를 각각 출력하는 간단 구현 문제입니다.

## 문제 요약
- 입력: 한 줄에 하나씩 양의 정수 `A`, `B`, `C` (0으로 시작하지 않음)
- 출력:
  1) 숫자로 계산한 `A + B - C`
  2) 문자열로 `A`와 `B`를 이어붙여 정수로 변환한 뒤 `- C`

## 접근
- 첫 줄은 정수 덧셈/뺄셈 그대로 계산합니다.
- 둘째 줄은 `str(A) + str(B)`를 만든 뒤 정수로 변환해 `C`를 뺍니다.
- 입력 구분(공백/개행)과 무관하게 안정적으로 파싱합니다.

## Python 풀이

```python
# 더 많은 정보: https://42jerrykim.github.io
import sys

t = sys.stdin.read().split()
a, b, c = int(t[0]), int(t[1]), int(t[2])

print(a + b - c)
print(int(t[0] + t[1]) - c)
```

## C++ 풀이

```cpp
// 더 많은 정보: https://42jerrykim.github.io
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string sa, sb, sc;
    if (!(cin >> sa >> sb >> sc)) return 0;

    long long a = stoll(sa);
    long long b = stoll(sb);
    long long c = stoll(sc);

    cout << (a + b - c) << '\n';
    cout << (stoll(sa + sb) - c) << '\n';
    return 0;
}
```

## 복잡도
- 시간: O(1) (자리수 결합 및 변환은 최대 자릿수에 비례하나 입력 범위가 작음)
- 공간: O(1)

## 예시
입력
```
3
4
5
```

출력
```
2
29
```


