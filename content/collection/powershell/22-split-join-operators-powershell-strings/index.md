---
draft: true
collection_order: 22
slug: split-join-operators-powershell-strings
title: "[PowerShell] 22. -split/-join 연산자"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell -split 연산자로 문자열을 정규식 구분자 기준으로 나누는 법과 -Max-substrings/옵션 매개변수, -join 연산자로 배열을 하나의 문자열로 합치는 법, 단항/이항 형태의 우선순위 차이를 정리한 챕터다."
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
- Split-Operator
- Join-Operator
- Regex(정규표현식)
- String-Manipulation
- Delimiter
- Text-Processing
- CSV(Comma-Separated Values)
image: "wordcloud.png"
---

## 개요

`-split`과 `-join`은 문자열을 나누고 합치는 한 쌍의 연산자다. Bash에서 `IFS`와 배열 확장으로 처리하던 문자열 분리·결합을 PowerShell은 연산자 두 개로 명시적으로 표현한다. 가장 중요한 차이는 `-split`의 구분자가 단순 문자가 아니라 **정규식**이라는 점이다 — 콤마 하나로 나누는 간단한 작업도, 여러 구분자를 한 번에 처리하는 복잡한 작업도 같은 연산자로 표현할 수 있다.

두 연산자는 CSV 한 줄을 필드 배열로 쪼개거나, 필드 배열을 다시 한 줄로 합쳐 파일에 쓰는 것처럼 서로 반대 방향의 변환을 짝지어 수행하는 데 특히 자주 쓰인다. `-split`으로 얻은 배열을 가공한 뒤 `-join`으로 되돌리는 왕복 패턴은, 정규식 하나로 텍스트 구조를 분해했다가 원하는 형태로 재조립하는 PowerShell 특유의 텍스트 처리 방식을 보여준다.

## 사용법

```powershell
-split <String>
-split (<String[]>)
<String> -split <Delimiter>[, <Max-substrings>[, "<Options>"]]
<String> -split { <ScriptBlock> } [, <Max-substrings>]

-join <String[]>
<String[]> -join <Delimiter>
```

## 매개변수

| 항목 | `-split` | `-join` |
|---|---|---|
| 구분자 | 정규식(기본 공백). 괄호로 감싼 부분은 결과에 포함된다 | 임의의 문자열(기본은 빈 문자열, 즉 구분자 없음) |
| 개수 제한 | `<Max-substrings>`로 최대 조각 수 지정(음수면 끝에서부터) | 없음(전체를 합침) |
| 옵션 | `SimpleMatch`(단순 문자열 비교), `IgnoreCase`, `Multiline`, `Singleline` 등(`<Max-substrings>` 지정 시에만 사용 가능) | 없음 |
| 대소문자 접두어 | `-isplit`(구분 안 함, 기본), `-csplit`(구분) | 해당 없음 |
| 단항/이항 | 단항(`-split "a b"`)과 이항(`"a b" -split " "`) 둘 다 지원 | 단항(`-join $arr`)과 이항(`$arr -join ","`) 둘 다 지원 |

## 예시

```powershell
"Lastname:FirstName:Address" -split ":"          # 콤마 구분자로 3조각
"Lastname:FirstName:Address" -split "(:)"        # 괄호로 감싸 구분자 자체도 결과에 포함
$c = "a,b,c,d,e,f,g,h"
$c -split ",", 3                                  # 최대 3조각 → a, b, c,d,e,f,g,h
$c -split ",", -3                                 # 끝에서부터 3조각
"This.is.a.test" -split "\."                      # 정규식이라 .을 이스케이프해야 함
"This.is.a.test" -split ".", 0, "SimpleMatch"     # 리터럴 점으로 취급

-join ("Windows", "PowerShell", "2.0")            # WindowsPowerShell2.0
"Windows", "PowerShell", "2.0" -join " "          # Windows PowerShell 2.0
$a = "WIND", "S P", "ERSHELL"
$a -join "OW"                                     # WINDOWS POWERSHELL

# split과 join을 조합해 값 재구성
(-split $hereString) -join " "
```

## 주의사항·함정

**단항 연산자는 쉼표보다 우선순위가 높다**: `-split "1 2", "a b"`처럼 쉼표로 구분된 문자열 목록을 단항 `-split`에 넘기면, 첫 번째 문자열(쉼표 앞)만 분리된다. 여러 문자열을 한 번에 나누려면 이항 형태(`<String[]> -split <Delimiter>`)를 쓰거나 변수에 담아서 넘겨야 한다. `-join`도 같은 우선순위 규칙을 따른다.

**정규식 특수문자를 리터럴로 쓰려면 이스케이프하거나 `SimpleMatch`를 쓴다**: `.`, `*`, `(` 같은 정규식 메타문자를 구분자로 그대로 쓰면 의도와 다르게 동작한다(`.`은 "모든 문자"를 뜻한다). 리터럴 문자로 나누려면 `\.`처럼 백슬래시로 이스케이프하거나, `<Max-substrings>`를 지정한 뒤 `"SimpleMatch"` 옵션을 함께 쓴다.

**악의적인 정규식 구분자는 성능 문제를 일으킬 수 있다**: 중첩된 수량자가 많은 정규식은 `-split`의 내부 정규식 엔진에서 지수적으로 느려질 수 있다(ReDoS). 신뢰할 수 없는 입력을 구분자로 그대로 사용하지 않는다.

**이식성**: Bash는 `IFS` 변수와 단어 분리(word splitting)로 문자열을 배열처럼 다루지만 명시적인 분리 연산자가 없고, `paste`나 `printf`로 합치는 방식이 각기 다르다. PowerShell은 `-split`/`-join`이라는 대칭적인 연산자 쌍으로 이 두 작업을 통일해서 표현한다.

## Reference

- [about_Split - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_split)
- [about_Join - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_join)
