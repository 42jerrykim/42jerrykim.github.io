---
draft: false
collection_order: 3
slug: get-command-cmdlet-search-powershell
title: "[PowerShell] 03. Get-Command — cmdlet 검색"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Command로 설치된 cmdlet·함수·별칭·애플리케이션을 동사·명사·모듈 기준으로 검색하는 법, Verb-Noun 이름 규칙, dir 같은 별칭이 실제로 가리키는 명령을 확인하는 법까지 정리한 PowerShell 입문 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
- .NET
- Automation(자동화)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- DevOps
- Naming-Convention
- Verb-Noun
- Get-Command
- Module
- PATH
- Alias
image: "wordcloud.png"
---

## 개요

`Get-Command`는 로컬 컴퓨터에 설치된 모든 명령 — cmdlet, 별칭, 함수, 필터, 스크립트, 애플리케이션 — 을 검색하는 cmdlet이다. CMD의 `where`나 Bash의 `which`가 실행 파일 하나의 경로만 찾아주는 것과 달리, `Get-Command`는 PowerShell 세션이 인식하는 모든 종류의 명령을 대상으로 동사·명사·모듈·매개변수 이름까지 기준으로 검색할 수 있다.

이 cmdlet이 성립하는 배경에는 PowerShell의 `Verb-Noun` 명명 규칙이 있다. `Get-Process`, `Set-Location`, `New-Item`처럼 거의 모든 cmdlet 이름은 승인된 동사(`Get`, `Set`, `New`, `Remove`, `Add` 등)와 명사의 조합이다. 이 규칙 덕분에 "프로세스와 관련된 명령이 뭐가 있지?"라는 질문을 `Get-Command -Noun Process`라는 구체적인 검색으로 바꿀 수 있다. `Get-Command`는 도움말 파일이 아니라 명령 코드 자체에서 정보를 가져오므로(`Get-Help`와의 차이), 도움말이 설치되지 않은 명령도 검색할 수 있다.

## 사용법

```powershell
Get-Command [[-Name] <String[]>] [-Verb <String[]>] [-Noun <String[]>] [-Module <String[]>] [-CommandType <CommandTypes>] [-Syntax] [-All] [<CommonParameters>]
```

매개변수 없이 실행하면 세션에 설치된 모든 cmdlet·함수·별칭을 나열한다. `Get-Command *`는 `$Env:PATH`에 있는 비-PowerShell 실행 파일(Application 타입)까지 포함한 전체 목록을 반환한다.

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Name` | 검색할 명령 이름. 와일드카드를 지원하며, 하이픈 없는 정확한 이름을 넘기면 해당 모듈을 자동으로 가져온다(import) |
| `-Verb` / `-Noun` | 동사·명사로 cmdlet을 검색한다. 둘 다 지정하면 AND 조건으로 좁혀진다 |
| `-Module` | 지정한 모듈에 속한 명령만 검색한다 |
| `-CommandType`(별칭 `-Type`) | `Alias`, `Cmdlet`, `Function`, `ExternalScript`, `Application` 등 명령 종류로 필터링한다 |
| `-Syntax` | 별칭은 원래 이름을, cmdlet은 문법을, 함수는 정의를, 스크립트는 경로를 간략히 보여준다 |
| `-All` | 이름이 같은 명령이 여러 개 있을 때 실행 우선순위 전체를 보여준다(기본은 실제 실행되는 것 하나만) |
| `-ParameterName` / `-ParameterType` | 특정 이름·타입의 매개변수를 가진 명령을 검색한다(현재 세션에 로드된 명령만 대상) |
| `-ListImported` | 도움말 파일이 아니라 현재 세션에 이미 임포트된 명령만 검색한다 |

## 예시

```powershell
Get-Command                                   # 세션의 모든 cmdlet·함수·별칭
Get-Command -Verb Get -Noun Process           # Get-Process 검색
Get-Command -Noun Service                     # 명사가 Service인 모든 명령(Get/Start/Stop/Restart-Service 등)
Get-Command -Module Microsoft.PowerShell.Security   # 특정 모듈이 제공하는 명령 목록
Get-Command -Name dir                         # 별칭 dir이 가리키는 실제 명령 확인
Get-Command -Name dir -Syntax                 # dir 별칭의 실제 문법(Get-ChildItem 문법)
Get-Command -Type Cmdlet | Sort-Object Noun | Format-Table -GroupBy Noun   # 명사별로 그룹화해 훑어보기
(Get-Command Get-Date).ModuleName             # Get-Date가 속한 모듈 이름 확인
Get-Command get-commnd -UseFuzzyMatching      # 오타를 허용하는 유사 검색(PowerShell 7.4+)
```

## 주의사항·함정

**같은 이름의 명령이 여러 개일 때**: 세션에 이름이 같은 명령이 여럿 있으면(예: 사용자 정의 함수가 내장 cmdlet과 이름이 같은 경우), `Get-Command`는 기본적으로 실제로 실행될 하나만 보여준다. 실행 우선순위 전체를 보고 싶다면 `-All`을 쓴다.

**별칭 검색 결과 해석**: `Get-Command -Name dir`은 `CommandType: Alias`, `Name: dir -> Get-ChildItem` 형태로 결과를 보여준다. 이 결과를 보고 "dir이라는 명령이 따로 있다"고 착각하기 쉽지만, 실제로는 `Get-ChildItem`을 가리키는 포인터일 뿐이며 `dir` 자체에는 CMD의 `/A`, `/S` 같은 스위치가 없다.

**정확한 이름으로 검색하면 모듈이 자동 로드된다**: 와일드카드 없이 정확한 명령 이름으로 `Get-Command`를 실행하면, 해당 명령이 속한 모듈이 아직 임포트되지 않았어도 자동으로 임포트된다. 세션에 이미 로드된 명령만 보고 싶다면 `-ListImported`를 함께 써야 한다.

**이식성**: CMD의 `where`는 실행 파일 경로만 반환하고, Bash의 `which`/`type`은 별칭·함수·빌트인·실행 파일을 구분해 알려준다는 점에서 `Get-Command`와 목적이 비슷하다. 다만 `Get-Command`는 결과를 문자열이 아니라 `CmdletInfo`·`AliasInfo` 같은 객체로 반환하므로, `(Get-Command Get-Date).ModuleName`처럼 결과를 바로 다음 계산에 활용할 수 있다는 점이 근본적으로 다르다.

## Reference

- [Get-Command (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-command)
