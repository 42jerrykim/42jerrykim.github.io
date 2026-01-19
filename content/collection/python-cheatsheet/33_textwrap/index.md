---

image: "wordcloud.png"
title: "[Python Cheatsheet] 33. textwrap - 텍스트 정렬과 줄바꿈"
slug: "textwrap-formatting-multiline-word-wrap-guide"
description: "파이썬 textwrap 모듈을 빠르게 사용하기 위한 치트시트입니다. wrap, fill, dedent, indent, shorten 함수로 텍스트 포맷팅하는 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 33
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - textwrap
  - text-formatting
  - 텍스트포맷팅
  - wrap
  - fill
  - dedent
  - indent
  - shorten
  - line-wrapping
  - 줄바꿈
  - word-wrap
  - 워드랩
  - text-alignment
  - 텍스트정렬
  - multiline
  - 멀티라인
  - string
  - 문자열
  - formatting
  - 포맷팅
  - cli
  - terminal
  - 터미널
  - docstring
  - 독스트링
  - triple-quote
  - heredoc
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - email
  - 이메일
  - report
  - 리포트
---
`textwrap` 모듈은 **텍스트 줄바꿈과 들여쓰기**를 다루는 도구입니다. CLI 출력, 이메일 본문, 리포트 생성 등에서 텍스트를 깔끔하게 정렬할 때 유용합니다.

## 언제 이 치트시트를 보나?

- 긴 텍스트를 **특정 너비로 줄바꿈**해야 할 때
- 멀티라인 문자열의 **들여쓰기를 제거**하고 싶을 때
- 텍스트를 **일정 길이로 자르고** 말줄임표를 붙일 때

## 핵심 함수

```python
import textwrap

textwrap.wrap(text, width=70)     # 리스트로 분할
textwrap.fill(text, width=70)     # 문자열로 줄바꿈
textwrap.dedent(text)             # 공통 들여쓰기 제거
textwrap.indent(text, prefix)     # 들여쓰기 추가
textwrap.shorten(text, width)     # 길이 제한 + 말줄임
```

## 최소 예제

### 1. wrap - 리스트로 분할

```python
import textwrap

text = "Python is a programming language that lets you work quickly and integrate systems more effectively."

lines = textwrap.wrap(text, width=30)
print(lines)
# ['Python is a programming', 'language that lets you work', 'quickly and integrate systems', 'more effectively.']

for line in lines:
    print(line)
# Python is a programming
# language that lets you work
# quickly and integrate systems
# more effectively.
```

### 2. fill - 줄바꿈된 문자열

```python
import textwrap

text = "Python is a programming language that lets you work quickly and integrate systems more effectively."

formatted = textwrap.fill(text, width=40)
print(formatted)
# Python is a programming language that
# lets you work quickly and integrate
# systems more effectively.
```

### 3. dedent - 들여쓰기 제거

```python
import textwrap

# 함수 내 멀티라인 문자열
def get_help():
    help_text = """\
        Usage: program [options]
        
        Options:
            -h  Show help
            -v  Verbose mode
        """
    return textwrap.dedent(help_text)

print(get_help())
# Usage: program [options]
# 
# Options:
#     -h  Show help
#     -v  Verbose mode
```

### 4. indent - 들여쓰기 추가

```python
import textwrap

text = """First line
Second line
Third line"""

# 모든 줄에 들여쓰기
indented = textwrap.indent(text, '    ')
print(indented)
#     First line
#     Second line
#     Third line

# 조건부 들여쓰기 (비어있지 않은 줄만)
text_with_empty = "Line 1\n\nLine 2"
indented = textwrap.indent(text_with_empty, '> ', predicate=lambda line: line.strip())
print(indented)
# > Line 1
# 
# > Line 2
```

### 5. shorten - 길이 제한

```python
import textwrap

text = "Hello World! This is a very long text that needs to be shortened."

short = textwrap.shorten(text, width=30)
print(short)
# Hello World! This is a [...]

# 커스텀 placeholder
short = textwrap.shorten(text, width=30, placeholder="...")
print(short)
# Hello World! This is a...
```

### 6. TextWrapper 클래스 (세부 설정)

```python
import textwrap

wrapper = textwrap.TextWrapper(
    width=40,
    initial_indent='* ',      # 첫 줄 들여쓰기
    subsequent_indent='  ',    # 이후 줄 들여쓰기
    break_long_words=False,    # 긴 단어 자르지 않음
    break_on_hyphens=True      # 하이픈에서 줄바꿈
)

text = "This is a demonstration of the TextWrapper class with custom settings."
print(wrapper.fill(text))
# * This is a demonstration of
#   the TextWrapper class with
#   custom settings.
```

### 7. 목록 포맷팅

```python
import textwrap

items = [
    "First item with a long description that might wrap",
    "Second item",
    "Third item with another long description"
]

wrapper = textwrap.TextWrapper(
    width=40,
    initial_indent='  - ',
    subsequent_indent='    '
)

for item in items:
    print(wrapper.fill(item))
#   - First item with a long
#     description that might wrap
#   - Second item
#   - Third item with another long
#     description
```

### 8. dedent + fill 조합

```python
import textwrap

def print_help():
    help_text = textwrap.dedent("""\
        This is a help message that explains how to use the program.
        It can span multiple lines and will be properly formatted
        when displayed to the user.
        """)
    print(textwrap.fill(help_text, width=50))

print_help()
# This is a help message that explains how to
# use the program. It can span multiple lines
# and will be properly formatted when displayed
# to the user.
```

### 9. 코드 블록 보존

```python
import textwrap

# wrap은 코드를 망가뜨릴 수 있음
code = "def hello(): print('world')"
print(textwrap.fill(code, width=20))  # 코드가 이상해짐

# 코드는 그대로 두고 설명만 wrap
description = "This function prints a greeting message to the console."
formatted_desc = textwrap.fill(description, width=40)
print(f"{formatted_desc}\n\n{code}")
```

## TextWrapper 주요 옵션

```python
import textwrap

wrapper = textwrap.TextWrapper(
    width=70,                  # 최대 줄 너비
    initial_indent='',         # 첫 줄 접두사
    subsequent_indent='',      # 이후 줄 접두사
    expand_tabs=True,          # 탭을 공백으로
    tabsize=8,                 # 탭 크기
    replace_whitespace=True,   # 공백 정규화
    fix_sentence_endings=False,# 문장 끝 공백 2개
    break_long_words=True,     # 긴 단어 자르기
    break_on_hyphens=True,     # 하이픈에서 줄바꿈
    drop_whitespace=True,      # 줄 시작/끝 공백 제거
    max_lines=None,            # 최대 줄 수
    placeholder=' [...]'       # 생략 시 표시
)
```

## 자주 하는 실수

### 1. dedent가 작동하지 않을 때

```python
import textwrap

# 첫 줄에 텍스트가 있으면 dedent 작동 안 함
bad = """    Line 1
    Line 2"""
print(textwrap.dedent(bad))  # 변화 없음

# 첫 줄을 비우거나 \ 사용
good = """\
    Line 1
    Line 2"""
print(textwrap.dedent(good))
# Line 1
# Line 2
```

### 2. shorten이 너무 짧을 때

```python
import textwrap

# placeholder 길이보다 width가 작으면 에러
# textwrap.shorten("Hello", width=3)  # ValueError

# width는 placeholder보다 커야 함
textwrap.shorten("Hello", width=10, placeholder="...")  # OK
```

## 한눈에 정리

| 함수 | 용도 | 반환 |
|------|------|------|
| `wrap(text, width)` | 줄바꿈 | 리스트 |
| `fill(text, width)` | 줄바꿈 | 문자열 |
| `dedent(text)` | 들여쓰기 제거 | 문자열 |
| `indent(text, prefix)` | 들여쓰기 추가 | 문자열 |
| `shorten(text, width)` | 길이 제한 | 문자열 |

## 참고

- [textwrap - Python Docs](https://docs.python.org/3/library/textwrap.html)
