---
draft: false
slug: setlocal-endlocal-command-variable-scope-windows-cmd
title: "[CMD] 40. setlocal, endlocal - 환경 변수 유효 범위"
description: "setlocal과 endlocal로 배치 파일의 환경 변수·현재 디렉터리 변경을 블록 안으로 국한하는 법과, enabledelayedexpansion으로 !변수! 지연 확장을 켜는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 400
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
- Advanced
- setlocal
- endlocal
- 변수유효범위
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Command-Extensions
- Comparison(비교)
- Configuration(설정)
- Beginner
- Administration
image: "wordcloud.png"
---

setlocal은 배치 파일 안에서 환경 변수 변경을 지역화하기 시작하는 명령이고, endlocal은 그 지역화를 끝내는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [39장: rem](/post/cmd/rem-command-batch-comments-windows-cmd/)에서 주석을 다룬 뒤 이어진다. 지금까지 배운 배치 스크립팅 도구(echo, set, if, for, call, goto, shift, pause, exit, rem)를 실전에서 안전하게 조합하려면, 그 변경 사항이 어디까지 영향을 미치는지 통제하는 이 장의 내용이 필요하다. 11장(pushd, popd)에서 이미 "setlocal과 함께 쓰면 디렉터리 스택도 자동 정리된다"고 예고했던 내용이 바로 이 장이다.

**이 장의 깊이**: 중급–고급. **다루지 않는 것**: 지연된 확장이 실제로 필요해지는 구체적인 반복문 패턴은 33장(for)에서 이미 언급했다. 이 장은 그 기능을 켜는 방법 자체에 집중한다.

## 사용법

```
setlocal [enableextensions | disableextensions] [enabledelayedexpansion | disabledelayedexpansion]
endlocal
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `enableextensions` | endlocal을 만날 때까지 명령 확장을 강제로 켬 |
| `disableextensions` | endlocal을 만날 때까지 명령 확장을 강제로 끔 |
| `enabledelayedexpansion` | endlocal을 만날 때까지 지연된 환경 변수 확장(`!변수!`)을 켬 |
| `disabledelayedexpansion` | endlocal을 만날 때까지 지연된 환경 변수 확장을 끔 |

## 예시

```bat
rem *******Begin Comment**************
rem This program starts the superapp batch program on the network,
rem directs the output to a file, and displays the file in Notepad.
rem *******End Comment**************
@echo off
setlocal
path=g:\programs\superapp;%path%
call superapp>c:\superapp.out
endlocal
start notepad c:\superapp.out
```

```bat
setlocal enabledelayedexpansion
set count=0
for %%f in (*.txt) do (
  set /a count+=1
  echo 지금까지 !count!개 처리함
)
endlocal
```

## 주의사항·함정

**setlocal 이후 변경은 endlocal이나 배치 종료 시 자동으로 되돌아간다**: setlocal을 실행한 뒤 바꾼 환경 변수와 현재 디렉터리는 endlocal을 만나거나 배치 파일이 끝나는 순간 setlocal 실행 이전 상태로 자동 복원된다. 대화형 CMD 세션 밖에서(즉 명령 프롬프트에 직접 입력해서) setlocal을 쓰면 아무 효과가 없다는 것도 함께 기억해야 한다.

**중첩할 수 있다**: setlocal과 endlocal을 배치 프로그램 안에서 여러 번 중첩해 쓸 수 있다. endlocal은 가장 최근에 실행된(가장 안쪽) setlocal부터 순서대로 해제한다.

**지연된 확장이 왜 필요한지는 33장(for)의 함정을 떠올리면 된다**: `for` 블록이나 `if` 블록 전체는 파싱 시점에 한 번에 해석되기 때문에, 블록 안에서 `%var%`로 변수를 참조하면 그 블록에 진입하기 전의 옛 값만 보인다. `enabledelayedexpansion`을 켜고 `%var%` 대신 `!var!`를 쓰면, 블록이 실제로 실행되는 매 순간의 최신 값을 읽을 수 있다. 위 예시에서 `set /a count+=1` 직후 `!count!`가 매 반복마다 갱신된 값을 보여주는 이유다.

**setlocal은 ERRORLEVEL을 설정해 명령 확장 지원 여부를 검사하는 데 쓸 수 있다**: setlocal에 `enableextensions`나 `enabledelayedexpansion` 같은 인자를 주면 성공 시 ERRORLEVEL을 0으로, 인자 없이 쓰면 1로 설정한다.

> "The **setlocal** command sets the ERRORLEVEL variable. If you pass {**enableextensions** | **disableextensions**} or {**enabledelayedexpansion** | **disabledelayedexpansion**}, the ERRORLEVEL variable is set to **0** (zero). Otherwise, it's set to **1**." — Microsoft Learn, "setlocal"

Microsoft Learn은 이를 이용해 명령 확장이 실제로 지원되는 환경인지 검사하는 패턴을 예시로 든다.

```bat
verify other 2>nul
setlocal enableextensions
if errorlevel 1 echo Unable to enable extensions
```

**호출한 쪽 세션에는 영향이 없다**: 34장(call)에서 다른 배치 파일을 호출했을 때, 호출된 배치 안에서 setlocal로 감싼 변경은 그 배치가 끝나면 사라지고 호출한 쪽 환경에는 전혀 반영되지 않는다. 여러 배치 파일이 협업하는 큰 스크립트를 짤 때, 서브루틴이 의도치 않게 부모 환경을 오염시키는 것을 막는 안전장치로 setlocal을 적극 활용할 수 있다.

**PowerShell에는 setlocal에 직접 대응하는 명령이 없다**: 스크립트와 함수 자체가 언어 차원에서 블록·함수 단위 변수 스코프를 갖고 있어서, "여기부터 지역 범위를 시작한다"고 명시적으로 선언할 필요가 없기 때문이다. CMD의 배치 모델은 기본적으로 변수가 전역인 평평한(flat) 환경이라 setlocal 같은 장치로 일부러 지역화해야 하지만, PowerShell 함수는 처음부터 자신만의 스코프를 갖고 시작한다. 마찬가지로 이 장에서 다룬 "지연된 확장"을 켜고 끄는 개념도 PowerShell에는 없다 — CMD의 괄호 블록처럼 코드 전체를 실행 전에 미리 문자열로 치환하는 파싱 단계가 PowerShell에는 없으므로, 애초에 켜고 꺼야 할 대상 자체가 존재하지 않는다.

## 흔한 오개념

<strong>"setlocal의 변수 격리는 PowerShell 함수의 로컬 스코프와 같은 것이다"</strong>는 오해가 있다. 결과가 비슷해 보여서 생기는 착각이지만, setlocal은 새로운 변수 이름 공간이나 진짜 렉시컬 스코프를 만드는 것이 아니라, 그 시점의 환경 상태를 스냅숏으로 기억해뒀다가 endlocal에서 되돌리는 것에 가깝다. 이 차이는 중첩된 setlocal이나, 중첩된 for 반복문이 각자 지연된 확장 상태를 따로 필요로 하는 경우처럼 가장자리 상황에서 다르게 나타난다 — PowerShell 함수의 로컬 스코프는 호출될 때마다 독립된 이름 공간을 새로 만드는 반면, setlocal은 어디까지나 하나의 공유된 환경을 임시로 저장·복원하는 메커니즘일 뿐이다.

## 다음 장에서는

다음은 41장 — Part 4의 마지막 장으로, 레거시 확장 CTRL+C 검사 설정을 다루는 `break` 명령을 다룬다.

## 평가 기준

- setlocal과 endlocal로 환경 변수·현재 디렉터리 변경을 블록 안으로 제한할 수 있다.
- setlocal과 endlocal을 중첩해 쓸 수 있고, endlocal이 가장 안쪽부터 해제된다는 것을 안다.
- `enabledelayedexpansion`이 왜 필요한지, `%var%`와 `!var!`의 차이를 설명할 수 있다.
- setlocal의 ERRORLEVEL 설정을 이용해 명령 확장 지원 여부를 검사하는 패턴을 이해한다.

## 참고

- [setlocal | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setlocal)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
