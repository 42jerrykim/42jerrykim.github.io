---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 53. shutil & tempfile - 파일/디렉토리 복사/이동/임시파일"
slug: "file-directory-automation-shutil-tempfile-best-practices"
description: "파이썬 shutil과 tempfile 모듈을 빠르게 쓰기 위한 치트시트입니다. 파일/디렉토리 복사/이동/삭제, 디스크 용량 확인, 임시 파일/디렉토리 안전 생성과 자동 정리 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 53
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - shutil
  - tempfile
  - copy
  - 복사
  - move
  - 이동
  - delete
  - 삭제
  - rmtree
  - copytree
  - 디렉토리
  - directory
  - file
  - 파일
  - temporary
  - 임시파일
  - temp
  - tmp
  - NamedTemporaryFile
  - TemporaryDirectory
  - mkstemp
  - mkdtemp
  - disk-usage
  - 디스크용량
  - archive
  - 아카이브
  - zip
  - tar
  - filesystem
  - 파일시스템
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - cleanup
  - 정리
  - security
  - 보안
---
shutil은 고수준 파일/디렉토리 작업을, tempfile은 안전한 임시 파일 생성을 제공합니다. 이 치트시트는 복사/이동/삭제, 임시 파일 패턴, 자동 정리 방법을 정리합니다.

## 언제 이 치트시트를 보나?

- 파일/폴더를 **복사, 이동, 삭제**해야 할 때
- **임시 파일/디렉토리**를 안전하게 만들고 자동 정리하고 싶을 때

## 핵심 패턴

- `shutil.copy()` / `shutil.copytree()`: 파일/디렉토리 복사
- `shutil.move()`: 파일/디렉토리 이동
- `shutil.rmtree()`: 디렉토리 재귀 삭제
- `tempfile.NamedTemporaryFile()`: 이름 있는 임시 파일 (자동 삭제)
- `tempfile.TemporaryDirectory()`: 임시 디렉토리 (자동 삭제)

## shutil - 파일 복사

```python
import shutil
from pathlib import Path

# 파일 복사 (메타데이터 유지 안 함)
shutil.copy("src.txt", "dst.txt")
shutil.copy("src.txt", "backup/")  # 디렉토리로 복사

# 파일 복사 (메타데이터 유지)
shutil.copy2("src.txt", "dst.txt")

# 파일 내용만 복사 (권한 등 무시)
shutil.copyfile("src.txt", "dst.txt")

# 권한만 복사
shutil.copymode("src.txt", "dst.txt")

# 메타데이터만 복사 (권한, 시간 등)
shutil.copystat("src.txt", "dst.txt")
```

## shutil - 디렉토리 복사

```python
import shutil

# 디렉토리 전체 복사
shutil.copytree("src_dir", "dst_dir")

# 특정 파일 제외하고 복사
def ignore_patterns(directory, files):
    return [f for f in files if f.endswith('.pyc') or f == '__pycache__']

shutil.copytree("src_dir", "dst_dir", ignore=ignore_patterns)

# 또는 shutil.ignore_patterns() 사용
shutil.copytree(
    "src_dir", "dst_dir",
    ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git")
)

# 이미 존재하는 디렉토리에 복사 (Py3.8+)
shutil.copytree("src_dir", "existing_dir", dirs_exist_ok=True)
```

## shutil - 이동/삭제

```python
import shutil

# 파일/디렉토리 이동 (rename과 유사하지만 다른 파일시스템도 가능)
shutil.move("old_path", "new_path")

# 디렉토리 재귀 삭제 (주의: 복구 불가!)
shutil.rmtree("dir_to_delete")

# 에러 무시하고 삭제
shutil.rmtree("dir_to_delete", ignore_errors=True)

# 에러 핸들링
def on_error(func, path, exc_info):
    print(f"Error deleting {path}: {exc_info}")

shutil.rmtree("dir_to_delete", onerror=on_error)
```

## shutil - 디스크 용량/아카이브

```python
import shutil

# 디스크 용량 확인
usage = shutil.disk_usage("/")
print(f"Total: {usage.total // (1024**3)} GB")
print(f"Used: {usage.used // (1024**3)} GB")
print(f"Free: {usage.free // (1024**3)} GB")

# 아카이브 생성
shutil.make_archive("backup", "zip", "src_dir")      # backup.zip 생성
shutil.make_archive("backup", "tar", "src_dir")      # backup.tar 생성
shutil.make_archive("backup", "gztar", "src_dir")    # backup.tar.gz 생성

# 아카이브 추출
shutil.unpack_archive("backup.zip", "extract_dir")
```

## tempfile - 임시 파일

```python
import tempfile

# 임시 파일 (자동 삭제)
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=True) as f:
    f.write("temporary content")
    f.flush()
    print(f.name)  # /tmp/tmpXXXXXX.txt
    # 파일 사용...
# with 블록 종료 시 자동 삭제

# 삭제하지 않고 유지 (수동 삭제 필요)
f = tempfile.NamedTemporaryFile(mode='w', delete=False)
try:
    f.write("content")
    f.close()
    # f.name으로 파일 경로 사용
finally:
    import os
    os.unlink(f.name)  # 수동 삭제
```

```python
# Windows 호환 패턴 (delete_on_close=False, Py3.12+)
# Py3.11 이하에서는 delete=False 후 수동 관리

import tempfile
import os

# 크로스 플랫폼 안전 패턴
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    temp_path = f.name
    f.write("content")

try:
    # temp_path 사용
    with open(temp_path, 'r') as f:
        print(f.read())
finally:
    os.unlink(temp_path)
```

## tempfile - 임시 디렉토리

```python
import tempfile
from pathlib import Path

# 임시 디렉토리 (자동 삭제)
with tempfile.TemporaryDirectory() as tmpdir:
    print(tmpdir)  # /tmp/tmpXXXXXX
    
    # 디렉토리 안에서 작업
    file_path = Path(tmpdir) / "test.txt"
    file_path.write_text("hello")
    
# with 블록 종료 시 디렉토리와 내용물 모두 자동 삭제
```

```python
# prefix/suffix 지정
with tempfile.TemporaryDirectory(prefix="myapp_", suffix="_cache") as tmpdir:
    print(tmpdir)  # /tmp/myapp_XXXXXX_cache
```

## tempfile - 저수준 함수

```python
import tempfile
import os

# 임시 파일 생성 (fd, path 튜플 반환)
fd, path = tempfile.mkstemp(suffix='.txt')
try:
    os.write(fd, b"content")
finally:
    os.close(fd)
    os.unlink(path)

# 임시 디렉토리 생성 (path만 반환)
tmpdir = tempfile.mkdtemp()
try:
    # 디렉토리 사용
    pass
finally:
    import shutil
    shutil.rmtree(tmpdir)

# 임시 디렉토리 경로 확인
print(tempfile.gettempdir())  # /tmp (Linux) 또는 C:\Users\...\Temp (Windows)
```

## 실전 패턴

```python
# 안전한 파일 교체 (atomic write)
import tempfile
import shutil
import os

def safe_write(filepath: str, content: str) -> None:
    """파일을 안전하게 덮어쓰기 (중간에 실패해도 원본 보존)"""
    dir_path = os.path.dirname(filepath) or '.'
    
    with tempfile.NamedTemporaryFile(
        mode='w', dir=dir_path, delete=False
    ) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        shutil.move(temp_path, filepath)
    except:
        os.unlink(temp_path)
        raise

safe_write("config.json", '{"key": "value"}')
```

```python
# 백업 후 작업
import shutil
import tempfile

def process_with_backup(filepath: str) -> None:
    with tempfile.TemporaryDirectory() as backup_dir:
        backup_path = f"{backup_dir}/backup"
        shutil.copy2(filepath, backup_path)
        
        try:
            # 위험한 작업 수행
            with open(filepath, 'a') as f:
                f.write("new content")
        except Exception:
            # 실패 시 복원
            shutil.copy2(backup_path, filepath)
            raise
```

## 자주 하는 실수/주의점

- **rmtree는 복구 불가**: 휴지통으로 가지 않음, 신중하게 사용
- **NamedTemporaryFile Windows 문제**: Windows에서는 열린 파일을 다른 프로세스가 열 수 없음 → `delete=False` 사용
- **경로 주의**: `shutil.move()`는 목적지가 디렉토리면 그 안으로 이동
- **권한 문제**: 복사 시 원본 파일 권한이 유지되지 않을 수 있음 → `copy2()` 사용
- **임시 파일 경로 의존 금지**: OS마다 임시 디렉토리 위치가 다름

## 관련 링크(공식 문서)

- [shutil — High-level file operations](https://docs.python.org/3/library/shutil.html)
- [tempfile — Generate temporary files and directories](https://docs.python.org/3/library/tempfile.html)
