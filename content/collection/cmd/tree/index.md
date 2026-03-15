---
draft: true
title: "[CMD] tree - 디렉터리 구조 표시"
description: "tree 명령어는 Windows CMD에서 드라이브나 경로의 디렉터리 구조를 트리 형태로 그래픽하게 보여줍니다. /f로 파일까지 표시, /a로 ASCII 문자 사용 등 옵션을 정리합니다."
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

tree는 Windows 명령 프롬프트(CMD)에서 지정한 드라이브 또는 경로의 디렉터리 구조를 트리 형태로 표시하는 명령어이다. 하위 디렉터리와, 옵션에 따라 파일 이름까지 계층적으로 볼 수 있다.

## 사용법

```
tree [드라이브:][경로] [/f] [/a]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/f` | 각 디렉터리 안의 파일 이름도 표시 |
| `/a` | 확장 문자 대신 ASCII 문자로 선을 그림(호환성용) |

## 예시

```
tree
tree C:\Projects
tree /f
tree D:\Data /f /a
```

## 주의사항

- 출력이 길면 `tree /f | more`로 한 화면씩 볼 수 있다.
- 특정 깊이만 보는 옵션은 없으며, 필요하면 출력을 다른 도구로 가공해야 한다.
