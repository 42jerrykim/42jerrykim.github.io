---
draft: true
title: "[CMD] icacls - ACL 표시·수정·백업"
description: "icacls 명령어는 Windows CMD에서 파일·디렉터리의 ACL(액세스 제어 목록)을 표시, 수정, 백업, 복원할 때 사용합니다. 상속, 권한 상속 차단, 여러 사용자 일괄 적용을 지원합니다."
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

icacls는 Windows 명령 프롬프트(CMD)에서 파일과 디렉터리의 ACL(액세스 제어 목록)을 표시, 수정, 백업, 복원할 때 사용하는 명령어이다. cacls보다 기능이 많고, 상속(/grant, /deny, /inheritance), 하위 개체 적용(/t) 등을 지원한다.

## 사용법

```
icacls 파일이름 [/grant[:r] 사용자:권한 [...]] [/deny 사용자:권한 [...]] [/remove 사용자 [...]] [/t] [/c] [/l] [/q] [/reset] [/restore 파일] [/setowner 사용자]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| (없음) | ACL 표시 |
| `/grant [r] 사용자:권한` | 권한 부여. :r이면 상속된 권한을 대체 |
| `/deny 사용자:권한` | 권한 거부 |
| `/remove 사용자` | 사용자 ACE 제거 |
| `/t` | 하위 디렉터리·파일 포함 |
| `/reset` | 상속된 ACE를 기본으로 초기화 |
| `/restore 파일` | 백업 파일에서 ACL 복원 |
| `/save 파일` | ACL을 파일로 백업(다른 구문) |

권한: F(전체), M(수정), RX(읽기 및 실행), R(읽기), W(쓰기), D(삭제) 등.

## 예시

```
icacls myfile.txt
icacls C:\Data /grant Users:RX /t
icacls folder /save aclbackup.txt
icacls folder /restore aclbackup.txt
```

## 주의사항

- 시스템 디렉터리나 중요한 폴더의 ACL을 바꿀 때는 백업 후 진행하고, 테스트 환경에서 먼저 확인하는 것이 좋다. 관리자 권한이 필요할 수 있다.
