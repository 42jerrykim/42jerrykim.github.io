---
draft: true
title: "[Bash Shell] man, history - 매뉴얼·명령 히스토리"
description: "리눅스·유닉스에서 명령·함수 매뉴얼을 보는 man과 셸 명령 히스토리를 다루는 history의 사용법, 섹션·검색·히스토리 확장 등 실무 예제를 다룹니다."
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
- man
- history
- 매뉴얼
- manual
- 히스토리
- HISTFILE
- 문서
image: "wordcloud.png"
---

`man`은 **매뉴얼 페이지**를 보여주고, `history`는 **셸 명령 히스토리**를 출력·검색·재사용할 때 쓴다.

---

## man — 매뉴얼 보기

### 사용법

```bash
man [섹션] 이름
man -k 검색어
```

### 섹션 (일반적)

| 섹션 | 내용 |
|------|------|
| 1 | 사용자 명령 |
| 2 | 시스템 콜 |
| 3 | 라이브러리 함수 |
| 5 | 파일 형식 |
| 8 | 관리자 명령 |

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-k 키워드` | 설명에 키워드가 포함된 페이지 검색 (apropos와 유사) |
| `-f 이름` | 이름에 해당하는 페이지 요약 (whatis와 유사) |
| `-a` | 모든 섹션 순서대로 표시 |

### 예시

```bash
man ls
man 2 open
man -k "sort"
```

---

## history — 명령 히스토리

### 사용법

```bash
history [n]
history -c
```

- 인자 없으면 히스토리 목록 출력.
- `n`을 주면 최근 n개만.
- `-c`는 현재 셸의 히스토리를 비운다 (파일은 보통 그대로).

### 히스토리 확장 (Bash)

- `!!`: 직전 명령
- `!n`: n번째 명령
- `!$`: 직전 명령의 마지막 인자
- `!*`: 직전 명령의 모든 인자

### 예시

```bash
history
history 20
!!              # 직전 명령 다시 실행
!$              # 직전 명령의 마지막 인자
```

---

## 참고

- [man(1) - Linux man page](https://man7.org/linux/man-pages/man1/man.1.html)
- [Bash Manual: History Builtins](https://www.gnu.org/software/bash/manual/html_node/History-Builtins.html)
