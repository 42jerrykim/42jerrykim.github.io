---
draft: true
title: "25. 패키징과 배포"
description: "패키징과 배포를 도구 나열이 아니라 표준과 선택 기준으로 정리합니다. pyproject.toml, wheel/sdist, 의존성 범위/고정, CI 배포 흐름과 흔한 함정을 함께 다룹니다."
tags:
  - python
  - Python
  - 파이썬
  - programming
  - 프로그래밍
  - software-engineering
  - 소프트웨어공학
  - computer-science
  - 컴퓨터과학
  - backend
  - 백엔드
  - development
  - 개발
  - best-practices
  - 베스트프랙티스
  - clean-code
  - 클린코드
  - refactoring
  - 리팩토링
  - testing
  - 테스트
  - debugging
  - 디버깅
  - logging
  - 로깅
  - security
  - 보안
  - performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - data-structures
  - 자료구조
  - algorithms
  - 알고리즘
  - standard-library
  - 표준라이브러리
  - packaging
  - 패키징
  - deployment
  - 배포
  - architecture
  - 아키텍처
  - design-patterns
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - ci-cd
  - 자동화
  - documentation
  - 문서화
  - git
  - 버전관리
  - tooling
  - 개발도구
  - code-quality
  - 코드품질
lastmod: 2026-01-17
collection_order: 25
---
# 챕터 25: 패키징과 배포 전략

파이썬에서 “패키징(packaging)”은 코드를 **설치 가능한 형태로 만드는 일**, “배포(deployment)”는 그 결과물을 **운영 환경에 안정적으로 전달하고 실행하는 일**입니다. 이 챕터는 도구 나열이 아니라, **무엇을 왜 선택하는지**(표준/트레이드오프/실무 함정)를 중심으로 정리합니다.

## 학습 목표
- 파이썬 패키지의 구조와 표준을 이해할 수 있다
- 패키지를 빌드하고 배포할 수 있다
- 의존성을 효과적으로 관리할 수 있다
- 배포 자동화와 버전 관리를 구현할 수 있다

## 핵심 개념(이론)

### 1) 패키징과 배포의 역할과 경계
이 챕터의 핵심은 “무엇을 할 수 있나”가 아니라, **어떤 문제를 해결하고 어디까지 책임지는지**를 분명히 하는 것입니다.
경계가 흐리면 코드는 커질수록 결합이 늘어나고 수정 비용이 커집니다.

### 2) 왜 이 개념이 필요한가(실무 동기)
실무에서는 예외 상황, 성능, 협업, 테스트가 항상 문제를 만듭니다.
따라서 이 주제는 기능이 아니라 **품질(신뢰성/유지보수성/보안)**을 위한 기반으로 이해해야 합니다.

### 3) 트레이드오프: 간단함 vs 확장성
대부분의 선택은 “더 단순하게”와 “더 확장 가능하게” 사이에서 균형을 잡는 일입니다.
초기에는 단순함을, 장기 운영/팀 협업이 커질수록 확장성을 더 우선합니다.

### 4) 실패 모드(Failure Modes)를 먼저 생각하라
무엇이 실패하는지(입력, I/O, 동시성, 외부 시스템)를 먼저 떠올리면 설계가 안정적으로 변합니다.
이 챕터의 예제는 실패 모드를 축소해서 보여주므로, 실제 적용 시에는 더 많은 방어가 필요합니다.

### 5) 학습 포인트: 외우지 말고 “판단 기준”을 남겨라
핵심은 API를 외우는 것이 아니라, “언제 무엇을 선택할지” 판단 기준을 정리하는 것입니다.
이 기준이 쌓이면 새로운 라이브러리/도구가 나와도 빠르게 적응할 수 있습니다.

## 선택 기준(Decision Guide)
- 기본은 **가독성/명확성** 우선(최적화는 측정 이후).
- 외부 의존이 늘수록 **경계/추상화**와 **테스트**를 먼저 강화.
- 복잡도가 증가하면 “규칙을 코드로”가 아니라 “구조로” 담는 방향을 고려.

## 흔한 오해/주의점
- 도구/문법이 곧 실력이라는 오해가 있습니다. 실력은 문제를 단순화하고 구조화하는 능력입니다.
- 극단적 최적화/과설계는 학습과 유지보수를 방해할 수 있습니다.

## 요약
- 패키징과 배포는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 핵심 내용

### 패키징에서 반드시 이해해야 하는 5가지
- **배포 형식 2가지**: `sdist`(소스 배포)와 `wheel`(빌드된 배포). 실무에서는 보통 둘 다 만들어 배포합니다.
- **표준 설정 파일**: `pyproject.toml`는 “이 프로젝트를 어떻게 빌드할지”를 정의하는 현대 표준입니다. (가능하면 `setup.py`는 최소화)
- **설치 방식**: 개발 중에는 `pip install -e .`(editable install)로 “소스 수정 → 즉시 반영” 흐름을 씁니다.
- **의존성의 두 얼굴**: “추상 의존성(>=)”과 “고정 의존성(lock)”은 목적이 다릅니다.
- **버전 전략**: 버전은 숫자가 아니라 “호환성 계약”입니다. (SemVer를 맹신하기보다, 공개 API 범위를 명확히)

### 언제 무엇을 선택할까?
| 상황 | 추천 | 이유 |
|---|---|---|
| 라이브러리 배포(Python 패키지) | `pyproject.toml` 기반 빌드(`build` + `twine`) | 표준 흐름, CI와 결합 쉬움 |
| 앱(서비스) 배포 | 패키지 배포보다 **컨테이너/이미지 배포**(예: Docker) | 실행환경까지 고정해야 안정적 |
| 팀 개발 | “추상 의존성 + lock 파일” | 재현성(같은 환경) 확보 |
| 교육/소규모 스크립트 | `requirements.txt` | 단순하고 빠름 |

### 표준 프로젝트 레이아웃(예시)
`src/` 레이아웃은 import 경로 실수를 줄이고, 패키징/테스트를 깔끔하게 만듭니다.

```text
my_pkg/
  pyproject.toml
  README.md
  src/
    my_pkg/
      __init__.py
      cli.py
      core.py
  tests/
    test_core.py
```

### `pyproject.toml` 최소 예시(라이브러리 + CLI)

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-pkg"
version = "0.1.0"
description = "Example package"
readme = "README.md"
requires-python = ">=3.10"
dependencies = ["requests>=2.31,<3"]

[project.scripts]
my-pkg = "my_pkg.cli:main"
```

### 빌드/배포 기본 명령(표준 흐름)

```bash
# 빌드 산출물 생성(sdist + wheel)
python -m pip install --upgrade build
python -m build

# TestPyPI에 먼저 올려 설치 검증
python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*

# 설치 테스트(별도 venv 권장)
python -m pip install -i https://test.pypi.org/simple/ my-pkg
```

### 자주 하는 실수/주의점
- **`setup.py`만 믿기**: 최신 생태계는 `pyproject.toml` 중심으로 이동했습니다. (도구 호환/CI 구성도 유리)
- **의존성 범위를 너무 빡빡/너무 넓게**: `requests==x.y.z` 고정은 재현성엔 좋지만 호환성엔 취약합니다. 라이브러리는 보통 범위를 둡니다.
- **앱을 PyPI로 배포하려는 습관**: 앱 배포는 “설치”보다 “운영”이 핵심이므로, 환경 고정이 가능한 방식(컨테이너 등)이 더 적합합니다.
- **비밀키/환경변수 누출**: 빌드 산출물/로그/CI 설정에 토큰이 들어가지 않도록 분리하세요.

## 실습 프로젝트
1. 유틸리티 라이브러리 패키징
2. CLI 도구 배포
3. 웹 프레임워크 플러그인
4. 자동화된 배포 파이프라인

## 체크리스트
- [ ] 패키지 구조 이해
- [ ] 빌드 도구 활용
- [ ] PyPI 배포 경험
- [ ] 의존성 관리 능력
- [ ] 배포 자동화 구축

## 다음 단계
패키징과 배포를 마스터했다면, 소프트웨어 설계 패턴과 아키텍처를 학습합니다. 
