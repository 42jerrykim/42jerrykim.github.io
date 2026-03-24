---
draft: true
title: "[CMD] subst - 경로를 드라이브 문자에 연결"
description: "subst 명령어는 Windows CMD에서 로컬 경로를 가상 드라이브 문자(예: Z:)에 연결할 때 사용합니다. 연결 해제는 subst 드라이브: /d 로 합니다. 재부팅 후에는 사라집니다."
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

subst는 Windows 명령 프롬프트(CMD)에서 로컬 폴더 경로를 가상 드라이브 문자(예: Z:)에 연결할 때 사용하는 내장 명령어이다. 긴 경로를 짧은 드라이브로 접근할 수 있으며, 인수 없이 쓰면 현재 연결 목록이 나온다.

## 사용법

```
subst [드라이브: [경로]]
subst 드라이브: /d
```

## 옵션

| 사용 | 설명 |
|------|------|
| `subst` | 현재 가상 드라이브 연결 목록 표시 |
| `subst Z: C:\Long\Path` | Z:를 해당 경로에 연결 |
| `subst Z: /d` | Z: 연결 해제 |

## 예시

```
subst
subst Z: C:\Projects\VeryLongFolderName
Z:
dir
subst Z: /d
```

## 주의사항

- 연결은 현재 세션에만 유지된다. 재부팅하면 사라진다. 자동 연결이 필요하면 로그인 스크립트나 시작 프로그램에서 subst를 실행한다.
- 사용하지 않는 드라이브 문자를 쓴다. 이미 사용 중인 드라이브는 지정할 수 없다.
