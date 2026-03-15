---
draft: true
title: "[CMD] title - CMD 창 제목 설정"
description: "title 명령어는 Windows CMD에서 명령 프롬프트 창의 제목 표시줄에 보이는 문자열을 바꿀 때 사용합니다. 배치 파일에서 단계별 제목을 넣어 가독성을 높일 수 있습니다."
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

title은 Windows 명령 프롬프트(CMD)에서 현재 CMD 창의 제목 표시줄에 보이는 텍스트를 설정할 때 사용하는 내장 명령어이다. 배치 파일에서 진행 단계를 제목에 표시하면 여러 창을 열었을 때 구분하기 쉽다.

## 사용법

```
title [문자열]
```

## 옵션

- 옵션 없음. 제목으로 쓸 문자열만 지정한다. 비우면 기본 제목으로 돌아간다(환경에 따라 다름).

## 예시

```
title Backup Script
title Step 2 - Copying files
title
```

## 주의사항

- 제목은 해당 CMD 세션에만 적용된다. 다른 CMD 창에는 영향을 주지 않는다.
- 특수문자가 들어가도 그대로 표시된다. 따옴표는 제목에 포함되지 않는다.
