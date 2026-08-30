---
draft: false
collection_order: 4
slug: get-set-new-alias-command-powershell
title: "[PowerShell] 04. Get-Alias/Set-Alias/New-Alias — 별칭 시스템"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 별칭 시스템의 동작 원리와 Get-Alias·Set-Alias·New-Alias 사용법, ReadOnly/Constant 옵션으로 별칭을 보호하는 법, 매개변수가 있는 명령에 별칭을 만들 때 함수가 필요한 이유를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
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
- Configuration(설정)
- DevOps
- Alias
- Get-Alias
- Set-Alias
- New-Alias
- Profile
- Scope
image: "wordcloud.png"
---

## 개요

<strong>별칭(alias)</strong>은 cmdlet·함수·스크립트·실행 파일을 가리키는 짧은 대체 이름이다. `dir`이 `Get-ChildItem`을, `cat`이 `Get-Content`를, `%`가 `ForEach-Object`를 가리키는 식이다. PowerShell은 CMD·Bash 사용자가 익숙한 이름을 그대로 입력해도 동작하도록 이런 별칭을 미리 만들어 두었지만, 별칭은 어디까지나 진짜 명령을 가리키는 이름표일 뿐 별도의 명령이 아니다.

정신 모델은 "별칭은 포인터다"라는 것이다. `Get-Alias`로 그 포인터가 무엇을 가리키는지 확인하고, `Set-Alias`/`New-Alias`로 새 포인터를 만들거나 기존 포인터의 대상을 바꾼다. 다만 포인터는 명령 이름 하나만 가리킬 수 있고 매개변수까지는 담을 수 없다 — `Set-Location -Path C:\Windows\System32` 전체를 별칭으로 만들 수는 없고, 그런 조합이 필요하면 먼저 함수로 감싸야 한다.

이 제약은 설계 실수가 아니라 의도된 것이다. 별칭 객체(`AliasInfo`)는 대상 명령 이름 하나만 `Definition` 속성에 저장하도록 설계되어 있어, 매개변수까지 포함한 임의의 명령줄 조합을 담을 자리가 애초에 없다. 그래서 "매개변수가 붙은 짧은 명령"이 필요하면 그 조합을 함수로 먼저 정의하고, 별칭은 그 함수 하나만 가리키게 하는 두 단계 구성이 PowerShell에서 유일하게 통하는 방법이다.

## 사용법

```powershell
Get-Alias [[-Name] <String[]>] [-Definition <String[]>] [-Scope <String>]
Set-Alias [-Name] <String> [-Value] <String> [-Option <ScopedItemOptions>] [-Scope <String>] [-Force]
New-Alias [-Name] <String> [-Value] <String> [-Option <ScopedItemOptions>] [-Scope <String>]
```

`Get-Alias`는 기본적으로 별칭 이름을 넣으면 대상 명령을, `-Definition`을 쓰면 반대로 명령 이름을 넣어 그 명령의 별칭들을 찾는다. `Set-Alias`는 별칭이 없으면 새로 만들고 있으면 대상을 바꾸며, `New-Alias`는 이미 존재하는 별칭 이름으로 실행하면 오류를 낸다(단 `-Force`를 쓰면 `Set-Alias`처럼 동작한다).

## 매개변수

| 매개변수 | 대상 cmdlet | 설명 |
|---|---|---|
| `-Name` | 셋 다 | 별칭 이름(숫자로 시작할 수 없다) |
| `-Value` | Set/New | 별칭이 가리킬 cmdlet·함수·실행 파일 이름 |
| `-Definition` | Get | 명령 이름으로 그 명령의 별칭을 역으로 검색 |
| `-Option` | Set/New | `ReadOnly`(Force 없이는 변경·삭제 불가), `Constant`(Force로도 불가), `Private`(현재 스코프에서만 유효), `AllScope`(하위 스코프에 상속) |
| `-Scope` | 셋 다 | `Global`/`Local`/`Script`/숫자. 기본은 `Local`(현재 스코프) |
| `-Force` | Set/New | `ReadOnly` 별칭을 변경하거나, `New-Alias`가 기존 별칭을 덮어쓰게 한다 |
| `-PassThru` | Set/New | 기본적으로 출력이 없는 두 cmdlet이 결과 객체를 반환하게 한다 |

## 예시

```powershell
Get-Alias                                     # 세션의 모든 별칭
Get-Alias -Name gc*, gci                      # 이름이 gc로 시작하거나 gci인 별칭
Get-Alias -Definition Get-ChildItem           # Get-ChildItem을 가리키는 모든 별칭(dir, gci, ls)
Set-Alias -Name list -Value Get-ChildItem     # list라는 새 별칭 생성
Set-Alias -Name loc -Value Get-Location -Option ReadOnly -PassThru | Format-List *
New-Alias -Name np -Value C:\Windows\notepad.exe   # 실행 파일에 대한 별칭
function Set-ParentDirectory { Set-Location -Path .. }
New-Alias -Name .. -Value Set-ParentDirectory      # 매개변수 조합이 필요하면 함수로 감싼 뒤 별칭 연결
Get-Alias | Where-Object { $_.Options -match "ReadOnly" }   # 내장 별칭(읽기 전용)만 필터링
Remove-Item -Path Alias:list                  # 별칭 삭제(PowerShell 6+는 Remove-Alias도 사용 가능)
```

## 주의사항·함정

**별칭은 현재 세션에서만 유지된다**: `Set-Alias`·`New-Alias`로 만든 별칭은 세션을 닫으면 사라진다. 매번 쓰고 싶은 별칭이라면 06장에서 다루는 프로파일 스크립트(`$PROFILE`)에 등록해야 한다.

**대화형 편의와 스크립트 가독성은 다른 문제다**: `dir`, `ls`, `%`, `?` 같은 별칭은 콘솔에서 타이핑을 줄여주지만, 공유·재사용되는 스크립트에서는 `Get-ChildItem`, `ForEach-Object`, `Where-Object`처럼 전체 이름을 쓰는 것이 PowerShell 커뮤니티의 관례다. 별칭은 로캘·모듈 구성에 따라 다르게 정의될 수 있어, 다른 사람의 환경에서 스크립트를 실행했을 때 예상과 다르게 동작할 위험이 있다.

**내장 별칭은 대부분 읽기 전용이다**: PowerShell이 기본 제공하는 별칭(`dir`, `cat`, `cd` 등)은 `ReadOnly` 옵션이 걸려 있어 실수로 덮어쓰기 어렵게 되어 있다. 굳이 바꿔야 한다면 `-Force`가 필요하지만, 다른 사람도 쓰는 공용 스크립트·모듈에서는 내장 별칭 재정의를 피하는 것이 안전하다.

**이식성**: Bash의 `alias`/`unalias`는 셸 함수에 가까운 텍스트 치환이라 매개변수를 포함한 전체 명령(`alias ll='ls -la'`)을 별칭으로 만들 수 있지만, PowerShell 별칭은 명령 이름만 가리킬 수 있어 매개변수가 필요하면 반드시 함수를 거쳐야 한다는 점이 근본적으로 다르다. CMD에는 별칭 개념 자체가 없고 `doskey` 매크로가 비슷한 역할을 한다.

## Reference

- [Set-Alias (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/set-alias)
- [Get-Alias (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-alias)
