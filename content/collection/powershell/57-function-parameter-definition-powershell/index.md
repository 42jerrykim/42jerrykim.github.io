---
draft: false
collection_order: 57
slug: function-parameter-definition-powershell
title: "[PowerShell] 57. 함수 정의와 매개변수"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell function 키워드로 함수를 만드는 법과 param() 블록으로 명명된 매개변수를 정의하는 법, 위치 매개변수와 $args 배열의 관계, 파이프라인을 처리하는 process 블록과 filter 키워드의 역할을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Scripting(스크립팅)
- Guide(가이드)
- Education(교육)
- Beginner
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Function
- Parameter
- Filter-Keyword
- Return-Value
- Positional-Parameter
- Process-Block
image: "wordcloud.png"
---

## 개요

**함수**는 `function` 키워드로 이름을 붙인 재사용 가능한 명령 블록이다. 53장에서 스크립트 전체를 하나의 단위로 실행하는 법을 배웠다면, 이 장은 스크립트 **안에서** 반복되는 로직을 이름 붙인 단위로 나누는 법을 다룬다. 잘 만든 함수는 사용하는 쪽에서 보면 실제 cmdlet과 거의 구분되지 않는다.

정신 모델은 "함수는 이름이 붙은 스크립트 블록이고, `param()`은 그 함수가 받을 입력의 이름표"라는 것이다. 함수 안의 모든 문장이 만들어내는 출력은 파이프라인으로 흘러나가 자동으로 함수의 반환값이 된다 — `return`은 선택 사항이며, 값을 계산하는 명령문이 있다면 그 자체로 이미 출력이다.

## 사용법

```powershell
function <이름> {
    param ([타입]$매개변수1, [타입]$매개변수2 = 기본값)
    <문장 목록>
}
filter <이름> { <문장 목록> }        # process 블록만 있는 함수의 축약형
```

## 종류

| 요소 | 설명 |
|---|---|
| 명명된 매개변수 | `param()`으로 선언, `-이름 값` 형태로 호출 |
| 위치 매개변수 | `param()` 순서대로 이름 없이 값만 전달 가능(41장의 위치 매개변수 개념과 동일) |
| `$args` | `param()`으로 선언되지 않은 나머지 인자를 담는 자동 배열(고급 함수에서는 사용 불가) |
| `[switch]` 매개변수 | 값 없이 존재 여부로 참/거짓을 전달(26장의 `-WhatIf`도 이 방식) |
| `filter` | `process` 블록만 있는 함수의 축약형, 파이프라인 요소별 처리에 특화 |
| `return` | 그 지점에서 함수를 즉시 종료(출력 자체를 억제하지는 않음) |

## 예시

```powershell
function Get-SmallFiles {
    param ($Size = 100)
    Get-ChildItem $HOME | Where-Object { $_.Length -lt $Size -and !$_.PSIsContainer }
}
Get-SmallFiles -Size 50                # 명명된 매개변수
Get-SmallFiles 50                       # 위치 매개변수(같은 결과)

function Add-Numbers([int]$One, [int]$Two) {   # param() 없이 괄호로 바로 선언(대안 문법)
    $One + $Two
}

function Switch-Item {
    param ([switch]$On)
    if ($On) { "켜짐" } else { "꺼짐" }
}
Switch-Item -On                          # "켜짐"

function Get-Extension {                  # $args로 위치 인자 직접 접근
    $args[0] + ".txt"
}
Get-Extension myfile                       # "myfile.txt"

filter Get-EventMessage ([switch]$MessageOnly) {   # process 블록 축약형
    if ($MessageOnly) { $_.Message } else { $_ }
}
Get-WinEvent -LogName System -MaxEvents 10 | Get-EventMessage -MessageOnly

function Get-Pipeline {
    process { "값: $_" }                   # 파이프라인 입력을 한 번에 하나씩 처리
}
1, 2, 4 | Get-Pipeline
```

## 주의사항·함정

**스크립트 파일 안에서는 함수가 호출되기 전에 먼저 정의돼 있어야 한다**: 대화형 세션에서는 함수를 나중에 정의해도 상관없지만, `.ps1` 스크립트 파일 안에서는 함수 정의가 그 함수를 호출하는 코드보다 앞에 있어야 한다. 파일 아래쪽에 정의한 함수를 파일 위쪽에서 호출하면 "인식할 수 없는 명령" 오류가 난다.

**파이프라인 입력을 처리하려면 `process` 블록이 반드시 있어야 한다**: 함수의 매개변수에 파이프라인 입력을 받도록 설정했더라도(61장에서 다룰 `ValueFromPipeline`), `process` 블록을 정의하지 않으면 파이프라인으로 여러 객체를 넘겨도 함수가 딱 한 번만 실행된다. `begin`/`process`/`end` 중 어떤 것도 쓰지 않으면 모든 코드가 암묵적으로 `end` 블록에 들어간다는 점을 기억해야 한다.

**`$args`는 명명된 매개변수를 `param()`으로 선언하는 순간 함께 쓰기 까다로워진다**: `$args`는 "선언되지 않은 나머지 인자"를 담는 배열이라, `param()`에 이미 매개변수를 여러 개 선언한 함수에서는 `$args`가 텅 비어 있거나 혼란스러운 값만 남기 쉽다. 58장에서 다룰 `[CmdletBinding()]`을 붙인 고급 함수에서는 `$args` 자체가 아예 비활성화된다.

**이식성**: Bash 함수(`function name() { ... }`)는 기본적으로 위치 인자(`$1`, `$2`, `$@`)만 지원하고 명명된 매개변수 개념이 없어, PowerShell의 `param()` 기반 함수보다 표현력이 제한적이다. CMD의 배치 서브루틴(`:label`/`call :label`)은 함수라는 개념 자체가 없어 `%1`, `%2`처럼 위치 인자만 훨씬 제한적으로 다룰 수 있다.

## Reference

- [about_Functions - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions)
