---
draft: true
collection_order: 5
slug: execution-policy-command-powershell-security
title: "[PowerShell] 05. 실행 정책 — Get/Set-ExecutionPolicy"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 실행 정책(Restricted/AllSigned/RemoteSigned 등)의 스코프별 우선순위, Get-ExecutionPolicy·Set-ExecutionPolicy 사용법, Unblock-File로 서명 없는 스크립트를 안전하게 실행하는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Security(보안)
- Automation(자동화)
- Guide(가이드)
- Education(교육)
- Beginner
- Configuration(설정)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- DevOps
- Permission
- Execution-Policy
- Get-ExecutionPolicy
- Set-ExecutionPolicy
- Code-Signing
- Group-Policy
image: "wordcloud.png"
---

## 개요

<strong>실행 정책(Execution Policy)</strong>은 PowerShell이 프로파일 스크립트를 불러오거나 `.ps1` 스크립트를 실행할지, 실행한다면 디지털 서명을 요구할지를 결정하는 보안 장치다. CMD·Bash에는 이런 개념 자체가 없다 — 아무 배치 파일·셸 스크립트나 그냥 실행된다. PowerShell이 실행 정책을 둔 이유는, 사용자가 인터넷에서 내려받은 스크립트를 무심코 더블클릭해 실행하는 사고를 구조적으로 줄이기 위해서다.

정신 모델에서 가장 중요한 점은 "실행 정책은 악의적 스크립트를 막는 보안 경계가 아니라, 부주의한 실행을 막는 안전장치"라는 것이다. 관리자 권한만 있으면 누구나 `Set-ExecutionPolicy`로 정책을 바꿀 수 있고, `-Command`나 `-EncodedCommand`로 스크립트 내용을 직접 넘기면 실행 정책이 아예 적용되지 않는다. 그래서 Microsoft도 이를 "보안 경계가 아니라 도우미"라고 명시한다. 실행 정책은 어디까지나 콘솔에서 `.ps1` 파일을 직접 실행하려는 시도를 가로채 "이 스크립트가 신뢰할 수 있는 출처에서 왔는가"를 한 번 더 묻는 절차이지, 스크립트 안에 들어 있는 코드 자체를 분석하거나 악성 여부를 판단하는 장치가 아니다.

이 관점에서 보면 정책 값 하나하나는 "어떤 상황을 얼마나 신뢰할 것인가"를 나타내는 단계로 이해하는 것이 더 정확하다. `Restricted`는 아무것도 신뢰하지 않는 기본값이고, `RemoteSigned`는 로컬에서 직접 작성한 스크립트는 신뢰하되 인터넷에서 내려받은 것만 서명을 요구하는 절충안이며, `Unrestricted`·`Bypass`로 갈수록 신뢰의 범위가 넓어진다.

## 사용법

```powershell
Get-ExecutionPolicy [-List] [[-Scope] <ExecutionPolicyScope>]
Set-ExecutionPolicy [-ExecutionPolicy] <ExecutionPolicy> [[-Scope] <ExecutionPolicyScope>] [-Force]
```

`Get-ExecutionPolicy`를 매개변수 없이 실행하면 현재 세션에 적용되는 **유효 정책** 하나만 보여주고, `-List`를 쓰면 스코프별 정책을 우선순위 순서로 모두 보여준다.

## 매개변수

| 값/매개변수 | 설명 |
|---|---|
| `Restricted` | 스크립트 실행·구성 파일 로드를 전혀 허용하지 않는다(Windows 클라이언트 기본값) |
| `AllSigned` | 로컬에서 작성한 스크립트를 포함해 모든 스크립트가 신뢰할 수 있는 게시자 서명을 요구한다 |
| `RemoteSigned` | 인터넷에서 내려받은 스크립트만 서명을 요구한다(Windows Server 기본값) |
| `Unrestricted` | 모든 스크립트 실행을 허용하되, 인터넷에서 내려받은 서명 없는 스크립트는 실행 전 확인을 묻는다 |
| `Bypass` | 아무것도 차단하지 않고 경고도 표시하지 않는다 |
| `Undefined` | 해당 스코프에 정책을 설정하지 않는다(모든 스코프가 Undefined면 유효 정책은 Restricted) |
| `-Scope` | `MachinePolicy` > `UserPolicy` > `Process` > `LocalMachine` > `CurrentUser` 순으로 우선순위가 높다. `Process` 스코프는 `$Env:PSExecutionPolicyPreference`에 저장되며 세션 종료 시 사라진다 |

## 예시

```powershell
Get-ExecutionPolicy                                       # 현재 세션의 유효 정책
Get-ExecutionPolicy -List                                 # 스코프별 정책 전체
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine   # 관리자 권한 필요
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process              # 현재 세션에서만 임시로 완화
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser       # 사용자 스코프 정책 제거
Unblock-File -Path .\Start-ActivityTracker.ps1             # 인터넷에서 받은 스크립트의 차단 표시(Zone.Identifier) 해제
Invoke-Command -ComputerName Server01 -ScriptBlock { Get-ExecutionPolicy } | Set-ExecutionPolicy   # 원격 정책을 로컬에 그대로 적용
```

## 주의사항·함정

**Restricted 정책은 프로파일 스크립트도 막는다**: 06장에서 다룰 `$PROFILE` 스크립트조차 `Restricted` 정책에서는 실행되지 않는다. 콘솔을 열 때 프로파일 커스터마이징이 전혀 반영되지 않는다면 가장 먼저 `Get-ExecutionPolicy`부터 확인해야 한다.

**Group Policy가 걸려 있으면 로컬 설정이 무시된다**: `MachinePolicy`·`UserPolicy` 스코프에 Group Policy로 값이 설정돼 있으면, `Set-ExecutionPolicy`로 `LocalMachine`·`CurrentUser`를 아무리 바꿔도 실제 유효 정책은 바뀌지 않는다. PowerShell은 이 경우 정책을 저장은 하되 "Group Policy가 이를 재정의했다"는 메시지를 보여준다.

**서명되지 않은 신뢰 가능한 스크립트를 실행하는 올바른 방법**: 직접 검토한 스크립트를 서명 없이 실행하고 싶다고 해서 정책 자체를 `Unrestricted`나 `Bypass`로 낮추기보다, `RemoteSigned`를 유지한 채 해당 파일만 `Unblock-File`로 인터넷 차단 표시(NTFS 대체 데이터 스트림의 Zone.Identifier)를 제거하는 편이 더 안전하다. 이 방식은 실행 정책 자체는 그대로 두고 파일 하나의 신뢰 상태만 바꾼다.

**비-Windows 플랫폼**: PowerShell 6부터 Linux·macOS의 기본 정책은 `Unrestricted`로 고정되어 변경할 수 없다. `Set-ExecutionPolicy`를 실행할 수는 있지만 콘솔에 지원되지 않는다는 메시지만 출력된다.

**이식성**: CMD·Bash에는 실행 정책과 정확히 대응하는 개념이 없다. 굳이 비교하면 Unix 계열의 실행 비트(`chmod +x`)가 "이 파일을 실행 가능하게 표시하는가"를 다루지만, 그건 파일 하나의 권한 문제이지 PowerShell 실행 정책처럼 "서명 여부"나 "다운로드 출처"를 기준으로 판단하지 않는다.

## Reference

- [Set-ExecutionPolicy (Microsoft.PowerShell.Security) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)
- [Get-ExecutionPolicy (Microsoft.PowerShell.Security) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-executionpolicy)
