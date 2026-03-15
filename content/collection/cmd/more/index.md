---
draft: true
title: "[CMD] more - 한 화면씩 출력"
description: "more 명령어는 Windows CMD에서 긴 출력을 한 화면(한 페이지)씩 보여 주고 스페이스로 다음 페이지를 넘길 때 사용합니다. 파일 내용이나 파이프 입력에 사용할 수 있습니다."
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

more는 Windows 명령 프롬프트(CMD)에서 긴 출력을 한 번에 한 화면(페이지)씩 표시하고, 사용자가 스페이스 등을 눌러 다음 페이지로 넘길 수 있게 할 때 사용하는 명령어이다. 유닉스의 more, less와 비슷한 역할이다.

## 사용법

```
more [/e [/c] [/p] [/s] [/tn]] [+n] < [드라이브:][경로]파일이름
명령 | more [/e [/c] [/p] [/s] [/tn]] [+n]
more [[/e [/c] [/p] [/s] [/tn]] [+n]] [드라이브:][경로]파일이름 [...]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `+n` | n번째 줄부터 표시 시작 |
| `/e` | 확장 모드. 아래 설명 참조 |
| `/c` | 페이지 넘기기 전에 화면 지우기 |
| `/p` | 폼피드(줄바꿈 확장) 사용 안 함 |
| `/s` | 연속 빈 줄을 한 줄로 |

## 예시

```
type longfile.txt | more
more +10 readme.txt
dir /s | more
```

## 주의사항

- 파이프로 넘길 때: `명령 | more`. 리다이렉트로 파일을 줄 때: `more < file.txt` 또는 `more file.txt`.
- 한 줄씩 넘기려면 Enter, 한 페이지씩 넘기려면 스페이스. q로 종료(환경에 따라 다름).
