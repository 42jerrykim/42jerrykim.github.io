---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 62. Packaging - pyproject.toml/배포 체크리스트"
slug: "advanced-package-distribution-pyproject-toml-pypi-guide"
description: "파이썬 패키지 배포를 빠르게 시작하기 위한 치트시트입니다. pyproject.toml 구조, build/twine으로 PyPI 배포, 의존성 명세, 엔트리포인트, 배포 전 체크리스트를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 62
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - packaging
  - 패키징
  - pyproject.toml
  - pyproject
  - setup.py
  - setuptools
  - build
  - twine
  - wheel
  - sdist
  - distribution
  - 배포
  - PyPI
  - TestPyPI
  - publish
  - 퍼블리시
  - upload
  - dependencies
  - 의존성
  - optional-dependencies
  - extras
  - entry-points
  - 엔트리포인트
  - console-scripts
  - CLI
  - version
  - 버전
  - metadata
  - 메타데이터
  - license
  - 라이선스
  - readme
  - classifiers
  - pip
  - install
  - editable
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - checklist
  - 체크리스트
  - standard-library
  - 표준라이브러리
  - ci
  - cd
  - automation
  - 자동화
---
파이썬 패키지 배포는 pyproject.toml 기반이 표준입니다. 이 치트시트는 pyproject.toml 구조, build + twine으로 PyPI 배포, 의존성 명세, 배포 전 체크리스트를 정리합니다.

## 언제 이 치트시트를 보나?

- 내가 만든 라이브러리를 **pip install**로 설치 가능하게 만들고 싶을 때
- PyPI에 패키지를 **배포**하고 싶을 때

## 핵심 패턴

- 설정 파일: `pyproject.toml` (PEP 517/518/621 표준)
- 빌드: `python -m build` → `dist/` 폴더에 wheel + sdist 생성
- 업로드: `twine upload dist/*`
- 개발 모드 설치: `pip install -e .`

## pyproject.toml 기본 구조

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
requires-python = ">=3.8"

# 의존성
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

# 선택적 의존성 (pip install my-package[dev])
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black",
    "mypy",
]

# CLI 엔트리포인트
[project.scripts]
my-cli = "my_package.cli:main"

[project.urls]
Homepage = "https://github.com/you/my-package"
Documentation = "https://my-package.readthedocs.io"
```

## 빌드 및 배포

```bash
# 필요 도구 설치
pip install build twine

# 빌드 (dist/ 폴더 생성)
python -m build

# TestPyPI에 먼저 테스트 업로드
twine upload --repository testpypi dist/*

# TestPyPI에서 설치 테스트
pip install --index-url https://test.pypi.org/simple/ my-package

# 실제 PyPI 업로드
twine upload dist/*
```

## 개발 모드 설치

```bash
# 소스 코드 변경이 바로 반영됨
pip install -e .

# 선택적 의존성 포함
pip install -e ".[dev]"
```

## 프로젝트 구조 예시

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
└── tests/
    └── test_core.py
```

```toml
# src 레이아웃 사용 시 추가 설정
[tool.setuptools.packages.find]
where = ["src"]
```

## 배포 전 체크리스트

- [ ] `pyproject.toml`의 **version** 업데이트
- [ ] **README.md** 최신 상태 확인
- [ ] **LICENSE** 파일 존재
- [ ] `python -m build` 성공
- [ ] 로컬에서 `pip install dist/*.whl` 테스트
- [ ] TestPyPI에 먼저 업로드 후 설치 테스트
- [ ] Git tag 생성 (`git tag v0.1.0`)
- [ ] PyPI 업로드

## 자주 하는 실수/주의점

- **패키지 이름 충돌**: PyPI에 이미 있는 이름은 사용 불가 → 먼저 검색
- **버전 형식**: [PEP 440](https://peps.python.org/pep-0440/) 준수 (예: `1.0.0`, `1.0.0a1`)
- `__init__.py` 없으면 패키지로 인식 안 됨
- `MANIFEST.in` 또는 `pyproject.toml`의 `include`로 데이터 파일 포함 필요
- PyPI 업로드 후에는 **같은 버전 덮어쓰기 불가** → 새 버전으로 올려야 함

## 관련 링크(공식 문서)

- [Python Packaging User Guide](https://packaging.python.org/)
- [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [Twine](https://twine.readthedocs.io/)
