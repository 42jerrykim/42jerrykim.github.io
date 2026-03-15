---
draft: true
title: "[CMD] fc - 파일 비교"
description: "fc 명령어는 Windows CMD에서 두 파일 또는 두 집합의 파일을 바이트·줄 단위로 비교하여 차이를 표시할 때 사용합니다. /b 바이너리, /l 텍스트 모드, /n 줄 번호 옵션을 정리합니다."
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

fc(File Compare)는 Windows 명령 프롬프트(CMD)에서 두 파일을 비교하여 차이를 보여 주는 명령어이다. 텍스트 모드(기본)에서는 줄 단위로, 바이너리 모드(/b)에서는 바이트 단위로 비교한다.

## 사용법

```
fc [/a] [/b] [/c] [/l] [/lb n] [/n] [/t] [/u] [/w] [/nnnn] [드라이브1:][경로1]파일1 [드라이브2:][경로2]파일2
fc /b [드라이브1:][경로1]파일1 [드라이브2:][경로2]파일2
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/a` | ASCII 비교 요약만 표시 |
| `/b` | 바이너리 비교 |
| `/l` | 텍스트(줄) 모드로 비교(기본) |
| `/n` | 줄 번호 표시 |
| `/w` | 연속 공백을 하나로 간주 |
| `nnnn` | 일치하는 연속 줄 수(기본 2). 이 수만큼 연속 일치하면 차이 출력에서 생략 |

## 예시

```
fc file1.txt file2.txt
fc /b image1.bin image2.bin
fc /n /w old.log new.log
```

## 주의사항

- 차이가 없으면 "차이 없음" 메시지만 나온다. 차이가 있으면 exit code가 1이다.
- 매우 큰 파일은 비교 시간이 오래 걸릴 수 있다.
