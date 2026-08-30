---
draft: false
collection_order: 116
slug: new-aduser-set-aduser-powershell
title: "[PowerShell] 116. New-ADUser/Set-ADUser — 계정 생성·수정"
date: 2026-08-29
lastmod: 2026-08-29
description: "New-ADUser로 도메인 계정을 생성할 때 -AccountPassword/-Enabled 같은 필수 매개변수를 챙기는 법과, Set-ADUser로 기존 계정 속성을 수정하는 방법을 115장 조회 지식 위에서 정리한 챕터다."
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
- New-ADUser
- Set-ADUser
- SecureString
- Account-Provisioning
- Enterprise(엔터프라이즈)
- Identity-Management
image: "wordcloud.png"
---

## 개요

115장이 AD 사용자를 "조회"하는 법을 다뤘다면, 이 장은 그 계정을 실제로 "생성"하고 "수정"하는 두 cmdlet — <strong>New-ADUser</strong>와 <strong>Set-ADUser</strong> — 를 다룬다. 조회는 실수해도 되돌릴 방법이 있지만, 계정 생성·수정은 조직 전체의 인증 체계에 직접 영향을 주는 작업이라 100장의 `PSCredential`·`SecureString` 개념이 여기서 실전 필수 지식으로 다시 등장한다.

정신 모델은 "`New-ADUser`가 도메인이라는 조직 데이터베이스에 새 레코드를 추가하는 것이라면, `Set-ADUser`는 이미 존재하는 레코드의 특정 필드만 골라 갱신하는 것"이라는 것이다. 신규 함수를 작성하는 것(생성)과 기존 함수의 매개변수 기본값만 바꾸는 것(수정)의 차이와 비슷하다.

## 사용법

```powershell
New-ADUser -Name <표시이름> -SamAccountName <계정명> -AccountPassword <SecureString> -Enabled $true
Set-ADUser -Identity <계정> -<속성이름> <새값>
```

## 종류

| cmdlet | 필수/핵심 매개변수 | 의미 |
|---|---|---|
| `New-ADUser` | `-Name` | 계정의 표시 이름(필수) |
| `New-ADUser` | `-SamAccountName` | 로그온에 쓰는 짧은 계정명 |
| `New-ADUser` | `-AccountPassword` | `SecureString`으로 감싼 초기 비밀번호 |
| `New-ADUser` | `-Enabled` | `$true`로 지정하지 않으면 기본적으로 비활성화 상태로 생성됨 |
| `New-ADUser` | `-Path` | 계정을 생성할 OU(조직 구성 단위)의 DN |
| `Set-ADUser` | `-Identity` | 수정할 대상 계정(DN·GUID·SID·SAM 계정명) |
| `Set-ADUser` | `-Replace`/`-Add`/`-Clear` | 스키마에 정의된 임의 속성을 갱신·추가·삭제 |
| `Set-ADUser` | `-ChangePasswordAtLogon` | 다음 로그온 시 비밀번호 변경 강제 |

## 예시

```powershell
$pw = ConvertTo-SecureString "TempP@ssw0rd!" -AsPlainText -Force              # 100장 방식으로 SecureString 생성

New-ADUser -Name "David Chew" -SamAccountName "dchew" `
    -UserPrincipalName "dchew@fabrikam.com" `
    -Path "OU=Sales,DC=FABRIKAM,DC=COM" `
    -AccountPassword $pw -Enabled $true -ChangePasswordAtLogon $true            # 신규 계정 생성 + 첫 로그온 시 비밀번호 변경 강제

Set-ADUser -Identity dchew -Title "Sales Manager" -Department "Sales"          # 부서·직함 갱신

Set-ADUser -Identity dchew -EmailAddress "dchew@fabrikam.com"                  # 이메일 주소 추가

Get-ADUser -Filter "Department -eq 'Sales'" | Set-ADUser -Office "Building 3"  # 115장 조회 결과를 파이프라인으로 넘겨 일괄 수정(89장 파이프라인 패턴 재사용)

Set-ADUser -Identity dchew -Enabled $false                                     # 퇴사 처리 시 계정 비활성화(삭제보다 안전한 첫 단계)
```

## 주의사항·함정

**`-Enabled` 없이 `New-ADUser`를 실행하면 계정이 기본적으로 비활성화 상태로 생성된다**: 도메인의 비밀번호 정책을 만족하는 `-AccountPassword`를 지정하지 않았거나 `-Enabled $true`를 빠뜨리면, 계정은 만들어지지만 로그온이 되지 않는다. "계정을 만들었는데 로그인이 안 된다"는 문제의 상당수가 이 두 매개변수 중 하나를 놓친 경우다.

**`-AccountPassword`는 반드시 `SecureString`이어야 하며 평문 문자열을 직접 넘길 수 없다**: 100장에서 다룬 `ConvertTo-SecureString -AsPlainText -Force` 패턴이 여기서 실전으로 쓰인다. 스크립트에 비밀번호를 하드코딩하면 그 스크립트 파일 자체가 자격 증명 유출 경로가 되므로, 실제 운영 스크립트에서는 비밀번호를 안전한 별도 저장소(104장의 `SecretManagement`)에서 가져오는 방식을 우선 고려해야 한다.

**`Set-ADUser`는 스키마에 정의된 속성 이름을 정확히 알아야 쓸 수 있다**: `Department`, `Title`처럼 자주 쓰는 속성은 전용 매개변수로 노출돼 있지만, 그 외의 속성은 `-Replace @{ extensionAttribute1 = "값" }`처럼 해시테이블로 직접 지정해야 한다. 어떤 속성이 전용 매개변수로 노출돼 있는지는 `Get-Help Set-ADUser -Full`로 확인하는 것이 가장 정확하다.

**계정을 완전히 삭제하는 `Remove-ADUser`와 비활성화만 하는 `Set-ADUser -Enabled $false`를 혼동하면 되돌릴 수 없는 실수로 이어진다**: 퇴사자 계정 처리처럼 나중에 감사·복구가 필요할 수 있는 상황에서는 삭제보다 비활성화를 우선 적용하고, 보존 기간이 지난 뒤에야 삭제를 고려하는 것이 안전한 절차다. AD 계정 삭제는 CMD·Bash의 `rm`처럼 휴지통이 없는 영구 삭제에 가깝다.

**이식성**: Linux 환경의 사용자 계정 관리는 `useradd`/`usermod` 명령이 로컬 `/etc/passwd`만을 대상으로 하는 반면, `New-ADUser`/`Set-ADUser`는 도메인 전체에 걸친 중앙 집중식 디렉터리를 대상으로 한다. LDAP 기반의 중앙 인증을 쓰는 Linux 환경(FreeIPA, OpenLDAP)에서는 `ldapadd`/`ldapmodify`가 개념적으로 대응하지만, AD만큼 GUI·GPO와 깊이 통합된 생태계는 아니다.

## Reference

- [New-ADUser (ActiveDirectory) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-aduser?view=windowsserver2025-ps)
- [Set-ADUser (ActiveDirectory) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-aduser?view=windowsserver2025-ps)
