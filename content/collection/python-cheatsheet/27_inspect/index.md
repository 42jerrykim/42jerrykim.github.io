---
draft: true
title: "[Python Cheatsheet] 27. inspect - 런타임 객체 검사"
slug: "inspect-module-runtime-analysis-introspection-reflection-guide"
description: "파이썬 inspect 모듈을 빠르게 사용하기 위한 치트시트입니다. 함수 시그니처, 소스 코드 조회, 스택 프레임, 클래스 계층 분석 등 런타임 객체 검사 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 27
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - inspect
  - introspection
  - 인트로스펙션
  - reflection
  - 리플렉션
  - signature
  - 시그니처
  - parameters
  - 매개변수
  - source-code
  - 소스코드
  - getsource
  - getmembers
  - stack
  - 스택
  - frame
  - 프레임
  - caller
  - 호출자
  - debugging
  - 디버깅
  - metaprogramming
  - 메타프로그래밍
  - decorator
  - 데코레이터
  - documentation
  - 문서화
  - docstring
  - 독스트링
  - module
  - 모듈
  - class
  - 클래스
  - function
  - 함수
  - method
  - 메서드
  - callable
  - 호출가능
  - advanced
  - 고급
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
---
`inspect` 모듈은 **런타임에 객체를 검사**하는 도구입니다. 함수 시그니처 분석, 소스 코드 조회, 스택 추적 등 메타프로그래밍과 디버깅에 필수적입니다.

## 언제 이 치트시트를 보나?

- 함수의 **매개변수 정보**를 동적으로 알아야 할 때
- **소스 코드**를 런타임에 조회하고 싶을 때
- **호출 스택**을 분석하거나 caller 정보가 필요할 때

## 핵심 함수

```python
import inspect

# 타입 체크
inspect.isfunction(obj)    # 함수인가?
inspect.ismethod(obj)      # 메서드인가?
inspect.isclass(obj)       # 클래스인가?
inspect.ismodule(obj)      # 모듈인가?

# 정보 조회
inspect.signature(func)    # 함수 시그니처
inspect.getsource(obj)     # 소스 코드
inspect.getfile(obj)       # 파일 경로
inspect.getmembers(obj)    # 멤버 목록
```

## 최소 예제

### 1. 함수 시그니처 분석

```python
import inspect

def greet(name: str, greeting: str = "Hello", *, loud: bool = False) -> str:
    """인사말 생성"""
    msg = f"{greeting}, {name}!"
    return msg.upper() if loud else msg

sig = inspect.signature(greet)

# 전체 시그니처
print(sig)  # (name: str, greeting: str = 'Hello', *, loud: bool = False) -> str

# 매개변수 순회
for param_name, param in sig.parameters.items():
    print(f"{param_name}: kind={param.kind.name}, default={param.default}")

# 출력:
# name: kind=POSITIONAL_OR_KEYWORD, default=<class 'inspect._empty'>
# greeting: kind=POSITIONAL_OR_KEYWORD, default=Hello
# loud: kind=KEYWORD_ONLY, default=False

# 반환 타입
print(sig.return_annotation)  # <class 'str'>
```

### 2. 매개변수 종류 (Parameter.kind)

```python
import inspect
from inspect import Parameter

def example(pos_only, /, pos_or_kw, *args, kw_only, **kwargs):
    pass

sig = inspect.signature(example)
for name, param in sig.parameters.items():
    kind = param.kind
    print(f"{name}: {kind.name}")

# pos_only: POSITIONAL_ONLY
# pos_or_kw: POSITIONAL_OR_KEYWORD
# args: VAR_POSITIONAL
# kw_only: KEYWORD_ONLY
# kwargs: VAR_KEYWORD
```

### 3. 소스 코드 조회

```python
import inspect

def my_function():
    """샘플 함수"""
    return 42

# 소스 코드
print(inspect.getsource(my_function))
# def my_function():
#     """샘플 함수"""
#     return 42

# 파일과 라인 번호
print(inspect.getfile(my_function))      # 파일 경로
print(inspect.getsourcelines(my_function))  # (소스라인리스트, 시작라인)

# 독스트링
print(inspect.getdoc(my_function))  # 샘플 함수
```

### 4. 클래스/모듈 멤버 조회

```python
import inspect

class MyClass:
    class_var = 10
    
    def __init__(self):
        self.instance_var = 20
    
    def method(self):
        pass
    
    @staticmethod
    def static_method():
        pass
    
    @classmethod
    def class_method(cls):
        pass

# 모든 멤버
members = inspect.getmembers(MyClass)

# 메서드만 필터링
methods = inspect.getmembers(MyClass, predicate=inspect.isfunction)
print([name for name, _ in methods])  # ['method', 'static_method']

# 클래스 계층
print(inspect.getmro(MyClass))  # (<class 'MyClass'>, <class 'object'>)
```

### 5. 스택 프레임 분석

```python
import inspect

def inner():
    # 현재 스택
    stack = inspect.stack()
    for frame_info in stack:
        print(f"{frame_info.function} at {frame_info.filename}:{frame_info.lineno}")
    
    # 호출자 정보
    caller = inspect.stack()[1]
    print(f"Called by: {caller.function}")

def outer():
    inner()

outer()
# inner at <file>:5
# outer at <file>:13
# <module> at <file>:15
# Called by: outer
```

### 6. 데코레이터에서 시그니처 활용

```python
import inspect
from functools import wraps

def validate_types(func):
    """타입 힌트 기반 자동 검증 데코레이터"""
    sig = inspect.signature(func)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
        for param_name, value in bound.arguments.items():
            param = sig.parameters[param_name]
            expected_type = param.annotation
            
            if expected_type != inspect.Parameter.empty:
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"{param_name} must be {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
        
        return func(*args, **kwargs)
    return wrapper

@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)      # OK
# add(1, "2")  # TypeError: b must be int, got str
```

### 7. 호출 가능 객체 판별

```python
import inspect

class CallableClass:
    def __call__(self):
        pass

def func(): pass

print(inspect.isfunction(func))         # True
print(inspect.ismethod(func))           # False

obj = CallableClass()
print(callable(obj))                    # True (내장 함수)
print(inspect.isfunction(obj))          # False
print(inspect.ismethod(obj.__call__))   # True
```

## 유용한 검사 함수들

```python
import inspect

# 객체 타입 검사
inspect.ismodule(obj)      # 모듈
inspect.isclass(obj)       # 클래스
inspect.isfunction(obj)    # 함수 (def로 정의)
inspect.ismethod(obj)      # 바운드 메서드
inspect.isgeneratorfunction(obj)  # 제너레이터 함수
inspect.iscoroutinefunction(obj)  # async 함수
inspect.isabstract(obj)    # 추상 클래스/메서드

# 정보 조회
inspect.getmodule(obj)     # 객체가 정의된 모듈
inspect.getfile(obj)       # 파일 경로
inspect.getsourcefile(obj) # 소스 파일 경로
inspect.getcomments(obj)   # 선행 주석
```

## 자주 하는 실수

### 1. 빌트인 함수에 getsource 시도

```python
import inspect

# TypeError: <built-in function len> is not a Python object
# inspect.getsource(len)

# 해결: 먼저 검사
if inspect.isfunction(obj):  # 빌트인은 False
    source = inspect.getsource(obj)
```

### 2. 람다 소스 코드 조회

```python
import inspect

f = lambda x: x * 2
# 한 줄로만 반환됨, 복잡한 람다는 정확하지 않을 수 있음
print(inspect.getsource(f))  # f = lambda x: x * 2
```

## 한눈에 정리

| 용도 | 함수 |
|------|------|
| 시그니처 분석 | `signature()`, `Parameter` |
| 소스 조회 | `getsource()`, `getsourcelines()` |
| 멤버 조회 | `getmembers()`, `getmro()` |
| 스택 분석 | `stack()`, `currentframe()` |
| 타입 체크 | `isfunction()`, `isclass()`, etc. |

## 참고

- [inspect - Python Docs](https://docs.python.org/3/library/inspect.html)
- [Signature Object](https://docs.python.org/3/library/inspect.html#inspect.Signature)
