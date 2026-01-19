---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 24. ABC - 추상 클래스 정의 패턴"
slug: "abstract-base-class-interface-abc-usage-oop-patterns-guide"
description: "파이썬 abc 모듈과 추상 클래스를 빠르게 쓰기 위한 치트시트입니다. ABC/abstractmethod로 인터페이스 정의, 추상 프로퍼티, collections.abc 활용, Protocol과의 비교를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 24
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - abc
  - ABC
  - abstract
  - 추상클래스
  - abstractmethod
  - interface
  - 인터페이스
  - inheritance
  - 상속
  - polymorphism
  - 다형성
  - collections.abc
  - Iterable
  - Sequence
  - Mapping
  - MutableSequence
  - protocol
  - Protocol
  - duck-typing
  - 덕타이핑
  - structural-subtyping
  - design-pattern
  - 디자인패턴
  - oop
  - 객체지향
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
abc 모듈은 추상 기반 클래스(Abstract Base Class)를 정의하는 도구를 제공합니다. 이 치트시트는 ABC/abstractmethod로 인터페이스 정의, collections.abc 활용, Protocol과의 비교를 정리합니다.

## 언제 이 치트시트를 보나?

- **인터페이스/계약**을 정의하고 구현을 강제하고 싶을 때
- 여러 클래스가 **공통 API**를 따르도록 하고 싶을 때
- `isinstance()` 체크로 **타입 검증**을 하고 싶을 때

## 핵심 패턴

- `ABC` 상속 + `@abstractmethod`: 추상 클래스 정의
- 추상 메서드 미구현 시 **인스턴스화 불가**
- `collections.abc`: 표준 인터페이스 (Iterable, Sequence 등)
- `Protocol` (Py3.8+): 명시적 상속 없이 구조적 서브타이핑

## ABC - 추상 클래스 정의

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """동물 추상 클래스"""
    
    @abstractmethod
    def speak(self) -> str:
        """소리내기 (구현 필수)"""
        pass
    
    @abstractmethod
    def move(self) -> str:
        """이동하기 (구현 필수)"""
        pass
    
    def sleep(self) -> str:
        """잠자기 (기본 구현 제공)"""
        return "Zzz..."

# 추상 클래스는 인스턴스화 불가
# animal = Animal()  # TypeError!

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"
    
    def move(self) -> str:
        return "Running on four legs"

# 모든 추상 메서드 구현 시 인스턴스화 가능
dog = Dog()
print(dog.speak())  # Woof!
print(dog.sleep())  # Zzz... (상속된 기본 구현)
```

```python
# 일부만 구현하면 여전히 추상 클래스
class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"
    # move() 미구현

# cat = Cat()  # TypeError: Can't instantiate abstract class
```

## 추상 프로퍼티

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        """면적 (구현 필수)"""
        pass
    
    @property
    @abstractmethod
    def perimeter(self) -> float:
        """둘레 (구현 필수)"""
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

rect = Rectangle(3, 4)
print(rect.area)       # 12
print(rect.perimeter)  # 14
```

## 추상 클래스메서드/정적메서드

```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @classmethod
    @abstractmethod
    def from_json(cls, data: str) -> "Serializer":
        """JSON에서 객체 생성"""
        pass
    
    @staticmethod
    @abstractmethod
    def validate(data: str) -> bool:
        """데이터 검증"""
        pass

class UserSerializer(Serializer):
    def __init__(self, name: str):
        self.name = name
    
    @classmethod
    def from_json(cls, data: str) -> "UserSerializer":
        import json
        parsed = json.loads(data)
        return cls(parsed['name'])
    
    @staticmethod
    def validate(data: str) -> bool:
        import json
        try:
            parsed = json.loads(data)
            return 'name' in parsed
        except:
            return False
```

## collections.abc - 표준 인터페이스

```python
from collections.abc import Iterable, Sequence, Mapping, MutableSequence

# isinstance 체크
print(isinstance([1, 2], Iterable))   # True
print(isinstance([1, 2], Sequence))   # True
print(isinstance({1, 2}, Sequence))   # False (set은 Sequence 아님)
print(isinstance({'a': 1}, Mapping))  # True
```

```python
# 커스텀 클래스에 인터페이스 구현
from collections.abc import Sequence

class MyList(Sequence):
    def __init__(self, data):
        self._data = list(data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __len__(self):
        return len(self._data)
    
    # Sequence의 다른 메서드들 (index, count, __contains__, __iter__, __reversed__)은
    # __getitem__과 __len__을 기반으로 자동 제공됨

ml = MyList([1, 2, 3, 2])
print(ml[0])        # 1
print(len(ml))      # 4
print(ml.count(2))  # 2 (자동 제공)
print(2 in ml)      # True (자동 제공)
```

## collections.abc 주요 클래스

| ABC | 추상 메서드 | Mixin 메서드 |
|-----|------------|-------------|
| `Iterable` | `__iter__` | - |
| `Iterator` | `__next__` | `__iter__` |
| `Sequence` | `__getitem__`, `__len__` | `__contains__`, `__iter__`, `__reversed__`, `index`, `count` |
| `MutableSequence` | 위 + `__setitem__`, `__delitem__`, `insert` | `append`, `clear`, `reverse`, `extend`, `pop`, `remove`, `__iadd__` |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, `__ne__` |
| `Set` | `__contains__`, `__iter__`, `__len__` | 비교 연산, `&`, `|`, `-`, `^` |

## ABC vs Protocol

```python
# ABC: 명시적 상속 필요 (nominal subtyping)
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

class Circle(Drawable):  # 명시적 상속 필요
    def draw(self) -> None:
        print("Drawing circle")

# Protocol: 상속 없이 구조만 맞으면 됨 (structural subtyping)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Square:  # 상속 없음!
    def draw(self) -> None:
        print("Drawing square")

def render(obj: Drawable) -> None:
    obj.draw()

render(Square())  # 타입 체커 OK (draw 메서드 있으므로)
```

| 특성 | ABC | Protocol |
|------|-----|----------|
| 상속 필요 | O | X |
| isinstance 체크 | O | X (runtime_checkable 필요) |
| 런타임 강제 | O | X (정적 분석만) |
| 용도 | 구현 강제 | 타입 힌트 |

## 가상 서브클래스 (register)

```python
from abc import ABC, abstractmethod

class Printable(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass

# 기존 클래스를 가상 서브클래스로 등록
@Printable.register
class int:
    pass  # int에 to_string이 없어도 등록 가능

print(isinstance(42, Printable))  # True (하지만 to_string 없음!)

# 주의: register는 구현을 검증하지 않음
```

## 자주 하는 실수/주의점

- **추상 메서드 호출**: `super().method()`로 기본 구현 호출 가능
- **메타클래스 충돌**: 다중 상속 시 메타클래스 충돌 주의
- **register 함정**: 가상 서브클래스는 구현 검증 안 함
- **@abstractmethod 순서**: 다른 데코레이터와 함께 쓸 때 **가장 안쪽**에

```python
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def method(self) -> str:
        return "base implementation"

class Derived(Base):
    def method(self) -> str:
        # 부모의 기본 구현 호출 가능
        base = super().method()
        return f"{base} + derived"
```

## 관련 링크(공식 문서)

- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [collections.abc — Abstract Base Classes for Containers](https://docs.python.org/3/library/collections.abc.html)
