---
draft: true
title: "[CMD] copy - 파일 복사"
description: "copy 명령어는 Windows CMD에서 하나 이상의 파일을 다른 위치나 같은 디렉터리에 다른 이름으로 복사할 때 사용합니다. /v 검증, /y 덮어쓰기 확인 생략, 디바이스 이름 활용법을 정리합니다."
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

copy는 Windows 명령 프롬프트(CMD)에서 파일을 다른 위치나 같은 폴더에 다른 이름으로 복사하는 내장 명령어이다. 디렉터리 트리 전체 복사는 지원하지 않으며, 그런 경우 xcopy나 robocopy를 사용한다.

## 사용법

```
copy [/d] [/v] [/n] [/y | /-y] [/z] [/a | /b] 원본 [+ 원본 ...] [대상]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/v` | 복사 후 검증 |
| `/y` | 덮어쓸 때 확인 없이 덮어쓰기 |
| `/-y` | 덮어쓸 때 확인 요청 |
| `/a` | ASCII 텍스트 모드 |
| `/b` | 바이너리 모드 |

## 예시

```
copy report.txt report.bak
copy *.txt D:\Backup\
copy file1.txt + file2.txt combined.txt
```

## 주의사항

- 대상이 디렉터리면 같은 이름으로 복사된다. 대상이 파일이면 해당 이름으로 복사된다.
- 여러 파일을 `+`로 이어 붙일 수 있다(텍스트 파일 결합 등).
- 복사 후 원본은 그대로 남는다. 이동이 필요하면 move를 사용한다.
