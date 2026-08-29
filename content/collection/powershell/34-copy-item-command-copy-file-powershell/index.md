---
draft: true
collection_order: 34
slug: copy-item-command-copy-file-powershell
title: "[PowerShell] 34. Copy-Item — 복사"
date: 2026-08-29
lastmod: 2026-08-29
description: "Copy-Item으로 파일·디렉터리·레지스트리 키를 복사하는 법과 -Recurse/-Container/-Filter 매개변수의 상호작용, -ToSession/-FromSession으로 원격 세션과 파일을 주고받는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- File-System
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
- Remoting
- PSSession
- Backup
- Get-ChildItem
- Deployment(배포)
image: "wordcloud.png"
---

## 개요

`Copy-Item`은 항목을 원본에서 지우지 않고 다른 위치에 복제하는 cmdlet이다. 같은 네임스페이스(같은 프로바이더) 안에서만 복사할 수 있다 — 파일을 폴더로 복사할 수는 있어도 인증서 저장소로 복사할 수는 없다. `-Destination`에 새 이름을 지정하면 복사와 동시에 이름도 바꿀 수 있다.

## 사용법

```powershell
Copy-Item [-Path] <String[]> [[-Destination] <String>] [-Container] [-Recurse] [-Filter <String>] [-Force] [-ToSession <PSSession>] [-FromSession <PSSession>]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Path` / `-Destination` | 원본과 대상 경로. `-Destination` 생략 시 현재 디렉터리 |
| `-Recurse` | 하위 디렉터리·파일까지 복사 |
| `-Container` | 디렉터리 구조를 유지할지 여부(기본 `$true`). `$false`로 주면 내용만 평평하게 복사(동명 파일은 덮어써짐) |
| `-Filter` / `-Include` / `-Exclude` | 31장과 같은 규칙 — `-Filter`는 프로바이더 수준, `-Include`/`-Exclude`는 후처리(둘 다 `-Path`의 와일드카드 매칭 결과에만 적용되고 `-Recurse`로 발견된 하위 항목에는 적용 안 됨) |
| `-Force` | 읽기 전용 항목도 덮어쓰기 허용 |
| `-ToSession` / `-FromSession` | 원격 컴퓨터로/에서 파일을 복사할 `PSSession` 지정(11부에서 원격 세션을 본격적으로 다룬다) |

## 예시

```powershell
Copy-Item "C:\Logs\a.txt" -Destination "C:\Backup"                     # 단일 파일
Copy-Item -Path "C:\Logfiles\*" -Destination "C:\Drawings" -Recurse    # 내용만 복사(디렉터리 자체는 제외)
Copy-Item -Path "C:\Logfiles" -Destination "C:\Drawings\Logs" -Recurse # 디렉터리 자체를 새 이름으로 복사
Copy-Item -Path C:\temp\tree -Filter *.txt -Recurse -Container:$false # 트리 구조를 무시하고 평평하게 복사

# 원본을 찾아 파이프로 넘기는 방식이 -Include보다 재귀에 안전하다
Get-ChildItem -Path D:\temp\tree -Recurse -Filter ex* | Copy-Item

# 원격 세션으로 파일 전송
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"
Copy-Item "D:\Folder001\test.log" -Destination "C:\Folder001_Copy\" -ToSession $Session
Copy-Item "C:\MyRemoteData\test.log" -Destination "D:\MyLocalData\" -FromSession $Session
```

## 주의사항·함정

**`-Include`/`-Exclude`는 `-Recurse`로 발견된 항목까지 걸러주지 않는다**: 이 두 매개변수는 `-Path`에 지정한 와일드카드가 1차로 펼쳐진 결과에만 적용되고, 그 하위로 재귀하며 새로 찾은 항목에는 적용되지 않는다. 재귀 중에 세밀한 패턴으로 걸러야 한다면, 예시처럼 `Get-ChildItem -Recurse -Filter`로 먼저 대상을 찾은 뒤 `Copy-Item`으로 파이프하는 방식이 더 예측 가능하다.

**`-Container $false`는 동명 파일을 조용히 덮어쓴다**: 서로 다른 하위 디렉터리에 있던 같은 이름의 파일들이 평평한 복사 과정에서 마지막에 처리된 파일로 덮어써진다. 파일 이름이 겹칠 가능성이 있는 트리를 평평하게 합칠 때는 사전에 이름 충돌 여부를 확인해야 한다.

**대상 디렉터리가 없으면 결과가 헷갈릴 수 있다**: `Copy-Item -Path "C:\Logfiles\*" -Destination "C:\Drawings" -Recurse`에서 `C:\Drawings`가 아예 존재하지 않으면, 여러 파일이 있는 트리 전체가 `Drawings`라는 이름의 파일 하나로 뭉개질 수 있다. 대상이 디렉터리인지 사전에 `Test-Path -PathType Container`로 확인하는 습관이 안전하다(39장에서 `Test-Path`를 다룬다).

**이식성**: `copy`/`xcopy`/`robocopy`가 별도 명령으로 나뉜 CMD와 달리, PowerShell은 단일 파일 복사부터 재귀 복사, 원격 전송까지 `Copy-Item` 하나의 매개변수 조합으로 표현한다. Bash의 `cp -r`, `scp`에 각각 `-Recurse`, `-ToSession`/`-FromSession`이 대응한다.

## Reference

- [Copy-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item)
