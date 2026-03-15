---
draft: true
title: "[Bash Shell] grep - 패턴 검색"
description: "리눅스·유닉스에서 텍스트와 정규식 패턴 검색에 쓰이는 grep 명령어의 사용법, 주요 옵션(-i, -r, -n 등), 실무 예제와 파이프 조합을 상세히 다룹니다. 로그 분석과 코드 검색에 바로 활용할 수 있습니다."
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
- grep
- 패턴검색
- 정규식
- Regex
- 필터
- 텍스트처리
- 로그분석
- 검색
- 매칭
- ERE
- BRE
- 파이프
- Pipeline
image: "tmp_wordcloud.png"
---

`grep`(global regular expression print)은 리눅스·유닉스에서 **패턴에 맞는 줄**을 검색해 출력하는 필터 명령어다. 파일 내용 검색, 파이프와 결합한 로그·코드 검색, 정규식 활용까지 실무에서 가장 자주 쓰는 도구 중 하나다.

## 사용법

```bash
grep [옵션] 패턴 [파일...]
```

- **패턴**: 검색할 문자열 또는 정규식. 여러 파일을 지정하면 파일별로 매칭된 줄을 출력한다.
- **파일**: 생략 시 표준 입력에서 읽는다. 디렉터리는 지정할 수 없고, 재귀 검색은 `-r` 옵션으로 한다.

## 옵션

### 매칭 방식

| 옵션 | 설명 |
|------|------|
| `-E`, `--extended-regexp` | 확장 정규식(ERE) 사용 |
| `-F`, `--fixed-strings` | 패턴을 고정 문자열로 취급(정규식 비활성화) |
| `-G`, `--basic-regexp` | 기본 정규식(BRE, 기본값) |
| `-P`, `--perl-regexp` | Perl 정규식(일부 환경에서만 지원) |
| `-i`, `--ignore-case` | 대소문자 구분 없이 검색 |

### 출력 제어

| 옵션 | 설명 |
|------|------|
| `-n`, `--line-number` | 줄 번호 출력 |
| `-c`, `--count` | 매칭된 줄 개수만 출력 |
| `-l`, `--files-with-matches` | 매칭이 있는 파일 이름만 출력 |
| `-L`, `--files-without-match` | 매칭이 없는 파일 이름만 출력 |
| `-v`, `--invert-match` | 패턴에 **매칭되지 않는** 줄만 출력 |
| `-o`, `--only-matching` | 매칭된 부분만 출력 |
| `-h`, `--no-filename` | 여러 파일일 때 파일명 생략 |
| `-H`, `--with-filename` | 항상 파일명 출력(기본: 파일이 2개 이상일 때만) |

### 검색 범위

| 옵션 | 설명 |
|------|------|
| `-r`, `-R`, `--recursive` | 하위 디렉터리까지 재귀 검색 |
| `--include=GLOB` | 재귀 시 GLOB에 맞는 파일만 검색 |
| `--exclude=GLOB` | GLOB에 맞는 파일 제외 |
| `--exclude-dir=DIR` | 지정 디렉터리 제외 |

### 기타

| 옵션 | 설명 |
|------|------|
| `-w`, `--word-regexp` | 단어 단위 매칭(단어 경계 적용) |
| `-x`, `--line-regexp` | 줄 전체가 패턴과 일치할 때만 |
| `-A N`, `--after-context=N` | 매칭 줄 뒤 N줄까지 출력 |
| `-B N`, `--before-context=N` | 매칭 줄 앞 N줄까지 출력 |
| `-C N`, `--context=N` | 매칭 줄 앞뒤 N줄 출력 |
| `--color[=WHEN]` | 매칭 부분 강조. WHEN: never, always, auto |

## 예시

### 기본 검색

```bash
# 파일에서 "error" 포함 줄 출력
grep "error" /var/log/syslog

# 대소문자 무시
grep -i "ERROR" app.log

# 줄 번호와 함께
grep -n "TODO" src/*.c
```

### 재귀·파일 제한

```bash
# 현재 디렉터리 아래 모든 텍스트 파일에서 검색
grep -r "function_name" .

# .git 제외하고 재귀 검색
grep -r --exclude-dir=.git "pattern" .

# .c, .h 파일만
grep -r --include="*.c" --include="*.h" "main" src/
```

### 개수·파일명만

```bash
# 각 파일별 매칭 줄 수
grep -c "warning" *.log

# 매칭이 하나라도 있는 파일 이름만
grep -l "deprecated" src/*.py
```

### 반전·단어 단위

```bash
# "debug"가 **없는** 줄만
grep -v "debug" config.ini

# 단어 "cat"만( "category", "catch" 제외)
grep -w "cat" words.txt
```

### 정규식(ERE)

```bash
# 확장 정규식: 숫자로 시작하는 줄
grep -E "^[0-9]+" data.txt

# 이메일 형태 줄만
grep -E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" contacts.txt
```

### 파이프 조합

```bash
# ps 출력에서 프로세스명 필터
ps aux | grep nginx

# 히스토리에서 명령 검색
history | grep "git commit"

# 에러 줄만 모아서 개수
cat build.log | grep -i error | wc -l
```

### 컨텍스트(앞뒤 줄)

```bash
# 매칭 줄 앞뒤 2줄씩
grep -C 2 "Exception" app.log

# 매칭 뒤 5줄만
grep -A 5 "stack trace" error.log
```

## 참고

- [GNU grep 매뉴얼](https://www.gnu.org/software/grep/manual/grep.html)
- [grep (Unix) - Wikipedia](https://en.wikipedia.org/wiki/Grep)
