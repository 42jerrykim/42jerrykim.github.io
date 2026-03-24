---
draft: true
title: "[CMD] chkntfs - 부팅 시 디스크 검사 설정"
description: "chkntfs 명령어는 Windows CMD에서 부팅 시 자동 디스크 검사(chkdsk)가 실행되도록 예약된 볼륨을 보거나, 해당 예약을 설정·해제할 때 사용합니다. /d 기본 동작 복원, /x 볼륨 제외를 정리합니다."
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

chkntfs는 Windows 명령 프롬프트(CMD)에서 부팅 시 자동으로 chkdsk가 실행되도록 예약된 볼륨을 조회하거나, 예약을 설정·해제할 때 사용하는 명령어이다. /x로 특정 볼륨을 다음 부팅 시 검사에서 제외할 수 있다.

## 사용법

```
chkntfs [볼륨: [...]]
chkntfs /d
chkntfs /t[:시간]
chkntfs /x 볼륨: [...]
chkntfs /c 볼륨: [...]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| 볼륨: | 해당 볼륨의 예약 상태 표시 |
| `/d` | 기본 동작 복원(모든 드라이브가 부팅 시 검사 대상이 됨) |
| `/t:초` | 자동 chkdsk 실행 전 카운트다운 시간(기본 10초) |
| `/x 볼륨:` | 해당 볼륨을 다음 부팅 시 검사에서 제외 |
| `/c 볼륨:` | 해당 볼륨을 다음 부팅 시 검사하도록 예약 |

## 예시

```
chkntfs C:
chkntfs /x C:
chkntfs /d
```

## 주의사항

- `/x`로 제외한 볼륨은 해당 부팅에서만 제외되고, `/d`를 실행하면 기본으로 돌아간다. 관리자 권한이 필요할 수 있다.
