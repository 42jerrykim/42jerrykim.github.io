---
draft: true
collection_order: 71
slug: pester-describe-it-should-powershell
title: "[PowerShell] 71. Pester 소개 — Describe/It/Should"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 표준 테스트 프레임워크 Pester의 Describe/Context/It 블록 구조와 Should 어서션으로 함수 동작을 검증하는 법, BeforeAll로 테스트 대상 함수를 불러오는 법을 정리한 Part 8 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Testing(테스트)
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
- Pester
- unittest
- Describe-It
- Should-Assertion
- Test-Driven-Development
- Assertion
image: "wordcloud.png"
---

## 개요

**Pester**는 PowerShell 생태계의 표준 테스트 프레임워크로, 함수·스크립트가 의도한 대로 동작하는지 자동으로 검증하는 테스트 코드를 작성하게 해 준다. Part 6에서 함수를 만들고 Part 7에서 오류 처리를 다뤘다면, 이 장은 "그 함수가 실제로 옳게 동작하는지 어떻게 확신할 것인가"라는 질문에 답하며 Part 8(테스트와 코드 품질)을 시작한다. Windows PowerShell 5.1부터 기본 내장되어 있고, PowerShell 7에서도 별도 설치 없이 널리 쓰인다.

정신 모델은 "`Describe`는 테스트 대상을 이름 붙여 묶는 상자, `It`은 '이런 상황에서는 이래야 한다'는 개별 주장 하나, `Should`는 그 주장이 실제로 참인지 확인하는 검사기"라는 것이다.

## 사용법

```powershell
Describe '함수이름' {
    Context '시나리오 설명' {
        It '구체적인 기대 동작' {
            <실행> | Should -Be <기대값>
        }
    }
}
```

## 종류

| 요소 | 역할 |
|---|---|
| `Describe` | 테스트 대상을 묶는 최상위 블록(보통 함수 이름) |
| `Context` | `Describe` 안에서 시나리오별로 테스트를 더 세분화(선택 사항) |
| `It` | 검증 하나를 나타내는 최소 단위 |
| `Should -Be` | 값이 예상과 같은지 비교하는 대표적인 어서션(`-BeTrue`, `-Throw`, `-Contain` 등도 있음) |
| `BeforeAll`/`BeforeEach` | 테스트 실행 전 준비 작업(주로 테스트 대상 스크립트를 점 소싱으로 불러옴) |
| `Invoke-Pester` | 작성한 테스트 파일(`*.Tests.ps1`)을 실행하는 cmdlet |

## 예시

```powershell
# MathUtils.ps1
function Add-Numbers ($A, $B) { $A + $B }
```

```powershell
# MathUtils.Tests.ps1
BeforeAll {
    . $PSScriptRoot\MathUtils.ps1          # 53장에서 배운 점 소싱으로 테스트 대상 함수 불러오기
}

Describe 'Add-Numbers' {
    It '두 양수를 더하면 합을 반환한다' {
        Add-Numbers -A 2 -B 3 | Should -Be 5
    }

    It '음수를 더해도 정확히 계산한다' {
        Add-Numbers -A -2 -B 5 | Should -Be 3
    }

    Context '경계값 처리' {
        It '0을 더하면 원래 값을 반환한다' {
            Add-Numbers -A 10 -B 0 | Should -Be 10
        }
    }
}
```

```powershell
Invoke-Pester -Path .\MathUtils.Tests.ps1        # 테스트 실행

Describe 'Get-Config' {
    It '존재하지 않는 파일이면 예외를 던진다' {
        { Get-Config -Path "없는파일.json" } | Should -Throw    # 65장에서 배운 예외를 검증
    }
}
```

## 주의사항·함정

**`It` 블록 안의 스크립트 블록은 파이프라인 결과를 `Should`로 직접 넘겨야 검증이 이뤄진다**: `Add-Numbers -A 2 -B 3`을 그냥 실행만 하고 `Should`로 파이프하지 않으면, 결과가 화면에 출력만 될 뿐 아무것도 검증되지 않은 채 테스트가 "통과"로 표시된다 — 이는 진짜 통과가 아니라 애초에 아무것도 확인하지 않은 것이다. 예외를 검증할 때(`{ ... } | Should -Throw`)처럼 스크립트 블록으로 감싸야 하는 경우와, 값 자체를 파이프하는 경우를 구분해야 한다.

**`BeforeAll`에서 점 소싱을 빠뜨리면 테스트 대상 함수를 찾을 수 없다**: 테스트 파일과 실제 함수 정의 파일은 보통 분리돼 있으므로, `BeforeAll` 블록에서 53장의 점 소싱(`. $PSScriptRoot\파일.ps1`)으로 명시적으로 불러오지 않으면 "함수를 찾을 수 없다"는 오류가 난다. `$PSScriptRoot`를 써서 테스트 파일이 어디서 실행되든 상대 경로가 깨지지 않게 하는 것이 관례다.

**테스트가 서로의 상태에 의존하면 실행 순서가 바뀔 때 깨지기 쉽다**: 한 `It` 블록에서 만든 변수나 파일을 다른 `It` 블록이 가정하고 사용하면, 테스트를 하나만 따로 실행하거나 순서가 바뀌었을 때 예상치 못하게 실패한다. 각 `It`은 독립적으로 실행 가능하게 작성하는 것이 원칙이다.

**이식성**: Bash에는 `bats`, Python에는 `pytest`가 있듯 PowerShell에는 Pester가 사실상 유일한 표준 테스트 프레임워크로 자리 잡았다는 점이 특징이다. `Describe`/`It` 구조는 RSpec·Jasmine 같은 BDD(행위 주도 개발) 스타일 프레임워크의 문법을 그대로 계승해, 테스트 코드 자체가 "이 함수는 이래야 한다"는 자연어 문장에 가깝게 읽힌다.

## Reference

- [Pester Quick Start](https://pester.dev/docs/quick-start)
