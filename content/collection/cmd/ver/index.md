---
draft: true
title: "[CMD] ver - Windows 버전 표시"
description: "ver 명령어는 Windows CMD에서 현재 Windows(또는 MS-DOS) 버전을 표시할 때 사용합니다. 배치 파일에서 OS 버전에 따라 분기할 때 참고할 수 있습니다."
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

ver는 Windows 명령 프롬프트(CMD)에서 현재 Windows(또는 호환되는 OS) 버전을 표시할 때 사용하는 내장 명령어이다. 출력 형식은 OS에 따라 다르며, 상세 버전이 필요하면 systeminfo나 레지스트리를 참고한다.

## 사용법

```
ver
```

## 옵션

- 옵션 없음.

## 예시

```
ver
```

## 주의사항

- 출력은 예를 들어 "Microsoft Windows [Version 10.0.19045.1234]" 형태이다. 배치에서 파싱해 사용할 수 있으나, 더 정확한 버전 정보는 systeminfo 또는 wmic/os를 사용하는 것이 좋다.
