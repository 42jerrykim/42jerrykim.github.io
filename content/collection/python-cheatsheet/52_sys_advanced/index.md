---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 52. sys 심화 - 인터프리터와 런타임 정보"
slug: "sys-module-advanced-runtime-interpreter-tips-guide"
description: "파이썬 sys 모듈 심화 치트시트입니다. 명령행 인자, 표준 입출력, 모듈 경로, 인터프리터 정보, 재귀 제한, 종료 처리 등 핵심 기능을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 52
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - sys
  - system
  - 시스템
  - argv
  - 명령행인자
  - stdin
  - stdout
  - stderr
  - 표준입출력
  - path
  - 모듈경로
  - modules
  - 모듈
  - exit
  - 종료
  - version
  - 버전
  - platform
  - 플랫폼
  - recursion
  - 재귀
  - getsizeof
  - 메모리
  - interpreter
  - 인터프리터
  - runtime
  - 런타임
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`sys` 모듈은 **파이썬 인터프리터와 런타임 환경**에 접근합니다. 명령행 인자, 모듈 시스템, 표준 스트림, 인터프리터 설정 등을 다룹니다.

## 언제 이 치트시트를 보나?

- **명령행 인자**를 처리할 때 (간단한 경우)
- **모듈 검색 경로**를 조작할 때
- **인터프리터 정보**나 제한을 확인/변경할 때

## 명령행 인자

### 1. sys.argv

```python
import sys

# python script.py arg1 arg2
print(sys.argv)     # ['script.py', 'arg1', 'arg2']
print(sys.argv[0])  # 'script.py' (스크립트 이름)
print(sys.argv[1:]) # ['arg1', 'arg2'] (인자들)

# 인자 개수 체크
if len(sys.argv) < 2:
    print("Usage: script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
```

## 표준 입출력

### 2. stdin, stdout, stderr

```python
import sys

# 표준 출력
sys.stdout.write("Hello\n")  # print()와 유사

# 표준 에러
sys.stderr.write("Error message\n")

# 표준 입력
line = sys.stdin.readline()

# 출력 리다이렉션
original_stdout = sys.stdout
with open('output.txt', 'w') as f:
    sys.stdout = f
    print("This goes to file")
sys.stdout = original_stdout
```

### 3. 버퍼링

```python
import sys

# 버퍼 즉시 플러시
print("Progress...", end='', flush=True)

# 또는
sys.stdout.flush()
```

## 모듈 시스템

### 4. 모듈 검색 경로 (sys.path)

```python
import sys

# 모듈 검색 경로 목록
print(sys.path)
# ['', '/usr/lib/python3.x', ...]

# 경로 추가 (임시)
sys.path.insert(0, '/my/custom/modules')

# 또는 append
sys.path.append('/another/path')
```

### 5. 로드된 모듈 (sys.modules)

```python
import sys
import json

# 로드된 모듈 딕셔너리
print('json' in sys.modules)  # True

# 모듈 언로드 (재import 강제)
if 'mymodule' in sys.modules:
    del sys.modules['mymodule']
import mymodule  # 다시 로드
```

## 인터프리터 정보

### 6. 버전 정보

```python
import sys

# 버전 문자열
print(sys.version)
# '3.11.0 (main, Oct 24 2022, 18:26:48) [GCC 11.2.0]'

# 버전 튜플 (비교에 유용)
print(sys.version_info)
# sys.version_info(major=3, minor=11, micro=0, releaselevel='final', serial=0)

# 버전 체크
if sys.version_info >= (3, 10):
    print("Python 3.10 이상")
```

### 7. 플랫폼 정보

```python
import sys

# 플랫폼
print(sys.platform)  # 'linux', 'darwin', 'win32'

# OS별 분기
if sys.platform == 'win32':
    path_sep = '\\'
else:
    path_sep = '/'

# 바이트 순서
print(sys.byteorder)  # 'little' 또는 'big'
```

### 8. 실행 파일 경로

```python
import sys

# Python 인터프리터 경로
print(sys.executable)
# '/usr/bin/python3'

# 접두사 (설치 경로)
print(sys.prefix)
# '/usr' 또는 가상환경 경로
```

## 제한과 설정

### 9. 재귀 제한

```python
import sys

# 현재 재귀 제한
print(sys.getrecursionlimit())  # 1000 (기본값)

# 재귀 제한 변경
sys.setrecursionlimit(2000)

# 주의: 너무 높이면 스택 오버플로우
```

### 10. 객체 크기

```python
import sys

# 객체의 메모리 크기 (바이트)
print(sys.getsizeof([]))         # 56
print(sys.getsizeof([1, 2, 3]))  # 80
print(sys.getsizeof("hello"))    # 54
print(sys.getsizeof(42))         # 28

# 딕셔너리
d = {'a': 1, 'b': 2}
print(sys.getsizeof(d))          # 184
```

### 11. 참조 카운트

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + 함수 인자로 임시 참조)

b = a  # 참조 추가
print(sys.getrefcount(a))  # 3
```

## 프로그램 종료

### 12. sys.exit

```python
import sys

# 정상 종료
sys.exit(0)

# 에러와 함께 종료
sys.exit(1)

# 에러 메시지와 함께
sys.exit("Error: Something went wrong")

# try-except로 잡기 가능
try:
    sys.exit(1)
except SystemExit as e:
    print(f"Exit code: {e.code}")
```

## 예외 정보

### 13. 현재 예외

```python
import sys

try:
    1 / 0
except:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(f"Type: {exc_type}")
    print(f"Value: {exc_value}")
    print(f"Traceback: {exc_tb}")
```

## 유용한 상수

### 14. 주요 상수들

```python
import sys

# 정수 최대값 (Python 3에서는 무제한이지만)
print(sys.maxsize)  # 9223372036854775807 (64비트)

# 부동소수점 정보
print(sys.float_info.max)      # 최대 float
print(sys.float_info.epsilon)  # 정밀도

# 해시 시드 (랜덤화)
print(sys.hash_info.hash_bits)

# 기본 인코딩
print(sys.getdefaultencoding())  # 'utf-8'
print(sys.getfilesystemencoding())  # 'utf-8'
```

## 실용 예제

### 15. 간단한 CLI 스크립트

```python
#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command> [args]", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'version':
        print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    elif command == 'platform':
        print(sys.platform)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## 자주 하는 실수

### 1. sys.path 수정 시점

```python
import sys

# 잘못: import 후 path 수정
import mymodule  # 이미 검색 완료
sys.path.insert(0, '/new/path')

# 올바름: import 전에 path 수정
sys.path.insert(0, '/new/path')
import mymodule
```

### 2. exit vs sys.exit

```python
# exit()은 대화형용, 스크립트에서는 sys.exit() 사용
import sys
sys.exit(0)  # 올바름
# exit(0)    # 작동하지만 권장하지 않음
```

## 한눈에 정리

| 카테고리 | 주요 속성/함수 |
|----------|---------------|
| 명령행 | `argv` |
| 입출력 | `stdin`, `stdout`, `stderr` |
| 모듈 | `path`, `modules` |
| 버전 | `version`, `version_info`, `platform` |
| 제한 | `getrecursionlimit()`, `getsizeof()` |
| 종료 | `exit()` |

## 참고

- [sys - Python Docs](https://docs.python.org/3/library/sys.html)
