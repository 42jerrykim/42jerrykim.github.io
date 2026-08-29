---
draft: true
collection_order: 77
slug: powershell-class-keyword-powershell
title: "[PowerShell] 77. PowerShell 클래스(class 키워드)"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 5.0+ class 키워드로 사용자 정의 타입을 만드는 법과 프로퍼티·생성자·메서드 문법, 정적(static) 멤버, 27장 PSCustomObject와의 차이, ForEach-Object -Parallel에서 클래스를 안전하게 쓰는 법을 정리한 챕터다."
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
- PowerShell-Class
- Constructor
- Static-Member
- Object-Oriented
- Inheritance
- Custom-Type
image: "wordcloud.png"
---

## 개요

PowerShell 5.0부터 `class` 키워드로 사용자 정의 **타입**을 직접 만들 수 있다. 27장에서 `[PSCustomObject]`로 임시 객체를 만들었다면, `class`는 그 객체가 항상 같은 속성 구조와 동작(메서드)을 갖도록 **청사진**을 정의한다는 점이 다르다 — `[PSCustomObject]`가 즉석에서 찍어낸 객체 하나라면, 클래스는 같은 모양의 객체를 몇 개든 찍어낼 수 있는 틀이다.

정신 모델은 "클래스는 속성(데이터)과 메서드(그 데이터로 할 수 있는 동작)를 하나로 묶은 새로운 타입 정의"라는 것이다. 인스턴스를 만들면 `[타입]::new(...)` 문법으로 그 청사진에서 실제 객체가 찍혀 나온다.

## 사용법

```powershell
class <클래스이름> {
    [타입]$속성
    <클래스이름>([타입]$매개변수) { <생성자 로직> }
    [반환타입] 메서드이름([타입]$매개변수) { <메서드 로직> }
}
$인스턴스 = [<클래스이름>]::new(<인자>)
```

## 종류

| 요소 | 설명 |
|---|---|
| 프로퍼티 | 클래스 스코프에 선언된 변수, 인스턴스마다 별개의 값을 가짐 |
| 생성자 | 클래스와 이름이 같은 메서드, `[클래스]::new(...)`로 호출됨 |
| 메서드 | 항상 반환 타입을 명시해야 함(값이 없으면 `[void]`) |
| `static` 키워드 | 인스턴스 없이 클래스 자체에 속하는 프로퍼티·메서드(`[클래스]::멤버`로 접근) |
| `hidden` 키워드 | `Get-Member`(11장)와 자동완성에서 숨기되, 여전히 공개 멤버로 접근은 가능 |
| 상속(`class A : B`) | 단일 상속만 지원(다중 상속 불가) |

## 예시

```powershell
class Book {
    [string]$Title
    [string]$Author
    [int]$PageCount

    Book([string]$Title, [string]$Author) {
        $this.Title = $Title
        $this.Author = $Author
    }

    [timespan] GetReadingTime() {
        if ($this.PageCount -le 0) { throw '페이지 수를 알 수 없습니다.' }
        return [timespan]::new(0, $this.PageCount * 2, 0)   # 페이지당 2분으로 가정
    }

    [string] ToString() {
        return "$($this.Title) by $($this.Author)"
    }
}

$book = [Book]::new("The Hobbit", "J.R.R. Tolkien")   # 생성자 호출
$book.PageCount = 310
$book.GetReadingTime()                                    # 메서드 호출
"$book"                                                     # ToString() 오버라이드가 자동 적용됨

$book2 = [Book] @{ Title = "1984"; Author = "George Orwell" }  # 해시테이블로 기본 생성자 활용(44장)

class Counter {
    static [int]$Total = 0            # 모든 인스턴스가 공유하는 static 프로퍼티
    Counter() { [Counter]::Total++ }
}
[Counter]::new(); [Counter]::new()
[Counter]::Total                       # 2 — 인스턴스와 무관하게 공유됨
```

## 주의사항·함정

**클래스는 기본적으로 `ForEach-Object -Parallel`(79장)에서 안전하지 않다**: PowerShell 클래스는 자신이 정의된 런스페이스(Runspace)에 결속돼 있어, 병렬로 실행되는 다른 런스페이스에서 메서드를 호출하면 상태가 손상되거나 교착 상태(deadlock)에 빠질 수 있다. 병렬 처리에서 안전하게 쓰려면 클래스 선언에 `[NoRunspaceAffinity()]` 특성(PowerShell 7.4+)을 추가해야 한다.

**모듈에 정의한 클래스는 `Import-Module`만으로는 자동으로 딸려 오지 않는다**: 75장에서 배운 `Import-Module`은 함수·별칭·변수는 가져오지만 클래스·열거형 정의는 별도로 취급한다 — 클래스를 쓰려면 스크립트 맨 위에 `using module <모듈이름>` 문을 추가해야 한다. 이 차이를 모르면 "모듈을 임포트했는데 왜 타입을 찾을 수 없다고 나오지?"라는 혼란에 빠지기 쉽다.

**세션 도중에 클래스를 다시 로드하거나 언로드할 수 없다**: 함수는 다시 정의하면 즉시 갱신되지만, 클래스는 한 번 정의되면 세션이 끝날 때까지 그 정의가 고정된다. 개발 중 클래스 코드를 수정했다면 새 세션을 시작해야 변경 사항이 반영된다 — `Import-Module -Force`로도 해결되지 않는다는 점이 다른 모듈 멤버와 다르다.

**생성자·메서드의 매개변수에는 검증 특성(`ValidateSet` 등)을 쓸 수 없다**: 59장에서 배운 `[ValidateNotNullOrEmpty()]` 같은 매개변수 검증 속성은 클래스의 생성자·메서드 매개변수에는 적용되지 않는다. 검증이 필요하다면 메서드 본문 안에서 직접 확인 로직을 작성해야 한다.

**이식성**: C#의 `class` 문법을 상당 부분 그대로 계승해, 접근 지정자(`hidden`↔`private`)와 `static` 키워드 사용법이 비슷하다. Python의 `class`와도 개념적으로 유사하지만, Python은 다중 상속을 지원하는 반면 PowerShell 클래스는 단일 상속만 허용한다는 차이가 있다. Bash·CMD에는 객체지향 타입 시스템 자체가 없다.

## Reference

- [about_Classes - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes)
