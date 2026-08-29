---
draft: true
collection_order: 103
slug: constrained-language-mode-execution-policy-powershell
title: "[PowerShell] 103. Constrained Language Mode와 실행 정책 심화"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 언어 모드 4단계의 차이와 AppLocker·WDAC 시스템 잠금 시 자동으로 적용되는 ConstrainedLanguage 모드, 105장 JEA가 NoLanguage 모드를 쓰는 이유를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Security(보안)
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
- Language-Mode
- ConstrainedLanguage
- AppLocker
- WDAC
- System-Lockdown
- Security-Boundary
image: "wordcloud.png"
---

## 개요

<strong>언어 모드(Language Mode)</strong>는 PowerShell 세션에서 어떤 언어 요소를 쓸 수 있는지를 결정하는 세션 속성이다. 05장에서 실행 정책이 "이 스크립트 파일을 실행해도 되는가"를 결정했다면, 언어 모드는 그보다 더 깊은 층위에서 "이 세션 안에서 어떤 .NET 타입·메서드·언어 구문을 쓸 수 있는가"를 결정한다. 102장에서 서명으로 코드의 신뢰성을 증명했다면, 이 장은 그 신뢰가 부족한 상황에서 시스템이 스스로를 어떻게 방어하는지를 다룬다.

정신 모델은 "언어 모드는 네 단계의 동심원이고, 안쪽으로 갈수록 쓸 수 있는 것이 줄어든다"는 것이다 — `FullLanguage`(전부 허용)에서 `ConstrainedLanguage`(허용된 타입만)를 거쳐 `RestrictedLanguage`(변수·연산자 극도로 제한), 마지막 `NoLanguage`(스크립팅 자체가 불가능, 명령 실행만 가능)까지 단계적으로 좁아진다.

## 사용법

```powershell
$ExecutionContext.SessionState.LanguageMode          # 현재 세션의 언어 모드 확인
```

## 종류

| 모드 | 특징 |
|---|---|
| `FullLanguage` | 기본값, 모든 언어 요소 허용 |
| `ConstrainedLanguage` | 모든 cmdlet은 정상 동작하지만, `New-Object`나 타입 변환이 **허용된 타입 목록**으로 제한됨(`[string]`, `[int]`, `[hashtable]` 등은 허용, 임의의 .NET 타입은 차단) |
| `RestrictedLanguage` | `$PSCulture`, `$true`, `$false`, `$null` 등 극소수 변수만 허용, 스크립트 블록·대입문·메서드 호출 불가 |
| `NoLanguage` | 스크립팅 언어 자체가 비활성화, cmdlet과 네이티브 명령만 실행 가능 |

## 예시

```powershell
$ExecutionContext.SessionState.LanguageMode                   # 보통은 FullLanguage

# AppLocker나 WDAC(Windows Defender Application Control) 시스템 잠금 상태에서는
# PowerShell이 자동으로 ConstrainedLanguage로 전환됨 — 사용자가 직접 설정하는 것이 아님
[string]$x = "허용됨"                                            # ConstrainedLanguage에서도 정상 동작
[System.Diagnostics.Process]::Start("notepad")                    # ConstrainedLanguage에서는 차단됨(허용 타입 아님)

New-Object -TypeName PSObject -Property @{ Name = "test" }          # PSCustomObject는 허용된 타입이라 정상 동작

(Get-PSSessionConfiguration -Name "Test").LanguageMode                # 세션 구성에 설정된 언어 모드 확인

# 실험 목적으로만 현재 세션의 언어 모드를 직접 바꿀 수 있음(실제 보안 경계로는 사용 불가)
$ExecutionContext.SessionState.LanguageMode = "ConstrainedLanguage"
```

## 주의사항·함정

**`$ExecutionContext.SessionState.LanguageMode = ...`로 직접 바꾼 언어 모드는 진짜 보안 경계가 아니다**: 이 대입은 실험·학습 목적으로만 유용하며, 공식 문서도 명시하듯 실제 보안 강화를 위해서는 시스템 애플리케이션 제어 정책(AppLocker, WDAC)이나 84–86장에서 배운 세션 구성을 통해 언어 모드를 설정해야 한다. 세션 안에서 스스로 설정을 바꿀 수 있다는 것 자체가, 그 방식이 신뢰 경계로 쓰일 수 없다는 증거다.

**`ConstrainedLanguage`는 세션 전체가 아니라 스크립트 단위로 다르게 적용될 수 있다**: 시스템 잠금 정책이 적용된 세션에서 실행되는 스크립트는 기본적으로 `ConstrainedLanguage`로 동작하지만, 정책이 명시적으로 신뢰한 서명된 스크립트나 모듈은 예외적으로 `FullLanguage`로 실행된다. 같은 세션 안에서도 "이 파일은 신뢰됐는가"에 따라 실제 적용되는 제약이 달라질 수 있다는 점이 처음에는 직관적이지 않다.

**허용된 타입 목록에 없는 타입으로 변환을 시도하면 오류가 나지만, 원인이 즉시 명확하지 않을 수 있다**: `ConstrainedLanguage`에서 임의의 .NET 타입을 쓰려고 하면 오류가 나는데, 오류 메시지만 보고는 "왜 평소엔 되던 코드가 여기선 안 되지?"라고 헷갈리기 쉽다. 오류가 언어 모드 제약 때문인지 의심된다면 `$ExecutionContext.SessionState.LanguageMode`를 먼저 확인하는 습관이 진단을 빠르게 한다.

**`RestrictedLanguage`/`NoLanguage` 세션에서는 `$ExecutionContext...LanguageMode`조차 조회할 수 없다**: 멤버 접근 연산자(`.`) 자체가 이 두 모드에서 제한되므로, 오류 메시지(`PropertyReferenceNotSupportedInDataSection`, `ScriptsNotAllowed` 등)로 간접적으로 현재 모드를 추측해야 한다.

**이식성**: Linux의 `rbash`(제한된 Bash)나 `chroot` 환경이 "실행 가능한 것을 좁힌다"는 목적은 공유하지만, PowerShell의 언어 모드처럼 .NET 타입 시스템 수준까지 세밀하게 통제하는 계층화된 모델은 아니다. 105장에서 다룰 JEA(Just Enough Administration)가 `NoLanguage` 모드를 세션 구성의 기반으로 사용해, 사용자가 정의된 명령 집합만 실행할 수 있도록 강제하는 것이 이 언어 모드 개념의 대표적인 실전 활용 사례다.

## Reference

- [about_Language_Modes - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes)
