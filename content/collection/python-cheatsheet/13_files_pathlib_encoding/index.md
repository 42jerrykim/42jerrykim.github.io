---

image: "wordcloud.png"
title: "[Python Cheatsheet] 13. Files - pathlib/encoding/open 패턴"
slug: "file-io-open-path-encoding-best-practice-guide"
description: "파일 입출력과 경로 처리를 빠르게 하기 위한 치트시트입니다. pathlib로 경로 다루기, open()의 encoding/newline, 텍스트·바이너리 모드, 안전한 읽기/쓰기(with) 패턴과 흔한 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 13
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - file-io
  - 파일
  - 입출력
  - io
  - open
  - with
  - context-manager
  - 컨텍스트매니저
  - pathlib
  - Path
  - path
  - 경로
  - filesystem
  - 파일시스템
  - encoding
  - 인코딩
  - decoding
  - 디코딩
  - utf-8
  - newline
  - text-mode
  - binary-mode
  - bytes
  - errors
  - exceptions
  - 예외처리
  - FileNotFoundError
  - OSError
  - permissions
  - 권한
  - glob
  - rglob
  - performance
  - 성능
  - buffering
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - logging
  - 로깅
  - portability
  - 이식성
  - windows
  - linux
  - macos
---
파일 입출력과 경로 처리는 대부분의 프로그램에서 필요합니다. 이 치트시트는 pathlib 경로 다루기, encoding 명시, 텍스트/바이너리 모드의 핵심 패턴과 OS별 함정을 정리합니다.

## 언제 이 치트시트를 보나?

- 경로 join/정규화 때문에 OS별 버그가 날 때
- “왜 한글이 깨지지?” 같은 encoding 문제가 생길 때

## 핵심 패턴

- 경로는 `pathlib.Path`로 처리(문자열 join 지양)
- 텍스트 파일은 `encoding="utf-8"`를 명시하는 습관
- CSV 등은 `newline=""`를 요구하는 경우가 있음(다음 챕터 참고)
- 자원 관리는 `with open(...) as f:`로

## 최소 예제

```python
from pathlib import Path

p = Path("data") / "input.txt"
print(p.exists())
```

```python
# 텍스트 읽기
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

```python
# 라인 단위 처리(메모리 절약)
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        # process line
```

```python
# 바이너리 읽기
with open("image.png", "rb") as f:
    blob = f.read(16)
    print(blob)
```

```python
# pathlib로 glob
from pathlib import Path

root = Path(".")
for md in root.rglob("*.md"):
    pass
```

## 자주 하는 실수/주의점

- Windows에서 역슬래시/이스케이프 문제 → 문자열로 경로 조합하지 말고 `Path` 사용
- encoding을 안 적으면 환경마다 기본값이 달라 깨질 수 있음 → `utf-8` 명시
- 큰 파일을 `read()`로 한 번에 읽지 말고 라인/청크 단위로 처리

## 관련 링크(공식 문서)

- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
- [open()](https://docs.python.org/3/library/functions.html#open)

