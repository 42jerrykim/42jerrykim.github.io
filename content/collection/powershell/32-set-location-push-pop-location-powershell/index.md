---
draft: false
collection_order: 32
slug: set-location-push-pop-location-powershell
title: "[PowerShell] 32. Set-Location/Push-Location/Pop-Location"
date: 2026-08-29
lastmod: 2026-08-29
description: "Set-Location(별칭 cd)으로 현재 위치를 바꾸는 법과 -/+로 위치 히스토리를 오가는 법, Push-Location/Pop-Location 위치 스택으로 여러 작업 디렉터리를 오가는 법, 이름 붙인 스택(-StackName)을 정리한 챕터다."
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
- Set-Location
- Push-Location
- Pop-Location
- Location-Stack
- Runspace
- Working-Directory
image: "wordcloud.png"
---

## 개요

`Set-Location`(별칭 `cd`, `chdir`, `sl`)은 현재 작업 위치를 바꾸는 cmdlet이다. 30장의 프로바이더 개념 덕분에 파일 시스템 디렉터리든 레지스트리 키든 인증서 저장소든 같은 명령으로 이동한다. `Push-Location`/`Pop-Location`은 여기에 "스택"이라는 기억 장치를 더해, 여러 작업 위치를 오가면서도 원래 있던 곳으로 정확히 돌아올 수 있게 해 준다.

## 사용법

```powershell
Set-Location [[-Path] <String>] [-PassThru]
Push-Location [[-Path] <String>] [-StackName <String>] [-PassThru]
Pop-Location [-StackName <String>] [-PassThru]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Path` | 이동할 위치. `-`는 방문 히스토리의 이전 위치, `+`는 다음 위치를 가리킨다(PowerShell 6.2+, 최근 20개까지 자동 기록) |
| `-StackName` | 사용할 위치 스택 이름. 지정하지 않으면 이름 없는 기본 스택을 쓴다 |
| `-PassThru` | 이동 결과(`PathInfo` 객체)를 반환한다(기본은 출력 없음) |

**위치 스택**은 후입선출(LIFO) 구조다. `Push-Location`으로 현재 위치를 스택에 쌓아 두고 다른 곳으로 이동한 뒤, `Pop-Location`으로 스택 맨 위에 쌓인 위치로 돌아온다. `Set-Location -`/`+`가 만드는 자동 히스토리(최근 20개, 순차 목록)와는 별개의 메커니즘이라는 점에 주의한다.

## 예시

```powershell
Set-Location -Path "HKLM:\"                 # 레지스트리 드라이브로 이동
cd C:\Windows                                # 별칭 사용
cd -                                         # 방금 전 위치로(히스토리)
cd +                                         # 다시 앞으로

Push-Location -Path "C:\Program Files"       # 현재 위치를 쌓고 이동
Pop-Location                                 # 쌓아 둔 위치로 복귀

Push-Location -Path "C:\Logs" -StackName "Work"   # 이름 붙인 스택 사용
Set-Location -StackName "Work"                    # 이 스택을 현재 스택으로 지정
Get-Location -Stack                               # 현재 스택의 위치 목록 확인
```

## 주의사항·함정

**`Set-Location`의 `-`/`+` 히스토리와 위치 스택은 서로 다른 목록이다**: 히스토리는 PowerShell이 자동으로 기록하는 순차 목록(최근 20개)이고, 스택은 `Push-Location`/`Pop-Location`으로 사람이 명시적으로 관리하는 후입선출 구조다. 둘을 혼동하면 "분명히 넣었는데 안 나온다"는 혼란이 생긴다.

**PowerShell은 런스페이스마다 별도의 현재 디렉터리를 가진다**: `Set-Location`으로 바꾼 위치는 그 PowerShell 세션(런스페이스) 안에서만 유효하며, `[System.Environment]::CurrentDirectory` 같은 프로세스 전역 값과는 다르다. .NET API를 직접 호출하거나 인자 없이 상대 경로로 네이티브 프로그램을 실행할 때 이 차이가 예상과 다른 동작을 일으킬 수 있다.

**이름 붙인 스택으로 전환하면 기본 스택 접근이 제한된다**: `Set-Location -StackName`으로 다른 스택을 현재 스택으로 만들면, 그 상태에서는 이름 없는 기본 스택에 `Push-Location`/`Pop-Location`을 직접 쓸 수 없다. 기본 스택으로 되돌리려면 `Set-Location -StackName $null`(또는 빈 문자열)을 쓴다.

**이식성**: Bash의 `cd -`(이전 디렉터리), `pushd`/`popd`(디렉터리 스택)와 이름·역할이 거의 그대로 대응한다. CMD도 05장(CMD 컬렉션 기준 11장)의 `pushd`/`popd`가 있지만 이름 붙인 다중 스택은 지원하지 않는다 — PowerShell의 `-StackName`은 여러 작업 맥락을 동시에 오가야 할 때 이 CMD·Bash 버전보다 더 유연하다.

## Reference

- [Set-Location (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location)
