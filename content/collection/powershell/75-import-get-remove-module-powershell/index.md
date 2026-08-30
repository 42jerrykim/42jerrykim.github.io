---
draft: false
collection_order: 75
slug: import-get-remove-module-powershell
title: "[PowerShell] 75. Import-Module/Get-Module/Remove-Module"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 모듈 자동 로딩(module autoloading) 원리와 Import-Module로 수동 임포트하는 법, Get-Module -ListAvailable로 설치된 모듈을 찾는 법, Remove-Module로 세션에서 제거하는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Module(모듈)
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
- Import-Module
- Get-Module
- Remove-Module
- Module-Autoloading
- Name-Conflict
- Session-Command
image: "wordcloud.png"
---

## 개요

`Import-Module`, `Get-Module`, `Remove-Module`은 74장에서 만든(또는 이미 설치된) 모듈을 세션에 불러오고, 무엇이 로드돼 있는지 확인하고, 다시 내보내는 세 가지 기본 동작을 담당한다. PowerShell 3.0부터는 대부분의 경우 이 cmdlet을 직접 부르지 않아도 <strong>자동 로딩(autoloading)</strong>으로 알아서 처리되지만, 그 기본 동작을 이해해야 자동 로딩이 안 되는 예외 상황에 대처할 수 있다.

정신 모델은 "설치된 모듈은 아직 세션에 들어오지 않은 상자와 같고, 그 안의 명령을 처음 부르는 순간 PowerShell이 알아서 상자를 열어 세션에 풀어놓는다"는 것이다 — `Import-Module`은 이 과정을 수동으로 강제하는 것이다.

## 사용법

```powershell
Import-Module <모듈이름 또는 경로> [-Force] [-Prefix <접두사>] [-NoClobber]
Get-Module [-ListAvailable] [-Name <이름>]
Remove-Module <모듈이름>
```

## 종류

| 상황 | 필요한 동작 |
|---|---|
| `$Env:PSModulePath`에 있는 모듈의 명령을 처음 호출 | 자동 로딩 — 아무것도 안 해도 됨 |
| 표준 경로 밖의 모듈 | `Import-Module <전체경로>`로 수동 임포트 |
| `.dll`/`.psm1` 파일 하나만 있는 경우 | 파일 경로를 직접 `Import-Module`에 지정 |
| 이름이 충돌하는 명령이 있는 모듈 | `-Prefix`(접두사 추가) 또는 `-NoClobber`(충돌 명령 제외) |
| 현재 세션에 로드된 모듈만 확인 | `Get-Module`(매개변수 없이) |
| 설치는 됐지만 아직 로드 안 된 모듈까지 확인 | `Get-Module -ListAvailable` |

## 예시

```powershell
Get-CimInstance Win32_OperatingSystem      # CimCmdlets 모듈이 자동으로 로드됨(별도 조치 불필요)

Import-Module BitsTransfer                  # 표준 경로의 모듈을 명시적으로 임포트
Import-Module C:\ps-test\TestCmdlets         # 표준 경로 밖의 모듈은 전체 경로 필요
Import-Module C:\ps-test\TestCmdlets.dll      # 폴더가 아니라 파일 하나만 있는 경우

Get-Module                                    # 현재 세션에 로드된 모듈만
Get-Module -ListAvailable                      # PSModulePath에 설치된 모든 모듈(로드 여부 무관)
Get-Command -Module BitsTransfer                # 특정 모듈이 제공하는 명령 목록

Import-Module MyModule -Prefix My               # Get-Item → Get-MyItem처럼 접두사로 충돌 회피
Import-Module MyModule -NoClobber                # 충돌하는 명령은 아예 임포트하지 않음

Get-Command Get-Date -All | Select-Object Name, CommandType, Module   # 이름 충돌 소스 확인
Microsoft.PowerShell.Utility\Get-Date              # 모듈명 접두사로 특정 버전 명시적 호출

Remove-Module BitsTransfer                          # 세션에서 제거(설치 자체는 그대로 유지)
```

## 주의사항·함정

**`Get-Command -Module`이 자동 로딩을 유발하지만, 와일드카드가 있으면 그렇지 않다**: `Get-Command Get-CimInstance`처럼 정확한 이름을 조회하면 해당 모듈이 자동으로 로드되지만, `Get-Command Get-Cim*`처럼 와일드카드를 쓰면 PowerShell은 어떤 모듈이 필요한지 확신할 수 없어 모듈을 로드하지 않는다 — 검색 목적으로 필요하지 않은 모듈까지 불필요하게 로드되는 것을 막기 위한 설계다.

**`Remove-Module`은 모듈을 삭제하는 것이 아니라 세션에서만 내리는 것이다**: 74장에서 설치한 모듈 파일 자체는 디스크에 그대로 남아 있고, `Remove-Module`은 단지 현재 세션에서 그 모듈이 추가한 명령·변수를 지우는 것뿐이다. 완전히 제거하려면 76장에서 다룰 `Uninstall-Module`이 필요하다.

**이름이 같은 함수와 cmdlet이 공존하면 함수가 우선한다**: 세션에 같은 이름의 함수와 cmdlet이 동시에 있으면 PowerShell은 기본적으로 함수를 실행한다. 어떤 소스의 명령이 실제로 실행되는지 확신이 서지 않는다면 `Get-Command -All`로 충돌 여부를 먼저 확인하는 습관이 안전하다 — 특히 여러 모듈을 조합해 쓰는 스크립트에서 흔히 발생하는 디버깅 함정이다.

**`Import-Module`을 프로필에 넣지 않으면 매 세션마다 다시 실행해야 한다**: 06장에서 다룬 `$PROFILE`에 자주 쓰는 모듈의 `Import-Module` 명령을 추가해 두면, 자동 로딩 대상이 아닌 모듈도 세션 시작 시 항상 준비된 상태로 만들 수 있다.

**이식성**: Bash의 `source module.sh`가 `Import-Module`과 개념적으로 가장 비슷하지만, "설치는 됐지만 아직 로드 안 된 모듈 목록"이라는 `Get-Module -ListAvailable` 같은 구분이나 자동 로딩 메커니즘은 없다. Python의 `import` 문이 처음 호출 시점에 자동으로 모듈을 찾아 로드한다는 점에서는 PowerShell의 자동 로딩과 비슷한 편의성을 제공한다.

## Reference

- [about_Modules - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_modules)
