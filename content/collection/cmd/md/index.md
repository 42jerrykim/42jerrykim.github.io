---
draft: true
title: "[CMD] md (MKDIR) - 디렉터리 만들기"
description: "md(MKDIR)는 Windows CMD에서 새 디렉터리(폴더)를 만들 때 사용합니다. 한 번에 여러 단계의 하위 디렉터리를 생성하는 방법과 유닉스 mkdir -p와의 차이를 정리합니다."
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

md 또는 MKDIR은 Windows 명령 프롬프트(CMD)에서 새 디렉터리(폴더)를 만들 때 사용하는 내장 명령어이다. 둘은 동일한 명령이며, 유닉스/Linux의 mkdir과 역할이 비슷하다.

## 사용법

```
mkdir [드라이브:][경로]이름
md [드라이브:][경로]이름
```

## 옵션

- CMD의 md/mkdir은 별도 옵션 없이 경로만 지정한다.
- 중간 경로가 없어도 한 번에 여러 단계를 만들 수 있다(예: `md A\B\C`).

## 예시

```
md NewFolder
md D:\Projects\2025\January
mkdir "Folder With Spaces"
```

## 주의사항

- 이미 같은 이름의 디렉터리가 있으면 오류가 난다.
- 경로에 공백이 있으면 큰따옴표로 감싼다.
- 빈 디렉터리 삭제는 rmdir(rd)를 사용한다.
