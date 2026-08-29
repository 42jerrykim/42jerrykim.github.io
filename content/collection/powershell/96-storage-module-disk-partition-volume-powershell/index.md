---
draft: true
collection_order: 96
slug: storage-module-disk-partition-volume-powershell
title: "[PowerShell] 96. Storage 모듈 — Get-Disk/Get-Partition/Get-Volume"
date: 2026-08-29
lastmod: 2026-08-29
description: "Storage 모듈이 물리 디스크(Get-Disk)·파티션(Get-Partition)·볼륨(Get-Volume) 세 계층을 어떻게 나눠 표현하는지와 각 cmdlet의 조회 방법, 94장 CIM/WMI와의 관계를 정리한 Part 13 시작 챕터다."
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
- Storage-Module
- Get-Disk
- Get-Partition
- Get-Volume
- Disk-Management
- Physical-Disk
image: "wordcloud.png"
---

## 개요

**Storage** 모듈은 물리 디스크부터 사용자가 실제로 보는 드라이브 문자까지, 스토리지를 세 계층으로 나눠 다루는 cmdlet 묶음이다. 89–95장이 프로세스·서비스·이벤트 로그 같은 "실행되는 것"을 다뤘다면, 이 장부터는 "저장되는 공간" 자체로 시선을 옮기며 Part 13(스토리지와 시스템 구성)을 시작한다. `Get-CimInstance`(94장)로도 디스크 정보를 조회할 수 있지만, Storage 모듈은 그 위에 더 다루기 쉬운 전용 cmdlet 계층을 얹어 둔 것이다.

정신 모델은 "물리 **디스크**(Disk) 위에 하나 이상의 **파티션**(Partition)이 있고, 각 파티션 위에 사람이 실제로 쓰는 **볼륨**(Volume, 드라이브 문자나 마운트 지점)이 있다"는 3단 계층 구조다. `Get-ChildItem`으로 파일을 다루기 전에, 이 계층이 그 파일들이 놓일 물리적 토대라는 점을 이해하는 것이 이 장의 핵심이다.

## 사용법

```powershell
Get-Disk [[-Number] <UInt32[]>]
Get-Partition [-DiskNumber <UInt32>]
Get-Volume [-DriveLetter <Char[]>]
```

## 종류

| cmdlet | 대상 | 대표 속성 |
|---|---|---|
| `Get-Disk` | 물리 디스크(기본 디스크만, 동적 디스크는 제외) | `Number`, `FriendlyName`, `OperationalStatus`, `PartitionStyle`, `BusType` |
| `Get-Partition` | 디스크 위의 파티션 | `DiskNumber`, `PartitionNumber`, `DriveLetter`, `Size` |
| `Get-Volume` | 포맷된 볼륨(드라이브 문자·마운트 지점) | `DriveLetter`, `FileSystem`, `SizeRemaining`, `HealthStatus` |
| `-CimSession` | 세 cmdlet 모두 94장의 CIM 세션으로 원격 조회 가능 |

## 예시

```powershell
Get-Disk                                                    # 모든 물리 디스크
Get-Disk -Number 0                                             # 0번 디스크만

Get-Disk | Where-Object BusType -eq "USB"                        # 12장 Where-Object로 USB 디스크만

Get-Disk | Get-Partition                                           # 각 디스크의 파티션(30장 프로바이더 개념과 유사한 계층 탐색)
Get-Partition -DiskNumber 0 | Where-Object Type -ne "Reserved"       # 예약 영역 제외

Get-Volume                                                            # 모든 볼륨
Get-Volume -DriveLetter C                                               # C 드라이브만

Get-Volume | Where-Object { $_.SizeRemaining / $_.Size -lt 0.1 } |         # 남은 공간 10% 미만
    Select-Object DriveLetter, FileSystemLabel, SizeRemaining

Get-Disk | Get-Partition | Get-Volume                                    # 디스크 → 파티션 → 볼륨 순서대로 파이프라인 연결

Get-Disk | Where-Object -FilterScript { $_.Bustype -Eq "iSCSI" } |          # iSCSI 디스크의 세션 정보까지 조회
    Get-IscsiSession | Format-Table
```

## 주의사항·함정

**`Get-Disk`는 동적 디스크(dynamic disk)를 반환하지 않는다**: 여러 물리 매체에 걸쳐 있을 수 있는 동적 디스크는 이 cmdlet의 대상이 아니며, 기본 디스크(basic disk)와 파티션된 드라이브만 조회된다. 동적 디스크를 쓰는 환경(RAID 소프트웨어 구성 등)이라면 예상한 디스크가 목록에서 빠져 있을 수 있다.

**세 cmdlet의 관계를 모르면 원하는 정보를 엉뚱한 곳에서 찾게 된다**: "이 드라이브가 어떤 물리 디스크에 있는가"를 알고 싶다면 `Get-Volume`이 아니라 `Get-Partition`의 `DiskNumber` 속성을 봐야 하고, "이 디스크에 파일 시스템이 몇 개 포맷돼 있는가"를 알고 싶다면 `Get-Disk`가 아니라 `Get-Volume`을 봐야 한다. 세 계층의 역할을 먼저 명확히 구분해야 어떤 cmdlet에서 원하는 속성을 찾을지 헤매지 않는다.

**클러스터 환경에서는 이 cmdlet들이 클러스터 전체를 대상으로 동작한다**: Failover Cluster에서 Storage 모듈 cmdlet을 실행하면 로컬 컴퓨터가 아니라 클러스터에 속한 모든 서버를 대상으로 결과가 반환된다 — 단일 서버로 범위를 좁히려면 별도의 매개변수나 필터링이 필요하다.

**친숙한 이름(FriendlyName)에 뒤에 공백이 붙어 있을 수 있다**: 일부 디스크는 표시 이름 끝에 공백 문자가 포함돼 있어, `Get-Disk -FriendlyName "MyDisk"`처럼 정확히 일치하는 이름으로 찾으면 실패할 수 있다. 이럴 때는 `Get-Disk -FriendlyName "MyDisk*"`처럼 끝에 와일드카드를 붙이는 것이 안전하다.

**이식성**: Linux의 `lsblk`(블록 장치 트리), `fdisk -l`(디스크·파티션), `df -h`(볼륨·마운트 지점)가 각각 이 세 계층에 대응한다 — Linux는 이 세 정보를 서로 다른 명령으로 나눠 보여주는 반면, PowerShell은 파이프라인으로 세 cmdlet을 자연스럽게 연결해 계층을 그대로 따라 탐색할 수 있다는 점이 다르다. CMD의 `diskpart`도 유사한 정보를 다루지만 대화형 셸 안에서 명령을 입력하는 방식이라 스크립팅에는 덜 적합하다.

## Reference

- [Get-Disk (Storage) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/storage/get-disk)
