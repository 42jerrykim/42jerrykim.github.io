---
draft: false
collection_order: 30
slug: psdrive-provider-concept-powershell
title: "[PowerShell] 30. PSDrive와 프로바이더 개념"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 프로바이더가 레지스트리·인증서·환경변수 같은 서로 다른 데이터 저장소를 파일 시스템처럼 드라이브로 노출하는 원리, 내장 프로바이더 목록, Get-PSDrive/Get-PSProvider로 확인하는 법을 정리한 Part 4 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
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
- File-System
- PSDrive
- PSProvider
- Registry
- Concept
- Cmdlet
- Get-ChildItem
- Environment
image: "wordcloud.png"
---

## 개요

<strong>프로바이더(provider)</strong>는 레지스트리, 인증서 저장소, 환경 변수, 함수 목록처럼 원래 파일 시스템이 아닌 데이터를 파일 시스템과 똑같은 방식(드라이브·경로·`cd`·`dir`)으로 다룰 수 있게 해 주는 .NET 프로그램이다. 4장부터 다룬 `Get-ChildItem`, `Test-Path` 같은 cmdlet이 파일뿐 아니라 레지스트리 키에도 그대로 통하는 이유가 바로 이 프로바이더 계층 덕분이다.

정신 모델은 "PowerShell은 계층 구조를 가진 어떤 데이터든 드라이브라는 동일한 틀에 끼워 넣는다"는 것이다. `C:`가 파일 시스템의 진입점이듯, `HKLM:`은 레지스트리의, `Cert:`는 인증서 저장소의, `Env:`는 환경 변수의 진입점이다 — 이 모든 드라이브를 같은 `Get-ChildItem`/`Set-Location`/`Get-Item` 세트로 탐색할 수 있다.

## 종류

| 프로바이더 | 드라이브 | 노출하는 객체 타입 |
|---|---|---|
| FileSystem | `C:` 등 | `System.IO.FileInfo`, `System.IO.DirectoryInfo` |
| Registry(Windows 전용) | `HKLM:`, `HKCU:` | `Microsoft.Win32.RegistryKey` |
| Certificate(Windows 전용) | `Cert:` | `X509Certificate2` |
| Alias | `Alias:` | `AliasInfo` |
| Environment | `Env:` | `DictionaryEntry` |
| Function | `Function:` | `FunctionInfo` |
| Variable | `Variable:` | `PSVariable` |
| WSMan(Windows 전용) | `WSMan:` | WS-Management 구성 요소 |

프로바이더가 지원하는 cmdlet은 공통이다 — `Get-ChildItem`, `Get-Item`, `New-Item`, `Copy-Item`, `Move-Item`, `Remove-Item`, `Rename-Item`, `Get-ItemProperty` 계열, `Set-Location`/`Push-Location`/`Pop-Location`, `Test-Path` 등은 어느 드라이브에서든 똑같이 동작한다.

## 예시

```powershell
Get-PSProvider                          # 세션에서 사용 가능한 프로바이더 목록
Get-PSDrive                             # 프로바이더가 노출하는 드라이브 목록
Get-PSDrive Function | Format-List *    # 특정 드라이브의 세부 정보

Get-Item Alias:                         # Alias: 드라이브 자체를 조회
Get-ChildItem HKLM:\SOFTWARE\           # 다른 드라이브에서 경로만으로 접근
Set-Location Cert:                      # Cert: 드라이브로 이동
Get-ChildItem                           # 현재 위치(Cert:) 조회

Set-Location HKLM:\SOFTWARE\Microsoft
Get-ChildItem .\PowerShell              # 상대 경로(.)
Set-Location ..\..\OtherKey             # 상위로 이동(..)

(Get-PSProvider FileSystem).Home = "C:\"   # 프로바이더별 홈 위치 설정
Set-Location ~                              # 홈으로 이동(~)
```

## 주의사항·함정

**모든 프로바이더가 모든 플랫폼에서 동작하지는 않는다**: Registry, Certificate, WSMan 프로바이더는 Windows 전용이다. 크로스플랫폼 스크립트를 작성한다면 `$IsWindows` 자동 변수로 분기하거나, 애초에 FileSystem·Environment·Variable처럼 모든 플랫폼에 있는 프로바이더만 의존하도록 설계해야 한다.

**프로바이더마다 동적 매개변수가 다르게 추가된다**: 예를 들어 `Cert:` 드라이브는 `Get-ChildItem`에 `-CodeSigningCert` 같은 프로바이더 전용 매개변수를 추가한다. 이런 매개변수는 그 드라이브 안에서만 나타나므로, 다른 드라이브에서 같은 cmdlet을 쓸 때는 보이지 않는다고 당황할 필요 없다.

**`Get-PSDrive`가 보여주는 드라이브가 전부는 아니다**: 어떤 프로바이더는 모듈을 임포트해야 비로소 드라이브가 나타난다. 필요한 드라이브가 안 보이면 관련 모듈이 로드됐는지부터 확인한다.

**이식성**: CMD·Bash에는 파일 시스템 외의 데이터를 "탐색 가능한 경로"로 노출하는 개념 자체가 없다 — 레지스트리를 다루려면 `reg.exe`처럼 완전히 별도의 도구·문법을 배워야 한다. PowerShell 프로바이더는 서로 다른 데이터 저장소를 배우는 비용을 "이미 아는 파일 시스템 명령을 다른 경로에 쓰는 것"으로 크게 낮춘다.

## Reference

- [about_Providers - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_providers)
