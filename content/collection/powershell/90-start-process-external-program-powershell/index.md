---
draft: true
collection_order: 90
slug: start-process-external-program-powershell
title: "[PowerShell] 90. Start-Process — 외부 프로그램 실행"
date: 2026-08-29
lastmod: 2026-08-29
description: "Start-Process로 외부 프로그램을 새 프로세스로 실행하는 법과 -ArgumentList/-Wait/-NoNewWindow 매개변수, -Verb RunAs로 관리자 권한 상승하는 법, 기본적으로 아무 값도 반환하지 않아 -PassThru가 필요한 이유를 정리한 챕터다."
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
- Start-Process
- ArgumentList
- RunAs
- PassThru
- Process-Launch
- Executable
image: "wordcloud.png"
---

## 개요

`Start-Process`는 실행 파일이나 문서를 새 프로세스로 시작하는 cmdlet이다. 89장의 `Get-Process`가 이미 실행 중인 프로세스를 들여다보는 도구였다면, 이 장은 그 반대편 — 프로세스를 새로 만드는 법을 다룬다. 단순히 명령 이름만 입력해 외부 프로그램을 실행하는 것과 달리, 창 스타일·권한 상승·표준 입출력 리다이렉션까지 세밀하게 제어할 수 있다.

정신 모델은 "`Start-Process`는 기본적으로 **비동기**로 동작해, 새 프로세스를 시작만 시켜 놓고 곧바로 PowerShell 프롬프트로 돌아온다"는 것이다. 새 프로세스가 끝날 때까지 기다리려면 `-Wait`를 명시해야 한다.

## 사용법

```powershell
Start-Process -FilePath <실행파일> [-ArgumentList <인자들>] [-Wait] [-NoNewWindow] [-Verb <동사>] [-PassThru]
```

## 종류

| 매개변수 | 설명 |
|---|---|
| `-ArgumentList`(별칭 `-Args`) | 실행 파일에 넘길 인자(공백 포함 시 이스케이프된 큰따옴표로 감싸야 함) |
| `-Wait` | 프로세스(와 그 자식 프로세스 전부)가 끝날 때까지 대기 |
| `-NoNewWindow` | 새 창 없이 현재 콘솔 안에서 실행(Windows 전용) |
| `-WindowStyle` | `Normal`/`Hidden`/`Minimized`/`Maximized` |
| `-Verb RunAs` | 관리자 권한으로 상승해 실행(UAC 프롬프트) |
| `-Credential` | 다른 사용자 계정으로 실행 |
| `-PassThru` | 시작한 프로세스의 `Process` 객체를 반환(기본은 아무 출력도 없음) |
| `-RedirectStandardOutput`/`-RedirectStandardError`/`-RedirectStandardInput` | 표준 스트림을 파일로 리다이렉션 |

## 예시

```powershell
Start-Process -FilePath "notepad"                            # 기본값으로 실행, 즉시 프롬프트로 복귀

Start-Process -FilePath "notepad" -Wait -WindowStyle Maximized  # 종료까지 대기, 최대화 창

Start-Process -FilePath "powershell" -Verb RunAs                 # 관리자 권한으로 상승(UAC 프롬프트)

$proc = Start-Process -FilePath "notepad" -PassThru               # -PassThru 없으면 $proc는 $null
$proc.Id                                                             # 나중에 이 PID로 89장의 Stop-Process 등에 활용

Start-Process -FilePath "$Env:ComSpec" -ArgumentList '/c dir "%SystemDrive%\Program Files"'   # 공백 포함 인자

$processOptions = @{
    FilePath                = "sort.exe"
    RedirectStandardInput   = "TestSort.txt"
    RedirectStandardOutput  = "Sorted.txt"
    RedirectStandardError   = "SortError.txt"
}
Start-Process @processOptions                                        # 25장 스플래팅과 결합

Start-Process -FilePath "myfile.txt" -WorkingDirectory "C:\PS-Test" -Verb Print   # 프린트 동사로 인쇄
```

## 주의사항·함정

**기본적으로 아무 출력도 반환하지 않는다**: `$proc = Start-Process notepad`처럼 결과를 변수에 담아도, `-PassThru`를 명시하지 않으면 `$proc`는 `$null`이다. 나중에 시작한 프로세스를 89장의 `Get-Process`/`Stop-Process`로 다시 다뤄야 한다면 반드시 `-PassThru`로 `Process` 객체를 받아 둬야 한다.

**로컬에서는 독립 프로세스지만, 원격 세션에서는 그렇지 않다**: 로컬 컴퓨터에서 시작한 프로세스는 PowerShell 세션과 완전히 독립적으로 계속 실행되지만, 85–86장에서 배운 원격 세션 안에서 `Start-Process`를 쓰면 그 세션이 끝나는 순간 새로 시작한 프로세스도 함께 종료된다. 원격 세션에서 오래 실행되는 프로세스를 시작해야 한다면 `-Wait`를 함께 쓰거나 78장의 `Start-Job` 같은 다른 방법을 고려해야 한다.

**공백이 포함된 인자는 이스케이프된 큰따옴표로 감싸야 한다**: `-ArgumentList`에 넘기는 문자열 안에 공백이 있는 경로가 있다면, 45장에서 배운 백틱 이스케이프(`` `"..."` ``)로 큰따옴표를 한 번 더 감싸야 실행 파일이 인자를 하나로 인식한다. 이 규칙을 놓치면 경로가 여러 인자로 쪼개져 전달되는 오류가 흔히 발생한다.

**비Windows에서는 `Start-Process`가 시작한 프로세스가 셸에 종속된다**: Windows에서는 독립 프로세스가 만들어지지만, Linux/macOS에서는 새 프로세스가 시작한 셸에 붙어 있어 그 셸이 닫히면 함께 종료된다. 세션이 끝나도 살아남는 백그라운드 프로세스가 필요하다면 `nohup`과 조합해야 한다(예: `Start-Process nohup 'pwsh -c "..."'`).

**이식성**: CMD의 `start` 명령(`Start-Process`의 Windows 별칭이기도 하다), Bash의 명령 뒤 `&`(백그라운드 실행)와 개념적으로 유사하다. `-Verb RunAs`는 Windows UAC 상승에 특화된 기능으로, Linux/macOS의 `sudo`에 대응하지만 플랫폼 간 동작 방식은 근본적으로 다르다.

## Reference

- [Start-Process (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process)
