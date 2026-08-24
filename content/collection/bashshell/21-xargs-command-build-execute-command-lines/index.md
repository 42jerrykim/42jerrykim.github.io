---
draft: false
slug: xargs-command-build-execute-command-lines
title: "[Bash Shell] 21. xargs - 인자 변환과 배치 실행"
description: "파이프는 표준입력만 연결하지만 많은 명령은 인자(argv)로 대상을 받는다. 표준입력 항목을 인자로 바꿔 뒤 명령을 반복 실행시키는 xargs의 정신 모델과 -I·-P·-n 옵션, find -print0 | xargs -0 안전 패턴, 병렬 실행의 함정을 예제로 정리한다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 210
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Process
- Automation(자동화)
- Pipe(파이프)
- Pipeline
- Parallel-Computing(병렬컴퓨팅)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- Best-Practices
- How-To
- Tips
- Beginner
- Comparison(비교)
- Deep-Dive
- Workflow(워크플로우)
- Error-Handling(에러처리)
- xargs
- 인자변환
- arguments
- find
- batch
- argv
- 표준입력
- 병렬실행
- 자리표시자
image: "wordcloud.png"
---

`xargs`는 **표준 입력**으로 들어온 텍스트를 **다른 명령의 명령줄 인자**로 변환해, 그 명령을 반복 실행시키는 어댑터다. `find` 결과를 `rm`·`cp`·`grep` 같은 명령에 한 번에 넘길 때 가장 자주 쓴다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/)에서 이어진다. 파이프(`|`)는 한 명령의 표준출력을 다른 명령의 **표준입력**에 연결할 뿐이다. 그런데 `rm`, `cp`, `grep`처럼 많은 명령은 삭제·복사·검색할 대상을 표준입력이 아니라 <strong>명령줄 인자(argv)</strong>로 받는다. 파이프만으로는 `find`가 찾아낸 파일 목록을 `rm`의 인자 자리에 밀어 넣을 방법이 없다 — `xargs`는 바로 이 간극, "표준입력으로 받은 것을 인자로 넘기고 싶다"는 요구를 메우기 위해 존재한다. [7장: cp, mv, rm](/post/bashshell/cp-mv-rm-commands-copy-move-delete-files/)에서 예고했던 `find ... -print0 | xargs -0 rm`이 이 장에서 다루는 안전 패턴의 실체다.

**이 장의 깊이**: **입문–중급** 난이도다. 기본 변환 원리부터 `-I` 자리표시자, `-0`/`-print0` 안전 패턴, `-P` 병렬 실행까지 실무에서 자주 쓰는 범위를 다룬다. **다루지 않는 것**: `xargs`가 넘겨받은 인자를 명령 안에서 어떻게 인용해야 하는지(변수 확장·따옴표 규칙 자체)는 [22장: 인용(Quoting)](/post/bashshell/bash-quoting-escaping-special-characters/)에서 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| find 결과를 바로 처리하고 싶은 사람 | 개요+정신 모델, 사용법·옵션의 "기본 변환"·"find 조합", 예시 1–5번 | `find ... \| xargs 명령` 형태로 검색 결과를 일괄 처리할 수 있다 |
| 안전하고 빠른 배치 처리가 필요한 사람 | 사용법·옵션 전체, 예시 6–9번, 주의사항·함정 전체 | 파일명에 공백·개행이 섞여도 깨지지 않게 처리하고, `-P`로 병렬 실행할 때의 트레이드오프를 판단할 수 있다 |

---

## 개요 + 정신 모델

`xargs`("eXtended ARGuments"에서 유래)는 표준입력을 한 줄씩 혹은 공백 단위로 읽어 **토큰의 목록**으로 만든 다음, 그 토큰들을 뒤에 적은 명령의 **끝에 인자로 붙여** 실행한다. 즉 `xargs`는 그 자체로는 아무 일도 하지 않는다 — "표준입력 → 인자 목록 → 명령 실행"이라는 변환 파이프의 어댑터 역할만 한다.

이 정신 모델에서 중요한 것은 `xargs`가 입력을 <strong>몇 개의 배치(batch)</strong>로 나눠 명령을 **여러 번 실행할 수도 있다**는 점이다. 인자 목록이 매우 길면(운영체제마다 `ARG_MAX`라는 명령줄 길이 제한이 있다) `xargs`는 한 번의 명령 실행에 다 담지 못하고 자동으로 여러 번 나눠 실행한다. 예를 들어 `find . -name "*.log" | xargs rm`이 파일을 100만 개 찾았다면, `xargs`는 이를 몇 번의 `rm file1 file2 ... fileN` 호출로 쪼개 실행한다 — `for` 루프로 한 파일씩 `rm`을 호출하는 것보다 훨씬 적은 프로세스 생성 비용으로 끝난다는 뜻이다.

## 사용법 · 옵션

기본 문법은 다음과 같다.

```bash
[표준입력을 만드는 명령] | xargs [옵션] [명령 [고정 인자...]]
```

`명령`을 생략하면 기본값인 `echo`가 실행돼, `xargs`가 인자를 어떻게 나눴는지 확인하는 용도로도 쓸 수 있다.

### 기본 변환

| 옵션 | 설명 |
|------|------|
| (기본 동작) | 표준입력을 공백·탭·개행으로 구분된 토큰으로 나눠 인자로 전달 |
| `-n N`, `--max-args=N` | 한 번의 명령 실행에 최대 N개 인자만 전달(배치 크기 강제) |
| `-L N`, `--max-lines=N` | 입력 N줄마다 한 번씩 명령 실행 |
| `-p`, `--interactive` | 각 실행 전에 확인 프롬프트 표시 |
| `-t`, `--verbose` | 실행할 명령을 실행 전에 화면에 출력 |

### 안전한 구분자 처리

| 옵션 | 설명 |
|------|------|
| `-0`, `--null` | 입력을 널 문자(`\0`)로 구분. 공백·따옴표·백슬래시를 특수 취급하지 않는다 |
| `-d DELIM`, `--delimiter=DELIM` | 구분자를 직접 지정(GNU 확장) |

### 자리표시자와 병렬 실행

| 옵션 | 설명 |
|------|------|
| `-I REPLSTR` | 입력 한 줄을 통째로 `REPLSTR` 자리에 치환(관례적으로 `{}` 사용). 자동으로 `-L 1`처럼 동작 |
| `-P N`, `--max-procs=N` | 최대 N개 프로세스를 **동시에** 병렬 실행(GNU 확장, 기본값 1) |
| `-i[REPLSTR]` | `-I`의 구식 표기(더 이상 권장하지 않음) |

### 안전 · 종료 코드

| 옵션 | 설명 |
|------|------|
| `-r`, `--no-run-if-empty` | 입력이 비어 있으면 명령을 아예 실행하지 않음(GNU 기본 동작이지만 POSIX xargs와 이식할 때 명시하면 안전) |
| `-x`, `--exit` | `-s`로 지정한 길이 제한을 넘으면 실행하지 않고 종료 |

## 예시

### find 결과를 인자로 넘기기

```bash
# .tmp 파일을 찾아 한 번에 삭제(파일이 많아도 rm 프로세스 호출 횟수가 적다)
find . -name "*.tmp" | xargs rm

# 인자 없이 xargs만 실행해 어떻게 배치가 나뉘는지 확인
find . -name "*.log" | xargs echo
```

### 배치 크기·병렬 제어

```bash
# 한 번에 최대 5개 파일씩만 묶어서 처리
find . -name "*.txt" | xargs -n 5 echo

# 최대 4개 프로세스로 URL을 병렬 다운로드
cat urls.txt | xargs -P 4 -n 1 curl -O
```

### -I 자리표시자로 인자 위치 지정

```bash
# 각 줄을 {} 자리에 넣어 원하는 위치에 인자를 배치
echo -e "a\nb\nc" | xargs -I {} echo "item: {} (처리 완료)"

# 찾은 디렉터리마다 백업 파일명을 붙여 압축
find . -maxdepth 1 -type d | xargs -I {} tar -czf "{}.tar.gz" "{}"
```

### 공백·개행이 있는 파일명 안전하게 처리(find -print0)

```bash
# 기본 xargs: 파일명에 공백이 있으면 서로 다른 두 인자로 쪼개져 버린다
find . -name "*.log"          # 예: "March report.log" 한 줄
find . -name "*.log" | xargs rm   # rm이 "March"와 "report.log"를 각각 별개 파일로 인식 → 실패

# 안전 패턴: -print0으로 널 문자 구분 출력, xargs -0으로 그대로 소비
find . -name "*.log" -print0 | xargs -0 rm
```

### 확인 후 실행 · 실행 전 미리보기

```bash
# 실행 전 각 명령을 사람이 눈으로 확인
find . -name "*.bak" | xargs -p rm

# 실행할 명령을 로그로 남기며 실행
find . -name "*.bak" | xargs -t rm
```

## 주의사항·함정

**파일명에 공백·개행·특수문자가 있으면 기본 `xargs`가 깨진다.** `xargs`는 기본적으로 입력을 공백·탭·개행으로 구분한다. 그런데 `find`가 찾아낸 파일 경로 자체에 공백이 들어 있으면(`March report.log`처럼), `xargs`는 이를 하나의 파일명이 아니라 `March`와 `report.log`라는 **두 개의 서로 다른 인자**로 쪼개버린다. 그 결과 `rm`은 존재하지 않는 `March`, `report.log`라는 두 "파일"을 지우려다 오류를 내거나, 최악의 경우 의도치 않은 다른 파일을 건드릴 수 있다. 해결책은 구분자 자체를 절대 파일명에 등장할 수 없는 <strong>널 문자(`\0`)</strong>로 바꾸는 것이다. `find`의 `-print0` 옵션은 각 결과를 널 문자로 구분해 출력하고, `xargs -0`은 그 널 문자를 구분자로 삼아 읽는다 — 이 둘을 짝으로 쓰면 공백·개행·따옴표가 섞인 파일명도 항상 하나의 온전한 인자로 전달된다. [7장: cp, mv, rm](/post/bashshell/cp-mv-rm-commands-copy-move-delete-files/)에서 재귀 삭제 예시로 미리 보여준 `find old_logs/ -name "*.log" -print0 | xargs -0 rm -v`가 바로 이 패턴이며, 삭제·이동처럼 되돌릴 수 없는 작업일수록 `-print0`/`-0` 조합을 기본값으로 삼는 편이 안전하다.

**`-I {}` 자리표시자는 인자 위치를 자유롭게 지정하지만 배치를 강제로 1개씩 쪼갠다.** 기본 `xargs`는 여러 인자를 명령 끝에 한꺼번에 붙이므로(`cmd a b c`), 인자를 명령 중간이나 여러 번 반복해 넣을 수 없다. `-I {}`를 쓰면 입력 한 줄을 `{}` 자리에 그대로 치환해 `tar -czf "{}.tar.gz" "{}"`처럼 같은 값을 여러 위치에 쓰거나 옵션 중간에 끼워 넣을 수 있다. 다만 `-I`는 내부적으로 한 번의 실행에 입력 한 줄만 처리하는 방식으로 동작하므로(`-L 1`과 사실상 동일한 효과), 입력이 아주 많으면 그만큼 명령 실행(프로세스 생성) 횟수도 늘어난다 — 처리량이 중요하면 `-I` 대신 기본 배치 방식이나 `-n`으로 여러 인자를 한 번에 묶는 편이 빠르다.

**`-P N`으로 병렬 실행하면 출력 순서가 비결정적이 된다.** `-P 4`처럼 여러 프로세스를 동시에 띄우면 처리 속도는 빨라지지만, 각 프로세스가 끝나는 시점은 예측할 수 없다. `cat urls.txt | xargs -P 4 -n 1 curl -O`를 실행하면 다운로드 자체는 병렬로 빨라져도, 터미널에 찍히는 로그 줄 순서는 입력 순서와 달라질 수 있다. 출력을 순서대로 기록해야 하는 스크립트(로그 병합, 번호 매기기 등)에서 `-P`를 그대로 쓰면 순서가 뒤섞인 결과를 그대로 신뢰하는 실수를 하기 쉽다 — 순서가 중요하면 각 작업 결과를 파일별로 따로 저장한 뒤 나중에 정렬해서 합치거나, 병렬 실행 자체를 포기하고 `-P 1`(기본값)로 순차 실행해야 한다.

## 흔한 오개념

**"`xargs`는 파이프의 일종이다"는 정확하지 않다.** 파이프(`|`)는 한 명령의 표준출력을 다른 명령의 표준입력에 연결하는 셸 문법 자체이고, `xargs`는 그 파이프로 들어온 데이터를 **인자로 바꿔주는 프로그램**이다. `xargs`가 없어도 파이프는 동작하지만(예: `cat file | grep pattern`은 `grep`이 표준입력을 직접 읽으므로 `xargs`가 필요 없다), `rm`·`cp`처럼 표준입력을 읽지 않고 인자만 받는 명령을 파이프 뒤에 두려면 반드시 `xargs`(또는 셸의 명령어 치환)를 거쳐야 한다.

**"인자가 하나도 없으면 명령이 그냥 아무 일도 안 한다"고 오해하기 쉽다.** `find` 결과가 0개일 때 `find ... | xargs rm`을 실행하면, GNU `xargs`는 기본적으로 인자가 없으면 명령을 아예 실행하지 않지만(POSIX `xargs`는 구현에 따라 인자 없이 `rm`을 한 번 실행해 "missing operand" 오류를 낼 수 있다), 명령에 **고정 인자**가 이미 붙어 있으면 이야기가 다르다. `find . -name "*.tmp" | xargs rm -rf /some/dir`처럼 고정 인자를 잘못 배치하면, 입력이 0개여도 `rm -rf /some/dir`이 그대로 실행될 위험이 있다 — 인자가 비었을 때의 동작을 확신할 수 없다면 `-r`(`--no-run-if-empty`)을 명시하거나, 실행 전 `-p`/`-t`로 먼저 확인하는 습관을 들이는 편이 안전하다.

## 다음 장에서는

다음은 [22장: 인용(Quoting)](/post/bashshell/bash-quoting-escaping-special-characters/) — `xargs`가 인자로 넘긴 값이 셸에서 어떻게 해석되는지, 변수 확장과 따옴표 규칙을 다룬다.

## 평가 기준

- 파이프(표준입력 연결)와 `xargs`(표준입력을 인자로 변환)의 역할 차이를 설명할 수 있다.
- `find ... -print0 | xargs -0` 패턴이 왜 필요한지, 기본 `xargs`가 어떤 파일명에서 깨지는지 설명할 수 있다.
- `-I {}` 자리표시자로 인자 위치를 지정하는 법과, 그로 인해 배치가 1개씩 쪼개지는 트레이드오프를 설명할 수 있다.
- `-n`으로 배치 크기를 제어하고 `-P`로 병렬 실행할 때 출력 순서가 비결정적이 됨을 이해하고 대응할 수 있다.
- 인자가 없을 때 GNU `xargs`의 기본 동작과, 고정 인자가 있는 명령을 병행할 때의 위험을 판단할 수 있다.

## 참고

- [xargs(1) - Linux manual page](https://man7.org/linux/man-pages/man1/xargs.1.html)
- [xargs - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/xargs.html)
