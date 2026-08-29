---
draft: true
collection_order: 24
slug: automatic-variables-powershell-underscore-null
title: "[PowerShell] 24. 자동 변수 총정리 — $_, $null, $Error, $LASTEXITCODE"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell이 자동으로 만들고 관리하는 자동 변수 $_/$PSItem, $null, $true/$false, $Error, $?, $LASTEXITCODE, $PSVersionTable의 역할과 스크립트 진단에 자주 쓰이는 이유를 정리한 챕터다."
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
- Automatic-Variables
- Error-Handling
- Exit-Code
- Debugging
- Environment
- Try-Catch
- Native-Command
image: "wordcloud.png"
---

## 개요

<strong>자동 변수(automatic variable)</strong>는 PowerShell이 세션 시작 시 스스로 만들고 계속 값을 갱신하는 변수다. 06장의 `$PROFILE`, 03장에서 언급한 `$PSVersionTable`도 자동 변수의 일종이다. 이 장은 그중 가장 자주 쓰이는 변수들을 스크립팅·디버깅 관점에서 묶어 정리한다.

정신 모델은 "자동 변수는 대부분 읽기 전용으로 취급해야 하는 상태 스냅샷"이라는 것이다. 값을 직접 대입할 수 있는 것들도 있지만(예: `$ErrorActionPreference`는 별개의 환경설정 변수), 이 장에서 다루는 변수 대부분은 PowerShell 엔진이 갱신하는 값을 읽기만 하는 용도로 쓰인다. 표기상 대입이 가능하다고 해서 그렇게 해도 안전하다는 뜻은 아니다 — Microsoft 공식 문서도 하위 호환을 위해 쓰기가 허용될 뿐, 자동 변수는 개념적으로 읽기 전용으로 다뤄야 한다고 명시한다.

## 자주 쓰는 자동 변수

| 변수 | 내용 |
|---|---|
| `$_` (= `$PSItem`) | 파이프라인의 현재 객체(`Where-Object`, `ForEach-Object` 등의 스크립트블록 안에서) |
| `$null` | 값이 없음을 나타내는 객체. 비교 시 항상 왼쪽에 두어야 컬렉션 필터링 부작용을 피한다(20장 참고) |
| `$true` / `$false` | 불리언 리터럴 |
| `$Error` | 세션에서 발생한 오류 객체의 배열. `$Error[0]`이 가장 최근 오류 |
| `$?` | 마지막 명령의 성공 여부(Boolean). 네이티브 명령은 `$LASTEXITCODE`가 0일 때만 `$true` |
| `$LASTEXITCODE` | 마지막으로 실행된 네이티브 프로그램 또는 PowerShell 스크립트의 종료 코드 |
| `$Matches` | `-match`/`-notmatch` 연산자가 스칼라 입력에서 매칭됐을 때 캡처 그룹을 담는 해시테이블 |
| `$PSVersionTable` | 현재 세션의 PowerShell 버전·에디션·플랫폼 정보(01장 참고) |
| `$PSScriptRoot` | 실행 중인 스크립트가 위치한 디렉터리의 전체 경로 |
| `$args` | 함수·스크립트에 전달된, `param`으로 선언되지 않은 매개변수 값 배열 |
| `$IsWindows` / `$IsLinux` / `$IsMacOS` | 현재 세션이 실행 중인 운영체제(PowerShell 6+) |

## 예시

```powershell
Get-Process | Where-Object { $_.CPU -gt 100 }         # $_ 로 현재 객체 참조
1,2,3 -eq 2 | ForEach-Object { "matched: $_" }

Get-Process -Id 999999 -ErrorAction SilentlyContinue  # 오류를 조용히 $Error에 기록
$Error[0].Exception.Message                            # 가장 최근 오류 메시지 확인

if (-not $?) { "이전 명령이 실패했다" }

ping.exe 127.0.0.1 | Out-Null
if ($LASTEXITCODE -ne 0) { "ping 실패, 코드: $LASTEXITCODE" }

"was CONTOSO\jsmith" -match 'was (?<domain>.+)\\(?<user>.+)'
$Matches.domain     # CONTOSO
$Matches.user       # jsmith

$PSVersionTable.PSEdition   # Desktop 또는 Core
```

## 주의사항·함정

**`$?`는 예상보다 미묘하게 동작한다**: 함수 안에서 `Write-Error`를 호출해도, 그 함수를 호출한 바깥에서 확인하는 `$?`는 다시 `True`로 리셋될 수 있다(함수가 정상적으로 반환됐기 때문). 함수 내부의 실패 여부를 정확히 전달하려면 `$PSCmdlet.WriteError()`를 쓰거나 명시적으로 상태를 반환해야 한다.

**`$LASTEXITCODE`는 네이티브 명령에만 의미가 있다**: 순수 PowerShell cmdlet은 종료 코드를 반환하지 않으므로, cmdlet만 실행한 직후 `$LASTEXITCODE`를 확인하면 그 이전에 실행된 네이티브 명령의 값이 그대로 남아 있을 수 있다. cmdlet 성공 여부는 `$?`나 `try`/`catch`로 확인해야 한다.

**`$Matches`는 매칭 실패 시 이전 값을 그대로 유지한다**: `-match`가 거짓을 반환한 경우 `$Matches`는 초기화되지 않고 이전 매칭 결과를 그대로 들고 있다. `-match` 호출 직후 `if` 조건 안에서만 `$Matches`를 참조하는 습관을 들이면 이 문제를 피할 수 있다.

**자동 변수 이름으로 새 변수를 만들면 안 된다**: `$Matches`, `$Error`, `$_` 같은 이름으로 직접 변수를 만들면 PowerShell 엔진이 관리하는 값과 충돌해 예측하기 어려운 동작을 일으킨다.

**이식성**: Bash의 `$?`(마지막 종료 코드), `$_`(마지막 인자 또는 파이프라인 컨텍스트에 따라 다름)와 이름은 비슷하지만 의미가 다르다 — PowerShell의 `$?`는 Boolean이고 `$_`는 파이프라인 객체 자체를 가리킨다. CMD의 `%ERRORLEVEL%`이 PowerShell의 `$LASTEXITCODE`와 가장 가깝게 대응한다.

## Reference

- [about_Automatic_Variables - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables)
