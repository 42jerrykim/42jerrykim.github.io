---
draft: false
collection_order: 15
slug: foreach-object-command-pipeline-loop-powershell
title: "[PowerShell] 15. ForEach-Object — 파이프라인 반복 처리"
date: 2026-08-29
lastmod: 2026-08-29
description: "ForEach-Object(별칭 %)로 파이프라인의 각 객체에 동작을 수행하는 법, -Begin/-Process/-End 블록, 간소화 구문, PowerShell 7의 -Parallel 병렬 처리와 스레드 안전성 주의점을 정리한 챕터다."
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
- Concurrency(동시성)
- ForEach-Object
- Loop
- Parallel-Processing
- Thread-Safety
- Runspace
- Multithreading(멀티스레딩)
image: "wordcloud.png"
---

## 개요

`ForEach-Object`(별칭 `%`, `foreach`)는 파이프라인을 지나는 각 객체에 대해 지정한 동작을 실행하는 cmdlet이다. 언어 내장 `foreach` 문(56장)과 이름이 비슷해 혼동하기 쉽지만, `foreach` 문은 이미 메모리에 있는 컬렉션을 순회하는 반면 `ForEach-Object`는 **파이프라인의 일부**로 동작해 앞 단계에서 오는 객체를 받는 즉시 하나씩 처리한다.

정신 모델은 "파이프라인 위에서 각 객체마다 실행되는 작은 스크립트"다. 이 스크립트는 객체 전체를 다 받은 뒤 실행되는 것이 아니라, 객체가 도착하는 즉시 실행되므로 대용량 데이터를 다룰 때도 전체를 메모리에 쌓아 둘 필요가 없다.

## 사용법

```powershell
# 스크립트블록 구문
Get-Process | ForEach-Object -Process { $_.ProcessName }

# 간소화 구문 — 속성·메서드 이름만 지정
Get-Process | ForEach-Object ProcessName

# Begin/Process/End
Get-EventLog -LogName System -Newest 1000 |
    ForEach-Object -Begin { Get-Date } -Process { Out-File -Path Events.txt -Append -InputObject $_.Message } -End { Get-Date }

# 병렬 처리(PowerShell 7+)
1..8 | ForEach-Object -Parallel { "$using:Message $_"; Start-Sleep 1 } -ThrottleLimit 4
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Process` | 각 파이프라인 객체마다 실행할 스크립트블록(위치 매개변수라 이름 생략 가능) |
| `-Begin` / `-End` | 파이프라인 전체에서 딱 한 번씩만 실행되는 시작/종료 블록 |
| `-MemberName` | 간소화 구문에서 조회할 속성·메서드 이름(선택적 매개변수 이름) |
| `-ArgumentList` | 간소화 구문으로 메서드를 호출할 때 넘길 인자 |
| `-Parallel` | PowerShell 7+에서 각 반복을 별도 런스페이스에서 동시에 실행할 스크립트블록 |
| `-ThrottleLimit` | 동시에 실행할 병렬 스크립트블록 개수(기본 5) |
| `-AsJob` | 병렬 실행을 즉시 대기하지 않고 Job 객체로 반환한다(78장에서 Job을 본격적으로 다룬다) |
| `-TimeoutSeconds` | 병렬 처리 전체에 대한 제한 시간 |

## 예시

```powershell
30000, 56798, 12432 | ForEach-Object { $_ / 1024 }
Get-Module -ListAvailable | ForEach-Object -MemberName Path         # 속성값만 뽑기
"Microsoft.PowerShell.Core", "Microsoft.PowerShell.Host" | ForEach-Object { $_.Split(".") }
Get-ItemProperty -Path HKCU:\Network\* | ForEach-Object { Set-ItemProperty -Path $_.PSPath -Name RemotePath -Value $_.RemotePath.ToUpper() }
1..2 | ForEach-Object { 'begin' } { 'process' }                      # 스크립트블록 2개 → Begin/Process로 매핑

# 스레드 안전 컬렉션으로 병렬 결과 모으기
$dict = [System.Collections.Concurrent.ConcurrentDictionary[string,object]]::new()
Get-Process | ForEach-Object -Parallel {
    ($using:dict).TryAdd($_.ProcessName, $_)
}
```

## 주의사항·함정

**`-Begin`/`-Process`/`-End`가 자동으로 매핑되는 규칙을 알아야 한다**: 스크립트블록을 여러 개 위치 인자로 넘기면, 첫 번째는 `Begin`, 마지막은 `End`, 중간 것들은 모두 `Process`로 매핑된다. 정확히 지정하려면 매개변수 이름을 명시해야 한다.

**`-Parallel`은 새 런스페이스에서 실행되므로 바깥 변수를 그냥 못 읽는다**: 병렬 스크립트블록 안에서 호출자 스코프의 변수를 참조하려면 `$using:변수명` 스코프 한정자가 필요하다. 이 제약은 원격 세션(11부)의 `Invoke-Command` 스크립트블록과 같은 이유에서 비롯된다.

**병렬 처리에서 스레드 안전하지 않은 객체를 공유하면 안 된다**: 여러 병렬 스크립트블록이 동시에 같은 객체를 수정하면 `System.Collections.Generic.Dictionary` 같은 일반 컬렉션은 손상될 수 있다. `System.Collections.Concurrent` 네임스페이스의 스레드 안전 컬렉션을 대신 써야 한다.

**`-Parallel`이 항상 더 빠른 것은 아니다**: 새 런스페이스를 만드는 오버헤드가 스크립트블록이 실제로 하는 일보다 크면, 병렬 처리가 오히려 순차 처리보다 느려질 수 있다. CPU 집약적 계산이나 I/O 대기가 긴 작업에서만 이득이 크다.

**이식성**: Bash의 `xargs`나 `while read`가 표준 입력 줄을 하나씩 처리하는 것과 비슷하지만, `ForEach-Object`는 텍스트가 아닌 객체를 받으므로 각 줄을 다시 파싱할 필요가 없다. `-Parallel`에 직접 대응하는 셸 기능은 없으며, 굳이 비교하면 `xargs -P`가 프로세스 단위 병렬화를 제공하는 정도다.

## Reference

- [ForEach-Object (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object)
