---
draft: true
title: "[CMD] break - 확장 CTRL+C 검사"
description: "break 명령어는 Windows CMD에서 확장된 CTRL+C 검사 설정을 켜거나 끌 때 사용합니다. on이면 디스크 작업 등에서도 Ctrl+C가 동작합니다. 레거시 호환용으로 잘 쓰이지 않습니다."
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

break는 Windows 명령 프롬프트(CMD)에서 확장된 CTRL+C 검사를 켜거나 끌 때 사용하는 내장 명령어이다. break on이면 디스크 I/O 등에서도 Ctrl+C가 검사되어 중단할 수 있다. 현대 CMD에서는 기본적으로 켜져 있는 경우가 많고, 레거시·호환용으로 남아 있다.

## 사용법

```
break [on | off]
```

## 옵션

- **on**: 확장 CTRL+C 검사 사용
- **off**: 확장 CTRL+C 검사 사용 안 함
- 인수 없이 `break`만 쓰면 현재 설정을 표시한다.

## 예시

```
break
break on
break off
```

## 주의사항

- 대부분의 사용자는 기본값을 그대로 둔다. 긴 디스크 작업 중 Ctrl+C로 중단이 필요할 때만 on으로 설정하는 경우가 있다.
