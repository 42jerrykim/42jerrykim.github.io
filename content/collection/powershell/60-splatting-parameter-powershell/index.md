---
draft: false
collection_order: 60
slug: splatting-parameter-powershell
title: "[PowerShell] 60. 매개변수 스플래팅(Splatting)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 스플래팅(@ 기호로 해시테이블·배열을 매개변수 묶음으로 넘기는 문법)과 $PSBoundParameters로 함수 인자를 다른 함수에 그대로 전달하는 법, PowerShell 7.1의 명시적 매개변수 우선순위를 정리한 챕터다."
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
- Splatting
- PSBoundParameters
- Hashtable
- Proxy-Function
- Argument-Forwarding
- Named-Parameter
image: "wordcloud.png"
---

## 개요

**스플래팅**은 44장에서 배운 해시테이블(또는 배열)을 명령 하나에 매개변수 묶음으로 통째로 넘기는 기법이다. `$` 대신 `@` 기호를 앞에 붙이는 것만으로, 해시테이블의 각 키-값 쌍이 `-키 값` 형태의 개별 매개변수로 자동 展開된다. 25장의 공통 매개변수 예제, 50장의 `ConvertTo-Html` 예제에서 이미 스플래팅을 스치듯 사용했는데, 이 장은 그 문법을 독립적으로 정리한다.

정신 모델은 "`@`는 '내가 든 이 컬렉션을 여러 개의 매개변수로 풀어서 전달하라'는 지시"라는 것이다. 매개변수가 5개, 10개로 늘어나는 긴 명령을 한 줄에 욱여넣는 대신, 값을 미리 변수에 정리해 두고 명령 자체는 짧게 유지할 수 있다.

## 사용법

```powershell
$파라미터 = @{ 이름1 = 값1; 이름2 = 값2 }    # 해시테이블 스플래팅(명명된 매개변수)
명령어 @파라미터

$파라미터 = 값1, 값2                          # 배열 스플래팅(위치 매개변수)
명령어 @파라미터
```

## 종류

| 형태 | 대응하는 매개변수 | 용도 |
|---|---|---|
| 해시테이블 스플래팅 | 명명된 매개변수, `[switch]` 포함 | 대부분의 상황에서 기본 선택 |
| 배열 스플래팅 | 위치 매개변수 | 순서만으로 전달되는 값이 많을 때, 네이티브 명령 인자 전달에도 사용 |
| `$PSBoundParameters` | 현재 함수가 받은 매개변수 전체 | 함수 A가 받은 인자를 그대로 함수 B에 전달(프록시 함수) |
| `@args` | 선언되지 않은 나머지 인자(57장) | 매개변수를 그대로 다른 cmdlet에 위임하는 래퍼 함수 |

## 예시

```powershell
$HashArguments = @{
    Path        = "test.txt"
    Destination = "test2.txt"
    WhatIf      = $true
}
Copy-Item @HashArguments                    # Copy-Item -Path test.txt -Destination test2.txt -WhatIf와 동일

$Colors = @{ ForegroundColor = "Black"; BackgroundColor = "White" }
Write-Host "메시지 1" @Colors                 # 여러 명령에서 같은 설정 재사용
Write-Host @Colors "메시지 2"                  # 스플래팅 위치는 상관없음

$ArrayArguments = "test.txt", "test2.txt"
Copy-Item @ArrayArguments -WhatIf            # 위치 매개변수로 전달

function Test1 { param($a, $b, $c); "a=$a b=$b c=$c" }
function Test2 {
    param($a, $b, $c)
    Test1 @PSBoundParameters                   # 받은 매개변수를 그대로 다음 함수에 전달
}
Test2 -a 1 -b 2 -c 3

# PowerShell 7.1+: 스플래팅된 값을 명시적 매개변수로 덮어쓰기
$commonParams = @{ ResourceGroupName = "myRG"; Location = "East US" }
New-AzVm @commonParams -Name "myVM2" -Location "West US"   # Location만 West US로 재정의
```

## 주의사항·함정

**해시테이블 스플래팅의 키 이름은 대상 명령의 매개변수 이름과 정확히 일치해야 한다**: 오타나 대소문자 실수가 있으면 그 키는 조용히 무시되지 않고 "해당 매개변수가 없다"는 오류로 이어질 수 있다. 특히 여러 명령에 재사용할 목적으로 만든 스플래팅 해시테이블은, 그 해시테이블을 넘기는 명령이 바뀔 때마다 매개변수 이름이 실제로 일치하는지 다시 확인해야 한다.

**`[switch]` 매개변수를 스플래팅할 때는 반드시 불리언 값을 명시해야 한다**: 일반 명령줄에서는 `-WhatIf`만 쓰면 되지만, 해시테이블 스플래팅에서는 `WhatIf = $true`처럼 명시적인 값이 필요하다. `WhatIf = "yes"`처럼 불리언이 아닌 값을 넣으면 원치 않는 방식으로 변환될 수 있다.

**PowerShell 7.0 이전에는 스플래팅된 값을 같은 명령의 명시적 매개변수로 덮어쓸 수 없었다**: 7.1부터 도입된 이 우선순위 규칙(예시의 `-Location "West US"`가 `$commonParams`의 `Location`을 이긴다)에 의존하는 스크립트를 Windows PowerShell 5.1 환경에도 배포해야 한다면, 매번 새 해시테이블을 만들거나 값을 직접 덮어써야 한다 — 이 저장소가 반복해서 강조하는 Windows PowerShell/PowerShell 7 버전 차이의 또 다른 사례다.

**이식성**: Bash의 배열을 `"${args[@]}"`로 展開해 명령에 넘기는 관용구가 배열 스플래팅과 개념적으로 비슷하지만, 명명된 매개변수를 키-값 쌍으로 통째로 넘기는 해시테이블 스플래팅에 직접 대응하는 문법은 없다. CMD에는 이런 매개변수 묶음 전달 개념 자체가 없어, 긴 명령줄을 변수 하나로 압축할 방법이 마땅치 않다.

## Reference

- [about_Splatting - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_splatting)
