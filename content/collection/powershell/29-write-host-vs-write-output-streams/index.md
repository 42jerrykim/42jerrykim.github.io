---
draft: true
collection_order: 29
slug: write-host-vs-write-output-streams-powershell
title: "[PowerShell] 29. Write-Host vs Write-Output — 출력 스트림 오개념 정리"
date: 2026-08-29
lastmod: 2026-08-29
description: "Write-Host가 정보 스트림에, Write-Output이 성공 스트림에 쓴다는 차이와 파이프라인 캡처 가능 여부, PowerShell의 6가지 출력 스트림 구조, 암묵적 출력과 Write-Output 생략 관례를 정리한 Part 3 마지막 챕터다."
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
- Write-Host
- Write-Output
- Output-Streams
- Success-Stream
- Information-Stream
- Redirection
- Misconception
image: "wordcloud.png"
---

## 개요

`Write-Host`와 `Write-Output`은 둘 다 화면에 텍스트를 표시할 수 있어서 같은 일을 하는 것처럼 보이지만, 실제로는 서로 다른 **출력 스트림**에 쓴다. 이 차이를 모르고 스크립트를 짜면 "화면에는 잘 보이는데 결과를 변수에 담거나 파이프로 넘기면 아무것도 안 잡힌다"는 대표적인 초보자 함정에 빠진다.

## 기본 개념

PowerShell은 출력을 용도별로 6개의 스트림으로 나눈다.

| 번호 | 스트림 | 관련 cmdlet |
|---|---|---|
| 1 | 성공(Success) | `Write-Output`(또는 암묵적 출력) |
| 2 | 오류(Error) | `Write-Error` |
| 3 | 경고(Warning) | `Write-Warning` |
| 4 | 상세(Verbose) | `Write-Verbose` |
| 5 | 디버그(Debug) | `Write-Debug` |
| 6 | 정보(Information) | `Write-Information`, 그리고 내부적으로 `Write-Host` |

`Write-Output`은 <strong>성공 스트림(파이프라인)</strong>에 객체를 보낸다 — 이것이 `Where-Object`·`Select-Object` 등 이 컬렉션에서 다룬 모든 cmdlet이 주고받는 바로 그 스트림이다. 반면 Windows PowerShell 5.0부터 `Write-Host`는 **정보 스트림**에 쓰는 `Write-Information`의 래퍼로 재구현됐다 — 화면(호스트)에 표시하는 것이 목적이고, 파이프라인으로는 흘러가지 않는다.

## 종류/세부

### 파이프라인 캡처 가능 여부

```powershell
$a = Write-Output "hello"     # $a = "hello" — 캡처됨
$b = Write-Host "hello"       # $b = $null   — 캡처 안 됨(화면에만 출력)

Write-Output "test" | Get-Member    # 문자열이 파이프로 전달되어 Get-Member가 처리
Write-Host "test" | Get-Member      # Write-Host는 아무것도 파이프로 보내지 않는다
```

### 암묵적 출력 — Write-Output은 대체로 생략한다

파이프라인 끝에서 자동으로 출력되는 값(함수의 마지막 식, `Get-Process` 등)에는 `Write-Output`을 굳이 쓸 필요가 없다. `Get-Process | Write-Output`은 그냥 `Get-Process`와 동등하며, PowerShell 커뮤니티 관례상 이런 명시적 호출은 불필요한 코드로 간주된다.

### 스트림별로 캡처하는 법

```powershell
Get-Process -Verbose 4>&1 | Out-File verbose.log     # 상세 스트림을 파일로 리다이렉션
Write-Host "no capture" -InformationAction Ignore     # 정보 스트림을 완전히 무시
Write-Host "no capture" 6> $null                      # 정보 스트림을 $null로 리다이렉션(6번 스트림)
```

## 주의사항·함정

**"화면에 보이니까 결과값이다"는 착각이 가장 흔한 오개념이다**: `Write-Host`로 출력한 값은 사람 눈에는 똑같이 보여도 함수의 반환값이나 파이프라인 결과에는 절대 포함되지 않는다. 함수 안에서 진행 상황을 사람에게 보여주고 싶으면 `Write-Host`(또는 `Write-Verbose`)를, 함수의 실제 결과를 반환하고 싶으면 값 자체를 그대로 두거나 `Write-Output` 없이 마지막 식으로 남기면 된다.

**`$InformationPreference`/`-InformationAction`은 `Write-Host`를 완전히는 제어하지 못한다**: `Write-Host`가 `Write-Information`의 래퍼이긴 하지만, `-InformationAction Ignore`를 제외한 다른 값들은 `Write-Host` 메시지의 표시 여부에 영향을 주지 않는다 — 하위 호환성을 위해 남겨진 예외적 동작이다. 확실히 숨기려면 `-InformationAction Ignore`나 `6> $null` 리다이렉션을 쓴다.

**해시테이블처럼 복잡한 객체를 `Write-Host`에 그냥 넘기면 `ToString()` 결과만 보인다**: `@{a=1;b=2} | Write-Host`는 `System.Collections.Hashtable`이라는 의미 없는 문자열만 출력한다. 의미 있는 텍스트가 필요하면 문자열 보간이나 `-f` 연산자로 직접 포맷하거나, `Out-String`을 거친 뒤 `Write-Host`에 넘긴다.

**이식성**: Bash의 `echo`는 표준 출력(stdout)에 쓰고 그대로 파이프로 흘러가므로 CMD·Bash 사용자는 "화면에 출력 = 파이프로도 전달"이라는 습관에 익숙하다. PowerShell에서는 이 등식이 성립하지 않는다는 것이 이 컬렉션 전체에서 가장 자주 반복해서 짚는 함정이다.

## Reference

- [Write-Host (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-host)
- [Write-Output (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-output)
