---
draft: true
collection_order: 11
slug: get-member-command-object-structure-powershell
title: "[PowerShell] 11. Get-Member — 객체 구조 탐색"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Member(별칭 gm)로 파이프라인 객체의 속성·메서드를 탐색하는 법과 -MemberType/-View 매개변수, psbase/psobject 같은 내재 멤버, Add-Member로 확장된 멤버의 관계를 정리한 챕터다."
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
- Get-Member
- Property
- Method
- MemberType
- Add-Member
- Introspection
- Get-Process
image: "wordcloud.png"
---

## 개요

`Get-Member`(별칭 `gm`)는 객체의 속성(Property)과 메서드(Method)를 조회하는 cmdlet이다. 10장에서 확인했듯 PowerShell 파이프라인은 텍스트가 아닌 객체를 주고받으므로, "이 객체에 무엇이 들어 있는지" 알아야 `Where-Object`·`Select-Object`로 무엇을 거르고 뽑을지 판단할 수 있다. `Get-Member`는 그 정찰 역할을 하는 첫 번째 도구이며, PowerShell을 배우는 사람이 낯선 cmdlet의 결과를 마주칠 때 가장 먼저 실행해야 할 명령이다.

정신 모델은 "모든 파이프라인 객체는 `| Get-Member`로 뜯어볼 수 있는 블랙박스"라는 것이다. 결과에는 메서드가 먼저, 속성이 나중에 알파벳순으로 나열되며, 각 줄의 `Definition` 열에 실제 .NET 타입 시그니처가 그대로 노출된다 — 이 정보만으로 그 객체가 어떤 .NET 클래스의 인스턴스인지, 어떤 값을 읽고 쓸 수 있는지 파악할 수 있다.

## 사용법

```powershell
Get-Member [[-Name] <String[]>] [-InputObject <PSObject>] [-MemberType <PSMemberTypes>] [-View <PSMemberViewTypes>] [-Static] [-Force]
```

가장 흔한 패턴은 조사하려는 명령의 결과를 그대로 파이프로 넘기는 것이다: `<명령> | Get-Member`.

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Name` | 조회할 멤버 이름을 좁힌다(와일드카드 미지원) |
| `-MemberType`(별칭 `-Type`) | `Property`, `Method`, `NoteProperty`, `ScriptProperty`, `AliasProperty` 등으로 멤버 종류를 필터링한다 |
| `-View` | `Base`(원본 .NET 멤버만), `Adapted`(PowerShell 확장 타입 시스템), `Extended`(`Types.ps1xml`나 `Add-Member`로 추가된 멤버), `All` 중 어느 계층의 멤버를 볼지 선택한다. 기본값은 `Adapted, Extended` |
| `-Static` | 인스턴스가 아니라 클래스 자체에 속한 정적 멤버를 조회한다 |
| `-Force` | `psbase`, `psobject`, `pstypenames` 같은 내재 멤버(intrinsic member)까지 표시한다 |
| `-InputObject` | 컬렉션을 파이프 대신 이 매개변수로 넘기면, 개별 요소가 아니라 컬렉션 자체의 멤버를 조회한다(11장 전체에서 반복되는 파이프 vs `-InputObject` 차이) |

## 예시

```powershell
Get-Service | Get-Member                              # 서비스 객체의 속성·메서드 전체
Get-Process | Get-Member -MemberType Property          # 속성만
Get-WinEvent -LogName System -MaxEvents 1 | Get-Member -MemberType NoteProperty
$array = @(1, 'hello')
$array | Get-Member                                    # 서로 다른 타입마다 별도로 표시(Int32, String)
Get-Member -InputObject $array                          # 배열 자체(Object[])의 멤버로 표시
Get-Service | Get-Member -Force                         # psbase 등 내재 멤버까지 표시
(Get-Item C:\test\file.txt).psobject.Properties | Where-Object IsSettable | Select-Object Name   # 변경 가능한 속성만 골라내기
```

## 주의사항·함정

**파이프 vs `-InputObject`는 결과가 다르다**: 컬렉션을 파이프로 넘기면 각 요소를 하나씩 조사하지만, `-InputObject`로 넘기면 컬렉션 자체(예: `System.Object[]`)를 하나의 객체로 조사한다. 배열 안 개별 요소의 구조가 궁금하다면 반드시 파이프를 써야 한다.

**중복 타입은 한 번만 표시된다**: 같은 타입의 객체 여러 개를 파이프로 넘기면 `Get-Member`는 타입별로 한 번만 결과를 보여준다 — 100개의 프로세스를 넘겨도 `System.Diagnostics.Process` 타입 설명은 한 번만 나온다.

**속성 순서는 알파벳순이지, 추가된 순서가 아니다**: `Add-Member`로 속성을 추가한 순서를 그대로 보고 싶다면 `Get-Member` 대신 `$object.psobject.Properties`를 직접 순회해야 한다.

**이식성**: CMD·Bash에는 "이 값의 구조가 무엇인지" 물어보는 대응 개념 자체가 없다 — 텍스트에는 애초에 구조가 없기 때문이다. 굳이 비교하면 동적 타입 언어의 리플렉션(Python의 `dir()`, JavaScript의 `Object.keys()`)이 `Get-Member`와 목적이 가장 비슷하다.

## Reference

- [Get-Member (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-member)
