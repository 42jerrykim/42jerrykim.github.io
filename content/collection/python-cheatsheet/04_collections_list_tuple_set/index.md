---

image: "wordcloud.png"
title: "[Python Cheatsheet] 04. Collections - list/tuple/set 패턴"
slug: "fast-list-tuple-set-guide-patterns-collection-copy-sort-unpack"
description: "list/tuple/set을 빠르게 선택하고 다루기 위한 치트시트입니다. 정렬·복사·언패킹, set 연산(교집합/합집합), 멤버십 성능 감각, 얕은 복사 함정까지 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 4
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
  - 자료구조
  - list
  - 리스트
  - tuple
  - 튜플
  - set
  - 세트
  - sequence
  - 시퀀스
  - iteration
  - 반복
  - membership
  - 포함검사
  - sorting
  - 정렬
  - sorted
  - sort
  - copy
  - 복사
  - shallow-copy
  - 얕은복사
  - deep-copy
  - 깊은복사
  - unpacking
  - 언패킹
  - destructuring
  - zip
  - enumerate
  - comprehension
  - 컴프리헨션
  - performance
  - 성능
  - big-o
  - 시간복잡도
  - hashing
  - 해시
  - deduplication
  - 중복제거
  - immutability
  - 불변성
  - mutability
  - 가변성
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
파이썬의 핵심 컬렉션 타입인 list, tuple, set을 언제/어떻게 선택하고, 정렬/중복제거/멤버십 검사에서 성능 감각을 잡는 치트시트입니다.

## 언제 이 치트시트를 보나?

- “이걸 list로 해야 하나 set으로 해야 하나”처럼 **자료구조 선택**이 필요할 때
- 정렬/중복제거/멤버십 검사 성능 때문에 고민될 때

## 핵심 패턴

- `list`: 순서 O, 중복 O, append 빠름, 멤버십(`x in list`)은 느릴 수 있음
- `tuple`: 불변(immutable) 시퀀스, “값 묶음” 표현에 적합
- `set`: 중복 제거 + 빠른 멤버십 검사(해시 기반), 순서 개념은 목적 아님

## 최소 예제

```python
# 중복 제거: list -> set -> list (순서 보존이 필요하면 dict 활용)
items = [3, 1, 3, 2, 1]
print(set(items))  # {1, 2, 3}

# 순서 보존 중복 제거 (Py3.7+ dict preserves insertion order)
dedup = list(dict.fromkeys(items))
print(dedup)       # [3, 1, 2]
```

```python
# set 연산
a = {1, 2, 3}
b = {3, 4}
print(a | b)  # 합집합 {1, 2, 3, 4}
print(a & b)  # 교집합 {3}
print(a - b)  # 차집합 {1, 2}
```

```python
# 정렬: 원본 변경 vs 새 리스트
nums = [3, 1, 2]
print(sorted(nums))  # [1, 2, 3] (새 리스트)
nums.sort()
print(nums)          # [1, 2, 3] (원본 변경)
```

```python
# 언패킹
pair = (10, 20)
x, y = pair
print(x, y)  # 10 20

head, *mid, tail = [1, 2, 3, 4, 5]
print(head, mid, tail)  # 1 [2, 3, 4] 5
```

## 자주 하는 실수/주의점

- `set`은 “정렬된 컬렉션”이 아님 → 출력 순서에 의존하지 말기
- 리스트 안에 리스트가 있으면 `copy()`/슬라이싱은 **얕은 복사**라 내부 객체는 공유됨
- `sorted()`는 새 리스트를 반환, `list.sort()`는 `None`을 반환(원본 변경)
- 멤버십이 잦으면 `list` 대신 `set`/`dict`를 고려(해시 기반)

## 관련 링크(공식 문서)

- [Built-in Types — list, tuple, set](https://docs.python.org/3/library/stdtypes.html)
- [Data Structures (Tutorial)](https://docs.python.org/3/tutorial/datastructures.html)

