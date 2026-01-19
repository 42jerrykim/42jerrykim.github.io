---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 20. dataclasses - default_factory/frozen 패턴"
slug: "immutable-object-dataclasses-default-factory-frozen-best-patterns"
description: "dataclasses를 빠르게 적용하기 위한 치트시트입니다. @dataclass 기본, field(default_factory), frozen/slots, 비교/정렬 옵션, 불변 객체로 모델링하는 패턴과 mutable default 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 20
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - dataclasses
  - dataclass
  - 데이터클래스
  - model
  - models
  - 모델
  - immutability
  - 불변성
  - frozen
  - slots
  - field
  - default_factory
  - defaults
  - mutable-default
  - 함정
  - pitfalls
  - equality
  - 비교
  - ordering
  - 정렬
  - repr
  - typing
  - 타입힌트
  - maintainability
  - 유지보수
  - readability
  - 가독성
  - performance
  - 성능
  - standard-library
  - 표준라이브러리
  - serialization
  - 직렬화
  - asdict
  - astuple
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
dataclass는 데이터 컨테이너 클래스를 보일러플레이트 없이 만드는 표준 방법입니다. 이 치트시트는 field(default_factory), frozen, slots 옵션과 흔한 함정을 정리합니다.

## 언제 이 치트시트를 보나?

- “데이터 담는 클래스”를 보일러플레이트 없이 만들고 싶을 때
- 기본값/불변성/비교 동작을 명확히 하고 싶을 때

## 핵심 패턴

- 가변 기본값은 `default_factory`로
- 불변 모델이 필요하면 `frozen=True`
- 메모리/속성 오타 방지 목적이면 `slots=True`(버전/환경 고려)

## 최소 예제

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    tags: list[str] = field(default_factory=list)
```

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

## 자주 하는 실수/주의점

- `tags: list[str] = []` 같은 기본값은 공유됨 → `field(default_factory=list)`
- `frozen=True`면 내부 가변 객체까지 자동으로 불변이 되진 않음(참조는 막지만 내부 변경은 가능할 수 있음)
- 직렬화가 필요하면 `asdict()`/`astuple()`를 고려(중첩 구조는 재귀 변환됨)

## 관련 링크(공식 문서)

- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html)

