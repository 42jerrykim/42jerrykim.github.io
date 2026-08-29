---
draft: true
collection_order: 104
slug: secretmanagement-module-powershell
title: "[PowerShell] 104. Microsoft.PowerShell.SecretManagement"
date: 2026-08-29
lastmod: 2026-08-29
description: "SecretManagement 모듈이 여러 비밀 저장소(Vault)를 하나의 Get-Secret/Set-Secret 인터페이스로 추상화하는 원리와 SecretStore 확장 모듈로 로컬 저장소를 쓰는 법, 100장 Get-Credential의 한계를 이 모듈이 어떻게 보완하는지 정리한 챕터다."
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
- SecretManagement
- SecretStore
- Vault
- Secret-Storage
- Credential-Management
- API-Key
image: "wordcloud.png"
---

## 개요

**SecretManagement** 모듈은 여러 비밀 저장소(Vault)를 `Get-Secret`/`Set-Secret`이라는 하나의 통일된 cmdlet 인터페이스로 추상화한다. 100장에서 배운 `Get-Credential`이 매번 사람이 직접 입력해야 하는 대화형 도구였다면, 이 장은 자격 증명·API 키 같은 비밀을 미리 안전하게 저장해 두고 스크립트가 필요할 때마다 꺼내 쓰는 법을 다루며 Part 14(보안과 자격 증명)를 마무리로 향해 간다.

정신 모델은 "SecretManagement는 여러 금고(Vault) 브랜드 앞에 놓인 공통 열쇠구멍"이라는 것이다 — 로컬 파일 기반 금고(SecretStore), Azure Key Vault, KeePass 등 저장소 종류는 다양하지만, 스크립트는 항상 같은 `Get-Secret` 명령으로 비밀을 꺼내므로 실제 저장소를 바꿔도 스크립트 코드는 그대로 유지된다.

## 사용법

```powershell
Register-SecretVault -Name <저장소이름> -ModuleName <확장모듈이름>
Set-Secret -Name <비밀이름> -Secret <값>
Get-Secret -Name <비밀이름>
```

## 종류

| 개념 | 설명 |
|---|---|
| **Vault**(저장소) | 실제로 비밀을 보관하는 백엔드 — 로컬 암호화 파일, 클라우드 서비스, 서드파티 비밀번호 관리자 등 |
| **확장 Vault(Extension Vault)** | SecretManagement와 특정 저장소를 연결하는 PowerShell 모듈(예: `Microsoft.PowerShell.SecretStore`) |
| `Register-SecretVault` | 사용할 저장소를 세션에 등록 |
| `Set-Secret`/`Get-Secret`/`Remove-Secret` | 저장소 종류와 무관하게 항상 동일한 사용법 |
| `-Vault` 매개변수 | 여러 저장소를 등록했을 때 특정 저장소를 지정 |

## 예시

```powershell
Install-Module -Name Microsoft.PowerShell.SecretManagement -Scope CurrentUser   # 76장에서 배운 방식
Install-Module -Name Microsoft.PowerShell.SecretStore -Scope CurrentUser          # 로컬 저장소 확장 모듈

Register-SecretVault -Name LocalVault -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault

Set-Secret -Name "MyApiKey" -Secret "sk-1234567890abcdef"       # 비밀 저장(최초 1회, 마스터 암호 설정 프롬프트)
Set-Secret -Name "DbCredential" -Secret (Get-Credential)           # 100장의 PSCredential도 그대로 저장 가능

$apiKey = Get-Secret -Name "MyApiKey" -AsPlainText                 # 스크립트에서 평문으로 꺼내 쓰기
$dbCred = Get-Secret -Name "DbCredential"                            # PSCredential 객체 그대로 복원

Get-SecretInfo                                                         # 저장된 비밀 이름·메타데이터 목록(값은 안 보임)
Remove-Secret -Name "MyApiKey"                                          # 삭제

# 여러 조직 구성원이 같은 스크립트를 쓰되, 각자 다른 저장소 이름만 등록해도 스크립트는 그대로
Get-Secret -Name "MyApiKey" -Vault "TeamAzureVault"
```

## 주의사항·함정

**이 모듈군은 더 이상 적극적으로 개발되지 않는다**: Microsoft PowerShell 팀은 SecretManagement/SecretStore가 "기능적으로 완성됐다"고 판단해 신규 기능 개발을 중단했고, 보안·심각한 버그 수정만 지원한다고 공식적으로 밝혔다 — 코드 저장소 자체도 보관(archive) 처리됐다. 패스키·SSO·연합 인증 같은 비밀번호 없는 인증 방식이 대세가 되는 흐름 속에서, 새 프로젝트를 설계한다면 이 모듈이 여전히 적합한 선택인지 조직의 인증 전략과 함께 재검토할 필요가 있다.

**SecretManagement 자체는 저장소가 아니라 추상화 계층일 뿐이다**: `Register-SecretVault`로 실제 확장 Vault 모듈을 등록하기 전까지는 이 모듈만으로는 아무 비밀도 저장할 수 없다. "설치했는데 왜 동작 안 하지?"라는 흔한 혼란은 대개 확장 Vault 모듈을 별도로 설치·등록하지 않았기 때문이다.

**각 확장 Vault는 자체 인증 방식을 요구할 수 있다**: SecretManagement 자체는 인증 요구사항을 강제하지 않으므로, 로컬 `SecretStore`는 마스터 암호를, Azure Key Vault 확장은 Azure 계정 인증을, 다른 확장은 또 다른 방식을 요구할 수 있다 — 저장소를 바꾸면 `Get-Secret` 호출 코드는 그대로여도 최초 설정·인증 절차는 다시 준비해야 한다.

**Microsoft가 공식 유지보수하지 않는 커뮤니티 확장 Vault는 신뢰 검토가 필요하다**: PowerShell Gallery에서 `SecretManagement` 태그로 검색되는 확장(KeePass, LastPass 연동 등)은 대부분 커뮤니티가 개발한 것이라, 76장에서 강조한 "설치 전 코드를 검토하라"는 원칙이 여기서는 특히 중요하다 — 비밀을 다루는 코드이기 때문이다.

**이식성**: `pass`(Unix 비밀번호 관리자), HashiCorp Vault CLI가 "여러 프로그램이 하나의 인터페이스로 비밀을 공유한다"는 목적을 공유한다. SecretManagement의 확장 Vault 모델은 특히 HashiCorp Vault의 플러그인 아키텍처와 유사한 설계 철학을 보인다 — 백엔드는 다양하지만 클라이언트 인터페이스는 통일한다는 점에서다.

## Reference

- [Overview of the SecretManagement and SecretStore modules - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/overview)
