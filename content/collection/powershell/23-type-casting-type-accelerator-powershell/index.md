---
draft: false
collection_order: 23
slug: type-casting-type-accelerator-powershell
title: "[PowerShell] 23. 타입 캐스팅과 [type] 접근자"
date: 2026-08-29
lastmod: 2026-08-29
description: "[int], [string] 같은 PowerShell 타입 캐스팅 문법과 암시적/명시적 변환 규칙, -is/-isnot/-as 타입 연산자, 숫자 반올림·배열-문자열 변환처럼 자주 놀라는 변환 규칙을 정리한 챕터다."
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
- Type-Casting
- Type-Conversion
- Type-Accelerator
- Get-Member
- Strong-Typing
- Rounding
- Cmdlet-Binding
image: "wordcloud.png"
---

## 개요

`[int]`, `[string]`, `[datetime]`처럼 대괄호로 감싼 타입 이름을 값 앞에 붙이면, PowerShell은 그 값을 해당 .NET 타입으로 변환(캐스팅)한다. 20장에서 본 것처럼 비교·산술 연산 중에도 PowerShell은 필요하면 값을 알아서 변환하는데(암시적 변환), 이 장에서 다루는 대괄호 캐스팅은 그 변환을 코드에 명시적으로 드러내는 방법이다.

정신 모델은 "PowerShell 변수는 기본적으로 타입에 묶여 있지 않지만, 필요하면 특정 타입에 고정(type-constrain)할 수 있다"는 것이다. `[int]$foo = 42`처럼 변수 앞에 타입을 붙이면 이후 그 변수에는 `int`로 변환 가능한 값만 대입할 수 있고, `[int]'43'`처럼 값 앞에 붙이면 그 자리에서 즉시 변환된 새 값을 얻는다.

## 사용법

```powershell
[int]$foo = 42            # 변수를 int로 타입 제약
$var = [int]'43'          # 문자열을 즉시 캐스팅
<input> -is [type]         # 타입 일치 여부(Boolean)
<input> -as [type]         # 변환 시도, 실패하면 $null 반환(오류 없음)
```

## 종류

| 방식 | 실패 시 동작 | 특징 |
|---|---|---|
| `[type]$value` 캐스팅 | 오류 발생(catch 가능) | 가장 흔히 쓰는 명시적 변환 |
| `-as [type]` | `$null` 반환(오류 없음) | 변환 가능 여부를 조용히 확인할 때 유용 |
| `-is [type]` / `-isnot` | 항상 Boolean 반환 | 값 자체를 바꾸지 않고 타입만 확인 |
| 암시적 변환 | 문맥에 따라 다름 | 매개변수 바인딩, 연산자, `if`/`while` 조건식 등에서 자동 발생 |

## 예시

```powershell
[int]"43"                        # 43 (문자열 → 정수)
[byte]42.1                       # 42 (소수점 버림이 아니라 반올림 규칙 적용)
[byte]21.5                       # 22 (가장 가까운 짝수로 반올림 — 은행가 반올림)
[boolean]0                       # False
[boolean]'Hello'                 # True (빈 문자열/빈 배열만 False)
[string]@(1, 2, 3)               # "1 2 3" (배열 → 공백 구분 문자열)
"5/7/07" -as [datetime]          # 변환 성공 시 DateTime 객체
1031 -as [System.Diagnostics.Process]   # 변환 불가 → $null (오류 없음)
(Get-Item /) -is [System.IO.FileSystemInfo]   # True (파생 타입도 매칭)
[regex]'a|b'                     # 단일 매개변수 생성자를 가진 타입은 캐스팅으로 인스턴스화 가능
```

## 주의사항·함정

**정수를 소수로 변환할 때는 버림이 아니라 반올림이다**: `[byte]42.1`은 42가 되지만, 이는 소수점을 버려서가 아니라 가장 가까운 정수로 반올림한 결과다. `21.5`와 `22.5`가 둘 다 `22`로 반올림되는 것("가장 가까운 짝수로 반올림", banker's rounding)은 흔히 놀라는 지점이다.

**배열을 문자열 매개변수에 넘기면 조용히 합쳐진다**: `[CmdletBinding()]` 없는 일반 함수의 `[string]` 매개변수에 배열을 넘기면 오류 없이 공백으로 합쳐진 문자열이 된다. 이 암시적 변환을 막으려면 함수에 `[CmdletBinding()]`을 붙여 고급 함수로 만들어야 한다(45장에서 다룬다) — 그러면 배열이 그대로 넘어올 때 명확한 오류가 난다.

**배열을 여러 인자로 오해하기 쉽다("의사 메서드 구문" 문제)**: `New-Object System.Guid($bytes)`처럼 `[byte[]]` 배열을 생성자에 그대로 넘기면, PowerShell은 그 배열의 각 원소를 개별 인자로 취급해 "인자 개수가 안 맞는다"는 오류를 낸다. 배열 전체를 인자 하나로 넘기려면 `New-Object -ArgumentList (, $bytes)`처럼 바깥에 배열을 한 겹 더 씌우거나, `[System.Guid]::new($bytes)`처럼 정적 `new()` 메서드를 직접 호출한다.

**`-as`는 오류를 던지지 않는다는 것이 캐스팅과의 핵심 차이다**: 변환 성공 여부를 스크립트 흐름에서 직접 판단하고 싶다면(예: 사용자 입력이 날짜 형식인지 확인) `try`/`catch`로 캐스팅 실패를 잡는 대신 `-as`로 시도하고 결과가 `$null`인지 확인하는 편이 더 간결하다.

**이식성**: Bash·CMD는 변수를 항상 텍스트로 다루므로 `[int]`에 대응하는 문법 자체가 없다 — 산술이 필요하면 `expr`이나 `$(( ))` 같은 별도 구문으로 전환해야 한다. PowerShell은 변수 자체가 .NET 객체이므로 타입 캐스팅이 언어에 내장된 1급 문법이다.

## Reference

- [about_Type_Conversion - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_conversion)
- [about_Type_Operators - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_operators)
