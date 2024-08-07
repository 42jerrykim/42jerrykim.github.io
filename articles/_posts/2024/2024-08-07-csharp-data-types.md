---
title: "[C#] C# 데이터 타입"
categories: csharp
tags:
- CSharp
- DataTypes
- .NET
- Programming
- Coding
- SoftwareDevelopment
- Variables
- TypeSystem
- NullableTypes
- Literals
header:
teaser: /assets/images/undefined/teaser.jpg
---

C#은 .NET 프로그래밍 언어의 하나로, 다양한 데이터 타입을 지원한다. C#에서 사용되는 데이터 타입은 .NET의 Common Type System에 정의된 타입을 기반으로 하며, 이는 C# 키워드와 .NET 데이터 클래스를 통해 표현할 수 있다. 예를 들어, int, double, string과 같은 C# 키워드는 각각 System.Int32, System.Double, System.String과 같은 .NET 데이터 클래스로 매핑된다. C# 컴파일러는 이러한 키워드를 사용하여 작성된 코드를 컴파일할 때, 내부적으로 .NET 데이터 타입으로 변환한다. C#의 데이터 타입은 크게 값 타입과 참조 타입으로 나뉘며, 값 타입은 메모리에서 직접 값을 저장하고, 참조 타입은 메모리에서 데이터에 대한 참조를 저장한다. 또한, C#에서는 리터럴을 사용하여 직접 값을 지정할 수 있으며, 이때 기본 데이터 타입이 자동으로 할당된다. 특정 데이터 타입을 명시적으로 지정하고자 할 경우, 접미사를 추가하여 사용할 수 있다. 예를 들어, long 타입의 경우 'L' 접미사를 사용하고, float 타입의 경우 'F' 접미사를 사용하여 구분할 수 있다. C#은 또한 Nullable Type을 지원하여, 일반적으로 NULL을 가질 수 없는 값 타입도 NULL을 가질 수 있도록 한다. 이러한 다양한 데이터 타입과 리터럴의 사용은 C# 프로그래밍의 유연성과 강력함을 더해준다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## C# 데이터 타입
**C# 데이터 타입의 개요**  
**C# 데이터 타입의 종류**  
**C# 데이터 타입의 사용법**  
**C# 데이터 타입의 변환**

## C# 리터럴 데이터
**리터럴 데이터의 정의**  
**리터럴 데이터의 기본 타입**  
**리터럴 데이터의 접미사**  
**리터럴 데이터의 예제**

## C# 데이터 타입 예제
**기본 데이터 타입 예제**  
**리터럴 데이터 예제**  
**Nullable 타입 예제**  
**정수 숫자 형식 예제**

## C# 데이터 타입의 최대값과 최소값
**최대값과 최소값의 정의**  
**최대값과 최소값의 사용법**  
**최대값과 최소값의 예제**  
**최대값과 최소값의 중요성**

## NULL과 Nullable Type
**NULL의 정의와 사용법**  
**Nullable Type의 개념**  
**Nullable Type의 예제**  
**Nullable Type의 활용**

## C#의 정수 숫자 형식
**정수 숫자 형식의 개요**  
**정수 형식의 종류**  
**정수 리터럴의 정의**  
**정수 리터럴의 예제**

## C#의 값 형식
**값 형식의 정의**  
**값 형식의 종류**  
**값 형식의 특징**  
**값 형식의 예제**

## C#의 참조 형식
**참조 형식의 정의**  
**참조 형식의 종류**  
**참조 형식의 특징**  
**참조 형식의 예제**

## 자주 묻는 질문(FAQ)
**C# 데이터 타입에 대한 질문**  
**리터럴 데이터에 대한 질문**  
**Nullable Type에 대한 질문**  
**정수 숫자 형식에 대한 질문**

## 관련 기술
**.NET Framework**  
**C# 언어 사양**  
**Visual Studio**  
**LINQ**

## 결론
**C# 데이터 타입의 중요성 요약**  
**C# 데이터 타입의 활용 방안**  
**C# 데이터 타입의 미래 전망**  
**C# 데이터 타입 학습의 필요성**  
---
-->

<!--
---
## C# 데이터 타입
**C# 데이터 타입의 개요**  
**C# 데이터 타입의 종류**  
**C# 데이터 타입의 사용법**  
**C# 데이터 타입의 변환**
-->

## C# 데이터 타입

**C# 데이터 타입의 개요**  
C#은 강타입 언어로, 다양한 데이터 타입을 제공한다. 데이터 타입은 변수에 저장할 수 있는 값의 종류를 정의하며, 각 데이터 타입은 메모리에서 차지하는 공간과 값의 범위를 결정한다. C#의 데이터 타입은 크게 기본 데이터 타입과 사용자 정의 데이터 타입으로 나눌 수 있다.

**C# 데이터 타입의 종류**  
C#에서 제공하는 기본 데이터 타입은 다음과 같다:

- **정수형**: `int`, `long`, `short`, `byte` 등
- **부동소수점형**: `float`, `double`, `decimal`
- **문자형**: `char`
- **불리언형**: `bool`
- **문자열형**: `string`

이 외에도 C#은 배열, 리스트, 딕셔너리와 같은 컬렉션 타입을 제공하여 다양한 데이터 구조를 지원한다.

**C# 데이터 타입의 사용법**  
C#에서 데이터 타입을 사용하는 방법은 간단하다. 변수를 선언할 때 데이터 타입을 명시하고, 값을 할당하면 된다. 예를 들어, 정수형 변수를 선언하고 값을 할당하는 코드는 다음과 같다:

```csharp
int number = 10;
```

이와 같이 데이터 타입을 명시함으로써, 컴파일러는 변수의 타입에 맞는 연산을 수행할 수 있다.

**C# 데이터 타입의 변환**  
C#에서는 데이터 타입 간의 변환이 필요할 때가 있다. 이를 위해 명시적 변환과 암시적 변환을 사용할 수 있다. 예를 들어, `int`를 `double`로 변환할 때는 암시적 변환이 가능하지만, `double`을 `int`로 변환할 때는 명시적 변환이 필요하다. 다음은 변환의 예시이다:

```csharp
double pi = 3.14;
int intPi = (int)pi; // 명시적 변환
```

이와 같이 데이터 타입 변환을 통해 다양한 연산을 수행할 수 있다.

<!--
## C# 리터럴 데이터
**리터럴 데이터의 정의**  
**리터럴 데이터의 기본 타입**  
**리터럴 데이터의 접미사**  
**리터럴 데이터의 예제**
-->

## C# 리터럴 데이터

**리터럴 데이터의 정의**  
리터럴 데이터는 프로그램 코드에서 직접적으로 표현된 값을 의미한다. 즉, 변수나 상수에 할당되는 고정된 값을 말하며, C#에서는 다양한 데이터 타입에 대해 리터럴을 사용할 수 있다. 예를 들어, 정수, 실수, 문자, 문자열 등이 리터럴 데이터에 해당한다.

**리터럴 데이터의 기본 타입**  
C#에서 사용되는 기본 리터럴 데이터 타입은 다음과 같다:

- **정수 리터럴**: 10진수, 16진수, 8진수, 2진수로 표현할 수 있다. 예를 들어, `123`, `0x7B`, `0173`, `0b1111011` 등이 있다.
  
- **실수 리터럴**: 부동 소수점 숫자를 표현하며, `3.14`, `2.5e10`과 같은 형식으로 사용된다.
  
- **문자 리터럴**: 단일 문자를 표현하며, 작은 따옴표로 감싸서 사용한다. 예를 들어, `'A'`, `'1'` 등이 있다.
  
- **문자열 리터럴**: 여러 문자로 구성된 문자열을 표현하며, 큰 따옴표로 감싸서 사용한다. 예를 들어, `"Hello, World!"`와 같은 형식이다.

**리터럴 데이터의 접미사**  
C#에서는 리터럴 데이터에 접미사를 추가하여 데이터 타입을 명시할 수 있다. 예를 들어:

- `L` 또는 `l`: long 타입을 나타낸다. 예: `123456789L`
- `F` 또는 `f`: float 타입을 나타낸다. 예: `3.14F`
- `D` 또는 `d`: double 타입을 나타낸다. 예: `3.14D`
- `M` 또는 `m`: decimal 타입을 나타낸다. 예: `3.14M`

이러한 접미사를 사용하면 컴파일러가 리터럴의 타입을 명확히 인식할 수 있다.

**리터럴 데이터의 예제**  
다음은 C#에서 리터럴 데이터를 사용하는 예제이다:

```csharp
using System;

class Program
{
    static void Main()
    {
        int integerLiteral = 100; // 정수 리터럴
        double doubleLiteral = 3.14; // 실수 리터럴
        char charLiteral = 'A'; // 문자 리터럴
        string stringLiteral = "Hello, World!"; // 문자열 리터럴

        Console.WriteLine($"정수 리터럴: {integerLiteral}");
        Console.WriteLine($"실수 리터럴: {doubleLiteral}");
        Console.WriteLine($"문자 리터럴: {charLiteral}");
        Console.WriteLine($"문자열 리터럴: {stringLiteral}");
    }
}
```

위의 예제에서는 다양한 리터럴 데이터를 정의하고 출력하는 방법을 보여준다. C#에서 리터럴 데이터는 프로그램의 가독성을 높이고, 코드의 의도를 명확히 하는 데 중요한 역할을 한다.

<!--
## C# 데이터 타입 예제
**기본 데이터 타입 예제**  
**리터럴 데이터 예제**  
**Nullable 타입 예제**  
**정수 숫자 형식 예제**
-->

## C# 데이터 타입 예제

**기본 데이터 타입 예제**  

C#에서 기본 데이터 타입은 크게 값 형식과 참조 형식으로 나눌 수 있다. 값 형식은 스택에 저장되며, 참조 형식은 힙에 저장된다. 기본 데이터 타입으로는 `int`, `float`, `double`, `char`, `bool` 등이 있다. 아래는 기본 데이터 타입을 사용하는 간단한 예제이다.

```csharp
using System;

class Program
{
    static void Main()
    {
        int age = 25; // 정수형
        float height = 5.9f; // 부동소수점형
        double weight = 70.5; // 더블형
        char initial = 'A'; // 문자형
        bool isStudent = true; // 불리언형

        Console.WriteLine($"Age: {age}, Height: {height}, Weight: {weight}, Initial: {initial}, Is Student: {isStudent}");
    }
}
```

**리터럴 데이터 예제**  

리터럴 데이터는 프로그램 코드에서 직접 사용되는 고정된 값을 의미한다. C#에서는 다양한 리터럴을 지원하며, 각 데이터 타입에 맞는 리터럴을 사용할 수 있다. 아래는 리터럴 데이터의 예제이다.

```csharp
using System;

class Program
{
    static void Main()
    {
        int decimalLiteral = 100; // 10진수 리터럴
        int hexLiteral = 0x64; // 16진수 리터럴
        float floatLiteral = 3.14f; // 부동소수점 리터럴
        char charLiteral = 'Z'; // 문자 리터럴
        string stringLiteral = "Hello, World!"; // 문자열 리터럴

        Console.WriteLine($"Decimal: {decimalLiteral}, Hex: {hexLiteral}, Float: {floatLiteral}, Char: {charLiteral}, String: {stringLiteral}");
    }
}
```

**Nullable 타입 예제**  

Nullable 타입은 값 형식이 null 값을 가질 수 있도록 해주는 기능이다. C#에서는 `Nullable<T>` 구조체를 사용하여 Nullable 타입을 정의할 수 있다. 아래는 Nullable 타입을 사용하는 예제이다.

```csharp
using System;

class Program
{
    static void Main()
    {
        int? nullableInt = null; // Nullable int
        if (nullableInt.HasValue)
        {
            Console.WriteLine($"Value: {nullableInt.Value}");
        }
        else
        {
            Console.WriteLine("Value is null");
        }

        nullableInt = 10; // 값 할당
        Console.WriteLine($"Value: {nullableInt.Value}");
    }
}
```

**정수 숫자 형식 예제**  

C#에서는 다양한 정수 숫자 형식을 제공한다. `int`, `long`, `short`, `byte` 등이 있으며, 각 형식은 저장할 수 있는 값의 범위가 다르다. 아래는 정수 숫자 형식의 예제이다.

```csharp
using System;

class Program
{
    static void Main()
    {
        int intValue = 100; // 32비트 정수
        long longValue = 100000L; // 64비트 정수
        short shortValue = 30000; // 16비트 정수
        byte byteValue = 255; // 8비트 정수

        Console.WriteLine($"Int: {intValue}, Long: {longValue}, Short: {shortValue}, Byte: {byteValue}");
    }
}
```

이와 같이 C#의 데이터 타입 예제는 다양한 형태로 활용될 수 있으며, 각 데이터 타입의 특성을 이해하고 적절히 사용하는 것이 중요하다.

<!--
## C# 데이터 타입의 최대값과 최소값
**최대값과 최소값의 정의**  
**최대값과 최소값의 사용법**  
**최대값과 최소값의 예제**  
**최대값과 최소값의 중요성**
-->

## C# 데이터 타입의 최대값과 최소값

**최대값과 최소값의 정의**  

C#에서 데이터 타입은 각각의 최대값과 최소값을 가지고 있다. 이는 해당 데이터 타입이 표현할 수 있는 값의 범위를 정의하며, 프로그래밍 시 데이터의 유효성을 검사하는 데 중요한 역할을 한다. 예를 들어, `int` 타입은 -2,147,483,648부터 2,147,483,647까지의 값을 가질 수 있다. 이러한 범위를 이해하는 것은 데이터 타입을 올바르게 사용하는 데 필수적이다.

**최대값과 최소값의 사용법**  

C#에서는 `System.Int32.MaxValue`와 `System.Int32.MinValue`와 같은 속성을 사용하여 각 데이터 타입의 최대값과 최소값을 쉽게 확인할 수 있다. 이러한 속성은 코드의 가독성을 높이고, 데이터의 유효성을 검사하는 데 유용하다. 예를 들어, 사용자가 입력한 값이 `int` 타입의 범위 내에 있는지 확인할 때 이 속성을 활용할 수 있다.

```csharp
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Int32의 최대값: " + Int32.MaxValue);
        Console.WriteLine("Int32의 최소값: " + Int32.MinValue);
    }
}
```

**최대값과 최소값의 예제**  

다음은 C#에서 최대값과 최소값을 사용하는 간단한 예제이다. 이 예제에서는 사용자가 입력한 숫자가 `int` 타입의 범위 내에 있는지를 확인한다.

```csharp
using System;

class Program
{
    static void Main()
    {
        Console.Write("숫자를 입력하세요: ");
        string input = Console.ReadLine();
        int number;

        if (int.TryParse(input, out number))
        {
            if (number >= Int32.MinValue && number <= Int32.MaxValue)
            {
                Console.WriteLine("입력한 숫자는 유효한 int 값입니다.");
            }
            else
            {
                Console.WriteLine("입력한 숫자는 int 값의 범위를 초과합니다.");
            }
        }
        else
        {
            Console.WriteLine("유효한 숫자가 아닙니다.");
        }
    }
}
```

**최대값과 최소값의 중요성**  

최대값과 최소값을 이해하는 것은 프로그래밍에서 매우 중요하다. 데이터 타입의 범위를 초과하는 값을 처리할 경우, 프로그램이 예기치 않게 종료되거나 잘못된 결과를 초래할 수 있다. 따라서, 데이터 타입의 최대값과 최소값을 항상 염두에 두고 프로그래밍하는 것이 좋다. 이는 코드의 안정성을 높이고, 버그를 줄이는 데 기여한다. 

이와 같이 C#의 데이터 타입에서 최대값과 최소값을 이해하고 활용하는 것은 프로그래밍의 기본적인 요소 중 하나이다.

<!--
## NULL과 Nullable Type
**NULL의 정의와 사용법**  
**Nullable Type의 개념**  
**Nullable Type의 예제**  
**Nullable Type의 활용**
-->

## NULL과 Nullable Type

**NULL의 정의와 사용법**  

NULL은 데이터베이스나 프로그래밍 언어에서 '값이 없음'을 나타내는 특별한 값이다. C#에서는 NULL을 사용하여 객체가 참조하는 값이 없음을 나타낸다. 예를 들어, 객체 변수를 선언했지만 초기화하지 않은 경우, 해당 변수는 NULL 값을 가진다. NULL을 사용하여 조건문에서 객체의 존재 여부를 확인할 수 있다.

```csharp
string name = null;

if (name == null)
{
    Console.WriteLine("이름이 설정되지 않았습니다.");
}
```

위의 코드에서 `name` 변수가 NULL인지 확인하고, NULL일 경우 메시지를 출력한다.

**Nullable Type의 개념**  

Nullable Type은 값 형식이지만 NULL 값을 가질 수 있는 데이터 타입이다. C#에서는 기본적으로 값 형식은 NULL을 가질 수 없지만, Nullable Type을 사용하면 값 형식도 NULL을 가질 수 있다. Nullable Type은 `?` 기호를 사용하여 정의한다.

```csharp
int? age = null;
```

위의 코드에서 `age`는 Nullable Type으로 정의되었으며, NULL 값을 가질 수 있다.

**Nullable Type의 예제**  

다음은 Nullable Type을 사용하는 간단한 예제이다. 이 예제에서는 사용자의 나이를 입력받고, 나이가 NULL인지 확인한 후에 출력한다.

```csharp
int? userAge = null;

Console.WriteLine("나이를 입력하세요 (정수형): ");
string input = Console.ReadLine();

if (int.TryParse(input, out int age))
{
    userAge = age;
}

if (userAge.HasValue)
{
    Console.WriteLine($"사용자의 나이는 {userAge.Value}세입니다.");
}
else
{
    Console.WriteLine("사용자의 나이가 설정되지 않았습니다.");
}
```

위의 코드에서 사용자가 나이를 입력하면, 입력된 값이 정수형인지 확인하고, 정수형일 경우 `userAge`에 값을 할당한다. 이후 `userAge`가 NULL인지 확인하여 적절한 메시지를 출력한다.

**Nullable Type의 활용**  

Nullable Type은 데이터베이스와의 상호작용에서 유용하게 사용된다. 예를 들어, 데이터베이스에서 NULL 값을 허용하는 컬럼을 읽어올 때, C#에서는 Nullable Type을 사용하여 해당 값을 처리할 수 있다. 또한, Nullable Type은 선택적 값이나 상태를 나타내는 데에도 유용하다.

```csharp
public class User
{
    public string Name { get; set; }
    public int? Age { get; set; }
}

User user = new User { Name = "홍길동", Age = null };

if (user.Age.HasValue)
{
    Console.WriteLine($"{user.Name}의 나이는 {user.Age.Value}세입니다.");
}
else
{
    Console.WriteLine($"{user.Name}의 나이는 설정되지 않았습니다.");
}
```

위의 예제에서 `User` 클래스는 `Age` 속성을 Nullable Type으로 정의하였다. 이를 통해 사용자의 나이가 설정되지 않았을 경우에도 안전하게 처리할 수 있다. 

이와 같이 NULL과 Nullable Type은 C#에서 데이터의 유효성을 검사하고, 안전하게 값을 처리하는 데 중요한 역할을 한다.

<!--
## C#의 정수 숫자 형식
**정수 숫자 형식의 개요**  
**정수 형식의 종류**  
**정수 리터럴의 정의**  
**정수 리터럴의 예제**
-->

## C#의 정수 숫자 형식

**정수 숫자 형식의 개요**  

C#에서 정수 숫자 형식은 정수를 표현하는 데 사용되는 데이터 타입이다. 정수는 소수점이 없는 숫자를 의미하며, 다양한 범위와 크기를 가진 여러 형식으로 제공된다. 정수 숫자 형식은 주로 수학적 계산, 반복문, 조건문 등에서 많이 사용된다. C#에서는 기본적으로 4가지 주요 정수 형식이 존재하며, 각각의 형식은 메모리 사용량과 표현할 수 있는 값의 범위가 다르다.

**정수 형식의 종류**  

C#에서 제공하는 정수 형식은 다음과 같다:

1. **byte**: 0부터 255까지의 값을 가질 수 있는 8비트 부호 없는 정수 형식이다.
2. **sbyte**: -128부터 127까지의 값을 가질 수 있는 8비트 부호 있는 정수 형식이다.
3. **short**: -32,768부터 32,767까지의 값을 가질 수 있는 16비트 부호 있는 정수 형식이다.
4. **ushort**: 0부터 65,535까지의 값을 가질 수 있는 16비트 부호 없는 정수 형식이다.
5. **int**: -2,147,483,648부터 2,147,483,647까지의 값을 가질 수 있는 32비트 부호 있는 정수 형식이다.
6. **uint**: 0부터 4,294,967,295까지의 값을 가질 수 있는 32비트 부호 없는 정수 형식이다.
7. **long**: -9,223,372,036,854,775,808부터 9,223,372,036,854,775,807까지의 값을 가질 수 있는 64비트 부호 있는 정수 형식이다.
8. **ulong**: 0부터 18,446,744,073,709,551,615까지의 값을 가질 수 있는 64비트 부호 없는 정수 형식이다.

**정수 리터럴의 정의**  

정수 리터럴은 코드에서 직접적으로 정수 값을 표현하는 방법이다. C#에서는 정수 리터럴을 다양한 형식으로 표현할 수 있으며, 기본적으로 10진수, 16진수, 8진수, 2진수 형식으로 사용할 수 있다. 예를 들어, `42`는 10진수 리터럴이고, `0x2A`는 16진수 리터럴이다.

**정수 리터럴의 예제**  

다음은 C#에서 정수 리터럴을 사용하는 예제이다:

```csharp
using System;

class Program
{
    static void Main()
    {
        int decimalValue = 42; // 10진수 리터럴
        int hexValue = 0x2A;   // 16진수 리터럴
        int octalValue = 052;  // 8진수 리터럴 (C# 7.0 이전)
        int binaryValue = 0b101010; // 2진수 리터럴 (C# 7.0 이상)

        Console.WriteLine($"Decimal: {decimalValue}");
        Console.WriteLine($"Hexadecimal: {hexValue}");
        Console.WriteLine($"Octal: {octalValue}");
        Console.WriteLine($"Binary: {binaryValue}");
    }
}
```

위의 예제에서는 다양한 형식의 정수 리터럴을 정의하고 출력하는 방법을 보여준다. 각 리터럴은 해당하는 숫자 값을 표현하며, 프로그램 실행 시 콘솔에 출력된다.

<!--
## C#의 값 형식
**값 형식의 정의**  
**값 형식의 종류**  
**값 형식의 특징**  
**값 형식의 예제**
-->

## C#의 값 형식

**값 형식의 정의**  
값 형식은 데이터를 직접 저장하는 데이터 타입이다. C#에서 값 형식은 스택 메모리에 저장되며, 각 변수는 고유한 값을 가진다. 값 형식은 기본적으로 숫자, 불리언, 구조체와 같은 데이터 타입을 포함한다. 이러한 값 형식은 메모리에서 직접 값을 저장하므로, 참조 형식과는 다르게 메모리 관리가 용이하다.

**값 형식의 종류**  
C#에서 사용되는 주요 값 형식은 다음과 같다:

1. **정수형**: `int`, `long`, `short`, `byte` 등
2. **부동 소수점형**: `float`, `double`, `decimal`
3. **불리언형**: `bool`
4. **문자형**: `char`
5. **구조체**: 사용자 정의 구조체

이 외에도 C#에서는 `struct` 키워드를 사용하여 사용자 정의 값 형식을 만들 수 있다.

**값 형식의 특징**  
값 형식의 주요 특징은 다음과 같다:

- **메모리 할당**: 값 형식은 스택에 저장되며, 메모리 할당과 해제가 빠르다.
- **복사**: 값 형식의 변수를 다른 변수에 할당하면, 값이 복사된다. 즉, 두 변수는 서로 독립적이다.
- **기본값**: 값 형식은 기본적으로 0 또는 해당 타입의 기본값으로 초기화된다.
- **Nullable**: 값 형식은 `Nullable<T>`를 사용하여 null 값을 가질 수 있다.

**값 형식의 예제**  
다음은 C#에서 값 형식을 사용하는 간단한 예제이다:

```csharp
using System;

class Program
{
    static void Main()
    {
        // 정수형 값 형식
        int a = 10;
        int b = a; // 값 복사
        b = 20; // b의 값만 변경됨

        Console.WriteLine($"a: {a}, b: {b}"); // 출력: a: 10, b: 20

        // 구조체 예제
        Point point1 = new Point(1, 2);
        Point point2 = point1; // 값 복사
        point2.X = 3; // point2의 X 값만 변경됨

        Console.WriteLine($"point1: ({point1.X}, {point1.Y}), point2: ({point2.X}, {point2.Y})"); // 출력: point1: (1, 2), point2: (3, 2)
    }
}

struct Point
{
    public int X;
    public int Y;

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }
}
```

위의 예제에서 `int`와 `Point` 구조체는 값 형식으로, 변수 간의 값 복사를 통해 독립적인 값을 유지하는 것을 보여준다. 이러한 특성 덕분에 값 형식은 메모리 관리와 성능 측면에서 유리하다.

<!--
## C#의 참조 형식
**참조 형식의 정의**  
**참조 형식의 종류**  
**참조 형식의 특징**  
**참조 형식의 예제**
-->

## C#의 참조 형식

**참조 형식의 정의**  
C#에서 참조 형식은 객체를 참조하는 데이터 타입이다. 이는 메모리의 힙(heap) 영역에 저장되며, 변수는 객체의 주소를 저장한다. 참조 형식은 클래스, 배열, 인터페이스, 델리게이트 등 다양한 형태로 존재한다.

**참조 형식의 종류**  
C#에서 사용되는 주요 참조 형식은 다음과 같다:

1. **클래스 (Class)**: 객체 지향 프로그래밍의 기본 단위로, 속성과 메서드를 포함할 수 있다.
2. **배열 (Array)**: 동일한 데이터 타입의 요소를 순차적으로 저장하는 데이터 구조이다.
3. **인터페이스 (Interface)**: 클래스가 구현해야 하는 메서드의 집합을 정의한다.
4. **델리게이트 (Delegate)**: 메서드에 대한 참조를 저장할 수 있는 타입으로, 이벤트 처리에 주로 사용된다.

**참조 형식의 특징**  
참조 형식의 주요 특징은 다음과 같다:

- **메모리 관리**: 참조 형식은 힙에 저장되므로, 가비지 컬렉터가 메모리를 자동으로 관리한다.
- **값의 공유**: 여러 변수가 동일한 객체를 참조할 수 있어, 한 변수의 변경이 다른 변수에 영향을 미칠 수 있다.
- **null 값**: 참조 형식은 null 값을 가질 수 있으며, 이는 객체가 존재하지 않음을 나타낸다.

**참조 형식의 예제**  
다음은 C#에서 참조 형식을 사용하는 간단한 예제이다:

```csharp
using System;

class Person
{
    public string Name { get; set; }
}

class Program
{
    static void Main()
    {
        Person person1 = new Person();
        person1.Name = "Alice";

        // person2는 person1을 참조
        Person person2 = person1;

        // person2의 Name을 변경
        person2.Name = "Bob";

        Console.WriteLine(person1.Name); // 출력: Bob
    }
}
```

위의 예제에서 `person1`과 `person2`는 동일한 `Person` 객체를 참조하고 있다. 따라서 `person2`의 `Name` 속성을 변경하면 `person1`의 `Name` 속성도 변경된다. 이는 참조 형식의 특성을 잘 보여준다.

<!--
## 자주 묻는 질문(FAQ)
**C# 데이터 타입에 대한 질문**  
**리터럴 데이터에 대한 질문**  
**Nullable Type에 대한 질문**  
**정수 숫자 형식에 대한 질문**
-->

## 자주 묻는 질문(FAQ)

**C# 데이터 타입에 대한 질문**  

C#에서 데이터 타입은 프로그램에서 사용되는 데이터의 종류를 정의하는 중요한 요소이다. 데이터 타입은 메모리에서 데이터가 어떻게 저장되고 처리되는지를 결정한다. C#은 강타입 언어로, 변수의 데이터 타입을 명시적으로 선언해야 하며, 이는 코드의 안정성과 가독성을 높이는 데 기여한다. 

예를 들어, 정수형 데이터는 `int`로 선언하고, 문자열 데이터는 `string`으로 선언한다. 이러한 데이터 타입의 명확한 정의는 컴파일러가 타입 체크를 수행할 수 있게 하여, 런타임 오류를 줄이는 데 도움을 준다.

**리터럴 데이터에 대한 질문**  

리터럴 데이터는 코드 내에서 직접적으로 사용되는 고정된 값을 의미한다. C#에서는 다양한 리터럴 데이터 타입을 지원하며, 각 타입은 특정한 형식의 값을 나타낸다. 예를 들어, 정수 리터럴은 `123`, 부동 소수점 리터럴은 `3.14`, 문자열 리터럴은 `"Hello, World!"`와 같이 표현된다.

리터럴 데이터는 코드의 가독성을 높이고, 프로그램의 동작을 명확하게 이해할 수 있도록 돕는다. 또한, 리터럴 데이터는 변수에 할당되거나, 함수의 인자로 전달될 수 있다.

**Nullable Type에 대한 질문**  

Nullable Type은 값 형식이지만 null 값을 가질 수 있는 데이터 타입이다. C#에서는 `Nullable<T>` 구조체를 사용하여 값 형식에 null 값을 허용할 수 있다. 예를 들어, `int?`는 null 값을 가질 수 있는 정수형 변수를 선언하는 방법이다.

Nullable Type은 데이터베이스와의 상호작용에서 유용하게 사용되며, 값이 없음을 명시적으로 표현할 수 있는 방법을 제공한다. 이를 통해 코드의 안정성을 높이고, null 참조 예외를 방지할 수 있다.

**정수 숫자 형식에 대한 질문**  

C#에서 정수 숫자 형식은 다양한 크기와 범위를 가진 여러 타입으로 나뉜다. 대표적인 정수 숫자 형식으로는 `byte`, `short`, `int`, `long`이 있다. 각 타입은 저장할 수 있는 값의 범위가 다르며, 메모리 사용량도 다르다.

예를 들어, `int`는 4바이트의 메모리를 사용하며, -2,147,483,648부터 2,147,483,647까지의 값을 저장할 수 있다. 반면, `byte`는 1바이트의 메모리를 사용하며, 0부터 255까지의 값을 저장할 수 있다. 이러한 정수 숫자 형식의 선택은 프로그램의 성능과 메모리 사용에 큰 영향을 미친다. 

이와 같은 질문들은 C# 데이터 타입에 대한 이해를 높이는 데 도움을 주며, 개발자가 보다 효율적으로 코드를 작성할 수 있도록 돕는다.

<!--
## 관련 기술
**.NET Framework**  
**C# 언어 사양**  
**Visual Studio**  
**LINQ**
-->

## 관련 기술

**.NET Framework**  

.NET Framework는 Microsoft에서 개발한 소프트웨어 프레임워크로, C#을 포함한 여러 프로그래밍 언어를 지원한다. 이 프레임워크는 Windows 운영 체제에서 애플리케이션을 개발하고 실행하는 데 필요한 다양한 라이브러리와 도구를 제공한다. .NET Framework는 CLR(Common Language Runtime)을 통해 메모리 관리, 보안, 예외 처리 등의 기능을 제공하여 개발자가 보다 쉽게 애플리케이션을 개발할 수 있도록 돕는다. 

.NET Framework의 주요 구성 요소는 다음과 같다:

- **CLR (Common Language Runtime)**: .NET 애플리케이션의 실행 환경을 제공하며, 메모리 관리와 가비지 컬렉션을 담당한다.
- **BCL (Base Class Library)**: 기본적인 데이터 구조, 파일 입출력, 네트워크 통신 등을 위한 클래스 라이브러리이다.
- **ASP.NET**: 웹 애플리케이션을 개발하기 위한 프레임워크로, 동적 웹 페이지와 웹 서비스 개발을 지원한다.

**C# 언어 사양**  

C# 언어 사양은 C# 프로그래밍 언어의 문법과 기능을 정의한 문서이다. 이 문서는 C#의 기본 개념, 데이터 타입, 제어 구조, 클래스 및 객체 지향 프로그래밍의 원칙 등을 포함하고 있다. C# 언어 사양은 개발자가 C#을 효과적으로 사용할 수 있도록 돕기 위해 설계되었다.

C# 언어의 주요 특징은 다음과 같다:

- **객체 지향 프로그래밍**: C#은 클래스와 객체를 기반으로 한 객체 지향 프로그래밍 언어이다.
- **타입 안전성**: C#은 강력한 타입 시스템을 제공하여 컴파일 타임에 오류를 발견할 수 있도록 돕는다.
- **LINQ 지원**: C#은 LINQ(Language Integrated Query)를 통해 데이터 쿼리를 쉽게 작성할 수 있도록 지원한다.

**Visual Studio**  

Visual Studio는 Microsoft에서 제공하는 통합 개발 환경(IDE)으로, C#을 포함한 다양한 프로그래밍 언어를 지원한다. 이 IDE는 코드 편집기, 디버거, 빌드 도구, GUI 디자인 도구 등을 포함하여 개발자가 효율적으로 애플리케이션을 개발할 수 있도록 돕는다.

Visual Studio의 주요 기능은 다음과 같다:

- **코드 완성**: 코드 작성 시 자동으로 제안하는 기능으로, 개발자의 생산성을 높인다.
- **디버깅 도구**: 코드의 오류를 찾고 수정할 수 있는 강력한 디버깅 도구를 제공한다.
- **버전 관리 통합**: Git과 같은 버전 관리 시스템과 통합되어 팀 협업을 지원한다.

**LINQ**  

LINQ(언어 통합 쿼리)는 C#에서 데이터 쿼리를 작성하는 데 사용되는 기능으로, SQL과 유사한 구문을 사용하여 데이터베이스, XML, 컬렉션 등 다양한 데이터 소스에 대한 쿼리를 작성할 수 있다. LINQ는 코드의 가독성을 높이고, 데이터 처리 작업을 간소화하는 데 큰 도움을 준다.

LINQ의 주요 구성 요소는 다음과 같다:

- **LINQ to Objects**: 메모리 내의 객체 컬렉션에 대한 쿼리를 작성할 수 있도록 지원한다.
- **LINQ to SQL**: SQL Server 데이터베이스에 대한 쿼리를 작성할 수 있도록 지원한다.
- **LINQ to XML**: XML 데이터를 쿼리하고 조작할 수 있도록 지원한다.

이와 같은 관련 기술들은 C# 프로그래밍을 보다 효율적이고 효과적으로 수행할 수 있도록 돕는다. C# 개발자는 이러한 기술들을 잘 이해하고 활용하여 더욱 뛰어난 애플리케이션을 개발할 수 있다.

<!--
## 결론
**C# 데이터 타입의 중요성 요약**  
**C# 데이터 타입의 활용 방안**  
**C# 데이터 타입의 미래 전망**  
**C# 데이터 타입 학습의 필요성**  
---
-->

## 결론

**C# 데이터 타입의 중요성 요약**  

C# 데이터 타입은 프로그래밍에서 매우 중요한 요소이다. 데이터 타입은 변수에 저장할 수 있는 데이터의 종류를 정의하며, 이는 프로그램의 안정성과 성능에 큰 영향을 미친다. C#은 강타입 언어로, 데이터 타입을 명확히 정의해야 하며, 이를 통해 컴파일 타임에 오류를 발견할 수 있다. 따라서 데이터 타입을 올바르게 이해하고 사용하는 것은 C# 프로그래밍의 기본이자 필수적인 요소이다.

**C# 데이터 타입의 활용 방안**  

C# 데이터 타입을 활용하는 방법은 다양하다. 기본 데이터 타입을 사용하여 간단한 계산을 수행하거나, 복잡한 데이터 구조를 만들기 위해 사용자 정의 타입을 생성할 수 있다. 또한, Nullable 타입을 사용하여 데이터베이스와의 상호작용 시 null 값을 처리하는 방법을 제공한다. 이러한 다양한 활용 방안을 통해 개발자는 더 안전하고 효율적인 코드를 작성할 수 있다.

**C# 데이터 타입의 미래 전망**  

C# 데이터 타입은 앞으로도 계속 발전할 것으로 예상된다. 새로운 기능이 추가되거나 기존 기능이 개선됨에 따라 데이터 타입의 사용 방식도 변화할 것이다. 예를 들어, C# 9.0에서는 레코드 타입이 도입되어 데이터 모델링이 더욱 간편해졌다. 이러한 변화는 개발자에게 더 많은 선택권과 유연성을 제공하며, C#의 경쟁력을 높이는 데 기여할 것이다.

**C# 데이터 타입 학습의 필요성**  

C# 데이터 타입을 학습하는 것은 프로그래밍의 기초를 다지는 데 필수적이다. 데이터 타입을 이해함으로써 변수의 메모리 사용량, 성능, 그리고 코드의 가독성을 높일 수 있다. 또한, 데이터 타입에 대한 깊은 이해는 복잡한 문제를 해결하는 데 큰 도움이 된다. 따라서 C#을 배우는 모든 개발자는 데이터 타입에 대한 충분한 지식을 갖추는 것이 중요하다. 

--- 

이와 같이 C# 데이터 타입에 대한 결론을 정리할 수 있다. 데이터 타입은 프로그래밍의 기초이자 핵심 요소로, 이를 잘 이해하고 활용하는 것이 성공적인 개발의 첫걸음이다.

<!--
##### Reference #####
-->

## Reference


* [https://www.csharpstudy.com/CSharp/CSharp-datatype.aspx](https://www.csharpstudy.com/CSharp/CSharp-datatype.aspx)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/built-in-types](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/built-in-types)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/integral-numeric-types](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/integral-numeric-types)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/value-types](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/value-types)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/reference-types](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/reference-types)


<!--
C# 데이타 타입  C#을 포함한 모든 .NET 프로그래밍 언어는 [ .NET의 Common Type System ](http://msdn.microsoft.com/ko-kr/library/2hf02550\(v=VS.90\).aspx) 에 정의된 .NET 데이타 타입을 사용한다. C#은 int, double, string 과 같은 C# 키워드로 데이타 타입을 표현할 수 있으며, 또한 System.Int32, System.Double, System.String 과 같은 .NET 데이타 클래스로 데이타 타입을 표현할 수도 있다. 내부적으로는 C# 컴파일러는 C# 키워드로 된 데이타 타입을 컴파일 후 .NET 데이타 타입으로 변경하게 된다.  C# 데이타 타입  |  .NET 데이타 타입  |  설명   
---|---|---  
bool  |  System.Boolean  |  True or False   
byte  |  System.Byte  |  8비트 unsigned integer   
sbyte  |  System.SByte  |  8비트 signed integer   
short  |  System.Int16  |  16비트 signed integer   
int  |  System.Int32  |  32비트 signed integer   
long  |  System.Int64  |  64비트 signed integer   
ushort  |  System.UInt16  |  16비트 unsigned integer   
uint  |  System.UInt32  |  32비트 unsigned integer   
ulong  |  System.UInt64  |  64비트 unsigned integer   
float  |  System.Single  |  32비트 single precision 부동소수점 숫자   
double  |  System.Double  |  64비트 double precision 부동소수점 숫자   
decimal  |  System.Decimal  |  128비트 Decimal   
char  |  System.Char  |  16비트 유니코드 문자   
string  |  System.String  |  유니코드 문자열   
|  System.DateTime  |  날짜와 시간, 별도의 C# 키워드가 없음   
object  |  System.Object  |  모든 타입의 기본 클래스로 모든 유형을 포함할 수 있음   
  
* * *

C# 리터럴 데이타  C# 코드에서 123, true, "ABC"와 같이 값을 직접 써줄 수 있는데, 이를 리터럴(Literal)이라 한다.
C#에서 리터럴 데이타를 사용할 때, 별도의 접미어 표시(Suffix)가 없는 경우 C# 컴파일러는 int, double, char,
string, bool 데이타 타입에 기본적으로 그 값을 할당한다. 따라서, 특정 데이타 타입을 지정하고 싶으면, 리터럴 데이타 뒤에
1~2자의 타입 지정 접미어(Suffix)를 추가해야 한다. Suffix는 대소문자 구분이 없다. 즉 decimal을 나타내는 접미어 M은
1024M 이나 1024m처럼 사용가능하다. 아래는 디폴트 리터럴 타입과 각 데이타 타입별 Suffix에 대한 예제이다.

##  디폴트 리터럴 타입

    
    

    123    // int 리터럴

    12.3   // double 리터럴

    "A"    // string 리터럴

    'a'    // char 리터럴

    true   // bool 리터럴

    

C# 리터럴 데이타 타입  |  Suffix (대소문자 모두 가능)  |  예제   
---|---|---  
long  |  L  |  1024L   
uint  |  U  |  1024U   
ulong  |  UL  |  1024UL   
float  |  F  |  10.24F   
double  |  D  |  10.24D 또는 10.24   
decimal  |  M  |  10.24M   
  
* * *

C# 데이타 타입 예제

##  예제

    
    

    // Bool

    bool b = true;

    

    // Numeric

    short sh = -32768;   

    int i = 2147483647;  

    long l = 1234L;      // L suffix

    float f = 123.45F;   // F suffix

    double d1 = 123.45; 

    double d2 = 123.45D; // D suffix

    decimal d = 123.45M; // M suffix

    

    // Char/String

    char c = 'A';

    string s = "Hello";

    

    // DateTime  2011-10-30 12:35

    DateTime dt = new DateTime(2011, 10, 30, 12, 35, 0);

    

  * **float** 데이타 타입은 숫자 뒤에 _123.45F_ 와 같이 **F** 를 붙여 double이 아닌 float 타입임을 나타낸다. 
  * **double** 데이타 타입은 숫자 뒤에 _123.45D_ 과 같이 **D** 를 붙이거나 혹은 아무것도 붙이지 않음으로 해서 double 타입임을 나타낸다. 
  * **decimal** 데이타 타입은 숫자 뒤에 _123.45M_ 과 같이 **M** 를 붙여 decimal 타입임을 나타낸다. 
  * **char** 데이타 타입은 작은따옴표 ' (single quotation)을 사용하여 한 문자를 할당한다. 
  * **string** 데이타 타입은 큰따옴표 " (double quotation)을 사용하여 문자열을 할당한다. 

* * *

최대값, 최소값?  
  

숫자형 데이타 타입의 최대값 혹은 최소값을 알아내기 위해서는 .NET 데이타 타입 클래스들의 MaxValue, MinValue 프로퍼티를
사용한다. C# 데이타 타입 키워드 뒤에서도 이러한 프로퍼티를 직접 호출할 수 있다. 즉, int.MaxValue 혹은
Int32.MaxValue 처럼 사용할 수 있다.  
  

* * *

NULL  
  

어떤 변수가 메모리 상에 어떤 데이타도 가지고 있지 않다는 의미로서 NULL을 사용하는데, NULL을 표현하기 위하여 C# 에서는 소문자
** null  ** 이라는 키워드를 사용한다.  
  
모든 데이타 타입이 NULL을 가질 수 있는 것은 아니며, 사실 데이타 타입은 NULL을 가질 수 있는 타입 (Reference 타입)과
가질 수 없는 타입 (Value 타입)으로 구분될 수 있다.  
  
아래는 NULL을 가질 수 있는 문자열(string) 타입의 변수 s 에 null 을 할당하는 예이다.  
  

* * *

Nullable Type  
  

정수(int)나 날짜(DateTime)와 같은 [ Value Type ](CSharp-struct.aspx) 은 일반적으로 NULL을 가질
수 없다. C# 2.0에서부터 이러한 타입들에 NULL을 가질 수 있게 하였는데, 이를 **Nullable Type** 이라 부른다.  
  
C#에서 물음표(?)를 int나 DateTime 타입명 뒤에 붙이면 즉, int? 혹은 DateTime? 같이 하면 Nullable
Type이 된다. 이는 컴파일하면 .NET의 Nullable<T> 타입으로 변환된다. Nullable Type (예: int?) 을 일반
Value Type (예: int)으로 변경하기 위해서는 Nullable의 .Value 속성을 사용한다.

##  예제

    
    

    // Nullable 타입

    int? i = null;

    i = 101;

                

    bool? b = null;

    

    //int? 를 int로 할당

    Nullable<int> j = null;

    j = 10;

    int k = j.Value;

    

* * *

본 웹사이트는 광고를 포함하고 있습니다. 광고 클릭에서 발생하는 수익금은 모두 웹사이트 서버의 유지 및 관리, 그리고 기술 콘텐츠 향상을
위해 쓰여집니다.

﻿


-->

<!--






-->

<!--
GitHub에서 Microsoft와 공동 작업

이 콘텐츠의 원본은 GitHub에서 찾을 수 있으며, 여기서 문제와 끌어오기 요청을 만들고 검토할 수도 있습니다. 자세한 내용은 [ 참여자
가이드 ](https://learn.microsoft.com/contribute/content/dotnet/dotnet-contribute)
를 참조하세요.


-->

<!--






-->

<!--
#  정수 숫자 형식(C# 참조)

##  이 문서의 내용

_정수 숫자 형식_ 은 정수를 표현합니다. 모든 정수 숫자 형식은 [ 값 형식 ](value-types) 입니다. 또한 [ 단순 형식
](value-types#built-in-value-types) 이며  리터럴  로 초기화할 수 있습니다. 모든 정수 숫자 형식은 [ 산술
](../operators/arithmetic-operators) , [ 비트 논리 ](../operators/bitwise-and-
shift-operators) , [ 비교 ](../operators/comparison-operators) 및 [ 같음
](../operators/equality-operators) 연산자를 지원합니다.

##  정수 형식의 특성

C#은 다음과 같은 미리 정의된 정수 형식을 지원합니다.

C# 형식/키워드  |  범위  |  Size  |  .NET 형식   
---|---|---|---  
` sbyte ` |  -128 ~ 127  |  부호 있는 8비트 정수  |  [ System.SByte ](/ko-kr/dotnet/api/system.sbyte)  
` byte ` |  0 ~ 255  |  부호 없는 8비트 정수  |  [ System.Byte ](/ko-kr/dotnet/api/system.byte)  
` short ` |  -32,768 ~ 32,767  |  부호 있는 16비트 정수  |  [ System.Int16 ](/ko-kr/dotnet/api/system.int16)  
` ushort ` |  0 ~ 65,535  |  부호 없는 16비트 정수  |  [ System.UInt16 ](/ko-kr/dotnet/api/system.uint16)  
` int ` |  -2,147,483,648 ~ 2,147,483,647  |  부호 있는 32비트 정수  |  [ System.Int32 ](/ko-kr/dotnet/api/system.int32)  
` uint ` |  0 ~ 4,294,967,295  |  부호 없는 32비트 정수  |  [ System.UInt32 ](/ko-kr/dotnet/api/system.uint32)  
` long ` |  -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807  |  부호 있는 64비트 정수  |  [ System.Int64 ](/ko-kr/dotnet/api/system.int64)  
` ulong ` |  0 ~ 18,446,744,073,709,551,615  |  부호 없는 64비트 정수  |  [ System.UInt64 ](/ko-kr/dotnet/api/system.uint64)  
` nint ` |  플랫폼에 따라 다름(런타임에 계산됨)  |  부호 있는 32비트 또는 64비트 정수  |  [ System.IntPtr ](/ko-kr/dotnet/api/system.intptr)  
` nuint ` |  플랫폼에 따라 다름(런타임에 계산됨)  |  부호 없는 32비트 또는 64비트 정수  |  [ System.UIntPtr ](/ko-kr/dotnet/api/system.uintptr)  
  
마지막 두 개를 제외한 모든 테이블 행에서 맨 왼쪽 열의 각 C# 형식 키워드는 해당하는 .NET 형식의 별칭입니다. 키워드와 .NET 형식
이름은 서로 바꿔 사용할 수 있습니다. 예를 들어 다음 선언은 동일한 형식의 변수를 선언합니다.

    
    
    int a = 123;
    System.Int32 b = 123;
    

표의 마지막 두 행에 있는 ` nint ` 및 ` nuint ` 형식은 기본 크기 정수입니다. ` nint ` 및 ` nuint ` 상황별
키워드를 사용하여 _원시 크기의 정수_ 를 정의할 수 있습니다. 이러한 정수는 32비트 프로세스에서 실행되는 경우 32비트 정수이고 64비트
프로세스에서 실행되는 경우 64비트 정수입니다. 이들은 상호 운용성 시나리오, 하위 수준 라이브러리에 사용할 수 있고 정수 연산이 광범위하게
사용되는 시나리오에서 성능을 최적화하는 데 사용할 수 있습니다.

기본 크기 정수 형식은 내부적으로 .NET 형식 [ System.IntPtr ](/ko-kr/dotnet/api/system.intptr)
및 [ System.UIntPtr ](/ko-kr/dotnet/api/system.uintptr) 로 표시됩니다. C# 11부터 ` nint
` 및 ` nuint ` 형식은 기본 형식의 별칭입니다.

각 정수 형식의 기본값은 ` 0 ` 입니다.

각 정수 형식에는 해당 형식의 최솟값과 최댓값을 제공하는 ` MinValue ` 및 ` MaxValue ` 속성이 있습니다. 이러한 속성은
원시 크기 형식( ` nint ` 및 ` nuint ` )의 경우를 제외하고 컴파일 시간 상수입니다. ` MinValue ` 및 `
MaxValue ` 속성은 런타임에 원시 크기 형식에 대해 계산됩니다. 이러한 형식의 크기는 프로세스 설정에 따라 달라집니다.

[ System.Numerics.BigInteger ](/ko-kr/dotnet/api/system.numerics.biginteger)
구조체를 사용하여 상한 또는 하한이 없는 부호 있는 정수를 나타냅니다.

##  정수 리터럴

정수 리터럴은 다음 형식일 수 있습니다.

  * _10진_ : 접두사가 없음 
  * _16진수_ : ` 0x ` 또는 ` 0X ` 접두사 사용 
  * _이진_ : ` 0b ` 또는 ` 0B ` 접두사 포함 

다음 코드에서는 각 예제를 보여 줍니다.

    
    
    var decimalLiteral = 42;
    var hexLiteral = 0x2A;
    var binaryLiteral = 0b_0010_1010;
    

앞의 예제에서는 ` _ ` 를 _숫자 구분 기호_ 로 사용하는 예를 보여줍니다. 모든 종류의 숫자 리터럴에서 숫자 구분 기호를 사용할 수
있습니다.

정수 리터럴의 형식은 접미사로 다음과 같이 결정됩니다.

  * 리터럴에 접미사가 없는 경우 해당 형식은 값이 표현될 수 있는 ` int ` , ` uint ` , ` long ` , ` ulong ` 형식 중 첫 번째 형식입니다. 

참고 항목

리터럴은 양수 값으로 해석됩니다. 예를 들어 리터럴 ` 0xFF_FF_FF_FF ` 는 ` uint ` 형식의 숫자 ` 4294967295
` 를 나타내지만, ` int ` 형식의 숫자 ` -1 ` 과 같은 비트를 표현합니다. 특정 형식의 값이 필요한 경우 리터럴을 해당 형식으로
캐스팅합니다. 리터럴 값을 대상 유형으로 표현할 수 없는 경우 ` unchecked ` 연산자를 사용합니다. 예를 들어 `
unchecked((int)0xFF_FF_FF_FF) ` 는 ` -1 ` 을 생성합니다.

  * 리터럴에 접미사가 ` U ` 또는 ` u ` 인 경우 해당 형식은 값이 표현될 수 있는 ` uint ` , ` ulong ` 형식 중 첫 번째 형식입니다. 

  * 리터럴에 접미사가 ` L ` 또는 ` l ` 인 경우 해당 형식은 값이 표현될 수 있는 ` long ` , ` ulong ` 형식 중 첫 번째 형식입니다. 

참고 항목

소문자 ` l ` 를 접미사로 사용할 수 있습니다. 그러나 이렇게 하면 문자 ` l ` 및 숫자 ` 1 ` 을 혼동하기 쉬우므로 컴파일러
경고가 생성됩니다. 쉽게 구별할 수 있도록 ` L ` 을 사용합니다.

  * 리터럴의 접미사가 ` UL ` , ` Ul ` , ` uL ` , ` ul ` , ` LU ` , ` Lu ` , ` lU ` 또는 ` lu ` 이면 해당 형식은 ` ulong ` 입니다. 

정수 리터럴로 표시되는 값이 [ UInt64.MaxValue ](/ko-
kr/dotnet/api/system.uint64.maxvalue#system-uint64-maxvalue) 를 초과하면 컴파일 오류 [
CS1021 ](../../misc/cs1021) 이 발생합니다.

결정된 정수 리터럴 형식이 ` int ` 이고 리터럴이 나타내는 값이 대상 형식의 범위 내에 있는 경우, 해당 값이 암시적으로 ` sbyte
` , ` byte ` , ` short ` , ` ushort ` , ` uint ` , ` ulong ` , ` nint ` 또는 `
nuint ` 으로 변환될 수 있습니다.

    
    
    byte a = 17;
    byte b = 300;   // CS0031: Constant value '300' cannot be converted to a 'byte'
    

앞의 예제에서 볼 수 있듯이 리터럴의 값이 대상 형식의 범위 내에 있지 않으면 컴파일러 오류 [ CS0031
](../../misc/cs0031) 이 발생합니다.

캐스트를 사용하여 정수 리터럴로 표시되는 값을 결정된 리터럴 형식 이외의 형식으로 변환할 수도 있습니다.

    
    
    var signedByte = (sbyte)42;
    var longVariable = (long)42;
    

##  변환

모든 정수 숫자 형식을 다른 정수 숫자 형식으로 변환할 수 있습니다. 대상 형식이 소스 형식의 모든 값을 저장할 수 있는 경우 변환은
암시적입니다. 저장할 수 없는 경우에는 [ 캐스트 식 ](../operators/type-testing-and-cast#cast-
expression) 를 사용하여 명시적 변환을 수행해야 합니다. 자세한 내용은 [ 기본 제공 숫자 변환 ](numeric-
conversions) 을 참조하세요.

##  원시 크기 정수

스토리지는 대상 컴퓨터의 자연 정수 크기에 따라 결정되므로 원시 크기의 정수 형식은 특별한 동작을 갖습니다.

  * 런타임에 기본 크기 정수의 크기를 가져오려면 ` sizeof() ` 를 사용할 수 있습니다. 그러나 안전하지 않은 컨텍스트에서는 코드를 컴파일해야 합니다. 예시: 
    
        Console.WriteLine($"size of nint = {sizeof(nint)}");
    Console.WriteLine($"size of nuint = {sizeof(nuint)}");
    
    // output when run in a 64-bit process
    //size of nint = 8
    //size of nuint = 8
    
    // output when run in a 32-bit process
    //size of nint = 4
    //size of nuint = 4
    

정적 [ IntPtr.Size ](/ko-kr/dotnet/api/system.intptr.size#system-intptr-size) 및
[ UIntPtr.Size ](/ko-kr/dotnet/api/system.uintptr.size#system-uintptr-size)
속성에서 동등한 값을 가져올 수도 있습니다.

  * 런타임에 기본 크기 정수의 최소값 및 최대값을 가져오려면 다음 예제와 같이 ` MinValue ` 및 ` MaxValue ` 를 ` nint ` 및 ` nuint ` 키워드를 포함하는 정적 속성으로 사용합니다. 
    
        Console.WriteLine($"nint.MinValue = {nint.MinValue}");
    Console.WriteLine($"nint.MaxValue = {nint.MaxValue}");
    Console.WriteLine($"nuint.MinValue = {nuint.MinValue}");
    Console.WriteLine($"nuint.MaxValue = {nuint.MaxValue}");
    
    // output when run in a 64-bit process
    //nint.MinValue = -9223372036854775808
    //nint.MaxValue = 9223372036854775807
    //nuint.MinValue = 0
    //nuint.MaxValue = 18446744073709551615
    
    // output when run in a 32-bit process
    //nint.MinValue = -2147483648
    //nint.MaxValue = 2147483647
    //nuint.MinValue = 0
    //nuint.MaxValue = 4294967295
    

  * 다음 범위에서 상수 값을 사용할 수 있습니다. 

  * 컴파일러는 다른 숫자 형식으로 암시적 변환과 명시적 변환을 제공합니다. 자세한 내용은 [ 기본 제공 숫자 변환 ](numeric-conversions) 을 참조하세요. 

  * 기본 크기 정수 리터럴에 대한 직접 구문은 없습니다. ` L ` 이 ` long ` 을 나타내는 것과 같이 리터럴이 기본 크기 정수임을 나타내는 접미사는 없습니다. 대신 다른 정수 값의 암시적 또는 명시적 캐스트를 사용할 수 있습니다. 예시: 
    
        nint a = 42
    nint a = (nint)42;
    

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../language-specification/readme) 의 다음 섹션을 참조하세요.

##  참고 항목


-->

<!--






-->

<!--
#  값 형식(C# 참조)

##  이 문서의 내용

_값 형식_ 및 [ 참조 형식 ](../keywords/reference-types) 은 C# 형식의 두 가지 주요 범주입니다. 값 형식의
변수에는 형식의 인스턴스가 포함되어 있습니다. 이는 형식 인스턴스에 대한 참조를 포함하는 참조 형식의 변수와 다릅니다. 기본적으로 변수 값은
[ 할당 ](../operators/assignment-operator) 시에, 인수를 메서드에 전달할 때, 그리고 메서드 결과를 반환할 때
복사됩니다. 값 형식 변수의 경우 해당 형식 인스턴스가 복사됩니다. 다음 예제에서는 해당 동작을 보여줍니다.

    
    
    using System;
    
    public struct MutablePoint
    {
        public int X;
        public int Y;
    
        public MutablePoint(int x, int y) => (X, Y) = (x, y);
    
        public override string ToString() => $"({X}, {Y})";
    }
    
    public class Program
    {
        public static void Main()
        {
            var p1 = new MutablePoint(1, 2);
            var p2 = p1;
            p2.Y = 200;
            Console.WriteLine($"{nameof(p1)} after {nameof(p2)} is modified: {p1}");
            Console.WriteLine($"{nameof(p2)}: {p2}");
    
            MutateAndDisplay(p2);
            Console.WriteLine($"{nameof(p2)} after passing to a method: {p2}");
        }
    
        private static void MutateAndDisplay(MutablePoint p)
        {
            p.X = 100;
            Console.WriteLine($"Point mutated in a method: {p}");
        }
    }
    // Expected output:
    // p1 after p2 is modified: (1, 2)
    // p2: (1, 200)
    // Point mutated in a method: (100, 200)
    // p2 after passing to a method: (1, 200)
    

앞의 예제와 같이 값 형식 변수에 대한 작업은 변수에 저장된 값 형식의 인스턴스에만 영향을 줍니다.

값 형식이 참조 형식의 데이터 구성원을 포함하는 경우에는 값 형식 인스턴스가 복사될 때 참조 형식의 인스턴스에 대한 참조만 복사됩니다. 복사
및 원래 값 형식 인스턴스는 모두 동일한 참조 형식 인스턴스에 액세스할 수 있습니다. 다음 예제에서는 해당 동작을 보여줍니다.

    
    
    using System;
    using System.Collections.Generic;
    
    public struct TaggedInteger
    {
        public int Number;
        private List<string> tags;
    
        public TaggedInteger(int n)
        {
            Number = n;
            tags = new List<string>();
        }
    
        public void AddTag(string tag) => tags.Add(tag);
    
        public override string ToString() => $"{Number} [{string.Join(", ", tags)}]";
    }
    
    public class Program
    {
        public static void Main()
        {
            var n1 = new TaggedInteger(0);
            n1.AddTag("A");
            Console.WriteLine(n1);  // output: 0 [A]
    
            var n2 = n1;
            n2.Number = 7;
            n2.AddTag("B");
    
            Console.WriteLine(n1);  // output: 0 [A, B]
            Console.WriteLine(n2);  // output: 7 [A, B]
        }
    }
    

참고 항목

코드를 오류가 덜 발생하고 더 강력하게 만들려면 변경할 수 없는 값 형식을 정의 및 사용합니다. 이 문서에서는 데모용으로만 변경 가능한 값
형식을 사용합니다.

##  값 형식 및 형식 제약 조건의 종류

값 형식은 다음 두 가지 중 하나일 수 있습니다.

  * 데이터 및 관련 기능을 캡슐화하는 [ 구조 형식 ](struct)
  * 명명된 상수 집합으로 정의되고 선택 사항 또는 선택 사항의 조합을 나타내는 [ 열거 형식 ](enum)

기본 값 형식 ` T ` 의 모든 값과 추가 [ Null ](../keywords/null) 값을 나타내는 [ 값 형식 ](nullable-
value-types) ` T? ` Null 허용 값 형식인 경우를 제외하고는 값 형식의 변수에 ` null ` 을 할당할 수 없습니다.

[ ` struct ` 제약 조건 ](../../programming-guide/generics/constraints-on-type-
parameters) 을 사용하여 형식 매개 변수가 null을 허용하지 않는 값 형식이라고 지정할 수 있습니다. 구조체 형식과 열거형 형식
모두 ` struct ` 제약 조건을 충족합니다. 기본 클래스 제약 조건( [ 열거형 제약 조건 ](../../programming-
guide/generics/constraints-on-type-parameters#enum-constraints) 이라고 함)에서 `
System.Enum ` 을 사용하여 형식 매개 변수가 열거형 형식이라고 지정할 수 있습니다.

##  기본 제공 값 형식

C#은 _단순 형식_ 이라고도 하는 다음과 같은 기본 제공 값 형식을 제공합니다.

모든 단순 형식은 구조체 형식이며, 특정 추가 작업을 허용한다는 점에서 다른 구조체 형식과 다릅니다.

  * 리터럴을 사용하여 단순 형식의 값을 제공할 수 있습니다. 예를 들어 ` 'A' ` 는 ` char ` 형식의 리터럴이고, ` 2001 ` 은 ` int ` 형식의 리터럴입니다. 

  * [ const ](../keywords/const) 키워드를 사용하여 단순 형식의 상수를 선언할 수 있습니다. 다른 구조체 형식의 상수는 포함할 수 없습니다. 

  * 해당 피연산자가 모두 단순 형식의 상수인 상수 식은 컴파일 시간에 계산됩니다. 

[ 값 튜플 ](value-tuples) 은 단순 형식이 아닌 값 형식입니다.

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../language-specification/readme) 의 다음 섹션을 참조하세요.

##  참고 항목


-->

<!--






-->

<!--
#  참조 형식(C# 참조)

##  이 문서의 내용

C# 형식은 참조 형식과 값 형식 두 가지가 있습니다. 참조 형식의 변수에는 데이터(개체)에 대한 참조가 저장되며, 값 형식의 변수에는 해당
데이터가 직접 포함됩니다. 참조 형식에서는 두 가지 변수가 같은 개체를 참조할 수 있으므로 한 변수에 대한 작업이 다른 변수에서 참조하는
개체에 영향을 미칠 수 있습니다. 값 형식에서는 각 변수에 데이터의 자체 사본이 들어 있으며 한 변수의 작업이 다른 변수에 영향을 미칠 수
없습니다( ` in ` , ` ref ` 및 ` out ` 매개 변수 제외. [ in ](method-parameters#in-
parameter-modifier) , [ ref ](ref) 및 [ out ](method-parameters#out-parameter-
modifier) 매개 변수 한정자 참조).

다음 키워드는 참조 형식을 선언하는 데 사용됩니다.

C#는 다음과 같은 기본 참조 형식도 제공합니다.

##  참고 항목


-->

<!--






-->

