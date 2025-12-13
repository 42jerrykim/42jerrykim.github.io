---
title: "[Algorithm] C++ 백준 16313번: Janitor Troubles"
description: "네 변의 길이로 만드는 최대 사각형 넓이 문제를 브라마굽타 공식으로 해결합니다. 원에 내접하는 사각형의 성질, 정당성 증명, 부동소수점 정밀도 처리를 다룬 기하학 풀이입니다."
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Geometry
tags:
  - Algorithm
  - 알고리즘
  - BOJ
  - 백준
  - Problem-16313
  - C++
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
  - 구현
  - Implementation
  - 수학적증명
  - Mathematical Proof
  - 최적화
  - Optimization
  - 문제풀이
  - Problem Solving
  - 알고리즘설계
  - Algorithm Design
  - Data Structure
  - 자료구조
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - Proof of Correctness
  - 정당성 증명
  - Edge Cases
  - 코너 케이스
  - Pitfalls
  - 실수 포인트
  - Competitive Programming
  - 경쟁프로그래밍
  - 부동소수점
  - Floating Point
  - 정밀도
  - Precision
  - 수학
  - Math
  - 페톨레마이오스정리
  - Ptolemy
image: "wordcloud.png"
---

# BOJ 16313: Janitor Troubles - 최대 사각형 넓이 문제

**문제 링크**: [https://www.acmicpc.net/problem/16313](https://www.acmicpc.net/problem/16313)

## 문제 요약

주어진 네 개의 변의 길이로 만들 수 있는 사각형 중에서 **최대 넓이**를 구하는 문제입니다. 입력된 네 변으로 도형을 만들 때, 모든 가능한 배치에서 가장 큰 넓이를 계산해야 합니다.

### 제한/스펙
- **입력**: 4개의 양의 정수 (변의 길이)
- **정밀도**: 상대오차 또는 절대오차 10⁻⁶ 이내

### 입력/출력 형식

**입력**:
```
s1 s2 s3 s4
```

**출력**:
```
최대 넓이 (실수)
```

### 예제

| 입력 | 출력 |
|------|------|
| 3 3 3 3 | 9 |
| 1 2 1 1 | 1.299038105676658 |
| 2 2 1 4 | 3.307189138830738 |

## 접근 개요 (아이디어 스케치)

**핵심 관찰**: 주어진 네 변의 길이로 만들 수 있는 사각형은 무수히 많지만, **원에 내접하는 사각형이 최대 넓이를 가집니다**. 이는 원에 내접하는 사각형의 성질(마주보는 각의 합 = 180°)로부터 도출됩니다.

**알고리즘**: 브라마굽타 공식을 직접 적용하면 O(1) 시간에 답을 구할 수 있습니다.

## 알고리즘 설계

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

## 복잡도

| 항목 | 내용 |
|------|------|
| **시간복잡도** | O(1) |
| **공간복잡도** | O(1) |

간단한 산술 연산과 제곱근 계산만 수행하므로 상수 시간에 해결됩니다.

## 구현

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
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

## 정당성 증명

### 쿨론의 정리 (Ptolemy's Theorem)
원에 내접하는 사각형 ABCD에 대해:
$$|AC| \cdot |BD| = |AB| \cdot |CD| + |AD| \cdot |BC|$$

### 대각선과 각의 관계
원에 내접하는 사각형에서 마주보는 각의 합이 180°라는 성질로부터:
$$\cos(\alpha + \gamma) = -1$$

이를 통해 코사인 항이 0이 되고, 최대 넓이 조건이 성립합니다.

## 코너 케이스 체크리스트

| 케이스 | 설명 | 검증 |
|--------|------|------|
| 정사각형 | 모든 변이 같음 (3 3 3 3) | 넓이 = a² |
| 직사각형 | 마주보는 변이 같음 (3 4 3 4) | 넓이 = 3 × 4 = 12 |
| 극단적 값 | 한 변이 매우 작음 (1 10 10 10) | s = 15.5, 거의 0에 가까움 |
| 이등변사다리꼴 | 다리가 같음 (2 5 2 5) | 원에 내접 가능 |
| 부동소수점 오차 | 경계값에서의 오차 누적 | setprecision(15) 필수 |

## 제출 전 점검

- [ ] **입출력 형식**: 네 변의 길이를 공백으로 구분하여 읽음
- [ ] **부동소수점 정밀도**: `fixed`와 `setprecision(15)` 사용 확인
- [ ] **수식 계산**: 반둘레 계산 시 정수 나눗셈 방지 (2.0 사용)
- [ ] **오버플로우**: double 범위 내 모든 값이 처리됨 (음수 체크 필수)
- [ ] **제약 조건**: 삼각형 부등식 만족 확인 (일반적으로 문제에서 보장)
- [ ] **개행 문자**: 출력 후 개행 확인

## 실전 팁

1. **정밀도**: setprecision(15)로 충분한 소수점 자리수를 보장합니다.
2. **부동소수점 오류**: `fixed`를 사용하여 고정 소수점 표기를 합니다.
3. **제약 조건**: 2si < Σsj가 만족하면 항상 사각형을 만들 수 있습니다.

## 관련 알고리즘

- **헤론의 공식**: 삼각형의 넓이를 세 변의 길이로 구하는 공식
- **코사인 법칙**: 각도를 모를 때 삼각형의 변 계산
- **삼각형 부등식**: 변의 길이 제약 조건
