---
draft: false
collection_order: 9
slug: format-table-list-wide-command-output
title: "[PowerShell] 09. Format-Table/List/Wide — 출력 형식 제어"
date: 2026-08-29
lastmod: 2026-08-29
description: "Format-Table·Format-List·Format-Wide로 PowerShell 객체를 표·목록·단일 열로 출력하는 법과 기본 뷰가 정해지는 원리, 계산된 속성(Label/Expression)으로 열을 새로 만드는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
- Documentation(문서화)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Object-Pipeline
- Format-Table
- Format-List
- Format-Wide
- Calculated-Property
- Output-Formatting
- Get-Member
image: "wordcloud.png"
---

## 개요

`Format-Table`, `Format-List`, `Format-Wide`는 PowerShell 객체를 화면에 어떤 모양으로 보여줄지 결정하는 세 가지 서식 cmdlet이다. `Get-Process`나 `Get-Service`를 실행했을 때 자동으로 표 형태로 나오는 것도 사실은 PowerShell이 내부적으로 `Format-Table`에 해당하는 기본 뷰를 적용한 결과다. CMD·Bash에서는 출력 형식이 명령마다 하드코딩되어 있지만, PowerShell에서는 "어떤 객체든 같은 서식 cmdlet으로 표·목록·와이드 뷰 중 원하는 모양을 고를 수 있다"는 점이 다르다.

정신 모델은 "서식 cmdlet은 데이터를 바꾸지 않고 보여주는 방식만 바꾼다"는 것이다. `Format-*` cmdlet이 반환하는 것은 원래 객체가 아니라 화면 표시 전용 서식 객체이므로, `Format-Table`을 거친 결과를 다시 `Where-Object`나 `Sort-Object`로 처리하면 예상과 다르게 동작한다 — 서식 적용은 언제나 파이프라인의 마지막 단계여야 한다.

## 사용법

```powershell
Get-Process | Format-Table -Property Name, Id, CPU -AutoSize
Get-Service | Format-List -Property *
Get-ChildItem | Format-Wide -Column 3
```

## 매개변수

| 매개변수 | 해당 cmdlet | 설명 |
|---|---|---|
| `-Property` | 셋 다 | 표시할 속성(또는 계산된 속성)을 지정한다. 생략하면 객체 타입의 기본 뷰를 따른다 |
| `-AutoSize` | Table, Wide | 데이터 너비에 맞춰 열 너비·개수를 자동 조정한다 |
| `-Wrap` | Table | 열 너비를 넘는 텍스트를 자르지 않고 다음 줄로 넘긴다 |
| `-GroupBy` | 셋 다 | 정렬된 입력을 지정한 속성 값별로 묶어서 별도 표로 표시한다 |
| `-Column` | Wide | 한 줄에 표시할 열 개수를 직접 지정한다(`-AutoSize`와 동시 사용 불가) |
| `-View` | 셋 다 | `.format.ps1xml`에 정의된 대체 뷰나 사용자 지정 뷰 이름을 지정한다 |
| `-Force` | 셋 다 | 문자열·기본 타입처럼 공개 속성이 없는 객체도 강제로 서식을 적용한다 |

## 예시

```powershell
Get-Host | Format-Table -AutoSize                                   # 열 너비 자동 조정
Get-Process | Sort-Object BasePriority | Format-Table -GroupBy BasePriority -Wrap
Get-Service | Format-Table -Property Name, DependentServices        # 원하는 속성만 표로
Get-Process notepad | Format-Table ProcessName, @{ Label = "가동시간"; Expression = { (Get-Date) - $_.StartTime } }
Get-ChildItem HKCU:\Software\Microsoft | Format-Wide -Property PSChildName -AutoSize
Get-Process winlogon | Format-List -Property *                      # 모든 속성을 목록으로
Get-Date | Format-Table DayOfWeek, { $_ / $null } -DisplayError     # 표현식 오류 디버깅
```

계산된 속성은 해시테이블로 `Label`(또는 `Name`)과 `Expression`을 지정해 원하는 이름의 새 열을 즉석에서 만든다 — 원본 객체에 없는 값(예: 경과 시간)도 이 방식으로 표시할 수 있다.

## 주의사항·함정

**세 cmdlet 중 무엇을 쓸지는 속성 개수와 화면 폭으로 판단한다**: 속성이 4개 이하로 적고 한 줄에 다 들어갈 때는 `Format-Table`, 속성이 많아 표로는 잘리는 객체는 `Format-List`, 이름 하나만 여러 열로 나열하고 싶을 때는 `Format-Wide`가 적합하다. 셋 다 맞지 않는 복잡한 레이아웃이 필요하면 `Format-Custom`을 검토한다.

**`-Property`와 `-View`는 동시에 쓸 수 없다**: 원하는 속성을 직접 지정하는 방식과, 미리 정의된 뷰 이름을 지정하는 방식은 서로 배타적이다.

**기본 타입에 `-Property`를 쓰려면 `-Force`가 필요할 수 있다**: `[string]`처럼 `ToString()`으로 자체 출력되는 기본 타입이나, 공개 속성이 없는 객체에 `-Property`를 지정하면 `-Force`를 함께 써야 한다.

**이식성**: CMD·Bash에는 이런 범용 서식 계층이 없다 — 각 명령이 자체적으로 텍스트 출력 형식을 결정하고, 형식을 바꾸려면 `awk`·`cut`처럼 텍스트를 다시 파싱해야 한다. PowerShell은 데이터(객체)와 표현(서식)을 분리해 두었기 때문에, 어떤 cmdlet의 결과든 같은 세 가지 서식 cmdlet으로 원하는 모양을 고를 수 있다.

## Reference

- [Format-Table (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/format-table)
- [Format-List (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/format-list)
- [Format-Wide (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/format-wide)
