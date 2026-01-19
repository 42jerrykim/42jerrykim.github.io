---
draft: true
title: "[Python Cheatsheet] 29. operator - 연산자 함수와 효율적 접근자"
slug: "operator-itemgetter-attrgetter-methodcaller-functional-sorting-lambda"
description: "파이썬 operator 모듈을 빠르게 사용하기 위한 치트시트입니다. itemgetter, attrgetter, methodcaller와 연산자 함수들을 활용한 정렬, 맵핑, 함수형 프로그래밍 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 29
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - operator
  - 연산자
  - itemgetter
  - attrgetter
  - methodcaller
  - functional
  - 함수형
  - sorting
  - 정렬
  - key-function
  - 키함수
  - lambda
  - 람다
  - performance
  - 성능
  - add
  - mul
  - eq
  - lt
  - gt
  - getitem
  - setitem
  - contains
  - reduce
  - map
  - filter
  - functools
  - itertools
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - tuple-unpacking
  - 튜플언패킹
  - dict-sorting
  - 딕셔너리정렬
---
`operator` 모듈은 **파이썬 연산자를 함수로 제공**합니다. `itemgetter`, `attrgetter`는 람다보다 빠르고 가독성 좋은 키 함수를 만들 때 유용합니다.

## 언제 이 치트시트를 보나?

- `sorted()`나 `max()`에서 **키 함수**가 필요할 때
- 람다 대신 **더 빠르고 명확한** 접근자가 필요할 때
- `functools.reduce()`와 함께 **연산자 함수**를 쓸 때

## 핵심 접근자

```python
from operator import itemgetter, attrgetter, methodcaller

# itemgetter: 인덱스/키로 항목 접근
itemgetter(1)           # lambda x: x[1]
itemgetter('name')      # lambda x: x['name']
itemgetter(0, 2)        # lambda x: (x[0], x[2])

# attrgetter: 속성 접근
attrgetter('name')      # lambda x: x.name
attrgetter('a.b')       # lambda x: x.a.b (중첩)

# methodcaller: 메서드 호출
methodcaller('upper')   # lambda x: x.upper()
methodcaller('split', '-')  # lambda x: x.split('-')
```

## 최소 예제

### 1. 정렬 키로 사용

```python
from operator import itemgetter, attrgetter

# 리스트 of 튜플 정렬
data = [('alice', 25), ('bob', 30), ('charlie', 20)]

# 두 번째 요소(나이)로 정렬
sorted(data, key=itemgetter(1))
# [('charlie', 20), ('alice', 25), ('bob', 30)]

# 딕셔너리 리스트 정렬
users = [
    {'name': 'alice', 'age': 25},
    {'name': 'bob', 'age': 30},
    {'name': 'charlie', 'age': 20}
]
sorted(users, key=itemgetter('age'))

# 객체 리스트 정렬
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

users = [User('alice', 25), User('bob', 30)]
sorted(users, key=attrgetter('age'))
```

### 2. 복합 키 정렬

```python
from operator import itemgetter

data = [
    ('HR', 'alice', 50000),
    ('IT', 'bob', 60000),
    ('HR', 'charlie', 55000),
    ('IT', 'diana', 58000)
]

# 부서 → 급여 순 정렬
sorted(data, key=itemgetter(0, 2))
# [('HR', 'alice', 50000), ('HR', 'charlie', 55000), 
#  ('IT', 'diana', 58000), ('IT', 'bob', 60000)]
```

### 3. max/min과 함께

```python
from operator import itemgetter

scores = {'alice': 85, 'bob': 92, 'charlie': 78}

# 최고 점수 학생
max(scores.items(), key=itemgetter(1))  # ('bob', 92)

# 최저 점수 학생
min(scores.items(), key=itemgetter(1))  # ('charlie', 78)
```

### 4. methodcaller 활용

```python
from operator import methodcaller

words = ['Hello', 'WORLD', 'Python']

# 모두 소문자로
list(map(methodcaller('lower'), words))
# ['hello', 'world', 'python']

# 특정 문자로 분할
lines = ['a-b-c', 'x-y-z']
list(map(methodcaller('split', '-'), lines))
# [['a', 'b', 'c'], ['x', 'y', 'z']]

# 조건 필터링
strings = ['hello', 'world', 'python', 'java']
list(filter(methodcaller('startswith', 'p'), strings))
# ['python']
```

### 5. 연산자 함수

```python
from operator import add, mul, sub, truediv, eq, lt, gt
from functools import reduce

# reduce와 함께
numbers = [1, 2, 3, 4, 5]
reduce(add, numbers)  # 15 (1+2+3+4+5)
reduce(mul, numbers)  # 120 (1*2*3*4*5)

# 비교 함수
eq(5, 5)   # True (==)
lt(3, 5)   # True (<)
gt(3, 5)   # False (>)
```

### 6. 중첩 속성 접근

```python
from operator import attrgetter

class Address:
    def __init__(self, city):
        self.city = city

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

people = [
    Person('Alice', Address('Seoul')),
    Person('Bob', Address('Busan')),
    Person('Charlie', Address('Incheon'))
]

# 중첩 속성으로 정렬
sorted(people, key=attrgetter('address.city'))
# Busan, Incheon, Seoul 순
```

## 주요 연산자 함수

```python
from operator import *

# 산술 연산
add(a, b)       # a + b
sub(a, b)       # a - b
mul(a, b)       # a * b
truediv(a, b)   # a / b
floordiv(a, b)  # a // b
mod(a, b)       # a % b
pow(a, b)       # a ** b
neg(a)          # -a

# 비교 연산
eq(a, b)        # a == b
ne(a, b)        # a != b
lt(a, b)        # a < b
le(a, b)        # a <= b
gt(a, b)        # a > b
ge(a, b)        # a >= b

# 논리 연산
and_(a, b)      # a and b (키워드라 언더스코어)
or_(a, b)       # a or b
not_(a)         # not a

# 시퀀스 연산
getitem(seq, i)     # seq[i]
setitem(seq, i, v)  # seq[i] = v
delitem(seq, i)     # del seq[i]
contains(seq, v)    # v in seq
concat(a, b)        # a + b (시퀀스)
```

## 성능 비교

```python
from operator import itemgetter
import timeit

data = [(i, i*2) for i in range(1000)]

# lambda vs itemgetter
lambda_time = timeit.timeit(
    lambda: sorted(data, key=lambda x: x[1]), number=1000
)
itemgetter_time = timeit.timeit(
    lambda: sorted(data, key=itemgetter(1)), number=1000
)

# itemgetter가 약 10-20% 빠름
```

## 자주 하는 실수

### 1. 호출 vs 객체 혼동

```python
from operator import itemgetter

# 잘못된 사용 - itemgetter를 호출해야 함
# sorted(data, key=itemgetter)  # TypeError

# 올바른 사용
sorted(data, key=itemgetter(1))  # itemgetter(1)이 callable 반환
```

### 2. 없는 키/인덱스

```python
from operator import itemgetter

data = [{'a': 1}, {'a': 2, 'b': 3}]

# KeyError 발생
# sorted(data, key=itemgetter('b'))

# 해결: 기본값이 있는 lambda 또는 사전 필터링
sorted(data, key=lambda x: x.get('b', 0))
```

## 한눈에 정리

| 목적 | 도구 | 예시 |
|------|------|------|
| 인덱스/키 접근 | `itemgetter` | `itemgetter(1)`, `itemgetter('name')` |
| 속성 접근 | `attrgetter` | `attrgetter('age')`, `attrgetter('a.b')` |
| 메서드 호출 | `methodcaller` | `methodcaller('upper')` |
| 연산 함수화 | `add`, `mul`, etc. | `reduce(add, numbers)` |

## 참고

- [operator - Python Docs](https://docs.python.org/3/library/operator.html)
- [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
