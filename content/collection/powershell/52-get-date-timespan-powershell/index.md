---
draft: false
collection_order: 52
slug: get-date-timespan-powershell
title: "[PowerShell] 52. Get-Date와 TimeSpan"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Date로 현재 시각을 DateTime 객체로 받는 법과 -Format/-UFormat 서식 지정자 차이, -AsUTC로 시간대를 변환하는 법, 두 날짜를 뺄셈해 TimeSpan을 얻는 법을 정리한 Part 5 마지막 챕터다."
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
- Get-Date
- DateTime
- TimeSpan
- UTC
- Timestamp
- Time-Zone
image: "wordcloud.png"
---

## 개요

`Get-Date`는 현재 날짜·시각을 `DateTime` 객체로 반환하는 cmdlet으로, 40장에서 이 Part의 예제 파일들에 등장했던 타임스탬프도 결국 이 타입이다. 이 장은 41장부터 이어 온 "PowerShell 값은 문자열이 아니라 진짜 .NET 타입"이라는 원칙을 날짜·시간에 적용해 확인하며 Part 5(데이터 구조와 텍스트 처리)를 마무리한다.

정신 모델은 "`Get-Date`가 반환하는 것은 화면에 찍힌 텍스트가 아니라, 연산이 가능한 `DateTime` 객체"라는 것이다. 두 `DateTime`을 빼면 자동으로 **`TimeSpan`**(기간을 나타내는 타입)이 나오고, 그 안에 `.Days`, `.Hours`, `.TotalMinutes` 같은 속성이 이미 계산되어 들어 있다 — 문자열을 파싱해 날짜를 계산하는 CMD·Bash 스크립트와 근본적으로 다른 지점이다.

## 사용법

```powershell
Get-Date [-Format <String>] [-UFormat <String>] [-AsUTC]
$date1 - $date2                 # 두 DateTime의 차이 → TimeSpan
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Format` | .NET 사용자 지정 날짜·시간 서식 문자열(`yyyy-MM-dd` 등), 또는 `FileDate`/`FileDateTime` 같은 파일명 친화적 사전 정의 값 |
| `-UFormat` | Unix `date` 스타일 서식 지정자(`%Y`, `%m`, `%d` 등) |
| `-AsUTC` | 값을 UTC(협정 세계시)로 변환해 반환 |
| `-Date` | 특정 날짜·시각을 문자열로 지정해 파싱 |
| `-UnixTimeSeconds` | Unix epoch(1970-01-01) 기준 초 단위 타임스탬프를 `DateTime`으로 변환 |

## 예시

```powershell
Get-Date                                          # 현재 날짜·시각(로캘 기본 서식)
Get-Date -Format "yyyy-MM-dd"                      # 이 저장소의 날짜 규칙과 같은 형식
Get-Date -Format "dddd MM/dd/yyyy HH:mm K"          # 요일·시간대 오프셋 포함
Get-Date -UFormat "%A %m/%d/%Y %R %Z"               # Unix 스타일 서식

$dst = Get-Date
$dst.IsDaylightSavingTime()                          # 일광 절약 시간 여부(메서드 직접 호출)

(Get-Date -Date "2020-01-01T00:00:00" -AsUTC)         # 로컬 시각을 UTC로 변환
Get-Date -UnixTimeSeconds 1577836800                   # Unix 타임스탬프 → DateTime

$start = Get-Date
Start-Sleep -Seconds 2
$elapsed = (Get-Date) - $start                          # 뺄셈 결과는 TimeSpan
$elapsed.TotalSeconds                                     # 초 단위로 확인

$timestamp = Get-Date -Format o | ForEach-Object { $_ -replace ":", "." }
New-Item -Path "C:\Test\$timestamp" -ItemType Directory    # 타임스탬프를 폴더명에 활용(33장)

New-TimeSpan -Start (Get-Date "2026-01-01") -End (Get-Date)  # 특정 기간을 직접 생성
```

## 주의사항·함정

**`-Format`을 쓰면 반환 타입이 `DateTime`이 아니라 `String`으로 바뀐다**: `Get-Date -Format "yyyy-MM-dd"`의 결과는 더 이상 `.AddDays()` 같은 `DateTime` 메서드를 쓸 수 있는 객체가 아니라 단순 문자열이다. 서식을 지정한 값과 계산에 쓸 값이 모두 필요하다면, 먼저 `$d = Get-Date`로 원본 `DateTime`을 변수에 담아 두고 `$d.ToString("yyyy-MM-dd")`나 `"{0:yyyy-MM-dd}" -f $d`처럼 서식은 별도로 적용하는 편이 안전하다.

**시간대(time zone) 정보를 놓치면 서버마다 계산 결과가 달라진다**: `Get-Date`는 기본적으로 로컬 시스템의 시간대를 기준으로 값을 반환한다. 여러 시간대에 걸친 서버에서 실행되는 자동화 스크립트가 시각을 비교·기록해야 한다면, `-AsUTC`로 명시적으로 UTC로 통일하지 않는 한 "같은 순간"이 서버마다 다른 값으로 기록될 수 있다.

**`Export-Csv`(49장)로 `DateTime` 객체를 내보내면 문화권(locale) 기본 서식의 문자열로 바뀐다**: CSV로 저장한 뒤 `Import-Csv`로 다시 읽으면 그 값은 더 이상 `DateTime`이 아니라 문자열이므로, 다시 날짜 연산을 하려면 `[datetime]::Parse()`나 `Get-Date -Date`로 재변환해야 한다. 이 함정은 41장에서 다룬 "값이 저장 매체를 거치면 원래 타입 정보를 잃을 수 있다"는 원칙의 구체적인 사례다.

**이식성**: Bash의 `date` 명령과 `-UFormat`의 `%Y`, `%m`, `%d` 같은 지정자는 상당 부분 겹치도록 설계돼 있어 스크립트를 옮기기 수월하다. CMD의 `%date%`/`%time%` 환경 변수는 로캘에 따라 형식이 들쭉날쭉한 순수 문자열이라 파싱 자체가 번거롭다. PowerShell은 두 날짜의 차이를 구조화된 `TimeSpan` 객체로 즉시 얻을 수 있어, 문자열을 초 단위로 직접 변환해 빼는 셸 스크립트의 반복 작업이 필요 없다.

## Reference

- [Get-Date (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-date)
