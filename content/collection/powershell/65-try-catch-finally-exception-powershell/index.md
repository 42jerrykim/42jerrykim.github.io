---
draft: true
collection_order: 65
slug: try-catch-finally-exception-powershell
title: "[PowerShell] 65. try/catch/finally — 예외 처리"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell try/catch/finally 문법과 종료 오류(terminating error)만 catch되는 원리, .NET 예외 타입별로 catch 블록을 나누는 법, $_ 자동 변수로 오류 정보를 꺼내는 법을 정리한 Part 7 시작 챕터다."
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
- Try-Catch
- Exception-Handling
- Terminating-Error
- ErrorRecord
- Finally-Block
- Try-Statement
image: "wordcloud.png"
---

## 개요

`try`/`catch`/`finally`는 스크립트 실행 중 발생한 오류를 감지하고 대응하는 PowerShell의 표준 예외 처리 구문이다. Part 6에서 함수와 스크립트를 재사용 가능한 단위로 만드는 법을 배웠다면, 이 장은 그 단위가 실패했을 때 프로그램 전체가 예기치 않게 멈추지 않도록 다루는 법을 배우며 Part 7(에러 처리와 진단)을 시작한다.

정신 모델은 "`try` 블록은 감시 구역이고, 그 안에서 <strong>종료 오류(terminating error)</strong>가 발생하면 나머지 문장은 건너뛰고 즉시 일치하는 `catch` 블록으로 점프한다"는 것이다. `finally` 블록은 오류 발생 여부와 무관하게 항상 마지막에 실행되어, 리소스 정리처럼 반드시 해야 할 뒷정리를 보장한다.

## 사용법

```powershell
try {
    <문장 목록>
}
catch [[<오류 타입>][',' <오류 타입>]*] {
    <오류 처리 문장>
}
finally {
    <항상 실행되는 문장>
}
```

## 종류

| 요소 | 설명 |
|---|---|
| `try` 블록 | 오류를 감시할 코드 구역, 최소 하나의 `catch` 또는 `finally`가 필요 |
| 타입 없는 `catch` | 어떤 종료 오류든 처리 |
| 타입 지정 `catch` | 특정 .NET 예외 타입(과 그 하위 타입)만 처리, 여러 `catch`를 나열 가능 |
| `finally` | 오류 발생 여부·Ctrl+C 중단과 무관하게 항상 실행 |
| `$_`/`$PSItem` | `catch` 블록 안에서 현재 오류(`ErrorRecord` 객체)를 가리킴 |

## 예시

```powershell
try { NonsenseString }
catch { "오류가 발생했습니다." }

try {
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile("https://example.com/doc.doc", "C:\temp\doc.doc")
}
catch [System.Net.WebException], [System.IO.IOException] {
    "파일 다운로드에 실패했습니다."
}
catch {
    "알 수 없는 오류가 발생했습니다."
}
finally {
    $wc.Dispose()
}

try { NonsenseString }
catch {
    Write-Host "오류: $($_.Exception.Message)"     # $_로 예외 세부 정보 접근
    Write-Host "위치: $($_.ScriptStackTrace)"
}

try {
    Remove-Item -Path "C:\존재하지않는파일.txt" -ErrorAction Stop   # 66장에서 다룰 -ErrorAction Stop 필수
}
catch [System.Management.Automation.ItemNotFoundException] {
    "파일이 없어서 삭제할 수 없습니다."
}
```

## 주의사항·함정

**`catch`는 종료 오류만 잡는다 — 비종료 오류는 그냥 지나쳐 버린다**: `Get-ChildItem 없는경로`처럼 대부분의 cmdlet이 내는 오류는 기본적으로 <strong>비종료 오류(non-terminating error)</strong>라 `try`/`catch`로 잡히지 않고 화면에 빨간 글씨만 남긴 채 다음 줄로 넘어간다. `try` 블록으로 반드시 잡고 싶은 명령이라면 66장에서 다룰 `-ErrorAction Stop`을 붙여 그 명령의 오류를 종료 오류로 강제 전환해야 한다 — 이 차이를 모르면 "`try`/`catch`로 감쌌는데 왜 오류가 안 잡히지?"라는 흔한 혼란에 빠진다.

**여러 `catch` 블록이 있을 때는 더 구체적인 타입을 먼저 써야 한다**: .NET 예외는 상속 관계를 따라 매칭되므로, 일반적인 부모 타입(`System.Exception`)을 자식 타입보다 앞에 두면 그 `catch`가 먼저 걸려 뒤에 있는 더 구체적인 `catch`는 절대 실행되지 않는다. 구체적인 예외부터 일반적인 예외 순서로 배치해야 의도한 대로 동작한다.

**`finally`는 `exit`나 Ctrl+C로 중단돼도 실행된다**: 이 점이 `finally`를 리소스 정리(파일 핸들 닫기, 임시 파일 삭제, 연결 해제)에 적합하게 만든다. 다만 파이프라인이 Ctrl+C로 멈추면 `finally` 안에서 화면에 출력한 내용 자체는 표시되지 않을 수 있으므로, `finally`의 역할은 "정리 작업 수행"이지 "사용자에게 메시지를 보여주는 것"으로 기대해서는 안 된다.

**이식성**: Bash는 `trap ERR`이나 `set -e`로 오류 발생 시 동작을 지정하지만, 특정 예외 타입별로 분기하는 문법 자체가 없다. CMD는 `%ERRORLEVEL%`을 매 명령 뒤에 수동으로 검사하는 방식이라 구조화된 예외 처리라고 부르기 어렵다. PowerShell의 `try`/`catch`/`finally`는 C#·Java 같은 예외 처리 모델을 그대로 셸 스크립팅에 가져온 설계로, 1장에서 강조한 .NET 기반 아키텍처의 또 다른 표현이다.

## Reference

- [about_Try_Catch_Finally - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally)
