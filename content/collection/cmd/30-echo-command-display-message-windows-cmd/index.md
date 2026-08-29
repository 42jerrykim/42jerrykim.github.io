---
draft: false
slug: echo-command-display-message-windows-cmd
title: "[CMD] 30. echo - 메시지 출력과 에코 설정"
description: "echo로 메시지를 출력하고 명령 에코를 켜고 끄는 법과, echo.으로 빈 줄을 출력하되 변수가 비었을 때 ECHO is off로 오염되는 함정, 캐럿(^)으로 특수문자를 이스케이프하는 규칙을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 300
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
- echo
- 배치스크립팅
- Batch
- Escape
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Advanced
- Command-Extensions
- Administration
image: "wordcloud.png"
---

echo는 메시지를 화면에 출력하거나, 배치 파일에서 실행되는 명령 자체를 화면에 보여줄지(에코) 켜고 끄는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [29장: more](/post/cmd/more-command-page-output-windows-cmd/)로 Part 3(텍스트 검색과 출력 제어)을 마친 뒤 이어지며, <strong>Part 4(배치 스크립팅)</strong>의 첫 장이다. 지금까지 세 Part는 이미 있는 파일과 그 내용을 다뤘다면, 이 장부터는 명령을 반복 가능한 `.bat` 프로그램으로 묶는 법을 다룬다.

**이 장의 깊이**: 입문. echo 자체는 단순하지만, 배치 스크립팅 전반에서 가장 많이 쓰이는 명령이라 함정도 그만큼 잘 알려져 있다. **다루지 않는 것**: 변수 자체를 만들고 값을 넣는 것은 31장(set)에서 다룬다.

## 사용법

```
echo [<메시지>]
echo [on | off]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `on` \| `off` | 명령 에코 기능을 켜거나 끔(기본값은 on) |
| `<메시지>` | 화면에 표시할 텍스트 |

인수 없이 `echo`만 실행하면 현재 에코 설정을 표시한다.

## 예시

```
echo
echo.
echo Hello World
echo off
@echo off
echo Current date: %date%
if exist *.rpt echo The report has arrived.
```

```bat
@echo off
if not exist *.txt (
echo This directory contains no text files.
) else (
   echo This directory contains the following text file^(s^):
   echo.
   dir /b *.txt
   )
```

## 주의사항·함정

**`echo.`은 점 앞에 공백이 있으면 안 된다**: 빈 줄을 출력하는 관용구인 `echo.`은 점과 echo 사이에 공백이 없어야 한다. 공백을 넣으면 점 자체가 그대로 출력된다.

> "To echo a blank line on the screen, type: echo. — Don't include a space before the period. Otherwise, the period appears instead of a blank line." — Microsoft Learn, "echo"

**변수가 비어 있으면 "ECHO is off."가 출력된다**: `echo %var%`에서 `var`가 정의되지 않았거나 빈 문자열이면, 화면에는 의도한 빈 줄 대신 다음 메시지가 나온다.

> "If there's an empty variable in a batch file while using **echo**, it displays 'ECHO is off'. To prevent seeing this message, and produce a blank line instead, place a colon (`:`) between **echo** and the variable. For example, `echo:%var%`." — Microsoft Learn, "echo"

즉 `echo %var%` 대신 `echo:%var%`로 쓰면, `var`가 비어 있어도 "ECHO is off." 대신 빈 줄이 출력된다. 사용자 입력이나 외부 명령 결과를 그대로 echo로 출력하는 스크립트에서 이 함정에 자주 걸린다.

**특수문자는 캐럿(`^`)으로 이스케이프한다**: 파이프(`|`), 앰퍼샌드(`&`), 리다이렉션(`<`, `>`)을 그대로 출력하려면 그 문자 바로 앞에 `^`를 붙인다. 괄호로 묶인 블록(`if`나 `for`의 본문) 안에서는 여는 괄호·닫는 괄호(`(`, `)`) 자체도 `^`로 이스케이프해야 한다는 점이 특히 자주 놓치는 부분이다 — 위 두 번째 예시의 `echo.` 앞줄에서 `^(s^)`가 그 사례다. 느낌표(`!`)를 출력하려면 문자열 전체를 큰따옴표로 감싼 뒤 느낌표 앞에 캐럿을 붙이거나(`"Hello World^!"`), 큰따옴표 없이 캐럿을 두 번 겹쳐 쓴다(`Hello World^^!`).

**PowerShell의 대응 명령은 두 갈래로 나뉜다**: `Write-Host`는 콘솔에 직접 출력한다는 점에서 echo의 단순한 화면 표시 목적과 비슷하지만, `Write-Output`은 화면이 아니라 **파이프라인**에 값을 흘려보내 다음 명령이 그 데이터를 이어받게 하는 용도다. 이 둘은 흔히 오해하듯 서로 바꿔 써도 되는 관계가 아니다 — 파이프라인으로 데이터를 넘길 작정으로 `Write-Host`를 쓰면 그 출력은 캡처도 파이프도 되지 않아 조용히 사라져 버린다. CMD의 echo는 애초에 화면 표시라는 목적 하나만 가지므로 이런 구분 자체가 존재하지 않는다.

## 흔한 오개념

<strong>"Write-Host와 Write-Output은 그냥 화면에 출력하는 두 가지 방법일 뿐이다"</strong>는 오해가 있다. CMD에서 넘어온 사람뿐 아니라 PowerShell을 어느 정도 써본 사람도 자주 걸리는 함정이다. `Write-Output`은 파이프라인으로 객체를 내보내 `$result = Get-Thing`처럼 다음 명령이나 변수가 그 값을 받을 수 있게 하지만, `Write-Host`는 콘솔에 직접 그리는 것이라 변수에 담거나 파이프로 넘길 수 없다. 함수 안에서 진행 상황 로그는 `Write-Host`로, 실제 반환값은 값을 그대로 남기거나 `Write-Output`으로 내보내는 식으로 구분하지 않으면, 함수의 반환값에 로그 메시지가 뒤섞여 들어가는 버그가 생긴다.

## 다음 장에서는

다음은 31장 — 환경 변수를 표시·설정하고 산술 연산까지 지원하는 `set` 명령을 다룬다.

## 평가 기준

- echo로 메시지를 출력하고, `echo off`/`echo on`으로 명령 에코를 제어할 수 있다.
- `echo.`으로 빈 줄을 출력할 때 점 앞에 공백이 없어야 하는 이유를 설명할 수 있다.
- 빈 변수를 echo할 때 "ECHO is off."가 출력되는 함정과 `echo:` 해법을 설명할 수 있다.
- `^`로 특수문자와 괄호를 이스케이프하는 규칙을 적용할 수 있다.

## 참고

- [echo | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/echo)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
