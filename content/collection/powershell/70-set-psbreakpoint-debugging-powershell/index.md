---
draft: false
collection_order: 70
slug: set-psbreakpoint-debugging-powershell
title: "[PowerShell] 70. Set-PSBreakpoint — 스크립트 디버깅"
date: 2026-08-29
lastmod: 2026-08-29
description: "Set-PSBreakpoint로 스크립트에 줄/명령/변수 단위 브레이크포인트를 거는 법과 -Action 매개변수로 조건부 중단을 만드는 법, Get-PSBreakpoint/Remove-PSBreakpoint로 관리하는 법을 정리한 Part 7 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Error-Handling
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
- Set-PSBreakpoint
- Debugging
- Line-Breakpoint
- Variable-Breakpoint
- Debugger
- Script-Debugging
image: "wordcloud.png"
---

## 개요

`Set-PSBreakpoint`는 스크립트나 세션의 특정 지점에서 실행을 멈추고 디버거로 제어를 넘기는 cmdlet이다. 65장부터 다룬 `try`/`catch`, 68장의 `Write-Verbose`/`Write-Debug`가 "오류가 났을 때, 또는 미리 넣어 둔 메시지로" 상황을 파악하는 도구였다면, 이 장의 브레이크포인트는 오류가 나지 않은 정상 실행 중에도 원하는 순간에 멈춰 세워 변수 상태를 직접 들여다보는 도구다. Part 7의 마지막 챕터로서, 지금까지 배운 진단 도구들과 함께 스크립트 문제를 파악하는 마지막 수단을 제공한다.

정신 모델은 "세 가지 브레이크포인트(줄, 명령, 변수)는 모두 '이 조건이 되면 실행을 멈추고 `DBG>` 프롬프트로 넘겨라'는 규칙을 미리 등록해 두는 것"이라는 것이다.

## 사용법

```powershell
Set-PSBreakpoint -Script <파일> -Line <줄번호>[,...]
Set-PSBreakpoint -Command <명령·함수이름>[,...] [-Script <파일>]
Set-PSBreakpoint -Variable <변수이름>[,...] [-Mode Write|Read|ReadWrite]
```

## 종류

| 브레이크포인트 유형 | 멈추는 시점 |
|---|---|
| 줄 브레이크포인트(`-Line`) | 지정한 줄이 실행되기 직전 |
| 명령 브레이크포인트(`-Command`) | 지정한 cmdlet·함수가 호출되기 직전(함수면 `begin`/`process`/`end` 블록마다) |
| 변수 브레이크포인트(`-Variable`) | 변수 값이 쓰이거나(`Write`, 기본값) 읽히거나(`Read`) 둘 다(`ReadWrite`)일 때 |
| `-Action` | 멈추는 대신 지정한 스크립트 블록을 실행 — `break` 키워드로 실제 중단 여부를 조건부로 결정 가능 |

## 예시

```powershell
Set-PSBreakpoint -Script "sample.ps1" -Line 5              # 5번째 줄 실행 전 멈춤

Set-PSBreakpoint -Command "Increment" -Script "sample.ps1"  # Increment 함수 호출마다 멈춤
Set-PSBreakpoint -Command "checklog"                          # 스크립트 지정 없이 — 세션 전체에서 호출 시 멈춤

Set-PSBreakpoint -Script "sample.ps1" -Variable "Server" -Mode ReadWrite   # 값을 읽거나 쓸 때마다 멈춤

# 조건부 중단 — $Disk가 2보다 클 때만 실제로 멈춤
Set-PSBreakpoint -Script "test.ps1" -Command "DiskTest" -Action { if ($Disk -gt 2) { break } }

Set-PSBreakpoint -Script Sample.ps1 -Command "write*"           # 와일드카드로 Write-* 계열 모두

Get-PSBreakpoint                                                  # 현재 설정된 브레이크포인트 목록
Get-PSBreakpoint | Remove-PSBreakpoint                             # 전부 제거
Disable-PSBreakpoint -Id 0                                          # 삭제 대신 임시 비활성화
```

## 주의사항·함정

**`Set-PSBreakpoint`는 원격 컴퓨터에는 걸 수 없다**: 이 cmdlet은 로컬 세션에서만 동작하며, 원격 컴퓨터의 스크립트를 디버깅하려면 스크립트를 로컬로 복사해 로컬에서 디버깅해야 한다(단, PowerShell 7.2부터는 `-Runspace` 매개변수로 백그라운드 작업의 런스페이스에는 브레이크포인트를 걸 수 있다). 11부에서 다룰 원격 세션 자체를 실시간으로 디버깅할 수 있다고 오해하기 쉬운 지점이다.

**`-Action` 스크립트 블록 안에서 `break`를 쓰지 않으면 실제로는 절대 멈추지 않는다**: `-Action`을 지정하면 브레이크포인트에 도달해도 기본 동작(디버거로 전환)이 일어나지 않고, 그 대신 지정한 스크립트 블록이 실행된다. 조건이 맞을 때 정말로 실행을 멈추고 싶다면 스크립트 블록 안에 명시적으로 `break` 키워드를 넣어야 한다 — 넣지 않으면 마치 로깅 훅처럼 조용히 실행되고 지나간다.

**명령 브레이크포인트는 함수의 각 처리 블록마다 걸린다**: `-Command`로 함수에 브레이크포인트를 걸면, 그 함수가 `begin`/`process`/`end`(57장) 블록을 모두 가지고 있을 경우 각 블록에 진입할 때마다 멈춘다. 파이프라인으로 여러 객체가 들어오는 함수라면 `process` 블록에서 객체 수만큼 반복해서 멈추는 것이 정상 동작이다.

**세션에 남은 브레이크포인트를 정리하지 않으면 다음 스크립트 실행에도 영향을 준다**: `-Script`를 지정하지 않은 명령·변수 브레이크포인트는 세션에서 실행되는 모든 코드에 적용되므로, 디버깅이 끝난 뒤 `Get-PSBreakpoint | Remove-PSBreakpoint`로 정리하지 않으면 나중에 실행하는 무관한 스크립트가 예상치 못하게 멈추는 원인이 된다.

**이식성**: Bash의 `bashdb`나 `set -x`(각 줄 실행 추적)가 개념적으로 비슷한 목적을 수행하지만, PowerShell처럼 변수 값의 읽기/쓰기 자체에 브레이크포인트를 거는 기능은 지원하지 않는다. CMD에는 대응하는 디버깅 도구가 없다. PowerShell의 브레이크포인트 모델은 Visual Studio 같은 통합 개발 환경의 디버거 개념을 셸 스크립팅에 그대로 가져온 결과다.

## Reference

- [Set-PSBreakpoint (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/set-psbreakpoint)
