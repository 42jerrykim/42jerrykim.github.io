---
draft: false
collection_order: 97
slug: get-computerinfo-system-summary-powershell
title: "[PowerShell] 97. Get-ComputerInfo — 시스템 정보 종합 조회"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-ComputerInfo 하나로 BIOS·운영체제·하드웨어 정보를 통합 조회하는 법과 -Property 매개변수로 필요한 항목만 골라내는 법, 94장 CIM 조회를 여러 번 조합할 필요 없이 한 번에 요약해 주는 장점을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- System-Management
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
- Get-ComputerInfo
- System-Information
- BIOS
- OS-Version
- Consolidated-Object
- Hardware-Info
image: "wordcloud.png"
---

## 개요

`Get-ComputerInfo`는 BIOS·운영체제·하드웨어 정보를 하나의 통합된 객체로 묶어 반환하는 cmdlet이다. 94장의 `Get-CimInstance`로 같은 정보를 얻으려면 `Win32_BIOS`, `Win32_OperatingSystem`, `Win32_ComputerSystem` 같은 여러 WMI 클래스를 각각 조회해야 하는데, `Get-ComputerInfo`는 Windows PowerShell 5.1부터 이 여러 클래스의 정보를 미리 조합해 하나의 명령으로 제공한다.

정신 모델은 "이 컴퓨터는 도대체 어떤 사양인가?"라는 흔한 질문 하나에 대한 **원스톱 답변**이라는 것이다. 94장에서 배운 개별 CIM 클래스 조회가 "정밀 조사"라면, `Get-ComputerInfo`는 "요약 보고서"에 가깝다.

## 사용법

```powershell
Get-ComputerInfo [[-Property] <String[]>]
```

## 종류

| 속성 그룹 | 예 |
|---|---|
| BIOS 정보 | `BiosBIOSVersion`, `BiosManufacturer`, `BiosSeralNumber` |
| Windows 버전 정보 | `WindowsVersion`, `WindowsBuildLabEx`, `OsVersion` |
| 하드웨어 정보 | `CsProcessors`, `CsTotalPhysicalMemory`, `CsManufacturer` |
| 핫픽스 정보 | `OsHotFixes`(99장에서 다룰 `Get-HotFix`와 유사한 정보를 요약된 형태로 포함) |
| `-Property` | 와일드카드를 지원해 특정 그룹만 골라 조회(예: `"*version"`) |

## 예시

```powershell
Get-ComputerInfo                                          # 전체 정보(속성 100개 이상)

Get-ComputerInfo -Property "*version"                        # 버전 관련 속성만
Get-ComputerInfo -Property "Os*"                                # OS로 시작하는 속성만

Get-ComputerInfo | Select-Object WindowsProductName, OsArchitecture, CsTotalPhysicalMemory   # 13장 응용

$info = Get-ComputerInfo
"{0}, {1}, RAM {2}GB" -f $info.WindowsProductName, $info.OsArchitecture,
    [Math]::Round($info.CsTotalPhysicalMemory / 1GB)          # 45장 -f 서식 연산자로 요약 문자열 생성

Get-ComputerInfo -Property "BiosSeralNumber" | Select-Object -ExpandProperty BiosSeralNumber   # 자산관리 시 자주 쓰는 값

Get-ComputerInfo -Property "Cs*" | Format-List                # 컴퓨터 시스템(Cs 접두사) 정보만 목록으로
```

## 주의사항·함정

**정보량이 매우 많아, 필요한 것만 뽑지 않으면 화면이 압도적으로 길어진다**: `Get-ComputerInfo`는 매개변수 없이 실행하면 100개가 넘는 속성을 한 번에 반환한다. 실무에서는 처음부터 `-Property`로 범위를 좁히거나, 결과를 변수에 담아 13장의 `Select-Object`로 필요한 속성만 다시 골라내는 방식이 훨씬 다루기 쉽다.

**Windows 전용이며 PowerShell 7에서도 macOS/Linux에서는 동작하지 않는다**: 크로스플랫폼 스크립트에서 시스템 정보를 요약해야 한다면, `$IsWindows` 자동 변수로 분기해 Windows에서만 이 cmdlet을 쓰고 다른 플랫폼에서는 별도의 방법(`/proc/cpuinfo` 읽기 등)을 마련해야 한다.

**속성 이름의 접두사가 정보 출처를 암시하지만 완전히 직관적이지는 않다**: `Bios`로 시작하는 속성은 BIOS/펌웨어 정보, `Os`는 운영체제, `Cs`(Computer System)는 하드웨어 관련 정보를 뜻하지만, 이 접두사 규칙을 모르면 원하는 속성을 `Get-Member`(11장)나 `-Property "*"` 와일드카드 탐색 없이 바로 찾기 어렵다.

**일부 환경에서는 실행이 상대적으로 느릴 수 있다**: 내부적으로 여러 WMI 클래스를 조합해 정보를 모으는 과정이 있어, 자주 반복 호출해야 하는 스크립트라면 한 번 호출한 결과를 변수에 저장해 재사용하는 편이 89–95장에서 강조해 온 것처럼 효율적이다.

**이식성**: Linux의 `neofetch`, `hostnamectl`, `lscpu` 같은 도구들을 하나로 합친 것과 비슷한 역할을 한다고 볼 수 있다 — 다만 Linux 생태계는 이 정보들이 여러 전용 명령으로 나뉘어 있는 반면, `Get-ComputerInfo`는 하나의 cmdlet이 구조화된 객체 하나로 이를 통합해 제공한다는 점이 특징이다. CMD의 `systeminfo` 명령도 유사한 목적을 가지지만 텍스트 출력이라 `Select-Object` 같은 후속 가공이 불가능하다.

## Reference

- [Get-ComputerInfo (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-computerinfo)
