---
draft: true
title: "[CMD] systeminfo - 시스템 정보 표시"
description: "systeminfo 명령어는 Windows CMD에서 컴퓨터의 하드웨어·OS·설치 날짜·부팅 시간 등 시스템 정보를 한 번에 표시할 때 사용합니다. 원격 컴퓨터 지정과 출력 형식 옵션을 정리합니다."
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

systeminfo는 Windows 명령 프롬프트(CMD)에서 현재 컴퓨터(또는 원격 컴퓨터)의 OS 이름, 버전, 제조사, 부팅 시간, 하드웨어 요약, 네트워크 어댑터 등 시스템 정보를 표시할 때 사용하는 명령어이다.

## 사용법

```
systeminfo [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/fo 형식] [/nh]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/s 컴퓨터` | 원격 컴퓨터 이름 또는 IP |
| `/u 도메인\사용자` | 원격 접속 시 사용자 |
| `/p 비밀번호` | 원격 접속 시 비밀번호 |
| `/fo table|list|csv` | 출력 형식 |
| `/nh` | 테이블 형식일 때 열 머리글 생략 |

## 예시

```
systeminfo
systeminfo /fo csv
systeminfo /s server01 /u DOMAIN\admin
```

## 주의사항

- 원격 컴퓨터를 조회하려면 해당 머신에 대한 권한과 방화벽·원격 설정이 허용되어 있어야 한다.
- 출력이 길어지면 `systeminfo | more` 또는 파일로 리다이렉트해 사용한다.
