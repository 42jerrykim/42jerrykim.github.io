---
draft: true
collection_order: 100
slug: get-credential-pscredential-object-powershell
title: "[PowerShell] 100. Get-Credential과 PSCredential 객체"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Credential로 사용자 이름·비밀번호를 SecureString으로 안전하게 담는 PSCredential 객체를 만드는 법과 -Credential 매개변수를 지원하는 cmdlet과의 관계, 자격 증명을 평문으로 스크립트에 남기지 말아야 하는 이유를 정리한 Part 14 시작 챕터다."
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
- Get-Credential
- PSCredential
- SecureString
- Authentication
- Credential-Object
- Password-Security
image: "wordcloud.png"
---

## 개요

`Get-Credential`은 사용자 이름과 비밀번호를 안전하게 담는 **PSCredential** 객체를 만드는 cmdlet이다. 84–86장에서 원격 세션에 `-Credential` 매개변수로 다른 계정을 지정할 때, 90장에서 `Start-Process -Credential`로 다른 사용자 권한으로 프로그램을 실행할 때 이미 이 객체를 스치듯 사용했다 — 이 장은 그 `PSCredential` 자체를 정식으로 다루며 Part 14(보안과 자격 증명)를 시작한다.

정신 모델은 "PSCredential은 사용자 이름(평문 문자열)과 비밀번호(**SecureString**, 암호화된 형태로 메모리에 보관되는 문자열)를 짝지은 봉투"라는 것이다. 41장에서 배운 일반 변수와 달리, 이 봉투 안의 비밀번호는 화면에 출력해도 실제 값이 아니라 `System.Security.SecureString` 타입 이름만 보인다.

## 사용법

```powershell
$cred = Get-Credential [[-Credential] <사용자이름>] [-Message <안내문구>]
```

## 종류

| 구성 요소 | 설명 |
|---|---|
| `UserName` 속성 | 평문 문자열 |
| `Password` 속성 | `SecureString` — 직접 출력해도 값이 노출되지 않음 |
| `GetNetworkCredential()` 메서드 | `.NET`의 `NetworkCredential`로 변환, 평문 비밀번호가 필요한 API에 넘길 때 사용 |
| `-Message`/`-Title` | 스크립트·함수 안에서 사용자에게 왜 자격 증명이 필요한지 설명하는 문구(PowerShell 3.0+) |
| `New-Object PSCredential` | `Get-Credential` 없이 직접 조립(자동화된 스크립트에서 자주 사용) |

## 예시

```powershell
$cred = Get-Credential                                  # 사용자 이름·비밀번호 모두 프롬프트
$cred = Get-Credential -Credential "User01"                # 사용자 이름 미리 지정, 비밀번호만 프롬프트
$cred.UserName                                                # 평문으로 조회 가능
$cred.Password                                                  # SecureString — 실제 값은 안 보임

$credentialParams = @{
    Message  = "\\Server1\Scripts 공유에 접근하려면 자격 증명이 필요합니다."
    UserName = "Server01\PowerUser"
}
Get-Credential @credentialParams                                  # 25장 스플래팅과 결합, 안내 문구 포함

# 자동화 스크립트에서 프롬프트 없이 자격 증명 객체를 직접 조립
$User = "Domain01\User01"
$PWord = Read-Host -Prompt '비밀번호 입력' -AsSecureString
$Credential = New-Object System.Management.Automation.PSCredential -ArgumentList $User, $PWord

# 원격 세션·프로세스 실행에 재사용(84–86장, 90장에서 이미 등장한 패턴)
Enter-PSSession -ComputerName Server01 -Credential $cred
Start-Process -FilePath "notepad" -Credential $cred

$networkCred = $cred.GetNetworkCredential()               # 평문 비밀번호가 필요한 레거시 API용
```

## 주의사항·함정

**모든 프로바이더·cmdlet이 `-Credential`을 지원하는 것은 아니다**: PowerShell에 내장된 파일 시스템 프로바이더 같은 일부는 `-Credential` 매개변수 자체가 없다 — `Copy-Item -Credential`처럼 지원하지 않는 곳에 억지로 시도하면 오류가 나거나 매개변수가 무시된다. 특정 cmdlet이 이 매개변수를 지원하는지는 `Get-Help <cmdlet이름> -Full`로 미리 확인해야 한다.

**비밀번호를 스크립트 파일에 평문 문자열로 남기면 SecureString의 보호 의미가 사라진다**: `$PWord = ConvertTo-SecureString "실제비밀번호" -AsPlainText -Force`처럼 평문을 코드에 하드코딩하면, 그 스크립트 파일 자체가 비밀번호 유출 지점이 된다. 자동화 시나리오에서 사람이 매번 입력할 수 없다면, 이 장의 방식 대신 104장에서 다룰 `SecretManagement` 모듈로 별도 저장소에 안전하게 보관해야 한다.

**`SecureString`은 메모리 보호일 뿐, 전송 구간 암호화를 보장하지 않는다**: `SecureString`은 로컬 메모리에서 값을 평문으로 노출하지 않도록 보호하는 것이 목적이며, 그 자격 증명이 네트워크로 전송될 때의 암호화는 별개의 문제다(83장에서 다룬 WinRM의 인증 메커니즘이 이 부분을 담당한다). "SecureString을 쓰니까 무조건 안전하다"고 오해하면 안 된다.

**원격 컴퓨터에서 `Get-Credential`을 호출하면 보안 경고 메시지가 함께 표시된다**: 85장의 `Invoke-Command`로 원격 세션 안에서 `Get-Credential`을 실행하면, "이 요청은 원격 컴퓨터의 스크립트나 애플리케이션이 하는 것이니 신뢰할 때만 입력하라"는 경고가 함께 뜬다. 이는 피싱성 자격 증명 요청을 사용자가 인지하도록 만든 의도적인 보안 장치다.

**이식성**: Bash의 `read -s`(입력을 화면에 표시하지 않고 읽기)가 부분적으로 유사하지만, 결과가 단순 문자열이라 `SecureString` 같은 메모리 보호 계층은 없다. `.NET`의 `SecureString`은 Windows 자격 증명 관리자(Credential Manager)와도 연동되며, 이는 PowerShell이 .NET 생태계 위에 구축됐다는 이 컬렉션의 근본 주제(1장)가 보안 영역에서 드러나는 사례다.

## Reference

- [Get-Credential (Microsoft.PowerShell.Security) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-credential)
