---
draft: true
title: "[CMD] date / time - 날짜·시간 표시 및 설정"
description: "date와 time 명령어는 Windows CMD에서 시스템 날짜와 시간을 표시하거나 설정할 때 사용합니다. 배치에서 %date%, %time% 변수로 현재 값을 쓰고, 새 값 입력 시 형식과 권한을 정리합니다."
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

date와 time은 Windows 명령 프롬프트(CMD)에서 현재 시스템 날짜와 시간을 표시하거나, 새 날짜·시간을 설정할 때 사용하는 내장 명령어이다. 인수 없이 실행하면 현재 값을 보여 주고, 새 값을 입력하라는 프롬프트가 나온다.

## 사용법

```
date [/t | 새날짜]
time [/t | 새시간]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/t` | 새 값을 묻지 않고 현재 날짜(또는 시간)만 표시 |

## 예시

```
date
date /t
time /t
echo %date% %time%
```

배치 파일에서는 `%date%`, `%time%` 환경 변수로 현재 날짜·시간 문자열을 쓴다. 형식은 지역 설정에 따라 다르다.

## 주의사항

- 날짜·시간을 변경하려면 보통 관리자 권한이 필요하다. 읽기만 할 때는 `/t`로 묻지 않고 출력한다.
- `%time%`은 밀리초 포함 시 소수점이 있어서 파일 이름 등에 그대로 쓰면 문제가 될 수 있으므로, 배치에서 공백·콜론·점을 치환해 사용하는 경우가 많다.
