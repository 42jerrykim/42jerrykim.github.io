---
draft: true
collection_order: 46
slug: select-string-command-powershell
title: "[PowerShell] 46. Select-String — 텍스트에서 패턴 찾기"
date: 2026-08-29
lastmod: 2026-08-29
description: "Select-String으로 파일이나 문자열에서 패턴을 찾는 법과 -Pattern/-SimpleMatch 차이, -Context로 앞뒤 줄을 함께 보는 법, -NotMatch/-AllMatches/-Quiet 매개변수를 grep과 비교하며 정리한 챕터다."
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
- Select-String
- Grep
- Regex
- Pattern-Matching
- Log-Analysis
- Text-Search
image: "wordcloud.png"
---

## 개요

`Select-String`은 파일이나 문자열, 파이프라인 입력에서 텍스트 패턴을 찾는 cmdlet으로, Bash의 `grep`에 가장 가깝다. 37장의 `Get-Content`로 파일을 통째로 줄 배열로 읽어 `Where-Object`(12장)로 걸러낼 수도 있지만, `Select-String`은 대용량 파일을 한 줄씩 스트리밍 처리하고 일치한 줄 번호·앞뒤 맥락까지 함께 알려준다는 점에서 로그·텍스트 검색에 특화돼 있다.

정신 모델은 "파일이나 텍스트 스트림을 한 줄씩 훑으며, 패턴과 일치하는 줄을 그 줄 번호·파일명과 함께 객체로 반환하는 도구"라는 것이다. 반환되는 `MatchInfo` 객체는 단순 문자열이 아니라 `.Line`, `.LineNumber`, `.Path`, `.Matches` 같은 속성을 가진 구조화된 결과다.

## 사용법

```powershell
Select-String [-Pattern] <String[]> [-Path] <String[]> [-SimpleMatch] [-CaseSensitive] [-Context <Int32[]>] [-NotMatch] [-AllMatches] [-Quiet]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Pattern` | 찾을 정규식(기본) 또는 `-SimpleMatch`와 함께면 리터럴 문자열 |
| `-Path` / `-LiteralPath` | 검색 대상 파일(와일드카드 지원) |
| `-SimpleMatch` | 정규식이 아니라 단순 리터럴 문자열로 검색(47장에서 다룰 정규식 특수문자를 신경 쓰지 않아도 됨) |
| `-CaseSensitive` | 대소문자 구분(기본은 구분 안 함) |
| `-Context <이전,이후>` | 일치한 줄의 앞뒤로 몇 줄을 더 보여줄지 |
| `-NotMatch` | 패턴과 **일치하지 않는** 줄만 반환(반대 필터) |
| `-AllMatches` | 한 줄에 여러 번 일치해도 전부 찾기(기본은 줄마다 첫 일치만) |
| `-Quiet` | 일치 여부만 `$true`/`$false`로 반환(내용은 필요 없을 때) |
| `-List` | 파일마다 첫 일치만 반환(파일 존재 여부 확인용) |

## 예시

```powershell
Select-String -Path "C:\Logs\*.log" -Pattern "Error"                  # 여러 파일에서 검색
Select-String -Path .\access.log -Pattern "500" -SimpleMatch          # 리터럴 문자열로 검색

Get-Content .\app.log | Select-String -Pattern "timeout"               # 파이프라인 입력
Select-String -Path .\app.log -Pattern "timeout" -Context 2,3          # 앞 2줄, 뒤 3줄 함께

Select-String -Path .\app.log -Pattern "warning" -NotMatch             # warning이 없는 줄만
Select-String -Path .\app.log -Pattern "\d+" -AllMatches               # 한 줄의 모든 숫자 찾기

if (Select-String -Path .\config.ini -Pattern "DebugMode" -Quiet) {
    "설정 파일에 DebugMode 항목이 있습니다"
}

$results = Select-String -Path .\app.log -Pattern "ERROR"
$results | ForEach-Object { "$($_.Path):$($_.LineNumber) - $($_.Line)" }   # 구조화된 결과 활용

Get-ChildItem -Recurse -Filter *.ps1 | Select-String -Pattern "Write-Host"  # 31장 재귀 탐색과 조합
```

## 주의사항·함정

**`-Pattern`은 기본이 정규식이라, 특수문자를 리터럴로 찾고 싶으면 `-SimpleMatch`가 필요하다**: `Select-String -Pattern "3.14"`는 마침표가 정규식에서 "임의의 한 문자"를 뜻하므로 "3.14"뿐 아니라 "3x14" 같은 문자열도 찾아낸다. 버전 번호나 IP 주소처럼 마침표가 실제로 등장하는 텍스트를 정확히 찾으려면 `-SimpleMatch`를 붙이거나, 47장에서 다룰 `[regex]::Escape()`로 패턴을 이스케이프해야 한다.

**대소문자를 구분하지 않는 것이 기본값이다**: `grep`은 기본적으로 대소문자를 구분하지만, `Select-String`은 그 반대다. 대소문자가 다른 값을 우연히 함께 찾아내는 상황을 피하려면 `-CaseSensitive`를 명시해야 한다.

**`-Quiet`와 `-List`를 혼동하기 쉽다**: `-Quiet`는 불리언 하나만 반환하고, `-List`는 (여러 파일 검색 시) 파일마다 첫 일치 결과 객체를 하나씩 반환한다. "패턴이 있는지 없는지만 알면 된다"면 `-Quiet`, "패턴이 있는 파일 목록이 필요하다"면 `-List`를 골라야 원하는 형태의 결과를 얻는다.

**이식성**: Bash의 `grep`(특히 `grep -n -C`)과 옵션 이름은 다르지만 개념적으로 거의 1:1 대응한다 — `-Pattern`→검색어, `-Path`→대상 파일, `-Context`→`-C`, `-NotMatch`→`-v`, `-CaseSensitive`(반대)→`-i`. CMD의 `findstr`도 유사한 역할을 하지만 정규식 지원 범위가 제한적이고 반환값이 구조화된 객체가 아니라 텍스트 줄이라는 점이 다르다. PowerShell은 `Select-String`이 반환한 `MatchInfo` 객체를 그대로 파이프라인 뒤에 이어 처리할 수 있다는 점이 가장 큰 차이다.

## Reference

- [Select-String (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-string)
