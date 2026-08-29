---
draft: true
collection_order: 92
slug: scheduledtasks-module-register-task-powershell
title: "[PowerShell] 92. ScheduledTasks 모듈 — 예약 작업 등록"
date: 2026-08-29
lastmod: 2026-08-29
description: "ScheduledTasks 모듈로 New-ScheduledTaskAction/New-ScheduledTaskTrigger를 조합해 예약 작업을 정의하고 Register-ScheduledTask로 등록하는 전체 흐름과 Get-ScheduledTask 관리법을 정리한 챕터다."
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
- ScheduledTasks
- Register-ScheduledTask
- Task-Scheduler
- ScheduledTaskTrigger
- ScheduledTaskAction
- Task-Automation
image: "wordcloud.png"
---

## 개요

**ScheduledTasks** 모듈은 Windows 작업 스케줄러(Task Scheduler)를 cmdlet으로 다루게 해 준다. 89–91장이 "지금 실행 중인 것"을 관리했다면, 이 장은 "미래의 특정 시점(또는 주기적으로) 무엇을 실행할지"를 등록하는 법을 다룬다. 78장에서 배운 `Start-Job`이 현재 세션이 살아 있는 동안만 유효한 백그라운드 작업이었다면, 예약 작업은 세션·재부팅과 무관하게 시스템 자체에 등록되어 지속된다는 점이 근본적으로 다르다.

정신 모델은 "예약 작업은 **동작(Action)**·**트리거(Trigger)**·**설정(Settings)** 세 부품을 조립해 만드는 조립품"이라는 것이다. 동작은 "무엇을 실행할지", 트리거는 "언제 실행할지"를 정의하고, `Register-ScheduledTask`가 이 부품들을 하나의 작업으로 등록한다.

## 사용법

```powershell
$Action  = New-ScheduledTaskAction -Execute <실행파일> [-Argument <인자>]
$Trigger = New-ScheduledTaskTrigger -At <시각> [-Daily | -Once]
Register-ScheduledTask -TaskName <이름> -Action $Action -Trigger $Trigger -User <계정>
```

## 종류

| cmdlet | 역할 |
|---|---|
| `New-ScheduledTaskAction` | "무엇을 실행할지"(`-Execute`) 정의 |
| `New-ScheduledTaskTrigger` | "언제 실행할지"(`-At`, `-Daily`, `-Once`, `-AtLogOn` 등) 정의 |
| `New-ScheduledTaskSettingsSet` | 유휴 시에만 실행, 배터리 사용 시 중단 등 부가 설정 |
| `Register-ScheduledTask` | 위 부품들을 조합해 작업 스케줄러에 실제로 등록(최대 32개 동작, 48개 트리거까지 조합 가능) |
| `Get-ScheduledTask` | 등록된 예약 작업 조회 |
| `Start-ScheduledTask` / `Stop-ScheduledTask` | 트리거를 기다리지 않고 즉시 수동 실행·중단 |
| `Unregister-ScheduledTask` | 등록 해제(삭제) |

## 예시

```powershell
$Time = New-ScheduledTaskTrigger -At 12:00 -Once             # 한 번, 정오에
$User = "Contoso\Administrator"
$PS   = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Scripts\Backup.ps1"
Register-ScheduledTask -TaskName "SoftwareScan" -Trigger $Time -User $User -Action $PS

$Daily = New-ScheduledTaskTrigger -Daily -At "03:00"           # 매일 새벽 3시
Register-ScheduledTask -TaskName "DailyCleanup" -Trigger $Daily -Action $PS -User "SYSTEM"

Get-ScheduledTask -TaskName "SoftwareScan" | Get-ScheduledTaskInfo   # 마지막 실행 결과·다음 실행 예정 확인

Start-ScheduledTask -TaskName "SoftwareScan"                     # 트리거 기다리지 않고 즉시 실행

Get-ScheduledTask | Where-Object State -eq "Ready" |                # 12장 Where-Object로 조회
    Select-Object TaskName, State

Unregister-ScheduledTask -TaskName "SoftwareScan" -Confirm:$false   # 등록 해제
```

## 주의사항·함정

**`-User`에 지정하는 계정이 잘못되면 트리거가 와도 조용히 실패한다**: 예약 작업은 등록 시 지정한 사용자 컨텍스트에서 실행되는데, 그 계정이 로그오프 상태거나 암호가 만료됐다면 화면에 아무 오류도 표시되지 않고 그냥 실행되지 않는다. `Get-ScheduledTaskInfo`의 `LastTaskResult` 속성으로 마지막 실행이 실제로 성공했는지 반드시 확인하는 습관이 필요하다 — `NT AUTHORITY\SYSTEM` 같은 잘 알려진 시스템 계정은 암호가 필요 없어 이런 문제에서 자유롭다.

**등록만 하고 실제 트리거 조건을 검증하지 않으면 "예약이 걸렸다고 착각"하기 쉽다**: `Register-ScheduledTask`가 성공적으로 반환됐다고 해서 트리거 시각·조건이 의도한 대로 정확히 설정됐다는 보장은 아니다. `New-ScheduledTaskTrigger`의 매개변수 조합(`-Daily`와 `-At`을 함께 쓰는 식)을 정확히 맞추지 않으면 예상과 다른 주기로 실행될 수 있으므로, 등록 후 `Get-ScheduledTask | Get-ScheduledTaskInfo`로 다음 실행 예정 시각을 반드시 재확인해야 한다.

**PowerShell 스크립트를 실행하는 작업이라면 실행 정책(53장)이 여전히 적용된다**: 예약 작업의 동작이 `powershell.exe -File script.ps1` 형태라면, 그 스크립트를 실행할 때도 05장에서 다룬 실행 정책이 그대로 적용된다. 예약 작업이 실행되지 않는 흔한 원인 중 하나가 `-ExecutionPolicy Bypass` 인자를 빠뜨린 것이다.

**작업을 삭제(`Unregister-ScheduledTask`)할 때 확인 프롬프트를 놓치기 쉽다**: 이 cmdlet은 기본적으로 확인을 요구하므로, 자동화 스크립트 안에서는 `-Confirm:$false`를 명시하지 않으면 스크립트가 프롬프트에서 멈춘다.

**이식성**: Linux/macOS의 `cron`(주기 작업)과 `at`(일회성 작업)이 개념적으로 대응한다. `crontab -e`가 텍스트 한 줄로 트리거를 표현하는 것과 달리, ScheduledTasks 모듈은 동작·트리거·설정을 각각 별도 객체로 만들어 조합하는 더 구조화된 접근을 취한다. CMD의 `schtasks` 명령도 같은 작업 스케줄러를 다루지만, 텍스트 기반 옵션이라 PowerShell cmdlet만큼 객체를 재사용하며 조합하기는 어렵다.

## Reference

- [Register-ScheduledTask (ScheduledTasks) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask)
