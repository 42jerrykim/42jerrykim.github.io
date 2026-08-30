---
draft: false
collection_order: 20
slug: comparison-operators-eq-like-contains-in-powershell
title: "[PowerShell] 20. 비교 연산자 — -eq/-like/-contains/-in"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 비교 연산자(-eq, -like, -match, -contains, -in 등)의 종류와 대소문자 구분 접두어(c/i), 스칼라 입력과 컬렉션 입력에서 반환값이 달라지는 규칙, $null 비교 시 흔한 실수를 정리한 챕터다."
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
- Comparison-Operators
- Wildcard
- Regex(정규표현식)
- Case-Sensitivity
- Where-Object
- Operator
- Boolean
image: "wordcloud.png"
---

## 개요

PowerShell의 비교 연산자는 부호(`==`, `>`, `<`)가 아니라 `-eq`, `-gt`, `-like`처럼 하이픈으로 시작하는 단어다. `>`와 `<`는 PowerShell에서 리다이렉션 연산자로 이미 쓰이고 있어 비교 연산자로 재사용할 수 없기 때문이다. 12장에서 `Where-Object`와 함께 몇 개를 이미 써봤지만, 이 장은 전체 목록과 공통 규칙을 정리한다.

정신 모델에서 핵심은 "왼쪽 값이 스칼라인가 컬렉션인가에 따라 연산자의 반환 타입 자체가 달라진다"는 것이다. 왼쪽이 스칼라 값이면 `True`/`False`를 반환하지만, 왼쪽이 컬렉션이면 조건에 맞는 원소들을 걸러 반환한다 — 이 이중적 동작이 `1,2,3 -eq 2`가 `True`가 아니라 `2`를 출력하는 이유다.

## 종류

| 분류 | 연산자 | 대소문자 접두어 |
|---|---|---|
| 동등 | `-eq`/`-ne`, `-gt`/`-ge`, `-lt`/`-le` | `c`(구분), `i`(구분 안 함, 기본) |
| 매칭 | `-like`/`-notlike`(와일드카드), `-match`/`-notmatch`(정규식) | `c`, `i` |
| 치환 | `-replace`(정규식 기반 치환) | `c`, `i` |
| 포함 | `-contains`/`-notcontains`(컬렉션이 값을 포함하는가), `-in`/`-notin`(값이 컬렉션에 있는가) | `c`, `i` |
| 타입 | `-is`/`-isnot`(같은 .NET 타입인가) | 대소문자 구분 없음(타입 이름 비교이므로) |

`-`뒤에 `c`를 붙이면(`-ceq`) 대소문자를 구분하고, `i`를 붙이면(`-ieq`) 명시적으로 구분하지 않는다 — 접두어 없는 기본형(`-eq`)은 이미 대소문자를 구분하지 않으므로 `-ieq`와 동일하다.

## 예시

```powershell
2 -eq 2                        # True
1,2,3 -eq 2                    # 2 (컬렉션이면 매칭된 원소 반환)
'PowerShell' -like '*shell'    # True (와일드카드)
'PowerShell' -match '^Power\w+' # True (정규식), $Matches 자동 변수도 채워짐
$DomainServers -contains $thisComputer   # 컬렉션이 특정 값을 포함하는가
$thisComputer -in $DomainServers         # 값이 컬렉션에 있는가(-contains의 반대 표기)
(Get-Date) -is [datetime]      # True (타입 비교)
'macOS' -clt 'MacOS'           # 대소문자 구분 정렬 비교
$null -ne $a                   # $null은 항상 왼쪽에 둔다(뒤 문단 참고)
```

## 주의사항·함정

**`$null` 비교는 항상 `$null`을 왼쪽에 둔다**: `$a -eq $null`은 `$a`가 컬렉션이면 그 안의 `$null` 원소들을 걸러내는 필터로 동작해 버린다. "변수 자체가 null인가"를 확인하려면 `$null -eq $a`처럼 `$null`을 왼쪽에 써야 한다.

**`-contains`/`-in`은 `-eq`보다 먼저 멈춘다**: `-contains`/`-in`은 첫 매칭을 찾으면 즉시 비교를 멈추고 항상 `Boolean`을 반환하지만, `-eq`는 컬렉션의 모든 원소를 끝까지 검사한다. 큰 컬렉션에서 "포함 여부"만 필요하다면 `-contains`/`-in`이 더 빠르다.

**타입이 다른 값 비교는 왼쪽 타입 기준으로 변환된다**: `1 -eq '1.0'`은 오른쪽 문자열이 정수로 변환되어 `True`이지만, `'1.0' -eq 1`은 반대로 `1`이 문자열로 변환되어 `False`다. 왼쪽 피연산자가 비교 방식을 결정한다는 규칙을 기억해야 한다.

**이식성**: Bash의 `[ "$a" = "$b" ]`나 `test`는 값을 문자열로만 비교하지만, PowerShell 비교 연산자는 왼쪽 값의 실제 .NET 타입(숫자, 날짜, 커스텀 클래스)에 맞는 비교를 시도한다. CMD의 `if "%a%"=="%b%"`도 순수 문자열 비교라는 점에서 마찬가지다.

## Reference

- [about_Comparison_Operators - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)
