---
draft: false
collection_order: 105
slug: just-enough-administration-jea-overview-powershell
title: "[PowerShell] 105. Just Enough Administration(JEA) 개요"
date: 2026-08-29
lastmod: 2026-08-29
description: "JEA가 최소 권한 원칙으로 관리자 권한을 위임하는 방식과 역할 기능(Role Capability)·세션 구성(Session Configuration)의 관계, 103장 NoLanguage 모드가 JEA 세션을 어떻게 뒷받침하는지 정리한 Part 14 마지막 챕터다."
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
- JEA
- Just-Enough-Administration
- Least-Privilege
- Role-Capability
- Session-Configuration
- Privileged-Access
image: "wordcloud.png"
---

## 개요

<strong>Just Enough Administration(JEA)</strong>은 PowerShell로 관리되는 모든 것에 <strong>최소 권한 원칙(Principle of Least Privilege)</strong>을 적용하는 보안 기술이다. 83–88장에서 배운 PowerShell Remoting이 "누구나 원격으로 전체 관리자 권한을 행사할 수 있게" 만드는 기반이었다면, JEA는 그 원격 접근을 "이 사람은 딱 이 명령들만 실행할 수 있다"는 좁은 창구로 제한한다. Part 14(보안과 자격 증명)의 마지막 챕터로서, 지금까지 다룬 자격 증명(100장)·권한(101장)·서명(102장)·언어 모드(103장)·비밀 관리(104장)가 결합돼 만들어내는 실전 보안 아키텍처가 바로 JEA다.

정신 모델은 "일반 원격 세션이 건물 전체 마스터키를 내주는 것이라면, JEA 세션은 딱 필요한 방 몇 개만 열리는 카드키를 내주는 것"이라는 것이다. DNS 관리자가 도메인 관리자 그룹에 속하지 않고도 DNS 서비스만 재시작할 수 있게 하는 것이 대표적인 예다.

## 사용법

```powershell
# JEA는 별도의 새 cmdlet을 배우는 것이 아니라, 84–86장의 세션 진입점에 제약을 거는 구성이다
Enter-PSSession -ComputerName <컴퓨터> -ConfigurationName <JEA엔드포인트이름>
```

## 종류

| 구성 요소 | 역할 |
|---|---|
| 역할 기능(Role Capability) 파일(`.psrc`) | 특정 역할이 실행할 수 있는 cmdlet·함수·외부 명령 목록 정의 |
| 세션 구성(Session Configuration) 파일(`.pssc`) | 어떤 사용자가 어떤 역할 기능을 갖는지 매핑, 103장의 언어 모드(`NoLanguage`)를 지정 |
| 가상 계정(Virtual Account) / 그룹 관리형 서비스 계정 | JEA 세션 안에서만 임시로 관리자 권한을 부여, 세션 종료 시 소멸 |
| 트랜스크립트·로그 | 69장에서 배운 `Start-Transcript`처럼 JEA 세션 안의 모든 명령을 자동 기록 |

## 예시

```powershell
# 관리자가 사전에 정의한 JEA 엔드포인트에 일반 사용자 권한으로 접속
Enter-PSSession -ComputerName DnsServer01 -ConfigurationName "DnsAdminEndpoint"
[DnsServer01]: PS> Restart-Service -Name DNS          # 역할 기능에 정의된 명령만 실행 가능
[DnsServer01]: PS> Get-Process                          # 역할 기능에 없다면 오류 — 도메인 전체 관리자 권한 없음

# (관리자 측) 세션 구성을 등록해 JEA 엔드포인트를 만드는 개념적 흐름
# Register-PSSessionConfiguration -Name "DnsAdminEndpoint" -Path .\DnsAdmin.pssc

Get-PSSessionConfiguration -Name "DnsAdminEndpoint" | Select-Object Name, RunAsUser   # 구성 확인
```

## 주의사항·함정

**JEA는 별도의 새 명령어 세트가 아니라 84–86장에서 배운 세션 진입점에 거는 제약이다**: `Enter-PSSession`/`Invoke-Command` 자체의 문법은 그대로이고, `-ConfigurationName`으로 어떤 세션 구성(JEA 엔드포인트)에 연결할지만 달라진다. "JEA를 쓴다"는 것은 새 도구를 배우는 것이 아니라, 이미 아는 도구를 제한된 문으로 통과시키는 것에 가깝다.

**JEA 세션은 파일 시스템이나 다른 시스템 리소스에 직접 접근할 수 없다**: 103장에서 다룬 `NoLanguage` 모드를 기반으로 하기 때문에, 사용자는 역할 기능에 명시적으로 나열된 명령만 실행할 수 있고 임의의 API·스크립트 블록·파일 시스템 탐색은 차단된다. 이 제약을 모르고 JEA 세션 안에서 평소처럼 자유롭게 스크립트를 작성하려 하면 대부분 막힌다 — 이것이 JEA의 버그가 아니라 설계 목적이다.

**가상 계정을 쓰면 사용자는 비관리자 자격 증명으로 접속해도 세션 안에서는 관리자 권한 명령이 동작한다**: 이 특성이 JEA의 핵심 가치다 — DNS 관리자가 굳이 도메인 관리자 그룹에 속하지 않아도, JEA 세션 안에서만 임시로 상승된 권한으로 DNS 서비스를 재시작할 수 있다. 권한 상승이 세션 종료와 함께 사라지므로, 그 계정이 탈취돼도 피해 범위가 역할 기능에 정의된 범위로 제한된다.

**역할 기능·세션 구성 설계 자체가 별도의 전문성을 요구한다**: JEA를 도입하려면 "이 역할이 정확히 어떤 명령까지 필요한가"를 세밀하게 분석해 `.psrc`/`.pssc` 파일을 작성해야 한다. 필요한 명령을 빠뜨리면 업무가 안 되고, 너무 넓게 허용하면 최소 권한 원칙이 무의미해진다 — 이 설계·검토 과정이 JEA 도입의 실질적인 비용이다.

**이식성**: Linux의 `sudo`와 `sudoers` 파일에서 특정 사용자에게 특정 명령만 허용하는 설정이 개념적으로 가장 가깝다. 다만 JEA는 명령 단위 제한에 더해 언어 모드 제약(임의 스크립팅 차단)과 가상 계정(임시 권한 상승)까지 통합한 훨씬 포괄적인 프레임워크라는 점에서 `sudoers`보다 범위가 넓다. CMD에는 이런 세밀한 위임 관리 개념이 없다.

## Reference

- [Overview of Just Enough Administration (JEA) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/overview)
