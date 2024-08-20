---
title: "[C#] C# 프로그램의 일반적인 구조체"
categories: CSharp
tags:
- CSharp
- programming
- .NET
- software development
- coding
- console application
- Main method
- namespaces
- classes
- structs
- interfaces
- enums
- delegates
- command line arguments
- async programming
- top-level statements
- error handling
- factorial
- data types
- variables
- methods
- return values
- exception handling
- Visual Studio
- .NET Core
- command line tools
- application structure
- programming concepts
- software engineering
- development environment
- coding standards
- best practices
- debugging
- performance
- code organization
- project management
- software architecture
- user input
- string manipulation
- data conversion
- task management
- asynchronous programming
- code examples
- tutorials
- learning resources
- programming languages
- software lifecycle
- application design
- system architecture
header:
teaser: /assets/images/undefined/teaser.jpg
---

C# 프로그램은 여러 파일로 구성되며, 각 파일은 0개 이상의 네임스페이스를 포함할 수 있다. 네임스페이스는 클래스, 구조체, 인터페이스, 열거형 및 대리자와 같은 다양한 형식을 포함하며, 이러한 요소들은 프로그램의 구조를 형성하는 데 중요한 역할을 한다. 예를 들어, C# 프로그램의 기본 구조는 최상위 문을 사용하여 간단하게 작성할 수 있으며, 이 경우 프로그램의 진입점은 `Main` 메서드가 아닌 최상위 문이 된다. 또한, `Main` 메서드는 C# 애플리케이션의 진입점으로, 애플리케이션이 시작될 때 호출되는 첫 번째 메서드이다. C#에서는 하나의 진입점만 존재할 수 있으며, 여러 개의 `Main` 메서드가 있을 경우 컴파일러 옵션을 통해 진입점을 지정해야 한다. 이러한 구조는 C# 언어의 기본 개념을 이해하는 데 도움을 주며, 비동기 프로그래밍, 명령줄 인수 처리, 예외 처리와 같은 다양한 프로그래밍 기법을 활용할 수 있는 기초를 제공한다. C#의 언어 사양을 참고하면 이러한 요소들에 대한 더 깊은 이해를 얻을 수 있으며, 이를 통해 보다 효율적이고 안정적인 소프트웨어를 개발할 수 있다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## C# 프로그램의 일반적인 구조체
**C# 프로그램의 기본 구성 요소**  
**네임스페이스와 클래스**  
**구조체, 인터페이스, 열거형 및 대리자**  
**최상위 문과 진입점**

## C# 언어 사양
**C# 언어 사양 개요**  
**기본 개념 및 문법**  

## Main()과 명령줄 인수
**Main() 메서드의 역할**  
**명령줄 인수 처리 방법**  
**Main() 반환 값의 중요성**  

## 비동기 Main 반환 값
**비동기 Main 메서드의 정의**  
**비동기 작업과 Main()의 관계**  

## 명령줄 인수
**명령줄 인수의 사용법**  
**인수 변환 및 검증**  
**예제: 계승 계산기**  

## 최상위 문 - Main 메서드가 없는 프로그램
**최상위 문 개요**  
**최상위 문 사용의 장점**  
**최상위 문과 네임스페이스**  

## Practical Examples
**C# 프로그램 예제 1: Hello World**  
**C# 프로그램 예제 2: 명령줄 인수 처리**  
**C# 프로그램 예제 3: 비동기 작업 처리**  

## Frequently Asked Questions
**C#에서 Main() 메서드는 왜 필요한가요?**  
**최상위 문을 사용할 때의 제한 사항은 무엇인가요?**  
**비동기 Main() 메서드의 장점은 무엇인가요?**  

## Related Technologies
**.NET Framework**  
**.NET Core**  
**Visual Studio**  

## Conclusion
**C# 프로그램 구조의 중요성 요약**  
**Main() 메서드와 명령줄 인수의 역할**  
**최상위 문과 비동기 프로그래밍의 장점**  
---
-->

<!--
---
## C# 프로그램의 일반적인 구조체
**C# 프로그램의 기본 구성 요소**  
**네임스페이스와 클래스**  
**구조체, 인터페이스, 열거형 및 대리자**  
**최상위 문과 진입점**
-->

## C# 프로그램의 일반적인 구조체

**C# 프로그램의 기본 구성 요소**  

C# 프로그램은 여러 구성 요소로 이루어져 있다. 가장 기본적인 구성 요소는 네임스페이스, 클래스, 메서드, 그리고 변수이다. 이러한 요소들은 프로그램의 구조를 정의하고, 코드의 가독성을 높이며, 유지보수를 용이하게 한다. C#은 객체 지향 프로그래밍 언어로, 클래스와 객체를 중심으로 설계되었다. 따라서 클래스는 C# 프로그램의 핵심적인 구성 요소라고 할 수 있다.

**네임스페이스와 클래스**  

네임스페이스는 관련된 클래스와 기타 타입을 그룹화하는 데 사용된다. 이를 통해 코드의 충돌을 방지하고, 코드의 구조를 명확하게 할 수 있다. 클래스는 객체의 속성과 동작을 정의하는 청사진으로, 객체 지향 프로그래밍의 기본 단위이다. C#에서는 클래스 내에 메서드, 속성, 필드 등을 정의하여 객체의 행동을 구현할 수 있다.

**구조체, 인터페이스, 열거형 및 대리자**  

C#에서는 구조체(struct), 인터페이스(interface), 열거형(enum), 대리자(delegate)와 같은 다양한 타입을 제공한다. 구조체는 값 타입으로, 간단한 데이터 구조를 정의하는 데 사용된다. 인터페이스는 클래스가 구현해야 하는 메서드의 집합을 정의하며, 다형성을 지원한다. 열거형은 관련된 상수 집합을 정의하는 데 유용하며, 대리자는 메서드 참조를 캡슐화하여 이벤트 처리와 콜백 메서드를 구현하는 데 사용된다.

**최상위 문과 진입점**  

C# 프로그램의 진입점은 Main() 메서드이다. 이 메서드는 프로그램이 시작되는 지점을 정의하며, 프로그램의 실행 흐름을 제어한다. 최상위 문은 C# 9.0에서 도입된 기능으로, Main() 메서드 없이도 프로그램을 작성할 수 있게 해준다. 이를 통해 코드의 간결성을 높이고, 간단한 스크립트 작성이 가능해진다. 

--- 

이와 같은 구조를 통해 C# 프로그램은 명확하고 효율적으로 작성될 수 있다. 각 구성 요소는 서로 유기적으로 연결되어 있으며, 이를 통해 복잡한 프로그램도 체계적으로 관리할 수 있다.

<!--
## C# 언어 사양
**C# 언어 사양 개요**  
**기본 개념 및 문법**  
-->

## C# 언어 사양

**C# 언어 사양 개요**  

C# 언어 사양은 C# 프로그래밍 언어의 문법, 의미, 그리고 사용 방법에 대한 공식적인 설명이다. 이 사양은 C# 언어의 모든 기능과 규칙을 정의하며, 개발자들이 C#을 사용할 때 참고할 수 있는 중요한 자료이다. C#은 객체 지향 프로그래밍 언어로, Microsoft에서 개발하였으며, .NET 플랫폼에서 주로 사용된다. C# 언어 사양은 C#의 버전이 업데이트될 때마다 새로운 기능과 변경 사항을 반영하여 지속적으로 발전하고 있다.

**기본 개념 및 문법**  

C#의 기본 개념은 객체, 클래스, 메서드, 속성 등으로 구성된다. C#은 강타입 언어로, 변수의 타입을 명시해야 하며, 이는 코드의 안정성을 높이는 데 기여한다. 기본적인 문법은 다음과 같다:

- **변수 선언**: `int number;`
- **변수 초기화**: `number = 10;`
- **조건문**: 
  ```csharp
  if (number > 0) {
      Console.WriteLine("Positive number");
  }
  ```
- **반복문**: 
  ```csharp
  for (int i = 0; i < 5; i++) {
      Console.WriteLine(i);
  }
  ```

C#의 문법은 Java와 유사하지만, LINQ, async/await와 같은 고급 기능을 제공하여 개발자들이 더 효율적으로 코드를 작성할 수 있도록 돕는다. C#의 문법을 이해하는 것은 프로그래밍의 기초를 다지는 데 매우 중요하다.

<!--
## Main()과 명령줄 인수
**Main() 메서드의 역할**  
**명령줄 인수 처리 방법**  
**Main() 반환 값의 중요성**  
-->

## Main()과 명령줄 인수

**Main() 메서드의 역할**  

C# 프로그램에서 Main() 메서드는 프로그램의 진입점이다. 즉, 프로그램이 시작될 때 가장 먼저 호출되는 메서드로, 모든 C# 프로그램은 반드시 하나의 Main() 메서드를 가져야 한다. Main() 메서드는 프로그램의 실행 흐름을 제어하며, 다른 메서드나 클래스를 호출하여 프로그램의 기능을 수행하게 된다. Main() 메서드는 다음과 같은 형식으로 정의할 수 있다:

```csharp
static void Main(string[] args)
{
    // 프로그램 코드
}
```

여기서 `string[] args`는 명령줄 인수를 받을 수 있는 매개변수이다. 이 매개변수를 통해 사용자가 프로그램을 실행할 때 입력한 인수를 받아 처리할 수 있다.

**명령줄 인수 처리 방법**  

명령줄 인수는 프로그램 실행 시 사용자로부터 입력받는 값으로, 프로그램의 동작을 제어하는 데 유용하다. Main() 메서드의 `args` 매개변수를 통해 명령줄 인수를 받을 수 있으며, 이를 배열 형태로 처리할 수 있다. 예를 들어, 사용자가 프로그램을 실행할 때 다음과 같이 입력했다고 가정해 보자:

```
myProgram.exe arg1 arg2 arg3
```

이 경우 `args` 배열은 `{"arg1", "arg2", "arg3"}`와 같은 값을 가지게 된다. 이를 통해 프로그램은 사용자가 입력한 인수에 따라 다르게 동작할 수 있다. 예를 들어, 특정 인수가 입력되었을 때 다른 기능을 수행하도록 코드를 작성할 수 있다.

**Main() 반환 값의 중요성**  

Main() 메서드는 반환 값을 가질 수 있으며, 이는 프로그램의 종료 상태를 나타낸다. 일반적으로 `int` 형식으로 반환되며, 0은 성공적인 종료를 의미하고, 0이 아닌 값은 오류를 나타낸다. 반환 값을 통해 운영 체제나 다른 프로그램은 현재 프로그램의 실행 결과를 확인할 수 있다. 예를 들어, 다음과 같이 Main() 메서드를 정의할 수 있다:

```csharp
static int Main(string[] args)
{
    // 프로그램 코드
    return 0; // 성공적으로 종료
}
```

이와 같이 Main() 메서드는 C# 프로그램의 핵심적인 역할을 하며, 명령줄 인수와 반환 값을 통해 프로그램의 유연성을 높일 수 있다.

<!--
## 비동기 Main 반환 값
**비동기 Main 메서드의 정의**  
**비동기 작업과 Main()의 관계**  
-->

## 비동기 Main 반환 값

**비동기 Main 메서드의 정의**  

비동기 Main 메서드는 C# 7.1부터 도입된 기능으로, 프로그램의 진입점인 Main() 메서드에서 비동기 작업을 수행할 수 있도록 해준다. 전통적으로 Main() 메서드는 동기적으로 실행되었지만, 비동기 Main() 메서드를 사용하면 비동기 프로그래밍 모델을 활용하여 더 효율적인 코드 작성을 가능하게 한다. 비동기 Main() 메서드는 `async` 키워드를 사용하여 정의되며, 반환 타입은 `Task` 또는 `Task<int>`가 될 수 있다. 

예를 들어, 다음과 같은 형태로 비동기 Main() 메서드를 정의할 수 있다:

```csharp
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        await SomeAsyncMethod();
    }

    static async Task SomeAsyncMethod()
    {
        // 비동기 작업 수행
    }
}
```

**비동기 작업과 Main()의 관계**  

비동기 Main() 메서드는 비동기 작업을 수행하는 데 있어 중요한 역할을 한다. 비동기 작업은 일반적으로 I/O 작업이나 네트워크 요청과 같이 시간이 오래 걸리는 작업을 비동기적으로 처리하여 프로그램의 응답성을 높이는 데 사용된다. 비동기 Main() 메서드를 사용하면 이러한 비동기 작업을 메인 스레드에서 직접 호출할 수 있으며, 프로그램이 종료되기 전에 모든 비동기 작업이 완료될 때까지 기다릴 수 있다.

비동기 Main() 메서드의 사용은 특히 대규모 애플리케이션에서 유용하다. 예를 들어, 여러 개의 비동기 API 호출을 동시에 수행하고, 모든 호출이 완료된 후 결과를 처리하는 경우 비동기 Main() 메서드를 통해 코드의 가독성을 높이고, 성능을 최적화할 수 있다.

이와 같이 비동기 Main() 메서드는 C# 프로그래밍에서 비동기 작업을 보다 쉽게 관리할 수 있도록 도와주는 중요한 기능이다.

<!--
## 명령줄 인수
**명령줄 인수의 사용법**  
**인수 변환 및 검증**  
**예제: 계승 계산기**  
-->

## 명령줄 인수

**명령줄 인수의 사용법**  

명령줄 인수는 프로그램을 실행할 때 외부에서 전달되는 값이다. C#에서는 `Main` 메서드의 매개변수로 `string[] args`를 사용하여 이러한 인수를 받을 수 있다. 사용자는 프로그램을 실행할 때 인수를 입력할 수 있으며, 이 인수들은 배열 형태로 `args`에 저장된다. 예를 들어, 사용자가 `MyProgram.exe arg1 arg2`와 같이 프로그램을 실행하면, `args` 배열은 `["arg1", "arg2"]`와 같은 값을 가지게 된다.

명령줄 인수는 프로그램의 동작을 제어하는 데 유용하다. 예를 들어, 파일 경로, 설정 값, 또는 특정 모드로 실행할 때 필요한 플래그 등을 전달할 수 있다. 이를 통해 사용자는 프로그램을 보다 유연하게 사용할 수 있다.

**인수 변환 및 검증**  

명령줄 인수는 문자열 형태로 전달되기 때문에, 필요한 경우 적절한 데이터 타입으로 변환해야 한다. 예를 들어, 숫자형 인수를 필요로 하는 경우 `int.Parse()` 또는 `Convert.ToInt32()`와 같은 메서드를 사용하여 문자열을 정수로 변환할 수 있다. 변환 과정에서 예외가 발생할 수 있으므로, 항상 예외 처리를 통해 안정성을 확보해야 한다.

인수의 유효성을 검증하는 것도 중요하다. 사용자가 잘못된 형식의 인수를 입력할 경우, 프로그램이 예기치 않게 종료될 수 있다. 따라서, 인수의 개수와 형식을 체크하고, 필요에 따라 사용자에게 올바른 입력을 요구하는 로직을 추가하는 것이 좋다.

**예제: 계승 계산기**  

아래는 명령줄 인수를 사용하여 계승을 계산하는 간단한 C# 프로그램의 예제이다.

```csharp
using System;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.WriteLine("사용법: MyProgram.exe <정수>");
            return;
        }

        if (int.TryParse(args[0], out int number) && number >= 0)
        {
            long result = Factorial(number);
            Console.WriteLine($"{number}! = {result}");
        }
        else
        {
            Console.WriteLine("유효한 양의 정수를 입력하세요.");
        }
    }

    static long Factorial(int n)
    {
        if (n == 0) return 1;
        return n * Factorial(n - 1);
    }
}
```

이 프로그램은 사용자가 입력한 정수의 계승을 계산한다. 사용자가 인수를 제공하지 않거나 잘못된 형식의 인수를 입력할 경우, 적절한 오류 메시지를 출력한다.

<!--
## 최상위 문 - Main 메서드가 없는 프로그램
**최상위 문 개요**  
**최상위 문 사용의 장점**  
**최상위 문과 네임스페이스**  
-->

## 최상위 문 - Main 메서드가 없는 프로그램

**최상위 문 개요**  

최상위 문은 C# 9.0에서 도입된 기능으로, 전통적인 Main() 메서드 없이도 프로그램을 작성할 수 있게 해준다. 이 기능은 코드의 간결성을 높이고, 특히 간단한 스크립트나 예제 코드를 작성할 때 유용하다. 최상위 문을 사용하면, 개발자는 클래스나 네임스페이스를 정의하지 않고도 직접적으로 코드를 작성할 수 있다. 이는 C#의 문법을 더욱 직관적으로 만들어 주며, 초보자들이 쉽게 접근할 수 있도록 돕는다.

**최상위 문 사용의 장점**  

최상위 문을 사용하는 주요 장점 중 하나는 코드의 가독성을 높인다는 것이다. 전통적인 C# 프로그램에서는 Main() 메서드와 클래스 정의가 필요했지만, 최상위 문을 사용하면 이러한 구조를 생략할 수 있다. 이로 인해 코드가 간결해지고, 불필요한 구문을 줄일 수 있다. 또한, 최상위 문은 스크립트 언어와 유사한 방식으로 코드를 작성할 수 있게 해주어, 빠른 프로토타입 개발이나 간단한 작업을 수행할 때 매우 유용하다.

**최상위 문과 네임스페이스**  

최상위 문은 네임스페이스와 함께 사용할 수 있다. 네임스페이스를 정의하면, 코드의 구조를 더욱 명확하게 할 수 있으며, 다른 코드와의 충돌을 방지할 수 있다. 최상위 문 내에서 네임스페이스를 정의하면, 해당 네임스페이스 내에서 작성된 모든 코드는 그 네임스페이스의 범위 내에서 실행된다. 이는 코드의 모듈화를 촉진하고, 대규모 프로젝트에서의 관리성을 높이는 데 기여한다.

최상위 문을 사용하여 간단한 예제를 작성해보자. 아래는 최상위 문을 사용한 Hello World 프로그램의 예시이다.

```csharp
using System;

Console.WriteLine("Hello, World!");
```

위의 코드는 Main() 메서드 없이도 "Hello, World!"를 출력하는 프로그램을 작성할 수 있게 해준다. 이처럼 최상위 문은 C# 프로그래밍의 접근성을 높이고, 개발자들이 더 쉽게 코드를 작성할 수 있도록 돕는다.

<!--
## Practical Examples
**C# 프로그램 예제 1: Hello World**  
**C# 프로그램 예제 2: 명령줄 인수 처리**  
**C# 프로그램 예제 3: 비동기 작업 처리**  
-->

## Practical Examples

**C# 프로그램 예제 1: Hello World**  

C#에서 가장 기본적인 프로그램은 "Hello World"를 출력하는 것이다. 이 프로그램은 C#의 기본 문법을 이해하는 데 큰 도움이 된다. 아래는 "Hello World"를 출력하는 간단한 C# 프로그램의 예제이다.

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

위의 코드는 `using System;`을 통해 System 네임스페이스를 포함하고, `Main` 메서드에서 `Console.WriteLine`을 사용하여 "Hello, World!"라는 문자열을 출력한다. 이 프로그램을 실행하면 콘솔 창에 "Hello, World!"가 나타난다.

**C# 프로그램 예제 2: 명령줄 인수 처리**  

명령줄 인수는 프로그램 실행 시 외부에서 값을 전달하는 방법이다. 아래는 명령줄 인수를 처리하여 사용자에게 입력된 이름을 출력하는 프로그램의 예제이다.

```csharp
using System;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length > 0)
        {
            Console.WriteLine($"Hello, {args[0]}!");
        }
        else
        {
            Console.WriteLine("Hello, World!");
        }
    }
}
```

이 프로그램은 사용자가 명령줄에서 이름을 입력하면 해당 이름을 출력하고, 입력이 없을 경우 "Hello, World!"를 출력한다. 예를 들어, `dotnet run John`이라고 입력하면 "Hello, John!"이 출력된다.

**C# 프로그램 예제 3: 비동기 작업 처리**  

비동기 프로그래밍은 프로그램의 성능을 향상시키는 데 중요한 역할을 한다. 아래는 비동기 메서드를 사용하여 데이터를 비동기적으로 가져오는 예제이다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.github.com/";
        using HttpClient client = new HttpClient();
        client.DefaultRequestHeaders.UserAgent.Add(new System.Net.Http.Headers.ProductInfoHeaderValue("MyApp", "1.0"));
        
        string response = await client.GetStringAsync(url);
        Console.WriteLine(response);
    }
}
```

이 프로그램은 `HttpClient`를 사용하여 비동기적으로 GitHub API에서 데이터를 가져온다. `await` 키워드를 사용하여 비동기 작업이 완료될 때까지 기다린 후, 결과를 출력한다. 비동기 프로그래밍을 통해 UI가 멈추지 않고 사용자 경험을 개선할 수 있다.

<!--
## Frequently Asked Questions
**C#에서 Main() 메서드는 왜 필요한가요?**  
**최상위 문을 사용할 때의 제한 사항은 무엇인가요?**  
**비동기 Main() 메서드의 장점은 무엇인가요?**  
-->

## Frequently Asked Questions

**C#에서 Main() 메서드는 왜 필요한가요?**  

C# 프로그램의 진입점은 Main() 메서드이다. 이 메서드는 프로그램이 시작될 때 가장 먼저 호출되는 메서드로, 프로그램의 실행 흐름을 제어하는 중요한 역할을 한다. Main() 메서드가 없으면 C# 런타임은 프로그램을 시작할 수 없기 때문에, 모든 C# 프로그램은 반드시 Main() 메서드를 포함해야 한다. 이 메서드는 프로그램의 시작 지점을 정의하고, 필요한 초기화 작업을 수행하며, 다른 메서드를 호출하여 프로그램의 주요 기능을 실행하는 데 사용된다.

**최상위 문을 사용할 때의 제한 사항은 무엇인가요?**  

최상위 문은 C# 9.0에서 도입된 기능으로, Main() 메서드 없이도 프로그램을 작성할 수 있게 해준다. 그러나 최상위 문을 사용할 때는 몇 가지 제한 사항이 있다. 첫째, 최상위 문은 네임스페이스 내에서 사용할 수 없으며, 전역 범위에서만 사용할 수 있다. 둘째, 최상위 문은 비동기 메서드를 지원하지 않기 때문에, 비동기 작업을 수행하려면 여전히 Main() 메서드를 사용해야 한다. 마지막으로, 최상위 문은 복잡한 프로그램 구조를 구현하기에는 적합하지 않으므로, 간단한 스크립트나 테스트 용도로 사용하는 것이 좋다.

**비동기 Main() 메서드의 장점은 무엇인가요?**  

비동기 Main() 메서드는 C# 7.1부터 지원되며, 비동기 프로그래밍을 보다 쉽게 구현할 수 있게 해준다. 비동기 Main() 메서드를 사용하면, 프로그램의 시작 지점에서 비동기 작업을 직접 호출할 수 있어 코드의 가독성이 향상된다. 또한, 비동기 작업을 수행하는 동안 UI 스레드를 차단하지 않기 때문에, 사용자 경험을 개선할 수 있다. 이로 인해, 네트워크 요청이나 파일 I/O와 같은 시간이 오래 걸리는 작업을 비동기적으로 처리할 수 있어 프로그램의 성능을 높일 수 있다.

<!--
## Related Technologies
**.NET Framework**  
**.NET Core**  
**Visual Studio**  
-->

## Related Technologies

**.NET Framework**  

.NET Framework는 Microsoft에서 개발한 소프트웨어 프레임워크로, Windows 운영 체제에서 실행되는 응용 프로그램을 개발하는 데 사용된다. 이 프레임워크는 다양한 프로그래밍 언어를 지원하며, 특히 C#과 VB.NET이 널리 사용된다. .NET Framework는 CLR(Common Language Runtime)을 기반으로 하여 메모리 관리, 예외 처리, 보안 및 스레드 관리를 제공한다. 또한, Windows Forms, WPF(Windows Presentation Foundation), ASP.NET과 같은 다양한 라이브러리와 API를 포함하고 있어 개발자들이 GUI 애플리케이션 및 웹 애플리케이션을 쉽게 만들 수 있도록 돕는다.

**.NET Core**  

.NET Core는 Microsoft에서 개발한 오픈 소스 크로스 플랫폼 프레임워크로, Windows, macOS 및 Linux에서 실행되는 애플리케이션을 개발할 수 있게 해준다. .NET Core는 경량화된 아키텍처를 가지고 있어 성능이 뛰어나며, 클라우드 기반 애플리케이션 및 마이크로서비스 아키텍처에 적합하다. 또한, .NET Core는 모듈화된 구조를 가지고 있어 필요한 구성 요소만 선택하여 사용할 수 있다. 이로 인해 개발자들은 더 빠르고 효율적인 애플리케이션을 구축할 수 있다.

**Visual Studio**  

Visual Studio는 Microsoft에서 제공하는 통합 개발 환경(IDE)으로, C#, VB.NET, F# 등 다양한 프로그래밍 언어를 지원한다. 이 IDE는 코드 편집기, 디버거, GUI 디자이너, 데이터베이스 도구 등 다양한 기능을 제공하여 개발자들이 효율적으로 소프트웨어를 개발할 수 있도록 돕는다. Visual Studio는 또한 Git과 같은 버전 관리 시스템과 통합되어 있어 팀 협업이 용이하다. 다양한 확장 기능을 통해 개발 환경을 개인의 필요에 맞게 커스터마이즈할 수 있는 점도 큰 장점이다. 

이와 같은 관련 기술들은 C# 프로그래밍을 보다 효율적이고 효과적으로 수행할 수 있도록 지원하며, 개발자들이 최신 기술 트렌드에 맞춰 애플리케이션을 개발하는 데 큰 도움이 된다.

<!--
## Conclusion
**C# 프로그램 구조의 중요성 요약**  
**Main() 메서드와 명령줄 인수의 역할**  
**최상위 문과 비동기 프로그래밍의 장점**  
---
-->

## Conclusion

**C# 프로그램 구조의 중요성 요약**  

C# 프로그램의 구조는 코드의 가독성과 유지보수성을 높이는 데 중요한 역할을 한다. 명확한 구조를 통해 개발자는 프로그램의 흐름을 쉽게 이해하고, 다른 개발자와의 협업 시에도 효율적으로 작업할 수 있다. C#의 기본 구성 요소인 네임스페이스, 클래스, 메서드 등을 적절히 활용하면 코드의 재사용성과 확장성을 높일 수 있다. 

**Main() 메서드와 명령줄 인수의 역할**  

Main() 메서드는 C# 프로그램의 진입점으로, 프로그램이 시작되는 위치를 정의한다. 이 메서드는 명령줄 인수를 통해 외부에서 입력된 데이터를 처리할 수 있는 기능을 제공한다. 명령줄 인수를 통해 사용자는 프로그램 실행 시 다양한 옵션을 전달할 수 있으며, 이를 통해 프로그램의 동작을 유연하게 조정할 수 있다. 

**최상위 문과 비동기 프로그래밍의 장점**  

최상위 문은 C# 9.0에서 도입된 기능으로, Main() 메서드 없이도 프로그램을 작성할 수 있게 해준다. 이는 코드의 간결성을 높이고, 작은 프로그램을 작성할 때 유용하다. 비동기 프로그래밍은 프로그램의 성능을 향상시키는 데 중요한 역할을 하며, 비동기 Main() 메서드를 통해 비동기 작업을 쉽게 처리할 수 있다. 이러한 기능들은 C# 프로그래밍의 유연성과 효율성을 높이는 데 기여한다. 

---

<!--
##### Reference #####
-->

## Reference


* [https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/](https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/main-command-line](https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/main-command-line)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/top-level-statements](https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/program-structure/top-level-statements)


<!--
#  C# 프로그램의 일반적인 구조체

##  이 문서의 내용

C# 프로그램은 하나 이상의 파일로 구성됩니다. 각 파일은 0개 이상의 네임스페이스가 포함합니다. 네임스페이스는 클래스, 구조체,
인터페이스, 열거형 및 대리자와 같은 형식이나 다른 네임스페이스를 포함합니다. 다음 예제는 이러한 모든 요소를 포함하는 C# 프로그램의 기본
구조입니다.

    
    
    // A skeleton of a C# program
    using System;
    
    // Your program starts here:
    Console.WriteLine("Hello world!");
    
    namespace YourNamespace
    {
        class YourClass
        {
        }
    
        struct YourStruct
        {
        }
    
        interface IYourInterface
        {
        }
    
        delegate int YourDelegate();
    
        enum YourEnum
        {
        }
    
        namespace YourNestedNamespace
        {
            struct YourStruct
            {
            }
        }
    }
    

앞의 예제에서는 프로그램의 진입점에 대해 _최상위 문_ 을 사용합니다. 다음 예제와 같이 프로그램의 진입점으로 ` Main ` (이)라는
정적 메서드를 만들 수도 있습니다.

    
    
    // A skeleton of a C# program
    using System;
    namespace YourNamespace
    {
        class YourClass
        {
        }
    
        struct YourStruct
        {
        }
    
        interface IYourInterface
        {
        }
    
        delegate int YourDelegate();
    
        enum YourEnum
        {
        }
    
        namespace YourNestedNamespace
        {
            struct YourStruct
            {
            }
        }
    
        class Program
        {
            static void Main(string[] args)
            {
                //Your program starts here...
                Console.WriteLine("Hello world!");
            }
        }
    }
    

기본 사항 가이드의 [ 형식 ](../types/) 섹션에서 이러한 프로그램 요소에 대해 알아봅니다.

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../../language-reference/language-specification/readme) 의
[ 기본 개념 ](../../language-reference/language-specification/basic-concepts) 을
참조하세요. 언어 사양은 C# 구문 및 사용법에 대 한 신뢰할 수 있는 소스 됩니다.


-->

<!--






-->

<!--
#  Main()과 명령줄 인수

##  이 문서의 내용

` Main ` 메서드는 C# 애플리케이션의 진입점입니다. 애플리케이션이 시작될 때 ` Main ` 메서드는 호출되는 첫 번째 메서드입니다.

C# 프로그램에는 하나의 진입점만 있을 수 있습니다. ` Main ` 메서드가 있는 클래스가 둘 이상 있는 경우
**StartupObject** 컴파일러 옵션으로 프로그램을 컴파일하여 진입점으로 사용할 ` Main ` 메서드를 지정해야 합니다. 자세한
내용은 [ **StartupObject** (C# 컴파일러 옵션) ](../../language-reference/compiler-
options/advanced#mainentrypoint-or-startupobject) 를 참조하세요.

    
    
    class TestClass
    {
        static void Main(string[] args)
        {
            // Display the number of command line arguments.
            Console.WriteLine(args.Length);
        }
    }
    

한 파일의 최상위 문을 애플리케이션의 진입점으로 사용할 수도 있습니다. ` Main ` 메서드와 마찬가지로 최상위 문은  값을 반환  하고
명령줄 인수  에 액세스할 수도 있습니다. 자세한 내용은 [ 최상위 문 ](top-level-statements) 을 참조하세요.

    
    
    using System.Text;
    
    StringBuilder builder = new();
    builder.AppendLine("The following arguments are passed:");
    
    // Display the command line arguments using the args variable.
    foreach (var arg in args)
    {
        builder.AppendLine($"Argument={arg}");
    }
    
    Console.WriteLine(builder.ToString());
    
    // Return a success code.
    return 0;
    

##  개요

  * ` Main ` 메서드는 실행 가능한 프로그램의 진입점으로, 프로그램의 제어가 시작되고 끝나는 위치합니다. 
  * ` Main ` 은 클래스 또는 구조체 내에서 선언되어야 합니다. 바깥쪽 ` class ` 는 ` static ` 일 수 있습니다. 
  * ` Main ` 해야 [ ` static ` ](../../language-reference/keywords/static) 합니다. 
  * ` Main ` 는 [ 액세스 한정자 ](../../programming-guide/classes-and-structs/access-modifiers) 를 가질 수 있습니다( ` file ` 제외). 
  * ` Main ` 은 ` void ` , ` int ` , ` Task ` 또는 ` Task<int> ` 반환 형식을 가질 수 있습니다. 
  * ` Main ` 에서 ` Task ` 또는 ` Task<int> ` 을 반환하는 경우에만 ` Main ` 선언에 [ ` async ` ](../../language-reference/keywords/async) 한정자가 포함될 수 있습니다. 이는 특히 ` async void Main ` 메서드를 제외합니다. 
  * ` Main ` 메서드는 명령줄 인수를 포함하는 ` string[] ` 매개 변수 사용 여부에 관계 없이 선언될 수 있습니다. Visual Studio를 사용하여 Windows 애플리케이션을 만드는 경우 매개 변수를 수동으로 추가하거나 [ GetCommandLineArgs() ](/ko-kr/dotnet/api/system.environment.getcommandlineargs#system-environment-getcommandlineargs) 메서드를 사용하여 명령줄 인수를 가져올 수 있습니다. 매개 변수는 0부터 시작하는 명령줄 인수로 읽힙니다. C 및 C++와 달리, 프로그램의 이름이 ` args ` 배열의 첫 번째 명령줄 인수로 처리되지 않지만, [ GetCommandLineArgs() ](/ko-kr/dotnet/api/system.environment.getcommandlineargs#system-environment-getcommandlineargs) 메서드의 첫 번째 요소입니다. 

다음 목록에서는 가장 일반적인 ` Main ` 선언을 보여줍니다.

    
    
    static void Main() { }
    static int Main() { }
    static void Main(string[] args) { }
    static int Main(string[] args) { }
    static async Task Main() { }
    static async Task<int> Main() { }
    static async Task Main(string[] args) { }
    static async Task<int> Main(string[] args) { }
    

앞의 예제에서는 액세스 한정자를 지정하지 않으므로 기본적으로 암시적으로 ` private ` 입니다. 그것이 일반적이지만, 명시적 액세스
한정자를 지정할 수도 있습니다.

팁

` async ` 및 ` Task ` , ` Task<int> ` 반환 형식을 추가하면 콘솔 애플리케이션을 시작해야 하고 비동기 작업을 `
Main ` 에서 ` await ` 해야 하는 경우에 프로그램 코드가 간소화됩니다.

##  Main() 반환 값

다음 방법 중 하나로 메서드를 정의하여 ` Main ` 메서드에서 ` int ` 를 반환할 수 있습니다.

` Main ` 선언  |  ` Main ` 메서드 코드   
---|---  
` static int Main() ` |  ` args ` 또는 ` await ` 사용 안 함   
` static int Main(string[] args) ` |  ` args ` 사용, ` await ` 사용 안 함   
` static async Task<int> Main() ` |  ` args ` 사용 안 함 , ` await ` 사용   
` static async Task<int> Main(string[] args) ` |  ` args ` 및 ` await ` 사용   
  
` Main ` 의 반환 값을 사용하지 않는 경우 ` void ` 또는 ` Task ` 를 반환하면 코드가 다소 단순해집니다.

` Main ` 선언  |  ` Main ` 메서드 코드   
---|---  
` static void Main() ` |  ` args ` 또는 ` await ` 사용 안 함   
` static void Main(string[] args) ` |  ` args ` 사용, ` await ` 사용 안 함   
` static async Task Main() ` |  ` args ` 사용 안 함 , ` await ` 사용   
` static async Task Main(string[] args) ` |  ` args ` 및 ` await ` 사용   
  
그러나 ` int ` 또는 ` Task<int> ` 를 반환하면 프로그램이 실행 파일을 호출하는 다른 프로그램이나 스크립트에 상태 정보를
전달할 수 있습니다.

다음 예제에서는 프로세스의 종료 코드에 액세스할 수 있는 방법을 보여줍니다.

이 예제에서는 [ .NET Core ](../../../core/introduction) 명령줄 도구를 사용합니다. .NET Core 명령줄
도구에 대해 잘 모르는 경우 이 [ 시작 문서 ](../../../core/tutorials/with-visual-studio-code)
에서 알아볼 수 있습니다.

` dotnet new console ` 을 실행하여 새 애플리케이션을 만듭니다. _Program.cs_ 에서 ` Main ` 메서드를
다음과 같이 수정합니다.

    
    
    // Save this program as MainReturnValTest.cs.
    class MainReturnValTest
    {
        static int Main()
        {
            //...
            return 0;
        }
    }
    

Windows에서 프로그램을 실행하는 경우 ` Main ` 함수에서 반환된 값은 환경 변수에 저장됩니다. 이 환경 변수는 배치 파일에서 `
ERRORLEVEL ` 을 사용하거나 PowerShell에서 ` $LastExitCode ` 를 사용하여 검색할 수 있습니다.

[ dotnet CLI ](../../../core/tools/dotnet) ` dotnet build ` 명령을 사용하여 애플리케이션을
빌드할 수 있습니다.

다음으로 애플리케이션을 실행하고 결과를 표시하는 PowerShell 스크립트를 만듭니다. 다음 코드를 텍스트 파일에 붙여넣고 이 파일을
프로젝트가 포함된 폴더에 ` test.ps1 ` 로 저장합니다. PowerShell 프롬프트에 ` test.ps1 ` 을 입력하여
PowerShell 스크립트를 실행합니다.

코드에서 0을 반환하기 때문에 배치 파일이 성공했다고 보고합니다. 그러나 0이 아닌 값을 반환하도록 MainReturnValTest.cs를
변경한 다음 프로그램을 다시 컴파일하면 다음에 PowerShell 스크립트를 실행할 때 오류가 보고됩니다.

    
    
    dotnet run
    if ($LastExitCode -eq 0) {
        Write-Host "Execution succeeded"
    } else
    {
        Write-Host "Execution Failed"
    }
    Write-Host "Return value = " $LastExitCode
    
    
    
    Execution succeeded
    Return value = 0
    

###  비동기 Main 반환 값

` Main ` 에 대한 ` async ` 반환 값을 선언하면 컴파일러는 ` Main ` 에서 비동기 메서드를 호출하기 위한 상용구 코드를
생성합니다. ` async ` 키워드를 지정하지 않으면 다음 예와 같이 해당 코드를 직접 작성해야 합니다. 예의 코드는 비동기 작업이 완료될
때까지 프로그램이 실행되도록 보장합니다.

    
    
    class AsyncMainReturnValTest
    {
        public static int Main()
        {
            return AsyncConsoleWork().GetAwaiter().GetResult();
        }
    
        private static async Task<int> AsyncConsoleWork()
        {
            // Main body here
            return 0;
        }
    }
    

이 상용구 코드는 다음으로 바뀔 수 있습니다.

    
    
    class Program
    {
        static async Task<int> Main(string[] args)
        {
            return await AsyncConsoleWork();
        }
    
        private static async Task<int> AsyncConsoleWork()
        {
            // main body here 
            return 0;
        }
    }
    

` Main ` 을 ` async ` 로 선언하면 컴파일러가 항상 올바른 코드를 생성한다는 이점이 있습니다.

애플리케이션 진입점에서 ` Task ` 또는 ` Task<int> ` 를 반환하는 경우 컴파일러는 애플리케이션 코드에서 선언된 진입점
메서드를 호출하는 새 진입점을 생성합니다. 이 진입점이 ` $GeneratedMain ` 이라고 가정하면 컴파일러는 이러한 진입점에 대해
다음 코드를 생성합니다.

  * ` static Task Main() ` \- 컴파일러에서 ` private static void $GeneratedMain() => Main().GetAwaiter().GetResult(); ` 에 해당하는 코드를 내보냅니다. 
  * ` static Task Main(string[]) ` \- 컴파일러에서 ` private static void $GeneratedMain(string[] args) => Main(args).GetAwaiter().GetResult(); ` 에 해당하는 코드를 내보냅니다. 
  * ` static Task<int> Main() ` \- 컴파일러에서 ` private static int $GeneratedMain() => Main().GetAwaiter().GetResult(); ` 에 해당하는 코드를 내보냅니다. 
  * ` static Task<int> Main(string[]) ` \- 컴파일러에서 ` private static int $GeneratedMain(string[] args) => Main(args).GetAwaiter().GetResult(); ` 에 해당하는 코드를 내보냅니다. 

참고 항목

예제에서 ` Main ` 메서드에 ` async ` 한정자를 사용하더라도 컴파일러는 동일한 코드를 생성합니다.

##  명령줄 인수

다음 방법 중 하나로 메서드를 정의하여 인수를 ` Main ` 메서드에 보낼 수 있습니다.

` Main ` 선언  |  ` Main ` 메서드 코드   
---|---  
` static void Main(string[] args) ` |  반환 값 없음, ` await ` 사용 없음   
` static int Main(string[] args) ` |  반환 값, ` await ` 사용 없음   
` static async Task Main(string[] args) ` |  반환 값 없음, ` await ` 사용   
` static async Task<int> Main(string[] args) ` |  반환 값, ` await ` 사용   
  
인수가 사용되지 않는 경우 약간 더 간단한 코드를 위해 메서드 선언에서 ` args ` 를 생략할 수 있습니다.

` Main ` 선언  |  ` Main ` 메서드 코드   
---|---  
` static void Main() ` |  반환 값 없음, ` await ` 사용 없음   
` static int Main() ` |  반환 값, ` await ` 사용 없음   
` static async Task Main() ` |  반환 값 없음, ` await ` 사용   
` static async Task<int> Main() ` |  반환 값, ` await ` 사용   
  
` Main ` 메서드의 매개 변수는 명령줄 인수를 나타내는 [ String ](/ko-kr/dotnet/api/system.string)
배열입니다. 일반적으로 다음과 같이 ` Length ` 속성을 테스트하여 인수가 있는지 확인합니다.

    
    
    if (args.Length == 0)
    {
        System.Console.WriteLine("Please enter a numeric argument.");
        return 1;
    }
    

팁

` args ` 배열은 null일 수 없습니다. 따라서 null 검사 없이 ` Length ` 속성에 액세스하는 것이 안전합니다.

[ Convert ](/ko-kr/dotnet/api/system.convert) 클래스 또는 ` Parse ` 메서드를 사용하여 문자열
인수를 숫자 형식으로 변환할 수도 있습니다. 예를 들어 다음 문은 [ Parse ](/ko-
kr/dotnet/api/system.int64.parse) 메서드를 사용하여 ` string ` 을 ` long ` 숫자로 변환합니다.

    
    
    long num = Int64.Parse(args[0]);
    

` Int64 ` 의 별칭을 지정하는 C# 형식 ` long ` 을 사용할 수도 있습니다.

    
    
    long num = long.Parse(args[0]);
    

` Convert ` 클래스 메서드 ` ToInt64 ` 를 사용하여 같은 작업을 수행할 수도 있습니다.

    
    
    long num = Convert.ToInt64(s);
    

자세한 내용은 [ Parse ](/ko-kr/dotnet/api/system.int64.parse) 및 [ Convert ](/ko-
kr/dotnet/api/system.convert) 를 참조하세요.

다음 예제에서는 콘솔 애플리케이션에서 명령줄 인수를 사용하는 방법을 보여 줍니다. 애플리케이션은 런타임에 하나의 인수를 사용하고, 인수를
정수로 변환하고, 숫자의 계승을 계산합니다. 인수가 제공되지 않으면 애플리케이션에서는 프로그램의 올바른 사용법을 설명하는 메시지를
표시합니다.

명령 프롬프트에서 애플리케이션을 컴파일 및 실행하려면 다음 단계를 수행합니다.

  1. 다음 코드를 텍스트 편집기에 붙여넣고 이름 _Factorial.cs_ 를 사용하여 파일을 텍스트 파일로 저장합니다. 
    
        public class Functions
    {
        public static long Factorial(int n)
        {
            // Test for invalid input.
            if ((n < 0) || (n > 20))
            {
                return -1;
            }
    
            // Calculate the factorial iteratively rather than recursively.
            long tempResult = 1;
            for (int i = 1; i <= n; i++)
            {
                tempResult *= i;
            }
            return tempResult;
        }
    }
    
    class MainClass
    {
        static int Main(string[] args)
        {
            // Test if input arguments were supplied.
            if (args.Length == 0)
            {
                Console.WriteLine("Please enter a numeric argument.");
                Console.WriteLine("Usage: Factorial <num>");
                return 1;
            }
    
            // Try to convert the input arguments to numbers. This will throw
            // an exception if the argument is not a number.
            // num = int.Parse(args[0]);
            int num;
            bool test = int.TryParse(args[0], out num);
            if (!test)
            {
                Console.WriteLine("Please enter a numeric argument.");
                Console.WriteLine("Usage: Factorial <num>");
                return 1;
            }
    
            // Calculate factorial.
            long result = Functions.Factorial(num);
    
            // Print result.
            if (result == -1)
                Console.WriteLine("Input must be >= 0 and <= 20.");
            else
                Console.WriteLine($"The Factorial of {num} is {result}.");
    
            return 0;
        }
    }
    // If 3 is entered on command line, the
    // output reads: The factorial of 3 is 6.
    

  2. **시작** 화면이나 **시작** 메뉴에서 Visual Studio **개발자 명령 프롬프트** 창을 열고 만든 파일이 포함된 폴더로 이동합니다. 

  3. 다음 명령을 입력하여 애플리케이션을 컴파일합니다. 

` dotnet build `

애플리케이션에 컴파일 오류가 없으면 _Factorial.exe_ 라는 실행 파일이 만들어집니다.

  4. 다음 명령을 입력하여 3의 계승을 계산합니다. 

` dotnet run -- 3 `

  5. 이 명령은 다음 출력을 생성합니다. ` The factorial of 3 is 6. `

##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../../language-reference/language-specification/readme) 을
참조하세요. 언어 사양은 C# 구문 및 사용법에 대 한 신뢰할 수 있는 소스 됩니다.

##  참고 항목


-->

<!--






-->

<!--
#  최상위 문 - ` Main ` 메서드가 없는 프로그램

##  이 문서의 내용

콘솔 애플리케이션 프로젝트에 ` Main ` 메서드를 명시적으로 포함할 필요가 없습니다. 대신 _최상위 문_ 기능을 사용하여 작성해야 하는
코드를 최소화할 수 있습니다.

최상위 문을 사용하면 파일의 루트에 직접 실행 코드를 작성할 수 있으므로 클래스 또는 메서드에서 코드를 래핑할 필요가 없습니다. 따라서 `
Program ` 클래스 및 ` Main ` 메서드의 형식 없이 프로그램을 만들 수 있습니다. 이 경우 컴파일러는 애플리케이션에 대한 진입점
메서드를 사용하여 ` Program ` 클래스를 생성합니다. 생성된 메서드의 이름은 ` Main ` 이(가) 아니며, 코드에서 직접 참조할
수 없는 구현 세부 정보입니다.

다음은 C# 10의 완전한 C# 프로그램인 _Program.cs_ 파일입니다.

    
    
    Console.WriteLine("Hello World!");
    

최상위 문을 사용하면 Azure Functions 및 GitHub Actions와 같은 소규모 유틸리티에 대한 간단한 프로그램을 작성할 수
있습니다. 또한 새로운 C# 프로그래머가 코드를 학습하고 작성하는 작업을 더 쉽게 수행할 수 있습니다.

다음 섹션에서는 최상위 문으로 수행할 수 있는 작업과 수행할 수 없는 작업에 대한 규칙을 설명합니다.

##  하나의 최상위 파일만

애플리케이션에는 진입점이 하나만 있어야 합니다. 프로젝트에는 최상위 문이 있는 파일이 하나만 있을 수 있습니다. 프로젝트의 두 개 이상의
파일에 최상위 문을 넣으면 다음과 같은 컴파일러 오류가 발생합니다.

> CS8802 하나의 컴파일 단위만 최상위 문을 포함할 수 있습니다.

프로젝트에는 최상위 문이 없는 추가 소스 코드 파일이 얼마든지 있을 수 있습니다.

##  다른 진입점 없음

` Main ` 메서드를 명시적으로 작성할 수 있지만 진입점으로 작동할 수는 없습니다. 컴파일러에서 다음과 같은 경고가 발생합니다.

> CS7022 프로그램의 진입점은 전역 코드이며 'Main()' 진입점은 무시됩니다.

최상위 문이 있는 프로젝트에서는 프로젝트에 하나 이상의 ` Main ` 메서드가 있는 경우에도 [ -main ](../../language-
reference/compiler-options/advanced#mainentrypoint-or-startupobject) 컴파일러 옵션을
사용하여 진입점을 선택할 수 없습니다.

##  ` using ` 지시문

지시문을 포함하는 ` using ` 경우 다음 예제와 같이 파일에서 먼저 와야 합니다.

    
    
    using System.Text;
    
    StringBuilder builder = new();
    builder.AppendLine("The following arguments are passed:");
    
    // Display the command line arguments using the args variable.
    foreach (var arg in args)
    {
        builder.AppendLine($"Argument={arg}");
    }
    
    Console.WriteLine(builder.ToString());
    
    // Return a success code.
    return 0;
    

##  전역 네임스페이스

최상위 문은 전역 네임스페이스에서 암시적으로 사용할 수 있습니다.

##  네임스페이스 및 형식 정의

최상위 문이 있는 파일에는 네임스페이스 및 형식 정의도 포함될 수 있지만 최상위 문 뒤에 와야 합니다. 예시:

    
    
    MyClass.TestMethod();
    MyNamespace.MyClass.MyMethod();
    
    public class MyClass
    {
        public static void TestMethod()
        {
            Console.WriteLine("Hello World!");
        }
    }
    
    namespace MyNamespace
    {
        class MyClass
        {
            public static void MyMethod()
            {
                Console.WriteLine("Hello World from MyNamespace.MyClass.MyMethod!");
            }
        }
    }
    

##  ` args `

최상위 문은 ` args ` 변수를 참조하여 입력된 명령줄 인수에 액세스할 수 있습니다. ` args ` 변수는 null이 아니지만 명령줄
인수가 제공되지 않은 경우 ` Length ` 는 0입니다. 예시:

    
    
    if (args.Length > 0)
    {
        foreach (var arg in args)
        {
            Console.WriteLine($"Argument={arg}");
        }
    }
    else
    {
        Console.WriteLine("No arguments");
    }
    

##  ` await `

` await ` 를 사용하여 비동기 메서드를 호출할 수 있습니다. 예시:

    
    
    Console.Write("Hello ");
    await Task.Delay(5000);
    Console.WriteLine("World!");
    

##  프로세스의 종료 코드

애플리케이션 종료될 때 ` int ` 값을 반환하려면 ` int ` 를 반환하는 ` Main ` 메서드에서와 같이 ` return ` 문을
사용합니다. 예시:

    
    
    string? s = Console.ReadLine();
    
    int returnValue = int.Parse(s ?? "-1");
    return returnValue;
    

##  암시적 진입점 메서드

컴파일러는 최상위 문이 있는 프로젝트의 프로그램 진입점 역할을 하는 메서드를 생성합니다. 메서드의 서명은 최상위 문에 ` await `
키워드 또는 ` return ` 문이 포함되어 있는지 여부에 따라 달라집니다. 다음 표에서는 편의를 위해 표에 있는 메서드 이름 ` Main
` 을 사용하여 메서드 서명이 어떻게 표시되는지 보여줍니다.

최상위 코드에는 다음이 포함됩니다.  |  암시적 ` Main ` 서명   
---|---  
` await ` 및 ` return ` |  ` static async Task<int> Main(string[] args) `  
` await ` |  ` static async Task Main(string[] args) `  
` return ` |  ` static int Main(string[] args) `  
` await ` 또는 ` return ` 없음  |  ` static void Main(string[] args) `  
  
##  C# 언어 사양

자세한 내용은 [ C# 언어 사양 ](../../language-reference/language-specification/readme) 을
참조하세요. 언어 사양은 C# 구문 및 사용법에 대 한 신뢰할 수 있는 소스 됩니다.

[ 기능 사양 - 최상위 문 ](../../language-reference/proposals/csharp-9.0/top-level-
statements)


-->

<!--






-->

