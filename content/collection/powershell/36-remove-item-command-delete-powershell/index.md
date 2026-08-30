---
draft: false
collection_order: 36
slug: remove-item-command-delete-powershell
title: "[PowerShell] 36. Remove-Item — 삭제"
date: 2026-08-29
lastmod: 2026-08-29
description: "Remove-Item으로 파일·디렉터리·레지스트리 키를 삭제하는 법과 -Recurse의 알려진 이슈, 디렉터리 삭제 시 -Confirm:$false로도 우회되지 않는 확인 프롬프트, -Stream으로 대체 데이터 스트림만 지우는 법을 정리한 챕터다."
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
- Remove-Item
- Registry
- Alternate-Data-Stream
- Get-ChildItem
- Confirm
- Backup
image: "wordcloud.png"
---

## 개요

`Remove-Item`은 파일, 디렉터리, 레지스트리 키, 변수, 별칭, 함수 등 여러 프로바이더가 노출하는 항목을 삭제하는 cmdlet이다. 삭제는 복구가 기본적으로 지원되지 않는 작업이므로, 이 컬렉션의 다른 어떤 cmdlet보다도 실행 전 확인이 중요하다.

## 사용법

```powershell
Remove-Item [-Path] <String[]> [-Recurse] [-Force] [-Filter <String>] [-Include <String[]>] [-Exclude <String[]>] [-Confirm] [-WhatIf]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Recurse` | 하위 항목까지 재귀적으로 삭제 |
| `-Force` | 숨김·읽기 전용 항목도 삭제(보안 제한까지 무시하지는 못함) |
| `-Filter` / `-Include` / `-Exclude` | 31장·34장과 같은 규칙 |
| `-Stream`(FileSystem 동적 매개변수, Windows) | NTFS 대체 데이터 스트림(예: `Zone.Identifier`)만 삭제. `-Recurse`와 함께 쓸 수 없다 |
| `-DeleteKey`(Certificate 동적 매개변수) | 인증서 삭제 시 개인 키도 함께 삭제 |

## 예시

```powershell
Remove-Item -Path C:\Test\hidden-RO-file.txt -Force        # 숨김·읽기전용 파일 삭제
Remove-Item HKLM:\Software\MyCompany\OldApp -Recurse       # 레지스트리 키와 하위 키·값 전체 삭제

# -Recurse의 알려진 이슈를 피하는 권장 패턴
Get-ChildItem * -Include *.csv -Recurse | Remove-Item

# 대괄호 등 특수문자가 포함된 파일명은 -LiteralPath로
Get-ChildItem | Where-Object Name -Like '*`[*' | ForEach-Object { Remove-Item -LiteralPath $_.Name }

# 인터넷 차단 표시(대체 데이터 스트림)만 제거
Remove-Item C:\Test\Copy-Script.ps1 -Stream Zone.Identifier
```

## 주의사항·함정

**`-Path`에 확장자를 넣고 `-Recurse`를 쓰면 예상과 다르게 동작할 수 있다(알려진 이슈)**: `Remove-Item -Path *.csv -Recurse`처럼 경로에 파일 형식을 직접 지정하면, cmdlet이 "자식이 없는 파일 하나를 찾는 중"이라고 오인해 `-Recurse`가 제대로 동작하지 않을 수 있다(Windows 1909부터는 개선됐지만 모든 환경에서 보장되지는 않는다). `Get-ChildItem -Include *.csv -Recurse | Remove-Item`처럼 먼저 대상을 찾아 파이프로 넘기는 패턴이 항상 안전하다.

**디렉터리 삭제 확인은 `-Confirm:$false`로도 우회되지 않는다**: 내용이 있는 디렉터리를 `-Recurse` 없이 지우려 하면 PowerShell은 항상 확인을 묻는다 — 이는 의도된 설계이며, `-Confirm:$false`를 붙여도 이 프롬프트는 사라지지 않는다. 스크립트에서 무인 실행이 필요하다면 애초에 `-Recurse`를 명시해야 한다.

**`-Exclude`는 `-Recurse` 중 발견된 하위 항목의 부모까지는 보호하지 못한다**: `-Recurse`와 `-Exclude`를 함께 쓸 때, `-Exclude`는 현재 디렉터리 결과에만 적용된다. 하위 폴더 안에 제외 패턴과 일치하는 파일이 있어도, 그 파일이 속한 상위 디렉터리 자체가 삭제 대상이면 함께 지워진다.

**이식성**: CMD의 `del`/`rd`, Bash의 `rm`/`rmdir`에 대응하지만, PowerShell은 레지스트리 키·별칭·변수처럼 파일이 아닌 항목까지 같은 cmdlet으로 삭제한다. 세 환경 모두 삭제가 기본적으로 복구 불가능한 작업이라는 점은 동일하다 — 실행 전 `-WhatIf`로 대상을 먼저 확인하는 습관은 어느 셸에서든 유효하다.

## Reference

- [Remove-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/remove-item)
