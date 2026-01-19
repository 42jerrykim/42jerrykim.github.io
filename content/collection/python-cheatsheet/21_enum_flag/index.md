---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 21. Enum & Flag - 열거형 실전 패턴"
slug: "enum-flag-intenum-strenum-auto-bitwise-guide-best-patterns"
description: "파이썬 Enum을 실전에서 빠르게 쓰기 위한 치트시트입니다. Enum/IntEnum/StrEnum 기본, auto() 자동값, Flag 비트 연산, 멤버 접근/비교/순회와 흔한 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 21
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - enum
  - Enum
  - IntEnum
  - StrEnum
  - Flag
  - IntFlag
  - enumeration
  - 열거형
  - 상수
  - constant
  - auto
  - 자동값
  - member
  - 멤버
  - value
  - name
  - comparison
  - 비교
  - iteration
  - 순회
  - bitwise
  - 비트연산
  - bitmask
  - 비트마스크
  - pattern
  - 패턴
  - type-safety
  - 타입안전
  - readability
  - 가독성
  - maintainability
  - 유지보수
  - magic-number
  - 매직넘버
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - python311
  - python312
---
Enum은 관련 상수를 그룹화하여 타입 안전성과 가독성을 높이는 방법입니다. 이 치트시트는 Enum, IntEnum, StrEnum, Flag의 기본 사용법과 실전 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- 매직 넘버/문자열 대신 **의미 있는 상수**를 정의하고 싶을 때
- 상태/옵션/타입을 **타입 안전**하게 관리하고 싶을 때

## 핵심 패턴

- `Enum`: 기본 열거형 (값 비교는 `is` 또는 `==`)
- `IntEnum`: 정수와 호환되는 열거형 (기존 API와 호환 필요시)
- `StrEnum`: 문자열과 호환되는 열거형 (Py3.11+)
- `Flag`: 비트 연산 가능한 열거형 (여러 옵션 조합)
- `auto()`: 자동 값 할당

## 최소 예제

```python
from enum import Enum, auto

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 또는 auto()로 자동 값 할당
class Status(Enum):
    PENDING = auto()   # 1
    RUNNING = auto()   # 2
    DONE = auto()      # 3
    FAILED = auto()    # 4
```

```python
# 멤버 접근
print(Color.RED)        # Color.RED
print(Color.RED.name)   # 'RED'
print(Color.RED.value)  # 1

# 값으로 멤버 찾기
print(Color(1))         # Color.RED

# 이름으로 멤버 찾기
print(Color["RED"])     # Color.RED
```

```python
# 비교
color = Color.RED

if color == Color.RED:
    print("It's red!")

if color is Color.RED:  # identity 비교도 가능
    print("Same object")

# 주의: 값 직접 비교는 False
print(Color.RED == 1)   # False (Enum은 값과 직접 비교 안 됨)
```

```python
# 순회
for color in Color:
    print(color.name, color.value)
# RED 1
# GREEN 2
# BLUE 3
```

## IntEnum - 정수 호환

```python
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 정수와 직접 비교 가능
print(Priority.HIGH == 3)      # True
print(Priority.HIGH > Priority.LOW)  # True

# 정수 연산 가능 (결과는 int)
print(Priority.HIGH + 1)       # 4
```

## StrEnum - 문자열 호환 (Py3.11+)

```python
from enum import StrEnum

class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

# 문자열과 직접 비교 가능
print(HttpMethod.GET == "GET")  # True

# 문자열로 바로 사용
url = f"/api/users"
method = HttpMethod.POST
print(f"{method} {url}")  # POST /api/users
```

## Flag - 비트 연산 조합

```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()    # 1
    WRITE = auto()   # 2
    EXECUTE = auto() # 4
    
    # 조합 멤버 정의 가능
    RW = READ | WRITE
    ALL = READ | WRITE | EXECUTE

# 조합
user_perms = Permission.READ | Permission.WRITE
print(user_perms)  # Permission.RW

# 포함 여부 확인
if Permission.READ in user_perms:
    print("Can read")

if Permission.EXECUTE not in user_perms:
    print("Cannot execute")

# 조합 해제
user_perms &= ~Permission.WRITE  # WRITE 제거
```

## 실전 패턴

```python
# 함수 인자로 Enum 사용
from enum import Enum

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"

def sort_items(items: list, order: SortOrder) -> list:
    reverse = order == SortOrder.DESC
    return sorted(items, reverse=reverse)

# 타입 안전한 호출
result = sort_items([3, 1, 2], SortOrder.ASC)
```

```python
# match-case와 함께 (Py3.10+)
from enum import Enum

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()

def handle_state(state: State) -> str:
    match state:
        case State.IDLE:
            return "Waiting..."
        case State.RUNNING:
            return "Processing..."
        case State.PAUSED:
            return "Paused"
        case State.STOPPED:
            return "Done"
```

```python
# 메서드/프로퍼티 추가
from enum import Enum

class Planet(Enum):
    EARTH = (5.97e24, 6.37e6)
    MARS = (6.42e23, 3.39e6)
    
    def __init__(self, mass: float, radius: float):
        self.mass = mass
        self.radius = radius
    
    @property
    def surface_gravity(self) -> float:
        G = 6.67e-11
        return G * self.mass / (self.radius ** 2)

print(Planet.EARTH.surface_gravity)  # ~9.8
```

## 자주 하는 실수/주의점

- **Enum vs IntEnum 선택**: 정수 비교가 필요 없으면 `Enum` 권장 (더 엄격)
- **값 중복**: 같은 값을 가진 멤버는 별칭(alias)이 됨
  ```python
  class Status(Enum):
      ACTIVE = 1
      ENABLED = 1  # ACTIVE의 별칭
  
  print(Status.ENABLED is Status.ACTIVE)  # True
  ```
- **상속 제한**: 멤버가 있는 Enum은 상속 불가
- **JSON 직렬화**: Enum은 기본적으로 JSON 직렬화 안 됨 → `.value` 또는 `.name` 사용
  ```python
  import json
  json.dumps({"color": Color.RED.value})  # {"color": 1}
  json.dumps({"color": Color.RED.name})   # {"color": "RED"}
  ```
- **auto() 값**: 기본은 1부터 시작하는 정수 (커스터마이징 가능)

## 관련 링크(공식 문서)

- [enum — Support for enumerations](https://docs.python.org/3/library/enum.html)
- [PEP 435 – Adding an Enum type to the Python standard library](https://peps.python.org/pep-0435/)
