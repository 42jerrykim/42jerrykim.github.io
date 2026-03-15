---
draft: true
title: "[CMD] cmd - 새 CMD 인스턴스 시작"
description: "cmd 명령어는 Windows CMD에서 Windows 명령 인터프리터(CMD.exe)의 새 인스턴스를 시작할 때 사용합니다. /c 한 번 실행 후 종료, /k 유지, /q 에코 끄기, 스위치와 인수 전달을 정리합니다."
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

cmd는 Windows 명령 프롬프트(CMD)에서 명령 인터프리터(cmd.exe)의 새 인스턴스를 시작할 때 사용하는 실행 파일 이름이자 명령이다. start와 함께 새 창에서 CMD를 띄우거나, /c로 한 번에 명령을 실행한 뒤 종료하는 용도로 쓴다.

## 사용법

```
cmd [/c | /k] [/q] [/a | /u] [/t:fg] [/e:on | /e:off] [/f:on | /f:off] [/v:on | /v:off] [[/s] [/c | /k] 문자열]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/c 문자열` | 문자열에 지정한 명령을 실행한 뒤 종료 |
| `/k 문자열` | 문자열에 지정한 명령을 실행한 뒤 창 유지 |
| `/q` | 에코 끄기(확장도 끔) |
| `/t:fg` | 전경/배경 색 지정 |
| `/e:on|off` | 명령 확장 사용 여부 |
| `/v:on|off` | 지연된 환경 변수 확장 |

## 예시

```
cmd /c dir
cmd /k
start cmd /k "cd C:\Projects && dir"
```

## 주의사항

- `/c`는 배치에서 한 번만 실행하고 끝내는 서브셸에 적합하다. `/k`는 대화형 셸을 열 때 쓴다.
- 0_cmd 문서는 cmd.exe 전체 개요와 내장 명령 목록을 다룬다. 이 글은 "새 인스턴스 시작" 용도에 초점을 둔다.
