---
title: "[C#] C#에서 변수와 상수의 이해"
categories: csharp
tags:
- C#
- variables
- constants
- programming
- coding
- softwaredevelopment
- examples
- tutorials
- learnprogramming
- dotnet
header:
teaser: /assets/images/undefined/teaser.jpg
---

C#에서 변수는 메서드 내에서 로컬 변수로 선언되거나 클래스 내에서 멤버들이 사용하는 전역적 변수인 필드(Field)로 선언될 수 있다. 로컬 변수는 해당 메서드 내에서만 사용되며, 메서드 호출이 끝나면 소멸된다. 반면 필드는 클래스의 객체가 살아있는 한 계속 존재하며 다른 메서드들에서 참조할 수 있다. 필드가 정적 필드(static field)인 경우, 클래스 타입이 처음으로 런타임에 의해 로드될 때 해당 타입 객체에 생성되어 프로그램이 종료될 때까지 유지된다. 로컬 변수는 기본값을 할당받지 못하므로 반드시 사용 전에 값을 할당해야 하며, 필드는 값을 할당하지 않으면 해당 타입의 기본값이 자동으로 할당된다. 예를 들어, int 타입의 필드인 경우 기본값 0이 할당된다. 모든 C# 변수의 이름은 대소문자를 구별하므로, var1과 Var1은 서로 다른 변수로 인식된다. C#에서 상수는 const 키워드를 사용하여 정의되며, 상수는 초기값을 변경할 수 없는 필드로, const는 필드 선언부나 메서드 내에서 사용될 수 있다. readonly 키워드를 사용하여 읽기 전용 필드를 만들 수 있으며, 이는 런타임 시 값이 결정된다. 상수를 사용하면 매직 넘버 대신 의미 있는 이름을 제공할 수 있어 코드의 가독성을 높이는 데 기여한다. C#에서는 enum을 사용하여 정수 형식의 상수를 정의할 수 있으며, static 클래스를 통해 상수를 그룹화할 수도 있다. 이러한 변수와 상수의 개념은 C# 프로그래밍에서 매우 중요하며, 이를 통해 코드의 구조와 가독성을 향상시킬 수 있다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## C# 변수
**C# 변수의 정의와 종류**  
**로컬 변수와 필드의 차이**  
**변수의 기본값과 초기화**  
**대소문자 구별과 변수 이름 규칙**  

## C# 변수 예제
**기본적인 C# 변수 예제**  
**로컬 변수와 필드 사용 예제**  

## C# 상수
**C# 상수의 정의와 사용법**  
**const와 readonly의 차이**  
**상수의 초기화와 사용 예제**  

## C#에서 상수 정의 방법
**상수의 정의와 사용 예**  
**열거형을 통한 상수 정의**  
**정적 클래스에서 상수 그룹화**  

## C# 언어 사양
**C# 언어 사양의 중요성**  
**상수와 변수의 선언 규칙**  
**암시적 형식 지역 변수의 사용**  

## C# 참조 변수
**참조 변수의 정의와 사용법**  
**ref와 scoped 키워드의 차이**  
**참조 반환 메서드의 예제**  

## C#에서의 암시적 형식
**암시적 형식 지역 변수의 정의**  
**var 키워드의 사용 예**  
**암시적 형식의 제한 사항**  

## C# 변수와 상수의 활용
**변수와 상수를 활용한 코드 예제**  
**상수 사용의 장점과 단점**  

## 자주 묻는 질문(FAQ)
**C# 변수와 상수의 차이는 무엇인가요?**  
**C#에서 변수를 초기화하지 않으면 어떻게 되나요?**  
**readonly와 const의 차이는 무엇인가요?**  

## 관련 기술
**C#과 .NET의 관계**  
**C#의 데이터 타입과 변수**  
**C#의 메모리 관리와 변수**  

## 결론
**C# 변수와 상수의 중요성 요약**  
**효율적인 변수 사용을 위한 팁**  
**C# 프로그래밍에서의 변수 관리의 중요성**  
---
-->

<!--
---
## C# 변수
**C# 변수의 정의와 종류**  
**로컬 변수와 필드의 차이**  
**변수의 기본값과 초기화**  
**대소문자 구별과 변수 이름 규칙**  
-->

## C# 변수

**C# 변수의 정의와 종류**  

C#에서 변수는 데이터를 저장하는 메모리 공간을 의미한다. 변수는 특정 데이터 타입을 가지며, 이 데이터 타입에 따라 저장할 수 있는 값의 종류가 결정된다. C#에서는 기본 데이터 타입으로 정수형, 실수형, 문자형, 불리언형 등이 있으며, 이러한 기본 데이터 타입을 기반으로 사용자 정의 데이터 타입도 생성할 수 있다. 변수는 크게 로컬 변수, 필드, 정적 변수 등으로 나눌 수 있다.

**로컬 변수와 필드의 차이**  

로컬 변수는 메서드 내에서 선언된 변수로, 해당 메서드가 실행되는 동안만 유효하다. 반면, 필드는 클래스 내에서 선언된 변수로, 클래스의 인스턴스가 존재하는 동안 유효하다. 로컬 변수는 메서드가 호출될 때 생성되고, 메서드가 종료되면 소멸된다. 필드는 클래스의 인스턴스가 생성될 때 초기화되며, 인스턴스가 소멸될 때까지 존재한다.

**변수의 기본값과 초기화**  

C#에서 변수를 선언할 때 초기화를 하지 않으면, 각 데이터 타입에 따라 기본값이 자동으로 할당된다. 예를 들어, 정수형 변수는 0, 불리언형 변수는 false, 문자열 변수는 null로 초기화된다. 변수를 사용하기 전에 반드시 초기화하는 것이 좋으며, 초기화하지 않은 변수를 사용하면 컴파일 오류가 발생한다.

**대소문자 구별과 변수 이름 규칙**  

C#은 대소문자를 구별하는 언어이다. 따라서 변수 이름을 정의할 때 대소문자를 정확히 구분해야 한다. 변수 이름은 영문자, 숫자, 언더스코어(_)로 구성할 수 있으며, 숫자로 시작할 수 없다. 또한, C#의 예약어는 변수 이름으로 사용할 수 없다. 변수 이름은 의미를 잘 나타내도록 작성하는 것이 좋다.

--- 

이와 같은 방식으로 나머지 목차에 대해서도 작성할 수 있다. 각 섹션에 대해 더 많은 세부 정보를 추가하고, 예제 코드를 포함하여 독자가 이해하기 쉽게 설명할 수 있다.

<!--
## C# 변수 예제
**기본적인 C# 변수 예제**  
**로컬 변수와 필드 사용 예제**  
-->

## C# 변수 예제

**기본적인 C# 변수 예제**  

C#에서 변수를 선언하는 방법은 매우 간단하다. 변수를 선언할 때는 데이터 타입과 변수 이름을 지정해야 한다. 예를 들어, 정수를 저장할 변수를 선언하려면 다음과 같이 작성할 수 있다.

```csharp
int number = 10;
```

위의 코드에서 `int`는 데이터 타입을 나타내고, `number`는 변수 이름이다. `10`은 변수에 할당된 초기값이다. C#에서는 다양한 데이터 타입을 지원하며, 각 데이터 타입에 따라 저장할 수 있는 값의 범위가 다르다.

**로컬 변수와 필드 사용 예제**  

로컬 변수는 메서드 내에서 선언된 변수로, 해당 메서드가 실행되는 동안만 유효하다. 반면, 필드는 클래스의 멤버로, 클래스의 인스턴스가 존재하는 동안 유효하다. 아래의 예제를 통해 이 두 가지의 차이를 살펴보자.

```csharp
class Example
{
    // 필드
    private int field;

    public void Method()
    {
        // 로컬 변수
        int localVariable = 5;
        field = localVariable + 10;
        Console.WriteLine("로컬 변수: " + localVariable);
        Console.WriteLine("필드: " + field);
    }
}
```

위의 코드에서 `field`는 클래스의 필드로, `Method` 메서드 내에서 `localVariable`이라는 로컬 변수를 선언하고 있다. `localVariable`은 메서드가 호출될 때만 존재하며, 메서드가 종료되면 사라진다. 반면, `field`는 클래스의 인스턴스가 존재하는 한 계속해서 값을 유지한다. 

이와 같이 C#에서는 변수의 범위와 생명주기를 이해하는 것이 중요하다. 변수를 적절히 사용하면 코드의 가독성과 유지보수성을 높일 수 있다.

<!--
## C# 상수
**C# 상수의 정의와 사용법**  
**const와 readonly의 차이**  
**상수의 초기화와 사용 예제**  
-->

## C# 상수

**C# 상수의 정의와 사용법**  

C#에서 상수는 프로그램 실행 중에 값이 변경되지 않는 변수를 의미한다. 상수는 `const` 키워드를 사용하여 선언하며, 초기화 시 반드시 값을 지정해야 한다. 상수는 코드의 가독성을 높이고, 실수로 값이 변경되는 것을 방지하는 데 유용하다. 예를 들어, 원주율과 같은 수학적 상수나 설정 값 등을 상수로 정의할 수 있다.

```csharp
const double PI = 3.14159;
```

**const와 readonly의 차이**  

`const`와 `readonly`는 모두 상수를 정의하는 데 사용되지만, 두 가지는 중요한 차이점이 있다. `const`는 컴파일 타임에 값이 결정되며, 이후 변경할 수 없다. 반면, `readonly`는 런타임에 값을 설정할 수 있으며, 생성자에서만 초기화할 수 있다. 이로 인해 `readonly`는 더 유연한 사용이 가능하다.

```csharp
readonly int maxAttempts;

public MyClass(int attempts)
{
    maxAttempts = attempts; // 생성자에서 초기화 가능
}
```

**상수의 초기화와 사용 예제**  

상수는 선언과 동시에 초기화해야 하며, 이후에는 값을 변경할 수 없다. 상수를 사용하는 예제로는 다음과 같은 코드가 있다. 이 예제에서는 상수를 사용하여 원의 면적을 계산하는 프로그램을 작성하였다.

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

이와 같이 상수를 사용하면 코드의 의미가 명확해지고, 유지보수가 용이해진다. 상수는 프로그램의 여러 곳에서 재사용할 수 있어, 코드의 중복을 줄이는 데도 도움이 된다.

<!--
## C#에서 상수 정의 방법
**상수의 정의와 사용 예**  
**열거형을 통한 상수 정의**  
**정적 클래스에서 상수 그룹화**  
-->

## C#에서 상수 정의 방법

**상수의 정의와 사용 예**  

C#에서 상수는 프로그램 실행 중에 변경되지 않는 값을 저장하는 데 사용된다. 상수는 `const` 키워드를 사용하여 정의할 수 있으며, 초기화 시 반드시 값을 할당해야 한다. 예를 들어, 원주율을 상수로 정의할 수 있다.

```csharp
const double PI = 3.14159;
```

이렇게 정의된 `PI`는 프로그램의 다른 부분에서 사용할 수 있으며, 값이 변경되지 않도록 보장된다. 상수는 주로 수학적 상수나 설정 값 등을 정의할 때 유용하다.

**열거형을 통한 상수 정의**  

C#에서는 열거형(enumeration)을 사용하여 관련된 상수 집합을 정의할 수 있다. 열거형은 `enum` 키워드를 사용하여 정의하며, 각 상수는 기본적으로 정수 값을 가진다. 예를 들어, 요일을 나타내는 열거형을 정의할 수 있다.

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

이렇게 정의된 `DayOfWeek` 열거형은 코드에서 요일을 쉽게 사용할 수 있게 해준다. 예를 들어, 특정 요일을 변수에 할당할 수 있다.

```csharp
DayOfWeek today = DayOfWeek.Monday;
```

**정적 클래스에서 상수 그룹화**  

정적 클래스(static class)를 사용하여 관련된 상수를 그룹화할 수 있다. 정적 클래스는 인스턴스를 생성할 수 없으며, 모든 멤버가 정적(static)으로 정의된다. 이를 통해 상수를 논리적으로 그룹화하여 코드의 가독성을 높일 수 있다.

```csharp
public static class Constants
{
    public const double PI = 3.14159;
    public const int MaxUsers = 100;
}
```

이렇게 정의된 `Constants` 클래스는 프로그램의 다른 부분에서 쉽게 접근할 수 있는 상수들을 제공한다. 예를 들어, 최대 사용자 수를 확인할 때 다음과 같이 사용할 수 있다.

```csharp
if (currentUsers > Constants.MaxUsers)
{
    Console.WriteLine("최대 사용자 수를 초과했습니다.");
}
```

이와 같이 C#에서 상수를 정의하고 사용하는 방법은 코드의 안정성과 가독성을 높이는 데 중요한 역할을 한다. 상수를 적절히 활용하면 프로그램의 유지보수성을 향상시킬 수 있다.

<!--
## C# 언어 사양
**C# 언어 사양의 중요성**  
**상수와 변수의 선언 규칙**  
**암시적 형식 지역 변수의 사용**  
-->

## C# 언어 사양

**C# 언어 사양의 중요성**  

C# 언어 사양은 C# 프로그래밍 언어의 문법, 의미, 그리고 사용 방법을 정의하는 공식 문서이다. 이 사양은 개발자들이 C#을 사용할 때 일관된 방식으로 코드를 작성할 수 있도록 돕는다. 또한, C#의 다양한 기능과 특성을 이해하는 데 중요한 역할을 한다. 언어 사양을 잘 이해하면 코드의 가독성과 유지보수성을 높일 수 있으며, 버그를 줄이는 데도 도움이 된다.

**상수와 변수의 선언 규칙**  

C#에서 변수를 선언할 때는 데이터 타입과 변수 이름을 명시해야 한다. 예를 들어, 정수형 변수를 선언할 때는 `int` 키워드를 사용하고, 변수 이름을 지정한다. 상수는 `const` 키워드를 사용하여 선언하며, 초기화 후에는 값을 변경할 수 없다. 변수와 상수를 선언할 때는 다음과 같은 규칙을 따라야 한다:

1. 변수 이름은 영문자, 숫자, 언더스코어(_)로 구성할 수 있다.
2. 변수 이름은 숫자로 시작할 수 없다.
3. 대소문자를 구별한다.
4. 예약어는 사용할 수 없다.

**암시적 형식 지역 변수의 사용**  

C#에서는 `var` 키워드를 사용하여 암시적 형식 지역 변수를 선언할 수 있다. 이 경우 컴파일러가 변수의 타입을 자동으로 추론한다. 예를 들어, 다음과 같이 사용할 수 있다:

```csharp
var number = 10; // number는 int 타입으로 추론된다.
var name = "C#"; // name은 string 타입으로 추론된다.
```

암시적 형식 지역 변수를 사용할 때는 타입이 명확한 경우에만 사용하는 것이 좋다. 그렇지 않으면 코드의 가독성이 떨어질 수 있다.

<!--
## C# 참조 변수
**참조 변수의 정의와 사용법**  
**ref와 scoped 키워드의 차이**  
**참조 반환 메서드의 예제**  
-->

## C# 참조 변수

**참조 변수의 정의와 사용법**  

C#에서 참조 변수는 객체를 가리키는 변수이다. 기본 데이터 타입(int, float 등)과 달리, 참조 변수는 메모리의 주소를 저장하고, 해당 주소에 있는 객체를 참조한다. 객체를 생성할 때는 `new` 키워드를 사용하여 메모리에 할당하고, 이 객체에 대한 참조를 변수에 저장한다. 예를 들어, 다음과 같은 코드가 있다.

```csharp
class Person
{
    public string Name { get; set; }
}

Person person = new Person();
person.Name = "홍길동";
```

위 코드에서 `person` 변수는 `Person` 객체를 참조하고 있으며, `Name` 속성에 접근할 수 있다. 참조 변수를 사용하면 객체의 상태를 변경하거나 메서드를 호출할 수 있다.

**ref와 scoped 키워드의 차이**  

C#에서는 `ref` 키워드를 사용하여 메서드에 참조 변수를 전달할 수 있다. `ref`를 사용하면 메서드 내에서 변수의 값을 변경할 수 있으며, 변경된 값은 호출한 곳에서도 반영된다. 예를 들어, 다음과 같은 코드가 있다.

```csharp
void UpdateValue(ref int number)
{
    number += 10;
}

int myNumber = 5;
UpdateValue(ref myNumber);
Console.WriteLine(myNumber); // 출력: 15
```

반면, `scoped` 키워드는 C# 7.0에서 도입된 기능으로, 변수를 특정 블록 내에서만 사용할 수 있도록 제한하는 데 사용된다. `scoped` 키워드는 주로 메모리 관리와 관련된 상황에서 유용하게 사용된다.

**참조 반환 메서드의 예제**  

C#에서는 메서드가 참조를 반환할 수 있다. 이를 통해 메서드 호출 후에도 객체의 상태를 변경할 수 있다. 다음은 참조 반환 메서드의 예제이다.

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
numberRef = 10; // numbers[0]의 값이 10으로 변경됨
```

위 코드에서 `GetNumber` 메서드는 배열의 특정 인덱스에 대한 참조를 반환한다. 이 참조를 통해 배열의 값을 직접 변경할 수 있다. 참조 반환 메서드는 성능을 향상시키고, 메모리 사용을 최적화하는 데 유용하다. 

이와 같이 C#의 참조 변수는 객체 지향 프로그래밍에서 중요한 역할을 하며, 메모리 관리와 성능 최적화에 기여한다.

<!--
## C#에서의 암시적 형식
**암시적 형식 지역 변수의 정의**  
**var 키워드의 사용 예**  
**암시적 형식의 제한 사항**  
-->

## C#에서의 암시적 형식

**암시적 형식 지역 변수의 정의**  

암시적 형식은 C#에서 변수를 선언할 때 타입을 명시하지 않고 `var` 키워드를 사용하여 컴파일러가 자동으로 타입을 추론하도록 하는 기능이다. 이 기능은 C# 3.0부터 도입되었으며, 코드의 가독성을 높이고, 타입을 명시적으로 지정할 필요가 없기 때문에 코드 작성 시 편리함을 제공한다. 

예를 들어, 다음과 같이 변수를 선언할 수 있다:

```csharp
var number = 10; // number는 int 타입으로 추론된다.
var name = "Hello"; // name은 string 타입으로 추론된다.
```

이와 같이 `var` 키워드를 사용하면, 컴파일러가 변수의 타입을 자동으로 결정하므로, 개발자는 코드 작성 시 더 간결하게 표현할 수 있다.

**var 키워드의 사용 예**  

`var` 키워드는 다양한 상황에서 유용하게 사용될 수 있다. 예를 들어, LINQ 쿼리 결과를 처리할 때, 복잡한 타입을 명시하는 대신 `var`를 사용하여 코드의 가독성을 높일 수 있다.

다음은 LINQ 쿼리에서 `var`를 사용하는 예제이다:

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

위의 코드에서 `evenNumbers`는 `List<int>` 타입으로 추론된다. 이처럼 `var`를 사용하면 코드가 간결해지고, 타입을 명시적으로 지정할 필요가 없어 코드 작성이 더 쉬워진다.

**암시적 형식의 제한 사항**  

암시적 형식은 편리하지만 몇 가지 제한 사항이 있다. 첫째, `var`를 사용할 때는 반드시 초기화와 함께 사용해야 한다. 즉, 변수를 선언할 때 타입을 추론할 수 있는 값으로 초기화해야 한다. 예를 들어, 다음과 같은 코드는 컴파일 오류를 발생시킨다:

```csharp
var x; // 오류: 'var'는 초기화가 필요하다.
```

둘째, `var`는 지역 변수에서만 사용할 수 있으며, 클래스 필드나 메서드의 반환 타입으로는 사용할 수 없다. 따라서 다음과 같은 코드는 유효하지 않다:

```csharp
var field; // 오류: 'var'는 필드 선언에 사용할 수 없다.
```

셋째, `var`를 사용하면 타입이 명확하지 않을 수 있으므로, 코드의 가독성이 떨어질 수 있는 경우도 있다. 따라서, 복잡한 타입이나 여러 타입이 혼합된 경우에는 명시적으로 타입을 지정하는 것이 좋다.

결론적으로, C#의 암시적 형식은 코드의 간결함과 가독성을 높이는 데 유용하지만, 사용 시 주의가 필요하다. 적절한 상황에서 `var`를 활용하면 효율적인 코드를 작성할 수 있다.

<!--
## C# 변수와 상수의 활용
**변수와 상수를 활용한 코드 예제**  
**상수 사용의 장점과 단점**  
-->

## C# 변수와 상수의 활용

**변수와 상수를 활용한 코드 예제**  

C#에서 변수와 상수는 프로그래밍의 기본 요소로, 다양한 상황에서 활용될 수 있다. 변수를 사용하여 데이터를 저장하고 조작할 수 있으며, 상수를 사용하여 변경되지 않는 값을 정의할 수 있다. 아래는 변수와 상수를 활용한 간단한 코드 예제이다.

```csharp
using System;

class Program
{
    const double PI = 3.14; // 상수 정의
    static void Main()
    {
        // 변수 정의 및 초기화
        double radius = 5.0;
        double area;

        // 면적 계산
        area = PI * radius * radius;

        // 결과 출력
        Console.WriteLine("반지름이 " + radius + "인 원의 면적은 " + area + "입니다.");
    }
}
```

위의 예제에서 `PI`는 상수로 정의되어 있으며, 원의 면적을 계산하는 데 사용된다. `radius`는 변수로, 사용자가 원하는 값으로 변경할 수 있다. 이처럼 변수를 사용하여 동적인 값을 처리하고, 상수를 사용하여 변하지 않는 값을 정의하는 것이 중요하다.

**상수 사용의 장점과 단점**  

상수를 사용하는 것에는 여러 가지 장점과 단점이 있다.

장점:
1. **코드의 가독성 향상**: 상수를 사용하면 코드의 의미를 명확하게 전달할 수 있다. 예를 들어, `const double PI = 3.14;`는 원주율을 나타내는 상수임을 쉽게 이해할 수 있다.
2. **오류 방지**: 상수는 변경할 수 없기 때문에, 실수로 값을 변경하는 오류를 방지할 수 있다. 이는 코드의 안정성을 높인다.
3. **유지보수 용이**: 상수를 사용하면 코드의 특정 값을 한 곳에서만 수정하면 되므로, 유지보수가 용이하다.

단점:
1. **유연성 부족**: 상수는 한 번 정의하면 변경할 수 없기 때문에, 상황에 따라 값이 변경되어야 하는 경우에는 적합하지 않다.
2. **메모리 사용**: 많은 상수를 정의하면 메모리 사용량이 증가할 수 있다. 특히, 대규모 애플리케이션에서는 상수의 수를 신중하게 관리해야 한다.

결론적으로, C#에서 변수와 상수를 적절히 활용하는 것은 코드의 품질을 높이고, 유지보수를 용이하게 하는 데 큰 도움이 된다. 프로그래머는 상황에 맞게 변수를 사용하고, 변경되지 않는 값은 상수로 정의하여 효율적인 코드를 작성해야 한다.

<!--
## 자주 묻는 질문(FAQ)
**C# 변수와 상수의 차이는 무엇인가요?**  
**C#에서 변수를 초기화하지 않으면 어떻게 되나요?**  
**readonly와 const의 차이는 무엇인가요?**  
-->

## 자주 묻는 질문(FAQ)

**C# 변수와 상수의 차이는 무엇인가요?**  

C#에서 변수는 프로그램 실행 중에 값이 변경될 수 있는 메모리 공간을 의미한다. 반면, 상수는 한 번 초기화된 후에는 그 값을 변경할 수 없는 메모리 공간을 의미한다. 즉, 변수는 동적인 값을 저장할 수 있지만, 상수는 고정된 값을 저장하는 데 사용된다. 이러한 차이로 인해 변수는 다양한 상황에서 유용하게 사용될 수 있으며, 상수는 코드의 가독성을 높이고 실수를 줄이는 데 도움을 준다.

**C#에서 변수를 초기화하지 않으면 어떻게 되나요?**  

C#에서 변수를 초기화하지 않으면, 해당 변수는 기본값으로 초기화된다. 기본값은 데이터 타입에 따라 다르며, 예를 들어 정수형(int)의 경우 0, 불리언형(bool)의 경우 false, 문자열(string)의 경우 null로 초기화된다. 그러나 로컬 변수는 초기화하지 않으면 컴파일 오류가 발생하므로, 반드시 초기화 후 사용해야 한다. 따라서 변수를 선언할 때는 항상 초기화를 고려해야 한다.

**readonly와 const의 차이는 무엇인가요?**  

`readonly`와 `const`는 모두 상수를 정의하는 데 사용되지만, 그 사용 방식과 특성이 다르다. `const`는 컴파일 타임에 값이 결정되며, 한 번 초기화된 후에는 변경할 수 없다. 반면, `readonly`는 런타임에 값을 설정할 수 있으며, 생성자에서만 초기화할 수 있다. 즉, `readonly`는 객체의 상태에 따라 다르게 초기화할 수 있는 반면, `const`는 항상 동일한 값을 유지한다. 이러한 차이로 인해 상황에 따라 적절한 키워드를 선택하여 사용하는 것이 중요하다.

<!--
## 관련 기술
**C#과 .NET의 관계**  
**C#의 데이터 타입과 변수**  
**C#의 메모리 관리와 변수**  
-->

## 관련 기술

**C#과 .NET의 관계**  

C#은 마이크로소프트에서 개발한 객체 지향 프로그래밍 언어이다. .NET은 C#을 포함한 여러 프로그래밍 언어를 지원하는 프레임워크로, 다양한 애플리케이션을 개발할 수 있는 환경을 제공한다. C#은 .NET의 주요 언어로, .NET의 기능을 최대한 활용할 수 있도록 설계되었다. .NET은 CLR(Common Language Runtime)을 통해 C# 코드의 실행을 관리하며, 다양한 라이브러리와 API를 제공하여 개발자가 효율적으로 작업할 수 있도록 돕는다. 

**C#의 데이터 타입과 변수**  

C#에서는 여러 가지 데이터 타입을 제공하여 다양한 종류의 데이터를 저장할 수 있다. 기본 데이터 타입으로는 `int`, `float`, `double`, `char`, `string`, `bool` 등이 있다. 각 데이터 타입은 메모리에서 차지하는 크기와 표현할 수 있는 값의 범위가 다르다. 변수를 선언할 때는 데이터 타입을 명시해야 하며, 예를 들어 `int age;`와 같이 사용할 수 있다. C#에서는 변수의 타입에 따라 메모리 할당이 이루어지며, 이는 성능에 큰 영향을 미칠 수 있다.

**C#의 메모리 관리와 변수**  

C#은 자동 메모리 관리를 지원하는 언어로, 가비지 컬렉션(Garbage Collection) 기능을 통해 사용하지 않는 메모리를 자동으로 회수한다. 이는 개발자가 메모리 관리를 직접 하지 않아도 되므로, 메모리 누수와 같은 문제를 줄일 수 있다. 그러나 가비지 컬렉션이 언제 발생할지는 예측할 수 없으므로, 성능에 민감한 애플리케이션에서는 메모리 사용을 최적화하는 것이 중요하다. 변수를 사용할 때는 필요하지 않은 객체를 참조하지 않도록 주의해야 하며, `using` 문을 통해 IDisposable 인터페이스를 구현한 객체를 자동으로 해제할 수 있다. 

이와 같이 C#과 .NET의 관계, 데이터 타입과 변수, 메모리 관리에 대한 이해는 C# 프로그래밍을 보다 효율적으로 수행하는 데 큰 도움이 된다.

<!--
## 결론
**C# 변수와 상수의 중요성 요약**  
**효율적인 변수 사용을 위한 팁**  
**C# 프로그래밍에서의 변수 관리의 중요성**  
---
-->

## 결론

**C# 변수와 상수의 중요성 요약**  

C#에서 변수와 상수는 프로그래밍의 기본적인 요소이다. 변수는 데이터를 저장하고 조작하는 데 사용되며, 상수는 변하지 않는 값을 저장하는 데 사용된다. 이 두 가지 요소는 프로그램의 가독성과 유지보수성을 높이는 데 중요한 역할을 한다. 변수와 상수를 적절히 활용하면 코드의 명확성을 높이고, 버그를 줄이며, 프로그램의 성능을 향상시킬 수 있다.

**효율적인 변수 사용을 위한 팁**  

효율적인 변수 사용을 위해 몇 가지 팁을 고려할 수 있다. 첫째, 변수의 이름은 의미 있게 지어야 한다. 예를 들어, `age`라는 변수는 나이를 저장하는 데 적합하지만, `a`라는 이름은 의미가 불명확하다. 둘째, 변수를 선언할 때는 가능한 한 초기화를 해주는 것이 좋다. 초기화하지 않은 변수는 예기치 않은 동작을 초래할 수 있다. 셋째, 변수를 사용할 때는 스코프를 고려해야 한다. 로컬 변수를 사용하면 메모리 사용을 최적화할 수 있다.

**C# 프로그래밍에서의 변수 관리의 중요성**  

C# 프로그래밍에서 변수 관리는 매우 중요하다. 변수의 생명주기를 이해하고, 적절한 시점에 변수를 선언하고 해제하는 것이 필요하다. 또한, 변수를 관리하는 방법에 따라 프로그램의 성능과 안정성이 크게 달라질 수 있다. 따라서, 변수와 상수를 적절히 관리하는 것은 C# 프로그래머에게 필수적인 기술이다. 

이와 같은 내용을 바탕으로 C#에서 변수와 상수를 효과적으로 활용하여 더 나은 프로그래밍을 할 수 있기를 바란다.

<!--
##### Reference #####
-->

## Reference


* [https://www.csharpstudy.com/CSharp/CSharp-variable.aspx](https://www.csharpstudy.com/CSharp/CSharp-variable.aspx)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/how-to-define-constants](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/how-to-define-constants)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/constants](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/constants)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/statements/declarations](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/statements/declarations)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/implicitly-typed-local-variables](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/implicitly-typed-local-variables)


<!--
C# 변수  
  

C# 변수는 메서드 안에서 해당 메서드의 로컬변수로 선언되거나, 혹은 클래스 안에서 클래스 내의 멤버들이 사용하는 전역적 변수(이를
필드(Field)라고 부름)로 선언될 수 있다. 로컬변수는 해당 메서드내에서만 사용되며, 메서드 호출이 끝나면 소멸된다. 반면 필드는
클래스의 객체가 살아있는 한 계속 존속하며 또한 다른 메서드들에서 필드를 참조할 수 있다. (주: 만약 필드가 정적 필드(static
field)이면 클래스 Type이 처음으로 런타임에 의해 로드될 때 해당 Type 객체(타입 메타정보를 갖는 객체)에 생성되어 프로그램이
종료될 때까지 유지된다).  
  
로컬변수는 기본값을 할당받지 못하기 때문에 반드시 사용 전에 값을 할당해야 하는 반면, 필드는 값을 할당하지 않으면, 해당 타입의 기본값이
자동으로 할당된다. 예를 들어, int 타입의 필드인 경우 기본값 0 이 할당된다.  
  
** 모든 C# 변수의 이름은 대소문자를 구별(case-sensitive)한다.  ** 예를 들어, var1 과 Var1은 서로 다른
변수이다.  
  

* * *

C# 변수 예제  
  

##  예제

    
    

    using System;

    

    namespace ConsoleApplication1

    {

        class CSVar

        {

            //필드 (클래스 내에서 공통적으로 사용되는 전역 변수)

            int globalVar;

            const int MAX = 1024;

    

            public void Method1()

            {

                // 로컬변수

                int localVar;

    

                // 아래 할당이 없으면 에러 발생

                localVar = 100;

    

                Console.WriteLine(globalVar);

                Console.WriteLine(localVar);

            }

        }

    

        class Program

        {

            // 모든 프로그램에는 Main()이 있어야 함.

            static void Main(string[] args)

            {

                // 테스트

                CSVar obj = new CSVar();

                obj.Method1();

            }

        }

    }

    

    

  * 필드 globalVar는 값을 명시적으로 할당하지 않은 경우 기본값 0 이 할당된다. 여기서 전역(Global)의 의미는 객체 (혹은 클래스) 내에서의 전역을 의미한다. 
  * 지역변수 localVar는 값을 할당하지 않고 사용하게 되면, 컴파일러 에러가 발생한다. 

* * *

C# 상수  
  

C# 상수는 C# 키워드 const를 사용하여 정의한다. C# 변수와 비슷하게 선언하는데, 다만 앞에 const를 붙여 상수임을 나타낸다.
상수와 변수의 차이점은, 변수는 프로그램 중간에 값을 변경할 수 있지만, 상수는 초기에 정한 값을 중간에 변경할 수 없다. const는 필드
선언부에서 사용되거나 메서드 내에서 사용될 수 있으며, 컴파일시 상수값이 결정된다.  
  
C# const 대신 readonly 키워드를 사용하여 읽기전용 (개념적으로 상수와 비슷한) 필드를 만들 수 있다. readonly는 필드
선언부나 클래스 생성자에서 그 값을 지정할 수 있고, 런타임시 값이 결정된다)  
  

##  예제

    
    

    using System;

    

    namespace ConsoleApplication1

    {

        class CSVar

        {

            // 상수

            const int MAX_VALUE = 1024;

    

            // readonly 필드 

            readonly int Max;

            public CSVar() 

            {

               Max = 1;

            }

            

            //...

        }

    }

    

    

* * *

본 웹사이트는 광고를 포함하고 있습니다. 광고 클릭에서 발생하는 수익금은 모두 웹사이트 서버의 유지 및 관리, 그리고 기술 콘텐츠 향상을
위해 쓰여집니다.

﻿


-->

<!--






-->

<!--
#  C#에서 상수 정의 방법

##  이 문서의 내용

상수는 해당 값이 컴파일 시간에 설정되며 변경할 수 없는 필드입니다. 상수를 사용하여 특수 값에 대해 숫자 리터럴(“매직 넘버”) 대신 의미
있는 이름을 제공할 수 있습니다.

참고 항목

C#에서는 [ #define ](../../language-reference/preprocessor-directives#defining-
symbols) 전처리기 지시문을 사용하여 일반적으로 C와 C++에서 사용되는 방식으로 상수를 정의할 수 없습니다.

정수 형식( ` int ` , ` byte ` 등)의 상수 값을 정의하려면 열거 형식을 사용합니다. 자세한 내용은 [ enum
](../../language-reference/builtin-types/enum) 을 참조하세요.

정수가 아닌 상수를 정의하는 한 가지 방법은 ` Constants ` 라는 단일 정적 클래스로 그룹화하는 것입니다. 이 경우 다음 예제와
같이 상수에 대한 모든 참조 앞에 클래스 이름이 와야 합니다.

##  예시

    
    
    static class Constants
    {
        public const double Pi = 3.14159;
        public const int SpeedOfLight = 300000; // km per sec.
    }
    
    class Program
    {
        static void Main()
        {
            double radius = 5.3;
            double area = Constants.Pi * (radius * radius);
            int secsFromSun = 149476000 / Constants.SpeedOfLight; // in km
            Console.WriteLine(secsFromSun);
        }
    }
    

클래스 이름 한정자를 통해 사용자와 상수를 사용하는 다른 사용자가 상수이며 수정할 수 없음을 쉽게 파악할 수 있습니다.

##  참고 항목


-->

<!--






-->

<!--
#  상수(C# 프로그래밍 가이드)

##  이 문서의 내용

상수는 컴파일 시간에 알려진 변경할 수 없는 값입니다. 프로그램 수명 동안 변경하지 마세요. 상수는 [ const
](../../language-reference/keywords/const) 한정자로 선언됩니다. C# [ 기본 제공 형식
](../../language-reference/builtin-types/built-in-types) 만 ` const ` 로 선언할 수
있습니다. [ String ](/ko-kr/dotnet/api/system.string) 이외의 참조 형식 상수는 [ null
](../../language-reference/keywords/null) 값으로만 초기화될 수 있습니다. 클래스, 구조체 및 배열을 비롯한
사용자 정의 형식은 ` const ` 가 될 수 없습니다. [ readonly ](../../language-
reference/keywords/readonly) 한정자를 사용하여 런타임에 한 번 초기화되고(예: 생성자에서) 그때부터는 변경할 수 없는
클래스, 구조체 또는 배열을 만듭니다.

C#에서는 ` const ` 메서드, 속성 또는 이벤트를 지원하지 않습니다.

열거형 형식을 사용하여 정수 계열 기본 제공 형식(예: ` int ` , ` uint ` , ` long ` 등)에 대한 명명된 상수를
정의할 수 있습니다. 자세한 내용은 [ enum ](../../language-reference/builtin-types/enum) 을
참조하세요.

상수는 선언될 때 초기화되어야 합니다. 예시:

    
    
    class Calendar1
    {
        public const int Months = 12;
    }
    

이 예제에서 ` Months ` 상수는 항상 12이고 클래스 자체에 의해서도 변경될 수 없습니다. 실제로 컴파일러는 C# 소스 코드에서 상수
식별자를 발견할 경우(예: ` Months ` ) 리터럴 값을 직접 컴파일러에서 생성하는 IL(중간 언어) 코드로 대체합니다. 런타임에
상수와 연결된 변수 주소가 없으므로 ` const ` 필드는 참조를 통해 전달될 수 없고 식에 l-value로 표시될 수 없습니다.

참고 항목

DLL과 같이 다른 코드에 정의된 상수 값을 참조할 경우 주의하세요. DLL의 새 버전에서 상수의 새 값을 정의할 경우 프로그램은 새 버전에
대해 다시 컴파일될 때까지 이전 리터럴 값을 포함합니다.

다음과 같이 같은 형식의 여러 상수를 동시에 선언할 수 있습니다.

    
    
    class Calendar2
    {
        public const int Months = 12, Weeks = 52, Days = 365;
    }
    

상수를 초기화하는 데 사용되는 식은 순환 참조를 만들지 않을 경우 다른 상수를 참조할 수 있습니다. 예시:

    
    
    class Calendar3
    {
        public const int Months = 12;
        public const int Weeks = 52;
        public const int Days = 365;
    
        public const double DaysPerWeek = (double) Days / (double) Weeks;
        public const double DaysPerMonth = (double) Days / (double) Months;
    }
    

상수는 [ public ](../../language-reference/keywords/public) , [ private
](../../language-reference/keywords/private) , [ protected ](../../language-
reference/keywords/protected) , [ internal ](../../language-
reference/keywords/internal) , [ protected internal ](../../language-
reference/keywords/protected-internal) 또는 [ private protected
](../../language-reference/keywords/private-protected) 로 표시될 수 있습니다. 이러한 액세스
한정자는 클래스의 사용자가 상수에 액세스하는 방법을 정의합니다. 자세한 내용은 [ 액세스 한정자 ](access-modifiers) 를
참조하세요.

형식의 모든 인스턴스에 대한 상수 값이 같으므로 상수가 [ static ](../../language-
reference/keywords/static) 필드인 것처럼 상수에 액세스합니다. 상수를 선언하는 데 ` static ` 키워드를 사용하지
않습니다. 상수를 정의하는 클래스에 포함되지 않은 식은 상수에 액세스할 때 클래스 이름, 마침표 및 상수 이름을 사용해야 합니다. 예시:

    
    
    int birthstones = Calendar.Months;
    

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../../language-reference/language-specification/readme) 을
참조하세요. 언어 사양은 C# 구문 및 사용법에 대 한 신뢰할 수 있는 소스 됩니다.

##  참고 항목


-->

<!--






-->

<!--
#  선언문

##  이 문서의 내용

선언문은 새 지역 변수, 지역 상수 또는  지역 참조 변수  를 선언합니다. 지역 변수를 선언하려면 해당 형식을 지정하고 해당 이름을
제공합니다. 다음 예제와 같이 한 문에서 동일한 형식의 여러 변수를 선언할 수 있습니다.

    
    
    string greeting;
    int a, b, c;
    List<double> xs;
    

선언문에서 초기 값을 사용하여 변수를 초기화할 수도 있습니다.

    
    
    string greeting = "Hello";
    int a = 3, b = 2, c = a + b;
    List<double> xs = new();
    

앞의 예제에서는 변수의 형식을 명시적으로 지정합니다. 컴파일러가 초기화 식에서 변수 형식을 유추하도록 할 수도 있습니다. 이렇게 하려면 형식
이름 대신 ` var ` 키워드를 사용합니다. 자세한 내용은  암시적 형식 지역 변수  섹션을 참조하세요.

지역 상수를 선언하려면 다음 예제와 같이 [ ` const ` 키워드 ](../keywords/const) 를 사용합니다.

    
    
    const string Greeting = "Hello";
    const double MinLimit = -10.0, MaxLimit = -MinLimit;
    

지역 상수도 선언할 때 초기화해야 합니다.

지역 참조 변수에 대한 자세한 내용은  참조 변수  섹션을 참조하세요.

##  암시적 형식 지역 변수

지역 변수를 선언할 때 컴파일러가 초기화 식에서 변수의 형식을 유추하도록 할 수 있습니다. 이렇게 하려면 형식 이름 대신 ` var `
키워드를 사용합니다.

    
    
    var greeting = "Hello";
    Console.WriteLine(greeting.GetType());  // output: System.String
    
    var a = 32;
    Console.WriteLine(a.GetType());  // output: System.Int32
    
    var xs = new List<double>();
    Console.WriteLine(xs.GetType());  // output: System.Collections.Generic.List`1[System.Double]
    

앞의 예제에서 알 수 있듯이 암시적 형식 지역 변수는 강력한 형식입니다.

참고 항목

활성화된 [ null 허용 인식 컨텍스트 ](../builtin-types/nullable-reference-types) 에서 ` var `
을 사용하고 초기화 식의 형식이 참조 형식인 경우 초기화 식의 형식이 null을 허용하지 않는 경우에도 컴파일러는 항상 **null 허용**
참조 형식을 유추합니다.

` var ` 은 일반적으로 [ 생성자 호출 식 ](../operators/new-operator#constructor-invocation)
과 함께 사용됩니다. ` var ` 를 사용하면 다음 예제와 같이 변수 선언 및 개체 인스턴스화에서 형식 이름을 반복하지 않을 수 있습니다.

    
    
    var xs = new List<int>();
    

[ 대상 형식 ` new ` 식 ](../operators/new-operator#target-typed-new) 을 대신 사용할 수
있습니다.

    
    
    List<int> xs = new();
    List<int>? ys = new();
    

[ 무명 형식 ](../../fundamentals/types/anonymous-types) 을 사용하는 경우 암시적 형식화 지역 변수를
사용해야 합니다. 다음 예제에서는 무명 형식을 사용하여 고객의 이름 및 전화번호를 보유하는 [ 쿼리 식 ](../keywords/query-
keywords) 을 보여줍니다.

    
    
    var fromPhoenix = from cust in customers
                      where cust.City == "Phoenix"
                      select new { cust.Name, cust.Phone };
    
    foreach (var customer in fromPhoenix)
    {
        Console.WriteLine($"Name={customer.Name}, Phone={customer.Phone}");
    }
    

앞의 예제에서는 ` fromPhoenix ` 변수의 형식을 명시적으로 지정할 수 없습니다. 형식은 [ IEnumerable<T> ](/ko-
kr/dotnet/api/system.collections.generic.ienumerable-1) 이지만 이 경우 ` T ` 는 무명
형식이므로 해당 이름을 제공할 수 없습니다. 이 때문에 ` var ` 을 사용해야 합니다. 같은 이유로 ` foreach ` 문에서 `
customer ` 반복 변수를 선언할 때 ` var ` 을 사용해야 합니다.

암시적 형식 지역 변수에 대한 자세한 내용은 [ 암시적 형식 지역 변수 ](../../programming-guide/classes-and-
structs/implicitly-typed-local-variables) 를 참조하세요.

패턴 일치에서 ` var ` 키워드는 [ ` var ` 패턴 ](../operators/patterns#var-pattern) 에
사용됩니다.

##  참조 변수

지역 변수를 선언하고 변수의 형식 앞에 ` ref ` 키워드를 추가할 때 _참조 변수_ 또는 ` ref ` 지역을 선언합니다.

    
    
    ref int aliasOfvariable = ref variable;
    

참조 변수는 _참조 대상(referent)_ 이라고 하는 다른 변수를 참조하는 변수입니다. 즉, 참조 변수는 해당 참조 대상에 대한 _별칭_
입니다. 참조 변수에 값을 할당하면 해당 값이 참조 대상에 할당됩니다. 참조 변수의 값을 읽으면 참조 대상의 값이 반환됩니다. 다음
예제에서는 해당 동작을 보여줍니다.

    
    
    int a = 1;
    ref int aliasOfa = ref a;
    Console.WriteLine($"(a, aliasOfa) is ({a}, {aliasOfa})");  // output: (a, aliasOfa) is (1, 1)
    
    a = 2;
    Console.WriteLine($"(a, aliasOfa) is ({a}, {aliasOfa})");  // output: (a, aliasOfa) is (2, 2)
    
    aliasOfa = 3;
    Console.WriteLine($"(a, aliasOfa) is ({a}, {aliasOfa})");  // output: (a, aliasOfa) is (3, 3)
    

다음 예제와 같이 [ ` ref ` 대입 연산자 ](../operators/assignment-operator#ref-assignment)
` = ref ` 를 사용하여 참조 변수의 참조 대상을 변경합니다.

    
    
    void Display(int[] s) => Console.WriteLine(string.Join(" ", s));
    
    int[] xs = [0, 0, 0];
    Display(xs);
    
    ref int element = ref xs[0];
    element = 1;
    Display(xs);
    
    element = ref xs[^1];
    element = 3;
    Display(xs);
    // Output:
    // 0 0 0
    // 1 0 0
    // 1 0 3
    

앞의 예제에서 ` element ` 참조 변수는 첫 번째 배열 요소에 대한 별칭으로 초기화됩니다. 그런 다음 마지막 배열 요소를 참조하도록
` ref ` 가 다시 할당됩니다.

` ref readonly ` 지역 변수를 정의할 수 있습니다. ` ref readonly ` 변수에는 값을 할당할 수 없습니다. 그러나
다음 예제와 같이 이러한 참조 변수를 ` ref ` 재할당할 수 있습니다.

    
    
    int[] xs = [1, 2, 3];
    
    ref readonly int element = ref xs[0];
    // element = 100;  error CS0131: The left-hand side of an assignment must be a variable, property or indexer
    Console.WriteLine(element);  // output: 1
    
    element = ref xs[^1];
    Console.WriteLine(element);  // output: 3
    

다음 예제와 같이 참조 변수에 [ 참조 반환 ](jump-statements#ref-returns) 을 할당할 수 있습니다.

    
    
    using System;
    
    public class NumberStore
    {
        private readonly int[] numbers = [1, 30, 7, 1557, 381, 63, 1027, 2550, 511, 1023];
    
        public ref int GetReferenceToMax()
        {
            ref int max = ref numbers[0];
            for (int i = 1; i < numbers.Length; i++)
            {
                if (numbers[i] > max)
                {
                    max = ref numbers[i];
                }
            }
            return ref max;
        }
    
        public override string ToString() => string.Join(" ", numbers);
    }
    
    public static class ReferenceReturnExample
    {
        public static void Run()
        {
            var store = new NumberStore();
            Console.WriteLine($"Original sequence: {store.ToString()}");
            
            ref int max = ref store.GetReferenceToMax();
            max = 0;
            Console.WriteLine($"Updated sequence:  {store.ToString()}");
            // Output:
            // Original sequence: 1 30 7 1557 381 63 1027 2550 511 1023
            // Updated sequence:  1 30 7 1557 381 63 1027 0 511 1023
        }
    }
    

앞의 예제에서 ` GetReferenceToMax ` 메서드는 참조로 반환( _return-by-ref_ ) 메서드입니다. 최대값 자체는
반환하지 않지만 최대값을 보유하는 배열 요소에 대한 별칭인 참조 반환입니다. ` Run ` 메서드는 ` max ` 참조 변수에 참조 반환을
할당합니다. 그런 다음 ` max ` 에 할당하여 ` store ` 인스턴스의 내부 스토리지를 업데이트합니다. ` ref readonly `
메서드를 정의할 수도 있습니다. ` ref readonly ` 메서드의 호출자는 해당 참조 반환에 값을 할당할 수 없습니다.

` foreach ` 문의 반복 변수는 참조 변수일 수 있습니다. 자세한 내용은 [ 반복 문 ](iteration-statements)
문서의 [ ` foreach ` 문 ](iteration-statements#the-foreach-statement) 섹션을 참조하세요.

성능이 중요한 시나리오에서 참조 변수 및 반환을 사용하면 잠재적으로 비용이 많이 들 수 있는 복사 작업을 방지하여 성능이 좋아질 수
있습니다.

컴파일러는 참조 변수가 참조 대상보다 오래 유지되지 않고 전체 수명 동안 유효한 상태를 유지하도록 합니다. 자세한 내용은 [ C# 언어 사양
](../language-specification/readme) 의 [ ref 안전 컨텍스트 ](../language-
specification/variables#972-ref-safe-contexts) 섹션을 참조하세요.

` ref ` 필드에 대한 자세한 내용은 [ ` ref ` 구조체 형식 ](../builtin-types/ref-struct) 문서의 [ `
ref ` 필드 ](../builtin-types/ref-struct#ref-fields) 섹션을 참조하세요.

##  scoped ref

상황별 키워드 ` scoped ` 는 값의 수명을 제한합니다. ` scoped ` 한정자는 [ _ref-safe-to-escape_ 또는
_safe-to-escape_ 수명 ](../keywords/method-parameters#safe-context-of-
references-and-values) 을 각각 현재 메서드로 제한합니다. 실질적으로 ` scoped ` 한정자 추가는 코드가 변수의
수명을 연장하지 않는다는 어설션입니다.

` scoped ` 는 매개 변수 또는 지역 변수에 적용할 수 있습니다. 형식이 [ ` ref struct ` ](../builtin-
types/ref-struct) 인 경우 매개 변수 및 지역 변수에 ` scoped ` 한정자를 적용할 수 있습니다. 그렇지 않으면 `
scoped ` 한정자는 지역  참조 변수  에만 적용될 수 있습니다. 여기에는 ` ref ` 한정자를 사용하여 선언된 지역 변수와 ` in
` , ` ref ` 또는 ` out ` 한정자를 사용하여 선언된 매개 변수가 포함됩니다.

` scoped ` 한정자는 형식이 ` ref struct ` 인 경우 ` struct ` 에 선언된 메서드의 ` this ` , ` out
` 매개 변수 및 ` ref ` 매개 변수에 암시적으로 추가됩니다.

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../language-specification/readme) 의 다음 섹션을 참조하세요.

` scoped ` 한정자에 대한 자세한 내용은 [ 하위 수준 구조체 개선 ](../proposals/csharp-11.0/low-
level-struct-improvements) 제안 참고 사항을 참조하세요.

##  참고 항목


-->

<!--






-->

<!--
#  암시적 형식 지역 변수(C# 프로그래밍 가이드)

##  이 문서의 내용

명시적 형식을 제공하지 않고 지역 변수를 선언할 수 있습니다. ` var ` 키워드는 초기화 문의 오른쪽에 있는 식에서 변수의 형식을
유추하도록 컴파일러에 지시합니다. 유추된 형식은 기본 제공 형식, 무명 형식, 사용자 정의 형식 또는 .NET 클래스 라이브러리에 정의된
형식일 수 있습니다. ` var ` 을 사용하여 배열을 초기화하는 방법에 대한 자세한 내용은 [ 암시적으로 형식화된 배열
](../../language-reference/builtin-types/arrays#implicitly-typed-arrays) 을
참조하세요.

다음 예제에서는 ` var ` 을 사용하여 지역 변수를 선언하는 다양한 방법을 보여 줍니다.

    
    
    // i is compiled as an int
    var i = 5;
    
    // s is compiled as a string
    var s = "Hello";
    
    // a is compiled as int[]
    var a = new[] { 0, 1, 2 };
    
    // expr is compiled as IEnumerable<Customer>
    // or perhaps IQueryable<Customer>
    var expr =
        from c in customers
        where c.City == "London"
        select c;
    
    // anon is compiled as an anonymous type
    var anon = new { Name = "Terry", Age = 34 };
    
    // list is compiled as List<int>
    var list = new List<int>();
    

` var ` 키워드는 "variant"를 의미하지 않고 변수가 느슨하게 형식화되었거나 런타임에 바인딩되었음을 나타내지도 않습니다. 단지
컴파일러가 가장 적절한 형식을 결정하고 할당함을 의미합니다.

` var ` 키워드는 다음과 같은 컨텍스트에서 사용할 수 있습니다.

  * 앞의 예제와 같이 지역 변수(메서드 범위에서 선언된 변수)에 대해 사용 

  * [ for ](../../language-reference/statements/iteration-statements#the-for-statement) 초기화 문에서 사용 
    
        for (var x = 1; x < 10; x++)
    

  * [ foreach ](../../language-reference/statements/iteration-statements#the-foreach-statement) 초기화 문에서 사용 
    
        foreach (var item in list) {...}
    

  * [ using ](../../language-reference/statements/using) 문에서 사용 
    
        using (var file = new StreamReader("C:\\myfile.txt")) {...}
    

자세한 내용은 [ 쿼리 식에서 암시적 형식 지역 변수 및 배열을 사용하는 방법 ](how-to-use-implicitly-typed-
local-variables-and-arrays-in-a-query-expression) 을 참조하세요.

##  var 및 무명 형식

대부분의 경우 ` var ` 사용은 선택 사항이며 단지 편리한 구문을 위해 사용됩니다. 그러나 변수가 무명 형식을 사용하여 초기화된 경우
나중에 개체의 속성에 액세스해야 하면 변수를 ` var ` 로 선언해야 합니다. 이것이 LINQ 쿼리 식의 일반적인 시나리오입니다. 자세한
내용은 [ 무명 형식 ](../../fundamentals/types/anonymous-types) 을 참조하세요.

소스 코드의 관점에서 무명 형식에는 이름이 없습니다. 따라서 쿼리 변수가 ` var ` 로 초기화된 경우 반환된 개체 시퀀스의 속성에
액세스하는 유일한 방법은 ` var ` 을 ` foreach ` 문의 반복 변수 형식으로 사용하는 것입니다.

    
    
    class ImplicitlyTypedLocals2
    {
        static void Main()
        {
            string[] words = { "aPPLE", "BlUeBeRrY", "cHeRry" };
    
            // If a query produces a sequence of anonymous types,
            // then use var in the foreach statement to access the properties.
            var upperLowerWords =
                 from w in words
                 select new { Upper = w.ToUpper(), Lower = w.ToLower() };
    
            // Execute the query
            foreach (var ul in upperLowerWords)
            {
                Console.WriteLine("Uppercase: {0}, Lowercase: {1}", ul.Upper, ul.Lower);
            }
        }
    }
    /* Outputs:
        Uppercase: APPLE, Lowercase: apple
        Uppercase: BLUEBERRY, Lowercase: blueberry
        Uppercase: CHERRY, Lowercase: cherry
     */
    

암시적 형식 변수 선언에는 다음과 같은 제한 사항이 적용됩니다.

  * 지역 변수가 동일한 문에서 선언 및 초기화된 경우에만 ` var ` 을 사용할 수 있습니다. 변수를 null이나 메서드 그룹 또는 익명 함수로 초기화할 수는 없습니다. 

  * 클래스 범위의 필드에는 ` var ` 을 사용할 수 없습니다. 

  * ` var ` 을 사용하여 선언된 변수는 초기화 식에 사용할 수 없습니다. 즉, 이 식( ` int i = (i = 20); ` )은 유효하지만, 이 식( ` var i = (i = 20); ` )은 컴파일 시간 오류를 생성합니다. 

  * 동일한 문에서 여러 개의 암시적 형식 변수를 초기화할 수 없습니다. 

  * ` var ` 라는 형식이 범위 내에 있으면 ` var ` 키워드가 해당 형식 이름으로 확인되고 암시적 형식 지역 변수 선언의 일부로 처리되지 않습니다. 

` var ` 키워드를 사용한 암시적 형식화는 로컬 메서드 범위의 변수에만 적용할 수 있습니다. C# 컴파일러가 코드를 처리하면서 논리적
패러독스를 만나게 되므로 암시적 형식 지정은 클래스 필드에 사용할 수 없습니다. 컴파일러는 필드 형식을 알아야 하나 할당 식을 분석할 때까지
형식을 결정할 수 없고 형식을 모르면 식을 평가할 수 없습니다. 다음 코드를 생각해 봅시다.

    
    
    private var bookTitles;
    

` bookTitles ` 는 ` var ` 형식의 클래스 필드입니다. 이 필드는 평가할 식이 없으므로 어떤 형식의 ` bookTitles
` 가 될지 컴파일러가 추론하는 것이 불가능합니다. 또한 필드에 식을 추가(로컬 변수에서처럼)하는 것으로는 부족합니다.

    
    
    private var bookTitles = new List<string>();
    

컴파일러에서 코드 컴파일 중 필드를 만나면 연결된 식을 처리하기 전에 각 필드의 형식을 기록합니다. 컴파일러가 ` bookTitles `
구문 분석을 시도하는 동일한 패러독스를 만나면 필드 형식을 알아야 하지만 컴파일러는 일반적으로 식을 분석하여 ` var ` 형식을
판단합니다. 이는 앞의 형식을 알지 못하면 불가능합니다.

` var ` 은 생성된 쿼리 변수 형식을 정확하게 확인하기 어려운 쿼리 식에서도 유용할 수 있습니다. 그룹화 및 정렬 작업에서 이러한
경우가 발생할 수 있습니다.

또한 ` var ` 키워드는 변수의 특정 형식이 키보드에서 입력하기 번거롭거나, 명확하거나, 코드의 가독성에 도움이 되지 않는 경우에 유용할
수 있습니다. 이런 방식으로 ` var ` 이 유용한 한 가지 예로 그룹 작업에 사용되는 경우 등의 중첩된 제네릭 형식이 있습니다. 다음
쿼리에서 쿼리 변수의 형식은 ` IEnumerable<IGrouping<string, Student>> ` 입니다. 사용자나 코드를 유지
관리해야 하는 다른 사용자가 이 점을 이해하기만 하면 편리하고 간단하도록 암시적 형식을 사용하는 데 문제가 없습니다.

    
    
    // Same as previous example except we use the entire last name as a key.
    // Query variable is an IEnumerable<IGrouping<string, Student>>
    var studentQuery3 =
        from student in students
        group student by student.Last;
    

` var ` 을 사용하면 코드를 간소화하는 데 도움이 되지만, 필요한 경우나 코드를 더 쉽게 읽도록 만들 때로 사용을 제한해야 합니다. `
var ` 을 제대로 사용해야 하는 경우에 대한 자세한 내용은 C# 코딩 지침 문서의 [ 암시적 형식 지역 변수
](../../fundamentals/coding-style/coding-conventions#implicitly-typed-local-
variables) 섹션을 참조하세요.

##  참고 항목


-->

<!--






-->

