---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 01. Basic - 연산자/변수/출력/형변환"
slug: "basic-basics-syntax-operators-arithmetic-precedence-variables-types"
description: "파이썬 기본 문법 치트시트입니다. 연산자, 변수, 출력, 형변환부터 walrus operator(:=), f-string 디버깅(=) 같은 최신 문법까지 실전 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 1
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - basic
  - basics
  - 기초
  - syntax
  - 문법
  - operators
  - 연산자
  - arithmetic
  - 산술
  - precedence
  - 우선순위
  - augmented-assignment
  - 증강연산자
  - variables
  - 변수
  - assignment
  - 할당
  - walrus-operator
  - 할당표현식
  - assignment-expression
  - types
  - 자료형
  - int
  - float
  - bool
  - str
  - casting
  - type-conversion
  - 형변환
  - print
  - output
  - 출력
  - input
  - 입력
  - comments
  - 주석
  - docstring
  - 문서화
  - strings
  - 문자열
  - formatting
  - f-string
  - f-string-debugging
  - 디버깅출력
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - readability
  - 가독성
  - debugging
  - 디버깅
  - beginner
  - 초보
  - tutorial
  - 튜토리얼
  - python38
  - python39
  - python310
last_modified_at: 2023-01-17
date: 2022-01-17
categories: Python
header:
  teaser: /assets/images/2023/Screenshot_2023-01-17_at_20-55-19_WelcometoPython.org.png
---
우리는 어디에선가 시작할 필요가 있다. 바로 여기서 그 시작점이다.

> [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)에서 내용을 가지고 왔다.
> 
> 파이썬은 배우기 쉬운 언어이면서 강력한 언어이다. 파이썬은 우아한 문법과 다이나믹 파입을 지원한다. 이것들은 자연스럽게 어우러져 스크립팅과 빠른 어플리케이션 개발하는데 있어서 이상적인 언어로 만든다.

## 산술 연산자

우선 순위가 높은 순서로 나열 하였다.

|Operators|Operation|Example|
|:---|:---|:---|
|**|Exponent|2 ** 3 = 8|
|%|Modulus/Remainder|22 % 8 = 6|
|//|Integer division|22 // 8 = 2|
|/|Division|22 / 8 = 2.75|
|*|Multiplication|3 * 3 = 9|
|-|Subtraction|5 - 2 = 3|
|+|Addition|2 + 2 = 4|

```python
>>> 2 + 3 * 6
## 20

>>> (2 + 3) * 6
## 30

>>> 2 ** 8
#256

>>> 23 // 7
## 3

>>> 23 % 7
## 2

>>> (5 - 1) * ((7 + 1) / (3 - 1))
## 16.0
```

## 증강 연산자

|Operator|Equivalent|
|:---|:---|
|var += 1|var = var + 1|
|var -= 1|var = var - 1|
|var *= 1|var = var * 1|
|var /= 1|var = var / 1|
|var %= 1|var = var % 1|

```python
>>> greeting = 'Hello'
>>> greeting += ' world!'
>>> greeting
## 'Hello world!'

>>> number = 1
>>> number += 1
>>> number
## 2

>>> my_list = ['item']
>>> my_list *= 3
>>> my_list
## ['item', 'item', 'item']
```

## 자료형

|Data Type|Examples
|:---|:---|
|Integers|-2, -1, 0, 1, 2, 3, 4, 5|
|Floating-point numbers|-1.25, -1.0, --0.5, 0.0, 0.5, 1.0, 1.25|
|Strings|'a', 'aa', 'aaa', 'Hello!', '11 cats'|

## 결합(Concatenation)과 복사

* 문자열 결합
    ```python
    >>> 'Alice' 'Bob'
    # 'AliceBob'
    ```
* 문자열 복사
    ```python
    >>> 'Alice' * 5
    # 'AliceAliceAliceAliceAlice'
    ```

## 변수

1. 한 단어로 변수를 지정할 수 있다.
    ```python
    >>> # bad
    >>> my variable = 'Hello'

    >>> # good
    >>> var = 'Hello'
    ```

2. 문자, 숫자, `_`만 사용 할 수 있다.
    ```python
    >>> # bad
    >>> %$@variable = 'Hello'

    >>> # good
    >>> my_var = 'Hello'

    >>> # good
    >>> my_var_2 = 'Hello'
    ```

3. 숫자로 시작 할 수 없다.
    ```python
    >>> # this wont work
    >>> 23_var = 'hello'
    ```

## 주석

* 내장 주석
    ```python
    # This is a comment
    ```

* 다중라인 주석
    ```python
    # This is a
    # multiline comment
    ```

* 코드와 함께 사용하기
    ```python
    a = 1  # initialization
    ```
    > 주석 앞에 2개의 띄어쓰기가 있어야 한다. 

* 함수 주석
    ```python
    def foo():
        """
        This is a function docstring
        You can also use:
        ''' Function Docstring '''
        """
    ```

## print() 함수

`print()`함수는 파라미터로 들어온 변수를 출력한다. 다중 변수를 처리 할 수 있으며, 부동 소수점 숫자와 문자열을 포함한다. 문자열은 쌍따옴표 없지 출력하며, 파라미터 사이에 띄어쓰기를 포함하여 출력하기 때문에 출력 형식을 조절하기 편하다.

```python
>>> print('Hello world!')
## Hello world!

>>> a = 1
>>> print('Hello world!', a)
## Hello world! 1
```

### end 키워드

`end` 키워드는 출력된 결과물에서 줄바꿈을 다른 문자로 변경 할 수 있다.

```python
phrase = ['printed', 'with', 'a', 'dash', 'in', 'between']
>>> for word in phrase:
...     print(word, end='-')
...
## printed-with-a-dash-in-between-
```

### sep 키워드

`sep` 키워드는 구분자를 바꿀수 있다.

```python
print('cats', 'dogs', 'mice', sep=',')
## cats,dogs,mice
```

## input() 함수

`input()` 함수는 사용자의 입력을 문자열로 받아드린다.

```python
>>> print('What is your name?')   # ask for their name
>>> my_name = input()
>>> print('Hi, {}'.format(my_name))
## What is your name?
## Martha
## Hi, Martha
```

`input()` 함수는 `print()` 함수를 사용하지 않고 기본 메시지를 출력 할 수 있다.

```python
>>> my_name = input('What is your name? ')  # default message
>>> print('Hi, {}'.format(my_name))
## What is your name? Martha
## Hi, Martha
```

## len() 함수

문자열, 리스트(List), 사전(Dictionary)등 변수의 길이를 반환한다.

```python
>>> len('hello')
## 5

>>> len(['cat', 3, 'dog'])
## 3
```

> 비어 있음을 테스트 할때는 len()을 사용하지 않고 변수를 바로 사용하는것이 좋다.

아래의 코드는 비어 있음을 테스트 하는 예시이다.

```python
>>> a = [1, 2, 3]

## bad
>>> if len(a) > 0:  # evaluates to True
...     print("the list is not empty!")
...
## the list is not empty!

## good
>>> if a: # evaluates to True
...     print("the list is not empty!")
...
## the list is not empty!
```

## str(), int(), and float() 함수

이 함수들은 변수의 타입을 바꾸는데 사용한다. 예를 들어 실수나 정수를 문자열로 바꿀때 사용한다.

```python
>>> str(29)
## '29'

>>> str(-3.14)
## '-3.14'
```

또는 문자열을 실수나 정수로 바꿀수 있다.

```python
>>> int('11')
## 11

>>> float('3.14')
## 3.14
```

## Walrus Operator `:=` (Py3.8+)

할당 표현식(Assignment Expression)이라고도 불리는 walrus operator는 값을 변수에 할당하면서 동시에 그 값을 표현식으로 사용할 수 있게 해준다.

```python
# 기존 방식
line = input()
while line != "quit":
    print(line)
    line = input()

# walrus operator 사용
while (line := input()) != "quit":
    print(line)
```

```python
# 리스트에서 조건부 필터링
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 기존 방식
filtered = []
for x in data:
    y = x * 2
    if y > 10:
        filtered.append(y)

# walrus operator 사용
filtered = [y for x in data if (y := x * 2) > 10]
print(filtered)  # [12, 14, 16, 18, 20]
```

```python
# 정규식 매칭
import re

text = "Hello, my email is test@example.com"

# 기존 방식
match = re.search(r'\S+@\S+', text)
if match:
    print(match.group())

# walrus operator 사용
if (match := re.search(r'\S+@\S+', text)):
    print(match.group())
```

```python
# 파일 읽기
# 기존 방식
while True:
    chunk = file.read(1024)
    if not chunk:
        break
    process(chunk)

# walrus operator 사용
while (chunk := file.read(1024)):
    process(chunk)
```

> **주의**: walrus operator는 코드를 간결하게 만들 수 있지만, 과도하게 사용하면 가독성이 떨어질 수 있다. 명확성이 우선!

## f-string 디버깅 `=` (Py3.8+)

f-string에서 `=`를 사용하면 변수명과 값을 함께 출력할 수 있다. 디버깅할 때 매우 유용하다.

```python
name = "Alice"
age = 30
score = 95.5

# 기존 방식
print(f"name={name}, age={age}, score={score}")
# name=Alice, age=30, score=95.5

# f-string = 사용 (Py3.8+)
print(f"{name=}, {age=}, {score=}")
# name='Alice', age=30, score=95.5
```

```python
# 표현식도 가능
x = 10
y = 20

print(f"{x + y=}")
# x + y=30

print(f"{x * 2=}, {y // 3=}")
# x * 2=20, y // 3=6
```

```python
# 포맷 지정자와 함께 사용
pi = 3.141592653589793

print(f"{pi=:.2f}")
# pi=3.14

value = 1234567
print(f"{value=:,}")
# value=1,234,567
```

```python
# 객체 디버깅
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(10, 20)
print(f"{p=}")
# p=Point(x=10, y=20)
```

```python
# 리스트/딕셔너리 디버깅
items = [1, 2, 3]
config = {"host": "localhost", "port": 8080}

print(f"{items=}")
# items=[1, 2, 3]

print(f"{config=}")
# config={'host': 'localhost', 'port': 8080}

print(f"{len(items)=}, {config.get('port')=}")
# len(items)=3, config.get('port')=8080
```

> **팁**: 디버깅 시 `print(f"{var=}")`를 사용하면 변수명을 직접 타이핑할 필요가 없어 오타를 줄일 수 있다.