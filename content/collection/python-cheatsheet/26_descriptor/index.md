---

image: "wordcloud.png"
title: "[Python Cheatsheet] 26. Descriptor - 속성 접근 제어 프로토콜"
slug: "descriptor-attribute-access-control-data-nondata-get-set-delete-property"
description: "파이썬 디스크립터를 빠르게 이해하기 위한 치트시트입니다. __get__, __set__, __delete__ 프로토콜, 데이터/비데이터 디스크립터 차이, property 구현 원리를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 26
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - descriptor
  - 디스크립터
  - __get__
  - __set__
  - __delete__
  - __set_name__
  - data-descriptor
  - 데이터디스크립터
  - non-data-descriptor
  - 비데이터디스크립터
  - property
  - 프로퍼티
  - attribute-access
  - 속성접근
  - protocol
  - 프로토콜
  - oop
  - 객체지향
  - validation
  - 검증
  - lazy-loading
  - 지연로딩
  - caching
  - 캐싱
  - bound-method
  - 바운드메서드
  - classmethod
  - staticmethod
  - slots
  - __slots__
  - advanced
  - 고급
  - metaprogramming
  - 메타프로그래밍
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
디스크립터는 **속성 접근을 커스터마이징**하는 파이썬의 핵심 프로토콜입니다. `@property`, `@classmethod`, `@staticmethod` 모두 디스크립터로 구현됩니다. 이 치트시트는 디스크립터의 핵심 개념과 실무 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- **속성 접근 시 자동 검증/변환**이 필요할 때
- 여러 클래스에서 **재사용 가능한 속성 로직**을 만들 때
- `@property`의 동작 원리를 이해하고 싶을 때

## 핵심 개념

디스크립터 = `__get__`, `__set__`, `__delete__` 중 하나 이상을 정의한 객체

```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        """obj.attr 접근 시 호출"""
        pass
    
    def __set__(self, obj, value):
        """obj.attr = value 할당 시 호출"""
        pass
    
    def __delete__(self, obj):
        """del obj.attr 삭제 시 호출"""
        pass
```

## 디스크립터 종류

| 종류 | 정의 | 우선순위 |
|------|------|----------|
| 데이터 디스크립터 | `__get__` + `__set__` (또는 `__delete__`) | 인스턴스 `__dict__`보다 높음 |
| 비데이터 디스크립터 | `__get__`만 | 인스턴스 `__dict__`보다 낮음 |

## 최소 예제

### 1. 타입 검증 디스크립터

```python
class TypedAttribute:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        obj.__dict__[self.name] = value

class Person:
    name = TypedAttribute('name', str)
    age = TypedAttribute('age', int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
# p.age = "thirty"  # TypeError: age must be int
```

### 2. __set_name__ 활용 (Python 3.6+)

```python
class TypedAttribute:
    def __init__(self, expected_type):
        self.expected_type = expected_type
    
    def __set_name__(self, owner, name):
        """클래스 정의 시 자동 호출 - 속성 이름 자동 설정"""
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        obj.__dict__[self.name] = value

class Person:
    name = TypedAttribute(str)  # 이름 자동 설정
    age = TypedAttribute(int)
```

### 3. 지연 로딩 (Lazy Loading)

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # 첫 접근 시 계산 후 인스턴스에 캐시
        value = self.func(obj)
        obj.__dict__[self.name] = value  # 비데이터라 이후 직접 반환
        return value

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def summary(self):
        print("Computing summary...")
        return {'mean': sum(self.data) / len(self.data)}

analyzer = DataAnalyzer([1, 2, 3, 4, 5])
print(analyzer.summary)  # Computing summary... {'mean': 3.0}
print(analyzer.summary)  # {'mean': 3.0} (캐시됨)
```

### 4. property 직접 구현

```python
class MyProperty:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
    
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel)

class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @MyProperty
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be positive")
        self._radius = value
```

### 5. 범위 검증 디스크립터

```python
class Range:
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        obj.__dict__[self.name] = value

class Product:
    price = Range(min_val=0)
    quantity = Range(min_val=0, max_val=1000)
```

## 속성 조회 순서

```
obj.attr 접근 시:
1. 데이터 디스크립터 (type(obj).__dict__에서)
2. 인스턴스 __dict__
3. 비데이터 디스크립터 (type(obj).__dict__에서)
4. __getattr__ (정의된 경우)
```

## 자주 하는 실수

### 1. 클래스 속성으로 값 저장

```python
# 잘못된 예 - 모든 인스턴스가 값 공유
class BadDescriptor:
    def __init__(self):
        self.value = None  # 클래스 레벨!
    
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        self.value = value  # 모든 인스턴스에 영향

# 올바른 예 - 인스턴스 __dict__ 사용
class GoodDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        obj.__dict__[self.name] = value
```

### 2. obj가 None인 경우 처리 누락

```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        # 클래스에서 직접 접근 시 obj는 None
        if obj is None:
            return self  # 디스크립터 자체 반환
        return obj.__dict__.get(self.name)
```

## 한눈에 정리

| 패턴 | 사용 사례 | 디스크립터 종류 |
|------|----------|----------------|
| 타입/범위 검증 | 입력 검증 | 데이터 |
| Lazy property | 캐싱, 지연 계산 | 비데이터 |
| Read-only | 상수, 계산 속성 | 데이터 (`__set__`에서 에러) |
| Logging/감사 | 접근 추적 | 데이터 |

## 참고

- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Data Model - Descriptors](https://docs.python.org/3/reference/datamodel.html#descriptors)
