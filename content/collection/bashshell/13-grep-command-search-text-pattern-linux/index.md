---
draft: false
slug: grep
title: "[Bash Shell] 13. grep - 패턴 검색"
description: "리눅스·유닉스에서 텍스트와 정규식 패턴을 검색하는 grep 명령어의 사용법과 매칭·출력·검색범위별 옵션(-i, -r, -n, -E 등)을 그룹별 표로 정리하고, 파이프·리다이렉션 조합 예제 7가지와 GNU/BSD 이식성 차이, 종료 코드 등 실무 함정까지 다룹니다."
date: 2026-03-15
lastmod: 2026-08-22
collection_order: 130
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Automation(자동화)
- Process
- String(문자열)
- Pipe(파이프)
- Pipeline
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Full-Text-Search(전문검색)
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
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
image: "wordcloud.png"
---

`grep`(global regular expression print)은 리눅스·유닉스에서 **패턴에 맞는 줄**을 검색해 출력하는 필터 명령어다. 파일 내용 검색, 파이프와 결합한 로그·코드 검색, 정규식 활용까지 실무에서 가장 자주 쓰는 도구 중 하나다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [12장: man, history](/post/bashshell/man-history/)에서 매뉴얼로 명령어 사용법을 찾고 히스토리로 과거 명령을 검색하는 법을 다룬 뒤 이어진다. 여기서부터 <strong>Part 2(텍스트 처리)</strong>가 시작된다 — [3장: cat](/post/bashshell/cat/)으로 파일을 읽고 [12장: man](/post/bashshell/man-history/)으로 궁금한 점을 찾아본 다음, 이제 그 파일 안에서 원하는 줄을 실제로 찾아내는 단계로 넘어가는 자연스러운 흐름이다. `grep`은 파이프라인의 첫 필터로 가장 자주 등장하므로, 파이프(`|`)가 무엇인지 대략 감이 있으면(자세한 내용은 19장에서 다룬다) 예시를 읽기 더 수월하다.

**이 장의 깊이**: **입문–중급** 난이도다. 기본 매칭부터 재귀 검색, ERE 정규식, 컨텍스트 출력까지 실무에서 매일 쓰는 범위를 다룬다. **다루지 않는 것**: 정규식 문법 자체의 심화(POSIX ERE 전체 메타문자, 캡처 그룹, 룩어라운드 등)는 각주 수준으로만 언급하고, grep으로 찾은 줄을 실제로 바꿔치는 스트림 편집(치환)은 [14장: sed](/post/bashshell/sed/)에서 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 로그·코드 검색이 급한 사람 | "사용법" ~ "예시"의 "기본 검색"·"재귀·파일 제한"·"파이프 조합" | 자주 쓰는 옵션 조합으로 로그·소스코드에서 원하는 줄을 바로 찾아낸다 |
| 정규식을 제대로 배우려는 사람 | "옵션"의 "매칭 방식"부터 "예시"의 "정규식(ERE)", "주의사항·함정" 전체 | BRE/ERE/Perl 정규식의 차이와 이식성 함정까지 이해하고 상황에 맞는 매칭 방식을 선택한다 |

---

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

## 주의사항·함정

`grep`은 배포판·운영체제마다 실제 동작이 미묘하게 달라, 스크립트를 옮겨 실행하는 순간 함정이 드러나는 경우가 많다.

**GNU vs BSD/macOS 이식성**: 이 글의 예시는 리눅스 배포판 대부분이 쓰는 **GNU grep** 기준이다. macOS 기본 `grep`은 GNU가 아니라 BSD grep 계열이라 옵션 지원 범위가 다르다. 특히 `-P`(Perl 정규식)는 GNU grep이 PCRE를 링크해 제공하는 확장으로, POSIX 표준 자체에 없는 기능이라 BSD/macOS grep에서는 대부분 지원하지 않는다(`grep -P` 실행 시 "invalid option" 류 에러가 난다). macOS에서 GNU grep과 동일하게 동작시키려면 Homebrew로 `brew install grep`을 설치해 `ggrep`(또는 `PATH`에 `gnubin` 우선 배치)으로 실행해야 한다. `-r`과 `-R`도 미묘하게 다르다 — GNU grep에서 `-r`은 명령줄에 직접 준 심볼릭 링크만 따라가고, `-R`(`--dereference-recursive`)은 하위 디렉터리에서 만나는 모든 심볼릭 링크까지 따라간다. 이 차이를 모르고 `-r`을 쓰면 심볼릭 링크로 연결된 디렉터리가 검색에서 조용히 빠질 수 있다.

**셸 인용·이스케이프**: 패턴에 `$`, `*`, `[`, `]`, `(`, `)` 같은 정규식 메타문자가 들어가면 반드시 작은따옴표(`'...'`)로 감싸야 한다. 큰따옴표나 무인용 상태로 두면 셸이 grep에 패턴을 넘기기 전에 와일드카드 확장·변수 치환을 먼저 시도해, 의도와 다른 파일 목록이나 빈 문자열이 전달될 수 있다. 또한 기본 정규식(BRE)에서는 `+`, `?`, `|`, `(`, `)`가 리터럴 문자로 취급되고 메타문자로 쓰려면 `\+`처럼 백슬래시를 붙여야 한다 — `-E`(ERE)를 쓰면 이 이스케이프가 필요 없어지므로, BRE와 ERE를 섞어 쓰다 이스케이프를 빠뜨리는 실수가 흔하다.

**종료 코드**: `grep`은 매칭된 줄이 있으면 0, 없으면 1, 파일을 못 열었거나 문법 오류가 있으면 2 이상을 반환한다. `if grep "pattern" file; then ...`처럼 쓰면 "매치 없음"도 셸 입장에서는 실패(1)이므로, 매치가 없는 것이 정상 상황인 로직에서는 `if ! grep -q "pattern" file; then ...`처럼 의도를 명확히 해야 한다. `set -e`가 걸린 스크립트에서 파이프 중간에 매치 없는 `grep`을 두면 스크립트 전체가 예상치 못하게 종료될 수 있어, `grep ... || true`로 의도적으로 무시하거나 종료 코드를 직접 검사하는 편이 안전하다.

## 다음 장에서는

다음은 [14장: sed](/post/bashshell/sed/) — `grep`으로 찾은 줄을 이번에는 그대로 바꿔치는 스트림 편집을 다룬다.

## 평가 기준

- BRE·ERE·고정 문자열(`-F`) 매칭 방식의 차이를 설명할 수 있다.
- 재귀 검색(`-r`/`-R`)과 파일 포함·제외(`--include`/`--exclude`) 옵션을 조합해 원하는 범위만 검색할 수 있다.
- 파이프와 결합해 프로세스 목록·로그·히스토리에서 원하는 줄을 걸러낼 수 있다.
- GNU grep과 BSD/macOS grep의 옵션 차이를 구분하고, 스크립트를 옮길 때 어떤 부분을 점검해야 하는지 설명할 수 있다.
- `grep`의 종료 코드가 스크립트 제어 흐름(`if`, `set -e`)에 미치는 영향을 설명하고 안전하게 처리할 수 있다.

## 참고

- [GNU grep 매뉴얼](https://www.gnu.org/software/grep/manual/grep.html)
- [POSIX grep 사양](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/grep.html)
- [grep (Unix) - Wikipedia](https://en.wikipedia.org/wiki/Grep)
