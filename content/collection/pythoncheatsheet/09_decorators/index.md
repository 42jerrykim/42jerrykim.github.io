---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 09. Decorators - 함수/클래스 데코레이터"
slug: "decorators-decorator-wrapper-functools-wraps-higher-order-closure"
description: "파이썬 데코레이터를 빠르게 이해하고 쓰기 위한 치트시트입니다. 함수 데코레이터 기본, @wraps로 메타데이터 보존, 인자 있는 데코레이터, 클래스 데코레이터, 실무 패턴과 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 9
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - decorator
  - decorators
  - 데코레이터
  - wrapper
  - 래퍼
  - functools
  - wraps
  - higher-order
  - 고차함수
  - closure
  - 클로저
  - function
  - 함수
  - class-decorator
  - 클래스데코레이터
  - method-decorator
  - 메서드데코레이터
  - syntax
  - 문법
  - logging
  - 로깅
  - timing
  - 타이밍
  - caching
  - 캐싱
  - validation
  - 검증
  - retry
  - 재시도
  - authentication
  - 인증
  - metaprogramming
  - 메타프로그래밍
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - debugging
  - 디버깅
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
---
데코레이터는 함수나 클래스를 감싸서 동작을 확장하는 파이썬의 강력한 패턴입니다. 이 치트시트는 함수 데코레이터 기본, @wraps, 인자 있는 데코레이터, 실무 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- 여러 함수에 **공통 로직**(로깅, 타이밍, 인증 등)을 적용하고 싶을 때
- `@decorator` 문법이 어떻게 동작하는지 이해하고 싶을 때

## 핵심 패턴

- 데코레이터 = 함수를 받아 함수를 반환하는 함수
- `@decorator`는 `func = decorator(func)`의 문법 설탕
- `@functools.wraps(func)`: 원본 함수의 메타데이터 보존
- 인자 있는 데코레이터: 3중 중첩 함수 또는 클래스 사용

## 최소 예제

```python
# 기본 데코레이터
from functools import wraps

def my_decorator(func):
    @wraps(func)  # func의 __name__, __doc__ 등 보존
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper

@my_decorator
def greet(name: str) -> str:
    """인사말 반환"""
    return f"Hello, {name}"

# @my_decorator는 greet = my_decorator(greet)와 동일
print(greet("Alice"))
# Calling greet
# Done greet
# Hello, Alice

print(greet.__name__)  # greet (@wraps 덕분)
print(greet.__doc__)   # 인사말 반환
```

```python
# 인자 있는 데코레이터
from functools import wraps

def repeat(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")

say_hello()
# Hello!
# Hello!
# Hello!
```

```python
# 실무 예: 실행 시간 측정
import time
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timing
def slow_function():
    time.sleep(0.5)
    return "done"

slow_function()  # slow_function took 0.5012s
```

```python
# 실무 예: 재시도 로직
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}, retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "success"
```

## 클래스 데코레이터

```python
# 클래스에 데코레이터 적용
def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p)  # Person(name='Alice', age=30)
```

```python
# 클래스로 데코레이터 구현
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
        wraps(func)(self)  # 메타데이터 복사
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet():
    return "Hello"

greet()  # Call 1 of greet
greet()  # Call 2 of greet
print(greet.count)  # 2
```

## 표준 라이브러리 데코레이터

| 데코레이터 | 모듈 | 용도 |
|------------|------|------|
| `@property` | built-in | getter/setter |
| `@classmethod` | built-in | 클래스 메서드 |
| `@staticmethod` | built-in | 정적 메서드 |
| `@functools.lru_cache` | functools | 결과 캐싱 |
| `@functools.wraps` | functools | 메타데이터 보존 |
| `@dataclass` | dataclasses | 데이터 클래스 |
| `@contextmanager` | contextlib | 컨텍스트 매니저 |
| `@abstractmethod` | abc | 추상 메서드 |

## 자주 하는 실수/주의점

- **`@wraps` 빠뜨리기**: 디버깅 시 `wrapper`로 보이고, `__doc__`도 사라짐
- **인자 있는 데코레이터**: `@decorator()` 괄호 빠뜨리면 동작 안 함
- **메서드에 데코레이터**: `self`가 첫 번째 인자로 전달됨을 고려
- **데코레이터 순서**: `@a @b def f()` → `a(b(f))` (아래에서 위로 적용)
- **디버깅 어려움**: 스택트레이스가 wrapper를 거침 → 로깅 추가 권장

## 데코레이터 스택 순서

```python
@decorator_a
@decorator_b
@decorator_c
def my_func():
    pass

# 위 코드는 다음과 동일:
# my_func = decorator_a(decorator_b(decorator_c(my_func)))
# 실행 순서: a의 전처리 → b의 전처리 → c의 전처리 → 원본 → c의 후처리 → b의 후처리 → a의 후처리
```

## 관련 링크(공식 문서)

- [PEP 318 – Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
