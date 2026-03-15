---
draft: true
title: "[CMD] openfiles - 열린 파일 조회·연결 해제"
description: "openfiles 명령어는 Windows CMD에서 파일 공유로 열린 파일·폴더 목록을 보거나, 열린 파일 연결을 끊을 때 사용합니다. /query 조회, /disconnect 연결 해제, 로컬 모드 활성화 방법을 정리합니다."
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

openfiles는 Windows 명령 프롬프트(CMD)에서 원격 사용자가 파일 공유를 통해 열어 둔 파일 목록을 조회하거나, 특정 연결을 끊을 때 사용하는 명령어이다. 로컬에서 열린 파일을 보려면 "로컬 모드"를 활성화해야 하며, 재부팅이 필요할 수 있다.

## 사용법

```
openfiles /query [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/fo 형식] [/v]
openfiles /disconnect [[/s 컴퓨터] [/u 사용자 [/p 비밀번호]]] {/id id | /a 사용자 | /o 모드}
openfiles /local [on | off]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/query` | 열린 파일 목록 표시 |
| `/disconnect` | 지정한 연결 끊기. /id, /a(사용자), /o(열기 모드) 등 |
| `/local on|off` | 로컬에서 열린 파일 추적 사용 여부(재부팅 필요할 수 있음) |
| `/fo table|list|csv` | 출력 형식 |
| `/v` | 상세 정보 |

## 예시

```
openfiles /query
openfiles /disconnect /id 1
openfiles /local on
```

## 주의사항

- 로컬 모드(/local on)를 켜면 성능 영향이 있을 수 있고 재부팅이 필요하다. 주로 파일 서버에서 원격으로 열린 파일을 관리할 때 사용한다. 관리자 권한이 필요하다.
