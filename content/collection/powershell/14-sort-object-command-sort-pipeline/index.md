---
draft: true
collection_order: 14
slug: sort-object-command-sort-pipeline-powershell
title: "[PowerShell] 14. Sort-Object — 정렬"
date: 2026-08-29
lastmod: 2026-08-29
description: "Sort-Object로 파이프라인 객체를 속성 기준으로 정렬하는 법과 -Descending, 다중 속성 정렬(해시테이블로 속성별 오름차순/내림차순 조합), -Unique로 중복 제거, -Top/-Bottom 최적화를 정리한 챕터다."
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
- Sort-Object
- Sorting
- Stable-Sort
- Calculated-Property
- Get-Process
- Culture
- IComparable
image: "wordcloud.png"
---

## 개요

`Sort-Object`는 객체를 속성 값 기준으로 오름차순 또는 내림차순 정렬하는 cmdlet이다. Bash의 `sort`가 텍스트 줄을 문자·숫자 기준으로 정렬하는 것과 비슷한 역할이지만, `Sort-Object`는 속성의 실제 .NET 타입에 맞는 비교 방식을 쓴다 — 문자열로 변환했다가 다시 비교하지 않으므로, 숫자 속성은 숫자로, 날짜 속성은 날짜로 올바르게 정렬된다.

정렬 기준 속성을 지정하지 않으면 PowerShell은 해당 객체 타입의 기본 정렬 속성(`types.ps1xml`에 정의된 `DefaultKeyPropertySet`)을 쓰고, 그마저 없으면 객체 자체를 비교하려 시도한다(`IComparable`을 구현했으면 그 방식을, 아니면 `ToString()` 결과를 문자열로 비교한다).

## 사용법

```powershell
Sort-Object [[-Property] <Object[]>] [-Descending] [-Unique] [-Top <Int32> | -Bottom <Int32>] [-Stable] [-CaseSensitive]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Property` | 정렬 기준 속성(들). 쉼표로 여러 개를 나열하면 첫 번째 속성이 같을 때만 다음 속성으로 비교한다 |
| `-Descending` | 내림차순 정렬(기본은 오름차순) |
| `-Unique` | 정렬 후 중복 값을 제거한다(대소문자 구분 없이 비교) |
| `-Top <n>` / `-Bottom <n>` | 정렬 결과에서 상위/하위 n개만 반환한다(PowerShell 6+, 안정 정렬을 보장) |
| `-Stable` | 정렬 기준이 같은 객체는 원래 받은 순서를 유지한다(PowerShell 6.2+) |
| `-CaseSensitive` | 문자열 비교를 대소문자 구분으로 바꾼다(기본은 구분 안 함) |
| `-Culture` | 정렬에 사용할 문화권(로캘)을 지정한다 |

다중 속성을 서로 다른 방향으로 정렬하려면 해시테이블을 쓴다: `@{Expression="속성"; Descending=$true}`.

## 예시

```powershell
Get-ChildItem -File | Sort-Object -Property Length                     # 오름차순(기본)
Get-Process | Sort-Object -Property WS | Select-Object -Last 5         # 메모리 사용량 상위 5개
Get-Process | Sort-Object -Property WS -Bottom 5                       # 위와 동등, PowerShell 6+ 안정 정렬
Get-History | Sort-Object -Property Id -Descending                     # 최신 명령이 먼저
Get-Service | Sort-Object -Property @{Expression="Status"; Descending=$true}, @{Expression="DisplayName"; Descending=$false}
Get-ChildItem -Path C:\Test | Sort-Object Length, Name                 # 다중 속성(길이 → 이름)
Get-Content ServerNames.txt | Sort-Object -Unique                      # 대소문자 구분 없이 중복 제거
1..20 | Sort-Object { $_ % 3 } -Stable                                 # 나머지 기준 정렬, 동률은 원순서 유지
```

## 주의사항·함정

**`-Unique`는 대소문자를 구분하지 않는다**: `Sort-Object -Unique`는 "character"와 "CHARACTER"를 같은 값으로 취급해 하나만 남긴다. 대소문자를 구분해 중복을 제거하려면 `-CaseSensitive`를 함께 지정한다.

**안정 정렬이 항상 기본은 아니다**: 정렬 기준 값이 같은 객체들의 상대 순서를 보장하는 "안정 정렬"은 `-Top`/`-Bottom`/`-Stable`을 쓸 때만 보장된다. 이들 없이 일반 정렬을 하면 기준이 같은 객체끼리는 순서가 뒤섞일 수 있다(예: `1..20 | Sort-Object {$_ % 3}` vs `-Stable` 버전의 결과가 다르다).

**문자열로 저장된 숫자는 문자열로 정렬된다**: 텍스트 파일에서 읽은 숫자(`Get-Content`의 결과는 항상 문자열)를 그대로 정렬하면 `"12345"`가 `"2"`보다 앞에 온다. 숫자로 정렬하려면 `Sort-Object {[int]$_}`처럼 캐스팅해야 한다.

**이식성**: Bash `sort -n`(숫자 정렬)·`sort -r`(역순)에 대응하지만, PowerShell은 속성 타입을 유지한 채 비교하므로 CMD·Bash처럼 정렬 전에 열을 텍스트로 추출·재조합할 필요가 없다.

## Reference

- [Sort-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/sort-object)
