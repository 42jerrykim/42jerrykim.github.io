---
draft: false
collection_order: 41
slug: variables-data-types-powershell
title: "[PowerShell] 41. 변수와 데이터 타입"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 변수 이름 규칙과 $ 접두사, [int]·[string] 같은 타입 제약(type-constrain) 문법, 변수 스코프의 기본 개념, Variable: 프로바이더로 변수를 항목처럼 다루는 법을 정리한 Part 5 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Scripting(스크립팅)
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
- Variables
- Data-Types
- Type-Casting
- Scope
- Variable-Provider
- Strict-Mode
image: "wordcloud.png"
---

## 개요

PowerShell **변수**는 이름 앞에 `$`를 붙여 만들며, 별도 선언 없이 대입하는 순간 생성된다. 지금까지 다뤄온 `$PROFILE`(06장), `$Matches`(20장 예고), `$_`(15장) 같은 자동 변수도 결국 이 변수 시스템 위에서 동작한다. 이 장은 Part 4까지 다양한 cmdlet의 결과를 담아 온 변수 자체의 규칙 — 이름, 타입, 스코프 — 을 정리하며 Part 5(데이터 구조와 텍스트 처리)의 출발점이 된다.

PowerShell 변수의 핵심 정신 모델은 "변수는 타입이 아니라 값에 묶인 이름표"라는 것이다. `$x = 1`이라고 쓴 뒤 `$x = "hello"`로 다시 대입해도 오류가 나지 않는다 — 변수 자체가 `[int]`나 `[string]`으로 고정되지 않고, 담긴 값의 타입만 그때그때 바뀌기 때문이다. 타입을 강제하고 싶다면 이름 앞에 타입 리터럴을 붙이는 별도 문법(type-constraining)을 써야 한다.

## 사용법

```powershell
$변수이름 = 값                 # 생성과 대입이 동시에 일어난다
[타입]$변수이름 = 값            # 변수를 특정 타입으로 제약
${특수 문자가 있는 이름} = 값    # 중괄호로 감싸면 공백·기호 포함 가능
```

## 종류

| 변수 유형 | 설명 | 예 |
|---|---|---|
| 사용자 변수 | 스크립트·세션에서 직접 만드는 변수 | `$count`, `$serverList` |
| 자동 변수 | PowerShell이 자동으로 채우는 변수(24장에서 전체 목록) | `$_`, `$?`, `$LASTEXITCODE` |
| 환경 변수 | OS 환경 변수를 감싼 접근자, `Env:` 프로바이더 사용 | `$env:PATH`, `$env:USERNAME` |
| 기본 설정 변수 | cmdlet 동작을 제어하는 변수(25장에서 다룬 공통 매개변수와 연동) | `$ErrorActionPreference`, `$PSDefaultParameterValues` |

타입 제약 문법에 쓸 수 있는 대표 타입은 다음과 같다.

| 타입 리터럴 | 의미 |
|---|---|
| `[int]` | 32비트 정수 |
| `[string]` | 문자열 |
| `[double]` | 배정밀도 부동소수점 |
| `[bool]` | `$true`/`$false` |
| `[datetime]` | 날짜·시간(52장에서 자세히) |
| `[array]` | 배열(42장) |
| `[hashtable]` | 해시테이블(44장) |

## 예시

```powershell
$number = 10                          # 타입 미지정 — 필요에 따라 자동 변환
[int]$strictNumber = 10               # int로 제약된 변수
$strictNumber = "20"                  # 문자열이지만 int로 자동 변환되어 저장됨
$strictNumber = "abc"                 # 캐스팅 실패 — 예외 발생

${my variable} = "공백 포함 변수명"     # 중괄호 표기법

$name = "world"
"Hello, $name!"                        # 큰따옴표 안에서 변수 자동 전개(45장에서 상세)

Get-Variable -Name strictNumber        # 변수 정보를 객체로 조회
Set-Variable -Name count -Value 0      # cmdlet 형태로 변수 생성
Remove-Variable -Name count            # 변수 삭제

Get-ChildItem Variable:\str*           # Variable: 프로바이더로 변수 목록 탐색(30장)
```

## 주의사항·함정

**타입 제약은 변수 하나에만 적용되고, 재대입 시 강제로 변환을 시도한다**: `[int]$x = 10` 이후 `$x = "20"`을 대입하면 문자열 "20"이 int 10으로 변환되어 저장되지만, `$x = "abc"`처럼 변환 불가능한 값을 넣으면 예외가 발생한다. 반대로 타입 제약이 없는 변수는 어떤 값이든 조용히 받아들이므로, 예상치 못한 타입의 값이 뒤늦게 다른 cmdlet에서 오류를 일으키는 원인이 되기 쉽다. 함수 매개변수나 반복적으로 재사용하는 변수에는 타입 제약을 붙여 실수를 조기에 드러내는 편이 안전하다.

**변수 이름의 대소문자는 구분되지 않는다**: `$Name`과 `$name`은 같은 변수를 가리킨다. 여러 사람이 협업하는 스크립트에서는 이 점이 혼란을 줄 수 있으므로, 프로젝트 전체에서 하나의 표기 관례(PascalCase 등)를 정해 일관되게 쓰는 편이 좋다.

**스코프를 명시하지 않으면 항상 "현재" 스코프에 생성·수정된다**: 함수 안에서 `$x = 1`을 쓰면 그 함수의 지역 변수가 새로 생기는 것이지, 같은 이름의 전역 변수를 바꾸는 것이 아니다. 스코프의 전체 규칙(전역·지역·스크립트·비공개)은 64장에서 함수와 함께 자세히 다룬다 — 지금은 "변수는 기본적으로 자신이 만들어진 블록 안에서만 보인다"는 원칙만 기억하면 된다.

**이식성**: Bash는 `x=10`처럼 `$` 없이 대입하고 참조할 때만 `$x`를 붙이며 기본적으로 모든 값을 문자열로 다룬다. CMD의 `set x=10`과 `%x%`도 문자열 전용이다. PowerShell은 대입·참조 모두 `$` 접두사를 쓰고, 문자열이 아닌 실제 .NET 타입(정수·불리언·날짜 등)을 그대로 저장한다는 점이 근본적으로 다르다 — 이 차이가 10장에서 강조한 객체 파이프라인의 토대이기도 하다.

## Reference

- [about_Variables - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_variables)
