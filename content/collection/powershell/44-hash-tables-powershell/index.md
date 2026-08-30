---
draft: false
collection_order: 44
slug: hash-tables-powershell
title: "[PowerShell] 44. 해시테이블(Hashtable) 다루기"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 해시테이블 @{} 생성 문법과 키-값 접근법, [ordered]@{}로 순서를 보존하는 법, Keys/Values 속성과 GetEnumerator()로 순회하는 법, ConvertFrom-StringData로 텍스트를 해시테이블로 바꾸는 법을 정리한 챕터다."
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
- Hashtable
- Key-Value
- Ordered-Dictionary
- PSCustomObject
- ConvertFrom-StringData
- Dictionary
image: "wordcloud.png"
---

## 개요

<strong>해시테이블</strong>(`Hashtable`, 다른 언어의 딕셔너리·맵에 대응)은 순서가 아니라 <strong>키(key)</strong>로 값을 찾는 컬렉션이다. 42장의 배열이 "몇 번째 요소인가"로 접근한다면, 해시테이블은 "이름이 무엇인가"로 접근한다. 27장에서 `[PSCustomObject]`를 만들 때 이미 `@{ 이름 = 값 }` 형태의 해시테이블 리터럴을 스치듯 사용했는데, 이 장은 그 문법 자체를 독립된 데이터 구조로 정식으로 다룬다.

정신 모델은 "각 키는 유일해야 하고, 순서는 (기본적으로) 보장되지 않는 이름표 붙은 상자들의 모음"이라는 것이다. 순서가 중요하다면 뒤에서 다룰 `[ordered]` 접두사가 필요하다. 설정 값, 함수 매개변수 묶음, 조회 테이블처럼 "이름으로 값을 찾는다"는 문제가 등장할 때마다 해시테이블이 자연스러운 첫 선택지가 되며, 25장에서 다룬 스플래팅(splatting)도 실제로는 이 해시테이블 문법 위에 세워진 기능이다.

## 사용법

```powershell
$hash = @{}                          # 빈 해시테이블
$hash = @{ 키1 = 값1; 키2 = 값2 }      # 리터럴로 즉시 생성
$hash.키                              # 점 표기법으로 값 접근
$hash["키"]                           # 대괄호 표기법으로 값 접근(공백·특수문자 포함 키에 필수)
```

## 종류

| 형태 | 설명 |
|---|---|
| 일반 `@{}` | 키의 순서가 보장되지 않음(내부적으로 해시 기반 정렬) |
| `[ordered]@{}` | PowerShell 3.0+, 입력한 순서를 그대로 유지하는 `OrderedDictionary` |
| 중첩 해시테이블 | 값 자체가 또 다른 해시테이블이나 배열일 수 있음 |
| `ConvertFrom-StringData` | `키=값` 형식의 텍스트(주로 `.psd1`, INI 유사 형식)를 해시테이블로 변환 |

## 예시

```powershell
$user = @{
    Name = "jsmith"
    Age  = 30
    City = "Seoul"
}

$user.Name              # 점 표기법
$user["Age"]             # 대괄호 표기법
$user.Add("Email", "jsmith@contoso.com")   # 새 키-값 추가
$user.Remove("City")                        # 키 제거
$user.ContainsKey("Name")                   # True

$user.Keys                # 모든 키
$user.Values               # 모든 값
$user.Count                 # 키-값 쌍 개수

foreach ($key in $user.Keys) {
    "$key = $($user[$key])"
}
$user.GetEnumerator() | Sort-Object Name   # 정렬된 순서로 순회(19장에서 배운 파이프라인 정렬 재활용)

$ordered = [ordered]@{ Third = 3; First = 1; Second = 2 }   # 입력 순서 그대로 유지
$ordered.Keys                                                 # Third, First, Second 순

$data = ConvertFrom-StringData -StringData @"
Server1 = web01
Server2 = web02
"@
$data.Server1              # "web01"

[PSCustomObject]$user      # 해시테이블을 객체로 변환(27장에서 다룬 문법의 역방향 활용)
```

## 주의사항·함정

**기본 `@{}`는 키 순서를 보장하지 않는다**: `@{ Third = 3; First = 1 }`처럼 입력한 순서와 `.Keys`로 꺼냈을 때의 순서가 다를 수 있다. 설정 파일처럼 사람이 읽는 순서가 중요한 데이터를 다룬다면 처음부터 `[ordered]@{}`로 만들어야 한다 — 나중에 일반 해시테이블을 순서가 있는 것으로 바꿀 방법은 없다.

**키가 존재하지 않을 때 `$hash.키`는 오류 없이 조용히 `$null`을 반환한다**: 오타로 잘못된 키 이름을 썼을 때 예외가 나지 않고 그냥 `$null`이 나오므로, 디버깅 중 "왜 값이 없지?"라는 혼란을 겪기 쉽다. 키 존재 여부 자체를 확인해야 한다면 `.ContainsKey()`를 명시적으로 써야 한다.

**해시테이블과 `[PSCustomObject]`는 비슷해 보이지만 용도가 다르다**: 해시테이블은 키를 프로그램적으로 동적으로 추가·조회하는 데 적합하고(`.Add()`, `.Remove()`, 반복문의 키 순회), `[PSCustomObject]`는 고정된 속성 집합을 가진 객체로 `Format-Table`이나 `Export-Csv`(49장) 같은 cmdlet과 자연스럽게 어울린다. 둘 사이를 변환하는 문법(`[PSCustomObject]$hash`)이 있다는 것 자체가, 상황에 맞는 쪽을 선택해 쓰라는 신호로 볼 수 있다. 속성 집합이 스크립트 실행 중에 계속 달라진다면 해시테이블을, 다른 cmdlet에 파이프라인으로 넘길 안정된 형태가 필요하다면 `[PSCustomObject]`를 우선 검토하는 것이 실용적인 기준이다.

**이식성**: Bash 4+의 연관 배열(`declare -A`)이 개념적으로 가장 가깝지만 값이 항상 문자열이고 중첩이 불가능하다. CMD에는 대응 개념이 없다. PowerShell 해시테이블은 값으로 어떤 객체든(다른 해시테이블, 배열, 사용자 정의 객체) 담을 수 있어 JSON(48장)이나 설정 데이터를 그대로 옮겨 담기에 자연스럽다.

## Reference

- [about_Hash_Tables - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables)
