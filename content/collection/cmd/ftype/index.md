---
draft: true
title: "[CMD] ftype - 파일 형식(연결) 명령 표시·수정"
description: "ftype 명령어는 Windows CMD에서 파일 형식(예: txtfile)에 대해 실행할 명령을 보여 주거나 설정할 때 사용합니다. assoc로 확장자와 형식을 연결한 뒤, ftype으로 열기 동작을 정의합니다."
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

ftype은 Windows 명령 프롬프트(CMD)에서 파일 형식(File Type)에 대해 실행할 기본 명령을 표시하거나 설정할 때 사용하는 내장 명령어이다. assoc로 확장자와 형식을 연결하고, ftype으로 그 형식을 열 때 쓸 명령줄(예: notepad.exe %1)을 지정한다.

## 사용법

```
ftype [파일형식[=[열기명령]]]
```

열기 명령에 %0, %1 등이 있으면 해당 자리에 파일 이름 등이 치환된다.

## 옵션

- 인수 없이 `ftype`만 쓰면 정의된 파일 형식 목록이 나온다.
- `파일형식=` 다음을 비우면 해당 형식의 명령을 삭제한다.

## 예시

```
ftype
ftype txtfile
ftype txtfile=notepad.exe %1
ftype mytype=C:\MyApp\open.exe "%1"
```

## 주의사항

- 시스템 기본 형식(txtfile, exefile 등)을 바꾸면 모든 사용자에게 영향을 주므로, 테스트는 사용자 단위 연결에서 하는 것이 안전하다.
- 경로에 공백이 있으면 따옴표로 감싼다.
