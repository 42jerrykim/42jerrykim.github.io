---
draft: true
collection_order: 51
slug: out-string-out-null-command-powershell
title: "[PowerShell] 51. Out-String과 Out-Null"
date: 2026-08-29
lastmod: 2026-08-29
description: "Out-String으로 객체를 콘솔 서식 그대로 텍스트 문자열로 바꿔 Select-String 같은 텍스트 도구와 연결하는 법과 -Stream 매개변수, 명령 출력을 완전히 없애는 Out-Null 사용법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Scripting(스크립팅)
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
- Out-String
- Out-Null
- Text-Conversion
- Output-Suppression
- Stream-Parameter
- Pipeline
image: "wordcloud.png"
---

## 개요

`Out-String`과 `Out-Null`은 이름의 `Out-` 접두사가 같지만 정반대 목적을 가진 cmdlet이다. `Out-String`은 객체를 화면에 표시될 서식 그대로 **문자열로 변환**해 텍스트 도구에 넘기고, `Out-Null`은 결과를 화면에도, 파이프라인에도 남기지 않고 **완전히 삭제**한다. 10장에서 배운 객체 파이프라인 모델에서, 이 둘은 "객체 세계와 텍스트 세계의 경계"와 "출력이 필요 없을 때의 처리"를 각각 담당한다.

## 사용법

```powershell
<객체> | Out-String [-Stream] [-Width <Int32>] [-NoNewline]
<명령> | Out-Null
```

## 매개변수

| 매개변수 | 대상 | 설명 |
|---|---|---|
| `-Stream` | Out-String | 하나의 큰 문자열 대신 줄마다 별도 문자열 객체로 반환(46장 `Select-String` 등 줄 단위 도구와 연결할 때 필수) |
| `-Width` | Out-String | 서식 폭(기본은 호스트 너비, 넓혀서 잘림 방지) |
| `-NoNewline` | Out-String | 서식이 만든 줄바꿈 제거(문자열 자체에 포함된 줄바꿈은 유지) |

## 예시

```powershell
$text = Get-Culture | Select-Object -Property * | Out-String -Width 100   # 객체를 통째로 문자열 하나로

Get-Alias | Out-String -Stream | Select-String -Pattern "gcm"              # 줄 단위로 쪼개 grep처럼 검색
# -Stream 없이 Select-String에 넘기면 문자열 하나 전체에서만 찾아 원하는 결과가 안 나온다

@{ TestKey = ('x' * 200) } | Out-String                      # 기본 폭에서 잘림(...)
@{ TestKey = ('x' * 200) } | Out-String -Width 250             # 폭을 넓혀 잘림 방지

New-Item -Path C:\Temp\NewFolder -ItemType Directory | Out-Null   # 생성 결과 객체를 화면에 안 보이게
$null = New-Item -Path C:\Temp\Another -ItemType Directory         # 동일한 효과의 대안 문법

Get-Process | Out-Null                                        # 실행은 하되 출력은 완전히 버림
```

## 주의사항·함정

**`Out-String`을 거치지 않고 텍스트 도구에 객체를 바로 넘기면 원하는 결과가 안 나온다**: `Get-Process | Select-String -Pattern "chrome"`처럼 객체를 곧바로 `Select-String`에 넘기면, PowerShell이 각 객체를 문자열로 자동 변환하는 과정에서 서식이 예상과 다르게 적용돼 검색이 실패하기 쉽다. 46장에서 다룬 `Select-String`은 원래 텍스트·파일을 다루는 cmdlet이므로, 객체 결과를 검색하려면 먼저 `Out-String -Stream`으로 명시적으로 줄 단위 텍스트로 바꿔야 한다.

**`-Stream` 없이는 여러 줄이 하나의 문자열로 뭉쳐져 줄 단위 처리가 안 된다**: `Out-String`의 기본 동작은 전체 출력을 개행 문자가 포함된 문자열 **하나**로 반환하는 것이다. `Select-String`처럼 "줄마다" 처리하는 cmdlet과 연결하려면 반드시 `-Stream`을 붙여야 한다 — 빠뜨리면 오류는 나지 않지만 검색이 항상 "모두 일치" 또는 "전혀 일치 안 함"처럼 부자연스럽게 동작한다.

**`Out-Null`과 `$null = ...`는 결과는 같지만 성능 특성이 다르다**: 둘 다 출력을 없애는 데 쓰이지만, `Out-Null`은 파이프라인을 통해 객체를 흘려보내는 반면 `$null = ...`는 대입 연산만으로 처리되어 일반적으로 더 빠르다고 알려져 있다. 반복문 안에서 대량으로 출력을 억제해야 한다면 `$null = ...` 형태를 우선 고려할 만하다.

**`Out-Null`로 버린 결과는 되돌릴 수 없다**: `New-Item ... | Out-Null`처럼 생성 결과를 즉시 버리면, 그 객체(예: 새로 만든 파일의 경로 정보)를 나중에 다시 쓸 수 없다. 생성된 객체 자체가 필요할 가능성이 있다면 `Out-Null` 대신 변수에 담아 두는 편이 안전하다.

**이식성**: `Out-Null`은 Bash·CMD의 `> /dev/null`, `> NUL` 리다이렉션과 정확히 같은 역할을 한다. `Out-String`은 "객체를 텍스트로 강제 변환한다"는 개념 자체가 텍스트 기반 셸에는 없는 동작이다 — 애초에 모든 것이 이미 텍스트인 Bash·CMD에서는 이 변환이 불필요하기 때문이다.

## Reference

- [Out-String (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/out-string)
- [Out-Null (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/out-null)
