---
draft: false
collection_order: 95
slug: get-counter-performance-powershell
title: "[PowerShell] 95. Get-Counter — 성능 카운터 조회"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Counter로 Windows 성능 모니터링 카운터를 조회하는 법과 -Counter 경로 문법, -SampleInterval/-Continuous/-MaxSamples로 시계열 샘플을 수집하는 법, CounterSamples 속성으로 실제 수치에 접근하는 법을 정리한 Part 12 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- System-Management
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
- Get-Counter
- Performance-Counter
- SampleInterval
- Continuous
- CounterSamples
- System-Monitoring
image: "wordcloud.png"
---

## 개요

`Get-Counter`는 Windows 성능 모니터링 인프라(성능 모니터, `perfmon`이 쓰는 것과 같은 데이터 소스)에서 CPU·메모리·디스크 같은 실시간 성능 카운터 값을 가져오는 cmdlet이다. 73장의 `Measure-Command`가 "이 코드 한 조각이 얼마나 걸리는가"를 측정했다면, 이 장은 "지금 이 순간 시스템 전체가 얼마나 바쁜가"를 측정하며 Part 12(프로세스·서비스·예약 작업)를 마무리한다.

정신 모델은 "성능 카운터는 `\카운터집합(인스턴스)\카운터이름`이라는 경로로 식별되는, 계속 갱신되는 게이지(gauge)"라는 것이다. `Get-Counter`는 이 경로를 지정된 시각에 한 번(또는 반복적으로) 읽어 스냅샷을 만든다.

## 사용법

```powershell
Get-Counter -Counter "<카운터경로>" [-SampleInterval <초>] [-MaxSamples <개수>] [-Continuous]
Get-Counter -ListSet <카운터집합이름>
```

## 종류

| 매개변수 | 설명 |
|---|---|
| `-Counter` | `\카운터집합(인스턴스)\카운터이름` 형식의 경로(인스턴스에 `*` 와일드카드 가능) |
| `-ListSet` | 사용 가능한 카운터 집합과 그 안의 전체 경로 목록 조회 |
| `-SampleInterval` | 샘플 사이 대기 시간(초 단위, 기본 1초) |
| `-MaxSamples` | 수집할 샘플 개수(기본은 1회만) |
| `-Continuous` | Ctrl+C로 멈출 때까지 계속 수집 |
| `-ComputerName` | 원격 컴퓨터의 카운터 조회(WinRM 없이도 동작, 83장에서 다룬 것과는 다른 별도 메커니즘) |
| `CounterSamples` 속성 | 실제 수치가 담긴 배열, 각 샘플의 `.CookedValue`가 사람이 읽는 계산된 값 |

## 예시

```powershell
Get-Counter -ListSet *                                            # 사용 가능한 카운터 집합 목록

Get-Counter -Counter "\Processor(_Total)\% Processor Time"           # 1회 샘플
Get-Counter -Counter "\Processor(_Total)\% Processor Time" -SampleInterval 2 -MaxSamples 3   # 2초 간격 3회
Get-Counter -Counter "\Processor(_Total)\% Processor Time" -Continuous    # Ctrl+C까지 계속(1초 간격)

(Get-Counter -ListSet Memory).Paths | Where-Object { $_ -like "*Cache*" }   # 46장 응용으로 경로 검색

$Counter = Get-Counter -Counter "\Processor(*)\% Processor Time"       # 모든 코어
$Counter.CounterSamples | Where-Object CookedValue -lt 20                 # 12장 Where-Object로 값 비교
$Counter.CounterSamples | Sort-Object CookedValue -Descending             # 19장 Sort-Object로 정렬

# 78장에서 배운 백그라운드 작업으로 장시간 수집
Start-Job -ScriptBlock {
    Get-Counter -Counter "\LogicalDisk(_Total)\% Free Space" -MaxSamples 1000
}

$DiskReads = "\LogicalDisk(C:)\Disk Reads/sec"
$DiskReads | Get-Counter -ComputerName Server01, Server02 -MaxSamples 10   # 여러 컴퓨터 동시 조회
```

## 주의사항·함정

**카운터 경로에서 원하는 값에 접근하려면 `CounterSamples` 속성을 한 단계 더 거쳐야 한다**: `Get-Counter`의 반환값 자체는 타임스탬프와 표시용 요약을 담은 `PerformanceCounterSampleSet` 객체라, 실제 숫자(`.CookedValue`)에 접근하려면 `.CounterSamples`로 한 번 더 들어가야 한다. 이 구조를 모르면 `Where-Object`로 값을 비교하려 할 때 속성을 찾지 못해 당황하기 쉽다.

**성능 카운터 이름은 시스템 로캘에 따라 달라진다**: 영어 Windows에서 동작하던 `\Processor(_Total)\% Processor Time` 경로가, 다른 언어로 설치된 Windows에서는 그대로 동작하지 않을 수 있다. 여러 언어 환경에 배포할 스크립트라면 `Get-Counter -ListSet` 결과에서 그 시스템의 실제 로캘화된 이름을 먼저 확인해야 한다.

**접근 권한이 없는 카운터 집합은 관리자 권한 없이 조회되지 않는다**: 일부 카운터 집합은 접근 제어 목록(ACL)으로 보호돼 있어, 일반 사용자 권한으로는 전체 카운터 집합 목록이 다 보이지 않을 수 있다. 전체 목록이 필요하면 관리자 권한으로 다시 실행해야 한다.

**`-Continuous`나 큰 `-MaxSamples`는 콘솔을 오래 점유한다**: 장시간 샘플링이 필요한 모니터링 작업이라면, 콘솔이 막히지 않도록 78장에서 배운 `Start-Job`으로 백그라운드에서 실행하고 나중에 `Receive-Job`으로 결과를 모으는 편이 실용적이다.

**이식성**: Linux의 `sar`, `vmstat`, `iostat` 같은 도구들이 성능 카운터 조회라는 목적은 공유하지만, 각각 CPU·메모리·디스크별로 별도 명령이 나뉘어 있다. `Get-Counter`는 하나의 cmdlet으로 모든 카운터 집합을 통일된 경로 문법과 객체 구조로 다룬다는 점에서, 89–94장에서 계속 확인해 온 "여러 시스템 영역을 일관된 인터페이스로 다룬다"는 PowerShell의 설계 철학을 성능 모니터링 영역까지 확장한 사례다.

## Reference

- [Get-Counter (Microsoft.PowerShell.Diagnostics) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-counter)
