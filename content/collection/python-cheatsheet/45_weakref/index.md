---

image: "wordcloud.png"
title: "[Python Cheatsheet] 45. weakref - 약한 참조와 메모리 관리"
slug: "weakref-memory-leak-circular-reference-garbage-collection-cache"
description: "파이썬 weakref 모듈을 빠르게 사용하기 위한 치트시트입니다. 약한 참조, WeakValueDictionary, WeakSet, 순환 참조 방지, 캐시 구현 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 45
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - weakref
  - weak-reference
  - 약한참조
  - memory
  - 메모리
  - garbage-collection
  - 가비지컬렉션
  - gc
  - reference-counting
  - 참조카운팅
  - circular-reference
  - 순환참조
  - WeakValueDictionary
  - WeakKeyDictionary
  - WeakSet
  - ref
  - proxy
  - finalize
  - cache
  - 캐시
  - memory-leak
  - 메모리누수
  - advanced
  - 고급
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`weakref`는 **객체에 대한 약한 참조**를 만들어 가비지 컬렉션을 방해하지 않으면서 객체를 참조합니다. 캐시, 순환 참조 방지, 옵저버 패턴 등에 유용합니다.

## 언제 이 치트시트를 보나?

- **캐시**를 만들되 메모리 부족 시 자동 정리되게 하고 싶을 때
- **순환 참조**로 인한 메모리 누수를 방지할 때
- 객체 **생존 여부를 확인**하면서 참조하고 싶을 때

## 핵심 개념

- **강한 참조**: 일반적인 참조, 참조 카운트 증가
- **약한 참조**: 참조 카운트 증가 안 함, 객체 삭제 시 자동 무효화

```python
import weakref

obj = SomeClass()
ref = weakref.ref(obj)  # 약한 참조 생성
obj_again = ref()       # 객체 접근 (None일 수 있음)
```

## 최소 예제

### 1. 기본 약한 참조

```python
import weakref

class MyClass:
    def __init__(self, name):
        self.name = name

obj = MyClass("example")
ref = weakref.ref(obj)

# 참조로 객체 접근
print(ref())       # <MyClass object>
print(ref().name)  # example

# 원본 삭제
del obj

# 이제 None 반환
print(ref())  # None
```

### 2. 콜백 함수

```python
import weakref

class Resource:
    def __init__(self, name):
        self.name = name

def callback(ref):
    print(f"Object was garbage collected!")

obj = Resource("data")
ref = weakref.ref(obj, callback)

del obj
# 출력: Object was garbage collected!
```

### 3. WeakValueDictionary - 자동 정리 캐시

```python
import weakref

class ExpensiveObject:
    def __init__(self, id):
        self.id = id
        print(f"Created {id}")

# 약한 참조 딕셔너리
cache = weakref.WeakValueDictionary()

def get_object(id):
    if id not in cache:
        cache[id] = ExpensiveObject(id)
    return cache[id]

obj1 = get_object(1)  # Created 1
obj2 = get_object(1)  # 캐시에서 반환
print(obj1 is obj2)   # True

del obj1, obj2
# 강한 참조가 없어지면 캐시에서 자동 제거
print(dict(cache))    # {}
```

### 4. WeakKeyDictionary - 객체에 데이터 연결

```python
import weakref

class User:
    def __init__(self, name):
        self.name = name

# 객체를 키로 사용하는 약한 참조 딕셔너리
extra_data = weakref.WeakKeyDictionary()

user = User("Alice")
extra_data[user] = {"score": 100, "level": 5}

print(extra_data[user])  # {'score': 100, 'level': 5}

del user
# user 객체 삭제 시 extra_data에서도 자동 제거
print(dict(extra_data))  # {}
```

### 5. WeakSet

```python
import weakref

class Observer:
    def __init__(self, name):
        self.name = name
    
    def notify(self, msg):
        print(f"{self.name} received: {msg}")

class Subject:
    def __init__(self):
        self._observers = weakref.WeakSet()
    
    def register(self, observer):
        self._observers.add(observer)
    
    def notify_all(self, msg):
        for observer in self._observers:
            observer.notify(msg)

subject = Subject()
obs1 = Observer("Observer1")
obs2 = Observer("Observer2")

subject.register(obs1)
subject.register(obs2)
subject.notify_all("Hello")
# Observer1 received: Hello
# Observer2 received: Hello

del obs1
subject.notify_all("World")
# Observer2 received: World
# (obs1은 자동으로 제거됨)
```

### 6. proxy - 투명한 약한 참조

```python
import weakref

class Data:
    def __init__(self, value):
        self.value = value
    
    def get(self):
        return self.value

obj = Data(42)
proxy = weakref.proxy(obj)

# ref()와 달리 직접 사용 가능
print(proxy.value)   # 42
print(proxy.get())   # 42

del obj
# 이제 접근하면 ReferenceError
# print(proxy.value)  # ReferenceError: weakly-referenced object no longer exists
```

### 7. finalize - 정리 콜백

```python
import weakref

class Resource:
    def __init__(self, name):
        self.name = name

def cleanup(name):
    print(f"Cleaning up {name}")

obj = Resource("data")
weakref.finalize(obj, cleanup, obj.name)

del obj
# 출력: Cleaning up data
```

### 8. 순환 참조 방지

```python
import weakref

class Parent:
    def __init__(self, name):
        self.name = name
        self.children = []

class Child:
    def __init__(self, name, parent):
        self.name = name
        # 약한 참조로 순환 참조 방지
        self._parent_ref = weakref.ref(parent)
    
    @property
    def parent(self):
        return self._parent_ref()

parent = Parent("Parent")
child = Child("Child", parent)
parent.children.append(child)

# 순환 참조가 있어도 gc가 정상 작동
print(child.parent.name)  # Parent
```

### 9. 캐시 with TTL 패턴

```python
import weakref
from functools import lru_cache

class CachedLoader:
    _cache = weakref.WeakValueDictionary()
    
    @classmethod
    def load(cls, key):
        obj = cls._cache.get(key)
        if obj is None:
            obj = cls._expensive_load(key)
            cls._cache[key] = obj
        return obj
    
    @staticmethod
    def _expensive_load(key):
        print(f"Loading {key}...")
        return {"data": key}

# 사용
data1 = CachedLoader.load("key1")  # Loading key1...
data2 = CachedLoader.load("key1")  # 캐시에서 반환

# 강한 참조 유지 중에는 캐시 유지
del data1
data3 = CachedLoader.load("key1")  # 아직 data2가 있어서 캐시 히트
```

## 약한 참조 불가능한 타입

```python
import weakref

# 약한 참조 불가능
# weakref.ref(42)       # TypeError
# weakref.ref("string") # TypeError
# weakref.ref([1, 2])   # TypeError
# weakref.ref((1, 2))   # TypeError

# 약한 참조 가능
class MyClass: pass
weakref.ref(MyClass())  # OK

# __slots__가 있으면 __weakref__ 포함 필요
class Slotted:
    __slots__ = ['value', '__weakref__']
```

## 자주 하는 실수

### 1. 약한 참조 결과 확인 없이 사용

```python
import weakref

ref = weakref.ref(some_object)

# 위험: 객체가 삭제되었을 수 있음
# ref().method()

# 안전: None 체크
obj = ref()
if obj is not None:
    obj.method()
```

### 2. 임시 객체에 약한 참조

```python
import weakref

# 잘못된 사용: 임시 객체는 바로 사라짐
ref = weakref.ref(SomeClass())
print(ref())  # None (이미 삭제됨)

# 올바른 사용: 강한 참조 유지
obj = SomeClass()
ref = weakref.ref(obj)
```

## 한눈에 정리

| 도구 | 용도 |
|------|------|
| `ref()` | 약한 참조 생성 |
| `proxy()` | 투명한 약한 참조 |
| `WeakValueDictionary` | 값이 약한 참조인 딕셔너리 |
| `WeakKeyDictionary` | 키가 약한 참조인 딕셔너리 |
| `WeakSet` | 약한 참조 집합 |
| `finalize()` | 객체 삭제 시 콜백 |

## 참고

- [weakref - Python Docs](https://docs.python.org/3/library/weakref.html)
- [Garbage Collection](https://docs.python.org/3/library/gc.html)
