---
draft: true
title: "[Python Cheatsheet] 25. Metaclass - 클래스를 만드는 클래스"
slug: "metaclass-type-creation-patterns-oop-metaprogramming-guide"
description: "파이썬 메타클래스를 빠르게 이해하기 위한 치트시트입니다. type(), __new__, __init_subclass__, 싱글톤/레지스트리 패턴 등 메타클래스의 핵심 개념과 실무 활용법을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 25
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - metaclass
  - 메타클래스
  - type
  - __new__
  - __init__
  - __call__
  - __init_subclass__
  - class-factory
  - 클래스팩토리
  - singleton
  - 싱글톤
  - registry
  - 레지스트리
  - metaprogramming
  - 메타프로그래밍
  - inheritance
  - 상속
  - class-creation
  - 클래스생성
  - dynamic-class
  - 동적클래스
  - oop
  - 객체지향
  - advanced
  - 고급
  - __class__
  - __bases__
  - __mro__
  - method-resolution-order
  - 메서드해결순서
  - abc
  - abstract
  - 추상
  - decorator
  - 데코레이터
  - __prepare__
  - namespace
  - 네임스페이스
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
메타클래스는 **클래스를 만드는 클래스**입니다. 파이썬에서 클래스 자체도 객체이며, 메타클래스는 그 클래스 객체의 타입입니다. 이 치트시트는 메타클래스의 핵심 개념과 실무 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- 클래스 생성 시점에 **자동으로 검증/등록/수정**하고 싶을 때
- 싱글톤, 레지스트리 같은 **클래스 레벨 패턴**을 구현할 때
- `__init_subclass__`로 부족할 때 더 강력한 제어가 필요할 때

## 핵심 개념

```python
# 모든 클래스는 type의 인스턴스
class Foo:
    pass

print(type(Foo))        # <class 'type'>
print(type(Foo()))      # <class '__main__.Foo'>
print(isinstance(Foo, type))  # True
```

- `type`은 기본 메타클래스
- `class Foo: pass`는 `Foo = type('Foo', (), {})`와 동일
- 커스텀 메타클래스: `type`을 상속받아 정의

## 최소 예제

### 1. type()으로 동적 클래스 생성

```python
# type(name, bases, namespace)
Dog = type('Dog', (), {
    'species': 'Canis familiaris',
    'bark': lambda self: print('Woof!')
})

d = Dog()
d.bark()  # Woof!
print(Dog.species)  # Canis familiaris
```

### 2. 커스텀 메타클래스 기본

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        # 클래스 생성 전에 namespace 수정 가능
        namespace['created_by'] = 'MyMeta'
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=MyMeta):
    pass

# 출력: Creating class: MyClass
print(MyClass.created_by)  # MyMeta
```

### 3. 싱글톤 패턴

```python
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Connecting...")

db1 = Database()  # Connecting...
db2 = Database()  # (출력 없음 - 같은 인스턴스)
print(db1 is db2)  # True
```

### 4. 클래스 레지스트리

```python
class PluginMeta(type):
    registry = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'Plugin':  # 베이스 클래스 제외
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class JSONPlugin(Plugin):
    pass

class XMLPlugin(Plugin):
    pass

print(PluginMeta.registry)
# {'JSONPlugin': <class 'JSONPlugin'>, 'XMLPlugin': <class 'XMLPlugin'>}
```

### 5. __init_subclass__ (Python 3.6+, 더 간단한 대안)

```python
class Plugin:
    registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[cls.__name__] = cls

class JSONPlugin(Plugin):
    pass

print(Plugin.registry)  # {'JSONPlugin': <class 'JSONPlugin'>}
```

## 메타클래스 메서드 흐름

```python
class Meta(type):
    def __prepare__(mcs, name, bases):
        """클래스 namespace 딕셔너리 반환 (Python 3+)"""
        print(f"1. __prepare__: {name}")
        return {}
    
    def __new__(mcs, name, bases, namespace):
        """클래스 객체 생성"""
        print(f"2. __new__: {name}")
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        """클래스 객체 초기화"""
        print(f"3. __init__: {name}")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        """인스턴스 생성 시 호출"""
        print(f"4. __call__: creating instance of {cls.__name__}")
        return super().__call__(*args, **kwargs)

class MyClass(metaclass=Meta):
    pass
# 출력: 1. __prepare__, 2. __new__, 3. __init__

obj = MyClass()
# 출력: 4. __call__: creating instance of MyClass
```

## 자주 하는 실수

### 1. 메타클래스 충돌

```python
class Meta1(type): pass
class Meta2(type): pass

class A(metaclass=Meta1): pass
class B(metaclass=Meta2): pass

# TypeError: metaclass conflict
# class C(A, B): pass

# 해결: 공통 메타클래스 상속
class Meta3(Meta1, Meta2): pass
class C(A, B, metaclass=Meta3): pass
```

### 2. __init_subclass__로 충분한 경우 메타클래스 사용

```python
# 과도한 사용 - 메타클래스
class ValidateMeta(type):
    def __new__(mcs, name, bases, namespace):
        if 'process' not in namespace:
            raise TypeError(f"{name} must define process()")
        return super().__new__(mcs, name, bases, namespace)

# 더 간단한 대안 - __init_subclass__
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'process'):
            raise TypeError(f"{cls.__name__} must define process()")
```

## 한눈에 정리

| 용도 | 방법 | 복잡도 |
|------|------|--------|
| 서브클래스 등록/검증 | `__init_subclass__` | 낮음 |
| 클래스 속성 자동 추가 | 메타클래스 `__new__` | 중간 |
| 싱글톤 패턴 | 메타클래스 `__call__` | 중간 |
| namespace 커스터마이징 | `__prepare__` | 높음 |

## 언제 메타클래스를 쓰나?

1. `__init_subclass__`로 부족할 때
2. 클래스 생성 **전**에 namespace를 수정해야 할 때
3. 프레임워크/라이브러리 개발 시

> "메타클래스는 99%의 사용자가 절대 걱정할 필요가 없는 더 깊은 마법입니다." - Tim Peters

## 참고

- [Python Data Model - Metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)
- [PEP 3115 - Metaclasses in Python 3](https://peps.python.org/pep-3115/)
- [__init_subclass__](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation)
