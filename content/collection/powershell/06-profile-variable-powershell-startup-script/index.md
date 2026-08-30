---
draft: false
collection_order: 6
slug: profile-variable-powershell-startup-script
title: "[PowerShell] 06. $PROFILE — 프로파일 스크립트"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 프로파일 4종류(AllUsersAllHosts부터 CurrentUserCurrentHost까지)의 경로와 실행 순서, $PROFILE 변수로 각 경로를 확인하는 법, 프로파일 작성·편집과 -NoProfile 문제 진단법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
- Configuration(설정)
- Automation(자동화)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- DevOps
- Profile
- Startup-Script
- VSCode
- Dotfiles
- Customization
image: "wordcloud.png"
---

## 개요

PowerShell **프로파일**은 세션이 시작될 때마다 자동으로 실행되는 `.ps1` 스크립트다. Bash의 `.bashrc`·`.bash_profile`과 목적은 같지만, PowerShell은 이 역할을 하는 파일을 하나가 아니라 네 개까지 두고 각각 다른 범위(모든 사용자/현재 사용자, 모든 호스트/현재 호스트)에 적용한다. 변수·함수·별칭·모듈 임포트·프롬프트 커스터마이징처럼 세션마다 반복해서 설정하고 싶은 항목을 프로파일에 넣어 두면, 콘솔을 열 때마다 자동으로 적용된다.

정신 모델은 "네 개의 파일이 정해진 순서대로 실행되고, 나중에 실행된 것이 앞선 설정을 덮어쓸 수 있다"는 것이다. 자동 변수 `$PROFILE`은 이 네 경로 중 "현재 사용자, 현재 호스트" 프로파일(가장 흔히 쓰이는 것)을 가리키며, 나머지 세 경로는 `$PROFILE`의 노트 속성(`$PROFILE.AllUsersAllHosts` 등)으로 접근한다.

## 사용법

프로파일 종류는 적용 범위(전체 사용자/현재 사용자)와 호스트 범위(전체 호스트/현재 호스트 프로그램)의 조합으로 4가지가 있으며, 실행 순서도 아래 표와 같다.

| 순서 | 프로파일 | `$PROFILE` 속성 | Windows 기본 경로 |
|---|---|---|---|
| 1 | 전체 사용자, 전체 호스트 | `AllUsersAllHosts` | `$PSHOME\Profile.ps1` |
| 2 | 전체 사용자, 현재 호스트 | `AllUsersCurrentHost` | `$PSHOME\Microsoft.PowerShell_profile.ps1` |
| 3 | 현재 사용자, 전체 호스트 | `CurrentUserAllHosts` | `$HOME\Documents\PowerShell\Profile.ps1` |
| 4 | 현재 사용자, 현재 호스트 | `CurrentUserCurrentHost`(= `$PROFILE` 자체) | `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` |

VS Code처럼 PowerShell을 호스팅하는 다른 프로그램은 `Microsoft.VSCode_profile.ps1`처럼 별도의 호스트 전용 프로파일을 추가로 지원한다. 목록 순서대로 실행되므로, 여러 호스트 프로그램에서 공통으로 쓰고 싶은 설정은 `CurrentUserAllHosts`에, 특정 호스트에서만 필요한 설정은 그 호스트 전용 프로파일에 넣는 것이 원칙이다.

## 예시

```powershell
$PROFILE                              # 현재 사용자·현재 호스트 프로파일 경로
$PROFILE | Select-Object *            # 4개 경로를 모두 노트 속성으로 확인
Test-Path -Path $PROFILE              # 프로파일 파일이 이미 존재하는지 확인

if (!(Test-Path -Path $PROFILE)) {    # 프로파일 파일이 없으면 새로 생성
  New-Item -ItemType File -Path $PROFILE -Force
}

notepad $PROFILE                      # 프로파일 편집
pwsh -NoProfile                       # 프로파일을 건너뛰고 콘솔 시작(문제 진단용)
```

프로파일에 자주 넣는 항목의 예시다.

```powershell
# 콘솔 제목에 PowerShell 버전을 표시
$hostVersion = "$($Host.Version.Major).$($Host.Version.Minor)"
$Host.UI.RawUI.WindowTitle = "PowerShell $hostVersion"

# 프롬프트를 사용자 지정 형식으로 재정의
function prompt {
    "$Env:COMPUTERNAME\" + (Get-Location) + "> "
}
```

## 주의사항·함정

**Restricted 실행 정책에서는 프로파일이 아예 실행되지 않는다**: 05장에서 다뤘듯, 기본 실행 정책인 `Restricted`는 구성 파일 로드 자체를 막는다. 프로파일에 넣은 설정이 반영되지 않는다면 `Get-ExecutionPolicy`부터 확인해야 한다.

**원격 세션에는 프로파일이 자동 실행되지 않는다**: `Invoke-Command`나 `Enter-PSSession`으로 연 원격 세션에서는 `$PROFILE` 자동 변수 자체가 채워지지 않고, 로컬 프로파일도 자동으로 실행되지 않는다. 원격 세션에서 프로파일을 적용하려면 `Invoke-Command -Session $s -FilePath $PROFILE`처럼 명시적으로 실행해야 한다(11부에서 원격 세션을 본격적으로 다룬다).

**Microsoft Store(MSIX) 설치본의 제약**: 01장에서 언급했듯, Microsoft Store로 설치한 PowerShell 7은 `$PSHOME`에 쓰기 권한이 없어 `AllUsersAllHosts`·`AllUsersCurrentHost` 프로파일을 만들거나 수정할 수 없다. 현재 사용자 프로파일 두 개만 사용할 수 있다.

**이식성**: Bash는 로그인 셸 여부에 따라 `.bash_profile`과 `.bashrc`를 구분해서 실행하지만, PowerShell의 4단계 프로파일은 로그인 여부가 아니라 "사용자 범위 × 호스트 범위"라는 서로 다른 축으로 나뉜다. CMD는 프로파일 개념 자체가 없고, 대신 `AutoRun` 레지스트리 값으로 비슷한 자동 실행을 흉내 낸다.

## Reference

- [about_Profiles - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles)
