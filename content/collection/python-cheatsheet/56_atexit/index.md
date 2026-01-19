---

image: "wordcloud.png"
title: "[Python Cheatsheet] 56. atexit - 프로그램 종료 시 정리"
slug: "atexit-module-exit-callbacks-cleanup-automation-guide"
description: "파이썬 atexit 모듈을 빠르게 사용하기 위한 치트시트입니다. 종료 콜백 등록, 리소스 정리, 임시 파일 삭제 등 프로그램 종료 시 실행할 작업을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 56
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - atexit
  - exit
  - 종료
  - cleanup
  - 정리
  - callback
  - 콜백
  - register
  - 등록
  - unregister
  - resource
  - 리소스
  - temporary
  - 임시파일
  - shutdown
  - 셧다운
  - finalization
  - 종료처리
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`atexit` 모듈은 **프로그램 정상 종료 시 실행할 함수를 등록**합니다. 리소스 정리, 임시 파일 삭제, 로그 기록 등 종료 작업에 유용합니다.

## 언제 이 치트시트를 보나?

- 프로그램 종료 시 **리소스 정리**가 필요할 때
- **임시 파일 삭제**를 보장하고 싶을 때
- **종료 로그**를 남기고 싶을 때

## 핵심 함수

```python
import atexit

atexit.register(func, *args, **kwargs)  # 종료 콜백 등록
atexit.unregister(func)                 # 콜백 제거
```

## 최소 예제

### 1. 기본 사용

```python
import atexit

def cleanup():
    print("Cleanup: Closing resources...")

def goodbye(name):
    print(f"Goodbye, {name}!")

# 종료 콜백 등록
atexit.register(cleanup)
atexit.register(goodbye, "User")

print("Program running...")
# 프로그램 종료 시:
# Goodbye, User!
# Cleanup: Closing resources...
# (LIFO 순서로 실행)
```

### 2. 데코레이터로 등록

```python
import atexit

@atexit.register
def cleanup():
    print("Cleanup executed")

print("Working...")
```

### 3. 임시 파일 정리

```python
import atexit
import os

temp_files = []

def create_temp_file(name):
    temp_files.append(name)
    with open(name, 'w') as f:
        f.write("temp data")
    return name

def cleanup_temp_files():
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed: {f}")

atexit.register(cleanup_temp_files)

# 임시 파일 생성
create_temp_file('temp1.txt')
create_temp_file('temp2.txt')
# 종료 시 자동 삭제
```

### 4. 데이터베이스 연결 종료

```python
import atexit

class Database:
    def __init__(self, name):
        self.name = name
        self.connected = True
        print(f"Connected to {name}")
        
        # 종료 시 자동 disconnect
        atexit.register(self.disconnect)
    
    def disconnect(self):
        if self.connected:
            print(f"Disconnecting from {self.name}")
            self.connected = False

db = Database("mydb")
print("Using database...")
# 종료 시 자동으로 disconnect 호출
```

### 5. 콜백 제거

```python
import atexit

def my_cleanup():
    print("This won't run")

atexit.register(my_cleanup)

# 조건에 따라 제거
if some_condition:
    atexit.unregister(my_cleanup)
```

### 6. 종료 로그 기록

```python
import atexit
from datetime import datetime

def log_shutdown():
    timestamp = datetime.now().isoformat()
    with open('shutdown.log', 'a') as f:
        f.write(f"Program terminated at {timestamp}\n")

atexit.register(log_shutdown)
```

### 7. 여러 핸들러 순서

```python
import atexit

def first():
    print("First (registered first, runs last)")

def second():
    print("Second")

def third():
    print("Third (registered last, runs first)")

atexit.register(first)
atexit.register(second)
atexit.register(third)

# 종료 시 출력:
# Third (registered last, runs first)
# Second
# First (registered first, runs last)
```

### 8. 클래스 메서드 등록

```python
import atexit

class Service:
    instances = []
    
    def __init__(self, name):
        self.name = name
        Service.instances.append(self)
    
    def cleanup(self):
        print(f"Cleaning up {self.name}")
    
    @classmethod
    def cleanup_all(cls):
        for instance in cls.instances:
            instance.cleanup()

atexit.register(Service.cleanup_all)

s1 = Service("Service1")
s2 = Service("Service2")
```

### 9. 컨텍스트 매니저와 함께

```python
import atexit
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    resource = acquire_resource(name)
    # 종료 시 정리 보장
    atexit.register(release_resource, resource)
    try:
        yield resource
    finally:
        release_resource(resource)
        atexit.unregister(release_resource)
```

## 실행되지 않는 경우

```python
import atexit
import os

def cleanup():
    print("This may not run")

atexit.register(cleanup)

# 실행되지 않는 경우:
# 1. os._exit() 호출 시
os._exit(1)  # atexit 핸들러 무시

# 2. SIGKILL로 종료 시 (kill -9)

# 3. 치명적 에러 (segfault 등)

# 실행되는 경우:
# - sys.exit()
# - 정상 종료
# - 처리되지 않은 예외
```

## 자주 하는 실수

### 1. 람다 사용 시 클로저 문제

```python
import atexit

files = []

# 잘못: 람다는 나중에 평가됨
for name in ['a.txt', 'b.txt']:
    atexit.register(lambda: print(f"Cleanup {name}"))
    # 모두 "Cleanup b.txt" 출력

# 올바름: 기본값으로 캡처
for name in ['a.txt', 'b.txt']:
    atexit.register(lambda n=name: print(f"Cleanup {n}"))
```

### 2. 핸들러에서 예외

```python
import atexit

def bad_handler():
    raise Exception("Error in cleanup")

def good_handler():
    try:
        risky_operation()
    except Exception as e:
        print(f"Cleanup error: {e}")

atexit.register(good_handler)
atexit.register(bad_handler)  # 예외가 출력되고 다음 핸들러 계속
```

## atexit vs __del__ vs finally

```python
import atexit

# atexit: 프로그램 종료 시 (권장)
atexit.register(cleanup)

# __del__: 객체 소멸 시 (신뢰하기 어려움)
class MyClass:
    def __del__(self):
        pass  # 호출 시점 불확실

# finally: 블록 종료 시
try:
    work()
finally:
    cleanup()  # 항상 실행

# 컨텍스트 매니저: 가장 명확
with resource as r:
    work()  # 종료 시 __exit__ 호출
```

## 한눈에 정리

| 함수 | 용도 |
|------|------|
| `register(func, *args)` | 종료 콜백 등록 |
| `unregister(func)` | 콜백 제거 |
| `@atexit.register` | 데코레이터로 등록 |

## 참고

- [atexit - Python Docs](https://docs.python.org/3/library/atexit.html)
