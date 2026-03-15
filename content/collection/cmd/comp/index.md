---
draft: true
title: "[CMD] comp - 파일 비교 (레거시)"
description: "comp 명령어는 Windows CMD에서 두 파일 또는 두 디렉터리 내 파일을 바이트 단위로 비교할 때 사용합니다. fc보다 단순하며, 차이 위치와 값을 보고할 수 있습니다."
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

comp는 Windows 명령 프롬프트(CMD)에서 두 파일 또는 두 디렉터리에 있는 같은 이름의 파일들을 바이트 단위로 비교할 때 사용하는 명령어이다. fc보다 오래된 레거시 명령이며, 차이가 나는 오프셋과 바이트 값을 보고한다.

## 사용법

```
comp [드라이브1:][경로1][파일1] [드라이브2:][경로2][파일2] [/d] [/a] [/l] [/n=줄수] [/c]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/d` | 차이를 10진수로 표시(기본은 16진수) |
| `/a` | 차이를 ASCII 문자로 표시 |
| `/l` | 차이가 나는 줄 번호만 표시 |
| `/n=줄수` | 비교할 줄 수 제한 |
| `/c` | 대소문자 구분 안 함 |

## 예시

```
comp file1.txt file2.txt
comp C:\Dir1 D:\Dir2
comp /a /l a.txt b.txt
```

## 주의사항

- 파일 크기가 다르면 비교하지 않고 메시지를 낸다.
- 텍스트 파일의 줄 단위 차이를 보기에는 fc가 더 편할 수 있다. comp는 바이트 단위 비교에 적합하다.
