---
draft: true
title: "[CMD] pause - 배치 실행 일시 정지"
description: "pause 명령어는 Windows CMD 배치 파일에서 '아무 키나 누르세요' 메시지를 보여 주고 사용자 키 입력이 있을 때까지 실행을 멈출 때 사용합니다. 디버깅과 대화형 스크립트에 유용합니다."
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

pause는 Windows 명령 프롬프트(CMD) 배치 파일에서 "아무 키나 누르십시오..." 메시지를 표시하고, 사용자가 키를 누를 때까지 실행을 일시 정지할 때 사용하는 내장 명령어이다.

## 사용법

```
pause
```

## 옵션

- 옵션 없음. 메시지 후 키 입력을 기다린다.

## 예시

```
@echo off
echo Backup completed.
pause
```

## 주의사항

- 더블클릭으로 실행한 배치가 끝나기 전에 창이 닫히는 것을 막고 싶을 때 끝에 pause를 두면 유용하다.
- 자동 실행·스케줄 작업에서는 pause가 걸리면 사람이 키를 눌러야 하므로 사용하지 않는 것이 좋다.
