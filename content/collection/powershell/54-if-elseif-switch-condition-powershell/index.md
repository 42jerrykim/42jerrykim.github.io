---
draft: false
collection_order: 54
slug: if-elseif-switch-condition-powershell
title: "[PowerShell] 54. if/elseif/else — 조건 분기"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell if/elseif/else 문법과 조건식 평가 방식, PowerShell 7부터 도입된 삼항 연산자(?:) 문법, elseif 체인이 길어질 때 switch 문으로 바꿔야 하는 이유를 정리한 챕터다."
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
- If-Statement
- Conditional
- Ternary-Operator
- Flow-Control
- Boolean
- Branching
image: "wordcloud.png"
---

## 개요

`if`/`elseif`/`else`는 조건에 따라 서로 다른 코드 블록을 실행하는 가장 기본적인 흐름 제어 구문이다. 20장의 비교 연산자(`-eq`, `-gt` 등)와 21장의 논리 연산자(`-and`, `-or`)가 만들어내는 참/거짓 값을 실제로 분기에 사용하는 자리가 바로 이 장이다.

정신 모델은 "각 조건을 위에서부터 순서대로 검사하다가, 처음으로 참(true)인 조건을 만나면 그 블록만 실행하고 나머지는 전부 건너뛴다"는 것이다. 어떤 조건도 참이 아니면 마지막 `else` 블록(있다면)이 실행된다.

## 사용법

```powershell
if (<조건1>) {
    <문장 목록 1>
}
elseif (<조건2>) {
    <문장 목록 2>
}
else {
    <문장 목록 3>
}
```

## 종류

| 형태 | 설명 |
|---|---|
| 단순 `if` | 조건이 참일 때만 실행, 거짓이면 아무 일도 안 함 |
| `if`/`else` | 참·거짓 두 갈래 처리 |
| `if`/`elseif`/.../`else` | 여러 조건을 순서대로 검사 |
| 삼항 연산자(`? :`) | PowerShell 7.0+, C# 스타일의 한 줄 조건식 |

## 예시

```powershell
if ($a -gt 2) {
    Write-Host "$a는 2보다 큽니다."
}

if ($a -gt 2) {
    Write-Host "$a는 2보다 큽니다."
}
else {
    Write-Host "$a는 2 이하이거나 초기화되지 않았습니다."
}

if ($a -gt 2) {
    Write-Host "$a는 2보다 큽니다."
}
elseif ($a -eq 2) {
    Write-Host "$a는 2와 같습니다."
}
else {
    Write-Host "$a는 2보다 작습니다."
}

# PowerShell 7+ 삼항 연산자
$message = (Test-Path $path) ? "경로가 존재합니다" : "경로를 찾을 수 없습니다"

$service = Get-Service BITS
$service.Status -eq 'Running' ? (Stop-Service $service) : (Start-Service $service)
```

## 주의사항·함정

**삼항 연산자에서 명령을 실행하려면 반드시 괄호로 감싸야 한다**: `(조건) ? Write-Host 'a' : Write-Host 'b'`처럼 참·거짓 분기에 명령을 그대로 쓰면 파싱 오류가 난다. `(조건) ? (Write-Host 'a') : (Write-Host 'b')`처럼 각 분기를 괄호로 감싸야 한다 — 삼항 연산자는 "값을 고르는 표현식"이지 "명령을 실행하는 문장"이 아니라는 설계 의도가 이 제약에 드러난다.

**`elseif`가 길게 이어지면 가독성이 급격히 떨어진다**: 같은 변수를 여러 값과 비교하는 `elseif` 체인이 4–5개를 넘어가면, 55장에서 다룰 `switch` 문으로 바꾸는 편이 훨씬 읽기 쉽고 관리하기도 편하다. 공식 문서도 `elseif`가 여러 개 필요한 상황에서는 `switch`를 권장한다.

**조건식은 항상 불리언으로 강제 변환된다**: `if ($a)`처럼 조건 자리에 불리언이 아닌 값(문자열, 숫자, 컬렉션)을 그대로 넣으면 PowerShell이 자동으로 참/거짓으로 변환한다 — 빈 문자열·`0`·`$null`·빈 배열은 거짓, 그 외 대부분은 참으로 취급된다. 이 자동 변환 규칙(41장에서 다룬 값-타입 원칙의 연장)을 모르면 `if ($result)`가 왜 예상과 다르게 동작하는지 헷갈리기 쉽다.

**이식성**: Bash의 `if [ ... ]; then ... elif ... else ... fi`, CMD의 `if ... else if ... else`와 개념은 같지만, PowerShell은 대괄호 대신 소괄호로 조건을 감싸고 `then`/`fi` 같은 종료 키워드 없이 중괄호로 블록을 구분한다는 문법 차이가 있다. 삼항 연산자는 Bash·CMD에 대응 문법이 없어 각각 `[ 조건 ] && cmd1 || cmd2`나 별도 `if` 블록으로 흉내 내야 한다.

## Reference

- [about_If - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_if)
