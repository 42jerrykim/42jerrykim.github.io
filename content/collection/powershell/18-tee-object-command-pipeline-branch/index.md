---
draft: true
collection_order: 18
slug: tee-object-command-pipeline-branch-powershell
title: "[PowerShell] 18. Tee-Object — 파이프라인 분기"
date: 2026-08-29
lastmod: 2026-08-29
description: "Tee-Object로 파이프라인 결과를 파일이나 변수에 저장하면서 동시에 다음 명령으로 흘려보내는 법과 -FilePath/-Variable 매개변수, Out-File·리다이렉션 연산자와 근본적으로 다른 지점을 정리한 챕터다."
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
- Tee-Object
- Redirection
- Debugging
- Logging
- Variable
- Out-File
- Backup
image: "wordcloud.png"
---

## 개요

`Tee-Object`(별칭 `tee`)는 파이프라인 결과를 파일이나 변수에 저장하면서, 동시에 그 결과를 그대로 다음 명령으로 계속 흘려보내는 cmdlet이다. 이름과 동작 모두 Unix `tee`(수도관을 T자로 분기한다는 뜻)를 그대로 계승했다. `Out-File`이나 `>` 리다이렉션이 파이프라인을 그 자리에서 끝내고 파일에만 저장하는 것과 달리, `Tee-Object`는 저장과 동시에 파이프라인을 계속 이어간다는 점이 다르다.

정신 모델은 "관측하고 싶은 중간 지점에 분기점을 꽂아 두는 것"이다. 디버깅 중인 긴 파이프라인의 중간 결과를 파일로 남기거나 변수에 담아 두고 싶을 때, 파이프라인 자체를 두 번 실행할 필요 없이 `Tee-Object` 한 줄만 끼워 넣으면 된다.

## 사용법

```powershell
<파이프라인> | Tee-Object [-FilePath] <String> [-Append] [-Encoding <Encoding>]
<파이프라인> | Tee-Object -Variable <String>
<파이프라인> | Tee-Object -LiteralPath <String>
```

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-FilePath` | 결과를 저장할 파일 경로(와일드카드는 단일 파일로 귀결되어야 함) |
| `-LiteralPath` | 와일드카드를 문자 그대로 취급하는 경로(파일명에 `*`, `[]` 등이 실제로 포함된 경우) |
| `-Variable` | 결과를 저장할 변수 이름(`$` 기호 없이 지정) |
| `-Append` | 기존 파일 내용에 이어 붙인다(기본은 덮어쓰기, 경고 없음) |
| `-Encoding` | 저장할 파일의 인코딩(PowerShell 6+ 기본값은 BOM 없는 UTF-8) |

## 예시

```powershell
Get-Process | Tee-Object -FilePath "C:\Test\proc.txt"                # 파일 저장 + 화면 출력
Get-Process notepad | Tee-Object -Variable proc | Select-Object ProcessName, Handles
Get-ChildItem -Path D: -Recurse -System |
    Tee-Object -FilePath "C:\test\AllSystemFiles.txt" -Append |
    Out-File C:\test\NewSystemFiles.txt

# Windows에서 콘솔 디바이스로 중간 결과를 확인하며 계속 필터링
Get-ChildItem -Path .\About |
    Tee-Object -FilePath '\\.\CON' |
    Where-Object { (Get-Content $_ -Raw) -match '(?s)^---(?<FrontMatter>.+)---' }
```

## 주의사항·함정

**`-Append` 없이는 경고 없이 기존 파일이 지워진다**: `-FilePath`만 지정하면 기존 파일 내용을 확인 없이 덮어쓴다. 로그처럼 누적해야 하는 파일이라면 반드시 `-Append`를 함께 써야 한다.

**변수로 저장한 결과에는 파이프라인의 전체 출력 정보가 포함된다**: `-Variable proc`으로 저장한 뒤 이어지는 `Select-Object`에서 속성을 제한해도, `$proc` 변수 자체에는 원래의 전체 속성을 가진 객체가 그대로 담긴다 — `Tee-Object`는 자신의 뒤에 오는 명령이 무엇을 하든 관여하지 않고, 오직 자신을 거쳐 가는 시점의 객체를 저장할 뿐이다.

**`-WhatIf`를 직접 지원하지는 않는다**: `Tee-Object` 자체는 `-WhatIf` 매개변수가 없지만, 내부적으로 `Set-Variable`·`Out-File`을 사용하므로 `[CmdletBinding(SupportsShouldProcess)]`로 작성한 함수·스크립트 안에서 호출되면 그 상태(`-WhatIf`)를 이어받아 실제로 파일에 쓰지 않고 시뮬레이션만 한다.

**이식성**: Unix `tee`와 이름·역할이 같지만, PowerShell 버전은 파일 저장 외에 세션 변수 저장(`-Variable`)까지 지원한다는 점이 다르다. CMD에는 대응하는 명령이 없다.

## Reference

- [Tee-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/tee-object)
