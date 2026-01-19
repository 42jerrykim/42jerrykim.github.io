---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 47. decimal & fractions - 정밀 수치 연산"
slug: "decimal-fraction-precision-finance-scientific-guide"
description: "파이썬 decimal과 fractions 모듈을 빠르게 사용하기 위한 치트시트입니다. 부동소수점 오차 없는 십진 연산, 분수 연산, 금융/과학 계산 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 47
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - decimal
  - Decimal
  - 십진법
  - fractions
  - Fraction
  - 분수
  - precision
  - 정밀도
  - floating-point
  - 부동소수점
  - accuracy
  - 정확도
  - finance
  - 금융
  - money
  - 돈
  - currency
  - 통화
  - rounding
  - 반올림
  - ROUND_HALF_UP
  - getcontext
  - scientific
  - 과학
  - rational
  - 유리수
  - gcd
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`decimal`은 **부동소수점 오차 없는 십진 연산**을, `fractions`는 **분수 연산**을 제공합니다. 금융 계산, 과학 계산 등 정밀도가 중요한 곳에서 사용합니다.

## 언제 이 치트시트를 보나?

- **금융/회계** 계산에서 정확한 소수점이 필요할 때
- **부동소수점 오차**를 피하고 싶을 때 (`0.1 + 0.2 != 0.3`)
- **분수** 연산이 필요할 때

## 부동소수점 문제

```python
# float의 한계
print(0.1 + 0.2)         # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False!

# 누적 오차
total = sum([0.1] * 10)
print(total)             # 0.9999999999999999
```

---

## decimal 모듈

### 기본 사용

```python
from decimal import Decimal

# 문자열로 생성 (권장)
d1 = Decimal('0.1')
d2 = Decimal('0.2')

print(d1 + d2)           # 0.3
print(d1 + d2 == Decimal('0.3'))  # True

# 정수로 생성
d3 = Decimal(10)

# float로 생성 (비권장 - 오차 포함)
d4 = Decimal(0.1)        # 0.1000000000000000055511151...
```

### 정밀도 설정

```python
from decimal import Decimal, getcontext

# 전역 정밀도 설정
getcontext().prec = 4

print(Decimal('1') / Decimal('3'))  # 0.3333

# 높은 정밀도
getcontext().prec = 50
print(Decimal('1') / Decimal('3'))
# 0.33333333333333333333333333333333333333333333333333
```

### 반올림 모드

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, ROUND_CEILING

d = Decimal('2.345')

# 소수점 2자리로 반올림
d.quantize(Decimal('0.01'))                    # 2.35 (기본: ROUND_HALF_EVEN)
d.quantize(Decimal('0.01'), ROUND_HALF_UP)     # 2.35 (사사오입)
d.quantize(Decimal('0.01'), ROUND_DOWN)        # 2.34 (버림)
d.quantize(Decimal('0.01'), ROUND_CEILING)     # 2.35 (올림)

# 정수로 반올림
Decimal('2.5').quantize(Decimal('1'), ROUND_HALF_UP)  # 3
```

### 금융 계산 예제

```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_tax(price, tax_rate):
    """세금 계산 (소수점 이하 버림)"""
    price = Decimal(str(price))
    tax_rate = Decimal(str(tax_rate))
    tax = price * tax_rate
    return tax.quantize(Decimal('1'), ROUND_DOWN)

def calculate_total(items):
    """총액 계산"""
    total = sum(Decimal(str(item)) for item in items)
    return total.quantize(Decimal('0.01'), ROUND_HALF_UP)

# 사용
items = [10.99, 23.50, 5.99]
total = calculate_total(items)
print(f"Total: ${total}")  # Total: $40.48

tax = calculate_tax(40.48, 0.1)
print(f"Tax: ${tax}")      # Tax: $4
```

### Decimal 유용한 메서드

```python
from decimal import Decimal

d = Decimal('123.456')

# 부호, 숫자, 지수
d.as_tuple()           # DecimalTuple(sign=0, digits=(1,2,3,4,5,6), exponent=-3)

# 비교
d.compare(Decimal('100'))  # Decimal('1') (d > 100)

# 특수값 체크
Decimal('Infinity').is_infinite()  # True
Decimal('NaN').is_nan()            # True

# 정규화 (후행 0 제거)
Decimal('10.00').normalize()       # Decimal('1E+1')

# 복사 (부호 변경)
d.copy_abs()           # 123.456
d.copy_negate()        # -123.456
```

---

## fractions 모듈

### 기본 사용

```python
from fractions import Fraction

# 분수 생성
f1 = Fraction(1, 3)       # 1/3
f2 = Fraction(2, 6)       # 자동 약분 → 1/3
f3 = Fraction('3/4')      # 문자열로
f4 = Fraction(0.5)        # float로 (정확히 변환)
f5 = Fraction('0.125')    # 문자열 소수

print(f1)                 # 1/3
print(f1.numerator)       # 1
print(f1.denominator)     # 3
```

### 분수 연산

```python
from fractions import Fraction

a = Fraction(1, 3)
b = Fraction(1, 4)

# 사칙연산
print(a + b)    # 7/12
print(a - b)    # 1/12
print(a * b)    # 1/12
print(a / b)    # 4/3

# 거듭제곱
print(a ** 2)   # 1/9

# 비교
print(a > b)    # True
```

### float ↔ Fraction 변환

```python
from fractions import Fraction

# float → Fraction
f = Fraction(0.5)
print(f)              # 1/2

# 0.1은 정확히 표현 불가
f = Fraction(0.1)
print(f)              # 3602879701896397/36028797018963968

# 문자열로 정확하게
f = Fraction('0.1')
print(f)              # 1/10

# Fraction → float
f = Fraction(1, 3)
print(float(f))       # 0.3333333333333333
```

### 근사 분수 (limit_denominator)

```python
from fractions import Fraction
import math

# π의 근사 분수
pi_fraction = Fraction(math.pi)
print(pi_fraction)
# 884279719003555/281474976710656 (정확한 변환)

# 분모 제한으로 근사
print(pi_fraction.limit_denominator(10))    # 22/7
print(pi_fraction.limit_denominator(100))   # 311/99
print(pi_fraction.limit_denominator(1000))  # 355/113
```

### 실용 예제

```python
from fractions import Fraction

# 비율 계산
total = 100
parts = [Fraction(1, 4), Fraction(1, 3), Fraction(5, 12)]
print(sum(parts))  # 1 (모든 비율의 합)

# 각 파트의 실제 값
for i, part in enumerate(parts):
    print(f"Part {i+1}: {float(part * total):.2f}")
# Part 1: 25.00
# Part 2: 33.33
# Part 3: 41.67
```

## Decimal vs Fraction vs float

```python
from decimal import Decimal
from fractions import Fraction

# 1/3 표현
print(1/3)                    # 0.3333333333333333
print(Decimal('1') / 3)       # 0.3333333333333333... (정밀도만큼)
print(Fraction(1, 3))         # 1/3 (정확)

# 0.1 + 0.2
print(0.1 + 0.2)              # 0.30000000000000004
print(Decimal('0.1') + Decimal('0.2'))  # 0.3
print(Fraction('0.1') + Fraction('0.2'))  # 3/10
```

## 자주 하는 실수

### 1. float로 Decimal 생성

```python
from decimal import Decimal

# 잘못된 방법
bad = Decimal(0.1)     # 오차 포함

# 올바른 방법
good = Decimal('0.1')  # 정확
```

### 2. 혼합 연산

```python
from decimal import Decimal

# float과 Decimal 혼합 불가
# Decimal('1.5') + 0.5  # TypeError

# 명시적 변환 필요
Decimal('1.5') + Decimal('0.5')  # OK
```

## 한눈에 정리

| 타입 | 용도 | 장점 | 단점 |
|------|------|------|------|
| `float` | 일반 계산 | 빠름 | 오차 있음 |
| `Decimal` | 금융/정밀 계산 | 십진 정확도 | 느림 |
| `Fraction` | 분수/비율 | 무손실 유리수 | 제한된 용도 |

## 참고

- [decimal - Python Docs](https://docs.python.org/3/library/decimal.html)
- [fractions - Python Docs](https://docs.python.org/3/library/fractions.html)
