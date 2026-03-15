---
draft: true
title: "[CMD] ren (RENAME) - 파일·디렉터리 이름 변경"
description: "ren(RENAME)은 Windows CMD에서 파일이나 디렉터리의 이름을 바꿀 때 사용합니다. 와일드카드로 일괄 이름 변경이 가능하며, 다른 디렉터리로의 이동은 지원하지 않습니다."
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

ren 또는 RENAME은 Windows 명령 프롬프트(CMD)에서 파일 또는 디렉터리의 이름을 바꿀 때 사용하는 내장 명령어이다. 같은 디렉터리 내에서만 이름 변경이 가능하며, 이동은 하지 않는다.

## 사용법

```
ren [드라이브:][경로]원본이름 새이름
rename [드라이브:][경로]원본이름 새이름
```

## 옵션

- 별도 옵션 없이 원본 이름과 새 이름만 지정한다.
- 와일드카드(`*`, `?`)를 사용하면 여러 파일을 한 번에 이름 변경할 수 있다.

## 예시

```
ren report.txt report_2025.txt
ren *.txt *.bak
rename "Old Folder" "New Folder"
```

## 주의사항

- 대상(새 이름)에 경로를 넣을 수 없다. 같은 폴더 안에서만 이름이 바뀐다.
- 이동까지 하려면 move를 사용한다.
- 이름에 공백이 있으면 큰따옴표로 감싼다.
