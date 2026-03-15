---
draft: true
title: "[CMD] wmic - WMI 명령줄"
description: "wmic 명령어는 Windows CMD에서 WMI(Windows Management Instrumentation)를 명령줄로 조회·호출할 때 사용합니다. OS, CPU, 디스크, 프로세스, 서비스 등 시스템 정보와 설정을 가져올 수 있습니다. PowerShell CIM 권장."
date: 2025-03-15
lastmod: 2025-03-15
categories: CMD
image: "tmp_wordcloud.png"
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

wmic(Windows Management Instrumentation Command-line)는 Windows 명령 프롬프트(CMD)에서 WMI를 명령줄로 조회·호출할 때 사용하는 도구이다. OS, 프로세스, 디스크, 서비스, 환경 변수 등 광범위한 시스템 정보를 alias(간단한 이름)로 조회할 수 있다. 최신 Windows에서는 PowerShell의 Get-WmiObject, Get-CimInstance 사용이 권장된다.

## 사용법

```
wmic [글로벌옵션] alias [alias옵션] [where 절] [verb 절]
wmic /?
```

## 주요 alias

- **os**: 운영 체제 정보
- **cpu**: 프로세서 정보
- **diskdrive**: 디스크 드라이브
- **process**: 프로세스
- **service**: 서비스
- **environment**: 환경 변수
- **computersystem**: 컴퓨터 시스템 정보

## 예시

```
wmic os get caption,version
wmic process get name,processid
wmic diskdrive get size,caption
wmic service where "name='wuauserv'" get state
wmic /node:server01 os get caption
```

## 주의사항

- wmic는 Windows 10/11에서 deprecated(단종 예정)이며, PowerShell CIM cmdlet 사용이 권장된다. 기존 스크립트 호환을 위해 아직 사용 가능하다.
- 원격 조회 시 /node:컴퓨터, /user, /password 등이 필요할 수 있고, 방화벽·권한이 허용되어야 한다.
