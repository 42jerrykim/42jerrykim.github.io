---
image: "tmp_wordcloud.png"
categories: CSharp
date: "2024-08-14T00:00:00Z"
header: null

tags:
- CSharp
- .NET
- programming
- SoftwareDevelopment
- object-oriented
- cross-platform
- open-source
- coding
- ProgrammingLanguages
- SoftwareEngineering
- ApplicationDevelopment
- performance
- productivity
- MemoryManagement
- GarbageCollection
- AsynchronousProgramming
- LINQ
- C# features
- C# history
- C# syntax
- C# applications
- C# tutorials
- C# examples
- C# libraries
- C# frameworks
- C# community
- C# tools
- C# IDE
- C# best practices
- C# for beginners
- C# advanced
- C# development
- C# programming concepts
- C# design patterns
- C# coding standards
- C# error handling
- C# debugging
- C# performance optimization
- C# web development
- C# mobile development
- C# game development
- C# cloud development
- C# IoT development
- C# data structures
- C# algorithms
- C# testing
- C# versioning
- C# updates
- C# community resources
- C# job market
- C# career
teaser: /assets/images/undefined/teaser.jpg
title: '[C#] C# 언어 둘러보기'
---

C# 언어는 마이크로소프트에서 개발한 객체 지향 프로그래밍 언어로, .NET 플랫폼에서 실행되는 다양한 응용 프로그램을 작성하는 데 사용된다. C#은 강력한 형식의 언어로, 메모리 관리를 자동으로 수행하며, 비동기 프로그래밍과 같은 현대적인 프로그래밍 패러다임을 지원한다. 이 언어는 C, C++, Java와 유사한 문법을 가지고 있어 기존의 프로그래머들이 쉽게 접근할 수 있도록 설계되었다. C#은 데스크톱, 웹, 모바일, 게임 등 다양한 분야에서 활용될 수 있으며, 특히 .NET 생태계와의 통합으로 인해 강력한 라이브러리와 도구를 활용할 수 있는 장점이 있다. C#의 발전은 지속적으로 이루어지고 있으며, 최신 버전에서는 LINQ, 비동기 프로그래밍, 제네릭 등 다양한 기능이 추가되어 개발자의 생산성을 높이고 있다. C#은 전 세계적으로 많은 개발자들에게 사랑받고 있으며, 그 이유는 간결한 문법과 강력한 기능 덕분이다. C#을 배우는 것은 현대 소프트웨어 개발의 기초를 다지는 데 큰 도움이 될 것이다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
# C# 언어 둘러보기 블로그 포스트 아웃라인

---

## C# 언어 소개
**C#의 역사와 발전**  
**C#의 주요 특징**  
**C#의 사용 사례**  
**C#의 장점과 단점**  

## C# 기본 문법
**변수와 데이터 타입**  
**제어문**  
**함수와 메서드**  
**클래스와 객체 지향 프로그래밍**  

## C#의 고급 기능
**LINQ(언어 통합 쿼리)**  
**비동기 프로그래밍**  
**제네릭 프로그래밍**  
**패턴 매칭**  

## C#과 .NET 플랫폼
**.NET 플랫폼 개요**  
**C#과 .NET의 관계**  
**.NET의 구성 요소**  
**.NET의 다양한 변형**  

## C# 실습 예제
**Hello World 프로그램 작성**  
**간단한 계산기 프로그램**  
**파일 입출력 예제**  
**비동기 웹 요청 예제**  

## 자주 묻는 질문(FAQ)
**C#은 어떤 용도로 사용되나요?**  
**C#의 장점은 무엇인가요?**  
**C#과 Java의 차이점은 무엇인가요?**  
**C#을 배우기 위한 추천 자료는 무엇인가요?**  

## 관련 기술
**ASP.NET**  
**Entity Framework**  
**Xamarin**  
**Unity**  

## 결론
**C#의 중요성과 미래**  
**C#을 배우는 것이 왜 중요한가**  
**C# 커뮤니티와 리소스**  

--- 

이 아웃라인은 C# 언어에 대한 포괄적인 이해를 제공하며, 각 섹션은 독자가 C#의 기본 개념부터 고급 기능까지 쉽게 이해할 수 있도록 구성되어 있습니다.
-->

<!--
## C# 언어 소개
**C#의 역사와 발전**  
**C#의 주요 특징**  
**C#의 사용 사례**  
**C#의 장점과 단점**  
-->

## C# 언어 소개

**C#의 역사와 발전**  

C#은 2000년 마이크로소프트에 의해 개발된 객체 지향 프로그래밍 언어이다. C#은 .NET 프레임워크의 일환으로 설계되었으며, C++와 Java의 장점을 결합하여 개발되었다. C#은 처음 발표된 이후로 지속적으로 발전해왔으며, 현재는 C# 10.0 버전까지 출시되었다. C#은 다양한 플랫폼에서 사용할 수 있도록 설계되었으며, 특히 웹, 모바일, 데스크탑 애플리케이션 개발에 널리 사용된다.

**C#의 주요 특징**  

C#은 다음과 같은 주요 특징을 가지고 있다. 첫째, 강력한 타입 시스템을 제공하여 코드의 안정성을 높인다. 둘째, 객체 지향 프로그래밍을 지원하여 코드의 재사용성과 유지보수성을 향상시킨다. 셋째, LINQ(언어 통합 쿼리)를 통해 데이터 쿼리를 간편하게 수행할 수 있다. 넷째, 비동기 프로그래밍을 지원하여 효율적인 멀티스레딩을 가능하게 한다. 이러한 특징들은 C#을 현대적인 프로그래밍 언어로 만들어준다.

**C#의 사용 사례**  

C#은 다양한 분야에서 사용된다. 웹 개발에서는 ASP.NET을 사용하여 동적인 웹 애플리케이션을 구축할 수 있다. 게임 개발에서는 Unity 엔진을 통해 2D 및 3D 게임을 만들 수 있다. 또한, 데스크탑 애플리케이션 개발에서는 WPF(Windows Presentation Foundation)와 WinForms를 사용하여 사용자 인터페이스를 설계할 수 있다. 이러한 다양한 사용 사례는 C#의 유연성과 강력함을 보여준다.

**C#의 장점과 단점**  

C#의 장점으로는 강력한 타입 시스템, 객체 지향 프로그래밍 지원, 다양한 라이브러리와 프레임워크, 그리고 활발한 커뮤니티가 있다. 그러나 단점으로는 Windows 플랫폼에 최적화되어 있어 다른 플랫폼에서의 호환성이 떨어질 수 있으며, 상대적으로 높은 학습 곡선이 있을 수 있다. 이러한 장단점을 고려하여 C#을 선택하는 것이 중요하다.

<!--
## C# 기본 문법
**변수와 데이터 타입**  
**제어문**  
**함수와 메서드**  
**클래스와 객체 지향 프로그래밍**  
-->

## C# 기본 문법

**변수와 데이터 타입**  

C#에서 변수는 데이터를 저장하는 공간이다. 변수를 선언할 때는 데이터 타입을 명시해야 하며, C#은 강타입 언어이기 때문에 변수의 타입을 명확히 지정해야 한다. 기본 데이터 타입으로는 `int`, `float`, `double`, `char`, `string`, `bool` 등이 있다. 예를 들어, 정수를 저장하고 싶다면 다음과 같이 변수를 선언할 수 있다.

```csharp
int number = 10;
```

이와 같이 변수를 선언하고 초기화하면, 이후에 해당 변수를 사용하여 다양한 연산을 수행할 수 있다. 데이터 타입에 따라 사용할 수 있는 연산이 다르므로, 적절한 데이터 타입을 선택하는 것이 중요하다.

**제어문**  

C#에서는 프로그램의 흐름을 제어하기 위해 다양한 제어문을 제공한다. 가장 기본적인 제어문으로는 조건문과 반복문이 있다. 조건문으로는 `if`, `else if`, `else`, `switch`가 있으며, 반복문으로는 `for`, `while`, `do while`이 있다. 예를 들어, `if` 문을 사용하여 조건에 따라 다른 코드를 실행할 수 있다.

```csharp
if (number > 0)
{
    Console.WriteLine("양수입니다.");
}
else
{
    Console.WriteLine("음수입니다.");
}
```

이와 같이 제어문을 사용하면 프로그램의 흐름을 유연하게 조정할 수 있다.

**함수와 메서드**  

C#에서 함수는 특정 작업을 수행하는 코드 블록이다. 함수는 재사용성을 높이고 코드의 가독성을 향상시키기 위해 사용된다. C#에서는 메서드라는 용어를 주로 사용하며, 메서드는 클래스 내에 정의된다. 메서드를 정의할 때는 반환 타입, 메서드 이름, 매개변수를 명시해야 한다. 예를 들어, 두 수를 더하는 메서드는 다음과 같이 정의할 수 있다.

```csharp
public int Add(int a, int b)
{
    return a + b;
}
```

이 메서드는 두 개의 정수를 매개변수로 받아서 그 합을 반환한다. 메서드를 호출할 때는 다음과 같이 사용할 수 있다.

```csharp
int result = Add(5, 10);
```

**클래스와 객체 지향 프로그래밍**  

C#은 객체 지향 프로그래밍(OOP) 언어로, 클래스와 객체를 기반으로 한다. 클래스는 객체의 설계도이며, 객체는 클래스의 인스턴스이다. 클래스는 속성과 메서드를 포함할 수 있으며, 이를 통해 데이터와 기능을 묶어 관리할 수 있다. 예를 들어, `Car`라는 클래스를 정의할 수 있다.

```csharp
public class Car
{
    public string Model { get; set; }
    public int Year { get; set; }

    public void Drive()
    {
        Console.WriteLine("차가 운전 중입니다.");
    }
}
```

이와 같이 클래스를 정의한 후, 객체를 생성하여 사용할 수 있다.

```csharp
Car myCar = new Car();
myCar.Model = "소나타";
myCar.Year = 2020;
myCar.Drive();
```

이처럼 C#의 기본 문법을 이해하면, 프로그래밍의 기초를 다질 수 있다. C#은 강력한 기능을 제공하며, 다양한 응용 프로그램을 개발하는 데 유용한 언어이다.

<!--
## C#의 고급 기능
**LINQ(언어 통합 쿼리)**  
**비동기 프로그래밍**  
**제네릭 프로그래밍**  
**패턴 매칭**  
-->

## C#의 고급 기능

**LINQ(언어 통합 쿼리)**  

LINQ는 C#에서 데이터 쿼리를 보다 간편하게 작성할 수 있도록 도와주는 기능이다. LINQ를 사용하면 데이터베이스, XML, 컬렉션 등 다양한 데이터 소스에 대해 일관된 방식으로 쿼리를 작성할 수 있다. LINQ의 주요 장점은 코드의 가독성을 높이고, 복잡한 쿼리를 간단하게 표현할 수 있다는 점이다. 예를 들어, 다음은 LINQ를 사용하여 리스트에서 짝수만 필터링하는 코드이다.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
        var evenNumbers = numbers.Where(n => n % 2 == 0);

        foreach (var number in evenNumbers)
        {
            Console.WriteLine(number);
        }
    }
}
```

**비동기 프로그래밍**  

비동기 프로그래밍은 프로그램의 성능을 향상시키고, 사용자 경험을 개선하는 데 중요한 역할을 한다. C#에서는 `async`와 `await` 키워드를 사용하여 비동기 메서드를 쉽게 작성할 수 있다. 비동기 프로그래밍을 통해 I/O 작업이나 네트워크 요청을 수행하는 동안 프로그램이 멈추지 않고 다른 작업을 계속 수행할 수 있다. 다음은 비동기 메서드를 사용하는 예제이다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        string result = await FetchDataAsync("https://api.example.com/data");
        Console.WriteLine(result);
    }

    static async Task<string> FetchDataAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }
}
```

**제네릭 프로그래밍**  

제네릭은 코드의 재사용성을 높이고, 타입 안전성을 제공하는 기능이다. C#에서 제네릭을 사용하면 다양한 데이터 타입에 대해 동일한 로직을 적용할 수 있다. 예를 들어, 제네릭 클래스를 사용하여 리스트를 구현할 수 있다. 다음은 제네릭 클래스를 사용하는 예제이다.

```csharp
using System;
using System.Collections.Generic;

class GenericList<T>
{
    private List<T> items = new List<T>();

    public void Add(T item)
    {
        items.Add(item);
    }

    public T Get(int index)
    {
        return items[index];
    }
}

class Program
{
    static void Main()
    {
        GenericList<int> intList = new GenericList<int>();
        intList.Add(1);
        Console.WriteLine(intList.Get(0));
        
        GenericList<string> stringList = new GenericList<string>();
        stringList.Add("Hello");
        Console.WriteLine(stringList.Get(0));
    }
}
```

**패턴 매칭**  

C# 7.0부터 도입된 패턴 매칭은 조건문을 보다 간결하게 작성할 수 있도록 도와주는 기능이다. 패턴 매칭을 사용하면 객체의 타입이나 속성에 따라 조건을 검사할 수 있다. 다음은 패턴 매칭을 사용하는 예제이다.

```csharp
using System;

class Program
{
    static void Main()
    {
        object obj = "Hello, World!";
        
        if (obj is string str)
        {
            Console.WriteLine($"String length: {str.Length}");
        }
        else
        {
            Console.WriteLine("Not a string");
        }
    }
}
```

이와 같이 C#의 고급 기능들은 개발자가 보다 효율적이고 간결한 코드를 작성할 수 있도록 도와준다. 이러한 기능들을 잘 활용하면 복잡한 문제를 해결하는 데 큰 도움이 된다.

<!--
## C#과 .NET 플랫폼
**.NET 플랫폼 개요**  
**C#과 .NET의 관계**  
**.NET의 구성 요소**  
**.NET의 다양한 변형**  
-->

## C#과 .NET 플랫폼

**.NET 플랫폼 개요**  

.NET 플랫폼은 마이크로소프트에서 개발한 소프트웨어 프레임워크로, 다양한 프로그래밍 언어를 지원하며, 특히 C#과 함께 많이 사용된다. 이 플랫폼은 개발자가 애플리케이션을 쉽게 만들 수 있도록 다양한 라이브러리와 도구를 제공한다. .NET 플랫폼은 웹, 데스크톱, 모바일, 클라우드 등 다양한 환경에서 애플리케이션을 개발할 수 있는 기능을 제공한다. 

.NET 플랫폼은 CLR(Common Language Runtime)이라는 실행 환경을 통해 다양한 언어로 작성된 코드를 실행할 수 있도록 지원한다. CLR은 메모리 관리, 예외 처리, 보안 등을 담당하여 개발자가 애플리케이션의 로직에 집중할 수 있게 해준다. 

**C#과 .NET의 관계**  

C#은 .NET 플랫폼에서 가장 널리 사용되는 프로그래밍 언어 중 하나이다. C#은 객체 지향 프로그래밍 언어로, .NET의 다양한 기능을 활용하여 강력하고 효율적인 애플리케이션을 개발할 수 있도록 설계되었다. C#은 .NET의 라이브러리와 API를 통해 데이터베이스와의 상호작용, 웹 서비스 호출, 사용자 인터페이스 구성 등 다양한 작업을 쉽게 수행할 수 있다. 

C#과 .NET의 관계는 매우 밀접하며, C#을 배우는 것은 .NET 플랫폼을 효과적으로 활용하는 데 필수적이다. C#의 문법과 개념을 이해하면 .NET의 다양한 기능을 보다 쉽게 사용할 수 있다. 

**.NET의 구성 요소**  

.NET 플랫폼은 여러 구성 요소로 이루어져 있다. 주요 구성 요소는 다음과 같다:

1. **CLR (Common Language Runtime)**: .NET 애플리케이션의 실행 환경으로, 메모리 관리, 스레드 관리, 예외 처리 등을 담당한다.
   
2. **BCL (Base Class Library)**: .NET에서 제공하는 기본 클래스 라이브러리로, 파일 입출력, 데이터베이스 연결, XML 처리 등 다양한 기능을 제공한다.
   
3. **ASP.NET**: 웹 애플리케이션을 개발하기 위한 프레임워크로, 동적 웹 페이지, 웹 API, MVC 패턴 등을 지원한다.
   
4. **Entity Framework**: 데이터베이스와의 상호작용을 쉽게 해주는 ORM(Object-Relational Mapping) 프레임워크이다.
   
5. **Xamarin**: 모바일 애플리케이션 개발을 위한 프레임워크로, C#을 사용하여 iOS와 Android 애플리케이션을 동시에 개발할 수 있다.

**.NET의 다양한 변형**  

.NET 플랫폼은 다양한 변형으로 제공되어, 개발자가 필요에 따라 선택할 수 있다. 주요 변형은 다음과 같다:

1. **.NET Framework**: 전통적인 Windows 애플리케이션과 웹 애플리케이션을 개발하기 위한 플랫폼이다. 주로 데스크톱 애플리케이션에 사용된다.
   
2. **.NET Core**: 크로스 플랫폼을 지원하는 경량화된 버전의 .NET으로, Windows, macOS, Linux에서 실행할 수 있다. 클라우드 기반 애플리케이션 개발에 적합하다.
   
3. **.NET 5/6**: .NET Core의 후속 버전으로, 모든 플랫폼에서 통합된 개발 환경을 제공한다. 최신 기능과 성능 개선이 포함되어 있다.
   
4. **Xamarin**: 모바일 애플리케이션 개발을 위한 .NET의 변형으로, C#을 사용하여 iOS와 Android 애플리케이션을 동시에 개발할 수 있다.

이와 같이 .NET 플랫폼은 다양한 환경과 요구에 맞춰 여러 변형으로 제공되며, C#과 함께 사용될 때 강력한 개발 도구가 된다.

<!--
## C# 실습 예제
**Hello World 프로그램 작성**  
**간단한 계산기 프로그램**  
**파일 입출력 예제**  
**비동기 웹 요청 예제**  
-->

## C# 실습 예제

**Hello World 프로그램 작성**  

C#에서 가장 기본적인 프로그램은 "Hello World"를 출력하는 것이다. 이 프로그램은 C#의 기본 문법을 이해하는 데 큰 도움이 된다. 아래는 Hello World 프로그램의 예제 코드이다.

```csharp
using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
```

위 코드를 실행하면 콘솔에 "Hello, World!"라는 메시지가 출력된다. 이 프로그램은 C#의 기본적인 구조를 보여주며, `using System;`은 시스템 네임스페이스를 포함하여 콘솔 입출력을 가능하게 한다. `Main` 메서드는 프로그램의 시작점이며, `Console.WriteLine` 메서드는 문자열을 콘솔에 출력하는 역할을 한다.

**간단한 계산기 프로그램**  

이제 간단한 계산기 프로그램을 작성해 보자. 이 프로그램은 두 숫자를 입력받아 사칙연산을 수행하는 기능을 가진다. 아래는 계산기 프로그램의 예제 코드이다.

```csharp
using System;

class Calculator
{
    static void Main(string[] args)
    {
        Console.WriteLine("첫 번째 숫자를 입력하세요:");
        double num1 = Convert.ToDouble(Console.ReadLine());

        Console.WriteLine("두 번째 숫자를 입력하세요:");
        double num2 = Convert.ToDouble(Console.ReadLine());

        Console.WriteLine("연산을 선택하세요: +, -, *, /");
        string operation = Console.ReadLine();

        double result = 0;

        switch (operation)
        {
            case "+":
                result = num1 + num2;
                break;
            case "-":
                result = num1 - num2;
                break;
            case "*":
                result = num1 * num2;
                break;
            case "/":
                if (num2 != 0)
                {
                    result = num1 / num2;
                }
                else
                {
                    Console.WriteLine("0으로 나눌 수 없습니다.");
                    return;
                }
                break;
            default:
                Console.WriteLine("잘못된 연산입니다.");
                return;
        }

        Console.WriteLine($"결과: {result}");
    }
}
```

이 프로그램은 사용자로부터 두 개의 숫자와 연산자를 입력받아 결과를 출력한다. `switch` 문을 사용하여 선택된 연산에 따라 결과를 계산하고, 0으로 나누는 경우를 처리하여 오류를 방지한다.

**파일 입출력 예제**  

C#에서는 파일 입출력을 통해 데이터를 저장하고 읽어올 수 있다. 아래는 텍스트 파일에 데이터를 쓰고 읽는 예제 코드이다.

```csharp
using System;
using System.IO;

class FileIOExample
{
    static void Main(string[] args)
    {
        string filePath = "example.txt";

        // 파일에 데이터 쓰기
        using (StreamWriter writer = new StreamWriter(filePath))
        {
            writer.WriteLine("Hello, File!");
            writer.WriteLine("C# 파일 입출력 예제입니다.");
        }

        // 파일에서 데이터 읽기
        using (StreamReader reader = new StreamReader(filePath))
        {
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                Console.WriteLine(line);
            }
        }
    }
}
```

위 코드는 `example.txt`라는 파일에 두 줄의 텍스트를 작성한 후, 다시 그 파일을 읽어 콘솔에 출력하는 예제이다. `StreamWriter`를 사용하여 파일에 데이터를 쓰고, `StreamReader`를 사용하여 파일에서 데이터를 읽는다.

**비동기 웹 요청 예제**  

C#에서는 비동기 프로그래밍을 통해 웹 요청을 효율적으로 처리할 수 있다. 아래는 비동기 방식으로 웹 페이지의 내용을 가져오는 예제 코드이다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class AsyncWebRequest
{
    static async Task Main(string[] args)
    {
        string url = "https://www.example.com";

        using (HttpClient client = new HttpClient())
        {
            try
            {
                string response = await client.GetStringAsync(url);
                Console.WriteLine(response);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"오류 발생: {ex.Message}");
            }
        }
    }
}
```

이 프로그램은 `HttpClient`를 사용하여 지정된 URL의 내용을 비동기적으로 가져온다. `await` 키워드를 사용하여 비동기 작업이 완료될 때까지 기다리며, 오류가 발생할 경우 예외를 처리한다. 비동기 프로그래밍을 통해 UI가 멈추지 않고 부드럽게 작동할 수 있다.

<!--
## 자주 묻는 질문(FAQ)
**C#은 어떤 용도로 사용되나요?**  
**C#의 장점은 무엇인가요?**  
**C#과 Java의 차이점은 무엇인가요?**  
**C#을 배우기 위한 추천 자료는 무엇인가요?**  
-->

## 자주 묻는 질문(FAQ)

**C#은 어떤 용도로 사용되나요?**  

C#은 다양한 용도로 사용되는 프로그래밍 언어이다. 주로 Windows 애플리케이션 개발, 웹 애플리케이션 개발, 게임 개발, 모바일 애플리케이션 개발 등에서 널리 사용된다. 특히, ASP.NET을 이용한 웹 개발과 Unity를 이용한 게임 개발에서 그 강점을 발휘한다. C#은 강력한 객체 지향 프로그래밍 언어로, 대규모 소프트웨어 프로젝트에 적합하다.

**C#의 장점은 무엇인가요?**  

C#의 장점은 여러 가지가 있다. 첫째, C#은 강력한 타입 시스템을 가지고 있어 코드의 안정성을 높인다. 둘째, .NET 프레임워크와의 통합으로 다양한 라이브러리와 도구를 활용할 수 있다. 셋째, 비동기 프로그래밍을 지원하여 효율적인 멀티스레딩 작업이 가능하다. 넷째, C#은 문법이 간결하고 이해하기 쉬워 초보자도 쉽게 접근할 수 있다. 마지막으로, C#은 활발한 커뮤니티와 풍부한 자료가 있어 학습과 문제 해결에 유리하다.

**C#과 Java의 차이점은 무엇인가요?**  

C#과 Java는 유사한 점이 많지만 몇 가지 중요한 차이점이 있다. 첫째, C#은 Microsoft의 .NET 플랫폼에서 주로 사용되며, Java는 Oracle의 Java 플랫폼에서 사용된다. 둘째, C#은 프로퍼티, 이벤트, 델리게이트와 같은 고유한 기능을 제공하는 반면, Java는 이러한 기능이 없다. 셋째, C#은 LINQ와 같은 데이터 쿼리 기능을 제공하여 데이터 처리에 유리하다. 마지막으로, C#은 Windows 환경에서 최적화되어 있지만, Java는 플랫폼 독립성을 강조한다.

**C#을 배우기 위한 추천 자료는 무엇인가요?**  

C#을 배우기 위한 추천 자료는 다양하다. 첫째, Microsoft의 공식 문서와 튜토리얼은 C#의 기초부터 고급 개념까지 잘 설명되어 있다. 둘째, 온라인 강의 플랫폼인 Udemy, Coursera, edX에서 제공하는 C# 강의를 통해 체계적으로 학습할 수 있다. 셋째, C# 관련 서적도 많은 도움이 된다. "C# 9.0 in a Nutshell"과 같은 서적은 깊이 있는 내용을 다룬다. 마지막으로, GitHub와 Stack Overflow와 같은 커뮤니티에서 다른 개발자들과 소통하며 실습할 수 있다.

<!--
## 관련 기술
**ASP.NET**  
**Entity Framework**  
**Xamarin**  
**Unity**  
-->

## 관련 기술

**ASP.NET**  

ASP.NET은 Microsoft에서 개발한 웹 애플리케이션 프레임워크이다. C#을 사용하여 동적 웹 사이트, 웹 애플리케이션 및 웹 서비스를 구축할 수 있도록 지원한다. ASP.NET은 MVC(Model-View-Controller) 아키텍처를 기반으로 하여, 개발자가 애플리케이션의 구조를 명확하게 정의하고 유지보수하기 쉽게 만든다. 또한, ASP.NET Core는 플랫폼 독립적인 버전으로, Windows, macOS, Linux에서 모두 실행할 수 있다. 이로 인해 개발자는 다양한 환경에서 애플리케이션을 배포할 수 있는 유연성을 갖게 된다.

**Entity Framework**  

Entity Framework는 .NET 애플리케이션에서 데이터베이스와 상호작용하기 위한 ORM(Object-Relational Mapping) 프레임워크이다. 개발자는 데이터베이스의 테이블을 C# 클래스와 매핑하여, SQL 쿼리를 직접 작성하지 않고도 데이터베이스 작업을 수행할 수 있다. Entity Framework는 LINQ를 지원하여, 데이터 쿼리를 더욱 직관적으로 작성할 수 있도록 돕는다. 이를 통해 개발자는 데이터베이스와의 상호작용을 간소화하고, 코드의 가독성을 높일 수 있다.

**Xamarin**  

Xamarin은 C#을 사용하여 iOS, Android 및 Windows 플랫폼을 위한 모바일 애플리케이션을 개발할 수 있도록 지원하는 프레임워크이다. Xamarin을 사용하면 코드의 재사용성을 극대화할 수 있으며, 단일 코드베이스로 여러 플랫폼에서 실행되는 애플리케이션을 만들 수 있다. Xamarin.Forms를 사용하면 UI를 공유할 수 있어, 개발자는 각 플랫폼에 맞는 UI를 별도로 작성할 필요가 없다. 이로 인해 개발 시간과 비용을 절감할 수 있다.

**Unity**  

Unity는 게임 개발을 위한 강력한 엔진으로, C#을 주요 프로그래밍 언어로 사용한다. Unity는 2D 및 3D 게임을 개발할 수 있는 다양한 도구와 기능을 제공하며, 크로스 플랫폼 배포를 지원한다. 개발자는 Unity의 직관적인 인터페이스를 통해 게임 오브젝트를 쉽게 관리하고, 물리 엔진, 애니메이션, 사운드 등 다양한 요소를 통합할 수 있다. Unity는 게임 개발뿐만 아니라, 가상 현실(VR) 및 증강 현실(AR) 애플리케이션 개발에도 널리 사용된다.

이와 같은 관련 기술들은 C#을 배우고 활용하는 데 있어 매우 중요한 요소들이다. 각 기술은 특정한 목적과 용도를 가지고 있으며, C# 개발자가 다양한 분야에서 성공적으로 작업할 수 있도록 돕는다.

<!--
## 결론
**C#의 중요성과 미래**  
**C#을 배우는 것이 왜 중요한가**  
**C# 커뮤니티와 리소스**  
-->

## 결론

**C#의 중요성과 미래**  

C#은 마이크로소프트에서 개발한 프로그래밍 언어로, 객체 지향 프로그래밍의 특징을 갖추고 있다. C#은 다양한 플랫폼에서 사용될 수 있으며, 특히 .NET 프레임워크와 함께 사용될 때 그 진가를 발휘한다. C#은 웹 개발, 데스크탑 애플리케이션, 게임 개발 등 다양한 분야에서 활용되고 있으며, 그 수요는 계속해서 증가하고 있다. 앞으로도 C#은 클라우드 컴퓨팅, 인공지능, IoT 등 최신 기술과 함께 발전할 것으로 예상된다. 이러한 이유로 C#은 프로그래머에게 매우 중요한 언어로 자리 잡고 있다.

**C#을 배우는 것이 왜 중요한가**  

C#을 배우는 것은 여러 가지 이유로 중요하다. 첫째, C#은 배우기 쉬운 문법을 가지고 있어 프로그래밍 입문자에게 적합하다. 둘째, C#은 강력한 객체 지향 프로그래밍 언어로, 소프트웨어 개발의 기본 개념을 이해하는 데 도움을 준다. 셋째, C#은 다양한 산업에서 널리 사용되므로, C#을 배우면 취업 기회가 넓어진다. 마지막으로, C#은 활발한 커뮤니티와 풍부한 자료가 있어 학습에 큰 도움이 된다. 이러한 이유로 C#을 배우는 것은 프로그래머로서의 경력을 쌓는 데 매우 유익하다.

**C# 커뮤니티와 리소스**  

C#을 배우고 활용하기 위해서는 다양한 커뮤니티와 리소스를 활용하는 것이 중요하다. 온라인 포럼, 블로그, 유튜브 채널 등에서 C# 관련 자료를 쉽게 찾을 수 있다. 특히, Stack Overflow와 같은 Q&A 사이트는 문제 해결에 큰 도움이 된다. 또한, 마이크로소프트의 공식 문서와 튜토리얼은 C#의 기능과 사용법을 깊이 있게 이해하는 데 유용하다. 마지막으로, GitHub와 같은 플랫폼에서 오픈 소스 프로젝트에 참여하면 실제 프로젝트 경험을 쌓을 수 있어 더욱 효과적인 학습이 가능하다. C# 커뮤니티는 매우 활발하므로, 다양한 사람들과 소통하며 지식을 나누는 것도 좋은 방법이다.

<!--
##### Reference #####
-->

## Reference


* [https://learn.microsoft.com/ko-kr/dotnet/csharp/tour-of-csharp/overview](https://learn.microsoft.com/ko-kr/dotnet/csharp/tour-of-csharp/overview)
* [https://learn.microsoft.com/ko-kr/dotnet/core/introduction](https://learn.microsoft.com/ko-kr/dotnet/core/introduction)
* [https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=linknote&logNo=10082840324](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=linknote&logNo=10082840324)
* [https://dotnetboom.tistory.com/10](https://dotnetboom.tistory.com/10)
* [https://haedallog.tistory.com/186](https://haedallog.tistory.com/186)
* [https://www.dotnetnote.com/docs/csharp/csharp-programming-language/](https://www.dotnetnote.com/docs/csharp/csharp-programming-language/)


<!--
#  C# 언어 둘러보기

##  이 문서의 내용

C# 언어는 무료 플랫폼 간 오픈 소스 개발 환경인 [ .NET 플랫폼 ](../) 에서 가장 널리 사용되는 언어입니다. C# 프로그램은
IoT(사물 인터넷) 디바이스에서 클라우드에 이르기까지 다양한 디바이스에서 실행될 수 있습니다. 휴대폰, 데스크톱, 랩톱 컴퓨터 및 서버용
앱을 작성할 수 있습니다.

C#은 성능이 뛰어난 코드를 작성하면서 개발자의 생산성을 높이는 플랫폼 간 범용 언어입니다. 수백만 명의 개발자가 있는 C#은 가장 인기
있는 .NET 언어입니다. C#은 에코시스템 및 모든 .NET [ 워크로드 ](../../standard/glossary#workload)
를 광범위하게 지원합니다. 개체 지향 원칙에 기반하여 함수형 프로그래밍을 비롯한 다른 패러다임의 많은 기능을 통합합니다. 하위 수준 기능은
안전하지 않은 코드를 작성하지 않고도 고효율 시나리오를 지원합니다. 대부분의 .NET 런타임 및 라이브러리는 C#으로 작성되며 C#의 발전은
모든 .NET 개발자에게 도움이 되는 경우가 많습니다.

##  Hello World

“Hello, World” 프로그램은 프로그래밍 언어를 소개하는 데 일반적으로 사용됩니다. C#에서는 다음과 같습니다.

    
    
    // This line prints "Hello, World" 
    Console.WriteLine("Hello, World");
    

` // ` 로 시작하는 줄은 _한 줄 주석_ 입니다. C# 한 줄 주석은 ` // ` 로 시작하여 현재 줄 끝까지 계속됩니다. C#은
_여러 줄 주석_ 도 지원합니다. 여러 줄 주석은 ` /* ` 로 시작하고 ` */ ` 로 끝납니다. ` System ` 네임스페이스에 있는
` Console ` 클래스의 ` WriteLine ` 메서드는 프로그램의 출력을 생성합니다. 이 클래스는 기본적으로 모든 C# 프로그램에서
자동으로 참조되는 표준 클래스 라이브러리에서 제공됩니다.

앞의 예는 [ 최상위 문 ](../fundamentals/program-structure/top-level-statements) 을 사용하는
"Hello, World" 프로그램의 한 형태를 보여 줍니다. 이전 버전의 C#에서는 메서드에서 프로그램의 진입점을 정의해야 했습니다. 이
형식은 여전히 유효하며 많은 기존 C# 샘플에서 볼 수 있습니다. 다음 예에 표시된 것처럼 이 형식에도 익숙해야 합니다.

    
    
    using System;
    
    class Hello
    {
        static void Main()
        {
            // This line prints "Hello, World" 
            Console.WriteLine("Hello, World");
        }
    }
    

이 버전은 프로그램에서 사용하는 구성 요소를 보여 줍니다. “Hello, World” 프로그램은 ` System ` 네임스페이스를 참조하는
` using ` 지시문으로 시작합니다. 네임스페이스는 계층적으로 C# 프로그램 및 라이브러리를 구성하는 방법을 제공합니다. 네임스페이스에는
형식 및 기타 네임스페이스가 포함됩니다. 예를 들어, ` System ` 네임스페이스에는 프로그램에서 참조되는 ` Console ` 클래스와
같은 많은 형식과 ` IO ` 및 ` Collections ` 와 같은 기타 많은 네임스페이스가 포함되어 있습니다. 지정된 네임스페이스를
참조하는 ` using ` 지시문을 사용하여 해당 네임스페이스의 멤버인 형식을 정규화되지 않은 방식으로 사용할 수 있습니다. ` using
` 지시문 때문에, 프로그램은 ` Console.WriteLine ` 을 ` System.Console.WriteLine ` 의 약식으로
사용할 수 있습니다. 이전 예에서는 해당 네임스페이스가 [ 암시적으로 ](../language-reference/keywords/using-
directive#global-modifier) 포함되었습니다.

“Hello, World” 프로그램에서 선언된 ` Hello ` 클래스에는 단일 멤버인 ` Main ` 메서드가 있습니다. ` Main `
메서드는 ` static ` 한정자로 선언됩니다. 인스턴스 메서드는 키워드 ` this ` 를 사용하여 특정 바깥쪽 개체 인스턴스를 참조할
수 있지만 정적 메서드는 특정 개체에 대한 참조 없이 작동합니다. 관례적으로 최상위 문이 없으면 ` Main ` 이라는 정적 메서드가 C#
프로그램의 [ 진입점 ](../fundamentals/program-structure/main-command-line) 역할을 합니다.

두 진입점 형식 모두 동등한 코드를 생성합니다. 최상위 문을 사용하면 컴파일러는 프로그램 진입점에 대한 포함 클래스와 메서드를 합성합니다.

팁

이 문서의 예에서는 C# 코드를 처음으로 살펴봅니다. 일부 샘플에는 익숙하지 않은 C# 요소가 표시될 수 있습니다. C#을 알아볼 준비가
되면 [ 초보자 자습서 ](tutorials/) 부터 시작하거나 각 섹션의 링크를 살펴봅니다. [ Java ](tips-for-java-
developers) , [ JavaScript ](tips-for-javascript-developers) , [ TypeScript
](tips-for-javascript-developers) 또는 [ Python ](tips-for-python-developers) 사용
환경이 있는 경우 C#을 빠르게 배우는 데 필요한 정보를 찾는 데 도움이 되는 팁을 읽어보세요.

##  익숙한 C# 기능

C#은 초보자가 접근하기 쉬우면서도 특수 애플리케이션을 작성하는 숙련된 개발자를 위한 유용한 기능을 제공합니다. 빠르게 생산성을 높일 수
있습니다. 사용자의 응용 분야에 필요하다면 보다 전문적인 기술을 알아볼 수 있습니다.

C# 앱은 .NET 런타임의 [ 자동 메모리 관리 ](../../standard/automatic-memory-management) 를
활용합니다. C# 앱은 .NET SDK에서 제공하는 광범위한 [ 런타임 라이브러리 ](../../standard/runtime-
libraries-overview) 도 사용합니다. 파일 시스템 라이브러리, 데이터 수집, 수학 라이브러리와 같은 일부 구성 요소는 플랫폼
독립적입니다. 다른 것들은 ASP.NET Core 웹 라이브러리 또는 .NET MAUI UI 라이브러리와 같은 단일 워크로드에만 해당됩니다.
[ NuGet ](https://nuget.org) 의 풍부한 오픈 소스 에코시스템은 런타임의 일부인 라이브러리를 강화합니다. 이러한
라이브러리는 사용할 수 있는 더 많은 구성 요소를 제공합니다.

C#은 C 언어 계열에 속합니다. C, C++, JavaScript 또는 Java를 사용해 본 적이 있다면 [ C# 구문
](../language-reference/keywords/) 이 익숙할 것입니다. C 계열의 모든 언어와 마찬가지로 세미콜론( ` ; `
)은 문의 끝을 정의합니다. C# 식별자는 대/소문자를 구분합니다. C#에서는 중괄호, ` { ` 및 ` } ` , ` if ` , `
else ` 및 ` switch ` 와 같은 제어 문, ` for ` 및 ` while ` 과 같은 반복 구문을 동일하게 사용합니다.
C#에는 모든 컬렉션 형식에 대한 ` foreach ` 문도 있습니다.

C#은 _강력한 형식_ 의 언어입니다. 선언하는 모든 변수에는 컴파일 시간에 알려진 형식이 있습니다. 컴파일러나 편집 도구는 해당 형식을
잘못 사용하고 있는지 알려 줍니다. 프로그램을 실행하기 전에 이러한 오류를 수정할 수 있습니다. [ 기본 데이터 형식
](../fundamentals/types/) 은 언어 및 런타임에 기본 제공되어 있습니다. 즉, ` int ` , ` double ` ,
` char ` 와 같은 값 형식, ` string ` 과 같은 참조 형식, 배열 및 기타 컬렉션이 있습니다. 프로그램을 작성하면서 고유의
형식을 만들게 됩니다. 이러한 형식은 값의 경우 ` struct ` 형식이거나 개체 지향 동작을 정의하는 ` class ` 형식일 수
있습니다. 컴파일러가 동등 비교를 위해 코드를 합성하도록 ` struct ` 또는 ` class ` 형식에 ` record ` 한정자를
추가할 수 있습니다. 해당 인터페이스를 구현하는 형식이 제공해야 하는 계약 또는 멤버 집합을 정의하는 ` interface ` 정의를 만들
수도 있습니다. 제네릭 형식 및 메서드를 정의할 수도 있습니다. [ 제네릭 ](../fundamentals/types/generics) 은
_형식 매개 변수_ 를 사용하여 사용 시 실제 형식에 대한 자리 표시자를 제공합니다.

코드를 작성할 때 [ 메서드 ](../programming-guide/classes-and-structs/methods) 라고도 하는 함수를
` struct ` 및 ` class ` 형식의 멤버로 정의합니다. 이러한 메서드는 형식의 동작을 정의합니다. 다양한 수 또는 형식의 매개
변수를 사용하여 메서드를 오버로드할 수 있습니다. 메서드는 선택적으로 값을 반환할 수 있습니다. 메서드 외에도 C# 형식에는 _접근자_ 라는
함수가 지원하는 데이터 요소인 [ 속성 ](../programming-guide/classes-and-structs/properties) 이
있을 수 있습니다. C# 형식은 구독자에게 중요한 작업을 알릴 수 있는 [ 이벤트 ](../events-overview) 를 정의할 수
있습니다. C#은 ` class ` 형식에 대한 상속 및 다형성과 같은 개체 지향 기술을 지원합니다.

C# 앱은 [ 예외 ](../fundamentals/exceptions/) 를 사용하여 오류를 보고하고 처리합니다. C++ 또는 Java를
사용해 본 적이 있다면 이 방법에 익숙할 것입니다. 의도한 대로 수행할 수 없는 경우 코드에서 예외가 throw됩니다. 다른 코드는 호출
스택의 수준에 관계없이 ` try ` \- ` catch ` 블록을 사용하여 선택적으로 복구할 수 있습니다.

##  독특한 C# 기능

C#의 일부 요소는 익숙하지 않을 수 있습니다. [ LINQ(언어 통합 쿼리) ](../linq/) 는 모든 데이터 컬렉션을 쿼리하거나
변환하는 일반적인 패턴 기반 구문을 제공합니다. LINQ는 메모리 내 컬렉션, XML 또는 JSON과 같은 구조화된 데이터, 데이터베이스
스토리지, 심지어 클라우드 기반 데이터 API를 쿼리하기 위한 구문을 통합합니다. 하나의 구문 집합을 학습하면 스토리지에 관계없이 데이터를
검색하고 조작할 수 있습니다. 다음 쿼리는 평점 평균이 3.5보다 큰 모든 학생을 찾습니다.

    
    
    var honorRoll = from student in Students
                    where student.GPA > 3.5
                    select student;
    

앞의 쿼리는 ` Students ` 로 표시되는 다양한 스토리지 유형에 대해 작동합니다. 개체 컬렉션, 데이터베이스 테이블, 클라우드
스토리지 Blob 또는 XML 구조일 수 있습니다. 모든 스토리지 유형에 동일한 쿼리 구문이 적용됩니다.

[ 작업 기반 비동기 프로그래밍 모델 ](../asynchronous-programming/) 을 사용하면 비동기적으로 실행되더라도
동기적으로 실행되는 것처럼 읽는 코드를 작성할 수 있습니다. 비동기식 메서드와 식이 비동기식으로 평가되는 경우를 설명하기 위해 ` async
` 및 ` await ` 키워드를 활용합니다. 다음 샘플은 비동기 웹 요청을 기다립니다. 비동기 작업이 완료되면 메서드는 응답 길이를
반환합니다.

    
    
    public static async Task<int> GetPageLengthAsync(string endpoint)
    {
        var client = new HttpClient();
        var uri = new Uri(endpoint);
        byte[] content = await client.GetByteArrayAsync(uri);
        return content.Length;
    }
    

C#은 GraphQL 페이징 API와 같은 비동기 작업으로 지원되는 컬렉션을 반복하는 ` await foreach ` 문도 지원합니다. 다음
샘플은 데이터를 청크로 읽고, 사용 가능한 경우 각 요소에 대한 액세스를 제공하는 반복기를 반환합니다.

    
    
    public static async IAsyncEnumerable<int> ReadSequence()
    {
        int index = 0;
        while (index < 100)
        {
            int[] nextChunk = await GetNextChunk(index);
            if (nextChunk.Length == 0)
            {
                yield break;
            }
            foreach (var item in nextChunk)
            {
                yield return item;
            }
            index++;
        }
    }
    

호출자는 ` await foreach ` 문을 사용하여 컬렉션을 반복할 수 있습니다.

    
    
    await foreach (var number in ReadSequence())
    {
        Console.WriteLine(number);
    }
    

C#은 [ 패턴 일치 ](../fundamentals/functional/pattern-matching) 를 제공합니다. 이러한 식을
사용하면 데이터를 검사하고 해당 특성에 따라 결정을 내릴 수 있습니다. 패턴 일치는 데이터 기반 제어 흐름에 대한 훌륭한 구문을 제공합니다.
다음 코드는 패턴 일치 구문을 사용하여 부울 _and_ , _or_ 및 _xor_ 연산의 메서드를 표현하는 방법을 보여 줍니다.

    
    
    public static bool Or(bool left, bool right) =>
        (left, right) switch
        {
            (true, true) => true,
            (true, false) => true,
            (false, true) => true,
            (false, false) => false,
        };
    
    public static bool And(bool left, bool right) =>
        (left, right) switch
        {
            (true, true) => true,
            (true, false) => false,
            (false, true) => false,
            (false, false) => false,
        };
    public static bool Xor(bool left, bool right) =>
        (left, right) switch
        {
            (true, true) => false,
            (true, false) => true,
            (false, true) => true,
            (false, false) => false,
        };
    

패턴 일치 식은 모든 값에 대한 catch all로 ` _ ` 을 사용하여 간소화할 수 있습니다. 다음 예에서는 _and_ 메서드를
간소화하는 방법을 보여 줍니다.

    
    
    public static bool ReducedAnd(bool left, bool right) =>
        (left, right) switch
        {
            (true, true) => true,
            (_, _) => false,
        };
    

마지막으로, .NET 에코시스템의 일부로 [ Visual Studio
](https://visualstudio.microsoft.com/vs) 또는 [ C# DevKit
](https://code.visualstudio.com/docs/csharp/get-started) 과 함께 [ Visual Studio
Code ](https://code.visualstudio.com) 를 사용할 수 있습니다. 이러한 도구는 사용자가 작성하는 코드를 포함하여
C#에 대한 풍부한 이해를 제공합니다. 또한 디버깅 기능도 제공합니다.


-->

<!--






-->

<!--
#  .NET 소개

##  이 문서의 내용

.NET은 [ 다양한 유형의 애플리케이션 ](apps) 을 빌드하기 위한 무료 크로스 플랫폼 [ 오픈 소스 개발자 플랫폼
](https://github.com/dotnet/core) 입니다. 이는 [ 여러 언어 ](../fundamentals/languages)
로 작성된 프로그램을 실행할 수 있으며, 그 중 가장 인기 있는 언어는 [ C# ](../csharp/) 입니다. 이는 많은 [ 대규모 앱
](https://devblogs.microsoft.com/dotnet/category/developer-stories/) 프로덕션에서
사용되는 [ 고성능 ](https://devblogs.microsoft.com/dotnet/category/performance/) 런타임에
의존합니다.

[ .NET을 다운로드 ](https://dotnet.microsoft.com/download/) 하고 첫 번째 앱 작성을 시작하는 방법을
알아보려면 [ 시작하기 ](get-started) 를 참조하세요.

.NET 플랫폼은 생산성, 성능, 보안 및 안정성을 제공하도록 설계되었습니다. [ 가비지 수집기(GC)
](../standard/automatic-memory-management) 를 통해 자동 메모리 관리를 제공합니다. GC 및 엄격한 언어
컴파일러를 사용하기 때문에 형식이 안전하며 메모리가 안전합니다. ` async ` / ` await ` 및 ` Task ` 프리미티브를 통해
[ 동시성 ](../csharp/asynchronous-programming/) 을 제공합니다. 여기에는 광범위한 기능을 갖추고 여러
운영체제 및 칩 아키텍처의 성능에 최적화된 대규모 라이브러리 집합이 포함되어 있습니다.

.NET에는 다음과 같은 [ 디자인 포인트 ](https://devblogs.microsoft.com/dotnet/why-dotnet/) 가
있습니다.

  * **생산성은 풀스택** 으로 런타임, 라이브러리, 언어 및 도구가 모두 개발자 사용자 경험에 기여합니다. 
  * **안전 코드** 는 기본 컴퓨팅 모델이며, [ 안전하지 않은 코드 ](../csharp/language-reference/unsafe-code) 추가 수동 최적화를 사용하도록 설정합니다. 
  * **정적 및 동적 코드** 모두 지원되어 광범위한 고유 시나리오 집합을 사용할 수 있습니다. 
  * **네이티브 코드 interop 및 하드웨어 내장 함수** 는 비용이 처렴하고 충실(원시 API 및 명령 액세스)합니다. 
  * **코드는 플랫폼 간에 이식 가능하며** (OS 및 칩 아키텍처), 플랫폼 대상을 지정하여 전문화 및 최적화가 가능합니다. 
  * 범용 프로그래밍 모델의 특수 구현을 통해 **프로그래밍 도메인 전반에 걸친 적응성** (클라우드, 클라이언트, 게임)을 구현할 수 있습니다. 
  * OpenTelemetry 및 gRPC와 같은 **업계 표준** 은 맞춤형 솔루션보다 선호됩니다. 

.NET은 Microsoft와 커뮤니티에서 유지 관리합니다. 사용자가 안전하고 신뢰할 수 있는 애플리케이션을 프로덕션 환경에 배포할 수
있도록 정기적으로 업데이트됩니다.

##  구성 요소

.NET에는 다음 구성 요소가 포함됩니다.

  * 런타임 -- 애플리케이션 코드를 실행합니다. 
  * 라이브러리 -- [ JSON 구문 분석 ](../standard/serialization/system-text-json/overview) 과 같은 유틸리티 기능을 제공합니다. 
  * 컴파일러 -- C#(및 기타 언어) 소스 코드를 (런타임) 실행 코드로 컴파일합니다. 
  * SDK 및 기타 도구 -- 최신 워크플로를 사용하여 앱을 빌드하고 모니터링할 수 있습니다. 
  * 앱 스택 -- ASP.NET Core 및 Windows Forms와 같이 앱을 작성할 수 있습니다. 

런타임, 라이브러리 및 언어는 .NET 스택의 핵심 요소입니다. .NET 도구와 같은 상위 수준 구성 요소 및 앱 스택(예: ASP.NET
Core)은 이러한 핵심 요소를 기반으로 합니다. C#은 .NET의 기본 프로그래밍 언어이며 대부분의 .NET은 C#으로 작성됩니다.

C#은 개체 지향이며 런타임은 개체 방향을 지원합니다. C#에는 가비지 컬렉션이 필요하며 런타임은 추적 가비지 수집기를 제공합니다.
라이브러리(및 앱 스택)는 개발자가 직관적인 워크플로에서 알고리즘을 생산적으로 작성할 수 있도록 하는 개념 및 개체 모델로 이러한 기능을
형성합니다.

핵심 라이브러리에는 수천 개의 형식이 노출되어 있으며, 이 중 상당수는 C# 언어와 통합되어 있습니다. 예를 들어 C#의 ` foreach
` 문을 사용하면 임의의 컬렉션을 열거할 수 있습니다. 패턴 기반 최적화를 통해 ` List<T> ` 컬렉션과 같은 작업을 간단하고
효율적으로 처리할 수 있습니다. 리소스 관리는 가비지 컬렉션에 맡길 수 있지만, ` using ` 명령문에서 ` IDisposable ` 및
직접 언어 지원을 통해 신속한 정리가 가능합니다.

여러 작업을 동시에 수행하는 기능은 거의 모든 워크로드의 기본입니다. UI 응답성을 유지하면서 백그라운드 처리를 수행하는 클라이언트
애플리케이션, 수천 개의 동시 요청을 처리하는 서비스, 수많은 동시 자극에 응답하는 디바이스, 컴퓨팅 집약적인 작업을 병렬 처리하는 고성능
머신 등이 이에 해당할 수 있습니다. 비동기 프로그래밍 지원은 C# 프로그래밍 언어의 최고급 기능으로, 이 언어가 제공하는 모든 제어 흐름
구조의 이점을 최대한 활용하면서 비동기 연산을 쉽게 작성하고 구성할 수 있는 ` async ` 및 ` await ` 키워드를 제공합니다.

이 [ 형식 시스템 ](../standard/base-types/common-type-system) 은 안전성, 설명력, 역동성 및 네이티브
interop을 어느 정도 동일하게 충족하면서 상당한 폭을 제공합니다. 무엇보다도 형식 시스템은 객체 지향 프로그래밍 모델을 가능하게
합니다. 여기에는 형식, (단일 기본 클래스) 상속, 인터페이스(기본 메서드 구현 포함), 가상 메서드 디스패치가 포함되어 객체 지향이
허용하는 모든 타입 레이어링에 대해 합리적인 동작을 제공합니다. [ 제네릭 형식 ](../standard/generics) 은 클래스를 하나
이상의 형식으로 전문화할 수 있는 범용 기능입니다.

.NET 런타임은 가비지 수집기를 통해 자동 메모리 관리를 제공합니다. 모든 언어에서 메모리 관리 모델은 그 언어의 가장 큰 특징일
것입니다. .NET 언어의 경우도 마찬가지입니다. .NET에는 자체 튜닝, 추적 GC가 있습니다. 일반적인 경우에는 “핸즈 오프” 작업을
제공하는 동시에 보다 극한의 워크로드를 위한 구성 옵션을 제공하는 것을 목표로 합니다. 현재의 GC는 다년간의 투자와 다양한 워크로드에서
얻은 학습의 결과물입니다.

값 형식과 스택 할당 메모리 블록은 .NET의 GC 관리 유형과 달리 데이터 및 네이티브 플랫폼 상호 운용에 대한 보다 직접적이고 낮은
수준의 제어를 제공합니다. 정수 형식과 같은 .NET의 기본 형식은 대부분 값 형식이며, 사용자는 비슷한 의미 체계로 자신만의 형식을 정의할
수 있습니다. 값 형식은 .NET의 제네릭 시스템을 통해 완벽하게 지원되므로, ` List<T> ` 같은 제네릭 형식은 값 형식 컬렉션에
대해 오버헤드 없는 플랫 메모리 표현을 제공할 수 있습니다.

[ 리플렉션 ](../csharp/advanced-topics/reflection-and-attributes/) 은 “데이터로서의 프로그램”
패러다임으로, 어셈블리, 형식 및 멤버 측면에서 프로그램의 한 부분이 다른 부분을 동적으로 쿼리하고 호출할 수 있게 해줍니다. 런타임에
바인딩된 프로그래밍 모델 및 도구에 특히 유용합니다.

예외는 .NET의 기본 오류 처리 모델입니다. 예외는 오류 정보를 메서드 서명에 표시하거나 모든 메서드에서 처리할 필요가 없다는 이점이
있습니다. 적절한 예외 처리는 애플리케이션 안정성에 필수적입니다. 앱이 충돌하지 않도록 하려면 코드에서 예상되는 예외를 의도적으로 처리할 수
있습니다. 크래시된 앱은 정의되지 않은 동작을 가진 앱보다 더 안정적이고 진단 가능합니다.

ASP.NET Core 및 Windows Forms와 같은 앱 스택은 하위 수준 라이브러리, 언어 및 런타임을 기반으로 빌드하고 활용합니다.
앱 스택은 앱이 구성되는 방식과 실행 수명 주기를 정의합니다.

SDK 및 기타 도구를 사용하면 개발자 데스크톱과 CI(연속 통합) 모두에서 최신 개발자 환경을 사용할 수 있습니다. 최신 개발자 환경에는
코드를 빌드, 분석 및 테스트할 수 있는 기능이 포함됩니다. .NET 프로젝트는 NuGet 패키지 복원 및 종속성 빌드를 오케스트레이션하는
단일 ` dotnet build ` 명령을 통해 빌드될 수 있습니다.

NuGet은 .NET의 패키지 관리자입니다. 여기에는 많은 시나리오에 대한 기능을 구현하는 수십만 개의 패키지가 포함되어 있습니다. 대부분의
앱은 일부 기능에 대해 NuGet 패키지를 사용합니다. [ NuGet 갤러리 ](https://nuget.org/) 는 Microsoft에서
유지 관리합니다.

##  무료 및 오픈 소스

.NET은 무료 오픈 소스이며 [ .NET Foundation ](https://dotnetfoundation.org/) 프로젝트입니다.
.NET은 [ 여러 리포지토리
](https://github.com/dotnet/core/blob/main/Documentation/core-repos.md) 의
Microsoft와 GitHub의 커뮤니티에서 유지 관리됩니다.

.NET 원본 및 이진 파일은 [ MIT 라이선스
](https://github.com/dotnet/runtime/blob/main/LICENSE.TXT) 가 라이선싱합니다. [
Windows에 추가 라이선스가 적용됩니다 ](https://github.com/dotnet/core/blob/main/license-
information-windows.md) .

##  지원

.NET을 [ 여러 운영 체제 ](https://github.com/dotnet/core/blob/main/os-lifecycle-
policy.md) 에서 실행하고 최신 상태로 유지하기 위해 노력하는 [ 여러 조직
](https://github.com/dotnet/core/blob/main/support.md) 에서 .NET을 지원합니다. Arm64,
x64 및 x86 아키텍처에서 사용할 수 있습니다.

.NET의 새 버전은 [ 릴리스 및 지원 정책 ](releases-and-support) 에 따라 매년 11월에 릴리스됩니다. [ 매월
](https://github.com/dotnet/announcements/labels/Monthly-Update) Patch
Tuesday(2주차 화요일)에 업데이트되며, 일반적으로 태평양 표준시 오전 10시에 업데이트됩니다.

##  .NET 에코시스템

.NET에는 여러 변형이 있으며 각각 다른 형식의 앱을 지원합니다. 다양한 변형이 존재하는 이유는 부분적으로는 역사적, 부분적으로는 기술적
이유 때문입니다.

.NET 구현:

  * **.NET Framework** \-- 원래 .NET입니다. Windows 및 Windows Server의 광범위한 기능에 액세스할 수 있습니다. 유지 관리 면에서는 적극적으로 지원됩니다. 
  * **Mono** \- 원래 커뮤니티 및 오픈 소스 .NET입니다. .NET Framework의 플랫폼 간 구현입니다. Android, iOS 및 WebAssembly에 대해 적극적으로 지원됩니다. 
  * **.NET(Core)** \- 최신 .NET. 클라우드 시대에 맞게 재구상된 플랫폼 간 및 오픈 소스 구현으로, .NET Framework와 상당한 호환성을 유지하면서 .NET을 구현합니다. Linux, macOS 및 Windows에 대해 적극적으로 지원됩니다. 

##  다음 단계


-->

<!--






-->

<!--
  
지난 20년 동안 C와 C++는 상용 및 업무 소프트웨어 개발에 가장 널리 사용되었습니다. 두 언어는 모두 프로그래머가 세밀한 부분까지
제어할 수 있는 반면에 이러한 융통성은 생산성을 저하시킵니다. Microsoft Visual Basic과 같은 언어에 비해 C와 C++를
사용한 응용 프로그램 개발은 더 많은 시간이 필요합니다. C와 C++는 난해하고 개발에 많은 시간이 소요되기 때문에 많은 C, C++
프로그래머는 성능과 생산성 간의 보다 나은 균형을 제공하는 언어를 찾으려고 노력해 왔습니다.  현재 C와 C++ 프로그래머가 요구하는
유연성을 줄이고 대신 생산성을 높일 수 있는 언어들이 있습니다. 이러한 솔루션은 개발자의 범위를 지나치게 제한하고(예: 저수준 코드 제어
메커니즘 삭제) 최소한의 일반적인 기능만 제공합니다. 이전의 시스템과 쉽게 호환되지 않으며 현재의 웹 프로그래밍에 알맞지 않은 부분도
있습니다.  C와 C++ 프로그래머에게 이상적인 솔루션은 신속한 개발이 가능하고 기본 플랫폼의 모든 기능을 액세스할 수 있는 성능이 결합된
제품입니다. 이들은 웹 표준과 완벽하게 부합되고 기존의 응용 프로그램과 쉽게 통합할 수 있는 환경을 원합니다. 또한 C와 C++ 개발자는
필요한 경우 저수준으로 코드를 작성할 수 있는 기능을 선호합니다.  Microsoft, C# 소개  이러한 문제에 대한 Microsoft의
솔루션은 C# ("C 샵"으로 발음)이라는 언어입니다. C# 은 최신 개체 지향 언어입니다. 프로그래머는 새 Microsoft .NET
플랫폼에서 실행되는 광범위한 응용 프로그램을 신속하게 작성할 수 있습니다. 이 플랫폼은 컴퓨팅 및 통신을 완벽하게 활용할 수 있는 도구와
서비스를 제공합니다.  C#은 최신 개체 지향 설계를 통해 고수준 업무 개체부터 시스템 수준 응용 프로그램까지 광범위한 구성 요소를 작성할
수 있습니다. 모든 플랫폼의 모든 언어에서 간단한 C# 언어 작성을 통해 구성 요소를 인터넷에서 실행되는 웹 서비스로 변환할 수 있습니다.
특히 C#은 C와 C++의 장점인 성능과 세밀한 제어 기능을 희생하지 않고 신속한 개발이 가능하도록 설계되었습니다. 이러한 설계에 따라
C#은 C와 C++의 기능을 거의 가지고 있습니다. C와 C++ 언어에 익숙한 개발자는 C#을 쉽게 사용할 수 있습니다.  생산성 및 안전성
새로운 웹 경제로 인해 이전보다 더욱 신속하게 경쟁력을 갖추어야 하는 업무 환경에 직면하게 되었습니다. 개발자는 프로그램의 개발 주기를
단축하고 버전을 지속적으로 업데이트해야 합니다.  C#은 이러한 상황을 염두에 두고 설계되었습니다. 이 언어는 개발자가 더 적은 코드를
사용하여 더 적은 오류가 발생하는 프로그램을 개발할 수 있도록 지원합니다.  ** 웹 프로그래밍 표준 준수  **  
새로운 응용 프로그램 개발 모델은 더 많은 솔루션에서 HTML(Hypertext Markup Language), XML(Extensible
Markup Language), SOAP(Simple Object Access Protocol) 등과 같은 웹 표준을 사용하도록 요구하고
있습니다. 기존의 개발 도구는 인터넷과 웹이 출현하기 이전이나 초창기에 개발되었습니다. 따라서 새로운 웹 기술에 적합하지 않은 부분들이
있습니다.  C#프로그래머는 Microsoft .NET 플랫폼에서 응용 프로그램을 작성할 경우 광범위한 프레임워크를 활용할 수 있습니다.
C#은 모든 플랫폼의 모든 언어에서 구성 요소를 인터넷에서 실행되는 웹 서비스로 변환할 수 있는 내장 지원 도구를 포함하고 있습니다.  또한
웹 서비스 프레임워크는 기존의 웹 서비스가 프로그래머에게 고유 C# 개체와 동일하게 보이도록 만들 수 있으므로 개발자가 기존의 웹 서비스에
개체 지향 프로그래밍 기법을 활용할 수 있습니다.  C#을 훌륭한 인터넷 프로그래밍 도구로 만드는 몇 가지 특징들이 있습니다. 예를 들어,
XML은 인터넷을 통해 구조화된 데이터를 전달하는 표준 방식으로 등장했습니다. 이러한 데이터 집합은 대개 매우 작습니다. 성능 개선을 위해
C#은 XML 데이터를 클래스 대신 직접 struct 데이터 형식으로 매핑할 수 있습니다. 이 방법은 작은 데이터를 다루는 데 효과적입니다.
** 손해가 큰 프로그래밍 오류 제거  **  
숙달된 C++ 프로그래머라도 변수 초기화를 잊는 등의 초보적인 실수를 할 수 있고 이러한 간단한 실수로 인해 오래 동안 발견되지 않는 예상치
못한 문제가 발생할 수 있습니다. 일단 프로그램이 제품으로 출시되면 아주 간단한 프로그래밍 오류라도 수정하는 데 비용이 많이 듭니다.
C#은 가장 일반적인 C++ 프로그래밍 오류를 줄일 수 있도록 설계되었습니다. 예를 들어,

  * 쓰레기 수집 기능을 통해 프로그래머가 직접 메모리를 관리해야 하는 부담을 없애줍니다. 
  * C#에서는 환경에 따라 변수가 자동으로 초기화됩니다. 
  * 안전한 형식의 변수를 사용합니다. 

따라서 개발자가 쉽게 프로그램을 작성하고 관리할 수 있으며 복잡한 업무 문제를 해결할 수 있습니다.  ** 내장 버전 지원 프로그램을
사용하여 개발 비용 절감  **  
소프트웨어 구성 요소의 업데이트는 주로 오류를 찾는 작업입니다. 코드를 수정할 경우 기존 프로그램의 내용이 의도와 다르게 변경될 수도
있습니다. 개발자가 이 문제를 해결할 수 있도록 지원하기 위해 C#은 버전 지원 도구를 포함하고 있습니다. 예를 들어, 메서드 재정의는
C++나 Java처럼 우연히 발생할 수 없도록 명시적이어야 합니다. 이렇게 하면 코딩 오류를 방지하고 버전을 유연하게 보존할 수 있습니다.
관련 기능으로 인터페이스와 인터페이스 상속의 지원 기능이 있습니다. 이러한 기능들을 통해 복잡한 프레임워크를 신속하게 개발하고 업데이트할 수
있습니다.  따라서 차기 버전의 프로젝트를 개발하는 과정이 더욱 간단해지고 버전 업데이트에 필요한 개발 비용을 줄일 수 있습니다.  성능,
기능 및 유연성  ** 업무 프로세스 및 구현 사이의 뛰어난 매핑  **  
기업에서 업무 계획을 수립할 경우 추상 업무 프로세스와 실제 소프트웨어 구현 사이의 밀접한 관련성은 필수적입니다. 그러나 대부분의 언어는
업무 논리와 코드를 연결하는 편리한 방법을 제공하지 못하고 있습니다. 예를 들어, 개발자는 추상 업무 개체를 구성하는 클래스를 식별하기 위해
대개 코드 주석을 사용합니다.  C# 언어는 모든 개체에 적용될 수 있는 형식이 지정된 광범위한 메타데이터를 허용합니다. 프로젝트 기획자는
도메인별 특성을 정의하고 클래스나 인터페이스 등의 모든 언어 요소에 이 특성을 적용할 수 있습니다. 그런 다음 개발자는 프로그램을 통해 각
요소의 특성을 조사합니다. 이렇게 하면 예를 들어, 각 클래스나 인터페이스가 특정한 추상 업무 개체의 일부로 올바로 식별되는 자동화 도구를
작성하거나 단순히 개체의 도메인별 특성에 따라 보고서를 생성하는 작업이 쉬워집니다. 사용자 정의 메타데이터와 프로그램 코드 사이의 엄격한
결합은 의도한 프로그램 동작과 실제 구현 사이의 연결을 강화할 수 있도록 지원합니다.  ** 광범위한 호환성  **  
엄격한 형식 검사 환경은 대부분의 기업 응용 프로그램에 적합합니다. 그러나 실제로 성능 및 기존 API와의 호환성 때문에 계속 원시 코드를
필요로 하는 일부 응용 프로그램이 있습니다. 이러한 시나리오 때문에 개발자가 더욱 생산적인 개발 환경을 선호하지만 C++를 사용해야 하는
경우도 있습니다.  C#은 다음과 같이 이러한 문제점을 해결합니다.

  * COM(Component Object Model)과 Windows 기반 API 지원. 
  * 고유 포인터 사용 제한 가능. 

C#에서는 모든 개체가 자동으로 COM 개체가 됩니다. 개발자는 더 이상 IUnknown 및 기타 COM 인터페이스를 명시적으로 구현할
필요가 없습니다. 대신 이러한 기능들이 내장되어 있으므로 C# 프로그램은 사용된 언어에 상관 없이 기존 COM 개체를 고유하게 사용할 수
있습니다.  기존 COM 개체가 필요한 개발자를 위해 C#은 프로그램에서 모든 고유 API를 호출할 수 있는 특별한 기능을 포함하고
있습니다. 개발자는 특정 표시가 있는 코드 블록에서 메모리 직접 관리나 포인터 계산과 같은 이전의 C/C++ 기능들을 사용할 수 있습니다.
이 기능은 서로 다른 환경에서 많은 장점을 가지고 있습니다. 즉, C# 프로그래머는 기존의 C와 C++ 코드를 다시 사용할 수 있습니다.
COM 지원 및 고유 API 액세스 기능의 목적은 모두 개발자가 필요로 하는 성능을 제공하고 C# 환경을 벗어나지 않고 프로그램을 개발할 수
있도록 하는 것입니다.  결론  C#은 Microsoft .NET 플랫폼에서 실행되는 솔루션을 신속하고 편리하게 개발할 수 있는 최신 개체
지향 언어입니다. 제공되는 프레임워크를 통해 모든 플랫폼의 모든 언어에서 C#구성 요소를 인터넷에서 실행되는 웹 서비스로 만들 수 있습니다.
C#은 개발자의 생산성을 높여주고 개발 비용 증가의 원인이 되는 프로그래밍 오류를 줄일 수 있습니다. C#은 C와 C++ 프로그래머가
요구하는 성능과 유연성을 제공하면서 신속한 웹 개발이 가능합니다.


-->

<!--






-->

<!--
![https://blog.kakaocdn.net/dn/mpH4H/btsHtpxggLT/xMtjRoY9xNatVdbqCHx8M1/img.png](https://blog.kakaocdn.net/dn/mpH4H/btsHtpxggLT/xMtjRoY9xNatVdbqCHx8M1/img.png)

##  .NET 이란?

> .NET은 다양한 유형의 애플리케이션을 빌드하기 위한 무료 크로스 플랫폼 오픈 소스 개발자 플랫폼입니다. 이는 여러 언어로 작성된
> 프로그램을 실행할 수 있으며, 그 중 가장 인기 있는 언어는 C#입니다. 이는 많은 대규모 앱 프로덕션에서 사용되는 고성능 런타임에
> 의존합니다.

  * .NET은 Microsoft에서 지원하는 무료 오픈 소스 애플리케이션 플랫폼이다. 
  * .NET은 2002년, 마소에서 발표한 닷넷 프레임워크(.NET Framework)가 시초이며, 여러 버전을 거처 현재 명칭은 오픈 소스 버전인 .NET으로 불린다. 
  * .NET 기반 응용 프로그램은 .NET 런타임 환경을 필요로 한다. 

##  .NET과 C#과의 관계?

> C#은 .NET용 프로그래밍 언어입니다. 강력한 타이핑 및 유형 안전성을 갖추고 있으며 동시성 및 자동 메모리 관리 기능이 통합되어
> 있습니다.

  * C#의 컴파일러는 C# 소스코드를 IL(Intermediate Languege)라고 하는 중간 언어로 실행 파일을 내부에 생성하게 되는데, 이 IL을 .NET Runtime이 실행한다. 
  * C#은 .NET 호환 언어 중 하나일 뿐이다. 

##  .NET 호환 언어

어떤 언어든 컴파일러나 다른 방식 통해 IL로 만들어낼 수 있다면 .NET Runtime에서 실행이 가능하고 .NET 호환 언어라고 할 수
있다. 아래 언어들은 MS에서 공식적으로 제공되는 .NET 호환언어이다.

.NET 호환 언어라는 것은 무엇을 의미하는가?

그것은 서로 동일한 중간언어에서 돌아간다는 것. 즉, C++에서 만든 클래스를 C#에서 사용 가능하다.

##  공통 중간 언어(Common Intermediate Languege, CIL)

위에서 설명한 IL의 풀네임이 바로 **‘공통 중간 언어, CIL’** 이다. (자바의 바이트코드 느낌)

프로그래밍 언어는 비교적 고수준 언어와 저수준 언어가 존재한다.

인간이 이해하기 쉬운 형태일수록 고수준, 기계가 이해하기 쉬운 형태일수록 저수준이다.

그런 의미에서 C#은 비교적 고수준, C#을 .NET 중간언어인 IL(CIL, MSIL, IL 등 다양하게 불림)은 비교적 저수준인 셈이다.

아무튼 IL로 컴파일된 후, 런타임이 실행될 때, IL 코드는 CPU의 기계어로 번역된다.

즉, 고수준에서 저수준으로 단계별 컴파일 된다.

** C# → (컴파일러 작동) ** →  ** IL, 중간언어 → (.NET Runtime 실행) ** →  ** CPU가 인식 가능한
기계어  **

##  공용 타입 시스템(Common Type System, CTS)

앞에서 알 수 있듯이, IL로 컴파일이 가능한 언어일 경우 닷넷 호환 언어라고 할 수 있다.

그렇다고 아무 언어나 닷넷 호환 언어가 될 수 있는 것은 아니다.

**‘이정도 안에서 구현하면 닷넷 호환언어’** 라고 정해둔 것이 바로 **CTS 규약** 이다.

  * 닷넷 호환 언어는 CTS의 한계를 넘어서 구현할 수는 없다. 예) IL은 클래스 다중 상속을 구현하지 않으므로 다중 상속을 구현할 수 없다. 
  * 닷넷 호환 언어는 CTS에서 정의한 모든 규격을 전부 구현할 필요는 없다. 예) 접근 제한자로 private, public 등 여러가지가 있지만, public만 구현해도 상관없다. 

##  공용 언어 사양(Common Languege Specification, CLS)

‘이정도 안에서 구현하면 닷넷 호환언어’라고 정해둔 것이 CTS라면,

**‘최소한 이것만큼은 구현해야 닷넷 호환언어’** 라고 정해둔 것이 **CLS** 이다.

그렇다면 왜 CLS 규약이 존재하는가? 라는 물음에는 이렇게 답할 수 있다.

닷넷 호환 언어끼리 같은 IL로 컴파일이 가능한 특성을 통해 각각 라이브러리화 하여 서로 사용할 수 있고 상속받을 수 있다는 특징이 있으나,
IL로 구현되어야 할 기능이 구현되지 않으면 같은 IL이지만 구현되지 않은 부분에 대한 호환성을 기대하기 어렵기 때문에 더이상 닷넷 ‘호환’
언어라고 부를 수 없게 될 것이기 때문이다.

##  공용 언어 기반구조(Common Language Infrastructure, CLI)

> Ecma International is an industry association dedicated to the
> standardization of information and communication systems.  
>  Ecma International은 정보통신 시스템 표준화를 전문으로 하는 산업 협회입니다.  
>  \- ECMA 공홈 메인 슬로건 번역 -

지금까지 .NET과 C#을 설명하면서 '공용, Common'이 붙은 단어들에 대한 설명이 많았는데, 그러한 모든 인프라적 구성 요소를
ECMA(정보통신 표준화 전문 협회) 표준 공개 규약으로 만든 것이 CLI이다.

이는 .NET 인프라에 대한 공개된 스팩이기 때문에 누구나 CLI 사양을 구현할 수 있다.

##  공용 언어 런타임(Common Language Runtime, CLR)

.NET Framework 버전의 CLR과 .NET Core 버전의 CLR(CoreCLR)로 나뉜다.

.NET Framework 버전의 CLR은 당연히 Windows 전용이고 CoreCLI은 크로스 플랫폼을 지원한다.

MS문서에 ' [ **_원래 Core CLR은 Silverlight의 런타임이고 여러 플랫폼, 특히 Windows 및 OS X에서 실행되도록
디자인되었습니다._ ** ](https://learn.microsoft.com/ko-
kr/dotnet/standard/glossary#clr) '라고 적혀 있는데, Silverlight가 뭐지? 하고 찾아보니 Adobe
Flash에 대항하기 위한 애플리케이션 프레임워크다. 즉, CLR은 Silverlight 기반으로 만들어졌으며, CoreCLI은 초기에 이를
계승했다고 볼 수 있으며  CLI, CoreCLI 둘 다 동일한 코드 베이스에서 시작되어 지금의 형태를 띄게 되었다고 한다.

CLR은 다음과 같은 역할을 한다.

  * 중간 언어를 JIT 컴파일러를 이용해 기계어로 변환하는 것 
  * 가비지 수집기(Garbage Collector, GC)를 제공하여 동적 메모리 할당 및 회수를 지원하는 것 

##  .NET

그럼 2024에 발표된 .NET8.0은 뭐라고 할 수 있을까?

이는 MS가 CLR + BLC(Base Class Library), 기타 파일(C# 컴파일러, 빌드 시스템 등) 등, 여러 구성요소를
패키지로 묶어서 배포한 최신 버전의 닷넷이다.

ASP.NET Core를 하든, 데스크톱 앱을 하든, 콘솔 앱을 하든지 간에 결국은 .NET BLC를 주로 사용하게 될 것이다.

이는 .NET 개발을 할 때, 개발 편의를 제공하기 위해 MS에서 미리 만들어 둔 핵심 라이브러리 집합이다.

.NET의 버전이 거듭될수록 발전하고 있으며, .NET 개발에서 BLC를 잘 알아둔다면 다른 플랫폼 개발을 하더라도 큰 도움이 될 것이다.

##  참고자료

[ 시작하세요! C# 12 프로그래밍 - 예스24  이 책의 목표는 여러분이 C#을 이용해 프로그래밍 기초를 탄탄하게 다질 수 있게 하는
것이다. 이를 위해 C# 언어의 최신 버전인 C# 12의 문법까지 구체적인 예제와 함께 상세히 설명하며, 단순히  www.yes24.com
](https://www.yes24.com/Product/Goods/125905684) [ .NET란? 오픈 소스 개발자 플랫폼.
.NET은 플랫폼 간 무료 오픈 소스 개발자 플랫폼입니다. .NET에는 웹, 모바일, 데스크톱, 게임 및 IoT용으로 빌드할 언어, 편집기
및 라이브러리가 있습니다.  dotnet.microsoft.com  ](https://dotnet.microsoft.com/ko-
kr/learn/dotnet/what-is-dotnet) [ .NET 소개 - .NET  .NET에 대해 자세히 알아봅니다. .NET은
다양한 종류의 앱을 빌드하기 위한 무료 오픈 소스 개발 플랫폼입니다.  learn.microsoft.com
](https://learn.microsoft.com/ko-
kr/dotnet/core/introduction?WT.mc_id=dotnet-35129-website) [ .NET 관리 언어 전략 -
.NET  각 .NET 언어는 고유합니다. C#은 가장 널리 사용되는 언어이며 대부분의 .NET이 이 언어로 작성됩니다. F#은 새로운 언어
가능성을 탐색하고 커뮤니티는 플랫폼 간에 풍부한 환경을 제공합니다. Mic  learn.microsoft.com
](https://learn.microsoft.com/ko-kr/dotnet/fundamentals/languages)


-->

<!--






-->

<!--
###  ** 개요  **

C#은  마이크로소프트에서 개발한 객체 지향 프로그래밍 언어  다. C#은  강건하고 유지보수를 위한 여러 가지 기능을 제공  하는데
메모리를 자동으로 정리해주는  가비지 컬렉션  , 함수형 프로그래밍을 위한  람다 식  , 비동기 프로그래밍 등이 있다.

###  ** .NET 아키텍처  **

C#과 함께 빼놓을 수 없는 것이 .NET이다. 마이크로소프트는 어떤 플랫폼이던지 언어를 동작시킬 수 있도록  ** 공용 언어 인프라  **
(CLI; Common Language Infrastructure)라는 사양을 발표했는데  , .NET은  이 사양에 맞춰 마이크로소프트가
구현한 프로그램인  **공용 언어 런타임** (CLR; Common Language Runtime)과 클래스 라이브러리 세트  를 말한다.
C#은 이러한 .NET 위에서 동작하는 프로그래밍 언어 중에 하나다.*  

*그 외에 F#, Visual Basic이 있다. 

###  ** 빌드  **

C#은 컴파일을 하면 CLI 사양을 준수하는  ** 중간 언어  ** (Intermediate Language)*로 컴파일 된다. 그리고
이러한 IL 코드와 프로그램에 사용되는 리소스**가 함께 패키징 되어 **어셈블리** (Assembly)가 된다.*** 어셈블리는  서로
함께 사용되어 논리적 기능 단위를 형성하도록 빌드되는 타입 및 리소스의 컬렉션  을 의미한다. 어셈블리는 실행 파일(.exe) 또는 동적
연결 라이브러리(.dll)의 형태를 가지며, .NET 기반 애플리케이션에 대한 배포, 버전 제어, 재사용, 활성화 범위 및 보안 권한의 기본
단위를 형성한다.

* 자바를 알고 있다면, 자바의 바이트 코드(Byte Code)를 생각하면 된다. 

** 아이콘, 마우스 커서, 메뉴 등이다.

*** C/C++를 컴파일하면 생성되는 어셈블리 언어와는 다른 개념이다. 혼동하지 않도록 주의하자.

****

C# 프로그램을 실행하면 어셈블리가 CLR에 로드 되는데, CLR은 IL 코드를 플랫폼에 따라  ** JIT  ** (Just-In-
Time) 컴파일* 혹은  ** AOT  ** (Ahead-Of-Time) 컴파일**을 수행하여 네이티브 명령어로 변환한다.

*프로그램 실행 중에 그때그때 컴파일을 하는 것이다. 

**프로그램 실행 전 미리 컴파일을 진행하는 것이다.

###  ** 참고자료  **


-->

<!--






-->

<!--
#  C# 프로그래밍 언어

" ` 씨샵 ` "으로 발음하는 ` C# ` 은 프로그래밍 언어입니다. 이 책은 ` C# ` 이름을 가진 프로그래밍 언어를 다룹니다. 자,
이제부터 오랜기간동안 많은 프로그래머에게 사랑받아 온 최고의 언어인 ` C# ` 을 배워보도록 하겠습니다.

` C# ` 을 한 줄로 압축해서 정의하면 다음과 같습니다. 여러모로 많은 뜻을 담고 있습니다.

    
    
    > // C#: 현재 전세계 시가총액 1위인 Microsoft에서 만들고 주력으로 사용하는 프로그래밍 언어
    

처음 이 글을 작성한 시점에는 Microsoft가 전세계 시가총액 1위였습니다. 지금은 바뀌었나요?

## 컴퓨터와 프로그래밍 언어

### 하드웨어와 소프트웨어

컴퓨터는 하드웨어(Hardware)와 소프트웨어(Software)로 이루어집니다. 하드웨어는 PC, 스마트폰과 같은 장치를 말하며
소프트웨어는 이러한 하드웨어에 설치된 운영체제, 앱 등을 말합니다.

#####  NOTE

2005년 제가 개인사업자로 창업할 때 회사 이름을 정할 때 하드웨어와 소프트웨어를 사용하여 제품(Ware)을 만든다는 의미로 **하와소**
(Hawaso)  로 결정했습니다. 2023년 현재까지도 망하지 않고 잘 버티고 있습니다. 제 책과 강의를 봐주시는 여러분들 덕분입니다.
감사합니다.  
(Hardware + Software) => Ware  

### 프로그래밍과 프로그래머

소프트웨어를 만드는 행위를 프로그래밍(Programming)이라고 합니다. 소프트웨어를 만드는 사람을 프로그래머(Programmer) 또는
개발자(Developer)로 부릅니다.

  * 프로그래머(Programmer) 
  * 소프트웨어 개발자(Software Developer) 
    * 솔루션 개발자(Solution Developer) 
    * 애플리케이션 개발자(Application Developer) 

### 프로그래밍 언어

명령(Instruction)을 통해서 컴퓨터에게 무엇인가를 시킬 수 있는 프로그램을 만들 수 있는 또 다른 소프트웨어가 프로그래밍
언어입니다. 사람이 어휘와 문법을 통해서 대화하듯이 프로그래밍 언어는 예약어(키워드)와 문법으로 무언가를 만들 수 있습니다. 세상에는
C언어, C++, C#, Java, JavaScript, Python 등의 많은 프로그래밍 언어가 있습니다. 그 중에서 이 강의는 C#
프로그래밍 언어를 다룹니다.

#### 프로그래밍 언어 순위

C# 프로그래밍 언어는 굉장히 오랜 기간동안 프로그래밍 언어 순위 5위 안에 항상 들어와 있습니다. 프로그래머마다 좋아하는 언어 스타일이
다르기에 순위에는 항상 변동이 있을 수 있습니다. 하지만, 박용준 강사는 프로그래밍 언어 순위 10위 안에 드는 대부분의 언어를 사용해
봤지만, 가장 좋아하는 언어는 C#을 1순위로 들고 있습니다. 이것 또한 순전히 주관적인 생각이지만, 간결함과 명확한 문법, 그리고
프로그래밍 언어가 가질 수 있는 대부분의 편리한 기능을 다 가지고 있는게 C#이라고 생각합니다.

다음 그림은 전세계 개발자 커뮤니티로 유명한 스택오버플로(StackOverflow) 사이트의 2020년 설문 조사 결과입니다. C#은 항상
상위권에 위치하고 있습니다. 실제 프로그래밍 언어로만 보면 JavaScript, Java, Python, C# 순서로 상위 5개 언어에
포함됩니다.

**그림:** 스택오버플로 사이트의 가장 인기있는 기술 순위 설문조사 결과

![C# 프로그래밍
순위](https://www.dotnetnote.com/docs/csharp/1-csharp/images/stackoverflow-
csharp-ranking-2020.png)

### 용어: 코드(Code)와 코딩(Coding)

  * 텍스트로 되어 있는 소프트웨어를 만드는 명령들의 집합을 코드(Code) 또는 소스(Source)라고 합니다. 
  * 코딩(Coding)은 프로그래밍 언어의 코드로 프로그램을 만드는 과정입니다. 코딩은 컴퓨터 프로그래밍과 비슷한 개념입니다. 

### 용어: 컴파일(Compile)과 인터프리트(Interpret)

프로그램 소스 코드를 컴퓨터와 같은 하드웨어가 실행할 수 있는 기계 코드로 변환해주는 프로그램을 컴파일러(Compiler)라하고 변환하는
과정을 컴파일(Compile)이라고 합니다. 따로 컴파일의 과정을 거치지 않고 소스를 바로 해석해서 실행해주는
인터프리터(Interpreter) 언어도 있습니다. 우리가 배울 C#은 컴파일 언어이지만 컴파일과 인터프리터의 장점을 가지는 하이브리드
언어로도 표현합니다.

  * 컴파일(Compile) 
    * 소스 코드를 기계 코드로 실행 
    * C, C++ 등 
  * 인터프리트(Interpret) 
    * 소스 코드를 인터프리터로 실행 
    * JavaScript, Python, PHP 등 
  * 하이브리드(물론, 둘 다 컴파일 언어임) 

## C# 소개

C#은 Microsoft에서 만든 개체 지향 프로그래밍 언어입니다. C# 프로그래밍 언어를 사용하면 데스크톱, 웹, 모바일, 게임 프로그램
등 분야를 가리지 않고 프로그램을 작성할 수 있습니다. 수많은 프로그래밍 언어 중에서 전 세계 개발자들에게 오랜 기간동안 가장 많이 사용되는
언어 중 하나입니다.

C#은 C언어 프로그래밍 계열(Family)의 개체 지향 프로그래밍 언어입니다. C#은 2000년 7월에 Microsoft
PDC(Professional Developers Conference) 행사에서 닷넷 프레임워크(.NET Framework)와 함께
소개되었습니다.

### C# 프로그래밍 언어

C#은 소프트웨어 즉, 응용 프로그램을 만들기 위한 프로그래밍 언어입니다. 프로그래밍 언어는 C# 이외에도 C, C++, Java,
Python, TypeScript 등 굉장히 많은 언어들이 있습니다. C#의 장점은 하나의 프로그래밍 언어를 배운 후 이를 가지고 데스크톱
프로그램 및 웹 프로그램 그리고 모바일과 게임 프로그램 등을 제작할 수 있다는 데 있습니다.

  * C#은 마이크로소프트의 최고 엔지니어 개발자인 앤더스 헤일스버그(Anders Hejlsberg)에 의해서 디자인되었습니다. 
  * C#은 2000년 7월 MS PDC 행사에서 처음으로 소개되었습니다. 
  * C# 프로그래밍 언어는 5.0 버전까지는 버전마다 큰 변화가 있었습니다. 그 이후로 6.0 버전부터 11.0 버전까지는 작지만 개발자에게 도움을 주는 기능들을 다수 추가하는 방식으로 업데이트가 되고 있습니다. 
  * C#은 강력하고 재 사용 가능한 응용 프로그램을을 쉽게 만들 수 있습니다. 

#####  CAUTION

C#을 만든 사람의 이름은 앤더스 헤일스버그(Anders Hejlsberg)입니다. 본인이 직접 그 이름으로 소개합니다.

### C#의 특징

C# 프로그래밍 언어의 특징은 다음과 같습니다. 대부분 처음보는 단어가 나오니 가볍게 한 번 읽어보세요. 자세한 내용들은 이어지는 강의들을
통해서 계속해서 학습할 예정입니다.

  * C#은 .NET을 위한 많은 언어 중 하나입니다. 
  * C#은 Microsoft의 .NET 플랫폼 기반의 프로그래밍 언어입니다. 
  * 절차적 언어와 개체 지향적 언어의 특징 그리고 함수형 프로그래밍 스타일을 제공하는 다중 패러다임 프로그래밍 언어입니다. 
  * C#은 C, C++, Java, JavaScript와 기초 문법이 비슷한 프로그래밍 언어입니다. 
  * C#은 메모리 관리를 자동으로 합니다. 
  * C#은 컴파일 기반 언어입니다. 
  * C#은 C와 JavaScript와 달리 Global 함수 및 변수는 없이 모두 클래스 안에서 생성됩니다. 
  * C#은 강력한 형식(Strongly Typed)의 언어입니다. 
  * 제네릭과 LINQ의 편리한 기능을 제공합니다. 

### C# 영역

C#은 일반적인 프로그래밍 영역을 모두 다룹니다.

  * 데스크톱 응용 프로그램 
  * 웹 응용 프로그램 
  * 모바일 응용 프로그램 
  * 데이터베이스 응용 프로그램 
  * 게임 프로그램 
  * 클라우드 프로그램 
  * IoT 프로그램 

**그림:** C#과 .NET의 영역

![.NET](https://www.dotnetnote.com/docs/csharp/1-csharp/images/csharp-
dotnet.png)

### C#의 역사와 버전

C#은 굉장히 오랜 기간 발전해 온 프로그래밍 언어입니다. 다음 이어지는 내용들은 간단히 읽고 넘어가면 됩니다.

#### C# 나오기 전의 프로그래밍 세계

C#이 세상에 나오기 전에는 Visual Basic, C, C++, Java 등의 프로그래밍 언어가 많이 사용되었습니다.

  * Win32 API : C언어 기반의 Windows 응용 프로그램 제작 명령어들의 집합 
  * MFC : C++ 기반의 OOP 프로그래밍 환경 

#### C# 버전

C#은 1.0 버전부터 11.0 버전까지 오랜기간 발전해 왔습니다. 이 강의 전체를 통해서 학생 개발자를 위한 C#의 거의 모든 기능을
학습합니다. 다음 표는 앞으로 배울 내용이니 참고용으로 보시면 됩니다.

버전  |  발표  |  특징   
---|---|---  
1.0  |  2002년 2월 13일  |  C#의 첫번째 버전   
닷넷 프레임워크(.NET Framework) 1.0  
간결하고 현대화된 언어  
관리된 코드(Managed Code)  
자동화된 가비지 컬렉션(Garbage Collection)  
1.1  |  2003년  |  Visual Studio 도구 기능 향상   
2.0  |  2005년  |  제네릭(Generics)   
부분(Partial) 클래스  
무명 메서드(Anonymous Method)  
이터레이터(반복기, Iterator)  
널 가능 형식(Nullable Types)  
Static 클래스  
3.0  |  2006년  |  암시적으로 형식화된 변수(Implicitly Typed Local Variables)   
개체 이니셜라이저(Object Initializer)  
컬렉션 이니셜라이저(Collection Initializer)  
무명 형식(Anonymous Types, 익명 형식)  
확장 메서드(Extension methods)  
람다 식(Lambda Expressions)  
자동 구현 속성(Auto-Implemented Properties)  
쿼리 식(Query Expressons)  
익스프레션 트리(Expression Trees)  
3.5  |  2007년  |  LINQ(Language Integrated Query)   
4.0  |  2010년  |  다이나믹 바인딩(Dynamic Binding)   
명명된 또는 선택적 인수(Named & Optional Arguments)  
4.5  |  2012년  |   
5.0  |  2013년  |  비동기(async와 await)   
비동기 메서드(Asynchronous Methods)  
6.0  |  2014년  |  문자열 보간법(String Interpolation)   
정적 멤버를 위한 using static 구문  
자동 속성 이니셜라이저(Auto-Property Initializers)  
널 조건부 연산자(Null-Conditional Operator)  
식 본문 멤버(Expression-Bodied Members)  
nameof 연산자  
7.0  |  2016년  |  튜플(Tuples)과 튜플 해체(Deconstruction)   
패턴 매칭(Pattern Matching)  
숫자 구분자(Digit Separator)와 이진 리터럴(Binary Literals)  
로컬 함수(Local Functions)  
참조 반환(ref returns)  
out 키워드 기능 향상(out var)  
8.0  |  2019년  |  nullable 참조 형식   
비동기 스트림  
9.0  |  2020년  |  Top Level Statements   
10.0  |  2021년  |  ...   
11.0  |  2022년  |  ...   
  
아직 C#에 대해서 전혀 배우지 않은 상태에서 위 표를 제시하는 이유는 C#이 오랜 기간동안 꾸준히 프로그래밍 언어로서 발전을 해왔다는
사실을 보여주기 위함입니다.

버전  |  출시 연도  |  기능 및 주요 변경 사항   
---|---|---  
C# 1.0  |  2002  |  초기 버전, 기본 문법 및 기능 추가   
C# 2.0  |  2005  |  C# 1.0 대비 개선된 문법 및 기능 추가, Nullable 데이터 타입 등   
C# 3.0  |  2007  |  람다식, 익명 타입, LINQ(Language-Integrated Query) 등 추가   
C# 4.0  |  2010  |  선택적 매개변수, 동적(dynamic) 키워드, 콜렉션 초기화 등 추가   
C# 5.0  |  2012  |  async/await 키워드, Caller Information 특성, 제네릭 반변성 등 추가   
C# 6.0  |  2015  |  null 조건부 연산자, 문자열 보간, using static 키워드 등 추가   
C# 7.0  |  2017  |  튜플(Tuple) 기능 추가, out 변수 지정, 패턴 매칭 등 추가   
C# 7.1  |  2017  |  async main 메서드, default 리터럴 표현식 등 추가   
C# 7.2  |  2018  |  private 보호 수준 프로퍼티 getter, ref readonly 지원 등 추가   
C# 7.3  |  2018  |  value Tuple 확장, ref readonly struct, enum 형식에 대한 고정 크기 buffer 추가   
C# 8.0  |  2019  |  nullable 참조형식, switch 식 패턴 매칭, 정적 로컬 함수 등 추가   
C# 9.0  |  2020  |  레코드(Record) 타입, init accessors, pattern matching for property 등 추가   
C# 10.0  |  2022  |  Global using, file-scoped namespaces, interpolated strings, lambda discard 등 추가   
  
### C#의 디자인 철학

C# 6.0 이후로는 디자인 철학이 큰 변화는 없지만 작은 기능들이 지속적으로 추가되고 깨끗한 코드가 만들어지도록 하는 노력들이 담기고
있습니다.

C#의 독특한 특징 중 하나는 100% 하위 호환성을 지키고 있습니다. C# 1.0 버전부터 11.0 버전까지 올라오면서 낮은 버전에서
지원하던 기능이 높은 버전으로 올라가면서 없어진게 단 하나도 없습니다.

### 새로운 C# 그리고 닷넷(.NET)

처음 C#이 만들어질 당시에는 Windows 기반의 .NET Framework에서 실행되었지만, 지금은 크로스 플랫폼을 지원하는 .NET
Core 기반으로 제공됩니다. 이제는 닷넷프레임워크와 닷넷코어는 합쳐서 그냥 닷넷으로 부릅니다.

  * 크로스 플랫폼 
  * 오픈소스 
  * 원하는 모든 에디터 사용 개발 
    * Visual Studio Code 
    * Visual Studio 

## 닷넷(.NET) 생태계

### .NET

.NET은 소프트웨어 프레임워크입니다. .NET은 응용 프로그램 개발 속도를 높이는 데 도움이되는 API(Application
Programming Interface) 및 서비스 모음입니다. 2002년 2월 13일 처음으로 1.0 버전으로 세상에 공개되었고 동일하게
C#도 1.0 버전으로 출시가 되었습니다. .NET으로 시작되는 많은 용어는 모두 .NET 생태계에 포함됩니다. 예를 들어, .NET
Framework, .NET Core, .NET Standard 등이 그것입니다. C#은 .NET 생태계의 모든 영역에서 사용할 수 있는
프로그래밍 언어입니다. 필자가 C#을 첫 번째 언어로 사용하고 있는 이유는 .NET의 모든 영역에서 사용할 수 있고 LINQ라는 기능을
통해서 쉽게 프로그래밍을 할 수 있기때문입니다.

**그림:** 닷넷 생태계

![.NET 생태계](https://www.dotnetnote.com/docs/csharp/1-csharp/images/dotnet-
ecosystem.png)

닷넷(.NET)은 다음과 같이 정리할 수 있습니다.

  * 무료, 오픈 소스, 크로스 플랫폼 개발 환경 
  * 런타임 엔진(여러 명령어들의 집합) 
  * 여러 언어 제공: C#, Visual Basic, F# 
  * 웹, 데스크톱, 모바일, 게임, IoT, 클라우드 등 모든 영역의 개발 환경 제공 

.NET은 내부적으로 CLR과 FCL로 구분할 수 있습니다. 다음은 간단히 읽고 넘어갑니다.

  * CLR(Common Language Runtime): 런타임 엔진으로 닷넷의 모든 소프트웨어를 돌리는 엔진 역할을 합니다. 
    * CLR에는 Type System, Garbage Collector, Exception Handling 등의 기능들이 들어 있습니다. 
  * FCL(Framework Class Library): 라이브러리 모음으로 닷넷 개발에 필요한 필수 라이브러리 클래스들의 집합입니다. 참고로, Windows Terminal 또는 Windows의 명령 프롬프트에서 “dotnet --info” 명령어를 실행하면 설치되어 있는 .NET에 대한 상세 정보를 확인할 수 있습니다. 

### .NET Framework

.NET Framework는 Windows 기반 운영체제에 설치되고 ASP.NET, Windows Forms, WPF 등의 기술을
포함합니다. C#은 .NET Framework의 일부입니다. .NET Framework는 실행 환경입니다. 닷넷 프레임워크(.NET
Framework)는 운영체제, 데이터베이스와 같이 프로그래밍을 위한 API의 집합체를 가리킵니다. 여기서 API(Application
Programming Interface)는 프로그래밍을 위한 주요 명령어들의 모음을 뜻합니다. .NET Framework는 응용 프로그램을
만드는 또 다른 종류의 소프트웨어입니다. 운영 체제, 데이터베이스 및 .NET 프레임워크는 모두 하나의 큰 소프트웨어 프로그램입니다. 응용
프로그램을 작성하려면 프로그래밍 언어가 필요합니다. C#, Visual Basic 및 F#과 같은 프로그래밍 언어는 .NET
Framework에 포함되어 있습니다.

### .NET Core

.NET Core는 크로스 플랫폼을 지원하고 ASP.NET Core, Blazor, Windows Forms, WPF 등의 기술을
포함합니다. .NET Core는 많은 버전들이 하나의 머신에서 함께 실행될 수 있으며 .NET Framework 기반보다 성능향상에 중점을
두고 있습니다.

### .NET MAUI와 자마린(Xamarin)

C# 프로그래밍 언어를 사용하여 모바일 응용 프로그램을 제작할 수 있습니다. 이 때 사용할 수 있는 기술이 마우이(MAUI) 및
자마린(Xamarin)입니다. 이 기술들을 사용하게 되면 iOS, Android 기반의 모바일 응용 프로그램을 C#과 XAML 기술로 만들어
낼 수 있습니다.

### .NET Standard

.NET Framework, .NET Core, 모바일 개발 영역에서 공통적으로 사용할 코드를 모아 놓는 기능을 닷넷 표준(.NET
Standard)로 볼 수 있습니다.

### 유니티(Unity)

.NET 생태계에 직접적으로 포함되지 않지만, 게임 엔진 중 유명한 유니티에서 가장 많이 사용되는 언어 중 하나가 C#입니다. 게임을 제작할
때 게임 로직을 C# 프로그래밍 언어를 사용하여 제작합니다.

## 이 강의의 범위

이 강의에서는 C#과 닷넷으로 할 수 있는 굉장히 많은 부분 중에서 다음 그림의 첫 번째에 해당하는 C#의 기초에 대해서 다룹니다.

**그림:** C#의 범위

![C#의 범위](https://www.dotnetnote.com/docs/csharp/1-csharp/images/csharp-
category.png)

## 요약

프로그래밍을 학습할 때 처음으로 C#을 선택했다면 이는 탁월한 선택 중 하나입니다. C#은 가장 현대적인 프로그래밍 문법과 도구를 제공하고
모든 영역의 프로그래밍을 가능하게 해줍니다. 이 강의 전체를 통해서 C# 프로그래밍 언어를 사용하여 프로그램을 작성할 수 있는 기초를 완성해
나가도록 하겠습니다.


-->

<!--






-->

