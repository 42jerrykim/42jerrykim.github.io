---
draft: false
collection_order: 91
slug: get-start-stop-restart-service-powershell
title: "[PowerShell] 91. Get-Service와 서비스 시작/중지/재시작"
date: 2026-08-29
lastmod: 2026-08-29
description: "Windows 서비스를 조회·시작·중지·재시작하는 Get-Service/Start-Service/Stop-Service/Restart-Service 사용법과 Status 속성값, -DependentServices/-RequiredServices로 서비스 의존 관계를 확인하는 법을 정리한 챕터다."
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
- Get-Service
- Start-Service
- Stop-Service
- Restart-Service
- Service-Dependency
- Windows-Service
image: "wordcloud.png"
---

## 개요

`Get-Service`/`Start-Service`/`Stop-Service`/`Restart-Service`는 Windows **서비스**(백그라운드에서 상시 실행되는 시스템 구성 요소)를 관리하는 cmdlet 묶음이다. 89장의 `Get-Process`가 다룬 일반 프로세스와 달리, 서비스는 로그온한 사용자가 없어도 시스템 부팅과 함께 자동으로 시작되고, 다른 서비스와 **의존 관계**를 맺는다는 점이 다르다.

정신 모델은 "서비스는 시작·중지 상태를 갖는 프로세스이고, 어떤 서비스는 다른 서비스가 먼저 실행돼 있어야만 시작될 수 있다"는 것이다. 이 의존 관계를 무시하고 서비스를 중지하면 그 서비스에 의존하는 다른 서비스까지 연쇄적으로 중단될 수 있다.

## 사용법

```powershell
Get-Service [[-Name] <String[]>] [-DependentServices] [-RequiredServices]
Start-Service -Name <서비스이름>
Stop-Service -Name <서비스이름> [-Force]
Restart-Service -Name <서비스이름> [-Force]
```

## 종류

| 값/매개변수 | 설명 |
|---|---|
| `Status` 속성 | `Running`/`Stopped`/`Paused` 등 — 내부적으로는 열거형 정수값이라 오름차순 정렬 시 `Stopped`(1)가 `Running`(4)보다 앞에 옴 |
| `-DependentServices` | 이 서비스에 **의존하는** 다른 서비스 목록 |
| `-RequiredServices`(별칭 `-ServicesDependedOn`) | 이 서비스가 **필요로 하는** 다른 서비스 목록 |
| `-Force`(Stop/Restart) | 의존 서비스가 있어도 함께 중지·재시작 |
| `-DisplayName` | 서비스 이름 대신 사람이 읽는 표시 이름으로 조회 |

## 예시

```powershell
Get-Service                                                # 모든 서비스
Get-Service "wmi*"                                            # 이름으로 와일드카드 조회
Get-Service -DisplayName "*network*"                            # 표시 이름으로 조회

Get-Service | Where-Object Status -eq "Running"                   # 12장 Where-Object 응용
Get-Service "s*" | Sort-Object Status                               # Stopped가 Running보다 먼저 나옴(열거형 순서)

Get-Service | Where-Object { $_.DependentServices } |                 # 의존 서비스가 있는 것만
    Format-List Name, DependentServices,
        @{ Label = "개수"; Expression = { $_.DependentServices.Count } }

Get-Service "WinRM" -RequiredServices                                  # WinRM이 필요로 하는 서비스

Start-Service -Name "Spooler"
Stop-Service -Name "Spooler"
Restart-Service -Name "Spooler" -Force                                  # 의존 서비스까지 함께 재시작

"WinRM" | Get-Service | Restart-Service                                   # 파이프라인으로 조회 후 즉시 재시작
```

## 주의사항·함정

**`Status`의 오름차순 정렬 결과가 직관과 반대다**: `Sort-Object Status`로 정렬하면 `Stopped` 서비스가 `Running` 서비스보다 **먼저** 나온다. `Status`는 문자열이 아니라 내부적으로 정수값을 가진 열거형이고, `Stopped`가 1, `Running`이 4이기 때문이다. 실행 중인 서비스를 먼저 보고 싶다면 `Sort-Object Status -Descending`을 써야 한다.

**의존 관계를 무시하고 `-Force` 없이 서비스를 중지하면 오류가 난다**: 다른 서비스가 의존하고 있는 서비스를 그냥 `Stop-Service`로 중지하려 하면, PowerShell이 안전장치로 오류를 낸다. 의존 서비스까지 함께 내려도 괜찮다는 확신이 있을 때만 `-Force`를 써야 한다 — 프로덕션 서버에서는 어떤 서비스가 연쇄적으로 영향받는지 `-DependentServices`로 미리 확인하는 습관이 중요하다.

**PowerShell 6.0부터 `Get-Service`에 `-ComputerName` 매개변수가 사라졌다**: Windows PowerShell 5.1까지는 `Get-Service -ComputerName`으로 원격 서비스를 조회할 수 있었지만, PowerShell 6부터는 이 매개변수가 제거됐다. 원격 컴퓨터의 서비스를 다루려면 85장에서 배운 `Invoke-Command`로 감싸야 한다 — 이는 이 저장소가 반복해서 강조하는 Windows PowerShell/PowerShell 7 버전 차이의 또 다른 구체적 사례다.

**이 cmdlet들은 Windows 전용이다**: `Get-Service` 계열은 Windows의 서비스 제어 관리자(SCM)를 대상으로 하므로 macOS·Linux에서는 사용할 수 없다. 크로스플랫폼 스크립트를 작성한다면 `$IsWindows` 자동 변수로 플랫폼을 먼저 확인해야 한다.

**이식성**: Linux의 `systemctl status`/`start`/`stop`/`restart`(systemd 기반)가 정확히 대응하는 개념이다. `-DependentServices`/`-RequiredServices`는 systemd의 `systemctl list-dependencies`와 유사한 목적을 수행한다. CMD의 `net start`/`net stop`도 서비스를 제어하지만 의존 관계 조회 기능은 제공하지 않는다.

## Reference

- [Get-Service (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service)
