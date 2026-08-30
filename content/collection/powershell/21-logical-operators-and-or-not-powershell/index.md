---
draft: false
collection_order: 21
slug: logical-operators-and-or-not-powershell
title: "[PowerShell] 21. 논리 연산자와 조건식 조합 — -and/-or/-not"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 논리 연산자(-and, -or, -xor, -not/!)로 여러 조건식을 조합하는 법, 단락 평가(short-circuit)로 뒤쪽 조건이 생략되는 규칙, 정수의 불리언 변환 규칙을 정리한 챕터다."
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
- Logical-Operators
- Short-Circuit
- Boolean
- Operator-Precedence
- Where-Object
- If-Statement
- Conditional-Logic
image: "wordcloud.png"
---

## 개요

논리 연산자는 여러 개의 조건식을 하나의 참/거짓 값으로 묶는다. `-and`, `-or`, `-xor`, `-not`(또는 `!`) 네 가지가 있으며, 20장의 비교 연산자와 짝을 이뤄 `Where-Object`·`if` 문에서 복합 조건을 표현하는 데 쓰인다.

정신 모델에서 중요한 것은 "단락 평가(short-circuit evaluation)"다. `-and`로 연결된 조건에서 왼쪽이 이미 거짓이면 오른쪽은 아예 평가하지 않고, `-or`로 연결된 조건에서 왼쪽이 이미 참이면 오른쪽을 평가하지 않는다. 이 덕분에 `if`문처럼 조건에 따라 실행 여부를 결정하는 용도로도 논리 연산자를 활용할 수 있다.

## 사용법

```powershell
<statement> {-and | -or | -xor} <statement>
{! | -not} <statement>
```

`-and`, `-or`, `-xor`는 모두 같은 우선순위를 가지며 왼쪽에서 오른쪽 순서로 평가된다(연산자 우선순위 전체는 `about_Operator_Precedence` 참고).

## 종류

| 연산자 | 참이 되는 조건 |
|---|---|
| `-and` | 양쪽 모두 참일 때 |
| `-or` | 둘 중 하나라도 참일 때 |
| `-xor` | 정확히 한쪽만 참일 때(배타적 논리합) |
| `-not` / `!` | 뒤따르는 값을 반전 |

## 예시

```powershell
(1 -eq 1) -and (1 -eq 2)              # False
(1 -eq 1) -or (1 -eq 2)               # True
(1 -eq 1) -xor (2 -eq 2)              # False (둘 다 참이라 배타적이지 않음)
-not (1 -eq 1)                        # False
!(1 -eq 1)                            # False (! 는 -not의 기호형)

($a -gt $b) -and (($a -lt 20) -or ($b -lt 20))    # 괄호로 우선순위 명시

# Where-Object에서 복합 조건
Get-Process | Where-Object { $_.CPU -gt 100 -and $_.WS -gt 50MB }

# 정수의 불리언 변환: 0은 거짓, 그 외는 모두 참
if (0) { "실행 안 됨" }
if (1) { "실행됨" }
```

## 주의사항·함정

**단락 평가는 부작용이 있는 표현식에서 특히 중요하다**: `$false -and (Remove-Item file.txt)`처럼 오른쪽에 실제 동작(파일 삭제)이 들어 있다면, 왼쪽이 거짓인 순간 오른쪽은 절대 실행되지 않는다. 조건과 실행할 동작을 논리 연산자로 압축해 쓸 때는 이 점을 반드시 의도해야 한다.

**`-xor`는 스위치 매개변수처럼 두 조건 다 참인 경우를 걸러낸다**: "둘 중 하나만"이라는 요구사항을 `-or`로 잘못 표현하면 둘 다 참인 경우까지 포함되는 실수가 흔하다. 정확히 하나만 참이어야 한다면 `-xor`를 써야 한다.

**정수의 불리언 변환 규칙을 정확히 알아야 한다**: 정수 `0`은 거짓(`$false`)으로, 그 외 모든 정수(음수 포함)는 참(`$true`)으로 변환된다. `if (-1) { ... }`도 참으로 평가되는 것은 이 규칙 때문이며, C 계열 언어의 직관과 다르지 않지만 명시적으로 확인해 두는 것이 좋다.

**이식성**: Bash의 `&&`/`||`도 단락 평가를 지원한다는 점은 같지만, Bash는 이 연산자를 명령어 사이(파이프라인 흐름 제어)에 쓰는 경우가 많은 반면 PowerShell의 `-and`/`-or`는 값·조건식 사이에 쓰는 순수한 논리 연산자다. CMD에는 이런 논리 연산자가 없어 `if`를 중첩하거나 `ERRORLEVEL`을 조합하는 방식으로 흉내 낸다.

## Reference

- [about_Logical_Operators - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logical_operators)
