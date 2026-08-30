---
draft: false
collection_order: 55
slug: switch-wildcard-regex-file-powershell
title: "[PowerShell] 55. switch 고급 모드 — 와일드카드/정규식/파일 처리"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell switch 문의 -Wildcard/-Regex/-File 매개변수와 break/continue로 흐름을 제어하는 법, 값을 문자열로 변환해 비교하는 기본 동작이 만드는 함정, default 절 사용법을 정리한 챕터다."
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
- Switch-Statement
- Wildcard
- Regex
- Break-Continue
- String-Conversion
- Default-Clause
image: "wordcloud.png"
---

## 개요

`switch` 문은 하나의 값을 여러 조건과 차례로 비교하는 구문으로, 54장에서 언급했듯 `elseif`가 여러 번 이어지는 상황을 대체하는 더 명료한 도구다. PowerShell의 `switch`는 다른 언어와 달리 **와일드카드**·**정규식**·**파일 한 줄씩 읽기**까지 지원한다는 점에서 훨씬 강력하다.

정신 모델은 "테스트 값을 조건 목록과 위에서부터 순서대로 비교하다가, 일치하는 모든 조건의 액션을 실행한다"는 것이다. C 계열 언어의 `switch`와 달리 **기본적으로 첫 일치에서 멈추지 않는다** — 이 차이가 아래 함정에서 가장 중요하게 다뤄진다.

## 사용법

```powershell
switch [-Regex | -Wildcard | -Exact] [-CaseSensitive] (<테스트 값>) {
    조건1 { <액션1> }
    조건2 { <액션2> }
    default { <일치하는 것이 없을 때> }
}
switch [-Regex | -Wildcard] [-CaseSensitive] -File <파일명> { ... }
```

## 종류

| 매개변수 | 설명 |
|---|---|
| (매개변수 없음, 기본) | `-Exact`와 동일 — 대소문자 구분 없는 정확한 일치 |
| `-Wildcard` | `*`, `?` 같은 와일드카드 패턴으로 비교 |
| `-Regex` | 정규식(47장)으로 비교, 일치 시 `$Matches` 변수 사용 가능 |
| `-CaseSensitive` | 위 모드들을 대소문자 구분 버전으로 |
| `-File <파일명>` | 파일을 한 줄씩 읽어 `switch`에 흘려보냄(대용량 파일에 `Get-Content`보다 효율적) |
| `break` | 그 즉시 `switch` 전체를 빠져나감 |
| `continue` | 현재 값 처리를 멈추고 다음 값으로 넘어감(배열 입력 시) |

## 예시

```powershell
switch (3) {
    1 { "하나입니다." }
    2 { "둘입니다." }
    3 { "셋입니다." }
}

switch ("fourteen") {
    1     { "하나"; break }
    "fo*" { "fo로 시작합니다" }
    default { "일치하는 것이 없습니다" }
}
# -Wildcard 없이는 "fo*"가 리터럴 문자열로 취급돼 일치하지 않음 → "일치하는 것이 없습니다" 출력

switch -Wildcard ("fourteen") {
    "fo*" { "fo로 시작합니다" }        # 이제는 일치
}

switch -Regex ($target) {
    '^ftp\://.*$'    { "$_ 는 ftp 주소입니다"; break }
    '^(http[s]?)\://.*$' { "$_ 는 $($Matches[1]) 웹 주소입니다"; break }
}

# 배열 입력과 continue — 음수는 건너뛰고, 숫자가 아니면 전체 중단
switch (1, 4, -1, 3, "Hello", 2, 1) {
    { $_ -lt 0 }          { continue }
    { $_ -isnot [int32] } { break }
    { $_ % 2 }            { "$_ 는 홀수입니다" }
    { -not ($_ % 2) }     { "$_ 는 짝수입니다" }
}

switch -Regex -File .\README.md {
    '^##\s' { break }              # 이 패턴을 만나면 파일 읽기 중단
    default { $_; continue }        # 그 전까지는 매 줄을 그대로 출력
}
```

## 주의사항·함정

**하나의 값이 여러 조건과 일치하면 기본적으로 모든 액션이 다 실행된다**: C·JavaScript의 `switch`는 `break`가 없으면 다음 case로 "흘러내리지만", PowerShell은 반대로 **명시적으로 `break`를 쓰지 않는 한 이후의 모든 일치 조건도 계속 검사해 전부 실행한다**. 조건 목록에 `3`이 두 번 있으면 두 액션이 모두 실행되는 것이 정상 동작이다. 다른 언어의 `switch`에 익숙하다면 이 반전된 기본값이 가장 흔한 실수의 원인이다 — 하나의 액션만 실행하고 끝내려면 각 블록 끝에 `break`를 명시해야 한다.

**모든 비교는 값을 문자열로 변환한 뒤 이뤄진다**: `switch`는 테스트 값과 조건을 비교하기 전에 둘 다 문자열로 바꾼다. `([datetime]'1 Jan 1970').DayOfWeek`처럼 열거형(enum) 값을 `switch`에 넘기면, 그 값의 숫자 표현이 아니라 "Thursday" 같은 문자열 표현과 비교된다 — 같은 조건을 `if ($x -eq $y)`로 검사했을 때와 결과가 달라질 수 있다. 이 자동 변환을 피하려면 조건 자리에 `{ $_ -eq $값 }`처럼 스크립트 블록을 써서 원래 타입 그대로 비교해야 한다.

**해시테이블을 `switch`에 넘기면 예상과 다르게 동작한다**: 44장에서 다룬 해시테이블을 `switch (테스트값)`에 그대로 넘기면, 해시테이블의 `.ToString()` 결과("System.Collections.Hashtable")와 비교된다 — 안의 키·값과는 비교되지 않는다. 해시테이블의 값을 검사하고 싶다면 먼저 `foreach`로 순회하며 각 값을 `switch`에 넘겨야 한다.

**이식성**: Bash의 `case ... esac`이 가장 가까운 대응이며 와일드카드 패턴을 기본 지원한다는 점은 비슷하지만, PowerShell처럼 정규식 모드나 파일 스트리밍 모드는 없다. CMD에는 `switch` 자체가 없어 여러 `if`를 연달아 쓰거나 `goto`로 흉내 낸다.

## Reference

- [about_Switch - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_switch)
