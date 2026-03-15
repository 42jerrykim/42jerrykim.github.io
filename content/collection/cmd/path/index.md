---
draft: true
title: "[CMD] path - 실행 파일 검색 경로"
description: "path 명령어는 Windows CMD에서 PATH 환경 변수를 표시하거나 설정할 때 사용합니다. 현재 세션에서만 변경하거나 영구적으로 시스템·사용자 환경 변수에 반영하는 방법을 정리합니다."
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

path는 Windows 명령 프롬프트(CMD)에서 실행 파일을 찾을 디렉터리 목록(PATH 환경 변수)을 표시하거나 설정할 때 사용하는 내장 명령어이다. 인수 없이 쓰면 현재 PATH가 출력된다.

## 사용법

```
path [[드라이브:]경로[;...]] [/v]
path ;
```

## 옵션

| 사용 | 설명 |
|------|------|
| `path` | 현재 PATH 표시 |
| `path 새경로` | PATH를 새 경로로 설정(기존 값 대체) |
| `path %path%;새경로` | 기존 PATH 뒤에 경로 추가 |
| `path ;` | PATH를 비움(현재 세션만) |
| `/v` | 설정 시 각 경로를 화면에 출력 |

## 예시

```
path
path C:\Tools;D:\Bin;%path%
path ;
```

## 주의사항

- path로 변경한 내용은 현재 CMD 세션에만 적용된다. 영구 반영은 setx나 시스템 속성의 환경 변수에서 설정한다.
- 경로 구분자는 세미콜론(;)이다.
