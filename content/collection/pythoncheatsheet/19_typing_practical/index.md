---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 19. Typing - 실전 타입힌트 패턴"
slug: "typing-typing-practical-type-hints-annotations-mypy-pyright-optional"
description: "실무에서 바로 쓰는 타입힌트 치트시트입니다. 기본 컨테이너 타입, Optional/Union(|), Callable, Generic/TypeVar, Literal/Final, TypedDict/Protocol까지 코드 가독성과 안정성을 높이는 패턴을 정리합니다."
lastmod: 2026-01-18
collection_order: 19
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - typing
  - type-hints
  - 타입힌트
  - annotations
  - 어노테이션
  - mypy
  - pyright
  - static-analysis
  - 정적분석
  - Optional
  - Union
  - Callable
  - Iterable
  - Iterator
  - Sequence
  - Mapping
  - dict
  - list
  - tuple
  - set
  - generics
  - Generic
  - TypeVar
  - 제네릭
  - protocol
  - Protocol
  - TypedDict
  - Literal
  - Final
  - ClassVar
  - dataclasses
  - dataclass
  - readability
  - 가독성
  - maintainability
  - 유지보수
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - api-design
  - 설계
  - standard-library
  - 표준라이브러리
  - python39
  - python310
  - python311
  - testing
  - 테스트
  - refactoring
  - 리팩토링
---
타입힌트는 코드의 의도를 명확히 하고 리팩토링 안정성을 높입니다. 이 치트시트는 기본 타입부터 Generic, TypeVar, Literal까지 실무에서 바로 쓰는 타입힌트 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- "이 함수는 뭘 받는지/뭘 리턴하는지"가 불분명할 때
- 리팩토링/코드리뷰에서 안정성을 올리고 싶을 때
- Generic 클래스/함수를 정의해야 할 때

## 핵심 패턴

- 컨테이너: `list[str]`, `dict[str, int]` (Py3.9+)
- Optional: `str | None` (Py3.10+) 또는 `Optional[str]`
- Generic: `TypeVar`로 타입 파라미터 정의
- 제한된 값: `Literal["a", "b"]`
- 상수: `Final[int]`

## 기본 타입

```python
# 기본 타입 (Py3.9+)
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def is_valid(value: float) -> bool:
    return value > 0
```

```python
# 컨테이너 타입 (Py3.9+ 내장 타입 직접 사용)
def total(nums: list[int]) -> int:
    return sum(nums)

def get_config() -> dict[str, str]:
    return {"host": "localhost", "port": "8080"}

def unique_items(items: list[str]) -> set[str]:
    return set(items)

# 튜플 (고정 길이 + 타입)
def get_point() -> tuple[int, int]:
    return (10, 20)

# 가변 길이 튜플
def get_scores() -> tuple[int, ...]:
    return (90, 85, 88)
```

## Optional / Union

```python
# Optional - None일 수 있는 타입
def find_user(user_id: int) -> str | None:  # Py3.10+
    if user_id == 1:
        return "Alice"
    return None

# Py3.9 이하
from typing import Optional
def find_user_old(user_id: int) -> Optional[str]:
    ...

# Union - 여러 타입 중 하나
def process(value: int | str) -> str:  # Py3.10+
    return str(value)

# Py3.9 이하
from typing import Union
def process_old(value: Union[int, str]) -> str:
    return str(value)
```

## Callable - 함수 타입

```python
from collections.abc import Callable

# 함수를 인자로 받기
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

result = apply(lambda x, y: x + y, 3, 4)  # 7

# 콜백 패턴
def on_complete(callback: Callable[[str], None]) -> None:
    callback("done")

# 임의 인자 함수
def logger(func: Callable[..., None]) -> None:
    func()
```

## Generic / TypeVar - 제네릭 타입

```python
from typing import TypeVar, Generic

T = TypeVar("T")  # 타입 변수 선언

# 제네릭 함수
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# 사용
first([1, 2, 3])      # int 반환
first(["a", "b"])     # str 반환
```

```python
# 제한된 TypeVar
from typing import TypeVar

Number = TypeVar("Number", int, float)  # int 또는 float만

def double(x: Number) -> Number:
    return x * 2

# bound 사용 - 특정 타입의 서브타입만
from typing import TypeVar

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

A = TypeVar("A", bound=Animal)

def make_speak(animal: A) -> str:
    return animal.speak()
```

```python
# 제네릭 클래스
from typing import TypeVar, Generic

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item
    
    def get(self) -> T:
        return self.item

int_box = Box(42)       # Box[int]
str_box = Box("hello")  # Box[str]
```

## Literal - 리터럴 타입

```python
from typing import Literal

# 특정 값만 허용
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode: {mode}")

set_mode("read")   # OK
# set_mode("delete")  # Type error!

# 불리언 대신 명시적 값
def get_status() -> Literal["success", "failure", "pending"]:
    return "success"

# 숫자 리터럴
def set_priority(level: Literal[1, 2, 3]) -> None:
    pass
```

## Final / ClassVar - 상수와 클래스 변수

```python
from typing import Final, ClassVar

# 상수 (재할당 금지)
MAX_SIZE: Final[int] = 100
API_URL: Final = "https://api.example.com"  # 타입 추론

# 클래스에서 사용
class Config:
    DEBUG: Final[bool] = False  # 인스턴스에서 재할당 불가
    
    # 클래스 변수 (인스턴스 변수와 구분)
    instance_count: ClassVar[int] = 0
    
    def __init__(self) -> None:
        Config.instance_count += 1
```

## TypedDict - 구조화된 딕셔너리

```python
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int
    email: str

def create_user(data: UserDict) -> None:
    print(data["name"], data["age"])

user: UserDict = {"name": "Alice", "age": 30, "email": "a@b.com"}
create_user(user)

# 선택적 필드 (total=False)
class PartialUser(TypedDict, total=False):
    name: str      # 선택
    age: int       # 선택

# 혼합: Required + Optional
from typing import Required, NotRequired  # Py3.11+

class MixedUser(TypedDict):
    name: str                    # 필수 (기본)
    age: NotRequired[int]        # 선택
```

## Protocol - 구조적 서브타이핑

```python
from typing import Protocol

# "이 메서드가 있으면 됨" - 덕 타이핑의 타입 버전
class Readable(Protocol):
    def read(self) -> str: ...

class File:
    def read(self) -> str:
        return "file content"

class StringIO:
    def read(self) -> str:
        return "string content"

def process(source: Readable) -> str:
    return source.read()

# File과 StringIO 모두 Readable을 "암시적으로" 구현
process(File())
process(StringIO())
```

## 추상 컬렉션 타입 (유연한 API)

```python
from collections.abc import Iterable, Sequence, Mapping

# Iterable - for문 가능한 모든 것
def sum_all(items: Iterable[int]) -> int:
    return sum(items)

sum_all([1, 2, 3])       # list
sum_all((1, 2, 3))       # tuple
sum_all({1, 2, 3})       # set
sum_all(range(4))        # range

# Sequence - 인덱싱 + 길이
def get_middle(items: Sequence[str]) -> str:
    return items[len(items) // 2]

# Mapping - 키-값 접근
def get_name(data: Mapping[str, str]) -> str:
    return data.get("name", "unknown")
```

## 자주 하는 실수/주의점

- **런타임 강제 아님**: 타입힌트는 "도구/사람을 위한 계약"
- **너무 구체적 ❌**: `list` 대신 `Iterable`로 유연성 확보
- **`Any` 남용 ❌**: 타입 체크 효과 상실
- **버전 호환성**:
  - Py3.9+: `list[str]` 직접 사용 가능
  - Py3.9-: `from typing import List` 필요
  - Py3.10+: `X | Y` 유니온 문법
  - Py3.10-: `Union[X, Y]` 사용
- **순환 참조**: 문자열로 forward reference 사용
  ```python
  class Node:
      def __init__(self, child: "Node | None") -> None:
          self.child = child
  ```

## 타입 체커 실행

```bash
# mypy
pip install mypy
mypy your_script.py

# pyright (더 빠름)
pip install pyright
pyright your_script.py
```

## 관련 링크(공식 문서)

- [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 604 – Allow X | Y union syntax](https://peps.python.org/pep-0604/)
- [PEP 586 – Literal Types](https://peps.python.org/pep-0586/)
- [PEP 544 – Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
