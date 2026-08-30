---
draft: false
collection_order: 40
slug: registry-provider-hklm-hkcu-powershell
title: "[PowerShell] 40. 레지스트리 프로바이더(Registry:) 다루기"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 레지스트리 프로바이더의 HKLM:/HKCU: 드라이브 구조, 레지스트리 키(컨테이너)와 값(속성)의 구분, New-ItemProperty로 값을 만드는 법, Get-Acl/Set-Acl로 권한을 다루는 법을 정리한 Part 4 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- File-System
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
- Registry
- HKLM
- HKCU
- New-ItemProperty
- Access-Control
- Backup
- System-Design
image: "wordcloud.png"
---

## 개요

**레지스트리 프로바이더**는 Windows 레지스트리를 `HKLM:`, `HKCU:` 드라이브로 노출해, 30장부터 다룬 파일 시스템 조작 cmdlet을 레지스트리에도 그대로 쓸 수 있게 해 준다(Windows 전용). 이 장은 Part 4에서 배운 `Get-ChildItem`, `New-Item`, `Copy-Item`, `Move-Item`, `Rename-Item`, `Remove-Item`, `Get-ItemProperty`/`Set-ItemProperty`가 레지스트리라는 구체적인 대상에서 어떻게 조합되는지 정리하며 Part 4를 마무리한다.

지금까지 이 Part의 모든 예제가 파일 시스템을 대상으로 했던 이유는 가장 직관적인 프로바이더이기 때문일 뿐, 다뤄온 cmdlet 자체는 처음부터 특정 프로바이더에 묶여 있지 않았다. 이 장은 그 일반성을 레지스트리라는 전혀 다른 데이터 저장소에 그대로 적용해 실제로 확인하는 자리다.

## 종류

| 개념 | 파일 시스템 대응 | 다루는 cmdlet |
|---|---|---|
| 레지스트리 키(컨테이너) | 디렉터리 | `Get-ChildItem`, `New-Item`, `Move-Item`, `Rename-Item`, `Remove-Item` |
| 레지스트리 값(Item Property) | 파일의 메타데이터/속성 | `Get-ItemProperty`, `New-ItemProperty`, `Set-ItemProperty`, `Move-ItemProperty`, `Rename-ItemProperty`, `Remove-ItemProperty` |
| 기본 드라이브 | — | `HKLM:`(HKEY_LOCAL_MACHINE), `HKCU:`(HKEY_CURRENT_USER) |
| 전체 하이브 이름으로 접근 | — | `Registry::HKEY_LOCAL_MACHINE\...`처럼 프로바이더 이름 + `::` 사용 |
| 값의 데이터 타입(`-Type`) | — | `String`(REG_SZ), `ExpandString`(REG_EXPAND_SZ), `Binary`, `DWord`, `MultiString`, `QWord` |

레지스트리 반환 타입도 파일 시스템과 대응한다 — 키는 `Microsoft.Win32.RegistryKey` 객체로, 값은 `PSCustomObject`로 반환된다.

## 예시

```powershell
Set-Location HKLM:                              # 레지스트리 드라이브로 이동
cd HKLM:\Software                                # 하위 키로 이동(별칭 사용)
cd "Registry::HKEY_LOCAL_MACHINE\Software"       # 전체 하이브 이름 표기법

Get-ChildItem -Path HKLM:\SYSTEM\CurrentControlSet\Services\Spooler   # 하위 키 목록
Get-Item -Path HKLM:\SYSTEM\CurrentControlSet\Services\Spooler        # 이 키 자체의 값들

$p = Get-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Spooler
$p.DependOnService                               # 특정 값만 꺼내기
Get-ItemPropertyValue -Path HKLM:\SOFTWARE\Microsoft\Wbem -Name BUILD   # PowerShell 5+

New-Item -Path "HKLM:\SOFTWARE" -Name "ContosoCompany"                 # 새 키
New-ItemProperty -Path "HKLM:\SOFTWARE\ContosoCompany" -Name Test -Type DWord -Value 1  # 새 값

Copy-Item -Path HKLM:\Software\Contoso -Destination HKLM:\Software\Fabrikam   # 키+값 복사
Move-Item -Path HKLM:\SOFTWARE\Contoso -Destination HKLM:\SOFTWARE\Fabrikam    # 키 이동
Rename-ItemProperty -Path $path -Name ContosoTest -NewName FabrikamTest       # 값 이름 변경

Remove-Item -Path HKLM:\SOFTWARE\Contoso\* -Recurse   # 키 자체는 남기고 내용만 삭제
Clear-Item .\Contoso\                                  # 모든 값을 지우되 키는 유지

# 레지스트리 키 권한 관리(14부에서 ACL을 본격적으로 다룬다)
$acl = Get-Acl -Path HKLM:\SOFTWARE\Contoso
$rule = New-Object System.Security.AccessControl.RegistryAccessRule("CONTOSO\jsmith", "FullControl", "Allow")
$acl.SetAccessRule($rule)
$acl | Set-Acl -Path HKLM:\SOFTWARE\Contoso
```

## 주의사항·함정

**키와 값을 혼동하면 아무것도 못 찾는다**: `Get-ChildItem`은 하위 **키**만 보여주고, 그 키가 가진 **값**은 절대 보여주지 않는다. 39장에서 짚었듯 `Test-Path`도 값의 존재는 확인하지 못한다. "이 레지스트리 데이터가 어디 있는가"를 찾을 때 키를 찾는 중인지 값을 찾는 중인지부터 구분해야 한다.

**값을 새로 만들 때 타입을 지정하지 않으면 REG_SZ(문자열)가 기본이다**: `Set-ItemProperty -Type` 동적 매개변수는 `Set-Item`에도 나타나지만 `Set-Item`에서는 아무 효과가 없다 — 반드시 `Set-ItemProperty`나 `New-ItemProperty`에서 지정해야 한다.

**내용이 있는 키를 `-Recurse` 없이 지우려 하면 항상 확인을 묻는다**: 36장에서 다룬 디렉터리 삭제와 동일한 안전장치가 레지스트리 키에도 적용된다. 키만 비우고 자체는 남기려면 `Remove-Item -Path 키\*`(끝에 백슬래시+와일드카드)를 쓰거나, 값만 지우려면 `Clear-Item`을 쓴다.

**레지스트리 조작은 시스템 전체에 영향을 줄 수 있다**: `HKLM:` 아래 키를 잘못 지우거나 잘못된 타입으로 값을 덮어쓰면 서비스가 시작되지 않거나 운영체제가 불안정해질 수 있다. 프로덕션 시스템에서는 변경 전 `Export-Clixml`이나 `.reg` 파일로 백업하고, 가능하면 `-WhatIf`로 먼저 확인하는 습관이 필요하다.

**이식성**: CMD의 `reg query`/`reg add`/`reg delete`가 정확히 이 프로바이더의 기능에 대응하지만, 텍스트 기반 명령줄 옵션을 따로 외워야 한다. PowerShell은 지금까지 배운 파일 시스템 cmdlet을 그대로 재사용한다는 점이 근본적으로 다르다 — 이것이 30장에서 소개한 프로바이더 개념이 실제로 배움의 비용을 줄여주는 대표적인 사례다.

## Reference

- [about_Registry_Provider - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_registry_provider)
