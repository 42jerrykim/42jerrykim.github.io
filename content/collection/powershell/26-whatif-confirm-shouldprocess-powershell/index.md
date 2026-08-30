---
draft: false
collection_order: 26
slug: whatif-confirm-shouldprocess-powershell
title: "[PowerShell] 26. -WhatIf/-Confirm과 ShouldProcess"
date: 2026-08-29
lastmod: 2026-08-29
description: "위험한 작업을 실행 전에 시뮬레이션하는 -WhatIf, 확인을 요구하는 -Confirm 매개변수의 동작 방식과 $ConfirmPreference 기본 임계값, 직접 만든 함수에 이 매개변수를 추가하는 SupportsShouldProcess를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
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
- WhatIf
- Confirm
- ShouldProcess
- Risk-Mitigation
- Cmdlet-Binding
- Remove-Item
- Function
image: "wordcloud.png"
---

## 개요

`-WhatIf`와 `-Confirm`은 25장의 다른 공통 매개변수와 달리 "위험 완화 매개변수(risk mitigation parameter)"로 따로 분류된다. 시스템이나 사용자 데이터에 위험을 끼칠 수 있는 cmdlet(주로 `Remove-*`, `Set-*`, `Stop-*` 계열)이 이 매개변수를 제공한다 — `-WhatIf`는 실제로 실행하지 않고 무엇을 할지만 보여주고, `-Confirm`은 실행 전에 승인을 요구한다.

## 사용법

```powershell
<위험한-cmdlet> -WhatIf
<위험한-cmdlet> -Confirm
```

## 매개변수

| 매개변수 | 동작 |
|---|---|
| `-WhatIf`(`wi`) | 실제 실행 대신 "무엇을 할 것인가"를 메시지로만 출력한다. `$WhatIfPreference`를 이 명령에 한해 재정의한다 |
| `-Confirm`(`cf`) | 실행 전 `[Y] Yes [A] Yes to All [N] No [L] No to All [S] Suspend [?] Help` 프롬프트를 띄운다 |
| `-Confirm:$false` | 자동 확인을 강제로 끈다(cmdlet의 기본 위험도가 `$ConfirmPreference`보다 높아 자동으로 확인을 요구하는 경우에도) |

`Suspend`(S) 옵션은 명령을 잠시 멈추고 중첩 세션을 열어, 그 안에서 다른 명령(예: `Get-Help`)을 실행해 본 뒤 `exit`로 돌아와 원래의 확인 여부를 마저 선택할 수 있게 해준다.

## 예시

```powershell
Remove-Item Date.csv -WhatIf
# 출력: What if: Performing operation "Remove File" on Target "C:\ps-test\date.csv".

Remove-Item tmp*.txt -Confirm
# Y/A/N/L/S/? 프롬프트 표시 후 선택에 따라 실행

New-Item -ItemType File -Name Test.txt -Confirm
# S(Suspend)로 중첩 세션을 열어 Get-Help로 매개변수를 확인한 뒤 exit, 이어서 Y 선택
```

직접 만든 함수에 이 매개변수를 추가하려면 `[CmdletBinding(SupportsShouldProcess)]`를 붙이고, 실제 위험한 동작 직전에 `$PSCmdlet.ShouldProcess(...)`를 호출해 그 반환값(Boolean)으로 실행 여부를 결정한다.

```powershell
function Remove-MyThing {
    [CmdletBinding(SupportsShouldProcess)]
    param([string]$Path)

    if ($PSCmdlet.ShouldProcess($Path, 'Remove')) {
        Remove-Item -Path $Path
    }
}
```

## 주의사항·함정

**`-WhatIf`는 명령을 완전히 건너뛰지, 부분적으로 실행하지 않는다**: `-WhatIf`를 준 명령은 대상 시스템에 어떤 변경도 가하지 않는다. 다만 명령 자체가 조회성 하위 작업(예: 대상이 존재하는지 확인하는 조회)을 미리 수행하는 경우는 있을 수 있으므로, 완전히 부작용 없는 실행이라고 가정하기보다는 "주요 변경 동작만 건너뛴다"고 이해하는 편이 정확하다.

**`-Confirm`을 지정하지 않아도 위험도가 높으면 자동으로 확인을 요구할 수 있다**: cmdlet마다 내장된 위험도가 `$ConfirmPreference`(기본값 `High`)를 넘으면, `-Confirm`을 명시하지 않아도 확인 프롬프트가 뜬다. 자동화 스크립트에서 사람의 개입 없이 실행돼야 한다면 `-Confirm:$false`를 명시적으로 붙여야 한다.

**직접 만든 함수는 `SupportsShouldProcess`를 선언해야만 두 매개변수를 지원한다**: 단순 함수(`[CmdletBinding()]` 없음)에는 `-WhatIf`/`-Confirm`이 아예 나타나지 않는다. 18장에서 본 것처럼 `Tee-Object` 같은 cmdlet은 자신은 이 매개변수를 지원하지 않아도, 내부적으로 호출하는 `Set-Variable`/`Out-File`에 `-WhatIf` 상태를 전달할 수 있다 — 호출하는 함수 자체가 `SupportsShouldProcess`로 선언되어 있다면 말이다.

**이식성**: CMD·Bash 명령 대부분은 "미리보기" 개념이 없어, `rm`처럼 되돌릴 수 없는 명령을 실행하기 전에는 사람이 직접 대상을 확인하는 수밖에 없다(`rm -i`로 확인을 받는 정도가 최선이다). PowerShell은 이 미리보기·확인 절차를 cmdlet 설계 규약(`SupportsShouldProcess`)으로 표준화했다는 점이 다르다.

## Reference

- [about_CommonParameters - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters)
