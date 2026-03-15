---
draft: true
title: "[CMD] find - 파일·출력에서 텍스트 검색"
description: "find 명령어는 Windows CMD에서 파일 내용이나 파이프로 넘어온 입력에서 지정한 문자열이 포함된 줄을 찾을 때 사용합니다. /i 대소문자 무시, /c 카운트, /n 줄 번호 옵션을 정리합니다."
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

find는 Windows 명령 프롬프트(CMD)에서 지정한 파일 또는 표준 입력(파이프)에서 특정 문자열이 포함된 줄을 검색할 때 사용하는 명령어이다. 정규식은 지원하지 않으며, 단순 문자열만 찾는다. 유닉스의 grep과 비슷하지만 기능은 제한적이다.

## 사용법

```
find "문자열" [드라이브:][경로]파일이름 [...]
find /v "문자열" ...
find /c "문자열" ...
find /n "문자열" ...
find /i "문자열" ...
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/v` | 지정한 문자열이 **포함되지 않은** 줄만 표시 |
| `/c` | 일치하는 줄의 개수만 표시 |
| `/n` | 줄 번호를 앞에 붙여 표시 |
| `/i` | 대소문자 구분 없이 검색 |

## 예시

```
find "error" log.txt
find /i "warning" *.log
dir /s /b | find ".txt"
find /c "OK" result.txt
```

## 주의사항

- 검색할 문자열은 반드시 큰따옴표로 감싼다.
- 정규식이나 와일드카드 패턴이 필요하면 findstr을 사용한다.
