---
draft: true
title: "[CMD] compact - NTFS 압축 표시·변경"
description: "compact 명령어는 Windows CMD에서 NTFS 볼륨의 파일·디렉터리 압축을 표시하거나 설정할 때 사용합니다. /c 압축, /u 압축 해제, /s 하위 디렉터리, /a 숨김·시스템 파일 포함을 정리합니다."
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

compact는 Windows 명령 프롬프트(CMD)에서 NTFS 볼륨에 있는 파일과 디렉터리의 압축 상태를 보여 주거나, 압축/압축 해제를 할 때 사용하는 명령어이다. FAT 볼륨에서는 사용할 수 없다.

## 사용법

```
compact [/c | /u] [/s[:경로]] [/a] [/i] [/f] [/q] [파일이름 [...]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/c` | 선택한 파일·디렉터리를 압축 |
| `/u` | 선택한 파일·디렉터리의 압축 해제 |
| `/s[:경로]` | 하위 디렉터리 포함(경로 지정 가능) |
| `/a` | 숨김·시스템 파일도 표시 또는 처리 |
| `/f` | 이미 압축된 파일도 강제로 다시 압축 |
| `/q` | 요약만 표시 |

## 예시

```
compact
compact /c C:\Data
compact /u /s C:\Backup
compact /c /s /a D:\Docs
```

## 주의사항

- 압축된 파일은 읽기·쓰기 시 자동으로 압축·해제되므로 사용 방법은 같다. 단, 성능과 CPU 사용에 영향을 줄 수 있다.
- 이미 압축된 형식(zip, jpg 등)은 compact로 더 줄어들지 않을 수 있다.
