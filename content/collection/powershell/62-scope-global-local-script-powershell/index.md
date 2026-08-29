---
draft: true
collection_order: 62
slug: scope-global-local-script-powershell
title: "[PowerShell] 62. 스코프(Scope) — 전역/지역/스크립트"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 스코프 규칙과 Global:/Script:/Local: 스코프 수정자, 함수·스크립트가 만드는 자식 스코프의 상속 규칙, Private 옵션으로 변수를 숨기는 법, 모듈이 만드는 독립된 스코프 계층을 정리한 챕터다."
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
- Scope
- Global-Scope
- Script-Scope
- Scope-Modifier
- Child-Scope
- Private-Variable
image: "wordcloud.png"
---

## 개요

**스코프**는 변수·함수·별칭·PSDrive가 어디에서 보이고 바뀔 수 있는지를 결정하는 경계다. 41장에서 "변수는 자신이 만들어진 블록 안에서만 보인다"고 짧게 언급했던 원칙을, 이 장에서 전역·지역·스크립트라는 이름 붙은 스코프와 스코프 수정자(scope modifier)로 정식으로 정리한다. 53장의 스크립트 스코프, 57장의 함수 스코프가 실제로는 모두 이 규칙 위에서 동작한다.

정신 모델은 "스코프는 부모-자식 관계로 중첩된 상자이고, 자식 상자는 부모 상자 안의 물건을 읽을 수 있지만, 자식이 뭔가를 새로 만들거나 바꾸면 그 변화는 기본적으로 자식 상자 안에만 남는다"는 것이다.

## 사용법

```powershell
$변수 = 값                       # 현재(지역) 스코프에 생성
$Global:변수 = 값                 # 전역 스코프에 생성/수정
$Script:변수 = 값                 # 가장 가까운 스크립트 파일의 스코프에 생성/수정
function Global:함수이름 { ... }    # 전역 스코프에 함수 정의
```

## 종류

| 스코프 이름 | 의미 |
|---|---|
| Global | PowerShell 시작 시 만들어지는 최상위 스코프, 프로필(06장)의 변수·함수도 여기 생성됨 |
| Local | "현재" 스코프 — 상황에 따라 전역이거나 그 안의 자식일 수 있음 |
| Script | 스크립트 파일이 실행되는 동안 그 파일 전용으로 만들어지는 스코프 |
| Private(옵션) | 스코프가 아니라 옵션 — 자식 스코프에서도 안 보이게 숨김 |
| 번호 스코프 | `-Scope 0`(현재)부터 `-Scope 1`(부모), `-Scope 2`(조부모)처럼 상대 위치로 참조 |

## 예시

```powershell
$test = "전역"                     # 전역 스코프에 생성(스크립트 밖 대화형 세션 기준)

function Show-Test {
    $test = "지역"                  # 함수 안의 새 지역 변수 — 전역 $test와는 별개
    "함수 안: $test"
    "Global 수정자로 본 전역 값: $Global:test"
}
Show-Test                            # "함수 안: 지역", "Global 수정자로 본 전역 값: 전역"
$test                                # 여전히 "전역" — 함수가 바꾸지 않았음

function Set-GlobalTest {
    $Global:test = "함수가 바꾼 전역값"   # 명시적으로 전역 스코프를 지정해 수정
}
Set-GlobalTest
$test                                  # "함수가 바꾼 전역값"으로 실제 변경됨

$Private:secret = "숨김"                # Private 옵션 — 자식 스코프에서 안 보임
function Show-Secret { $secret }         # 결과: 빈 값(부모의 private 변수를 못 봄)

Get-Variable -Scope Local                 # 현재 스코프의 변수 목록
Get-Variable test -Scope 1                 # 부모 스코프의 test 값 직접 조회

. .\UtilityFunctions.ps1                    # 점 소싱(53장) — 스크립트를 현재 스코프에서 실행
```

## 주의사항·함정

**함수·스크립트 안에서의 대입은 기본적으로 "새 지역 변수 생성"이지 "부모 변수 수정"이 아니다**: 부모 스코프에 같은 이름의 변수가 있어도, 자식 스코프에서 `$x = 값`을 실행하면 참조가 아니라 그 스코프에 새 변수를 만드는 것이다. 부모의 원본 값을 실제로 바꾸고 싶다면 `$Global:x = 값`이나 `$Script:x = 값`처럼 스코프를 명시해야 한다 — 이 규칙을 놓치면 "함수 안에서 분명히 값을 바꿨는데 밖에서는 그대로다"라는 흔한 혼란에 빠진다.

**모듈은 스크립트나 함수와 달리 전역 스코프의 자식이 아니다**: 74장에서 다룰 모듈은 임포트된 지점의 스코프에 연결된 독립된 병렬 스코프 컨테이너를 만든다. 모듈 안의 `$a`와 세션의 전역 `$a`는 완전히 다른 변수이며, 모듈 함수 안에서 `$Global:a`로 명시해야만 세션의 전역 변수에 접근한다 — 지금 당장은 "모듈은 스코프 규칙이 조금 다르다"는 점만 기억해 두고, 74장에서 자세히 다룬다.

**`Private` 옵션은 스코프가 아니라 가시성 제한이라 혼동하기 쉽다**: `Private:` 수정자로 만든 변수는 그것을 만든 스코프 안에서는 정상적으로 보이지만, 그 스코프의 **자식** 스코프에서는 `Global:`을 붙여도 보이지 않는다. "전역 스코프에 있으니 어디서든 보이겠지"라고 생각하면 이 예외적인 동작에 놀라기 쉽다.

**이식성**: Bash는 기본적으로 모든 변수가 전역이고, 함수 안에서만 지역으로 만들려면 명시적으로 `local` 키워드를 써야 한다 — PowerShell과 정반대 기본값이다. CMD는 `setlocal`/`endlocal`로 배치 파일 전체의 변수 변경을 되돌릴 수는 있지만, PowerShell처럼 함수 단위의 세밀한 스코프 계층 구조는 없다.

## Reference

- [about_Scopes - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scopes)
