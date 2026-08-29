---
draft: true
collection_order: 49
slug: import-export-csv-command-powershell
title: "[PowerShell] 49. Import-Csv/Export-Csv/ConvertTo-Csv"
date: 2026-08-29
lastmod: 2026-08-29
description: "Import-Csv로 CSV 파일을 PSCustomObject 배열로 읽는 법과 Export-Csv의 -NoTypeInformation 기본값 변화, -Append/-Delimiter 매개변수, Format-Table을 CSV 저장 전에 쓰면 안 되는 이유를 정리한 챕터다."
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
- CSV
- Import-Csv
- Export-Csv
- Excel
- Data-Export
- Tabular-Data
image: "wordcloud.png"
---

## 개요

`Import-Csv`/`Export-Csv`는 CSV(쉼표로 구분된 값) 파일과 PowerShell 객체를 오가는 cmdlet 쌍이다. 48장의 JSON이 웹 API·설정 파일에 특화돼 있다면, CSV는 Excel처럼 표 형태 데이터를 다루는 도구·사람과 데이터를 주고받을 때 여전히 널리 쓰인다. `ConvertTo-Csv`/`ConvertFrom-Csv`는 파일 대신 파이프라인 문자열을 다룬다는 점만 다를 뿐 동작은 동일하다.

정신 모델은 "CSV 파일의 첫 줄은 객체의 속성 이름(헤더)이 되고, 그 아래 각 줄은 객체 하나가 된다"는 것이다. `Export-Csv`로 내보낸 객체를 `Import-Csv`로 다시 읽으면 원래 객체의 **문자열 버전**(모든 속성값이 `ToString()`으로 변환됨)을 얻는다 — 메서드는 사라지고 값만 남는다.

## 사용법

```powershell
Export-Csv [-Path] <String> -InputObject <PSObject> [-Delimiter <Char>] [-NoTypeInformation] [-Append]
Import-Csv [-Path] <String[]> [-Delimiter <Char>] [-Header <String[]>]
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Delimiter` | 둘 다 | 구분자(기본 쉼표), 세미콜론 등으로 변경 가능 |
| `-NoTypeInformation` | Export-Csv | PowerShell 6부터 기본 동작이라 사실상 불필요(하위 호환용으로 남음), `#TYPE` 헤더 줄을 뺀다 |
| `-Append` | Export-Csv | 기존 파일 끝에 추가(속성이 다르면 오류, `-Force`와 함께 쓰면 불일치 속성은 버려짐) |
| `-Header` | Import-Csv | 파일의 첫 줄을 헤더로 쓰지 않고 지정한 이름으로 속성명 지정 |
| `-UseCulture` | 둘 다 | 현재 문화권의 목록 구분자(`(Get-Culture).TextInfo.ListSeparator`)를 구분자로 사용 |

## 예시

```powershell
Get-Process | Select-Object Name, Id, CPU | Export-Csv -Path .\proc.csv -NoTypeInformation
$data = Import-Csv -Path .\proc.csv
$data | Get-Member          # 반환 타입은 모두 PSCustomObject(원래 Process 타입이 아님)

Get-Process | Export-Csv -Path .\proc.csv -Delimiter ';'                # 세미콜론 구분
Import-Csv -Path .\proc.csv -Delimiter ';'

$app = Get-Service -DisplayName *Application* | Select-Object DisplayName, Status
$app | Export-Csv -Path .\services.csv -NoTypeInformation
$win = Get-Service -DisplayName *Windows* | Select-Object DisplayName, Status
$win | Export-Csv -Path .\services.csv -NoTypeInformation -Append       # 이어서 추가

$obj = [PSCustomObject]@{ Name = "PowerShell"; Version = "7.0" }
$obj | ConvertTo-Csv -NoTypeInformation                                  # 파일 없이 문자열로만 변환

Import-Csv -Path .\data.csv -Header 'Id', 'Name'                         # 헤더 없는 CSV에 이름 부여
```

## 주의사항·함정

**`Format-Table`을 거친 뒤 `Export-Csv`에 넘기면 완전히 엉뚱한 결과가 나온다**: `Get-Date | Format-Table | Export-Csv`처럼 서식 cmdlet을 파이프라인 중간에 끼워 넣으면, `Export-Csv`는 원래 객체가 아니라 "화면에 표를 그리기 위한 서식 지정 객체"를 CSV로 저장해 버린다. 9장에서 다룬 `Format-*` cmdlet은 항상 파이프라인의 마지막에만 놓아야 한다는 원칙이 여기서도 그대로 적용된다 — CSV로 내보내기 전에는 `Select-Object`(13장)로 속성만 고르는 것이 안전하다.

**`Import-Csv`로 되돌린 객체는 원래 타입이 아니라 전부 문자열이다**: `Export-Csv`한 `Get-Process` 결과를 `Import-Csv`로 다시 읽으면 `Id`, `CPU` 같은 값이 숫자가 아니라 문자열로 반환된다. `.ToString()`으로 값이 저장되고 메서드는 함께 저장되지 않기 때문이다. 정렬·연산이 필요하면 `[int]$obj.Id`처럼 41장에서 배운 타입 캐스팅을 다시 적용해야 한다. 객체를 원래 타입 그대로 완전히 보존해야 한다면 CSV 대신 `Export-Clixml`(19부)을 검토해야 한다.

**`-Append`는 속성 이름이 정확히 일치해야 하고, 그렇지 않으면 오류가 난다**: 기존 CSV 파일의 헤더와 새로 추가하려는 객체의 속성 이름이 다르면 `Export-Csv -Append`가 오류를 낸다. `-Force`를 함께 쓰면 오류 없이 진행되지만 일치하지 않는 속성은 조용히 버려지므로, 데이터가 유실될 수 있다는 점을 감안해야 한다.

**이식성**: CMD와 Bash 모두 CSV를 다루는 전용 cmdlet이 없어 `awk`/`cut`으로 텍스트를 직접 파싱하거나 별도 도구에 의존한다. PowerShell은 CSV를 객체 배열로 자동 파싱해, 파이프라인 전체(`Where-Object`, `Sort-Object` 등)를 그대로 이어 쓸 수 있다는 점이 가장 큰 차이다.

## Reference

- [Import-Csv (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/import-csv)
- [Export-Csv (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/export-csv)
