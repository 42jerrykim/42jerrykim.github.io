---
draft: true
title: "[CMD] move - 파일·디렉터리 이동 및 이름 변경"
description: "move 명령어는 Windows CMD에서 파일이나 디렉터리를 다른 위치로 옮기거나 이름을 바꿀 때 사용합니다. /y 덮어쓰기 확인 생략, 드라이브 간 이동 시 동작을 정리합니다."
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

move는 Windows 명령 프롬프트(CMD)에서 파일 또는 디렉터리를 다른 경로로 이동하거나, 같은 디렉터리 내에서 이름을 바꿀 때 사용하는 내장 명령어이다. 유닉스의 mv와 역할이 비슷하다.

## 사용법

```
move [/y | /-y] [드라이브:][경로]파일명 [대상]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/y` | 덮어쓸 때 확인하지 않음 |
| `/-y` | 덮어쓸 때 확인 요청(기본값) |

## 예시

```
move report.txt D:\Backup\
move oldname.txt newname.txt
move C:\Data\*.log C:\Logs\
```

## 주의사항

- 같은 드라이브 내에서는 실제로 데이터를 옮기지 않고 디렉터리 항목(메타데이터)만 변경된다.
- 서로 다른 드라이브 간에는 복사 후 원본이 삭제되는 방식으로 동작한다.
- 디렉터리 이름 변경도 같은 드라이브에서 move로 할 수 있다.
