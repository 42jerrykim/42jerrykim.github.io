---
draft: true
collection_order: 10
slug: powershell-pipeline-object-model-not-text
title: "[PowerShell] 10. 파이프라인 정신 모델 — 텍스트가 아닌 객체"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 파이프라인이 텍스트가 아닌 .NET 객체를 한 번에 하나씩 전달하는 원리, ByValue/ByPropertyName 매개변수 바인딩, 배열·해시테이블의 열거 방식 차이를 정리해 Part 2 전체의 기초를 다지는 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Automation(자동화)
- Guide(가이드)
- Education(교육)
- Beginner
- Comparison(비교)
- Reference(참고)
- How-To
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- DevOps
- Data-Structures(자료구조)
- Pipeline
- Parameter-Binding
- ByValue
- ByPropertyName
- Get-Member
- Concept
- Enumeration
- Quick-Reference
image: "wordcloud.png"
---

## 개요

CMD와 Bash에서 파이프(`|`)는 앞 명령의 표준 출력을 뒤 명령의 표준 입력으로 그대로 흘려보낸다 — 그 내용물은 언제나 줄바꿈으로 구분된 텍스트다. PowerShell의 파이프라인도 겉모습(`Command-1 | Command-2 | Command-3`)은 똑같지만, 흘러가는 내용물이 텍스트가 아니라 **.NET 객체**라는 점이 근본적으로 다르다. 이 챕터는 Part 1에서 다룬 개별 조작(도움말, 별칭, 실행 정책)을 뒤로하고, 이후 Part 2 전체(`Where-Object`, `Select-Object` 등)가 딛고 설 가장 중요한 개념적 토대를 다룬다.

## 기본 개념

파이프라인은 파이프라인 연산자(`|`)로 연결된 일련의 명령이다. 앞 명령이 만든 객체는 다음 명령의 입력으로 전달되고, 그 명령이 처리한 결과가 또 다음 명령으로 전달된다. 명령이 왼쪽에서 오른쪽 순서로 실행되며, 더 이상 이어지는 명령이 없으면 결과가 콘솔에 표시된다.

```powershell
Get-ChildItem -Path *.txt |
  Where-Object {$_.Length -gt 10000} |
    Sort-Object -Property Length |
      Format-Table -Property Name, Length
```

이 예시는 `.txt` 파일을 가져와 10,000바이트보다 큰 것만 거르고, 크기순으로 정렬한 뒤, 이름과 크기를 표로 보여준다. 각 단계에서 흘러가는 것은 텍스트 줄이 아니라 `System.IO.FileInfo` 객체이며, `Where-Object`는 그 객체의 `Length` 속성 값으로 조건을 판단한다 — 문자열을 잘라 숫자로 다시 변환하는 과정이 어디에도 없다.

## 종류/세부

### 매개변수 바인딩 — ByValue와 ByPropertyName

파이프로 전달된 객체가 다음 cmdlet의 어떤 매개변수에 연결될지는 PowerShell의 매개변수 바인딩 규칙이 결정한다. 방식은 두 가지다.

| 방식 | 동작 |
|---|---|
| **ByValue** | 매개변수가 기대하는 .NET 타입과 일치하거나 변환 가능한 값을 그대로 받는다(예: `Start-Service`의 `-Name`은 문자열을 ByValue로 받는다) |
| **ByPropertyName** | 파이프로 들어온 객체가 매개변수와 이름이 같은 속성을 가지고 있을 때만 그 속성 값을 받는다 |

어떤 매개변수가 파이프라인 입력을 받는지는 `Get-Help <cmdlet> -Full`이나 `-Parameter *`로 확인할 수 있다. 두 방식 중 무엇으로도 연결되지 않으면 "입력 객체를 매개변수에 바인딩할 수 없다"는 오류가 나며, 이때는 `Trace-Command -Name ParameterBinding`으로 바인딩 시도 과정을 추적해 원인을 좁힐 수 있다.

### 한 번에 하나씩 처리된다

파이프로 여러 객체를 넘기면 PowerShell은 그것을 배열 하나로 뭉쳐 보내지 않고, **한 번에 하나씩** 다음 명령으로 흘려보낸다. 이 차이는 `-InputObject` 매개변수로 컬렉션 전체를 한 번에 넘기는 것과 결과가 달라지는 지점에서 드러난다.

```powershell
Get-Process | Get-Member          # 프로세스 객체를 하나씩 전달 → System.Diagnostics.Process 타입 표시
Get-Member -InputObject (Get-Process)   # 배열 전체를 하나의 객체로 전달 → System.Object[] 타입 표시
```

`IEnumerable` 인터페이스(또는 그 제네릭 버전)를 구현한 타입은 파이프라인에서 자동으로 낱개로 풀린다. 다만 예외가 있다 — 해시테이블·`IDictionary` 구현체·`System.Xml.XmlNode`는 자동으로 열거되지 않고(`GetEnumerator()`를 직접 호출해야 함), 문자열(`System.String`)은 `IEnumerable`을 구현하지만 PowerShell이 의도적으로 열거하지 않는다(그렇지 않으면 문자열 하나가 문자 단위로 쪼개져 흘러갈 것이다).

```powershell
@(1,2,3) | Measure-Object          # 배열은 하나씩 열거되어 Count: 3
@{"One"=1;"Two"=2} | Measure-Object   # 해시테이블은 열거되지 않고 통째로 하나 → Count: 1
```

## 예제·다이어그램

앞서의 예시가 각 단계에서 무엇을 주고받는지는 다음과 같이 정리된다.

```mermaid
flowchart LR
    getItem["Get-ChildItem</br>FileInfo 객체 스트림"] --> whereObj["Where-Object</br>Length > 10000 필터"]
    whereObj --> sortObj["Sort-Object</br>Length 기준 정렬"]
    sortObj --> formatTbl["Format-Table</br>Name, Length 표 출력"]
```

네 단계 모두 같은 `FileInfo` 객체가 형태만 걸러지고 정렬되며 흘러갈 뿐, 중간에 텍스트로 직렬화됐다가 다시 파싱되는 단계가 없다는 것이 이 다이어그램의 핵심이다.

## 주의사항·함정

**네이티브 명령을 파이프라인에 섞을 때는 다시 텍스트로 돌아간다**: `ipconfig.exe | Select-String -Pattern 'IPv4'`처럼 PowerShell 밖의 실행 파일을 파이프라인에 섞으면, 그 실행 파일의 출력은 여전히 텍스트다. PowerShell 7.4부터는 `curl | tar`처럼 두 네이티브 명령 사이에 바이트 스트림을 그대로 보존하는 기능도 추가됐지만, 이는 객체 파이프라인과는 별개의 메커니즘이다.

**표준 입력(stdin)은 파이프라인과 별개다**: CMD·Bash의 파이프는 표준 출력/표준 오류/표준 입력(stdout/stderr/stdin)을 다루지만, PowerShell 파이프라인의 성공 스트림·오류 스트림은 이와 성격이 비슷해도 stdin은 PowerShell 파이프라인의 입력으로 연결되어 있지 않다.

**이식성**: Bash 파이프가 프로세스 사이를 흐르는 바이트 스트림이라면, PowerShell 파이프라인은 같은 프로세스(런타임) 안에서 객체 참조가 오가는 것에 더 가깝다 — 그래서 파일 하나 처리하는 데도 텍스트 파싱 도구(`awk`, `cut`, `grep`) 없이 속성 이름만으로 값을 다룰 수 있다. 11장부터 다룰 `Get-Member`, `Where-Object`, `Select-Object`는 모두 이 정신 모델 위에서 동작한다.

## Reference

- [about_Pipelines - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)
