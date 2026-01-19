---
draft: true
title: "[Python Cheatsheet] 34. pprint & reprlib - 예쁜 출력과 요약"
slug: "pprint-and-reprlib-pretty-print-repr-debugging-logging-data-structure"
description: "파이썬 pprint와 reprlib 모듈을 빠르게 사용하기 위한 치트시트입니다. 복잡한 자료구조를 읽기 좋게 출력하고, 긴 객체를 적절히 요약하는 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 34
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - pprint
  - pretty-print
  - 예쁜출력
  - reprlib
  - repr
  - 요약
  - debugging
  - 디버깅
  - logging
  - 로깅
  - data-structure
  - 자료구조
  - nested
  - 중첩
  - dict
  - 딕셔너리
  - list
  - 리스트
  - json
  - formatting
  - 포맷팅
  - truncate
  - 자르기
  - ellipsis
  - 말줄임
  - width
  - 너비
  - depth
  - 깊이
  - indent
  - 들여쓰기
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`pprint`는 복잡한 자료구조를 **들여쓰기와 줄바꿈으로 읽기 좋게** 출력합니다. `reprlib`는 긴 객체를 **적절한 길이로 요약**합니다. 디버깅과 로깅에 유용합니다.

## 언제 이 치트시트를 보나?

- 중첩된 딕셔너리/리스트를 **가독성 있게 출력**하고 싶을 때
- API 응답이나 설정 파일을 **디버깅**할 때
- 로그에 **긴 객체를 요약**해서 남기고 싶을 때

## pprint 핵심 함수

```python
from pprint import pprint, pformat

pprint(obj)              # 예쁘게 출력
pformat(obj)             # 예쁜 문자열 반환
pprint(obj, width=80)    # 줄 너비 지정
pprint(obj, depth=2)     # 깊이 제한
pprint(obj, indent=4)    # 들여쓰기 크기
```

## 최소 예제

### 1. 기본 pprint

```python
from pprint import pprint

data = {
    'name': 'Alice',
    'age': 30,
    'skills': ['Python', 'JavaScript', 'SQL'],
    'address': {
        'city': 'Seoul',
        'country': 'Korea'
    }
}

# 일반 print
print(data)
# {'name': 'Alice', 'age': 30, 'skills': ['Python', 'JavaScript', 'SQL'], 'address': {'city': 'Seoul', 'country': 'Korea'}}

# pprint
pprint(data)
# {'address': {'city': 'Seoul', 'country': 'Korea'},
#  'age': 30,
#  'name': 'Alice',
#  'skills': ['Python', 'JavaScript', 'SQL']}
```

### 2. width - 줄 너비 제어

```python
from pprint import pprint

data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

pprint(data, width=20)
# {'a': 1,
#  'b': 2,
#  'c': 3,
#  'd': 4,
#  'e': 5}

pprint(data, width=80)
# {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
```

### 3. depth - 깊이 제한

```python
from pprint import pprint

deep = {'level1': {'level2': {'level3': {'level4': 'deep'}}}}

pprint(deep, depth=2)
# {'level1': {'level2': {...}}}
```

### 4. indent - 들여쓰기

```python
from pprint import pprint

data = {'a': [1, 2, 3], 'b': [4, 5, 6]}

pprint(data, indent=4, width=20)
# {   'a': [   1,
#              2,
#              3],
#     'b': [   4,
#              5,
#              6]}
```

### 5. pformat - 문자열로 반환

```python
from pprint import pformat

data = {'key': 'value', 'items': [1, 2, 3]}

formatted = pformat(data)
print(f"Data: {formatted}")

# 로깅에 활용
import logging
logging.info("Received data:\n%s", pformat(data))
```

### 6. sort_dicts - 정렬 제어 (Python 3.8+)

```python
from pprint import pprint

data = {'z': 1, 'a': 2, 'm': 3}

# 기본값: 키 정렬
pprint(data)
# {'a': 2, 'm': 3, 'z': 1}

# 원래 순서 유지
pprint(data, sort_dicts=False)
# {'z': 1, 'a': 2, 'm': 3}
```

### 7. PrettyPrinter 클래스

```python
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2, width=40, depth=3)

data = {'users': [{'name': 'Alice'}, {'name': 'Bob'}]}
pp.pprint(data)
```

---

## reprlib - 객체 요약

### 8. 기본 repr vs reprlib.repr

```python
import reprlib

long_list = list(range(100))

print(repr(long_list))
# [0, 1, 2, 3, 4, ... 95, 96, 97, 98, 99]  (전체 출력)

print(reprlib.repr(long_list))
# [0, 1, 2, 3, 4, 5, ...]  (요약)
```

### 9. 문자열 요약

```python
import reprlib

long_string = "A" * 100

print(repr(long_string))
# 'AAAA...AAAA' (100자 전체)

print(reprlib.repr(long_string))
# 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA...'  (약 30자로 제한)
```

### 10. 중첩 구조 요약

```python
import reprlib

nested = [[list(range(10)) for _ in range(5)] for _ in range(3)]

print(reprlib.repr(nested))
# [[[0, 1, 2, 3, 4, 5, ...], [0, 1, 2, 3, 4, 5, ...], ...], ...]
```

### 11. Repr 클래스로 커스터마이징

```python
import reprlib

class MyRepr(reprlib.Repr):
    def __init__(self):
        super().__init__()
        self.maxlist = 3      # 리스트 요소 최대 3개
        self.maxstring = 20   # 문자열 최대 20자
        self.maxother = 30    # 기타 객체 최대 30자

my_repr = MyRepr()

print(my_repr.repr(list(range(100))))
# [0, 1, 2, ...]

print(my_repr.repr("A" * 50))
# 'AAAAAAAAAAAAAAAAAAAA...'
```

### 12. 클래스에 __repr__ 구현 시 활용

```python
import reprlib

class DataContainer:
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"DataContainer({reprlib.repr(self.data)})"

container = DataContainer(list(range(100)))
print(container)
# DataContainer([0, 1, 2, 3, 4, 5, ...])
```

## pprint vs json.dumps

```python
from pprint import pprint
import json

data = {'name': 'Alice', 'items': [1, 2, 3]}

# pprint - Python 표현식 유지
pprint(data)
# {'items': [1, 2, 3], 'name': 'Alice'}

# json.dumps - JSON 형식
print(json.dumps(data, indent=2))
# {
#   "name": "Alice",
#   "items": [1, 2, 3]
# }

# json은 문자열만, pprint는 모든 Python 객체
```

## 자주 하는 실수

### 1. pprint 반환값 사용

```python
from pprint import pprint, pformat

# pprint는 None 반환
result = pprint({'a': 1})  # 출력됨
print(result)  # None

# 문자열이 필요하면 pformat 사용
formatted = pformat({'a': 1})
```

### 2. 파일에 쓸 때

```python
from pprint import pprint

data = {'key': 'value'}

# stream 파라미터 사용
with open('output.txt', 'w') as f:
    pprint(data, stream=f)
```

## 한눈에 정리

| 모듈 | 함수 | 용도 |
|------|------|------|
| pprint | `pprint()` | 예쁘게 출력 |
| pprint | `pformat()` | 예쁜 문자열 반환 |
| reprlib | `repr()` | 요약된 표현 |
| reprlib | `Repr` 클래스 | 커스텀 요약 |

## 참고

- [pprint - Python Docs](https://docs.python.org/3/library/pprint.html)
- [reprlib - Python Docs](https://docs.python.org/3/library/reprlib.html)
