---
draft: true
collection_order: 12
slug: where-object-command-filter-pipeline-powershell
title: "[PowerShell] 12. Where-Object — 필터링"
date: 2026-08-29
lastmod: 2026-08-29
description: "Where-Object로 파이프라인 객체를 조건에 맞게 거르는 법, 스크립트블록 구문($_)과 간소화 구문(-Property -operator value) 두 가지 문법의 차이, 자주 쓰는 비교 연산자를 정리한 챕터다."
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
- Where-Object
- Filter
- Comparison-Operators
- Script-Block
- Get-Process
- Wildcard
- Regex(정규표현식)
image: "wordcloud.png"
---

## 개요

`Where-Object`는 파이프라인을 지나는 객체 중 조건에 맞는 것만 통과시키는 필터 cmdlet이다. Bash의 `grep`이 텍스트 줄을 패턴으로 거르는 것과 목적은 비슷하지만, `Where-Object`는 문자열이 아니라 객체의 **속성 값**을 기준으로 판단한다는 점이 다르다. `Get-Process | Where-Object {$_.PriorityClass -eq "Normal"}`은 출력 텍스트에서 "Normal"이라는 글자를 찾는 것이 아니라, 각 프로세스 객체의 `PriorityClass` 속성 값을 직접 비교한다.

정신 모델은 "파이프로 들어온 객체를 하나씩 조건식에 대입해, 참이면 통과시키고 거짓이면 버린다"는 것이다. Windows PowerShell 3.0부터는 이 조건식을 표현하는 두 가지 문법 — 스크립트블록 구문과 간소화 구문 — 이 함께 존재한다.

## 사용법

```powershell
# 스크립트블록 구문 — $_ 로 현재 객체를 참조
Get-Process | Where-Object { $_.PriorityClass -eq "Normal" }

# 간소화 구문 — 속성명, 연산자, 값을 매개변수로 직접 전달
Get-Process | Where-Object -Property PriorityClass -EQ -Value "Normal"
Get-Process | Where-Object PriorityClass -EQ "Normal"    # 매개변수 이름 생략 가능
```

두 구문은 완전히 동등하며 상호 교환 가능하다. 스크립트블록 구문은 `-and`/`-or`로 여러 조건을 조합하거나 속성 값을 가공해야 할 때 필요하고, 간소화 구문은 단일 조건을 짧게 쓸 때 읽기 편하다.

## 매개변수

| 항목 | 설명 |
|---|---|
| 스크립트블록(`{ }`) | `$_`(또는 `$PSItem`)로 현재 파이프라인 객체를 참조하는 조건식. 모든 PowerShell 비교·논리 연산자를 그대로 쓸 수 있다 |
| `-Property` | 간소화 구문에서 비교할 속성 이름 |
| `-Value` | 간소화 구문에서 비교할 값 |
| 31개의 연산자 스위치 | `-EQ`, `-NE`, `-GT`, `-LT`, `-Like`, `-Match`, `-Contains`, `-In` 등 비교 연산자를 스위치 매개변수로 제공해 간소화 구문을 완성한다 |
| `-Not` | 조건을 반전한다(스위치 연산자와 조합 가능) |

## 예시

```powershell
Get-ChildItem | Where-Object { $_.Length -gt 1MB }              # 1MB보다 큰 파일
Get-Service | Where-Object Status -eq 'Running'                 # 간소화 구문
Get-Process | Where-Object { $_.CPU -gt 100 -and $_.WS -gt 50MB }   # 복합 조건은 스크립트블록만 가능
Get-ChildItem | Where-Object { $_.Name -like "*.ps1" }           # 와일드카드 패턴
Get-ChildItem -Path C:\Test | Where-Object { $_.PSIsContainer }  # 디렉터리만
Get-EventLog -LogName System | Where-Object { $_.EntryType -eq "Error" } | Select-Object -First 5
1..10 | Where-Object { $_ % 2 -eq 0 }                            # 짝수만
```

## 주의사항·함정

**`-eq`는 `==`가 아니다**: PowerShell 비교 연산자는 부호가 아니라 `-eq`, `-ne`, `-gt`, `-lt`, `-like`, `-match`처럼 하이픈 접두 단어다. `$_.Status == "Running"`처럼 다른 언어의 습관대로 쓰면 구문 오류가 난다. 연산자 전체 목록은 20장에서 다룬다.

**간소화 구문은 단일 조건에서만 쓸 수 있다**: `-and`/`-or`로 여러 속성을 조합해야 하는 조건은 간소화 구문으로 표현할 수 없고 스크립트블록 구문이 필요하다.

**`$_`는 스크립트블록 안에서만 유효하다**: `Where-Object` 바깥에서 `$_`를 참조하면 이전 파이프라인 단계(예: `catch` 블록이나 다른 `ForEach-Object`)의 값이 남아 있을 수 있어 혼란을 준다. 조건이 복잡해지면 스크립트블록을 변수에 미리 담아두고 재사용하는 편이 안전하다.

**필터링은 언제나 정렬·선택보다 먼저 오는 것이 자연스럽다**: `Where-Object`로 먼저 대상을 좁힌 뒤 `Sort-Object`·`Select-Object`를 적용하면, 이후 단계가 처리할 객체 수가 줄어 파이프라인 전체가 더 빠르게 끝난다.

**이식성**: Bash의 `grep`·`awk '조건'`은 텍스트 줄 단위로 패턴을 매칭하지만, `Where-Object`는 객체의 속성 타입을 그대로 유지한 채 비교한다 — 숫자 속성을 문자열로 바꿨다가 다시 파싱할 필요가 없다.

## Reference

- [Where-Object (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/where-object)
