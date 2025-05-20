---
title: "[CleanCode] 코드 최적화의 비밀: 조건문을 호출부로 올리고 반복문을 하위 레벨로 내리기"
date: 2025-05-20
categories:
  - CleanCode
  - Programming
tags:
  - 코드 최적화
  - 조건문
  - 반복문
  - 코드 최적화
  - 조건문
  - 반복문
  - 성능 개선
  - 클린 코드
  - 리팩토링
  - 소프트웨어 개발
  - 프로그래밍 기법
  - 코드 가독성
  - 유지보수성
  - 함수형 프로그래밍
  - 객체지향 프로그래밍
  - 디자인 패턴
  - 테스트 주도 개발
  - 버그 수정
  - 코드 리뷰
  - 개발 도구
  - 알고리즘 최적화
  - 데이터 구조
  - 코드 품질
  - 개발 방법론
  - 협업
  - 문서화
  - 코드 스니펫
  - 성능 분석
  - 코드 스멜
  - 클린 아키텍처
  - 소프트웨어 공학
  - 프로그래밍 언어
  - 기술 블로그
  - code optimization
  - conditional statements
  - loops
  - performance improvement
  - clean code
  - refactoring
  - software development
  - programming techniques
  - code readability
  - maintainability
  - functional programming
  - object-oriented programming
  - design patterns
  - test-driven development
  - bug fixing
  - code review
  - development tools
  - algorithm optimization
  - data structures
  - code quality
  - development methodologies
  - collaboration
  - documentation
  - code snippets
  - performance analysis
  - code smell
  - clean architecture
  - software engineering
  - programming languages
  - technical blog
description: "조건문과 반복문을 최적화하는 방법에 대해 설명한다. 조건문은 함수 내부가 아닌 호출부로 이동시켜 코드의 복잡성을 줄이고, 반복문은 하위 레벨로 내리거나 배치 처리하여 성능을 향상시킬 수 있다. 이러한 접근은 코드의 가독성과 유지보수성을 높이는 데 기여한다."
image: index.png
---

본 글에서는 조건문과 반복문을 최적화하는 방법에 대해 다룬다. 조건문을 호출부로 올리고 반복문을 하위 레벨로 내리는 기법은 코드의 가독성과 유지보수성을 높이는 데 중요한 역할을 한다. 이러한 최적화 기법을 통해 개발자는 더 효율적이고 명확한 코드를 작성할 수 있으며, 이는 소프트웨어의 품질을 향상시키는 데 기여한다.

## 조건문을 호출부로 올리기

조건문을 함수 내부에 두기보다, 가능한 한 호출부로 이동시키는 것을 의미한다. 이렇게 하면 제어 흐름이 중앙 집중화되어 코드의 복잡성을 줄이고, 중복된 조건 검사를 방지할 수 있다.

### 조건문 예시

**좋은 예:**

```csharp
public void Frobnicate(Walrus walrus)
{
    // walrus를 처리하는 로직
}
```

**나쁜 예:**

```csharp
public void Frobnicate(Walrus? walrus)
{
    if (walrus == null)
        return;

    // walrus를 처리하는 로직
}
```

위의 나쁜 예에서는 `Walrus` 객체가 null인지 확인하는 조건문이 함수 내부에 있다. 하지만 좋은 예처럼 호출부에서 null 체크를 수행하고, 함수는 `Walrus` 객체만 처리하도록 하면 함수의 책임이 명확해지고, 중복된 조건 검사를 줄일 수 있다.

또한, 조건문을 호출부로 올리면 제어 흐름이 한 곳에 모여 있어, 불필요한 조건이나 중복된 로직을 쉽게 식별할 수 있다.

## 반복문을 하위 레벨로 내리기

반복문을 상위 레벨에서 처리하기보다, 가능한 한 하위 레벨에서 처리하거나 배치(batch) 처리로 전환하는 것을 의미다. 이는 성능 최적화와 코드의 명확성을 동시에 달성할 수 있는 방법이다.

### 반복문 예시

**좋은 예:**

```csharp
public void FrobnicateBatch(IEnumerable<Walrus> walruses)
{
    foreach (var walrus in walruses)
    {
        // walrus를 처리하는 로직
    }
}
```

**나쁜 예:**

```csharp
foreach (var walrus in walruses)
{
    Frobnicate(walrus);
}
```

좋은 예에서는 `walruses` 컬렉션을 한 번에 처리하는 `FrobnicateBatch` 함수를 사용하여 반복문을 하위 레벨로 내렸다. 이렇게 하면 반복문 내부에서 조건문을 반복적으로 평가하는 것을 피할 수 있고, 벡터화(vectorization)와 같은 성능 최적화를 적용하기 용이하다.

또한, 조건문과 반복문을 조합할 때도 이 원칙을 적용할 수 있다:

**좋은 예:**

```csharp
if (condition)
{
    foreach (var walrus in walruses)
    {
        walrus.Frobnicate();
    }
}
else
{
    foreach (var walrus in walruses)
    {
        walrus.Transmogrify();
    }
}
```

**나쁜 예:**

```csharp
foreach (var walrus in walruses)
{
    if (condition)
    {
        walrus.Frobnicate();
    }
    else
    {
        walrus.Transmogrify();
    }
}
```

좋은 예에서는 조건문을 반복문 밖으로 이동시켜, 조건을 한 번만 평가하도록 하여 성능을 향상시킨다.

## 결론

"Push Ifs Up and Fors Down"은 코드의 가독성과 성능을 동시에 향상시킬 수 있는 실용적인 방법론이다. 조건문을 호출부로 올리고, 반복문을 하위 레벨로 내리는 이러한 접근 방식은 코드의 명확성을 높이고, 중복된 로직을 줄이며, 성능 최적화를 가능하게 합니다. 특히 C#과 같은 객체 지향 언어에서도 이러한 원칙을 적용하면 더욱 큰 효과를 볼 수 있다.

* [Push Ifs Up And Fors Down : r/programming - Reddit](https://www.reddit.com/r/programming/comments/1kp9w35/push_ifs_up_and_fors_down/?utm_source=chatgpt.com)
* [How to break out of an IF statement - Stack Overflow](https://stackoverflow.com/questions/29297305/how-to-break-out-of-an-if-statement?utm_source=chatgpt.com)
* [Push Ifs Up And Fors Down Nov 15, 2023 - matklad](https://matklad.github.io/2023/11/15/push-ifs-up-and-fors-down.html?utm_source=chatgpt.com)
