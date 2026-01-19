---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 41. configparser & tomllib - INI/TOML 설정 파일"
slug: "configparser-and-tomllib-toml-ini-config-configuration-settings-key"
description: "파이썬 configparser와 tomllib 모듈을 빠르게 쓰기 위한 치트시트입니다. INI/TOML 설정 파일 읽기/쓰기, 섹션/키 접근, 기본값 처리, pyproject.toml 파싱 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 41
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - configparser
  - tomllib
  - toml
  - ini
  - config
  - 설정
  - configuration
  - settings
  - pyproject
  - pyproject.toml
  - section
  - 섹션
  - key
  - value
  - 키
  - 값
  - default
  - 기본값
  - fallback
  - interpolation
  - 보간
  - read
  - write
  - parse
  - 파싱
  - file
  - 파일
  - standard-library
  - 표준라이브러리
  - python311
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
configparser는 INI 형식을, tomllib(Py3.11+)은 TOML 형식의 설정 파일을 처리합니다. 이 치트시트는 설정 파일 읽기/쓰기, 섹션 접근, 기본값 처리 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- **INI/TOML 형식**의 설정 파일을 읽거나 써야 할 때
- `pyproject.toml`에서 프로젝트 메타데이터를 파싱하고 싶을 때

## 핵심 패턴

- `configparser`: INI 파일 읽기/쓰기 (모든 값이 문자열)
- `tomllib`: TOML 파일 읽기 전용 (Py3.11+, 타입 보존)
- TOML 쓰기: `tomli_w` 또는 `tomlkit` 라이브러리 필요

## configparser - INI 읽기

```ini
# config.ini 예시
[DEFAULT]
debug = false
timeout = 30

[database]
host = localhost
port = 5432
name = myapp

[api]
url = https://api.example.com
timeout = 60
```

```python
import configparser

# INI 파일 읽기
config = configparser.ConfigParser()
config.read('config.ini')

# 섹션 목록
print(config.sections())  # ['database', 'api']

# 값 읽기
host = config['database']['host']
print(host)  # 'localhost'

# get() 메서드 (기본값 지정 가능)
port = config.get('database', 'port')
print(port)  # '5432' (문자열!)

# 기본값 사용
missing = config.get('database', 'missing', fallback='default')
print(missing)  # 'default'

# DEFAULT 섹션 값 상속
debug = config.get('database', 'debug')
print(debug)  # 'false' (DEFAULT에서 상속)
```

```python
# 타입 변환 메서드
config = configparser.ConfigParser()
config.read('config.ini')

# 정수
port = config.getint('database', 'port')
print(port, type(port))  # 5432 <class 'int'>

# 불리언
debug = config.getboolean('DEFAULT', 'debug')
print(debug, type(debug))  # False <class 'bool'>

# 실수
timeout = config.getfloat('DEFAULT', 'timeout')
print(timeout)  # 30.0
```

## configparser - INI 쓰기

```python
import configparser

config = configparser.ConfigParser()

# 섹션 추가
config['DEFAULT'] = {
    'debug': 'false',
    'timeout': '30'
}

config['database'] = {
    'host': 'localhost',
    'port': '5432',
    'name': 'myapp'
}

config['api'] = {}
config['api']['url'] = 'https://api.example.com'

# 파일로 저장
with open('config.ini', 'w') as f:
    config.write(f)
```

```python
# 기존 파일 수정
config = configparser.ConfigParser()
config.read('config.ini')

# 값 변경
config['database']['host'] = 'production-db.example.com'

# 섹션 추가
config['new_section'] = {'key': 'value'}

# 저장
with open('config.ini', 'w') as f:
    config.write(f)
```

## tomllib - TOML 읽기 (Py3.11+)

```toml
# config.toml 예시
title = "My Application"
debug = true

[database]
host = "localhost"
port = 5432  # 정수 유지
enabled = true  # 불리언 유지

[database.connection]
timeout = 30.5
retries = 3

[api]
endpoints = ["users", "products", "orders"]  # 배열

[[servers]]  # 배열 of 테이블
name = "server1"
ip = "10.0.0.1"

[[servers]]
name = "server2"
ip = "10.0.0.2"
```

```python
import tomllib

# TOML 파일 읽기
with open('config.toml', 'rb') as f:  # 바이너리 모드 필수
    config = tomllib.load(f)

# 딕셔너리로 반환 (타입 보존)
print(config['title'])           # 'My Application'
print(config['debug'])           # True (bool)
print(config['database']['port']) # 5432 (int)

# 중첩 테이블
print(config['database']['connection']['timeout'])  # 30.5 (float)

# 배열
print(config['api']['endpoints'])  # ['users', 'products', 'orders']

# 테이블 배열
for server in config['servers']:
    print(server['name'], server['ip'])
# server1 10.0.0.1
# server2 10.0.0.2
```

```python
# 문자열에서 파싱
import tomllib

toml_string = """
[database]
host = "localhost"
port = 5432
"""

config = tomllib.loads(toml_string)
print(config['database']['host'])  # 'localhost'
```

## pyproject.toml 파싱

```python
import tomllib
from pathlib import Path

def get_project_version() -> str:
    """pyproject.toml에서 버전 읽기"""
    pyproject_path = Path('pyproject.toml')
    
    with open(pyproject_path, 'rb') as f:
        data = tomllib.load(f)
    
    # setuptools/hatch 형식
    if 'project' in data:
        return data['project'].get('version', '0.0.0')
    
    # poetry 형식
    if 'tool' in data and 'poetry' in data['tool']:
        return data['tool']['poetry'].get('version', '0.0.0')
    
    return '0.0.0'

print(get_project_version())
```

## TOML 쓰기 (외부 라이브러리)

```python
# pip install tomli-w
import tomli_w

config = {
    'title': 'My Application',
    'database': {
        'host': 'localhost',
        'port': 5432
    }
}

# 파일로 저장
with open('config.toml', 'wb') as f:  # 바이너리 모드
    tomli_w.dump(config, f)

# 문자열로 변환
toml_string = tomli_w.dumps(config)
print(toml_string)
```

## Py3.10 이하에서 TOML 사용

```python
# pip install tomli (읽기)
# pip install tomli-w (쓰기)

try:
    import tomllib  # Py3.11+
except ImportError:
    import tomli as tomllib  # Py3.10 이하

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
```

## 자주 하는 실수/주의점

### configparser (INI)
- **모든 값이 문자열**: `getint()`, `getboolean()` 등으로 변환 필요
- **대소문자 구분 안 함**: 키 이름이 소문자로 변환됨
- **섹션 필수**: `[section]` 없이 키만 있으면 에러 (또는 DEFAULT 사용)

### tomllib (TOML)
- **읽기 전용**: 쓰기는 `tomli-w` 사용
- **바이너리 모드 필수**: `open(..., 'rb')` 사용
- **Py3.11+ 전용**: 이전 버전은 `tomli` 패키지 설치

### INI vs TOML

| 특성 | INI | TOML |
|------|-----|------|
| 타입 | 모두 문자열 | 타입 보존 (int, bool 등) |
| 중첩 | 제한적 | 자유로움 |
| 배열 | 지원 안 함 | 지원 |
| 표준 | 비공식 | 공식 스펙 있음 |
| 용도 | 단순 설정 | pyproject.toml, 복잡한 설정 |

## 관련 링크(공식 문서)

- [configparser — Configuration file parser](https://docs.python.org/3/library/configparser.html)
- [tomllib — Parse TOML files](https://docs.python.org/3/library/tomllib.html)
- [TOML Spec](https://toml.io/)
