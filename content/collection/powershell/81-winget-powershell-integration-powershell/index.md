---
draft: false
collection_order: 81
slug: winget-powershell-integration-powershell
title: "[PowerShell] 81. winget과 PowerShell 통합"
date: 2026-08-29
lastmod: 2026-08-29
description: "Windows 패키지 관리자 winget의 install/upgrade/search 명령을 PowerShell에서 호출하는 법과 Microsoft.WinGet.Client 모듈로 cmdlet 형태로 다루는 법, 80장 PackageManagement와의 역할 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Package-Management
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
- winget
- Windows-Package-Manager
- App-Installer
- Software-Installation
- Native-Command
- CLI-Tool
image: "wordcloud.png"
---

## 개요

**winget**(Windows Package Manager)은 데스크톱 애플리케이션을 검색·설치·업그레이드·제거하는 Microsoft의 공식 명령줄 도구다. 80장의 PackageManagement가 PowerShell cmdlet 프레임워크 안에서 여러 프로바이더를 통합했다면, winget은 그 자체로 독립된 네이티브 실행 파일(`winget.exe`)이며 PowerShell에서는 다른 외부 명령(1장에서 언급한 네이티브 명령 실행 방식)처럼 호출한다.

정신 모델은 "winget은 스마트폰의 앱 스토어를 명령줄로 옮겨온 것"이라는 것이다 — 데스크톱 GUI 프로그램(Chrome, VS Code, 7-Zip 등)을 검색해 자동으로 다운로드·설치까지 마쳐 준다는 점에서, PowerShell 모듈만 다루는 76장의 `Install-Module`보다 다루는 대상의 폭이 훨씬 넓다.

## 사용법

```powershell
winget search <앱이름>
winget install <앱이름>
winget upgrade <앱이름 또는 --all>
winget uninstall <앱이름>
winget list
```

## 종류

| 명령 | 역할 |
|---|---|
| `search` | 사용 가능한 앱 검색 |
| `install` | 지정한 앱 설치 |
| `upgrade` | 설치된 앱을 최신 버전으로(`--all`로 전체 일괄 업그레이드) |
| `uninstall` | 설치된 앱 제거 |
| `list` | 현재 시스템에 설치된 패키지 목록 |
| `export`/`import` | 설치된 패키지 목록을 파일로 내보내거나, 그 파일대로 일괄 설치(새 컴퓨터 셋업에 유용) |
| `Microsoft.WinGet.Client` 모듈 | winget 기능을 PowerShell cmdlet(`Find-WinGetPackage`, `Install-WinGetPackage` 등)으로 감싼 공식 모듈 |

## 예시

```powershell
winget search "Visual Studio Code"                 # 검색
winget install --id Microsoft.VisualStudioCode        # 정확한 ID로 설치(이름 중복 방지)
winget upgrade --all                                    # 설치된 모든 앱 일괄 업그레이드
winget list                                               # 설치된 패키지 목록

winget export -o apps.json                                # 현재 설치 목록을 파일로 저장
winget import -i apps.json                                 # 다른 컴퓨터에서 그대로 재현

# Microsoft.WinGet.Client 모듈로 cmdlet 형태로 다루기(76장의 Install-Module 패턴과 동일하게 설치)
Install-Module -Name Microsoft.WinGet.Client -Scope CurrentUser
Find-WinGetPackage -Query "7zip"
Install-WinGetPackage -Id "7zip.7zip"

# PowerShell 스크립트 안에서 winget 결과를 파이프라인으로 활용
winget list | Out-String -Stream | Select-String "Chrome"    # 51장/46장 조합으로 텍스트 출력 검색
```

## 주의사항·함정

**winget은 네이티브 실행 파일이라 출력이 구조화된 객체가 아니라 텍스트다**: `winget list`의 결과는 10장에서 강조한 PowerShell 객체 파이프라인이 아니라 사람이 읽기 좋은 표 형태의 **텍스트**다. 이 출력을 프로그램적으로 파싱하려면 46장의 `Select-String`이나 문자열 분할로 직접 처리해야 하며, `Where-Object`로 속성을 걸러내는 것 같은 자연스러운 파이프라인 조작은 되지 않는다 — 구조화된 결과가 필요하다면 `Microsoft.WinGet.Client` 모듈의 cmdlet을 쓰는 편이 낫다.

**관리자 권한 여부에 따라 설치 동작이 달라진다**: 일부 앱은 설치 시 UAC(사용자 계정 컨트롤) 상승 프롬프트가 뜨는데, 관리자 권한 없이 `winget install`을 실행하면 사용자가 그 프롬프트를 승인해야 설치가 계속된다. 자동화 스크립트에서 사람의 개입 없이 실행해야 한다면, 관리자 권한 세션에서 실행하도록 스크립트를 설계해야 한다.

**`winget`은 최초 사용자 로그인 후에야 등록이 완료된다**: 새로 프로비저닝된 Windows 환경에서는 `winget`이 아직 등록되지 않아 명령을 찾을 수 없는 경우가 있다 — 이때는 `Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe`로 수동 등록을 요청해야 한다.

**이식성**: winget은 macOS의 Homebrew(`brew install`), Linux 배포판의 `apt`/`dnf`와 정확히 같은 역할을 하는 Windows 전용 도구다. 세 도구 모두 "명령 하나로 GUI 애플리케이션까지 설치한다"는 목표는 같지만, winget은 PowerShell이나 CMD 어디서든 그냥 실행 파일처럼 호출된다는 점에서 76장의 `Install-Module`(PowerShell 전용 cmdlet)과 호출 방식이 근본적으로 다르다.

## Reference

- [Use WinGet to install and manage applications | Microsoft Learn](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
