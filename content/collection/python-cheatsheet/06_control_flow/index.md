---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 06. Control Flow - if/for/while 패턴"
slug: "master-if-for-while-control-flow-examples-best-guide"
description: "if/for/while 제어 흐름을 빠르게 쓰기 위한 치트시트입니다. truthy/falsy, enumerate/zip, loop-else, break/continue, match-case(선택)까지 실무에서 자주 쓰는 패턴과 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 6
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - control-flow
  - 제어흐름
  - if
  - 조건문
  - for
  - while
  - 반복문
  - loops
  - loop-else
  - break
  - continue
  - pass
  - enumerate
  - zip
  - range
  - iteration
  - 반복
  - truthiness
  - truthy
  - falsy
  - 비교
  - comparison
  - operators
  - 연산자
  - membership
  - 포함검사
  - in-operator
  - any
  - all
  - builtins
  - 내장함수
  - match
  - match-case
  - python310
  - readability
  - 가독성
  - performance
  - 성능
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - error-handling
  - 예외처리
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - debugging
  - 디버깅
  - style
  - clean-code
  - 클린코드
  - refactoring
  - 리팩토링
  - guard-clause
  - early-return
---
if/for/while 제어 흐름은 모든 프로그램의 뼈대입니다. 이 치트시트는 truthy/falsy, enumerate/zip, loop-else, guard clause 등 깔끔한 제어 흐름 패턴을 빠르게 훑습니다.

## 언제 이 치트시트를 보나?

- 조건/반복을 깔끔하게 쓰고 싶을 때(가독성)
- 인덱스가 필요한 반복, 두 리스트 동시 반복이 필요할 때

## 핵심 패턴

- truthy/falsy: `if items:` / `if not items:`로 비었는지 판단
- 인덱스 포함 반복: `enumerate(iterable, start=0)`
- 병렬 반복: `zip(a, b)` (길이 다른 경우 정책 확인)
- `for ... else`: **break 없이 끝났을 때** else 실행
- guard clause: 중첩 `if`를 줄이고 빠르게 return/continue

## 최소 예제

```python
# truthy/falsy
items = []
if not items:
    print("empty")
```

```python
# enumerate
names = ["a", "b", "c"]
for i, name in enumerate(names, start=1):
    print(i, name)
```

```python
# zip
a = [1, 2, 3]
b = ["x", "y", "z"]
for n, s in zip(a, b):
    print(n, s)
```

```python
# loop-else: break가 없으면 else 실행
nums = [2, 4, 6, 7]
for n in nums:
    if n % 2 == 1:
        print("found odd", n)
        break
else:
    print("all even")
```

```python
# guard clause (early continue)
for n in [1, -2, 3]:
    if n <= 0:
        continue
    print("process", n)
```

## 자주 하는 실수/주의점

- `if len(x) > 0:` 대신 `if x:`가 더 파이썬스럽고 안전한 경우가 많음
- `zip()`은 **짧은 쪽 길이**에 맞춰 끊김 → 길이 불일치가 버그면 사전에 검증
- `for ... else`의 else는 “조건이 거짓이면”이 아니라 **break가 없으면** 실행

## 관련 링크(공식 문서)

- [More Control Flow Tools (Tutorial)](https://docs.python.org/3/tutorial/controlflow.html)
- [Built-in Functions — enumerate, zip, any, all](https://docs.python.org/3/library/functions.html)

