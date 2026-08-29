---
draft: true
collection_order: 94
slug: get-ciminstance-get-wmiobject-powershell
title: "[PowerShell] 94. Get-CimInstance/Get-WmiObject — CIM/WMI 조회"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-CimInstance로 WMI 클래스를 조회하는 법과 -ClassName/-Filter 매개변수, WSMan 프로토콜 기반 CIM cmdlet이 레거시 DCOM 기반 Get-WmiObject를 대체하는 이유, -CimSession으로 원격 조회하는 법을 정리한 챕터다."
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
- Get-CimInstance
- Get-WmiObject
- WMI
- CIM
- CimSession
- WQL-Query
image: "wordcloud.png"
---

## 개요

`Get-CimInstance`는 **WMI**(Windows Management Instrumentation)가 관리하는 시스템 정보를 CIM(Common Information Model) 표준을 통해 조회하는 cmdlet이다. 89장의 `Get-Process`, 91장의 `Get-Service`가 각각 프로세스·서비스라는 좁은 영역을 다뤘다면, `Get-CimInstance`는 컴퓨터 하드웨어부터 운영체제 설정까지 WMI가 노출하는 수백 개의 **클래스** 전체에 접근하는 훨씬 넓은 창구다.

정신 모델은 "WMI는 시스템의 거의 모든 것을 클래스와 인스턴스로 모델링해 둔 거대한 데이터베이스이고, `Get-CimInstance`는 그 데이터베이스에 SQL과 비슷한 쿼리(WQL)를 던지는 도구"라는 것이다. `Get-WmiObject`는 이 개념의 더 오래된 구현체로, 전송 프로토콜(DCOM)만 다를 뿐 같은 WMI 데이터를 대상으로 한다.

## 사용법

```powershell
Get-CimInstance -ClassName <클래스이름> [-Filter <조건식>]
Get-CimInstance -ComputerName <컴퓨터이름> -ClassName <클래스이름>
```

## 종류

| 요소 | 설명 |
|---|---|
| `-ClassName` | 조회할 WMI 클래스(예: `Win32_Process`, `Win32_ComputerSystem`, `Win32_LogicalDisk`) |
| `-Filter` | `WHERE` 키워드 없이 조건식만 지정(WQL 문법) |
| `-Query` | WQL/CQL 쿼리 문 전체를 직접 작성 |
| `-Property` | 필요한 속성만 선택해 네트워크 트래픽 절감 |
| `-CimSession` | 84–86장에서 배운 지속 세션과 유사하게, 여러 CIM 조회에 재사용할 연결 |
| `Get-WmiObject`(레거시) | DCOM 기반, PowerShell 7(크로스플랫폼)에서는 지원되지 않음 |

## 예시

```powershell
Get-CimInstance -ClassName Win32_Process                       # 프로세스 정보(89장 Get-Process의 WMI 버전)
Get-CimInstance -ClassName Win32_OperatingSystem                 # 운영체제 정보
Get-CimInstance -ClassName Win32_LogicalDisk                       # 논리 디스크(13부에서 스토리지와 함께 재등장)

Get-CimInstance -ClassName Win32_Process -Filter "Name like 'P%'"    # WQL 필터 — WHERE 없이 조건만
Get-CimInstance -Query "SELECT * from Win32_Process WHERE name LIKE 'P%'"   # 전체 쿼리 직접 작성

Get-CimInstance -ClassName Win32_Process -Property Name, KernelModeTime   # 필요한 속성만 선택

$s = New-CimSession -ComputerName Server01, Server02              # CIM 세션(86장 New-PSSession과 유사한 개념)
Get-CimInstance -ClassName Win32_ComputerSystem -CimSession $s       # 세션 재사용
Get-CimInstance -ClassName Win32_ComputerSystem -ComputerName Server01, Server02   # 세션 없이 임시 연결

$proc = Get-CimInstance -Class Win32_Process -Filter "name='pwsh.exe'"
$proc | Invoke-CimMethod -MethodName GetOwner                        # 프로세스 소유자 조회(메서드 호출)
```

## 주의사항·함정

**`Get-WmiObject`는 PowerShell 7(크로스플랫폼)에서 아예 지원되지 않는다**: WMI 자체가 DCOM이라는 Windows 전용 프로토콜에 의존하는데, `Get-CimInstance`는 WSMan(83장에서 배운 그 WinRM 프로토콜)을 통해 같은 데이터에 접근하도록 재설계됐다. Windows PowerShell 5.1에서 작성된 `Get-WmiObject` 기반 스크립트를 PowerShell 7로 이전한다면, `Get-CimInstance`로 바꾸는 것이 사실상 필수다.

**`-Filter`의 조건식은 WQL 문법이지, PowerShell의 비교 연산자(20장)가 아니다**: `-Filter "Name like 'P%'"`처럼 SQL과 비슷한 `like`, 퍼센트 와일드카드(`%`)를 쓰며, PowerShell의 `-eq`/`-like` 연산자와는 문법이 다르다. 이 차이를 모르고 PowerShell 연산자를 그대로 쓰면 조용히 잘못된 결과나 오류로 이어진다.

**여러 번 조회할 계획이라면 `-ComputerName`보다 `-CimSession`이 효율적이다**: 85–86장에서 `-ComputerName`(임시 연결)과 `-Session`(지속 연결)의 성능 차이를 다뤘던 것과 같은 원리가 여기도 적용된다 — `-ComputerName`은 매번 새 연결을 만들고 끊으므로, 같은 컴퓨터에 여러 번 CIM 쿼리를 보낸다면 `New-CimSession`으로 세션을 먼저 만들어 재사용하는 편이 빠르다.

**클래스 이름과 네임스페이스를 모르면 원하는 정보를 찾기 어렵다**: WMI는 수백 개의 클래스로 나뉘어 있고 기본 네임스페이스(`root/CIMV2`)를 벗어난 정보는 `-Namespace`를 명시해야 조회된다. `Get-CimClass`로 사용 가능한 클래스 목록을 먼저 탐색하는 것이 낯선 정보를 찾는 첫걸음이다.

**이식성**: Linux의 `dmidecode`(하드웨어 정보), `/proc` 파일 시스템이 부분적으로 유사한 역할을 하지만, WMI처럼 통일된 쿼리 언어로 수백 개 영역을 일관되게 조회하는 단일 인터페이스는 아니다. WMI/CIM은 DMTF(Distributed Management Task Force)의 CIM 표준을 구현한 것으로, 이론적으로는 다른 플랫폼의 CIM 구현체와도 같은 쿼리 언어(WQL 계열)로 상호 운용될 수 있도록 설계됐다.

## Reference

- [Get-CimInstance (CimCmdlets) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance)
