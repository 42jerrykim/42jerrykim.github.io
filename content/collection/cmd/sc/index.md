---
draft: true
title: "[CMD] sc - 서비스 제어"
description: "sc 명령어는 Windows CMD에서 서비스(백그라운드 프로세스)를 조회·생성·시작·중지·삭제할 때 사용합니다. query, create, start, stop, delete, config 등으로 서비스를 관리합니다."
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

sc(Service Control)는 Windows 명령 프롬프트(CMD)에서 Windows 서비스를 조회·생성·설정·시작·중지·삭제할 때 사용하는 명령어이다. 원격 컴퓨터에 대한 작업도 가능하며, 관리자 권한이 필요한 경우가 많다.

## 사용법

```
sc [\\컴퓨터] 하위명령 [서비스이름] [옵션...]
```

## 주요 하위 명령

- **query**: 서비스 상태·목록 조회
- **qc**: 서비스 구성 조회
- **create**: 서비스 생성
- **start**: 서비스 시작
- **stop**: 서비스 중지
- **delete**: 서비스 삭제
- **config**: 서비스 설정 변경(시작 유형, 경로 등)

## 예시

```
sc query
sc query wuauserv
sc start wuauserv
sc stop wuauserv
sc config MyService start= auto
sc \\server01 query
```

## 주의사항

- 시스템 서비스를 잘못 중지하거나 삭제하면 부팅이나 동작에 문제가 생길 수 있다. 서비스 이름과 역할을 확인한 뒤 작업한다. 원격 제어 시 해당 컴퓨터에 대한 권한이 필요하다.
