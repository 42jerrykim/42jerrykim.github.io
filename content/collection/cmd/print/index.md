---
draft: true
title: "[CMD] print - 텍스트 파일 인쇄"
description: "print 명령어는 Windows CMD에서 텍스트 파일을 인쇄 대기열(기본 프린터 또는 지정 프린터)로 보낼 때 사용합니다. /d로 프린터 지정, /c·/p로 작업 취소·추가를 할 수 있습니다."
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

print는 Windows 명령 프롬프트(CMD)에서 텍스트 파일을 인쇄 대기열에 넣을 때 사용하는 명령어이다. 기본 프린터로 보내거나 /d로 프린터를 지정할 수 있다. 레거시 환경에서 배치 인쇄에 쓰인다.

## 사용법

```
print [/d:프린터] [[드라이브:][경로]파일이름 [...]]
print /d:프린터 파일이름 [/c] [/p] ...
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/d:프린터` | 사용할 프린터(이름 또는 포트). 맨 처음에 한 번만 지정 |
| `/c` | 해당 파일 인쇄 작업 취소 |
| `/p` | 해당 파일을 인쇄 대기열에 추가 |

## 예시

```
print report.txt
print /d:LPT1 doc.txt
print /d:"My Printer" file1.txt file2.txt
```

## 주의사항

- 프린터 이름에 공백이 있으면 큰따옴표로 감싼다.
- 현대 Windows에서는 스크립트에서 인쇄할 때 PowerShell이나 API를 쓰는 경우가 많다. print는 간단한 텍스트 인쇄용으로만 쓴다.
