---
draft: true
collection_order: 66
slug: erroractionpreference-command-powershell
title: "[PowerShell] 66. $ErrorActionPreference와 -ErrorAction/-ErrorVariable"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell $ErrorActionPreference 기본 설정 변수와 명령별로 재정의하는 -ErrorAction 공통 매개변수의 관계, Continue/Stop/SilentlyContinue 값의 차이, -ErrorVariable로 오류를 변수에 담는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Error-Handling
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
- ErrorActionPreference
- ErrorAction
- ErrorVariable
- Non-Terminating-Error
- Preference-Variable
- Error-Stream
image: "wordcloud.png"
---

## 개요

`$ErrorActionPreference`는 비종료 오류가 발생했을 때 PowerShell이 기본적으로 어떻게 반응할지를 정하는 설정 변수이고, `-ErrorAction`은 25장에서 다룬 공통 매개변수 중 하나로 특정 명령 **하나**에 대해서만 그 기본값을 재정의한다. 65장에서 "`try`/`catch`는 종료 오류만 잡는다"고 짚었던 그 간극을 메우는 것이 바로 이 두 설정이다 — 비종료 오류를 종료 오류로 승격시켜야 `catch`가 잡을 수 있다.

정신 모델은 "`$ErrorActionPreference`는 세션 전체의 기본 반응 정책이고, `-ErrorAction`은 그 정책을 명령 단위로 덮어쓰는 스위치"라는 것이다.

## 사용법

```powershell
$ErrorActionPreference = "Stop"                # 세션(또는 스코프) 전체 기본값 변경
명령어 -ErrorAction Stop                          # 이 명령에만 적용
명령어 -ErrorVariable 변수이름                      # 오류를 변수에 저장(누적 시 +변수이름)
```

## 종류

| 값 | 동작 |
|---|---|
| `Continue`(기본값) | 오류 메시지를 표시하고 다음 문장으로 계속 진행 |
| `Stop` | 오류를 종료 오류로 전환 — `try`/`catch`가 잡을 수 있게 됨 |
| `SilentlyContinue` | 오류 메시지를 표시하지 않고 계속 진행(단, `$Error`에는 여전히 기록됨) |
| `Ignore` | 오류를 아예 기록하지 않음(PowerShell 3.0+, `$Error`에도 안 남음) |
| `Inquire` | 오류가 나면 계속할지 사용자에게 물어봄 |
| `-ErrorVariable`(별칭 `-ev`) | 그 명령의 오류를 지정한 변수에 저장, 이름 앞에 `+`를 붙이면 기존 값에 누적 |

## 예시

```powershell
Get-ChildItem "존재하지않는경로" -ErrorAction SilentlyContinue    # 오류 메시지 숨기고 계속
Get-ChildItem "존재하지않는경로" -ErrorAction Stop                 # 이 명령만 종료 오류로 전환

try {
    Get-ChildItem "존재하지않는경로" -ErrorAction Stop              # 이제 try/catch가 잡을 수 있음
}
catch {
    "경로를 찾을 수 없습니다: $($_.Exception.Message)"
}

$ErrorActionPreference = "Stop"          # 이후 모든 명령이 기본적으로 종료 오류로 취급됨
try {
    Get-ChildItem "존재하지않는경로"       # -ErrorAction 없이도 이제 catch됨
}
catch { "잡혔습니다." }
$ErrorActionPreference = "Continue"       # 원래 기본값으로 복원

Get-ChildItem "a", "존재하지않는경로", "b" -ErrorVariable myErrors -ErrorAction SilentlyContinue
$myErrors.Count                            # 발생한 오류 개수 확인

Get-ChildItem "a" -ErrorVariable +myErrors  # 앞에 +를 붙이면 기존 변수에 누적
```

## 주의사항·함정

**`$ErrorActionPreference`를 전역으로 바꾼 뒤 되돌리는 것을 잊기 쉽다**: 스크립트 안에서 `$ErrorActionPreference = "Stop"`을 설정하고 원래 값으로 복원하지 않으면, 그 이후 실행되는 다른 코드까지 예상치 못하게 모든 오류를 종료 오류로 취급하게 된다. 특정 블록에서만 이 설정이 필요하다면, 62장에서 배운 스코프 개념을 활용해 함수 안에서만 지역적으로 바꾸거나, 작업이 끝난 뒤 원래 값으로 되돌리는 습관이 안전하다. 더 안전한 대안은 전역 변수 대신 문제가 되는 그 명령 하나에만 `-ErrorAction Stop`을 붙이는 것이다.

**`-ErrorAction`은 그 명령 자체의 오류에만 적용되고, 그 명령이 내부적으로 호출하는 다른 명령에는 전파되지 않는다**: 함수 안에서 여러 cmdlet을 호출하는데 그 함수 호출부에만 `-ErrorAction Stop`을 붙였다고 해서, 함수 내부의 모든 cmdlet이 자동으로 종료 오류를 내는 것은 아니다 — 함수 내부 로직 자체가 오류를 어떻게 처리할지 별도로 설계해야 한다.

**`SilentlyContinue`는 오류를 숨길 뿐 지운 것은 아니다**: 화면에 표시되지 않아도 오류는 여전히 `$Error` 자동 변수에 기록된다. 오류 자체를 완전히 무시하고 기록도 남기지 않으려면 `Ignore`를 써야 한다 — 이 차이를 모르면 "분명히 `SilentlyContinue`로 숨겼는데 `$Error`에는 왜 남아 있지?"라는 혼란을 겪을 수 있다.

**이식성**: Bash의 `set -e`(오류 시 즉시 종료)가 `$ErrorActionPreference = "Stop"`과 개념적으로 가장 가깝지만, Bash는 명령 단위로 이 설정을 세밀하게 재정의하는 표준 문법이 없어 서브셸이나 조건부 실행(`command || true`)으로 우회해야 한다. PowerShell은 전역 기본값과 명령별 재정의를 명확히 분리된 두 계층으로 제공한다는 점이 다르다.

## Reference

- [about_Preference_Variables - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)
