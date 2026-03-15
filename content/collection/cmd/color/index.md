---
draft: true
title: "[CMD] color - 콘솔 전경·배경 색"
description: "color 명령어는 Windows CMD에서 콘솔 창의 전경색과 배경색을 변경할 때 사용합니다. 16색 코드 한 자리 또는 두 자리(배경+전경)로 지정하며, 인수 없이 쓰면 기본색으로 복원합니다."
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

color는 Windows 명령 프롬프트(CMD)에서 콘솔 창의 전경색과 배경색을 바꿀 때 사용하는 내장 명령어이다. 0~9, A~F의 16색 코드를 사용하며, 한 자리는 전경만, 두 자리는 배경+전경 순서로 지정한다.

## 사용법

```
color [배경코드전경코드]
```

## 색 코드

0=검정, 1=파랑, 2=녹색, 3=청록, 4=빨강, 5=자주, 6=노랑, 7=흰색, 8=회색, 9=연파랑, A=연녹색, B=연청록, C=연빨강, D=연자주, E=연노랑, F=밝은흰색.

## 예시

```
color 0A
color 1f
color
```

인수 없이 `color`만 쓰면 기본 색(보통 0f 등)으로 복원된다.

## 주의사항

- 배경과 전경을 같은 코드로 하면 보이지 않을 수 있다.
- 변경은 현재 CMD 세션에만 적용된다.
