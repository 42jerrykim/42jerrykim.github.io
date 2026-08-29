---
draft: true
collection_order: 38
slug: get-set-itemproperty-command-powershell
title: "[PowerShell] 38. Get-ItemProperty/Set-ItemProperty"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-ItemProperty로 파일 속성이나 레지스트리 값을 조회하는 법과 Set-ItemProperty로 값을 만들거나 바꾸는 법, Get-Item이 보여주지 않는 레지스트리 값이 왜 ItemProperty로 따로 분리돼 있는지를 정리한 챕터다."
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
- Get-ItemProperty
- Set-ItemProperty
- Registry
- ReadOnly
- New-ItemProperty
- Metadata
image: "wordcloud.png"
---

## 개요

`Get-ItemProperty`/`Set-ItemProperty`는 항목 자체가 아니라 그 항목의 **속성**을 조회·설정하는 cmdlet이다. 파일 시스템에서는 `LastAccessTime`이나 `IsReadOnly` 같은 파일 속성을, 레지스트리에서는 키 안의 값(레지스트리 값, "Item Property"라고 부른다)을 다룬다.

정신 모델은 "레지스트리 키는 컨테이너(디렉터리에 대응)이고, 그 안의 값은 컨테이너의 속성(파일 자체가 아니라 파일의 메타데이터에 대응)"이라는 것이다. 그래서 `Get-ChildItem`으로는 레지스트리 값이 보이지 않는다 — 값은 자식 항목이 아니라 부모 키의 속성이기 때문에 `Get-ItemProperty`로 따로 조회해야 한다.

## 사용법

```powershell
Get-ItemProperty [-Path] <String[]> [[-Name] <String[]>]
Set-ItemProperty [-Path] <String[]> [-Name] <String> [-Value] <Object> [-Type <RegistryValueKind>]
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Name` | 둘 다 | 조회·설정할 속성(값) 이름. `Get-ItemProperty`에서는 와일드카드 지원, 생략 시 모든 속성 반환 |
| `-Value` | Set-ItemProperty | 설정할 값 |
| `-Type`(Registry 동적 매개변수) | Set-ItemProperty | `String`(REG_SZ), `DWord`(REG_DWORD), `Binary`, `MultiString`, `QWord` 등 레지스트리 값 타입 지정(기본 `String`) |
| `-InputObject` | Set-ItemProperty | 파이프로 받은 객체의 속성을 바로 변경 |

## 예시

```powershell
Get-ItemProperty C:\Windows                                    # 파일/디렉터리 속성 조회
Get-ItemProperty C:\Test\Weather.xls | Format-List               # 파일 속성 전체
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion -Name "ProgramFilesDir"

Set-ItemProperty -Path C:\GroupFiles\final.doc -Name IsReadOnly -Value $true   # 파일 속성 설정
Set-ItemProperty -Path "HKLM:\Software\ContosoCompany" -Name "NoOfEmployees" -Value 823
New-ItemProperty -Path "HKLM:\SOFTWARE\ContosoCompany" -Name "Test" -Type DWord -Value 1  # 새 값 생성

Get-ChildItem weekly.txt | Set-ItemProperty -Name IsReadOnly -Value $true      # 파이프로 대상 지정
Get-ItemPropertyValue -Path HKLM:\SOFTWARE\Microsoft\Wbem -Name BUILD          # 값만 바로 반환(PowerShell 5+)
```

## 주의사항·함정

**레지스트리 값을 만들 때는 `Set-ItemProperty`와 `New-ItemProperty` 중 무엇을 써도 되지만 의미가 다르다**: `Set-ItemProperty`는 값이 없으면 만들고 있으면 덮어쓰는 하나의 명령이고, `New-ItemProperty`는 명시적으로 새로 만드는 것이 목적인 명령이다(타입을 처음부터 지정하기에 더 자연스럽다). 이미 있는 값을 실수로 다른 타입으로 덮어쓰지 않으려면, 존재 여부가 불확실할 때 `New-ItemProperty`로 시작하는 편이 의도가 분명하다.

**`Get-Item`으로는 레지스트리 값이 보이지 않는다**: `Get-Item HKLM:\SOFTWARE\ContosoCompany`는 키 자체의 정보만 주고, 그 안에 설정한 값(`NoOfEmployees` 등)은 `Get-ItemProperty`로 별도 조회해야 나타난다. 이 구분을 모르면 "분명히 값을 저장했는데 안 보인다"는 혼란에 빠지기 쉽다.

**레지스트리 값 타입을 지정하지 않으면 기본이 문자열(String)이다**: 숫자로 저장해야 하는 값을 `-Type`을 지정하지 않고 `Set-ItemProperty`로 새로 만들면 REG_SZ(문자열)로 저장되어, 그 값을 읽는 다른 프로그램이 숫자를 기대할 경우 오작동할 수 있다. 새 레지스트리 값을 만들 때는 `-Type DWord`처럼 명시하는 습관이 안전하다.

**이식성**: CMD의 `reg add`/`reg query`, Bash에는 대응하는 표준 개념이 없다(레지스트리 자체가 Windows 고유 개념). 파일 속성 조회·설정 측면에서는 CMD의 `attrib`이 `Get-ItemProperty`/`Set-ItemProperty`의 아주 좁은 부분집합에 대응한다.

## Reference

- [Get-ItemProperty (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itemproperty)
- [Set-ItemProperty (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-itemproperty)
