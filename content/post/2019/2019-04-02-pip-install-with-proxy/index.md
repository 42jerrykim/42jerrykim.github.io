---
title: "[Tutorial] pip install 프록시 환경에서 사용하기"
description: "프록시 환경에서 pip으로 Python 패키지를 설치하는 방법을 정리합니다. pip install --proxy 옵션, HTTP_PROXY·HTTPS_PROXY 환경 변수, pip.conf 설정 파일 방식과 실전 예시·주의사항·FAQ를 담았으며, 개발·운영·CI 환경에서 바로 참고할 수 있도록 구성했습니다."
date: "2019-04-02T00:00:00Z"
lastmod: "2026-03-16T00:00:00Z"
categories:
- Tutorial
- Proxy
redirect_from:
- /2019/04/02/
tags:
- Python
- 파이썬
- pip
- Proxy
- Shell
- 셸
- Bash
- Terminal
- 터미널
- Flask
- Tutorial
- 튜토리얼
- Guide
- 가이드
- How-To
- Reference
- 참고
- Configuration
- 설정
- Networking
- 네트워킹
- Deployment
- 배포
- Troubleshooting
- 트러블슈팅
- Error-Handling
- 에러처리
- Documentation
- 문서화
- Best-Practices
- Workflow
- 워크플로우
- Open-Source
- 오픈소스
- Beginner
- Windows
- 윈도우
- Linux
- 리눅스
- macOS
- Automation
- 자동화
- DevOps
- Web
- 웹
- Backend
- 백엔드
- HTTP
- Security
- 보안
- Productivity
- 생산성
- Education
- 교육
- Technology
- 기술
- Tips
- Quick-Reference
- Cheatsheet
- 치트시트
- Migration
- 마이그레이션
- Case-Study
- 실습
- venv
- IDE
- VSCode
- Git
- GitHub
- Docker
- Cloud
- 클라우드
- API
- JSON
- YAML
- Markdown
- 마크다운
- Blog
- 블로그
- Comparison
- 비교
- Performance
- 성능
- Testing
- 테스트
- Debugging
- 디버깅
- Implementation
- 구현
- Clean-Code
- 클린코드
- Maintainability
- Code-Quality
- 코드품질
image: "wordcloud.png"
---

## 개요

회사·학교·공공망 등에서는 보안·정책상 외부 인터넷 접속이 **프록시(Proxy)** 를 통해서만 가능한 경우가 많다. 이때 터미널에서 `pip install`을 그대로 쓰면 PyPI에 연결되지 않아 패키지 설치가 실패한다. 이 글은 **프록시 환경에서 pip으로 Python 패키지를 설치하는 방법**을, 명령줄 옵션·환경 변수·설정 파일까지 포함해 정리한다.

**대상 독자**: 프록시/방화벽 뒤에서 Python 개발 환경을 쓰는 개발자, CI/CD·서버 배포 시 프록시 설정이 필요한 운영자.

---

## 사용법 (기본 문법)

`pip install`에 `--proxy` 옵션으로 프록시 URL을 주고, 그 뒤에 설치할 패키지 이름을 적는다.

**기본 형식:**

```bash
pip install --proxy [Proxy http url] [Package name]
```

프록시 URL은 `http://호스트:포트` 또는 `https://호스트:포트` 형태다. 인증이 필요하면 `http://사용자:비밀번호@호스트:포트` 형식을 사용할 수 있다(특수문자 포함 시 URL 인코딩 필요).

**실제 사용 예:**

```bash
pip install --proxy http://000.111.222.333:4444 Flask
```

위처럼 하면 해당 프록시를 경유해 PyPI에서 Flask와 의존성이 내려받아지고, 정상적으로 설치가 진행된다.

---

## 요청 흐름 (Mermaid)

프록시를 사용할 때 pip의 요청 경로는 다음과 같다.

```mermaid
flowchart LR
  subgraph clientEnv["클라이언트 환경"]
    Pip["pip install"]
  end
  subgraph netEnv["네트워크"]
    Proxy["프록시 서버"]
    PyPI["PyPI"]
  end
  Pip -->|"HTTP/HTTPS 요청"| Proxy
  Proxy -->|"전달"| PyPI
  PyPI -->|"패키지 응답"| Proxy
  Proxy -->|"응답"| Pip
```

- **노드 ID**: camelCase·PascalCase 사용, 예약어 미사용.
- **라벨**: 특수문자·등호가 있으면 큰따옴표로 감쌈. 줄바꿈은 `</br>` 사용.

---

## 옵션·대안 정리

프록시를 지정하는 방법은 크게 세 가지다. 우선순위는 **명령줄 옵션 > 환경 변수 > 설정 파일**이다.

### 1. 명령줄 옵션 `--proxy`

- **문법**: `pip install --proxy <프록시_URL> <패키지명>`
- **특징**: 한 번만 쓸 때, 스크립트에서 한 명령만 프록시를 쓰고 싶을 때 유리.
- **예**:  
  `pip install --proxy http://proxy.company.com:8080 requests`

### 2. 환경 변수

- **변수**: `HTTP_PROXY`, `HTTPS_PROXY` (대소문자 구분 없이 쓰는 구현이 많음).
- **설정 예 (Bash/Zsh):**
  ```bash
  export HTTP_PROXY=http://proxy.company.com:8080
  export HTTPS_PROXY=http://proxy.company.com:8080
  pip install Flask
  ```
- **Windows (PowerShell):**
  ```powershell
  $env:HTTP_PROXY="http://proxy.company.com:8080"
  $env:HTTPS_PROXY="http://proxy.company.com:8080"
  pip install Flask
  ```
- **특징**: 세션·쉘 전체에 적용되므로, 같은 터미널에서 여러 번 `pip install` 할 때 편하다.

### 3. 설정 파일 (pip.conf / pip.ini)

- **위치**: 사용자 설정은 `~/.config/pip/pip.conf`(Unix/macOS) 또는 `%APPDATA%\pip\pip.ini`(Windows). 가상환경은 `$VIRTUAL_ENV/pip.conf`.
- **예시:**
  ```ini
  [global]
  proxy = http://proxy.company.com:8080
  ```
- **특징**: 매번 옵션이나 환경 변수를 넣지 않아도 되며, 팀·서버 공통 설정으로 쓰기 좋다.

---

## 실전 예시

| 상황 | 명령 예시 |
|------|-----------|
| 단일 패키지, 프록시만 지정 | `pip install --proxy http://192.168.1.10:3128 Flask` |
| 인증 프록시 (URL 인코딩 필요) | `pip install --proxy http://user%40domain:pass%23@proxy:8080 requests` |
| requirements.txt 일괄 설치 | `pip install --proxy http://proxy:8080 -r requirements.txt` |
| 특정 버전 설치 | `pip install --proxy http://proxy:8080 "Django==4.2"` |
| 가상환경 활성화 후 (환경 변수 사용) | `export HTTPS_PROXY=http://proxy:8080` 후 `pip install -r requirements.txt` |
| Windows에서 한 줄로 | `set HTTP_PROXY=http://proxy:8080 && pip install Flask` |
| Python -m pip 사용 (권장) | `python -m pip install --proxy http://proxy:8080 Flask` |

---

## 주의사항·FAQ

- **인증이 있는 프록시**: URL에 `사용자:비밀번호`를 넣을 때 `@`, `#`, `:` 등은 퍼센트 인코딩해야 한다. 예: `@` → `%40`, `#` → `%23`.
- **SSL/HTTPS**: HTTPS로만 접속 가능한 PyPI를 쓸 때는 `HTTPS_PROXY` 또는 `--proxy`에 `https://` 프록시 URL을 지정하는 것이 안전하다. 인증서 오류가 나면 `trusted-host` 등은 공식 문서를 참고해 예외 처리한다.
- **타임아웃**: 프록시가 느리면 `pip install --proxy ... --timeout 120` 처럼 `--timeout`을 늘려 본다.
- **환경 변수 vs --proxy**: 같은 세션에서 여러 번 설치할 때는 환경 변수나 `pip.conf`로 두면 명령이 짧아진다.
- **CI/CD**: Jenkins, GitHub Actions 등에서는 해당 러너의 프록시 설정 또는 환경 변수로 `HTTP_PROXY`/`HTTPS_PROXY`를 설정한 뒤 `pip install`을 실행하면 된다.

---

## 참고 문헌

- [pip install - pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/) — 공식 사용법·옵션.
- [Configuration - pip documentation](https://pip.pypa.io/en/stable/topics/configuration/) — 설정 파일·환경 변수 우선순위.
- [Command line and environment — Python 3 documentation](https://docs.python.org/3/using/cmdline.html#environment-variables) — Python 실행 시 환경 변수.
