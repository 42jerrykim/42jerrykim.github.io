---
draft: false
slug: if-command-conditional-batch-windows-cmd
title: "[CMD] 32. if - 배치 파일 조건 분기"
description: "if로 ERRORLEVEL·문자열·파일 존재 여부를 검사해 분기하는 법과 EQU·NEQ 등 세 글자 비교 연산자, else는 반드시 같은 줄에 와야 하는 문법 제약, if defined가 추가하는 세 예약 변수를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 320
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- if
- 조건분기
- ERRORLEVEL
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Command-Extensions
- Advanced
- Configuration(설정)
- Administration
image: "wordcloud.png"
---

if는 배치 프로그램에서 조건에 따라 다른 명령을 실행하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [31장: set](/post/cmd/set-command-environment-variables-windows-cmd/)에서 변수를 다루는 법을 배운 뒤 이어진다. set으로 저장한 값을 실제로 검사해 분기하는 것이 이 장의 목표다.

**이 장의 깊이**: 중급. **다루지 않는 것**: 반복 실행은 33장(for)에서, 조건 분기를 goto와 결합해 서브루틴처럼 쓰는 패턴은 34–35장(call, goto)에서 다룬다.

## 사용법

```
if [not] errorlevel <숫자> <명령> [else <식>]
if [not] <문자열1>==<문자열2> <명령> [else <식>]
if [not] exist <파일이름> <명령> [else <식>]
```

명령 확장이 켜져 있으면(기본값) 다음 문법도 지원된다.

```
if [/i] <문자열1> <비교연산자> <문자열2> <명령> [else <식>]
if cmdextversion <숫자> <명령> [else <식>]
if defined <변수> <명령> [else <식>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `not` | 조건을 부정 |
| `errorlevel <숫자>` | 직전 프로그램의 종료 코드가 지정한 숫자 **이상**이면 참 |
| `<문자열1>==<문자열2>` | 두 문자열이 같으면 참 |
| `exist <파일이름>` | 지정한 파일이 있으면 참 |
| `/i` | 문자열 비교 시 대소문자 무시. 양쪽이 모두 숫자면 숫자 비교로 처리 |
| `cmdextversion <숫자>` | 명령 확장 내부 버전이 지정한 숫자 이상이면 참 |
| `defined <변수>` | 변수가 정의되어 있으면 참 |

### 세 글자 비교 연산자

| 연산자 | 의미 |
|---|---|
| `EQU` | 같음 |
| `NEQ` | 다름 |
| `LSS` | 작음 |
| `LEQ` | 작거나 같음 |
| `GTR` | 큼 |
| `GEQ` | 크거나 같음 |

## 예시

```
if not exist product.dat echo Cannot find data file
if %errorlevel% LEQ 1 goto okay
if exist config.ini echo Found
if defined MYVAR echo MYVAR is set
```

```bat
IF EXIST Product.dat (
del Product.dat
) ELSE (
echo The Product.dat file is missing.
)
```

```bat
:begin
@echo off
format a: /s
if not errorlevel 1 goto end
echo An error occurred during formatting.
:end
echo End of batch program.
```

## 주의사항·함정

**`errorlevel <숫자>`는 "이상"을 뜻하지 "같음"을 뜻하지 않는다**: `if errorlevel 1`은 종료 코드가 정확히 1일 때가 아니라 1 이상일 때 참이 된다. 그래서 여러 종료 코드를 구분하려면 큰 숫자부터 먼저 검사해야 한다 — 15장(xcopy)에서 다룬 `if errorlevel 4 ... if errorlevel 2 ... if errorlevel 0 ...` 순서가 이 규칙을 따른 예다. 정확히 특정 값과 비교하고 싶다면 `if %errorlevel% EQU 1`처럼 세 글자 연산자를 쓰는 편이 명확하다.

**else는 반드시 같은 줄에 있어야 한다**: Microsoft Learn은 이 제약을 명시한다.

> "You must use the **else** clause on the same line as the command after the **if**." — Microsoft Learn, "if"

`if` 블록을 괄호로 감싸 여러 줄에 걸쳐 썼더라도, 닫는 괄호 `)`와 `else`는 같은 줄에 있어야 한다 — 위 예시의 `) ELSE (`처럼 줄바꿈 없이 이어 써야 한다. `)`만 쓰고 다음 줄에서 `else`를 시작하면 문법 오류가 난다.

**`if defined`는 세 예약 변수를 함께 만든다**: `defined`를 한 번이라도 쓰면 `%errorlevel%`, `%cmdcmdline%`, `%cmdextversion%` 세 변수가 환경에 추가된다(단, 이미 같은 이름의 변수가 있으면 그 값이 우선한다). `%errorlevel%`은 이미 익숙하겠지만, `%cmdcmdline%`(cmd.exe에 전달된 원래 명령줄 전체)과 `%cmdextversion%`(명령 확장 버전)은 디버깅 시 유용한 잘 알려지지 않은 변수다.

**빈 변수를 따옴표 없이 비교하면 문법 오류가 난다**: `if %var%==""`처럼 `var`가 비어 있으면 `if ==""`가 되어 문법 오류가 난다. `if "%var%"==""`처럼 양쪽을 항상 따옴표로 감싸는 습관이 안전하다.

**괄호 블록 안에서 변수를 설정하고 같은 블록에서 바로 참조하면 옛 값만 보인다**: CMD 스크립팅에서 가장 널리 알려진 함정이다. `if (...) else (...)`처럼 블록을 괄호로 감싸면, CMD는 그 블록 전체를 실행하기 전에 한 번에 읽어 그 시점의 값으로 `%변수%`를 미리 치환해버린다.

```bat
set x=1
if %x%==1 (
  set x=2
  echo %x%
)
```

`set x=2`가 먼저 실행됐으니 `2`가 나올 것 같지만, 실제로는 블록이 파싱되던 시점(즉 `if` 줄에 처음 진입하기 전)의 값인 **`1`이 그대로 출력된다**. 블록 안에서 방금 `set`으로 바꾼 값을 같은 블록 안에서 바로 읽으려면 `%x%`가 아니라 `!x!`(느낌표 지연 확장)를 써야 하고, 그러려면 먼저 `setlocal enabledelayedexpansion`으로 지연 확장을 켜야 한다 — 40장(setlocal)이 이 기능을 다룬다. 같은 함정이 반복문에서는 어떻게 나타나는지는 33장(for)의 주의사항·함정에서 이어서 다룬다.

**PowerShell의 조건문은 중괄호와 비교 연산자를 쓴다**: `if (...) { } elseif (...) { } else { }` 형태로, CMD의 `EQU`/`NEQ`/`LSS`/`GTR` 세 글자 연산자나 `==` 대신 `-eq`, `-ne`, `-lt`, `-gt`, `-like`, `-match` 같은 대시(-) 붙은 연산자를 쓴다. 그리고 이 장에서 다룬 괄호 블록의 지연된 확장 함정 자체가 PowerShell에는 없다 — PowerShell은 CMD처럼 블록 전체를 실행 전에 미리 훑어 변수를 문자열로 치환하는 파싱 방식을 쓰지 않고, `{ }` 안의 코드를 실제 실행되는 순간에 그때그때 평가하기 때문이다. CMD 사용자에게는 낯설게 느껴질 수 있지만, 이 장에서 겪은 혼란의 근본 원인 자체가 PowerShell에는 존재하지 않는다는 점에서 긍정적인 차이다.

## 흔한 오개념

<strong>"`/i`를 안 쓰면 항상 대소문자를 구분한다"</strong>는 것은 `==` 형식에는 맞지만, `/i` 자체는 세 글자 비교 연산자(`EQU` 등)와 함께 쓰는 명령 확장 문법에 속한다. 또한 `/i` 비교에서 양쪽 문자열이 모두 숫자로만 이루어져 있으면, 문자열이 아니라 숫자로 변환해 비교한다는 점도 놓치기 쉽다 — `"9" LSS "10"`이 문자열 비교였다면 거짓(문자 `9`가 `1`보다 크므로)이지만, 숫자로 변환되어 참이 된다.

## 다음 장에서는

다음은 33장 — 파일 집합·디렉터리·숫자 범위를 반복 처리하는 `for` 명령을 다룬다.

## 평가 기준

- errorlevel·문자열·exist·defined 네 가지 조건 형식으로 분기할 수 있다.
- `errorlevel <숫자>`가 "이상"을 뜻한다는 것과, 정확한 값 비교에는 `EQU`를 써야 하는 이유를 설명할 수 있다.
- else가 반드시 같은 줄에 와야 한다는 문법 제약을 지켜 여러 줄 조건문을 작성할 수 있다.
- `if defined`가 추가하는 세 예약 변수(`%errorlevel%`, `%cmdcmdline%`, `%cmdextversion%`)를 안다.
- 빈 변수 비교 시 따옴표가 필요한 이유를 설명할 수 있다.

## 참고

- [if | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/if)
- [goto | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/goto)
