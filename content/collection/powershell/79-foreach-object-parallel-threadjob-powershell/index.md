---
draft: false
collection_order: 79
slug: foreach-object-parallel-threadjob-powershell
title: "[PowerShell] 79. ForEach-Object -Parallel(PowerShell 7+)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 7의 ForEach-Object -Parallel로 반복 작업을 스레드 기반으로 병렬 실행하는 법과 -ThrottleLimit, $using: 스코프 수정자로 외부 변수를 전달하는 법, 78장 Start-Job과의 성능·격리 차이를 정리한 Part 9 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Module(모듈)
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
- ForEach-Object-Parallel
- ThrottleLimit
- Using-Scope
- Runspace
- Thread-Safety
- Parallel-Processing
image: "wordcloud.png"
---

## 개요

PowerShell 7부터 `ForEach-Object`에 추가된 `-Parallel` 매개변수는 15장에서 배운 반복 처리를 여러 스레드에 나눠 동시에 실행한다. 78장의 `Start-Job`이 무거운 별도 프로세스를 띄우는 방식이라면, `ForEach-Object -Parallel`은 같은 프로세스 안에서 여러 <strong>런스페이스(Runspace)</strong>를 병렬로 돌려 훨씬 가볍고 빠르게 반복 작업을 나눠 처리한다. Part 9(모듈과 병렬 처리)의 마지막 챕터로서, 지금까지 이 컬렉션이 순차적으로 실행해 온 모든 작업에 "동시에"라는 축을 더한다.

정신 모델은 "각 반복(iteration)이 독립된 미니 세션에서 실행되므로, 바깥 스코프의 변수는 자동으로 보이지 않는다"는 것이다 — 62장에서 배운 스코프 규칙이 병렬 실행에서는 훨씬 엄격하게 적용되며, `$using:` 스코프 수정자로 명시적으로 값을 전달해야 한다.

## 사용법

```powershell
<입력> | ForEach-Object -Parallel { <각 $_ 마다 실행할 코드, $using:변수로 외부값 참조> } [-ThrottleLimit <N>]
```

## 종류

| 요소 | 설명 |
|---|---|
| `-Parallel` | 병렬 실행할 스크립트 블록(필수) |
| `-ThrottleLimit` | 동시에 실행할 최대 스레드 수(기본값 5) |
| `$using:변수` | 호출 스코프의 변수 값을 병렬 스레드로 전달(63장에서 배운 클로저와 유사한 개념) |
| `-AsJob` | 결과를 즉시 스트리밍하지 않고 78장에서 배운 Job 객체로 반환 |
| `-TimeoutSeconds` | 지정한 시간이 지나면 남은 작업을 중단 |
| 스레드 안전 컬렉션 | 여러 스레드가 동시에 값을 써야 한다면 `System.Collections.Concurrent.*` 타입 필요 |

## 예시

```powershell
$Message = "처리 중"
1..8 | ForEach-Object -Parallel {
    "$Using:Message $_"
    Start-Sleep 1
} -ThrottleLimit 4                                          # 최대 4개씩 동시 실행

$logNames = 'Security', 'Application', 'System'
$entries = $logNames | ForEach-Object -Parallel {
    Get-WinEvent -LogName $_ -MaxEvents 1000                  # 로그별로 동시에 수집
} -ThrottleLimit 3
$entries.Count

$job = 1..10 | ForEach-Object -Parallel {
    "Output: $_"; Start-Sleep 1
} -ThrottleLimit 2 -AsJob                                    # Job으로 백그라운드 실행
$job | Receive-Job -Wait

# 스레드 안전 컬렉션으로 결과 안전하게 수집(44장 해시테이블은 이 용도로 부적합)
$dict = [System.Collections.Concurrent.ConcurrentDictionary[string,object]]::new()
Get-Process | ForEach-Object -Parallel {
    $d = $Using:dict
    $d.TryAdd($_.ProcessName, $_)
}

1..3 | ForEach-Object -Parallel { throw "오류: $_" }            # 하나가 실패해도 나머지는 계속 실행됨
```

## 주의사항·함정

**병렬 스크립트 블록은 매번 새 런스페이스를 만드는 비용이 있어, 가벼운 작업에는 오히려 손해다**: 반복마다 하는 일이 아주 짧다면(단순 계산 등), 런스페이스 생성 오버헤드가 실제 작업 시간보다 커서 순차 `ForEach-Object`보다 **느려진다**. `-Parallel`은 파일 I/O나 네트워크 대기처럼 "기다리는 시간이 긴 작업", 또는 CPU를 많이 쓰는 계산에 쓸 때 이득이 크다.

**바깥 스코프 변수는 `$using:` 없이는 아예 보이지 않는다**: 62장의 일반적인 자식 스코프 규칙(부모 값을 읽을 수는 있다)과 달리, `-Parallel` 스크립트 블록은 완전히 분리된 스레드에서 실행되므로 `$using:` 접두사 없이 외부 변수를 참조하면 빈 값이 나온다. 이는 78장의 `Start-Job`이 별도 프로세스라 상태를 아예 공유하지 않는 것과 비슷한 이유에서 비롯된 제약이다.

**여러 스레드가 같은 객체를 동시에 수정하면 데이터가 손상될 수 있다**: 44장의 일반 해시테이블처럼 스레드에 안전하지 않은 컬렉션에 병렬 스레드가 동시에 값을 추가하면 예외가 나거나 일부 값이 유실될 수 있다. 여러 스레드가 결과를 모아야 한다면 `System.Collections.Concurrent.ConcurrentDictionary` 같은 스레드 안전 타입을 써야 한다.

**77장에서 만든 PowerShell 클래스는 기본적으로 병렬 실행에 안전하지 않다**: 클래스 메서드 호출이 원래 런스페이스로 마샬링(marshalling)되면서 상태가 손상되거나 교착 상태가 발생할 수 있다 — `[NoRunspaceAffinity()]` 특성 없이 만든 클래스를 `-Parallel` 안에서 쓸 때는 이 제약을 반드시 염두에 둬야 한다.

**이식성**: Bash의 `xargs -P`나 GNU `parallel`이 명령어를 병렬로 실행한다는 점에서 비슷하지만, PowerShell 객체를 그대로 스레드 간에 안전하게 넘기는 스코프 규칙(`$using:`)이나 스레드 안전 컬렉션과의 통합은 지원하지 않는다. `-Parallel`은 파이썬의 `concurrent.futures.ThreadPoolExecutor`에 가장 가까운 대응 개념으로, 스레드 풀을 관리하며 병렬 작업의 동시 실행 수를 조절한다는 설계가 유사하다.

## Reference

- [ForEach-Object (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object)
