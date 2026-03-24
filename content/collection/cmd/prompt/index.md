---
draft: true
title: "[CMD] prompt - 프롬프트 문자열 변경"
description: "prompt 명령어는 Windows CMD에서 명령 프롬프트(예: C:\\>)에 표시되는 문자열을 변경할 때 사용합니다. $p 경로, $g >, $d 날짜 등 메타 문자와 사용자 정의 형식을 정리합니다."
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

prompt는 Windows 명령 프롬프트(CMD)에서 명령을 입력하기 전에 보이는 프롬프트 문자열을 변경할 때 사용하는 내장 명령어이다. $p(경로), $d(날짜), $t(시간), $g(>) 등 메타 문자를 조합해 원하는 형식을 만들 수 있다.

## 사용법

```
prompt [문자열]
```

문자열에 사용할 수 있는 메타 문자: $q=(등호), $$=$, $t=시간, $d=날짜, $p=현재 드라이브와 경로, $v=버전, $n=현재 드라이브, $g=>, $l=<, $b=|, $_=줄바꿈, $e=ESC, $a=&, $h=백스페이스 등.

## 예시

```
prompt $p$g
prompt [$t] $p$g
prompt
```

인수 없이 `prompt`만 쓰면 기본 프롬프트(보통 $p$g)로 복원된다.

## 주의사항

- 변경은 현재 CMD 세션에만 적용된다. 영구 반영은 레지스트리나 바로 가기에서 "시작 위치" 등으로 설정할 수 있다.
