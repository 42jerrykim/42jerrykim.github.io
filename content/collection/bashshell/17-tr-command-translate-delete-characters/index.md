---
draft: false
slug: tr-command-translate-delete-characters
title: "[Bash Shell] 17. tr - 문자 치환·삭제"
description: "표준 입력의 문자를 SET1↔SET2 대응표로 1:1 치환·삭제하는 tr을 정신모델·옵션(-d, -s, -c, [:upper:] 등)으로 정리하고, 로케일에 따라 [a-z] 범위 해석이 달라지는 함정과 GNU/BSD 이식성 차이를 다룹니다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 170
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
- String(문자열)
- Process
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- tr
- 문자변환
- translate
- 삭제
- 대소문자
- 문자집합
- Translation-Table
- Character-Class
- Squeeze-Repeats
- Complement
- Collating-Order
- 로케일
image: "wordcloud.png"
---

`tr`(translate)는 **표준 입력**의 문자를 다른 문자로 바꾸거나 삭제하는 필터 명령어다. 줄 단위가 아니라 **문자 단위**로 동작하며, 파일 인자를 받지 않고 항상 표준 입력에서 읽는다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [16장: cut](/post/bashshell/cut-command-extract-columns-linux/)에서 이어진다. `cut`이 탭이나 구분자로 나눈 **컬럼(위치) 단위**로 텍스트를 잘라냈다면, `tr`은 그보다 더 작은 단위인 **개별 문자 단위**로 1:1 치환·삭제를 수행한다 — "어느 필드를 뽑을까"에서 "어떤 문자를 다른 문자로 바꿀까"로 관심 대상이 한 단계 더 세밀해지는 전환이다.

**이 장의 깊이**: **입문–중급** 난이도다. 기본 치환·삭제부터 문자 클래스, `-s`/`-c` 조합, 로케일 함정까지 실무에서 자주 마주치는 범위를 다룬다. **다루지 않는 것**: 정규식 기반의 패턴 치환(원하는 부분만 찾아 바꾸는 것)은 [14장: sed](/post/bashshell/sed-command-stream-editor-linux/)에서 다룬다 — `tr`은 정규식 엔진이 아니므로 애초에 "패턴 매칭"이라는 개념 자체가 없다는 점이 이 장의 핵심 포인트 중 하나다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 대소문자 변환·공백 정리가 급한 사람 | "사용법·옵션"의 기본 표, "예시"의 "대소문자 변환"·"공백·개행 정리" | 자주 쓰는 옵션 조합으로 파이프라인 안에서 바로 문자를 다듬는다 |
| tr의 동작 원리를 제대로 이해하려는 사람 | "개요 + 정신 모델"부터 "주의사항·함정", "흔한 오개념" 전체 | 치환표라는 정신 모델로 SET1/SET2 대응 규칙을 스스로 추론하고, 로케일·이식성 함정을 피한다 |

## 개요 + 정신 모델

`tr`을 처음 배울 때 가장 흔한 오해는 이것을 grep이나 sed처럼 **패턴을 찾아 바꾸는 도구**로 여기는 것이다. 실제로는 전혀 다른 층위에서 동작한다. `tr SET1 SET2`는 정규식이 아니라 <strong>문자 집합 대 문자 집합의 위치 대응표(translation table)</strong>를 만든다 — SET1의 *n*번째 문자가 입력에 나타나면 SET2의 *n*번째 문자로 바꾼다는, 순전히 위치 기반의 1:1 매핑이다. `tr 'abc' 'xyz'`는 "a·b·c 중 하나를 찾아서 바꿔라"가 아니라 "a는 x로, b는 y로, c는 z로"라는 세 개의 독립적인 치환 규칙을 동시에 등록하는 것과 같다. 이 모델을 받아들이면 SET1과 SET2의 **길이가 서로 대응해야 한다**는 사실, 그리고 왜 `tr`이 패턴 매칭이 아니라 "이 문자를 만나면 즉시 저 문자로"라는 스트림 단위의 문자 대체기로 동작하는지가 자연스럽게 이해된다. grep이 줄을 필터링하고 sed가 패턴을 찾아 치환한다면, `tr`은 그보다 한 단계 아래에서 **개별 바이트(문자)를 순회하며 표를 찾아보는** 가장 단순하고 빠른 변환기다.

## 사용법 · 옵션

```bash
tr [옵션] SET1 [SET2]
```

- **SET1**: 변환·삭제 대상이 될 문자 집합.
- **SET2**: SET1과 대응할 문자 집합. 삭제(`-d`)만 할 때는 생략 가능하다. SET2가 SET1보다 짧으면 GNU `tr`은 SET2의 마지막 문자를 SET1 길이만큼 반복해 채운다.

### 동작 모드 옵션

| 옵션 | 설명 |
|------|------|
| `-d`, `--delete` | SET1에 있는 문자를 삭제한다(치환하지 않음). |
| `-s`, `--squeeze-repeats` | 연속으로 반복되는 동일 문자를 하나로 축약한다. |
| `-c`, `-C`, `--complement` | SET1의 여집합(SET1에 **없는** 문자)을 대상으로 삼는다. |
| `-t`, `--truncate-set1` | SET1을 SET2 길이에 맞춰 자른다(기본은 SET2가 SET1 길이에 맞춰 늘어남). |

### 문자 집합 표기

| 표기 | 의미 |
|------|------|
| `a-z`, `A-Z`, `0-9` | 연속된 문자 범위(로케일에 따라 해석이 달라질 수 있음 — 아래 "주의사항·함정" 참고) |
| `[:lower:]`, `[:upper:]` | 소문자·대문자 문자 클래스(POSIX 표준) |
| `[:digit:]`, `[:alpha:]`, `[:alnum:]` | 숫자·알파벳·영숫자 클래스 |
| `[:space:]`, `[:punct:]` | 공백류·구두점 클래스 |
| `[c*n]` | 문자 `c`를 `n`번 반복(주로 SET2를 SET1 길이에 맞출 때 사용, GNU 확장) |
| `\n`, `\t`, `\\` | 개행·탭·백슬래시 등 이스케이프 시퀀스 |

## 예시

### 대소문자 변환

```bash
# 소문자 → 대문자
echo "hello world" | tr 'a-z' 'A-Z'

# 문자 클래스로 동일한 작업(POSIX 표준 표기라 이식성이 더 좋다)
echo "hello world" | tr '[:lower:]' '[:upper:]'
```

### 공백·개행 정리

```bash
# 개행을 공백으로 바꿔 한 줄로 합치기
tr '\n' ' ' < file.txt

# 연속된 공백을 하나로 압축(-s)
tr -s ' ' < file.txt

# 탭을 공백 한 칸으로
tr '\t' ' ' < file.txt
```

### 삭제(-d)

```bash
# 숫자 삭제
tr -d '0-9' < file.txt

# 캐리지 리턴(\r) 제거 — 윈도우식 CRLF를 유닉스식 LF로
tr -d '\r' < windows_file.txt > unix_file.txt
```

### 여집합(-c)과 조합

```bash
# 영숫자가 아닌 문자를 전부 개행으로 바꿔 단어를 한 줄씩 나열
echo "hello, world! 123" | tr -c '[:alnum:]' '\n'

# 인쇄 가능한 문자만 남기고 나머지(제어 문자 등)는 삭제
tr -cd '[:print:]\n' < binary_ish.txt
```

### 파이프 조합

```bash
# 로그에서 대문자로 시작하는 레벨 표기를 통일해서 세기
cat app.log | tr 'a-z' 'A-Z' | grep -c "ERROR"

# 콤마 구분 목록을 줄바꿈 목록으로 바꿔 wc로 개수 세기
echo "a,b,c,d" | tr ',' '\n' | wc -l
```

### 로케일 고정(이식성 있는 실행)

```bash
# 범위·클래스 해석을 POSIX 기준으로 고정
LC_ALL=C tr 'a-z' 'A-Z' < file.txt
```

## 주의사항·함정

**문자 집합 범위는 로케일에 따라 다르게 해석될 수 있다.** `[a-z]`처럼 하이픈으로 잇는 범위 표기는 겉보기엔 "알파벳 26개"로 고정된 것 같지만, 실제로는 시스템의 <strong>대조 순서(collating order)</strong>를 따른다. POSIX 사양은 이를 명시적으로 경고한다 — "POSIX 로케일이 아닌 로케일에서는 이 구문(범위 표현식)의 동작이 정의되지 않는다(unspecified behavior)"([POSIX tr 사양](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tr.html) RANGE 관련 절 참고). 즉 `en_US.UTF-8` 같은 로케일에서는 대소문자가 섞여서 정렬되거나 예상과 다른 문자가 범위에 포함될 수 있다. 스크립트가 어떤 환경에서 실행되든 항상 같은 결과를 내야 한다면, `LC_ALL=C tr ...`처럼 **POSIX(C) 로케일로 고정**해 실행하는 것이 안전하다 — 이렇게 하면 대조 순서가 바이트 값 순서로 고정되어 `[a-z]`가 항상 소문자 26개만을 의미하게 된다.

**GNU 확장과 POSIX 표준을 구분해야 한다.** `[:upper:]`, `[:lower:]`, `[:digit:]` 같은 문자 클래스는 POSIX 표준에 정의된 표기라 GNU `tr`뿐 아니라 BSD `tr`(macOS 기본 `tr`)에서도 대부분 동일하게 동작해 이식성이 좋다. 반대로 `--complement`, `--squeeze-repeats`, `--delete`처럼 두 글자 이상의 긴 옵션(long option) 형태는 **GNU coreutils의 확장**이며, BSD `tr`에는 존재하지 않는다. BSD 계열에서는 `-c`, `-s`, `-d` 같은 짧은 옵션만 지원하므로, macOS나 BSD 환경까지 옮겨 쓸 스크립트라면 장옵션 대신 짧은 옵션으로 통일하는 편이 안전하다.

**SET2가 SET1보다 짧을 때의 동작이 구현마다 역사적으로 갈렸다.** POSIX 사양의 APPLICATION USAGE 절은 BSD 계열과 System V 계열 구현이 이 경우를 서로 다르게 처리해온 역사를 언급하며, 이식성을 보장하려면 `[c*n]` 반복 구문으로 SET2 길이를 SET1과 명시적으로 맞추라고 권한다. GNU `tr`은 기본적으로 SET2의 마지막 문자를 반복해 늘리지만, 이 기본 동작에 의존하지 않고 길이를 명시하는 습관을 들이면 다른 구현으로 옮겨도 같은 결과를 보장할 수 있다.

**`tr`은 파일을 인자로 받지 않는다.** `tr 'a-z' 'A-Z' file.txt`처럼 파일명을 그냥 뒤에 붙이면 `file.txt`가 SET2로 해석되어 엉뚱한 치환이 일어난다. 항상 `tr 'a-z' 'A-Z' < file.txt`처럼 리다이렉션으로 표준 입력을 연결해야 한다.

## 흔한 오개념

**"tr도 정규식을 쓴다"는 오해.** grep·sed·awk를 먼저 배운 사람일수록 `tr 'a-z' 'A-Z'`를 정규식 매칭으로 착각하기 쉽다. 하지만 SET1·SET2는 **문자 하나하나의 나열**일 뿐 패턴이 아니다. POSIX 사양도 "tr이 받는 문자열 피연산자는 정규식이 아니다(the string operands used by tr are not regular expressions)"라고 명시한다. `tr 'ab' 'x'`처럼 SET2가 SET1보다 짧으면(단, `-t` 없이) 에러가 나거나 예상과 다른 결과가 나올 수 있다 — 이는 "패턴 'ab'를 찾아 'x'로 바꾼다"는 정규식적 사고에서 비롯된 실수다.

**"`-d`는 SET2를 참고해 삭제할 문자를 고른다"는 오해.** `tr -d SET1 SET2`처럼 두 번째 인자를 주면, `-d`는 SET2를 완전히 무시하고 SET1에 있는 문자만 삭제한다. SET2가 의미를 가지려면 `-s`와 함께 써서 "삭제 후 SET2에 남은 문자 중 반복된 것을 축약"하는 조합(`tr -ds SET1 SET2`)이어야 한다 — 단독 `-d`에 SET2를 넘기는 것은 사실상 아무 효과가 없는 군더더기다.

## 다음 장에서는

다음은 [18장: sort, uniq, wc](/post/bashshell/sort-uniq-wc-commands-sort-count-lines/) — 문자 단위 치환을 넘어, 줄 단위로 정렬하고 중복을 제거하고 개수를 세는 도구로 넘어간다.

## 평가 기준

- `tr SET1 SET2`가 정규식 매칭이 아니라 위치 기반 치환표(translation table)라는 것을 설명할 수 있다.
- `-d`, `-s`, `-c` 옵션을 목적에 맞게 단독·조합해서 문자를 삭제·압축·여집합 변환할 수 있다.
- 문자 범위(`a-z`)와 POSIX 문자 클래스(`[:upper:]` 등)의 차이, 그리고 범위 표기가 로케일에 따라 달라질 수 있다는 함정을 설명하고 `LC_ALL=C`로 회피할 수 있다.
- GNU `tr`의 장옵션(`--complement` 등)이 BSD `tr`에는 없다는 이식성 차이를 설명할 수 있다.
- `tr`이 파일 인자를 받지 않고 표준 입력만 처리한다는 제약을 이해하고 리다이렉션으로 올바르게 연결할 수 있다.

## 참고

- [tr(1) - Linux manual page (GNU coreutils)](https://man7.org/linux/man-pages/man1/tr.1.html)
- [tr - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tr.html)
