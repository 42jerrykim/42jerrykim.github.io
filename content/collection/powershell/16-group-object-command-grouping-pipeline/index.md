---
draft: true
collection_order: 16
slug: group-object-command-grouping-powershell
title: "[PowerShell] 16. Group-Object — 그룹화"
date: 2026-08-29
lastmod: 2026-08-29
description: "Group-Object로 파이프라인 객체를 속성 값 기준으로 그룹화하는 법, -NoElement로 개수만 세는 법, -AsHashTable로 키-값 컬렉션을 만드는 법, Format-Table -GroupBy와의 차이를 정리한 챕터다."
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
- Data-Structures(자료구조)
- Group-Object
- HashTable
- Aggregation
- Get-Process
- Database(데이터베이스)
- Data-Analysis
image: "wordcloud.png"
---

## 개요

`Group-Object`는 속성 값이 같은 객체끼리 묶어 그룹별 개수와 구성원을 보여주는 cmdlet이다. SQL의 `GROUP BY`와 목적이 같다 — "프로세스를 우선순위별로 몇 개씩 묶어 볼까", "파일을 확장자별로 몇 개씩 볼까" 같은 질문에 답한다. `Sort-Object`가 순서를 바꾸고 `Where-Object`가 대상을 거른다면, `Group-Object`는 대상을 범주로 재구성한다.

정신 모델은 "지정한 속성 값을 키(key)로 삼아 객체를 여러 통에 나눠 담는다"는 것이다. 결과로 반환되는 `GroupInfo` 객체는 `Name`(그룹 키 값), `Count`(그룹 크기), `Group`(그룹에 속한 원본 객체들) 세 속성을 가진다.

## 사용법

```powershell
Group-Object [[-Property] <Object[]>] [-NoElement] [-AsHashTable] [-AsString] [-CaseSensitive]
```

속성을 여러 개 지정하면 첫 번째 속성으로 먼저 나누고, 그 안에서 다시 다음 속성으로 나누는 계층적 그룹화가 이뤄진다.

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Property` | 그룹화 기준 속성(들). 계산된 속성(스크립트블록)도 지정 가능하다. 생략하면 값 자체(또는 `ToString()`)로 그룹화한다 |
| `-NoElement` | 결과에서 `Group`(구성원 목록)을 빼고 `Count`/`Name`만 남긴다 — 개수만 필요할 때 메모리를 아낀다 |
| `-AsHashTable` | `GroupInfo` 객체 목록 대신 키-값 해시테이블로 반환한다. `$result.Get`처럼 점(dot) 표기로 그룹에 바로 접근할 수 있다 |
| `-AsString` | `-AsHashTable`과 함께 써서 해시테이블 키를 문자열로 강제 변환한다 |
| `-CaseSensitive` | 문자열 그룹화를 대소문자 구분으로 바꾼다. PowerShell 7부터 `-AsHashTable`과 조합하면 대소문자 구분 해시테이블을 만들 수 있다 |
| `-Culture` | 그룹화 시 문자열 비교에 사용할 문화권을 지정한다 |

## 예시

```powershell
Get-ChildItem -Recurse | Group-Object -Property Extension -NoElement | Sort-Object -Property Count -Descending
1..20 | Group-Object -Property { $_ % 2 }                            # 홀짝 그룹화
Get-Process | Group-Object -Property PriorityClass -NoElement        # 우선순위별 개수
Get-Process | Group-Object -Property Name -NoElement | Where-Object { $_.Count -gt 1 }   # 중복 실행 중인 프로세스 찾기
$byVerb = Get-Command Get-*, Set-* -CommandType Cmdlet | Group-Object -Property Verb -AsHashTable -AsString
$byVerb.Get                                                            # Get 계열 cmdlet만 바로 조회
$hash = Get-ChildItem -Path C:\Files | Group-Object -Property Extension -CaseSensitive -AsHashTable
```

## 주의사항·함정

**`Group-Object`와 `Format-Table -GroupBy`는 목적이 다르다**: `Format-Table -GroupBy`는 이미 정렬된 객체를 화면에 그룹별 소제목이 붙은 여러 표로 나눠 보여줄 뿐, 새로운 객체를 만들지 않는다. 반면 `Group-Object`는 그룹별 `Count`·`Group`을 담은 실제 객체를 반환하므로, 그 결과를 다시 파이프라인에서 가공(정렬, 필터링)할 수 있다. "그룹별 개수 상위 5개를 보고 싶다"처럼 그룹 자체를 다시 다뤄야 한다면 `Group-Object`가 필요하다.

**서로 다른 .NET 타입의 객체도 그룹화할 수 있다**: `Group-Object`는 그룹화할 속성 이름과 타입이 다른 객체 사이에서도 최선을 다해 값을 변환해 그룹화를 시도한다. 다만 지정한 속성 자체가 없는 객체는 그룹화되지 못하고 `AutomationNull.Value`라는 이름의 그룹으로 따로 모인다.

**결과는 그룹 이름 기준 오름차순으로 정렬되지만, 그룹 내부 순서는 보장되지 않는다**: 그룹에 속한 개별 항목(`Group` 속성)은 원래 파이프라인에서 받은 순서 그대로 유지된다.

**이식성**: Bash에서는 `sort | uniq -c`로 텍스트 줄의 등장 횟수를 세는 것이 `Group-Object -NoElement`와 목적이 비슷하지만, 텍스트를 정확히 같은 형태로 맞춰야 제대로 세어진다. `Group-Object`는 속성 값(숫자·날짜·열거형 포함)을 타입 그대로 비교하므로 이런 사전 정규화가 필요 없다.

## Reference

- [Group-Object (Microsoft.PowerShell.Utility) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/group-object)
