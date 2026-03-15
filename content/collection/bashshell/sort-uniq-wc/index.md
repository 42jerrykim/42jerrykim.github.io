---
draft: true
title: "[Bash Shell] sort, uniq, wc - 정렬·중복 제거·줄·단어 수"
description: "리눅스·유닉스에서 줄 단위 정렬 sort, 연속 중복 제거 uniq, 줄·단어·바이트 수를 세는 wc의 사용법과 옵션, 파이프 조합 실무 예제를 다룹니다."
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
- sort
- uniq
- wc
- 정렬
- 중복제거
- 줄수
- 단어수
- word-count
- Pipeline
image: "tmp_wordcloud.png"
---

`sort`는 **줄 단위 정렬**, `uniq`는 **연속된 동일 줄**만 제거·집계하고, `wc`는 **줄·단어·바이트 수**를 센다. 파이프로 묶어 로그·텍스트 처리에 자주 쓴다.

---

## sort — 정렬

### 사용법

```bash
sort [옵션] [파일...]
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-n`, `--numeric-sort` | 숫자로 정렬 |
| `-r`, `--reverse` | 역순 |
| `-k N` | N번째 필드 기준 정렬 |
| `-t C` | 필드 구분자 C |
| `-u`, `--unique` | 정렬 후 중복 줄 제거 |
| `-o FILE` | 결과를 FILE로 저장 |

### 예시

```bash
sort names.txt
sort -n numbers.txt
sort -r file.txt
sort -t: -k3 -n /etc/passwd   # 세 번째 필드(숫자) 기준
```

---

## uniq — 연속 중복 처리

### 사용법

```bash
uniq [옵션] [입력 [출력]]
```

**연속된** 동일 줄만 하나로 합친다. 미리 `sort`로 정렬한 뒤 쓰는 경우가 많다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-c`, `--count` | 연속 반복 횟수 출력 |
| `-d`, `--repeated` | 중복된 줄만 출력 |
| `-u`, `--unique` | 중복 없는 줄만 출력 |
| `-i` | 대소문자 무시 |

### 예시

```bash
sort file.txt | uniq
sort file.txt | uniq -c
```

---

## wc — 줄·단어·바이트 수

### 사용법

```bash
wc [옵션] [파일...]
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-l`, `--lines` | 줄 수만 |
| `-w`, `--words` | 단어 수만 |
| `-c`, `--bytes` | 바이트 수만 |
| `-m`, `--chars` | 문자 수 |

### 예시

```bash
wc -l access.log
cat file.txt | wc -w
```

---

## 참고

- [GNU coreutils: sort, uniq, wc](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)
