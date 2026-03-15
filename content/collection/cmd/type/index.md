---
draft: true
title: "[CMD] type - 텍스트 파일 내용 표시"
description: "type 명령어는 Windows CMD에서 텍스트 파일의 내용을 콘솔에 그대로 출력할 때 사용합니다. 여러 파일을 이어서 출력하는 방법과 파이프·리다이렉트와의 조합을 정리합니다."
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

type은 Windows 명령 프롬프트(CMD)에서 텍스트 파일의 내용을 콘솔에 출력하는 내장 명령어이다. 바이너리 파일에 사용하면 깨진 문자가 나올 수 있으므로, 주로 .txt 등 텍스트 파일에 쓴다. 유닉스의 cat과 비슷한 역할이다.

## 사용법

```
type [드라이브:][경로]파일이름
```

## 옵션

- type에는 별도 옵션이 없다. 와일드카드로 여러 파일을 지정하면 순서대로 이어서 출력된다.

## 예시

```
type readme.txt
type *.log
type file1.txt file2.txt
```

## 주의사항

- 출력이 길면 `type file.txt | more`로 한 화면씩 볼 수 있다.
- 리다이렉트로 다른 파일에 저장할 수 있다: `type a.txt > b.txt`.
- UTF-8 등 인코딩에 따라 한글이 깨질 수 있으면 chcp로 코드 페이지를 맞추거나 PowerShell Get-Content를 고려한다.
