---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 65. HTTP Requests - urllib/requests 기본"
slug: "http-requests-guide-urllib-requests-api-rest-get-post-tutorial"
description: "HTTP 요청을 빠르게 보내기 위한 치트시트입니다. requests 라이브러리의 GET/POST/JSON, 세션 재사용, 타임아웃/재시도, 에러 핸들링, urllib 표준 라이브러리 기본을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 65
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - http
  - requests
  - urllib
  - GET
  - POST
  - PUT
  - DELETE
  - REST
  - API
  - json
  - headers
  - cookies
  - session
  - 세션
  - timeout
  - 타임아웃
  - retry
  - 재시도
  - error-handling
  - 에러처리
  - status-code
  - 상태코드
  - authentication
  - 인증
  - ssl
  - https
  - proxy
  - 프록시
  - download
  - upload
  - streaming
  - 스트리밍
  - networking
  - 네트워킹
  - web
  - 웹
  - scraping
  - 크롤링
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - performance
  - 성능
  - standard-library
  - 표준라이브러리
  - third-party
  - 서드파티
---
HTTP 요청은 API 연동과 웹 데이터 수집의 기본입니다. 이 치트시트는 requests 라이브러리의 핵심 패턴(GET/POST/JSON), 세션, 타임아웃, 에러 핸들링과 urllib 표준 라이브러리 기본을 정리합니다.

## 언제 이 치트시트를 보나?

- REST API를 호출하거나 웹 페이지를 가져올 때
- 타임아웃/재시도/에러 처리 패턴이 필요할 때

## 핵심 패턴

- **requests 설치**: `pip install requests`
- GET: `requests.get(url, params=..., timeout=...)`
- POST JSON: `requests.post(url, json=data, timeout=...)`
- 상태 확인: `response.raise_for_status()` 또는 `response.status_code`
- 세션 재사용: `requests.Session()`으로 연결 풀링 + 쿠키 유지

## 최소 예제 (requests)

```python
import requests

# GET 요청
response = requests.get(
    "https://httpbin.org/get",
    params={"key": "value"},
    timeout=10,
)
response.raise_for_status()  # 4xx/5xx면 예외
print(response.json())
```

```python
# POST JSON
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Alice", "age": 30},
    timeout=10,
)
print(response.status_code)
print(response.json())
```

```python
# 세션 재사용 (연결 풀링 + 쿠키 유지)
with requests.Session() as session:
    session.headers.update({"Authorization": "Bearer TOKEN"})
    
    r1 = session.get("https://httpbin.org/cookies/set/foo/bar")
    r2 = session.get("https://httpbin.org/cookies")
    print(r2.json())
```

```python
# 에러 핸들링
try:
    response = requests.get("https://httpbin.org/status/500", timeout=5)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## urllib (표준 라이브러리)

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

# GET
with urlopen("https://httpbin.org/get", timeout=10) as response:
    data = json.loads(response.read().decode())
    print(data)

# POST (표준 라이브러리만 사용 시)
req = Request(
    "https://httpbin.org/post",
    data=json.dumps({"key": "value"}).encode(),
    headers={"Content-Type": "application/json"},
)
with urlopen(req, timeout=10) as response:
    print(response.read().decode())
```

## 자주 하는 실수/주의점

- **timeout 필수**: 없으면 무한 대기 가능 → 항상 `timeout=` 지정
- `response.json()`은 Content-Type이 JSON이 아니면 에러 → 먼저 확인하거나 try/except
- `raise_for_status()` 호출 안 하면 4xx/5xx도 정상 응답처럼 처리됨
- 대량 요청 시 **세션 재사용**으로 TCP 연결 오버헤드 줄이기
- 민감한 데이터(토큰 등)는 URL 파라미터 대신 **헤더**에 담기

## 관련 링크(공식 문서)

- [requests (PyPI)](https://requests.readthedocs.io/)
- [urllib.request](https://docs.python.org/3/library/urllib.request.html)
