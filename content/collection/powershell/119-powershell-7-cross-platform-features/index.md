---
draft: true
collection_order: 119
slug: powershell-7-cross-platform-features
title: "[PowerShell] 119. PowerShell 7의 크로스플랫폼 특징과 새 기능"
date: 2026-08-29
lastmod: 2026-08-29
description: ".NET 위에서 Windows·Linux·macOS를 모두 지원하는 PowerShell 7(pwsh)이 Windows PowerShell 5.1과 근본적으로 다른 실행 기반을 갖는 이유와, ternary 연산자·파이프라인 체이닝 같은 7.x의 주요 신규 문법을 정리한 Part 18 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Cross-Platform
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
- Pwsh
- Dotnet-Core
- Ternary-Operator
- Pipeline-Chain-Operator
- Version-History
- Language-Feature
image: "wordcloud.png"
---

## 개요

이 컬렉션은 지금까지 대부분 Windows 전용 cmdlet(NetAdapter, ActiveDirectory, GroupPolicy 등)을 다뤄왔지만, 그 바탕이 되는 <strong>PowerShell 7(pwsh)</strong> 자체는 Windows·Linux·macOS를 모두 지원하는 완전한 크로스플랫폼 셸이다. Part 18을 여는 이 장은 지금까지 곳곳에서 "Windows 전용"이라고 짚었던 경계선을 다시 정리하며, PowerShell 7이 어떤 기반 위에서 그 크로스플랫폼 지원을 가능하게 했는지, 그리고 Windows PowerShell 5.1에는 없던 어떤 새 문법을 얻었는지를 다룬다.

정신 모델은 "Windows PowerShell 5.1이 .NET Framework라는 Windows 전용 런타임 위에 얹혀 있었다면, PowerShell 7은 크로스플랫폼 런타임인 .NET(과거 .NET Core) 위에 완전히 새로 지어진 별채"라는 것이다. 이름은 이어지지만 실행 기반 자체가 다르며, 이 차이가 이 컬렉션 전체에서 반복적으로 등장한 "이 cmdlet은 Windows 전용" 경계의 근본 원인이다.

## 사용법

```powershell
$PSVersionTable            # 현재 세션이 Windows PowerShell인지 PowerShell 7인지, .NET 버전은 무엇인지 확인
```

## 종류

| 구분 | Windows PowerShell 5.1 | PowerShell 7(pwsh) |
|---|---|---|
| 실행 파일 | `powershell.exe` | `pwsh`(Windows/Linux/macOS 공통) |
| 런타임 | .NET Framework(Windows 전용, Desktop 에디션) | .NET(과거 .NET Core, 크로스플랫폼, Core 에디션) |
| 지원 OS | Windows만 | Windows, Linux, macOS |
| 업데이트 주기 | Windows와 함께 서비스, 신규 기능 개발 중단 | GitHub에서 독립적으로 활발히 개발·배포 |
| 병행 설치 | 시스템에 내장(제거 불가) | 별도 설치, 5.1과 나란히 공존 가능 |
| 신규 문법(7.0+) | 없음 | 삼항 연산자(`?:`), 파이프라인 체이닝(`&&`/`\|\|`), null 병합(`??`) 등 |

| 신규 문법(7.0 이상) | 예시 |
|---|---|
| 삼항 연산자 | `$result = $x -gt 0 ? "양수" : "음수"` |
| 파이프라인 체이닝 | `Test-Path $path && Get-ChildItem $path` |
| null 병합 대입 | `$config.Timeout ??= 30` |

## 예시

```powershell
$PSVersionTable                                                   # PSVersion, PSEdition(Core/Desktop), OS 필드로 실행 환경 확인
# PSVersion  : 7.5.10
# PSEdition  : Core
# OS         : Microsoft Windows 10.0.26200

if ($PSVersionTable.PSEdition -eq "Core") {                         # 스크립트 안에서 실행 환경을 분기(88장 SSH 원격처럼 플랫폼별 분기가 필요할 때)
    Write-Host "PowerShell 7 이상에서 실행 중"
} else {
    Write-Host "Windows PowerShell 5.1에서 실행 중"
}

$grade = 85 -ge 60 ? "합격" : "불합격"                                # 삼항 연산자 — 20장의 if/else를 한 줄로 축약(가독성이 떨어지면 굳이 쓸 필요 없음)

Test-Path "C:\Data" && Get-ChildItem "C:\Data" || Write-Warning "경로 없음"   # 파이프라인 체이닝 — CMD의 && / Bash의 && 문법을 그대로 이식

$Timeout = $null
$Timeout ??= 30                                                     # null 병합 대입 — 값이 없을 때만 기본값 지정(41장 변수 초기화 패턴을 한 줄로)

Get-Random -Maximum 100 | ForEach-Object -Parallel { $_ * 2 } -ThrottleLimit 5   # 79장 ForEach-Object -Parallel도 PowerShell 7 전용 기능
```

## 주의사항·함정

**"PowerShell 7이 Windows PowerShell 5.1의 새 버전"이라는 생각은 절반만 맞다**: 버전 번호는 이어지지만 내부적으로는 완전히 다른 런타임(.NET Framework → .NET) 위에 다시 지어진 셸이다. 이 때문에 94장에서 다룬 `Get-WmiObject`처럼 .NET Framework의 COM/DCOM 기반 기능에 의존하던 일부 cmdlet은 PowerShell 7에 아예 존재하지 않으며, `Get-CimInstance` 같은 대체 cmdlet으로 옮겨가야 한다.

**7.0 이상의 신규 문법(`?:`, `&&`, `??`)은 Windows PowerShell 5.1에서는 구문 오류를 낸다**: 두 버전을 함께 지원해야 하는 스크립트를 작성한다면, 이 새 연산자들을 쓰는 순간 5.1과의 호환성이 깨진다. 스크립트 상단에 64장에서 배운 `#Requires -Version 7.0`을 명시해 두면, 5.1에서 실수로 실행했을 때 알아보기 힘든 구문 오류 대신 명확한 버전 요구 메시지를 보여준다.

**Windows PowerShell 5.1은 더 이상 신규 기능 개발이 이뤄지지 않지만, Windows에서 완전히 사라지는 것은 아니다**: 5.1은 Windows의 구성 요소로 계속 포함돼 보안·긴급 수정만 받는 유지보수 상태다. 일부 레거시 관리 도구나 특정 벤더 스크립트가 여전히 5.1(Desktop 에디션)에서만 동작하는 경우가 있어, 실무에서는 두 버전이 당분간 함께 존재하는 상황을 전제로 스크립트를 설계해야 한다.

**pwsh를 설치해도 기본 콘솔 단축키(`Win+X` 메뉴 등)는 여전히 Windows PowerShell 5.1을 가리킬 수 있다**: PowerShell 7은 Windows에 기본 내장되지 않고 별도로 설치해야 하며, 설치 후에도 시스템 기본값이 자동으로 바뀌지 않는다. `pwsh`를 기본 셸로 쓰려면 터미널 앱(Windows Terminal 등)의 기본 프로필을 직접 변경해야 한다.

**이식성**: PowerShell 7의 크로스플랫폼 지원은 "Windows 전용 cmdlet도 어디서나 동작한다"는 뜻이 아니다 — 109–118장에서 다룬 NetAdapter·ActiveDirectory·GroupPolicy 모듈은 여전히 Windows(또는 도메인 환경) 전용이며, pwsh 자체가 크로스플랫폼이라는 것과 그 위에서 실행되는 모든 모듈이 크로스플랫폼이라는 것은 별개의 문제다. Bash·CMD 경험자에게는 이 구분이 "셸 자체는 어디서나 쓸 수 있지만, 셸 위에서 호출하는 명령이 그 운영체제에만 있는 것과 마찬가지"라는 비유로 설명하면 이해하기 쉽다.

## Reference

- [What's New in PowerShell 7.5 - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-75)
