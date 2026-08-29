---
draft: true
collection_order: 35
slug: move-rename-item-command-powershell
title: "[PowerShell] 35. Move-Item/Rename-Item — 이동과 이름 변경"
date: 2026-08-29
lastmod: 2026-08-29
description: "Move-Item으로 파일·디렉터리·레지스트리 키를 이동하는 법과 Rename-Item으로 이름만 바꾸는 법의 차이, Rename-Item이 경로 이동을 거부하는 이유, -NewName 스크립트블록으로 일괄 이름 변경하는 법을 정리한 챕터다."
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
- Move-Item
- Rename-Item
- Registry
- Batch-Rename
- Get-ChildItem
- Regex(정규표현식)
image: "wordcloud.png"
---

## 개요

`Move-Item`은 항목을 원본에서 삭제하고 새 위치에 추가하는 cmdlet이고, `Rename-Item`은 같은 위치에서 이름만 바꾸는 cmdlet이다. 34장의 `Copy-Item`이 "복사(원본 유지)"였다면, 이 둘은 "이동(원본 소멸)"과 "개명(위치 불변)"으로 각각 역할이 나뉜다.

## 사용법

```powershell
Move-Item [-Path] <String[]> [[-Destination] <String>] [-Force]
Rename-Item [-Path] <String> [-NewName] <String> [-Force]
```

## 매개변수

| 매개변수 | `Move-Item` | `Rename-Item` |
|---|---|---|
| `-Destination` / `-NewName` | 새 위치(경로+이름 가능) | 새 이름만(경로가 섞이면 오류) |
| `-Force` | 읽기 전용 항목도 이동, 기존 대상 덮어쓰기 | 읽기 전용 항목도 이름 변경(단 기존 이름 대체는 불가) |
| 재귀 여부 | 항상 재귀(디렉터리를 옮기면 내용물 전체가 함께 이동) | 해당 없음(이름만 바꾸므로 내용은 그대로) |

## 예시

```powershell
Move-Item -Path C:\test.txt -Destination E:\Temp\tst.txt   # 이동과 동시에 이름도 변경 가능
Move-Item -Path C:\Temp -Destination C:\Logs                # 디렉터리와 그 내용 전체 이동
Get-ChildItem -Path ".\*.txt" -Recurse | Move-Item -Destination "C:\TextFiles"

Move-Item "HKLM:\software\mycompany\*" "HKLM:\software\mynewcompany"   # 레지스트리 값 이동

Rename-Item -Path "daily_file.txt" -NewName "monday_file.txt"          # 단순 이름 변경
Rename-Item -Path "HKLM:\Software\MyCompany\Advertising" -NewName "Marketing"  # 레지스트리 키 이름 변경

# 여러 파일을 정규식으로 일괄 이름 변경
Get-ChildItem *.txt | Rename-Item -NewName { $_.Name -replace '\.txt$', '.log' }
```

## 주의사항·함정

**`Rename-Item`으로는 디렉터리를 옮길 수 없다**: `-NewName`에 경로가 섞인 값(`D:\archive\old-project.txt`)을 주면 "경로나 장치 이름을 나타내므로 이름을 바꿀 수 없다"는 오류가 난다. 이름을 바꾸면서 동시에 위치도 옮기고 싶다면 처음부터 `Move-Item -Destination`을 써야 한다.

**`Move-Item`은 파일은 드라이브를 넘나들지만 디렉터리는 같은 드라이브 안에서만 옮길 수 있다**: 서로 다른 드라이브(다른 물리 디스크) 사이에서 디렉터리 자체를 이동하려면 `Copy-Item -Recurse` 뒤 원본을 `Remove-Item`으로 지우는 두 단계가 필요할 수 있다.

**대상이 이미 있으면 두 cmdlet 모두 기본적으로 실패한다**: `Move-Item`의 대상 경로가 이미 존재하는 항목이면 오류가 나고, `-Force`로 덮어써야 한다. `Rename-Item`은 `-Force`를 줘도 이미 있는 이름으로는 절대 바꿀 수 없다 — 기존 항목을 대체해야 한다면 `Move-Item -Force`를 쓰라고 문서가 명시한다.

**대량 이동 중 이름이 겹치면 일부만 조용히 손실될 수 있다**: 여러 하위 디렉터리에 흩어진 동명 파일들을 한 디렉터리로 `Move-Item`하면, 먼저 이동한 파일 하나만 남고 나머지는 오류와 함께 원래 위치에 남는다. 대상 디렉터리가 이미 있는지, 이름 충돌 가능성이 있는지 사전에 확인해야 한다.

**이식성**: CMD의 `move`/`ren`, Bash의 `mv`(이동과 이름변경을 겸함)에 대응한다. Bash의 `mv`는 이동과 개명을 구분하지 않는 단일 명령이지만, PowerShell은 "위치가 바뀌는가"와 "이름만 바뀌는가"를 서로 다른 cmdlet으로 명시적으로 구분한다.

## Reference

- [Move-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/move-item)
- [Rename-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/rename-item)
