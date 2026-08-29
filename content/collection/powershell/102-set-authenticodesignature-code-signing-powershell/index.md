---
draft: true
collection_order: 102
slug: set-authenticodesignature-code-signing-powershell
title: "[PowerShell] 102. Set-AuthenticodeSignature — 스크립트 코드 서명"
date: 2026-08-29
lastmod: 2026-08-29
description: "Set-AuthenticodeSignature로 PowerShell 스크립트에 디지털 서명을 추가하는 법과 코드 서명 인증서를 Cert: 드라이브에서 찾는 법, 05장 AllSigned 실행 정책과의 관계, Get-AuthenticodeSignature로 서명을 검증하는 법을 정리한 챕터다."
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
- Set-AuthenticodeSignature
- Code-Signing
- Certificate
- AllSigned
- Digital-Signature
- Script-Trust
image: "wordcloud.png"
---

## 개요

`Set-AuthenticodeSignature`는 PowerShell 스크립트 파일에 디지털 서명을 추가하는 cmdlet이다. 05장에서 언급했던 실행 정책 값 중 `AllSigned`가 바로 이 서명이 없는 스크립트를 실행하지 못하게 막는 정책이다 — 이 장은 그 서명을 실제로 만드는 법을 다루며, "신뢰할 수 있는 코드만 실행한다"는 원칙을 정책 설정 차원을 넘어 코드 자체의 증명으로 구현한다.

정신 모델은 "서명은 스크립트 끝에 '이 코드는 특정 인증서 소유자가 만들었고, 서명 이후 한 글자도 바뀌지 않았다'는 것을 증명하는 봉인 스탬프를 찍는 것"이라는 것이다. 파일 내용이 조금이라도 바뀌면 그 서명은 무효가 된다.

## 사용법

```powershell
$cert = Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert
Set-AuthenticodeSignature -FilePath <스크립트경로> -Certificate $cert
```

## 종류

| 요소 | 설명 |
|---|---|
| `Cert:` 드라이브 | 30장의 프로바이더 개념으로 인증서 저장소를 탐색(`-CodeSigningCert`로 코드 서명 인증서만 필터) |
| `Get-PfxCertificate` | `.pfx` 파일에서 인증서 로드(저장소에 등록 안 된 인증서 사용 시) |
| `-IncludeChain` | 서명에 포함할 인증서 체인 범위(`Signer`/`NotRoot`/`All`) |
| `-TimestampServer` | 타임스탬프 서버 지정 — 인증서가 나중에 만료돼도 서명 당시 유효했음을 증명 |
| `Get-AuthenticodeSignature` | 서명 상태 검증(`Valid`/`NotSigned`/`HashMismatch` 등) |

## 예시

```powershell
$cert = Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert   # 저장소에서 코드 서명 인증서 찾기
Set-AuthenticodeSignature -FilePath .\PsTestInternet2.ps1 -Certificate $cert

$cert = Get-PfxCertificate -FilePath C:\Test\Mysign.pfx                # PFX 파일에서 인증서 로드
Set-AuthenticodeSignature -FilePath .\ServerProps.ps1 -Certificate $cert

$signingParameters = @{
    FilePath        = 'C:\scripts\Remodel.ps1'
    Certificate     = $cert
    HashAlgorithm   = 'SHA256'
    IncludeChain    = 'All'
    TimestampServer = 'http://timestamp.fabrikam.com/scripts/timstamper.dll'
}
Set-AuthenticodeSignature @signingParameters                             # 25장 스플래팅, 타임스탬프 포함 서명

Get-AuthenticodeSignature -FilePath .\Remodel.ps1                          # 서명 상태 확인
(Get-AuthenticodeSignature -FilePath .\Remodel.ps1).Status                   # Valid / NotSigned / HashMismatch 등

Get-ChildItem -Path .\Scripts -Filter *.ps1 -Recurse |                       # 여러 스크립트 일괄 서명
    ForEach-Object { Set-AuthenticodeSignature -FilePath $_.FullName -Certificate $cert }
```

## 주의사항·함정

**서명 후 파일을 한 글자라도 수정하면 서명이 무효화된다**: 스크립트 내용이 바뀌면 원래 서명의 해시값과 실제 파일 해시값이 달라져 `Get-AuthenticodeSignature`가 `HashMismatch` 상태를 반환한다. 서명된 스크립트를 수정해야 한다면, 수정 후 반드시 다시 서명해야 한다 — 텍스트 편집기의 줄바꿈 문자 변환(CRLF↔LF)처럼 눈에 안 보이는 변경도 서명을 깨뜨릴 수 있다.

**타임스탬프 없이 서명하면 인증서 만료 후 그 서명이 무효로 취급될 수 있다**: `-TimestampServer` 없이 서명한 스크립트는, 서명에 쓰인 인증서가 만료되면 서명 자체도 유효하지 않은 것으로 판정될 위험이 있다. 장기간 배포·유지보수할 스크립트라면 타임스탬프 서버를 반드시 지정해 "이 서명은 인증서가 유효했던 시점에 이뤄졌다"는 증거를 남겨야 한다.

**`-Force`를 써도 읽기 전용 파일에는 서명을 추가할 수 있지만 보안 제한 자체는 우회할 수 없다**: 파일 시스템 권한(101장에서 다룬 ACL)이 애초에 쓰기를 막고 있다면 `-Force`로도 서명을 추가할 수 없다.

**코드 서명 인증서 자체를 얻는 과정은 이 cmdlet의 범위 밖이다**: 조직 내부 PKI(사설 인증기관)에서 발급받거나, 공인 인증기관(CA)에서 구매해야 한다 — 자체 서명(self-signed) 인증서로 테스트는 할 수 있지만, 다른 컴퓨터가 그 인증서를 신뢰하려면 별도로 신뢰할 수 있는 루트로 등록해야 한다.

**이식성**: Linux/macOS의 GPG 서명이나 코드 서명 개념과 목적은 비슷하지만, PowerShell의 Authenticode는 Windows 인증서 저장소(`Cert:` 드라이브)와 밀접하게 통합돼 있어 플랫폼 간 서명 검증 메커니즘이 직접 호환되지는 않는다. CMD에는 스크립트 서명이라는 개념 자체가 없다 — 배치 파일은 서명 여부와 무관하게 항상 실행된다는 점이 PowerShell의 실행 정책·서명 체계와 근본적으로 다른 보안 모델이다.

## Reference

- [Set-AuthenticodeSignature (Microsoft.PowerShell.Security) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-authenticodesignature)
