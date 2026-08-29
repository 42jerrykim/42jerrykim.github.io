---
draft: true
collection_order: 28
slug: add-member-command-custom-object-properties-powershell
title: "[PowerShell] 28. Add-Member — 커스텀 객체에 속성·메서드 추가"
date: 2026-08-29
lastmod: 2026-08-29
description: "Add-Member로 기존 객체 인스턴스에 NoteProperty·ScriptMethod·AliasProperty를 추가하는 법, -NotePropertyMembers/-PassThru 매개변수, $this 자동 변수로 스크립트 메서드를 작성하는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
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
- Add-Member
- NoteProperty
- ScriptMethod
- PSObject
- Extensible-Type-System
- Get-Item
- Export-Clixml
image: "wordcloud.png"
---

## 개요

`Add-Member`는 이미 존재하는 객체 **인스턴스 하나**에 속성이나 메서드를 추가하는 cmdlet이다. 27장의 `[PSCustomObject]`가 객체를 처음부터 새로 만드는 방법이라면, `Add-Member`는 `Get-Item`이 반환한 파일 객체처럼 이미 만들어진 객체에 임시로 정보를 덧붙이는 방법이다. 이 확장은 PowerShell의 확장 타입 시스템(Extensible Type System, ETS)을 통해 이뤄지며, 원본 .NET 타입 자체를 바꾸지 않고 그 객체의 이 인스턴스에만 적용된다.

이렇게 덧붙인 값은 그 객체가 살아 있는 동안(변수에 담겨 있거나 파이프라인을 흘러가는 동안)에만 유지된다. 세션을 넘어 값을 보존하고 싶다면 `Export-Clixml`로 확장된 인스턴스를 파일에 직렬화해 두고, 나중에 `Import-Clixml`로 다시 읽어 들이면 추가했던 멤버까지 그대로 복원된다 — `Add-Member`가 원본 타입 정의를 바꾸는 것이 아니라 인스턴스에 값을 얹는 것임을 보여주는 또 다른 단면이다.

## 사용법

```powershell
<객체> | Add-Member -NotePropertyName <String> -NotePropertyValue <Object>
<객체> | Add-Member -NotePropertyMembers <IDictionary>
<객체> | Add-Member -MemberType <PSMemberTypes> -Name <String> -Value <Object> [-SecondValue <Object>]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-MemberType`(별칭 `-Type`) | `NoteProperty`, `AliasProperty`, `ScriptProperty`, `ScriptMethod`, `CodeProperty`, `CodeMethod` 중 하나 |
| `-Name` / `-Value` | 추가할 멤버 이름과 값(또는 스크립트블록) |
| `-NotePropertyName` / `-NotePropertyValue` | 단일 NoteProperty를 더 간결하게 추가(PowerShell 3+) |
| `-NotePropertyMembers` | 여러 NoteProperty를 해시테이블로 한 번에 추가 |
| `-SecondValue` | `AliasProperty`의 변환 타입, 또는 `ScriptProperty`의 Set 접근자 스크립트블록 |
| `-Force` | 같은 이름의 멤버가 이미 있으면 덮어쓴다 |
| `-PassThru` | 확장된 객체를 반환한다(문자열처럼 `Add-Member`가 원본을 직접 바꿀 수 없는 타입에는 필수) |

## 예시

```powershell
$file = Get-ChildItem C:\ps-test\test.txt
$file | Add-Member -NotePropertyName Status -NotePropertyValue Done
$file.Status                                             # Done

$file | Add-Member -MemberType AliasProperty -Name Size -Value Length
$file.Size                                                # Length 값과 동일

# 문자열처럼 원본을 직접 바꿀 수 없는 타입은 -PassThru가 필요
$s = "A string"
$s = $s | Add-Member -NotePropertyMembers @{StringUse = "Display"} -PassThru

# $this로 현재 인스턴스를 참조하는 스크립트 메서드
$sizeInMB = { [Math]::Round(($this.Length / 1MB), 2) }
$file | Add-Member -MemberType ScriptMethod -Name SizeInMB -Value $sizeInMB
$file.SizeInMB()

# ScriptProperty로 get/set 접근자 둘 다 정의(중첩 속성 접근을 감싸는 용도)
$user = [pscustomobject]@{ Position = [pscustomobject]@{ Role = 'Manager' } }
$user | Add-Member -MemberType ScriptProperty -Name Title `
    -Value { $this.Position.Role } `
    -SecondValue { $this.Position.Role = $args[0] }
$user.Title = 'Dev Manager'   # Set 접근자를 통해 중첩 속성이 갱신된다
```

## 주의사항·함정

**`Add-Member`는 원본 .NET 타입을 바꾸지 않는다**: 확장은 그 인스턴스 하나에만 적용되며, 같은 타입의 다른 인스턴스에는 영향을 주지 않는다. 같은 타입 전체에 새 속성을 일관되게 추가하고 싶다면 `Types.ps1xml` 파일이나 `Update-TypeData`를 쓰는 것이 맞는 방법이다.

**문자열 같은 원시 타입에는 `-PassThru`가 필수다**: `[string]` 같은 원시 타입은 `Add-Member`가 원본 객체에 직접 멤버를 추가할 수 없다. `-PassThru`로 새 객체를 받아 변수에 다시 대입해야 확장된 결과를 계속 쓸 수 있다.

**속성이 추가된 순서는 `Get-Member`가 아니라 `.psobject.Properties`로 확인해야 한다**: 11장에서 다뤘듯 `Get-Member`는 알파벳순으로 결과를 정렬한다. `Add-Member`로 추가한 순서 그대로 보고 싶다면 `$object.psobject.Properties`를 순회해야 한다.

**`$this`는 스크립트 메서드·스크립트 속성 정의 안에서만 유효하다**: 그 바깥에서 `$this`를 참조하면 아무 의미가 없거나 다른 컨텍스트의 값을 가리킨다. `$this`는 멤버를 정의하는 스크립트블록 안에서 "이 멤버가 붙은 객체 자신"을 가리키는 특수한 참조다.

**이식성**: JavaScript 객체에 프로퍼티를 동적으로 추가하는 것과 개념은 비슷하지만, PowerShell의 `Add-Member`는 `AliasProperty`·`ScriptMethod`처럼 강타입 .NET 위에서 동작하는 멤버 종류를 명시적으로 구분해 정의한다는 점이 다르다. CMD·Bash에는 이런 객체 확장 개념 자체가 없다.

## Reference

- [Add-Member (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/add-member)
