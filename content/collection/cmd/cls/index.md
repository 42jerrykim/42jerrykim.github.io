---
draft: true
title: "[CMD] cls - 화면 지우기"
description: "cls 명령어는 Windows CMD에서 콘솔 화면의 모든 문자를 지우고 커서를 왼쪽 위로 옮길 때 사용합니다. 배치 파일에서 출력을 정리하거나 가독성을 높일 때 유용합니다."
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

cls(Clear Screen)는 Windows 명령 프롬프트(CMD)에서 콘솔 화면에 표시된 내용을 모두 지우고 커서를 화면 왼쪽 위로 이동시키는 내장 명령어이다. 유닉스의 clear 또는 reset과 비슷한 역할이다.

## 사용법

```
cls
```

## 옵션

- 옵션 없이 `cls`만 입력한다.

## 예시

```
cls
```

배치 파일에서 메뉴를 보여주기 전에 화면을 비울 때 자주 쓴다.

## 주의사항

- 화면 버퍼에 저장된 이전 출력은 지워지지만, 스크롤로 올려서 다시 볼 수 있는 경우가 있다(콘솔 설정에 따라 다름).
- 명령 기록(히스토리)은 지워지지 않는다.
