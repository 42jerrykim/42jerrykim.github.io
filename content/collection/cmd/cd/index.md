---
draft: true
title: "[CMD] cd (CHDIR) - 현재 디렉터리 확인 및 변경"
description: "cd(CHDIR)는 Windows CMD에서 현재 작업 디렉터리를 표시하거나 다른 디렉터리로 이동할 때 사용합니다. 드라이브 전환, 상대·절대 경로, 환경 변수 활용 방법과 유닉스/Linux의 cd, pwd와의 차이를 정리합니다."
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

cd(Change Directory) 또는 CHDIR은 Windows 명령 프롬프트(CMD)에서 현재 작업 디렉터리를 표시하거나, 지정한 디렉터리로 이동할 때 사용하는 내장 명령어이다. DOS, OS/2, Windows NT 계열에서 공통으로 지원된다.

## 사용법

```
cd [/d] [드라이브:][경로]
cd ..
cd [드라이브:]
```

- 경로 없이 `cd`만 입력하면 현재 디렉터리 경로를 표시한다.
- `cd ..`는 상위 디렉터리로 이동한다.
- 다른 드라이브로 이동할 때는 `/d` 옵션을 사용한다(옵션 없이 경로만 주면 드라이브는 바뀌지 않고 해당 드라이브의 현재 디렉터리만 표시된다).

## 옵션

| 옵션 | 설명 |
|------|------|
| `/d` | 드라이브와 디렉터리를 동시에 변경한다. |

## 예시

```
C:\Users> cd
C:\Users

C:\Users> cd \Windows\System32
C:\Windows\System32> cd ..
C:\Windows>

D:\> cd /d C:\Projects
C:\Projects>
```

## 주의사항

- 드라이브 문자만 바꾸려면 `cd /d D:`처럼 `/d`와 함께 사용해야 한다.
- 경로에 공백이 있으면 큰따옴표로 감싼다: `cd "C:\Program Files"`.
- 유닉스/Linux의 `pwd`에 해당하는 동작은 `cd`만 입력했을 때이다.
