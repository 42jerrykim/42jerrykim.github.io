---
draft: true
collection_order: 86
slug: new-pssession-persistent-session-powershell
title: "[PowerShell] 86. New-PSSession — 지속 세션 관리"
date: 2026-08-29
lastmod: 2026-08-29
description: "New-PSSession으로 원격 컴퓨터와의 연결을 여러 명령에 걸쳐 재사용하는 지속 세션을 만드는 법과 Get-PSSession/Remove-PSSession으로 관리하는 법, 85장 -ComputerName 방식과의 상태 유지 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Remoting
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
- New-PSSession
- Persistent-Session
- Get-PSSession
- Remove-PSSession
- Session-Reuse
- Connection-Management
image: "wordcloud.png"
---

## 개요

`New-PSSession`은 원격 컴퓨터와의 연결을 **지속 세션(PSSession)** 객체로 만들어, 여러 명령에 걸쳐 그 연결과 상태를 재사용할 수 있게 해 준다. 85장에서 짚었듯 `Invoke-Command -ComputerName`은 매번 연결을 새로 만들고 끊었는데, 이 장은 그 연결 자체를 변수에 담아 계속 살려 두는 법을 다룬다.

정신 모델은 "지속 세션은 원격 컴퓨터에 열어 둔 채로 유지되는 하나의 작업 공간"이라는 것이다. 이 작업 공간 안에서 만든 변수·임포트한 모듈은 그 세션이 살아 있는 동안 계속 남아 있어, 마치 원격 컴퓨터에 별도의 PowerShell 창을 하나 열어 둔 것과 같다.

## 사용법

```powershell
$세션 = New-PSSession -ComputerName <컴퓨터이름들>
Get-PSSession
Remove-PSSession -Session $세션
```

## 종류

| cmdlet | 역할 |
|---|---|
| `New-PSSession` | 지속 세션 생성, `PSSession` 객체(들) 반환 |
| `Get-PSSession` | 현재 열려 있는 세션 목록·상태 확인 |
| `Remove-PSSession` | 세션을 완전히 닫고 리소스 반환 |
| `Disconnect-PSSession` / `Connect-PSSession` | 세션 연결을 끊었다가(연결 종료 후에도 세션은 원격에 살아있음) 나중에 다시 연결 |
| `Receive-PSSession` | 연결이 끊긴 세션에서 그동안 쌓인 출력을 가져옴 |

## 예시

```powershell
$s = New-PSSession -ComputerName Server01, Server02       # 두 컴퓨터에 지속 세션 생성

Invoke-Command -Session $s -ScriptBlock { $h = Get-HotFix }   # 세션 안에 변수 저장
Invoke-Command -Session $s -ScriptBlock { $h.Count }             # 같은 세션이므로 그대로 재사용 가능

Get-PSSession                                                      # 세션 상태(Opened 등) 확인
Get-PSSession | Where-Object State -ne 'Opened'                      # 끊긴 세션만 찾기(19장 응용)

Enter-PSSession -Session $s[0]                                       # 84장의 대화형 진입에도 재사용 가능

Disconnect-PSSession -Session $s[0]                                    # 연결만 끊고 원격 세션 상태는 유지
Connect-PSSession -ComputerName Server01                                 # 나중에 다시 연결해 이어서 작업
Receive-PSSession -ComputerName Server01 -Id 1                            # 끊긴 동안 쌓인 출력 회수

Remove-PSSession -Session $s                                                # 완전히 정리
Get-PSSession | Remove-PSSession                                              # 남은 세션 일괄 정리
```

## 주의사항·함정

**세션을 다 쓰고 `Remove-PSSession`으로 정리하지 않으면 리소스가 계속 소비된다**: 지속 세션은 원격 컴퓨터에서 실제로 리소스(메모리, 세션 슬롯)를 점유하므로, 스크립트가 끝났는데도 세션을 정리하지 않으면 원격 컴퓨터에 열린 세션이 누적된다. 특히 세션 수 제한(기본 동시 세션 수 제한이 있음)에 걸리면 이후 연결 시도가 실패할 수 있다.

**`Disconnect-PSSession`은 84장의 `Enter-PSSession`이 만든 임시 대화형 세션에는 쓸 수 없다**: 84장에서 짚었듯 연결 끊기·재연결 기능은 오직 `New-PSSession`으로 만든 지속 세션에서만 지원된다. "대화형으로 접속했다가 나중에 다시 이어서 하고 싶다"는 요구가 있다면 처음부터 `New-PSSession`으로 세션을 만들고, 그 세션에 `Enter-PSSession -Session`으로 진입하는 방식을 써야 한다.

**세션이 여러 개면 `Invoke-Command -Session`은 전부에 명령을 보낸다**: `New-PSSession -ComputerName Server01, Server02`로 배열 형태의 세션을 만들면, 이후 `-Session $s`로 넘기는 모든 `Invoke-Command`는 두 컴퓨터 모두에서 실행된다. 한 컴퓨터에만 명령을 보내고 싶다면 `$s[0]`처럼 배열 인덱스로 특정 세션만 골라 넘겨야 한다.

**네트워크가 끊기면 세션 상태를 확실히 알 수 없다**: `Get-PSSession`의 `State` 속성이 `Broken`으로 나타날 수 있지만, 일시적인 네트워크 문제인지 원격 컴퓨터 자체의 문제인지는 이 정보만으로 구분되지 않는다. 장시간 배치 작업에는 65장의 `try`/`catch`로 세션 오류를 감지하고 재연결을 시도하는 로직을 함께 고려해야 한다.

**이식성**: Bash의 `tmux`/`screen`이 "연결을 끊어도 세션이 살아있고 나중에 다시 붙을 수 있다"는 점에서 `Disconnect-PSSession`/`Connect-PSSession`과 개념적으로 유사하다. 다만 PowerShell 지속 세션은 원격 **컴퓨터**의 PowerShell 프로세스를 대상으로 하고, `tmux`는 로컬 터미널 멀티플렉서라는 점에서 적용 범위가 다르다.

## Reference

- [Running Remote Commands - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/running-remote-commands)
