---
draft: true
collection_order: 63
slug: script-block-closure-powershell
title: "[PowerShell] 63. 스크립트 블록과 클로저"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 스크립트 블록 {} 리터럴이 System.Management.Automation.ScriptBlock 객체인 원리와 호출 연산자(&)로 실행하는 법, GetNewClosure()로 클로저를 만드는 법, 지연 바인딩(delay-bind) 스크립트 블록을 정리한 챕터다."
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
- Script-Block
- Closure
- Call-Operator
- Delay-Bind
- Invoke-Command
- Anonymous-Function
image: "wordcloud.png"
---

## 개요

**스크립트 블록**(`{ }`)은 중괄호로 감싼 명령 목록 자체를 하나의 값으로 다루는 .NET `ScriptBlock` 객체다. 12장의 `Where-Object { $_.Length -gt 100KB }`, 47장의 `switch` 조건에서 이미 스크립트 블록을 수도 없이 써 왔는데, 이 장은 그 `{ }`가 사실은 변수에 담고 매개변수로 넘기고 나중에 실행할 수 있는 독립된 데이터 타입이라는 점을 정식으로 다룬다.

정신 모델은 "스크립트 블록은 아직 실행되지 않은 코드 뭉치이고, 원할 때 원하는 스코프에서 실행을 '트리거'할 수 있다"는 것이다. 이 지연 실행 성질이 `Invoke-Command`의 원격 실행(11부), `Start-Job`의 백그라운드 실행(78장)의 토대가 된다.

## 사용법

```powershell
$sb = { <문장 목록> }         # 스크립트 블록을 변수에 저장
& $sb                          # 호출 연산자로 실행
$sb.Invoke()                    # 메서드로 실행
```

## 종류

| 요소 | 설명 |
|---|---|
| `{ }` 리터럴 | 스크립트 블록을 만드는 기본 문법, 함수처럼 `param()` 사용 가능 |
| 호출 연산자(`&`) | 스크립트 블록이나 문자열 경로를 자식 스코프에서 실행 |
| `.Invoke()` | 스크립트 블록 객체의 메서드로 직접 실행 |
| `GetNewClosure()` | 현재 스코프의 변수 값을 스냅샷으로 "가둬(close over)" 새 스크립트 블록을 반환 |
| 지연 바인딩(delay-bind) 스크립트 블록 | 파이프라인 입력을 받는 타입 지정 매개변수에서 `$_`를 참조하는 스크립트 블록을 값처럼 넘기는 문법 |

## 예시

```powershell
$sb = { Get-Service BITS }
& $sb                                     # 호출 연산자로 실행
Invoke-Command -ScriptBlock $sb             # cmdlet에 스크립트 블록 전달

$sb2 = { param($p1, $p2) "p1: $p1, p2: $p2" }
& $sb2 -p1 "첫째" -p2 "둘째"                  # 매개변수와 함께 실행

$result = & { 1 + 1 }                       # 실행 결과를 변수에 저장
$result                                       # 2

# 클로저 — 현재 값을 스냅샷으로 가두기
function New-Multiplier ($factor) {
    { param($n) $n * $factor }.GetNewClosure()
}
$double = New-Multiplier 2
$triple = New-Multiplier 3
& $double -n 5     # 10 — 클로저 없이는 $factor가 나중에 바뀐 값을 참조해 버림
& $triple -n 5     # 15

# 지연 바인딩 — $_로 파이프라인 값을 참조하는 스크립트 블록을 매개변수로
Get-ChildItem config.log | Rename-Item -NewName { "old_$($_.Name)" }
```

## 주의사항·함정

**중괄호로 감싼 모든 것이 스크립트 블록은 아니다**: `if`/`for` 문의 `{ }`는 통계 블록(statement block)일 뿐 `ScriptBlock` 객체가 아니며, 새 스코프를 만들지도 않고 `param()`을 쓸 수도 없다. `$sb = { ... }`처럼 변수에 직접 대입되거나 `-ScriptBlock` 같은 매개변수 자리에 오는 `{ }`만 진짜 스크립트 블록으로 취급된다는 점을 구분해야 한다.

**클로저 없이는 스크립트 블록이 외부 변수를 "그 시점의 값"이 아니라 "그 이름"으로 참조한다**: 위 예시에서 `GetNewClosure()`를 빼면 `$double`과 `$triple`이 똑같이 마지막으로 호출된 `$factor` 값을 참조하게 되어 두 배·세 배 곱셈기를 독립적으로 만드는 데 실패한다. 반복문 안에서 스크립트 블록을 여러 개 만들어 나중에 실행할 계획이라면, 각 스크립트 블록이 그 시점의 값을 "고정"해야 하는지부터 판단해야 한다.

**지연 바인딩 스크립트 블록은 파이프라인 입력 없이는 오류를 낸다**: `Rename-Item -NewName {$_.Name + ".old"}`처럼 파이프라인으로 아무것도 넘기지 않고 이 문법만 단독으로 쓰면 "스크립트 블록을 입력 없이 평가할 수 없다"는 오류가 난다. 이 문법은 61장에서 다룬 파이프라인 바인딩 매개변수 전용이다.

**이식성**: Bash의 함수나 서브셸(`( ... )`)이 "나중에 실행할 코드 뭉치"라는 개념적으로는 가장 가깝지만, 클로저처럼 외부 변수를 스냅샷으로 가두는 문법은 지원하지 않는다. JavaScript의 화살표 함수·클로저 개념에 익숙하다면 PowerShell 스크립트 블록의 `GetNewClosure()`가 가장 직관적으로 이해될 것이다 — .NET 기반 설계(1장)가 셸 스크립팅에 함수형 언어 개념을 끌어들인 대표적인 사례다.

## Reference

- [about_Script_Blocks - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_script_blocks)
