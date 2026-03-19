---
draft: true
title: "[CMD] if - 배치 파일 조건 분기"
description: "if 명령어는 Windows CMD 배치 파일에서 조건에 따라 명령을 실행하거나 건너뛸 때 사용합니다. ERRORLEVEL, 문자열 비교, 파일·디렉터리 존재 검사, not 연산을 정리합니다."
date: 2025-03-15
lastmod: 2025-03-15
categories: CMD
image: "wordcloud.png"
tags:
- Windows
- 윈도우
- Shell
- 셸
- Terminal
- 터미널
- OS
- 운영체제
- Technology
- 기술
- Tutorial
- 튜토리얼
- Guide
- 가이드
- Reference
- 참고
- How-To
- Tips
- Best-Practices
- Documentation
- 문서화
- Beginner
- Advanced
- Automation
- 자동화
- Deployment
- 배포
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- Education
- 교육
- Comparison
- 비교
- Productivity
- 생산성
- Workflow
- 워크플로우
- Web
- 웹
- Blog
- 블로그
- Markdown
- 마크다운
- DevOps
- Git
- GitHub
- Linux
- 리눅스
- Monitoring
- 모니터링
- Backend
- 백엔드
- Security
- 보안
- Implementation
- 구현
- Clean-Code
- 클린코드
---

if는 Windows 명령 프롬프트(CMD) 배치 파일에서 조건이 참인지 거짓인지에 따라 다른 명령을 실행할 때 사용하는 내장 명령어이다. ERRORLEVEL 검사, 문자열 비교, 파일·디렉터리 존재 여부 확인 등을 지원한다.

## 사용법

```
if [not] errorlevel 숫자 명령
if [not] 문자열1==문자열2 명령
if [not] exist 파일이름 명령
if [not] defined 변수 명령
if [not] 문자열1 compareop 문자열2 명령
```

## 옵션

- `errorlevel 숫자`: 마지막 프로그램 종료 코드가 숫자 이상이면 참.
- `문자열1==문자열2`: 문자열이 같으면 참. 변수는 `%변수%`로.
- `exist 경로`: 파일 또는 디렉터리가 있으면 참.
- `defined 변수`: 변수가 정의되어 있으면 참.
- `not`: 조건을 부정.

## 예시

```
if exist config.ini echo Found
if %errorlevel% neq 0 echo Error occurred
if defined MYVAR echo MYVAR is set
if not exist backup md backup
```

## 주의사항

- 문자열 비교 시 공백과 대소문자를 구분한다. 변수 값이 비어 있으면 문법 오류가 날 수 있으므로 `"%var%"==""` 형태로 따옴표를 쓰는 것이 안전하다.
- 여러 명령을 실행하려면 괄호로 묶는다: `if condition ( 명령1 & 명령2 )`.
