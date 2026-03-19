---
draft: true
title: "[CMD] call - 다른 배치 파일 호출"
description: "call 명령어는 Windows CMD 배치 파일에서 다른 배치 파일을 호출한 뒤 제어를 돌려받을 때 사용합니다. 레이블 호출, 인수 전달, exit /b와의 차이를 정리합니다."
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

call은 Windows 명령 프롬프트(CMD) 배치 파일에서 다른 배치 파일(.bat, .cmd)이나 같은 배치 파일 내의 레이블을 서브루틴처럼 호출한 뒤, 실행이 끝나면 호출한 위치로 제어가 돌아오도록 할 때 사용하는 내장 명령어이다.

## 사용법

```
call [드라이브:][경로]배치파일 [배치인수]
call :레이블 [인수]
```

## 옵션

- 다른 배치 파일을 호출할 때는 경로와 파일 이름, 필요하면 인수를 넘긴다.
- 같은 파일 내 레이블을 호출할 때는 `:레이블` 형식으로 쓰고, 인수는 공백으로 구분해 넘긴다.

## 예시

```
call other.bat
call scripts\setup.cmd arg1 arg2
call :subroutine 100
```

## 주의사항

- call 없이 `other.bat`만 실행하면 현재 배치가 끝나고 other.bat으로 제어가 넘어가며, other.bat이 끝난 뒤에는 호출한 배치로 돌아오지 않는다. 돌아오려면 반드시 call을 쓴다.
- 호출된 배치에서 exit /b [코드]를 쓰면 호출한 쪽으로 종료 코드를 넘길 수 있다.
