---
draft: true
collection_order: 68
slug: write-verbose-debug-warning-powershell
title: "[PowerShell] 68. Write-Verbose/Debug/Warning/Information"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell Write-Verbose/Write-Debug/Write-Warning/Write-Information이 각각 다른 출력 스트림에 쓰는 원리와 -Verbose/-Debug 공통 매개변수로 표시 여부를 켜는 법, 29장 Write-Host와의 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Error-Handling
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
- Write-Verbose
- Write-Debug
- Write-Warning
- Output-Streams
- Preference-Variable
- Diagnostic-Message
image: "wordcloud.png"
---

## 개요

`Write-Verbose`, `Write-Debug`, `Write-Warning`, `Write-Information`은 각각 서로 다른 **출력 스트림**에 메시지를 보내는 진단용 cmdlet이다. 29장에서 `Write-Host`와 `Write-Output`의 차이를 다루며 스트림 개념을 처음 소개했는데, 이 장은 그 스트림 모델을 진단 목적의 나머지 네 스트림으로 확장한다. 58장에서 다룬 `[CmdletBinding()]`이 함수에 `-Verbose`/`-Debug` 매개변수를 자동으로 추가해 주는 이유가 바로 이 cmdlet들과 짝을 이루기 위해서다.

정신 모델은 "각 스트림은 서로 다른 청중을 위한 것"이라는 것이다 — Verbose는 "지금 무슨 일이 일어나고 있는지" 더 자세히 알고 싶은 사용자, Debug는 스크립트를 작성한 개발자, Warning은 치명적이지 않지만 주의가 필요한 상황, Information은 구조화된 로그 기록용이다.

## 사용법

```powershell
Write-Verbose -Message "메시지"
Write-Debug -Message "메시지"
Write-Warning -Message "메시지"
Write-Information -MessageData "메시지" [-Tags <String[]>]
```

## 종류

| cmdlet | 스트림 번호 | 기본 표시 여부 | 켜는 방법 |
|---|---|---|---|
| `Write-Verbose` | 4 | 숨김 | `-Verbose` 공통 매개변수 또는 `$VerbosePreference = "Continue"` |
| `Write-Debug` | 5 | 숨김 | `-Debug` 공통 매개변수 또는 `$DebugPreference = "Continue"`(기본적으로 확인 프롬프트도 뜸) |
| `Write-Warning` | 3 | 표시됨(노란 글씨) | `-WarningAction SilentlyContinue`로 숨길 수 있음(66장) |
| `Write-Information` | 6 | 숨김(PowerShell 5+) | `-InformationAction Continue` 또는 `$InformationPreference` |

## 예시

```powershell
function Search-Log {
    [CmdletBinding()]
    param($Path)
    Write-Verbose "$Path 에서 로그를 검색하는 중입니다."   # -Verbose 없이는 표시 안 됨
    Write-Debug "내부 변수 상태: Path=$Path"                # -Debug 없이는 표시 안 됨(확인 프롬프트 뜸)
    if (-not (Test-Path $Path)) {
        Write-Warning "$Path 경로가 존재하지 않습니다."       # 기본적으로 항상 표시됨
    }
    Get-Content $Path
}
Search-Log -Path .\app.log -Verbose            # Verbose 메시지까지 표시
Search-Log -Path .\app.log -Debug               # Debug 메시지 표시 + 계속할지 확인 프롬프트

$VerbosePreference = "Continue"                  # 세션 전체에서 Verbose 메시지 항상 표시
Search-Log -Path .\app.log                        # -Verbose 없이도 표시됨
$VerbosePreference = "SilentlyContinue"            # 원래대로 복원

Write-Information "배포 시작" -Tags "Deployment"     # 태그로 분류된 정보 메시지
$InformationPreference = "Continue"
Write-Information "이제는 화면에 보임"
```

## 주의사항·함정

**`Write-Host`(29장)와 이 네 cmdlet은 근본적으로 다른 목적을 가진다**: `Write-Host`는 사용자에게 항상 보여줄 콘솔 전용 출력이고 리다이렉션이나 캡처가 안 되지만, 이 장의 네 cmdlet은 각자의 스트림 번호를 가져 `*>&1`처럼 다른 스트림으로 리다이렉션하거나 파일로 캡처할 수 있다. "디버깅 정보를 로그 파일에도 남기고 싶다"면 `Write-Host`가 아니라 `Write-Verbose`/`Write-Debug`를 쓰고 스트림을 리다이렉션해야 한다.

**`Write-Debug`는 기본적으로 확인 프롬프트를 띄운다**: `-Debug`를 붙이면 메시지가 나올 때마다 "계속하시겠습니까?" 같은 프롬프트가 뜬다 — 자동화 스크립트에서 예상치 못하게 이 프롬프트에 걸려 멈추는 경우가 있다. 프롬프트 없이 메시지만 보고 싶다면 `-Debug:$false`가 아니라 `$DebugPreference = "Continue"`로 설정해야 확인 없이 흘러간다.

**공통 매개변수로 켠 스트림 표시는 그 명령 호출에만 적용되고, 그 명령이 내부에서 호출하는 다른 함수에는 자동으로 전파되지 않는다**: `Search-Log -Verbose`를 호출해도, `Search-Log` 내부에서 호출하는 다른 사용자 정의 함수의 `Write-Verbose`까지 자동으로 표시되지는 않는다 — 그 함수도 `[CmdletBinding()]`을 갖추고 있어야 하며, `-Verbose`를 전달하려면 60장에서 배운 스플래팅이나 `$PSBoundParameters`를 활용해야 한다.

**이식성**: Bash·CMD는 표준 출력(stdout)과 표준 오류(stderr) 두 스트림만 기본 제공해, "상세 로그"·"경고"·"디버그"를 구분하려면 관례적으로 접두사를 붙이거나 별도 로깅 함수를 직접 구현해야 한다. PowerShell이 애초에 6개(성공·오류·경고·상세·디버그·정보)의 이름 붙은 스트림을 표준으로 제공하는 것은, 29장에서 강조한 "출력의 의도를 명확히 구분한다"는 설계 철학의 연장이다.

## Reference

- [Write-Verbose (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-verbose)
