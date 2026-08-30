---
draft: false
collection_order: 45
slug: string-formatting-here-string-powershell
title: "[PowerShell] 45. 문자열 서식과 Here-String"
date: 2026-08-29
lastmod: 2026-08-29
description: "작은따옴표와 큰따옴표의 문자열 전개(interpolation) 차이, 이스케이프 문자 백틱(`), -f 서식 연산자, 여러 줄 텍스트를 다루는 Here-String(@\"...\"@) 문법을 정리한 PowerShell 문자열 서식 챕터다."
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
- String-Interpolation
- Here-String
- Escape-Character
- Format-Operator
- Quoting-Rules
- Multiline-String
image: "wordcloud.png"
---

## 개요

PowerShell 문자열은 어떤 따옴표를 쓰느냐에 따라 동작이 완전히 달라진다. **작은따옴표**(`'...'`)는 안의 내용을 있는 그대로 문자 그대로(literal) 취급하고, **큰따옴표**(`"..."`)는 그 안의 변수·표현식을 실제 값으로 치환한다(문자열 전개, interpolation). 41장에서 만든 변수를 화면에 표시할 때 이미 이 차이를 스치듯 썼는데, 이 장은 그 규칙과 여러 줄 텍스트를 위한 Here-String을 정리한다.

정신 모델은 "큰따옴표는 내용을 매번 다시 해석하는 템플릿이고, 작은따옴표는 봉인된 문자 그대로의 상자"라는 것이다. 어느 쪽을 쓸지는 "이 문자열 안의 `$` 기호를 변수로 해석해야 하는가"라는 질문 하나로 결정된다.

## 사용법

```powershell
'작은따옴표: $var는 전개되지 않는다'
"큰따옴표: $var는 값으로 전개된다"
"표현식도 넣을 수 있다: $($var.Length)"
@"
여러 줄
Here-String(큰따옴표, 전개됨)
"@
```

## 종류

| 구문 | 전개 여부 | 용도 |
|---|---|---|
| `'...'` | 안 됨 | 리터럴 문자열, 정규식 패턴(47장), 파일 경로 등 |
| `"..."` | 됨 | 변수·표현식을 포함한 동적 문자열 |
| `` `n``, `` `t``, `` `` ` `` `` | 이스케이프 문자(백틱) | 큰따옴표 안에서 줄바꿈·탭·백틱 자체를 표현 |
| `@"..."@` | 됨 | 여러 줄 텍스트(Here-String), 따옴표를 이스케이프할 필요 없음 |
| `@'...'@` | 안 됨 | 여러 줄 리터럴 텍스트 |
| `-f` 연산자 | — | .NET 복합 서식 문자열로 값 정렬·자릿수 지정 |

## 예시

```powershell
$name = "Alice"
'Hello, $name'                 # 출력: Hello, $name (전개 안 됨)
"Hello, $name"                  # 출력: Hello, Alice
"1 + 1 = $(1 + 1)"               # 하위 표현식 연산자 $()로 계산 결과 삽입
"경로: C:\Temp"                  # 백슬래시는 이스케이프 문자가 아니므로 그대로 출력됨

"첫 줄`n둘째 줄"                  # `n으로 줄바꿈
"탭`t구분"                        # `t로 탭
"큰따옴표 안의 `$변수는 전개 안 함"  # 백틱으로 $ 자체를 이스케이프

@"
여러 줄 문자열입니다.
변수도 전개됩니다: $name
따옴표(")를 이스케이프할 필요가 없습니다.
"@

@'
전개되지 않는 여러 줄 문자열입니다.
$name 은 그대로 출력됩니다.
'@

# -f 서식 연산자
"{0}는 {1}살입니다" -f $name, 30
"{0,10}" -f "우측정렬"              # 너비 10, 우측 정렬
"{0:N2}" -f 1234.5678                # 소수점 2자리, 천단위 구분: 1,234.57
```

## 주의사항·함정

**Here-String의 닫는 태그는 반드시 줄 맨 앞에 와야 한다**: `@"`나 `@'`로 연 뒤 마지막 줄의 `"@`(또는 `'@`)는 앞에 공백이나 다른 문자가 전혀 없이 그 줄의 첫 글자여야 한다. 들여쓰기된 코드 블록 안에 Here-String을 넣으면서 닫는 태그까지 함께 들여쓰면 파싱 오류가 난다 — 이는 이 저장소의 문서 작성 규칙에서 Here-String을 코드블록 예외로 다루는 이유이기도 하다.

**작은따옴표 문자열에 작은따옴표 자체를 넣으려면 두 번 반복해야 한다**: `'It''s'`처럼 작은따옴표를 연달아 두 번 쓰면 하나의 작은따옴표로 이스케이프된다. 큰따옴표 문자열이라면 그냥 `"It's"`처럼 안에 작은따옴표를 그대로 써도 되므로, 아포스트로피가 포함된 텍스트는 큰따옴표를 쓰는 편이 간단할 때가 많다.

**백슬래시는 PowerShell의 이스케이프 문자가 아니다**: C나 Bash에 익숙하면 `\n`이 줄바꿈이라고 기대하기 쉽지만, PowerShell의 이스케이프 문자는 백틱(`` ` ``)이다. `"C:\temp\n"`은 줄바꿈 없이 그대로 `C:\temp\n`이라는 문자열이 된다 — 줄바꿈이 필요하면 반드시 `` `n``을 써야 한다. 이 차이를 모르면 파일 경로는 문제없이 동작하다가 줄바꿈만 안 되는 상황에서 원인을 찾기 어렵다.

**이식성**: Bash도 작은따옴표(리터럴)와 큰따옴표(변수 전개) 구분이 있어 개념적으로 가장 비슷하지만, 이스케이프 문자가 백슬래시라는 점이 다르다. CMD는 따옴표에 따른 전개 개념 자체가 없고 `%var%` 치환만 지원한다. PowerShell의 `$()` 하위 표현식 연산자처럼 문자열 안에서 임의의 코드를 실행해 삽입하는 기능은 Bash의 `$(...)`, `"$(cmd)"`와 가장 유사하다.

## Reference

- [about_Quoting_Rules - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)
