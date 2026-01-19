---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 32. contextlib 심화 - suppress, redirect, ExitStack"
slug: "contextlib-advanced-suppress-redirect-exitstack-nullcontext-examples"
description: "파이썬 contextlib 모듈 심화 기능 치트시트입니다. suppress로 예외 무시, redirect_stdout/stderr로 출력 리다이렉트, ExitStack으로 동적 컨텍스트 관리, nullcontext 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 32
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - contextlib
  - context-manager
  - 컨텍스트매니저
  - suppress
  - 예외무시
  - redirect_stdout
  - redirect_stderr
  - 출력리다이렉트
  - ExitStack
  - 동적컨텍스트
  - nullcontext
  - closing
  - contextmanager
  - asynccontextmanager
  - with-statement
  - with문
  - resource-management
  - 리소스관리
  - exception-handling
  - 예외처리
  - cleanup
  - 정리
  - nested-context
  - 중첩컨텍스트
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - advanced
  - 고급
---
`contextlib` 모듈은 컨텍스트 매니저 작성을 도와주는 유틸리티를 제공합니다. 이 치트시트는 `@contextmanager` 외의 **심화 기능**인 `suppress`, `redirect_*`, `ExitStack` 등을 다룹니다.

## 언제 이 치트시트를 보나?

- 특정 **예외를 조용히 무시**하고 싶을 때
- **stdout/stderr를 리다이렉트**해야 할 때
- **동적 개수의 컨텍스트 매니저**를 관리할 때

## 핵심 도구

```python
from contextlib import (
    suppress,           # 예외 무시
    redirect_stdout,    # stdout 리다이렉트
    redirect_stderr,    # stderr 리다이렉트
    ExitStack,          # 동적 컨텍스트 스택
    nullcontext,        # 아무것도 안 하는 컨텍스트
    closing,            # close() 자동 호출
    asynccontextmanager # async 컨텍스트 매니저
)
```

## 최소 예제

### 1. suppress - 예외 무시

```python
from contextlib import suppress
import os

# 파일 삭제 시 없어도 무시
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')
# 예외 없이 통과

# 여러 예외 타입
with suppress(FileNotFoundError, PermissionError):
    os.remove('some_file.txt')

# 동등한 코드 (suppress 없이)
try:
    os.remove('nonexistent_file.txt')
except FileNotFoundError:
    pass
```

### 2. redirect_stdout - 출력 캡처

```python
from contextlib import redirect_stdout
from io import StringIO

# 출력을 문자열로 캡처
f = StringIO()
with redirect_stdout(f):
    print("Hello, World!")
    print("This is captured")

output = f.getvalue()
print(f"Captured: {output!r}")
# Captured: 'Hello, World!\nThis is captured\n'
```

### 3. redirect_stderr - 에러 출력 캡처

```python
from contextlib import redirect_stderr
from io import StringIO
import sys

f = StringIO()
with redirect_stderr(f):
    print("Error message", file=sys.stderr)

error_output = f.getvalue()
```

### 4. 파일로 출력 리다이렉트

```python
from contextlib import redirect_stdout

with open('output.log', 'w') as f:
    with redirect_stdout(f):
        print("This goes to file")
        help(str)  # help 출력도 파일로
```

### 5. ExitStack - 동적 컨텍스트 관리

```python
from contextlib import ExitStack

# 동적 개수의 파일 열기
filenames = ['file1.txt', 'file2.txt', 'file3.txt']

with ExitStack() as stack:
    files = [
        stack.enter_context(open(fname, 'w'))
        for fname in filenames
    ]
    # 모든 파일에 쓰기
    for f in files:
        f.write("content")
# ExitStack이 모든 파일을 자동으로 닫음
```

### 6. ExitStack - 콜백 등록

```python
from contextlib import ExitStack

def cleanup(name):
    print(f"Cleaning up: {name}")

with ExitStack() as stack:
    stack.callback(cleanup, "resource1")
    stack.callback(cleanup, "resource2")
    print("Working...")
# 출력:
# Working...
# Cleaning up: resource2
# Cleaning up: resource1
# (LIFO 순서로 호출)
```

### 7. ExitStack - 예외 시에도 정리

```python
from contextlib import ExitStack

def acquire_resource(name):
    print(f"Acquiring {name}")
    if name == "bad":
        raise ValueError("Failed!")
    return name

with ExitStack() as stack:
    try:
        r1 = acquire_resource("good1")
        stack.callback(print, f"Releasing {r1}")
        
        r2 = acquire_resource("bad")  # 예외 발생
        stack.callback(print, f"Releasing {r2}")
    except ValueError:
        print("Error occurred")

# 출력:
# Acquiring good1
# Acquiring bad
# Error occurred
# Releasing good1
```

### 8. nullcontext - 조건부 컨텍스트

```python
from contextlib import nullcontext

def process(data, lock=None):
    # lock이 있으면 사용, 없으면 무시
    with lock if lock else nullcontext():
        print(f"Processing {data}")

# lock 없이
process("data1")

# lock과 함께
import threading
my_lock = threading.Lock()
process("data2", lock=my_lock)
```

### 9. nullcontext로 값 전달 (Python 3.10+)

```python
from contextlib import nullcontext

# 조건부로 파일 또는 stdout
def write_output(data, filename=None):
    cm = open(filename, 'w') if filename else nullcontext(sys.stdout)
    with cm as f:
        f.write(data)
```

### 10. closing - close() 자동 호출

```python
from contextlib import closing
from urllib.request import urlopen

# urlopen은 컨텍스트 매니저가 아닌 버전 대응
with closing(urlopen('https://example.com')) as page:
    content = page.read()

# 커스텀 객체에도 사용
class Resource:
    def close(self):
        print("Resource closed")

with closing(Resource()) as r:
    print("Using resource")
# Resource closed
```

### 11. ExitStack을 클래스에서 사용

```python
from contextlib import ExitStack

class ResourceManager:
    def __init__(self):
        self._stack = ExitStack()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc_info):
        return self._stack.__exit__(*exc_info)
    
    def add_file(self, path, mode='r'):
        f = self._stack.enter_context(open(path, mode))
        return f

with ResourceManager() as rm:
    f1 = rm.add_file('file1.txt', 'w')
    f2 = rm.add_file('file2.txt', 'w')
    f1.write("content1")
    f2.write("content2")
# 모든 파일 자동 닫힘
```

## 자주 하는 실수

### 1. suppress 범위 과도하게 넓히기

```python
from contextlib import suppress

# 나쁨 - 모든 예외 무시
with suppress(Exception):
    risky_operation()

# 좋음 - 특정 예외만 무시
with suppress(FileNotFoundError):
    os.remove('temp.txt')
```

### 2. redirect 후 원래 출력 사용

```python
from contextlib import redirect_stdout
from io import StringIO

# 주의: redirect 블록 안에서 원래 stdout 사용 불가
original_stdout = sys.stdout

f = StringIO()
with redirect_stdout(f):
    print("Captured")
    # 원래 stdout으로 출력하려면:
    print("Direct", file=original_stdout)
```

## 한눈에 정리

| 도구 | 용도 | 예시 |
|------|------|------|
| `suppress` | 예외 무시 | `suppress(KeyError)` |
| `redirect_stdout` | stdout 리다이렉트 | 로그 캡처 |
| `redirect_stderr` | stderr 리다이렉트 | 에러 로그 캡처 |
| `ExitStack` | 동적 컨텍스트 | 가변 개수 리소스 |
| `nullcontext` | 조건부 컨텍스트 | 선택적 락 |
| `closing` | close() 보장 | 레거시 객체 |

## 참고

- [contextlib - Python Docs](https://docs.python.org/3/library/contextlib.html)
- [ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack)
