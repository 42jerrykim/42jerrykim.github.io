---

image: "wordcloud.png"
title: "[Python Cheatsheet] 55. signal - 시그널 처리"
slug: "signal-module-unix-signal-handling-graceful-shutdown-interrupts"
description: "파이썬 signal 모듈을 빠르게 사용하기 위한 치트시트입니다. SIGINT, SIGTERM 처리, 그레이스풀 종료, 타임아웃, 알람 등 시그널 핸들링 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 55
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - signal
  - 시그널
  - SIGINT
  - SIGTERM
  - SIGKILL
  - SIGALRM
  - SIGHUP
  - handler
  - 핸들러
  - interrupt
  - 인터럽트
  - ctrl-c
  - graceful-shutdown
  - 그레이스풀종료
  - timeout
  - 타임아웃
  - alarm
  - 알람
  - process
  - 프로세스
  - unix
  - linux
  - daemon
  - 데몬
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`signal` 모듈은 **Unix 시그널 핸들링**을 제공합니다. Ctrl+C 처리, 그레이스풀 종료, 타임아웃 등에 사용됩니다. (Windows에서는 일부 기능 제한)

## 언제 이 치트시트를 보나?

- **Ctrl+C (SIGINT)**를 우아하게 처리하고 싶을 때
- **프로세스 종료 시 정리 작업**이 필요할 때
- **타임아웃**을 시그널로 구현하고 싶을 때

## 주요 시그널

| 시그널 | 번호 | 설명 |
|--------|------|------|
| SIGINT | 2 | Ctrl+C, 인터럽트 |
| SIGTERM | 15 | 종료 요청 (kill 기본) |
| SIGKILL | 9 | 강제 종료 (처리 불가) |
| SIGALRM | 14 | 알람 타이머 |
| SIGHUP | 1 | 터미널 종료 |

## 최소 예제

### 1. Ctrl+C (SIGINT) 처리

```python
import signal
import sys

def signal_handler(signum, frame):
    print("\nCtrl+C pressed! Cleaning up...")
    sys.exit(0)

# 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

print("Press Ctrl+C to exit")
while True:
    pass
```

### 2. 그레이스풀 종료

```python
import signal
import sys
import time

running = True

def graceful_shutdown(signum, frame):
    global running
    print(f"\nReceived signal {signum}. Shutting down gracefully...")
    running = False

# SIGINT와 SIGTERM 모두 처리
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

print("Server running. PID:", os.getpid())
while running:
    print("Working...")
    time.sleep(1)

print("Cleanup complete. Goodbye!")
```

### 3. 이전 핸들러 저장

```python
import signal

def custom_handler(signum, frame):
    print("Custom handler called")
    # 이전 핸들러 호출
    if callable(old_handler):
        old_handler(signum, frame)

# 이전 핸들러 저장
old_handler = signal.signal(signal.SIGINT, custom_handler)

# 나중에 복원
signal.signal(signal.SIGINT, old_handler)
```

### 4. 시그널 무시

```python
import signal

# SIGINT 무시 (Ctrl+C가 작동 안 함)
signal.signal(signal.SIGINT, signal.SIG_IGN)

# 기본 동작 복원
signal.signal(signal.SIGINT, signal.SIG_DFL)
```

### 5. 알람 타이머 (Unix)

```python
import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out!")

# 알람 핸들러 설정
signal.signal(signal.SIGALRM, timeout_handler)

# 5초 후 알람
signal.alarm(5)

try:
    print("Starting long operation...")
    time.sleep(10)  # 5초 후 TimeoutError
except TimeoutError as e:
    print(e)
finally:
    signal.alarm(0)  # 알람 취소
```

### 6. 타임아웃 컨텍스트 매니저

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Timed out after {seconds} seconds")
    
    # 핸들러 설정
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)  # 알람 취소
        signal.signal(signal.SIGALRM, old_handler)  # 복원

# 사용
try:
    with timeout(3):
        import time
        time.sleep(10)  # TimeoutError 발생
except TimeoutError as e:
    print(e)
```

### 7. 특정 시그널 블록 (Unix)

```python
import signal
import time

# SIGINT 일시 블록
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT])
print("SIGINT blocked for 5 seconds")
time.sleep(5)

# 블록 해제
signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGINT])
print("SIGINT unblocked")
```

### 8. 대기 중 시그널 처리 (pause)

```python
import signal
import os

def handler(signum, frame):
    print(f"Received signal {signum}")

signal.signal(signal.SIGUSR1, handler)
print(f"PID: {os.getpid()}")
print("Waiting for SIGUSR1...")

# 시그널 대기 (다른 터미널에서 kill -USR1 <PID>)
signal.pause()
print("Signal received!")
```

### 9. 자식 프로세스 종료 감지

```python
import signal
import os

def child_handler(signum, frame):
    # 종료된 자식 수거
    pid, status = os.waitpid(-1, os.WNOHANG)
    print(f"Child {pid} terminated with status {status}")

signal.signal(signal.SIGCHLD, child_handler)
```

### 10. 데몬 프로세스 리로드 (SIGHUP)

```python
import signal
import sys

config = {'debug': False}

def reload_config(signum, frame):
    global config
    print("Reloading configuration...")
    # 설정 파일 다시 로드
    # config = load_config()
    config['debug'] = not config['debug']
    print(f"Config reloaded: {config}")

signal.signal(signal.SIGHUP, reload_config)

print(f"PID: {os.getpid()}")
print("Send SIGHUP to reload config")
while True:
    signal.pause()
```

## Windows 제한사항

```python
import signal
import sys

if sys.platform == 'win32':
    # Windows에서 사용 가능한 시그널
    # SIGINT, SIGTERM, SIGABRT, SIGFPE, SIGILL, SIGSEGV
    
    # SIGALRM, SIGHUP 등은 사용 불가
    pass
else:
    # Unix 전용 시그널 사용 가능
    signal.signal(signal.SIGHUP, handler)
    signal.signal(signal.SIGALRM, handler)
```

## 자주 하는 실수

### 1. 핸들러에서 복잡한 작업

```python
import signal

# 나쁨: 핸들러에서 I/O나 락 사용
def bad_handler(signum, frame):
    with open('log.txt', 'w') as f:  # 위험!
        f.write("Signal received")

# 좋음: 플래그만 설정
shutdown_flag = False

def good_handler(signum, frame):
    global shutdown_flag
    shutdown_flag = True

# 메인 루프에서 플래그 확인
while not shutdown_flag:
    do_work()
```

### 2. 비동기 안전하지 않은 함수 호출

```python
import signal

# 핸들러에서 피해야 할 것들:
# - print() (버퍼링 문제)
# - logging
# - 락 획득
# - 메모리 할당

# 안전한 작업:
# - 플래그 설정 (volatile)
# - 파이프에 바이트 쓰기
```

## 한눈에 정리

| 함수 | 용도 |
|------|------|
| `signal(sig, handler)` | 핸들러 등록 |
| `alarm(seconds)` | 알람 설정 |
| `pause()` | 시그널 대기 |
| `SIG_IGN` | 시그널 무시 |
| `SIG_DFL` | 기본 동작 |

## 참고

- [signal - Python Docs](https://docs.python.org/3/library/signal.html)
