---
draft: true
title: "[CMD] exit - 명령 프롬프트 종료"
description: "exit 명령어는 Windows CMD에서 현재 CMD.exe 세션을 종료할 때 사용합니다. 배치 파일에서 오류 코드를 반환하거나, 다른 CMD 창을 닫을 때 활용할 수 있습니다."
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

exit는 Windows 명령 프롬프트(CMD)에서 현재 CMD.exe 인스턴스를 종료할 때 사용하는 내장 명령어이다. 배치 파일에서는 exit 후에 반환할 종료 코드(숫자)를 지정할 수 있다.

## 사용법

```
exit [/b] [종료코드]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/b` | 현재 배치 스크립트만 종료하고 CMD 창은 닫지 않음. 종료 코드 지정 가능. |

## 예시

```
exit
exit /b 1
exit 0
```

## 주의사항

- `exit`만 쓰면 CMD 창이 닫힌다. 배치 파일 안에서 호출된 CMD가 종료되면 그 창이 사라진다.
- `exit /b`는 배치 파일 실행을 끝내고, 호출한 쪽(다른 배치나 명령)으로 제어를 돌린다. CMD 세션 자체는 유지된다.
- 종료 코드는 0~255 범위로, 0은 보통 성공을 의미한다.
