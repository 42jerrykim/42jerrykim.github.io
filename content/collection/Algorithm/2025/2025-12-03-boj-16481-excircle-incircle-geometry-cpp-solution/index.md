---
title: "[Algorithm] C++ 백준 16481번 원 전문가 진우 - 방접원과 내접원의 관계"
description: "삼각형의 세 방접원 반지름이 주어졌을 때 내접원의 반지름을 구하는 기하학 문제입니다. 방접원과 내접원의 수학적 관계식을 유도하여 O(1) 시간복잡도로 해결하는 풀이를 제시합니다."
categories:
- Algorithm
- Geometry
- Math
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16481
- cpp
- C++
- Geometry
- 기하
- 기하학
- Math
- 수학
- Circle
- 원
- Incircle
- 내접원
- Excircle
- 방접원
- Triangle
- 삼각형
- Formula
- 공식
- Mathematical Formula
- 수학공식
- Trigonometry
- 삼각법
- Area
- 넓이
- Semiperimeter
- 반둘레
- Radius
- 반지름
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(1)
- Constant Time
- 상수시간
- Competitive Programming
- 경쟁프로그래밍
- Problem Solving
- 문제해결
- Editorial
- 에디토리얼
- Data Structures
- 자료구조
- Edge Cases
- 코너 케이스
- Floating Point
- 부동소수점
- Precision
- 정밀도
- Double
- 더블
- Special Judge
- 스페셜저지
- Flow Cup
- 플로우컵
- 원전문가
- 진우
- Subtask
- 서브태스크
date: 2025-12-03
lastmod: 2025-12-03
image: wordcloud.png
---

## 문제 정보

- **문제 링크**: [https://www.acmicpc.net/problem/16481](https://www.acmicpc.net/problem/16481)
- **난이도**: Silver III
- **분류**: 수학, 기하학
- **시간 제한**: 1초 (추가 시간 없음)
- **메모리 제한**: 512 MB

## 문제 요약

평면에 있는 삼각형 ABC의 서로 다른 위치에 있는 세 방접원의 반지름의 길이가 r1, r2, r3일 때, 삼각형 ABC의 내접원의 반지름을 구하는 문제입니다.

**입력**: r1, r2, r3 (1,000 이하의 양의 정수)

**출력**: 내접원의 반지름 (절대/상대 오차 10^-6 허용)

## 입출력 예제

```
입력 1:
4 4 4

출력 1:
1.3333333333
```

```
입력 2:
18 13 14

출력 2:
4.904191617
```

## 접근 방법

### 핵심 수학 공식 유도

삼각형의 기하학적 특성을 활용하여 방접원과 내접원의 관계를 유도합니다.

**기본 정의**:
- 삼각형의 넓이: K
- 반둘레: s = (a + b + c) / 2
- 내접원 반지름: r = K / s
- 방접원 반지름:
  - r_a = K / (s - a)
  - r_b = K / (s - b)
  - r_c = K / (s - c)

**관계식 유도**:

각 방접원 반지름의 역수를 구하면:
- 1/r_a = (s - a) / K
- 1/r_b = (s - b) / K
- 1/r_c = (s - c) / K

이들을 모두 더하면:
```
1/r_a + 1/r_b + 1/r_c = [(s-a) + (s-b) + (s-c)] / K
                      = [3s - (a+b+c)] / K
                      = [3s - 2s] / K
                      = s / K
                      = 1/r
```

따라서 최종 공식은:

$$r = \frac{1}{\frac{1}{r_1} + \frac{1}{r_2} + \frac{1}{r_3}}$$

## 복잡도 분석

- **시간 복잡도**: O(1) - 단순 수학 계산
- **공간 복잡도**: O(1) - 상수 개의 변수만 사용

## 풀이 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    double r1, r2, r3;
    cin >> r1 >> r2 >> r3;
    
    // 내접원 반지름 공식: r = 1 / (1/r1 + 1/r2 + 1/r3)
    double r = 1.0 / (1.0/r1 + 1.0/r2 + 1.0/r3);
    
    cout << fixed << setprecision(10) << r << '\n';
    
    return 0;
}
```

## 알고리즘 설명

### 1단계: 입력 처리

세 방접원의 반지름 r1, r2, r3을 입력받습니다.

### 2단계: 내접원 반지름 계산

유도한 공식을 적용합니다:
- 1/r1 + 1/r2 + 1/r3을 먼저 계산
- 그 역수가 내접원의 반지름

### 3단계: 출력

소수점 10자리까지 출력하여 오차 조건(10^-6)을 만족시킵니다.

## 예제 검증

**예제 1**: r1 = r2 = r3 = 4
- 계산: r = 1 / (1/4 + 1/4 + 1/4) = 1 / (3/4) = 4/3 = 1.3333...

**예제 2**: r1 = 18, r2 = 13, r3 = 14
- 계산: r = 1 / (1/18 + 1/13 + 1/14)
- 1/18 + 1/13 + 1/14 = (13×14 + 18×14 + 18×13) / (18×13×14)
- = (182 + 252 + 234) / 3276
- = 668 / 3276
- r = 3276 / 668 ≈ 4.904191617

## 코너 케이스 체크리스트

- [x] 세 방접원 반지름이 모두 같은 경우 (정삼각형)
- [x] 방접원 반지름이 최소값(1)인 경우
- [x] 방접원 반지름이 최대값(1000)인 경우
- [x] 부동소수점 정밀도 처리

## 수학적 배경

### 방접원(Excircle)이란?

방접원은 삼각형의 한 변에 접하고, 나머지 두 변의 연장선에 접하는 원입니다. 삼각형에는 세 개의 방접원이 존재합니다.

### 내접원(Incircle)이란?

내접원은 삼각형의 세 변 모두에 내접하는 원입니다. 삼각형에는 정확히 하나의 내접원이 존재합니다.

### 기하학적 관계

방접원과 내접원의 반지름 사이의 관계식은 삼각형의 넓이와 반둘레를 통해 유도됩니다. 이 문제는 이러한 기하학적 관계를 활용하여 효율적으로 해결할 수 있습니다.

## 제출 전 점검

- [x] 입출력 형식 확인
- [x] 부동소수점 정밀도 (10자리 출력)
- [x] double 자료형 사용
- [x] 오차 범위 10^-6 충족

## 참고 자료

- [Baekjoon Online Judge](https://www.acmicpc.net/problem/16481)
- [방접원 - Wikipedia](https://en.wikipedia.org/wiki/Incircle_and_excircles_of_a_triangle)
- [삼각형의 내접원과 방접원](https://en.wikipedia.org/wiki/Incircle_and_excircles)

## 관련 문제

- BOJ 1085: 직사각형에서 탈출
- BOJ 3053: 택시 기하학
- BOJ 1002: 터렛


