---
draft: true
title: "[CMD] gpresult - 그룹 정책 결과"
description: "gpresult 명령어는 Windows CMD에서 현재 사용자 또는 컴퓨터에 적용된 그룹 정책(RSoP) 결과를 표시할 때 사용합니다. /r 요약, /v 상세, /h HTML 보고서, 원격 사용자·컴퓨터 지정을 정리합니다."
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

gpresult는 Windows 명령 프롬프트(CMD)에서 사용자 또는 컴퓨터에 적용된 그룹 정책(Group Policy) 결과(RSoP)를 표시할 때 사용하는 명령어이다. 도메인·로컬 정책 적용 결과, 적용된 GPO 목록 등을 확인할 수 있다.

## 사용법

```
gpresult [/s 컴퓨터] [/u 사용자 [/p 비밀번호]] [/scope user|computer] [/r] [/v] [/z] [/x 출력파일] [/h 출력파일]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/r` | 사용자·컴퓨터에 대한 요약(정책 적용 요약) |
| `/v` | 상세 정보 |
| `/z` | 최대 상세(매우 긴 출력) |
| `/h 파일` | HTML 보고서로 저장 |
| `/scope user|computer` | 사용자 또는 컴퓨터 정책만 |
| `/s 컴퓨터` | 원격 컴퓨터 |

## 예시

```
gpresult /r
gpresult /v
gpresult /h report.html
gpresult /s server01 /u DOMAIN\user /r
```

## 주의사항

- 원격 컴퓨터를 조회하려면 해당 머신에 대한 권한이 필요하다. 도메인 환경에서 그룹 정책 문제 해결 시 유용하다.
