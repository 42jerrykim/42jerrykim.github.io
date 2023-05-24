---
title: "내장 함수들"
last_modified_at: 2023-01-20
date: 2022-01-17
header:
  teaser: /assets/images/2023/Screenshot_2023-01-17_at_20-55-19_WelcometoPython.org.png
---

파이썬 인터프리터에는 항상 사용할 수 있는 많은 함수와 형이 내장되어 있다. 알파벳 순으로 정리 하였다.

> [파이썬 표준 라이브러리 - 내장 함수](https://docs.python.org/3/library/functions.html?highlight=built)를 참고해서 작성하였다.

# 파이썬 내장 함수들

| Function | Description |
| :--- | :--- |
| [abs(x)](#absx) | 숫자의 절대값을 반환한다. |
| [all(iterable)](#alliterable) | 반복 가능한 모든 요소가 참인 경우에 참을 반환한다. |
| [any(iterable)](#anyiterable) | 반복 가능한 요소들 중에서 참인 경우가 있으면 참을 반환한다. |
| [awaitable anext(async_iterator)<br>awaitable anext(async_iterator, default)](#awaitable-anextasync_iterator-awaitable-anextasync_iterator-default) | awaited 중일때, 주어진 비동기 이터레이터로 부터 다음 아이템을 반환한다. |


# A

## abs(x)

숫자의 절댓값을 반환한다. 인자는 정수, 실수와 같이 `__abs__()`를 구현하는 객체이어야 한다. 인자가 복소수면 그 크기를 반환한다.

## aiter(async_iterable)

비동기적으로 반복가능한 객체의 이터레이터를 반환한다. `x.__aiter__()`를 호출하는것과 같다.

> 주의: `iter()`와 다르게 `aiter()`는 2개의 인자를 받을 수 없다.

> 버전 3.10에서 추가됨.

## all(iterable)

iterable 의 모든 요소가 참이면 (또는 iterable 이 비어있으면) True를 반환한다. `all(iterable)`은 아래의 코드와 동일한 동작을 한다.

```python
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```

## awaitable anext(async_iterator)<br>awaitable anext(async_iterator, default)

awaited 중일때, 주어진 비동기 이터레이터로 부터 다음 아이템을 반환한다. 또는 이터레이터를 다 사용한 경우에는 기본값이 있으면 기본값이 반환된다. `anext()`는 `next()` 내장 함수의 비동기 변형이며, 유사하게 동작한다.

`anext()`는 awaitable을 반환하는 async_iterator의 `__anext__()`를 호출한다. 함수 호출이 끝나면 반복자의 다음 값이 반환된다. 이터레이터를 다 사용한 경우에, 기본값이 있으면 기본값이 반환되고, 그렇지 않으면 StopAsyncIteration 익셉션이 발생한다.
     
> 버전 3.10에서 추가됨.

## any(iterable)

iterable 의 요소 중 어느 하나라도 참이면 True를 반환한다. iterable이 비어 있으면 False를 반환한다. `any(iterable)`는 아래의 코드와 동일한 동작을 한다.

```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```

## ascii(object)
repr()는 객체의 출력 가능한 표현을 포함하는 문자열을 반환한다. 그러나 ASCII가 아닌 문자는 `\x`, `\u` 또는 `\U` 이스케이프를 사용하여 출력한다.

```python
>>> ascii('Python')
"'Python'"
>>> ascii('Pythön')
"'Pyth\xf6n'"
```

# B

## bin(x)

정수를 `0b`로 시작하는 이진 문자열로 변환한다. 이 결과는 파이썬 문법에 적합한 표현이다. 만약에 `x`가 파이썬 정수 객체가 아니면, 실수를 반환하는 `__index__()` 메소드를 정의해야 한다. 

```python
>>> bin(3)
'0b11'
>>> bin(-10)
'-0b1010'
```

`0b`로 시작하는 것을 변경하기 위해서는 아래와 같은 방법을 사용 할 수 있다.

```python
>>> format(14, '#b'), format(14, 'b')
('0b1110', '1110')
>>> f'{14:#b}', f'{14:b}'
('0b1110', '1110')
```
