---
draft: true
collection_order: 67
slug: trap-legacy-exception-powershell
title: "[PowerShell] 67. trap — 레거시 예외 처리"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell trap 키워드로 스코프 전체의 종료 오류를 처리하는 법과 break/continue로 이후 실행 여부를 결정하는 법, try/catch가 표준이 된 오늘날 trap을 써야 할 때와 스코프 규칙의 차이를 정리한 챕터다."
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
- Trap-Statement
- Legacy-Code
- Break-Continue
- Scope
- Exception-Type
- Error-Handling-Legacy
image: "wordcloud.png"
---

## 개요

`trap`은 `try`/`catch`/`finally`(65장)보다 먼저 PowerShell에 도입된 예외 처리 키워드로, 지금은 대부분 `try`/`catch`로 대체됐지만 오래된 스크립트나 특정 상황에서는 여전히 마주치게 된다. `trap`은 `catch`처럼 특정 코드 블록만 감시하는 것이 아니라, **자신이 정의된 스코프 전체**에 적용된다는 점이 근본적으로 다르다.

정신 모델은 "`trap`은 그 스코프 안 어디에서 종료 오류가 나든 걸리는 그물이고, `try`/`catch`는 명시적으로 감싼 블록만 감시하는 좁은 창"이라는 것이다. 오늘날 새 코드에서는 65장의 `try`/`catch`가 표준이지만, 기존 코드를 유지보수하려면 `trap`의 동작 원리를 알아야 한다.

## 사용법

```powershell
trap [[<오류 타입>]] {
    <문장 목록>
}
```

## 종류

| 동작 | 결과 |
|---|---|
| 아무 키워드 없이 끝남(기본) | 오류를 표시한 뒤 `trap`이 정의된 블록의 다음 문장부터 계속 실행 |
| `break` | 오류를 표시한 뒤 `trap`이 정의된 함수·스크립트 실행을 완전히 중단 |
| `continue` | 오류를 표시하지 **않고** 조용히 다음 문장부터 계속 실행 |
| 타입 지정 `trap` | 특정 .NET 예외 타입만 처리(여러 `trap`을 두면 가장 구체적으로 일치하는 것 우선) |

## 예시

```powershell
function TrapTest {
    trap { "오류를 잡았습니다." }
    NonsenseString
    "이 줄도 실행됩니다 — 기본 동작은 계속 진행"
}
TrapTest

function BreakExample {
    trap {
        "오류를 잡았습니다"
        break                      # 여기서 함수 실행 중단
    }
    1 / $null
    "이 줄은 실행되지 않습니다"
}

function ContinueExample {
    trap {
        "오류를 잡았습니다"
        continue                    # 오류 메시지 없이 조용히 계속
    }
    foreach ($x in 3..-1) { "1/$x = $(1/$x)" }
    "함수 종료"                       # 실행됨
}

trap [System.Management.Automation.CommandNotFoundException] {
    "명령을 찾을 수 없는 오류"
}
trap {
    "그 외 모든 종료 오류"
}
NonsenseString                        # 더 구체적인 첫 번째 trap이 처리
```

## 주의사항·함정

**`trap`은 정의된 위치와 무관하게 그 스코프 전체에 미리 적용된다("호이스팅")**: JavaScript의 함수 호이스팅과 비슷하게, 스크립트 맨 끝에 `trap`을 적어도 그 스코프의 첫 문장에서 발생한 오류부터 이미 적용된다. 코드를 위에서 아래로 읽으며 "여기까지는 아직 trap이 없겠지"라고 가정하면 실제 동작과 어긋난다.

**`trap`이 있는 스코프 밖에서 오류가 나면, `trap` 처리 후 그 함수로 다시 돌아가지 않는다**: 오류가 발생한 함수 안에 `trap`이 있으면 처리 후 그 함수 안에서 계속 실행되지만, `trap`이 오류가 난 함수의 **바깥**(호출자 쪽)에 있으면 처리 후 함수 안으로 다시 들어가지 않고 호출자 스코프의 다음 문장으로 넘어간다. 이 미묘한 차이 때문에 "trap이 걸렸는데 왜 함수의 나머지 부분이 실행되지 않지?"라는 혼란이 자주 발생한다.

**여러 `trap`이 같은 오류 타입을 겨냥하면 스크립트상 가장 먼저 나온 것만 실행된다**: `catch`처럼 상속 관계로 매칭하는 것은 같지만, 완전히 동일한 조건의 `trap`이 여럿이면 나중 것은 무시된다는 점에서 여러 `catch` 블록을 순서대로 쌓을 수 있는 `try`/`catch`보다 유연성이 떨어진다.

**새 코드에서는 `try`/`catch`/`finally`를 우선 고려해야 한다**: 공식 문서도 "더 세밀한 오류 처리가 필요하면 `try`/`catch`를 쓰라"고 명시한다 — `trap`은 스코프 전체에 암묵적으로 걸리는 특성 때문에 코드가 복잡해질수록 어디서 어떤 trap이 발동할지 추적하기 어려워진다. `trap`은 레거시 코드 유지보수나 스코프 전체에 일괄 안전망을 걸어야 하는 특수한 상황에만 남겨 두는 편이 좋다.

**이식성**: Bash의 `trap 'command' ERR`이 이름과 "스코프(셸 전체)에 걸리는 그물"이라는 개념 면에서 가장 유사하다 — 둘 다 특정 블록이 아니라 실행 환경 전체에 핸들러를 등록한다는 공통점이 있다. CMD에는 대응하는 개념이 없다.

## Reference

- [about_Trap - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_trap)
