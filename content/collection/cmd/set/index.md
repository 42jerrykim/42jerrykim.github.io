---
draft: true
title: "[CMD] set - 환경 변수 표시 및 설정"
description: "set 명령어는 Windows CMD에서 환경 변수를 표시하거나, 새 변수를 만들고 값을 할당할 때 사용합니다. 배치 파일에서 변수 사용, /p 사용자 입력, 치환 문법을 정리합니다."
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

set은 Windows 명령 프롬프트(CMD)에서 환경 변수를 표시하거나, 새 환경 변수를 만들고 값을 할당할 때 사용하는 내장 명령어이다. 배치 파일에서 변수 사용, 사용자 입력 받기(/p), 문자열 치환 등에 쓰인다.

## 사용법

```
set [변수=[문자열]]]
set /p 변수=[프롬프트문자열]
set /a 식
```

## 옵션

| 옵션 | 설명 |
|------|------|
| (없음) | 모든 환경 변수 표시 |
| `변수=값` | 변수에 값 할당. 값이 비면 변수 삭제 |
| `/p 변수=` | 사용자 입력을 변수에 저장. 선택적으로 프롬프트 문자열 지정 |
| `/a 식` | 수식 계산 후 결과를 변수에 저장 |

## 예시

```
set
set MYVAR=Hello
set /p name=Enter your name:
set /a result=10+20
echo %PATH%
```

## 주의사항

- 변수 참조는 `%변수명%`이다. setlocal/endlocal 안에서는 지역 변수로 동작할 수 있다.
- `/a`에서 연산자 우선순위와 괄호를 지원한다. 나머지 연산은 `%` 대신 `%%`로 쓴다.
- 등호 주변 공백은 값에 포함될 수 있으므로 주의한다.
