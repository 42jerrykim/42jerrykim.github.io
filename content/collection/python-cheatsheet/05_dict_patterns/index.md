---

image: "wordcloud.png"
title: "[Python Cheatsheet] 05. dict 패턴 - 조회/기본값/카운팅/병합"
slug: "advanced-dictionary-patterns-safe-lookup-merging-counting"
description: "파이썬 dict를 실무에서 빠르게 쓰기 위한 치트시트입니다. 안전한 조회(get), 기본값(setdefault/defaultdict), 카운팅(Counter), 정렬/순회, 병합(|/update) 패턴과 흔한 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 5
tags:
  - Python
  - 파이썬
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - Implementation
  - sorting
  - 정렬
  - Algorithm
  - JSON
  - Performance
  - 성능
  - 시간복잡도
  - Best-Practices
  - pitfalls
  - 함정
  - error-handling
  - Tutorial
  - 튜토리얼
  - 구현
  - Code-Quality
  - 코드품질
  - HTML
  - 에러처리
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Testing
  - 테스트
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Optimization
  - 최적화
  - Logging
  - 로깅
  - Configuration
  - 설정
  - Guide
  - 가이드
  - Deployment
  - 배포
  - Automation
  - 자동화
  - Workflow
  - 워크플로우
  - Troubleshooting
  - 트러블슈팅
---
dict는 파이썬에서 가장 많이 쓰이는 매핑 타입입니다. 이 치트시트는 안전한 조회(get), 기본값 처리(setdefault/defaultdict), 카운팅(Counter), 병합 패턴과 흔한 함정을 빠르게 정리합니다.

## 언제 이 치트시트를 보나?

- key로 빠르게 조회하고 싶을 때(`O(1)` 감)
- 누락 key 처리(기본값/카운팅/중첩 dict)가 자주 필요할 때

## 핵심 패턴

- 안전 조회: `d.get(k, default)`
- 존재 체크: `if k in d: ...`
- 누적/그룹핑: `setdefault()` 또는 `defaultdict(list)`
- 카운팅: `Counter(iterable)`
- 병합: `d3 = d1 | d2` (Py3.9+) / `d1.update(d2)` (원본 변경)

## 최소 예제

```python
# 안전 조회
d = {"a": 1}
print(d.get("a"))        # 1
print(d.get("missing"))  # None
print(d.get("missing", 0))  # 0
```

```python
# setdefault: 중첩/누적
groups = {}
for k, v in [("A", 1), ("A", 2), ("B", 9)]:
    groups.setdefault(k, []).append(v)
print(groups)  # {'A': [1, 2], 'B': [9]}
```

```python
from collections import defaultdict, Counter

# defaultdict: 누적에 더 자연스러움
groups = defaultdict(list)
for k, v in [("A", 1), ("A", 2), ("B", 9)]:
    groups[k].append(v)

# Counter: 카운팅
cnt = Counter("banana")
print(cnt["a"])  # 3
```

```python
# 정렬: key/value 기준
d = {"b": 2, "a": 3, "c": 1}
print(sorted(d.items()))                 # key 기준
print(sorted(d.items(), key=lambda kv: kv[1]))  # value 기준
```

```python
# 병합
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}
print(d1 | d2)   # {'a': 1, 'b': 99, 'c': 3} (새 dict)

d1.update(d2)
print(d1)        # 원본 변경
```

## 자주 하는 실수/주의점

- `d[k]`는 key가 없으면 `KeyError` → “없으면 기본값”이면 `get()`/`setdefault()`/`defaultdict`
- `setdefault()`는 “없는 경우에만” 기본값을 넣음(하지만 기본값 생성 비용이 크면 주의)
- `dict | dict`는 **새 dict**를 만듦, `update()`는 **원본 변경**
- `for k in d:`는 key만 순회 → 값까지 필요하면 `for k, v in d.items():`

## 관련 링크(공식 문서)

- [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [collections — defaultdict, Counter](https://docs.python.org/3/library/collections.html)

