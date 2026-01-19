---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 42. pickle - 객체 직렬화 (보안 주의)"
slug: "pickle-serialization-deserialization-security-best-practices"
description: "파이썬 pickle 모듈을 빠르게 쓰기 위한 치트시트입니다. 객체 직렬화/역직렬화, dump/load 패턴, 프로토콜 버전, 보안 위험과 대안(JSON, shelve)을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 42
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - pickle
  - serialization
  - 직렬화
  - deserialization
  - 역직렬화
  - marshal
  - dump
  - load
  - dumps
  - loads
  - object
  - 객체
  - binary
  - 바이너리
  - protocol
  - 프로토콜
  - security
  - 보안
  - vulnerability
  - 취약점
  - arbitrary-code-execution
  - 임의코드실행
  - shelve
  - json
  - persistence
  - 영속성
  - cache
  - 캐시
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - warning
  - 경고
---
pickle은 파이썬 객체를 바이너리로 직렬화/역직렬화합니다. 이 치트시트는 dump/load 기본, 프로토콜 버전, **보안 위험**과 안전한 대안을 정리합니다.

## 언제 이 치트시트를 보나?

- 파이썬 객체를 **파일에 저장**하거나 불러와야 할 때
- ML 모델, 캐시 데이터 등 **복잡한 객체**를 직렬화해야 할 때

## ⚠️ 보안 경고

> **신뢰할 수 없는 소스의 pickle 데이터는 절대 로드하지 마세요!**
> pickle.load()는 **임의의 코드를 실행**할 수 있습니다.

```python
# 악의적인 pickle 예시 (이렇게 될 수 있음)
import pickle
import os

class Malicious:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))  # 시스템 명령 실행!

# 이 pickle을 load하면 rm -rf / 실행됨
```

## 핵심 패턴

- `pickle.dump(obj, file)`: 객체를 파일에 저장
- `pickle.load(file)`: 파일에서 객체 로드
- `pickle.dumps(obj)`: 객체를 bytes로 변환
- `pickle.loads(data)`: bytes에서 객체 복원
- **신뢰할 수 있는 데이터만** 로드할 것

## 기본 사용법

```python
import pickle

# 객체를 파일에 저장
data = {
    'name': 'Alice',
    'scores': [90, 85, 88],
    'metadata': {'version': 1}
}

with open('data.pkl', 'wb') as f:  # 바이너리 모드
    pickle.dump(data, f)

# 파일에서 객체 로드
with open('data.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

print(loaded_data)
# {'name': 'Alice', 'scores': [90, 85, 88], 'metadata': {'version': 1}}
```

```python
# bytes로 직렬화/역직렬화
data = [1, 2, 3, {'key': 'value'}]

# 직렬화
pickled_bytes = pickle.dumps(data)
print(type(pickled_bytes))  # <class 'bytes'>

# 역직렬화
restored_data = pickle.loads(pickled_bytes)
print(restored_data)  # [1, 2, 3, {'key': 'value'}]
```

## 프로토콜 버전

```python
import pickle

data = {'key': 'value'}

# 프로토콜 지정 (높을수록 효율적이지만 호환성 낮음)
# Protocol 0: ASCII (읽기 가능, 느림)
# Protocol 1: 이전 바이너리
# Protocol 2: Py2 호환
# Protocol 3: Py3 전용 (기본)
# Protocol 4: Py3.4+ (큰 객체 지원)
# Protocol 5: Py3.8+ (out-of-band 데이터)

# 최신 프로토콜 사용
pickled = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

# 특정 프로토콜 지정
pickled = pickle.dumps(data, protocol=4)

# 기본 프로토콜 확인
print(pickle.DEFAULT_PROTOCOL)  # 4 (Py3.8+)
```

## 커스텀 클래스 직렬화

```python
import pickle

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

# 커스텀 클래스도 직렬화 가능
person = Person("Alice", 30)

with open('person.pkl', 'wb') as f:
    pickle.dump(person, f)

with open('person.pkl', 'rb') as f:
    loaded_person = pickle.load(f)

print(loaded_person.greet())  # Hello, I'm Alice
```

```python
# __getstate__ / __setstate__로 직렬화 커스터마이징
class Connection:
    def __init__(self, host: str):
        self.host = host
        self._socket = None  # 직렬화 불가능한 객체
    
    def __getstate__(self):
        # 직렬화할 상태 반환
        state = self.__dict__.copy()
        del state['_socket']  # 소켓 제외
        return state
    
    def __setstate__(self, state):
        # 역직렬화 시 상태 복원
        self.__dict__.update(state)
        self._socket = None  # 다시 연결 필요
```

## 여러 객체 저장/로드

```python
import pickle

data1 = [1, 2, 3]
data2 = {'a': 1, 'b': 2}
data3 = "hello"

# 여러 객체 저장
with open('multi.pkl', 'wb') as f:
    pickle.dump(data1, f)
    pickle.dump(data2, f)
    pickle.dump(data3, f)

# 여러 객체 로드
with open('multi.pkl', 'rb') as f:
    loaded1 = pickle.load(f)
    loaded2 = pickle.load(f)
    loaded3 = pickle.load(f)
```

## shelve - 딕셔너리 스타일 영속성

```python
import shelve

# shelve는 pickle 기반의 딕셔너리 스타일 DB
with shelve.open('mydata') as db:
    db['users'] = ['Alice', 'Bob']
    db['config'] = {'debug': True}

with shelve.open('mydata') as db:
    print(db['users'])   # ['Alice', 'Bob']
    print(db['config'])  # {'debug': True}
```

## 안전한 대안

```python
# JSON (권장) - 기본 타입만
import json

data = {'name': 'Alice', 'scores': [90, 85]}
with open('data.json', 'w') as f:
    json.dump(data, f)

# MessagePack - 바이너리 JSON (더 빠름)
# pip install msgpack
import msgpack

packed = msgpack.packb(data)
unpacked = msgpack.unpackb(packed)

# dataclasses + JSON
from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    name: str
    age: int

user = User("Alice", 30)
json_str = json.dumps(asdict(user))
```

## 자주 하는 실수/주의점

- **보안 취약점**: 신뢰할 수 없는 pickle 데이터 로드 금지 (RCE 가능)
- **파이썬 버전 호환성**: 프로토콜 버전에 따라 다른 버전에서 로드 불가할 수 있음
- **클래스 변경 시 문제**: 클래스 구조가 변경되면 기존 pickle 로드 실패 가능
- **lambda/중첩 함수**: 직렬화 불가
- **파일/소켓/락 객체**: 직렬화 불가

```python
# pickle 로드 제한 (Py3.8+)
import pickle

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # 허용된 클래스만 로드
        if module == "builtins" and name in ("dict", "list", "str", "int"):
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(f"Not allowed: {module}.{name}")

def restricted_loads(data):
    return RestrictedUnpickler(io.BytesIO(data)).load()
```

## pickle vs 대안 비교

| 특성 | pickle | JSON | msgpack |
|------|--------|------|---------|
| 타입 지원 | 모든 파이썬 객체 | 기본 타입만 | 기본 타입만 |
| 보안 | ❌ 위험 | ✅ 안전 | ✅ 안전 |
| 속도 | 빠름 | 느림 | 매우 빠름 |
| 호환성 | 파이썬만 | 범용 | 범용 |
| 가독성 | ❌ 바이너리 | ✅ 텍스트 | ❌ 바이너리 |

## 관련 링크(공식 문서)

- [pickle — Python object serialization](https://docs.python.org/3/library/pickle.html)
- [shelve — Python object persistence](https://docs.python.org/3/library/shelve.html)
- [Security considerations](https://docs.python.org/3/library/pickle.html#restricting-globals)
