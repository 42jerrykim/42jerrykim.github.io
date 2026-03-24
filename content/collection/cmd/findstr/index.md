---
draft: true
title: "[CMD] findstr - 문자열·정규식 검색"
description: "findstr 명령어는 Windows CMD에서 파일이나 표준 입력에서 문자열을 검색할 때 사용합니다. 간단한 정규식, /r 리터럴, /s 하위 디렉터리, /b 줄 시작 등 옵션을 정리합니다."
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

findstr은 Windows 명령 프롬프트(CMD)에서 파일 또는 파이프 입력에서 문자열을 검색할 때 사용하는 명령어이다. find보다 기능이 많고, 간단한 정규식(., *, ^, $ 등)과 여러 패턴, 디렉터리 재귀 검색을 지원한다.

## 사용법

```
findstr [/b] [/e] [/l] [/r] [/s] [/i] [/x] [/v] [/n] [/m] [/o] [/p] [/f:파일] [/c:문자열] [/g:파일] [/d:디렉터리] [문자열] [드라이브:][경로]파일이름 [...]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/b` | 줄의 시작과 일치할 때만 |
| `/e` | 줄의 끝과 일치할 때만 |
| `/i` | 대소문자 구분 안 함 |
| `/r` | 검색 문자열을 정규식으로 해석 |
| `/s` | 현재 디렉터리와 하위 디렉터리 검색 |
| `/n` | 줄 번호 표시 |
| `/x` | 줄 전체가 일치할 때만 |
| `/v` | 일치하지 **않는** 줄만 표시 |

## 예시

```
findstr "error" *.log
findstr /s /i "TODO" *.txt
findstr /r "^[0-9]" data.txt
findstr /c:"exact phrase" file.txt
```

## 주의사항

- 공백이 포함된 문자열은 `/c:"문자열"` 형태로 넣는다.
- 정규식 문법은 grep 등과 일부 다르다. 메타문자 사용 시 테스트를 권장한다.
