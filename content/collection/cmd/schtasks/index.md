---
draft: true
title: "[CMD] schtasks - 예약 작업"
description: "schtasks 명령어는 Windows CMD에서 예약된 작업(스케줄 작업)을 만들거나, 조회·실행·수정·삭제할 때 사용합니다. /create, /query, /run, /change, /delete, /tn 작업 이름을 정리합니다."
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

schtasks는 Windows 명령 프롬프트(CMD)에서 작업 스케줄러에 등록된 작업(예약 작업)을 만들거나, 조회·실행·수정·삭제할 때 사용하는 명령어이다. at 명령보다 기능이 많고, 트리거·동작·권한 등을 세밀하게 설정할 수 있다.

## 사용법

```
schtasks /create ...
schtasks /query [/fo 형식] [/v] [/tn 작업이름]
schtasks /run /tn 작업이름
schtasks /change /tn 작업이름 ...
schtasks /delete /tn 작업이름 [/f]
```

## 주요 옵션

- **/create**: 새 예약 작업 생성. /tn(이름), /tr(실행할 프로그램), /sc(일정: daily, weekly, onstart 등), /st(시작 시간), /ru(실행 사용자) 등
- **/query**: 작업 목록 또는 특정 작업 정보 표시
- **/run**: 작업을 즉시 한 번 실행
- **/change**: 작업 설정 변경
- **/delete**: 작업 삭제

## 예시

```
schtasks /query
schtasks /create /tn "Daily Backup" /tr "C:\Scripts\backup.bat" /sc daily /st 02:00
schtasks /run /tn "Daily Backup"
schtasks /delete /tn "OldTask" /f
```

## 주의사항

- 작업을 만들 때 /ru로 실행 계정을 지정하지 않으면 현재 사용자로 만들어진다. 시스템 계정으로 실행하려면 /ru System 등을 사용한다. 관리자 권한이 필요할 수 있다.
- at 명령은 레거시이며 schtasks 사용이 권장된다.
