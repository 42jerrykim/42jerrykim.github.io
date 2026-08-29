---
draft: true
collection_order: 42
slug: arrays-collections-powershell
title: "[PowerShell] 42. 배열과 컬렉션 기초"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 배열 @() 생성 문법과 인덱싱, 음수 인덱스, 범위 슬라이싱, .ForEach()/.Where() 메서드, Count/Length 속성, 다차원 배열과 재정렬 배열(jagged array)의 차이를 정리한 챕터다."
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
- Arrays
- Indexing
- Collections
- Where-Object
- ForEach-Object
- Jagged-Array
image: "wordcloud.png"
---

## 개요

PowerShell **배열**은 `@()`로 만드는 고정 크기 컬렉션으로, 16장에서 `Group-Object`가 그룹별로 만들어 준 컬렉션이나 12장 `Where-Object`가 걸러낸 결과가 실제로는 대부분 배열이었다. 이 장은 그 배열 자체를 직접 만들고 인덱싱하고 순회하는 법을 정리한다.

정신 모델은 "배열은 객체를 순서대로 담는 상자이고, 각 상자에는 0부터 시작하는 번호(인덱스)가 붙어 있다"는 것이다. 파이프라인이 객체를 한 번에 하나씩 흘려보내는 것과 달리, 배열은 이미 메모리에 다 올라온 상태에서 번호로 즉시 접근할 수 있다는 점이 다르다.

## 사용법

```powershell
$arr = @(값1, 값2, 값3)          # 명시적 배열 생성
$arr = 1, 2, 3                    # 쉼표만으로도 배열 생성
$arr = 1..5                       # 범위 연산자로 연속된 정수 배열
$arr[인덱스]                       # 요소 접근(0부터 시작)
```

## 종류

| 개념 | 설명 |
|---|---|
| 단일 차원 배열 | 가장 일반적인 형태, `@(1,2,3)` |
| 다차원 배열(Multidimensional) | `New-Object 'object[,]' 4,3`처럼 고정된 사각형 구조 |
| 재정렬 배열(Jagged Array) | 배열의 배열, 각 하위 배열 길이가 서로 달라도 됨(`@(@(1,2), @(1,2,3))`) |
| `.ForEach()` / `.Where()` 메서드 | PowerShell 4.0+, `ForEach-Object`/`Where-Object`보다 빠른 배열 전용 메서드 |
| `Count`/`Length` 속성 | 요소 개수(둘은 동의어) |

## 예시

```powershell
$a = 22, 5, 10, 8, 12, 9, 80
$a[0]              # 첫 요소: 22
$a[-1]             # 마지막 요소: 80(음수 인덱스)
$a[1..3]           # 슬라이싱: 5, 10, 8
$a[0,2+0..1]       # 인덱스 조합: 다양한 방식으로 원하는 요소만 추출

$a.Count           # 요소 개수: 7
$a += ,84          # 배열 끝에 새 요소 추가(불변이라 사실은 새 배열 생성)

$a.Where({ $_ -gt 10 })              # 조건에 맞는 요소만(12장 Where-Object의 메서드 버전)
$a.ForEach({ $_ * 2 })                # 각 요소를 변환(15장 ForEach-Object의 메서드 버전)

# 다차원 배열
$matrix = New-Object 'int[,]' 3,3
$matrix[0,0] = 1

# 재정렬 배열
$jagged = @(@(1,2), @(1,2,3,4,5), @(1,2,3))
$jagged[1][2]      # 두 번째 하위 배열의 세 번째 요소: 3

$empty = @()               # 빈 배열 명시적 생성
$single = ,"딱 하나"        # 요소가 하나뿐인 배열(쉼표 없으면 문자열로 취급됨)
```

## 주의사항·함정

**배열은 크기가 고정돼 있어, `+=`로 요소를 추가할 때마다 사실은 새 배열이 통째로 다시 만들어진다**: `$a += ,84`는 언뜻 배열 끝에 요소 하나를 붙이는 것처럼 보이지만, 실제로는 기존 배열 전체를 복사해 새 배열을 만드는 연산이다. 반복문 안에서 배열에 계속 `+=`를 쓰면 요소가 늘어날수록 매번 전체를 복사하므로 성능이 급격히 나빠진다 — 크기가 자주 바뀌는 컬렉션이 필요하다면 43장에서 다룰 `ArrayList`나 `List<T>`가 훨씬 적합하다.

**단일 요소 배열을 만들 때 쉼표를 빠뜨리면 배열이 아니게 된다**: `$single = "딱 하나"`는 문자열 변수일 뿐이고, 배열로 만들려면 `$single = ,"딱 하나"`처럼 앞에 쉼표(단항 배열 연산자)를 붙여야 한다. 함수가 항상 배열을 반환하도록 보장해야 하는 상황에서 이 차이를 놓치면, 요소가 하나일 때만 호출 코드가 예상과 다르게 동작하는 버그가 생긴다.

**다차원 배열과 재정렬 배열은 인덱싱 문법이 다르다**: 다차원 배열은 `$matrix[0,0]`처럼 쉼표로 구분한 인덱스 하나로 접근하지만, 재정렬 배열(배열의 배열)은 `$jagged[1][2]`처럼 대괄호를 연달아 써야 한다. 겉보기에 비슷해 보여도 내부 구조가 다르므로 혼용하면 인덱스 오류가 난다.

**이식성**: Bash 배열(`arr=(1 2 3)`, `${arr[0]}`)은 문자열 값만 담는 얕은 컬렉션이고, CMD는 배열 자체가 없어 지연 확장 변수나 `FOR` 루프로 흉내 낸다. PowerShell 배열은 어떤 .NET 객체든 담을 수 있고 음수 인덱스·범위 슬라이싱을 기본 문법으로 지원한다는 점에서 표현력이 훨씬 넓다.

## Reference

- [about_Arrays - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays)
