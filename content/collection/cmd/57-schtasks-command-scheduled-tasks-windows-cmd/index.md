---
draft: false
slug: schtasks-command-scheduled-tasks-windows-cmd
title: "[CMD] 57. schtasks - 예약 작업 생성과 관리"
description: "schtasks로 특정 시각·조건에 프로그램을 자동 실행하도록 예약하는 법과 스케줄 유형별 필수 옵션, System 계정으로 실행할 때 상호작용이 불가능한 이유, 비밀번호를 검증하지 않아 조용히 실패하는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 570
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Advanced
- schtasks
- 예약작업
- Scheduling
- Automation(자동화)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Configuration(설정)
- Beginner
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

schtasks는 작업 스케줄러에 등록된 예약 작업을 만들고, 조회·실행·수정·삭제하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [56장: sc](/post/cmd/sc-command-manage-windows-services-cmd/)에서 상시 실행되는 서비스를 다룬 뒤 이어진다. sc가 "항상 떠 있는 백그라운드 프로세스"를 다뤘다면, schtasks는 "특정 시각이나 조건에 맞춰 한 번 실행되는 작업"을 다룬다.

**이 장의 깊이**: 고급. 스케줄 유형이 많아 자주 쓰는 유형 위주로 다룬다.

## 사용법

```
schtasks /create /sc <스케줄유형> /tn <작업이름> /tr <실행할프로그램> [/st <시작시간>] [/sd <시작날짜>] [/ru <계정>] [/rp <비밀번호>] [...]
schtasks /query [/fo <형식>] [/v] [/tn <작업이름>]
schtasks /run /tn <작업이름>
schtasks /change /tn <작업이름> ...
schtasks /delete /tn <작업이름> [/f]
```

## 옵션

### 스케줄 유형(`/sc`)

| 값 | 의미 |
|---|---|
| `MINUTE` \| `HOURLY` \| `DAILY` \| `WEEKLY` \| `MONTHLY` | n분·시간·일·주·월마다 반복 |
| `ONCE` | 지정한 날짜·시간에 한 번만 실행 |
| `ONSTART` | 시스템이 시작될 때마다 실행 |
| `ONLOGON` | 아무 사용자든 로그온할 때 실행 |
| `ONIDLE` | 시스템이 지정한 시간(`/i`) 동안 유휴 상태일 때 실행 |
| `ONEVENT` | 시스템 이벤트 로그 조건(`/ec`)과 일치할 때 실행 |

### 자주 쓰는 옵션

| 옵션 | 설명 |
|---|---|
| `/tn <이름>` | 작업 이름(최대 238자, 공백 있으면 따옴표) |
| `/tr <프로그램>` | 실행할 프로그램·스크립트의 전체 경로 |
| `/ru <계정>` | 작업을 실행할 계정(기본은 현재 사용자). `System` 지정 가능 |
| `/rp <비밀번호>` | `/ru` 계정의 비밀번호(System 계정에는 사용하지 않음) |
| `/mo <n>` | 스케줄 유형 안에서의 반복 간격 |
| `/st <시간>` | 시작 시각(HH:mm, 24시간제) |
| `/sd`, `/ed` | 시작·종료 날짜 |
| `/it` | 지정한 실행 계정이 로그온해 있을 때만 실행 |
| `/f` | 이미 같은 이름의 작업이 있어도 경고 없이 덮어씀 |

## 예시

```
schtasks /query
schtasks /create /tn "Security Script" /tr \\central\data\scripts\sec.vbs /sc minute /mo 20
schtasks /create /tn "Daily Backup" /tr "C:\Scripts\backup.bat" /sc daily /st 02:00
schtasks /create /tn MyApp /tr c:\apps\myapp.exe /sc monthly /mo lastday /m *
schtasks /create /tn MyApp /tr c:\apps\myapp.exe /sc weekly /d TUE /ru Admin06
schtasks /create /tn MyApp /tr c:\apps\myapp.exe /sc monthly /d 15 /ru System
schtasks /run /tn "Daily Backup"
schtasks /delete /tn "OldTask" /f
```

"지금 즉시 한 번 실행"에 해당하는 전용 옵션은 없지만, 몇 분 뒤로 시작 시각을 지정한 `ONCE` 스케줄로 같은 효과를 낼 수 있다.

## 주의사항·함정

**System 계정으로 실행한 작업은 사용자와 상호작용할 수 없다**: `/ru System`으로 예약하면 비밀번호 없이도 매우 높은 권한으로 실행되지만, System 계정은 대화형 로그온 권한이 없다.

> "The **System** account doesn't have interactive logon rights. Users can't see or interact with programs or tasks run with system permissions." — Microsoft Learn, "schtasks create"

화면에 창을 띄우거나 사용자 입력을 받는 프로그램을 System 계정으로 예약하면, 프로그램은 실행되지만 아무도 그 창을 볼 수 없는 상태로 백그라운드에 머문다.

**비밀번호나 경로가 틀려도 작업은 "성공적으로 생성"됐다고 나온다**: schtasks는 프로그램 파일 경로나 계정 비밀번호가 올바른지 미리 검증하지 않는다.

> "Schtasks doesn't verify program file locations or user account passwords. If you don't enter the correct file location or the correct password for the user account, the task is created, but it won't run." — Microsoft Learn, "schtasks create"

즉 "SUCCESS: 작업이 생성되었습니다"라는 메시지가 나와도, 실제 예약 시각이 됐을 때 조용히 실패할 수 있다. 작업을 만든 직후에는 `/run`으로 즉시 한 번 실행해보고 `SchedLgU.txt` 로그를 확인하는 습관이 필요하다.

**원격 컴퓨터에 예약하려면 그 컴퓨터의 관리자 권한이 필요하다**: `/s`로 원격 컴퓨터를 지정할 때는 로컬 컴퓨터가 원격 컴퓨터의 도메인과 같거나 신뢰 관계에 있어야 계정을 인증할 수 있다. 이 조건이 만족되지 않으면 작업 항목은 만들어지지만 실제로는 비어 있어 실행되지 않는다 — Microsoft Learn 예시에서도 이런 경고 메시지가 실제로 나타난다.

**PowerShell에서는 `ScheduledTasks` 모듈이 대응한다**: `Register-ScheduledTask`(생성), `Get-ScheduledTask`(조회), `Unregister-ScheduledTask`(삭제), `Start-ScheduledTask`(즉시 실행)로 나뉘어 있어, schtasks 하나가 `/create`·`/query`·`/delete`·`/run` 서브옵션으로 처리하던 일을 별도 cmdlet으로 분리해 다룬다. 트리거·동작·설정을 `New-ScheduledTaskTrigger`·`New-ScheduledTaskAction`처럼 객체로 먼저 만들고 조합하는 방식이라, schtasks의 한 줄짜리 `/sc`·`/mo`·`/st` 옵션 조합보다 코드는 길어지지만 조건을 재사용하거나 프로그래밍적으로 다루기는 더 쉽다.

## 흔한 오개념

<strong>"`/ru`로 다른 사용자 계정을 지정하면 그 사용자에게 로그인 창이나 확인 창이 뜬다"</strong>는 오해가 있다. `/ru`와 `/rp`로 지정한 계정은 작업이 실행될 때 대화형으로 로그인하거나 승인하는 절차 없이, 그 계정 권한으로 완전히 백그라운드에서 조용히 실행된다. 화면에 뭔가 뜨는 프로그램을 예약해도 지정한 사용자가 실제로 로그온해 있지 않으면(또는 `/it` 없이 실행하면) 아무도 그 창을 볼 수 없는 채로 작업만 진행된다 — 이는 앞서 System 계정 예약에서 본 것과 같은 원리다.

## 다음 장에서는

다음은 58장 — 프로그램이나 명령을 새 창에서 실행하는 `start` 명령을 다룬다.

## 평가 기준

- schtasks로 다양한 스케줄 유형(MINUTE, DAILY, WEEKLY, ONSTART 등)의 예약 작업을 만들 수 있다.
- System 계정으로 예약한 작업이 사용자와 상호작용할 수 없는 이유를 설명할 수 있다.
- schtasks가 경로·비밀번호를 미리 검증하지 않아 조용히 실패할 수 있다는 것과, 이를 확인하는 방법을 안다.
- 원격 컴퓨터에 예약할 때 필요한 도메인 신뢰 조건을 설명할 수 있다.

## 참고

- [schtasks create | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
