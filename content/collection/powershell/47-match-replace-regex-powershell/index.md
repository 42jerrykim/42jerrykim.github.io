---
draft: true
collection_order: 47
slug: match-replace-regex-powershell
title: "[PowerShell] 47. -match/-replace 연산자와 정규식"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell -match/-replace 연산자가 .NET 정규식 엔진을 쓰는 원리와 $Matches 자동 변수로 캡처 그룹을 꺼내는 법, 이름 있는 캡처 그룹, -replace 치환 문자열에서 $1·${name}으로 참조하는 법을 정리한 챕터다."
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
- Regex
- Regular-Expressions
- Capture-Group
- Matches-Variable
- Comparison-Operators
- Text-Processing
image: "wordcloud.png"
---

## 개요

20장에서 `-eq`, `-like` 같은 비교 연산자를 다뤘는데, `-match`와 `-replace`는 그 계열에서 **정규식**을 쓰는 연산자다. 46장의 `Select-String`이 "파일에서 패턴이 있는 줄"을 찾는 도구라면, `-match`/`-replace`는 "문자열 하나가 패턴과 일치하는지, 일치한 부분을 어떻게 바꿀지"를 다루는 연산자 수준의 도구다. 둘 다 내부적으로는 같은 .NET 정규식 엔진을 공유한다.

정신 모델은 "`-match`는 패턴과 맞는지 참/거짓을 answer하면서 부수적으로 `$Matches`에 세부 결과를 남기고, `-replace`는 패턴과 맞는 부분을 다른 문자열로 바꿔치기한다"는 것이다.

## 사용법

```powershell
<입력> -match <패턴>              # 정규식 일치 여부(Boolean), 성공 시 $Matches 채움
<입력> -replace <패턴>, <대체문자열>  # 패턴과 일치하는 부분을 치환
<입력> -cmatch / -creplace          # 대소문자 구분 버전(대문자 c 접두사)
```

## 종류

| 요소 | 설명 |
|---|---|
| 문자 클래스 | `[0-9]`, `\d`(숫자), `\w`(단어 문자), `\s`(공백) 등 |
| 수량자 | `*`(0회 이상), `+`(1회 이상), `?`(0 또는 1회), `{n,m}`(n–m회) |
| 앵커 | `^`(문자열/줄 시작), `$`(문자열/줄 끝) |
| 캡처 그룹 | `(...)`로 감싼 부분, 번호(`$1`, `$2`)로 참조 |
| 이름 있는 캡처 그룹 | `(?<이름>...)`, `$Matches.이름`이나 `${이름}`으로 참조 |
| `[regex]::Escape()` | 정규식 특수문자를 리터럴로 이스케이프하는 정적 메서드 |

## 예시

```powershell
'book' -match 'oo'                       # True
'Server-01' -match 'Server-\d\d'          # True — \d는 숫자 문자 클래스
42 -match '[0-9][0-9]'                    # True — 두 자리 숫자 패턴

'The last logged on user was CONTOSO\jsmith' -match '(.+was )(.+)'
$Matches[0]        # 전체 일치 문자열
$Matches[1]        # 첫 번째 캡처 그룹
$Matches[2]        # 두 번째 캡처 그룹: CONTOSO\jsmith

'The last logged on user was CONTOSO\jsmith' -match 'was (?<domain>.+)\\(?<user>.+)'
$Matches.domain     # CONTOSO
$Matches.user       # jsmith(이름 있는 캡처 그룹)

'John D. Smith' -replace '(\w+) (\w+)\. (\w+)', '$1.$2.$3@contoso.com'
# John.D.Smith@contoso.com — 번호로 캡처 그룹 참조

'CONTOSO\Administrator' -replace '\w+\\(?<user>\w+)', 'FABRIKAM\${user}'
# FABRIKAM\Administrator — 이름으로 캡처 그룹 참조

'3.141' -match '3\.\d{2,}'                # 마침표를 백슬래시로 이스케이프해 리터럴로 매치
[regex]::Escape('3.14')                    # 3\.14 — 특수문자 자동 이스케이프

'5.72' -replace '(.+)', '$$$1'             # $ 리터럴 표현: $$ 사용 → $5.72
```

## 주의사항·함정

**정규식 앵커(`$`)가 있는 패턴은 반드시 작은따옴표로 감싸야 한다**: 큰따옴표 안에서 `$`는 변수 전개 기호(45장)로 먼저 해석되므로, `"^fish$"`처럼 큰따옴표로 감싸면 PowerShell이 `$`를 변수 참조로 오해해 의도와 다르게 동작할 수 있다. 정규식 패턴은 특별한 이유가 없다면 작은따옴표로 작성하는 습관이 안전하다.

**`$Matches`는 항상 마지막으로 성공한 매치 결과만 담고 있다**: 반복문 안에서 여러 문자열에 `-match`를 적용하면 `$Matches`는 매번 덮어써지므로, 이전 반복의 결과를 나중에 다시 참조할 수 없다. 여러 개의 매치 결과를 모아둬야 한다면 `-match` 대신 `[regex]::Matches()`나 `Select-String -AllMatches`(46장)처럼 전체 결과 컬렉션을 반환하는 방법을 써야 한다.

**`-replace`의 치환 문자열에서 `$` 기호는 이중으로 조심해야 한다**: 정규식 치환 구문 자체가 `$1`, `${name}`처럼 `$`를 특수하게 쓰는데, 이 문자열이 큰따옴표라면 PowerShell이 `$1`을 변수로 먼저 해석하려 시도한다. 작은따옴표를 쓰거나, 부득이 큰따옴표를 쓴다면 `` `$1``처럼 백틱으로 이스케이프해야 한다. `$` 자체를 리터럴로 넣고 싶다면 `$$`를 쓴다.

**이식성**: Bash의 `[[ ... =~ ... ]]`나 `sed`의 정규식은 POSIX ERE/BRE 계열로 문법이 조금씩 다르며(예: 캡처 그룹 참조가 `\1`), PowerShell은 .NET 정규식(Perl 호환에 가까운 확장 문법, 이름 있는 캡처 그룹 `(?<name>...)` 등)을 그대로 쓴다는 점이 다르다. Bash `sed -E 's/pattern/replace/'`가 개념적으로 `-replace`에 대응한다.

## Reference

- [about_Regular_Expressions - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions)
