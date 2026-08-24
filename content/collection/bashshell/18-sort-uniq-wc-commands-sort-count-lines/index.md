---
draft: false
slug: sort-uniq-wc-commands-sort-count-lines
title: "[Bash Shell] 18. sort, uniq, wc - 정렬·중복 제거·개수 세기"
description: "sort·uniq·wc는 정렬 → 인접 중복 확인 → 개수 세기라는 로그 분석의 전형적 3단계를 이루는 명령어 조합이다. 각 명령의 옵션·예시와 함께 sort | uniq -c | sort -rn 조합 패턴, 로케일(LC_ALL)·개행 문자 관련 함정까지 정리한다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 180
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
- Pipeline
- Sorting(정렬)
- Tutorial(튜토리얼)
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- sort
- uniq
- wc
- 정렬
- 중복제거
- 줄수
- 단어수
- word-count
- POSIX
- Locale(로케일)
- 로그분석
- 필터
image: "wordcloud.png"
---

`sort`, `uniq`, `wc`는 각각 따로 배우기 쉬운 명령어지만, 실무에서는 거의 항상 **셋을 이 순서로 이어 붙여** 로그·텍스트에서 "무엇이 몇 번 나왔는지"를 찾아낸다. 이 장은 세 명령어의 옵션을 개별적으로 익히는 데서 그치지 않고, 왜 항상 정렬 → 중복 확인 → 개수 세기 순서로 조합하는지를 정신 모델로 잡는 데 초점을 둔다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [17장: tr](/post/bashshell/tr-command-translate-delete-characters/)에서 문자 단위 변환·삭제를 다룬 뒤 이어진다. `tr`로 문자를 다듬고, [16장: cut](/post/bashshell/cut-command-extract-columns-linux/)으로 필드를 잘라내고, [13장: grep](/post/bashshell/grep-command-search-text-pattern-linux/)으로 줄을 걸러낸 결과를 이번 장에서는 정렬하고 개수를 세는 단계로 넘긴다. 이 장은 <strong>Part 2(텍스트 처리)</strong>의 마지막 챕터다 — grep부터 sed, awk, cut, tr을 거쳐 sort/uniq/wc까지, 텍스트를 읽고 찾고 바꾸고 자르고 세는 개별 도구를 여기서 모두 익히게 된다.

**이 장의 깊이**: **입문–중급** 난이도다. 세 명령어의 기본 옵션과 파이프 조합 패턴까지는 입문 범위이고, `sort -k`의 필드 지정 문법과 로케일에 따른 정렬 순서 차이는 중급 범위다. **다루지 않는 것**: 이 장에서 나오는 파이프(`|`)는 아직 개념 설명 없이 "명령을 이어 붙이는 기호" 정도로만 쓴다 — 표준 입출력과 파이프의 작동 원리 자체는 [19장: 파이프](/post/bashshell/pipe-operator-linux-command-chaining/)에서 본격적으로 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 로그 집계가 급한 사람 | "개요 + 정신 모델", "예시"의 "조합 패턴" | `sort \| uniq -c \| sort -rn` 패턴을 그대로 가져다 로그에서 빈도 상위 항목을 뽑아낼 수 있다 |
| 정확한 정렬·집계를 하려는 사람 | "사용법·옵션" 전체, "주의사항·함정" | 필드 기준 정렬, 로케일별 정렬 순서 차이, `uniq`의 인접 비교 한계, `wc -l`의 개행 카운트 방식까지 이해하고 정확한 결과를 낼 수 있다 |

---

## 개요 + 정신 모델

세 명령어는 서로 다른 일을 하지만, 로그 분석이라는 관점에서 보면 **하나의 파이프라인이 세 단계로 쪼개진 것**에 가깝다. 먼저 `sort`가 흩어진 줄들을 정렬해 같은 값끼리 인접하게 모으고, 그다음 `uniq`가 바로 옆줄끼리만 비교해 중복을 접고(`-c`를 주면 몇 번 반복됐는지까지 세고), 마지막으로 `wc`가 전체 결과의 줄·단어·바이트 수를 요약한다. 셋 다 표준 입력을 읽고 표준 출력으로 내보내는 **필터**이기 때문에 이 순서를 그대로 파이프로 이어 붙일 수 있고, 그래서 `sort file.txt | uniq -c | sort -rn`(정렬 → 인접 중복 집계 → 빈도 내림차순 재정렬)이라는 조합이 로그 분석에서 사실상 관용구처럼 쓰인다.

이 순서가 왜 항상 정렬이 먼저인지가 정신 모델의 핵심이다. `uniq`는 파일 전체를 훑어 같은 값을 찾는 것이 아니라 **바로 앞 줄과 지금 줄, 딱 두 줄만 비교**하는 단순한 도구다. 정렬 없이 흩어진 데이터를 그대로 `uniq`에 넣으면 같은 값이라도 멀리 떨어져 있으면 중복으로 인식되지 않는다. 반대로 `sort`로 미리 정렬해 두면 같은 값은 반드시 인접하게 되므로, `uniq`의 "옆줄만 본다"는 단순함이 오히려 빠르고 메모리를 적게 쓰는 장점이 된다. `wc`는 이 파이프라인의 어느 위치에든 끼워 넣을 수 있는 최종 집계 도구로, "몇 종류가 있는지"(`sort | uniq | wc -l`)처럼 개수 자체가 궁금할 때 마지막에 붙인다.

## 사용법 · 옵션

### sort — 줄 단위 정렬

```bash
sort [옵션] [파일...]
```

| 옵션 | 설명 |
|------|------|
| `-n`, `--numeric-sort` | 문자열이 아니라 숫자 값으로 정렬 |
| `-r`, `--reverse` | 역순(내림차순) 정렬 |
| `-k N[,M]` | N번째 필드(생략 시 N번째부터 끝까지, `,M`을 주면 N–M 필드)를 기준으로 정렬 |
| `-t C` | 필드 구분자를 공백 대신 문자 C로 지정 |
| `-u`, `--unique` | 정렬 후 중복 줄을 하나만 남김(`sort` 다음에 `uniq`를 따로 쓴 것과 결과는 같지만 한 번에 처리) |
| `-f`, `--ignore-case` | 대소문자 구분 없이 정렬 |
| `-h`, `--human-numeric-sort` | `1K`, `2M`처럼 사람이 읽는 단위 표기를 값으로 정렬 |
| `-o FILE` | 정렬 결과를 FILE로 저장(입력과 같은 파일을 지정해도 안전하게 덮어씀) |

### uniq — 인접 중복 처리

```bash
uniq [옵션] [입력 [출력]]
```

**연속으로 인접한** 동일 줄만 하나로 합친다. 정렬돼 있지 않은 입력에는 기대한 결과가 나오지 않으므로 거의 항상 `sort` 뒤에 파이프로 연결해 쓴다.

| 옵션 | 설명 |
|------|------|
| `-c`, `--count` | 각 줄 앞에 연속 반복 횟수를 붙여 출력 |
| `-d`, `--repeated` | 중복(2회 이상 연속)된 줄만 출력 |
| `-u`, `--unique` | 중복 없이 한 번만 나온 줄만 출력 |
| `-i`, `--ignore-case` | 대소문자 구분 없이 비교 |
| `-f N`, `--skip-fields=N` | 비교 시 앞의 N개 필드를 건너뜀 |
| `-w N`, `--check-chars=N` | 각 줄의 앞 N글자만 비교 |

### wc — 줄·단어·바이트·문자 수

```bash
wc [옵션] [파일...]
```

| 옵션 | 설명 |
|------|------|
| `-l`, `--lines` | 줄 수만(정확히는 개행 문자 개수) 출력 |
| `-w`, `--words` | 단어 수만 출력 |
| `-c`, `--bytes` | 바이트 수만 출력 |
| `-m`, `--chars` | 문자 수 출력(멀티바이트 로케일에서 `-c`와 다를 수 있음) |
| `-L`, `--max-line-length` | 가장 긴 줄의 길이 출력 |

## 예시

### 기본 정렬

```bash
# 이름 목록을 사전순으로 정렬
sort names.txt

# 숫자로 정렬 (문자열 정렬과 결과가 다름: "9" > "10"이 문자열 정렬 결과)
sort -n numbers.txt

# /etc/passwd를 세 번째 필드(UID, 숫자) 기준 정렬
sort -t: -k3 -n /etc/passwd
```

### 중복 확인·집계

```bash
# 정렬 후 중복 없는 줄만
sort file.txt | uniq

# 정렬 후 각 줄이 몇 번 나왔는지 집계
sort file.txt | uniq -c

# 딱 한 번만 나온 줄(진짜 유일한 값)만 추리기
sort file.txt | uniq -u
```

### 줄·단어 수 세기

```bash
# 로그 파일의 줄 수
wc -l access.log

# 표준 입력으로 넘긴 텍스트의 단어 수
cat file.txt | wc -w

# 여러 파일의 줄 수를 한 번에(총합 포함)
wc -l *.log
```

### 조합 패턴 (로그 분석의 정석)

```bash
# 접속 로그에서 IP별 요청 횟수를 많은 순으로 정렬
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 명령 히스토리에서 가장 자주 쓴 명령 상위 5개
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -5

# 파일에 서로 다른 값이 몇 종류 있는지(정렬→중복 제거→줄 수)
sort file.txt | uniq | wc -l
```

## 주의사항 · 함정

**`uniq`는 정렬된 입력을 전제로 인접한 줄끼리만 비교한다.** POSIX 사양도 "입력에서 반복된 줄이 인접해 있지 않으면 감지되지 않는다"고 명시한다. `sort` 없이 `uniq`만 단독으로 쓰면 파일 앞뒤로 떨어져 있는 동일한 줄은 중복으로 잡히지 않고 그대로 통과한다 — 초심자가 "`uniq`로 중복을 제거했는데 왜 여전히 같은 줄이 여러 개 남아 있지?"라고 묻는 가장 흔한 원인이다. `uniq`는 항상 `sort` 뒤에 파이프로 연결해서 쓴다고 기억해 두는 편이 안전하다.

**`sort`의 기본 정렬 순서는 로케일(`LC_ALL`)에 따라 달라진다.** POSIX `sort` 사양은 "비교는 현재 로케일의 collating sequence(정렬 규칙)를 사용해 수행한다"고 규정한다. 예를 들어 로케일이 `en_US.UTF-8`처럼 사전식(dictionary) 정렬을 쓰면 대소문자·구두점이 뒤섞인 순서로 나오고, 심지어 `a1`과 `A2`처럼 대소문자가 섞인 줄의 순서가 배포판·로케일 설정에 따라 달라질 수 있다. 스크립트에서 항상 동일한 바이트 값 기준 정렬을 보장하려면 `LC_ALL=C sort`처럼 C 로케일(순수 바이트 값 비교)로 고정해 실행하는 것이 정석이다. GNU `sort` 매뉴얼도 이식성과 재현성이 중요한 상황에서는 `LC_ALL=C`를 권장한다.

**`wc -l`은 줄 수가 아니라 개행 문자 개수를 센다.** POSIX 사양은 `-l`을 "입력 파일의 개행(`<newline>`) 문자 개수를 출력한다"고 정의한다. 텍스트 파일 대부분은 마지막 줄도 개행으로 끝나기 때문에 이 둘이 같아 보이지만, 마지막 줄에 개행이 없는 파일(예: 편집기에서 저장 시 줄바꿈 없이 끝낸 파일, 또는 `echo -n`으로 만든 출력)에서는 그 마지막 줄이 카운트에서 빠진다. `printf 'a\nb\nc'`(세 줄이지만 마지막에 개행 없음)를 `wc -l`에 넘기면 2가 나온다 — "파일에 분명 세 줄이 있는데 `wc -l`은 2를 출력한다"는 흔한 혼란의 원인이다.

## 흔한 오개념

**"`sort -u`와 `sort | uniq`는 다르다"고 생각하기 쉽지만, 단순 중복 제거 결과는 동일하다.** 다만 `-c`(개수 집계)나 `-d`/`-u`(중복만/유일한 값만) 같은 세부 옵션은 `uniq`에만 있으므로, 개수까지 필요하면 `sort | uniq -c`처럼 여전히 두 명령을 이어 써야 한다. `sort -u`는 "정렬과 중복 제거를 한 번에 끝내고 싶을 때"의 지름길일 뿐, `uniq`를 완전히 대체하지는 않는다.

**`wc -w`의 "단어"는 공백으로 구분된 토큰일 뿐, 언어적 의미의 단어가 아니다.** `wc -w`는 공백·탭·개행으로 분리된 연속 문자 덩어리를 하나의 "단어"로 세므로, `hello-world`는 하이픈으로 이어져 있어 한 단어로 카운트되고 `don't stop`은 공백 기준으로 두 단어로 카운트된다. 한국어처럼 띄어쓰기가 문법적 단어 경계와 정확히 일치하지 않는 언어에서는 이 값이 실제 어휘 수와 더 크게 벌어질 수 있다.

## 다음 장에서는

지금까지 grep부터 sed, awk, cut, tr을 거쳐 sort/uniq/wc까지 각 텍스트 처리 도구를 하나씩 개별적으로 배웠다. [19장: 파이프(|)](/post/bashshell/pipe-operator-linux-command-chaining/)부터 시작하는 <strong>Part 3(파이프라인과 입출력)</strong>에서는 이 도구들을 파이프로 조합해 진짜 로그 분석 파이프라인을 만드는 법을 다룬다 — 이번 장의 `sort | uniq -c | sort -rn` 같은 조합이 왜 동작하는지, 표준 입출력이 무엇인지부터 원리를 짚는다.

## 평가 기준

- `sort`, `uniq`, `wc`가 로그 분석에서 왜 "정렬 → 인접 중복 확인 → 개수 세기" 순서로 조합되는지 설명할 수 있다.
- `sort -k`로 필드 기준 정렬을, `uniq -c`로 빈도 집계를, `wc -l`로 줄 수 확인을 각각 수행하고 셋을 파이프로 연결할 수 있다.
- `uniq`가 인접한 줄만 비교한다는 한계를 알고, 정렬 없이 `uniq`만 썼을 때 생기는 문제를 진단할 수 있다.
- `LC_ALL`(로케일)이 `sort`의 정렬 순서에 영향을 준다는 것과, 이식성이 필요할 때 `LC_ALL=C sort`를 쓰는 이유를 설명할 수 있다.
- `wc -l`이 "줄 수"가 아니라 "개행 문자 수"를 센다는 점과, 마지막 줄에 개행이 없을 때 결과가 어떻게 달라지는지 설명할 수 있다.

## 참고

- [sort(1) - Linux manual page](https://man7.org/linux/man-pages/man1/sort.1.html)
- [uniq(1) - Linux manual page](https://man7.org/linux/man-pages/man1/uniq.1.html)
- [wc(1) - Linux manual page](https://man7.org/linux/man-pages/man1/wc.1.html)
- [sort - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/sort.html)
- [uniq - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/uniq.html)
- [wc - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/wc.html)
