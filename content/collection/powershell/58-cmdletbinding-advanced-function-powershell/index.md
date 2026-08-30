---
draft: false
collection_order: 58
slug: cmdletbinding-advanced-function-powershell
title: "[PowerShell] 58. [CmdletBinding()]과 고급 함수"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell [CmdletBinding()] 속성이 일반 함수를 컴파일된 cmdlet처럼 만드는 원리와 공통 매개변수 자동 추가, SupportsShouldProcess로 -WhatIf/-Confirm을 얻는 법, $PSCmdlet 자동 변수를 정리한 챕터다."
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
- CmdletBinding
- Advanced-Function
- SupportsShouldProcess
- Common-Parameters
- PSCmdlet
- ShouldProcess
image: "wordcloud.png"
---

## 개요

`[CmdletBinding()]`은 57장에서 만든 일반 함수를 25장에서 다룬 공통 매개변수(`-Verbose`, `-ErrorAction` 등)까지 갖춘 <strong>고급 함수(advanced function)</strong>로 승격시키는 속성이다. 이 속성 하나를 함수 맨 위에 붙이는 것만으로, 사용자 입장에서는 그 함수가 C#으로 컴파일된 진짜 cmdlet인지 PowerShell 함수인지 구분할 수 없게 된다.

정신 모델은 "`[CmdletBinding()]`은 함수에게 `$PSCmdlet`이라는 특수 변수와 cmdlet급 매개변수 바인딩 규칙을 부여하는 스위치"라는 것이다. 이 스위치를 켜는 순간 57장에서 다룬 `$args` 자동 변수는 비활성화되고, 대신 더 엄격하고 예측 가능한 매개변수 처리 방식이 적용된다.

## 사용법

```powershell
function <이름> {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
    param ($매개변수1)
    <문장 목록>
}
```

## 종류

| CmdletBinding 인자 | 효과 |
|---|---|
| (인자 없음) | 공통 매개변수 자동 추가, `$PSCmdlet` 사용 가능 |
| `SupportsShouldProcess` | `-WhatIf`/`-Confirm` 매개변수 추가(26장에서 다룬 그 동작을 직접 함수에 구현) |
| `ConfirmImpact` | `-Confirm` 프롬프트가 뜨는 민감도 기준(`Low`/`Medium`/`High`) |
| `DefaultParameterSetName` | 매개변수 세트가 여러 개일 때 기본으로 선택할 세트 |
| `PositionalBinding` | `$false`로 지정하면 매개변수가 기본적으로 위치 기반이 되지 않도록 변경 |
| `SupportsPaging` | `-First`/`-Skip`/`-IncludeTotalCount` 매개변수 자동 추가(대용량 결과 페이징용) |

## 예시

```powershell
function Remove-TempFile {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param ([string]$Path)

    if ($PSCmdlet.ShouldProcess($Path, "삭제")) {
        Remove-Item -Path $Path
    }
}
Remove-TempFile -Path C:\Temp\old.log -WhatIf     # 실제 삭제 없이 예고만
Remove-TempFile -Path C:\Temp\old.log -Confirm     # 삭제 전 확인 프롬프트

function Test-Something {
    [CmdletBinding()]
    param ($Value)
    Write-Verbose "값을 확인하는 중: $Value"           # -Verbose 없이는 표시 안 됨(25장)
    $Value
}
Test-Something -Value 42 -Verbose                    # 이제 Write-Verbose 메시지도 보임

function Get-Numbers {
    [CmdletBinding(SupportsPaging)]
    param()
    $first = $PSCmdlet.PagingParameters.Skip
    $last = $first + $PSCmdlet.PagingParameters.First - 1
    $first..$last
}
```

## 주의사항·함정

**`[CmdletBinding()]`을 붙이면 `$args`가 완전히 사라진다**: 57장에서 쓴 `$args` 자동 변수는 고급 함수에서는 지원되지 않는다 — `param()`에 선언되지 않은 인자를 넘기면 바인딩 오류가 난다. 알 수 없는 매개변수를 관대하게 받아 그대로 다른 명령에 넘기던 함수를 고급 함수로 바꾸려면, `ValueFromRemainingArguments` 인자를 가진 명시적 매개변수로 다시 설계해야 한다.

**`SupportsShouldProcess`만 붙이고 `ShouldProcess()` 호출을 빠뜨리면 `-WhatIf`가 아무 효과도 없다**: `[CmdletBinding(SupportsShouldProcess)]`는 `-WhatIf`/`-Confirm` 매개변수를 함수에 "추가"만 할 뿐, 실제로 그 값에 따라 동작을 건너뛰는 로직은 함수 작성자가 `if ($PSCmdlet.ShouldProcess(...))`로 직접 구현해야 한다. 이 호출을 빠뜨리면 `-WhatIf`를 줘도 실제 변경이 그대로 실행되는, 매우 위험한 착각을 일으키는 함수가 된다.

**공통 매개변수 이름과 겹치는 매개변수는 만들 수 없다**: `[CmdletBinding()]`을 쓰는 순간 `-Verbose`, `-ErrorAction`, `-WarningAction` 같은 공통 매개변수가 자동으로 예약되므로, 함수 자체의 매개변수 중 하나를 같은 이름으로 지으면 충돌 오류가 난다.

**이식성**: Bash·CMD에는 사용자 정의 함수가 내장 명령과 동일한 표준화된 옵션 인터페이스(공통 매개변수, `-WhatIf` 같은 안전장치)를 자동으로 얻는 개념 자체가 없다 — 각 스크립트가 `getopts`나 수동 인자 파싱으로 매번 새로 구현해야 한다. `[CmdletBinding()]`이 제공하는 이 통일성은 PowerShell 생태계 전체의 명령이 비슷한 방식으로 동작하게 만드는 핵심 장치다.

## Reference

- [about_Functions_CmdletBindingAttribute - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute)
