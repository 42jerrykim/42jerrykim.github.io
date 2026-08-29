---
draft: true
collection_order: 99
slug: get-hotfix-installed-update-powershell
title: "[PowerShell] 99. Get-HotFix — 설치된 업데이트 조회"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-HotFix가 Win32_QuickFixEngineering WMI 클래스로 CBS 기반 업데이트만 조회하는 원리와 -Id/-Description 매개변수, 82장 PSWindowsUpdate 모듈과의 역할 차이를 정리한 Part 13 마지막 챕터다."
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
- Get-HotFix
- QuickFixEngineering
- Windows-Update
- Patch-Audit
- KB-Article
- Update-Compliance
image: "wordcloud.png"
---

## 개요

`Get-HotFix`는 `Win32_QuickFixEngineering` WMI 클래스를 통해 컴퓨터에 설치된 업데이트(핫픽스, KB로 시작하는 그 항목들)를 조회하는 cmdlet이다. 82장에서 다룬 PSWindowsUpdate 모듈이 "업데이트를 검색·설치"하는 능동적 도구였다면, `Get-HotFix`는 "이미 설치된 것을 감사(audit)"하는 조회 전용 도구라는 점이 다르다. Part 13(스토리지와 시스템 구성)의 마지막 챕터로서, 지금까지 조회해 온 디스크·시스템 정보·환경 변수에 이어 "이 시스템에 무엇이 패치됐는가"라는 마지막 질문에 답한다.

정신 모델은 "`Get-HotFix`는 컴퓨터 관리 콘솔의 '설치된 업데이트' 목록을 명령줄로 옮겨온 것"이라는 것이다. 다만 이 목록이 **모든** 업데이트를 다 보여주지는 않는다는 중요한 제약이 있다.

## 사용법

```powershell
Get-HotFix [[-Id] <String[]>] [-Description <String[]>] [-ComputerName <String[]>]
```

## 종류

| 매개변수/속성 | 설명 |
|---|---|
| `-Id`(별칭 `-HFID`) | 특정 KB 번호로 조회(와일드카드 미지원) |
| `-Description` | 업데이트 유형으로 조회(`"Security*"` 등 와일드카드 지원) |
| `-ComputerName` | 원격 컴퓨터 조회(WinRM 없이 별도 메커니즘으로 동작) |
| `HotFixID` 속성 | KB 번호 |
| `InstalledOn` 속성 | 설치된 날짜(52장의 `DateTime` 타입) |
| `InstalledBy` 속성 | 설치한 계정(대개 `NT AUTHORITY\SYSTEM`) |

## 예시

```powershell
Get-HotFix                                                  # 로컬 컴퓨터의 모든 핫픽스

Get-HotFix -Id KB4495590                                       # 특정 업데이트가 설치됐는지 확인

$hotFixParams = @{
    Description  = "Security*"
    ComputerName = "Server01", "Server02"
    Credential   = "Domain01\admin01"
}
Get-HotFix @hotFixParams                                        # 25장 스플래핑, 여러 컴퓨터의 보안 업데이트만

(Get-HotFix | Sort-Object -Property InstalledOn)[-1]              # 19장 Sort-Object로 가장 최근 설치 항목

# 특정 업데이트가 없는 컴퓨터 찾아 기록
$Servers = Get-Content -Path .\Servers.txt
$Servers | ForEach-Object {
    if (-not (Get-HotFix -Id KB957095 -ComputerName $_ -ErrorAction SilentlyContinue)) {
        Add-Content -Path .\Missing-KB957095.txt -Value $_
    }
}

Get-HotFix | Where-Object InstalledOn -gt (Get-Date).AddDays(-30)     # 12장 응용, 최근 30일 내 설치분만
```

## 주의사항·함정

**모든 업데이트를 다 보여주는 것은 아니다**: `Win32_QuickFixEngineering` 클래스는 CBS(Component Based Servicing)로 적용된 업데이트만 반환하며, MSI(Windows Installer)나 Windows Update 사이트를 통해 설치된 일부 업데이트는 이 목록에 나타나지 않는다. "이 KB가 확실히 설치 안 됐다"는 결론을 내리기 전에, 82장의 PSWindowsUpdate 모듈이나 `Get-ComputerInfo`(97장)의 `OsHotFixes` 속성처럼 다른 소스로도 교차 확인하는 것이 안전하다.

**시스템·업데이트 유형에 따라 출력 항목이 크게 달라질 수 있다**: 문서에도 명시돼 있듯, `Get-HotFix`의 결과는 운영체제 버전과 설치된 업데이트 종류에 따라 들쭉날쭉할 수 있다. 여러 서버를 감사하는 스크립트라면 특정 컴퓨터에서 예상보다 적은 결과가 나와도 곧바로 "패치가 안 됐다"고 단정하지 말고, 이 cmdlet 자체의 조회 범위 한계를 먼저 의심해야 한다.

**`-Id`는 와일드카드를 지원하지 않는다**: `-Description`과 달리 `-Id`는 정확한 KB 번호를 요구하므로, `KB449*`처럼 부분 일치로 찾으려 하면 결과가 나오지 않는다. 패턴으로 찾아야 한다면 `Get-HotFix | Where-Object HotFixID -like "KB449*"`처럼 12장의 `Where-Object`로 다시 걸러야 한다.

**Windows 전용 cmdlet이다**: `Get-Service`(91장), `Get-ComputerInfo`(97장)와 마찬가지로 macOS·Linux에서는 사용할 수 없다.

**이식성**: Linux의 `apt list --installed`, `dpkg -l`, `rpm -qa`가 "설치된 패키지·패치 목록 조회"라는 목적에서 대응하는 도구다. Windows의 업데이트 체계가 CBS·MSI·Windows Update라는 여러 경로로 나뉘어 있는 것과 달리, Linux 배포판은 대개 패키지 관리자 하나로 시스템 패치까지 통합 관리한다는 점이 이 cmdlet의 조회 범위 제약과 대조적이다.

## Reference

- [Get-HotFix (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix)
