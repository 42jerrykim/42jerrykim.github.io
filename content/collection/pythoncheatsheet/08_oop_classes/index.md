---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 08. OOP & Classes - 클래스/상속/프로퍼티"
slug: "oop-and-classes-object-oriented-class-inheritance-super-constructor"
description: "파이썬 객체지향 프로그래밍을 빠르게 쓰기 위한 치트시트입니다. class 정의, __init__, 상속과 super(), @property, __slots__, 매직 메서드 기본과 실무에서 자주 만나는 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 8
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - oop
  - object-oriented
  - 객체지향
  - class
  - classes
  - 클래스
  - inheritance
  - 상속
  - super
  - __init__
  - constructor
  - 생성자
  - instance
  - 인스턴스
  - attribute
  - 속성
  - method
  - 메서드
  - self
  - cls
  - classmethod
  - staticmethod
  - property
  - 프로퍼티
  - getter
  - setter
  - __slots__
  - slots
  - magic-method
  - dunder
  - __str__
  - __repr__
  - __eq__
  - encapsulation
  - 캡슐화
  - polymorphism
  - 다형성
  - composition
  - 합성
  - mro
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - design
  - 설계
---
파이썬의 클래스는 데이터와 동작을 묶는 기본 단위입니다. 이 치트시트는 class 정의, 상속과 super(), @property, __slots__, 자주 쓰는 매직 메서드를 빠르게 정리합니다.

## 언제 이 치트시트를 보나?

- 데이터와 관련 동작을 **하나의 단위**로 묶고 싶을 때
- 상속/오버라이딩 문법이 헷갈릴 때

## 핵심 패턴

- `__init__`: 인스턴스 초기화 (생성자 역할)
- `self`: 인스턴스 자신을 가리킴 (첫 번째 인자로 자동 전달)
- 상속: `class Child(Parent):` + `super().__init__(...)`
- `@property`: getter/setter를 메서드처럼 정의, 속성처럼 접근
- `__slots__`: 메모리 절약 + 오타 방지

## 최소 예제

```python
# 기본 클래스 정의
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
    
    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age})"

p = Person("Alice", 30)
print(p.greet())  # Hello, I'm Alice
print(p)          # Person(name='Alice', age=30)
```

```python
# 상속과 super()
class Employee(Person):
    def __init__(self, name: str, age: int, emp_id: str):
        super().__init__(name, age)  # 부모 __init__ 호출
        self.emp_id = emp_id
    
    def greet(self) -> str:  # 오버라이딩
        return f"{super().greet()}, ID: {self.emp_id}"

e = Employee("Bob", 25, "E001")
print(e.greet())  # Hello, I'm Bob, ID: E001
```

```python
# @property - getter/setter
class Circle:
    def __init__(self, radius: float):
        self._radius = radius  # 관례: _로 시작 = "내부용"
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("radius must be non-negative")
        self._radius = value
    
    @property
    def area(self) -> float:  # 읽기 전용 프로퍼티
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)  # 5
print(c.area)    # 78.53975
c.radius = 10    # setter 호출
```

```python
# __slots__ - 메모리 절약 + 오타 방지
class Point:
    __slots__ = ("x", "y")
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

p = Point(1, 2)
# p.z = 3  # AttributeError: 'Point' object has no attribute 'z'
```

```python
# classmethod vs staticmethod
class MyClass:
    count = 0  # 클래스 변수
    
    def __init__(self):
        MyClass.count += 1
    
    @classmethod
    def get_count(cls) -> int:  # cls = 클래스 자체
        return cls.count
    
    @staticmethod
    def utility(x: int) -> int:  # self/cls 없음
        return x * 2

print(MyClass.get_count())  # 0
obj = MyClass()
print(MyClass.get_count())  # 1
print(MyClass.utility(5))   # 10
```

## 자주 쓰는 매직 메서드

| 메서드 | 용도 | 예시 |
|--------|------|------|
| `__init__` | 초기화 | `obj = MyClass()` |
| `__repr__` | 개발자용 문자열 | `repr(obj)` |
| `__str__` | 사용자용 문자열 | `str(obj)`, `print(obj)` |
| `__eq__` | 동등 비교 | `obj1 == obj2` |
| `__hash__` | 해시 (set/dict 키) | `hash(obj)` |
| `__len__` | 길이 | `len(obj)` |
| `__getitem__` | 인덱싱 | `obj[key]` |
| `__iter__` | 이터레이션 | `for x in obj` |
| `__call__` | 호출 가능 | `obj()` |

## 자주 하는 실수/주의점

- **클래스 변수 vs 인스턴스 변수**: 클래스 본문에 정의하면 모든 인스턴스가 공유
- **가변 기본값**: `def __init__(self, items=[])` → 모든 인스턴스가 같은 리스트 공유 (함정!)
- `__repr__` 없으면 디버깅 시 `<MyClass object at 0x...>`만 보임
- `__eq__` 정의하면 `__hash__`도 함께 고려 (기본적으로 None이 됨)
- 다중 상속은 MRO(Method Resolution Order) 이해 필요 → `MyClass.__mro__`로 확인

## dataclass와의 비교

```python
# 일반 클래스
class PersonManual:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"PersonManual(name={self.name!r}, age={self.age})"
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

# dataclass - 위와 동일한 기능 자동 생성
from dataclasses import dataclass

@dataclass
class PersonAuto:
    name: str
    age: int
```

→ 단순 데이터 컨테이너는 `@dataclass` 권장 (17챕터 참고)

## 관련 링크(공식 문서)

- [Classes](https://docs.python.org/3/tutorial/classes.html)
- [Data Model (Magic Methods)](https://docs.python.org/3/reference/datamodel.html)
