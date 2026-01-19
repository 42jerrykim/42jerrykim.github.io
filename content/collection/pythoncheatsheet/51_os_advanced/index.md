---
draft: true
title: "[Python Cheatsheet] 51. os 심화 - 파일시스템과 프로세스"
slug: "os-os-advanced-operating-system-filesystem-directory-path-walk-listdir"
description: "파이썬 os 모듈 심화 치트시트입니다. 디렉토리 순회, 파일 정보, 환경 변수, 프로세스 관리, 경로 처리 등 os 모듈의 핵심 기능을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 51
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - os
  - operating-system
  - 운영체제
  - filesystem
  - 파일시스템
  - directory
  - 디렉토리
  - path
  - 경로
  - walk
  - listdir
  - scandir
  - makedirs
  - remove
  - rename
  - stat
  - environ
  - 환경변수
  - process
  - 프로세스
  - pid
  - fork
  - getenv
  - getcwd
  - chdir
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - cross-platform
  - 크로스플랫폼
---
`os` 모듈은 **운영체제와 상호작용**하는 기능을 제공합니다. 파일 시스템 조작, 환경 변수, 프로세스 정보 등을 다룹니다. 경로 처리는 `pathlib`을 권장하지만, `os`도 여전히 유용합니다.

## 언제 이 치트시트를 보나?

- **디렉토리 순회** (`os.walk`)가 필요할 때
- **환경 변수**를 읽거나 설정할 때
- **프로세스 정보**가 필요할 때

## 디렉토리 작업

### 1. 현재 디렉토리

```python
import os

# 현재 작업 디렉토리
cwd = os.getcwd()
print(cwd)  # /home/user/project

# 디렉토리 변경
os.chdir('/tmp')
print(os.getcwd())  # /tmp
```

### 2. 디렉토리 목록

```python
import os

# 기본 목록 (이름만)
entries = os.listdir('.')
print(entries)  # ['file.txt', 'subdir', ...]

# scandir (더 효율적, 파일 정보 포함)
with os.scandir('.') as entries:
    for entry in entries:
        print(f"{entry.name}: dir={entry.is_dir()}, file={entry.is_file()}")
```

### 3. 디렉토리 생성/삭제

```python
import os

# 단일 디렉토리 생성
os.mkdir('new_dir')

# 중첩 디렉토리 생성
os.makedirs('path/to/nested', exist_ok=True)

# 빈 디렉토리 삭제
os.rmdir('new_dir')

# 중첩 디렉토리 삭제 (빈 디렉토리만)
os.removedirs('path/to/nested')
```

### 4. os.walk - 재귀 순회

```python
import os

# 모든 하위 파일/디렉토리 순회
for root, dirs, files in os.walk('.'):
    print(f"\n디렉토리: {root}")
    print(f"  하위 디렉토리: {dirs}")
    print(f"  파일: {files}")
    
    # 특정 디렉토리 제외
    if '.git' in dirs:
        dirs.remove('.git')  # in-place 수정으로 순회 제외

# 특정 확장자 파일만 찾기
python_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            python_files.append(os.path.join(root, f))
```

## 파일 작업

### 5. 파일 정보 (stat)

```python
import os
from datetime import datetime

stat_info = os.stat('file.txt')

print(f"크기: {stat_info.st_size} bytes")
print(f"수정 시간: {datetime.fromtimestamp(stat_info.st_mtime)}")
print(f"접근 시간: {datetime.fromtimestamp(stat_info.st_atime)}")
print(f"권한: {oct(stat_info.st_mode)}")
```

### 6. 파일 삭제/이름 변경

```python
import os

# 파일 삭제
os.remove('file.txt')

# 파일/디렉토리 이름 변경
os.rename('old_name.txt', 'new_name.txt')

# 파일 이동 (다른 디렉토리로)
os.rename('file.txt', 'subdir/file.txt')
```

### 7. 존재 확인

```python
import os

# 존재 여부
os.path.exists('/path/to/file')

# 파일인지 확인
os.path.isfile('/path/to/file')

# 디렉토리인지 확인
os.path.isdir('/path/to/dir')

# 심볼릭 링크인지 확인
os.path.islink('/path/to/link')
```

## 경로 처리

### 8. os.path 함수들

```python
import os

path = '/home/user/documents/file.txt'

# 경로 분해
os.path.dirname(path)     # '/home/user/documents'
os.path.basename(path)    # 'file.txt'
os.path.split(path)       # ('/home/user/documents', 'file.txt')

# 확장자 분리
os.path.splitext(path)    # ('/home/user/documents/file', '.txt')

# 경로 결합 (OS에 맞게)
os.path.join('dir', 'subdir', 'file.txt')  # 'dir/subdir/file.txt'

# 절대 경로
os.path.abspath('file.txt')

# 정규화
os.path.normpath('/home/user/../user/./file')  # '/home/user/file'
```

## 환경 변수

### 9. 환경 변수 읽기/설정

```python
import os

# 읽기
home = os.environ.get('HOME')
path = os.environ.get('PATH')

# 기본값과 함께
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

# 필수 환경 변수 (없으면 KeyError)
api_key = os.environ['API_KEY']

# 설정 (현재 프로세스만)
os.environ['MY_VAR'] = 'value'

# 삭제
del os.environ['MY_VAR']
```

### 10. 모든 환경 변수

```python
import os

# 딕셔너리처럼 사용
for key, value in os.environ.items():
    print(f"{key}={value}")

# 특정 접두사 필터
db_vars = {k: v for k, v in os.environ.items() if k.startswith('DB_')}
```

## 프로세스 정보

### 11. 프로세스 ID

```python
import os

print(f"현재 PID: {os.getpid()}")
print(f"부모 PID: {os.getppid()}")
print(f"사용자 ID: {os.getuid()}")    # Unix
print(f"그룹 ID: {os.getgid()}")      # Unix
```

### 12. 시스템 정보

```python
import os

# OS 이름
print(os.name)  # 'posix' (Linux/Mac) 또는 'nt' (Windows)

# CPU 코어 수
print(os.cpu_count())  # 8

# 터미널 크기
try:
    size = os.get_terminal_size()
    print(f"터미널: {size.columns}x{size.lines}")
except OSError:
    print("터미널 아님")
```

### 13. 프로세스 종료

```python
import os
import sys

# 정상 종료
sys.exit(0)

# 즉시 종료 (_exit은 cleanup 없음)
os._exit(0)

# 다른 프로세스에 시그널
os.kill(pid, signal.SIGTERM)
```

## 유틸리티

### 14. 임시 파일 디렉토리

```python
import os
import tempfile

# 시스템 임시 디렉토리
print(tempfile.gettempdir())  # '/tmp' 또는 'C:\Users\...\Temp'

# 또는
print(os.environ.get('TMPDIR', '/tmp'))
```

### 15. 파일 디스크립터

```python
import os

# 저수준 파일 열기
fd = os.open('file.txt', os.O_RDONLY)
content = os.read(fd, 1024)
os.close(fd)

# 파이프
r, w = os.pipe()
os.write(w, b'hello')
os.close(w)
data = os.read(r, 100)
os.close(r)
```

## 자주 하는 실수

### 1. 경로 결합에 + 사용

```python
import os

# 잘못: OS별 구분자 문제
path = 'dir' + '/' + 'file.txt'

# 올바름: os.path.join 사용
path = os.path.join('dir', 'file.txt')

# 더 나음: pathlib 사용
from pathlib import Path
path = Path('dir') / 'file.txt'
```

### 2. 환경 변수 없을 때

```python
import os

# 위험: KeyError 발생 가능
# value = os.environ['MAYBE_NOT_SET']

# 안전: get 사용
value = os.environ.get('MAYBE_NOT_SET', 'default')
```

## 한눈에 정리

| 카테고리 | 주요 함수 |
|----------|----------|
| 디렉토리 | `getcwd()`, `listdir()`, `walk()`, `makedirs()` |
| 파일 | `remove()`, `rename()`, `stat()` |
| 경로 | `path.join()`, `path.split()`, `path.exists()` |
| 환경 변수 | `environ`, `getenv()` |
| 프로세스 | `getpid()`, `cpu_count()` |

## 참고

- [os - Python Docs](https://docs.python.org/3/library/os.html)
- [os.path - Python Docs](https://docs.python.org/3/library/os.path.html)
