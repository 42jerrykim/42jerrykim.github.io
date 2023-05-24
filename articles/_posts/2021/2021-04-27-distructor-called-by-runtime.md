---
title: "[C#] Runtime에 따른 Finalizer 호출 차이"
categories:
  - .NET
tags:
  - CSharp
  - Distructor
  - Class
  - GC
  - Memory
  - .NET
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

대부분의 개발자는 자기의 경험이나 생각에 따라서 코드를 작성 하는 경우가 많다. 하나의 예시로는 C++개발에 익숙한 개발자들이 C#으로 개발을 시작할때 Class Finalizer에서 자원을 관리 하는 경우이다.

# Sample code

아래의 코드는 MyClass내에서 자원을 Create하고 Delete하는 간단한 예제에 GC.WaitForPendingFinalizers()를 추가하여 자원을 개발자가 컨트롤 한다.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp8
{
    class Program
    {
        static void Main(string[] args)
        {
            MyClass a = new MyClass();

            a = null;

            Console.WriteLine("1");
            GC.Collect();
            Console.WriteLine("2");
            GC.WaitForPendingFinalizers();
            Console.WriteLine("3");
        }
    }
    internal class MyClass
    {
        public MyClass()
        {
            Console.WriteLine("Create");
        }

        ~MyClass()
        {
            Console.WriteLine("Delete");
        }
    }
}

```

# 결과

## .NET Core에서 동작 한 결과

```bash
Create
1
2
Delete
3
```

## .NET Framework에서 동작한 결과

```bash
Create
1
2
3
```

# 결론

[종료자를 사용하여 리소스 해제](https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/finalizers#using-finalizers-to-release-resources)하는 방법은 개체를 종료할 수 있으면 가비지 수집기에서 개체의 Finalize 메서드를 실행하므로 런타임의 상황이나 구현에 따라서 달라질수 있다. 비록 함수의 이름은 GC.WaitForPendingFinalizers()이지만 이름과는 다르게 동작할 수 있다는 것을 주의 해야한다. 함수의 자원을 관리하는 더 적합한 방법은 [IDisposable](https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/finalizers#explicit-release-of-resources)을 사용하는 방법이다.