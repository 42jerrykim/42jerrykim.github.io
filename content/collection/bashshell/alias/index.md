---
draft: true
title: "[Bash Shell] alias - 명령 별칭"
description: "리눅스·유닉스 셸에서 명령에 별칭(alias)을 붙이는 방법, 영구 설정(.bashrc), 실무 예제를 다룹니다."
date: 2026-03-15
lastmod: 2026-03-15
categories:
- Bash Shell
tags:
- Bash
- Shell
- Linux
- 리눅스
- Terminal
- 터미널
- Command
- 셸
- Guide
- 가이드
- Tutorial
- 튜토리얼
- Reference
- 참고
- Quick-Reference
- File-System
- Process
- Automation
- 자동화
- Deployment
- 배포
- Error-Handling
- 에러처리
- Troubleshooting
- 트러블슈팅
- Workflow
- 워크플로우
- Best-Practices
- Documentation
- 문서화
- Configuration
- 설정
- Education
- 교육
- Technology
- 기술
- Productivity
- 생산성
- How-To
- Tips
- Beginner
- Advanced
- Comparison
- 비교
- Case-Study
- Deep-Dive
- 실습
- Review
- 리뷰
- Markdown
- 마크다운
- Open-Source
- 오픈소스
- History
- 역사
- alias
- 별칭
- .bashrc
- unalias
- profile
- 셸설정
- 단축키
- Shortcut
image: "tmp_wordcloud.png"
---

`alias`는 **명령에 짧은 이름**을 붙여서 쓸 수 있게 한다. 셸 내장 명령이며, `.bashrc` 등에 넣어 두면 로그인할 때마다 적용된다.

## 사용법

```bash
alias 이름='명령'
alias              # 목록 출력
unalias 이름       # 별칭 제거
```

## 예시

```bash
alias ll='ls -la'
alias g=git
alias ..='cd ..'
```

---

## 참고

- [Bash Manual: Aliases](https://www.gnu.org/software/bash/manual/html_node/Aliases.html)
