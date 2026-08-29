---
draft: true
collection_order: 64
slug: requires-directive-metadata-powershell
title: "[PowerShell] 64. #Requires 지시문과 스크립트 메타데이터"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell #Requires -Version/-Modules/-PSEdition/-RunAsAdministrator 지시문으로 스크립트 실행 전 전제 조건을 강제하는 법과 검사가 스크립트 실행 자체를 막는 전역적 성격을 정리한 Part 6 마지막 챕터다."
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
- Requires-Directive
- Script-Metadata
- Version-Check
- RunAsAdministrator
- Module-Dependency
- Prerequisite-Check
image: "wordcloud.png"
---

## 개요

`#Requires`는 스크립트가 실행되기도 전에 PowerShell 버전·필요 모듈·관리자 권한 같은 전제 조건을 검사해, 조건이 안 맞으면 스크립트를 아예 시작하지 못하게 막는 특수 주석이다. 53장에서 스크립트를 작성하고 실행하는 법을 배운 뒤, 61장까지 함수와 파이프라인 바인딩으로 스크립트의 내부 로직을 다듬어 왔다면, 이 장은 그 스크립트가 애초에 잘못된 환경에서 실행되는 것 자체를 막는 마지막 안전장치를 다루며 Part 6을 마무리한다.

정신 모델은 "`#Requires`는 스크립트 본문이 시작하기 전에 실행되는, 실패하면 아예 진입을 거부하는 문지기"라는 것이다. 이는 스크립트 본문 안에서 `if ($PSVersionTable.PSVersion -lt ...) { throw ... }`처럼 직접 검사하는 것과 달리, PowerShell 엔진 수준에서 강제된다.

## 사용법

```powershell
#Requires -Version <N>[.<n>]
#Requires -Modules <모듈이름> | <해시테이블>
#Requires -PSEdition <Core | Desktop>
#Requires -RunAsAdministrator
```

## 종류

| 매개변수 | 검사 내용 |
|---|---|
| `-Version` | 최소 PowerShell 버전(예: `6.0`) |
| `-Modules` | 필요한 모듈(문자열, 또는 `ModuleVersion`/`RequiredVersion`/`MaximumVersion`을 가진 해시테이블) |
| `-PSEdition` | `Core`(PowerShell 7/pwsh) 또는 `Desktop`(Windows PowerShell 5.1) — 01장에서 다룬 두 에디션 구분과 직결 |
| `-RunAsAdministrator` | 관리자 권한으로 시작된 세션이어야 함(비Windows에서는 무시됨) |

## 예시

```powershell
#Requires -Version 7.0
#Requires -Modules @{ ModuleName = "Az.Accounts"; ModuleVersion = "2.0.0" }
#Requires -RunAsAdministrator

param (
    [Parameter(Mandatory)]
    [string[]]$Path
)
# 여기부터 본문 — 위 조건을 모두 만족해야 도달함
```

```powershell
#Requires -Modules AzureRM.Netcore, PowerShellGet     # 여러 모듈, 버전 무관하게

#Requires -Modules @{ ModuleName = "Pester"; RequiredVersion = "5.3.1" }   # 정확히 이 버전만

#Requires -PSEdition Core        # PowerShell 7(pwsh)에서만 실행 허용
```

## 주의사항·함정

**`#Requires`는 스크립트 안 어디에 적어도 전역적으로 먼저 검사된다**: 코드 순서상 스크립트 첫 줄에서 필요한 모듈을 `Remove-Module`로 제거한 뒤 그 아래에 `#Requires -Modules`를 적더라도, 검사 자체는 스크립트가 시작되기 **전에** 이미 통과한 상태이므로 실행 자체는 막히지 않는다. `#Requires`의 위치는 가독성의 문제일 뿐, 실행 순서에 영향을 주지 않는다는 점을 오해하기 쉽다.

**모듈 버전 문자열은 정확히 일치해야 한다**: `RequiredVersion = "0.12"`처럼 실제 설치된 버전("0.12.0")과 자릿수가 다르면 검사가 실패한다. `Get-Module -ListAvailable`로 정확한 버전 문자열을 확인한 뒤 그대로 옮겨 적어야 한다.

**`-RunAsAdministrator`는 비Windows 플랫폼에서 조용히 무시된다**: 크로스플랫폼 스크립트(1장에서 다룬 PowerShell 7의 특징)를 작성한다면, 이 지시문 하나만으로는 macOS·Linux에서 관리자 권한(`sudo`) 여부를 검사할 수 없다는 점을 감안해야 한다. 플랫폼을 가리지 않는 권한 검사가 필요하다면 별도의 코드로 직접 확인해야 한다.

**`#Requires -Modules`는 클래스·열거형 정의까지 불러오지는 않는다**: 모듈이 있는지만 확인하고 세션에 임포트할 뿐, 그 모듈 안에 정의된 사용자 정의 클래스·열거형(77장에서 다룰 `class` 키워드)을 실제로 사용하려면 `using module` 문을 스크립트 맨 앞에 별도로 추가해야 한다.

**이식성**: Bash·CMD에는 `#Requires`에 해당하는 표준화된 전제 조건 검사 문법이 없어, 스크립트 맨 앞에 버전이나 명령 존재 여부를 수동으로 검사하는 관용구(`command -v git`, `if not exist ...`)를 직접 작성해야 한다. PowerShell은 이런 검사를 언어 차원의 선언적 지시문으로 표준화해, 스크립트를 열어 보지 않고도 `Get-Help`나 정적 분석 도구(72장의 PSScriptAnalyzer)가 요구 사항을 파악할 수 있게 한다.

## Reference

- [about_Requires - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_requires)
