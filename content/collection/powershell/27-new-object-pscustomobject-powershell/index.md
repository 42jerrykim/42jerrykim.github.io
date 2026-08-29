---
draft: true
collection_order: 27
slug: new-object-pscustomobject-powershell
title: "[PowerShell] 27. New-Object와 [PSCustomObject]"
date: 2026-08-29
lastmod: 2026-08-29
description: "New-Object로 .NET/COM 객체를 생성하는 법과 [PSCustomObject] 타입 가속기로 순서가 보장된 커스텀 객체를 만드는 법, 두 방식의 성능·가독성 차이와 배열 인자를 생성자에 넘길 때의 함정을 정리한 챕터다."
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
- New-Object
- PSCustomObject
- Object-Creation
- Hashtable
- COM
- Constructor
- Performance(성능)
image: "wordcloud.png"
---

## 개요

지금까지는 `Get-Process`, `Get-Service`처럼 기존 cmdlet이 만들어 주는 객체를 다뤘다. 이 장은 반대로 **직접 객체를 만드는** 두 가지 방법을 다룬다 — 기존 .NET/COM 타입의 인스턴스를 생성하는 `New-Object`와, 속성 몇 개로 즉석에서 커스텀 객체를 만드는 `[PSCustomObject]`다.

정신 모델은 "이미 정의된 타입의 인스턴스가 필요하면 `New-Object`(또는 `[type]::new()`), 이 스크립트 안에서만 쓸 임시 데이터 구조가 필요하면 `[PSCustomObject]`"라는 역할 분담이다. 두 방법 모두 결과는 파이프라인에 흘려보낼 수 있는 객체이지만, 목적과 성능 특성이 다르다.

## 사용법

```powershell
New-Object -TypeName <String> [-ArgumentList <Object[]>] [-Property <IDictionary>]
New-Object -ComObject <String> [-Property <IDictionary>]

[PSCustomObject]@{ 속성1 = 값1; 속성2 = 값2 }
```

## 매개변수

| 항목 | 설명 |
|---|---|
| `-TypeName` | 생성할 .NET 타입의 정규화된 이름(`System.Version` 등) |
| `-ArgumentList`(별칭 `-Args`) | 생성자에 전달할 인자 배열 |
| `-ComObject` | 생성할 COM 객체의 ProgID(레거시 COM 자동화용) |
| `-Property` | 생성 직후 설정할 속성-값 해시테이블(순서대로 적용) |
| `[PSCustomObject]@{ }` | 해시테이블(순서 보존을 위해 `[ordered]@{}` 권장)을 즉시 커스텀 객체로 변환 |

## 예시

```powershell
New-Object -TypeName System.Version -ArgumentList "1.2.3.4"
[System.Version]::new("1.2.3.4")                          # 정적 new() 메서드로도 동일하게 생성 가능

$objShell = New-Object -ComObject "Shell.Application"     # 레거시 COM 자동화
$objShell.ToggleDesktop()

# 순서가 보장되는 커스텀 객체
[PSCustomObject]@{
    Name      = 'Server30'
    System    = 'Server Core'
    PSVersion = '4.0'
}

# 배열을 생성자에 그대로 넘기면 실패, 배열로 한 번 더 감싸야 함
[byte[]]$bytes = 1..16
$guid = New-Object -TypeName System.Guid -ArgumentList (, $bytes)   # 성공
[System.Guid]::new($bytes)                                          # new()는 이 문제가 없다
```

## 주의사항·함정

**`[PSCustomObject]`는 속성 순서를 그대로 보존한다**: `Get-Member`(11장)는 결과를 알파벳순으로 보여주지만, `[PSCustomObject]@{ }`로 만든 객체 자체는 해시테이블에 적은 순서대로 속성을 유지한다(`Format-Table`로 출력할 때도 그 순서가 반영된다). 일반 `@{ }` 해시테이블은 순서를 보장하지 않으므로, 순서가 중요하면 `[ordered]@{ }`를 먼저 만든 뒤 캐스팅하는 습관을 들인다.

**배열을 생성자 인자로 넘길 때 "의사 메서드 구문" 문제를 조심한다**: `New-Object -ArgumentList $array`처럼 배열 하나를 그대로 넘기면, PowerShell은 배열의 각 원소를 개별 인자로 분해해서 시도한다. 생성자가 실제로 배열 하나를 받는 타입이라면, `(, $array)`처럼 바깥에 배열을 한 겹 더 씌워야 한다. 23장에서 다룬 `New-Object System.Guid($bytes)` 실패 사례가 같은 문제다.

**`[type]::new()`가 대부분 더 빠르고 이 함정도 없다**: .NET 타입에 정적 `new()` 메서드가 노출되어 있다면(`[System.Guid]::new($bytes)`), `New-Object`보다 실행 속도가 빠르고 배열 인자 문제도 겪지 않는다. `New-Object`는 COM 객체 생성처럼 `::new()` 문법이 통하지 않는 경우, 또는 타입 이름을 문자열 변수로 동적으로 받아야 하는 경우에 여전히 유용하다.

**이식성**: CMD·Bash에는 임의 구조의 객체를 만드는 개념이 없다 — 구조화된 데이터가 필요하면 텍스트 포맷(JSON, 구분자 있는 줄)으로 직접 인코딩해야 한다. `[PSCustomObject]`는 이런 임시 데이터 구조를 언어에 내장된 문법으로 즉시 만들 수 있게 해준다.

## Reference

- [New-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object)
- [about_Type_Conversion - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_conversion)
