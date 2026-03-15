---
draft: true
title: "[CMD] attrib - 파일 속성 표시 및 변경"
description: "attrib 명령어는 Windows CMD에서 파일이나 디렉터리의 속성(읽기 전용, 숨김, 보관, 시스템)을 보거나 바꿀 때 사용합니다. /s, /d로 하위 디렉터리·폴더 포함 방법을 정리합니다."
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

attrib는 Windows 명령 프롬프트(CMD)에서 파일 또는 디렉터리의 속성(읽기 전용 R, 숨김 H, 보관 A, 시스템 S)을 표시하거나 변경할 때 사용하는 명령어이다.

## 사용법

```
attrib [+r | -r] [+a | -a] [+s | -s] [+h | -h] [[드라이브:][경로]파일이름] [/s [/d]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `+r` / `-r` | 읽기 전용 설정/해제 |
| `+h` / `-h` | 숨김 설정/해제 |
| `+a` / `-a` | 보관(아카이브) 설정/해제 |
| `+s` / `-s` | 시스템 파일 설정/해제 |
| `/s` | 하위 디렉터리 처리 |
| `/d` | 디렉터리도 함께 처리(/s와 함께 사용) |

## 예시

```
attrib report.txt
attrib +r readme.txt
attrib -h +r *.bak
attrib /s /d *.*
```

## 주의사항

- 시스템(S) 또는 숨김(H) 속성을 바꿀 때는 관리자 권한이 필요할 수 있다.
- 중요한 시스템 파일의 속성을 함부로 바꾸면 부팅이나 동작에 문제가 생길 수 있으므로 주의한다.
