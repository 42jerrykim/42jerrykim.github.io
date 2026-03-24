---
draft: true
title: "[Bash Shell] which, whereis, locate - 명령·파일 위치 검색"
description: "리눅스·유닉스에서 실행 파일 경로를 찾는 which, 바이너리·매뉴얼을 찾는 whereis, 파일명 DB로 검색하는 locate의 사용법과 차이를 다룹니다."
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
- which
- whereis
- locate
- PATH
- 실행파일
- 검색
image: "wordcloud.png"
---

`which`는 **PATH 기준 실행 파일** 경로를, `whereis`는 **바이너리·매뉴얼·소스** 위치를, `locate`는 **미리 만든 DB**로 파일명을 빠르게 검색한다.

---

## which — PATH에서 실행 파일

### 사용법

```bash
which [-a] 명령...
```

- `-a`: PATH에서 찾은 **모든** 경로 출력.

### 예시

```bash
which python
which -a python
```

---

## whereis — 바이너리·매뉴얼·소스

### 사용법

```bash
whereis [-bmsu] 이름...
```

- `-b`: 바이너리, `-m`: 매뉴얼, `-s`: 소스 (시스템에 있을 때).

### 예시

```bash
whereis ls
whereis -b grep
```

---

## locate — 파일명 DB 검색

### 사용법

```bash
locate [옵션] 패턴...
```

- **updatedb**로 만든 DB를 검색해 매우 빠르다. 최신 생성 파일은 DB에 없을 수 있다.
- `-i`: 대소문자 무시. `-n N`: 최대 N개만.

### 예시

```bash
locate "*.conf"
locate -i readme
sudo updatedb   # DB 갱신 (주기적 크론 등)
```

---

## 참고

- [which(1)], [whereis(1)], [locate(1)] — man 페이지
