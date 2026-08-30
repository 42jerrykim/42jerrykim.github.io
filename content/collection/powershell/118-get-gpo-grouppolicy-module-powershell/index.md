---
draft: false
collection_order: 118
slug: get-gpo-grouppolicy-module-powershell
title: "[PowerShell] 118. Get-GPO — 그룹 정책 조회(GroupPolicy 모듈)"
date: 2026-08-29
lastmod: 2026-08-29
description: "GroupPolicy 모듈의 Get-GPO로 도메인의 그룹 정책 객체(GPO)를 이름·GUID로 조회하는 법과, 115–117장의 계정·그룹 관리가 정책이라는 세 번째 축과 어떻게 맞물리는지 정리한 Part 17 마지막 챕터다."
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
- GroupPolicy
- Get-GPO
- GPO
- Domain-Controller
- Enterprise(엔터프라이즈)
- Identity-Management
- Configuration-Drift
image: "wordcloud.png"
---

## 개요

115–117장이 "누가"(사용자)와 "어떤 묶음에 속하는가"(그룹)를 다뤘다면, Part 17을 마무리하는 이 장은 세 번째 축인 "무엇이 적용되는가" — <strong>그룹 정책 객체(GPO, Group Policy Object)</strong>를 조회하는 <strong>Get-GPO</strong>를 다룬다. 106–108장에서 배운 DSC가 개별 노드의 상태를 선언적으로 정의했다면, GPO는 AD 도메인 전체에 걸쳐 컴퓨터·사용자 설정을 중앙에서 배포하는 훨씬 오래되고 더 널리 쓰이는 메커니즘이다.

정신 모델은 "AD 사용자·그룹이 '누가 무엇에 속하는가'를 정의하는 명부라면, GPO는 '그 명부에 속한 대상에게 어떤 설정을 강제할 것인가'를 정의하는 규정집"이라는 것이다. `Get-GPO`는 이 규정집 자체를 조회할 뿐, 그 규정이 실제로 적용되는 대상(OU에 대한 GPO 링크)까지는 다루지 않는다는 점이 이 장의 핵심 경계선이다.

## 사용법

```powershell
Get-GPO -Name <표시이름> [-Domain <도메인>]
Get-GPO -Guid <GUID> [-Domain <도메인>]
Get-GPO -All [-Domain <도메인>]
```

## 종류

| 매개변수 집합 | 트리거 매개변수 | 동작 |
|---|---|---|
| ByName | `-Name` | 표시 이름으로 GPO 하나 조회(이름이 도메인 내에서 중복되면 오류) |
| ByGUID | `-Guid` | 전역 고유 식별자로 GPO 하나 조회(이름과 달리 항상 고유) |
| GetAll | `-All` | 도메인의 모든 GPO 조회 |

| 반환 속성 | 의미 |
|---|---|
| `DisplayName` | GPO의 표시 이름 |
| `Id` | GPO의 GUID |
| `GpoStatus` | `AllSettingsEnabled`/`UserSettingsDisabled`/`ComputerSettingsDisabled`/`AllSettingsDisabled` |
| `CreationTime`/`ModificationTime` | 생성·마지막 수정 시각 |
| `Owner` | GPO를 소유한 보안 주체 |
| `WmiFilter` | 이 GPO 적용 여부를 결정하는 94장 CIM/WMI 기반 필터 |

## 예시

```powershell
Get-GPO -Name "Group Policy Test"                                # 표시 이름으로 GPO 조회

Get-GPO -Guid 31a09564-cd4a-4520-98fa-446a2af23b4b -Domain "sales.contoso.com"   # 다른 도메인의 GPO를 GUID로 조회

Get-GPO -All -Domain "sales.contoso.com" |                         # 도메인 내 모든 GPO를 조회해 상태별로 정리
    Select-Object DisplayName, GpoStatus, ModificationTime |
    Sort-Object ModificationTime -Descending                        # 14장에서 배운 Sort-Object 재사용

Get-GPO -All | Where-Object GpoStatus -ne "AllSettingsEnabled"      # 일부 설정이 비활성화된 GPO만 필터링(12장 패턴)

Get-GPO -Name "Group Policy Test" | Get-GPOReport -ReportType Html -Path "C:\Reports\gpo.html"   # 정책 세부 내용을 HTML 보고서로 추출
```

## 주의사항·함정

**`Get-GPO`는 GPO 객체 자체만 반환하며, 그 GPO가 어느 OU에 링크돼 있는지는 알려주지 않는다**: "이 정책이 실제로 어디에 적용되는가"를 확인하려면 `Get-GPOReport`나 그룹 정책 관리 콘솔(GPMC)에서 GPO 링크를 별도로 확인해야 한다. `Get-GPO`만 보고 "이 GPO는 존재하니 어딘가에 적용되고 있다"고 단정하면 안 된다 — 링크되지 않은 GPO는 정의돼 있어도 아무 컴퓨터에도 영향을 주지 않는다.

**`-Name`으로 조회할 때 같은 이름의 GPO가 두 개 이상 있으면 오류가 난다**: GPO의 표시 이름은 고유함이 보장되지 않는다. 자동화 스크립트에서 GPO를 안정적으로 식별해야 한다면 이름 대신 절대 유일한 `-Guid`를 쓰는 것이 더 안전하며, 처음 GPO를 만들 때 `Id`(GUID)를 기록해 두는 습관이 필요하다.

**GroupPolicy 모듈도 ActiveDirectory 모듈과 마찬가지로 기본 설치돼 있지 않다**: RSAT의 "Group Policy Management Tools" 기능을 별도로 설치해야 `Get-GPO`를 쓸 수 있으며, 도메인에 가입되지 않은 컴퓨터에서는 애초에 이 모듈이 의미가 없다.

**GPO를 조회하는 것과 그 내용(어떤 레지스트리 값·정책이 설정돼 있는지)을 확인하는 것은 다른 작업이다**: `Get-GPO`의 반환 객체에는 정책 자체의 상세 설정이 들어있지 않으며, 세부 내용을 보려면 `Get-GPOReport`로 XML/HTML 보고서를 생성해 별도로 파싱해야 한다. 이 계층 분리를 모르면 `Get-GPO` 결과에서 원하는 설정값을 찾으려다 헤매게 된다.

**이식성**: Linux 진영에는 GPO에 정확히 대응하는 개념이 없다. Ansible이나 Puppet 같은 구성 관리 도구가 "여러 대상에 설정을 일괄 배포한다"는 목표는 공유하지만, 그 도구들은 명시적으로 실행해야 적용되는 반면 GPO는 도메인에 가입된 컴퓨터가 주기적으로 스스로 정책을 재확인하고 적용하는 푸시 방식에 가깝다 — 108장에서 다룬 DSC의 LCM이 "지속적으로 감시하며 스스로 교정한다"는 개념과 오히려 더 유사하다.

## Reference

- [Get-GPO (GroupPolicy) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/grouppolicy/get-gpo?view=windowsserver2025-ps)
