---
draft: false
collection_order: 73
slug: measure-command-benchmark-powershell
title: "[PowerShell] 73. Measure-Command — 성능 측정과 벤치마킹"
date: 2026-08-29
lastmod: 2026-08-29
description: "Measure-Command로 스크립트 블록 실행 시간을 TimeSpan으로 측정하는 법과 -Expression이 현재 스코프에서 실행되는 부작용, 결과가 화면에 표시되지 않는 이유, 여러 구현을 비교 벤치마킹하는 법을 정리한 Part 8 마지막 챕터다."
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
- Measure-Command
- Benchmark
- Performance-Test
- TimeSpan
- Out-Default
- Execution-Time
image: "wordcloud.png"
---

## 개요

`Measure-Command`는 스크립트 블록이나 명령의 실행 시간을 측정해 `TimeSpan`(52장) 객체로 반환하는 cmdlet이다. 71장의 Pester가 "정답을 내는가", 72장의 PSScriptAnalyzer가 "관례를 지키는가"를 검사했다면, 이 장은 "충분히 빠른가"라는 세 번째 축을 다루며 Part 8(테스트와 코드 품질)을 마무리한다.

정신 모델은 "`Measure-Command`는 스크립트 블록을 실행하되, 그 결과 자체는 버리고 걸린 시간만 돌려주는 스톱워치"라는 것이다. 42장에서 배열 `+=`의 성능 문제, 43장에서 `ArrayList`/`List<T>`가 그 문제를 해결한다고 말로 설명했던 것을, 이 cmdlet으로 실제 수치를 재서 확인할 수 있다.

## 사용법

```powershell
Measure-Command -Expression { <측정할 코드> }
<입력> | Measure-Command -Expression { <$_ 를 사용하는 코드> }
```

## 종류

| 특성 | 설명 |
|---|---|
| 반환 타입 | `System.TimeSpan`(52장에서 다룬 그 타입) |
| 실행 스코프 | 자식 스코프가 아니라 **현재 스코프**에서 실행됨 — 변수 대입이 바깥에 그대로 남음 |
| 파이프라인 입력 | `-InputObject`로 여러 값을 넘기면 스크립트 블록이 각 값마다 한 번씩 실행됨 |
| 출력 억제 | 스크립트 블록 안의 명령이 만드는 출력은 기본적으로 화면에 표시되지 않음 |

## 예시

```powershell
Measure-Command { Get-ChildItem -Path C:\Windows -Filter "*.txt" -Recurse }
# TotalSeconds 등 여러 단위로 결과를 바로 확인 가능

Measure-Command { Get-ChildItem -Path C:\Windows\*.txt -Recurse } |
    Select-Object TotalSeconds                                          # 13장으로 원하는 속성만

# 42장/43장에서 다룬 배열 vs List<T> 성능 차이를 직접 측정
$arrTime = Measure-Command {
    $arr = @()
    1..5000 | ForEach-Object { $arr += $_ }
}
$listTime = Measure-Command {
    $list = [System.Collections.Generic.List[int]]::new()
    1..5000 | ForEach-Object { $list.Add($_) }
}
"배열: $($arrTime.TotalMilliseconds)ms, List<T>: $($listTime.TotalMilliseconds)ms"

10, 20, 50 | Measure-Command -Expression { for ($i = 0; $i -lt $_; $i++) { $i } }   # 파이프라인 입력마다 측정

# 스크립트 블록 안의 출력을 확인하고 싶다면 Out-Default로 강제 표시
10, 20 | Measure-Command -Expression { for ($i = 0; $i -lt $_; $i++) { $i }; "$_" | Out-Default }

# 스크립트 블록이 현재 스코프를 바꾸는 부작용을 피하려면 호출 연산자로 자식 스코프 강제
$foo = "원래값"
$null = Measure-Command { & { $foo = "바뀐값" } }     # 63장에서 배운 & 호출 연산자로 격리
$foo                                                    # 여전히 "원래값"
```

## 주의사항·함정

**`Measure-Command`는 스크립트 블록의 출력을 화면에 표시하지 않는다**: 코드가 정상 동작하는지 궁금해 `Measure-Command { Get-Process }`를 실행해 보면 프로세스 목록이 아니라 `TimeSpan` 객체만 나와 당황하기 쉽다. 스크립트 블록 안의 출력을 실제로 보고 싶다면 그 안에서 `| Out-Default`로 명시적으로 표시하도록 강제해야 한다.

**스크립트 블록이 자식 스코프가 아니라 현재 스코프에서 실행된다**: 62장에서 다룬 스코프 규칙의 일반적인 기대(함수·스크립트 블록은 새 스코프를 만든다)와 달리, `Measure-Command`의 `-Expression`은 **현재 스코프**에서 그대로 실행된다. 측정하려는 코드가 변수를 변경하면 그 변경이 측정이 끝난 뒤에도 바깥에 그대로 남는다 — 부작용 없이 순수하게 시간만 재고 싶다면 예시처럼 호출 연산자(`&`)로 스크립트 블록을 한 번 더 감싸 자식 스코프를 강제해야 한다.

**한 번의 측정만으로 성능을 단정하면 안 된다**: 디스크 캐시, 다른 프로세스의 CPU 점유, JIT 컴파일 warm-up 등으로 같은 코드도 실행할 때마다 시간이 들쭉날쭉할 수 있다. 신뢰할 만한 벤치마크를 하려면 같은 코드를 여러 번 반복 측정해 평균이나 중앙값을 비교하는 편이 안전하다.

**이식성**: Bash의 `time` 명령어가 개념적으로 가장 가깝지만 셸 프로세스 전체의 실행 시간만 측정할 뿐 코드 블록 단위로 세밀하게 측정하기는 어렵다. CMD에는 대응하는 표준 도구가 없다. `Measure-Command`가 구조화된 `TimeSpan` 객체를 반환한다는 점은 이 컬렉션 전체가 강조해 온 "텍스트가 아니라 객체"라는 원칙이 성능 측정 영역까지 일관되게 적용된 사례다.

## Reference

- [Measure-Command (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/measure-command)
