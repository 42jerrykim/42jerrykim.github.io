---
draft: true
collection_order: 74
slug: module-structure-psm1-psd1-powershell
title: "[PowerShell] 74. 모듈 개념과 구조(.psm1/.psd1)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 모듈의 스크립트 모듈(.psm1)과 매니페스트(.psd1) 구조, $Env:PSModulePath 표준 경로, Export-ModuleMember로 공개 범위를 제한하는 법을 정리한 Part 9 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Module(모듈)
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
- Script-Module
- Module-Manifest
- PSModulePath
- Export-ModuleMember
- Namespace
- Module-Manifest-File
image: "wordcloud.png"
---

## 개요

**모듈**은 cmdlet·함수·변수·별칭 등을 하나의 재사용 가능한 단위로 묶은 패키지다. 57장부터 만들어 온 함수들이 지금까지는 세션이나 스크립트 파일 안에만 존재했다면, 이 장부터는 그 함수들을 다른 사람과 공유하거나 여러 스크립트에서 재사용할 수 있는 형태로 포장하는 법을 다루며 Part 9(모듈과 병렬 처리)를 시작한다.

정신 모델은 "**스크립트 모듈**(`.psm1`)이 실제 코드를 담는 몸통이고, **모듈 매니페스트**(`.psd1`)는 그 모듈의 이름표이자 설명서"라는 것이다. `.psm1`만으로도 모듈은 동작하지만, `.psd1`이 있어야 버전·의존성·작성자 같은 메타데이터를 함께 관리할 수 있다.

## 사용법

```powershell
# MyModule.psm1 — 실제 함수 정의
function Get-Greeting { "Hello from MyModule" }
Export-ModuleMember -Function Get-Greeting

# MyModule.psd1 — 매니페스트(New-ModuleManifest로 생성 가능)
New-ModuleManifest -Path .\MyModule.psd1 -RootModule 'MyModule.psm1' -ModuleVersion '1.0.0'
```

## 종류

| 파일 | 역할 |
|---|---|
| `.psm1`(스크립트 모듈) | 함수·변수 정의가 담긴 실제 코드 파일 |
| `.psd1`(모듈 매니페스트) | 버전, 작성자, 필요 PowerShell 버전, 내보낼 멤버 목록 등 메타데이터 |
| `.dll`(바이너리 모듈) | C#으로 컴파일된 네이티브 모듈(이 컬렉션은 스크립트 모듈에 집중) |
| `Export-ModuleMember` | `.psm1` 안에서 어떤 함수·변수·별칭을 외부에 공개할지 명시적으로 선택 |
| 모듈 폴더 구조 | `MyModule\MyModule.psm1`, `MyModule\MyModule.psd1`처럼 폴더명과 파일명을 일치시켜야 함 |

## 예시

```
$HOME\Documents\PowerShell\Modules\MyModule\
├── MyModule.psd1
└── MyModule.psm1
```

```powershell
# MyModule.psm1
function Get-Greeting {
    param($Name = "World")
    "Hello, $Name!"
}

function Set-InternalState {           # 내부용 — 외부에 공개하지 않을 함수
    $script:state = "modified"
}

Export-ModuleMember -Function Get-Greeting   # Get-Greeting만 공개, Set-InternalState는 숨김
```

```powershell
$Env:PSModulePath -split [System.IO.Path]::PathSeparator   # 모듈을 찾는 표준 경로들 확인

New-ModuleManifest -Path .\MyModule\MyModule.psd1 `
    -RootModule 'MyModule.psm1' `
    -ModuleVersion '1.0.0' `
    -Author 'Your Name' `
    -Description 'A sample module'                          # 매니페스트 생성

Test-ModuleManifest -Path .\MyModule\MyModule.psd1            # 매니페스트 유효성 검증
```

## 주의사항·함정

**`Export-ModuleMember`을 빠뜨리면 `.psm1` 안의 모든 함수가 기본적으로 전부 공개된다**: 의도적으로 내부 헬퍼 함수를 숨기고 싶다면 반드시 `Export-ModuleMember -Function`으로 공개할 함수를 명시적으로 선택해야 한다. 이 문을 빠뜨리면 "내부용으로만 쓰려던 함수"가 모듈을 가져온 세션에 그대로 노출돼, 62장에서 다룬 스코프 경계가 모듈 수준에서 무의미해진다.

**모듈 폴더 이름과 `.psm1`/`.psd1` 파일 이름이 정확히 일치해야 한다**: `MyModule` 폴더 안에 `MyModule.psm1`, `MyModule.psd1`이 있어야 PowerShell이 이를 하나의 모듈로 인식한다. 폴더명과 파일명이 다르면(예: `Utils` 폴더 안의 `MyModule.psm1`) 모듈이 정상적으로 검색·임포트되지 않는다.

**모듈이 표준 경로(`$Env:PSModulePath`) 밖에 있으면 자동 임포트되지 않는다**: 30장에서 다룬 `Env:` 프로바이더로 확인할 수 있는 이 경로 목록에 없는 위치의 모듈은, 75장에서 다룰 `Import-Module`에 전체 경로를 명시적으로 지정해야만 불러올 수 있다.

**이식성**: Bash에는 표준화된 모듈 시스템이 없어 `source` 명령으로 여러 스크립트를 이어 붙이는 정도가 최선이고, 이름 충돌이나 버전 관리는 스크립트 작성자가 직접 신경 써야 한다. Python의 패키지(`__init__.py`)나 Node.js의 `package.json`이 개념적으로 가장 가깝다 — `.psd1` 매니페스트가 `package.json`의 역할을, `.psm1`이 패키지 진입점 역할을 한다고 보면 비교하기 쉽다.

## Reference

- [about_Modules - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_modules)
