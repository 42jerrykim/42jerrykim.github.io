---
draft: true
title: "[CMD] chcp - 코드 페이지(코드 페이지) 표시·설정"
description: "chcp 명령어는 Windows CMD에서 활성 코드 페이지(콘솔 문자 인코딩)를 표시하거나 변경할 때 사용합니다. 949(한국어), 65001(UTF-8) 등 코드 페이지 번호로 한글·유니코드 출력을 맞출 수 있습니다."
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

chcp(Change Code Page)는 Windows 명령 프롬프트(CMD)에서 현재 콘솔의 활성 코드 페이지(문자 인코딩)를 표시하거나 변경할 때 사용하는 내장 명령어이다. 한글이 깨질 때 949(한국어)로 맞추거나, UTF-8 출력을 위해 65001로 설정할 수 있다.

## 사용법

```
chcp [nnn]
```

nnn은 코드 페이지 번호(예: 437, 949, 65001).

## 주요 코드 페이지

- **437**: OEM 미국
- **949**: 한국어(한글)
- **65001**: UTF-8

## 예시

```
chcp
chcp 949
chcp 65001
```

## 주의사항

- 콘솔 폰트가 해당 코드 페이지를 지원해야 문자가 제대로 보인다. UTF-8(65001)은 TrueType 폰트(예: Consolas)와 함께 쓴다.
- type, echo 등으로 출력하는 파일·문자열의 인코딩과 코드 페이지가 맞아야 한다.
