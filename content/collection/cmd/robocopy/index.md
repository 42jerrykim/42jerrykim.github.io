---
draft: true
title: "[CMD] robocopy - 고급 복사·동기화"
description: "robocopy(Robust File Copy)는 Windows CMD에서 파일·디렉터리 트리를 복사·미러링·동기화할 때 사용합니다. 재시도, 제외, 로그, 다중 스레드 등 옵션이 풍부하며 xcopy보다 강력합니다."
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

robocopy(Robust File Copy)는 Windows에서 제공하는 고급 파일·디렉터리 복사 도구이다. 재시도, 제외 패턴, 로그, 미러링(/mir), 다중 스레드(/mt) 등을 지원하며, xcopy보다 안정적이고 옵션이 많다.

## 사용법

```
robocopy 원본 대상 [파일 [파일]...] [옵션]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `/s` | 하위 디렉터리 복사(빈 디렉터리 제외) |
| `/e` | 빈 디렉터리 포함 |
| `/mir` | 미러링(대상을 원본과 동일하게, 삭제된 항목도 반영) |
| `/r:n` | 실패 시 재시도 횟수(기본 1백만) |
| `/w:n` | 재시도 대기 초(기본 30) |
| `/mt:n` | 다중 스레드(n개, 기본 8) |
| `/xd 디렉터리` | 제외할 디렉터리 |
| `/xf 파일` | 제외할 파일 |
| `/log:파일` | 로그 파일에 기록 |

## 예시

```
robocopy C:\Source D:\Backup /s /e
robocopy C:\Data D:\Mirror /mir /r:3 /w:5
robocopy C:\Src D:\Dst /mt:16 /log:copy.log
```

## 주의사항

- `/mir`는 대상에 있는 원본에 없는 파일·디렉터리를 삭제하므로 사용 전 대상을 확인한다.
- 네트워크 복사 시 `/r`, `/w`로 재시도와 대기 시간을 조정하면 안정적이다.
