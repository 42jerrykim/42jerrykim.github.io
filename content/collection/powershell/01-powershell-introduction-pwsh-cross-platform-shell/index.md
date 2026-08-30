---
draft: false
collection_order: 1
slug: powershell-pwsh-introduction-cross-platform-shell
title: "[PowerShell] 01. PowerShell 소개 — pwsh와 Windows PowerShell"
date: 2026-08-29
lastmod: 2026-08-29
description: "Windows PowerShell 5.1과 PowerShell 7(pwsh)의 차이, 설치 방법, $PSVersionTable로 버전·에디션을 확인하는 법, 콘솔을 시작·종료하는 기본 조작을 정리한 PowerShell 입문 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Windows(윈도우)
- macOS
- Linux(리눅스)
- Shell(셸)
- Terminal
- .NET
- DevOps
- Automation(자동화)
- Cross-Platform
- Installation
- Configuration(설정)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- Version-Control
- Cmdlet
- pwsh
- WinGet
- MSI
- MSIX
image: "wordcloud.png"
---

PowerShell을 처음 설치하려는 사람이 가장 먼저 마주치는 혼란은 "PowerShell을 설치하라"는 말이 실제로는 두 가지 서로 다른 프로그램 중 하나를 가리킬 수 있다는 점이다. Windows에는 이미 `powershell.exe`가 있는데, 왜 또 `pwsh.exe`를 따로 설치해야 하는지 모르면 첫 단계부터 막힌다. 이 장은 Windows PowerShell 5.1과 PowerShell 7(pwsh)의 관계를 정리하고, 설치·시작·종료라는 가장 기본적인 조작을 다룬다.

## 개요

PowerShell은 2006년 "Windows PowerShell"이라는 이름으로 Windows 전용 셸로 출발했다. 2016년 Microsoft는 .NET Core 위에서 동작하는 오픈소스 "PowerShell Core"를 공개하며 Linux·macOS까지 지원 범위를 넓혔고, 이후 버전 6을 거쳐 지금은 "PowerShell 7"이라는 이름으로 이어지고 있다. 이 역사 때문에 지금도 Windows 환경에는 서로 다른 두 실행 파일이 공존한다.

| 구분 | Windows PowerShell 5.1 | PowerShell 7(pwsh) |
|---|---|---|
| 실행 파일 | `powershell.exe` | `pwsh.exe` |
| 기반 런타임 | .NET Framework | .NET |
| 지원 플랫폼 | Windows 전용 | Windows·Linux·macOS |
| 설치 방식 | Windows에 기본 내장 | 별도 설치 필요(WinGet·MSI·MSIX·ZIP 등) |
| 에디션(`$PSVersionTable.PSEdition`) | Desktop | Core |
| Microsoft 권장 대상 | 5.1 전용 레거시 모듈 유지 보수 | 신규 자동화 전반 |

PowerShell 7은 Windows PowerShell 5.1을 대체하지 않고 별도 디렉터리에 나란히 설치되어 함께 동작한다. 일부 Windows PowerShell 전용 모듈은 PowerShell 7의 Windows 호환성 기능으로 실행할 수 있지만, 그렇지 않은 모듈은 여전히 Windows PowerShell 5.1에서 실행해야 한다.

## 기본 개념

두 버전이 공존하는 시스템에서 "지금 내가 어떤 PowerShell을 쓰고 있는가"를 확인하는 방법은 자동 변수 `$PSVersionTable`이다.

```powershell
$PSVersionTable
```

이 명령은 `PSVersion`(버전 번호), `PSEdition`(`Desktop` 또는 `Core`), `OS`, `Platform`, `PSCompatibleVersions` 등을 표 형태로 보여준다. `PSEdition`이 `Desktop`이면 Windows PowerShell 5.1, `Core`이면 PowerShell 7 계열이다. 스크립트가 두 에디션 모두에서 실행돼야 한다면, 이 값으로 분기해 에디션별 동작 차이를 처리할 수 있다.

설치 위치를 알고 싶다면 `$PSHOME` 변수를 확인한다. 값이 `$Env:ProgramFiles\PowerShell\7`이면 대체로 MSI 패키지로 설치된 것이고, `$Env:ProgramFiles\WindowsApps\`로 시작하면 Microsoft Store(MSIX) 설치, `$HOME\.dotnet\tools`이면 .NET Global Tool로 설치된 것이다.

## 종류/세부

### 설치 방법 선택

Windows에서 PowerShell 7을 설치하는 방법은 여러 가지이며, 상황에 따라 권장되는 방식이 다르다.

| 설치 방법 | 적합한 상황 |
|---|---|
| WinGet | 개인 Windows 클라이언트에 설치할 때 권장하는 기본 방법 |
| MSI 패키지 | Windows Server·엔터프라이즈 배포 시나리오 |
| MSIX 패키지(Microsoft Store 포함) | 자동 업데이트가 필요한 일반 사용자, 단 원격 관리(Remoting)·전체 사용자 프로파일 미지원 등 제약이 있다 |
| ZIP 패키지 | 여러 버전을 나란히 설치하거나 Windows Server Core·Arm 기반 시스템에 설치할 때 |
| .NET Global Tool | .NET SDK가 이미 설치된 개발자 환경 |

가장 간단한 방법은 WinGet이다.

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Linux·macOS에서는 각 배포판의 패키지 관리자(APT, Homebrew 등)를 통해 설치한다. 이 컬렉션은 Windows 환경을 기준으로 서술하므로, Linux·macOS별 세부 설치 절차는 아래 참고 링크의 공식 문서를 따른다.

### 콘솔 시작과 종료

Windows PowerShell은 시작 메뉴의 "Windows PowerShell" 항목이나 `powershell` 명령으로, PowerShell 7은 "PowerShell 7" 항목이나 `pwsh` 명령으로 시작한다. 두 실행 파일 모두 `cmd.exe`, 다른 PowerShell 세션, 또는 파일 탐색기 주소창에서 직접 호출할 수 있다.

```powershell
pwsh                 # PowerShell 7 세션 시작
pwsh -NoProfile      # 프로파일 스크립트를 실행하지 않고 시작(문제 진단 시 유용)
pwsh -NoLogo         # 시작 배너 없이 시작
exit                 # 현재 세션 종료
```

`-NoProfile` 스위치는 프로파일 스크립트(06장에서 다룬다)가 오류를 일으켜 콘솔이 정상적으로 열리지 않을 때, 프로파일을 건너뛰고 원인을 진단하는 용도로 자주 쓰인다.

### 업그레이드와 제거

WinGet으로 설치했다면 아래 명령으로 업그레이드 가능 여부를 확인하고 갱신한다.

```powershell
winget list --id Microsoft.PowerShell --upgrade-available
winget upgrade --id Microsoft.PowerShell
```

제거도 설치에 사용한 방법과 짝을 맞춘다 — WinGet으로 설치했다면 `winget uninstall --id Microsoft.PowerShell`, MSI로 설치했다면 제어판의 "프로그램 추가/제거"를 이용한다.

## 주의사항·함정

**Microsoft Store(MSIX) 설치본의 제약**: Microsoft Store에서 설치한 PowerShell 7은 애플리케이션 샌드박스 안에서 실행되어 PowerShell Remoting을 지원하지 않고, `$PROFILE.AllUsersAllHosts`처럼 전체 사용자 대상 프로파일을 만들거나 수정할 수 없다. `Register-PSSessionConfiguration`, `Update-Help -Scope AllUsers`, `Set-ExecutionPolicy -Scope LocalMachine` 같은 명령도 이 설치본에서는 지원되지 않는다. 원격 관리(11부)를 다뤄야 한다면 MSI나 WinGet(MSI 설치 타입)으로 설치하는 편이 안전하다.

**시작 메뉴의 "Windows PowerShell ISE"는 Windows PowerShell 5.1 전용이다**: 통합 스크립팅 환경(ISE)은 PowerShell 7을 지원하지 않는 별도 애플리케이션이다. PowerShell 7 스크립트를 편집·디버깅하려면 Visual Studio Code와 PowerShell 확장을 쓰는 것이 현재 권장되는 방식이다(120장에서 다시 다룬다).

**이식성**: CMD의 `cmd.exe`나 Bash의 `bash`처럼 단일 실행 파일 하나로 끝나는 다른 셸과 달리, PowerShell은 "어느 실행 파일(`powershell.exe`/`pwsh.exe`)을 실행했는가"에 따라 사용 가능한 cmdlet과 모듈 호환성이 달라진다. 스크립트 상단에 `#Requires -PSEdition Core`처럼 요구 에디션을 명시해 두면(64장에서 다룬다), 잘못된 버전에서 실행됐을 때 바로 오류로 알려준다.

## Reference

- [What is PowerShell? - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/overview)
- [Install PowerShell 7 on Windows | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows)
- [Differences between Windows PowerShell 5.1 and PowerShell 7.x | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell)
