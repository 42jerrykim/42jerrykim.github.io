---
draft: true
collection_order: 43
slug: arraylist-generic-list-powershell
title: "[PowerShell] 43. ArrayList와 Generic List(List&lt;T&gt;)"
date: 2026-08-29
lastmod: 2026-08-29
description: "42장 배열의 += 성능 문제를 해결하는 System.Collections.ArrayList와 System.Collections.Generic.List&lt;T&gt;의 Add/Remove 메서드 사용법, 두 컬렉션의 타입 안전성 차이, 언제 배열 대신 이들을 선택해야 하는지 정리한 챕터다."
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
- ArrayList
- Generic-List
- Collections
- Performance
- Type-Safety
- Boxing
image: "wordcloud.png"
---

## 개요

42장에서 짚었듯, 고정 크기 배열에 `+=`를 반복하면 매번 전체 배열을 복사하느라 성능이 나빠진다. `System.Collections.ArrayList`와 `System.Collections.Generic.List<T>`는 이 문제를 해결하는 **가변 크기 컬렉션**으로, .NET Framework Class Library가 제공하는 타입을 PowerShell에서 `New-Object`나 타입 리터럴로 바로 가져다 쓴다.

정신 모델은 "배열이 크기가 고정된 상자 줄이라면, 이 둘은 필요할 때마다 상자를 추가·제거할 수 있는 신축 가능한 목록"이라는 것이다. `List<T>`는 여기에 더해 "이 목록에는 오직 이 타입만 들어간다"는 제약(제네릭)을 컴파일 시점에 강제한다.

## 종류

| 타입 | 특징 |
|---|---|
| `System.Collections.ArrayList` | 어떤 타입의 객체든 담을 수 있음(타입 안전하지 않음), 값 타입 추가 시 박싱(boxing) 발생 |
| `System.Collections.Generic.List<T>` | 특정 타입 `T`만 담도록 제약, 박싱 없이 더 나은 성능과 타입 안전성 제공 |

Microsoft는 `ArrayList` 대신 가능하면 `List<T>`의 타입 특화 구현을 쓰라고 권장한다 — 값 타입을 담을 때 `ArrayList`는 매번 박싱/언박싱이 일어나지만 `List<T>`는 그렇지 않기 때문이다.

## 예시

```powershell
# ArrayList — 어떤 타입이든 섞어 담을 수 있다
$list = [System.Collections.ArrayList]::new()
[void]$list.Add("문자열")
[void]$list.Add(123)
$list.Remove(123)
$list.Count

# List<T> — 타입을 제약해 안전하게 담는다
$intList = [System.Collections.Generic.List[int]]::new()
$intList.Add(1)
$intList.Add(2)
# $intList.Add("문자열")   # 타입이 맞지 않아 오류

$stringList = New-Object 'System.Collections.Generic.List[string]'
$stringList.AddRange(@("a", "b", "c"))
$stringList.Contains("b")     # True
$stringList.IndexOf("c")      # 2
$stringList.Sort()
$stringList.Reverse()

# 배열보다 훨씬 빠른 반복 추가
$fast = [System.Collections.Generic.List[int]]::new()
1..10000 | ForEach-Object { $fast.Add($_) }
```

## 주의사항·함정

**`Add()` 메서드가 반환값을 파이프라인이나 화면에 출력할 수 있다**: `ArrayList.Add()`는 추가된 요소의 인덱스를 반환하는데, 스크립트 안에서 이 반환값을 버리지 않으면 원치 않는 숫자가 출력에 섞여 들어간다. 위 예시처럼 `[void]$list.Add(...)`로 감싸거나 `$list.Add(...) | Out-Null`(51장)로 출력을 억제하는 습관이 필요하다. `List<T>.Add()`는 반환값이 없어 이 문제가 없다.

**PowerShell 배열(`@()`)의 익숙한 문법에 익숙해지면 두 컬렉션의 타입 이름 표기가 낯설게 느껴질 수 있다**: `[System.Collections.Generic.List[int]]`처럼 제네릭 타입 매개변수를 대괄호로 감싸는 PowerShell 고유 표기(`List[int]`)는 C#의 `List<int>` 표기와 형태가 다르다. .NET 문서를 참고할 때 이 표기 차이를 염두에 두지 않으면 타입 이름을 잘못 옮겨 적기 쉽다.

**모든 상황에서 배열보다 무조건 낫다고 단정하지 않는다**: 요소 개수가 이미 정해져 있고 반복적으로 추가·삭제할 필요가 없다면, 42장의 단순 배열 문법(`@()`, 슬라이싱)이 여전히 더 읽기 쉽고 충분히 빠르다. `ArrayList`/`List<T>`는 "반복문 안에서 크기가 계속 늘어나는 컬렉션을 만들 때"처럼 명확한 성능 이유가 있을 때 선택하는 도구다.

**이식성**: Bash의 배열도 `array+=(값)`으로 동적으로 늘릴 수 있어 겉보기엔 비슷하지만 내부적으로 항상 새 배열을 만드는 셸 구현에 따라 성능 특성이 다르며, 타입 제약 개념 자체가 없다. CMD에는 대응 개념이 없다. .NET 컬렉션 타입을 직접 가져다 쓸 수 있다는 점은 PowerShell이 텍스트 기반 셸과 근본적으로 다른 지점 중 하나다(1장에서 소개한 .NET 기반 설계의 연장선).

## Reference

- [List&lt;T&gt; Class - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1)
- [ArrayList Class - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.collections.arraylist)
