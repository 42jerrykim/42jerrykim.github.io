---
draft: true
title: "[CMD] help - 명령어 도움말"
description: "help 명령어는 Windows CMD에서 내장 명령어 목록과 간단한 사용법을 보여 줍니다. 'help 명령이름'으로 해당 명령의 도움말을 볼 수 있으며, 명령 /? 도와 동일합니다."
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

help는 Windows 명령 프롬프트(CMD)에서 지원하는 내장 명령 목록을 보여 주거나, 지정한 명령의 도움말을 표시할 때 사용하는 내장 명령어이다. `명령 /?`를 입력해도 같은 도움말을 볼 수 있다.

## 사용법

```
help [명령이름]
명령이름 /?
```

## 옵션

- 인수 없이 `help`만 입력하면 도움말이 제공되는 명령 목록이 나온다.
- `help copy`, `copy /?`처럼 명령 이름을 주면 해당 명령의 옵션·문법이 출력된다.

## 예시

```
help
help xcopy
dir /?
```

## 주의사항

- 외부 프로그램(.exe)은 CMD 내장 명령이 아니므로 `help`나 `/?'`로 도움말이 나오지 않을 수 있다. 해당 프로그램의 `--help`, `-?` 등을 사용한다.
