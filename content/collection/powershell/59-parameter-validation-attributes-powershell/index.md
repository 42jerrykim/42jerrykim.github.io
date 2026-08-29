---
draft: true
collection_order: 59
slug: parameter-validation-attributes-powershell
title: "[PowerShell] 59. 매개변수 검증(Validate 속성군)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell ValidateSet/ValidateRange/ValidatePattern/ValidateScript 같은 매개변수 검증 속성으로 함수 본문에 도달하기 전 입력값을 걸러내는 법과 Mandatory·AllowNull 등 필수성 관련 속성을 정리한 챕터다."
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
- ValidateSet
- ValidateRange
- ValidateScript
- Parameter-Attribute
- Input-Validation
- Mandatory-Parameter
image: "wordcloud.png"
---

## 개요

**매개변수 검증 속성**은 함수 본문이 실행되기도 전에 잘못된 입력을 걸러내는 선언적 규칙이다. 58장의 `[CmdletBinding()]`이 함수를 cmdlet처럼 보이게 만드는 뼈대였다면, 이 장의 `Validate*` 속성들은 26장에서 다룬 `-WhatIf`처럼 함수 안에 `if` 문을 직접 쓰지 않고도 "이 값은 받아들일 수 없다"를 PowerShell 엔진이 대신 판단하게 만든다.

정신 모델은 "함수 본문에 도달하는 시점에는 이미 입력값이 유효하다고 신뢰할 수 있어야 한다"는 것이다. 검증을 매개변수 선언에 몰아두면, 함수 본문은 오직 "정상적인 값으로 무엇을 할지"에만 집중할 수 있다.

## 사용법

```powershell
param (
    [Parameter(Mandatory)]
    [ValidateSet("Low", "Average", "High")]
    [string]$Detail
)
```

## 종류

| 속성 | 검증 내용 |
|---|---|
| `Mandatory` | 값이 반드시 있어야 함(생략하면 프롬프트로 물어봄) |
| `ValidateNotNullOrEmpty` | `$null`, 빈 문자열(`""`), 빈 배열(`@()`)을 모두 거부 |
| `ValidateSet` | 지정한 값 목록 중 하나여야 함(탭 자동완성도 함께 제공) |
| `ValidateRange` | 숫자가 지정한 범위 안에 있어야 함(`Positive`/`Negative` 등 키워드도 가능) |
| `ValidatePattern` | 정규식(47장)과 일치해야 함 |
| `ValidateLength` | 문자열 길이가 최소·최대 범위 안에 있어야 함 |
| `ValidateCount` | 배열의 요소 개수가 최소·최대 범위 안에 있어야 함 |
| `ValidateScript` | 임의의 스크립트 블록이 `$true`를 반환해야 함(가장 유연함) |
| `AllowNull` / `AllowEmptyString` / `AllowEmptyCollection` | 필수 매개변수인데도 예외적으로 비어 있는 값을 허용 |

## 예시

```powershell
function Set-Priority {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Low", "Average", "High")]
        [string]$Detail
    )
    "우선순위: $Detail"
}
Set-Priority -Detail Medium    # 오류 — 목록에 없는 값

function Set-RetryCount {
    param (
        [Parameter(Mandatory)]
        [ValidateRange(0, 10)]
        [int]$Attempts
    )
    "재시도 횟수: $Attempts"
}
Set-RetryCount -Attempts 15     # 오류 — 범위 초과

function Set-TicketId {
    param (
        [Parameter(Mandatory)]
        [ValidatePattern("^[0-9]{4}$")]
        [string]$TicketId
    )
    "티켓: $TicketId"
}

function New-Event {
    param (
        [Parameter(Mandatory)]
        [ValidateScript(
            { $_ -ge (Get-Date) },
            ErrorMessage = "{0}은(는) 미래 날짜가 아닙니다."
        )]
        [datetime]$EventDate
    )
    "행사 예정일: $EventDate"
}

function Get-Server {
    param (
        [Parameter(Mandatory)]
        [ValidateCount(1, 5)]
        [string[]]$ComputerName
    )
    $ComputerName
}
```

## 주의사항·함정

**검증은 사용자가 입력한 값에만 적용되고, 기본값이나 스크립트 내부의 대입에는 적용되지 않는다고 오해하기 쉽다**: 실제로는 반대다 — `ValidateSet` 같은 속성이 붙은 변수는 함수 호출 시점의 인자뿐 아니라, 함수 **내부**에서 그 변수에 값을 다시 대입할 때도 똑같이 검사한다. `[ValidateSet("hello","world")] [string]$Message`로 선언된 변수에 함수 안에서 `$Message = "bye"`를 대입하면 런타임에 오류가 난다는 점을 놓치면, "왜 내가 직접 넣은 값인데 검증에 걸리지?"라는 혼란에 빠지기 쉽다.

**`ValidateScript`는 `$null` 값을 검증할 수 없다**: 매개변수에 `$null`을 넘기면 `ValidateScript`의 스크립트 블록 자체가 그 값을 판단할 방법이 없어 오류가 난다. `$null`을 허용하면서 검증도 하고 싶다면 `AllowNull`과 `ValidateScript`를 함께 쓰되, 스크립트 블록 안에서 `$null` 여부를 먼저 명시적으로 처리해야 한다.

**`ValidateNotNull`과 `ValidateNotNullOrEmpty`를 혼동하기 쉽다**: `[string]` 타입 매개변수에 `ValidateNotNull`만 붙이면, `$null`이 문자열 타입으로 변환되는 과정에서 자동으로 빈 문자열(`""`)로 바뀌어 버려 검증이 실질적으로 아무 효과가 없다. 문자열 매개변수에서 빈 값까지 막고 싶다면 반드시 `ValidateNotNullOrEmpty`를 써야 한다.

**이식성**: Bash·CMD 스크립트에서는 매개변수 검증을 `if [ -z "$1" ]`처럼 함수 본문 맨 앞에 수작업으로 작성해야 하고, 이런 검증 코드가 실제 로직과 뒤섞여 가독성을 해치기 쉽다. PowerShell의 선언적 검증 속성은 "무엇을 받을 것인가"와 "받은 값으로 무엇을 할 것인가"를 문법적으로 분리해 준다는 점에서 근본적으로 다른 접근이다.

## Reference

- [about_Functions_Advanced_Parameters - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters)
