---
draft: true
collection_order: 108
slug: dsc-resource-lcm-powershell
title: "[PowerShell] 108. DSC 리소스와 로컬 구성 관리자(LCM)"
date: 2026-08-29
lastmod: 2026-08-29
description: "각 노드에서 MOF 구성을 실제로 적용·감시하는 로컬 구성 관리자(LCM)의 역할과 RefreshMode(Push/Pull), ConfigurationMode(ApplyOnly/ApplyAndMonitor/ApplyAndAutoCorrect) 설정을 정리한 Part 15 마지막 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- DSC
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
- Local-Configuration-Manager
- LCM
- RefreshMode
- ConfigurationMode
- Pull-Server
- Configuration-Monitoring
image: "wordcloud.png"
---

## 개요

<strong>로컬 구성 관리자(LCM, Local Configuration Manager)</strong>는 모든 대상 노드에서 실행되며 MOF 구성을 실제로 파싱하고 적용하는 DSC의 엔진이다. 107장에서 `Start-DscConfiguration`으로 구성을 "밀어 넣었을" 때, 그 뒤에서 실제로 작업을 수행하는 것이 바로 이 LCM이다. Part 15(DSC)의 마지막 챕터로서, "DSC가 구성을 어떻게 적용하는가"뿐 아니라 "적용 후에도 그 상태를 계속 유지할 것인가"라는 지속성의 문제를 다룬다.

정신 모델은 "LCM은 각 노드에 상주하는 감독관이고, `Settings` 블록으로 그 감독관에게 '지시를 어떻게 받을지'(Push/Pull)와 '드리프트가 생기면 어떻게 할지'(ApplyOnly/ApplyAndMonitor/ApplyAndAutoCorrect)를 지시하는 것"이라는 것이다.

## 사용법

```powershell
[DSCLocalConfigurationManager()]
Configuration <메타구성이름> {
    Node <노드> {
        Settings { RefreshMode = "Push"; ConfigurationMode = "ApplyAndAutoCorrect" }
    }
}
Set-DscLocalConfigurationManager -Path <메타구성경로>
```

## 종류

| Settings 속성 | 값 | 의미 |
|---|---|---|
| `RefreshMode` | `Disabled`/`Push`(기본)/`Pull` | `Push`는 `Start-DscConfiguration`으로 수동 전달, `Pull`은 노드가 스스로 주기적으로 서버에서 구성을 가져옴 |
| `ConfigurationMode` | `ApplyOnly`/`ApplyAndMonitor`(기본)/`ApplyAndAutoCorrect` | 적용 후 상태가 어긋나면(드리프트) 로그만 남길지, 스스로 다시 맞출지 |
| `ConfigurationModeFrequencyMins` | 정수(기본 15) | `ApplyAndMonitor`/`ApplyAndAutoCorrect`에서 얼마나 자주 상태를 재확인할지 |
| `RefreshFrequencyMins` | 정수(기본 30) | `Pull` 모드에서 서버로부터 새 구성을 얼마나 자주 확인할지 |
| `RebootNodeIfNeeded` | `$true`/`$false`(기본) | 구성 적용에 재부팅이 필요하면 자동으로 재부팅할지 |

## 예시

```powershell
[DSCLocalConfigurationManager()]
Configuration LCMConfig {
    Node "localhost" {
        Settings {
            RefreshMode                    = "Push"
            ConfigurationMode              = "ApplyAndAutoCorrect"   # 드리프트 발생 시 자동으로 재적용
            ConfigurationModeFrequencyMins = 30
            RebootNodeIfNeeded             = $true
        }
    }
}

LCMConfig -OutputPath "C:\DSC\LCMConfig"                      # 일반 Configuration과 동일하게 컴파일
Set-DscLocalConfigurationManager -Path "C:\DSC\LCMConfig"       # Start-DscConfiguration이 아니라 이 cmdlet 사용

Get-DscLocalConfigurationManager                                  # 현재 LCM 설정 확인(RefreshMode, ConfigurationMode 등)

# Pull 모드 예시 — 노드가 스스로 서버에서 구성을 가져오도록 설정
[DSCLocalConfigurationManager()]
Configuration PullLCM {
    Node "localhost" {
        Settings { RefreshMode = "Pull" }
        ConfigurationRepositoryWeb PullServer {
            ServerURL = "https://dscpull.contoso.com:8080/PSDSCPullServer.svc"
            RegistrationKey = "d4b28f8c-..."
        }
    }
}
```

## 주의사항·함정

**LCM 설정은 `Start-DscConfiguration`이 아니라 `Set-DscLocalConfigurationManager`로 적용한다**: 107장의 일반 Configuration과 문법은 똑같아 보이지만, `[DSCLocalConfigurationManager()]` 특성이 붙은 메타 구성은 별도의 cmdlet으로 적용해야 한다. 이 둘을 혼동해 `Start-DscConfiguration`으로 LCM 설정을 적용하려 하면 오류가 난다.

**`ApplyOnly`은 이름과 달리 "한 번만 적용하고 다시는 확인하지 않는다"는 뜻이 아니다**: 정확히는, 최초 적용이 성공할 때까지는 재시도하지만 일단 성공적으로 적용된 이후에는 드리프트(상태 이탈)를 감시하지 않는다는 뜻이다. 지속적인 상태 유지가 필요하다면 `ApplyAndMonitor`나 `ApplyAndAutoCorrect`를 선택해야 한다.

**`ApplyAndAutoCorrect`는 강력하지만 예기치 않은 변경을 계속 되돌릴 수 있다**: 운영자가 긴급 상황에서 수동으로 임시 조치를 했는데, LCM이 `ConfigurationModeFrequencyMins` 주기마다 그 변경을 조용히 "정상"으로 되돌려 버릴 수 있다. 긴급 대응 중에는 LCM을 일시적으로 `ApplyOnly`나 `Disabled`로 전환하는 것도 고려해야 하는 이유다.

**`RefreshFrequencyMins`와 `ConfigurationModeFrequencyMins`를 혼동하기 쉽다**: 전자는 `Pull` 모드에서 "서버로부터 새 구성을 확인하는 주기"이고, 후자는 "로컬 상태의 드리프트를 재확인하는 주기"다. 원래 의도는 `RefreshFrequencyMins`를 `ConfigurationModeFrequencyMins`보다 길게 설정해, 구성 자체는 드물게 갱신하되 로컬 드리프트는 더 자주 감시하는 것이다 — 이 둘을 반대로 설정하면 의도한 감시 주기와 실제 동작이 어긋난다.

**이식성**: Puppet 에이전트의 `--test`/`--noop` 모드(변경 없이 드리프트만 보고)와 일반 적용 모드의 구분이 LCM의 `ApplyAndMonitor`/`ApplyAndAutoCorrect` 구분과 유사하다. Ansible은 기본적으로 지속적인 데몬 감시 없이 수동/예약 실행에 의존하는데(Ansible Tower/AWX 같은 별도 도구로 이를 보완), LCM처럼 각 노드에 상주하며 자율적으로 드리프트를 교정하는 에이전트 모델은 Puppet·Chef의 아키텍처에 더 가깝다.

## Reference

- [Configuring the Local Configuration Manager - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/dsc/managing-nodes/metaconfig)
