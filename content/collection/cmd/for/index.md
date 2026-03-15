---
draft: true
title: "[CMD] for - 반복 및 집합 처리"
description: "for 명령어는 Windows CMD와 배치 파일에서 파일 집합, 디렉터리, 문자열 목록, 숫자 범위에 대해 반복할 때 사용합니다. /r, /d, /l, 토큰·구분자 활용을 정리합니다."
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

for는 Windows 명령 프롬프트(CMD)와 배치 파일에서 파일 집합, 디렉터리 목록, 문자열 목록, 숫자 시퀀스 등에 대해 반복 실행할 때 사용하는 내장 명령어이다. 여러 형태(for, for /d, for /r, for /l, for /f)가 있다.

## 사용법

```
for %변수 in (집합) do 명령
for /d %변수 in (집합) do 명령
for /r [경로] %변수 in (집합) do 명령
for /l %변수 in (시작,단계,끝) do 명령
for /f ["옵션"] %변수 in (집합) do 명령
```

## 옵션

| 옵션 | 설명 |
|------|------|
| (기본) | 집합에 나열된 각 항목에 대해 명령 실행 |
| `/d` | 디렉터리만 대상 |
| `/r [경로]` | 지정 경로부터 재귀적으로 디렉터리 순회 |
| `/l` | 숫자 시퀀스(시작, 단계, 끝) |
| `/f` | 파일 내용, 명령 출력, 문자열을 파싱하여 토큰 사용 |

## 예시

```
for %f in (*.txt) do echo %f
for /d %d in (C:\*) do @echo %d
for /l %i in (1,1,10) do echo %i
for /f "tokens=1" %a in (list.txt) do echo %a
```

## 주의사항

- 배치 파일 안에서는 `%변수`를 `%%변수`로 쓴다.
- `/f`의 구분자, 토큰, skip 등 옵션은 따옴표 안에 넣는다. 공백·특수문자 처리에 주의한다.
