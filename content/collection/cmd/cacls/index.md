---
draft: true
title: "[CMD] cacls - ACL 표시·수정 (레거시)"
description: "cacls 명령어는 Windows CMD에서 파일·디렉터리의 ACL(액세스 제어 목록)을 표시하거나 수정할 때 사용합니다. icacls가 권장되며, cacls는 레거시 호환용으로 남아 있습니다."
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

cacls(Change Access Control List)는 Windows 명령 프롬프트(CMD)에서 파일 또는 디렉터리의 ACL(액세스 제어 목록)을 표시하거나 수정할 때 사용하는 레거시 명령어이다. 새 스크립트에서는 icacls 사용이 권장되며, cacls는 간단한 권한 보기·변경에 여전히 쓸 수 있다.

## 사용법

```
cacls 파일이름 [/t] [/e] [/g 사용자:권한] [/r 사용자 [...]] [/p 사용자:권한 [...]] [/d 사용자 [...]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| (없음) | ACL 표시 |
| `/t` | 하위 디렉터리·파일 포함 |
| `/e` | 기존 ACL 편집(삭제하지 않고 수정) |
| `/g 사용자:권한` | 사용자에게 권한 부여 |
| `/r 사용자` | 사용자 권한 제거 |
| `/p 사용자:권한` | 사용자 권한 교체 |

권한: R 읽기, W 쓰기, C 변경, F 전체 제어.

## 예시

```
cacls myfile.txt
cacls C:\Data /e /g Users:R
cacls /t /e /p User2:F folder
```

## 주의사항

- 상속·고급 권한 등은 icacls가 더 잘 지원한다. 복잡한 ACL 작업은 icacls를 사용한다.
