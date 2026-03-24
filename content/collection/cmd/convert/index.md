---
draft: true
title: "[CMD] convert - FAT 볼륨을 NTFS로 변환"
description: "convert 명령어는 Windows CMD에서 FAT/FAT32 볼륨을 NTFS로 변환할 때 사용합니다. 현재 드라이브는 변환할 수 없으며, 데이터는 유지된 채 파일 시스템만 바뀝니다."
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

convert는 Windows 명령 프롬프트(CMD)에서 FAT 또는 FAT32로 포맷된 볼륨을 NTFS로 변환할 때 사용하는 명령어이다. 데이터를 지우지 않고 파일 시스템만 변환하며, 변환 중에는 해당 드라이브를 사용하지 않는 것이 좋다.

## 사용법

```
convert [드라이브:] /fs:ntfs [/v] [/cvtarea:파일이름] [/x]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/fs:ntfs` | NTFS로 변환(필수) |
| `/v` | 자세한 메시지 출력 |
| `/x` | 필요 시 볼륨을 먼저 마운트 해제 |

## 예시

```
convert D: /fs:ntfs
convert E: /fs:ntfs /v
```

## 주의사항

- **현재 드라이브(예: C:)는 변환할 수 없다.** 변환은 다음 부팅 시에 예약될 수 있다.
- 변환 전에 가능하면 백업을 해 두고, 변환 중에는 해당 드라이브에 쓰기 작업을 하지 않는다.
