---
draft: true
title: "[CMD] shutdown - 시스템 종료·재부팅·로그오프"
description: "shutdown 명령어는 Windows CMD에서 로컬 또는 원격 컴퓨터를 종료, 재시작, 로그오프할 때 사용합니다. /s 종료, /r 재시작, /t 지연 초, /a 중단, 예약 종료 방법을 정리합니다."
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

shutdown은 Windows 명령 프롬프트(CMD)에서 로컬 또는 원격 컴퓨터를 종료(/s), 재시작(/r), 로그오프(/l)할 때 사용하는 명령어이다. 지연 시간(/t), 취소(/a), 이유 코드(/d) 등을 지정할 수 있다.

## 사용법

```
shutdown [/i | /l | /s | /r | /g | /a | /p | /h | /e] [/f] [/m \\컴퓨터] [/t 초] [/d [p|u:]주요:부차] [/c "메시지"]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/s` | 컴퓨터 종료 |
| `/r` | 컴퓨터 재시작 |
| `/l` | 로그오프(현재 사용자) |
| `/t 초` | 지정한 초 후에 수행(기본 30). 0이면 즉시 |
| `/f` | 실행 중인 응용 프로그램을 강제 종료 |
| `/a` | 예약된 종료/재시작 취소 |
| `/c "메시지"` | 종료 이유 메시지(최대 512자) |

## 예시

```
shutdown /s /t 60
shutdown /r /f /t 0
shutdown /a
shutdown /s /m \\server01 /t 0
```

## 주의사항

- 종료/재시작은 보통 관리자 권한이 필요하다.
- `/t`로 지연을 두면 그 사이에 `shutdown /a`로 취소할 수 있다.
