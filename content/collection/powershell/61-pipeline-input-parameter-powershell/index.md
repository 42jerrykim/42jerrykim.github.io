---
draft: true
collection_order: 61
slug: pipeline-input-parameter-powershell
title: "[PowerShell] 61. 파이프라인 입력 매개변수(ValueFromPipeline 등)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 함수 매개변수가 ValueFromPipeline과 ValueFromPipelineByPropertyName으로 파이프라인 입력을 받는 법과 두 방식의 차이, process 블록과의 상호작용, 사용자 정의 함수를 진짜 cmdlet처럼 파이프라인에 끼워 넣는 법을 정리한 챕터다."
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
- ValueFromPipeline
- ValueFromPipelineByPropertyName
- Process-Block
- Pipeline-Binding
- Custom-Cmdlet
- Parameter-Binding
image: "wordcloud.png"
---

## 개요

`ValueFromPipeline`과 `ValueFromPipelineByPropertyName`은 사용자 정의 함수의 매개변수가 10장부터 강조해 온 객체 파이프라인에 직접 참여하도록 만드는 매개변수 속성이다. 지금까지 만든 함수는 대부분 인자를 직접 지정해 호출했는데, 이 장을 거치면 `Get-Process | Stop-MyProcess`처럼 자신이 만든 함수도 파이프라인 왼쪽의 결과를 자연스럽게 받을 수 있게 된다.

정신 모델은 "`ValueFromPipeline`은 파이프라인 객체 **전체**를 매개변수에 담고, `ValueFromPipelineByPropertyName`은 그 객체의 **같은 이름을 가진 속성값만** 매개변수에 담는다"는 것이다. 어느 쪽이든 56장에서 배운 `process` 블록이 있어야 파이프라인 요소마다 반복 실행된다.

## 사용법

```powershell
param(
    [Parameter(Mandatory, ValueFromPipeline)]
    [string[]]$ComputerName
)
param(
    [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
    [string[]]$ComputerName
)
```

## 종류

| 속성 | 파이프라인에서 받는 것 | 요구 조건 |
|---|---|---|
| `ValueFromPipeline` | 객체 전체 | 매개변수 타입이 파이프라인 객체 타입과 일치해야 함(또는 변환 가능해야 함) |
| `ValueFromPipelineByPropertyName` | 객체의 특정 속성값 | 파이프라인 객체에 매개변수와 **이름이 같은 속성**이 있어야 함 |
| `ValueFromRemainingArguments` | 다른 매개변수에 할당되지 않은 나머지 값 전부 | 위치 매개변수와 함께 주로 사용 |
| `$input` | 파이프라인 입력 전체를 담는 열거자(enumerator) | `begin`/`end` 블록에서 파이프라인 전체를 조망할 때 |

## 예시

```powershell
function Test-ValueFromPipeline {
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string[]]$ComputerName
    )
    process {
        "객체 전체로 받음: $ComputerName"
    }
}
"Server01", "Server02" | Test-ValueFromPipeline    # 문자열 배열을 객체 그대로 받음

function Test-ValueFromPipelineByPropertyName {
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [string[]]$ComputerName
    )
    process {
        "속성으로 받음: $ComputerName"
    }
}
[pscustomobject]@{ ComputerName = "HelloWorld" } |
    Test-ValueFromPipelineByPropertyName            # ComputerName "속성"만 뽑아 바인딩

function Get-SumOfNumbers {
    param ([int[]]$Numbers)
    begin { $total = 0 }
    process {
        if ($MyInvocation.ExpectingInput) {
            $total += $_                             # 파이프라인 입력일 때
        } else {
            foreach ($n in $Numbers) { $total += $n }  # 매개변수로 직접 받았을 때
        }
    }
    end { "합계 = $total" }
}
1, 2, 3, 4 | Get-SumOfNumbers                          # 파이프라인 입력
Get-SumOfNumbers -Numbers 1, 2, 3, 4                     # 매개변수 직접 지정 — 같은 결과
```

## 주의사항·함정

**`process` 블록이 없으면 파이프라인 입력이 있어도 함수가 딱 한 번만 실행된다**: 57장에서 짚었듯, `ValueFromPipeline`을 매개변수에 붙였더라도 함수 본문에 `process` 블록을 정의하지 않으면 여러 객체가 파이프라인으로 들어와도 함수는 첫 객체만(또는 예측 불가능하게) 처리하고 만다. 파이프라인 입력을 정말로 하나씩 처리하려면 `process` 블록이 필수다.

**두 속성을 같은 매개변수에 함께 붙이면 우선순위가 헷갈릴 수 있다**: `ValueFromPipeline`과 `ValueFromPipelineByPropertyName`을 동시에 지정하면, PowerShell은 먼저 객체 전체 타입이 일치하는지 시도하고, 실패하면 속성 이름으로 다시 시도한다. 이 이중 시도가 항상 직관적이지는 않으므로, 파이프라인 객체의 타입이 명확하지 않다면 둘 중 하나만 선택하는 편이 예측하기 쉽다.

**`ValueFromPipelineByPropertyName`은 속성 이름이 정확히 일치해야 동작하고, 별칭(alias)은 매개변수 쪽에서 등록해야 한다**: 파이프라인 객체의 속성 이름이 매개변수 이름과 다르면(예: 객체는 `CN`, 매개변수는 `ComputerName`) 바인딩되지 않는다. 이런 경우 매개변수에 `[Alias("CN")]`을 추가해 별칭을 등록해야 두 이름 모두로 바인딩이 가능해진다.

**이식성**: Bash·CMD 파이프는 텍스트 스트림만 전달하므로, "속성 이름으로 자동 바인딩"이라는 개념 자체가 존재하지 않는다 — 스크립트가 직접 각 줄을 파싱해 원하는 필드를 추출해야 한다. PowerShell의 `ValueFromPipelineByPropertyName`은 10장에서 강조한 객체 파이프라인의 정수를 사용자 정의 함수에까지 그대로 확장한 기능이다.

## Reference

- [about_Functions_Advanced_Parameters - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters)
