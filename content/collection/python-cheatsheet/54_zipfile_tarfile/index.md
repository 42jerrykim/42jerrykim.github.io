---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 54. zipfile & tarfile - 압축 파일 읽기/쓰기/추출"
slug: "zipfile-tarfile-archive-compression-extract-secure-guide"
description: "파이썬 zipfile과 tarfile 모듈을 빠르게 쓰기 위한 치트시트입니다. ZIP/TAR 아카이브 생성/추출, 파일 추가/목록 조회, 암호화, 메모리 내 처리 패턴과 보안 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 54
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - zipfile
  - tarfile
  - archive
  - 아카이브
  - compression
  - 압축
  - zip
  - tar
  - gzip
  - bz2
  - xz
  - extract
  - 추출
  - compress
  - decompress
  - 압축해제
  - file
  - 파일
  - directory
  - 디렉토리
  - ZipFile
  - TarFile
  - namelist
  - extractall
  - write
  - add
  - security
  - 보안
  - path-traversal
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
zipfile과 tarfile은 파이썬에서 압축 파일을 다루는 표준 모듈입니다. 이 치트시트는 ZIP/TAR 아카이브 생성, 추출, 파일 추가와 보안 주의점을 정리합니다.

## 언제 이 치트시트를 보나?

- **ZIP/TAR 파일**을 프로그래밍으로 생성하거나 추출해야 할 때
- 파일들을 **하나의 아카이브**로 묶어서 배포/백업하고 싶을 때

## 핵심 패턴

- `ZipFile(path, 'r'/'w'/'a')`: ZIP 읽기/쓰기/추가
- `TarFile.open(path, 'r'/'w'/'r:gz')`: TAR 읽기/쓰기 (압축 옵션)
- 추출 시 **경로 순회 공격** 주의 → `extractall()` 대신 검증 후 추출

## zipfile - ZIP 읽기

```python
import zipfile

# ZIP 파일 열기 및 목록 확인
with zipfile.ZipFile('archive.zip', 'r') as zf:
    # 파일 목록
    print(zf.namelist())
    # ['file1.txt', 'folder/file2.txt']
    
    # 상세 정보
    for info in zf.infolist():
        print(f"{info.filename}: {info.file_size} bytes")

# 특정 파일 읽기
with zipfile.ZipFile('archive.zip', 'r') as zf:
    content = zf.read('file1.txt')  # bytes
    text = content.decode('utf-8')
    print(text)

# 파일처럼 열기
with zipfile.ZipFile('archive.zip', 'r') as zf:
    with zf.open('file1.txt') as f:
        for line in f:
            print(line.decode('utf-8').strip())
```

## zipfile - ZIP 추출

```python
import zipfile
from pathlib import Path

# 전체 추출
with zipfile.ZipFile('archive.zip', 'r') as zf:
    zf.extractall('output_dir')

# 특정 파일만 추출
with zipfile.ZipFile('archive.zip', 'r') as zf:
    zf.extract('file1.txt', 'output_dir')

# 안전한 추출 (경로 순회 공격 방지)
def safe_extract(zip_path: str, extract_dir: str) -> None:
    extract_path = Path(extract_dir).resolve()
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for member in zf.namelist():
            member_path = (extract_path / member).resolve()
            # 추출 경로가 대상 디렉토리 안에 있는지 확인
            if not str(member_path).startswith(str(extract_path)):
                raise ValueError(f"Path traversal detected: {member}")
        
        zf.extractall(extract_dir)

safe_extract('archive.zip', 'output_dir')
```

## zipfile - ZIP 생성

```python
import zipfile
from pathlib import Path

# 새 ZIP 파일 생성
with zipfile.ZipFile('new_archive.zip', 'w') as zf:
    # 파일 추가
    zf.write('file1.txt')
    
    # 아카이브 내 경로 지정
    zf.write('file2.txt', arcname='folder/file2.txt')
    
    # 문자열에서 직접 추가
    zf.writestr('hello.txt', 'Hello, World!')

# 압축 옵션
with zipfile.ZipFile('compressed.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('large_file.txt')

# 압축률 조정 (compresslevel: 0-9)
with zipfile.ZipFile('compressed.zip', 'w', 
                     zipfile.ZIP_DEFLATED, 
                     compresslevel=9) as zf:
    zf.write('large_file.txt')
```

```python
# 디렉토리 전체 압축
import zipfile
from pathlib import Path

def zip_directory(dir_path: str, zip_path: str) -> None:
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in Path(dir_path).rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dir_path)
                zf.write(file_path, arcname)

zip_directory('my_folder', 'my_folder.zip')
```

## zipfile - 기존 ZIP에 추가

```python
import zipfile

# 기존 ZIP에 파일 추가
with zipfile.ZipFile('archive.zip', 'a') as zf:
    zf.write('new_file.txt')
```

## tarfile - TAR 읽기/추출

```python
import tarfile

# TAR 파일 열기 (자동 압축 감지)
with tarfile.open('archive.tar.gz', 'r:*') as tf:
    # 파일 목록
    print(tf.getnames())
    
    # 상세 정보
    for member in tf.getmembers():
        print(f"{member.name}: {member.size} bytes")

# 전체 추출
with tarfile.open('archive.tar.gz', 'r:gz') as tf:
    tf.extractall('output_dir')

# 특정 파일만 추출
with tarfile.open('archive.tar.gz', 'r:gz') as tf:
    tf.extract('file1.txt', 'output_dir')

# 안전한 추출 (Py3.12+)
with tarfile.open('archive.tar.gz', 'r:gz') as tf:
    tf.extractall('output_dir', filter='data')  # 안전한 필터

# Py3.11 이하 안전 추출
def safe_tar_extract(tar_path: str, extract_dir: str) -> None:
    from pathlib import Path
    extract_path = Path(extract_dir).resolve()
    
    with tarfile.open(tar_path, 'r:*') as tf:
        for member in tf.getmembers():
            member_path = (extract_path / member.name).resolve()
            if not str(member_path).startswith(str(extract_path)):
                raise ValueError(f"Path traversal: {member.name}")
            if member.issym() or member.islnk():
                raise ValueError(f"Symlink not allowed: {member.name}")
        
        tf.extractall(extract_dir)
```

## tarfile - TAR 생성

```python
import tarfile

# 비압축 TAR
with tarfile.open('archive.tar', 'w') as tf:
    tf.add('file1.txt')
    tf.add('folder', arcname='renamed_folder')

# gzip 압축
with tarfile.open('archive.tar.gz', 'w:gz') as tf:
    tf.add('file1.txt')

# bzip2 압축
with tarfile.open('archive.tar.bz2', 'w:bz2') as tf:
    tf.add('file1.txt')

# xz 압축 (높은 압축률)
with tarfile.open('archive.tar.xz', 'w:xz') as tf:
    tf.add('file1.txt')
```

```python
# 특정 파일 제외
import tarfile

def exclude_filter(tarinfo):
    # .pyc 파일과 __pycache__ 제외
    if tarinfo.name.endswith('.pyc') or '__pycache__' in tarinfo.name:
        return None
    return tarinfo

with tarfile.open('archive.tar.gz', 'w:gz') as tf:
    tf.add('my_project', filter=exclude_filter)
```

## 메모리 내 처리

```python
import zipfile
import io

# 메모리에서 ZIP 생성
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('hello.txt', 'Hello from memory!')

# buffer.getvalue()로 bytes 얻기
zip_bytes = buffer.getvalue()

# 메모리에서 ZIP 읽기
buffer = io.BytesIO(zip_bytes)
with zipfile.ZipFile(buffer, 'r') as zf:
    print(zf.read('hello.txt').decode())
```

## 자주 하는 실수/주의점

- **경로 순회 공격**: `../../../etc/passwd` 같은 악의적 경로 → 추출 전 검증 필수
- **심볼릭 링크 공격**: TAR의 symlink로 시스템 파일 덮어쓰기 가능 → 필터링 필요
- **대용량 파일**: 압축 해제 시 디스크 가득 참 (zip bomb) → 크기 검증
- **인코딩 문제**: 파일명 인코딩이 다를 수 있음 (특히 Windows에서 생성된 ZIP)
- **모드 문자열**:
  - TAR: `'r'` (자동), `'r:gz'` (gzip), `'r:bz2'`, `'r:xz'`
  - ZIP: `'r'`, `'w'`, `'a'` (추가)

## 관련 링크(공식 문서)

- [zipfile — Work with ZIP archives](https://docs.python.org/3/library/zipfile.html)
- [tarfile — Read and write tar archive files](https://docs.python.org/3/library/tarfile.html)
