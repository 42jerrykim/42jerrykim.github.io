---
draft: true
title: "[CMD] replace - 파일 바꾸기"
description: "replace 명령어는 Windows CMD에서 대상 디렉터리의 파일을 원본 디렉터리 파일로 덮어쓰거나, 대상에 없는 파일만 추가할 때 사용합니다. /s 하위 디렉터리, /u 최신만, /a 추가 전용을 정리합니다."
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

replace는 Windows 명령 프롬프트(CMD)에서 원본 디렉터리의 파일로 대상 디렉터리의 같은 이름 파일을 덮어쓰거나, 대상에 없는 파일만 추가할 때 사용하는 명령어이다. 동기화·배포 시 유용하다.

## 사용법

```
replace [드라이브1:][경로1]파일이름 [드라이브2:][경로2] [/a] [/p] [/r] [/w] [/s] [/u] [/o]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/a` | 대상에 없는 파일만 추가(덮어쓰지 않음) |
| `/p` | 각 대상 파일 덮어쓰기 전에 확인 |
| `/r` | 읽기 전용 파일도 덮어쓰기 |
| `/s` | 하위 디렉터리 포함 |
| `/u` | 원본이 대상보다 최신인 파일만 업데이트 |
| `/w` | 디스크 넣기 등 대기 후 진행 |

## 예시

```
replace C:\New\*.* D:\Old\ /s /u
replace C:\Src\*.dll D:\App\ /a
replace C:\Patch\*.* D:\Target\ /s /p
```

## 주의사항

- 원본에 와일드카드(*.txt 등)를 쓰면 해당 패턴 파일만 대상과 비교·대체된다. 대상 경로는 디렉터리만 지정한다.
- 읽기 전용·시스템 파일을 바꿀 때는 /r이 필요하고, 권한이 있어야 한다.
