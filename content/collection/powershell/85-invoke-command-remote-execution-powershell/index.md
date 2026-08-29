---
draft: true
collection_order: 85
slug: invoke-command-remote-execution-powershell
title: "[PowerShell] 85. Invoke-Command — 원격 명령 실행"
date: 2026-08-29
lastmod: 2026-08-29
description: "Invoke-Command로 하나 또는 수백 대의 원격 컴퓨터에 한 번에 명령을 보내는 법과 -ComputerName/-Session의 차이, -AsJob으로 비동기 실행하는 법, $using: 스코프 수정자로 로컬 변수를 전달하는 법을 정리한 챕터다."
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
- Invoke-Command
- Fan-Out
- ThrottleLimit
- Using-Scope
- Remote-Scriptblock
- Multi-Computer
image: "wordcloud.png"
---

## 개요

`Invoke-Command`는 하나 또는 수백 대의 원격 컴퓨터에 스크립트 블록을 한 번에 보내 실행하고, 그 결과를 모두 로컬로 모아 오는 cmdlet이다. 84장의 `Enter-PSSession`이 "한 대의 컴퓨터에 들어가 직접 명령을 입력한다"는 대화형 방식이었다면, `Invoke-Command`는 "여러 컴퓨터에 명령을 보내고 결과만 받는다"는 비대화형·**팬아웃(fan-out)** 방식이다.

정신 모델은 "스크립트 블록을 여러 원격 컴퓨터에 동시에 뿌리고(fan out), 각 컴퓨터의 결과를 다시 하나의 파이프라인으로 모으는(fan in) 것"이라는 것이다. 79장의 `ForEach-Object -Parallel`이 같은 컴퓨터의 여러 스레드에 작업을 나눴다면, 이 장은 그 병렬성을 네트워크 상의 여러 컴퓨터로 확장한다.

## 사용법

```powershell
Invoke-Command -ComputerName <컴퓨터이름들> -ScriptBlock { <원격에서 실행할 코드> }
Invoke-Command -Session <PSSession들> -ScriptBlock { <코드> }
```

## 종류

| 매개변수 | 특징 |
|---|---|
| `-ComputerName` | 임시 연결 생성 후 명령 실행하고 즉시 종료(연결을 재사용하지 않음) |
| `-Session` | 86장의 지속 세션 재사용 — 여러 번 호출해도 같은 세션 상태(변수 등) 유지 |
| `-ScriptBlock` | 원격에서 실행할 코드 |
| `-FilePath` | 로컬에 있는 스크립트 파일을 원격에 보내 실행 |
| `-ArgumentList` | 스크립트 블록의 `param()`으로 값 전달(25장의 스플래팅 방식과 유사) |
| `-AsJob` | 78장에서 배운 Job으로 반환 — 즉시 프롬프트로 복귀, 나중에 `Receive-Job` |
| `-ThrottleLimit` | 동시에 연결할 최대 컴퓨터 수(기본값 32) |
| `$using:` | 63장의 클로저와 유사하게, 로컬 변수 값을 원격 스크립트 블록에 전달 |

## 예시

```powershell
Invoke-Command -ComputerName Server01, Server02 -ScriptBlock { Get-UICulture }   # 여러 컴퓨터 동시 실행

Invoke-Command -ComputerName Server01, Server02 -FilePath C:\Scripts\DiskCollect.ps1   # 로컬 스크립트를 원격 실행

$parameters = @{
    ComputerName = 'Server01', 'Server02', 'localhost'
    ScriptBlock  = { Get-WinEvent -LogName System -MaxEvents 100 }
    ThrottleLimit = 10
}
Invoke-Command @parameters                                                       # 25장 스플래팅과 결합

Invoke-Command -ComputerName Server01 -ScriptBlock {
    param($Pattern, $Extension)
    Get-ChildItem -Path C:\Logs -Filter "$Pattern*.$Extension"
} -ArgumentList 'app', 'log'

$Log = 'System'
Invoke-Command -ComputerName Server01 -ScriptBlock {
    Get-WinEvent -LogName $Using:Log -MaxEvents 10                                # 로컬 변수를 $using:으로 전달
}

$s = New-PSSession -ComputerName Server01, Server02
Invoke-Command -Session $s -ScriptBlock { $h = Get-HotFix }                        # 세션에 변수 저장
Invoke-Command -Session $s -ScriptBlock { $h | Where-Object InstalledBy -ne "SYSTEM" }  # 같은 세션에서 재사용

$job = Invoke-Command -Session $s -ScriptBlock { Get-EventLog System } -AsJob        # 78장 Job으로
$job | Receive-Job -Wait
```

## 주의사항·함정

**`-ComputerName`은 매번 새 연결을 만들고 끊어, 이전 호출의 상태를 기억하지 못한다**: `-ComputerName`으로 두 번 `Invoke-Command`를 호출하면 완전히 독립된 연결이라, 첫 번째 호출에서 만든 변수를 두 번째 호출에서 쓸 수 없다. 여러 명령에 걸쳐 상태를 유지해야 한다면 86장에서 배울 `New-PSSession`으로 지속 세션을 먼저 만들고 `-Session`을 써야 한다.

**`$using:` 없이 로컬 변수를 스크립트 블록 안에서 참조하면 빈 값이 나온다**: `Invoke-Command`의 스크립트 블록은 원격 컴퓨터의 완전히 다른 프로세스에서 실행되므로, 62장의 일반 스코프 규칙이 적용되지 않는다. 79장의 `ForEach-Object -Parallel`과 마찬가지로, 로컬 세션의 변수 값을 원격으로 넘기려면 반드시 `$using:변수이름` 문법이 필요하다.

**결과 객체에는 `PSComputerName` 속성이 자동으로 추가된다**: 여러 컴퓨터에서 온 결과를 한 파이프라인으로 받으면 "어느 컴퓨터에서 온 결과인지" 구분이 안 될 것 같지만, `Invoke-Command`는 각 결과 객체에 원본 컴퓨터 이름을 자동으로 붙여 준다. `Select-Object -Property *, PSComputerName`처럼 굳이 신경 쓰지 않아도 13장의 `Select-Object`로 이 속성을 바로 활용할 수 있다.

**`-ThrottleLimit` 기본값(32)을 넘는 컴퓨터 목록은 자동으로 배치 처리된다**: 수백 대에 명령을 보내야 한다면, 한 번에 32대씩 순차적으로 처리되므로 전체 완료 시간이 그만큼 늘어난다. 대규모 환경에서는 `-ThrottleLimit`을 상황에 맞게 조정하거나 `-AsJob`으로 비동기 처리해 콘솔이 막히지 않게 해야 한다.

**이식성**: Bash의 `parallel-ssh`나 Ansible의 팬아웃 실행 모델과 개념적으로 가장 가깝다 — "여러 원격 호스트에 같은 명령을 보내고 결과를 모은다"는 목표는 같지만, `Invoke-Command`는 결과를 텍스트가 아니라 10장에서 강조한 구조화된 객체로 돌려받는다는 점이 근본적으로 다르다. CMD에는 이런 팬아웃 원격 실행에 대응하는 표준 도구가 없다.

## Reference

- [Running Remote Commands - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/running-remote-commands)
