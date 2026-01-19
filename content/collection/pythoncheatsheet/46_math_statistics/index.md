---
draft: true
title: "[Python Cheatsheet] 46. math & statistics - 수학/통계 함수"
slug: "math-and-statistics-sqrt-pow-log-sin-cos-tan-pi-e-ceil-floor-round-gcd"
description: "파이썬 math와 statistics 모듈을 빠르게 사용하기 위한 치트시트입니다. 기본 수학 함수, 삼각함수, 로그, 평균, 중앙값, 표준편차 등 핵심 함수를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 46
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - math
  - 수학
  - statistics
  - 통계
  - sqrt
  - pow
  - log
  - sin
  - cos
  - tan
  - pi
  - e
  - ceil
  - floor
  - round
  - factorial
  - gcd
  - lcm
  - mean
  - 평균
  - median
  - 중앙값
  - mode
  - 최빈값
  - stdev
  - 표준편차
  - variance
  - 분산
  - fsum
  - isclose
  - inf
  - nan
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - scientific
  - 과학
---
`math`는 기본 수학 함수를, `statistics`는 통계 함수를 제공하는 표준 라이브러리입니다. NumPy 없이도 기본적인 수학/통계 연산이 가능합니다.

## 언제 이 치트시트를 보나?

- **제곱근, 로그, 삼각함수** 등이 필요할 때
- **평균, 중앙값, 표준편차** 등 기초 통계가 필요할 때
- NumPy 없이 **가벼운 수학 연산**을 할 때

## math 모듈

### 상수

```python
import math

math.pi       # 3.141592653589793
math.e        # 2.718281828459045
math.tau      # 6.283185307179586 (2π)
math.inf      # 양의 무한대
math.nan      # Not a Number
```

### 기본 연산

```python
import math

# 제곱근
math.sqrt(16)        # 4.0

# 거듭제곱
math.pow(2, 3)       # 8.0
2 ** 3               # 8 (내장 연산자)

# 절대값
math.fabs(-3.5)      # 3.5
abs(-3.5)            # 3.5 (내장 함수)

# 올림/내림
math.ceil(3.2)       # 4
math.floor(3.8)      # 3
math.trunc(3.8)      # 3 (정수부만)

# 반올림
round(3.5)           # 4 (내장 함수)
round(3.14159, 2)    # 3.14
```

### 로그/지수

```python
import math

# 자연로그 (밑 e)
math.log(math.e)     # 1.0

# 밑 지정
math.log(100, 10)    # 2.0
math.log10(100)      # 2.0
math.log2(8)         # 3.0

# 지수
math.exp(1)          # 2.718... (e^1)
```

### 삼각함수

```python
import math

angle = math.pi / 4  # 45도

# 기본 삼각함수 (라디안)
math.sin(angle)      # 0.707...
math.cos(angle)      # 0.707...
math.tan(angle)      # 1.0

# 역삼각함수
math.asin(0.5)       # 0.523... (라디안)
math.acos(0.5)       # 1.047...
math.atan(1)         # 0.785...

# 각도 변환
math.degrees(math.pi)  # 180.0
math.radians(180)      # 3.14159...

# 직교좌표 → 극좌표
math.hypot(3, 4)     # 5.0 (빗변)
math.atan2(1, 1)     # 0.785... (각도)
```

### 팩토리얼, GCD, LCM

```python
import math

# 팩토리얼
math.factorial(5)    # 120 (5!)

# 최대공약수
math.gcd(12, 18)     # 6

# 최소공배수 (Python 3.9+)
math.lcm(4, 6)       # 12

# 여러 수의 GCD/LCM
math.gcd(12, 18, 24) # 6
math.lcm(4, 6, 8)    # 24
```

### 특수 함수

```python
import math

# 부동소수점 정밀 합계
math.fsum([0.1] * 10)  # 1.0 (sum은 0.999...9)

# 근사 비교
math.isclose(0.1 + 0.2, 0.3)  # True

# 무한/NaN 체크
math.isinf(math.inf)   # True
math.isnan(float('nan'))  # True

# 조합/순열 (Python 3.8+)
math.comb(5, 2)        # 10 (5C2)
math.perm(5, 2)        # 20 (5P2)
```

---

## statistics 모듈

### 평균

```python
import statistics

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 산술 평균
statistics.mean(data)           # 5.5

# 기하 평균 (Python 3.8+)
statistics.geometric_mean(data) # 4.528...

# 조화 평균
statistics.harmonic_mean(data)  # 3.414...

# 가중 평균 (Python 3.11+)
statistics.fmean([1, 2, 3], weights=[1, 2, 3])
```

### 중앙값

```python
import statistics

data = [1, 2, 3, 4, 5]

# 중앙값
statistics.median(data)         # 3

# 짝수 개일 때 낮은/높은 값
data_even = [1, 2, 3, 4]
statistics.median_low(data_even)   # 2
statistics.median_high(data_even)  # 3
```

### 최빈값

```python
import statistics

data = [1, 1, 2, 2, 2, 3, 3]

# 최빈값 (가장 빈번한 값)
statistics.mode(data)           # 2

# 여러 최빈값 (Python 3.8+)
statistics.multimode([1, 1, 2, 2, 3])  # [1, 2]
```

### 분산과 표준편차

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]

# 표본 분산 (n-1로 나눔)
statistics.variance(data)       # 4.571...

# 모집단 분산 (n으로 나눔)
statistics.pvariance(data)      # 4.0

# 표본 표준편차
statistics.stdev(data)          # 2.138...

# 모집단 표준편차
statistics.pstdev(data)         # 2.0
```

### 분위수 (Python 3.8+)

```python
import statistics

data = list(range(1, 101))  # 1~100

# 사분위수
statistics.quantiles(data)  # [25.5, 50.5, 75.5]

# n분위수
statistics.quantiles(data, n=10)  # 10분위수
```

### 상관계수와 선형회귀 (Python 3.10+)

```python
import statistics

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]

# 피어슨 상관계수
statistics.correlation(x, y)  # 0.774...

# 선형회귀
slope, intercept = statistics.linear_regression(x, y)
print(f"y = {slope}x + {intercept}")
# y = 0.6x + 2.2
```

## 예제: 기본 통계 분석

```python
import statistics

scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

print(f"개수: {len(scores)}")
print(f"평균: {statistics.mean(scores):.2f}")
print(f"중앙값: {statistics.median(scores)}")
print(f"표준편차: {statistics.stdev(scores):.2f}")
print(f"최소: {min(scores)}, 최대: {max(scores)}")

# 개수: 10
# 평균: 86.80
# 중앙값: 88.5
# 표준편차: 6.05
# 최소: 76, 최대: 95
```

## 자주 하는 실수

### 1. 부동소수점 비교

```python
# 위험: 부동소수점 오차
0.1 + 0.2 == 0.3  # False!

# 안전: isclose 사용
import math
math.isclose(0.1 + 0.2, 0.3)  # True
```

### 2. 정수 나눗셈

```python
import math

# 주의: //는 -∞ 방향, trunc는 0 방향
math.floor(-3.5)  # -4
math.trunc(-3.5)  # -3
-7 // 2           # -4
int(-7 / 2)       # -3
```

## 한눈에 정리

| 카테고리 | math | statistics |
|----------|------|------------|
| 기본 연산 | `sqrt`, `pow`, `ceil`, `floor` | - |
| 삼각함수 | `sin`, `cos`, `tan`, `radians` | - |
| 로그 | `log`, `log10`, `exp` | - |
| 중심경향 | - | `mean`, `median`, `mode` |
| 분산 | - | `stdev`, `variance` |
| 조합 | `comb`, `perm`, `factorial` | - |

## 참고

- [math - Python Docs](https://docs.python.org/3/library/math.html)
- [statistics - Python Docs](https://docs.python.org/3/library/statistics.html)
