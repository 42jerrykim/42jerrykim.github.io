---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 23. match-case - 구조적 패턴 매칭 (Py3.10+)"
slug: "structural-pattern-matching-switch-guide-py310-py311-code-examples"
description: "파이썬 3.10+ 구조적 패턴 매칭을 빠르게 쓰기 위한 치트시트입니다. match-case 기본 문법, 리터럴/시퀀스/매핑/클래스 패턴, 가드(if), 와일드카드, OR 패턴과 실전 사용 사례를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 23
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - match
  - case
  - pattern-matching
  - 패턴매칭
  - structural-pattern-matching
  - 구조적패턴매칭
  - switch
  - switch-case
  - control-flow
  - 제어흐름
  - literal
  - 리터럴
  - sequence
  - 시퀀스
  - mapping
  - 매핑
  - class-pattern
  - 클래스패턴
  - guard
  - 가드
  - wildcard
  - 와일드카드
  - OR-pattern
  - capture
  - 캡처
  - destructuring
  - 구조분해
  - python310
  - python311
  - python312
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - readability
  - 가독성
  - enum
  - dataclass
---
match-case는 Python 3.10에서 도입된 구조적 패턴 매칭입니다. 이 치트시트는 리터럴, 시퀀스, 매핑, 클래스 패턴과 가드 조건 사용법을 정리합니다.

## 언제 이 치트시트를 보나?

- 복잡한 if-elif 체인을 **더 읽기 쉽게** 바꾸고 싶을 때
- 데이터 구조를 **분해하면서 조건 분기**할 때

## 핵심 패턴

- `match subject:` + `case pattern:` 구문
- `_` 와일드카드: 모든 값 매칭 (default)
- `|` OR 패턴: 여러 패턴 중 하나
- `if` 가드: 추가 조건 검사
- 캡처: 패턴 내 변수에 값 바인딩

## 최소 예제

```python
# 기본 리터럴 매칭
def http_status(status: int) -> str:
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  # 와일드카드 (default)
            return "Unknown"

print(http_status(200))  # OK
print(http_status(999))  # Unknown
```

```python
# OR 패턴 (|)
def categorize(code: int) -> str:
    match code:
        case 200 | 201 | 204:
            return "Success"
        case 400 | 401 | 403 | 404:
            return "Client Error"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Other"
```

## 시퀀스 패턴 (리스트/튜플)

```python
def process_command(command: list) -> str:
    match command:
        case ["quit"]:
            return "Exiting..."
        case ["hello", name]:  # 캡처
            return f"Hello, {name}!"
        case ["add", x, y]:
            return f"Result: {int(x) + int(y)}"
        case ["echo", *args]:  # *로 나머지 캡처
            return " ".join(args)
        case []:
            return "Empty command"
        case _:
            return "Unknown command"

print(process_command(["hello", "Alice"]))  # Hello, Alice!
print(process_command(["add", "2", "3"]))   # Result: 5
print(process_command(["echo", "a", "b", "c"]))  # a b c
```

## 매핑 패턴 (딕셔너리)

```python
def process_event(event: dict) -> str:
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"Click at ({x}, {y})"
        case {"type": "keypress", "key": key}:
            return f"Key pressed: {key}"
        case {"type": "scroll", "direction": d, **rest}:  # 나머지 캡처
            return f"Scroll {d}, extra: {rest}"
        case {"type": t}:
            return f"Unknown event type: {t}"
        case _:
            return "Invalid event"

print(process_event({"type": "click", "x": 100, "y": 200}))
# Click at (100, 200)
```

## 클래스 패턴

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float

def describe_shape(shape) -> str:
    match shape:
        case Point(x=0, y=0):
            return "Origin"
        case Point(x=x, y=y):
            return f"Point at ({x}, {y})"
        case Circle(center=Point(x=x, y=y), radius=r):
            return f"Circle at ({x}, {y}) with radius {r}"
        case Rectangle(width=w, height=h) if w == h:
            return f"Square with side {w}"
        case Rectangle(width=w, height=h):
            return f"Rectangle {w}x{h}"
        case _:
            return "Unknown shape"

print(describe_shape(Point(0, 0)))  # Origin
print(describe_shape(Circle(Point(1, 2), 5)))  # Circle at (1, 2) with radius 5
```

## 가드 조건 (if)

```python
def classify_number(n: int) -> str:
    match n:
        case 0:
            return "Zero"
        case x if x < 0:
            return "Negative"
        case x if x % 2 == 0:
            return "Positive Even"
        case _:
            return "Positive Odd"

print(classify_number(-5))   # Negative
print(classify_number(4))    # Positive Even
print(classify_number(7))    # Positive Odd
```

## Enum과 함께 사용

```python
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()

def handle_state(state: State) -> str:
    match state:
        case State.IDLE:
            return "Waiting for input..."
        case State.RUNNING:
            return "Processing..."
        case State.PAUSED:
            return "Paused, press resume"
        case State.STOPPED:
            return "Finished"
```

## 타입 체크 패턴

```python
def process_value(value) -> str:
    match value:
        case bool():  # bool 먼저! (bool은 int의 서브클래스)
            return f"Boolean: {value}"
        case int():
            return f"Integer: {value}"
        case float():
            return f"Float: {value}"
        case str():
            return f"String: {value}"
        case list():
            return f"List with {len(value)} items"
        case dict():
            return f"Dict with {len(value)} keys"
        case _:
            return f"Other: {type(value)}"
```

## 자주 하는 실수/주의점

- **Python 3.10+ 필수**: 이전 버전에서는 SyntaxError
- **case 순서 중요**: 위에서 아래로 순차 매칭, 먼저 매칭되면 종료
- **bool vs int 순서**: `bool`은 `int`의 서브클래스이므로 `bool()` 패턴을 먼저 배치
- **변수 캡처 vs 상수**:
  ```python
  # 변수 캡처 (항상 매칭됨)
  case x:  # x에 값 바인딩
  
  # 상수 비교 (리터럴만)
  case 42:  # 42와 같을 때만
  
  # 상수를 변수로 비교하려면 가드 사용
  MY_CONST = 42
  case x if x == MY_CONST:
  ```
- **`_` 와일드카드**: 값이 바인딩되지 않음 (참조 불가)
- **매핑 패턴**: 지정하지 않은 키가 있어도 매칭됨 (부분 매칭)

## if-elif vs match-case

```python
# Before (if-elif)
def categorize_old(value):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int) and value > 0:
        return "positive int"
    elif isinstance(value, int):
        return "non-positive int"
    elif isinstance(value, str):
        return "string"
    else:
        return "other"

# After (match-case) - 더 선언적
def categorize_new(value):
    match value:
        case bool():
            return "bool"
        case int() as n if n > 0:
            return "positive int"
        case int():
            return "non-positive int"
        case str():
            return "string"
        case _:
            return "other"
```

## 관련 링크(공식 문서)

- [PEP 634 – Structural Pattern Matching: Specification](https://peps.python.org/pep-0634/)
- [PEP 636 – Structural Pattern Matching: Tutorial](https://peps.python.org/pep-0636/)
- [match Statements](https://docs.python.org/3/reference/compound_stmts.html#match)
