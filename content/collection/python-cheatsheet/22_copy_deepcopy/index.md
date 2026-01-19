---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 22. copy - 얕은 복사/깊은 복사 패턴"
slug: "object-copy-deepcopy-shallow-guide-reference-clone-tips"
description: "파이썬 객체 복사를 정확히 이해하기 위한 치트시트입니다. 할당 vs 얕은 복사 vs 깊은 복사의 차이, copy.copy()/copy.deepcopy(), 가변 객체 함정과 커스텀 복사 구현을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 22
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - copy
  - deepcopy
  - shallow-copy
  - 얕은복사
  - deep-copy
  - 깊은복사
  - clone
  - 복제
  - mutable
  - 가변객체
  - immutable
  - 불변객체
  - reference
  - 참조
  - assignment
  - 할당
  - list
  - dict
  - nested
  - 중첩
  - object
  - 객체
  - memory
  - 메모리
  - pitfalls
  - 함정
  - side-effect
  - 부작용
  - bug
  - 버그
  - debugging
  - 디버깅
  - best-practices
  - 베스트프랙티스
  - standard-library
  - 표준라이브러리
  - __copy__
  - __deepcopy__
  - custom
  - 커스텀
---
파이썬에서 객체 복사는 의도치 않은 버그의 원인이 됩니다. 이 치트시트는 할당, 얕은 복사, 깊은 복사의 차이와 copy 모듈 사용법을 정리합니다.

## 언제 이 치트시트를 보나?

- 리스트/딕셔너리를 복사했는데 **원본도 변경**되는 버그가 발생할 때
- 중첩된 객체를 **완전히 독립적**으로 복제하고 싶을 때

## 핵심 패턴

- **할당 (`=`)**: 같은 객체를 가리킴 (복사 아님)
- **얕은 복사 (`copy.copy()`)**: 새 객체 생성, 내부 요소는 원본과 공유
- **깊은 복사 (`copy.deepcopy()`)**: 새 객체 생성, 내부 요소도 모두 재귀적으로 복사
- 리스트/딕셔너리: `list()`, `dict()`, 슬라이싱 `[:]`도 얕은 복사

## 시각적 비교

```
할당 (Assignment)         얕은 복사 (Shallow)        깊은 복사 (Deep)
─────────────────        ─────────────────         ─────────────────
a = [[1,2], [3,4]]       b = copy.copy(a)          c = copy.deepcopy(a)

a ──┐                    a ──> [ref1, ref2]        a ──> [ref1, ref2]
    │                           │      │                 │      │
    ▼                           ▼      ▼                 ▼      ▼
[[1,2], [3,4]]           b ──> [ref1, ref2]        c ──> [[1,2], [3,4]]
    ▲                           (같은 내부 객체)          (새로운 내부 객체)
    │
b ──┘ (같은 객체)
```

## 최소 예제

```python
import copy

# 원본 리스트 (중첩)
original = [[1, 2], [3, 4]]

# 할당 - 같은 객체
assigned = original
assigned[0][0] = 99
print(original)  # [[99, 2], [3, 4]] - 원본도 변경됨!

# 얕은 복사 - 새 리스트, 내부 객체는 공유
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] - 내부 객체는 공유되므로 원본도 변경!

shallow.append([5, 6])
print(original)  # [[99, 2], [3, 4]] - 최상위 리스트는 독립

# 깊은 복사 - 완전히 독립
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original)  # [[1, 2], [3, 4]] - 원본 유지!
```

## 다양한 얕은 복사 방법

```python
# 리스트
original = [1, 2, 3]

copy1 = list(original)      # list() 생성자
copy2 = original[:]         # 슬라이싱
copy3 = original.copy()     # .copy() 메서드
copy4 = copy.copy(original) # copy 모듈

# 딕셔너리
original_dict = {"a": 1, "b": 2}

copy1 = dict(original_dict)      # dict() 생성자
copy2 = original_dict.copy()     # .copy() 메서드
copy3 = {**original_dict}        # 언패킹
copy4 = copy.copy(original_dict) # copy 모듈

# 세트
original_set = {1, 2, 3}

copy1 = set(original_set)
copy2 = original_set.copy()
```

## 중첩 구조에서의 차이

```python
import copy

# 중첩 딕셔너리
data = {
    "users": [
        {"name": "Alice", "scores": [90, 85]},
        {"name": "Bob", "scores": [80, 75]},
    ]
}

# 얕은 복사
shallow = copy.copy(data)
shallow["users"][0]["name"] = "Changed"
print(data["users"][0]["name"])  # "Changed" - 원본 변경됨!

# 깊은 복사
data = {
    "users": [
        {"name": "Alice", "scores": [90, 85]},
        {"name": "Bob", "scores": [80, 75]},
    ]
}
deep = copy.deepcopy(data)
deep["users"][0]["name"] = "Changed"
print(data["users"][0]["name"])  # "Alice" - 원본 유지
```

## 커스텀 클래스 복사

```python
import copy

class MyClass:
    def __init__(self, data: list):
        self.data = data
    
    # 얕은 복사 커스터마이징 (선택)
    def __copy__(self):
        new = MyClass(self.data.copy())
        return new
    
    # 깊은 복사 커스터마이징 (선택)
    def __deepcopy__(self, memo):
        new = MyClass(copy.deepcopy(self.data, memo))
        return new

obj = MyClass([1, 2, [3, 4]])
shallow = copy.copy(obj)
deep = copy.deepcopy(obj)
```

## 자주 하는 실수/주의점

- **불변 객체는 복사 불필요**: `int`, `str`, `tuple`(내부가 불변일 때)은 복사해도 같은 객체
  ```python
  a = (1, 2, 3)
  b = copy.copy(a)
  print(a is b)  # True (최적화로 같은 객체 반환)
  ```
- **기본 인자 함정**: 함수 기본 인자로 가변 객체 사용 시 복사 필요
  ```python
  # BAD
  def add_item(item, lst=[]):
      lst.append(item)
      return lst
  
  # GOOD
  def add_item(item, lst=None):
      if lst is None:
          lst = []
      lst.append(item)
      return lst
  ```
- **순환 참조**: `deepcopy`는 순환 참조도 처리함 (memo 딕셔너리 사용)
- **성능**: `deepcopy`는 큰 객체에서 비용이 클 수 있음 → 필요한 경우만 사용
- **복사 불가 객체**: 파일 핸들, 소켓, 락 등은 복사 불가

## 언제 어떤 복사를 쓸까?

| 상황 | 권장 방법 |
|------|-----------|
| 단순 1차원 리스트/딕셔너리 | 얕은 복사 (`.copy()`, 슬라이싱) |
| 중첩 구조를 완전히 분리 | `copy.deepcopy()` |
| 불변 객체 (str, tuple, frozenset) | 복사 불필요 |
| 클래스 인스턴스 (복잡한 내부 상태) | `copy.deepcopy()` 또는 커스텀 |

## 관련 링크(공식 문서)

- [copy — Shallow and deep copy operations](https://docs.python.org/3/library/copy.html)
- [Mutable vs Immutable Objects](https://docs.python.org/3/glossary.html#term-mutable)
