---
draft: true
collection_order: 80
slug: packagemanagement-get-install-package-powershell
title: "[PowerShell] 80. PackageManagement — Get-Package/Install-Package"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell PackageManagement 모듈이 여러 패키지 소스를 하나의 cmdlet 인터페이스로 통합하는 프로바이더 개념과 Get-Package/Install-Package/-ProviderName 사용법, 76장 PowerShellGet과의 관계를 정리한 Part 10 시작 챕터다."
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
- PackageManagement
- Get-Package
- Install-Package
- Provider-Model
- Software-Inventory
- Package-Provider
image: "wordcloud.png"
---

## 개요

**PackageManagement**는 NuGet, PowerShellGet 등 서로 다른 패키지 소스를 하나의 통일된 cmdlet 인터페이스로 다루게 해 주는 모듈이다. 76장에서 PowerShell Gallery 전용으로 쓴 `Install-Module`이 사실은 이 PackageManagement 프레임워크 위에 얹힌 "PowerShellGet 프로바이더"의 한 사례였다는 것이 이 장의 핵심이다. Part 10(패키지·업데이트 관리)을 시작하며, "PowerShell 모듈"을 넘어 "이 컴퓨터에 설치된 소프트웨어 전반"으로 관리 범위를 넓힌다.

정신 모델은 30장에서 다룬 프로바이더 개념과 정확히 같다 — `Get-ChildItem`이 파일 시스템이든 레지스트리든 같은 인터페이스로 다뤘듯, `Get-Package`/`Install-Package`도 **프로바이더**(NuGet, PowerShellGet, Bootstrap 등)만 바꾸면 서로 다른 패키지 소스를 같은 명령으로 다룰 수 있다.

## 사용법

```powershell
Get-Package [-Name <이름>] [-ProviderName <프로바이더>]
Install-Package -Name <이름> -ProviderName <프로바이더>
```

## 종류

| 프로바이더 | 다루는 대상 |
|---|---|
| `PowerShellGet` | PowerShell 모듈·스크립트(76장의 `Install-Module`이 내부적으로 쓰는 것과 같은 계열) |
| `NuGet` | .NET NuGet 패키지 |
| `Bootstrap` | 다른 프로바이더 자체를 설치하는 프로바이더(최초 부트스트랩용) |
| `msi` | Windows `.msi` 설치 패키지 |
| `Programs` | 제어판의 "프로그램 및 기능"에 등록된 프로그램 |

## 예시

```powershell
Get-PackageProvider                                  # 현재 사용 가능한 프로바이더 목록
Get-Package                                            # 모든 프로바이더의 설치된 패키지 전부

Get-Package -ProviderName PowerShellGet -AllVersions    # 특정 프로바이더로 범위 좁히기
Get-Package -Name PackageManagement -RequiredVersion 1.3.1

Install-Package -Name 7zip -ProviderName Programs         # 다른 프로바이더로 설치(사용 가능한 경우)

Get-Package -Name posh-git -RequiredVersion 0.7.3 | Uninstall-Package   # 파이프라인으로 제거

Invoke-Command -ComputerName Server01 -Credential CONTOSO\User -ScriptBlock { Get-Package }  # 원격 조회(11부 예고)
```

## 주의사항·함정

**`Get-Package`가 시스템의 모든 소프트웨어를 다 보여주는 것은 아니다**: 오직 PackageManagement 프레임워크(그리고 등록된 프로바이더)를 통해 설치된 패키지만 목록에 나타난다. 사용자가 수동으로 `.exe` 설치 파일을 실행해 깐 프로그램은 이 목록에서 빠질 수 있다 — 시스템 전체의 설치된 프로그램 목록이 필요하다면 `Get-Package -ProviderName Programs`처럼 해당 프로바이더를 명시하거나, 13부에서 다룰 다른 조회 방법을 함께 써야 한다.

**같은 이름의 cmdlet이라도 프로바이더에 따라 동적 매개변수가 달라진다**: `Get-Package`의 `-NoPathUpdate`, `-AllowClobber` 같은 매개변수는 `-ProviderName PowerShellGet`을 지정했을 때만 나타나는 동적 매개변수다. `Get-Help Get-Package -Full`으로 확인해야 프로바이더별로 어떤 매개변수가 추가되는지 알 수 있다 — 38장에서 다룬 프로바이더별 동적 매개변수 개념이 여기서도 그대로 적용된다.

**PackageManagement와 PowerShellGet은 별개의 모듈이지만 자주 혼동된다**: `Install-Module`(76장, PowerShellGet 모듈)과 `Install-Package -ProviderName PowerShellGet`(PackageManagement 모듈)은 최종 결과가 비슷하지만 서로 다른 모듈이 제공하는 명령이다. 스크립트를 작성할 때는 어느 모듈의 cmdlet을 실제로 쓰고 있는지 `Get-Command`로 확인하는 습관이 안전하다.

**이식성**: Linux의 `apt`/`dnf`가 배포판 저장소 하나에 특화된 것과 달리, PackageManagement는 처음부터 "여러 이질적인 패키지 소스를 하나의 인터페이스로 통합한다"는 설계 목표를 갖고 만들어졌다. macOS의 Homebrew, Windows의 `winget`(81장에서 다룸)은 각각 독자적인 명령 인터페이스를 갖고 있어, PackageManagement처럼 여러 프로바이더를 한 cmdlet 아래 묶는 추상화 계층은 PowerShell 생태계의 특징적인 설계다.

## Reference

- [Get-Package (PackageManagement) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/packagemanagement/get-package)
