---
title: "Basic - 연산자, 변수, 출력, 형변환"
last_modified_at: 2023-01-17
date: 2022-01-17
header:
  teaser: /assets/images/2023/Screenshot_2023-01-17_at_20-55-19_WelcometoPython.org.png
---

우리는 어디에선가 시작할 필요가 있다. 바로 여기서 그 시작점이다.

> [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)에서 내용을 가지고 왔다.
> 
> 파이썬은 배우기 쉬운 언어이면서 강력한 언어이다. 파이썬은 우아한 문법과 다이나믹 파입을 지원한다. 이것들은 자연스럽게 어우러져 스크립팅과 빠른 어플리케이션 개발하는데 있어서 이상적인 언어로 만든다.

# 산술 연산자

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
# 20

>>> (2 + 3) * 6
# 30

>>> 2 ** 8
#256

>>> 23 // 7
# 3

>>> 23 % 7
# 2

>>> (5 - 1) * ((7 + 1) / (3 - 1))
# 16.0
```

# 증강 연산자

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
# 'Hello world!'

>>> number = 1
>>> number += 1
>>> number
# 2

>>> my_list = ['item']
>>> my_list *= 3
>>> my_list
# ['item', 'item', 'item']
```

# 자료형

|Data Type|Examples
|:---|:---|
|Integers|-2, -1, 0, 1, 2, 3, 4, 5|
|Floating-point numbers|-1.25, -1.0, --0.5, 0.0, 0.5, 1.0, 1.25|
|Strings|'a', 'aa', 'aaa', 'Hello!', '11 cats'|

# 결합(Concatenation)과 복사

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

# 변수

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

# 주석

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

# print() 함수

`print()`함수는 파라미터로 들어온 변수를 출력한다. 다중 변수를 처리 할 수 있으며, 부동 소수점 숫자와 문자열을 포함한다. 문자열은 쌍따옴표 없지 출력하며, 파라미터 사이에 띄어쓰기를 포함하여 출력하기 때문에 출력 형식을 조절하기 편하다.

```python
>>> print('Hello world!')
# Hello world!

>>> a = 1
>>> print('Hello world!', a)
# Hello world! 1
```

## end 키워드

`end` 키워드는 출력된 결과물에서 줄바꿈을 다른 문자로 변경 할 수 있다.

```python
phrase = ['printed', 'with', 'a', 'dash', 'in', 'between']
>>> for word in phrase:
...     print(word, end='-')
...
# printed-with-a-dash-in-between-
```

## sep 키워드

`sep` 키워드는 구분자를 바꿀수 있다.

```python
print('cats', 'dogs', 'mice', sep=',')
# cats,dogs,mice
```

# input() 함수

`input()` 함수는 사용자의 입력을 문자열로 받아드린다.

```python
>>> print('What is your name?')   # ask for their name
>>> my_name = input()
>>> print('Hi, {}'.format(my_name))
# What is your name?
# Martha
# Hi, Martha
```

`input()` 함수는 `print()` 함수를 사용하지 않고 기본 메시지를 출력 할 수 있다.

```python
>>> my_name = input('What is your name? ')  # default message
>>> print('Hi, {}'.format(my_name))
# What is your name? Martha
# Hi, Martha
```

# len() 함수

문자열, 리스트(List), 사전(Dictionary)등 변수의 길이를 반환한다.

```python
>>> len('hello')
# 5

>>> len(['cat', 3, 'dog'])
# 3
```

> 비어 있음을 테스트 할때는 len()을 사용하지 않고 변수를 바로 사용하는것이 좋다.

아래의 코드는 비어 있음을 테스트 하는 예시이다.

```python
>>> a = [1, 2, 3]

# bad
>>> if len(a) > 0:  # evaluates to True
...     print("the list is not empty!")
...
# the list is not empty!

# good
>>> if a: # evaluates to True
...     print("the list is not empty!")
...
# the list is not empty!
```

# str(), int(), and float() 함수

이 함수들은 변수의 타입을 바꾸는데 사용한다. 예를 들어 실수나 정수를 문자열로 바꿀때 사용한다.

```python
>>> str(29)
# '29'

>>> str(-3.14)
# '-3.14'
```

또는 문자열을 실수나 정수로 바꿀수 있다.

```python
>>> int('11')
# 11

>>> float('3.14')
# 3.14
```