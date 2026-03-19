---
draft: true
title: "[CMD] xcopy - 디렉터리 트리 복사"
description: "xcopy 명령어는 Windows CMD에서 파일과 디렉터리 트리를 복사할 때 사용합니다. /s, /e로 하위 디렉터리 포함, /exclude, /d 날짜 필터 등 다양한 옵션을 정리합니다."
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

xcopy는 Windows 명령 프롬프트(CMD)에서 파일과 디렉터리 트리를 복사하는 명령어이다. copy보다 옵션이 많아 하위 디렉터리 포함(/s, /e), 빈 디렉터리 포함(/e), 속성 유지(/k), 날짜 기준 복사(/d) 등을 할 수 있다.

## 사용법

```
xcopy 원본 [대상] [/a | /m] [/d[:날짜]] [/p] [/s [/e]] [/v] [/w] [/c] [/i] [/q] [/f] [/l] [/g] [/h] [/r] [/t] [/u] [/k] [/n] [/o] [/x] [/y] [/-y] [/z] [/b] [/exclude:파일목록]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/s` | 비어 있지 않은 하위 디렉터리까지 복사 |
| `/e` | 빈 하위 디렉터리도 복사(/s와 함께 사용) |
| `/i` | 대상을 디렉터리로 간주 |
| `/d:날짜` | 지정한 날짜 이후에 변경된 파일만 복사 |
| `/y` | 덮어쓸 때 확인하지 않음 |
| `/exclude:파일` | 제외할 패턴이 나열된 파일 지정 |

## 예시

```
xcopy C:\Source D:\Backup /s /e
xcopy *.txt D:\Text /d /y
xcopy C:\Data D:\Data /s /e /exclude:exclude.txt
```

## 주의사항

- 대상이 없으면 "대상은 파일인가 디렉터리인가"라고 묻는다. 배치에서는 `/i`로 디렉터리로 간주하도록 하면 된다.
- 더 강력한 복사·동기화가 필요하면 robocopy를 사용하는 것이 좋다.
