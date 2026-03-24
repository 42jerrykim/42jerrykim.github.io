---
draft: true
title: "[CMD] graftabl - 확장 문자 세트"
description: "graftabl 명령어는 Windows CMD에서 그래픽 모드에서 확장 문자 세트(코드 페이지별 추가 문자)를 표시할 수 있게 할 때 사용합니다. 레거시 DOS 호환용으로 현대 콘솔에서는 잘 쓰이지 않습니다."
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

graftabl은 Windows 명령 프롬프트(CMD)에서 그래픽 모드(코드 페이지)에서 확장 문자 세트를 사용할 수 있도록 설정할 때 사용하는 레거시 명령어이다. DOS 시절 확장 ASCII·국가별 문자 표시용으로 쓰였으며, 현대 Windows 콘솔(TrueType 폰트, UTF-8 등)에서는 거의 사용하지 않는다.

## 사용법

```
graftabl [nnn]
graftabl /status
```

nnn은 코드 페이지 번호.

## 옵션

- 코드 페이지를 지정하면 해당 확장 문자가 로드된다.
- `/status`: 현재 로드된 코드 페이지 표시.

## 예시

```
graftabl 437
graftabl /status
```

## 주의사항

- 최신 Windows에서는 chcp와 콘솔 폰트 설정으로 인코딩을 다루는 경우가 많다. 레거시 환경이 아니면 graftabl은 생략해도 된다.
