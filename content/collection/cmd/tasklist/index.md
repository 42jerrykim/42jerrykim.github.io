---
draft: true
title: "[CMD] tasklist - 실행 중인 프로세스 목록"
description: "tasklist 명령어는 Windows CMD에서 현재 실행 중인 프로세스(작업) 목록을 표시할 때 사용합니다. /v 상세 정보, /fi 필터, /m DLL, 서비스 포함 등 옵션을 정리합니다."
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

tasklist는 Windows 명령 프롬프트(CMD)에서 현재 시스템에서 실행 중인 프로세스(작업) 목록을 표시할 때 사용하는 명령어이다. 이미지 이름, PID, 메모리 사용량 등을 보여 주며, taskkill과 함께 프로세스 관리에 쓴다.

## 사용법

```
tasklist [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/fo 형식] [/nh] [/fi 필터] [/m [모듈]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/fo table|list|csv` | 출력 형식(테이블, 목록, CSV) |
| `/nh` | 테이블일 때 열 머리글 생략 |
| `/fi "필터"` | 조건에 맞는 프로세스만 표시 |
| `/v` | 상세 정보(창 제목, 상태 등) |
| `/m [모듈]` | 지정한 DLL을 사용하는 프로세스만, 또는 모듈 목록 |

## 예시

```
tasklist
tasklist /fi "imagename eq notepad.exe"
tasklist /v /fo list
tasklist /m ntdll.dll
```

## 주의사항

- 원격 컴퓨터를 조회할 때는 `/s`, `/u`, `/p`를 사용한다. 관리 권한이 필요할 수 있다.
- PID는 taskkill로 프로세스를 종료할 때 사용한다.
