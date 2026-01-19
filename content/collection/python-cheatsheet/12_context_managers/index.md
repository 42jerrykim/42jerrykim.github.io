---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 12. Context Managers - with문/리소스 관리"
slug: "context-manager-with-resource-management-best-practices-guide"
description: "파이썬 컨텍스트 매니저를 빠르게 쓰기 위한 치트시트입니다. with문 기본, __enter__/__exit__ 프로토콜, @contextmanager 데코레이터, 다중 컨텍스트, 실무 패턴과 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 12
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - context-manager
  - context-managers
  - 컨텍스트매니저
  - with
  - with-statement
  - __enter__
  - __exit__
  - contextlib
  - contextmanager
  - resource
  - 리소스
  - cleanup
  - 정리
  - file
  - 파일
  - lock
  - 락
  - transaction
  - 트랜잭션
  - connection
  - 연결
  - database
  - 데이터베이스
  - exception
  - 예외
  - error-handling
  - 예외처리
  - finally
  - try
  - suppress
  - ExitStack
  - closing
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
---
컨텍스트 매니저는 리소스의 획득과 해제를 안전하게 관리하는 파이썬의 핵심 패턴입니다. 이 치트시트는 with문, `__enter__/__exit__`, @contextmanager, 실무 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- 파일, DB 연결, 락 등 **정리가 필요한 리소스**를 다룰 때
- 예외가 나도 **반드시 실행**되어야 하는 정리 코드가 있을 때

## 핵심 패턴

- `with` 문: 블록 진입 시 `__enter__()`, 종료 시 `__exit__()` 자동 호출
- 예외가 발생해도 `__exit__()`는 반드시 실행됨
- `@contextmanager`: 제너레이터로 간단하게 컨텍스트 매니저 작성
- `contextlib.suppress()`: 특정 예외 무시

## 최소 예제

```python
# 기본 사용: 파일 자동 닫기
with open("file.txt", "w") as f:
    f.write("Hello")
# 블록 종료 시 f.close() 자동 호출 (예외 발생해도)
```

```python
# 클래스로 컨텍스트 매니저 구현
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self  # as 뒤의 변수에 바인딩
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # 예외를 다시 raise (True면 억제)

with Timer() as t:
    sum(range(1000000))
# Elapsed: 0.0234s
```

```python
# @contextmanager로 간단하게 구현
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.perf_counter()
    try:
        yield  # with 블록 실행 지점
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed: {elapsed:.4f}s")

with timer():
    sum(range(1000000))
```

```python
# 값을 yield하는 컨텍스트 매니저
from contextlib import contextmanager

@contextmanager
def temp_directory():
    import tempfile
    import shutil
    
    dirpath = tempfile.mkdtemp()
    try:
        yield dirpath  # with ... as dirpath
    finally:
        shutil.rmtree(dirpath)  # 항상 정리

with temp_directory() as tmpdir:
    print(f"Working in {tmpdir}")
    # 작업 수행...
# 블록 종료 시 디렉토리 삭제
```

## 다중 컨텍스트 매니저

```python
# 여러 파일 동시에
with open("input.txt") as f_in, open("output.txt", "w") as f_out:
    f_out.write(f_in.read())

# Python 3.10+ 괄호 사용 가능
with (
    open("a.txt") as a,
    open("b.txt") as b,
    open("c.txt") as c,
):
    pass
```

## contextlib 유틸리티

```python
from contextlib import suppress, closing, ExitStack

# suppress: 특정 예외 무시
with suppress(FileNotFoundError):
    os.remove("maybe_not_exists.txt")
# 파일이 없어도 예외 없이 통과

# closing: close() 메서드 자동 호출
from urllib.request import urlopen
with closing(urlopen("https://example.com")) as page:
    html = page.read()

# ExitStack: 동적으로 컨텍스트 매니저 관리
files = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    handles = [stack.enter_context(open(f)) for f in files]
    # 모든 파일이 블록 종료 시 자동으로 닫힘
```

## `__exit__` 시그니처

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    """
    exc_type: 예외 클래스 (예외 없으면 None)
    exc_val: 예외 인스턴스
    exc_tb: traceback 객체
    
    반환값:
    - False/None: 예외를 다시 raise
    - True: 예외를 억제 (삼키기)
    """
    if exc_type is not None:
        print(f"Exception occurred: {exc_val}")
    return False  # 예외 전파
```

## 실무 패턴

```python
# DB 트랜잭션
@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

with transaction(db_connection) as conn:
    conn.execute("INSERT INTO ...")
    conn.execute("UPDATE ...")
# 성공 시 commit, 예외 시 rollback
```

```python
# 임시 작업 디렉토리 변경
import os
from contextlib import contextmanager

@contextmanager
def working_directory(path):
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)

with working_directory("/tmp"):
    print(os.getcwd())  # /tmp
print(os.getcwd())  # 원래 디렉토리
```

## 자주 하는 실수/주의점

- **`finally` 대신 `with` 사용**: 컨텍스트 매니저가 더 읽기 쉽고 안전
- **예외 억제 주의**: `__exit__`에서 `True` 반환 시 예외가 사라짐 → 디버깅 어려움
- **`yield` 전후 구분**: `yield` 전 = `__enter__`, `yield` 후 = `__exit__`
- **중첩 vs 다중**: `with a: with b:` 보다 `with a, b:` 권장
- **비동기**: `async with`는 `__aenter__`/`__aexit__` 사용

## 관련 링크(공식 문서)

- [The with statement](https://docs.python.org/3/reference/compound_stmts.html#with)
- [contextlib](https://docs.python.org/3/library/contextlib.html)
