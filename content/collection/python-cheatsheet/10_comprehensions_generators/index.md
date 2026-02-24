---

image: "wordcloud.png"
title: "[Python Cheatsheet] 10. Comprehensions & Generators"
slug: "efficient-comprehensions-generators-list-dict-set-iterator-guide"
description: "컴프리헨션과 제너레이터를 빠르게 선택하기 위한 치트시트입니다. list/dict/set comprehension, generator expression, yield, next, 메모리 관점에서의 선택 기준과 대표 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 10
tags:
  - Python
  - 파이썬
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - iterator
  - map
  - Implementation
  - Performance
  - 성능
  - memory
  - 메모리
  - Clean-Code
  - Design-Pattern
  - pitfalls
  - 함정
  - Best-Practices
  - debugging
  - 디버깅
  - async
  - 비동기
  - error-handling
---
컴프리헨션과 제너레이터는 파이썬다운 코드를 작성하는 핵심 도구입니다. 이 치트시트는 list/dict/set comprehension과 generator expression의 선택 기준(가독성 vs 메모리)을 빠르게 정리합니다.

## 언제 이 치트시트를 보나?

- “한 줄로 만들까, for-loop로 풀어 쓸까” 고민될 때
- 데이터가 커서 **메모리**가 걱정될 때(지연 평가가 필요할 때)

## 핵심 패턴

- 컴프리헨션: “작은 변환/필터”를 **간결하게**
- 제너레이터: “큰 데이터/스트리밍”을 **메모리 효율적으로**
- 디버깅/가독성이 우선이면 for-loop로 풀어 쓰는 게 더 좋을 때가 많음

## 최소 예제

```python
# list comprehension: 변환
nums = [1, 2, 3]
squares = [n * n for n in nums]
print(squares)
```

```python
# dict comprehension: 매핑 생성
names = ["a", "b", "c"]
idx = {name: i for i, name in enumerate(names)}
print(idx)
```

```python
# generator expression: 지연 평가
nums = range(10_000_000)
total = sum(n * n for n in nums)  # 괄호: generator expression
print(total)
```

```python
# generator function (yield)
def chunks(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]

for c in chunks([1, 2, 3, 4, 5], 2):
    print(c)
```

## 자주 하는 실수/주의점

- 컴프리헨션 안에 조건/삼항/중첩 루프가 과해지면 가독성이 급격히 떨어짐 → for-loop로 분해
- `sum([ ... ])`처럼 불필요한 리스트를 만들지 말고 `sum( ... for ... )`를 고려
- 제너레이터는 “한 번 소비하면 끝”인 경우가 많음(재사용하려면 새로 만들어야 함)

## 관련 링크(공식 문서)

- [Data Structures — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Iterators and Generators (Tutorial)](https://docs.python.org/3/tutorial/classes.html#iterators)

