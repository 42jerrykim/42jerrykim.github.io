---
draft: true
collection_order: 39
slug: test-path-command-check-path-powershell
title: "[PowerShell] 39. Test-Path — 경로 존재 확인"
date: 2026-08-29
lastmod: 2026-08-29
description: "Test-Path로 경로 존재 여부를 확인하는 법과 -PathType으로 파일/디렉터리를 구분하는 법, -IsValid로 문법만 검사하는 법, $null·빈 문자열 입력 시 반환값 차이, 레지스트리 값 확인의 함정을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- File-System
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
- Test-Path
- Boolean
- Registry
- Validation
- Copy-Item
- Error-Handling
image: "wordcloud.png"
---

## 개요

`Test-Path`는 경로가 실제로 존재하는지, 또는 경로 문법 자체가 유효한지를 `Boolean`으로 알려주는 cmdlet이다. 34장에서 언급했듯 `Copy-Item` 같은 명령을 실행하기 전 대상이 이미 있는지, 컨테이너인지 미리 확인하는 안전장치로 자주 쓰인다.

## 사용법

```powershell
Test-Path [-Path] <String[]> [-PathType <TestPathType>] [-IsValid] [-Filter <String>] [-Include <String[]>] [-Exclude <String[]>]
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Path` | 확인할 경로. 모든 구성 요소가 존재해야 `$true` |
| `-PathType`(별칭 `-Type`) | `Leaf`(파일 등 자식이 없는 항목), `Container`(디렉터리·레지스트리 키 등), `Any`(둘 중 하나) |
| `-IsValid` | 실제 존재 여부가 아니라 경로 **문법**이 유효한지만 검사(대상이 없어도 `$true`일 수 있음) |
| `-NewerThan` / `-OlderThan`(FileSystem 동적 매개변수, PowerShell 7.5+에서 기능 확장) | 지정한 날짜 기준으로 파일·디렉터리의 최신/오래됨 여부 확인 |
| `-Filter` / `-Include` / `-Exclude` | 31장과 같은 규칙 |

## 예시

```powershell
Test-Path -Path "C:\Documents and Settings\DavidC"     # 전체 경로 존재 확인
Test-Path -Path $PROFILE                                 # 프로파일 파일이 실제 있는지(06장)
Test-Path -Path $PROFILE -IsValid                         # 경로 문법만 확인(파일이 없어도 True 가능)
Test-Path -Path $PROFILE -PathType Leaf                   # 파일(비컨테이너)인지 확인
Test-Path -Path "C:\CAD\Buildings\*" -Exclude *.dwg        # 특정 확장자 외 파일이 있는지

Test-Path -Path "HKLM:\Software\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell"   # 레지스트리 키는 확인 가능
Test-Path -Path "...\Microsoft.PowerShell\ExecutionPolicy" # 레지스트리 "값"은 늘 False(주의사항 참고)

Get-Command pwsh | Select-Object -ExpandProperty Path |
    Test-Path -NewerThan "July 13, 2009" -OlderThan (Get-Date).AddDays(-7)

Test-Path -IsValid Z:\abc.txt                # 존재하지 않는 드라이브면 False
Test-Path -IsValid FileSystem::Z:\abc.txt    # 프로바이더 이름을 붙이면 드라이브 문제를 우회
```

## 주의사항·함정

**레지스트리 "값"에는 `Test-Path`가 항상 `False`를 반환한다**: `Test-Path`는 레지스트리 **키**(컨테이너)의 존재는 정확히 확인하지만, 38장에서 다룬 레지스트리 **값**(Item Property)의 존재는 확인하지 못하고 값이 실제로 있어도 `False`를 준다. 값의 존재를 확인하려면 `Get-ItemProperty`로 조회를 시도하고 예외나 `$null` 여부로 판단해야 한다. 공식 문서도 이 동작을 명시적으로 "모든 프로바이더에서 올바르게 동작하지는 않는다"고 경고한다.

**빈 문자열과 공백 문자열, `$null`은 서로 다르게 처리된다**: 공백만 있는 문자열(`' '`)이나 빈 문자열(`''`)을 넘기면 `$false`를 반환하지만, `$null`이나 빈 배열을 넘기면 비종료 오류가 난다(`-ErrorAction SilentlyContinue`로 억제 가능). 사용자 입력을 그대로 `Test-Path`에 넘기는 스크립트라면 이 세 가지 입력이 각각 다르게 처리된다는 점을 감안해야 한다.

**`-IsValid`와 `-PathType`을 함께 쓰면 `-PathType`이 무시될 수 있다**: PowerShell 6.1.2까지는 두 매개변수를 같이 쓰면 `-PathType`이 조용히 무시되고 문법 검사만 수행된다(알려진 이슈). 정확한 동작이 필요하면 두 검사를 별도의 `Test-Path` 호출로 나누는 편이 안전하다.

**이식성**: CMD의 `if exist`, Bash의 `[ -e ]`/`[ -f ]`/`[ -d ]`에 각각 `Test-Path`, `-PathType Leaf`, `-PathType Container`가 대응한다. 다만 PowerShell은 파일 시스템뿐 아니라 레지스트리 키 같은 다른 프로바이더 경로에도 같은 검사를 적용할 수 있다는 점이 더 넓다.

## Reference

- [Test-Path (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-path)
