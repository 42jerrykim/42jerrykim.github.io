---
draft: true
title: "[CMD] start - 새 창에서 프로그램 실행"
description: "start 명령어는 Windows CMD에서 프로그램이나 명령을 새 창에서 실행할 때 사용합니다. /wait로 종료 대기, /min 최소화, /b 같은 창에서 실행, 타이틀 지정 등을 정리합니다."
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

start는 Windows 명령 프롬프트(CMD)에서 응용 프로그램, 문서, 또는 다른 명령을 새 창에서 실행할 때 사용하는 내장 명령어이다. 같은 창에서 비동기로 실행하거나(/b), 새 프로세스가 끝날 때까지 대기(/wait)할 수 있다.

## 사용법

```
start ["제목"] [/d 경로] [/i] [/min] [/max] [/separate | /shared] [/wait] [/b] [명령/프로그램] [인수]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `"제목"` | 새 창의 제목 표시줄에 표시할 문자열 |
| `/d 경로` | 작업 디렉터리 |
| `/min` | 최소화된 상태로 실행 |
| `/wait` | 시작한 프로그램이 종료될 때까지 CMD가 대기 |
| `/b` | 새 창을 열지 않고 현재 창에서 실행(비동기) |

## 예시

```
start notepad
start "" /wait myprogram.exe
start /min cmd /k dir
start /d C:\Projects myapp.exe
```

## 주의사항

- 실행할 항목에 공백이 있으면 첫 번째 인수를 창 제목으로 간주할 수 있으므로, 빈 제목 `""`을 앞에 두는 경우가 많다.
- `/wait`를 쓰면 해당 프로세스가 끝날 때까지 배치 파일이 다음 줄로 진행하지 않는다.
