---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 30. collections 심화 - deque/namedtuple/ChainMap"
slug: "effective-collections-deque-namedtuple-chainmap-advanced-guide"
description: "파이썬 collections 모듈 심화 내용을 빠르게 쓰기 위한 치트시트입니다. deque(양방향 큐), namedtuple(명명된 튜플), ChainMap, OrderedDict 패턴과 Counter/defaultdict 복습을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 30
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - collections
  - deque
  - 덱
  - 양방향큐
  - double-ended-queue
  - namedtuple
  - 명명된튜플
  - ChainMap
  - OrderedDict
  - Counter
  - defaultdict
  - data-structures
  - 자료구조
  - queue
  - 큐
  - stack
  - 스택
  - performance
  - 성능
  - O(1)
  - append
  - appendleft
  - rotate
  - maxlen
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
collections 모듈은 기본 자료구조를 확장한 특수 컨테이너를 제공합니다. 이 치트시트는 deque, namedtuple, ChainMap, OrderedDict의 실전 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- **양쪽 끝에서 효율적 삽입/삭제**가 필요할 때 (deque)
- **읽기 쉬운 튜플**(필드명 접근)이 필요할 때 (namedtuple)
- 여러 딕셔너리를 **하나처럼** 접근하고 싶을 때 (ChainMap)

## 핵심 패턴

- `deque`: O(1) 양방향 삽입/삭제 + `maxlen`으로 고정 크기 버퍼
- `namedtuple`: 인덱스와 이름 둘 다로 접근 가능한 튜플
- `ChainMap`: 여러 딕셔너리를 순차 검색 (설정 우선순위 구현)
- `OrderedDict`: 삽입 순서 유지 (Py3.7+ dict도 유지하지만 추가 기능 있음)

## deque - 양방향 큐

```python
from collections import deque

# 생성
dq = deque([1, 2, 3])
dq = deque('abc')  # deque(['a', 'b', 'c'])

# 오른쪽 삽입/삭제 - O(1)
dq.append(4)       # [1, 2, 3, 4]
dq.pop()           # 4, dq = [1, 2, 3]

# 왼쪽 삽입/삭제 - O(1) (리스트는 O(n))
dq.appendleft(0)   # [0, 1, 2, 3]
dq.popleft()       # 0, dq = [1, 2, 3]

# 여러 요소 추가
dq.extend([4, 5])       # [1, 2, 3, 4, 5]
dq.extendleft([0, -1])  # [-1, 0, 1, 2, 3, 4, 5] (역순 삽입)
```

```python
# 회전
from collections import deque

dq = deque([1, 2, 3, 4, 5])

dq.rotate(2)   # 오른쪽으로 2칸: [4, 5, 1, 2, 3]
dq.rotate(-2)  # 왼쪽으로 2칸: [1, 2, 3, 4, 5]
```

```python
# 고정 크기 버퍼 (maxlen)
from collections import deque

# 최근 5개만 유지
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)

print(list(recent))  # [5, 6, 7, 8, 9]

# 슬라이딩 윈도우 평균
def moving_average(iterable, n):
    window = deque(maxlen=n)
    for x in iterable:
        window.append(x)
        if len(window) == n:
            yield sum(window) / n

list(moving_average([1, 2, 3, 4, 5, 6], 3))
# [2.0, 3.0, 4.0, 5.0]
```

## namedtuple - 명명된 튜플

```python
from collections import namedtuple

# 정의
Point = namedtuple('Point', ['x', 'y'])
# 또는
Point = namedtuple('Point', 'x y')
Point = namedtuple('Point', 'x, y')

# 생성
p = Point(10, 20)
p = Point(x=10, y=20)

# 접근
print(p.x, p.y)    # 이름으로 접근
print(p[0], p[1])  # 인덱스로 접근
x, y = p           # 언패킹

# 불변 (튜플이므로)
# p.x = 30  # AttributeError
```

```python
# 기본값 (Py3.7+)
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'], defaults=[0])
# z만 기본값 0

p1 = Point(1, 2)      # Point(x=1, y=2, z=0)
p2 = Point(1, 2, 3)   # Point(x=1, y=2, z=3)
```

```python
# 유용한 메서드
from collections import namedtuple

Point = namedtuple('Point', 'x y')
p = Point(10, 20)

# dict로 변환
print(p._asdict())  # {'x': 10, 'y': 20}

# 값 변경 (새 객체 반환)
p2 = p._replace(x=30)
print(p2)  # Point(x=30, y=20)

# dict/iterable에서 생성
data = {'x': 1, 'y': 2}
p = Point(**data)

data = [1, 2]
p = Point._make(data)
```

```python
# typing.NamedTuple (더 현대적)
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0  # 기본값
    
    def distance(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

p = Point(3, 4)
print(p.distance())  # 5.0
```

## ChainMap - 딕셔너리 체인

```python
from collections import ChainMap

# 여러 딕셔너리를 하나처럼 사용
defaults = {'theme': 'light', 'language': 'en', 'debug': False}
user_settings = {'theme': 'dark'}
cli_args = {'debug': True}

# 우선순위: cli_args > user_settings > defaults
config = ChainMap(cli_args, user_settings, defaults)

print(config['theme'])     # 'dark' (user_settings)
print(config['language'])  # 'en' (defaults)
print(config['debug'])     # True (cli_args)
```

```python
# 새 값 추가/변경 (첫 번째 딕셔너리에만 적용)
from collections import ChainMap

base = {'a': 1, 'b': 2}
overlay = {'b': 3}
cm = ChainMap(overlay, base)

cm['c'] = 4  # overlay에 추가됨
print(overlay)  # {'b': 3, 'c': 4}
print(base)     # {'a': 1, 'b': 2}
```

```python
# 새 컨텍스트 추가
from collections import ChainMap

defaults = {'x': 1}
cm = ChainMap(defaults)

# 새 레이어 추가 (스코프 구현 등)
with_override = cm.new_child({'x': 2, 'y': 3})
print(with_override['x'])  # 2
print(cm['x'])             # 1 (원본 유지)
```

## OrderedDict - 순서 유지 딕셔너리

```python
from collections import OrderedDict

# Py3.7+ 기본 dict도 삽입 순서 유지
# OrderedDict는 추가 기능 제공

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3

# 끝으로 이동
od.move_to_end('a')       # {'b': 2, 'c': 3, 'a': 1}
od.move_to_end('c', last=False)  # 앞으로: {'c': 3, 'b': 2, 'a': 1}

# 마지막 요소 제거
od.popitem()              # ('a', 1) - LIFO
od.popitem(last=False)    # ('c', 3) - FIFO
```

```python
# 순서를 고려한 비교
from collections import OrderedDict

od1 = OrderedDict([('a', 1), ('b', 2)])
od2 = OrderedDict([('b', 2), ('a', 1)])
d1 = {'a': 1, 'b': 2}
d2 = {'b': 2, 'a': 1}

print(od1 == od2)  # False (순서 다름)
print(d1 == d2)    # True (순서 무시)
```

## Counter / defaultdict 복습

```python
from collections import Counter, defaultdict

# Counter - 빈도수 계산
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
count = Counter(words)
print(count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count.most_common(2))  # [('apple', 3), ('banana', 2)]

# 연산
count1 = Counter(a=3, b=1)
count2 = Counter(a=1, b=2)
print(count1 + count2)  # Counter({'a': 4, 'b': 3})
print(count1 - count2)  # Counter({'a': 2}) (음수는 제외)

# defaultdict - 기본값 자동 생성
dd = defaultdict(list)
dd['fruits'].append('apple')
dd['fruits'].append('banana')
print(dd)  # defaultdict(<class 'list'>, {'fruits': ['apple', 'banana']})

dd = defaultdict(int)  # 기본값 0
for word in words:
    dd[word] += 1
```

## 자주 하는 실수/주의점

- **deque 인덱싱 O(n)**: 중간 접근이 많으면 리스트 사용
- **namedtuple은 불변**: 변경 가능하면 dataclass 사용
- **ChainMap 쓰기**: 첫 번째 딕셔너리에만 적용됨
- **Counter 음수**: `subtraction`은 음수를 만들지 않음 (`subtract()`는 만듦)

```python
from collections import Counter

c = Counter(a=3, b=1)
c.subtract(Counter(a=5))  # c = Counter({'b': 1, 'a': -2})
# c - Counter(a=5)는 음수 제외: Counter({'b': 1})
```

## 관련 링크(공식 문서)

- [collections — Container datatypes](https://docs.python.org/3/library/collections.html)
- [deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)
