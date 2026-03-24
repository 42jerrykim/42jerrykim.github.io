---
draft: true
title: "[CMD] echo - 메시지 출력 및 echo on/off"
description: "echo 명령어는 Windows CMD와 배치 파일에서 메시지를 화면에 출력하거나, 명령 에코(echo on/off)를 켜고 끌 때 사용합니다. 변수 확장, 빈 줄, 리다이렉트 활용을 정리합니다."
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

echo는 Windows 명령 프롬프트(CMD)와 배치 파일에서 메시지를 콘솔에 출력하거나, 명령 에코(실행되는 명령을 화면에 보여 주는 것)를 켜거나 끌 때 사용하는 내장 명령어이다.

## 사용법

```
echo [on | off]
echo [메시지]
```

## 옵션

- `echo on`: 이후 실행되는 각 명령을 그대로 화면에 표시(기본값).
- `echo off`: 명령 자체는 숨기고, 결과만 표시. 배치 파일 첫 줄에 `@echo off`를 쓰면 echo off 명령 자체도 숨긴다.
- `echo 메시지`: 메시지를 출력. 메시지가 비어 있으면 현재 echo on/off 상태를 보여 준다.

## 예시

```
echo Hello World
echo off
@echo off
echo.
echo Current date: %date%
```

## 주의사항

- `echo.`은 빈 줄을 출력하는 데 자주 쓰인다(점 앞에 공백이 없어야 함).
- `echo %변수명%`으로 환경 변수 값을 출력할 수 있다.
- 특수문자 `>`, `|` 등은 echo 출력 시 이스케이프 처리가 필요할 수 있다.
