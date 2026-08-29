---
draft: true
collection_order: 76
slug: powershell-gallery-install-find-module-powershell
title: "[PowerShell] 76. PowerShell Gallery — Install-Module/Find-Module"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell Gallery에서 Find-Module로 모듈을 검색하고 Install-Module로 설치하는 법과 -Scope CurrentUser/AllUsers 차이, 설치 후 자동 임포트되지 않는 보안 설계, Update-Module/Uninstall-Module 사용법을 정리한 챕터다."
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
- PowerShell-Gallery
- Install-Module
- Find-Module
- Package-Manager
- PowerShellGet
- Repository
image: "wordcloud.png"
---

## 개요

**PowerShell Gallery**는 커뮤니티와 Microsoft가 게시한 모듈·스크립트를 모아 둔 공개 저장소이고, `Find-Module`/`Install-Module`은 74–75장에서 다룬 "직접 만든 모듈"이 아니라 "남이 만들어 배포한 모듈"을 가져오는 통로다. `PowerShellGet` 모듈(PowerShell 5.0+ 기본 포함)이 이 cmdlet들을 제공하며, PowerShell 7.4부터는 더 새로운 `Microsoft.PowerShell.PSResourceGet`이 권장 대안으로 함께 제공된다.

정신 모델은 "`Find-Module`은 카탈로그를 검색하는 것이고, `Install-Module`은 실제로 다운로드해 로컬 디스크에 설치하는 것"이라는 것이다. 75장의 `Import-Module`과 마찬가지로, 설치는 세션에 자동으로 로드되는 것과는 별개의 단계다.

## 사용법

```powershell
Find-Module -Name <모듈이름>
Install-Module -Name <모듈이름> [-Scope CurrentUser|AllUsers] [-RequiredVersion <버전>]
Update-Module -Name <모듈이름>
Uninstall-Module -Name <모듈이름>
```

## 종류

| cmdlet | 역할 |
|---|---|
| `Find-Module` | 저장소에서 모듈 검색(설치는 안 함) |
| `Install-Module` | 검색된 모듈을 로컬에 다운로드·설치 |
| `Update-Module` | 이미 설치된 모듈을 최신 버전으로 갱신 |
| `Uninstall-Module` | 설치된 모듈을 디스크에서 완전히 제거(75장의 `Remove-Module`과 달리 영구적) |
| `-Scope CurrentUser` | 현재 사용자 전용 경로에 설치(관리자 권한 불필요) |
| `-Scope AllUsers` | 모든 사용자가 쓸 수 있는 경로에 설치(관리자 권한 필요) |

## 예시

```powershell
Find-Module -Name PowerShellGet | Install-Module          # 검색 결과를 그대로 파이프로 설치

Install-Module -Name Pester -Scope CurrentUser              # 현재 사용자 전용, 관리자 권한 불필요
Install-Module -Name PSScriptAnalyzer -RequiredVersion 1.20.0   # 특정 버전 고정 설치

Find-Module PSReadLine -AllVersions -AllowPrerelease |        # 프리릴리스 버전까지 포함해 검색
    Select-Object -First 5

Update-Module -Name Pester                                     # 설치된 모듈을 최신 버전으로
Get-InstalledModule                                              # 이 저장소에서 설치한 모듈 목록
Uninstall-Module -Name Pester                                     # 완전히 제거
```

## 주의사항·함정

**설치된 모듈은 보안을 위해 자동으로 임포트되지 않는다**: `Install-Module`로 모듈을 설치해도 세션에 바로 사용할 수 있게 되는 것은 아니다 — 악성 코드가 포함된 모듈을 설치 즉시 실행하는 사고를 막기 위한 의도적인 설계다. 처음 사용하는 모듈이라면 코드를 먼저 검토한 뒤, 75장에서 배운 `Import-Module`이나 명령을 처음 호출할 때의 자동 로딩으로 실제로 세션에 들여와야 한다.

**`-Scope`를 생략하면 PowerShell 버전과 실행 권한에 따라 기본값이 달라진다**: PowerShellGet 1.x는 기본이 `AllUsers`(관리자 권한 필요)지만, PowerShellGet 2.0 이상에서 일반 세션으로 실행하면 기본이 `CurrentUser`(권한 불필요)로 바뀐다. 관리자 권한으로 실행 중인 세션에서는 다시 `AllUsers`가 기본이 된다 — 스크립트를 여러 환경에 배포한다면 `-Scope`를 명시적으로 지정해 이 버전별 기본값 차이에 흔들리지 않게 하는 편이 안전하다.

**같은 이름의 명령을 제공하는 모듈이 이미 있으면 경고가 뜨고 설치가 중단될 수 있다**: 기존 모듈과 이름·명령이 충돌하면 `Install-Module`이 경고를 표시하며 확인을 요구한다. 의도적으로 덮어쓰려면 `-Force`와 `-AllowClobber`를 함께 써야 하지만, 이는 기존에 의존하던 다른 스크립트를 깨뜨릴 수 있으므로 신중하게 판단해야 한다.

**TLS 1.2 미만 설정에서는 PowerShell Gallery 접근 자체가 실패한다**: 오래된 Windows PowerShell 5.1 환경이라면 `[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12`를 먼저 실행해야 갤러리 연결이 되는 경우가 있다 — PowerShell Gallery가 오래된 TLS 버전 지원을 중단했기 때문이다.

**이식성**: PowerShell Gallery는 Python의 PyPI(`pip install`), Node.js의 npm(`npm install`)에 정확히 대응하는 개념이다. Bash·CMD 생태계에는 언어 자체에 내장된 패키지 관리자가 없어 각 배포판의 시스템 패키지 관리자(`apt`, `winget` 등, 10부에서 다룰 예정)에 의존해야 한다는 점이 다르다.

## Reference

- [Install-Module (PowerShellGet) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/powershellget/install-module)
