---
draft: false
collection_order: 25
slug: common-parameters-verbose-debug-erroraction-powershell
title: "[PowerShell] 25. 공통 매개변수 — -Verbose/-Debug/-ErrorAction/-OutVariable"
date: 2026-08-29
lastmod: 2026-08-29
description: "모든 cmdlet에 자동으로 제공되는 PowerShell 공통 매개변수(-Verbose, -Debug, -ErrorAction, -ErrorVariable, -OutVariable 등)의 목록과 ActionPreference 값, 선호 변수와의 관계를 정리한 챕터다."
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
- Common-Parameters
- Preference-Variable
- Verbose
- ErrorAction
- Logging
- Try-Catch
- Cmdlet-Binding
image: "wordcloud.png"
---

## 개요

<strong>공통 매개변수(common parameters)</strong>는 PowerShell 엔진이 모든 cmdlet과 고급 함수에 자동으로 추가하는 매개변수 집합이다. cmdlet 개발자가 따로 구현하지 않아도 `-Verbose`, `-ErrorAction` 같은 매개변수를 어떤 cmdlet에서나 쓸 수 있는 이유가 여기에 있다. 다만 cmdlet이 해당 스트림에 실제로 메시지를 보내지 않으면 효과가 없다 — `Write-Verbose`를 호출하지 않는 cmdlet에 `-Verbose`를 붙여도 아무 일도 일어나지 않는다.

이 공통 매개변수들은 대부분 `$VerbosePreference`, `$ErrorActionPreference` 같은 선호 변수(preference variable)의 세션 전역 기본값을 그 명령 하나에 한해서만 재정의하는 역할을 한다. 선호 변수를 바꾸면 이후 실행되는 모든 명령에 영향을 주지만, 공통 매개변수는 그 자리의 명령 한 번에만 적용되고 세션 전체 설정은 그대로 남는다는 점이 중요한 차이다. 이 구분 덕분에 스크립트 안에서 특정 명령 하나만 조용히 실행하거나(`-ErrorAction SilentlyContinue`), 특정 명령의 진행 상황만 자세히 보고 싶을 때(`-Verbose`) 세션 전체 설정을 건드리지 않고 그 자리에서만 동작을 바꿀 수 있다.

## 목록

| 매개변수(별칭) | 역할 |
|---|---|
| `-Verbose`(`vb`) | 상세 진행 메시지 표시(`Write-Verbose` 출력을 켠다) |
| `-Debug`(`db`) | 프로그래머 수준의 디버그 메시지 표시(`Write-Debug` 출력을 켠다) |
| `-ErrorAction`(`ea`) | 비종료 오류 발생 시 동작(`Stop`, `Continue`, `SilentlyContinue`, `Ignore`, `Inquire` 등) |
| `-ErrorVariable`(`ev`) | 오류 레코드를 지정한 변수에도 저장(`+`를 앞에 붙이면 누적) |
| `-WarningAction`(`wa`) / `-WarningVariable`(`wv`) | 경고 메시지 처리 방식과 저장 |
| `-InformationAction`(`infa`) / `-InformationVariable`(`iv`) | 정보 스트림(`Write-Information`, `Write-Host`가 내부적으로 사용) 처리 |
| `-OutVariable`(`ov`) | 성공 스트림 출력을 파이프라인과 별개로 변수에도 저장 |
| `-OutBuffer`(`ob`) | 다음 cmdlet으로 넘기기 전 버퍼링할 객체 개수 |
| `-PipelineVariable`(`pv`) | 파이프라인의 현재 세그먼트가 다음 세그먼트로 넘긴 마지막 값을 다른 명령에서도 참조 |
| `-WhatIf`(`wi`) / `-Confirm`(`cf`) | 위험 완화 매개변수(26장에서 별도로 다룬다) |

`-ErrorAction`/`-WarningAction`/`-InformationAction`이 받는 값은 모두 `ActionPreference` 열거형(`Break`, `Suspend`, `Ignore`, `Inquire`, `Continue`, `Stop`, `SilentlyContinue`)을 공유한다.

## 예시

```powershell
Get-Process -Verbose                                   # (Write-Verbose를 쓰는 cmdlet에서만 효과)
Remove-Item missing.txt -ErrorAction SilentlyContinue   # 오류를 화면에 안 띄우되 $Error에는 기록
Remove-Item missing.txt -ErrorAction Ignore             # 화면에도 안 띄우고 $Error에도 기록 안 함
Get-Process -Id 6 -ErrorVariable myErr                  # 오류를 $myErr에 저장
Get-Process -Id 2 -ErrorVariable +myErr                 # 기존 $myErr에 누적
Get-Process powershell -OutVariable out                 # 결과를 파이프라인과 $out 둘 다에 저장
Remove-Item tmp*.txt -ErrorAction Stop -ErrorVariable errs -OutVariable removed
```

## 주의사항·함정

**`-ErrorAction Stop`은 비종료 오류를 종료 오류로 격상시킨다**: 원래 `Continue`(기본값)면 오류 메시지를 띄우고 계속 진행하지만, `-ErrorAction Stop`을 주면 그 비종료 오류가 `ActionPreferenceStopException`으로 바뀌어 `try`/`catch`로 잡을 수 있게 된다. 특정 명령의 실패만 확실히 잡아내고 싶을 때 이 조합을 자주 쓴다.

**`-ErrorAction`은 함수·스크립트 안의 개별 명령까지 강제하지 못한다**: 스크립트나 함수를 실행하며 `-ErrorAction`을 지정하면 `$ErrorActionPreference` 값을 재정의하긴 하지만, 그 값을 대체하는 것이지 함수 내부의 모든 명령에 무조건 전파되는 것은 아니다. 함수 내부에서 이미 `-ErrorAction`을 다른 값으로 명시한 명령에는 영향을 주지 않는다.

**`-OutBuffer`는 고급 사용자용이다**: 파이프라인 사이의 배치 크기를 조정하는 매개변수로, 일반적인 스크립팅에서는 거의 쓸 일이 없다. 잘못 설정하면 예상과 다른 시점에 출력이 나타나는 것처럼 보일 수 있다.

**이식성**: Bash에는 모든 명령에 공통으로 적용되는 매개변수 개념이 없다 — 각 명령이 `-v`(verbose) 같은 옵션을 지원하는지는 그 명령을 만든 사람 마음이다. PowerShell은 이 지원 여부를 cmdlet 개발자의 선택에서 언어 차원의 보장으로 끌어올렸다는 점이 다르다.

## Reference

- [about_CommonParameters - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters)
