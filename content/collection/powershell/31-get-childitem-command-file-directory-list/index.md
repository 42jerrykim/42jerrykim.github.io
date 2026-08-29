---
draft: true
collection_order: 31
slug: get-childitem-command-file-directory-list-powershell
title: "[PowerShell] 31. Get-ChildItem — 파일·디렉터리 목록"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-ChildItem(별칭 dir/ls)으로 파일·디렉터리·레지스트리 키를 조회하는 법과 -Recurse/-Depth/-Filter/-Include/-Exclude/-Force 매개변수, -Filter가 -Include보다 빠른 이유를 정리한 챕터다."
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
- Get-ChildItem
- Recursion
- Wildcard
- Filter
- Symbolic-Link
- Registry
image: "wordcloud.png"
---

## 개요

`Get-ChildItem`(별칭 `dir`, `ls`, `gci`)은 지정한 위치의 항목과 그 하위 항목(child item)을 가져오는 cmdlet이다. 30장에서 다룬 프로바이더 계층 덕분에 파일 시스템뿐 아니라 레지스트리 키, 인증서 저장소에서도 똑같이 동작한다.

## 사용법

```powershell
Get-ChildItem [[-Path] <String[]>] [[-Filter] <String>] [-Include <String[]>] [-Exclude <String[]>] [-Recurse] [-Depth <UInt32>] [-Force] [-Name]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Path` | 대상 위치(생략 시 현재 디렉터리) |
| `-Filter` | FileSystem 프로바이더가 항목을 가져오는 시점에 직접 적용하는 필터. `*`, `?`만 지원하지만 `-Include`보다 빠르다 |
| `-Include` / `-Exclude` | PowerShell이 항목을 다 가져온 뒤에 적용하는 필터. `[]` 패턴까지 지원하지만 `-Path`가 `\*`로 끝나야 하거나 `-Recurse`가 필요하다 |
| `-Recurse` | 하위 디렉터리까지 재귀적으로 탐색 |
| `-Depth` | 재귀 시 몇 단계까지 내려갈지 제한(PowerShell 5+) |
| `-Force` | 숨김·시스템 파일까지 포함 |
| `-Directory` / `-File` / `-Hidden` / `-ReadOnly` / `-System` | FileSystem 전용 동적 매개변수로 특정 속성의 항목만 조회 |
| `-Attributes` | `!`(NOT), `+`(AND), `,`(OR) 연산자로 여러 파일 속성을 조합해 정교하게 필터링 |
| `-Name` | 전체 객체 대신 이름(문자열)만 반환 |

## 예시

```powershell
Get-ChildItem -Path C:\Test                          # 기본 목록
Get-ChildItem -Path C:\Test -Name                     # 이름만
Get-ChildItem -Path .\*.txt -Recurse -Force            # 하위 디렉터리까지, 숨김 파일 포함
Get-ChildItem -Path C:\Test -Filter '*.log'            # 프로바이더 수준 필터(빠름)
Get-ChildItem -Path C:\Test\* -Include *.txt           # PowerShell 필터(느리지만 유연)
Get-ChildItem -Path C:\Parent -Depth 2                 # 2단계 하위까지만 재귀
Get-ChildItem -Path HKLM:\HARDWARE                     # 레지스트리 키 조회
Get-ChildItem -Path Cert:\* -Recurse -CodeSigningCert  # 인증서 저장소(프로바이더 동적 매개변수)
Get-ChildItem -Attributes !Directory+!System+Encrypted # 복합 속성 조건
```

## 주의사항·함정

**`-Filter`와 `-Include`는 동작 위치와 속도가 다르다**: `-Filter`는 FileSystem 프로바이더(.NET API 수준)에서 항목을 열거하는 시점에 바로 적용되어 빠르지만, 지원하는 와일드카드가 `*`/`?`로 제한적이다. `-Include`/`-Exclude`는 일단 모든 항목을 가져온 뒤 PowerShell이 다시 걸러내므로 유연하지만 느리다. 대용량 디렉터리에서는 `-Filter`를 우선 검토한다.

**`-Include`를 쓰려면 `-Path`가 내용물을 가리켜야 한다**: `-Path C:\Test -Include *.txt`는 아무 결과도 안 준다. `-Path C:\Test\* -Include *.txt`처럼 끝에 `*`를 붙이거나 `-Recurse`를 함께 써야 `-Include`가 실제로 적용된다.

**`-Recurse`와 `-Path`의 와일드카드를 같이 쓸 때는 동작이 미묘하다**: `-Path`의 마지막 구성 요소가 실제 하위 디렉터리 이름과 일치하면 그 디렉터리부터 재귀하고, 일치하지 않으면 패턴으로 취급해 전체를 재귀 탐색한다. 예측 가능한 결과가 필요하면 `-LiteralPath`로 대상 디렉터리를 지정하고 `-Filter`/`-Include`로 패턴을 걸어야 한다.

**심볼릭 링크는 기본적으로 따라가지 않는다**: `-Recurse` 중 만난 디렉터리 심볼릭 링크는 표시만 되고 그 안으로 들어가지 않는다. 링크 대상까지 탐색하려면 `-FollowSymlink`(FileSystem 동적 매개변수, PowerShell 6+)를 추가한다.

**이식성**: CMD `dir`의 `/S`(재귀)·`/A`(속성)·`/B`(이름만)에 각각 `-Recurse`·`-Attributes`·`-Name`이 대응하고, Bash `find`의 `-maxdepth`에 `-Depth`가 대응한다. 다만 PowerShell의 `dir` 별칭에 CMD 스위치를 그대로 넘기면 인식되지 않는다 — 00장에서 짚었듯 별칭은 이름만 같을 뿐 완전히 다른 구현이다.

## Reference

- [Get-ChildItem (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem)
