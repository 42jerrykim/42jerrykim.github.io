---
draft: true
title: "[CMD] assoc - 파일 확장명 연결 표시·수정"
description: "assoc 명령어는 Windows CMD에서 파일 확장명과 파일 형식(연결)의 연결을 보여 주거나 바꿀 때 사용합니다. .txt=txtfile 형태로 연결을 설정하며, ftype과 함께 사용합니다."
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

assoc는 Windows 명령 프롬프트(CMD)에서 파일 확장명(예: .txt)과 파일 형식(예: txtfile)의 연결을 표시하거나 수정할 때 사용하는 내장 명령어이다. 확장명을 더블클릭했을 때 어떤 프로그램이 실행될지는 ftype과 연결되어 결정된다.

## 사용법

```
assoc [.확장자[=파일형식]]
```

## 옵션

- 인수 없이 `assoc`만 쓰면 현재 연결 목록이 나온다.
- `.확장자=파일형식`으로 연결을 설정한다. 파일형식을 빈 문자열로 하면 연결을 제거한다.

## 예시

```
assoc
assoc .txt
assoc .log=txtfile
assoc .myext=
```

## 주의사항

- 파일형식은 ftype으로 정의된 이름을 쓴다. 존재하지 않는 형식을 지정하면 ftype에서 먼저 정의해야 한다.
- 시스템 기본 연결을 바꾸면 더블클릭 동작이 달라지므로, 변경 전 현재 값을 기록해 두는 것이 좋다.
