---
draft: true
collection_order: 101
slug: get-set-acl-access-control-powershell
title: "[PowerShell] 101. Get-Acl/Set-Acl — 접근 제어 목록"
date: 2026-08-29
lastmod: 2026-08-29
description: "Get-Acl로 파일·레지스트리 키의 보안 설명자(security descriptor)를 조회하는 법과 Set-Acl로 권한을 복사·수정하는 전형적인 흐름, Access 속성으로 개별 권한 항목을 다루는 법을 정리한 챕터다."
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
- Get-Acl
- Set-Acl
- Access-Control-List
- Security-Descriptor
- Permission
- File-Permission
image: "wordcloud.png"
---

## 개요

`Get-Acl`/`Set-Acl`은 파일·디렉터리·레지스트리 키 같은 리소스의 <strong>접근 제어 목록(ACL)</strong>을 조회·수정하는 cmdlet이다. 30장에서 배운 프로바이더 개념이 여기서도 그대로 적용된다 — `Get-Acl`은 FileSystem과 Registry 두 프로바이더가 공통으로 지원하며, "어떤 사용자가 이 리소스에 어떤 권한을 갖는가"를 파일이든 레지스트리 키든 같은 인터페이스로 다룬다.

정신 모델은 "보안 설명자(security descriptor)는 리소스의 소유자·권한 목록을 담은 꼬리표이고, `Get-Acl`은 그 꼬리표를 읽어 오는 것, `Set-Acl`은 (대개 다른 리소스에서 읽어 온) 꼬리표를 다시 붙이는 것"이라는 것이다. 실제로 개별 권한을 세밀하게 바꾸려면, 읽어 온 객체의 `.SetAccessRule()` 같은 메서드를 먼저 호출한 뒤 `Set-Acl`로 저장하는 두 단계를 거친다.

## 사용법

```powershell
Get-Acl -Path <경로> [-Audit]
(Get-Acl -Path <경로)).SetAccessRule($규칙객체)
Set-Acl -Path <경로> -AclObject <ACL객체>
```

## 종류

| 요소 | 설명 |
|---|---|
| `Access` 속성 | 임의 접근 제어 목록(DACL)의 개별 항목들 — 누가 무엇을 허용/거부받는지 |
| `Owner` 속성 | 리소스 소유자 |
| `Sddl` 속성 | 보안 설명자 전체를 문자열 하나(SDDL)로 표현 — 저장·전달·파싱에 유용 |
| `-Audit` | SACL(감사 목록)까지 함께 조회 — 접근 시도가 언제 로그로 남는지 |
| `System.Security.AccessControl.*AccessRule` | `.SetAccessRule()`에 넘길 새 권한 규칙을 만드는 .NET 타입 |

## 예시

```powershell
Get-Acl C:\Windows                                        # 디렉터리의 보안 설명자
Get-Acl C:\Windows\s*.log | Format-List PSPath, Sddl          # 여러 파일의 SDDL 문자열만 확인

Get-Acl -Path HKLM:\System\CurrentControlSet\Control | Format-List   # 40장에서 다룬 레지스트리 키에도 동일하게 적용

Get-Acl C:\Windows\s*.log -Audit |                            # SACL(감사 항목) 개수 확인
    ForEach-Object { $_.Audit.Count }

# 한 폴더의 권한을 다른 폴더로 복사하는 전형적인 흐름
$Acl = Get-Acl -Path "C:\SourceFolder"
Set-Acl -Path "C:\DestFolder" -AclObject $Acl

# 새 권한 규칙을 추가한 뒤 다시 적용
$Acl = Get-Acl -Path "C:\SharedFolder"
$Rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "CONTOSO\jsmith", "FullControl", "Allow")
$Acl.SetAccessRule($Rule)
$Acl | Set-Acl -Path "C:\SharedFolder"                          # 파이프라인으로 곧바로 적용

Get-Acl -InputObject (Get-StorageSubSystem -Name S087)             # 경로 없는 객체의 ACL(96장 스토리지 모듈과 조합)
```

## 주의사항·함정

**`Get-Acl`이 반환한 객체를 수정하지 않고 그냥 `Set-Acl`에 다시 넘기면 원본과 다를 게 없다**: 이 두 cmdlet 자체는 "읽기"와 "쓰기"만 담당할 뿐, 권한을 실제로 바꾸는 것은 그 객체의 `.SetAccessRule()`/`.RemoveAccessRule()`/`.AddAccessRule()` 같은 .NET 메서드다. `Get-Acl`만으로 권한을 바꿀 수 있다고 오해하면 아무 변화 없는 코드를 짜게 된다.

**Windows 전용이며, 파일 시스템·레지스트리 프로바이더에서만 동작한다**: `Get-Acl`은 macOS·Linux에서 지원되지 않고, Windows 안에서도 이 두 프로바이더 외의 경로(예: 환경 변수 `Env:`)에는 적용되지 않는다.

**`Set-Acl`로 잘못된 권한을 적용하면 자기 자신도 그 리소스에 접근하지 못하게 될 수 있다**: 관리자 그룹의 접근 권한을 실수로 제거하는 등 되돌리기 어려운 권한 오류를 만들 수 있으므로, 프로덕션 리소스에 적용하기 전에는 반드시 원본 ACL을 `.Sddl` 속성으로 백업해 두거나 테스트 환경에서 먼저 검증해야 한다 — 이는 65장에서 강조한 "되돌리기 어려운 작업은 신중하게"라는 원칙이 파일 권한에도 그대로 적용되는 사례다.

**상속된 권한은 `Access` 속성만 봐서는 그 리소스에 직접 설정된 것인지 부모에서 물려받은 것인지 구분하기 어렵다**: 각 접근 규칙의 `IsInherited` 속성을 확인해야 "이 폴더에 직접 설정한 권한"과 "상위 폴더에서 내려온 권한"을 구분할 수 있다. 이 구분을 놓치면 권한 감사 스크립트가 실제보다 훨씬 많은(또는 적은) 권한이 설정된 것으로 잘못 보고할 수 있다.

**이식성**: Linux의 `chmod`/`chown`(기본 권한), `getfacl`/`setfacl`(확장 ACL)이 개념적으로 대응하지만, Windows ACL은 사용자·그룹별로 훨씬 세분화된 권한(읽기/쓰기/실행/삭제/권한변경 등)을 지원한다는 점에서 POSIX 권한 모델보다 풍부하다. CMD의 `icacls`도 같은 ACL을 다루지만 텍스트 기반 명령줄 문법이라 PowerShell처럼 객체를 프로그래밍적으로 조합하기는 어렵다.

## Reference

- [Get-Acl (Microsoft.PowerShell.Security) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-acl)
