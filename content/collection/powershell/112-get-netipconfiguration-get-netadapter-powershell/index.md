---
draft: true
collection_order: 112
slug: get-netipconfiguration-get-netadapter-powershell
title: "[PowerShell] 112. Get-NetIPConfiguration/Get-NetAdapter"
date: 2026-08-29
lastmod: 2026-08-29
description: "네트워크 인터페이스의 IP·게이트웨이·DNS 설정을 요약해 주는 Get-NetIPConfiguration과 어댑터 하드웨어 상태(링크 속도, MAC 주소, 연결 상태)를 보여주는 Get-NetAdapter의 역할 차이를 층위별로 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Network(네트워크)
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
- Get-NetIPConfiguration
- Get-NetAdapter
- Network-Interface
- IP-Configuration
- Ipconfig
- Network-Configuration
image: "wordcloud.png"
---

## 개요

<strong>Get-NetIPConfiguration</strong>과 <strong>Get-NetAdapter</strong>는 둘 다 "이 컴퓨터의 네트워크는 지금 어떤 상태인가"를 보여주지만, 서로 다른 층위를 다루는 상호 보완적인 cmdlet이다. 109–111장이 다른 컴퓨터·이름과의 연결성을 진단했다면, 이 장은 진단의 출발점인 "로컬 컴퓨터 자체의 네트워크 구성"으로 시선을 돌린다.

정신 모델은 "`Get-NetIPConfiguration`이 네트워크 층(IP 주소, 게이트웨이, DNS 서버)을 요약해 주는 것이라면, `Get-NetAdapter`는 그보다 한 단계 아래인 링크 층(물리적 어댑터 자체의 이름, 상태, 속도, MAC 주소)을 보여준다"는 것이다. 전통적인 `ipconfig`가 이 두 정보를 한 화면에 섞어 보여줬다면, PowerShell은 이를 역할이 분명한 두 개의 cmdlet으로 나눠 각각 필요한 정보만 정확히 조회할 수 있게 한다.

## 사용법

```powershell
Get-NetIPConfiguration [-InterfaceAlias <이름>] [-Detailed]
Get-NetAdapter [-Name <이름>] [-Physical]
```

## 종류

| cmdlet | 다루는 층위 | 주요 반환 속성 |
|---|---|---|
| `Get-NetIPConfiguration` | 네트워크(IP) 층 | `InterfaceAlias`, `IPv4Address`, `IPv4DefaultGateway`, `DNSServer` |
| `Get-NetAdapter` | 링크(하드웨어) 층 | `Name`, `Status`, `LinkSpeed`, `MacAddress`, `InterfaceDescription` |

| 주요 매개변수 | 대상 cmdlet | 의미 |
|---|---|---|
| `-All` | `Get-NetIPConfiguration` | 가상·루프백·연결 끊김 인터페이스까지 전부 포함(기본은 활성 인터페이스만) |
| `-Detailed` | `Get-NetIPConfiguration` | 컴퓨터 이름, MTU, DHCP 상태 등 추가 정보 포함 |
| `-Physical` | `Get-NetAdapter` | 가상 어댑터를 제외하고 물리 어댑터만 조회 |
| `-IncludeHidden` | `Get-NetAdapter` | 숨겨진 어댑터까지 포함 |

## 예시

```powershell
Get-NetIPConfiguration                                          # 활성 인터페이스의 IP 구성 요약(97장 Get-ComputerInfo와 함께 초기 점검에 유용)

Get-NetIPConfiguration -Detailed                                  # 컴퓨터 이름, MAC, MTU, DHCP 상태까지 포함한 상세 정보

Get-NetIPConfiguration -InterfaceIndex 12                          # 특정 인터페이스 인덱스로 조회

Get-NetIPConfiguration | Get-NetIPAddress                          # 파이프라인으로 이어 프리픽스 길이까지 포함한 상세 IP 주소 확인

Get-NetAdapter -Name *                                              # 모든 가시적 어댑터의 이름·상태·링크 속도 확인

Get-NetAdapter -Physical                                            # 가상 어댑터(VPN, Hyper-V 등)를 제외한 물리 NIC만 조회

Get-NetAdapter -Name "Ethernet" | Format-List -Property *            # 특정 어댑터의 모든 속성 상세 조회

Get-NetAdapter | Where-Object Status -eq "Up"                       # 12장 방식으로 현재 연결된 어댑터만 필터링
```

## 주의사항·함정

**두 cmdlet 모두 Windows 전용이며 NetTCPIP/NetAdapter 모듈에 속한다**: 110–111장의 Windows 전용 cmdlet들과 마찬가지로 macOS/Linux pwsh에서는 사용할 수 없다. 크로스플랫폼 환경에서 인터페이스 정보가 필요하면 `Get-NetIPAddress`류 대신 `.NET`의 `System.Net.NetworkInformation.NetworkInterface` 클래스를 직접 활용해야 한다.

**`Get-NetIPConfiguration`은 기본적으로 "연결된" 인터페이스만 보여준다**: 연결이 끊긴 어댑터나 비활성 가상 인터페이스는 기본 출력에 나타나지 않는다. 문제가 있는 인터페이스까지 모두 살펴보려면 `-All` 매개변수를 명시적으로 추가해야 한다 — 이를 놓치면 "왜 이 어댑터가 안 보이지"라는 혼란으로 이어진다.

**`Get-NetAdapter`의 기본 출력(`Format-Table`)에는 일부 속성만 표시된다**: `MacAddress`나 `DriverVersion` 같은 세부 정보는 기본 테이블 뷰에 나오지 않으므로, `Format-List -Property *`나 `Format-Table -View Driver`처럼 명시적으로 뷰를 바꿔야 확인할 수 있다. 필요한 속성이 안 보인다고 해서 그 값이 없는 것은 아니다.

**어댑터 이름(`Name`)은 컴퓨터마다 다를 수 있어 하드코딩하면 이식성이 떨어진다**: "Ethernet"이라는 이름은 흔하지만 보장된 것이 아니며, 다중 NIC 환경이나 가상 머신에서는 "Ethernet 2", "vEthernet (External)"처럼 달라진다. 스크립트에서는 `-Physical`이나 `Where-Object Status -eq "Up"`처럼 이름이 아닌 속성 기반으로 대상을 특정하는 편이 안전하다.

**이식성**: 전통적인 `ipconfig /all`(Windows)이나 `ip addr`(Linux)은 IP 구성과 인터페이스 상태를 한 화면에 텍스트로 섞어 보여주지만, `Get-NetIPConfiguration`/`Get-NetAdapter` 조합은 이를 층위별 객체로 분리해 파이프라인으로 다시 조합할 수 있게 한다. `Get-NetIPConfiguration | Get-NetIPAddress`처럼 두 cmdlet을 파이프로 잇는 패턴은 CMD·Bash의 단일 명령 출력 파싱 방식과 근본적으로 다른 PowerShell 특유의 접근이다.

## Reference

- [Get-NetIPConfiguration (NetTCPIP) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netipconfiguration?view=windowsserver2025-ps)
- [Get-NetAdapter (NetAdapter) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapter?view=windowsserver2025-ps)
