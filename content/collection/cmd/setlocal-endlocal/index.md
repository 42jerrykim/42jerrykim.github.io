---
draft: true
title: "[CMD] setlocal / endlocal - 환경 변경 지역화"
description: "setlocal과 endlocal은 Windows CMD 배치 파일에서 환경 변수·디렉터리 변경을 해당 블록 안으로 제한할 때 사용합니다. setlocal 이후 변경 사항은 endlocal 또는 배치 종료 시 원래대로 돌아갑니다."
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

setlocal과 endlocal은 Windows 명령 프롬프트(CMD) 배치 파일에서 환경 변경을 지역화할 때 사용하는 내장 명령어이다. setlocal 이후에 설정·변경한 환경 변수와 현재 디렉터리는 endlocal을 만나거나 배치가 끝날 때 자동으로 되돌아간다.

## 사용법

```
setlocal [enableextensions | disableextensions] [enabledelayedexpansion | disabledelayedexpansion]
endlocal
```

## setlocal 옵션

| 옵션 | 설명 |
|------|------|
| (없음) | 환경 변경만 지역화 |
| `enableextensions` | 확장 명령 사용(기본) |
| `enabledelayedexpansion` | 지연된 환경 변수 확장 사용(!변수!) |

## 예시

```
setlocal
set MYVAR=temp
cd \Temp
echo %MYVAR%
endlocal
rem MYVAR and CD are restored here
```

## 주의사항

- setlocal을 여러 번 중첩할 수 있다. endlocal은 가장 안쪽 setlocal부터 해제한다.
- 배치 파일이 끝나면 남아 있는 setlocal도 자동으로 해제된다. 호출한 쪽 CMD 세션에는 setlocal 안에서의 변경이 반영되지 않는다.
