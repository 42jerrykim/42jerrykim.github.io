---
draft: true
collection_order: 53
slug: script-execution-ps1-powershell
title: "[PowerShell] 53. 스크립트 작성과 실행(.ps1)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell .ps1 스크립트 파일을 실행하는 법과 실행 정책의 관계, param() 블록으로 스크립트 인자를 받는 법, 점 소싱(dot sourcing)으로 스크립트의 함수·변수를 현재 세션에 가져오는 법을 정리한 Part 6 시작 챕터다."
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
- Ps1-Script
- Dot-Sourcing
- Execution-Policy
- Script-Scope
- Exit-Code
- Batch-Script
image: "wordcloud.png"
---

## 개요

`.ps1` 파일은 PowerShell 명령을 모아 둔 일반 텍스트 스크립트다. 05장에서 다룬 실행 정책(`Set-ExecutionPolicy`)이 바로 이 `.ps1` 파일을 실행해도 되는지를 결정하는 안전장치였는데, 이 장은 그 정책 아래에서 실제로 스크립트를 작성·실행·재사용하는 법을 다루며 Part 6(스크립팅과 흐름 제어)을 시작한다.

정신 모델은 "스크립트는 자신만의 스코프(범위)를 가진 채 실행되는 독립된 명령 목록"이라는 것이다. 스크립트 안에서 만든 변수·함수는 기본적으로 스크립트가 끝나면 함께 사라진다 — 이 원칙이 뒤에서 다룰 점 소싱(dot sourcing)과 62장의 스코프 규칙을 이해하는 출발점이다.

## 사용법

```powershell
.\script.ps1              # 현재 디렉터리의 스크립트 실행(상대 경로, .\ 접두사 필수)
C:\Scripts\script.ps1     # 절대 경로로 실행
.\script.ps1 -Param 값     # 매개변수와 함께 실행
. .\script.ps1             # 점 소싱 — 현재 스코프에서 실행
```

## 종류

| 요소 | 설명 |
|---|---|
| `param()` 블록 | 스크립트 맨 앞(주석·`#Requires` 제외)에 위치, 함수 매개변수와 동일한 문법 사용 |
| 점 소싱(`. 경로`) | 스크립트를 새 스코프가 아니라 현재 스코프에서 실행 — 만든 함수·변수가 세션에 남음 |
| 호출 연산자(`&`) | 문자열로 된 경로를 실행할 때 사용, 스크립트 스코프에서 실행됨(점 소싱과 다름) |
| `exit` 문 | 스크립트 종료 코드 지정, `$LASTEXITCODE`에 반영(CMD의 `%ERRORLEVEL%`에 대응) |
| `$PSScriptRoot` | 현재 실행 중인 스크립트가 위치한 디렉터리 경로(자동 변수) |
| `$MyInvocation` | 스크립트가 어떻게 호출됐는지에 대한 정보(경로, 호출 인자 등) |

## 예시

```powershell
# ServiceLog.ps1
param ($ComputerName = $(throw "ComputerName 매개변수가 필요합니다."))

Get-Service -ComputerName $ComputerName | Out-File "$($ComputerName).log"
```

```powershell
.\ServiceLog.ps1 -ComputerName Server01     # 매개변수와 함께 실행
& "C:\Scripts\ServiceLog.ps1" Server01       # 호출 연산자로 실행(경로가 변수·문자열일 때)

# 점 소싱: UtilityFunctions.ps1이 만든 함수를 현재 세션에서 계속 쓰고 싶을 때
. C:\Scripts\UtilityFunctions.ps1
New-Profile                                    # 점 소싱했기 때문에 세션에서 바로 호출 가능

Get-Help C:\admin\scripts\ServiceLog.ps1        # 스크립트도 Get-Help 대상이 된다(02장)

exit 1                                          # 0이 아닌 종료 코드 — 실패를 알림
$LASTEXITCODE                                    # exit로 지정한 값 확인
```

## 주의사항·함정

**현재 디렉터리의 스크립트는 이름만으로 실행되지 않는다**: 보안상 PowerShell은 `script.ps1`처럼 경로 없이 스크립트 이름만 입력하면 실행하지 않는다. 반드시 `.\script.ps1`처럼 현재 디렉터리를 명시하는 `.\` 접두사가 필요하다 — CMD·Bash에 익숙하다면 이 강제 사항이 낯설게 느껴지기 쉽다.

**점 소싱 없이 실행한 스크립트의 함수·변수는 스크립트가 끝나면 사라진다**: `.\UtilityFunctions.ps1`로 그냥 실행하면 그 안에서 정의한 함수는 스크립트 스코프에만 존재하다가 실행이 끝나는 즉시 소멸한다. 스크립트가 만든 함수·변수를 이후 명령에서 계속 쓰려면 앞에 점과 공백(`. `)을 붙여 점 소싱해야 한다 — 이 차이를 모르면 "방금 만든 함수인데 왜 없다고 나오지?"라는 혼란에 빠지기 쉽다.

**`exit` 없이 끝난 스크립트는 종료 코드를 남기지 않는다**: CI/CD 파이프라인이나 배치 작업에서 스크립트 성공·실패를 판단해야 한다면, 스크립트 끝에 명시적으로 `exit 0`(성공) 또는 `exit 1`(실패) 같은 종료 코드를 남겨야 한다. 아무것도 하지 않으면 호출자는 스크립트가 실제로 잘 끝났는지 알 방법이 없다.

**이식성**: CMD의 `.bat` 파일, Bash의 `.sh` 스크립트에 대응한다. Bash의 `source script.sh`(또는 `. script.sh`)가 PowerShell의 점 소싱과 정확히 같은 개념 — 현재 셸 세션에 함수·변수를 그대로 남긴다 — 이지만, PowerShell은 이 개념을 명시적인 스코프 규칙으로 문서화해 둔 점이 다르다. `$LASTEXITCODE`는 Bash의 `$?`, CMD의 `%ERRORLEVEL%`에 대응한다.

## Reference

- [about_Scripts - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts)
