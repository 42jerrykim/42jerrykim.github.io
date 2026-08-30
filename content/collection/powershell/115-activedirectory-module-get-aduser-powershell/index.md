---
draft: false
collection_order: 115
slug: activedirectory-module-get-aduser-powershell
title: "[PowerShell] 115. ActiveDirectory 모듈 개요와 Get-ADUser"
date: 2026-08-29
lastmod: 2026-08-29
description: "RSAT로 설치하는 ActiveDirectory 모듈의 역할과 Get-ADUser의 -Filter/-Identity/-Properties 매개변수로 도메인 사용자 계정을 조회하는 방법을 정리한 Part 17 시작 챕터다."
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
- Get-ADUser
- RSAT
- Domain-Controller
- LDAP-Filter
- Enterprise(엔터프라이즈)
- Identity-Management
image: "wordcloud.png"
---

## 개요

<strong>ActiveDirectory 모듈</strong>은 조직의 사용자·그룹·컴퓨터·정책을 중앙에서 관리하는 Active Directory(AD)를 PowerShell 객체로 다루게 해 주는 모듈이다. 지금까지 Part 1–16이 한 대의 컴퓨터(로컬 또는 원격 세션 하나)를 대상으로 했다면, Part 17(엔터프라이즈 디렉터리 관리)은 시야를 도메인 전체 — 수십에서 수만 대의 컴퓨터와 계정을 아우르는 조직 구조 — 로 넓힌다. 11부(원격 관리)와 14부(보안과 자격 증명)에서 다진 지식이 여기서 실전 전제 조건이 된다.

정신 모델은 "지금까지의 cmdlet들이 한 컴퓨터의 파일 시스템이나 프로세스 목록을 조회했다면, `Get-ADUser`는 그 대상을 디렉터리 서비스(AD)라는 거대한 데이터베이스로 바꿔치기한 것"이라는 것이다. 30장에서 배운 프로바이더 개념처럼 조회·필터링 문법 자체는 익숙하지만, 그 대상이 파일이 아니라 조직 전체의 계정 정보라는 점이 다르다.

## 사용법

```powershell
Get-ADUser -Filter <조건> [-Properties <속성목록>]
Get-ADUser -Identity <SAM계정명/GUID/SID/DN> [-Properties <속성목록>]
```

## 종류

| 매개변수 집합 | 트리거 매개변수 | 용도 |
|---|---|---|
| Identity(단일 조회) | `-Identity` | DN·GUID·SID·SAM 계정명 중 하나로 정확히 한 사용자 조회 |
| Filter(검색) | `-Filter` | PowerShell 표현식 언어로 여러 사용자를 조건 검색 |
| LdapFilter(검색) | `-LDAPFilter` | 기존 LDAP 쿼리 문자열을 그대로 재사용 |

| 주요 매개변수 | 의미 |
|---|---|
| `-Properties` | 기본 속성 집합 외에 추가로 가져올 속성(`*`로 전체 속성 조회 가능) |
| `-SearchBase` | 검색 범위를 특정 OU(조직 구성 단위)로 제한 |
| `-SearchScope` | `Base`/`OneLevel`/`Subtree` — 검색 깊이 지정 |
| `-Credential` | 현재 로그온 계정이 아닌 다른 자격 증명으로 질의(100장 `PSCredential`과 조합) |
| `-Server` | 특정 도메인 컨트롤러를 지정해 질의 |

## 예시

```powershell
Get-ADUser -Filter * -SearchBase "OU=Finance,OU=UserAccounts,DC=FABRIKAM,DC=COM"   # 특정 OU 안의 모든 사용자

Get-ADUser -Filter 'Name -like "*SvcAccount"' |                                     # 12장 방식과 유사한 필터 표현식
    Format-Table Name, SamAccountName -AutoSize

Get-ADUser -Identity ChewDavid -Properties *                                        # 특정 사용자의 모든 속성 조회

Get-ADUser -LDAPFilter '(!userAccountControl:1.2.840.113556.1.4.803:=2)'            # 기존 LDAP 쿼리로 활성화된 계정만 조회

Get-ADUser -Filter "Department -eq 'Sales'" -Properties EmailAddress, Title |         # 부서별 조회 + 필요한 속성만 추가
    Select-Object Name, EmailAddress, Title

Import-Module ActiveDirectory                                                        # 모듈이 아직 로드되지 않았다면 명시적으로 임포트(74–75장 참고)
```

## 주의사항·함정

**ActiveDirectory 모듈은 기본 설치되어 있지 않고 RSAT(원격 서버 관리 도구)를 통해 별도로 설치해야 한다**: Windows 클라이언트에서는 "설정 → 앱 → 선택적 기능"에서 "RSAT: Active Directory Domain Services and Lightweight Directory Tools"를 추가해야 하며, 도메인 컨트롤러가 아닌 일반 워크스테이션에는 기본적으로 이 모듈이 없다. 80장에서 배운 PackageManagement로 설치되는 일반 모듈과 달리, RSAT는 Windows 기능 자체를 켜는 절차라는 점이 다르다.

**`-Filter`의 문법은 `Where-Object`의 `-eq`/`-like` 연산자와 비슷해 보이지만 실제로는 완전히 다른 쿼리 언어(PowerShell 표현식 언어)로 서버 측에서 실행된다**: 클라이언트 쪽에서 객체를 받아온 뒤 필터링하는 12장의 `Where-Object`와 달리, `-Filter`는 조건을 도메인 컨트롤러로 그대로 전달해 서버에서 검색을 수행한다. 이 차이 때문에 `-Filter`에는 임의의 PowerShell 스크립트 블록이나 `?` 와일드카드를 쓸 수 없고, 지원되는 연산자 집합도 제한적이다.

**기본 속성 집합에는 이메일·부서 같은 흔히 필요한 속성이 빠져 있다**: `Get-ADUser`를 매개변수 없이 호출하면 `Name`, `SamAccountName` 같은 최소한의 속성만 반환되고, `Department`나 `mail` 같은 속성은 `-Properties`에 명시적으로 나열해야만 나타난다. 필요한 속성이 결과에 없다고 해서 그 사용자에게 값이 없는 것은 아니라, 애초에 요청하지 않았을 뿐인 경우가 많다.

**대규모 도메인에서 `-Filter *`로 전체 조회를 하면 `-ResultPageSize`(기본 256)에 따라 여러 페이지로 나뉘어 응답 시간이 길어질 수 있다**: 필요한 범위를 `-SearchBase`로 좁히거나 구체적인 필터 조건을 지정하지 않으면, 수만 개의 계정을 가진 조직에서는 쿼리 자체가 상당한 부하를 유발할 수 있다.

**이식성**: Linux 진영에서 LDAP 디렉터리를 다루는 표준 도구는 `ldapsearch`이며, `Get-ADUser -LDAPFilter`는 바로 그 LDAP 쿼리 문법을 그대로 재사용할 수 있게 다리를 놓아준다. 다만 `ldapsearch`는 원시 LDAP 프로토콜 수준에서 동작해 반환값이 텍스트 속성 목록인 반면, `Get-ADUser`는 그 결과를 `Microsoft.ActiveDirectory.Management.ADUser` 객체로 감싸 파이프라인의 다른 cmdlet과 곧바로 연결할 수 있게 해준다.

## Reference

- [Get-ADUser (ActiveDirectory) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-aduser?view=windowsserver2025-ps)
