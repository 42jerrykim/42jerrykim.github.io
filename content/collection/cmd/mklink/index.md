---
draft: true
title: "[CMD] mklink - 심볼릭·하드 링크 생성"
description: "mklink 명령어는 Windows CMD에서 심볼릭 링크, 하드 링크, 디렉터리 정션을 만들 때 사용합니다. /d 디렉터리 링크, /h 하드 링크, /j 정션, 관리자 권한 요구 사항을 정리합니다."
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

mklink는 Windows 명령 프롬프트(CMD)에서 심볼릭 링크(파일/디렉터리), 하드 링크(파일만), 디렉터리 정션을 만들 때 사용하는 명령어이다. 심볼릭 링크와 정션은 관리자 권한이 필요할 수 있으며, 개발자 모드가 켜져 있으면 일부 제한이 완화된다.

## 사용법

```
mklink [[/d] | [/h] | [/j]] 링크 대상
```

## 옵션

| 옵션 | 설명 |
|------|------|
| (없음) | 파일에 대한 심볼릭 링크 생성 |
| `/d` | 디렉터리에 대한 심볼릭 링크(디렉터리 심볼릭 링크) |
| `/h` | 하드 링크(파일만, 같은 볼륨) |
| `/j` | 디렉터리 정션(Junction) |

## 예시

```
mklink MyLink.txt C:\Data\RealFile.txt
mklink /d C:\LinkDir D:\RealDir
mklink /h hardlink.txt original.txt
mklink /j C:\Junction D:\Target
```

## 주의사항

- 심볼릭 링크/정션 생성은 보통 관리자 권한이 필요하다. Windows 10 이후 개발자 모드에서는 사용자 권한으로 디렉터리 심볼릭 링크를 만들 수 있다.
- 하드 링크는 같은 NTFS 볼륨 안에서만 만들 수 있고, 디렉터리에는 사용할 수 없다. 대상 파일을 지워도 하드 링크는 남아 있다.
