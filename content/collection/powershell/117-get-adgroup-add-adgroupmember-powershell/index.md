---
draft: true
collection_order: 117
slug: get-adgroup-add-adgroupmember-powershell
title: "[PowerShell] 117. Get-ADGroup/Add-ADGroupMember — 그룹 관리"
date: 2026-08-29
lastmod: 2026-08-29
description: "AD 그룹을 조회하는 Get-ADGroup과 -Members로 구성원을 추가하는 Add-ADGroupMember를 통해 116장의 개별 계정 관리를 넘어 조직 단위 권한 부여로 확장하는 방법을 GroupScope 개념과 함께 정리한 챕터다."
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
- ActiveDirectory
- Get-ADGroup
- Add-ADGroupMember
- Group-Membership
- Security-Group
- Enterprise(엔터프라이즈)
- Identity-Management
image: "wordcloud.png"
---

## 개요

115–116장이 개별 사용자 계정을 다뤘다면, 이 장은 그 계정들을 묶는 단위인 <strong>AD 그룹</strong>을 조회·관리하는 <strong>Get-ADGroup</strong>과 <strong>Add-ADGroupMember</strong>를 다룬다. 실무에서 권한은 거의 항상 개별 사용자가 아니라 그룹 단위로 부여된다 — "이 파일 서버에 dchew가 접근할 수 있다"가 아니라 "Sales 그룹이 접근할 수 있고 dchew는 그 그룹의 구성원이다"라는 간접 구조가 표준이다.

정신 모델은 "AD 그룹은 91장에서 다룬 Windows 서비스의 의존 관계와 비슷하게, 권한이라는 자원을 여러 계정이 공유하게 해주는 간접 계층"이라는 것이다. 권한을 계정에 직접 부여하는 대신 그룹에 부여하고 계정을 그룹에 넣었다 뺐다 하면, 각 계정마다 권한을 일일이 재설정할 필요 없이 그룹 구성원 관계만 조정하면 된다.

## 사용법

```powershell
Get-ADGroup -Identity <그룹명> [-Properties <속성목록>]
Add-ADGroupMember -Identity <그룹명> -Members <계정1>, <계정2>, ...
```

## 종류

| cmdlet | 주요 매개변수 | 의미 |
|---|---|---|
| `Get-ADGroup` | `-Identity` | DN·GUID·SID·SAM 계정명으로 그룹 하나 조회 |
| `Get-ADGroup` | `-Filter` | 조건에 맞는 여러 그룹 검색(115장 `Get-ADUser -Filter`와 동일한 문법) |
| `Get-ADGroup` | `-Properties member` | 그룹의 현재 구성원 목록까지 함께 조회 |
| `Add-ADGroupMember` | `-Identity` | 구성원을 추가할 대상 그룹 |
| `Add-ADGroupMember` | `-Members` | 추가할 사용자·그룹·컴퓨터 계정 목록(쉼표로 구분, 파이프라인 입력 불가) |
| `Add-ADGroupMember` | `-PassThru` | 기본적으로 출력이 없는 이 cmdlet이 수정된 그룹 객체를 반환하게 함 |

| 그룹 속성 | 의미 |
|---|---|
| `GroupCategory` | `Security`(권한 부여용) 또는 `Distribution`(메일 배포용) |
| `GroupScope` | `DomainLocal`/`Global`/`Universal` — 그룹이 유효한 범위 |

## 예시

```powershell
Get-ADGroup -Identity Administrators                                   # SAM 계정명으로 그룹 조회

Get-ADGroup -Identity S-1-5-32-544 -Properties member                    # SID로 조회 + 구성원 목록 포함

Get-ADGroup -Filter 'GroupCategory -eq "Security" -and GroupScope -ne "DomainLocal"'   # 115장과 동일한 필터 문법

Add-ADGroupMember -Identity SvcAccPSOGroup -Members SQL01, SQL02          # 여러 계정을 한 그룹에 한 번에 추가

Get-ADGroup -Filter "name -like 'AccountLeads'" |                         # Get-ADGroup 결과를 파이프라인으로 전달
    Add-ADGroupMember -Members 'CN=PattiFuller,OU=AccountDeptOU,DC=AppNC'

Get-ADUser -Identity dchew | Get-ADPrincipalGroupMembership               # 반대 방향 — 이 계정이 속한 모든 그룹 조회

Add-ADGroupMember -Identity "Sales" -Members dchew -WhatIf                # 26장 방식으로 실제 적용 전 미리보기
```

## 주의사항·함정

**`Add-ADGroupMember -Members`는 파이프라인으로 값을 받지 않는다**: `-Identity`는 파이프라인 입력을 받아 `Get-ADGroup | Add-ADGroupMember`처럼 쓸 수 있지만, 추가할 대상 목록인 `-Members`는 반드시 매개변수로 직접 전달해야 한다. 이 비대칭을 모르고 사용자 목록을 파이프로 넘기려 하면 조용히 무시되거나 오류가 난다 — 여러 사용자를 여러 그룹에 넣는 반대 방향의 파이프라인이 필요하다면 `Add-ADPrincipalGroupMembership`을 대신 써야 한다.

**이미 구성원인 계정을 다시 추가하면 기본적으로 오류 없이 무시된다("permissive modify")**: 이 기본 동작 덕분에 스크립트를 여러 번 실행해도 안전(멱등적)하지만, 중복 추가 시도를 명시적으로 오류로 감지하고 싶다면 `-DisablePermissiveModify`를 지정해야 한다. 이 옵션은 Windows Server 2019 이후에서만 사용할 수 있다.

**`GroupScope`(도메인 로컬/글로벌/유니버설)의 차이를 무시하고 그룹을 설계하면 나중에 여러 도메인에 걸친 권한 부여가 꼬인다**: 이 범위 규칙은 AD의 오래된 설계이지만 여전히 유효하며, 특히 여러 도메인·포리스트가 얽힌 환경에서는 어떤 범위의 그룹에 어떤 유형의 구성원을 넣을 수 있는지 미리 확인해야 한다 — 예를 들어 유니버설 그룹은 다른 도메인의 구성원도 포함할 수 있지만 도메인 로컬 그룹은 그렇지 않다.

**그룹을 자기 자신의 구성원으로 추가할 수 있다는 것을 놓치기 쉽다**: `Add-ADGroupMember`는 이런 순환 참조를 막아주지 않으며, 공식 문서도 이로 인해 불안정한 동작이 발생할 수 있다고 명시한다. 스크립트로 그룹 구성원을 자동화할 때는 추가하려는 대상이 그룹 자신이 아닌지 확인하는 방어 로직을 넣는 것이 안전하다.

**이식성**: Linux의 `usermod -aG <그룹> <사용자>`가 개념적으로 `Add-ADGroupMember`와 가장 가깝지만, 로컬 `/etc/group` 파일만을 대상으로 한다는 점에서 범위가 다르다. 도메인 전체에 걸친 그룹 기반 권한 위임이라는 개념 자체는 LDAP 기반의 중앙 인증 시스템(FreeIPA 등)에서도 존재하지만, `GroupScope`처럼 AD 특유의 세분화된 범위 개념까지 그대로 대응하지는 않는다.

## Reference

- [Get-ADGroup (ActiveDirectory) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adgroup?view=windowsserver2025-ps)
- [Add-ADGroupMember (ActiveDirectory) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/add-adgroupmember?view=windowsserver2025-ps)
