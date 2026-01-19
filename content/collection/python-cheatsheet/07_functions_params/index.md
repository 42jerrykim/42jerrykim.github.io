---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 07. Functions - 인자/리턴/*args/**kwargs"
slug: "fast-guide-functions-args-kwargs-defaults-annotations-tips"
description: "함수 정의와 인자 패턴을 빠르게 쓰기 위한 치트시트입니다. 기본값 인자의 함정, *args/**kwargs, keyword-only/positional-only, 반환값 언패킹, 어노테이션/독스트링 기본까지 실전 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 7
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - functions
  - 함수
  - parameters
  - arguments
  - 인자
  - 매개변수
  - return
  - 반환
  - unpacking
  - 언패킹
  - args
  - kwargs
  - varargs
  - keyword-only
  - positional-only
  - defaults
  - default-arg
  - mutable-default
  - 함정
  - pitfalls
  - annotations
  - 타입힌트
  - typing
  - docstring
  - 독스트링
  - scope
  - 스코프
  - closures
  - 클로저
  - lambda
  - 람다
  - higher-order
  - 고차함수
  - readability
  - 가독성
  - best-practices
  - 베스트프랙티스
  - refactoring
  - 리팩토링
  - debugging
  - 디버깅
  - standard-library
  - 표준라이브러리
  - api-design
  - 설계
  - clean-code
  - 클린코드
  - error-handling
  - 예외처리
  - None
  - sentinel
  - patterns
  - 패턴
---
함수는 코드 재사용과 구조화의 핵심입니다. 이 치트시트는 기본값 인자 함정, *args/**kwargs, keyword-only, 다중 반환 등 함수 시그니처 패턴과 실수 포인트를 정리합니다.

## 언제 이 치트시트를 보나?

- 함수 시그니처를 “읽기 쉬운 API”로 만들고 싶을 때
- 기본값 인자/가변 인자 때문에 버그가 날 때

## 핵심 패턴

- 기본값으로 “가변 객체(list/dict/set)”를 두지 말기 → `None` + 내부에서 초기화
- `*args`: 위치 인자 가변, `**kwargs`: 키워드 인자 가변
- keyword-only: `def f(*, x): ...` (호출 시 `f(x=...)` 강제)
- positional-only: `def f(x, /, y): ...` (일부 API에서 사용)
- 다중 반환: 튜플 반환 + 호출부 언패킹

## 최소 예제

```python
# mutable default arg 함정
def add_item(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items
```

```python
# *args / **kwargs
def f(*args, **kwargs):
    return args, kwargs

print(f(1, 2, a=3))
```

```python
# keyword-only
def connect(host, *, timeout=3.0):
    return host, timeout

connect("example.com", timeout=1.0)
# connect("example.com", 1.0)  # TypeError
```

```python
# 다중 반환 + 언패킹
def min_max(nums):
    return min(nums), max(nums)

lo, hi = min_max([3, 1, 9])
print(lo, hi)
```

```python
# 어노테이션(선택)
def greet(name: str) -> str:
    return f"hi {name}"
```

## 자주 하는 실수/주의점

- `def f(x=[]):` 같은 기본값은 호출 간에 공유되어 예상치 못한 누적 버그가 생김
- `*args/**kwargs`는 편하지만 남용하면 호출부가 불명확해짐 → 필요한 곳에만
- 반환이 여러 개인 함수는 의미 있는 네이밍/문서화(또는 `dataclass`/`NamedTuple`)를 고려

## 관련 링크(공식 문서)

- [Defining Functions (Tutorial)](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Function definitions (Language reference)](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

