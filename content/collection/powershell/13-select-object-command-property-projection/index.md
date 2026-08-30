---
draft: false
collection_order: 13
slug: select-object-command-property-projection-powershell
title: "[PowerShell] 13. Select-Object — 속성 선택과 투영"
date: 2026-08-29
lastmod: 2026-08-29
description: "Select-Object로 객체의 특정 속성만 뽑거나 First/Last/Unique/Skip으로 개수를 제한하는 법, -ExpandProperty로 중첩 속성을 펼치는 법, 계산된 속성(Label/Expression)으로 새 열을 만드는 법을 정리한 챕터다."
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
- Select-Object
- Calculated-Property
- ExpandProperty
- Projection
- Get-Process
- PSCustomObject
- Database(데이터베이스)
image: "wordcloud.png"
---

## 개요

`Select-Object`는 객체에서 원하는 속성만 골라내거나, 컬렉션에서 원하는 개수·위치의 객체만 골라내는 cmdlet이다. `Where-Object`가 "어떤 객체를 통과시킬지"(행 필터링에 가깝다)를 결정한다면, `Select-Object`는 "그 객체의 어떤 속성을 남길지"(열 투영에 가깝다)를 결정한다 — 관계형 데이터베이스의 `WHERE`와 `SELECT`에 비유하면 이해가 쉽다.

정신 모델에서 중요한 것은 "속성을 선택하면 원본과 다른 새 객체가 만들어진다"는 점이다. `Select-Object -Property Name, Id`는 원본 프로세스 객체가 아니라 `Name`과 `Id`라는 `NoteProperty` 두 개만 가진 전혀 새로운 객체를 반환한다 — 그래서 이렇게 만든 객체에는 원본의 `Stop()` 같은 메서드가 남아 있지 않다.

## 사용법

```powershell
Select-Object [[-Property] <Object[]>] [-ExcludeProperty <String[]>] [-ExpandProperty <String>] [-First <Int32>] [-Last <Int32>] [-Skip <Int32>] [-Unique] [-Index <Int32[]>]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Property` | 남길 속성 이름(들). 계산된 속성(해시테이블 `@{Label=...; Expression=...}`)도 지정할 수 있다 |
| `-ExcludeProperty` | 지정한 속성만 제외하고 나머지를 모두 남긴다 |
| `-ExpandProperty` | 지정한 속성이 배열·객체이면 그 내용을 펼쳐서 최상위 결과로 만든다(펼쳐지는 대신 원본 타입은 사라진다) |
| `-First` / `-Last` | 컬렉션의 앞 또는 뒤에서 지정한 개수만 선택한다 |
| `-Skip` / `-SkipLast` | 앞(또는 뒤)에서 지정한 개수를 건너뛴다 |
| `-Unique` | 모든 속성 값이 같은 객체 중복을 제거한다(대소문자 구분, `-CaseInsensitive`로 완화 가능) |
| `-Index` | 0부터 시작하는 인덱스로 특정 위치의 객체만 선택한다 |
| `-Wait` | `-First`/`-Index` 사용 시 파이프라인 앞 단계를 조기 종료시키는 최적화를 끈다 |

## 예시

```powershell
Get-Process | Select-Object -Property ProcessName, Id, WS       # 원하는 속성만
Get-Process | Sort-Object WS | Select-Object -Last 5             # 메모리 사용량 상위 5개
"a","a","b","c" | Select-Object -Unique                          # 중복 제거 → a, b, c
Get-Content Servers.txt | Select-Object -Skip 1                  # 첫 줄 건너뛰기
Get-Process Explorer | Select-Object -Property ProcessName -ExpandProperty Modules | Format-List
1..20 | Select-Object -First 3 -Last 3 -Skip 4                    # 건너뛴 뒤 앞 3개 + 뒤 3개
Get-ChildItem $PSHOME -File | Select-Object Name,
    @{Label="Size(KB)"; Expression={$_.Length/1KB}},
    @{Label="Days"; Expression={((Get-Date) - $_.LastAccessTime).Days}}
```

계산된 속성은 `Format-Table`(09장)에서 본 것과 같은 해시테이블 문법(`Label`/`Expression`)을 쓰지만, `Format-Table`은 화면 표시용 서식만 바꾸는 반면 `Select-Object`는 실제로 그 속성을 가진 새 객체를 만든다는 점이 다르다.

## 주의사항·함정

**`-ExpandProperty`는 원본 객체를 변형시키는 부작용이 있다**: `-ExpandProperty`로 하위 객체를 펼치면서 동시에 `-Property`로 다른 속성을 지정하면, PowerShell은 그 속성을 펼쳐진 객체에 `NoteProperty`로 추가한다 — 이 과정에서 원본 객체 자체가 변경된다. 원본을 보존하려면 `[pscustomobject]`로 새 객체를 직접 조립하는 편이 안전하다.

**`-First`/`-Index`는 파이프라인을 조기 종료시킬 수 있다**: Windows PowerShell 3.0부터 `Select-Object -First`/`-Index`는 필요한 개수만큼 객체를 받으면 앞 단계 명령 자체를 멈추는 최적화를 수행한다. 이 동작이 부작용(로그 남기기 등)이 있는 명령과 함께 쓰일 때 문제가 된다면 `-Wait`로 끌 수 있다. `Sort-Object`처럼 전체 객체를 모아야 하는 명령 뒤에는 이 최적화가 적용되지 않는다.

**이식성**: Bash에서 `cut`·`awk '{print $1,$3}'`으로 텍스트 열을 잘라내는 작업에 대응하지만, `Select-Object`는 열 이름(속성명)으로 선택하므로 열 순서가 바뀌어도 스크립트가 깨지지 않는다는 것이 근본적 차이다.

## Reference

- [Select-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-object)
