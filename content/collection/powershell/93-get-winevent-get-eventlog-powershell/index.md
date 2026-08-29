---
draft: true
collection_order: 93
slug: get-winevent-get-eventlog-powershell
title: "[PowerShell] 93. Get-WinEvent/Get-EventLog — 이벤트 로그 조회"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-WinEvent로 Windows 이벤트 로그 채널을 조회하는 법과 -FilterHashtable로 효율적으로 필터링하는 법, 레거시 Get-EventLog와의 차이, -LogName/-ListLog로 로그 목록을 탐색하는 법을 정리한 챕터다."
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
- Get-WinEvent
- Get-EventLog
- Event-Log
- FilterHashtable
- XPath-Query
- System-Log
image: "wordcloud.png"
---

## 개요

`Get-WinEvent`는 Windows 이벤트 로그(고전적인 시스템/애플리케이션 로그부터 최신 이벤트 로그 채널, ETW 추적 파일까지)를 조회하는 cmdlet이다. 89–92장이 "지금 실행 중이거나 예약된 것"을 다뤘다면, 이 장은 시스템에 "이미 기록된 과거의 사건"을 조회하며 문제를 진단하는 법을 다룬다. 레거시 `Get-EventLog`도 여전히 남아 있지만, `Get-WinEvent`가 그 상위 호환으로 도입됐다는 점을 이 장에서 짚는다.

정신 모델은 "이벤트 로그는 시스템이 스스로 남긴 일기장이고, `Get-WinEvent`는 그 일기장 여러 권(로그·채널·파일)을 가로질러 원하는 사건만 찾아내는 검색 도구"라는 것이다.

## 사용법

```powershell
Get-WinEvent -LogName <로그이름들> [-MaxEvents <개수>]
Get-WinEvent -FilterHashtable @{ LogName=<로그>; Id=<이벤트ID>; StartTime=<시작시각> }
```

## 종류

| 방식 | 설명 |
|---|---|
| `-ListLog` | 사용 가능한 로그 이름·레코드 수 목록 조회 |
| `-LogName` | 특정 로그(들)에서 이벤트 조회(와일드카드 지원) |
| `-FilterHashtable` | 44장의 해시테이블로 `LogName`/`Id`/`Level`/`StartTime` 등을 조합해 서버 측에서 효율적으로 필터링 |
| `-FilterXPath` / `-FilterXml` | 더 복잡한 조건이 필요할 때 XPath·XML 쿼리 사용 |
| `-Path` | 저장된 `.evtx`/`.etl` 아카이브 파일에서 조회 |
| `Get-EventLog`(레거시) | 고전 로그(Application, System 등)만 지원, Windows Vista 이후 `Get-WinEvent`로 대체 권장 |

## 예시

```powershell
Get-WinEvent -ListLog *                                        # 사용 가능한 로그 목록
Get-WinEvent -ListLog * | Where-Object RecordCount               # 12장 Where-Object로 내용 있는 로그만

Get-WinEvent -LogName "Windows PowerShell" -MaxEvents 50            # 최신 50개(기본 최신순)

# -FilterHashtable — Where-Object보다 효율적(서버에서 미리 걸러서 가져옴)
$Yesterday = (Get-Date) - (New-TimeSpan -Day 1)
Get-WinEvent -FilterHashtable @{ LogName='Windows PowerShell'; Level=3; StartTime=$Yesterday }

$Date = (Get-Date).AddDays(-2)
Get-WinEvent -FilterHashtable @{ LogName='Application'; StartTime=$Date; Id='1003' }

$Event = Get-WinEvent -LogName 'Windows PowerShell'                 # 통계 확인
$Event | Group-Object -Property Id -NoElement |                       # 16장 Group-Object
    Sort-Object -Property Count -Descending

Get-WinEvent -Path 'C:\Test\Windows PowerShell.evtx'                  # 저장된 아카이브 파일 조회

Get-WinEvent -LogName *PowerShell*, Microsoft-Windows-Kernel-WHEA* |     # 여러 로그 동시 조회
    Group-Object -Property LevelDisplayName, LogName -NoElement
```

## 주의사항·함정

**`-FilterHashtable`이 `Where-Object`로 나중에 거르는 것보다 훨씬 효율적이다**: `Get-WinEvent -LogName X | Where-Object { $_.TimeCreated -ge $Yesterday }`는 로그의 **모든** 이벤트를 일단 다 가져온 뒤에야 필터링하지만, `-FilterHashtable`은 이벤트 로그 서비스 자체가 조건에 맞는 것만 골라 전달한다. 대용량 로그(수만 건 이상)를 다룰 때 이 차이는 체감될 만큼 크다 — 가능하면 항상 `-FilterHashtable`이나 `-FilterXPath`를 `Where-Object`보다 먼저 고려해야 한다.

**Windows API 자체의 제약으로 한 번에 조회할 수 있는 로그 개수가 256개로 제한된다**: 매우 많은 로그를 순회해야 한다면 `Get-WinEvent -ListLog * | ForEach-Object { Get-WinEvent -LogName $_.LogName }`처럼 반복문(15장)으로 하나씩 처리해야 한다.

**관리자 권한 없이 실행하면 일부 로그(보안 로그 등)에 접근할 수 없다**: 이 경우 오류 메시지가 나오더라도 "로그가 없다"는 뜻이 아니라 "권한이 부족하다"는 뜻일 수 있으므로, 예상한 이벤트가 안 나오면 관리자 권한으로 다시 시도해 봐야 한다.

**`Get-EventLog`는 새 이벤트 로그 채널(예: `Microsoft-Windows-PowerShell/Operational`)을 조회하지 못한다**: 레거시 cmdlet은 고전적인 이벤트 로그(Application, System, Security 등)만 지원하며, Windows Vista 이후 도입된 확장 이벤트 채널은 오직 `Get-WinEvent`로만 조회할 수 있다. 새 스크립트를 작성한다면 하위 호환 목적이 아닌 한 `Get-WinEvent`를 기본으로 선택해야 한다.

**이식성**: Linux의 `journalctl`(systemd 저널)이나 `/var/log/syslog`가 개념적으로 대응하지만, 텍스트 로그 파일을 `grep`/`awk`로 직접 파싱해야 하는 경우가 많다. Windows 이벤트 로그는 처음부터 구조화된 이진 형식(`.evtx`)으로 저장되고 `Get-WinEvent`가 이를 즉시 구조화된 객체로 반환한다는 점에서, 47장의 정규식 파싱 없이도 `Id`·`Level`·`TimeCreated` 같은 속성에 바로 접근할 수 있다는 것이 근본적인 차이다.

## Reference

- [Get-WinEvent (Microsoft.PowerShell.Diagnostics) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent)
