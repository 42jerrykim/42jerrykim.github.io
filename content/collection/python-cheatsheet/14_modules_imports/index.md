---

image: "wordcloud.png"
title: "[Python Cheatsheet] 14. Modules & Imports - 구조/엔트리포인트"
slug: "effective-modules-imports-absolute-relative-entrypoint-guide"
description: "모듈/임포트를 실무에서 안전하게 쓰기 위한 치트시트입니다. import 패턴, __name__ == \"__main__\", 상대/절대 import, 패키지 구조 감각, sys.path 함정과 간단한 프로젝트 레이아웃을 정리합니다."
lastmod: 2026-01-17
collection_order: 14
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - modules
  - module
  - 모듈
  - packages
  - package
  - 패키지
  - imports
  - import
  - 임포트
  - absolute-import
  - relative-import
  - __init__.py
  - __main__
  - entrypoint
  - 엔트리포인트
  - scripts
  - 스크립트
  - sys.path
  - path
  - 경로
  - project-structure
  - 프로젝트구조
  - packaging
  - 배포
  - pip
  - venv
  - namespace
  - 네임스페이스
  - circular-import
  - 순환참조
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - debugging
  - 디버깅
  - clean-code
  - 클린코드
  - architecture
  - 아키텍처
  - typing
  - 타입힌트
  - testing
  - 테스트
---
모듈과 패키지 구조는 프로젝트 규모가 커질수록 중요해집니다. 이 치트시트는 import 패턴, `__name__ == "__main__"` 가드, sys.path 함정, 순환 import 해결 등을 정리합니다.

## 언제 이 치트시트를 보나?

- “같은 파일인데 import가 안 된다” 같은 경로/패키지 문제를 만났을 때
- 스크립트 실행과 라이브러리 사용을 동시에 지원하고 싶을 때

## 핵심 패턴

- 엔트리포인트 가드:
  - `if __name__ == "__main__": main()`
- 상대 import는 패키지 내부에서만(스크립트로 직접 실행 시 깨질 수 있음)
- 순환 import가 나면 “공통 의존”을 분리하거나 import 위치를 조정

## 최소 예제

```python
def main():
    print("run")

if __name__ == "__main__":
    main()
```

```python
# 절대 import 예시
import json
from pathlib import Path
```

## 자주 하는 실수/주의점

- 실행 위치(cwd)에 따라 import가 우연히 되거나 깨질 수 있음 → 패키지 구조로 정리
- `sys.path`를 런타임에 수정하는 방식은 임시방편이 되기 쉬움
- 파일명이 `json.py` 같은 표준 라이브러리와 충돌하면 import가 꼬일 수 있음

## 관련 링크(공식 문서)

- [Modules (Tutorial)](https://docs.python.org/3/tutorial/modules.html)
- [The import system](https://docs.python.org/3/reference/import.html)

