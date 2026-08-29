---
draft: true
collection_order: 88
slug: ssh-remoting-cross-platform-powershell
title: "[PowerShell] 88. SSH 기반 PowerShell Remoting(크로스플랫폼)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 6+가 SSH 프로토콜로 Windows·Linux·macOS를 가리지 않고 Remoting하는 법과 -HostName 매개변수 사용법, WinRM 방식과의 차이, sudo·프로필 미지원 같은 SSH Remoting의 제약을 정리한 Part 11 마지막 챕터다."
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
- SSH-Remoting
- Cross-Platform
- OpenSSH
- HostName-Parameter
- Key-Authentication
- Linux(리눅스)
image: "wordcloud.png"
---

## 개요

PowerShell 6부터는 WS-Management(WinRM) 대신 **SSH** 프로토콜로도 Remoting을 할 수 있다. 83–87장에서 다룬 WinRM 기반 Remoting이 Windows 생태계에 최적화돼 있었다면, SSH 기반 Remoting은 01장에서 강조한 PowerShell 7의 크로스플랫폼 특성을 원격 관리에도 실현해, Windows·Linux·macOS를 진짜로 가리지 않고 서로 접속할 수 있게 해 준다. Part 11(원격 관리)의 마지막 챕터로서, 지금까지 배운 `Enter-PSSession`/`Invoke-Command`/`New-PSSession`이 전송 계층만 바꿔 그대로 재사용된다는 점을 확인한다.

정신 모델은 "SSH 서버가 각 대상 컴퓨터에 `powershell`이라는 이름의 서브시스템(subsystem)을 등록해 두면, SSH 클라이언트로 접속했을 때 일반 셸 대신 PowerShell 프로세스가 그 연결을 받는다"는 것이다.

## 사용법

```powershell
New-PSSession -HostName <호스트> -UserName <사용자>
Enter-PSSession -HostName <호스트> -UserName <사용자> [-KeyFilePath <키경로>]
Invoke-Command -HostName <호스트> -UserName <사용자> -ScriptBlock { ... }
```

## 종류

| 요소 | 설명 |
|---|---|
| `-HostName` | WinRM의 `-ComputerName` 대신 SSH 접속 대상을 지정 |
| `-UserName` | SSH 접속 계정(생략 시 프롬프트로 비밀번호 입력 요구) |
| `-KeyFilePath` | 비밀번호 대신 SSH 키 기반 인증 사용 |
| `sshd_config`의 `Subsystem powershell` | 대상 컴퓨터에서 SSH가 PowerShell 프로세스를 실행하도록 등록하는 설정 |
| 지원 방향 | Windows↔Windows, Windows↔Linux, Linux↔Linux, macOS 포함 모든 조합 |

## 예시

```powershell
# 대상 컴퓨터의 sshd_config에 다음 줄이 미리 등록돼 있어야 함(관리자가 사전 설정)
# Subsystem powershell /usr/bin/pwsh -sshs -NoLogo

$session = New-PSSession -HostName UbuntuVM1 -UserName TestUser   # 최초 접속 시 호스트 신뢰 여부 확인 프롬프트
Enter-PSSession $session
[UbuntuVM1]: PS /home/TestUser> uname -a                            # 실제로 Linux 셸 명령도 실행 가능
[UbuntuVM1]: PS /home/TestUser> Exit-PSSession

Invoke-Command $session -ScriptBlock { Get-Process pwsh }             # 85장의 방식 그대로 재사용

Enter-PSSession -HostName UserA@LinuxServer02:22 -KeyFilePath C:\sshkeys\userAKey_rsa   # 키 인증 + 포트 지정

$options = @{ Port = 22; User = 'UserA'; Host = 'LinuxServer02' }
Enter-PSSession -KeyFilePath C:\sshkeys\userAKey_rsa -Options $options   # 옵션 해시테이블로 세밀한 SSH 설정

# Windows에서 Windows로도 SSH 기반 접속 가능(WinRM 대신)
$session2 = New-PSSession -HostName WinVM2 -UserName PSRemoteUser
```

## 주의사항·함정

**SSH 기반 세션에서는 `sudo`가 동작하지 않는다**: Linux 대상 컴퓨터에 접속한 SSH 기반 원격 세션 안에서 `sudo` 명령을 실행하면 정상적으로 동작하지 않는다는 것이 공식적으로 알려진 제약이다. 관리자 권한이 필요한 작업이라면 애초에 관리자 권한을 가진 계정으로 접속해야 한다.

**`$PROFILE`이 자동으로 로드되지 않는다**: 84장에서 WinRM 기반 세션은 원격 사용자 프로필을 자동으로 적용한다고 했는데, SSH 기반 Remoting은 이 동작을 지원하지 않는다. 프로필의 함수·별칭이 필요하다면 세션 안에서 `. $PROFILE`처럼 점 소싱(53장)으로 수동으로 불러와야 한다.

**JEA(Just Enough Administration)와 커스텀 세션 구성을 지원하지 않는다**: WinRM 기반 Remoting이 제공하는 세밀한 권한 제한·엔드포인트 구성 기능(14부에서 다룰 예정)이 SSH 기반에는 아직 없다. 보안이 중요한 환경에서 접근 권한을 세밀하게 제어해야 한다면 이 제약을 감안해 WinRM 방식을 유지하거나 다른 보완책을 마련해야 한다.

**PowerShell 7.1 이전에는 SSH 세션 안에서 다시 다른 컴퓨터로 재접속(2차 홉)이 안 됐다**: WinRM 기반 세션은 원격 세션 안에서 또 다른 컴퓨터로 재차 `Enter-PSSession`하는 것이 오래전부터 가능했지만, SSH 기반은 PowerShell 7.1부터 이 기능이 추가됐다. 오래된 버전으로 다단계 원격 접속 체인을 구성하려던 스크립트라면 이 버전 제약을 고려해야 한다.

**이식성**: 이 장 자체가 "이식성"을 주제로 삼는다 — SSH 기반 Remoting은 `ssh user@host`로 Linux/macOS 서버에 접속하던 익숙한 흐름을 PowerShell 세션 안으로 그대로 가져온 것이다. 반대로 WinRM 기반 Remoting(83–87장)에 익숙한 Windows 관리자에게는, SSH 기반이 인증·신뢰 관계 설정 방식(TrustedHosts 대신 SSH 호스트 키 확인)이 다르다는 점이 가장 먼저 체감되는 차이다.

## Reference

- [PowerShell Remoting Over SSH - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/ssh-remoting-in-powershell)
