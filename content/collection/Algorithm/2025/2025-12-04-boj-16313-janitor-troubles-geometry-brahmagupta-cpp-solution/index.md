---
title: "[Algorithm] C++ 백준 16313번 Janitor Troubles"
description: "최대 사각형 넓이 문제를 브라마굽타 공식으로 해결합니다. 원에 내접하는 사각형의 성질을 이용한 기하학 풀이를 알아봅니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
tags:
  - 백준
  - BOJ
  - 기하학
  - Geometry
  - 최대값
  - Maximum
  - 사각형
  - Quadrilateral
  - 넓이
  - Area
  - 브라마굽타
  - Brahmagupta
  - 공식
  - Formula
  - 원에내접
  - Cyclic
  - 우아한수학
  - Elegant
  - Mathematics
  - 수학올림피아드
  - Mathematical Olympiad
  - 고급알고리즘
  - Advanced Algorithm
  - ICPC
  - 경시대회
  - Programming Contest
  - C++
  - 구현
  - Implementation
  - 수학적증명
  - Mathematical Proof
  - 최적화
  - Optimization
  - 함수형
  - Functional
  - 문제풀이
  - Problem Solving
  - 알고리즘설계
  - Algorithm Design
  - 데이터구조
  - Data Structure
  - 성능최적화
  - Performance
  - 코딩테스트
  - Coding Test
  - 개발역량
  - Development Skill
  - 기술면접
  - Technical Interview
  - 알고리즘마스터
  - Algorithm Master
---

# BOJ 16313: Janitor Troubles - 최대 사각형 넓이 문제

**문제 링크**: [https://www.acmicpc.net/problem/16313](https://www.acmicpc.net/problem/16313)

## 문제 이해

주어진 네 개의 변의 길이로 만들 수 있는 사각형 중에서 **최대 넓이**를 구하는 문제입니다.

### 입력
- 네 개의 양의 정수: s1, s2, s3, s4 (변의 길이)

### 출력
- 만들 수 있는 최대 넓이 (상대오차 또는 절대오차 10^-6 이내)

### 예제
| 입력 | 출력 |
|------|------|
| 3 3 3 3 | 9 |
| 1 2 1 1 | 1.299038105676658 |
| 2 2 1 4 | 3.307189138830738 |

## 풀이 방법

### 핵심 원리: 브라마굽타 공식 (Brahmagupta's Formula)

네 개의 변으로 만든 사각형 중 **최대 넓이를 갖는 사각형은 원에 내접하는 사각형**입니다.

원에 내접하는 사각형의 넓이는 다음 공식으로 계산됩니다:

$$A = \sqrt{(s-a)(s-b)(s-c)(s-d)}$$

여기서:
- $a, b, c, d$ = 네 변의 길이
- $s = \frac{a+b+c+d}{2}$ = 반둘레 (semi-perimeter)

### 왜 원에 내접하는 사각형이 최대인가?

일반적인 사각형의 넓이 공식은:

$$A = \sqrt{(s-a)(s-b)(s-c)(s-d) - abcd \cdot \cos^2\left(\frac{\alpha + \gamma}{2}\right)}$$

여기서 α와 γ는 마주보는 각입니다.

원에 내접하는 사각형은 마주보는 각의 합이 180°이므로:
$$\cos\left(\frac{\alpha + \gamma}{2}\right) = \cos(90°) = 0$$

따라서 코사인 항이 0이 되어 **넓이가 최대**가 됩니다.

## 해결 코드

```cpp
// https://42jerrykim.github.io 에서 더 많은 정보를 확인할 수 있습니다.
#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    double a, b, c, d;
    cin >> a >> b >> c >> d;
    
    // 반둘레 계산
    double s = (a + b + c + d) / 2.0;
    
    // 브라마굽타 공식으로 최대 넓이 계산
    double area = sqrt((s - a) * (s - b) * (s - c) * (s - d));
    
    cout << fixed << setprecision(15) << area << '\n';
    
    return 0;
}
```

## 예제 검증

### 예제 1: 정사각형 (3 3 3 3)
- 반둘레: s = (3+3+3+3)/2 = 6
- 넓이: √(3×3×3×3) = √81 = 9 ✓

### 예제 2: (1 2 1 1)
- 반둘레: s = 5/2 = 2.5
- 넓이: √(1.5 × 0.5 × 1.5 × 1.5) = √(1.6875) ≈ 1.299 ✓

### 예제 3: (2 2 1 4)
- 반둘레: s = 9/2 = 4.5
- 넓이: √(2.5 × 2.5 × 3.5 × 0.5) = √(10.9375) ≈ 3.307 ✓

## 알고리즘 분석

| 항목 | 내용 |
|------|------|
| **시간복잡도** | O(1) |
| **공간복잡도** | O(1) |
| **핵심 개념** | 기하학, 브라마굽타 공식 |
| **자료구조** | 없음 |
| **알고리즘** | 수학 공식 적용 |

## 수학적 증명

### 쿨론의 정리 (Ptolemy's Theorem)
원에 내접하는 사각형 ABCD에 대해:
$$|AC| \cdot |BD| = |AB| \cdot |CD| + |AD| \cdot |BC|$$

### 대각선과 각의 관계
원에 내접하는 사각형에서 마주보는 각의 합이 180°라는 성질로부터:
$$\cos(\alpha + \gamma) = -1$$

이를 통해 코사인 항이 0이 되고, 최대 넓이 조건이 성립합니다.

## 실전 팁

1. **정밀도**: setprecision(15)로 충분한 소수점 자리수를 보장합니다.
2. **부동소수점 오류**: `fixed`를 사용하여 고정 소수점 표기를 합니다.
3. **제약 조건**: 2si < Σsj가 만족하면 항상 사각형을 만들 수 있습니다.

## 관련 알고리즘

- **헤론의 공식**: 삼각형의 넓이를 세 변의 길이로 구하는 공식
- **코사인 법칙**: 각도를 모를 때 삼각형의 변 계산
- **삼각형 부등식**: 변의 길이 제약 조건

## 출처

- **문제**: ICPC > Regionals > Europe > Northwestern European Regional Contest > Benelux Algorithm Programming Contest > BAPC 2018 J번
- **알고리즘 분류**: 기하학 (Geometry), 수학 (Mathematics)

---

**작성일**: 2025-12-04  
**마지막 수정일**: 2025-12-04  
**난이도**: 🟡 중상  
**풀이 시간**: 10분

