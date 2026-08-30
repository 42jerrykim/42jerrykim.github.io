---
draft: false
collection_order: 19
slug: compare-object-command-diff-powershell
title: "[PowerShell] 19. Compare-Object — 객체 비교(diff)"
date: 2026-08-29
lastmod: 2026-08-29
description: "Compare-Object(별칭 diff)로 두 컬렉션의 차이를 비교하는 법, SideIndicator(<=, =>, ==)의 의미, -Property로 특정 속성만 비교하는 법, -IncludeEqual/-PassThru 매개변수를 정리한 Part 2 마지막 챕터다."
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
- Compare-Object
- Diff
- SideIndicator
- IComparable
- Version-Control
- Configuration-Drift
- Deployment(배포)
image: "wordcloud.png"
---

## 개요

`Compare-Object`(별칭 `diff`, `compare`)는 두 컬렉션을 비교해 어느 쪽에만 있는 값, 또는 양쪽에 공통으로 있는 값을 찾아주는 cmdlet이다. Bash의 `diff` 명령이 텍스트 파일 두 개를 줄 단위로 비교하는 것과 이름·목적이 같지만, `Compare-Object`는 파일뿐 아니라 배열·프로세스 목록 등 임의의 객체 컬렉션 두 개를 비교할 수 있다.

정신 모델은 "기준(Reference)과 대상(Difference), 두 집합 사이의 여집합과 교집합을 찾는다"는 것이다. 결과 객체의 `SideIndicator` 속성이 그 값이 어느 쪽에서만 발견됐는지 알려준다 — `<=`는 기준 쪽에만, `=>`는 대상 쪽에만, `-IncludeEqual`을 쓰면 `==`로 양쪽 모두에 있음을 표시한다.

## 사용법

```powershell
Compare-Object [-ReferenceObject] <PSObject[]> [-DifferenceObject] <PSObject[]> [-Property <Object[]>] [-IncludeEqual] [-ExcludeDifferent] [-PassThru] [-CaseSensitive]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-ReferenceObject` | 비교 기준이 되는 컬렉션 |
| `-DifferenceObject` | 기준과 비교할 대상 컬렉션(파이프로도 전달 가능) |
| `-Property` | 객체 전체가 아니라 지정한 속성 값만 비교한다 |
| `-IncludeEqual` | 양쪽에 모두 있는 값도 결과에 포함한다(`SideIndicator: ==`) |
| `-ExcludeDifferent` | 차이는 빼고 공통값만 보여준다(PowerShell 7.1+부터 `-IncludeEqual`이 자동으로 함께 적용된 것처럼 동작) |
| `-PassThru` | 결과를 `SideIndicator`가 붙은 `PSCustomObject` 래퍼로 감싸지 않고, 원본 타입 그대로에 `SideIndicator`만 추가해 반환한다 |
| `-SyncWindow` | 순서가 어긋난 컬렉션에서 같은 값을 찾기 위해 앞뒤로 살펴볼 범위(기본은 전체) |

## 예시

```powershell
Compare-Object (Get-Content File1.txt) (Get-Content File2.txt)          # 두 텍스트 파일 비교
Compare-Object (Get-Content File1.txt) (Get-Content File2.txt) -ExcludeDifferent -IncludeEqual   # 공통 줄만
Compare-Object -ReferenceObject 'abc' -DifferenceObject 'xyz' -Property Length -IncludeEqual   # 길이만 비교
Compare-Object $a $b -Property ProcessName, Id, CPU                     # 특정 속성 기준 비교
Compare-Object ([timespan]"0:0:1") "0:0:1" -IncludeEqual                 # 타입이 다르면 기준 타입으로 변환 후 비교
$before = Get-Service
# ... 어떤 작업 수행 ...
$after = Get-Service
Compare-Object $before $after -Property Name, Status                    # 작업 전후 상태 변화 확인
```

## 주의사항·함정

**속성을 지정하지 않으면 `ToString()` 결과로 비교한다**: `Compare-Object`는 비교 가능한 방법을 먼저 찾고(예: `IComparable` 구현), 마땅한 방법이 없으면 객체를 문자열로 바꿔 비교한다. `System.Diagnostics.Process`처럼 `IComparable`을 구현하지 않는 복잡한 객체를 속성 지정 없이 비교하면, `ToString()` 값(예: `System.Diagnostics.Process (pwsh)`)이 같으면 실제 내용이 달라도 "같다"고 판단될 수 있다 — 의미 있는 비교를 하려면 `-Property`로 실제 비교하려는 속성을 명시해야 한다.

**`$null`을 넘기면 종료 오류가 난다**: `-ReferenceObject`나 `-DifferenceObject`에 `$null`을 그대로 넘기면 `Compare-Object`는 계속 진행하지 않고 종료 오류(terminating error)를 던진다. 컬렉션이 비어 있을 수 있는 경우 `@()`(빈 배열)로 넘기는 것이 안전하다.

**결과가 없으면 아무 출력도 없다**: 두 컬렉션이 완전히 같으면(그리고 `-IncludeEqual`을 쓰지 않으면) `Compare-Object`는 아무것도 반환하지 않는다. "차이가 없다"를 프로그램적으로 확인하려면 결과를 변수에 담아 `$null` 여부나 개수를 확인해야 한다.

**이식성**: Bash의 `diff`는 줄 단위 텍스트 비교와 컨텍스트 표시(`+`/`-`)에 특화되어 있지만, `Compare-Object`는 객체 속성 단위 비교(`-Property`)까지 지원해 "배포 전후 서비스 목록이 같은가" 같은 구조화된 비교에도 그대로 쓸 수 있다.

## Reference

- [Compare-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/compare-object)
