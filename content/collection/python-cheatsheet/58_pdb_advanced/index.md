---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 58. pdb 심화 - 대화형 디버깅"
slug: "pdb-interactive-debugger-advanced-usage-post-mortem-breakpoint-guide"
description: "파이썬 pdb 모듈 심화 치트시트입니다. breakpoint(), 중단점, 변수 검사, 스텝 실행, 조건부 중단, 사후 분석 디버깅 등 대화형 디버거 명령을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 58
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - pdb
  - debugger
  - 디버거
  - debugging
  - 디버깅
  - breakpoint
  - 중단점
  - step
  - 스텝
  - next
  - continue
  - print
  - 출력
  - variable
  - 변수
  - stack
  - 스택
  - frame
  - 프레임
  - post-mortem
  - 사후분석
  - conditional
  - 조건부
  - watch
  - 감시
  - interactive
  - 대화형
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`pdb`는 파이썬의 **대화형 디버거**입니다. 중단점 설정, 코드 스텝 실행, 변수 검사 등 강력한 디버깅 기능을 제공합니다.

## 언제 이 치트시트를 보나?

- **print 디버깅**으로 부족할 때
- **런타임에 변수 상태**를 검사하고 싶을 때
- **예외 발생 시점**의 상태를 분석하고 싶을 때

## pdb 시작 방법

```python
# 방법 1: breakpoint() (Python 3.7+, 권장)
breakpoint()

# 방법 2: import pdb
import pdb; pdb.set_trace()

# 방법 3: 명령행에서 실행
# python -m pdb script.py
```

## 핵심 명령어

| 명령 | 단축 | 설명 |
|------|------|------|
| `help` | `h` | 도움말 |
| `next` | `n` | 다음 줄 (함수 안으로 들어가지 않음) |
| `step` | `s` | 다음 줄 (함수 안으로 들어감) |
| `continue` | `c` | 다음 중단점까지 실행 |
| `list` | `l` | 현재 위치 소스 보기 |
| `print` | `p` | 표현식 출력 |
| `pp` | | 예쁘게 출력 |
| `where` | `w` | 스택 트레이스 |
| `quit` | `q` | 디버거 종료 |

## 최소 예제

### 1. 기본 사용

```python
def calculate(x, y):
    result = x + y
    breakpoint()  # 여기서 멈춤
    return result * 2

total = calculate(3, 4)
print(total)
```

```
> script.py(4)calculate()
-> return result * 2
(Pdb) p result
7
(Pdb) p x, y
(3, 4)
(Pdb) n
--Return--
> script.py(4)calculate()->14
(Pdb) c
14
```

### 2. 코드 탐색

```python
def outer():
    x = 10
    inner()

def inner():
    y = 20
    breakpoint()
    print(y)

outer()
```

```
(Pdb) l          # 현재 위치 코드 보기
(Pdb) l 1, 10    # 1-10줄 보기
(Pdb) ll         # 현재 함수 전체
(Pdb) w          # 스택 트레이스
(Pdb) u          # 상위 프레임으로
(Pdb) d          # 하위 프레임으로
```

### 3. 변수 검사

```
(Pdb) p variable      # 변수 출력
(Pdb) pp large_dict   # 예쁘게 출력
(Pdb) p type(obj)     # 타입 확인
(Pdb) p dir(obj)      # 속성 목록
(Pdb) p vars(obj)     # __dict__
(Pdb) !x = 10         # 변수 수정 (! 접두사)
```

### 4. 스텝 실행

```python
def func_a():
    return func_b()

def func_b():
    return 42

breakpoint()
result = func_a()
```

```
(Pdb) n    # func_a() 전체 실행 (안으로 들어가지 않음)
(Pdb) s    # func_a() 안으로 들어감
(Pdb) r    # 현재 함수 끝까지 실행 후 반환
```

### 5. 중단점 관리

```
(Pdb) b 10           # 10번 줄에 중단점
(Pdb) b func_name    # 함수 시작에 중단점
(Pdb) b file.py:20   # 특정 파일의 줄
(Pdb) b              # 모든 중단점 보기
(Pdb) cl 1           # 중단점 1 삭제
(Pdb) cl             # 모든 중단점 삭제
(Pdb) disable 1      # 중단점 1 비활성화
(Pdb) enable 1       # 중단점 1 활성화
```

### 6. 조건부 중단점

```
(Pdb) b 10, x > 5          # x > 5일 때만 멈춤
(Pdb) b func, len(items) > 100

# 또는 코드에서
def process(items):
    for i, item in enumerate(items):
        if i == 50:  # 50번째에서만
            breakpoint()
        handle(item)
```

### 7. 사후 분석 디버깅 (Post-mortem)

```python
import pdb

def buggy():
    x = 1
    y = 0
    return x / y  # ZeroDivisionError

try:
    buggy()
except:
    pdb.post_mortem()  # 예외 발생 시점으로
```

```
# 또는 명령행에서
# python -m pdb script.py
# 예외 발생 시 자동으로 pdb 진입
```

### 8. 표현식 실행

```
(Pdb) !import json           # 모듈 import
(Pdb) !result = x + y        # 코드 실행
(Pdb) p json.dumps(data)     # 함수 호출
(Pdb) interact               # 대화형 Python 쉘
```

### 9. 디버깅 없이 실행

```python
import os

# PYTHONBREAKPOINT 환경 변수로 제어
# export PYTHONBREAKPOINT=0  # breakpoint() 무시
# export PYTHONBREAKPOINT=ipdb.set_trace  # ipdb 사용

def debug_code():
    breakpoint()  # PYTHONBREAKPOINT=0이면 무시됨
    print("code")
```

### 10. 원격 디버깅 (remote-pdb)

```python
# pip install remote-pdb
from remote_pdb import set_trace
set_trace(host='0.0.0.0', port=4444)

# 다른 터미널에서:
# telnet 127.0.0.1 4444
```

## 유용한 팁

### .pdbrc 설정 파일

```
# ~/.pdbrc
alias pi p dir(%1)
alias pl p locals()
alias pg p globals()
```

### pdb++ (향상된 pdb)

```bash
pip install pdbpp
```

```python
# 자동으로 pdb 대체
# 구문 강조, sticky mode 등 제공
breakpoint()
```

## 자주 쓰는 패턴

```
# 루프에서 특정 조건일 때만 멈추기
for i in range(1000):
    if i == 500:
        breakpoint()
    process(i)

# 함수 시작점에서 항상 멈추기
def complex_function(data):
    breakpoint()
    # ...

# 예외 직전 상태 확인
try:
    risky_operation()
except Exception:
    import pdb; pdb.set_trace()
    raise
```

## 자주 하는 실수

### 1. 명령어와 변수명 충돌

```
(Pdb) p n        # 'n'이라는 변수? 아니면 next 명령?
(Pdb) p(n)       # 변수 n 출력
(Pdb) !n         # 변수 n 출력
```

### 2. 프로덕션에 breakpoint 남기기

```python
# 커밋 전 체크
# git diff --staged | grep -E "breakpoint|pdb"
```

## 한눈에 정리

| 카테고리 | 명령 |
|----------|------|
| 실행 | `n` (next), `s` (step), `c` (continue), `r` (return) |
| 검사 | `p` (print), `pp`, `w` (where), `l` (list) |
| 중단점 | `b` (break), `cl` (clear), `disable`, `enable` |
| 프레임 | `u` (up), `d` (down) |
| 기타 | `q` (quit), `h` (help), `interact` |

## 참고

- [pdb - Python Docs](https://docs.python.org/3/library/pdb.html)
- [pdb++ (pdbpp)](https://github.com/pdbpp/pdbpp)
