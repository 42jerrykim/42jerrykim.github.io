---
draft: true
title: "[CMD] rem - 배치 파일 주석"
description: "rem 명령어는 Windows CMD 배치 파일에서 주석(설명)을 넣을 때 사용합니다. 실행되지 않는 줄을 만들어 코드 설명이나 비활성화할 명령을 기록할 수 있습니다."
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

rem(Remark)는 Windows 명령 프롬프트(CMD) 배치 파일에서 주석을 달 때 사용하는 내장 명령어이다. rem 다음에 오는 내용은 실행되지 않고, echo on인 경우에만 화면에 그대로 출력될 수 있다.

## 사용법

```
rem [주석 내용]
```

## 옵션

- 옵션 없음. 해당 줄 전체가 주석으로 처리된다.

## 예시

```
rem This script backs up the data folder
rem 2025-03-15 Updated path
echo Starting...
rem call old-script.bat
```

## 주의사항

- rem 줄 안에서 `%`는 변수로 확장되지 않는다(일반적으로).
- 짧은 주석은 `::`로 대체할 수 있으나, ::는 레이블 문법을 이용한 것이므로 일부 문맥에서는 동작이 다를 수 있다. 호환성을 위해 rem 사용을 권장한다.
