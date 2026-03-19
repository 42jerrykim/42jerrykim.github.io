---
draft: true
title: "[CMD] sort - 입력 정렬"
description: "sort 명령어는 Windows CMD에서 파일 내용이나 파이프로 넘어온 입력을 줄 단위로 정렬할 때 사용합니다. /r 역순, /+n n번째 문자부터 정렬, 대소문자·숫자 정렬 옵션을 정리합니다."
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

sort는 Windows 명령 프롬프트(CMD)에서 파일 또는 표준 입력의 내용을 줄 단위로 정렬할 때 사용하는 명령어이다. 정렬 결과를 화면에 출력하거나 리다이렉트로 파일에 쓸 수 있다.

## 사용법

```
sort [/r] [/+n] [/m 킬로바이트] [/l 로케일] [/rec 문자수] [드라이브:][경로]파일이름 [...]
sort /+n [드라이브:][경로]파일이름
명령 | sort [/r] [/+n]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/r` | 역순(내림차순) 정렬 |
| `/+n` | 각 줄의 n번째 문자부터 정렬(기본 1) |
| `/l 로케일` | 정렬에 사용할 로케일 지정 |

## 예시

```
sort names.txt
sort /r numbers.txt
type list.txt | sort
dir /b | sort
```

## 주의사항

- 기본적으로 오름차순(문자 코드 기준)이다. 숫자로 정렬하려면 숫자 자리 수를 맞추거나 별도 스크립트가 필요할 수 있다.
- 출력을 파일로 저장할 때는 `sort input.txt > output.txt`. 같은 파일에 덮어쓰면 안 된다(입력이 먼저 읽히므로).
