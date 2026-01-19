---
draft: true
title: "[Python Cheatsheet] 40. urllib.parse - URL 파싱과 조립"
slug: "urllib-parse-url-urlparse-urlunparse-urljoin-urlencode-quote-unquote"
description: "파이썬 urllib.parse 모듈을 빠르게 사용하기 위한 치트시트입니다. URL 파싱, 쿼리 문자열 처리, URL 인코딩/디코딩, URL 조립 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 40
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - urllib
  - url
  - URL
  - parse
  - 파싱
  - urlparse
  - urlunparse
  - urljoin
  - urlencode
  - quote
  - unquote
  - query-string
  - 쿼리스트링
  - encoding
  - 인코딩
  - decoding
  - 디코딩
  - percent-encoding
  - 퍼센트인코딩
  - web
  - 웹
  - http
  - api
  - requests
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - security
  - 보안
  - scheme
  - netloc
  - path
  - params
  - fragment
---
`urllib.parse`는 **URL을 파싱하고 조립**하는 표준 라이브러리입니다. 쿼리 문자열 처리, URL 인코딩, 상대/절대 URL 변환 등 웹 프로그래밍에 필수적입니다.

## 언제 이 치트시트를 보나?

- URL에서 **특정 부분(호스트, 경로, 쿼리)을 추출**할 때
- **쿼리 파라미터를 딕셔너리로 변환**하거나 그 반대가 필요할 때
- URL에 **특수문자를 인코딩**해야 할 때

## 핵심 함수

```python
from urllib.parse import (
    urlparse,      # URL → 컴포넌트 분해
    urlunparse,    # 컴포넌트 → URL 조립
    urljoin,       # 상대 URL 결합
    urlencode,     # 딕셔너리 → 쿼리 문자열
    parse_qs,      # 쿼리 문자열 → 딕셔너리 (리스트값)
    parse_qsl,     # 쿼리 문자열 → 튜플 리스트
    quote,         # URL 인코딩
    unquote,       # URL 디코딩
)
```

## 최소 예제

### 1. URL 파싱 (urlparse)

```python
from urllib.parse import urlparse

url = "https://user:pass@example.com:8080/path/to/page?name=alice&age=30#section"
result = urlparse(url)

print(result.scheme)    # https
print(result.netloc)    # user:pass@example.com:8080
print(result.hostname)  # example.com
print(result.port)      # 8080
print(result.path)      # /path/to/page
print(result.query)     # name=alice&age=30
print(result.fragment)  # section
print(result.username)  # user
print(result.password)  # pass
```

### 2. 쿼리 문자열 파싱

```python
from urllib.parse import parse_qs, parse_qsl

query = "name=alice&tags=python&tags=web&age=30"

# 딕셔너리로 (값이 리스트)
params = parse_qs(query)
print(params)
# {'name': ['alice'], 'tags': ['python', 'web'], 'age': ['30']}

# 튜플 리스트로
params_list = parse_qsl(query)
print(params_list)
# [('name', 'alice'), ('tags', 'python'), ('tags', 'web'), ('age', '30')]
```

### 3. 쿼리 문자열 생성 (urlencode)

```python
from urllib.parse import urlencode

params = {'name': 'alice', 'city': 'seoul', 'tag': ['python', 'web']}

# 기본
query = urlencode(params)
print(query)  # name=alice&city=seoul&tag=%5B%27python%27%2C+%27web%27%5D

# 리스트 값 처리
query = urlencode(params, doseq=True)
print(query)  # name=alice&city=seoul&tag=python&tag=web
```

### 4. URL 인코딩/디코딩

```python
from urllib.parse import quote, unquote, quote_plus, unquote_plus

# 공백 → %20
text = "hello world 안녕"
encoded = quote(text)
print(encoded)  # hello%20world%20%EC%95%88%EB%85%95

# 디코딩
decoded = unquote(encoded)
print(decoded)  # hello world 안녕

# 공백 → + (form 인코딩)
encoded_plus = quote_plus(text)
print(encoded_plus)  # hello+world+%EC%95%88%EB%85%95

decoded_plus = unquote_plus(encoded_plus)
print(decoded_plus)  # hello world 안녕
```

### 5. URL 조립 (urlunparse)

```python
from urllib.parse import urlunparse, ParseResult

# 튜플로
components = ('https', 'example.com', '/path', '', 'query=1', 'frag')
url = urlunparse(components)
print(url)  # https://example.com/path?query=1#frag

# ParseResult 수정
from urllib.parse import urlparse

original = urlparse("https://example.com/old?a=1")
# _replace로 특정 부분만 변경
modified = original._replace(path='/new', query='b=2')
new_url = urlunparse(modified)
print(new_url)  # https://example.com/new?b=2
```

### 6. 상대 URL 결합 (urljoin)

```python
from urllib.parse import urljoin

base = "https://example.com/path/page.html"

# 상대 경로
print(urljoin(base, "other.html"))
# https://example.com/path/other.html

print(urljoin(base, "../images/logo.png"))
# https://example.com/images/logo.png

# 루트 상대
print(urljoin(base, "/absolute/path"))
# https://example.com/absolute/path

# 절대 URL은 그대로
print(urljoin(base, "https://other.com/page"))
# https://other.com/page
```

### 7. URL에 쿼리 파라미터 추가

```python
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs

def add_query_params(url, params):
    """URL에 쿼리 파라미터 추가"""
    parsed = urlparse(url)
    
    # 기존 쿼리 파싱
    existing = parse_qs(parsed.query)
    
    # 새 파라미터 병합
    existing.update({k: [v] if not isinstance(v, list) else v 
                     for k, v in params.items()})
    
    # 쿼리 문자열 재생성
    new_query = urlencode(existing, doseq=True)
    
    # URL 재조립
    return urlunparse(parsed._replace(query=new_query))

url = "https://example.com/search?q=python"
new_url = add_query_params(url, {'page': '2', 'sort': 'date'})
print(new_url)
# https://example.com/search?q=python&page=2&sort=date
```

### 8. 안전 문자 지정

```python
from urllib.parse import quote

path = "/path/to/file with spaces"

# 기본: / 는 인코딩되지 않음
print(quote(path))
# /path/to/file%20with%20spaces

# safe 지정: 인코딩하지 않을 문자
print(quote(path, safe=''))
# %2Fpath%2Fto%2Ffile%20with%20spaces

# 추가 안전 문자
print(quote("a=b&c=d", safe='=&'))
# a=b&c=d
```

### 9. URL 유효성 검사 패턴

```python
from urllib.parse import urlparse

def is_valid_url(url):
    """기본적인 URL 유효성 검사"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

print(is_valid_url("https://example.com"))  # True
print(is_valid_url("not-a-url"))            # False
print(is_valid_url("//example.com"))        # False (scheme 없음)
```

### 10. 호스트명만 추출

```python
from urllib.parse import urlparse

urls = [
    "https://www.example.com/path",
    "http://subdomain.example.co.kr:8080/",
    "ftp://files.example.com"
]

for url in urls:
    print(urlparse(url).hostname)
# www.example.com
# subdomain.example.co.kr
# files.example.com
```

## URL 컴포넌트 구조

```
  https://user:pass@example.com:8080/path/to/page?name=alice#section
  \___/   \__/ \__/ \_________/ \__/\__________/ \_________/ \_____/
    |      |    |       |        |       |            |         |
  scheme  user pass   host     port    path        query    fragment
          \________/
             userinfo
          \__________________/
                netloc
```

## 자주 하는 실수

### 1. parse_qs 값이 리스트

```python
from urllib.parse import parse_qs

params = parse_qs("name=alice")
# 잘못: params['name']은 문자열이 아님
# print(params['name'].upper())  # AttributeError

# 올바름: 리스트에서 첫 번째 값
print(params['name'][0].upper())  # ALICE

# 또는 parse_qsl 사용
from urllib.parse import parse_qsl
params_list = dict(parse_qsl("name=alice"))
print(params_list['name'].upper())  # ALICE
```

### 2. 인코딩 중복

```python
from urllib.parse import quote

# 이미 인코딩된 문자열을 다시 인코딩
encoded = "hello%20world"
double_encoded = quote(encoded)
print(double_encoded)  # hello%2520world (잘못!)

# quote의 safe에 %를 추가하거나, 먼저 디코딩
```

## 한눈에 정리

| 작업 | 함수 |
|------|------|
| URL → 컴포넌트 | `urlparse(url)` |
| 컴포넌트 → URL | `urlunparse(tuple)` |
| 쿼리 → 딕셔너리 | `parse_qs(query)` |
| 딕셔너리 → 쿼리 | `urlencode(dict)` |
| 상대 URL 결합 | `urljoin(base, url)` |
| URL 인코딩 | `quote(string)` |
| URL 디코딩 | `unquote(string)` |

## 참고

- [urllib.parse - Python Docs](https://docs.python.org/3/library/urllib.parse.html)
- [RFC 3986 - URI Syntax](https://tools.ietf.org/html/rfc3986)
