---
draft: true
collection_order: 98
slug: env-drive-environment-variable-powershell
title: "[PowerShell] 98. Env: 드라이브와 환경 변수 관리"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell $Env: 드라이브로 환경 변수를 읽고 쓰는 법과 세션 범위 변경이 프로세스 범위에 그치는 이유, [Environment]::SetEnvironmentVariable로 영구 저장하는 법, 대소문자·구분자가 플랫폼마다 다른 함정을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- System-Management
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
- Environment-Variable
- Env-Drive
- PSModulePath
- Environment-Provider
- Persistent-Variable
- Cross-Platform
image: "wordcloud.png"
---

## 개요

`$Env:` 드라이브는 30장에서 배운 프로바이더 개념이 환경 변수에 적용된 사례로, 운영체제와 다른 프로그램이 공유하는 **환경 변수**를 파일 시스템 드라이브를 다루듯 조회·수정하게 해 준다. 41장에서 배운 일반 PowerShell 변수(`$변수`)와 달리, 환경 변수는 항상 문자열이고 **자식 프로세스에 상속**된다는 점이 근본적으로 다르다 — 78장의 `Start-Job`, 90장의 `Start-Process`가 새로 만드는 프로세스가 부모의 환경 변수를 그대로 물려받는 이유가 여기에 있다.

정신 모델은 "환경 변수는 프로세스가 시작될 때 부모로부터 물려받는 설정값 봉투이고, `$Env:`로 하는 수정은 그 봉투의 로컬 사본만 바꾸는 것"이라는 것이다.

## 사용법

```powershell
$Env:<변수이름>                    # 읽기
$Env:<변수이름> = "<새값>"          # 쓰기(현재 세션에만 적용)
[Environment]::SetEnvironmentVariable('이름', '값', 'Machine')   # 영구 저장
```

## 종류

| 방법 | 범위 | 영구성 |
|---|---|---|
| `$Env:변수` 문법 | 현재 프로세스 | 세션 종료 시 사라짐 |
| `New-Item`/`Set-Item`/`Get-Item`/`Remove-Item -Path Env:\...` | 현재 프로세스 | 세션 종료 시 사라짐(문법만 다를 뿐 위와 동일 범위) |
| `[Environment]::GetEnvironmentVariable()`/`SetEnvironmentVariable()` | 세 번째 인자로 `Process`/`User`/`Machine` 지정 가능 | `User`/`Machine` 지정 시 영구 저장(Windows만) |
| `$PROFILE`에 설정 | 현재 프로세스(단, 매 세션 자동 재실행) | 사실상 영구적(profile이 유지되는 한) |

## 예시

```powershell
$Env:windir                                  # 읽기
$Env:Foo = 'An example'                        # 세션에만 존재하는 새 변수 생성
$Env:Foo += '!'                                  # 문자열이므로 이어붙이기 가능

New-Item -Path Env:\Bar -Value 'Baz'               # cmdlet 문법으로 생성(동일한 결과)
Get-ChildItem Env:                                   # 모든 환경 변수 나열(31장 응용)
Remove-Item -Path Env:\Bar                             # 세션에서 제거

[Environment]::SetEnvironmentVariable('Foo', 'Bar', 'Machine')   # 컴퓨터 전체에 영구 저장(관리자 권한 필요)
[Environment]::SetEnvironmentVariable('Foo', '', 'Machine')        # 빈 문자열로 설정해 영구 삭제

# 06장에서 다룬 $PROFILE에 추가하면 매 세션 자동 적용
# $Env:CompanyUri = 'https://internal.contoso.com'
# $Env:PATH += ';C:\Tools'   (Windows는 세미콜론, Linux/macOS는 콜론 구분자)

$Env:PSModulePath -split [System.IO.Path]::PathSeparator   # 74장에서 다룬 모듈 검색 경로 확인

$Env:TEST = $null                                            # PowerShell 7.5+ — 값을 $null로 하면 세션에서 제거됨
```

## 주의사항·함정

**`$Env:변수 = 값`으로 바꾼 값은 현재 세션(프로세스 범위)에만 적용된다**: CMD의 `set` 명령이나 Unix의 `setenv`와 마찬가지로, 이 대입은 현재 실행 중인 PowerShell 프로세스에만 영향을 준다. 세션을 닫으면 원래 값으로 되돌아간다 — 시스템 전체나 사용자 전체에 영구적으로 적용하려면 `[Environment]::SetEnvironmentVariable()`의 세 번째 인자로 `User`나 `Machine` 스코프를 명시하거나, 06장의 `$PROFILE`에 설정을 넣어 매 세션 자동으로 재적용되게 해야 한다.

**macOS·Linux에서는 환경 변수 이름이 대소문자를 구분한다**: Windows에서는 `$Env:Path`와 `$Env:PATH`가 같은 변수를 가리키지만, macOS·Linux에서는 서로 다른 두 변수로 취급된다. 크로스플랫폼 스크립트를 작성한다면 환경 변수 이름의 대소문자를 플랫폼에 따라 통일해서 다뤄야 한다 — 관례상 표준 변수는 대문자(`PATH`, `HOME`)로 쓰는 것이 안전하다.

**경로를 이어붙일 때 구분자가 플랫폼마다 다르다**: `$Env:PATH`에 새 경로를 추가할 때 Windows는 세미콜론(`;`), macOS/Linux는 콜론(`:`)을 구분자로 쓴다. 이 차이를 무시하고 하드코딩된 구분자를 쓰면 다른 플랫폼에서 경로가 깨진다 — `[System.IO.Path]::PathSeparator`를 쓰면 플랫폼에 맞는 구분자를 자동으로 얻을 수 있다.

**`[Environment]::SetEnvironmentVariable()`로 값을 `$null`로 설정해도 변수가 삭제되지 않는다**: `$Env:변수 = $null`이나 `Remove-Item Env:\변수`는 변수를 완전히 제거하지만, `.NET` 메서드로 `$null`을 넘기면 변수는 남아 있고 값만 비워진다 — 두 방식의 동작이 미묘하게 다르다는 점이 문서에도 명시된 함정이다.

**이식성**: Bash의 `export VAR=value`(영구화하려면 `.bashrc`에 추가), CMD의 `set VAR=value`(영구화하려면 `setx`)와 개념적으로 대응한다. PowerShell이 다른 점은 `$Env:` 변수 문법, `Env:` 프로바이더(`Get-Item`/`Set-Item` 등), `.NET` `Environment` 클래스라는 **세 가지** 서로 다른 방법을 모두 제공한다는 것이다 — 이 저장소 곳곳에서 강조해 온 "여러 계층(변수 문법/프로바이더/.NET)이 같은 데이터를 다른 방식으로 노출한다"는 설계가 여기서도 반복된다.

## Reference

- [about_Environment_Variables - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables)
