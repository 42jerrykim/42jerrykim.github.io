---
draft: true
title: "[CMD] chkdsk - 디스크 검사"
description: "chkdsk 명령어는 Windows CMD에서 디스크의 파일 시스템과 선택적으로 배드 섹터를 검사·수정할 때 사용합니다. /f 수정, /r 배드 섹터 복구, 볼륨이 사용 중일 때 예약 방법을 정리합니다."
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

chkdsk(Check Disk)는 Windows 명령 프롬프트(CMD)에서 지정한 볼륨의 파일 시스템 무결성을 검사하고, 옵션에 따라 오류를 수정하거나 배드 섹터를 복구할 때 사용하는 명령어이다.

## 사용법

```
chkdsk [볼륨:][[경로]파일이름] [/f] [/v] [/r] [/x] [/i] [/c] [/l[:크기]] [/b]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/f` | 디스크 오류 수정(볼륨이 사용 중이면 다음 재부팅 시 실행 예약) |
| `/r` | 배드 섹터 찾기 및 복구(/f 포함). 시간이 오래 걸릴 수 있음 |
| `/x` | 필요 시 볼륨을 먼저 마운트 해제(NTFS, /f와 함께 사용) |
| `/v` | NTFS에서 정리 메시지 표시 |

## 예시

```
chkdsk C:
chkdsk C: /f
chkdsk D: /r
```

## 주의사항

- `/f`나 `/r`는 볼륨이 사용 중이면 즉시 실행되지 않고 재부팅 시 실행되도록 예약할 수 있다.
- 시스템 드라이브(C:)를 검사·수정할 때는 보통 재부팅이 필요하다. 중요한 작업은 저장하고 진행한다.
