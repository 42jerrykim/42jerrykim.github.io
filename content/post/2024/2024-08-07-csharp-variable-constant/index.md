---
image: "tmp_wordcloud.png"
description: "C# 변수(로컬·필드·정적)와 상수(const·readonly)의 정의, 생명주기, 기본값 규칙을 설명하고, 로컬 변수는 반드시 초기화해야 하며 필드는 타입 기본값이 자동 할당됩니다. const vs readonly 비교, var·ref·참조 반환, 실무 판단 기준과 학습 목표를 요약합니다."
categories: CSharp
date: "2024-08-07T00:00:00Z"
lastmod: "2026-03-17T00:00:00Z"
header:
  teaser: /assets/images/undefined/teaser.jpg
tags:
  - CSharp
  - .NET
  - Implementation
  - Software-Architecture
  - Memory
  - 메모리
  - String
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Reference
  - 참고
  - Best-Practices
  - Documentation
  - 문서화
  - Code-Quality
  - 코드품질
  - Type-Safety
  - Readability
  - Maintainability
  - Technology
  - 기술
  - Education
  - 교육
  - Blog
  - 블로그
  - Comparison
  - 비교
  - How-To
  - Tips
  - Productivity
  - 생산성
  - Open-Source
  - 오픈소스
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - OOP
  - 객체지향
  - Encapsulation
  - 캡슐화
  - Data-Structures
  - 자료구조
  - Compiler
  - 컴파일러
  - Performance
  - 성능
  - Pitfalls
  - 함정
  - Error-Handling
  - 에러처리
  - Configuration
  - 설정
  - Troubleshooting
  - 트러블슈팅
  - Workflow
  - 워크플로우
  - Career
  - 커리어
  - Innovation
  - 혁신
  - Markdown
  - 마크다운
  - Review
  - 리뷰
  - Migration
  - 마이그레이션
  - Beginner
  - Web
  - 웹
  - Backend
  - 백엔드
  - API
  - Linux
  - Windows
  - 윈도우
title: "[C#] 변수와 상수: 로컬·필드·const·readonly·var 완벽 정리"
---

C#에서 **변수**와 **상수**는 메모리 관리와 코드 안정성의 기초가 된다. 변수는 메서드 안의 **로컬 변수**로 쓰이거나, 클래스 안에서 여러 멤버가 공유하는 **필드(Field)**로 선언될 수 있다. 로컬 변수는 해당 메서드가 실행되는 동안만 유효하고, 메서드가 끝나면 사라진다. 필드는 클래스 인스턴스가 살아 있는 한 유지되며, 다른 메서드에서도 접근할 수 있다. **정적 필드(static field)**는 클래스 타입이 런타임에 처음 로드될 때 생성되어 프로그램이 끝날 때까지 유지된다. 로컬 변수는 기본값을 자동으로 받지 않으므로 사용 전 반드시 할당해야 하고, 필드는 명시적으로 초기화하지 않으면 해당 타입의 **기본값**(예: `int`는 0)이 자동으로 들어간다. C#은 **대소문자를 구분**하므로 `var1`과 `Var1`은 서로 다른 변수다. **상수**는 `const`로 정의하며, 한 번 정해진 값을 바꿀 수 없다. `readonly`는 생성자에서만 값을 넣을 수 있는 읽기 전용 필드로, 런타임에 값이 정해진다. 상수를 쓰면 매직 넘버 대신 의미 있는 이름을 쓸 수 있어 가독성과 유지보수에 도움이 된다. 이 글에서는 변수와 상수의 종류, `const`와 `readonly`의 차이, `var`·참조 변수(`ref`)·참조 반환까지 정리하고, 언제 무엇을 쓸지 판단 기준을 제시한다.

## 변수와 상수의 분류

C#에서 값이 들어가는 저장소는 **변수**와 **상수**로 나뉜다. 변수는 **로컬 변수**, **인스턴스 필드**, **정적 필드** 등으로 구분되며, 생명주기와 초기화 규칙이 다르다. 아래 다이어그램은 이 구분을 한눈에 보여 준다.

```mermaid
flowchart LR
  subgraph StorageTypes["저장소 종류"]
    LocalVar["로컬 변수</br>메서드 내"]
    InstanceField["인스턴스 필드</br>객체 수명"]
    StaticField["정적 필드</br>프로그램 수명"]
    ConstVal["const</br>컴파일 시 고정"]
    ReadonlyVal["readonly</br>런타임 1회 설정"]
  end
```

---

## C# 변수

**변수**는 데이터를 담는 메모리 공간이다. 타입에 따라 저장할 수 있는 값이 정해지며, C#에는 정수·실수·문자·불리언 등 **기본 타입**과 사용자 정의 타입이 있다. 변수는 **로컬 변수**, **필드**, **정적 필드** 등으로 나눌 수 있다.

**로컬 변수와 필드의 차이**

로컬 변수는 메서드 안에서만 선언·사용되며, 그 메서드가 실행되는 동안만 유효하다. 메서드가 끝나면 스택에서 제거된다. 필드는 클래스 멤버로 선언되며, 해당 클래스의 **인스턴스**가 있는 동안 유효하다. 로컬 변수는 메서드가 호출될 때 생성되고 반환 시 소멸하고, 필드는 인스턴스가 생성될 때 함께 초기화되어 인스턴스가 사라질 때까지 유지된다.

**변수의 기본값과 초기화**

필드는 선언만 해 두면 타입별 **기본값**이 들어간다(정수 0, `bool`은 `false`, 참조 타입은 `null` 등). 반면 **로컬 변수**는 기본값이 없으므로, 사용 전에 반드시 값을 넣어야 하며 그렇지 않으면 컴파일 오류가 난다.

**대소문자 구분과 이름 규칙**

C#은 대소문자를 구분한다. 변수 이름은 영문자, 숫자, 언더스코어(`_`)로 지을 수 있고, 숫자로 시작할 수 없으며, C# 예약어는 쓸 수 없다. 의미를 드러내는 이름을 쓰는 것이 좋다.

### C# 변수 예제

변수는 **타입**과 **이름**을 지정해 선언한다. 다음은 정수 변수 하나를 선언하고 10으로 초기화하는 예이다.

```csharp
int number = 10;
```

`int`가 타입, `number`가 이름, `10`이 초기값이다. 로컬 변수는 메서드 안에서만 살고, 필드는 인스턴스 전체에서 공유된다. 아래 예는 **필드**와 **로컬 변수**를 함께 쓰는 방식이다.

```csharp
class Example
{
    // 필드: 인스턴스가 있는 동안 유지
    private int field;

    public void Method()
    {
        // 로컬 변수: Method 실행 중에만 존재
        int localVariable = 5;
        field = localVariable + 10;
        Console.WriteLine("로컬 변수: " + localVariable);
        Console.WriteLine("필드: " + field);
    }
}
```

`field`는 클래스의 필드라서 `Method` 밖에서도 인스턴스를 통해 접근할 수 있고, `localVariable`은 `Method` 안에서만 쓰인다. 이렇게 **스코프**와 **생명주기**를 구분해 두면 메모리와 동작을 이해하기 쉬워진다.

---

## C# 상수

**상수**는 실행 중에 값이 바뀌지 않는 저장소이다. `const` 키워드로 선언하며, 선언 시 반드시 값을 지정해야 한다. 원주율·최대 시도 횟수 같은 고정값을 이름으로 두면 가독성과 실수 방지에 도움이 된다.

```csharp
const double PI = 3.14159;
```

**const와 readonly의 차이**

`const`는 **컴파일 시점**에 값이 고정되고, 이후 변경할 수 없다. `readonly`는 **런타임**에 한 번(보통 생성자에서) 값을 넣을 수 있고, 그 다음부터는 읽기만 가능하다. 그래서 생성자 인자나 설정에 따라 달라져야 하는 값은 `readonly`가 맞다.

```csharp
readonly int maxAttempts;

public MyClass(int attempts)
{
    maxAttempts = attempts; // 생성자에서만 초기화 가능
}
```

**상수 초기화와 사용**

상수는 선언과 동시에 초기화해야 하며, 이후 대입할 수 없다. 원의 면적 계산처럼 고정된 수치를 쓰는 예는 다음과 같다.

```csharp
using System;

class Program
{
    const double PI = 3.14159;

    static void Main()
    {
        double radius = 5.0;
        double area = PI * radius * radius;
        Console.WriteLine($"원의 면적: {area}");
    }
}
```

상수로 의미를 부여하면 코드가 읽기 쉬워지고, 값을 바꿀 때 한 곳만 수정하면 된다.

---

## C#에서 상수 정의 방법

상수는 `const`로 선언하고, 선언 시 반드시 값을 넣는다. 수학 상수나 설정값을 이름으로 두면 유지보수가 수월하다.

```csharp
const double PI = 3.14159;
```

**열거형(enum)으로 상수 묶기**

관련된 정수 상수들은 `enum`으로 묶을 수 있다. 기본적으로 각 멤버에는 0부터 순서대로 정수 값이 부여된다.

```csharp
enum DayOfWeek
{
    Sunday,
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday
}
```

사용할 때는 타입과 멤버 이름을 쓰면 된다.

```csharp
DayOfWeek today = DayOfWeek.Monday;
```

**정적 클래스로 상수 그룹화**

여러 상수를 한 덩어리로 두고 싶다면 `static` 클래스를 쓰는 방법이 있다. 인스턴스는 만들 수 없고, 클래스 이름으로 상수에 접근한다.

```csharp
public static class Constants
{
    public const double PI = 3.14159;
    public const int MaxUsers = 100;
}
```

```csharp
if (currentUsers > Constants.MaxUsers)
{
    Console.WriteLine("최대 사용자 수를 초과했습니다.");
}
```

이렇게 하면 상수가 상수임이 이름만 봐도 드러나고, 수정 가능한 필드와 구분하기 쉽다.

---

## const vs readonly 한눈에 보기

언제 `const`를 쓰고 언제 `readonly`를 쓸지 판단할 때 아래 표를 참고하면 된다.

| 항목 | const | readonly |
|------|--------|----------|
| 값 결정 시점 | 컴파일 시 | 런타임(생성자 등) |
| 초기화 | 선언 시 반드시 | 선언부 또는 생성자 |
| 허용 타입 | 기본 타입·string·null 등 | 모든 타입 |
| 메모리 | 리터럴로 대체·주소 없음 | 필드로 존재·참조 가능 |

`const`는 컴파일 시 리터럴로 치환되므로, DLL 등 외부에서 정의한 상수를 참조할 때는 버전이 바뀌어도 재컴파일하기 전까지 예전 값이 유지될 수 있다. 런타임에 결정되거나 타입이 클래스/구조체인 경우에는 `readonly`를 사용한다.

---

## C# 언어 사양과 선언 규칙

C# 언어 사양은 문법·의미·동작을 정의하는 공식 문서다. 변수·상수 선언 규칙도 여기서 정해진다.

**변수·상수 선언 규칙**

- 변수: 타입과 이름을 명시한다(예: `int count;`).
- 상수: `const`로 선언하고 선언 시 초기화한다.
- 이름: 영문자, 숫자, `_` 가능, 숫자로 시작 불가, 대소문자 구분, 예약어 사용 불가.

**암시적 형식 지역 변수(var)**

`var`를 쓰면 컴파일러가 초기화 식으로부터 타입을 추론한다. 선언과 초기화를 한 문장에서 해야 한다.

```csharp
var number = 10;   // number는 int
var name = "C#";   // name은 string
```

타입이 분명할 때만 쓰는 것이 가독성에 유리하다.

---

## C# 참조 변수

**참조 변수**는 다른 변수(또는 위치)를 가리키는 변수다. 값 타입도 `ref`를 통해 참조로 다룰 수 있다. `ref`로 메서드에 넘기면 메서드 안에서 값을 바꿀 수 있고, 그 변경이 호출부에 반영된다.

```csharp
void UpdateValue(ref int number)
{
    number += 10;
}

int myNumber = 5;
UpdateValue(ref myNumber);
Console.WriteLine(myNumber); // 15
```

**ref와 scoped**

`scoped`는 C# 11에서 도입된 한정자로, 참조(또는 값)의 **수명**을 현재 메서드 안으로 제한한다. 참조가 메서드 밖으로 새나가지 않도록 보장할 때 사용한다. 자세한 동작은 [C# 언어 사양](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/statements/declarations)의 선언문·참조 변수 섹션을 참고하면 된다.

**참조 반환**

메서드가 **참조를 반환**(return by ref)하면, 호출 쪽에서 그 위치를 통해 값을 읽고 쓸 수 있다. 대량 복사 없이 배열 요소 등을 직접 다룰 때 유용하다.

```csharp
class Sample
{
    private int[] numbers = new int[5];

    public ref int GetNumber(int index)
    {
        return ref numbers[index];
    }
}

Sample sample = new Sample();
ref int numberRef = ref sample.GetNumber(0);
numberRef = 10; // numbers[0]이 10으로 변경됨
```

참조 반환은 성능이 중요한 구간에서 복사를 줄일 수 있지만, 수명과 스코프를 잘 이해하고 써야 한다.

---

## C#에서의 암시적 형식(var)

**암시적 형식 지역 변수**는 `var`로 선언하며, 컴파일러가 초기화 식으로 타입을 추론한다. C# 3.0에서 도입되었고, 타입이 길거나 자명할 때 코드를 짧게 쓸 수 있게 해 준다.

```csharp
var number = 10;    // int
var name = "Hello"; // string
```

**var 사용 예**

LINQ 결과처럼 타입이 길거나, 생성자와 함께 쓸 때 반복을 줄일 수 있다.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

**제한 사항**

- `var`는 **지역 변수**에만 쓸 수 있다. 필드나 메서드 반환 타입에는 사용할 수 없다.
- 선언과 동시에 **초기화**가 필요하다. `var x;`는 오류다.
- 타입이 불명확해지면 가독성이 떨어질 수 있으므로, 타입이 드러나는 곳에서는 명시적 타입을 쓰는 편이 낫다.

---

## C# 변수와 상수의 활용

변수로는 실행 중 바뀌는 값을 담고, 상수로는 고정값에 이름을 붙인다. 다음 예는 상수 `PI`와 변수 `radius`, `area`를 함께 쓰는 경우다.

```csharp
using System;

class Program
{
    const double PI = 3.14;

    static void Main()
    {
        double radius = 5.0;
        double area;
        area = PI * radius * radius;
        Console.WriteLine("반지름이 " + radius + "인 원의 면적은 " + area + "입니다.");
    }
}
```

**상수 사용의 장단점**

- **장점**: 의미가 분명해지고, 실수로 값을 바꾸는 일을 막을 수 있으며, 한 곳만 수정하면 되어 유지보수가 쉽다.
- **단점**: 값이 상황에 따라 달라져야 하면 부적합하고, 상수가 많아지면 관리 비용이 늘 수 있다.

상황에 맞게 변수와 상수를 나누어 쓰는 것이 중요하다.

---

## 자주 묻는 질문(FAQ)

**Q. C# 변수와 상수의 차이는?**  
변수는 실행 중에 값을 바꿀 수 있는 저장소이고, 상수(`const`)는 선언 시 정해진 값을 변경할 수 없다. `readonly`는 필드를 생성자 등에서 한 번만 설정하고 이후에는 읽기만 가능하게 한다.

**Q. 변수를 초기화하지 않으면?**  
**필드**는 타입 기본값(숫자 0, `bool` false, 참조 null 등)으로 초기화된다. **로컬 변수**는 기본값이 없어서, 초기화 없이 사용하면 컴파일 오류가 난다.

**Q. readonly와 const의 차이는?**  
`const`는 컴파일 시점에 값이 고정되고, 기본 타입·string 등만 허용된다. `readonly`는 런타임에 생성자 등에서 한 번 설정할 수 있고, 모든 타입에 쓸 수 있다. 객체마다 다른 값이 필요하면 `readonly`를 쓴다.

---

## 관련 기술

**C#과 .NET**  
C#은 .NET 위에서 동작하는 객체 지향 언어이고, .NET이 제공하는 런타임(CLR)과 라이브러리를 함께 쓴다. 변수·상수도 CLR의 타입 시스템과 메모리 모델 위에서 동작한다.

**데이터 타입과 변수**  
C#에는 `int`, `double`, `string`, `bool` 등 기본 타입과 사용자 정의 타입이 있다. 변수는 이 타입에 따라 메모리 크기와 표현 범위가 정해진다.

**메모리 관리**  
C#은 가비지 컬렉션으로 힙 메모리를 관리한다. 값 타입 변수는 스택(또는 객체 내부)에, 참조 타입 객체는 힙에 할당된다. `using`으로 `IDisposable` 리소스를 정리할 수 있다.

---

## 학습 성과 목표와 판단 기준

**이 글을 읽은 뒤 할 수 있는 것**

- 로컬 변수·필드·정적 필드의 **스코프와 생명주기**를 설명할 수 있다.
- **const**와 **readonly**의 결정 시점·초기화 방식·적용 타입 차이를 설명할 수 있다.
- 주어진 상황에서 **const / readonly / 일반 필드** 중 어떤 것을 쓸지 선택할 수 있다.
- **var**를 써도 되는 경우와, 명시적 타입이 나은 경우를 구분할 수 있다.
- **ref**·참조 반환의 기본 동작과, 성능·안전성 측면의 주의점을 설명할 수 있다.

**언제 무엇을 쓸지**

- **const**: 컴파일 시 알 수 있는 진짜 상수(원주율, 버전 번호 등). 기본/문자열 타입.
- **readonly**: 생성자나 설정 단계에서 한 번 정해지는 값, 또는 타입이 클래스/구조체인 경우.
- **var**: 타입이 초기화 식에서 분명할 때(LINQ, `new List<int>()` 등). 가독성이 떨어지면 명시적 타입 사용.

---

## 결론

C#에서 **변수**는 로컬·필드·정적 필드로 나뉘며, 각각 스코프와 생명주기가 다르다. **상수**는 `const`(컴파일 시 고정)와 `readonly`(런타임 1회 설정)로 구분된다. 변수·상수를 올바르게 쓰면 가독성과 유지보수성이 좋아지고, `var`·`ref`·참조 반환은 적절한 상황에서만 사용하면 성능과 명확성을 함께 잡을 수 있다. 이름을 의미 있게 짓고, 로컬은 꼭 초기화한 뒤 사용하며, 상수와 변경 가능한 필드를 구분해 두는 습관이 실무에서 도움이 된다.

---

## Reference

- [C# 변수 및 상수 - C# 스터디](https://www.csharpstudy.com/CSharp/CSharp-variable.aspx)
- [C#에서 상수 정의 방법 - Microsoft Learn](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/how-to-define-constants)
- [상수 - C# 프로그래밍 가이드 - Microsoft Learn](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/constants)
- [선언문 - C# 참조 - Microsoft Learn](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/statements/declarations)
- [암시적 형식 지역 변수 - C# 프로그래밍 가이드 - Microsoft Learn](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/implicitly-typed-local-variables)
