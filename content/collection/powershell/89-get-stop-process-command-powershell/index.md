---
draft: false
collection_order: 89
slug: get-stop-process-command-powershell
title: "[PowerShell] 89. Get-Process/Stop-Process — 프로세스 관리"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Process가 반환하는 Process 객체의 NPM/PM/WS/CPU 등 기본 표시 열의 의미와 -IncludeUserName으로 소유자를 확인하는 법, Stop-Process -Force로 강제 종료하는 법을 정리한 Part 12 시작 챕터다."
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
- Get-Process
- Stop-Process
- Process-Management
- WorkingSet
- Task-Manager
- Process-Id
image: "wordcloud.png"
---

## 개요

`Get-Process`/`Stop-Process`는 현재 컴퓨터에서 실행 중인 프로세스를 조회하고 종료하는 cmdlet으로, GUI의 작업 관리자를 명령줄로 옮겨온 것과 같다. Part 11(원격 관리)에서 다른 컴퓨터를 다루는 법을 배웠다면, 이 장부터는 다시 로컬 컴퓨터로 돌아와 시스템 자체를 들여다보는 Part 12(프로세스·서비스·예약 작업)를 시작한다. `Get-Process`가 반환하는 것은 `.NET`의 `System.Diagnostics.Process` 객체 그대로라, 10장에서 강조한 객체 파이프라인의 힘을 시스템 관리에도 그대로 적용할 수 있다.

정신 모델은 "각 프로세스는 이름·ID·메모리 사용량 같은 속성과, 종료 같은 동작(메서드)을 함께 가진 객체"라는 것이다. `Stop-Process`는 사실 이 객체의 `.Kill()` 메서드를 cmdlet 형태로 감싼 것에 가깝다.

## 사용법

```powershell
Get-Process [[-Name] <String[]>] [-Id <Int32[]>] [-IncludeUserName]
Stop-Process [-Id] <Int32[]> [-Force]
```

## 종류

| 매개변수/속성 | 설명 |
|---|---|
| `-Name` | 프로세스 이름으로 조회(와일드카드 지원) |
| `-Id` | 정확한 프로세스 ID(PID)로 조회, `$PID`는 현재 세션 자체의 PID |
| `-IncludeUserName` | 프로세스 소유자를 `UserName` 속성으로 추가(관리자 권한 필요할 수 있음) |
| `-Module` / `-FileVersionInfo` | 프로세스가 로드한 모듈, 실행 파일의 버전 정보 조회(반환 타입이 `Process`가 아니게 됨) |
| 기본 표시 열 | `NPM(K)`(비페이징 메모리), `PM(M)`(페이징 메모리), `WS(M)`(작업 집합), `CPU(s)`, `Id`, `ProcessName` |

## 예시

```powershell
Get-Process                                            # 모든 프로세스
Get-Process winword, explorer | Format-List *             # 특정 이름의 모든 속성

Get-Process | Where-Object WorkingSet -gt 20MB              # 12장 Where-Object로 메모리 많이 쓰는 것만
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5   # 19장/13장 조합으로 CPU 상위 5개

Get-Process -Name pwsh -IncludeUserName                       # 소유자 확인
Get-Process -Id $PID                                            # 현재 세션 자체의 프로세스

Stop-Process -Name notepad                                       # 이름으로 종료(정상 종료 시도)
Stop-Process -Id 1234 -Force                                       # 응답 없는 프로세스 강제 종료
Get-Process notepad | Stop-Process                                   # 파이프라인으로 종료

Get-Process | Where-Object -Property MainWindowTitle |                # 창이 있는 프로세스만
    Format-Table Id, Name, MainWindowTitle -AutoSize
```

## 주의사항·함정

**기본 표시 값은 바이트가 아니라 KB/MB 단위로 반올림된 것이다**: 화면에 보이는 `NPM(K)`, `WS(M)` 열은 사람이 읽기 좋게 단위를 바꾼 값이라, 점 표기법(`.`)으로 실제 속성값(`$proc.WorkingSet`)에 접근하면 항상 바이트 단위의 원래 숫자가 나온다. 정확한 계산이 필요하다면 화면 표시가 아니라 속성값을 직접 참조해야 한다.

**`-Module`이나 `-FileVersionInfo`를 쓰면 결과가 더 이상 `Process` 객체가 아니다**: 이 매개변수들은 각각 `ProcessModule`, `FileVersionInfo` 타입을 반환하므로, 그 결과를 곧바로 `Stop-Process`에 파이프하면 실패한다 — 종료하려는 프로세스 객체가 필요하다면 별도로 다시 `Get-Process`를 호출해야 한다.

**`Stop-Process`는 기본적으로 확인 없이 즉시 종료를 시도하며, 저장하지 않은 데이터는 사라질 수 있다**: 26장에서 배운 `-WhatIf`/`-Confirm`으로 실행 전 미리 확인하는 습관이 특히 이 cmdlet에서 중요하다 — 잘못된 PID를 지정하면 사용자가 작업 중이던 다른 프로그램이 예고 없이 종료될 수 있다.

**다른 사용자가 소유한 프로세스를 종료하려면 관리자 권한이 필요하다**: 일반 사용자 권한으로 다른 계정 소유의 프로세스에 `Stop-Process`를 시도하면 접근 거부 오류가 난다. `-IncludeUserName`으로 소유자를 먼저 확인하는 습관이 이런 실패를 예측하는 데 도움이 된다.

**이식성**: Bash의 `ps`(조회)와 `kill`(종료), CMD의 `tasklist`/`taskkill`이 각각 대응한다. `kill -9`가 `Stop-Process -Force`와 같은 "강제 종료" 개념이다. PowerShell의 차이는 조회 결과가 텍스트 표가 아니라 `Sort-Object`·`Where-Object`로 즉시 재가공할 수 있는 객체 컬렉션이라는 점이다.

## Reference

- [Get-Process (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process)
