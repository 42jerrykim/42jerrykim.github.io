---
draft: false
slug: set-command-environment-variables-windows-cmd
title: "[CMD] 31. set - 환경 변수 표시·설정과 산술 연산"
description: "set으로 환경 변수를 조회·설정·삭제하는 법과 /p 사용자 입력, /a 산술 연산의 연산자 우선순위 표, 지연된 환경 변수 확장이 기본적으로 꺼져 있다는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 310
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
- Set
- 환경변수
- Environment
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

set은 cmd.exe 환경 변수를 표시·설정·제거하는 내장 명령이다. `/a`로 산술 연산도 수행할 수 있다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [30장: echo](/post/cmd/echo-command-display-message-windows-cmd/)에서 메시지 출력을 다룬 뒤 이어진다. echo가 값을 "보여주는" 명령이었다면, set은 그 값을 "저장하는" 첫 명령이다 — 배치 스크립팅에서 상태를 유지하는 가장 기본적인 수단이다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: set으로 만든 변수의 유효 범위를 블록 안으로 제한하는 것은 40장(setlocal, endlocal)에서 다룬다.

## 사용법

```
set [<변수>=[<문자열>]]
set [/p] <변수>=[<프롬프트문자열>]
set /a <변수>=<식>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | 인수 없이 쓰면 모든 환경 변수 표시. 값을 하나 주면 그 값으로 시작하는 변수만 표시 |
| `<변수>=<문자열>` | 변수에 값 할당. 값을 생략하면(`변수=`) 변수 삭제 |
| `/p` | 사용자 입력을 받아 변수에 저장. 프롬프트 문자열 지정 가능 |
| `/a` | 수식을 계산해 결과를 변수에 저장 |

### `/a`의 연산자 우선순위(높은 순)

| 연산자 | 연산 |
|---|---|
| `( )` | 그룹화 |
| `! ~ -` | 단항 연산 |
| `* / %` | 곱셈·나눗셈·나머지 |
| `+ -` | 덧셈·뺄셈 |
| `<< >>` | 논리 시프트 |
| `&` | 비트 AND |
| `^` | 비트 XOR |
| `= *= /= %= += -= &= ^= <<= >>=` | 대입 |
| `,` | 식 구분자 |

## 예시

```
set
set p
set include=c:\directory
set testVar=TEST^^1
set /p name=Enter your name:
set /a result=10+20
set /a "hex=0x1F"
@echo off
set path=%1;%path%
```

## 주의사항·함정

**같은 이름으로 시작하는 값을 지정하면 필터로 동작한다**: `set` 뒤에 값을 하나만 주면(등호 없이) 그 문자열로 시작하는 변수 이름을 모두 나열해 보여준다. `set path=...`처럼 등호가 있으면 할당이지만, `set p`처럼 등호가 없으면 조회 필터라는 차이를 혼동하기 쉽다.

**특수문자는 캐럿이나 따옴표로 감싸야 한다**: `<`, `>`, `|`, `&`, `^`는 값에 그대로 들어가면 셸이 먼저 해석해버린다. 캐럿(`^`)으로 이스케이프하거나 값 전체를 따옴표로 감싸야 하는데, 따옴표를 쓰면 그 따옴표 자체가 변수 값에 포함된다는 점도 함께 기억해야 한다.

**`/a`의 나머지 연산은 `%%`로 써야 한다**: 배치 파일 안에서는 `%`가 변수 참조 문자이므로, 나머지 연산자를 쓰려면 `%%`로 이스케이프해야 한다. 로직 연산자(`&&`, `||`)나 나머지 연산자를 쓸 때는 식 전체를 따옴표로 감싸는 것도 필요하다.

**숫자가 아닌 문자열은 변수 이름으로 취급된다**: `/a` 안에서 숫자가 아닌 토큰은 자동으로 환경 변수 이름으로 해석되고, 그 변수가 정의되지 않았으면 0으로 취급된다.

> "Any non-numeric strings in the expression are considered environment variable names, and their values are converted to numbers before they're processed. If you specify an environment variable name that isn't defined in the current environment, a value of zero is allotted." — Microsoft Learn, "set"

즉 `%` 기호로 감싸지 않고도 `set /a total=count+1`처럼 쓸 수 있다 — `count`는 자동으로 그 이름의 환경 변수 값으로 치환된다.

**지연된 환경 변수 확장은 기본적으로 꺼져 있다**: 01장(cmd)에서 짧게 언급한 지연된 확장(`!변수!`)은 `set`만으로는 켤 수 없고, `cmd /v:on`으로 새 세션을 열거나 40장에서 다룰 `setlocal enabledelayedexpansion`을 명시적으로 실행해야 한다. `for`나 `if` 블록 안에서 변수 값을 실시간으로 갱신하며 참조해야 하는 상황(33장에서 다시 다룬다)에서 이 설정을 빠뜨리면 항상 블록 진입 시점의 옛 값만 보인다.

**PowerShell은 세션 변수에 `set` 같은 키워드가 필요 없다**: `$var = "value"`라고 쓰면 그 자체로 PowerShell 변수에 값이 대입된다. 하지만 이렇게 만든 변수는 현재 세션(또는 스코프)에만 존재하는 것이지, CMD의 `set`이 만드는 것과 같은 **환경 변수**가 아니다 — 자식 프로세스에도 보이게 하려면 `$env:VAR = "value"`처럼 반드시 `$env:` 접두사를 붙여야 한다. "세션 변수"와 "환경 변수"를 구분하는 이 개념은 CMD에는 없다. CMD의 `set`은 애초에 환경 변수 하나만 다루므로 이런 구분이 생길 여지가 없기 때문이다.

## 흔한 오개념

<strong>"set MYVAR=Hello 뒤에 공백을 넣어도 값은 Hello다"</strong>는 오해가 있다. set은 등호 뒤에 오는 모든 문자를 값으로 취급하므로, `set MYVAR= Hello`처럼 등호 뒤에 공백을 넣으면 그 공백까지 값의 일부가 된다. 등호 앞뒤 공백을 의도치 않게 넣는 실수는 변수 비교(`if "%MYVAR%"=="Hello"`)가 항상 거짓으로 나오는 원인 중 하나다.

## 다음 장에서는

다음은 32장 — set으로 만든 변수와 파일 존재 여부, 종료 코드를 검사해 분기하는 `if` 명령을 다룬다.

## 평가 기준

- set으로 변수를 조회·설정·삭제하고, `/p`로 사용자 입력을 받을 수 있다.
- `/a`의 연산자 우선순위를 이해하고 간단한 산술식을 작성할 수 있다.
- `/a` 안에서 숫자가 아닌 토큰이 변수 이름으로 자동 해석된다는 것을 설명할 수 있다.
- 지연된 환경 변수 확장이 기본적으로 꺼져 있고, 이를 켜는 방법(cmd /v:on, setlocal enabledelayedexpansion)을 안다.
- 등호 주변 공백이 변수 값에 그대로 포함될 수 있다는 함정을 설명할 수 있다.

## 참고

- [set | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
