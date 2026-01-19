---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 03. Strings - 슬라이싱/포맷팅/검색/치환"
slug: "string-slicing-format-find-replace-text-guide-fast"
description: "파이썬 문자열을 빠르게 다루기 위한 치트시트입니다. 슬라이싱, split/join, strip/replace, 검색(find/index), f-string 포맷팅, bytes/encoding 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 3
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - string
  - strings
  - 문자열
  - slicing
  - 슬라이싱
  - indexing
  - 인덱싱
  - split
  - join
  - strip
  - replace
  - find
  - index
  - startswith
  - endswith
  - formatting
  - 포맷팅
  - f-string
  - fstring
  - format
  - repr
  - print
  - output
  - 출력
  - unicode
  - 유니코드
  - encoding
  - 인코딩
  - decoding
  - 디코딩
  - bytes
  - bytearray
  - text-processing
  - 텍스트처리
  - performance
  - 성능
  - readability
  - 가독성
  - immutability
  - 불변성
  - iteration
  - 반복
  - loops
  - 반복문
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
문자열(str)은 파이썬에서 가장 자주 다루는 타입입니다. 이 치트시트는 슬라이싱, split/join, 검색/치환, f-string 포맷팅, bytes 변환의 핵심 패턴과 흔한 실수를 빠르게 훑습니다.

## 언제 이 치트시트를 보나?

- 텍스트를 **자르고/붙이고/찾고/치환**해야 할 때
- 출력/로그에서 **가독성 좋은 포맷**이 필요할 때
- `str` vs `bytes` 때문에 에러가 날 때

## 핵심 패턴

- 슬라이싱: `s[a:b:c]` (끝 인덱스는 **미포함**)
- 검색: 존재 여부는 `in`, 위치는 `find()`(없으면 -1) / `index()`(없으면 예외)
- 조립: 반복문에서 `+` 대신 `''.join(...)`
- 포맷: 기본은 f-string, 디버깅은 `!r`로 `repr` 출력
- 변환: 텍스트 `str` ↔ 바이너리 `bytes`는 `encode()/decode()`

## 최소 예제

```python
# 슬라이싱
s = "abcdef"
print(s[:3])     # abc
print(s[3:])     # def
print(s[::2])    # ace
print(s[::-1])   # fedcba
```

```python
# split / join
line = "a, b, c"
parts = [p.strip() for p in line.split(",")]
print(parts)                 # ['a', 'b', 'c']
print(",".join(parts))       # a,b,c
```

```python
# find vs index
s = "hello world"
print(s.find("world"))       # 6
print(s.find("nope"))        # -1

# s.index("nope")  # ValueError
```

```python
# f-string (디버깅은 !r)
name = "Kim"
count = 3
print(f"{name} x {count}")
print(f"name={name!r}, count={count}")
```

```python
# str vs bytes
text = "안녕"
b = text.encode("utf-8")
print(b)                     # b'...'
print(b.decode("utf-8"))     # 안녕
```

## 자주 하는 실수/주의점

- `s.index(x)`는 없으면 예외 → “없으면 -1”이 필요하면 `find()`
- `split()`은 “공백 여러 개”를 잘 처리하지만, 구분자 지정 시엔 동작이 달라짐
- 반복문에서 `result += piece`는 O(n^2)로 느려질 수 있음 → `list`에 모아 `''.join`
- `str`는 **불변(immutable)** → 수정이 아니라 “새 문자열 생성”임
- `bytes`를 `str`처럼 처리하려고 하면 타입 에러가 남 → 경계에서 명확히 `encode/decode`

## 관련 링크(공식 문서)

- [Text Sequence Type — str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
- [Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax)

