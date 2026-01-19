---

image: "wordcloud.png"
title: "[Python Cheatsheet] 28. itertools & functools - 자주 쓰는 조합"
slug: "efficient-iteration-caching-itertools-functools-productivity-guide"
description: "itertools/functools를 실전에서 바로 쓰기 위한 치트시트입니다. chain/islice/groupby/product, lru_cache/partial/reduce 등 자주 쓰는 조합과 groupby 함정, 캐시 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 28
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - itertools
  - functools
  - standard-library
  - 표준라이브러리
  - iterator
  - iterable
  - 이터레이터
  - 이터러블
  - chain
  - islice
  - groupby
  - product
  - permutations
  - combinations
  - accumulate
  - lru_cache
  - cache
  - memoization
  - 메모이제이션
  - partial
  - reduce
  - performance
  - 성능
  - memory
  - 메모리
  - streaming
  - 스트리밍
  - lazy-evaluation
  - 지연평가
  - pitfalls
  - 함정
  - best-practices
  - 베스트프랙티스
  - patterns
  - 패턴
  - functional-programming
  - 함수형
  - map
  - filter
  - lambda
  - debugging
  - 디버깅
  - testing
  - 테스트
---
itertools와 functools는 함수형 스타일의 데이터 처리와 성능 최적화를 돕는 표준 라이브러리입니다. 이 치트시트는 chain, islice, groupby, lru_cache 등 자주 쓰는 조합과 함정을 정리합니다.

## 언제 이 치트시트를 보나?

- 반복/조합/슬라이싱 로직을 “for-loop 없이” 깔끔하게 만들고 싶을 때
- 캐시로 성능을 끌어올리고 싶을 때

## 핵심 패턴

- `itertools.chain(a, b)`로 시퀀스 이어붙이기
- 큰 이터러블은 `islice`로 일부만 소비
- `groupby`는 **연속된 키**만 묶음 → 보통 정렬이 먼저 필요
- `lru_cache`는 “순수 함수 + 입력이 해시 가능”일 때 가장 안전함

## 최소 예제

```python
from itertools import chain, islice

xs = chain([1, 2], [3, 4])
print(list(xs))

print(list(islice(range(100), 5)))  # [0, 1, 2, 3, 4]
```

```python
from itertools import groupby

data = ["a", "a", "b", "b", "b", "a"]
for k, g in groupby(data):
    print(k, list(g))  # 연속 구간 기준
```

```python
from functools import lru_cache, partial

@lru_cache(maxsize=1024)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

pow2 = partial(pow, 2)
print(pow2(10))  # 1024
```

## 자주 하는 실수/주의점

- `groupby`는 정렬된 입력이 아니면 “원하는 그룹”이 안 나올 수 있음 → 필요하면 정렬 후 사용
- `lru_cache`는 인자에 list/dict 같은 **해시 불가 타입**이 오면 에러
- 캐시는 메모리를 사용함 → maxsize/수명 정책 고려

## 관련 링크(공식 문서)

- [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html)
- [functools — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html)

