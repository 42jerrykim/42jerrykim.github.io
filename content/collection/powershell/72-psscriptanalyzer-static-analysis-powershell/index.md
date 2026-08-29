---
draft: true
collection_order: 72
slug: psscriptanalyzer-static-analysis-powershell
title: "[PowerShell] 72. PSScriptAnalyzer — 정적 분석과 코딩 규칙"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 정적 분석 도구 PSScriptAnalyzer로 코드를 실행하지 않고도 잠재적 결함을 찾는 법과 Invoke-ScriptAnalyzer의 -Severity/-IncludeRule 매개변수, 71장 Pester와의 역할 차이를 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Testing(테스트)
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
- PSScriptAnalyzer
- Static-Analysis
- Code-Quality
- Linter
- Coding-Convention
- Best-Practice-Rule
image: "wordcloud.png"
---

## 개요

**PSScriptAnalyzer**는 스크립트를 실제로 실행하지 않고 코드 자체를 정적으로 분석해 잠재적 결함·나쁜 관례를 찾아내는 도구다. 71장의 Pester가 "이 함수가 실제로 옳게 동작하는가"를 실행을 통해 검증했다면, PSScriptAnalyzer는 "이 코드에 흔히 문제를 일으키는 패턴이 있는가"를 실행 없이 코드 구조만 보고 판단한다는 점에서 역할이 다르다 — 두 도구는 경쟁 관계가 아니라 서로 다른 층위를 보완하는 관계다.

정신 모델은 "PSScriptAnalyzer는 PowerShell 팀과 커뮤니티가 정리한 모범 사례를 규칙(Rule) 목록으로 만들어, 코드가 그 규칙을 어기는지 하나씩 대조하는 검사기"라는 것이다.

## 사용법

```powershell
Install-Module -Name PSScriptAnalyzer -Force        # 최초 설치(74–76장에서 다룰 모듈 설치의 선행 사례)
Invoke-ScriptAnalyzer -Path .\script.ps1 [-Severity <수준>] [-Recurse]
```

## 종류

| 개념 | 설명 |
|---|---|
| 내장 규칙 | 초기화 안 된 변수 사용, `PSCredential` 타입 오용, `Invoke-Expression` 남용 등 수십 개 |
| `-Severity` | `Error`/`Warning`/`Information`으로 결과 필터링 |
| `-IncludeRule` / `-ExcludeRule` | 특정 규칙만 검사하거나 제외 |
| `-Recurse` | 디렉터리 전체의 `.ps1`/`.psm1` 파일을 재귀적으로 검사 |
| 자동 서식 교정 | 일부 규칙은 검사뿐 아니라 코드 서식을 표준에 맞게 자동으로 고쳐 줌 |

## 예시

```powershell
Invoke-ScriptAnalyzer -Path .\MyScript.ps1                       # 기본 검사
Invoke-ScriptAnalyzer -Path .\MyScript.ps1 -Severity Error         # 심각한 문제만
Invoke-ScriptAnalyzer -Path .\Scripts -Recurse                     # 디렉터리 전체 검사

Invoke-ScriptAnalyzer -Path .\MyScript.ps1 -ExcludeRule PSAvoidUsingWriteHost   # 특정 규칙 제외

$results = Invoke-ScriptAnalyzer -Path .\MyScript.ps1
$results | Where-Object Severity -eq 'Warning'                       # 13장 Where-Object로 결과 다시 필터링
$results | Group-Object RuleName | Sort-Object Count -Descending      # 16장 Group-Object로 규칙별 위반 빈도 확인
```

## 주의사항·함정

**PSScriptAnalyzer는 "실행 가능한 코드"와 "좋은 코드"를 다른 기준으로 판단한다**: 문법 오류가 전혀 없어 정상적으로 실행되는 스크립트도, `Write-Host` 남용이나 초기화되지 않은 변수 참조 같은 관례 위반이 있으면 경고를 낸다. "일단 돌아가니까 괜찮다"와 "유지보수하기 좋은 코드다"는 서로 다른 질문이라는 점을 이 도구가 계속 상기시켜 준다.

**규칙을 무조건 전부 따르는 것이 항상 정답은 아니다**: 예를 들어 대화형 스크립트에서 의도적으로 `Write-Host`를 쓰는 경우처럼, 프로젝트의 맥락에 따라 특정 규칙이 오히려 부적절할 수 있다. `-ExcludeRule`로 팀이 합의한 예외를 명시적으로 배제하는 것이 "규칙을 무시한 채 경고를 방치하는 것"보다 안전하다 — 의도가 코드에 남기 때문이다.

**정적 분석은 논리적 오류까지 잡아내지는 못한다**: PSScriptAnalyzer는 코드의 **형태**를 검사할 뿐, "이 함수가 계산 로직을 실제로 올바르게 구현했는가"는 검사하지 못한다. 이 부분은 71장의 Pester가 담당하는 영역이며, 실무에서는 두 도구를 함께 CI 파이프라인에 넣어 상호 보완적으로 쓴다.

**이식성**: Python의 `pylint`/`flake8`, JavaScript의 `ESLint`가 개념적으로 정확히 대응하는 도구다 — 세 언어 생태계 모두 "실행 전에 코드 관례를 자동으로 점검한다"는 같은 아이디어를 채택했다. Bash에는 `shellcheck`이 유사한 역할을 하지만, CMD 배치 스크립트에는 이에 준하는 표준화된 정적 분석 도구가 마땅치 않다.

## Reference

- [PSScriptAnalyzer module - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview)
