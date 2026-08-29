---
draft: true
collection_order: 83
slug: powershell-remoting-winrm-enable-powershell
title: "[PowerShell] 83. PowerShell Remoting 개념과 WinRM 활성화"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell Remoting이 WS-Management(WinRM) 프로토콜로 원격 컴퓨터에서 명령을 실행하는 원리와 Enable-PSRemoting으로 활성화하는 법, ComputerName 매개변수만으로 되는 명령과 진짜 Remoting의 차이를 정리한 Part 11 시작 챕터다."
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
- PowerShell-Remoting
- WinRM
- WS-Management
- Enable-PSRemoting
- TrustedHosts
- Remote-Management
image: "wordcloud.png"
---

## 개요

**PowerShell Remoting**은 WS-Management(WinRM) 프로토콜을 통해 원격 컴퓨터에서 PowerShell 명령을 실행하는 기능이다. 지금까지 이 컬렉션의 모든 예제는 로컬 컴퓨터를 대상으로 했는데, 이 장부터는 그 범위를 네트워크 너머의 다른 컴퓨터로 확장하며 Part 11(원격 관리)을 시작한다. 이미 65장의 `Get-WinEvent`나 78장의 `Start-Job` 같은 일부 cmdlet은 별도 설정 없이도 `-ComputerName` 매개변수로 부분적인 원격 기능을 제공했지만, 진짜 Remoting은 그보다 훨씬 넓은 범위의 명령을 지원한다.

정신 모델은 "Remoting을 활성화한다는 것은, 원격 컴퓨터에 '내가 PowerShell 명령을 받아 대신 실행해 줄게'라는 리스너(listener)를 세워 두는 것"이라는 것이다. 이 리스너가 없으면 아무리 정확한 명령을 보내도 받아 줄 상대가 없다.

## 사용법

```powershell
Enable-PSRemoting -Force              # 대상 컴퓨터에서 실행 — 리스너 활성화
Test-WSMan -ComputerName <컴퓨터이름>   # 원격 컴퓨터가 리스너를 갖췄는지 확인
```

## 종류

| 구분 | 설명 |
|---|---|
| `-ComputerName`만 지원하는 cmdlet | `Get-Process`, `Get-Service` 등, 별도 설정 없이도 제한적 원격 조회 가능 |
| 진짜 PowerShell Remoting | `Enable-PSRemoting`으로 WinRM 리스너를 켜야 함, `-Session`/`Invoke-Command` 전체 기능 사용 가능 |
| WSMan 프로바이더 | `WSMan:` 드라이브로 원격 설정을 탐색·변경(30장의 프로바이더 개념 재사용) |
| TrustedHosts 목록 | 워크그룹 환경(도메인 미가입)에서 IP 주소로 접속 시 반드시 등록해야 하는 신뢰 대상 목록 |

## 예시

```powershell
# 대상 컴퓨터에서 실행 — Remoting 활성화(관리자 권한 필요)
Enable-PSRemoting -Force

Test-WSMan -ComputerName Server01                # 리스너 응답 확인

# -ComputerName만으로 별도 설정 없이 되는 예(진짜 Remoting과 구분)
Get-Process | Where-Object {
    $_.Parameters.Keys -contains "ComputerName" -and
    $_.Parameters.Keys -notcontains "Session"
}

# 워크그룹 환경에서 IP로 접속 시 TrustedHosts 등록 필요
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.100" -Force
Get-Item WSMan:\localhost\Client\TrustedHosts       # 등록된 목록 확인

winrm quickconfig                                     # winrm 자체 명령으로도 유사하게 확인 가능
```

## 주의사항·함정

**`-ComputerName` 매개변수가 있다고 해서 모든 cmdlet이 진짜 Remoting을 쓰는 것은 아니다**: `Get-Process -ComputerName`, `Get-Service -ComputerName`처럼 일부 관리 cmdlet은 WMI/RPC 같은 다른 프로토콜로 별도 설정 없이 원격 조회를 지원하지만, 이런 cmdlet에는 `-Session` 매개변수가 없다. 임의의 명령·스크립트 블록을 원격에서 실행하려면(84–86장에서 다룰 `Enter-PSSession`/`Invoke-Command`/`New-PSSession`) 반드시 `Enable-PSRemoting`으로 WinRM 리스너를 먼저 켜야 한다.

**워크그룹(도메인 미가입) 환경에서 IP 주소로 접속하려면 TrustedHosts 등록이 필수다**: 도메인에 가입된 컴퓨터끼리는 Kerberos 인증으로 신뢰 관계가 자동으로 성립하지만, 워크그룹 환경이거나 컴퓨터 이름 대신 IP 주소를 쓴다면 로컬 컴퓨터의 `WSMan:\localhost\Client\TrustedHosts` 목록에 상대방을 미리 등록해야 한다 — 그렇지 않으면 인증 단계에서 연결이 거부된다.

**관리자 권한 없이는 `Enable-PSRemoting`도, 원격 접속도 되지 않는다**: 대상 컴퓨터에서 리스너를 켜는 작업도, 원격 컴퓨터에 접속하는 쪽도 기본적으로 관리자(Administrators) 그룹 권한이 필요하다. 일반 사용자 권한으로 시도하면 접근 거부 오류가 난다.

**이식성**: Linux/macOS의 SSH가 88장에서 다룰 크로스플랫폼 Remoting의 기반이 되며, WinRM은 그와 별개로 Windows 생태계에 특화된 프로토콜이다. Bash에서 `ssh user@host command`로 원격 명령을 실행하는 것과 개념적으로 대응하지만, WinRM 기반 Remoting은 SOAP 기반 WS-Management 표준을 사용해 방화벽·인증 설정이 SSH와는 다른 방식으로 이뤄진다는 점이 다르다.

## Reference

- [Running Remote Commands - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/running-remote-commands)
