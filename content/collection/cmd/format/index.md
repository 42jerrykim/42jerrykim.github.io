---
draft: true
title: "[CMD] format - 볼륨 포맷"
description: "format 명령어는 Windows CMD에서 디스크 볼륨을 포맷할 때 사용합니다. /fs 파일시스템, /q 빠른 포맷, /v 레이블, 주의할 점과 데이터 손실 경고를 정리합니다."
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

format은 Windows 명령 프롬프트(CMD)에서 지정한 드라이브(볼륨)를 포맷할 때 사용하는 명령어이다. NTFS, FAT32 등 파일 시스템을 지정하고, 빠른 포맷(/q) 또는 전체 포맷을 할 수 있다. **포맷하면 해당 볼륨의 데이터가 삭제된다.**

## 사용법

```
format 볼륨: [/fs:파일시스템] [/v:레이블] [/q] [/a:단위크기] [/c] [/x]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/fs:ntfs|fat32|exfat` | 파일 시스템 지정 |
| `/v:레이블` | 볼륨 레이블 |
| `/q` | 빠른 포맷(볼륨만 지우고 재생성, 전체 지우기 아님) |
| `/x` | 필요 시 볼륨을 먼저 마운트 해제 |

## 예시

```
format D: /fs:ntfs /v:Data /q
format E: /fs:fat32
```

## 주의사항

- 시스템 드라이브(C:)나 사용 중인 볼륨은 포맷할 수 없다. 대상 드라이브와 데이터 백업을 반드시 확인한다.
- `/q`는 디스크 표면 검사를 생략하므로, 새 디스크가 아니면 전체 포맷을 권장할 수 있다.
