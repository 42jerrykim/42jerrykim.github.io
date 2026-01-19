---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 16. Environment Variables - os.environ/dotenv 패턴"
slug: "manage-env-variables-os-environ-dotenv-envfile-configuration-guide"
description: "환경 변수를 안전하게 다루기 위한 치트시트입니다. os.environ 읽기/쓰기, python-dotenv로 .env 파일 로드, 설정 분리 패턴, 보안 주의점과 12-factor app 원칙을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 16
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - environment-variables
  - 환경변수
  - os.environ
  - environ
  - dotenv
  - python-dotenv
  - .env
  - env-file
  - configuration
  - 설정
  - config
  - secrets
  - 시크릿
  - 비밀키
  - api-key
  - API키
  - credentials
  - 자격증명
  - security
  - 보안
  - 12-factor
  - twelve-factor
  - deployment
  - 배포
  - docker
  - 도커
  - getenv
  - setenv
  - os
  - pathlib
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - development
  - 개발환경
  - production
  - 운영환경
  - separation
  - 분리
---
환경 변수는 코드와 설정을 분리하는 핵심 방법입니다. 이 치트시트는 os.environ으로 환경 변수 읽기/쓰기, python-dotenv로 .env 파일 관리, 보안 주의점을 정리합니다.

## 언제 이 치트시트를 보나?

- API 키, DB 연결 문자열 등 **민감한 정보**를 코드에서 분리하고 싶을 때
- 개발/스테이징/프로덕션 환경별 설정을 다르게 하고 싶을 때

## 핵심 패턴

- 읽기: `os.environ.get("KEY", "default")` → 없으면 기본값 반환
- 필수 값: `os.environ["KEY"]` → 없으면 KeyError (의도적 실패)
- .env 파일: `python-dotenv`로 로드 → 개발 환경에서 편리
- **절대 커밋 금지**: `.env`는 `.gitignore`에 추가

## 최소 예제

```python
import os

# 환경 변수 읽기 (기본값 지정)
db_host = os.environ.get("DB_HOST", "localhost")
db_port = int(os.environ.get("DB_PORT", "5432"))
debug = os.environ.get("DEBUG", "false").lower() == "true"

print(f"Connecting to {db_host}:{db_port}, debug={debug}")
```

```python
# 환경 변수 필수 값 (없으면 바로 에러)
import os

api_key = os.environ["API_KEY"]  # KeyError if not set
```

```python
# 환경 변수 쓰기 (현재 프로세스에서만 유효)
import os

os.environ["MY_VAR"] = "value"
print(os.environ.get("MY_VAR"))  # "value"
```

```python
# 모든 환경 변수 확인
import os

for key, value in os.environ.items():
    print(f"{key}={value}")
```

## python-dotenv 사용

```bash
# 설치
pip install python-dotenv
```

```text
# .env 파일 예시 (프로젝트 루트에 생성)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
API_KEY=your-secret-key-here
DEBUG=true
```

```python
# .env 파일 로드
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()  # 기본: 현재 디렉토리의 .env

# 이제 os.environ으로 접근 가능
api_key = os.environ.get("API_KEY")
debug = os.environ.get("DEBUG", "false").lower() == "true"
```

```python
# 특정 경로의 .env 파일 로드
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env.local"
load_dotenv(dotenv_path=env_path)
```

```python
# .env 파일 내용을 dict로 가져오기 (os.environ에 로드하지 않음)
from dotenv import dotenv_values

config = dotenv_values(".env")
print(config["DB_HOST"])
```

## 설정 클래스 패턴 (권장)

```python
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    db_host: str = os.environ.get("DB_HOST", "localhost")
    db_port: int = int(os.environ.get("DB_PORT", "5432"))
    db_name: str = os.environ.get("DB_NAME", "myapp")
    api_key: str = os.environ.get("API_KEY", "")
    debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

config = Config()
print(config.db_host, config.debug)
```

## .gitignore 설정

```gitignore
# .gitignore에 반드시 추가
.env
.env.local
.env.*.local
*.pem
*.key
```

## 자주 하는 실수/주의점

- **.env 파일 커밋 금지**: API 키, 비밀번호가 Git 히스토리에 남으면 보안 사고
- **타입 변환 필수**: 환경 변수는 항상 **문자열**로 반환됨 → `int()`, `bool()` 직접 변환
  ```python
  # 숫자
  port = int(os.environ.get("PORT", "8080"))
  
  # 불리언 (주의: "false"도 truthy)
  debug = os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")
  ```
- **로드 순서**: `load_dotenv()`는 기존 환경 변수를 덮어쓰지 않음 → 시스템 환경 변수가 우선
- **프로덕션에서는 .env 사용 자제**: Docker/K8s에서는 시스템 환경 변수나 시크릿 매니저 사용
- **.env.example 제공**: 필요한 환경 변수 목록을 팀원에게 공유 (값은 비움)

## .env.example 템플릿

```text
# .env.example (커밋 가능)
# 이 파일을 .env로 복사하고 실제 값을 채우세요

DB_HOST=localhost
DB_PORT=5432
DB_NAME=
API_KEY=
DEBUG=false
```

## 관련 링크(공식 문서)

- [os.environ — Environment mapping](https://docs.python.org/3/library/os.html#os.environ)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [The Twelve-Factor App - Config](https://12factor.net/config)
