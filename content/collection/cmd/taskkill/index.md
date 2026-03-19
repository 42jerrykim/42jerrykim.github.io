---
draft: true
title: "[CMD] taskkill - 프로세스 종료"
description: "taskkill 명령어는 Windows CMD에서 실행 중인 프로세스(응용 프로그램)를 PID 또는 이미지 이름으로 종료할 때 사용합니다. /f 강제 종료, /t 자식 프로세스 종료, /fi 필터를 정리합니다."
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

taskkill은 Windows 명령 프롬프트(CMD)에서 실행 중인 프로세스를 종료할 때 사용하는 명령어이다. 프로세스 ID(PID) 또는 이미지 이름(실행 파일 이름)으로 지정할 수 있으며, tasklist로 PID를 확인한 뒤 사용한다.

## 사용법

```
taskkill [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/fi 필터] [/pid PID | /im 이미지이름] [/f] [/t]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/pid PID` | 종료할 프로세스 ID |
| `/im 이미지이름` | 종료할 프로세스의 이미지 이름(예: notepad.exe) |
| `/f` | 강제 종료 |
| `/t` | 해당 프로세스와 그 자식 프로세스 모두 종료 |
| `/fi "필터"` | 조건에 맞는 프로세스만 대상 |

## 예시

```
taskkill /im notepad.exe
taskkill /pid 1234 /f
taskkill /im myapp.exe /f /t
taskkill /fi "windowtitle eq My Window*" /f
```

## 주의사항

- 시스템 프로세스나 다른 사용자 세션의 프로세스를 종료하려면 관리자 권한이 필요하다.
- `/f` 없이 보내면 프로세스에 종료 요청을 보내고, 응답하지 않으면 강제 종료는 하지 않는다. 데이터 손실을 줄이려면 먼저 `/f` 없이 시도하는 것이 좋다.
