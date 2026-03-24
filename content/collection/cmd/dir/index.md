---
draft: true
title: "[CMD] dir - 디렉터리 내용 목록 보기"
description: "dir 명령어는 Windows CMD에서 디렉터리 안의 파일과 하위 디렉터리 목록을 보여줍니다. 옵션으로 정렬, 숨김 파일 표시, 와일드카드 필터, 재귀 목록 등을 사용할 수 있으며, 유닉스의 ls에 대응합니다."
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

dir은 Windows 명령 프롬프트(CMD)에서 지정한 디렉터리(또는 현재 디렉터리)에 있는 파일과 하위 디렉터리 목록을 표시하는 내장 명령어이다. 파일 크기, 날짜·시간, 속성 등을 함께 보여 주며, 유닉스/Linux의 ls와 역할이 비슷하다.

## 사용법

```
dir [드라이브:][경로][파일이름] [/a[[:]속성]] [/b] [/c] [/d] [/l] [/n] [/o[[:]정렬순서]] [/p] [/q] [/r] [/s] [/t[[:]시간필드]] [/w] [/x] [/4]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/a` | 지정한 속성의 파일만 표시. 속성: d(디렉터리), r(읽기전용), h(숨김), a(보관), s(시스템) 등 |
| `/b` | 간단한 형식(파일명만) |
| `/s` | 하위 디렉터리까지 재귀 표시 |
| `/o` | 정렬. n(이름), s(크기), e(확장자), d(날짜) 등 |
| `/p` | 한 화면씩 멈춤 |
| `/w` | 가로로 여러 열 표시 |

## 예시

```
dir
dir /a:h
dir *.txt /s /b
dir /o:n
```

## 주의사항

- 숨김·시스템 파일은 `/a:h` 또는 `/a`로 표시할 수 있다.
- 용량이 큰 디렉터리에서 `/s` 사용 시 출력이 길어지므로 `/p`와 함께 쓰거나 파이프로 more을 사용하는 것이 좋다.
