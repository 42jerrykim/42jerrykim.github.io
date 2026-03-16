---
image: "wordcloud.png"
title: "[RPM] Spec 파일에서 주석과 매크로 동시 사용 시 주의사항"
description: "RPM Spec 파일에서 주석(#)과 매크로(%define 등)를 함께 쓸 때 매크로가 먼저 확장되어 주석이 무시되는 동작 원리, 오동작 사례, %% 이스케이프를 이용한 올바른 사용법과 실무 체크리스트를 정리한 가이드. RPM 패키징·빌드 담당자와 DevOps 실무 참고용."
categories:
  - RPM
date: "2021-11-24T00:00:00Z"
lastmod: "2026-03-16"
tags:
  - Linux
  - 리눅스
  - Shell
  - 셸
  - Bash
  - Configuration
  - 설정
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Reference
  - 참고
  - Best-Practices
  - Documentation
  - 문서화
  - Open-Source
  - 오픈소스
  - Troubleshooting
  - 트러블슈팅
  - How-To
  - Tips
  - Deployment
  - 배포
  - DevOps
  - Pitfalls
  - 함정
  - Error-Handling
  - 에러처리
  - Debugging
  - 디버깅
  - Code-Quality
  - 코드품질
  - Readability
  - Maintainability
  - Automation
  - 자동화
  - Technology
  - 기술
  - Education
  - 교육
  - Beginner
  - Implementation
  - 구현
  - Edge-Cases
  - 엣지케이스
  - Clean-Code
  - 클린코드
  - Performance
  - 성능
  - Terminal
  - 터미널
  - Comparison
  - 비교
  - Case-Study
  - Deep-Dive
  - 실습
  - Workflow
  - 워크플로우
  - Productivity
  - 생산성
  - Migration
  - 마이그레이션
  - Networking
  - 네트워킹
  - YAML
  - File-System
  - OS
  - 운영체제
  - Git
  - GitHub
  - IDE
  - Markdown
  - 마크다운
  - Testing
  - 테스트
  - Docker
  - Kubernetes
  - Ansible
  - CI-CD
  - Monitoring
  - 모니터링
  - Web
  - 웹
  - Blog
  - 블로그
  - Review
  - 리뷰
  - Quick-Reference
  - Cheatsheet
  - 치트시트
  - Innovation
  - 혁신
  - Career
  - 커리어
  - Cloud
  - 클라우드
  - Hardware
  - 하드웨어
  - Agile
  - 애자일
  - Refactoring
  - 리팩토링
  - Code-Review
  - 코드리뷰
  - Design-Pattern
  - 디자인패턴
  - Software-Architecture
  - 소프트웨어아키텍처
  - Modularity
  - Security
  - 보안
  - API
  - Backend
  - 백엔드
  - Database
  - 데이터베이스
  - JSON
  - XML
  - HTTP
  - REST
  - Caching
  - 캐싱
  - Scalability
  - 확장성
  - Concurrency
  - 동시성
  - Async
  - 비동기
  - Memory
  - 메모리
  - Compiler
  - 컴파일러
  - Process
  - Thread
  - IO
  - Logging
  - 로깅
  - Profiling
  - 프로파일링
  - Benchmark
  - Type-Safety
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
  - Abstraction
  - 추상화
draft: false
---

RPM 패키지를 빌드할 때 사용하는 **Spec 파일**에서는 주석(`#`)과 **매크로**(`%define`, `%macro` 등)를 함께 쓰는 경우가 많다. 이때 "이 줄은 주석이니까 무시될 것"이라고 생각하고 `# %define ...`처럼 적으면, 실제로는 매크로가 먼저 확장되어 주석이 무시되고 예상과 다른 빌드 결과가 나올 수 있다. 이 글은 그 동작 원리, 오동작 사례, 그리고 **%%** 이스케이프를 이용한 올바른 사용법까지 정리한다.

## 왜 이 주제인가

Spec 파일을 수정하거나 조건부 매크로를 켜고 끌 때, "주석 처리한 줄은 실행되지 않는다"는 일반적인 스크립트 경험을 그대로 적용하기 쉽다. 그러나 Spec 파일은 **매크로 확장이 먼저** 이루어진 뒤에 줄 단위로 주석이 적용되는 전처리 모델을 사용한다. 이 순서를 모르면 디버깅이 어렵고, 패키징 실수로 이어질 수 있어, 동작 원리와 대응 방법을 명확히 하는 것이 중요하다.

## 정의와 원칙

- **RPM**: Red Hat Package Manager. 리눅스에서 소프트웨어를 패키지 형태로 설치·제거·조회하는 도구이다.
- **Spec 파일**: RPM 패키지의 메타데이터, 빌드 절차, 설치 경로 등을 정의하는 스크립트형 설정 파일이다. 확장자는 보통 `.spec`이다.
- **주석**: Spec 파일에서 줄 맨 앞에 `#`를 두면 그 줄은 주석으로 간주되어 빌드 시 해석 대상에서 제외된다.
- **매크로**: `%define 이름 값` 또는 `%macro 이름 ...` 형태로 정의되며, `%이름` 또는 `%{이름}`으로 참조된다. **매크로 확장은 파서가 줄을 해석하는 단계에서 먼저** 일어나며, 그 다음에 주석 제거가 적용된다. 따라서 한 줄에 `#`와 매크로 정의가 함께 있더라도, 매크로가 먼저 처리되면 `#` 뒤의 `%define` 등이 실행될 수 있다.

아래는 Spec 파서의 처리 순서를 요약한 것이다.

```mermaid
flowchart LR
  specInput["Spec 파일 입력"]
  macroExpand["매크로 확장</br>(%define 등)"]
  commentStrip["줄 단위 주석 제거</br>(# 로 시작하는 줄)"]
  finalResult["최종 전처리 결과"]
  specInput --> macroExpand --> commentStrip --> finalResult
```

즉, "주석으로 보이는 줄"이라도 그 줄 안에 매크로 문법이 있으면 **매크로 단계에서 먼저 확장**되고, 그 결과가 남은 뒤에 주석 처리 여부가 결정된다. 그래서 `## %define TEST enable`처럼 `#`를 두 개 써도, 첫 번째 `#`는 일반 문자로 남고 두 번째 `%`부터 매크로로 해석될 수 있어, 결국 `%define TEST enable`가 실행되는 식의 오동작이 발생한다.

## 오동작 예시

의도는 "`TEST`를 disable로 두고, enable로 바꾼 줄은 주석 처리해서 무시하기"인데, 실제로는 주석으로 보이는 줄까지 매크로가 실행되는 전형적인 사례다.

### 잘못된 샘플 코드

```spec
%define TEST disable
## %define TEST enable

echo %TEST
```

첫 줄에서 `TEST`는 `disable`로 정의된다. 두 번째 줄은 사람 눈에는 "주석"으로 보이지만, Spec 파서는 **매크로 확장 단계**에서 `## %define TEST enable`를 처리할 때 `%define TEST enable`를 실행한다. 그 결과 `TEST`가 `enable`로 다시 정의되고, `echo %TEST`는 `enable`를 출력하게 된다.

### 실제 결과

```text
enable
```

즉, "주석이라 무시될 줄"에서 `%define`가 실행되어 `disable`이 아닌 `enable`이 출력된다.

## 이유 정리

Spec에서 주석은 **줄 맨 앞의 `#`**로 표시하는 것이 맞다. 다만 **처리 순서**가 "매크로 확장 → 주석 제거"이기 때문에, 같은 줄에 `#`와 매크로 문법이 함께 있으면 매크로가 먼저 동작한다. `## %define ...`처럼 `#`를 두 개 적어도, 첫 번째 `#`만으로는 그 줄 전체가 주석으로 인식되기 전에 매크로 토큰이 처리될 수 있다.

매크로를 **진짜로 주석 처리**하려면, 매크로 쪽을 이스케이프해서 파서가 매크로로 인식하지 않게 해야 한다. **`%`를 두 번 써서 `%%`로 쓰면**, 한 개의 `%` 문자로 치환되므로 `%define`가 매크로 정의로 해석되지 않는다.

## 올바른 사용법

주석 안에서 매크로 정의를 완전히 비활성화하려면 `%define` 앞의 `%`를 이스케이프한다.

### 수정된 샘플 코드

```spec
%define TEST disable
# %%define TEST enable

echo %TEST
```

`# %%define TEST enable`에서는 `%%`가 하나의 `%`로 확장된 뒤, `# % define TEST enable`처럼 해석될 수 있는 형태가 되거나, 최소한 `%define`라는 매크로 키워드로 인식되지 않는다. 이렇게 하면 두 번째 줄은 주석으로만 처리되고, `TEST`는 `disable`로 유지된다.

### 기대 결과

```text
disable
```

## 비교 요약

| 구분 | 잘못된 작성 | 올바른 작성 |
|------|-------------|-------------|
| 주석 처리 의도 줄 | `## %define TEST enable` | `# %%define TEST enable` |
| 매크로 확장 여부 | `%define`가 실행됨(오동작) | `%define`로 인식되지 않음(주석 유지) |
| `echo %TEST` 결과 | `enable` | `disable` |
| 사용 원칙 | `#`만으로는 매크로 비활성화 불가 | `%%`로 `%` 이스케이프 후 주석 처리 |

## 언제 이 방법을 쓰고, 언제 피할지

- **사용하는 경우**: Spec 파일에서 조건부로 매크로 정의를 켜거나 끄면서, "지금은 사용하지 않는 정의"를 주석으로 남기고 싶을 때. 기존 `%define` 줄을 주석 처리할 때는 반드시 `# %%define ...` 형태로 `%`를 이스케이프한다.
- **피하는 경우**: 단순 설명용 주석에는 `%`가 없으므로 `#`만 사용하면 된다. 매크로가 전혀 없는 줄을 주석 처리할 때 `%%`를 붙일 필요는 없다.
- **대안**: 아예 해당 줄을 삭제하거나, 매크로 이름을 바꿔서 사용하지 않는 정의(예: `%define TEST_DISABLED enable`)로 두고, 실제로 쓰는 매크로만 한 곳에서 정의하는 방식도 있다. 주석으로 남기고 싶다면 `# %%define ...`가 안전하다.

## 실무 체크리스트

Spec 파일을 수정·리뷰할 때 아래를 확인하면 오동작을 줄일 수 있다.

- [ ] `#` 뒤에 `%define`, `%global`, `%macro` 등 매크로 정의가 오는 줄이 있는가? 있다면 `%`를 `%%`로 이스케이프했는가?
- [ ] 조건부로 켜는/끄는 매크로를 주석으로 "비활성화"했다고 가정하지 말고, 실제 빌드 결과(`rpmbuild` 또는 `%TEST` 출력 등)로 확인했는가?
- [ ] Spec 파일 내 매크로 확장 순서를 의식하고 있는가? (매크로 확장 → 주석 제거 순서)

## 이 글을 읽은 후 할 수 있는 일

- Spec 파일에서 주석(`#`)과 매크로가 **처리되는 순서**(매크로 확장 먼저, 그 다음 주석)를 설명할 수 있다.
- `## %define ...`가 의도대로 주석으로 동작하지 않는 이유를 말할 수 있다.
- 매크로를 주석으로 비활성화할 때 `# %%define ...`처럼 `%%`를 사용해 올바르게 작성할 수 있다.
- Spec 파일 리뷰 시 "주석처럼 보이는 줄에 매크로가 있는지"를 확인할 수 있다.

## 참고

- RPM 및 Spec 파일 문법은 Fedora Packagers Guide의 Spec File Reference(Comments 섹션) 등에서 다룬다. 매크로 확장과 주석 처리 순서에 대한 공식 설명은 해당 문서를 참고하면 된다.
- 동일한 원리가 `%global`, `%macro` 등 다른 매크로 정의에도 적용된다. 주석 처리 시 `%`는 `%%`로 이스케이프하는 것을 원칙으로 두면 된다.
