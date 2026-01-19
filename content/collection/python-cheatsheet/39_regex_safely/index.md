---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 39. Regex - 안전하게 쓰는 최소 패턴"
slug: "regex-safely-minimal-pattern-usage-tips-seo"
description: "정규표현식을 안전하게 쓰기 위한 치트시트입니다. re.search/match/findall/sub, 그룹/이름그룹, greedy vs non-greedy, flags, raw string, 과도한 백트래킹 회피 등 실무 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 39
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - regex
  - regexp
  - 정규표현식
  - re
  - pattern
  - patterns
  - search
  - match
  - findall
  - sub
  - split
  - groups
  - group
  - named-groups
  - capture
  - non-capturing
  - greedy
  - non-greedy
  - quantifiers
  - flags
  - IGNORECASE
  - MULTILINE
  - DOTALL
  - raw-string
  - r-string
  - text-processing
  - 텍스트처리
  - validation
  - 검증
  - parsing
  - 파싱
  - performance
  - 성능
  - catastrophic-backtracking
  - backtracking
  - security
  - 보안
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - strings
  - 문자열
  - debugging
  - 디버깅
---
정규표현식은 강력하지만 남용하면 가독성과 성능을 해칩니다. 이 치트시트는 re 모듈의 핵심 함수, 그룹/플래그, greedy vs non-greedy, 그리고 "언제 쓰지 말아야 하는지"를 정리합니다.

## 언제 이 치트시트를 보나?

- 문자열 메서드로는 어렵고, “패턴 추출/검증”이 필요할 때
- 성능/가독성 때문에 정규식 사용을 최소화하고 싶을 때

## 핵심 패턴

- 가능하면 `startswith/endswith/split` 같은 문자열 메서드를 먼저 고려
- raw string: `r"\d+"` (백슬래시 이스케이프 혼란 방지)
- 위치 1개 찾기: `search()`, 전체 찾기: `findall()`/`finditer()`
- greedy(`.*`)는 과하게 먹을 수 있음 → 필요하면 non-greedy(`.*?`)

## 최소 예제

```python
import re

m = re.search(r"(\d+)", "id=123")
print(m.group(1))  # 123
```

```python
# 이름 그룹
import re

m = re.search(r"(?P<user>[a-z]+)@(?P<domain>[\w.]+)", "a@ex.com")
print(m.groupdict())
```

```python
# greedy vs non-greedy
import re

text = "<tag>hello</tag><tag>world</tag>"
print(re.findall(r"<tag>.*</tag>", text))    # greedy: 하나로 뭉칠 수 있음
print(re.findall(r"<tag>.*?</tag>", text))   # non-greedy: 개별 매칭
```

## 자주 하는 실수/주의점

- `match()`는 문자열 시작부터, `search()`는 어디서든 찾음(의도 확인)
- 정규식이 길어지면 유지보수가 급락 → 작은 패턴으로 분해하거나 파서/문자열 처리로 대체
- 잘못된 패턴은 “과도한 백트래킹”으로 느려질 수 있음 → 단순한 패턴/앵커(`^`, `$`) 활용

## 관련 링크(공식 문서)

- [re — Regular expression operations](https://docs.python.org/3/library/re.html)

