---
draft: false
collection_order: 78
slug: start-job-get-job-receive-job-powershell
title: "[PowerShell] 78. Start-Job/Get-Job/Receive-Job — 백그라운드 작업"
date: 2026-08-29
lastmod: 2026-08-29
description: "Start-Job으로 별도 프로세스에서 백그라운드 작업을 실행하는 법과 Get-Job으로 상태를 확인하고 Receive-Job으로 결과를 꺼내는 법, -ArgumentList로 값을 전달하는 법, 79장 ForEach-Object -Parallel과의 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Module(모듈)
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
- Start-Job
- Background-Job
- Get-Job
- Receive-Job
- Wait-Job
- Background-Process
image: "wordcloud.png"
---

## 개요

`Start-Job`은 명령을 현재 세션과 분리된 **별도 프로세스**에서 백그라운드로 실행하는 cmdlet이다. 지금까지 배운 명령은 모두 실행이 끝날 때까지 콘솔을 붙잡고 있었는데, `Start-Job`은 오래 걸리는 작업을 뒤로 보내 놓고 그동안 다른 작업을 계속할 수 있게 해 준다. 79장에서 다룰 `ForEach-Object -Parallel`과 함께 PowerShell의 병렬·비동기 실행 모델을 이루는 두 축 중 하나다.

정신 모델은 "`Start-Job`은 작업을 시작하고 즉시 작업 **정보**만 돌려주는 접수증이고, 그 작업이 실제로 만들어낸 **결과**는 `Receive-Job`으로 나중에 따로 찾으러 가야 한다"는 것이다.

## 사용법

```powershell
$job = Start-Job -ScriptBlock { <백그라운드에서 실행할 코드> } [-ArgumentList <값들>]
Get-Job [-Id <ID>]
Receive-Job -Job $job [-Wait] [-Keep]
```

## 종류

| cmdlet | 역할 |
|---|---|
| `Start-Job` | 백그라운드 작업 시작, 즉시 작업 객체 반환(결과 아님) |
| `Get-Job` | 실행 중인·완료된 작업의 상태(State) 조회 |
| `Receive-Job` | 작업이 만든 출력을 가져옴(기본적으로 한 번 가져오면 비워짐, `-Keep`으로 유지) |
| `Wait-Job` | 작업이 끝날 때까지 대기(스크립트를 동기적으로 만들고 싶을 때) |
| `Stop-Job` / `Remove-Job` | 실행 중인 작업 중단 / 작업 객체 자체를 정리 |
| `&`(백그라운드 연산자) | PowerShell 6+, `Start-Job`과 거의 동일한 효과를 내는 단축 문법 |

## 예시

```powershell
$job = Start-Job -ScriptBlock { Get-Process -Name pwsh }   # 즉시 반환, 백그라운드에서 실행 중
$job                                                          # State: Running

Get-Job                                                        # 세션의 모든 작업 상태 확인
Receive-Job -Job $job -Wait                                     # 끝날 때까지 기다렸다가 결과 수령

Get-Process -Name pwsh &                                        # 백그라운드 연산자로 동일한 효과

Start-Job -ScriptBlock { Get-Process -Name $args } -ArgumentList "notepad", "pwsh"   # 인자 전달

$j = Start-Job -Name "SystemLog" -ScriptBlock { Get-WinEvent -LogName System }
while ((Get-Job -Id $j.Id).State -eq 'Running') { Start-Sleep -Seconds 1 }             # 폴링 대기
Receive-Job -Job $j

Start-Job -FilePath C:\Scripts\LongTask.ps1                       # 스크립트 파일 자체를 작업으로 실행

"C:\Servers.txt" | Start-Job -ScriptBlock { Get-Content -Path $input }  # $input으로 파이프 입력 받기

Receive-Job -Job $job -Keep                                        # 결과를 비우지 않고 유지(재조회 가능)
Remove-Job -Job $job                                                # 작업 정리
```

## 주의사항·함정

**작업 스크립트 블록은 완전히 별도의 프로세스에서 실행되어, 현재 세션의 함수·변수를 자동으로 볼 수 없다**: `Start-Job -ScriptBlock { MyFunction }`처럼 세션에서 정의한 함수를 그대로 부르면 "명령을 찾을 수 없다"는 오류가 난다. `-InitializationScript`로 필요한 모듈·함수를 먼저 로드하거나, `-ArgumentList`로 필요한 값만 명시적으로 전달해야 한다 — 63장의 클로저와 달리 잡(Job)은 부모 세션의 상태를 자동으로 물려받지 않는다.

**`Receive-Job`은 기본적으로 결과를 한 번 가져오면 비워 버린다**: `-Keep`을 붙이지 않으면 같은 작업에 `Receive-Job`을 두 번 호출했을 때 두 번째는 빈 결과만 나온다. 결과를 여러 번 참조해야 한다면 `-Keep`을 쓰거나, 처음 받은 결과를 변수에 저장해 둬야 한다.

**작업이 많아지면 프로세스 생성 오버헤드가 누적된다**: `Start-Job`은 매번 별도의 `pwsh` 프로세스를 새로 띄우기 때문에, 아주 짧은 작업을 수백 개 병렬로 돌리기에는 79장의 `ForEach-Object -Parallel`(스레드 기반)이나 `Start-ThreadJob`이 훨씬 가볍다. `Start-Job`은 작업 하나하나가 상당히 무겁고 오래 걸리는 경우(파일 처리, 네트워크 대기 등)에 적합하다.

**세션을 닫으면 실행 중이던 작업 정보도 함께 사라진다**: 잡은 현재 세션에 종속되므로, 콘솔을 닫으면 미처 `Receive-Job`으로 수거하지 못한 결과는 잃어버린다. 장시간 실행되는 배치 작업이라면 예약 작업(78장이 아니라 12부에서 다룰 스케줄러)이나 결과를 파일로 저장하는 방식을 함께 고려해야 한다.

**이식성**: Bash의 `&`(백그라운드 실행)와 `jobs`/`wait` 명령이 개념적으로 가장 가깝다 — PowerShell 6+의 `&` 백그라운드 연산자도 이름과 동작이 유사하게 설계됐다. 다만 Bash의 백그라운드 작업은 같은 셸 프로세스 안의 서브프로세스인 반면, PowerShell의 `Start-Job`은 완전히 독립된 `pwsh` 프로세스를 새로 띄운다는 점이 격리 수준에서 다르다. CMD의 `start` 명령도 새 창에서 명령을 실행하지만, 구조화된 결과 수집(`Receive-Job`에 대응하는 개념)은 없다.

## Reference

- [Start-Job (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job)
