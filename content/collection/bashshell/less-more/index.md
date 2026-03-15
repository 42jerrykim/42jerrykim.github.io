---
draft: true
title: "[Bash Shell] less, more - 페이징 뷰어"
description: "리눅스·유닉스에서 긴 출력을 한 화면씩 보는 less와 more의 사용법, 검색·스크롤·실시간 추적 등 옵션과 단축키를 다룹니다."
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
- String
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
- less
- more
- pager
- 페이징
- 뷰어
- 스크롤
image: "tmp_wordcloud.png"
---

`less`와 `more`는 **긴 텍스트**를 한 화면(페이지)씩 보여주는 **페이저**다. `less`가 위아래 스크롤·검색 등이 더 풍부해 실무에서는 `less`를 더 많이 쓴다.

## less

### 사용법

```bash
less [옵션] [파일...]
```

### 자주 쓰는 동작 (실행 중)

| 키 | 동작 |
|----|------|
| Space, Page Down | 다음 페이지 |
| b, Page Up | 이전 페이지 |
| /패턴 | 아래로 검색 |
| ?패턴 | 위로 검색 |
| n, N | 다음/이전 검색 결과 |
| g, G | 맨 앞/맨 뒤로 |
| q | 종료 |
| F | 파일 끝 추적 (tail -f처럼) |

### 예시

```bash
less longfile.txt
ls -l | less
```

---

## more

### 사용법

```bash
more [옵션] [파일...]
```

- 아래로만 진행 가능한 경우가 많고, `less`보다 기능이 적다.
- Space로 다음 페이지, q로 종료.

---

## 참고

- [less(1) - Linux man page](https://man7.org/linux/man-pages/man1/less.1.html)
