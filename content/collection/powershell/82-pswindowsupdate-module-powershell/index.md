---
draft: true
collection_order: 82
slug: pswindowsupdate-module-powershell
title: "[PowerShell] 82. PSWindowsUpdate — Windows 업데이트 관리 모듈"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell Gallery의 PSWindowsUpdate 모듈로 Get-WindowsUpdate/Install-WindowsUpdate를 통해 Windows 업데이트를 조회·설치하는 법과 -RecurseCycle로 재부팅 후 자동 재개하는 법을 정리한 Part 10 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Package-Management
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
- PSWindowsUpdate
- Windows-Update
- Patch-Management
- Get-WindowsUpdate
- Install-WindowsUpdate
- System-Maintenance
image: "wordcloud.png"
---

## 개요

**PSWindowsUpdate**는 Windows Update 클라이언트를 PowerShell cmdlet으로 다룰 수 있게 해 주는 커뮤니티 모듈로, 76장에서 배운 `Install-Module`로 PowerShell Gallery에서 직접 설치한다. 80–81장이 "애플리케이션"을 설치·관리하는 도구였다면, 이 장은 "운영체제 자체"의 패치를 관리하는 영역으로 넘어가며 Part 10(패키지·업데이트 관리)을 마무리한다. Windows 자체에는 이 작업을 위한 표준 내장 cmdlet이 없어, PSWindowsUpdate가 사실상 업계 표준처럼 널리 쓰인다.

정신 모델은 "GUI의 '설정 → Windows Update' 화면이 하는 일을, 스크립트로 자동화하고 여러 컴퓨터에 일괄 적용할 수 있게 만든 것"이라는 것이다.

## 사용법

```powershell
Install-Module -Name PSWindowsUpdate -Scope CurrentUser    # 76장에서 배운 방식으로 설치
Get-WindowsUpdate
Install-WindowsUpdate [-AcceptAll] [-AutoReboot] [-RecurseCycle]
```

## 종류

| cmdlet | 역할 |
|---|---|
| `Get-WindowsUpdate` | 적용 가능한 업데이트 목록 조회(설치는 안 함) |
| `Install-WindowsUpdate` | 업데이트 다운로드·설치 |
| `Get-WUHistory` | 과거에 설치된 업데이트 이력 |
| `Get-WUSettings` / `Set-WUSettings` | Windows Update 클라이언트 설정 조회·변경 |
| `Remove-WindowsUpdate` | 설치된 특정 업데이트 제거 |
| `-RecurseCycle` | 설치 후 재부팅이 필요하면 자동 재부팅하고, 재부팅 뒤 세션에서 남은 업데이트를 이어서 설치 |

## 예시

```powershell
Install-Module -Name PSWindowsUpdate -Scope CurrentUser -Force

Get-WindowsUpdate                                          # 적용 가능한 업데이트 확인(설치 안 함)
Get-WindowsUpdate -Category "Security Updates"                # 카테고리로 좁혀서 확인

Install-WindowsUpdate -AcceptAll -AutoReboot                    # 전부 설치하고 필요하면 자동 재부팅
Install-WindowsUpdate -AcceptAll -RecurseCycle                    # 여러 번의 재부팅이 필요해도 끝까지 자동 진행

Get-WUHistory | Select-Object Title, Date, Result                  # 13장 Select-Object로 설치 이력 요약

# 원격 여러 서버에 일괄 적용(11부에서 다룰 원격 관리와 결합)
Invoke-Command -ComputerName Server01, Server02 -ScriptBlock {
    Install-WindowsUpdate -AcceptAll -AutoReboot
}

Get-WUSettings                                                       # 현재 업데이트 정책 설정 확인
```

## 주의사항·함정

**PSWindowsUpdate는 Microsoft 공식 모듈이 아니라 커뮤니티 모듈이다**: `Install-WindowsUpdate` 같은 이름이 마치 시스템 내장 명령처럼 보이지만, 실제로는 개인 개발자가 유지보수하는 PowerShell Gallery 모듈이다. 76장에서 다룬 대로 설치 전 코드를 신뢰할 수 있는지 검토하는 습관이 특히 이 모듈처럼 시스템 깊은 곳(운영체제 패치)에 관여하는 도구에는 더욱 중요하다.

**`-AutoReboot`나 `-RecurseCycle` 없이는 재부팅이 필요한 업데이트가 중간에 멈춘다**: 많은 보안 업데이트가 재부팅을 요구하는데, 이 매개변수를 지정하지 않으면 스크립트가 "재부팅이 필요합니다"라는 상태만 남기고 다음 단계로 진행하지 않는다. 무인 자동화 스크립트에서는 재부팅 전략(즉시 재부팅할지, 예약할지)을 명확히 설계해야 한다 — 특히 여러 서버를 한 번에 재부팅하면 서비스 중단이 동시에 발생할 수 있다는 점을 감안해야 한다.

**업데이트 설치는 되돌리기 어려운 시스템 변경이다**: 65장에서 배운 `try`/`catch`로 오류를 잡을 수는 있지만, 이미 적용된 Windows 업데이트 자체를 스크립트로 안전하게 롤백하는 것은 훨씬 까다롭다. 프로덕션 서버에 일괄 적용하기 전에는 반드시 테스트 환경에서 먼저 검증하는 절차가 필요하다.

**이식성**: Linux의 `apt upgrade`/`dnf update`, macOS의 `softwareupdate` 명령이 운영체제 패치라는 같은 목적을 수행하지만, 각 플랫폼이 자체 패키지 관리자에 이 기능을 통합해 둔 것과 달리 Windows는 표준 명령줄 도구가 없어 PSWindowsUpdate 같은 서드파티 모듈에 의존한다는 점이 특징이다. 대규모 조직이라면 WSUS(Windows Server Update Services)나 Microsoft Intune 같은 전용 패치 관리 시스템이 이 모듈보다 더 널리 쓰인다.

## Reference

- [PSWindowsUpdate - PowerShell Gallery](https://www.powershellgallery.com/packages/PSWindowsUpdate)
