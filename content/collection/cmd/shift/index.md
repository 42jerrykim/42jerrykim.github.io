---
draft: true
title: "[CMD] shift - 배치 인자 위치 이동"
description: "shift 명령어는 Windows CMD 배치 파일에서 %1, %2 등 배치 인자의 위치를 한 칸씩 왼쪽으로 밀 때 사용합니다. 인자 개수가 정해지지 않은 스크립트나 10개 넘는 인자 처리에 유용합니다."
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

shift는 Windows 명령 프롬프트(CMD) 배치 파일에서 배치 인자(%1, %2, ... %9)를 한 칸씩 왼쪽으로 밀 때 사용하는 내장 명령어이다. shift 후에는 원래 %2가 %1이 되고, 원래 %3이 %2가 되는 식이다. 인자가 10개를 넘을 때나 루프에서 인자를 하나씩 처리할 때 쓴다.

## 사용법

```
shift [/n]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/n` | n번째 인자부터만 shift(n은 0~8). 그 앞 인자는 유지. |

## 예시

```
:loop
if "%~1"=="" goto done
echo Processing %1
shift
goto loop
:done
```

## 주의사항

- shift는 되돌릴 수 없다. 필요한 값은 미리 변수에 저장해 두어야 한다.
- `/n` 옵션은 Windows Vista 이후에서 지원된다.
