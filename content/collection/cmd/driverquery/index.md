---
draft: true
title: "[CMD] driverquery - 드라이버 목록"
description: "driverquery 명령어는 Windows CMD에서 설치된 장치 드라이버 목록을 표시할 때 사용합니다. /v 상세 정보, /fo 형식, 원격 컴퓨터 지정으로 드라이버 상태를 점검할 수 있습니다."
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

driverquery는 Windows 명령 프롬프트(CMD)에서 현재 컴퓨터(또는 원격 컴퓨터)에 설치된 장치 드라이버 목록을 표시할 때 사용하는 명령어이다. 모듈 이름, 표시 이름, 드라이버 유형, 링크 날짜 등을 볼 수 있다.

## 사용법

```
driverquery [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/fo 형식] [/nh] [/v] [/si]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/fo table|list|csv` | 출력 형식 |
| `/nh` | 테이블일 때 열 머리글 생략 |
| `/v` | 상세 정보 표시 |
| `/si` | 서명된 드라이버 정보 포함 |
| `/s 컴퓨터` | 원격 컴퓨터 |

## 예시

```
driverquery
driverquery /v
driverquery /fo csv
driverquery /s server01
```

## 주의사항

- 원격 조회 시 권한과 방화벽이 허용되어 있어야 한다. 관리자 권한이 필요할 수 있다.
