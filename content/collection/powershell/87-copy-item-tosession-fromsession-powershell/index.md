---
draft: true
collection_order: 87
slug: copy-item-tosession-fromsession-powershell
title: "[PowerShell] 87. Copy-Item -ToSession/-FromSession — 원격 파일 전송"
date: 2026-08-29
lastmod: 2026-08-29
description: "34장 Copy-Item에 -ToSession/-FromSession 동적 매개변수를 더해 86장 지속 세션을 통해 원격 컴퓨터와 파일을 주고받는 법과 -Recurse로 디렉터리 전체를 전송하는 법을 정리한 챕터다."
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
- Copy-Item
- ToSession
- FromSession
- Remote-File-Transfer
- Dynamic-Parameter
- File-Transfer
image: "wordcloud.png"
---

## 개요

`Copy-Item`의 `-ToSession`/`-FromSession` 동적 매개변수는 34장에서 배운 파일 복사 cmdlet을, 86장의 지속 세션을 통해 로컬과 원격 컴퓨터 사이의 파일 전송으로 확장한다. 이 두 매개변수는 FileSystem 프로바이더가 제공하는 동적 매개변수(38장에서 다룬 개념)라, `Get-Help Copy-Item -Full`의 기본 출력에는 안 보이다가 실제로 파일 시스템 경로에 대해 쓸 때만 나타난다.

정신 모델은 "`-ToSession`은 로컬 파일을 원격으로 밀어 넣는(push) 것이고, `-FromSession`은 원격 파일을 로컬로 끌어오는(pull) 것"이라는 것이다. 두 경우 모두 84–86장에서 만든 지속 세션이 실제 파일 데이터가 오가는 통로가 된다.

## 사용법

```powershell
Copy-Item -Path <로컬경로> -Destination <원격경로> -ToSession <세션>
Copy-Item -Path <원격경로> -Destination <로컬경로> -FromSession <세션>
```

## 종류

| 매개변수 | 방향 | `-Path`/`-Destination`의 의미 |
|---|---|---|
| `-ToSession` | 로컬 → 원격 | `-Path`는 로컬 경로, `-Destination`은 원격 컴퓨터의 로컬 경로 |
| `-FromSession` | 원격 → 로컬 | `-Path`는 원격 컴퓨터의 로컬 경로, `-Destination`은 로컬 경로 |
| `-Recurse` | — | 디렉터리 전체(하위 디렉터리 포함)를 전송 |
| `-Force` | — | 읽기 전용 파일도 덮어쓰기 |

## 예시

```powershell
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"   # 86장에서 만든 세션

Copy-Item "D:\Folder001\test.log" -Destination "C:\Folder001_Copy\" -ToSession $Session   # 로컬 → 원격

Copy-Item "D:\Folder002\" -Destination "C:\Folder002_Copy\" -ToSession $Session -Recurse    # 디렉터리 전체

Copy-Item "C:\MyRemoteData\test.log" -Destination "D:\MyLocalData\" -FromSession $Session   # 원격 → 로컬

$copyParams = @{
    Path        = "D:\Folder004\scriptingexample.ps1"
    Destination = "C:\Folder004_Copy\scriptingexample_copy.ps1"    # 복사하며 이름도 함께 변경
    ToSession   = $Session
}
Copy-Item @copyParams

Copy-Item "C:\MyRemoteData\scripts" -Destination "D:\MyLocalData\" -FromSession $Session -Recurse   # 원격 폴더 통째로 회수
```

## 주의사항·함정

**`-ToSession`/`-FromSession`은 `Get-Help`의 기본 출력에 보이지 않는 동적 매개변수다**: 38장에서 배운 것처럼, 이 매개변수들은 FileSystem 프로바이더가 실제 파일 시스템 경로를 다룰 때만 나타난다. 문서에서 처음 찾으려 하면 안 보여서 당황할 수 있는데, `Get-Help Copy-Item -Full`을 실제 파일 시스템 경로와 함께 확인하거나 이 장의 예시처럼 그대로 쓰면 된다.

**`-Path`와 `-Destination`이 각각 로컬인지 원격인지는 어느 매개변수를 쓰느냐에 따라 반대로 해석된다**: `-ToSession`을 쓸 때는 `-Path`가 로컬, `-Destination`이 원격이지만, `-FromSession`을 쓰면 정반대로 `-Path`가 원격, `-Destination`이 로컬이 된다. 이 방향을 헷갈리면 엉뚱한 위치에서 파일을 찾거나 엉뚱한 곳에 파일을 만드는 실수로 이어지기 쉽다.

**대용량 파일 전송은 WinRM의 기본 전송 제한에 걸릴 수 있다**: WS-Management 프로토콜은 기본적으로 한 번에 전송할 수 있는 데이터 크기에 제한이 있어, 매우 큰 파일을 전송하면 실패하거나 매우 느릴 수 있다. 대용량 파일이라면 `New-PSSessionOption -MaximumReceivedDataSizePerCommand` 같은 세션 옵션을 조정하거나, 네트워크 공유 폴더처럼 WinRM을 거치지 않는 다른 전송 방법을 고려해야 한다.

**`-Recurse` 없이 디렉터리를 복사하면 폴더만 만들어지고 내용은 비어 있다**: 34장에서 배운 로컬 `Copy-Item`의 규칙이 세션 전송에도 그대로 적용된다 — 디렉터리 자체는 생성되지만 그 안의 파일·하위 폴더까지 함께 옮기려면 반드시 `-Recurse`를 명시해야 한다.

**이식성**: `scp`(Secure Copy Protocol)가 SSH 기반으로 원격 파일을 주고받는 것과 정확히 같은 목적을 수행한다 — 88장에서 SSH Remoting을 다루고 나면, `Copy-Item -ToSession`을 SSH 기반 세션에도 적용해 `scp`와 매우 비슷한 사용자 경험을 얻을 수 있다. CMD에는 표준화된 원격 파일 복사 명령이 없어 공유 폴더 매핑이나 `robocopy` 같은 별도 도구에 의존해야 한다.

## Reference

- [Copy-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item)
