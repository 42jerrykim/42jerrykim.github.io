---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 15. venv & pip - 환경/의존성 기본"
slug: "venv-and-pip-virtualenv-packaging-dependency-dependencies-lockfile-ci"
description: "가상환경과 패키지 설치를 빠르게 정리하는 치트시트입니다. venv 생성/활성화, pip install/upgrade, requirements.txt 관리, 재현 가능한 설치 습관과 흔한 환경 꼬임을 최소 체크리스트로 정리합니다."
lastmod: 2026-01-17
collection_order: 15
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - venv
  - virtualenv
  - 가상환경
  - pip
  - packaging
  - 패키징
  - dependency
  - dependencies
  - 의존성
  - requirements.txt
  - lockfile
  - pyproject
  - build
  - wheel
  - install
  - upgrade
  - uninstall
  - pythonpath
  - sys.path
  - environment
  - 환경
  - reproducible
  - 재현성
  - windows
  - powershell
  - macos
  - linux
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - troubleshooting
  - 트러블슈팅
  - stdlib
  - 표준라이브러리
  - security
  - 보안
  - supply-chain
  - ci
  - cd
  - automation
  - 자동화
  - testing
  - 테스트
---
가상환경과 의존성 관리는 재현 가능한 개발 환경의 기본입니다. 이 치트시트는 venv 생성/활성화, pip 설치, requirements.txt 관리의 핵심 체크리스트를 정리합니다.

## 언제 이 치트시트를 보나?

- “왜 내 컴퓨터에서는 되지?” 환경 차이로 깨질 때
- 프로젝트마다 의존성이 달라 충돌할 때

## 핵심 패턴

- 프로젝트마다 가상환경을 분리: `python -m venv .venv`
- 설치는 가상환경 안에서: `python -m pip install ...`
- 재현성: `requirements.txt`(또는 pyproject 기반)로 의존성 관리

## 최소 예제

```bash
# venv 생성
python -m venv .venv
```

```bash
# (Windows PowerShell) 활성화
.\\.venv\\Scripts\\Activate.ps1
```

```bash
# pip 업그레이드 + 설치
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 자주 하는 실수/주의점

- `pip` 대신 `python -m pip`를 습관화하면 “다른 파이썬에 설치” 실수를 줄일 수 있음
- 전역 설치(시스템 Python)에 깔아두면 프로젝트 간 충돌이 생김 → 가상환경 사용
- 환경이 꼬일 때는 “현재 python이 누구인지”부터 확인(경로/버전)

## 관련 링크(공식 문서)

- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Installing Python Modules](https://docs.python.org/3/installing/index.html)

