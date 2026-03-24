---
draft: true
title: "[CMD] mode - 시스템 장치 구성"
description: "mode 명령어는 Windows CMD에서 콘솔(코드 페이지, 크기), 직렬(COM) 포트, 병렬(LPT) 포트, 디스크 재시도 등 시스템 장치 구성을 할 때 사용합니다. 레거시·호환용으로 일부 환경에서만 쓰입니다."
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

mode는 Windows 명령 프롬프트(CMD)에서 콘솔(화면 버퍼·코드 페이지), 직렬(COM) 포트, 병렬(LPT) 포트, 디스크 재시도 등 장치 구성을 할 때 사용하는 내장 명령어이다. DOS 시절부터 있던 레거시 명령으로, 현대에서는 콘솔 크기·코드 페이지 등 일부만 쓰인다.

## 사용법

```
mode [장치] [[/status]]
mode con[:] [cols=n] [lines=n]
mode con[:] cp select=nnn
mode com[:]n [baud=숫자] [parity=n|e|o] [data=n] [stop=n]
mode lpt[:]n [cols=n] [lines=n]
```

## 옵션

- **con**: 콘솔. cols, lines로 화면/버퍼 크기, cp select로 코드 페이지.
- **com n**: 직렬 포트 n. baud, parity, data, stop.
- **lpt n**: 병렬 포트 n.
- **/status**: 지정한 장치 상태만 표시.

## 예시

```
mode con cols=120 lines=30
mode con cp select=949
mode com1 baud=9600
mode /status
```

## 주의사항

- 직렬·병렬 포트는 가상 포트나 USB 변환기에만 해당할 수 있다. 콘솔 설정은 터미널 속성에서 하는 경우가 더 많다.
