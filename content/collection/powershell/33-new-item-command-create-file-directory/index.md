---
draft: false
collection_order: 33
slug: new-item-command-create-file-directory-powershell
title: "[PowerShell] 33. New-Item — 파일·디렉터리 생성"
date: 2026-08-29
lastmod: 2026-08-29
description: "New-Item으로 파일·디렉터리·심볼릭 링크·레지스트리 키를 생성하는 법과 -ItemType/-Value/-Force 매개변수, 프로바이더별로 -ItemType 값이 달라지는 이유, -Force가 기존 파일을 덮어쓰는 함정을 정리한 챕터다."
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
- New-Item
- Symbolic-Link
- Registry
- ItemType
- Permission
- Junction
image: "wordcloud.png"
---

## 개요

`New-Item`(별칭 `ni`)은 새 항목을 만들고 그 값을 설정하는 cmdlet이다. 만들 수 있는 항목의 종류는 위치(프로바이더)에 따라 달라진다 — FileSystem 드라이브에서는 파일·디렉터리·심볼릭 링크를, Registry 드라이브에서는 레지스트리 키를, `Alias:` 드라이브에서는 별칭을 만든다.

## 사용법

```powershell
New-Item [-Path] <String[]> [-Name <String>] [-ItemType <String>] [-Value <Object>] [-Force]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Path` | 새 항목을 만들 위치. 이름까지 포함해 지정할 수도 있다 |
| `-Name` | `-Path`와 별개로 이름을 지정(둘 다 지정 시 `-Path` 아래에 `-Name`으로 생성) |
| `-ItemType`(별칭 `-Type`) | FileSystem: `File`, `Directory`, `SymbolicLink`, `Junction`, `HardLink`. Certificate: `Certificate`, `Store`, `StoreLocation` 등 프로바이더별로 다르다 |
| `-Value`(별칭 `-Target`) | 새 항목의 초기 값(파일 내용, 또는 심볼릭 링크의 대상 경로) |
| `-Force` | 읽기 전용 항목 덮어쓰기를 허용(단, 기존 디렉터리에 `-Force`를 다시 쓰면 내용은 그대로 두고 디렉터리 객체만 반환한다) |

## 예시

```powershell
New-Item -Path . -Name "test.txt" -ItemType File -Value "초기 내용"
New-Item -Path "C:\Logfiles" -ItemType Directory
New-Item -Path $PROFILE -ItemType File -Force        # 상위 디렉터리가 없어도 강제 생성
New-Item -ItemType SymbolicLink -Path .\link -Target .\Notice.txt

# 와일드카드로 여러 디렉터리에 한 번에 파일 생성
New-Item -Path C:\Temp\* -Name temp.txt -ItemType File

# 레지스트리 키 생성
New-Item -Path "HKCU:\Software\MyCompany" -Name "Settings"

# 이미 있는 파일에 -Force를 쓰면 내용이 비워진다(덮어쓰기)
New-Item ./TestFile.txt -ItemType File -Value 'first' 
New-Item ./TestFile.txt -ItemType File -Force   # Length 0으로 초기화됨
```

## 주의사항·함정

**파일에 대한 `-Force`와 디렉터리에 대한 `-Force`는 동작이 다르다**: 이미 있는 파일 경로에 `New-Item -Force`를 다시 실행하면 기존 내용을 지우고 빈 파일로 덮어쓴다 — 레지스트리 키에 대해서도 마찬가지로 값이 전부 초기화된다. 반면 이미 있는 디렉터리 경로에 `-Force`를 실행하면 아무것도 지우지 않고 기존 디렉터리 객체를 그대로 반환한다. "존재하면 건드리지 않는다"는 가정으로 디렉터리에는 `-Force`를 안전하게 쓸 수 있지만, 같은 가정을 파일에 적용하면 데이터를 잃는다.

**심볼릭 링크 생성은 권한이 필요할 수 있다**: Windows에서 `SymbolicLink` 타입 생성은 기본적으로 관리자 권한이 필요하다. Windows 10(빌드 14972+)에서 개발자 모드를 켜면 일반 사용자 권한으로도 만들 수 있다.

**`-Path`에는 와일드카드를 해석하지 않는다는 예외가 있다**: 대부분의 프로바이더 cmdlet과 달리, `New-Item`의 `-Path`는 만들 대상의 경로 자체이므로 와일드카드 문자를 리터럴로 취급한다(예: 파일 이름에 `*`를 쓸 수 없다는 제약과 관련). 다만 여러 디렉터리에 동시에 만드는 예시처럼 상위 경로에 와일드카드를 써서 "이미 존재하는 여러 위치"를 가리키는 용도로는 여전히 와일드카드가 해석된다.

**이식성**: CMD의 `md`/`type nul >`, Bash의 `mkdir`/`touch`에 각각 대응하지만, PowerShell은 이 모든 것을 `-ItemType` 하나로 통일했고 레지스트리 키 생성까지 같은 cmdlet으로 처리한다는 점이 다르다.

## Reference

- [New-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item)
