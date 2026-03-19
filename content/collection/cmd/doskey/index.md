---
draft: true
title: "[CMD] doskey - 명령 편집·매크로"
description: "doskey 명령어는 Windows CMD에서 명령줄 편집, 이전 명령 불러오기(히스토리), 매크로 정의를 할 때 사용합니다. /reinstall, /macro, /history 등 옵션을 정리합니다."
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

doskey는 Windows 명령 프롬프트(CMD)에서 명령줄 버퍼(히스토리), 화살표로 이전 명령 불러오기, 매크로(단축 명령) 정의를 관리할 때 사용하는 명령어이다. CMD 창을 닫으면 매크로와 버퍼는 사라진다.

## 사용법

```
doskey [/reinstall] [/bufsize=크기] [/history] [/macros] [/macrofile=파일] [매크로이름=[텍스트]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/history` | 저장된 명령 목록(히스토리) 표시 |
| `/macros` | 현재 정의된 매크로 표시 |
| `/macrofile=파일` | 파일에 있는 매크로 정의 로드 |
| `이름=텍스트` | 매크로 정의. 텍스트에 $1, $* 등 인수 사용 가능 |
| `/reinstall` | doskey를 새로 로드(기본 버퍼·매크로 초기화) |

## 예시

```
doskey /history
doskey ls=dir $*
doskey up=cd ..
doskey /macrofile=mymacros.txt
```

## 주의사항

- 매크로 이름이 내장 명령과 같으면 해당 세션에서는 매크로가 우선한다. 혼동을 피하려면 다른 이름을 쓰는 것이 좋다.
- 영구적으로 쓰려면 시작 시 실행되는 스크립트나 레지스트리에서 doskey 매크로를 로드하도록 설정한다.
