---
draft: true
collection_order: 56
slug: foreach-for-while-loop-powershell
title: "[PowerShell] 56. foreach/for/while/do-while — 반복문"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell foreach 문 문법과 ForEach-Object cmdlet의 차이, for/while/do-while/do-until 반복문의 사용법, break/continue로 반복을 제어하는 법을 비교하며 정리한 챕터다."
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
- Foreach-Loop
- For-Loop
- While-Loop
- Break-Continue
- Iteration
- Loop-Label
image: "wordcloud.png"
---

## 개요

PowerShell은 반복을 표현하는 네 가지 문(statement) — `foreach`, `for`, `while`, `do`— 을 제공한다. 15장에서 배운 `ForEach-Object` cmdlet은 파이프라인 객체를 하나씩 처리하는 도구였다면, 이 장의 `foreach` **문**(키워드)은 언어 자체의 반복 구문으로 컬렉션 전체를 메모리에 올려놓고 순회한다는 점이 근본적으로 다르다.

정신 모델은 "컬렉션을 이미 다 갖고 있다면 `foreach`, 반복 횟수나 조건으로 직접 제어하고 싶다면 `for`/`while`/`do`"라는 것이다. 어떤 반복문이든 `break`(반복 전체 종료)와 `continue`(현재 반복만 건너뛰고 다음으로)로 흐름을 제어할 수 있다.

## 사용법

```powershell
foreach ($항목 in $컬렉션) { <문장 목록> }
for ($초기화; $조건; $반복) { <문장 목록> }
while (<조건>) { <문장 목록> }
do { <문장 목록> } while (<조건>)
do { <문장 목록> } until (<조건>)
```

## 종류

| 구문 | 조건 검사 시점 | 용도 |
|---|---|---|
| `foreach` | — | 배열·컬렉션의 각 항목을 순회 |
| `for` | 각 반복 시작 전 | 반복 횟수를 카운터로 직접 제어할 때 |
| `while` | 각 반복 시작 전 | 조건이 참인 동안 반복(0번 실행될 수 있음) |
| `do...while` | 각 반복이 끝난 뒤 | 최소 1번은 반드시 실행해야 할 때 |
| `do...until` | 각 반복이 끝난 뒤(조건이 참이 되면 종료) | `while`의 반대 논리로 종료 조건을 표현할 때 |

## 예시

```powershell
$letterArray = 'a', 'b', 'c', 'd'
foreach ($letter in $letterArray) {
    Write-Host $letter
}

foreach ($file in Get-ChildItem) {          # cmdlet 결과도 그대로 순회 가능
    if ($file.Length -gt 100KB) {
        Write-Host $file
    }
}

for ($i = 0; $i -lt 5; $i++) {               # 카운터 기반 반복
    Write-Host "반복 $i"
}

$i = 0
while ($i -lt 5) {                            # 조건이 거짓이면 한 번도 실행 안 될 수 있음
    Write-Host $i
    $i++
}

$i = 0
do {
    Write-Host $i                             # 조건과 무관하게 최소 1번 실행
    $i++
} while ($i -lt 5)

do {
    $input = Read-Host "종료하려면 'quit' 입력"
} until ($input -eq 'quit')

foreach ($n in 1..10) {
    if ($n -eq 5) { continue }                # 5는 건너뛰고
    if ($n -eq 8) { break }                    # 8에서 반복 전체 종료
    Write-Host $n
}
```

## 주의사항·함정

**`foreach` 문과 `ForEach-Object` cmdlet은 이름은 비슷해도 동작 방식이 다르다**: `foreach ($x in $collection)`은 컬렉션 전체가 메모리에 이미 있어야 순회를 시작할 수 있는 반면, `ForEach-Object`는 10장에서 배운 파이프라인 방식대로 객체가 하나씩 도착하는 대로 즉시 처리한다. 매우 큰 컬렉션을 다룰 때는 `ForEach-Object`가 메모리를 더 적게 쓰지만, `foreach` 문은 반복 중간에 `break`로 즉시 빠져나갈 수 있다는 장점이 있다 — `ForEach-Object`의 스크립트 블록 안에서는 `break`가 예상과 다르게 동작한다.

**`while`과 `do...while`은 조건 검사 시점이 달라 결과가 갈릴 수 있다**: 조건이 처음부터 거짓이면 `while`은 블록을 한 번도 실행하지 않지만, `do...while`은 무조건 최소 한 번은 실행한 뒤에야 조건을 검사한다. "사용자에게 최소 한 번은 메뉴를 보여줘야 한다"처럼 최초 실행이 보장돼야 하는 로직에는 `do...while`이 적합하고, "조건이 맞을 때만 시작해야 한다"면 `while`을 써야 한다.

**중첩 반복문에서 `break`는 기본적으로 가장 안쪽 반복만 빠져나간다**: 바깥쪽 반복까지 한 번에 종료하려면 반복문에 레이블(`:outer`처럼 콜론으로 시작하는 이름)을 붙이고 `break outer`처럼 레이블을 지정해야 한다. 레이블 없이 `break`만 쓰면 가장 가까운 반복문만 종료된다는 점을 놓치면, 중첩 반복이 예상보다 오래 계속 도는 버그로 이어진다.

**이식성**: Bash의 `for x in list; do ... done`, `while ... do ... done`과 개념은 같지만 PowerShell은 조건을 항상 소괄호로 감싼다는 문법 차이가 있다. CMD의 `for`는 파일·목록·숫자 범위마다 옵션(`/f`, `/l`, `/d`)이 갈리는 하나의 명령이라, PowerShell처럼 네 가지 반복 **문**으로 명확히 나뉘어 있는 쪽이 각 상황의 의도를 더 분명히 드러낸다.

## Reference

- [about_Foreach - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_foreach)
